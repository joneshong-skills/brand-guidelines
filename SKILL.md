---
name: brand-guidelines
description: >-
  This skill should be used when the user asks to "apply brand guidelines",
  "use brand colors", "apply brand styling", "brand guide", "design standards",
  "品牌規範", "品牌指南", "設計規範", "視覺識別",
  or discusses Anthropic brand colors, typography, corporate identity,
  visual formatting, or company design standards.
version: 0.2.0
tools: Bash, Read, Write, Glob, Edit
license: Complete terms in LICENSE.txt
argument-hint: "Describe the artifact to apply brand styling to"
---

# Anthropic Brand Styling

## Overview

Apply Anthropic's official brand identity (colors, typography, accent palette) to presentations, documents, HTML pages, and other visual artifacts.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design

---

## Workflow

### Step 1: Discover the Target Artifact

Use Glob to locate the file(s) to style:

```
Glob: **/*.pptx          # presentations
Glob: **/*.html           # web pages
Glob: **/*.docx           # Word documents
```

Then use Read to inspect the file content or structure. For `.pptx` files, extract text first:

```bash
python -m markitdown target.pptx
```

### Step 2: Determine the Output Format

| Format | Approach |
|--------|----------|
| `.pptx` | Write a python-pptx script, run with Bash |
| `.html` | Use Read to load the file, Edit to inject brand CSS |
| `.docx` | Write a python-docx script, run with Bash |
| `.css` | Use Edit to replace color/font values inline |

### Step 3: Apply Brand Styling

- For **python-pptx / python-docx scripts**: Use Write to create the script in a temp location, then Bash to execute it.
- For **HTML/CSS**: Use Read + Edit to surgically replace colors and font-family declarations.
- Always preserve the original file; write styled output to a new file (e.g., `output_branded.pptx`).

### Step 4: Verify

For `.pptx` output, generate a thumbnail to visually confirm:

```bash
python ~/.claude/skills/pptx/scripts/thumbnail.py output_branded.pptx
```

---

## Brand Guidelines

### Colors

**Main Colors:**

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Dark | `#141413` | `(20, 20, 19)` | Primary text, dark backgrounds |
| Light | `#faf9f5` | `(250, 249, 245)` | Light backgrounds, text on dark |
| Mid Gray | `#b0aea5` | `(176, 174, 165)` | Secondary elements, borders |
| Light Gray | `#e8e6dc` | `(232, 230, 220)` | Subtle backgrounds, dividers |

**Accent Colors:**

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Orange | `#d97757` | `(217, 119, 87)` | Primary accent |
| Blue | `#6a9bcc` | `(106, 155, 204)` | Secondary accent |
| Green | `#788c5d` | `(120, 140, 93)` | Tertiary accent |

### Typography

| Role | Font | Fallback | Size Guidance |
|------|------|----------|---------------|
| Headings | Poppins | Arial | 24pt+ for titles, 18pt for subtitles |
| Body | Lora | Georgia | 12-14pt for body text |

### Accent Cycling

For multi-element layouts (shapes, icons, section dividers), cycle through accents in order: Orange -> Blue -> Green -> Orange -> ...

---

## Common Patterns

### python-pptx: Brand Color Constants

```python
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# === Brand Colors ===
BRAND_DARK      = RGBColor(0x14, 0x14, 0x13)
BRAND_LIGHT     = RGBColor(0xFA, 0xF9, 0xF5)
BRAND_MID_GRAY  = RGBColor(0xB0, 0xAE, 0xA5)
BRAND_LIGHT_GRAY = RGBColor(0xE8, 0xE6, 0xDC)

ACCENT_ORANGE   = RGBColor(0xD9, 0x77, 0x57)
ACCENT_BLUE     = RGBColor(0x6A, 0x9B, 0xCC)
ACCENT_GREEN    = RGBColor(0x78, 0x8C, 0x5D)

ACCENTS = [ACCENT_ORANGE, ACCENT_BLUE, ACCENT_GREEN]

# === Typography ===
FONT_HEADING = "Poppins"
FONT_BODY    = "Lora"
FONT_HEADING_FALLBACK = "Arial"
FONT_BODY_FALLBACK    = "Georgia"
```

### python-pptx: Apply Font to a Text Run

```python
def style_run(run, font_name, size_pt, color, bold=False):
    """Apply brand styling to a single text run."""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.color.rgb = color
    run.font.bold = bold
```

### python-pptx: Style All Slides in a Presentation

```python
from pptx import Presentation

def apply_brand_to_pptx(input_path, output_path):
    prs = Presentation(input_path)
    accent_idx = 0

    for slide in prs.slides:
        for shape in slide.shapes:
            # Style text frames
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        size = run.font.size
                        if size and size >= Pt(24):
                            style_run(run, FONT_HEADING, 24, BRAND_DARK, bold=True)
                        elif size and size >= Pt(18):
                            style_run(run, FONT_HEADING, 18, BRAND_DARK)
                        else:
                            style_run(run, FONT_BODY, 12, BRAND_DARK)

            # Style non-text shapes with accent colors
            elif shape.shape_type is not None:
                if shape.fill is not None:
                    try:
                        shape.fill.solid()
                        shape.fill.fore_color.rgb = ACCENTS[accent_idx % len(ACCENTS)]
                        accent_idx += 1
                    except Exception:
                        pass

    prs.save(output_path)
```

### python-pptx: Set Slide Background

```python
from pptx.oxml.ns import qn

def set_slide_bg(slide, color):
    """Set solid background color on a slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

# Dark slide (title/conclusion)
set_slide_bg(slide, BRAND_DARK)
# Light slide (content)
set_slide_bg(slide, BRAND_LIGHT)
```

### python-pptx: Add Accent Divider Line

```python
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

def add_accent_line(slide, color=ACCENT_ORANGE, top=Inches(2), width=Inches(2)):
    """Add a horizontal accent line divider."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left=Inches(0.5), top=top,
        width=width, height=Pt(4)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()  # no border
```

### HTML/CSS: Brand Variables

```css
:root {
  --brand-dark: #141413;
  --brand-light: #faf9f5;
  --brand-mid-gray: #b0aea5;
  --brand-light-gray: #e8e6dc;
  --accent-orange: #d97757;
  --accent-blue: #6a9bcc;
  --accent-green: #788c5d;
  --font-heading: 'Poppins', Arial, sans-serif;
  --font-body: 'Lora', Georgia, serif;
}
```

### HTML: Google Fonts Import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Lora:wght@400;700&display=swap" rel="stylesheet">
```

---

## Tool Usage Summary

| Tool | When to Use |
|------|-------------|
| **Glob** | Find target files by extension/pattern |
| **Read** | Inspect file contents before styling |
| **Write** | Create python-pptx / python-docx scripts; write new styled HTML |
| **Edit** | Surgically inject brand CSS or replace color/font values in-place |
| **Bash** | Execute python scripts; run markitdown; generate thumbnails |

## Continuous Improvement

This skill evolves with each use. After every invocation:

1. **Reflect** — Identify what worked, what caused friction, and any unexpected issues
2. **Record** — Append a concise lesson to `lessons.md` in this skill's directory
3. **Refine** — When a pattern recurs (2+ times), update SKILL.md directly

### lessons.md Entry Format

```
### YYYY-MM-DD — Brief title
- **Friction**: What went wrong or was suboptimal
- **Fix**: How it was resolved
- **Rule**: Generalizable takeaway for future invocations
```

Accumulated lessons signal when to run `/skill-optimizer` for a deeper structural review.
