# SAGE_BLUEPRINT.md

Version: 1.0
Status: Frozen Architecture
Project Codename: Sage

---

# 1. Introduction

## 1.1 Purpose

Sage is a privacy-first, AI-powered personal assistant designed to function as a long-term digital companion for a single user. Unlike a traditional chatbot, Sage is an intelligent agent capable of planning, remembering, researching, organizing information, and executing tasks through specialized tools.

The goal of Sage is not to replace human judgment but to augment it by providing reliable assistance, structured memory, transparent reasoning, and modular capabilities.

Version 1 targets a single-user, self-hosted deployment running locally on the user's computer. The architecture must remain extensible so that future versions can support additional interfaces, deployment targets, and capabilities without requiring major redesign.

---

## 1.2 Product Philosophy

Every design decision within Sage must follow these principles.

### Privacy First

The user owns all data.

No analytics, telemetry, hidden tracking, or undisclosed data collection shall exist.

All persistent data shall remain within the user's configured storage unless explicitly transmitted to an external service chosen by the user (e.g., an LLM provider or search API).

---

### Transparency

Sage must never silently perform important actions.

Whenever Sage:

- searches the web,
- updates memory,
- creates reminders,
- modifies notes,
- edits tasks,
- processes files,
- invokes external APIs,

the user should understand what happened.

---

### Reliability

Correctness is preferred over speed.

If Sage is uncertain, it must communicate uncertainty rather than fabricate confidence.

---

### Modularity

Every subsystem shall be replaceable.

Examples include:

- LLM provider
- Search provider
- Database engine
- Reminder scheduler
- File parser

Replacing one subsystem should require minimal or no changes to the rest of the application.

---

### Simplicity

Complexity must exist internally—not in the user experience.

The interface should remain simple even as internal capabilities grow.

---

## 1.3 Vision

Sage should become the user's private AI operating system.

Rather than merely answering questions, Sage should help the user:

- think,
- remember,
- organize,
- research,
- plan,
- write,
- learn,
- and complete work.

The interaction should feel natural while remaining predictable and transparent.

---

# 2. Project Goals

The primary goals are:

- Build a production-quality AI application.
- Follow clean architecture principles.
- Maintain long-term memory.
- Support multi-step planning.
- Automatically select and execute tools.
- Keep all user data under user control.
- Provide a modern ChatGPT-like interface.
- Remain easy to extend.
- Support multiple AI providers.
- Be suitable as a long-term personal productivity platform.

---

# 3. Project Scope

## Included in Version 1

### AI Agent

- Natural conversations
- Multi-step planning
- Automatic tool selection
- Context management
- Streaming responses

---

### Long-Term Memory

Support persistent storage of:

- User preferences
- Goals
- Projects
- Important facts
- Important events
- Personal notes

Memory must survive application restarts.

---

### Conversation Management

- Conversation history
- Conversation summaries
- Session management
- Recall previous discussions

Example:

"What did we discuss last week?"

---

### Productivity

- Notes
- Tasks
- Priorities
- Deadlines
- Internal reminders

---

### Research

- Tavily web search
- Source citations
- Summaries
- Distinguish facts from opinions

---

### Document Understanding

Supported formats:

- PDF
- DOCX
- TXT
- CSV
- XLSX
- Images

---

### Writing Assistance

Version 1 supports:

- Professional email drafting

Future versions may support direct sending.

---

### Scam Detection

Analyze:

- URLs
- Emails
- Job offers
- Messages

Return:

- Risk level
- Confidence estimate
- Warning signs
- Recommended action

---

### Daily Briefing

Generate a summary including:

- Today's tasks
- Upcoming reminders
- Deadlines
- Suggested priorities

---

### Logging

Maintain internal logs for:

- Tool usage
- Search requests
- Memory updates
- Reminder creation
- System errors

---

## Excluded from Version 1

The following features are intentionally excluded:

- Voice interaction
- Mobile application
- Multi-user support
- Authentication system
- Cloud synchronization
- Browser extension
- Automatic email sending
- Autonomous internet browsing
- Social media integrations

These may be considered in future releases.

---

# 4. Core Design Principles

Every module within Sage must satisfy the following architectural principles.

## Single Responsibility

Every module should have one clear responsibility.

Examples:

MemoryService

Stores and retrieves memory.

ReminderService

Schedules reminders.

Planner

Creates execution plans.

SearchTool

Searches the web.

Each module should remain independent.

---

## Separation of Concerns

The architecture shall be divided into distinct layers.

Frontend

↓

Backend API

↓

AI Agent

↓

Tool Manager

↓

Individual Tools

↓

Database

No layer should bypass another without explicit justification.

---

## Extensibility

Adding a new tool should require:

- implementing the tool,
- registering it,
- writing tests.

No major architectural modifications should be necessary.

---

## Testability

Every major component shall be independently testable.

Dependency injection should be preferred where appropriate.

Business logic should not depend directly on UI frameworks.

---

## Maintainability

Code should prioritize readability.

Avoid premature optimization.

Follow SOLID principles where applicable.

---

## Error Recovery

Failures in one module should not terminate the application.

Whenever possible:

- report the error,
- log it,
- continue operating.

Graceful degradation is preferred over crashes.

---

# 5. Success Criteria

Version 1 is considered complete when:

✓ Sage supports natural conversations.

✓ Sage remembers important information.

✓ Sage performs multi-step planning.

✓ Sage automatically invokes tools.

✓ Notes function correctly.

✓ Tasks function correctly.

✓ Reminders function correctly.

✓ Web search includes citations.

✓ Email drafting is production quality.

✓ Scam detection produces transparent analyses.

✓ File understanding supports all required formats.

✓ Docker deployment works on a clean machine.

✓ All critical modules are covered by automated tests.

✓ Documentation enables another developer to set up the project without additional explanation.

---

End of Part 1.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 2 — System Architecture & Technology Stack
# =============================================================================

# 6. High-Level System Architecture

## 6.1 Architectural Philosophy

Sage follows a layered Clean Architecture.

The user interface must never contain business logic.

The AI Agent must never directly communicate with the database.

Every external capability must be exposed through tools.

Every module has exactly one responsibility.

The architecture must remain modular so that any subsystem can be replaced with minimal code changes.

---

## 6.2 High-Level Architecture

                            User
                              │
                              ▼
                 React Frontend (UI)
                              │
                    REST API / WebSocket
                              │
                              ▼
                   FastAPI Backend Server
                              │
                Request / Response Layer
                              │
                              ▼
                    AI Agent Orchestrator
                              │
        ┌─────────────────────┼──────────────────────┐
        │                     │                      │
        ▼                     ▼                      ▼
     Planner           Memory Manager        Conversation Manager
        │                     │                      │
        └──────────────┬──────┴──────────────┬───────┘
                       │                     │
                       ▼                     ▼
                 Tool Execution Engine   PostgreSQL
                       │
     ┌─────────────────┼───────────────────────────────┐
     │                 │                │              │
     ▼                 ▼                ▼              ▼
 Search Tool     Reminder Tool    Notes Tool    Task Tool
     │                 │                │              │
     ▼                 ▼                ▼              ▼
 Tavily          APScheduler       PostgreSQL    PostgreSQL

Additional tools:

- Scam Detection
- Email Drafting
- File Processing
- Daily Briefing

All tools must follow the same interface.

---

# 7. Technology Stack

The following technologies are frozen for Version 1.

## Backend

Language

Python 3.12+

Framework

FastAPI

Reasons

• Excellent async support
• High performance
• Automatic OpenAPI generation
• Mature ecosystem
• Easy testing

No other backend framework shall be used.

---

## Frontend

Framework

React

Language

TypeScript

Reasons

• Large ecosystem

• Component architecture

• Easy future expansion

• Excellent developer tooling

---

Styling

TailwindCSS

Reasons

• Utility-first

• Fast development

• Easy maintenance

---

UI Components

shadcn/ui

Reasons

• Modern

• Accessible

• Professional appearance

• Easy customization

---

Icons

Lucide React

---

Markdown Rendering

react-markdown

Syntax Highlighting

rehype-highlight

---

Animations

Framer Motion

Animations must remain subtle.

Avoid unnecessary visual effects.

---

# 8. AI Provider Layer

Sage must support multiple providers.

Version 1 officially supports

- Google Gemini
- OpenAI
- Anthropic Claude
- OpenRouter

The AI Agent must never directly depend on a specific provider.

Instead:

Provider Interface

↓

Gemini Adapter

Claude Adapter

OpenAI Adapter

OpenRouter Adapter

The Planner communicates only with the Provider Interface.

This allows changing providers through configuration.

No business logic should depend on the provider.

---

# 9. Search Provider

Version 1

Tavily

Reasons

• Designed for LLM workflows

• Reliable citations

• Good search quality

Future providers may include

- Brave Search
- SerpAPI
- DuckDuckGo

Provider abstraction must be implemented.

---

# 10. Database

Version 1

PostgreSQL

Reasons

• Mature

• Reliable

• ACID compliance

• JSON support

• Excellent indexing

• Future scalability

SQLite shall not be used as the primary database.

---

ORM

SQLAlchemy 2.x

Migration Tool

Alembic

---

# 11. Scheduler

Version 1

APScheduler

Reasons

• Reliable

• Lightweight

• Cron support

• Interval support

• Date-based scheduling

Scheduler must survive application restarts.

Reminder metadata must persist inside PostgreSQL.

---

# 12. Docker

Version 1 uses

Docker

Docker Compose

Containers

frontend

backend

postgres

optional redis

Redis remains optional.

The system must function without Redis.

---

# 13. Logging

Python Logging Module

Structured logs

Log Levels

DEBUG

INFO

WARNING

ERROR

CRITICAL

Logs should be written to

logs/

Daily rotation should be enabled.

---

# 14. Configuration

Environment Variables

Stored inside

.env

Never hardcode

API Keys

Passwords

Database URLs

Secrets

The repository shall include

.env.example

Only placeholders.

Never real credentials.

---

# 15. Folder Structure

The following structure is frozen.

sage/

│

├── backend/

│   ├── app/

│   │

│   ├── api/

│   ├── core/

│   ├── config/

│   ├── database/

│   ├── models/

│   ├── schemas/

│   ├── services/

│   ├── repositories/

│   ├── memory/

│   ├── planner/

│   ├── execution/

│   ├── tools/

│   │

│   │   ├── search/

│   │   ├── reminders/

│   │   ├── notes/

│   │   ├── tasks/

│   │   ├── email/

