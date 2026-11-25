# Code Quality Tools — Lint, Type-Check, Test, Complexity

## python-quality — Python + Multi-language

### check_pep8
Run ruff on Python files (pyproject.toml configured).

```bash
curl -s -X POST http://localhost:3200/python-quality/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"check_pep8","arguments":{"repo_path":"/workspace/my-project","files":["src/app.py"]}}}'
```

### run_tests
Run pytest with JSON output.

```bash
curl -s -X POST http://localhost:3200/python-quality/tools/call \
  -d '{"method":"tools/call","params":{"name":"run_tests","arguments":{"repo_path":"/workspace/my-project","test_paths":["tests/"],"verbose":true}}}'
```

### analyze_pyscn
Python complexity via radon/pyscn: CC, LOC, HAL, maintainability index.

```bash
curl -s -X POST http://localhost:3200/python-quality/tools/call \
  -d '{"method":"tools/call","params":{"name":"analyze_pyscn","arguments":{"repo_path":"/workspace/my-project"}}}'
```

### check_quality
Combined: pep8 + pyscn + test count.

### prioritize_fixes
Rank files by complexity + issue count — suggest where to refactor first.

### run_mypy (TODO — TASK-MEDIUM-002)
Python type checker. **Not yet implemented** — tracked in TASK-MEDIUM-002.

```bash
# Planned:
curl -s -X POST http://localhost:3200/python-quality/tools/call \
  -d '{"method":"tools/call","params":{"name":"run_mypy","arguments":{"repo_path":"/workspace/my-project","files":["src/"]}}}'
```

### run_tsc (TODO — TASK-MEDIUM-002)
TypeScript compiler check (`tsc --noEmit`). Requires `tsconfig.json` in repo.

### run_jest (TODO — TASK-MEDIUM-002)
Run jest tests with JSON output. Requires `jest.config.js` or `jest` in `package.json`.

### run_eslint (TODO — TASK-MEDIUM-002)
ESLint with JSON output. Requires `.eslintrc*` in repo.

## markdown-tools — Markdown analysis

### gather_files
Collect all markdown files in a directory tree.

### extract_code_structure
Parse code blocks from markdown, extract imports, function signatures.

### merge_markdown
Merge multiple `.md` files into one with TOC.

## Quick reference

| Tool | Language | Notes |
|------|----------|-------|
| check_pep8 | Python | ruff-based |
| run_tests | Python | pytest-based |
| analyze_pyscn | Python | radon/pyscn |
| check_quality | Python | combined |
| prioritize_fixes | Python | ranked by complexity |
| run_mypy | Python | TODO (TASK-MEDIUM-002) |
| run_tsc | TypeScript | TODO (TASK-MEDIUM-002) |
| run_jest | JavaScript | TODO (TASK-MEDIUM-002) |
| run_eslint | JS/TS | TODO (TASK-MEDIUM-002) |
