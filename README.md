# Cline agent playbook

Reusable procedures for the Cline coding agent, extracted from a daily
workflow and published as a small, reviewable set.

| Part | Count | What it is |
|---|---|---|
| `skills/` | 9 | `SKILL.md` procedures an agent loads when a task matches |
| `workflows/` | 9 | slash-command playbooks (commit, test, refactor, ...) |
| `rules/` | 4 | global rules the agent follows in every session |

## Install

Cline reads the global configuration directory directly, so the playbook can be
copied in place:

```bash
git clone <this repo> /tmp/cline-agent-playbook
cp -r /tmp/cline-agent-playbook/skills /tmp/cline-agent-playbook/workflows \
      /tmp/cline-agent-playbook/rules ~/.cline/
```

Or cherry-pick a single item: copy `skills/<name>/` (or one file from
`workflows/` or `rules/`) into `~/.cline/`.

## What is deliberately missing

This repository contains only items marked `public` in `registry.json`.
The author's local configuration also holds `sanitize` items (generic idea,
but with personal paths or hardware details) and `private` items (company
specific). Both stay in a separate private repository and are not licensed for
redistribution here.

## Checks

```bash
make check     # registry coverage, frontmatter, forbidden paths and markers
make status    # git status
```

`registry.json` is the machine-readable index: every skill, workflow and rule
is listed with its visibility and one-line description.

## License

MIT, see `LICENSE` and `NOTICE`.
