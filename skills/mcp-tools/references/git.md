# Git & Repo Tools — History, AI, Knowledge

## unified — Multi-domain MCP server

### get_commits
```bash
curl -s -X POST http://localhost:3200/unified/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"get_commits","arguments":{"repo_path":"/workspace/my-project","max_count":20,"author":"..."}}}'
```

**Returns:** array of `{hash, message, author, date, files_changed}`

### get_stats
Git statistics: commits/day, top authors, lines changed.

### analyze_history
Deep analysis: detect merge patterns, refactoring waves, productivity trends.

### list_repositories
List all git repos under `/workspace`.

### extract_structure
Extract project structure: directories, file types, dependencies.

## AI-augmented tools (unified)

### ask_question
Ask a natural-language question about the codebase. Uses AI gateway.

```bash
curl -s -X POST http://localhost:3200/unified/tools/call \
  -d '{"method":"tools/call","params":{"name":"ask_question","arguments":{"question":"How does auth work?","repo_path":"/workspace/my-project"}}}'
```

### learn_content
Store a fact or note about the codebase in the knowledge base.

```bash
curl -s -X POST http://localhost:3200/unified/tools/call \
  -d '{"method":"tools/call","params":{"name":"learn_content","arguments":{"content":"Auth uses JWT with 24h expiry","context":"token system","repo_path":"/workspace/my-project"}}}'
```

### search_knowledge
Query the internal knowledge base.

```bash
curl -s -X POST http://localhost:3200/unified/tools/call \
  -d '{"method":"tools/call","params":{"name":"search_knowledge","arguments":{"query":"JWT token expiry","repo_path":"/workspace/my-project"}}}'
```

## Markdown tools (unified)

### gather_files
Collect files matching patterns across a directory tree.

### merge_markdown
Merge multiple markdown files with automatic TOC generation.

## Quick reference

| Tool | Purpose |
|------|---------|
| get_commits | Recent commits with details |
| get_stats | Repo statistics |
| analyze_history | Deep history analysis |
| ask_question | AI-powered codebase Q&A |
| learn_content | Store fact in knowledge base |
| search_knowledge | Query knowledge base |
| list_repositories | Find all repos in workspace |
| extract_structure | Project structure overview |