│   │   ├── scam/

│   │   ├── files/

│   │   └── daily_briefing/

│   │

│   ├── providers/

│   ├── middleware/

│   ├── utils/

│   ├── logging/

│   ├── tests/

│   └── main.py

│

├── frontend/

│   ├── src/

│   ├── public/

│   ├── components/

│   ├── pages/

│   ├── hooks/

│   ├── services/

│   ├── contexts/

│   ├── types/

│   ├── utils/

│   └── styles/

│

├── docs/

├── docker/

├── scripts/

├── backups/

├── logs/

├── docker-compose.yml

├── Dockerfile

├── README.md

└── .env.example

This structure shall not be changed unless there is a compelling architectural reason.

---

# 16. Module Communication Rules

The following communication rules are mandatory.

Frontend

↓

FastAPI API

↓

AI Agent

↓

Planner

↓

Execution Engine

↓

Tools

↓

Database

Forbidden:

Frontend → Database

Planner → PostgreSQL

Tools → UI

Repositories → React

Business logic → Components

Every dependency must point downward.

No circular dependencies are allowed.

---

# 17. Architectural Constraints

The following constraints are mandatory.

1.

No module may exceed its responsibility.

2.

Business logic must never exist inside React components.

3.

Database queries belong only inside repositories.

4.

Provider-specific code belongs only inside provider adapters.

5.

Tool implementations must remain independent.

6.

The Planner must never directly call PostgreSQL.

7.

The Execution Engine is responsible for invoking tools.

8.

The Memory Manager owns all memory operations.

9.

Conversation history is not memory.

10.

Memory is never updated silently unless explicitly instructed by the user.

---

End of Part 2.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 3 — AI Agent Runtime
# =============================================================================

# 18. AI Agent Runtime

## 18.1 Purpose

The AI Agent Runtime is the central intelligence layer of Sage.

It is responsible for converting a user's request into one or more executable actions, gathering the required information, coordinating tool execution, constructing the final context, invoking the configured LLM provider, validating the response, and returning a transparent, high-quality answer.

The AI Agent Runtime is the heart of Sage.

The LLM is considered a dependency of the runtime, not the runtime itself.

---

# 19. Runtime Components

The runtime consists of the following components.

User

↓

Intent Analyzer

↓

Planner

↓

Execution Manager

↓

Context Builder

↓

Memory Manager

↓

Conversation Manager

↓

Tool Registry

↓

Tool Execution

↓

Provider Interface

↓

Response Validator

↓

Response Formatter

↓

Frontend

Every component has one clearly defined responsibility.

---

# 20. Intent Analyzer

## Purpose

Determine what the user is trying to accomplish.

The Intent Analyzer should classify requests into one or more categories.

Examples

• Conversation

• Question Answering

• Planning

• Web Search

• Note Management

• Task Management

• Reminder Management

• Memory Operations

• Email Drafting

• Scam Detection

• File Analysis

Multiple intents may exist within the same message.

Example

"Search for GATE scholarships, save the important ones as notes and remind me tomorrow."

Detected intents:

✓ Search

✓ Notes

✓ Reminder

The Intent Analyzer shall not execute any actions.

Its only responsibility is intent classification.

---

# 21. Planner

## Purpose

The Planner converts user intent into an execution plan.

The Planner decides:

- what needs to happen
- which tools are required
- execution order
- whether execution can occur in parallel

The Planner never executes tools.

Example

User:

"Find three Python internships and remember my favorite."

Execution Plan

1. Search internships
2. Summarize results
3. Ask user which is preferred
4. Store preference in memory

---

## Planner Responsibilities

The Planner shall:

✓ Build multi-step plans

✓ Detect dependencies

✓ Avoid unnecessary tool usage

✓ Minimize API calls

✓ Reduce execution time

✓ Respect execution policies

---

## Planner Constraints

The Planner must never:

- access PostgreSQL directly
- call APIs directly
- modify memory
- create reminders
- execute tools

Those responsibilities belong to other components.

---

# 22. Execution Manager

## Purpose

Execute the plan created by the Planner.

Responsibilities

• Execute tools

• Handle retries

• Handle failures

• Manage execution order

• Manage parallel execution

• Return execution results

The Execution Manager is the only component allowed to invoke tools.

---

## Execution Policies

Policy 1

Independent tools should execute in parallel.

Example

Search

+

Memory Retrieval

Policy 2

Dependent tools execute sequentially.

Example

Search

↓

Summarize

↓

Store Memory

Policy 3

Critical failures terminate execution.

Policy 4

Non-critical failures should be reported while continuing remaining work.

Policy 5

Every tool execution must generate an execution log.

---

# 23. Context Builder

Purpose

Construct the final prompt sent to the configured LLM.

The Context Builder gathers:

• User message

• Relevant conversation history

• Relevant long-term memory

• Tool outputs

• Retrieved documents

• Search summaries

• System instructions

The Context Builder should include only information relevant to the current task.

Avoid unnecessary token usage.

---

## Context Priority

Highest

Current User Message

↓

Tool Results

↓

Relevant Memory

↓

Recent Conversation

↓

Conversation Summary

↓

Older Context

The builder should automatically discard irrelevant information.

---

# 24. Conversation Manager

Purpose

Manage active conversations.

Responsibilities

Maintain:

• Conversation IDs

• Session metadata

• Conversation history

• Conversation summaries

Conversation history is temporary.

Conversation summaries are persistent.

Conversation history is NOT long-term memory.

---

# 25. Memory Manager

Purpose

Manage long-term memory.

The Memory Manager owns every memory operation.

No other module may directly update memory.

Responsibilities

• Store memory

• Retrieve memory

• Update memory

• Delete memory

• Search memory

• Export memory

• Import memory

Memory updates require confirmation unless the user explicitly issues a memory command.

Examples

"Remember that I am preparing for GATE."

No confirmation required.

"I am preparing for GATE."

Confirmation required.

---

# 26. Tool Registry

Purpose

Provide a centralized registry of all available tools.

The Planner never references concrete tool implementations.

Instead

Planner

↓

Tool Registry

↓

Tool

Adding a new tool requires only:

1. Implement the tool.
2. Register the tool.
3. Write tests.

No Planner modifications should be necessary.

---

# 27. Provider Interface

Purpose

Provide a unified abstraction over all supported LLM providers.

Supported providers

✓ Gemini

✓ OpenAI

✓ Claude

✓ OpenRouter

Future providers can be added without modifying business logic.

The rest of Sage communicates only with the Provider Interface.

Never with provider SDKs directly.

---

# 28. Response Validator

Purpose

Perform validation before the response reaches the user.

Validation includes:

✓ Empty responses

✓ Tool failures

✓ Missing citations

✓ Invalid markdown

✓ Hallucination indicators (where detectable)

✓ Required disclaimers

The validator should improve reliability but must not fabricate content.

---

# 29. Response Formatter

Purpose

Convert validated output into frontend-ready content.

Responsibilities

• Markdown formatting

• Code block formatting

• Citation rendering

• Tables

• Lists

• Tool activity summaries

The formatter must remain presentation-only.

No business logic belongs here.

---

# 30. Internal Reasoning Trace

The runtime maintains a structured execution record.

This is NOT chain-of-thought.

It records system actions only.

Example

Goal:
Find internship opportunities.

Plan:
1. Search web
2. Filter results
3. Summarize

Tools Used:
- Tavily Search

Execution Time:
2.4 seconds

Result:
Success

This trace is intended for debugging, logging, and future analytics.

It is not displayed to the user unless a dedicated debug mode is enabled.

---

# 31. Runtime Acceptance Criteria

The AI Agent Runtime is considered complete when:

✓ Multi-step plans execute correctly.

✓ Tool selection is automatic.

✓ Parallel execution works.

✓ Provider switching requires no business logic changes.

✓ Context is assembled dynamically.

✓ Memory is managed exclusively by the Memory Manager.

✓ Every tool execution is logged.

✓ Responses are validated before display.

✓ New tools can be added without modifying the Planner.

---

End of Part 3.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 4 — Long-Term Memory Architecture
# =============================================================================


# 32. Long-Term Memory System


## 32.1 Purpose

The Long-Term Memory System allows Sage to remember important information about the user across conversations and application restarts.

The purpose of memory is not to store everything.

The purpose is to preserve information that improves future assistance.

Memory must be:

- Useful
- Controlled
- Transparent
- Editable
- Deletable
- Private


---

# 33. Memory Philosophy


## 33.1 Store Value, Not Volume

Sage must not become a database of every conversation.

The system must avoid storing:

- casual conversations
- temporary questions
- random messages
- unnecessary details


Example:

User:

"What is Python?"

DO NOT store.

---

User:

"I am learning Python for backend development."

Potential memory:

User is learning Python for backend development.


---

# 33.2 User Control Principle

The user always owns memory.

The user can:

- view memories
- create memories
- update memories
- delete memories
- export memories


No memory should become impossible to remove.


---

# 34. Memory Categories


Sage supports the following memory categories.


## 34.1 User Preferences


Information about how the user prefers Sage to behave.


Examples:

- Preferred response style
- Preferred programming language
- Learning preferences
- Communication preferences


Example:

"I prefer detailed explanations."

Stored as:

Category:
Preference

Content:
User prefers detailed explanations.


---

## 34.2 Goals


Long-term objectives.


Examples:

- Career goals
- Learning goals
- Personal projects


Example:

"I want to become a backend developer."


---

## 34.3 Important Facts


Stable factual information.


Examples:

- User's skills
- User's projects
- User's interests


Example:

"User is building Sage AI assistant."


---

## 34.4 Important Events


Meaningful events that may affect future conversations.


Examples:

- Completed internship
- Started project
- Important deadline


---

## 34.5 Personal Notes


User-created memories.

Example:

"Remember my project deadline is December."


---

# 35. Memory Creation Rules


## 35.1 Explicit Memory Command


If the user says:

"Remember that I am preparing for GATE."

Sage immediately creates memory.

No confirmation required.


Supported commands:

Remember...

Save this...

Keep this in mind...


---

## 35.2 Automatic Memory Detection


If Sage detects potentially useful information:

Example:

"I am preparing for GATE."

Sage should ask:


"Would you like me to remember that?"


Only after confirmation:

Store memory.


---

# 36. Memory Commands


Sage supports natural language commands.


## Remember


Examples:

"Remember that I prefer Java."

"Remember my project name."


Action:

Create memory.


---

## Forget


Examples:

"Forget that I am learning Java."

"Delete my internship goal."


