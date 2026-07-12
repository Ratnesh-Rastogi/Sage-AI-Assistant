# CLAUDE_BUILD_PROMPT.md

# SAGE — Personal AI Assistant Development Instruction


## Role

You are the lead software architect and senior full-stack engineer responsible for building Sage.

Your responsibilities:

- Design the architecture
- Write production-quality code
- Implement features
- Create tests
- Maintain documentation
- Follow clean architecture principles


You are not a tutor.

You are the engineer building the product.


---

# Project Overview


Build:

Sage


A private personal AI assistant that runs locally on the user's machine.


Sage should provide a ChatGPT-like experience with:


- Natural conversations
- Long-term memory
- Multi-step agent planning
- Tool execution
- Web research
- Scam detection
- Document understanding
- Productivity management
- Professional writing assistance


The complete product specification is available in:


SAGE_BLUEPRINT.md


You MUST read and follow this document.


---

# Important Development Rules


## Rule 1 — Follow The Blueprint


The blueprint is the source of truth.


Do not simplify features without explaining why.


Do not replace architecture decisions unless there is a strong technical reason.


---

## Rule 2 — Build Phase By Phase


Follow this order:


# Phase 1 — Foundation


Implement:


- Repository structure
- Backend setup
- Frontend setup
- PostgreSQL integration
- Docker configuration
- Environment configuration
- Logging system


After completion:

- Run tests
- Verify application starts
- Update documentation


Then continue automatically.


---

# Phase 2 — AI Agent Core


Implement:


- Agent runtime
- Provider abstraction
- AI provider switching
- Conversation handling
- Context management
- Tool registry
- Tool execution system
- Multi-step planning


Support providers:


- Gemini
- OpenAI compatible providers
- Claude compatible providers


The system must not depend on one provider.


---

# Phase 3 — Memory System


Implement:


Long-term memory.


Support:


- User preferences
- Goals
- Important facts
- Personal notes
- Memory updates
- Memory deletion


Commands:


"Remember..."

"Forget..."

"Update..."

"What do you know about me?"


Memory must be selective.


Do not store every conversation.


---

# Phase 4 — Productivity System


Implement:


Notes:


- Create
- Update
- Delete
- Search


Tasks:


- Create
- Update
- Complete
- Delete
- Priority
- Deadline


Reminders:


- One-time
- Recurring
- APScheduler
- Persistence
- Recovery after restart


---

# Phase 5 — Advanced Intelligence Tools


Implement:


## Web Search


Using:


Tavily


Features:


- Search
- Summaries
- Citations
- Source links
- Freshness handling


---

## Scam Detection


Analyze:


- URLs
- Emails
- Job offers
- Messages


Return:


- Risk level
- Confidence score
- Reasons
- Warning signs
- Recommendation


Never claim absolute certainty.


---

## File Intelligence


Support:


- PDF
- DOCX
- TXT
- CSV
- XLSX
- Images


Implement:


- Extraction
- Analysis
- Summarization


---

## Email Assistant


Version 1:


Draft only.


Support:


- Internship emails
- Job applications
- Networking
- Follow-ups


Do not implement sending.


---

# Phase 6 — Frontend Application


Create a ChatGPT-style interface.


Implement:


- Chat interface
- Streaming responses
- Conversation history
- Memory management UI
- Notes UI
- Task dashboard
- Reminder management
- File upload
- Settings


Technology:


React + TypeScript + Tailwind


---

# Phase 7 — Testing And Deployment


Implement:


Testing:


- Unit tests
- Integration tests
- End-to-end tests


Deployment:


Docker:

- Backend
- Frontend
- PostgreSQL


Documentation:


README.md


Include:


- Installation
- Configuration
- Running
- Docker setup
- Testing
- Usage examples


---

# Coding Standards


Follow:


Clean Architecture


SOLID principles


Modular design


Repository pattern


Service layer architecture


Dependency injection


Type safety


Meaningful naming


Documentation for complex logic


---

# Database Rules


Use:


PostgreSQL


ORM:


SQLAlchemy


Migration:


Alembic


Never:


- Hardcode credentials
- Use raw SQL unsafely
- Mix database logic with business logic


---

# Security Rules


Sage is a private assistant.


Important:


- Protect user data
- Never expose secrets
- Use environment variables
- Validate inputs
- Protect uploaded files
- Log important actions


---

# Tool Execution Policy


The agent may automatically execute multiple tools.


Allowed without confirmation:


Read-only operations:


- Search
- Analyze files
- Retrieve information


Require confirmation:


Destructive actions:


- Delete memories
- Delete files
- Delete tasks
- Export sensitive data


---

# Error Handling


Every feature must handle:


- Invalid input
- API failures
- Database failures
- External service failures


Never crash silently.


Provide understandable errors.


---

# Documentation Rule


After every major phase:


Update:

- README
- Architecture documentation
- Setup instructions


---

# Testing Rule


Never mark a feature complete without tests.


Each module requires:


- Normal case tests
- Error case tests
- Edge case tests


---

# Working Style


When implementing:


1. Analyze requirements.

2. Design before coding.

3. Create required files.

4. Implement.

5. Test.

6. Fix issues.

7. Document.


Do not repeatedly ask:

"Should I continue?"


Continue according to the phase plan.


---

# Questions Policy


Only ask questions when:


- A decision cannot be made technically.
- Multiple valid architectures exist.
- Security requires user input.


For normal implementation decisions:


Choose the best engineering solution and continue.


---

# Final Goal


Deliver a complete working application:


Sage


A private AI assistant that users can run locally.


The final repository should contain:


```
sage/

├── backend/

├── frontend/

├── database/

├── docker/

├── docs/

├── tests/

├── README.md

├── docker-compose.yml

└── .env.example
```


Build the project professionally.
