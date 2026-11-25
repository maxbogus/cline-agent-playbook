# Browser & Vision Tools — Screenshots, OCR, UI Automation

## vision — Screen capture + OCR

### screenshot
Capture a screenshot of the entire screen or a region.

```bash
curl -s -X POST http://localhost:3200/vision/tools/call \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"screenshot","arguments":{"region":{"x":0,"y":0,"width":1920,"height":1080}}}}'
```

**Returns:** `{image_base64: "...", width, height, format}`

### find_text_on_screen
OCR + find text coordinates on screen. Uses RapidOCR.

```bash
curl -s -X POST http://localhost:3200/vision/tools/call \
  -d '{"method":"tools/call","params":{"name":"find_text_on_screen","arguments":{"text":"Submit","region":{"x":0,"y":0,"width":1920,"height":1080}}}}'
```

**Returns:** `{matches: [{text, x, y, width, height, confidence}]}`

### click_at_text
Find text on screen and click at its center.

```bash
curl -s -X POST http://localhost:3200/vision/tools/call \
  -d '{"method":"tools/call","params":{"name":"click_at_text","arguments":{"text":"OK"}}}'
```

### get_screen_info
Get screen dimensions, DPI, active window info.

### type_text
Type text at current cursor position (useful for filling forms).

## browser-parser — Web UI automation

### open_page
Open a URL in headless browser. See references/web.md.

### get_screenshot
Screenshot of a specific URL after JS rendering.

```bash
curl -s -X POST http://localhost:3200/browser-parser/tools/call \
  -d '{"method":"tools/call","params":{"name":"get_screenshot","arguments":{"url":"https://example.com"}}}'
```

### click_element
Click an element by CSS selector.

### wait_for_element
Wait for a DOM element to appear (with timeout).

### get_page_html
Full DOM HTML after JS rendering.

### close_browser
Close the browser instance (free resources).

## Quick reference

| Tool | Server | Use |
|------|--------|-----|
| screenshot | vision | Capture screen |
| find_text_on_screen | vision | OCR + locate text |
| click_at_text | vision | Click by text |
| type_text | vision | Keyboard input |
| get_screen_info | vision | Screen dimensions |
| open_page | browser-parser | Navigate URL |
| get_screenshot | browser-parser | Page screenshot |
| click_element | browser-parser | Click by selector |
| wait_for_element | browser-parser | Wait for DOM |

## Workflow: UI automation
1. `screenshot` — see current state
2. `find_text_on_screen` — locate target
3. `click_at_text` or `click_element` — interact
4. `screenshot` or `get_screenshot` — verify result
