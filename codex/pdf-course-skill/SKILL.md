---
name: pdf-course-skill
description: >
  Use this skill whenever the user wants to create a polished, publication-ready
  PDF book, manual, guide, or course material. Covers the full pipeline:
  Markdown authoring with LaTeX headers, pandoc compilation, flowchart rendering
  from Mermaid diagrams, and a premium minimal cover page rendered via Playwright.
  Also use when the user asks to create a cover page for a PDF, build a
  multi-chapter book or guide, render Mermaid diagrams to PNG for embedding, or
  produce a final ZIP deliverable containing the PDF and all source files.
  Trigger on any request like "create a PDF book", "make a course PDF",
  "build a technical guide", "generate a manual", "create a book with cover",
  or any mention of producing a professional PDF document with chapters.
  This skill is general-purpose — it works for ANY topic, not just courses.
---

# PDF Book Production — Full Pipeline Skill

## Overview

This skill produces publication-quality PDF books/guides/manuals on **any topic
the user requests**. Nothing is hardcoded — title, subtitle, author, chapters,
diagrams, and cover content are all derived from the user's request.

### Pipeline Summary

1. **Gather requirements** — ask the user what they need (topic, chapters, audience, etc.)
2. **Content pipeline** — Markdown → LaTeX (pandoc) → content PDF
3. **Diagram pipeline** — Mermaid `.mmd` → SVG → PNG (via Playwright)
4. **Cover pipeline** — HTML → PDF (via Playwright print, NOT screenshot)
5. **Merge pipeline** — cover PDF + content PDF → final PDF
6. **ZIP packaging** — final deliverable with all source files

---

## 0. CRITICAL — Gather Requirements First

**Before writing ANY content or code, you MUST clarify the following with the user.**
Do NOT assume or invent details. Ask what's missing, confirm what you have.

### Required Information (ask if not provided)

| Detail | Example | Ask if missing? |
|---|---|---|
| **Book title** | "Practical Agentic AI" | YES — always |
| **Subtitle** (optional) | "Tool Calling with Ollama" | Ask if they want one |
| **Author name** | "Sam Rivera" | YES — always |
| **Target audience** | Beginners, intermediate, experts | YES |
| **Chapter outline** | List of chapters/topics to cover | YES — at minimum get topics |
| **Include diagrams?** | Flowcharts, architecture diagrams | Ask if relevant |
| **Series name** (optional) | "Local AI Series" | Only if they mention a series |
| **Tagline** (optional) | "From Zero to Confident" | Ask or suggest one |
| **Cover style** | Minimal B&W (default) or custom | Offer default, ask if they want changes |

### Interaction Flow

1. **Parse the user's request** — extract everything they already told you.
2. **Ask ONLY about what's missing** — don't re-ask what they already said.
3. **Present a summary** — show them the plan (title, chapters, structure).
4. **Wait for confirmation** — "Does this look good? Should I proceed?"
5. **Only then start building** — begin the technical pipeline.

If the user says "just go with it" or "you decide", make reasonable choices
and state your assumptions clearly before proceeding.

---

## 1. Dependencies — Install First

```bash
# Python packages
pip install pypdf img2pdf pillow pymupdf cairosvg --break-system-packages

# Node packages (global)
npm install -g @mermaid-js/mermaid-cli   # provides `mmdc` command

# Playwright (for SVG→PNG and cover rendering)
npm install playwright
# Download Chromium browser for Playwright
npx playwright install chromium

# System tools
apt-get install -y pandoc texlive-xetex texlive-fonts-recommended \
  texlive-latex-extra poppler-utils
```

---

## 2. Project Directory Structure

```
project/
├── docs/
│   ├── book.md              # master Markdown source
│   ├── content_only.pdf     # compiled content (no cover)
│   └── final_book.pdf       # cover + content merged
├── cover/
│   ├── cover.html           # cover page source (generated from user input)
│   └── cover.pdf            # rendered cover (via Playwright print)
├── flowcharts/              # only if diagrams are needed
│   ├── diagram_01.mmd       # Mermaid source
│   ├── diagram_01.svg       # rendered SVG
│   ├── diagram_01.png       # final PNG (Playwright-rendered, cropped)
│   └── puppeteer.json       # Playwright/Puppeteer config
└── src/                     # optional — code files if relevant
    └── *.py
```