Action:

Remove matching memory.


---

## Update


Examples:

"Update my goal from frontend development to full stack development."


Action:

Modify existing memory.


---

## Recall


Examples:

"What do you know about me?"

"What memories do you have?"

"What have you remembered about my goals?"


Action:

Display stored memories.


---

# 37. Memory Architecture


The Memory System consists of:


```
User

↓

Memory Request

↓

Memory Manager

↓

Memory Classifier

↓

Memory Storage

↓

PostgreSQL


```


---

# 38. Memory Manager


## Responsibility

The Memory Manager is the only component allowed to modify memory.


Other modules:

Planner

Tools

Conversation Manager

LLM Provider


cannot directly access memory storage.


---

## Responsibilities


The Memory Manager handles:


Create memory

Retrieve memory

Search memory

Update memory

Delete memory

Summarize memory

Export memory



---

# 39. Memory Classification


Before storing memory, Sage classifies it.


Classification pipeline:


```
User Information

↓

Memory Classifier

↓

Category Detection

↓

Importance Score

↓

Storage Decision

↓

Database

```


---

# 40. Importance Scoring


Every memory receives an importance score.


Range:

0-100


Example:


"I like dark mode."

Importance:
40


"I want to become a software engineer."

Importance:
90


"I have an exam tomorrow."

Importance:
70


Low importance memories should eventually expire or be removed.


---

# 41. Memory Retrieval


Sage should not load all memories every conversation.


Instead:


```
User Query

↓

Memory Search

↓

Relevant Memories

↓

Context Builder

↓

LLM

```


Only relevant memories should enter the context.


---

# 42. Memory Search


Version 1 supports:


Keyword search

+

Semantic search


Future:

Vector embeddings


Possible implementation:

PostgreSQL + pgvector


---

# 43. Memory Conflict Handling


Example:


Old memory:

User prefers Python.


New memory:

User prefers Java.


Sage should not silently overwrite.


Process:


Detect conflict

↓

Notify user

↓

Ask clarification

↓

Update memory


---

# 44. Memory Privacy Rules


Mandatory:


1.

Never expose memory to another user.


2.

Never send full memory database to external providers.


3.

Only send relevant memories during AI requests.


4.

Allow complete deletion.


5.

Allow export.


---

# 45. Memory Export


User command:


"Export my memories."


Supported formats:


JSON

CSV


Example:


```json
{
 "category":"goal",
 "content":"Become backend developer",
 "created":"2026-07-12"
}
```


---

# 46. Memory Backup


Memory data should be included in database backups.


Backup frequency:


Configurable.


Recommended:


Daily local backup.


---

# 47. Memory Acceptance Criteria


Memory System is complete when:


✓ User can create memories.

✓ User can delete memories.

✓ User can update memories.

✓ User can view stored memories.

✓ Memories survive restart.

✓ Automatic memory asks permission.

✓ Explicit memory commands work immediately.

✓ Relevant memories are retrieved automatically.

✓ Memory conflicts are handled safely.

✓ Export works.

✓ No unnecessary conversations are stored.



End of Part 4.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 5 — Tool System Architecture
# =============================================================================


# 48. Tool System Overview


## 48.1 Purpose

The Tool System allows Sage to interact with external capabilities and perform actions beyond generating text.

Examples:

- Searching the internet
- Creating notes
- Managing tasks
- Scheduling reminders
- Analyzing files
- Detecting scams
- Preparing emails


The AI Agent must never directly implement these capabilities.

Instead:

```
User Request

↓

Planner

↓

Capability Request

↓

Tool Registry

↓

Tool Selection

↓

Execution Manager

↓

Tool Execution

↓

Result

↓

AI Response
```


---

# 49. Tool Design Principles


Every tool must follow these principles.


## 49.1 Independent Modules

Each tool must exist independently.

Example:

Search Tool

does not know:

- Notes Tool
- Reminder Tool
- Database structure of other modules


---

## 49.2 Common Interface

Every tool must implement the same base interface.


Example:

```python
class BaseTool:

    name

    description

    capabilities

    input_schema

    output_schema

    execute()
```


---

## 49.3 Capability-Based Discovery


Tools are discovered through capability declarations.


The Planner does not ask:


"Use Tavily."


Instead:


"I need web_search capability."


The Tool Registry decides which tool satisfies that capability.


---

# 50. Capability Manifest


Each tool must provide a manifest.


Example:


```yaml
tool:
  name: web_search

description:
  Search the internet and return verified sources.

capabilities:
  - web_search
  - citation_generation
  - source_summary

inputs:
  - query

outputs:
  - results
  - citations
  - summaries

requires_confirmation:
  false
```


---

# 51. Tool Registry


## Purpose


Central location for discovering and managing tools.


Responsibilities:


- Register tools
- Remove tools
- Search capabilities
- Validate tools
- Provide tools to Execution Manager


---

Architecture:


```
Tool Registry

    |

    |-- Search Tool

    |-- Notes Tool

    |-- Task Tool

    |-- Reminder Tool

    |-- Email Tool

    |-- Scam Tool

    |-- File Tool

    |-- Briefing Tool

```


---

# 52. Tool Execution Rules


## 52.1 Confirmation Policy


Tools are divided into categories.


## Read-Only Tools


Examples:

- Search
- File analysis
- Scam detection


No confirmation required.


---

## Write Tools


Examples:

- Create memory
- Create task
- Create reminder
- Delete note


Confirmation depends on user intent.


Explicit commands:

No confirmation.


Example:

"Create a reminder tomorrow at 8."

Execute.


Implicit actions:

Ask confirmation.


Example:

"You mentioned an exam tomorrow. Should I create a reminder?"


---

# 52.2 Error Handling


Every tool must return structured errors.


Example:


```json
{
 "status":"failed",
 "error":"Search API unavailable",
 "recoverable":true
}
```


The Execution Manager decides recovery.


---

# 53. Web Search Tool


## Purpose


Provide reliable internet search capabilities.


Provider:


Tavily


---

Capabilities:


- web_search
- citation_generation
- source_summary
- freshness_check


---

Input:


```json
{
 "query":"latest AI research"
}
```


---

Output:


```json
{
 "sources":[],
 "summary":"",
 "citations":[]
}
```


---

Requirements:


The tool must:


✓ Provide source links.

✓ Mention outdated information.

✓ Prefer reliable sources.

✓ Separate facts from opinions.


---

# 54. Notes Tool


## Purpose


Provide lightweight personal knowledge storage.


Capabilities:


- create_note
- edit_note
- delete_note
- search_notes
- retrieve_notes


---

Examples:


User:

"Save this note."


Action:


Create note.


---

User:

"Find my grocery list."


Action:


Search notes.


---

# 55. Task Management Tool


## Purpose


Manage user tasks and productivity.


Capabilities:


- create_task
- update_task
- delete_task
- complete_task
- list_tasks


---

Task properties:


Title

Description

Priority

Status

Deadline

Created date

Completed date


---

Priority Levels:


Low

Medium

High

Critical


---

# 56. Reminder Tool


## Purpose


Manage internal reminders.


The reminder system must not depend on external services.


Scheduler:


APScheduler


---

Capabilities:


- create_reminder
- update_reminder
- delete_reminder
- list_reminders


---

Supported reminders:


One-time:


"Remind me tomorrow at 10 AM."


Recurring:


"Remind me every Monday."


Daily:


"Remind me every day at 9 PM."


---

Execution:


```
Reminder Database

↓

APScheduler

↓

Reminder Trigger

↓

Notification Service

↓

User
```


---

# 57. Email Drafting Tool


## Purpose


Generate professional emails.


Version 1:


Draft only.


No automatic sending.


---

Capabilities:


- internship_email
- job_application_email
- follow_up_email
- networking_email
- business_email


---

Workflow:


User Request

↓

Collect Missing Information

↓

Generate Draft

↓

User Review

↓

User Copies Email


---

Supported customization:


Tone:

- Formal
- Friendly
- Professional
- Concise


---

# 58. Scam Detection Tool


## Purpose


Analyze potentially suspicious content.


Supported inputs:


- URLs
- Emails
- Job offers
- Messages


---

Output:


```json
{
 "risk_level":"medium",
 "confidence":75,
 "warnings":[],
 "recommendation":"Verify before proceeding"
}
```


---

Important:


The tool must never claim absolute certainty.


Example:


Bad:

"This is definitely a scam."


Good:

"This shows several indicators commonly associated with scams."


---

# 59. File Processing Tool


## Purpose


Allow Sage to understand user files.


Supported formats:


PDF

DOCX

TXT

CSV

XLSX

Images


---

Capabilities:


- extract_text
- summarize_document
- analyze_data
- answer_questions


---

Processing:


```
Upload

↓

File Detector

↓

Parser

↓

Content Extraction

↓

Context Builder

↓

AI Analysis

```


---

# 60. Daily Briefing Tool


## Purpose


Generate a daily overview.


Information sources:


- Tasks
- Reminders
- Deadlines
- Important notes


Output:


Example:


```
Good morning.

Today's priorities:

1. Complete project work
2. Study DSA

Upcoming:

Tomorrow:
Assignment deadline
```


---

# 61. Tool Testing Requirements


Every tool must include:


Unit tests:

- Valid input
- Invalid input
- Failure cases
- Edge cases


Integration tests:

- Tool Registry integration
- Execution Manager integration


---

# 62. Tool Acceptance Criteria


The Tool System is complete when:


✓ Tools are discovered dynamically.

✓ Tools expose capabilities.

✓ Planner does not depend on tool names.

✓ Execution Manager controls execution.

✓ Errors are handled safely.

✓ Every tool has tests.

✓ New tools can be added without architecture changes.

✓ Tool usage is logged.

✓ User actions requiring confirmation are protected.



End of Part 5.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 6 — Database Architecture
# =============================================================================


# 63. Database Architecture


## 63.1 Purpose

The database is responsible for persistent storage of Sage's long-term information.

The database stores:

- User data
- Conversations
- Memory
- Notes
- Tasks
- Reminders
- Tool execution history
- File metadata
- System configuration


The database must provide:

- Reliability
- Data integrity
- Query efficiency
- Backup capability
- Future scalability


---

# 64. Database Technology


## Primary Database

PostgreSQL


Version:

PostgreSQL 16+ recommended


---

## ORM

SQLAlchemy 2.x


Reasons:

- Type-safe database operations
- Clean repository pattern
- Async support
- Mature ecosystem


---

## Migration System

Alembic


All schema changes must be managed through migrations.


