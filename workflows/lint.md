# Lint & Format Workflow

Trigger: `/lint`

## When to Use
- Before commits
- After significant code changes
- When linter warnings appear

## Procedure

### Step 1: Run Linter
```bash
# Python - ruff
uv run ruff check .
uv run ruff format --check .  # Check without modifying

# Python - mypy (optional, type checking)
uv run mypy .

# Node.js - eslint
yarn lint
yarn lint --fix  # Auto-fix where possible

# Node.js - prettier
yarn format --check  # Check without modifying
yarn format  # Auto-format
```

### Step 2: Review Linter Output
- **Errors (E)** — MUST fix before proceeding
- **Warnings (W)** — should fix, but not blockers
- **Info (I)** — suggestions, optional

### Step 3: Fix Issues
```bash
# Python - auto-fix
uv run ruff check --fix .

# Node.js - auto-fix
yarn lint --fix
yarn format
```

### Step 4: Manual Review
For issues that can't be auto-fixed:
1. Read the linter message carefully.
2. Understand why this is flagged.
3. Fix appropriately or add inline ignore with justification.

### Step 5: Verify
```bash
# Python
uv run ruff check .   # Should show no errors
uv run ruff format .  # Should show no changes needed

# Node.js
yarn lint   # Should show no errors
yarn format --check  # Should show no changes needed
```

## Common Fixes

| Error | Python Fix | Node.js Fix |
|-------|------------|-------------|
| Import order | `ruff format` handles | `prettier --write` |
| Unused imports | `ruff check --fix` | Manual + eslint fix |
| Missing types | Add type hints | Add TypeScript types |
| Line too long | Break lines | Break lines |
| Trailing whitespace | `ruff format` | `prettier --write` |

## Output

Provide:
- Linter version and configuration used
- Results (errors/warnings found and fixed)
- Any issues that couldn't be auto-fixed