---

## 3. Markdown Source — YAML Front Matter

Every book.md must start with this YAML block. **Replace placeholder values
with the user's actual book details.** These settings control LaTeX compilation.

```yaml
---
title: ""
author: ""
date: ""
documentclass: report
geometry: margin=1in
toc: true
toc-depth: 1
colorlinks: true
linkcolor: black
urlcolor: blue
header-includes:
  - \usepackage{fancyhdr}
  - \usepackage{titling}
  - \usepackage{xcolor}
  - \usepackage{tcolorbox}
  - \usepackage{float}
  - \usepackage{etoolbox}
  - \floatplacement{figure}{H}
  - \tcbuselibrary{breakable, skins}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyhead[L]{\nouppercase{\leftmark}}
  - \fancyhead[R]{BOOK_TITLE_HERE}
  - \fancyfoot[C]{\thepage}
  - \renewcommand{\headrulewidth}{0.4pt}
  - \newtcolorbox{tipbox}{colback=blue!5!white,colframe=blue!50!black,title=Tip,breakable}
  - \newtcolorbox{warnbox}{colback=red!5!white,colframe=red!60!black,title=Warning,breakable}
  - \newtcolorbox{turnbox}{colback=green!5!white,colframe=green!50!black,title=Try It Yourself,breakable}
---
```

**Critical notes:**
- Set `title: ""`, `author: ""`, `date: ""` to suppress pandoc's auto-generated
  title page (the cover is added separately).
- Replace `BOOK_TITLE_HERE` in `\fancyhead[R]` with the actual book title.
- `toc-depth: 1` in YAML is ignored by pandoc — use `--variable toc-depth=0`
  on the CLI instead (see Section 4).
- `\floatplacement{figure}{H}` prevents figures from floating away.
- The callout box names (`tipbox`, `warnbox`, `turnbox`) can be customized
  to match the book's domain (e.g., `notebox`, `dangerbox`, `exercisebox`).

### Callout Box Usage in Markdown

```latex
\begin{tipbox}
\textbf{Title.} Body text here.
\end{tipbox}

\begin{warnbox}
\textbf{Title.} Warning text here.
\end{warnbox}

\begin{turnbox}
\textbf{Exercise title.}
\begin{enumerate}
    \item Step one.
    \item Step two.
\end{enumerate}
\end{turnbox}
```

### Clickable URLs in Markdown

```latex
% Centered clickable URL block
\begin{center}
\url{https://github.com/user/repo}
\end{center}

% Inline clickable link with display text
\href{https://example.com}{display text}
```

---

## 4. Content PDF — pandoc Build Command

```bash
pandoc book.md \
  -o content_only.pdf \
  --pdf-engine=xelatex \
  --toc \
  --highlight-style=tango \
  --resource-path=. \
  -V mainfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V title="" \
  -V author="" \
  -V date="" \
  --variable toc-depth=0
```

**Key flags explained:**
- `--pdf-engine=xelatex` — required for Unicode support and custom fonts.
- `--toc` — generates table of contents.
- `--variable toc-depth=0` — **must be passed as CLI flag**, not YAML.
  In the `report` documentclass, depth 0 = chapters only (no subsections).
- `-V title=""` etc. — suppresses pandoc's auto title page.
- `--resource-path=.` — resolves image paths from current directory.
- `--highlight-style=tango` — syntax highlighting theme for code blocks.
- `DejaVu Sans` / `DejaVu Sans Mono` — widely available Unicode fonts.

---

## 5. Embedding Figures in Markdown

