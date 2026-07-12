# PROJECT_STRUCTURE.md

# Sage AI Assistant — Project Structure


## 1. Overview

Sage follows a modular clean architecture.

The project is divided into:

- Backend
- Frontend
- Database
- AI Agent Core
- Tools
- Tests
- Documentation
- Deployment


The structure should support:

- Easy maintenance
- Adding new tools
- Provider switching
- Testing
- Future scaling


---

# 2. Root Directory Structure


```
Sage-AI-Assistant/

│
├── backend/
│
├── frontend/
│
├── database/
│
├── tests/
│
├── docs/
│
├── docker/
│
├── storage/
│
├── .env.example
│
├── .gitignore
│
├── docker-compose.yml
│
├── README.md
│
└── LICENSE
```


---

# 3. Backend Structure


```
backend/

├── app/

│
├── main.py
│
├── api/
│
├── core/
│
├── config/
│
├── database/
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── agent/
│
├── tools/
│
├── providers/
│
├── memory/
│
├── scheduler/
│
├── utils/
│
└── logging/
```


---

# 4. API Layer


Location:

```
backend/app/api/
```


Responsible for:


- HTTP routes
- Request validation
- Response formatting


Contains:


```
api/

├── routes/

│   ├── chat.py

│   ├── memory.py

│   ├── notes.py

│   ├── tasks.py

│   ├── reminders.py

│   └── files.py


└── dependencies.py
```


API layer must not contain business logic.


---

# 5. Agent Core Structure


Location:

```
backend/app/agent/
```


Purpose:

The brain of Sage.


Structure:


```
agent/

├── planner/

│   └── planner.py


├── runtime/

│   └── agent.py


├── context/

│   └── context_manager.py


├── memory/

│   └── memory_manager.py


└── execution/

    └── tool_executor.py
```


Responsibilities:


Planner:

Decides steps.


Runtime:

Controls conversations.


Context Manager:

Handles information given to the AI.


Tool Executor:

Runs tools safely.


---

# 6. Tools Structure


Location:


```
backend/app/tools/
```


Each tool must be independent.


Structure:


```
tools/

├── base.py

├── registry.py

│
├── web_search/

├── scam_detection/

├── file_processing/

├── email_writer/

├── notes/

├── tasks/

└── reminders/
```


Every tool must contain:


```
tool.py

schemas.py

service.py

tests/
```


---

# 7. Provider System


Location:


```
backend/app/providers/
```


Purpose:

Allow AI model switching.


Structure:


```
providers/

├── base.py

├── gemini.py

├── openai.py

└── claude.py
```


All providers implement the same interface.


---

# 8. Database Structure


Location:


```
database/
```


Contains:


```
database/

├── migrations/

├── seeds/

└── backups/
```


PostgreSQL is the primary database.


---

# 9. Frontend Structure


```
frontend/

├── src/

│
├── components/

├── pages/

├── hooks/

├── services/

├── contexts/

├── types/

├── utils/

└── styles/
```


Technology:


- React
- TypeScript
- TailwindCSS


---

# 10. Testing Structure


```
tests/


├── backend/

│
├── frontend/

│
├── integration/

│
└── e2e/
```


Testing required for every major feature.


---

# 11. Docker Structure


```
docker/


├── backend/

├── frontend/

└── postgres/
```


Root:


```
docker-compose.yml
```


Controls all services.


---

# 12. Documentation Structure


```
docs/


├── SAGE_BLUEPRINT.md

├── CLAUDE_BUILD_PROMPT.md

├── PROJECT_STRUCTURE.md

├── API_DOCUMENTATION.md

└── DEVELOPMENT_GUIDE.md
```


---

# 13. Coding Rules


The developer must:


- Keep modules independent
- Avoid duplicate logic
- Use meaningful names
- Write tests with features
- Update documentation
- Follow clean architecture


---

# 14. Adding New Features


New features should follow:


```
Feature

↓

Tool/Service

↓

Repository

↓

Database

↓

API

↓

Frontend

↓

Tests

↓

Documentation
```


---

# 15. Final Rule


Do not create random files in the root directory.

Every file must have a clear responsibility.

Sage should remain modular and easy to extend.
