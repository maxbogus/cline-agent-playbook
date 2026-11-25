# Bug Fix Workflow

Trigger: `/bugfix`

## When to Use
- User reports a bug or error
- Tests are failing
- Something isn't working as expected

## Procedure

### Step 1: Reproduce the Bug
1. Read AGENTS.md and README.md
2. Gather information:
   - What is the exact error message?
   - What were the steps to reproduce?
   - What is the expected vs actual behavior?
   - Is there a stack trace or log output?
3. Try to reproduce locally.

### Step 2: Investigate
1. Run the failing code with verbose output.
2. Use `git blame` on the affected file to find when it was last changed.
3. Look at recent commits in `git log --oneline -10 -- <file>`.
4. Identify the root cause (not just the symptom).

### Step 3: Write a Failing Test
Before fixing, write a test that:
- Demonstrates the bug
- Will pass once fixed
- Covers the regression case

### Step 4: Fix the Bug
1. Make the minimal fix necessary.
2. Don't introduce new features or refactor while fixing.
3. Keep the fix focused on the root cause.

### Step 5: Verify
```bash
# Python
uv run pytest -v  # Specific test

# Node.js
yarn test  # Specific test
```

### Step 6: Commit
```bash
git add <files>
git commit -m "fix: <short description>

Root cause: <explanation>
Fix: <what was changed>

Reproduction:
$ <steps to reproduce>
```

## Output

Provide:
- Root cause explanation
- What was changed
- How to verify the fix