Forbidden:

Direct database modifications in production.


---

# 65. Database Design Principles


## 65.1 Repository Pattern


Services must never directly communicate with PostgreSQL.


Architecture:


```
Service

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL
```


Example:


MemoryService

does not execute SQL.

MemoryRepository handles database operations.


---

## 65.2 Data Ownership


Each module owns its data.


Example:


Memory Module:

memory tables


Task Module:

task tables


Reminder Module:

reminder tables


No module should modify another module's tables directly.


---

# 66. Database Schema Overview


Main entities:


```
users

conversations

messages

conversation_summaries

memories

memory_history

notes

tasks

reminders

tool_executions

search_history

files

daily_briefings

system_logs
```


---

# 67. Users Table


## Purpose

Stores user profile information.


Table:

users


Columns:


id

UUID

Primary key


created_at

Timestamp


updated_at

Timestamp


settings

JSONB


---

Notes:

Version 1 supports one user.

The schema keeps user separation possible for future multi-user support.


---

# 68. Conversations Table


## Purpose

Stores conversation sessions.


Table:

conversations


Columns:


id

UUID


user_id

Foreign Key


title

String


created_at

Timestamp


updated_at

Timestamp


archived

Boolean


---

Relationships:


User

↓

Many Conversations


---

# 69. Messages Table


## Purpose

Stores conversation messages.


Table:

messages


Columns:


id

UUID


conversation_id

Foreign Key


role

Enum:

- user
- assistant
- system
- tool


content

Text


metadata

JSONB


created_at

Timestamp


---

Metadata examples:


```
{
"provider":"gemini",
"tokens":1200,
"tools_used":["search"]
}
```


---

# 70. Conversation Summary Table


## Purpose


Stores compressed conversation history.


Table:

conversation_summaries


Columns:


id

UUID


conversation_id

Foreign Key


summary

Text


message_range_start

Timestamp


message_range_end

Timestamp


created_at

Timestamp


---

Reason:

Older conversations should not consume context unnecessarily.


---

# 71. Memory Tables


## 71.1 Memories Table


Purpose:

Store long-term user memories.


Table:

memories


Columns:


id

UUID


user_id

Foreign Key


category

Enum:


- preference
- goal
- fact
- event
- note


content

Text


importance_score

Integer


confidence_score

Integer


source

Enum:


- explicit
- automatic
- imported


confirmed

Boolean


created_at

Timestamp


updated_at

Timestamp


---

# 71.2 Memory History Table


Purpose:


Track memory changes.


Columns:


id

UUID


memory_id

Foreign Key


action

Enum:


- created
- updated
- deleted


old_value

JSONB


new_value

JSONB


created_at

Timestamp


---

Reason:

Allows recovery and auditing.


---

# 72. Notes Tables


## Notes


Purpose:

Store user notes.


Columns:


id

UUID


user_id

Foreign Key


title

String


content

Text


tags

JSONB


created_at


updated_at


deleted


Boolean


---

Features supported:


- Search
- Edit
- Delete
- Tag filtering


---

# 73. Tasks Tables


## Tasks


Purpose:

Manage user productivity tasks.


Columns:


id

UUID


user_id

Foreign Key


title

String


description

Text


priority

Enum:


- low
- medium
- high
- critical


status

Enum:


- pending
- in_progress
- completed


deadline

Timestamp


created_at


updated_at


completed_at


---

# 74. Reminders Tables


## Reminders


Purpose:

Persist scheduled reminders.


Columns:


id

UUID


user_id

Foreign Key


title

String


description

Text


schedule_type

Enum:


- once
- recurring


schedule_expression

String


next_execution

Timestamp


active

Boolean


created_at


updated_at


---

Examples:


One time:


2026-07-13 10:00


Recurring:


CRON:

0 21 * * *


---

# 75. Tool Execution Tables


## Tool Executions


Purpose:

Record agent actions.


Columns:


id

UUID


conversation_id

Foreign Key


tool_name


capability


input

JSONB


output

JSONB


status


Enum:


- started
- success
- failed


execution_time_ms


created_at


---

Reason:


Allows:


- Debugging
- Performance monitoring
- Error analysis


---

# 76. Search History Table


Purpose:


Track search operations.


Columns:


id


user_id


query


provider


sources


JSONB


created_at


---

Important:

This is history.

It is not memory.


---

# 77. File Metadata Table


Purpose:


Track processed files.


Columns:


id


user_id


filename


file_type


storage_path


size


processing_status


created_at


---

Supported:


PDF

DOCX

TXT

CSV

XLSX

Images


---

# 78. Daily Briefing Table


Purpose:


Store generated briefings.


Columns:


id


user_id


content


generated_at


---

# 79. System Logs Table


Purpose:


Application-level logging.


Columns:


id


level


module


message


metadata JSONB


created_at


---

# 80. Database Indexing Strategy


Required indexes:


messages:

conversation_id


memories:

user_id

category

importance_score


tasks:

user_id

status

deadline


reminders:

next_execution

active


tool_executions:

tool_name

created_at


---

# 81. Backup Strategy


Database backups must support:


Full backup

Daily recommended


Export backup

User-triggered


Example command:


"Export my Sage data."


Export includes:


- Memories
- Notes
- Tasks
- Conversations
- Settings


---

# 82. Database Security


Rules:


1.

Credentials stored only in environment variables.


2.

Database is not exposed publicly.


3.

Least privilege database user.


4.

Parameterized queries only.


5.

No raw SQL from user input.


---

# 83. Database Acceptance Criteria


Database implementation is complete when:


✓ All migrations run successfully.

✓ Repository layer works.

✓ Data survives restart.

✓ Backup and export work.

✓ Relationships are enforced.

✓ Indexes exist.

✓ Tests cover repositories.

✓ No service directly accesses database.



End of Part 6.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 7 — Backend Architecture
# =============================================================================


# 84. Backend Architecture


## 84.1 Purpose

The backend is the central application layer responsible for:

- API communication
- AI agent execution
- Business logic
- Database operations
- Tool coordination
- Background processing
- Security
- Application configuration


The backend must act as the bridge between the user interface and Sage's internal intelligence system.


---

# 85. Backend Technology


Framework:

FastAPI


Language:

Python 3.12+


Architecture Style:

Clean Architecture

+

Service-Oriented Modular Design


API Style:

REST API

+

WebSocket streaming where required


---

# 86. Backend Layer Architecture


The backend follows:


```
API Layer

↓

Service Layer

↓

Domain Layer

↓

Repository Layer

↓

Database Layer
```


External integrations:


```
Services

↓

Provider Interfaces

↓

External APIs
```


---

# 87. Backend Folder Structure


```
backend/

app/

├── main.py

├── api/

│   ├── routes/

│   ├── dependencies.py

│   └── middleware.py


├── core/

│   ├── security.py

│   ├── exceptions.py

│   └── constants.py


├── config/

│   └── settings.py


├── database/

│   ├── connection.py

│   ├── migrations/

│   └── session.py


├── models/

│   └── database_models/


├── schemas/

│   └── request_response_models/


├── repositories/


├── services/


├── agent/

│   ├── planner/

│   ├── execution/

│   ├── context/

│   └── runtime/


├── memory/


├── tools/


├── providers/


├── scheduler/


├── logging/


├── utils/


└── tests/
```


---

# 88. Application Entry Point


File:


```
main.py
```


Responsibilities:


- Create FastAPI application
- Load configuration
- Initialize database
- Register routes
- Register middleware
- Start background services


It must NOT contain business logic.


---

# 89. Configuration Management


Configuration is handled through environment variables.


Technology:


Pydantic Settings


Example:


```
DATABASE_URL

OPENAI_API_KEY

GEMINI_API_KEY

TAVILY_API_KEY

LOG_LEVEL
```


---

# 90. Environment Files


Repository contains:


```
.env.example
```


Example:


```
DATABASE_URL=your_database_url

GEMINI_API_KEY=your_key

TAVILY_API_KEY=your_key
```


Actual:


```
.env
```


must never be committed.


---

# 91. API Layer


Purpose:

Handle HTTP communication.


Responsibilities:


- Validate requests
- Call services
- Return responses
- Handle HTTP errors


The API layer must not:

- Execute database queries
- Call external APIs directly
- Contain business rules


---

# 92. API Route Structure


Base:


```
/api/v1
```


---

## Chat API


```
POST /chat
```


Purpose:

Send message to Sage.


Request:


```json
{
 "message":"Find internships for me",
 "conversation_id":"uuid"
}
```


Response:


```json
{
 "response":"",
 "conversation_id":"",
 "tools_used":[]
}
```


---

## Streaming Chat


```
WS /chat/stream
```


Purpose:


Provide real-time token streaming.


---

# 93. Memory APIs


## Get Memories


```
GET /memory
```


---

## Create Memory


```
POST /memory
```


---

## Update Memory


```
PUT /memory/{id}
```


---

## Delete Memory


```
DELETE /memory/{id}
```


---

# 94. Notes APIs


Create:


```
POST /notes
```


List:


```
GET /notes
```


Update:


```
PUT /notes/{id}
```


Delete:


```
DELETE /notes/{id}
```


Search:


```
GET /notes/search
```


---

# 95. Task APIs


Create task:


```
POST /tasks
```


List:


```
GET /tasks
```


Complete:


```
PATCH /tasks/{id}/complete
```


Delete:


```
DELETE /tasks/{id}
```


---

# 96. Reminder APIs


Create:


```
POST /reminders
```


List:


```
GET /reminders
```


Update:


```
PUT /reminders/{id}
```


Delete:


```
DELETE /reminders/{id}
```


---

# 97. File APIs


Upload:


```
POST /files/upload
```


Analyze:


```
POST /files/{id}/analyze
```


Supported:


PDF

DOCX

TXT

CSV

XLSX

Images


---

# 98. Service Layer


Purpose:

Contains business logic.


Examples:


MemoryService


TaskService


ReminderService


AgentService


FileService


EmailService


ScamDetectionService


---

Rules:


Services may call:


✓ repositories

✓ providers

✓ tools


Services may NOT call:


✗ frontend

✗ API routes directly


---

# 99. Repository Layer


Purpose:

Database abstraction.


Examples:


MemoryRepository


TaskRepository


ConversationRepository


Responsibilities:


- CRUD operations
- Database queries
- Transactions


Repositories should contain no business decisions.


---

# 100. Dependency Injection


FastAPI dependency injection should be used for:


- Database sessions
- Services
- Providers
- Configuration


