---
name: safe-file-edits
description: |
  Edit, replace, rename, refactor, or move files. Use before any file mutation
  (including cp/mv/sed) to avoid silent failures. Triggers on: edit, replace,
  modify, patch, sed, in-place, rename, refactor, move, restructure, change.
allowed-tools: Bash(python3:*) Read Write
---

# Safe File Edits — Python First

## CRITICAL: Do NOT Use the `editor` Tool

**The `editor` tool with `replace_in_file` is FORBIDDEN for existing files.**
It requires exact `old_text` match — any whitespace difference causes
"Editor operation failed: Parameter `old_text` is required" failure.

**For ALL existing file edits: use Python heredoc via `execute_command`.**
This is non-negotiable.

## The Rule

**Never use `sed -i`, `awk`, `perl -i`, or any shell in-place tools for file edits.**
Use Python via a quoted heredoc in `Bash`.

Shell in-place tools fail on: multiline replacements, special chars (`$`, backticks, quotes),
Unicode, and patterns that span lines. Python handles all of these correctly.

## Refactoring Safety (rename, move, split)

Before any multi-step refactor (e.g. `a.py` → `b.py` + update all imports):

```bash
# 1. Save original (insurance)
cp <old> /tmp/<old>.original

# 2. Verify insurance exists BEFORE deleting anything
ls -la /tmp/<old>.original

# 3. Take git snapshot (read-only, no pager)
git --no-pager -C <repo> status --short

# 4. Create new file
cp <old> <new>

# 5. CHECK step 4 (this is the step I missed last time)
ls -la <new>

# 6. ONLY if step 5 succeeded → update references
python3 << 'PYSUB'
from pathlib import Path
import re

old_name = "<old>"
new_name = "<new>"
files = [list of file paths]

for fp in files:
    p = Path(fp)
    content = p.read_text()
    new_content = content.replace(old_name, new_name)
    if new_content != content:
        p.write_text(new_content)
        print(f"updated: {fp}")
print(f"Done.")
PYSUB

# 7. ONLY if step 6 is clean → delete original
rm <old>

# 8. Verify imports work
PYTHONPATH=<repo_parent> python3 -c 'from <package>.<new> import ...'
```

**Rule:** never delete (step 7) before step 5 succeeds. Rollback = `cp /tmp/<old>.original <old>`.

## Algorithm

1. **Read** the file first — always. Use `read_file` to confirm exact content.
2. **Build the replacement** in Python using `str.replace()` or regex.
3. **Write** with Python, confirm the result.
4. **Verify** the change was applied.

## Template: Simple Text Replace

```bash
python3 << 'PYEOF'
from pathlib import Path

path = Path("/abs/path/to/file.py")
text = path.read_text()

# Replace only the FIRST occurrence (safer)
new_text = text.replace("EXACT_OLD_STRING", "EXACT_NEW_STRING", 1)

# Or replace all occurrences
# new_text = text.replace("OLD", "NEW")

if new_text == text:
    print("ERROR: pattern not found")
    exit(1)

path.write_text(new_text)
print(f"OK: {len(new_text)} bytes written")
PYEOF
```

## Template: Line-Range Replace

When you need to replace specific lines (read file first to get line numbers):

```bash
python3 << 'PYEOF'
from pathlib import Path

path = Path("/abs/path/to/file.py")
lines = path.read_text().splitlines()

# Replace lines 10-15 (0-indexed: indices 9-14)
lines[9:15] = [
    "new line 1",
    "new line 2",
    "new line 3",
]

path.write_text("\n".join(lines) + "\n")
print("OK")
PYEOF
```

## Template: Full Rewrite (complex changes)

When the replacement is complex, replace the entire file:

```bash
python3 << 'PYEOF'
from pathlib import Path

path = Path("/abs/path/to/file.py")
original = path.read_text()

# Build new content (full rewrite)
new_content = original.replace("OLD_BLOCK", """NEW_BLOCK
WITH MULTIPLE LINES
AND "QUOTES"
""")

path.write_text(new_content)
print(f"OK: {len(new_content)} bytes")
PYEOF
```

## Anti-Patterns (NEVER do these)

- ❌ `sed -i 's/old/new/' file` — fails on special chars, multiline, Unicode
- ❌ `echo "new" >> file` — appends, not replaces
- ❌ Shell `cat` heredoc without quotes — interpolates `$` and backticks
- ❌ `awk '{gsub(/old/,"new")}1' file > tmp && mv tmp file` — fragile, loses permissions
- ❌ Inline regex in `sed` — complex patterns belong in Python `re` module
- ❌ `rm <old>` before verifying `ls <new>` succeeded — silent partial refactor
- ❌ Multiple `sed -i` in sequence without `grep` check between — failures compound
- ❌ `git checkout -- <file>` to "revert" — overwrites uncommitted edits without backup; use `cp /tmp/*.original` instead

## Tool Selection Table

| Situation | Tool |
|-----------|------|
| Creating a **new** file | `write_to_file` (Write) |
| Replacing text in an **existing** file | **Python heredoc** via `execute_command` |
| Complex / multiline / conditional replace | **Python heredoc** via `execute_command` |
| Adding content to end of file | `cat >>` with heredoc is OK |
| Changing specific lines | Python line-range template |
| Multi-file batch refactor | Python heredoc loop |
| **NEVER** — existing file | `editor` tool with `replace_in_file` |
| **NEVER** — any file | `sed -i`, `awk`, `perl -i` |

## Verification

After any edit, always verify:
1. Run the relevant linter: `uv run ruff check /path` (Python) or `yarn lint` (TS)
2. Check the diff: `git diff /path`
3. If it looks wrong, `git checkout /path` and redo with Python
