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

### Step 2: Find the Root Cause (method, not intuition)

Work from the smallest reproduction outward. Fix the first place where a value
diverges from the expected one, not the first place where it becomes visible.

1. **Minimal reproduction.** Shrink the input and the steps until the bug still
   reproduces: one test case or a five-line `python -c`. A bug you cannot
   reproduce in isolation is not yet understood.
2. **Bisect the change.** When the bug appeared somewhere in the last N commits
   and there is no obvious suspect: `git bisect start`, `git bisect bad`,
   `git bisect good <sha>`, `git bisect run <test command>`.
3. **Trace the data.** Log the value at each boundary (input → parser → model →
   response). The first boundary where the actual value differs from the expected
   one is the defect site; everything downstream is a consequence.
4. **One hypothesis per iteration.** Change one thing, re-run the minimal
   reproduction. Two changes at once and you learn nothing about either.
5. **State the cause in one sentence.** "The cache lookup uses the raw key while
   the writer normalises it, so the second read misses." If the sentence does not
   come out, the cause has not been found yet.

`git --no-pager blame -L <start>,<end> <file>` and
`git --no-pager log --oneline -10 -- <file>` show when the code changed. They
show history, not the cause.

### Step 3: Write a Failing Test First

Before fixing, write a test that:

- Fails on the current code and passes after the fix — run it both ways
- Reproduces the minimal case from Step 2, not the full user scenario
- Is named after the defect: `test_<unit>_<wrong_behaviour>_<expected>`
- Stays in the suite as the regression guard; do not delete it after the fix

If the failure is in the test or the environment rather than in the code, this is
not a `/bugfix`. Run `/test` — its Step 3 classifies program, test and
environment failures — and fix the failing layer first.

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