Example:


```
Route

↓

Dependency

↓

Service

↓

Repository
```


Benefits:


- Easier testing
- Cleaner architecture
- Replaceable components


---

# 101. Error Handling


All errors must follow a standard format.


Example:


```json
{
 "success":false,
 "error":{
    "code":"MEMORY_NOT_FOUND",
    "message":"Memory does not exist"
 }
}
```


---

# 102. Custom Exceptions


Application exceptions:


```
BaseApplicationException

├── DatabaseException

├── ToolExecutionException

├── ProviderException

├── ValidationException

└── MemoryException
```


---

# 103. Middleware


Required middleware:


## Logging Middleware


Records:


- Request path
- Duration
- Status code


---

## Error Middleware


Catches unexpected errors.

Returns safe responses.


---

## CORS Middleware


Required for frontend communication.


---

# 104. Background Workers


Used for:


- Reminder execution
- Daily briefing generation
- Cleanup tasks
- Summarization


Scheduler:


APScheduler


---

# 105. Backend Security


Requirements:


- Validate all input.
- Never expose internal errors.
- Sanitize file uploads.
- Limit file size.
- Protect secrets.
- Use environment variables.


---

# 106. Backend Testing


Required tests:


API tests:


- Valid requests
- Invalid requests
- Error cases


Service tests:


- Business logic


Repository tests:


- Database operations


Integration tests:


- Full request flow


---

# 107. Backend Acceptance Criteria


Backend is complete when:


✓ FastAPI server starts successfully.

✓ Database connection works.

✓ API routes function.

✓ Services are separated.

✓ Repository pattern is implemented.

✓ Errors are handled.

✓ Tests pass.

✓ Agent runtime can execute through API.

✓ Background workers run correctly.



End of Part 7.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 8 — Frontend Architecture
# =============================================================================


# 108. Frontend Architecture


## 108.1 Purpose

The frontend provides the user interface for interacting with Sage.

The frontend must provide:

- Natural chat experience
- Conversation management
- Memory control
- Notes management
- Task management
- Reminder management
- File interaction
- Tool activity visibility


The frontend must not contain business logic.

All intelligence exists in the backend.


---

# 109. Frontend Technology Stack


Framework:

React


Language:

TypeScript


Build Tool:

Vite


Styling:

TailwindCSS


Component Library:

shadcn/ui


Icons:

Lucide React


Animations:

Framer Motion


API Client:

Axios


State Management:

React Context initially

Zustand recommended if application complexity increases


---

# 110. Frontend Architecture


Structure:


```
Pages

↓

Components

↓

Hooks

↓

Services

↓

API

```


---

# 111. Frontend Folder Structure


```
frontend/

src/

├── main.tsx

├── App.tsx


├── components/


│   ├── chat/

│   ├── memory/

│   ├── notes/

│   ├── tasks/

│   ├── reminders/

│   ├── files/

│   ├── common/


├── pages/


│   ├── ChatPage.tsx

│   ├── MemoryPage.tsx

│   ├── NotesPage.tsx

│   ├── TasksPage.tsx

│   ├── ReminderPage.tsx

│   └── SettingsPage.tsx


├── hooks/


├── services/


│   ├── api.ts

│   ├── chatService.ts

│   ├── memoryService.ts

│   ├── taskService.ts


├── contexts/


├── types/


├── utils/


└── styles/
```


---

# 112. Main User Interface


The primary interface is the Chat page.


Layout:


```
------------------------------------------------

 Sidebar          Chat Area

------------------------------------------------


Sidebar:

- New Conversation
- History
- Memory
- Notes
- Tasks
- Reminders
- Settings


Chat Area:

- Messages
- Tool Activity
- Input Box


------------------------------------------------
```


---

# 113. Chat Interface


## Purpose


Provide the main interaction method.


Features:


✓ Markdown rendering

✓ Code highlighting

✓ File attachments

✓ Streaming responses

✓ Tool activity display

✓ Conversation history


---

# 114. Message Component


Each message supports:


User message:

- Text
- Attachments
- Timestamp


Assistant message:

- Markdown
- Code blocks
- Citations
- Tool results


---

# 115. Streaming Responses


The frontend receives responses through:


WebSocket


Flow:


```
User

↓

Frontend

↓

WebSocket

↓

FastAPI

↓

Agent Runtime

↓

Streaming Tokens

↓

Frontend Rendering

```


Benefits:


- Faster perceived response time
- ChatGPT-like experience


---

# 116. Tool Activity UI


Sage should show controlled transparency.


Example:


```
Sage is working...

✓ Understanding request

✓ Searching web

✓ Reading sources

✓ Preparing response

```


The UI should show:

- Tool name
- Status
- Completion state


It should NOT show:

- Internal reasoning
- Private system prompts


---

# 117. Memory Interface


Purpose:

Allow user control over memory.


Features:


View memories


Categories:


- Preferences
- Goals
- Facts
- Events


Actions:


- Edit
- Delete
- Search


---

# 118. Memory Confirmation UI


When Sage detects possible memory:


Example:


```
I noticed this may be useful later:

"You are preparing for GATE."

Would you like me to remember this?


[Remember]

[Ignore]
```


---

# 119. Notes Interface


Features:


- Create notes
- Edit notes
- Delete notes
- Search notes
- Add tags


Layout:


```
Notes List

+

Note Editor
```


---

# 120. Task Dashboard


Purpose:


Manage productivity.


Features:


- Task creation
- Priority selection
- Deadline view
- Completion tracking


Example:


```
High Priority

[ ] Complete project documentation


Medium Priority

[ ] Practice DSA


Completed

[x] Setup Docker
```


---

# 121. Reminder Interface


Features:


- Create reminder
- Edit reminder
- Delete reminder
- View upcoming reminders


Display:


```
Upcoming


Tomorrow

10:00 AM

Study DSA


Monday

9:00 PM

Weekly Review
```


---

# 122. File Upload Interface


Supported:


PDF

DOCX

TXT

CSV

XLSX

Images


Features:


- Drag and drop
- Upload progress
- Processing status
- Results display


---

# 123. Settings Interface


Settings include:


## AI Provider


Example:


Gemini

Claude

OpenAI


---

## Appearance


- Light mode
- Dark mode


---

## Privacy


Options:


- Memory management
- Export data
- Delete data


---

# 124. State Management


Frontend state categories:


## Server State


Managed through API calls.


Examples:

- Tasks
- Notes
- Memories


---

## UI State


Examples:

- Sidebar status
- Theme
- Modal visibility


---

## Chat State


Examples:

- Current conversation
- Streaming response
- Messages


---

# 125. API Communication


All communication goes through:


```
services/
```


Example:


```
chatService.ts


memoryService.ts


taskService.ts
```


Components must never directly call APIs.


---

# 126. Frontend Security


Requirements:


- Sanitize rendered content
- Validate uploaded files
- Avoid storing secrets
- Handle expired sessions safely


---

# 127. Responsive Design


The interface must work on:


Desktop

Tablet

Mobile browser


Although Sage Version 1 is primarily a desktop application, responsive design is required.


---

# 128. Frontend Testing


Required:


Component tests:

- UI rendering
- User interactions


Integration tests:

- API communication


End-to-end tests:

- Complete user flows


Recommended tools:


Vitest

React Testing Library

Playwright


---

# 129. Frontend Acceptance Criteria


Frontend is complete when:


✓ Chat works smoothly.

✓ Streaming responses work.

✓ Markdown renders correctly.

✓ Memory management works.

✓ Notes work.

✓ Tasks work.

✓ Reminders work.

✓ Files upload correctly.

✓ Tool activity is visible.

✓ Interface works on different screens.

✓ Tests pass.



End of Part 8.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 9 — File Processing & Document Intelligence
# =============================================================================


# 130. File Processing System


## 130.1 Purpose

The File Processing System allows Sage to understand and analyze user-provided files.

Supported formats:

- PDF
- DOCX
- TXT
- CSV
- XLSX
- Images


The system converts different file formats into structured information that can be used by the AI Agent.


---

# 131. Design Principles


## 131.1 Format Independence


The AI Agent should not know how files are processed.


Flow:


```
File

↓

File Processing Tool

↓

Parser

↓

Extracted Content

↓

Context Builder

↓

AI Agent

```


---

## 131.2 Security First


Files are considered untrusted input.


The system must:


- Validate file type
- Limit file size
- Prevent malicious uploads
- Store files securely
- Avoid executing file content


---

# 132. File Processing Architecture


```
User Upload

↓

File API

↓

File Validation

↓

File Type Detection

↓

Parser Selection

↓

Content Extraction

↓

Processing Pipeline

↓

AI Analysis

↓

Response
```


---

# 133. Supported File Types


## 133.1 PDF


Purpose:


Extract text and understand documents.


Recommended libraries:


Primary:

PyMuPDF


Alternative:

pdfplumber


Capabilities:


- Text extraction
- Page extraction
- Metadata extraction


Future:


- Table extraction
- PDF image extraction


---

## 133.2 DOCX


Purpose:


Process Microsoft Word documents.


Library:


python-docx


Capabilities:


- Paragraph extraction
- Heading detection
- Table extraction


---

## 133.3 TXT


Purpose:


Process plain text files.


Processing:


Direct reading


Validation:


UTF-8 preferred


---

## 133.4 CSV


Purpose:


Analyze structured data.


Library:


Pandas


Capabilities:


- Read data
- Summarize columns
- Detect patterns
- Answer questions


Example:


User:

"Analyze this CSV."


Sage:


- Row count
- Column information
- Missing values
- Important observations


---

## 133.5 XLSX


Purpose:


Process Excel files.


Library:


OpenPyXL


Capabilities:


- Read sheets
- Extract tables
- Analyze data


---

## 133.6 Images


Purpose:


Understand visual information.


Capabilities:


- OCR
- Image description
- Text extraction


Possible providers:


Cloud vision APIs

or

Vision-capable LLM providers


Local processing remains optional.


---

# 134. File Tool Interface


All file operations use the Tool architecture.


Capability Manifest:


```yaml
tool:
 name: file_processor

capabilities:

 - extract_text
 - analyze_document
 - summarize_file
 - analyze_data
 - image_understanding

inputs:

 - file_id

outputs:

 - extracted_content
 - metadata
 - analysis
```


---

# 135. File Database Flow


```
Upload

↓

files table

↓

Processing Status

↓

Extraction

↓

Analysis

↓

Result Storage

```


---

# 136. File Storage Strategy


Version 1:


Local storage.


