---
name: git-history-readonly
description: |
  View git history — ANY git command, including git log/diff/show/blame and
  git -C <path> ... variants. Use before running git to avoid pager hangs and
  silent pipe failures. Triggers on: git, git log, git diff, git show, git blame,
  git status, git -C, recent commits, what changed, history, changelog.
allowed-tools: Bash(git:*) Bash(head:*) Bash(tail:*) Bash(grep:*) Bash(wc:*) Bash
---

# Git History — Read-Only Commands

## Always Set Environment (first line of every session)

```bash
export GIT_PAGER=cat PAGER=cat GIT_TERMINAL_PROMPT=0
```

Without this, even `git status` or `git -C subdir diff` can hang on pager.

## The Golden Rules

1. **Always pass `--no-pager` explicitly** — `GIT_PAGER=cat` env is not enough.
   `git --no-pager log ...` wins over `git log ...`.
2. **Always pipe to `head`** for `git log` and `git show` — full output can be megabytes.
3. **`git -C <path>` requires `--no-pager`** — same pager issue, often missed.
3. **Use `--oneline` or `--stat`** for overview — avoid `-p` (full patches) without limit.

## The Fix

If a git command hangs on pager, abort and retry with:

```bash
# Add --no-pager to any git subcommand
git --no-pager log --oneline -n 20
git --no-pager diff HEAD~1 HEAD
git --no-pager show <sha> --stat

# Or set the environment variable once (still add --no-pager when you remember it)
export GIT_PAGER=cat
git --no-pager log --oneline -n 20 | head
```

## Command Templates

### Recent commits (one line each)

```bash
git --no-pager log --oneline -n 20
```

### Diff of last N commits

```bash
git --no-pager diff HEAD~3 HEAD
```

### Changes to a specific file

```bash
git --no-pager log --oneline -- apps/backend/app/models/user.py
git --no-pager diff HEAD~5 HEAD -- apps/backend/app/models/user.py
```

### Show a specific commit

```bash
git --no-pager show abc1234 --stat        # stat summary
git --no-pager show abc1234 --name-only   # files changed
git --no-pager show abc1234 -p | head -80 # first 80 lines of patch
```

### Blame a file

```bash
git --no-pager blame path/to/file.ts | head -30
git --no-pager blame -L 50,70 path/to/file.ts  # lines 50-70 only
```

### Search commit messages

```bash
git --no-pager log --oneline --all --grep="fix\|bug" -n 20
```

### Files changed in a commit

```bash
git --no-pager show --stat --name-only abc1234
```

### Branches

```bash
git --no-pager branch -a
git --no-pager log --oneline --graph --all -n 20
```

### Subdirectory repos (git -C)

```bash
git --no-pager -C /path/to/repo log --oneline -n 10
git --no-pager -C /path/to/repo status --short
git --no-pager -C /path/to/repo diff --name-only
```

## Anti-Patterns (NEVER do these)

- ❌ `git log` (no flags, no pager guard) — hangs on `less`
- ❌ `git log -p` (full patches) without `| head` — megabytes of output
- ❌ `git diff` (no `--no-pager`) — same pager problem
- ❌ `git show` (no `--no-pager`) — same pager problem
- ❌ `git difftool` / `git mergetool` — interactive, not suitable for scripts
- ❌ Piping `git log` output to `wc -l` without `--no-pager` — pager still blocks before wc sees data
- ❌ `git -C <path> <anything>` without `--no-pager` — same pager hang as plain git
- ❌ `git checkout -- <file>` — silently discards uncommitted changes; use `cp` to save first
- ❌ `git reset --hard` without `git --no-pager status --short` first — irreversible

## When to Use Which Format

| Goal | Command |
|------|---------|
| "What did I change recently?" | `git --no-pager log --oneline -n 20` |
| "Show me the diff" | `git --no-pager diff HEAD~1 HEAD` |
| "Who touched this line?" | `git --no-pager blame file.ts \| head -20` |
| "What files changed in this commit?" | `git --no-pager show <sha> --stat --name-only` |
| "Find commits about X" | `git --no-pager log --oneline --grep="X" -n 20` |
| "How did this branch evolve?" | `git --no-pager log --oneline --graph -n 30` |

## Pro Tip: Pre-set GIT_PAGER

At the start of any session or script, set it once:

```bash
export GIT_PAGER=cat
export PAGER=cat
```

This makes every git command pager-free automatically, without needing `--no-pager` every time.
