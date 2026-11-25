# Feature Development Workflow

Trigger: `/feature`

## When to Use
- User requests a new feature for an existing system
- Expanding functionality of a project
- Adding new API endpoints, UI components, etc.

## Procedure

### Step 1: Understand Requirements
1. Read AGENTS.md and README.md
2. Clarify with user:
   - What is the input?
   - What is the expected output?
   - What are the acceptance criteria?
   - Are there existing similar features to follow?
3. Identify affected modules and files.

### Step 2: Create Feature Branch
```bash
git checkout -b feature/<short-description>
```
Branch naming: `feature/<ticket-id>-<short-description>` or `feature/<short-description>`.

### Step 3: Write Tests First (TDD)
1. Write failing unit tests for the new feature.
2. Tests should cover:
   - Happy path
   - Edge cases
   - Error conditions
3. Run tests — confirm they fail.

### Step 4: Implement Feature
1. Implement the minimal code to pass tests.
2. Follow existing code conventions.
3. Add type hints (Python) or types (TypeScript).
4. Add docstrings/JSDoc.
5. No shortcuts or placeholders.

### Step 5: Run Quality Gates
```bash
# Python
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run pytest -v

# Node.js
yarn lint
yarn format
yarn test
```

### Step 6: Verify
1. All tests pass.
2. Linter passes.
3. No type errors.
4. Documentation updated (if API changed).

### Step 7: Commit
```bash
git add <files>
git commit -m "feat: add <feature-name>

- Added new feature X
- Implemented Y based on Z
- Tests cover A, B, C cases

Closes #<ticket-id>"
```

### Step 8: Push and Create PR (if applicable)
```bash
git push -u origin feature/<branch-name>
# Create PR via GitHub UI or:
gh pr create --title "feat: add <feature>" --body "..."
```

## Output

Provide summary:
- What was implemented
- What files were changed
- How to test the feature
- Any breaking changes