Example:


```
storage/

files/

user_id/

filename
```


Database stores:


- File path
- Metadata
- Processing status


---

# 137. File Processing Status


States:


```
uploaded

↓

validating

↓

processing

↓

completed

↓

failed
```


---

# 138. File Validation


Required checks:


## Extension Validation


Allowed:


PDF

DOCX

TXT

CSV

XLSX

Images


---

## Size Validation


Configurable limit.


Recommended default:


25MB


---

## Content Validation


Check:


- File is readable
- File is not corrupted
- MIME type matches extension


---

# 139. Document Context Management


Large files cannot be directly sent to the LLM.


Pipeline:


```
Document

↓

Extraction

↓

Chunking

↓

Relevant Retrieval

↓

Context Builder

↓

LLM
```


---

# 140. Chunking Strategy


Documents should be split into manageable sections.


Chunk metadata:


```
{
file_id:"",
chunk_number:"",
content:"",
page_number:""
}
```


---

# 141. Future Vector Search


Future enhancement:


PostgreSQL pgvector


Purpose:


Semantic document retrieval.


Example:


User:


"Find information about payment terms."


System:


Searches document meaning, not only keywords.


---

# 142. File Privacy Rules


Mandatory:


1.

Files belong only to the user.


2.

Files are not shared.


3.

External APIs receive files only when explicitly required.


4.

Temporary files are deleted after processing.


5.

User can delete uploaded files.


---

# 143. File Deletion


Command:


"Delete this document."


Action:


Remove:


- File storage
- Database metadata
- Extracted content


---

# 144. File Processing Errors


Examples:


Invalid file:


```
Unsupported file type
```


Corrupted document:


```
Unable to read document
```


Large file:


```
File exceeds size limit
```


The system should explain errors clearly.


---

# 145. File Processing Tests


Required tests:


PDF:

- Extract text
- Invalid PDF


DOCX:

- Extract paragraphs


TXT:

- Read content


CSV:

- Analyze dataset


XLSX:

- Read sheets


Images:

- OCR pipeline


Security:

- Invalid uploads
- Large files


---

# 146. File System Acceptance Criteria


File Processing is complete when:


✓ All supported formats work.

✓ Files are validated.

✓ Processing is modular.

✓ Large files are handled safely.

✓ Extracted content can be used by Sage.

✓ User can delete files.

✓ Tests pass.

✓ No unsafe file execution occurs.



End of Part 9.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 10 — Reminder System & Background Jobs
# =============================================================================


# 147. Reminder and Background Job System


## 147.1 Purpose

The Reminder System allows Sage to schedule and execute future actions.

Examples:

- One-time reminders
- Recurring reminders
- Daily briefings
- Scheduled maintenance tasks


The system must work reliably even after Sage restarts.


---

# 148. Design Principles


## 148.1 Persistent Scheduling


Reminders must not exist only in memory.

Incorrect:


```
Application Memory

↓

APScheduler
```


because restarting the application loses reminders.


Correct:


```
PostgreSQL

↓

APScheduler

↓

Execution

```


---

## 148.2 Internal Reminders Only


Version 1 reminder notifications are internal to Sage.

No external services required.


Future integrations:

- Telegram
- Email
- Mobile notifications


---

# 149. Scheduler Technology


Scheduler:


APScheduler


Reason:


- Lightweight
- Python native
- Cron support
- Date scheduling
- Background execution


---

# 150. Scheduler Architecture


```
User

↓

Reminder Tool

↓

Reminder Service

↓

PostgreSQL

↓

APScheduler

↓

Job Execution

↓

Notification Service

↓

User
```


---

# 151. Reminder Types


## 151.1 One-Time Reminder


Example:


"Remind me tomorrow at 10 AM."


Stored:


```
type:

once


execution_time:

2026-07-13 10:00
```


After execution:


status:

completed


---

# 151.2 Recurring Reminder


Example:


"Remind me every Monday."


Stored:


```
type:

recurring


schedule:

MON 09:00
```


Continues until deleted.


---

# 151.3 Interval Reminder


Example:


"Remind me every 3 hours."


Stored:


```
interval:

3 hours
```


---

# 152. Reminder Commands


Natural language support:


Create:


"Remind me to study DSA at 8 PM."


List:


"Show my reminders."


Update:


"Change my meeting reminder to 7 PM."


Delete:


"Delete my gym reminder."


---

# 153. Reminder Confirmation Rules


Explicit:


"Create a reminder for tomorrow."

Action:

Create immediately.


Implicit:


"You have an exam tomorrow."

Response:


"Would you like me to create a reminder?"


---

# 154. Reminder Service


Responsibilities:


- Create reminders
- Validate schedules
- Update reminders
- Delete reminders
- Trigger jobs


The service communicates with:


Reminder Repository

Scheduler


---

# 155. Job Recovery System


Problem:


Application stops.


Solution:


On startup:


```
Application Start

↓

Load Active Reminders

↓

Validate Next Execution

↓

Register Jobs

↓

Resume Scheduler
```


---

# 156. Missed Reminder Handling


Example:


Reminder:

9 AM


Computer was off.


Application starts:

11 AM


Policy:


For one-time reminders:


Mark as missed.


For important reminders:


Notify user:


"You missed this reminder."


---

# 157. Notification Service


Version 1:


Internal notification.


Example:


```
Reminder:

Study DSA
Time:

8 PM
```


Future:


Can support:


- Telegram Bot
- Email
- Push Notifications


---

# 158. Daily Briefing Scheduler


Daily briefing is implemented as a scheduled job.


Example:


Every morning:


```
08:00 AM

↓

Generate Briefing

↓

Collect:

Tasks

Reminders

Deadlines

Notes

↓

Create Summary

↓

Display to User
```


---

# 159. Background Jobs


Other scheduled jobs:


## Conversation Summarization


Purpose:

Compress old conversations.


---

## Memory Maintenance


Purpose:

Detect outdated memories.


---

## Database Backup


Purpose:

Protect user data.


---

## Cleanup Tasks


Purpose:

Remove temporary files.


---

# 160. Job Execution Logging


Every job must log:


```
Job Name

Start Time

End Time

Status

Error

Duration
```


Stored in:


system_logs


---

# 161. Scheduler Failure Handling


If a job fails:


1.

Log failure.


2.

Retry if safe.


3.

Notify user if required.


4.

Do not crash application.


---

# 162. Scheduler Security


Rules:


- Validate user schedules.
- Prevent unlimited jobs.
- Prevent duplicate reminders.
- Protect against invalid cron expressions.


---

# 163. Reminder Testing


Required tests:


Creation:


✓ Create reminder


✓ Invalid time


Execution:


✓ Job triggers


✓ Database updated


Recovery:


✓ Restart application


✓ Restore reminders


Failure:


✓ Failed job handling


---

# 164. Reminder Acceptance Criteria


Reminder System is complete when:


✓ One-time reminders work.

✓ Recurring reminders work.

✓ Reminders survive restart.

✓ Jobs recover automatically.

✓ Users can edit reminders.

✓ Users can delete reminders.

✓ Daily briefing works.

✓ Failures are logged.

✓ Tests pass.



End of Part 10.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 11 — Scam Detection & Verification System
# =============================================================================


# 165. Scam Detection System


## 165.1 Purpose

The Scam Detection System helps users evaluate suspicious:

- URLs
- Emails
- Job offers
- Messages
- Business communications


The system provides a risk assessment based on available evidence.

It must never claim absolute certainty.


---

# 166. Core Philosophy


## 166.1 No Absolute Claims


Incorrect:


"This is definitely a scam."


Correct:


"This contains several indicators commonly associated with scams."


---

## 166.2 Explainable Results


Every analysis must explain:

- Why the risk exists
- Which signals were detected
- What evidence was considered
- What action the user should take


---

# 167. Scam Detection Architecture


```
User Input

↓

Scam Detection Tool

↓

Input Analyzer

↓

Verification Modules

↓

Risk Engine

↓

Report Generator

↓

User
```


---

# 168. Supported Analysis Types


## 168.1 URL Analysis


Purpose:

Determine whether a website appears legitimate.


Checks:


- Domain spelling
- HTTPS availability
- Domain age (if available)
- Suspicious patterns
- Redirect behavior
- Known reputation sources


---

Example:


User:


"Is this website real?"

Input:


https://example.com


Output:


```
Risk Level:

Low


Confidence:

82%


Reasons:

- Valid HTTPS
- Domain appears consistent
- No suspicious patterns detected


Recommendation:

Proceed carefully.
```


---

# 168.2 Official Website Verification


Purpose:


Determine whether a website belongs to a claimed organization.


Example:


User:

"Is this the official Google careers website?"


Checks:


- Domain ownership patterns
- Official domain matching
- Website consistency
- Contact information


---

Important:


A website looking professional does not prove legitimacy.


---

# 168.3 Email Analysis


Purpose:


Analyze suspicious emails.


Checks:


Sender:

- Domain authenticity
- Misspellings
- Suspicious addresses


Content:

- Urgency tactics
- Requests for sensitive information
- Payment requests
- Suspicious links


---

Example:


```
Risk:

High


Reasons:

- Sender domain differs from company domain
- Requests payment
- Uses urgency language


Recommendation:

Do not provide personal information.
```


---

# 168.4 Job Offer Verification


Purpose:


Analyze internship and employment offers.


Checks:


Company:

- Official presence
- Domain matching
- Contact details


Offer:

- Unrealistic salary
- Payment requests
- Missing interview process
- Suspicious documents


---

Example:


Input:


"Pay ₹5000 for guaranteed internship."


Analysis:


Risk:

High


Warning signs:

- Requires upfront payment
- Guaranteed employment claims


Recommendation:

Avoid payment until independently verified.


---

# 168.5 Message Analysis


Supported:


- SMS
- WhatsApp messages
- Chat messages


Checks:


- Suspicious links
- Manipulation techniques
- Requests for credentials
- Financial requests


---

# 169. Risk Assessment Engine


Every result includes:


## Risk Level


Possible values:


Low

Medium

High

Critical


---

## Confidence Score


Range:


0-100%


Meaning:


Confidence in the assessment, not probability of fraud.


Example:


```
Risk:

Medium


Confidence:

75%
```


---

# 170. Detection Signals


The engine evaluates signals.


## Technical Signals


Examples:


- Domain mismatch
- Invalid certificates
- Suspicious URL structure
- Unknown domains


---

## Behavioral Signals


Examples:


- Urgency
- Fear tactics
- Pressure
- Secret requests


