"""
Agent Runtime.

SAGE_BLUEPRINT.md Section 18-19: the central intelligence layer. Converts a
user's message into a response by running it through, in order:

    Intent Analyzer -> Planner -> Execution Manager -> Context Builder
    -> Memory Manager (read) -> Conversation Manager -> Provider Interface
    -> Response Validator -> Response Formatter

The LLM is a dependency of this runtime, not the runtime itself (Section
18.1) — swapping providers or adding tools never requires changes here.
"""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.context.context_manager import ContextBuilder
from app.agent.execution.tool_executor import ExecutionManager
from app.agent.planner.planner import Planner
from app.agent.runtime.intent_analyzer import IntentAnalyzer
from app.agent.runtime.response_formatter import AgentResponse, ReasoningTrace, ResponseFormatter
from app.agent.runtime.response_validator import ResponseValidator
from app.core.exceptions import ProviderException
from app.logging.logger import get_logger
from app.memory.memory_manager import MemoryManager, memory_manager as default_memory_manager
from app.providers.base import BaseProvider
from app.providers.factory import get_provider
from app.services.conversation_service import ConversationService
from app.services.user_service import UserService
from app.tools.registry import ToolRegistry, tool_registry as default_tool_registry

logger = get_logger(__name__)


class AgentRuntime:
    def __init__(
        self,
        tool_registry: ToolRegistry | None = None,
        memory_manager: MemoryManager | None = None,
        provider: BaseProvider | None = None,
    ):
        registry = tool_registry or default_tool_registry
        self.tool_registry = registry
        self.memory_manager = memory_manager or default_memory_manager
        self.provider = provider  # if None, resolved per-call from settings

        self.intent_analyzer = IntentAnalyzer()
        self.planner = Planner(registry)
        self.execution_manager = ExecutionManager(registry)
        self.context_builder = ContextBuilder()
        self.response_validator = ResponseValidator()
        self.response_formatter = ResponseFormatter()

    async def handle_message(
        self,
        session: AsyncSession,
        message: str,
        conversation_id: UUID | None = None,
        provider_name: str | None = None,
        debug: bool = False,
    ) -> AgentResponse:
        user_service = UserService(session)
        conversation_service = ConversationService(session)

        user = await user_service.get_or_create_default_user()
        conversation = await conversation_service.get_or_create(conversation_id, user.id)

        await conversation_service.add_message(conversation.id, role="user", content=message)

        analysis = self.intent_analyzer.analyze(message)
        plan = self.planner.build_plan(analysis)
        execution_result = await self.execution_manager.execute(plan, session, conversation.id)

        relevant_memories = await self.memory_manager.retrieve_relevant(message)
        recent_history = await conversation_service.get_recent_history(conversation.id, limit=20)
        # Exclude the user message we just persisted — it's passed separately
        # as the current turn (Context Builder's highest-priority slot).
        recent_history = recent_history[:-1] if recent_history else recent_history

        provider_messages = self.context_builder.build(
            user_message=message,
            tool_outputs=execution_result.tool_outputs,
            relevant_memories=relevant_memories,
            recent_messages=recent_history,
            unavailable_capabilities=execution_result.unavailable_capabilities,
        )

        provider = self.provider or get_provider(provider_name)

        try:
            provider_response = await provider.generate(provider_messages)
        except ProviderException:
            logger.exception("Provider call failed")
            raise

        validation = self.response_validator.validate(
            provider_response, execution_result.unavailable_capabilities
        )
        if not validation.is_valid:
            raise ProviderException("Provider returned an unusable response.")

        await conversation_service.add_message(
            conversation.id,
            role="assistant",
            content=provider_response.content,
            metadata={
                "provider": provider_response.provider_name,
                "model": provider_response.model,
                "tools_used": execution_result.tools_used,
            },
        )
        await session.commit()

        trace = ReasoningTrace(
            intents=[i.value for i in analysis.intents],
            tools_used=execution_result.tools_used,
            unavailable_capabilities=execution_result.unavailable_capabilities,
            warnings=validation.warnings,
            provider=provider_response.provider_name,
            model=provider_response.model,
        )

        return self.response_formatter.format(
            content=provider_response.content,
            conversation_id=conversation.id,
            tools_used=execution_result.tools_used,
            trace=trace,
            include_trace=debug,
        )