Always use raw LaTeX figure blocks for reliable placement:

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.45\textwidth]{flowcharts/diagram_01.png}
\caption{Description of what this diagram shows.}
\end{figure}
```

**Choosing the right `\textwidth` fraction:**
The PDF text body is 6.5in wide × 9in tall.

| Diagram aspect ratio (h/w) | Recommended width | Resulting height |
|---|---|---|
| Very tall (> 2.0) | `0.30\textwidth` | ~2in tall |
| Tall (1.2–2.0) | `0.42\textwidth` | ~2.5–3.5in tall |
| Square (~1.0) | `0.52\textwidth` | ~3.4in tall |
| Wide (0.5–1.0) | `0.80\textwidth` | ~2.6in tall |
| Very wide (< 0.5) | `0.85\textwidth` | ~2in tall |

**Rule:** never set width so high that the figure exceeds ~4in tall.

---

## 6. Mermaid Diagram Pipeline

Only use this section if the user's book needs diagrams.

### Step 1 — Write the Mermaid source (.mmd)

Create `.mmd` files relevant to the user's topic. Example:

```
flowchart TD
    A([Start]) --> B[Process]
    B --> C{Decision?}
    C -->|Yes| D[Action A]
    C -->|No| E[Action B]
    D --> F([End])
    E --> F
