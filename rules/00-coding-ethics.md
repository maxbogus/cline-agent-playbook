---
paths: ["**/*.py", "**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.md", "**/*.yml", "**/*.yaml", "**/*.json", "**/*.sh"]
---

# Coding Ethics & Quality Standards

## Core Principles

### 1. Test-Driven Development (TDD)
- **Red-Green-Refactor**: Write a failing test FIRST, then make it pass, then refactor.
- Tests must be written BEFORE implementation for any new functionality.
- Minimum coverage: 80% for critical paths, 100% for security-relevant code.

### 2. Clean Code
- **Single Responsibility**: Each function/module does one thing well.
- **DRY**: Don't Repeat Yourself — extract common patterns.
- **KISS**: Keep It Simple, Stupid.
- Maximum function length: 50 lines. If longer, split it.
- Maximum cyclomatic complexity: 10.

### 3. Documentation
- All public functions MUST have JSDoc (TypeScript) or docstrings (Python).
- All non-obvious code MUST have inline comments explaining WHY, not WHAT.
- README.md required for every project with: setup, usage, architecture, testing.

### 4. Type Safety
- **TypeScript**: Use `strict: true` in tsconfig. No `any`. Use `unknown` + type guards.
- **Python**: Use type hints everywhere. Use Pydantic for data validation.
- **No implicit any** — always specify return types.

### 5. Error Handling
- Never swallow exceptions silently (`except: pass` is forbidden).
- Always log errors with context: `logger.error(f"Failed to X because: {e}")`.
- Use custom exceptions for domain-specific errors.
- Return error responses via proper HTTP status codes.

### 6. Security
- **Never commit secrets** — use `.env` + `.gitignore`.
- **Never use `eval()`** or string interpolation in shell commands.
- Validate ALL user input — never trust external data.
- Use parameterized queries for database operations.

### 7. Async/Await
- All I/O operations MUST be async (file reads, DB queries, HTTP calls).
- Never use `requests` in Python — use `httpx` with async.
- Never use `fetch` with `.then()` chains — use `await`.

## Language-Specific Rules

### Python
- Use `ruff` for linting and formatting.
- Follow PEP 8 with line length 100.
- Use `pytest` for testing.
- Use `uv` as package manager.
- All new projects: Python 3.11+.

### TypeScript/Node.js
- Use `prettier` for formatting, `eslint` for linting.
- Use `strict` TypeScript mode.
- Use `vitest` for testing (React projects) or `jest` (legacy).
- Use `yarn` as package manager.

## Code Review Checklist

Before marking a task complete, verify:
- [ ] Tests pass (`pytest` / `vitest`)
- [ ] Linter passes (`ruff` / `eslint`)
- [ ] Formatter applied (`ruff format` / `prettier`)
- [ ] Type errors resolved (`mypy` / `tsc --noEmit`)
- [ ] No hardcoded secrets
- [ ] Documentation updated if API changed
- [ ] Git commit with meaningful message