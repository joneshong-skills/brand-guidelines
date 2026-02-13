[English](README.md) | [繁體中文](README.zh.md)

# brand-guidelines

A Claude Code skill that applies Anthropic's official brand colors, typography, and visual identity to any artifact. Based on the [official Anthropic skill](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines), adapted for local use.

## What It Does

1. Provides Anthropic's official brand color palette (dark, light, gray, accent colors)
2. Applies correct typography: Poppins for headings, Lora for body text
3. Automatically falls back to Arial/Georgia when custom fonts are unavailable
4. Cycles accent colors (orange, blue, green) across non-text shapes
5. Works with presentations, documents, HTML, and other visual artifacts

## Prerequisites

- For PPTX styling: `python-pptx` Python package
- For best results: Poppins and Lora fonts installed on your system

## Installation

```bash
git clone https://github.com/joneshong-skills/brand-guidelines.git ~/.claude/skills/brand-guidelines
```

## Usage

Once installed, ask Claude to apply brand styling:

- *"Apply Anthropic brand guidelines to this presentation"*
- *"Use brand colors for this document"*
- *"Style this page with Anthropic's visual identity"*
- *"Apply brand styling to the slide deck"*

## Brand Colors

| Name | Hex | Usage |
|------|-----|-------|
| Dark | `#141413` | Primary text, dark backgrounds |
| Light | `#faf9f5` | Light backgrounds, text on dark |
| Mid Gray | `#b0aea5` | Secondary elements |
| Light Gray | `#e8e6dc` | Subtle backgrounds |
| Orange | `#d97757` | Primary accent |
| Blue | `#6a9bcc` | Secondary accent |
| Green | `#788c5d` | Tertiary accent |

## Project Structure

```
brand-guidelines/
├── SKILL.md         # Skill definition with brand specs
├── LICENSE.txt      # Apache 2.0 license
├── README.md        # This file
├── README.zh.md     # Traditional Chinese README
├── references/      # Reference materials
├── scripts/         # Helper scripts
└── assets/          # Brand assets
```

## License

Apache 2.0 (from Anthropic)