```

### Step 2 — Configure Playwright/Puppeteer for mmdc

Create `flowcharts/puppeteer.json`:

```json
{
  "executablePath": "/path/to/chromium",
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
```

Find your Chromium path with:
```bash
find /opt /home -name "chrome" -type f 2>/dev/null | head -5
```

### Step 3 — Render SVG via mmdc

```bash
mmdc -i diagram.mmd -o diagram.svg -p puppeteer.json -b white --quiet
```

**Why SVG first, not PNG?**
`mmdc` renders at the diagram's natural pixel size (~200–400px wide), which
is too small for print. SVG is resolution-independent.

### Step 4 — Convert SVG → PNG via Playwright (NOT cairosvg)

**Critical:** Mermaid SVGs use `<foreignObject>` elements for text labels.
`cairosvg` silently drops `<foreignObject>` → boxes with no text.
Playwright (real browser) renders `<foreignObject>` correctly.

```javascript
// render_svgs.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const TARGET_LONG = 2200; // px on long side — gives 300 DPI at any print size

async function svgToPng(svgPath, pngPath) {
  const browser = await chromium.launch({
    executablePath: '/path/to/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const svgContent = fs.readFileSync(svgPath, 'utf8');

  // Parse natural dimensions from viewBox
  const vb = svgContent.match(/viewBox="([^"]+)"/);
  if (!vb) { await browser.close(); return; }
  const parts = vb[1].trim().split(/\s+/).map(Number);
  const natW = parts[2], natH = parts[3];

  // Scale so the long side = TARGET_LONG
  let renderW, renderH;
  if (natW >= natH) {
    renderW = TARGET_LONG;
    renderH = Math.round(TARGET_LONG * natH / natW);
  } else {
    renderH = TARGET_LONG;
    renderW = Math.round(TARGET_LONG * natW / natH);
  }

  const html = `<!DOCTYPE html><html><head><meta charset="utf-8">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:white; width:${renderW}px; height:${renderH}px; overflow:hidden; }
    svg { width:${renderW}px !important; height:${renderH}px !important; display:block; }
  </style></head><body>${svgContent}</body></html>`;

  const page = await browser.newPage();
  await page.setViewportSize({ width: renderW, height: renderH });
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.waitForTimeout(300);

  await page.screenshot({
    path: pngPath,
    clip: { x: 0, y: 0, width: renderW, height: renderH },
    type: 'png'
  });
  await browser.close();
}

// Run for all SVGs in a directory
(async () => {
  const dir = './flowcharts';
  const svgs = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
  for (const svg of svgs.sort()) {
    await svgToPng(path.join(dir, svg), path.join(dir, svg.replace('.svg','.png')));
    console.log('Rendered:', svg);
  }
})();
```

### Step 5 — Autocrop whitespace + ensure minimum resolution

```python
from PIL import Image, ImageChops
import glob

def autocrop_and_upscale(path, min_long_side=1400, pad=30):
    img = Image.open(path).convert('RGB')
    bg = Image.new('RGB', img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        x0 = max(0, bbox[0] - pad)
        y0 = max(0, bbox[1] - pad)
        x1 = min(img.width,  bbox[2] + pad)
        y1 = min(img.height, bbox[3] + pad)
        img = img.crop((x0, y0, x1, y1))
    w, h = img.size
    if max(w, h) < min_long_side:
        scale = min_long_side / max(w, h)
        img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    img.save(path)

for f in glob.glob('flowcharts/*.png'):
    autocrop_and_upscale(f)
```

---

## 7. Cover Page — Design System

### Philosophy

Minimal premium typographic cover. Inspired by SICP, DDIA, and O'Reilly
engineering guides. No color, no decoration, no images — only type and rules.
The design communicates quality through restraint.

**All cover text is derived from the user's input** — title, subtitle, author,
series name, tagline. Nothing is hardcoded.

### Color

- Background: `#ffffff` (pure white)
- All text and rules: `#000000` (pure black)
- No exceptions. No grays. No accents.

### Font

**IBM Plex Sans** — IBM's open-source typeface, designed for technical
documentation. Load from Google Fonts:

```html
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');
```

Weights used:
- `700` Bold — title only
- `400` Regular — guide description, series line
- `300` Light — subtitle
- `300 Italic` — tagline, footer focus line

**Do NOT use monospace fonts** anywhere on the cover. Chromium's screen
renderer applies subpixel color tinting to monospace italic text.

### Required CSS Reset

```css
*, *::before, *::after {
  margin: 0; padding: 0; box-sizing: border-box; color: #000;
}
html, body, div, span, p, h1, h2, h3 {
  color: #000000;
  -webkit-text-fill-color: #000000;
}
```

### Page Layout

```
┌──────────────────────────────────────┐  ← 2px solid black rule
│                                      │
│  [series line — 10.5px italic]       │  ← 30px below rule
│                                      │
│                                      │
│  [H1 TITLE — 96px Bold]             │  ← vertically centered
│  [H1 line 2]                        │    in flex:1 middle zone
│                                      │
│  ━━━━  ← 44px × 3px black rule      │
│                                      │
│  [subtitle — 24px Light]            │
│                                      │
│  [tagline — 13px Light Italic]      │
│                                      │
│                                      │
├──────────────────────────────────────┤  ← 1px solid black rule
│  [guide description — 12px Regular] │
│  [AUTHOR NAME — 21px Bold]          │  [Focus line — 10.5px Italic →]
└──────────────────────────────────────┘
```

**Page dimensions:** 816px × 1056px (8.5in × 11in at 96 DPI)
**Page margins:** top 72px | right 88px | bottom 68px | left 88px

### Typography Scale

| Element | Size | Weight | Style | Letter-spacing | Line-height |
|---|---|---|---|---|---|
| Series line | 10.5px | 400 | italic | 0.10em | — |
| H1 title | 96px | 700 | normal | -0.035em | 0.91 |
| Mid-rule | 44px wide, 3px tall | — | — | — | — |
| Subtitle | 24px | 300 | normal | -0.01em | 1.35 |
| Tagline | 13px | 300 | italic | 0.02em | 1.9 |
| Guide description | 12px | 400 | normal | 0.005em | — |
| Author name | 21px | 700 | normal | -0.02em | — |
| Focus right | 10.5px | 300 | italic | — | 2.0 |

**Title font size adjustment:** If the title is long (4+ words or 20+ chars),
reduce `h1` font-size to 72px or 60px to prevent overflow. For very short
titles (1-2 words), 96px works perfectly.

### Cover HTML Template

**Replace ALL placeholder values** (marked with `{{PLACEHOLDER}}`) with
the user's actual content before rendering.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');

  *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; color:#000; }
  html, body, div, span, p, h1, h2, h3 {
    color: #000000; -webkit-text-fill-color: #000000;
  }
  body {
    width: 816px; height: 1056px; background: #fff;
    font-family: 'IBM Plex Sans', sans-serif; overflow: hidden;
  }
  .page {
    width: 100%; height: 100%;
    padding: 72px 88px 68px;
    display: flex; flex-direction: column;
  }
  .top-rule { width:100%; height:2px; background:#000; margin-bottom:30px; }
  .series {
    font-size:10.5px; font-weight:400; font-style:italic; letter-spacing:.10em;
  }
  .middle {
    flex: 1; display: flex; flex-direction: column;
    justify-content: center; padding: 32px 0 28px;
  }
  h1 {
    font-size:96px; font-weight:700; line-height:.91;
    letter-spacing:-.035em; margin-bottom:34px;
  }
  .mid-rule { width:44px; height:3px; background:#000; margin-bottom:28px; }
  .subtitle {
    font-size:24px; font-weight:300; letter-spacing:-.01em;
    line-height:1.35; margin-bottom:52px;
  }
  .tagline {
    font-size:13px; font-weight:300; font-style:italic;
    letter-spacing:.02em; line-height:1.9;
  }
  .footer-rule { width:100%; height:1px; background:#000; margin-bottom:26px; }
  .footer { display:flex; align-items:flex-end; justify-content:space-between; }
  .f-guide { font-size:12px; font-weight:400; margin-bottom:7px; }
  .f-author { font-size:21px; font-weight:700; letter-spacing:-.02em; }
  .f-right {
    font-size:10.5px; font-weight:300; font-style:italic;
    text-align:right; line-height:2.0;
  }
</style>
</head>
<body>
<div class="page">
  <div class="top-rule"></div>
  <p class="series">{{SERIES_LINE}}</p>

  <div class="middle">
    <h1>{{TITLE_LINE_1}}<br>{{TITLE_LINE_2}}</h1>
    <div class="mid-rule"></div>
    <p class="subtitle">{{SUBTITLE}}</p>
    <p class="tagline">
      {{TAGLINE_LINE_1}}<br>
      {{TAGLINE_LINE_2}}
    </p>
  </div>

  <div class="footer-rule"></div>
  <div class="footer">
    <div>
      <p class="f-guide">{{GUIDE_DESCRIPTION}}</p>
      <p class="f-author">{{AUTHOR_NAME}}</p>
    </div>
    <p class="f-right">{{FOCUS_LINE_1}}<br>&amp; {{FOCUS_LINE_2}}</p>
  </div>
</div>
</body>
</html>
```

**Placeholder guide:**

| Placeholder | What to fill | Example |
|---|---|---|
| `{{SERIES_LINE}}` | Series or branding line (caps + dots style) | `FROM ZERO TO CONFIDENT · LOCAL AI SERIES` |
| `{{TITLE_LINE_1}}`, `{{TITLE_LINE_2}}` | Main title split across lines | `Practical` / `Agentic AI` |
| `{{SUBTITLE}}` | Subtitle or secondary title | `Tool Calling with Ollama` |
| `{{TAGLINE_LINE_1}}`, `{{TAGLINE_LINE_2}}` | Two-line tagline | `From Zero to Confident` / `in Building Local AI Agents` |
| `{{GUIDE_DESCRIPTION}}` | Short description of the guide | `A Practical Guide to Modern Python` |
| `{{AUTHOR_NAME}}` | Author's full name | `Sam Rivera` |
| `{{FOCUS_LINE_1}}`, `{{FOCUS_LINE_2}}` | Two focus keywords | `Machine Learning` / `Deep Learning` |

If the user doesn't provide a series line or tagline, omit those elements
from the HTML (remove the `<p>` tags entirely, don't leave empty elements).

---

## 8. Cover PDF — Rendering via Playwright

**CRITICAL:** Export as PDF via the print pipeline, NOT via screenshot.

| Method | Result |
|---|---|
| `page.screenshot()` → `img2pdf` | Color artifacts on italic text, raster quality |
| `page.pdf()` print pipeline | True vector text, pure black, print quality |

```javascript
// render_cover.js
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/path/to/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 816, height: 1056 });
  await page.goto('file:///absolute/path/to/cover.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500); // wait for Google Fonts to load

  // Export as PDF — print pipeline, not screenshot
  const pdf = await page.pdf({
    width: '8.5in',
    height: '11in',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  fs.writeFileSync('cover/cover.pdf', pdf);
  await browser.close();
  console.log('Cover PDF written:', pdf.length, 'bytes');
})();
```

---

## 9. Merge Cover + Content → Final PDF

```python
from pypdf import PdfWriter, PdfReader

def merge_cover_and_content(cover_path, content_path, output_path):
    writer = PdfWriter()

    cover = PdfReader(cover_path)
    for page in cover.pages:
        writer.add_page(page)

    content = PdfReader(content_path)
    for page in content.pages:
        writer.add_page(page)

    with open(output_path, 'wb') as f:
        writer.write(f)

    print(f"Final PDF: {1 + len(content.pages)} pages → {output_path}")

merge_cover_and_content(
    'cover/cover.pdf',
    'docs/content_only.pdf',
    'docs/final_book.pdf'
)
```

---

## 10. Final ZIP Packaging

```python
import zipfile, os, shutil

def package_deliverable(project_dir, output_zip):
    """Package entire project into a ZIP for delivery."""
    shutil.copy(
        os.path.join(project_dir, 'docs/final_book.pdf'),
        '/mnt/user-data/outputs/final_book.pdf'
    )
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in ('node_modules', '__pycache__', '.git')]
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, os.path.dirname(project_dir))
                zf.write(filepath, arcname)
    print(f"ZIP: {output_zip}")
```

---

## 11. Full Build Script (all steps combined)

```bash
#!/bin/bash
set -e
PROJECT="project"
cd $PROJECT

echo "Step 1: Render Mermaid diagrams to SVG..."
if ls flowcharts/*.mmd 1>/dev/null 2>&1; then
  for f in flowcharts/*.mmd; do
    mmdc -i "$f" -o "${f%.mmd}.svg" -p flowcharts/puppeteer.json -b white --quiet
  done

  echo "Step 2: Convert SVGs to PNG via Playwright..."
  node flowcharts/render_svgs.js

  echo "Step 3: Autocrop and upscale PNGs..."
  python3 flowcharts/autocrop.py
else
  echo "No Mermaid diagrams found, skipping diagram pipeline."
fi

echo "Step 4: Compile content PDF via pandoc..."
pandoc docs/book.md \
  -o docs/content_only.pdf \
  --pdf-engine=xelatex \
  --toc \
  --highlight-style=tango \
  --resource-path=. \
  -V mainfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V title="" -V author="" -V date="" \
  --variable toc-depth=0

echo "Step 5: Render cover PDF via Playwright..."
node cover/render_cover.js

echo "Step 6: Merge cover + content..."
python3 -c "
from pypdf import PdfWriter, PdfReader
w = PdfWriter()
for p in PdfReader('cover/cover.pdf').pages: w.add_page(p)
content = PdfReader('docs/content_only.pdf')
for p in content.pages: w.add_page(p)
with open('docs/final_book.pdf', 'wb') as f: w.write(f)
print('Done:', 1+len(content.pages), 'pages')
"

echo "Step 7: Package ZIP..."
cd .. && zip -rq project.zip project/

echo "Build complete."
```

---

## 12. Common Mistakes & Fixes

| Problem | Cause | Fix |
|---|---|---|
| Figures float away from text | No `[H]` placement | Use `\begin{figure}[H]` always |
| TOC shows subsections | `toc-depth` in YAML ignored | Pass `--variable toc-depth=0` on CLI |
| Blank title page before TOC | pandoc auto-generates title | Pass `-V title="" -V author="" -V date=""` |
| Diagram text missing in PNG | `cairosvg` drops `<foreignObject>` | Use Playwright browser renderer instead |
| Cover has dead gap in lower half | Static layout doesn't fill page | Use `flex:1` on middle zone with `justify-content:center` |
| Code block overflows page width | Long lines in code | Add `\usepackage{fvextra}` and `\DefineVerbatimEnvironment` |
| Title too long for cover | Title overflows h1 area | Reduce `font-size` to 72px or 60px |
| Images too large, overflow page | `\textwidth` fraction too high | Use aspect ratio table (Section 5) |
| PDF text is raster, not vector | Used `img2pdf` after screenshot | Export directly via `page.pdf()` |

---

## 13. Quality Checklist (Before Delivering)

- [ ] All content matches what the user requested
- [ ] User confirmed the chapter outline before content was written
- [ ] Cover has the correct title, author, and subtitle
- [ ] All code examples are complete and runnable (if applicable)
- [ ] All exercises have working hints (if applicable)
- [ ] Diagrams are relevant to the topic and correctly labeled
- [ ] TOC page numbers are accurate
- [ ] No orphaned `\end{...box}` without matching `\begin`
- [ ] Cover PDF is pure black text (no color artifacts)
- [ ] Final PDF opens correctly and all pages render
- [ ] ZIP contains all source files
