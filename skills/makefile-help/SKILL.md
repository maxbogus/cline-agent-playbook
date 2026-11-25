---
name: makefile-help
description: |
  Discover and use Makefile targets in the current project. Use when the user
  asks about Makefile, make targets, build commands, project scripts, or when
  starting work on a new project to enumerate available commands. Triggers on:
  "make", "makefile", "make help", "list commands", "list targets", "show
  commands", "build commands", "project scripts", "what can I run", "available
  targets", "show make", "all make targets".
allowed-tools: Bash(make:*) Bash(grep:*) Bash(awk:*) Read Glob
---

# Makefile Help — Discovery & Execution

## Why this skill exists

Most modern projects have a `Makefile` as a single entry point. The Makefile
in `finance_academy` (and many other `~/Repositories` projects) is a thin
wrapper around `package.json` / `pyproject.toml` scripts — the **single source
of truth is `package.json` / `pyproject.toml`**, not the Makefile.

This skill teaches you to: (1) discover what targets exist, (2) explain them
to the user, (3) run the right one.

## Step 1: Discovery

When starting work on any project, check if a `Makefile` exists in the root
(or any subdirectory up to depth 2):

```bash
ls Makefile 2>/dev/null && echo "found"
```

If found, list targets via the self-documenting `help` target:

```bash
make help
```

If `make help` is not defined, fall back to listing all targets:

```bash
make -qp 2>/dev/null | awk -F':' '/^[a-zA-Z0-9_.-]+:/{print $1}' | sort -u | head -50
```

## Step 2: Reading the help output

Each line is `  <target>                <description>`. Color codes may be
present (green target, white description) — strip them mentally.

**Always show the help table to the user first** when asked "what can I run?",
"show commands", or "list targets". Don't guess.

## Step 3: Running a target

When the user asks for a specific action, **map their request to a Make
target first**, then to a yarn/uv command if no Makefile exists.

| User asks | Check `make help` for | If no Makefile, use |
|-----------|----------------------|---------------------|
| "run tests" | `test`, `test-unit`, `test-coverage` | `yarn test` / `yarn test:unit` |
| "lint" | `lint`, `lint-fix`, `lint-strict` | `yarn lint` |
| "type check" | `type-check` | `yarn type-check` |
| "format" | `format`, `format-fix`, `format-check` | `yarn format` |
| "build" | `build` | `yarn build` |
| "start dev" | `dev` | `yarn dev` |
| "scan secrets" | `secrets`, `secrets-scan`, `gitleaks-detect` | `gitleaks detect` |
| "install" | `install`, `install-tools` | `yarn install` / `uv sync` |
| "clean" | `clean`, `clean-cache`, `clean-deep` | rm build artifacts |
| "check everything" | `check`, `check-full`, `ci`, `validate` | `yarn check:full` |
| "audit code" | `audit-code` | `yarn audit-code` |
| "run docker" | `docker-up`, `docker-down`, `docker-logs` | `docker compose up` |
| "pre-commit hook" | `hooks-install` | `husky install` |
| "python tools" | `py-install`, `py-lint`, `py-test` | `uv run ...` |

## Step 4: Dry-run before executing

For any non-trivial target, preview the commands first:

```bash
make -n <target>     # dry-run — print commands without executing
```

This is especially important for:
- `clean`, `clean-deep` — they delete files
- `hooks-uninstall` — removes git hooks
- `docker-down` — stops containers
- `gitleaks-baseline` — writes a file

Always confirm with the user before running destructive targets.

## Step 5: Running in the right directory

`make` runs in the current shell's CWD. If the project has sub-Makefiles
(e.g. monorepo with `packages/*/Makefile`), navigate first:

```bash
(cd packages/api && make test)
```

## Common conventions in this workspace

Looking at `~/Repositories/`:

- `mlaw-rag`, `mlaw-rag-public`, `evehicle_pred`, `kaggle` — Python+uv, `make reproduce` runs full pipeline.
- `lawcopilot-api`, `lawcopilot` — Python+uv+ruff+pre-commit, `make setup` installs deps + hooks.
- `mcp-servers` — `docker-build-%` and `docker-up-%` patterns for per-service commands.
- `hh-matcher`, `fltrVd` — short Makefiles with 5-10 essential targets.
- `finance_academy` — TypeScript+React+yarn, Makefile wraps `package.json` scripts.

## Anti-patterns

❌ Never invent a make target — always check `make help` first.
❌ Never run `make clean` without `make -n clean` first to see what it does.
❌ Never modify the `Makefile` without also updating the underlying `package.json` script.
❌ Never `sudo make` anything.
❌ Never run `make -j` (parallel) unless you know the recipe is safe — Python uv commands can race.