---

## Financial Signals


Examples:


- Advance payment
- Cryptocurrency requests
- Gift cards
- Banking information


---

## Identity Signals


Examples:


- Fake company names
- Impersonation
- Fake recruiters


---

# 171. Scam Analysis Output Schema


Example:


```json
{
 "risk_level":"high",

 "confidence_score":85,

 "summary":
 "This job offer contains multiple suspicious indicators.",

 "reasons":[
   "Requires upfront payment",
   "No official company verification"
 ],

 "warning_signs":[
   "Guaranteed job promise"
 ],

 "recommendation":
 "Do not send money or personal documents."
}
```


---

# 172. External Verification Sources


Possible sources:


- Domain reputation APIs
- Official company websites
- Search providers
- Public databases


External APIs must be optional.


Sage should still function without paid services.


---

# 173. Tool Execution Rules


Scam Detection is:


Read-only.


It cannot:


- Send reports
- Contact companies
- Block websites


---

# 174. Privacy Rules


User-provided:

- Emails
- Messages
- Job offers


must remain private.


Only required information should be sent to external providers.


---

# 175. Limitations


Sage must communicate limitations.


Examples:


"Unable to verify ownership of this domain."


"Analysis is based on available indicators."


"This does not guarantee safety."


---

# 176. Scam Detection Testing


Required tests:


URL:


✓ Valid URL

✓ Suspicious URL

✓ Fake domain patterns


Email:


✓ Legitimate email

✓ Phishing indicators


Job Offers:


✓ Normal offer

✓ Payment scam


Messages:


✓ Suspicious links

✓ Urgency attacks


---

# 177. Scam Detection Acceptance Criteria


System is complete when:


✓ URLs can be analyzed.

✓ Emails can be analyzed.

✓ Job offers can be analyzed.

✓ Risk levels are generated.

✓ Confidence scores are provided.

✓ Reasons are explained.

✓ Recommendations are actionable.

✓ Uncertainty is communicated.

✓ Tests pass.



End of Part 11.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 12 — Web Search & Research System
# =============================================================================


# 178. Web Search System


## 178.1 Purpose

The Web Search System allows Sage to retrieve current information from the internet.

It enables Sage to:

- Search reliable sources
- Summarize information
- Provide citations
- Compare sources
- Detect outdated information
- Separate facts from opinions


---

# 179. Search Philosophy


## 179.1 Search Is Not Knowledge Replacement


Sage's internal knowledge may become outdated.

For:

- Latest news
- Current prices
- Current policies
- Recent releases
- Events


Sage should use web search.


---

## 179.2 Source Transparency


Every externally retrieved answer should show:

- Source name
- Link
- Relevant information
- Date if available


The user should be able to verify claims.


---

# 180. Search Architecture


```
User Query

↓

Intent Analyzer

↓

Research Decision

↓

Search Tool

↓

Tavily API

↓

Source Processing

↓

Citation Generator

↓

Context Builder

↓

AI Response

```


---

# 181. Search Provider


Primary Provider:


Tavily


Reason:


- Designed for AI agents
- Provides relevant search results
- Supports citations
- Provides summaries


---

# 182. Search Tool Capability Manifest


```yaml
tool:

 name:
  web_search


capabilities:

 - internet_search
 - source_retrieval
 - citation_generation
 - information_summary


inputs:

 - query


outputs:

 - sources
 - summaries
 - citations

```


---

# 183. Search Decision Logic


The Agent decides whether search is required.


Search required:


- Current information
- Unknown information
- Verification requests
- User explicitly asks


Examples:


"Who is the current CEO?"


Search.


---

Search not required:


"What is polymorphism?"


Internal knowledge is enough.


---

# 184. Search Workflow


Step 1:

Analyze query.


Step 2:

Determine if external information is required.


Step 3:

Generate search query.


Step 4:

Retrieve sources.


Step 5:

Filter results.


Step 6:

Extract relevant information.


Step 7:

Generate cited response.


---

# 185. Source Evaluation


Sources should be evaluated based on:


## Authority


Examples:


Government websites

Official documentation

Academic sources


---

## Relevance


Does the source answer the question?


---

## Freshness


Is the information recent?


---

## Reliability


Is the source trustworthy?


---

# 186. Source Ranking


Priority:


Highest:


Official sources


↓

Research papers


↓

Established organizations


↓

Reliable news sources


↓

Community discussions


↓

Unknown websites


---

# 187. Citation Format


Responses should include:


Example:


```
According to the official documentation,
the feature was introduced in version 3.2.


Sources:

1. Official Documentation
   https://example.com

2. Release Notes
   https://example.com
```


---

# 188. Fact vs Opinion Separation


Sage must distinguish:


## Verified Fact


Supported by reliable evidence.


Example:


"Python 3.12 was released in October 2023."


---

## Opinion


Interpretation or recommendation.


Example:


"Python is a good choice for beginners."


---

Response example:


```
Fact:

The company released version 2.0.


Opinion:

Many developers consider it easier to use.
```


---

# 189. Outdated Information Handling


Sage should indicate:


"Information may have changed since my knowledge cutoff."


or


"This information was retrieved from current sources."


---

# 190. Search History


All searches may be logged.


Stored:


- Query
- Date
- Provider
- Sources


Search history is not memory.


---

# 191. Search Caching


Optional optimization.


Purpose:


Reduce repeated API calls.


Example:


Same query within short time:


Use cached result.


---

Cache rules:


- Expire after configured duration.
- Never store sensitive searches permanently without user control.


---

# 192. Research Mode


Future enhancement:


Dedicated research workflow.


Example:


User:


"Research the best backend frameworks."


Sage performs:


1. Multiple searches.

2. Source comparison.

3. Summary generation.

4. Recommendation.


---

# 193. Search Failure Handling


Possible failures:


API unavailable


↓

Explain:


"Search is temporarily unavailable."


---

No results


↓

Explain:


"No reliable sources found."


---

Low-quality sources


↓

Warn user.


---

# 194. Search Security


Requirements:


- Validate URLs.
- Do not execute scripts.
- Do not download unsafe content.
- Limit external requests.


---

# 195. Search Testing


Required tests:


Tool:


✓ Successful search

✓ API failure

✓ Empty results


Citation:


✓ Sources included

✓ Links preserved


Freshness:


✓ Old information warning


Integration:


✓ Agent selects search correctly


---

# 196. Search Acceptance Criteria


Web Search System is complete when:


✓ Sage can search the web.

✓ Results contain citations.

✓ Sources are ranked.

✓ Facts and opinions are separated.

✓ Outdated information is handled.

✓ Search failures are graceful.

✓ Search usage is logged.

✓ Tests pass.



End of Part 12.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 13 — Email Drafting & Writing Assistant
# =============================================================================


# 197. Email Drafting System


## 197.1 Purpose


The Email Drafting System allows Sage to create professional written communication.

Version 1 supports:

- Draft creation
- Editing
- Tone customization
- Professional formatting


Version 1 does NOT automatically send emails.


---

# 198. Design Philosophy


Sage should act as a professional writing assistant.

It should:

- Understand context
- Ask missing information
- Produce polished drafts
- Allow user control before sending


---

# 199. Supported Email Types


## Internship Applications


Example:


"Write an internship application email."


---

## Job Applications


Example:


"Draft an email for a software developer position."


---

## Networking Emails


Example:


"Write a LinkedIn networking email."


---

## Follow-Up Emails


Example:


"Write a follow-up after my interview."


---

## Business Communication


Examples:


- Client communication
- Professional requests
- Meeting follow-ups


---

# 200. Email Generation Workflow


```
User Request

↓

Intent Detection

↓

Information Collection

↓

Email Planning

↓

Draft Generation

↓

Quality Validation

↓

User Review

↓

Final Draft

```


---

# 201. Information Collection


Before generating an email, Sage should identify missing details.


Required information:


Recipient:

Purpose:

Context:

Important points:

Desired tone:


---

Example:


User:


"Write an internship email."


Sage:


"I can do that. Please provide:

- Company name
- Role
- Your skills
- Any previous experience
- Recipient name (if available)
"


---

# 202. Tone Customization


Supported tones:


## Formal


For:

- Recruiters
- Companies
- Official communication


---

## Professional Friendly


For:

- Networking
- Mentorship


---

## Concise


For:

- Short follow-ups


---

## Persuasive


For:

- Applications
- Business requests


---

# 203. Email Quality Checks


Generated emails should verify:


Grammar

Professional tone

Clear purpose

Proper structure

No unnecessary claims

No false experience


---

# 204. Email Structure


Recommended:


```
Subject

Greeting

Introduction

Purpose

Relevant Information

Call To Action

Closing

Signature
```


---

# 205. Email Tool Manifest


```yaml
tool:

 name:
  email_writer


capabilities:

 - draft_email
 - improve_email
 - change_tone
 - summarize_email


inputs:

 - context
 - requirements


outputs:

 - email_draft

```


---

# 206. Future Email Sending


Not included in Version 1.


Future architecture:


```
Draft

↓

User Approval

↓

Email Provider

↓

Send

↓

Confirmation
```


Sending requires:

- Authentication
- Permission handling
- Security review


---

# 207. Email Testing


Required tests:


✓ Missing information handling

✓ Different tones

✓ Different email types

✓ Grammar validation

✓ No hallucinated information


---

# 208. Email Acceptance Criteria


Email system is complete when:


✓ Professional drafts are generated.

✓ Missing information is requested.

✓ Tone can change.

✓ No automatic sending occurs.

✓ Output quality is validated.

✓ Tests pass.



End of Part 13.



# =============================================================================
# Part 14 — Notes & Task Management System
# =============================================================================


# 209. Productivity System Overview


## 209.1 Purpose


The Productivity System allows Sage to act as a lightweight personal organization assistant.


It manages:


- Notes
- Tasks
- Priorities
- Deadlines
- Progress tracking


---

# 210. Notes Management


## Purpose


Store user information that does not belong in long-term memory.


Difference:


Memory:

Information about the user.


Example:

"I prefer Java."


---

Note:

Information user wants to save.


Example:

"Meeting notes."


---

# 211. Notes Capabilities


Supported actions:


Create

Read

Update

Delete

Search


---

# 212. Notes Commands


Examples:


"Save this note."


"Show my notes."


"Find my project notes."


"Delete my grocery list."


---

# 213. Notes Data Model


Note contains:


Title

Content

Tags

Created Date

Updated Date


---

# 214. Notes Search


Supported:


Keyword search


Future:


