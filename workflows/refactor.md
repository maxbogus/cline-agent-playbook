# Refactoring Workflow

Trigger: `/refactor`

## When to Use
- Code needs structural improvements without changing behavior
- Removing dead code, simplifying logic
- Improving performance bottlenecks

## ⚠️ Critical Rule
**Never change behavior** — the refactored code must produce identical results.

## Procedure

### Step 1: Establish Baseline
1. Read AGENTS.md
2. Run full test suite — must pass before refactoring.
3. Note current test coverage metrics.
4. Document what "correct behavior" means for this code.

### Step 2: Plan Refactoring
1. Identify target code (what needs changing).
2. Break large refactors into smaller steps.
3. For each step: define start state, end state, verification.
4. Plan rollback points.

### Step 3: Make Incremental Changes
1. Make ONE small change at a time.
2. Run tests after each change.
3. If tests break — STOP, revert, reconsider approach.
4. Common refactoring patterns:
   - Extract method/function
   - Rename variables for clarity
   - Replace magic numbers with constants
   - Simplify boolean expressions
   - Remove dead code
   - Consolidate duplicate logic

### Step 4: Verify
```bash
# Python
uv run pytest -v
uv run ruff check .
uv run mypy .

# Node.js
yarn test
yarn lint
```

### Step 5: Commit
```bash
git add <files>
git commit -m "refactor: <what was refactored>

Why: <reason for change>
How: <approach taken>
Verification: tests pass, behavior unchanged"
```

## Output

Provide:
- What was refactored
- Why it was needed
- How behavior was preserved
- Test results confirming no regressions