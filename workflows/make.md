# `/make` — Make Target Runner

Trigger: `/make [target]`

## When to Use

- "How do I run X in this project?" → `/make help`
- "Run the tests" → `/make test-unit`
- "Lint the code" → `/make lint`
- "Show all make commands" → `/make help` (or just `/make`)

## Procedure

### Step 1: Check Makefile exists

```bash
test -f Makefile && echo "OK" || echo "NO_MAKEFILE"
```

If no Makefile in the project root, look up to depth 2:

```bash
find . -maxdepth 2 -name Makefile -not -path '*/node_modules/*' 2>/dev/null
```

If still nothing: tell the user "no Makefile in this project; available
commands are in package.json / pyproject.toml" and offer `yarn <script>`.

### Step 2a: No target specified (or `help`)

Run `make help` and show the output:

```bash
make help
```

Format the output for the user. Explain the structure:
- `<target>` is the name passed to `make <target>`
- `<description>` is the one-line explanation
- All targets are thin wrappers around yarn/uv scripts

### Step 2b: Target specified

Dry-run first to preview:

```bash
make -n <target>
```

If the dry-run output is destructive (contains `rm -rf`, `docker down`,
`reset`, etc.), **ask for explicit confirmation** before running.

Otherwise, run:

```bash
make <target>
```

If `make` exits with non-zero, show the failure to the user and suggest
running `make -n <target>` to see what would have run.

### Step 3: Map user request to target

If the user says "run all checks" but doesn't specify a target, prefer:
- `make check-full` — full quality gate
- `make ci-critical` — fast gate (lint:critical + format:check + type-check)
- `make test-coverage` — tests with coverage report
- `make audit-code` — code health (unused + duplicates + deadcode)

## Output

Always report:
- The exact `make <target>` command run
- Exit code
- For `make help`: the formatted target list

## Anti-patterns

❌ Don't run `make` without arguments (defaults to `help`, but explicit is better).
❌ Don't run `make clean` or `make clean-deep` without confirming with the user.
❌ Don't invent a target — if `make help` doesn't list it, it doesn't exist.
❌ Don't `sudo make install` — use `make install` (or `make install-tools` for global tools).