Semantic search with embeddings


---

# 215. Task Management


## Purpose


Help users track actionable items.


---

# 216. Task Capabilities


Create task


Update task


Delete task


Complete task


List tasks


Filter tasks


---

# 217. Task Properties


Each task contains:


Title


Description


Priority


Status


Deadline


Created date


Completed date


---

# 218. Task Priority


Levels:


Low


Medium


High


Critical


---

# 219. Task Status


States:


Pending


In Progress


Completed


Cancelled


---

# 220. Natural Language Task Creation


Examples:


"Create a task to finish my portfolio."


"Remind me to submit assignment Friday."


"Show incomplete tasks."


---

# 221. Task Workflow


```
User Request

↓

Task Tool

↓

Task Service

↓

Task Repository

↓

Database

↓

Response

```


---

# 222. Task and Reminder Relationship


Tasks and reminders are separate.


Task:


"What needs to be done?"


Reminder:


"When should Sage notify me?"


They may be connected.


Example:


Task:

Complete project.


Reminder:

Tomorrow 6 PM.


---

# 223. Productivity Dashboard


Frontend should display:


Today's tasks


Upcoming deadlines


High priority items


Completed tasks


---

# 224. Productivity Automation


Future enhancements:


- Automatic task suggestions
- Task prioritization
- Weekly reviews
- Productivity analytics


---

# 225. Productivity Testing


Notes:


✓ Create note

✓ Edit note

✓ Delete note

✓ Search note


Tasks:


✓ Create task

✓ Update task

✓ Complete task

✓ Delete task


Integration:


✓ Agent creates tasks correctly


---

# 226. Productivity Acceptance Criteria


System is complete when:


✓ Notes work.

✓ Tasks work.

✓ Search works.

✓ Priorities work.

✓ Deadlines work.

✓ Database persistence works.

✓ Agent can interact naturally.

✓ Tests pass.



End of Part 14.

# =============================================================================
# SAGE_BLUEPRINT.md
# Version: 1.0
# Part 15 — Daily Briefing & Personal Assistant Workflows
# =============================================================================


# 227. Daily Briefing System


## 227.1 Purpose


Daily Briefing provides the user with a summary of important information.


It combines:

- Tasks
- Reminders
- Deadlines
- Notes
- Goals
- Important updates


---

# 228. Daily Briefing Flow


```
Scheduler

↓

Daily Briefing Service

↓

Collect User Data

↓

AI Summary Generation

↓

Store Briefing

↓

Display To User

```


---

# 229. Briefing Content


Example:


```
Good morning.


Today's priorities:

1. Complete Sage development
2. Practice DSA


Upcoming:

Tomorrow:
Project submission


Reminders:

8 PM:
Study session

```


---

# 230. Briefing Schedule


Default:


Every day at configured time.


Example:


8:00 AM


User can customize.


---

# 231. Weekly Review


Future feature:


"What did we achieve this week?"


Uses:


- Completed tasks
- Conversations
- Notes
- Goals


---

# 232. Personal Assistant Workflows


Sage supports multi-step workflows.


Example:


User:


"Help me prepare for internship applications."


Agent:


1. Check stored skills.

2. Review resume notes.

3. Suggest improvements.

4. Create task list.

5. Schedule reminders.


---

# 233. Workflow Engine


Architecture:


```
Goal

↓

Planner

↓

Steps

↓

Tools

↓

Execution

↓

Result
```


---

# 234. Multi-Step Planning Rules


The Agent may execute multiple tools automatically.


Allowed:


Read-only operations.


Example:

Search + Analyze + Summarize


---

Require confirmation:


Destructive actions.


Example:

Delete data.


---

# 235. Personal Assistant Acceptance Criteria


✓ Daily briefing works.

✓ Scheduled generation works.

✓ Tasks and reminders integrate.

✓ Multi-step workflows work.

✓ User maintains control.



End Part 15.



# =============================================================================
# Part 16 — Security, Privacy & Data Protection
# =============================================================================


# 236. Security Philosophy


Sage is a private personal AI assistant.


Primary principle:


User data belongs to the user.


---

# 237. Data Privacy Rules


Sage must:


✓ Store data locally.

✓ Avoid unnecessary external APIs.

✓ Protect secrets.

✓ Allow export.

✓ Allow deletion.


---

# 238. External API Policy


Possible external providers:


- AI providers
- Tavily search


Only required data should leave the machine.


Sensitive data should not be sent without user permission.


---

# 239. Secret Management


Secrets:


Stored in:


.env


Never:


- GitHub
- Source code
- Documentation


---

# 240. Database Security


Requirements:


- PostgreSQL password protection
- Local-only access
- Parameterized queries
- Migration control


---

# 241. File Security


Rules:


- Validate uploads
- Limit size
- Store securely
- Delete when requested


---

# 242. Agent Safety


The agent must:


- Explain actions
- Ask confirmation when required
- Avoid destructive operations
- Log tool usage


---

# 243. Privacy Controls


User commands:


"Export my data."


"Delete my memories."


"Forget everything."


"Show stored information."


---

# 244. Security Acceptance Criteria


✓ Secrets protected.

✓ User data private.

✓ Dangerous actions controlled.

✓ Export works.

✓ Delete works.



End Part 16.



# =============================================================================
# Part 17 — Docker Deployment & Local Running
# =============================================================================


# 245. Deployment Strategy


Sage is designed for local deployment.


Primary target:


User laptop.


No VPS required.


---

# 246. Docker Architecture


Containers:


```
Docker Compose

|

|-- Backend

|

|-- Frontend

|

|-- PostgreSQL

|

|-- Optional Redis

```


---

# 247. Backend Container


Contains:


- FastAPI
- Python dependencies
- Agent runtime


---

# 248. Frontend Container


Contains:


- React application
- Static build


---

# 249. Database Container


PostgreSQL:


Stores:


- Memory
- Conversations
- Tasks
- Notes
- Reminders


---

# 250. Optional Redis


Purpose:


Future:


- Caching
- Queue management
- Faster processing


Not required for Version 1.


---

# 251. Environment Configuration


Required:


```
.env.example
```


Contains:


Database URL

AI provider keys

Search provider key

Application settings


---

# 252. Running Sage


User experience:


First time:


```
git clone

↓

configure .env

↓

docker compose up

↓

open browser

↓

use Sage

```


Future improvement:


One-click launcher.


---

# 253. Production Practices


Recommended:


- Health checks
- Logging
- Backups
- Automatic migrations


---

# 254. Docker Acceptance Criteria


✓ Containers build.

✓ Application starts.

✓ Database persists.

✓ Environment variables work.

✓ Documentation exists.



End Part 17.



# =============================================================================
# Part 18 — Testing Strategy
# =============================================================================


# 255. Testing Philosophy


Every important component must have automated tests.


Testing levels:


- Unit tests
- Integration tests
- End-to-end tests


---

# 256. Backend Testing


Frameworks:


pytest


Test:


- Services
- Repositories
- APIs
- Agent logic


---

# 257. Tool Testing


Every tool requires:


✓ Valid input test

✓ Invalid input test

✓ Failure test

✓ Recovery test


---

# 258. Frontend Testing


Tools:


- Vitest
- React Testing Library
- Playwright


Test:


- Components
- User interactions
- Complete workflows


---

# 259. Agent Testing


Test:


- Correct tool selection
- Planning
- Memory usage
- Error recovery


---

# 260. Test Execution


Command:


```
pytest
```


Frontend:


```
npm test
```


---

# 261. Testing Acceptance Criteria


✓ Tests exist.

✓ Tests pass.

✓ Critical features covered.

✓ Failures are understandable.



End Part 18.



# =============================================================================
# Part 19 — Documentation Requirements
# =============================================================================


# 262. README.md


The project must include:


## Overview


What Sage is.


---

## Features


List capabilities.


---

## Technology Stack


Example:


Backend:

FastAPI


Frontend:

React


Database:

PostgreSQL


AI:

Provider based


---

## Installation


Simple steps.


---

## Configuration


Explain .env.


---

## Running Locally


Docker instructions.


---

## Testing


Commands.


---

## Usage Examples


Examples:


"Remember I prefer Java."

"Create a task."

"Analyze this URL."


---

## Future Improvements


Examples:


- Mobile app
- Voice assistant
- More integrations


---

## License


Open source license.


---

# 263. Architecture Documentation


Include:


Architecture diagram:


```
User

↓

Frontend

↓

Backend API

↓

Agent Runtime

↓

Tools

↓

Database

```


---

# 264. Development Documentation


Include:


- Folder structure
- Adding new tools
- Database migrations
- Testing guide


---

# 265. Documentation Acceptance Criteria


✓ New users can install.

✓ Developers can extend.

✓ Architecture is understandable.



End Part 19.



# =============================================================================
# Part 20 — Claude Development Handoff Instructions
# =============================================================================


# 266. Purpose


This section defines how another AI coding assistant should build Sage.


---

# 267. Development Rules


The AI developer must:


- Follow this blueprint exactly.
- Not skip architecture.
- Build modularly.
- Write production-quality code.
- Add tests.
- Explain decisions.


---

# 268. Development Order


Build phases:


## Phase 1

Foundation


Includes:

- Repository setup
- Backend setup
- Database
- Configuration


---

## Phase 2

Core AI Agent


Includes:

- Agent runtime
- Provider switching
- Tool registry
- Planning


---

## Phase 3

Memory


Includes:

- Long-term memory
- Conversation storage
- Memory commands


---

## Phase 4

Productivity


Includes:

- Notes
- Tasks
- Reminders


---

## Phase 5

Advanced Tools


Includes:

- Web search
- Scam detection
- File processing
- Email drafting


---

## Phase 6

Frontend


Includes:

- Chat interface
- Dashboards
- Settings


---

## Phase 7

Deployment


Includes:

- Docker
- Documentation
- Testing


---

# 269. Important Instruction For AI Developer


After completing each phase:


1. Verify tests.

2. Update documentation.

3. Explain completed work.

4. Continue automatically to next phase.


The developer should not wait for user approval unless a major architectural decision is required.


---

# 270. Final Project Goal


Build:


Sage


A private, modular, extensible personal AI assistant.


Capabilities:


✓ ChatGPT-like experience

✓ Long-term memory

✓ Tool usage

✓ Multi-step planning

✓ Web research

✓ Scam analysis

✓ Productivity management

✓ Document understanding

✓ Professional writing

✓ Local privacy-first deployment


---

# END OF SAGE_BLUEPRINT.md
