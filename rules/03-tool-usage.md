---
paths: ["**/*"]
---

# Tool Usage Rules

## MCP Tools vs Native Tools

### Decision Framework

```
Task type → Preferred tool
─────────────────────────────────────────────────────
Read / create a file                 → Native tools (read_file, write_to_file)
Edit an existing file                → Python heredoc via execute_command
                                       (see `skills/safe-file-edits`)
Rename / move / batch refactor       → Python heredoc via execute_command
Shell commands                       → Native tools (execute_command)
Web scraping / parsing               → MCP (static-parser, browser-parser)
Code quality analysis                → MCP (python-quality)
Document transformation (PDF/DOCX)   → MCP (document-transformer)
Git history (log/diff/show/blame)    → native `git --no-pager ... | head`
                                       (see `skills/git-history-readonly`)
Docker monitoring                    → MCP (docker metrics via mcp-registry)
AI operations (Q&A, summarization)  → MCP (unified ask_question)
Knowledge base                       → MCP (search_knowledge, learn_content)
```

## When to Use `use_skill`

Use `use_skill` for:
- **Repetitive structured tasks** with known patterns (code reviews, test generation)
- **Context-heavy tasks** where skill provides specialized instructions
- **Multi-step workflows** that follow a fixed procedure

Do NOT use `use_skill` for:
- **One-off exploratory tasks** — context switching overhead isn't worth it
- **Tasks requiring real-time knowledge** — skills may have outdated context
- **Security-sensitive operations** — prefer explicit MCP tool calls

## MCP Registry Best Practices

### Available MCP Servers (via mcp-registry)

| Server | Capabilities | Auto-approve |
|--------|-------------|--------------|
| `python-quality` | PEP8 check, PySCN analysis, tests, quality | ✅ check_pep8, run_tests |
| `check-docs` | clinerules sync, health check | ✅ sync, health |
| `document-transformer` | PDF/DOCX/JPG extraction, OCR | ❌ Manual |
| `static-parser` | Web scraping, metadata | ❌ Manual |
| `browser-parser` | JS rendering, screenshots | ❌ Manual |
| `unified` | AI operations, knowledge base | ❌ Manual |

### Using MCP Tools Correctly

1. **Check availability** — MCP tools depend on server running at `localhost:3200`.
2. **Handle errors gracefully** — MCP calls can fail if server is down.
3. **Use appropriate OCR engine**:
   - RapidOCR (default) — faster, neural network
   - Tesseract — CPU-based, better for simple text
4. **Respect rate limits** — don't spam external APIs.

## Native Tool Best Practices

### `execute_command`
- **Always use absolute paths** — never `cd` then run.
- **Use `--no-pager`** for grep/find to avoid interactive prompts.
  For git commands (`git log`, `git diff`, `git show`, `git blame`), always use
  `git --no-pager` or set `GIT_PAGER=cat`. See `~/.cline/skills/git-history-readonly/SKILL.md`.
- **Redirect stderr to stdout** (`2>&1`) when you need to see errors.
- **Chain commands** with `&&` or `||` for safe conditional execution.
- **Avoid `~` or `$HOME`** — always use absolute paths.

### `read_file`
- **For large files** — use `start_line` and `end_line` parameters.
- **For configuration** — read entire file if < 500 lines.
- **Don't re-read** files you've already read in the same session.

### `write_to_file` / editing existing files
- **New file** → `write_to_file` with an absolute path.
- **Existing file** → Python heredoc via `execute_command`; the procedure,
  the atomic-write template and the rollback table are in
  `skills/safe-file-edits`.
- **Do not use** `editor` + `replace_in_file` on an existing file: the exact
  `old_text` match breaks on whitespace and the retry loop hides the failure.
- **Writes are atomic** — temp file in the same directory plus `os.replace`,
  so an interrupted run never leaves a half-written file.

## Error Handling

### When a tool fails:
1. Read the error message carefully.
2. Determine if it's a:
   - **User error** (wrong path, missing dependency) → Fix and retry
   - **System error** (server down, permission denied) → Report to user
   - **Tool limitation** (can't do what was asked) → Propose alternative
3. Never pretend the error didn't happen.

### Tool timeouts:
- Long-running commands (> 30s) — inform user they may take time.
- Docker commands can take 1-5 minutes — be patient.
- If stuck, ask user if they want to cancel.

## Command Permissions

Allowed command patterns:
```
✅ git status, git add, git commit, git push
✅ npm install, npm run build, npm test
✅ yarn install, yarn build, yarn test
✅ docker compose up, docker compose down
✅ python -m pytest, python -m ruff
✅ uv pip install, uv run pytest
✅ make test, make lint, make docker
```

Denied command patterns:
```
❌ rm -rf (without specific path)
❌ curl/wget from untrusted URLs
❌ pip install from untrusted sources
❌ Any command requiring sudo without explicit ask
```

## Workflows: Use Them

When a task matches a known workflow pattern, **offer to use it**:

```
This task looks like a "feature development" workflow.
Should I run /feature to follow the standard procedure?
```

Available workflows (in priority order):
- `/commit` — safe git commit with verification
- `/lint` — run linter and formatter
- `/test` — run test suite
- `/context-update` — refresh AGENTS.md
- `/feature` — full feature development cycle
- `/bugfix` — bug investigation and fix
- `/refactor` — refactoring with safety checks
- `/docs-update` — documentation update procedure