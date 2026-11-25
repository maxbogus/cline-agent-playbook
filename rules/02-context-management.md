---
paths: ["**/*"]
---

# Context Management Rules

## Golden Rule: AGENTS.md First

**Before starting ANY task**, you MUST:

1. **Read the project's AGENTS.md** (or PROJECT.md) if it exists in the workspace root.
2. If AGENTS.md does NOT exist:
   - Inform the user that it's missing
   - **Offer to create it** using the template
   - Do NOT proceed with the task until context is established (or explicitly ask for permission to proceed without it)
3. If AGENTS.md exists but is outdated:
   - Note this in your response
   - Proceed with the task, but flag what needs updating

## What AGENTS.md Should Contain

A proper AGENTS.md (or .clinerules/00-project-map.md) contains:

```
# Project Map

## Architecture
- Brief description of the system
- Tech stack (Python 3.11, FastAPI, PostgreSQL, Redis, ...)
- Key services and their responsibilities

## Structure
/frontend    — React app
/backend     — FastAPI app  
/db          — Migrations, schemas
/tests       — Test suites
/ai          — AI-specific logic, prompts

## Commands
- `make setup`  — Initial setup
- `make test`   — Run tests
- `make lint`   — Run linter
- `make docker` — Docker compose up

## Key Files
- `config.py`    — Main configuration
- `models.py`    — Database models
- `api/v1/`      — API routes

## Gotchas
- Sensitive endpoints require API key
- Database requires migrations after schema changes
```

## Context Loading Priority

When loading context, follow this order:

1. **AGENTS.md** (project map) — MUST READ FIRST
2. **README.md** — setup, architecture, getting started
3. **Architecture docs** (ai/, docs/, ARCHITECTURE.md)
4. **Existing tests** — understand expected behavior
5. **Recent git history** — `git --no-pager log --oneline -10` to understand recent changes
6. **Open issues/PRs** — if relevant to the task

## Requesting Clarification

If the context is insufficient, **ask before assuming**:

```
I need more context to proceed:
1. Which service should I modify — api-gateway or recommendations?
2. Is this for production or development environment?
3. Should I follow the existing pattern in `src/services/` or create new module?
```

**Do NOT make assumptions** about:
- Which environment (prod/dev/staging)
- Which version of a dependency to use
- Whether to modify shared infrastructure
- Security requirements without explicit mention

## Context Budget Management

To avoid token bloat:

1. **Read only what's needed** — not entire codebase.
2. **Use specific paths** — `read_file(path, start_line, end_line)` for large files.
3. **Summarize long files** — instead of dumping full content.
4. **Lazy-load skills** — if a skill exists for the task type, activate it.
5. **Don't re-read what you've already seen** — remember context within session.

## Workflow-Specific Context

For specific task types, prioritize these:

| Task Type | Primary Context | Secondary |
|-----------|-----------------|-----------|
| Feature development | AGENTS.md → existing similar feature | tests, API docs |
| Bug fix | AGENTS.md → failing test | error logs, git blame |
| Refactoring | AGENTS.md → affected modules | tests, type definitions |
| Research | AGENTS.md → architecture | external docs |
| Docs update | existing docs → changes | PR/issue description |

## Never Assume

- **Never assume** the user wants production changes without asking.
- **Never assume** a file hasn't changed since last read — re-read if task spans multiple turns.
- **Never assume** which branch to commit to — always confirm.
- **Never assume** credentials/secrets are available — ask.