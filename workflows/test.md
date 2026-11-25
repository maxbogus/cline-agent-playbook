# Test Workflow

Trigger: `/test`

## When to Use
- Running tests before commits
- Debugging failing tests
- Writing new tests

## Procedure

### Step 1: Identify Test Scope
```bash
# Python
uv run pytest --collect-only  # List all tests

# Node.js
yarn test -- --listTests  # List all tests
```

### Step 2: Run Tests
```bash
# Python - run all
uv run pytest -v

# Python - run specific file
uv run pytest tests/test_file.py -v

# Python - run with coverage
uv run pytest --cov=. --cov-report=term-missing

# Node.js - run all
yarn test

# Node.js - specific file
yarn test --testPathPattern=test_file
```

### Step 3: Analyze Failures
For each failing test:
1. Read the test code — understand what it's testing.
2. Run the test with verbose output: `pytest -vv --tb=long`
3. Identify whether failure is:
   - **Test bug** — test is wrong
   - **Code bug** — implementation is wrong
   - **Environment bug** — missing deps, wrong config

### Step 4: Fix Issues
- If test bug: fix the test
- If code bug: fix the code, then verify test passes
- If environment: report to user

### Step 5: Write New Tests
For new features:
1. Write test BEFORE implementation (TDD if applicable).
2. Tests should be:
   - Deterministic (no flakiness)
   - Isolated (no dependencies between tests)
   - Focused (one assertion per test ideally)
   - Readable (clear names, setup/teardown)

### Step 6: Final Verification
```bash
# Python
uv run pytest -v --tb=short

# Node.js
yarn test --coverage
```

## Output

Provide:
- Test results summary (passed/failed)
- Any new tests added
- Any fixes made