# Context Update Workflow

Trigger: `/context-update`

## When to Use
- AGENTS.md is missing or outdated
- Project structure has changed
- New services/endpoints added
- Configuration changes not reflected in docs
- Starting a task and AGENTS.md doesn't exist

## Procedure

### Step 1: Check if AGENTS.md Exists
```bash
ls -la AGENTS.md 2>/dev/null || echo "NOT FOUND"
ls -la .clinerules/00-project-map.md 2>/dev/null || echo "NOT FOUND"
```

### Step 2: If AGENTS.md Exists — Review and Update
Read current AGENTS.md and compare with reality:
```bash
# Check file structure
ls -la

# Check recent changes
git log --oneline -20

# Check for new services
git diff --name-only HEAD~5..HEAD
```

Update sections:
- **Architecture** — if services changed
- **Structure** — if directories added/removed
- **Commands** — if new make targets, scripts added
- **Key Files** — if critical files renamed/moved
- **Gotchas** — if new pitfalls discovered

### Step 3: If AGENTS.md Doesn't Exist — Create It
Create at workspace root with template:

```markdown
# Project Map

## Overview
Brief description of the project (1-3 sentences).

## Architecture
- Tech stack: ...
- Key services: ...
- Data flow: ...

## Structure
```
/src         — source code
/tests       — test suite
/docs        — documentation
/config      — configuration
```

## Commands
| Command | Description |
|---------|-------------|
| `make setup` | Initial setup |
| `make test` | Run tests |
| `make lint` | Run linter |

## Key Files
- `src/main.py` — entry point
- `config.py` — configuration

## Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection | Yes |
| `API_KEY` | External API key | Yes |

## Gotchas
- Database requires migrations after schema changes
- Tests must pass before commit
- ...

## Recent Changes
- `<date>` — `<summary of last significant change>`
```

### Step 4: Verify and Commit
```bash
git add AGENTS.md
git commit -m "docs: update AGENTS.md

- <list of updates>
- Verified accuracy against current codebase"
```

## Output

Provide:
- Whether AGENTS.md was created or updated
- Summary of changes
- Recommendation for team (e.g., "Add AGENTS.md update to pre-commit hook")