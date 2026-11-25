# Docs Tools — Transform, Summarize, Storage

## document-transformer — PDF/DOCX/JPG + OCR

### transform_documents
Convert between formats (PDF→text, DOCX→markdown, JPG→text via OCR).

```bash
curl -s -X POST http://localhost:3200/document-transformer/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"transform_documents","arguments":{"files":["/workspace/repo/docs/report.pdf"],"output_format":"markdown"}}}'
```

**Arguments:**
- `files`: list of file paths
- `output_format`: `text` | `markdown` | `structured_json`
- `ocr_engine`: `rapidocr` (default) | `tesseract`
- `language`: OCR language code (e.g. `eng`, `rus`)

### get_document_stats
File size, page count, word count, detected language.

### get_document_content
Extract full text content from a document.

### search_documents
Full-text search across stored documents.

### get_failed_documents
List documents that failed to process.

## summarization — File summarization

### summarize_file
```bash
curl -s -X POST http://localhost:3200/summarization/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"summarize_file","arguments":{"file_path":"/workspace/repo/README.md","max_length":500}}}'
```

**Returns:** `{summary, key_points: [...], word_count, language}`

### summarize_batch
Summarize multiple files at once.

### get_summarization_stats
Cache hit rate, average processing time.

### clear_summarization_cache
Clear the LLM cache.

## parser-storage — Document storage + search

### save_document
Store a parsed document with metadata.

### get_document
Retrieve a stored document by ID.

### document_exists
Check if a document is already stored (by hash).

### list_documents
List all stored documents with filters.

### search_documents
Full-text search across stored documents.

## Quick reference

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| transform_documents | Format conversion + OCR | PDF, DOCX, JPG | text, markdown |
| get_document_stats | Metadata extraction | any doc | size, pages, lang |
| summarize_file | LLM summarization | any text file | summary + points |
| summarize_batch | Batch summarization | multiple files | array of summaries |
| save_document | Store for later | parsed content | doc_id |
| search_documents | Find by content | query | matching docs |
