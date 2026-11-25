---
name: write-kaggle-benchmarks
description: Minimal workflow for creating and pushing Kaggle Benchmark tasks via `kaggle b` CLI (2.2.4+). Use when the user wants to write a benchmark task, run it on models, check status, download results, or publish it. Triggers on: kaggle b init, kaggle b t push, kaggle b t run, kaggle b t status, kaggle b t download, kaggle b t publish, kaggle_benchmarks, kbench, MODEL_PROXY_API_KEY.
allowed-tools: Bash(kaggle:*) Bash(uv:*) Bash(python3:*) Bash(ls:*) Read Write
version: 1.1.0
---

# Write Kaggle Benchmarks (minimal)

> CLI-side workflow for `kaggle benchmarks`. Task-writing syntax
> (decorators, assertions, ChatRoom, multimodal) lives in the sibling
> skill `kaggle-benchmarks` — do NOT duplicate it here.

## One-shot happy path

```bash
kaggle b init -y                                    # creds + .env + reference.md
uv run --with kaggle-benchmarks python task.py      # local validation (must produce *.run.json)
ls -1 *.run.json                                    # proof runs were recorded
kaggle b t push <slug> -f task.py --wait            # upload
kaggle b t models                                   # list available models
kaggle b t run <slug> -m <model> --wait             # execute
kaggle b t status <slug>                            # per-model state
kaggle b t download <slug> -o results               # fetch outputs
```

## Required task-file skeleton

```python
# %%
import kaggle_benchmarks as kbench

# %%
@kbench.task(name="<slug>")                         # slug MUST equal the directory name
def my_task(llm):
    response = llm.prompt("...")
    kbench.assertions.assert_in("expected", response)

my_task.run(kbench.llm)                             # without this, the task is a silent no-op
```

- jupytext percent format (`# %%` cells).
- No imports of `neuro_slop.*` or local modules — Kaggle runtime has none.
- Returning tasks need a return annotation (`-> float`, `-> dict`, `-> bool`).

## Pacing — one step at a time

Do **not** chain the full pipeline. After every command:
1. Show relevant output.
2. Stop and wait for the user.
3. Only proceed when the user says "continue", "next", or names the next step.

The exception is when the user explicitly asks for "the whole pipeline" — then
summarise the planned chain and ask for a single confirmation.

## Gotchas (silent failures)

| Symptom | Cause | Fix |
|---|---|---|
| Push succeeds but no runs | Missing `task_fn.run(...)` at module level | Add the `.run(kbench.llm)` call |
| `python task.py` fails with auth error | `MODEL_PROXY_API_KEY` expired | `kaggle b auth -y` to refresh |
| Push fails: "slug mismatch" | `<slug>` arg != `@kbench.task(name=...)` value (normalised) | Match the names exactly |
| Re-push silently detached datasets | Repeated `-d` flags not passed on re-push | Always repeat the full `-d` list |
| `download -s` skipped cached runs | Without `-f`, cached dirs are kept | Re-run with `-f -s` |
| Multiple values not accepted | `-m a b` (space) is invalid | Use `-m a -m b` (repeat) |
| `publish` is irreversible | No unpublish in CLI | Only run after explicit user confirmation |

## CLI command tree (kaggle CLI 2.2.4)

```
kaggle b
├── auth              — refresh MODEL_PROXY_* in .env
├── init              — auth + .env + example_task.py + reference.md
└── t (tasks)
    ├── push          — upload task (-f FILE, --wait, -d owner/ds)
    ├── run           — execute (-m MODEL, --wait)
    ├── list          — show tasks (--name-regex, --status)
    ├── status        — per-model runs
    ├── download      — outputs (-o DIR, -s sources, -f force)
    ├── log           — execution logs (sequential, not interleaved)
    ├── publish       — make public (irreversible; --no-publish-backing-notebook)
    ├── models        — available models
    └── delete        — not supported server-side yet
```

Notes:
- `LLMS_AVAILABLE` in `.env` is a **curated subset** for local dev. The full
  catalog is at `kaggle b t models`; `kaggle b t run` uses any of them on
  Kaggle infra.
- `init`/`auth` append to `.env` (last-wins), so the file accumulates dupes
  over time — trim periodically.
- `quota` is in upstream docs but missing in 2.2.4 → check the web UI.

## Project wiring (this repo: neuro-slop-detector)

- Pipeline: `scripts/benchmark_task.py` wraps the CLI and enforces the `-d`
  invariant (no push without `-d`, because re-push without `-d` detaches
  attached datasets — see Gotchas above).
- Targets: `make benchmark-init|build|push|run|status|download|publish`.
- Task templates: `content/benchmarks/<slug>/task.py.j2`.
- Every run is logged to `docs/ledger/benchmarks.jsonl` (append-only) and
  summarised in `docs/BENCHMARKS.md`.
- All publishing targets are `manual_only` in the DAG registry. Never
  schedule push/run/publish — humans run them with `--yes`.

## Token hygiene

- Kaggle token: `~/.kaggle/access_token` (chmod 600). Never print or commit.
- `MODEL_PROXY_*` vars live in gitignored `.env` only.
- No file under `data/` or `docs/` may contain the raw token string (the literal `KGAT_` prefix that begins the access token).

## Anti-patterns

- ❌ Push / run / publish from CI or DAG without a human in the loop.
- ❌ Print or commit `MODEL_PROXY_API_KEY` / `access_token`.
- ❌ Import `neuro_slop.*` in a task file (won't exist on Kaggle).
- ❌ Skip `python task.py` validation before `push` — silent no-ops are
  expensive to debug after the round-trip.
- ❌ Re-push without the full `-d` list.

## See also

- `~/.cline/skills/kaggle-benchmarks/SKILL.md` — task-writing SDK reference
  (vendored upstream, decorators, assertions, multimodal).
- `~/.cline/skills/kaggle-cli/SKILL.md` — `kaggle competitions` / `kernels`
  safety (token, disk, kernel-push modes). Different commands, same CLI.
- `~/.clinerules/08-contracts-and-artifacts.md` §4 — benchmark task contract
  (`@kbench.task`, `.run(`, return annotation, jupytext format).
- `~/.clinerules/33-mlops-lab.md` — why push/run/publish are `manual_only`.
