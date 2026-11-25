---
paths: ["**/*"]
---

# Context Management Rules

## Golden Rule: AGENTS.md First

**Before starting ANY task**:

1. **Read the project's AGENTS.md** (or PROJECT.md) if it exists in the workspace root.
2. If it does not exist — say so once, offer to create it from the template, and ask
   whether to proceed without it. Record the answer as an assumption instead of
   asking again later.
3. If it exists but is outdated — name the stale sections in the response and
   continue. Do not re-derive the whole project map before the task.

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

Budget per task, not per session: aim for under 20% of the context window on
reading, and keep room for the answer.

1. **Read only what's needed** — not the entire codebase.
2. **Targeted ranges** for files over roughly 300 lines:
   `read_file(path, start_line, end_line)`.
3. **Summarize long files** — two accurate lines beat a full dump.
4. **Lazy-load skills** — activate a skill only when the task matches its triggers.
5. **Don't re-read unchanged files** — but do re-check what changed (see Context
   Freshness).

## Project State Block

Keep a compact state for long tasks — ten lines, not a summary of the conversation:

```
goal:     what "done" means, one sentence
branch:   current branch and its base
facts:    verified claims with a source, e.g. "tests use vitest (package.json:12)"
open:     questions blocking the work
assumed:  decisions taken without confirmation, and why
```

Update it when a fact changes, and delete facts that turned out wrong instead of
appending corrections. The block is the handoff artifact when a session ends.

## Context Freshness

Facts decay. Treat as stale and re-check before relying on them:

- a file read more than ~10 turns ago and written since;
- a dependency version, test result or error message from earlier in the session;
- anything the user corrected or contradicted later;
- branch and commit state after any git mutation.

Re-read the specific range and re-run the narrow command, not the whole file and
not the whole suite.

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
- **Never assume** which branch to commit to — state the branch you are on; ask
  only if it differs from the one the task started from.
- **Never assume** credentials/secrets are available — ask.