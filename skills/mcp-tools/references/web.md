# Web Tools — HTTP + JS Rendering

## static-parser — Fast HTML parsing

### parse_url
Fast HTTP fetch + BeautifulSoup + selectolax.

```bash
curl -s -X POST http://localhost:3200/static-parser/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "parse_url",
      "arguments": {
        "url": "https://example.com",
        "max_length": 5000
      }
    }
  }'
```

**Returns:** `{text, metadata: {title, description, og_image}, raw_html, error}`

### extract_metadata
```bash
curl -s -X POST http://localhost:3200/static-parser/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"extract_metadata","arguments":{"url":"..."}}}'
```

### normalize_text
Clean extracted text: whitespace, encoding, line breaks.

### validate_url
Check if URL is reachable and valid HTTP(S).

### check_robots
Parse robots.txt for a given URL path.

## browser-parser — Playwright JS rendering

**Warning:** Slow (10-30s startup). Use static-parser for simple pages.

### open_page
```bash
curl -s -X POST http://localhost:3200/browser-parser/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"open_page","arguments":{"url":"https://example.com","wait_for":"body"}}}'
```

### search
```bash
curl -s -X POST http://localhost:3200/browser-parser/tools/call \
  -d '{"method":"tools/call","params":{"name":"search","arguments":{"query":"python jobs","engine":"google","max_results":5}}}'
```

### extract_table_data
Extract `<table>` data as JSON.

### get_screenshot
Returns base64 PNG screenshot.

### get_page_html
Full DOM HTML after JS rendering.

## When to use which

| Scenario | Use |
|----------|-----|
| Simple HTML, no JS | static-parser `parse_url` |
| JS-rendered content | browser-parser `open_page` |
| SEO metadata | static-parser `extract_metadata` |
| Interactive SPA | browser-parser `open_page` + `get_screenshot` |
