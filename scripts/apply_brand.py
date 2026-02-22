#!/usr/bin/env python3
"""Apply brand guidelines to artifacts (CSS, PPTX, HTML).

Usage:
  python3 apply_brand.py --type css --input style.css --output branded.css
  python3 apply_brand.py --type html --input page.html --output branded.html
  python3 apply_brand.py --show  # Display brand constants
"""

import argparse
import sys
import os

BRAND = {
    "primary": "#191918",        # Ink (dark text)
    "secondary": "#E8E1D5",      # Parchment (warm bg)
    "accent": "#DA7756",         # Sienna (CTA, highlights)
    "accent_light": "#E3A17D",   # Light Sienna
    "surface": "#FFFFFF",        # White
    "text": "#191918",           # Primary text
    "text_secondary": "#666660", # Secondary text
    "font_heading": "'Copernicus', 'Georgia', serif",
    "font_body": "'Styrene A', 'Helvetica Neue', sans-serif",
    "font_mono": "'Söhne Mono', 'Menlo', monospace",
}

CSS_VAR_MAP = {
    "primary": "--brand-primary",
    "secondary": "--brand-secondary",
    "accent": "--brand-accent",
    "accent_light": "--brand-accent-light",
    "surface": "--brand-surface",
    "text": "--brand-text",
    "text_secondary": "--brand-text-secondary",
    "font_heading": "--brand-font-heading",
    "font_body": "--brand-font-body",
    "font_mono": "--brand-font-mono",
}

GOOGLE_FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Georgia&display=swap" rel="stylesheet">'
)


def show_brand():
    """Print all brand constants in a readable format."""
    print("=" * 50)
    print("  Anthropic Brand Guidelines")
    print("=" * 50)
    print()
    print("Colors:")
    color_keys = ["primary", "secondary", "accent", "accent_light", "surface", "text", "text_secondary"]
    for key in color_keys:
        value = BRAND[key]
        label = key.replace("_", " ").title()
        print(f"  {label:<20} {value}")
    print()
    print("Typography:")
    font_keys = ["font_heading", "font_body", "font_mono"]
    for key in font_keys:
        value = BRAND[key]
        label = key.replace("_", " ").title()
        print(f"  {label:<20} {value}")
    print()
    print("CSS Variable Names:")
    for key, var in CSS_VAR_MAP.items():
        print(f"  {var:<30} {BRAND[key]}")


def _build_css_root_block():
    """Build the :root CSS block with all brand variables."""
    lines = [":root {"]
    for key, var in CSS_VAR_MAP.items():
        value = BRAND[key]
        lines.append("  {}: {};".format(var, value))
    lines.append("}")
    return "\n".join(lines)


def inject_css_vars(css_content):
    """Inject :root { --brand-*: value; ... } at top of CSS content.

    Args:
        css_content (str): Original CSS content.

    Returns:
        str: CSS content with brand variables injected at the top.
    """
    root_block = _build_css_root_block()
    header = "/* Anthropic Brand Variables — auto-injected by apply_brand.py */\n"
    return header + root_block + "\n\n" + css_content


def apply_to_html(html_content):
    """Inject brand CSS vars + font link into HTML content.

    Inserts a <style> block with :root variables and a Google Fonts link
    just before </head>. If no </head> is found, prepends to the content.

    Args:
        html_content (str): Original HTML content.

    Returns:
        str: HTML content with brand styles and font links injected.
    """
    root_block = _build_css_root_block()
    style_block = (
        "  <!-- Anthropic Brand Variables — auto-injected by apply_brand.py -->\n"
        "  {fonts}\n"
        "  <style>\n"
        "    {css}\n"
        "  </style>"
    ).format(
        fonts=GOOGLE_FONTS_LINK,
        css=root_block.replace("\n", "\n    "),
    )

    head_close = "</head>"
    if head_close in html_content:
        return html_content.replace(head_close, style_block + "\n" + head_close, 1)
    else:
        # Fallback: prepend style block
        return style_block + "\n" + html_content


def main():
    parser = argparse.ArgumentParser(
        description="Apply Anthropic brand guidelines to CSS or HTML artifacts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--show", action="store_true", help="Display brand constants and exit")
    parser.add_argument(
        "--type",
        choices=["css", "html"],
        help="Artifact type to process",
    )
    parser.add_argument("--input", "-i", help="Input file path")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if args.show:
        show_brand()
        return

    if not args.type:
        parser.error("--type is required unless --show is used")
    if not args.input:
        parser.error("--input is required")
    if not args.output:
        parser.error("--output is required")

    input_path = os.path.expanduser(args.input)
    output_path = os.path.expanduser(args.output)

    if not os.path.isfile(input_path):
        print("Error: input file not found: {}".format(input_path), file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    if args.type == "css":
        result = inject_css_vars(content)
    elif args.type == "html":
        result = apply_to_html(content)
    else:
        print("Error: unsupported type: {}".format(args.type), file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print("Brand applied ({}) → {}".format(args.type.upper(), output_path))


if __name__ == "__main__":
    main()
