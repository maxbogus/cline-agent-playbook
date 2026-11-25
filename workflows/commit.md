# Safe Git Commit Workflow

Trigger: `/commit`

## When to Use
- Before any git commit
- Ensures safe, well-formatted commits

## Procedure

### Step 1: Check Status
```bash
git --no-pager status
```
Review:
- What files changed?
- Are there unintended changes?
- Are all changes necessary for this commit?

### Step 2: Review Changes
```bash
git --no-pager diff
```
Check:
- No secrets committed (API keys, passwords, tokens)
- No debug code left in
- Changes are logically grouped

### Step 3: Stage Files
```bash
git add <specific-files>
# OR for clean staging:
git add -p  # Interactively stage specific hunks
```
Avoid `git add .` unless you know exactly what changed.

### Step 4: Commit with Template
```bash
git commit
```
Use conventional commit format:
```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

Types:
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation
- `style` — formatting (no code change)
- `refactor` — restructuring (no behavior change)
- `test` — adding tests
- `chore` — maintenance

### Step 5: Verify
```bash
git --no-pager log --oneline -3
git --no-pager status  # Should be clean
```

## Anti-Patterns to Avoid

❌ `git commit -m "fixed stuff"`
❌ `git commit -m "WIP"`
❌ `git commit -m "asdfasdf"`
❌ Committing generated files (check .gitignore)
❌ Committing without running tests

## Output

Provide:
- Commit hash
- Commit message
- Files included