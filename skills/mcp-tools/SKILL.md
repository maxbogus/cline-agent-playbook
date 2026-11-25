---
name: mcp-tools
description: |
  Call MCP tools via local registry (http://localhost:3200).
  Use when the user wants to parse URLs, check code quality, summarize
  files, transcribe audio, screenshot, or query project history.
  Triggers on: parse url, check pep8, summarize, mcp, registry, mcp tools,
  get commits, analyze history, transcribe, screenshot, transform document,
  search knowledge, ask question, check quality, mypy, jest, tsc, eslint.
allowed-tools: Bash(curl:*) Bash(jq:*) Read
---

# MCP Tools — Index

## Health check
```bash
curl -s --max-time 2 http://localhost:3200/health
```

## List all available tools
```bash
curl -s http://localhost:3200/tools/list | jq -r '.[].name'
```

## Call a tool (JSON-RPC 2.0)
```bash
curl -s -X POST http://localhost:3200/<server>/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"<tool>","arguments":{...}}}'
```

## Tool branches

| Branch | Servers | Use when |
|--------|---------|----------|
| **web** — references/web.md | static-parser, browser-parser | parse URLs, HTTP, JS rendering |
| **code** — references/code.md | python-quality, markdown-tools | lint, type-check, test, complexity |
| **docs** — references/docs.md | document-transformer, summarization, parser-storage | PDF/DOCX, summarize, storage |
| **git** — references/git.md | unified | commits, AI queries, repo history |
| **browser** — references/browser.md | vision, browser-parser | screenshots, OCR, UI automation |

## Fallback

If registry at localhost:3200 is not reachable:
1. Tell user: "MCP registry unavailable. Falling back to native tools."
2. Use native alternatives (curl, grep, python, etc.)
3. Suggest: `cd ~/Repositories/mcp-servers && docker compose up -d`
