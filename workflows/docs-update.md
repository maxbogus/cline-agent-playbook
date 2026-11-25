# Documentation Update Workflow

Trigger: `/docs-update`

## When to Use
- README needs updating
- API documentation is stale
- Architecture docs don't match code
- Adding inline comments

## Procedure

### Step 1: Identify Documentation Scope
1. Read AGENTS.md and README.md
2. Identify:
   - Which docs need updating?
   - What changed recently that isn't documented?
   - Are there undocumented APIs or features?

### Step 2: Gather Changes
1. Check recent commits: `git --no-pager log --oneline -20`
2. Identify features/changes not yet documented.
3. Check for TODO/FIXME comments that should be addressed.
4. Review open issues for documentation requests.

### Step 3: Update Documentation
For each document:
1. Read current version.
2. Make targeted updates (don't rewrite entirely).
3. Check:
   - Code examples still work
   - Commands are accurate
   - Links are valid
   - Formatting is consistent

### Step 4: Verify
```bash
# Check markdown links (if available)
markdown-link-check README.md

# Check spell check (if available)
typos .

# Verify no broken code examples
# Run the documented commands
```

### Step 5: Commit
```bash
git add docs/ README.md CHANGELOG.md
git commit -m "docs: update <what was updated>

Changes:
- <list of updates made>
- Verified code examples work"
```

## Output

Provide:
- List of documents updated
- Summary of changes
- Any follow-up documentation needed