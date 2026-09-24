#!/usr/bin/env python3
"""Generate hand-authored HTML/CSS fixtures, render headlessly via WeasyPrint.
Each fixture is a standalone HTML file with embedded CSS, rendered to 480x360
PNG via WeasyPrint (headless, CLI from local files), converted to .img format.
"""
import os, struct, subprocess, sys

OUTDIR = os.path.expanduser("~/workspace/code-ui/judge-repair/calibration/html_fixtures")
os.makedirs(OUTDIR, exist_ok=True)

PAGE_CSS = """
@page { size: 480px 360px; margin: 0; }
body { font-family: sans-serif; margin: 0; padding: 32px; background: #ffffff; }
"""

def render(name, html_body, css_extra=""):
    html = f"""<!DOCTYPE html><html><head><style>{PAGE_CSS}{css_extra}</style></head>
<body>{html_body}</body></html>"""
    html_path = os.path.join(OUTDIR, name + ".html")
    pdf_path = os.path.join(OUTDIR, name + ".pdf")
    png_path = os.path.join(OUTDIR, name + ".png")
    img_path = os.path.join(OUTDIR, name + ".img")
    with open(html_path, "w") as f:
        f.write(html)
    # Render via WeasyPrint (headless HTML/CSS)
    from weasyprint import HTML as WHTML
    WHTML(filename=html_path).write_pdf(pdf_path)
    # PDF -> PNG via pdftoppm (CLI)
    subprocess.run(["pdftoppm", "-png", "-r", "72", "-singlefile", pdf_path,
                    os.path.join(OUTDIR, name)], check=True, capture_output=True)
    # PNG -> .img (u32LE w, u32LE h, RGB24)
    from PIL import Image
    im = Image.open(png_path).convert("RGB")
    # Ensure 480x360 (pad/crop if needed)
    if im.size != (480, 360):
        canvas = Image.new("RGB", (480, 360), (255, 255, 255))
        canvas.paste(im, (0, 0))
        im = canvas
    with open(img_path, "wb") as f:
        f.write(struct.pack("<II", 480, 360) + im.tobytes())
    print(f"wrote {name}.img ({im.size})")
    # Cleanup intermediates (keep html for audit)
    os.remove(pdf_path)
    os.remove(png_path)

# --- Good fixtures ---
def good_clean():
    render("html_good_clean", """
<h1 style="color:#111;font-size:32px;margin:0 0 16px 0">Build something great</h1>
<p style="color:#555;font-size:15px;line-height:1.6;margin:0 0 12px 0">The fastest way to ship beautiful interfaces. Start with a clean layout and clear hierarchy.</p>
<p style="color:#555;font-size:15px;line-height:1.6;margin:0 0 12px 0">Every element has room to breathe. Spacing is consistent and deliberate.</p>
<div style="margin-top:24px"><span style="background:#2563eb;color:#fff;padding:10px 24px;border-radius:6px;font-size:15px">Get started</span></div>
""")

def good_dark():
    render("html_good_dark", """
<h1 style="color:#f5f5f5;font-size:32px;margin:0 0 16px 0">Build something great</h1>
<p style="color:#b5b5b5;font-size:15px;line-height:1.6;margin:0 0 12px 0">The fastest way to ship beautiful interfaces. Dark theme with readable contrast.</p>
<p style="color:#b5b5b5;font-size:15px;line-height:1.6;margin:0 0 12px 0">Every element has room to breathe. Spacing is consistent and deliberate.</p>
""", "body{background:#0b0d10;}")

# --- Bad fixtures (one per failure class) ---
def bad_contrast_faint():
    # Near-invisible body text: #d8d8d8 on white
    render("html_bad_contrast_faint", """
<h1 style="color:#111;font-size:32px;margin:0 0 16px 0">Build something great</h1>
<p style="color:#d8d8d8;font-size:15px;line-height:1.6;margin:0 0 12px 0">This body text is near-invisible. It should be flagged as poor contrast.</p>
<p style="color:#d8d8d8;font-size:15px;line-height:1.6;margin:0 0 12px 0">More faint text here that is very hard to read against the white background.</p>
""")

def bad_clutter():
    # Dense clutter: many small text blocks
    items = "".join([f'<div style="font-size:11px;color:#333;margin:0 0 4px 0">Clutter line {i} with dense text packing</div>' for i in range(20)])
    render("html_bad_clutter", f"<div>{items}</div>")

def bad_spacing():
    # Irregular spacing: random gaps
    render("html_bad_spacing", """
<h1 style="color:#111;font-size:28px;margin:0 0 4px 0">Title</h1>
<p style="color:#555;font-size:14px;margin:0 0 48px 0">Huge gap below.</p>
<p style="color:#555;font-size:14px;margin:0 0 2px 0">Tiny gap.</p>
<p style="color:#555;font-size:14px;margin:0 0 32px 0">Medium gap.</p>
<p style="color:#555;font-size:14px;margin:0">No gap at end.</p>
""")

def bad_margin():
    # Content crowded to edges (no margins)
    render("html_bad_margin", """
<h1 style="color:#111;font-size:28px;margin:0">Edge Title</h1>
<p style="color:#555;font-size:14px;margin:0">Text pushed to the very edge with no breathing room at all.</p>
<p style="color:#555;font-size:14px;margin:0">Another line crammed against the margin.</p>
""", "body{padding:2px;}")

def bad_align():
    # Misaligned: mixed left/center/right
    render("html_bad_align", """
<h1 style="color:#111;font-size:28px;text-align:left;margin:0 0 12px 0">Left Title</h1>
<p style="color:#555;font-size:14px;text-align:center;margin:0 0 12px 0">Centered paragraph text here.</p>
<p style="color:#555;font-size:14px;text-align:right;margin:0 0 12px 0">Right-aligned text.</p>
<p style="color:#555;font-size:14px;text-align:left;margin:0">Back to left.</p>
""")

def bad_type():
    # Inconsistent typography: many sizes
    render("html_bad_type", """
<div style="font-size:40px;color:#111;margin:0 0 8px 0">Huge</div>
<div style="font-size:10px;color:#111;margin:0 0 8px 0">Tiny</div>
<div style="font-size:24px;color:#111;margin:0 0 8px 0">Medium</div>
<div style="font-size:12px;color:#111;margin:0 0 8px 0">Small</div>
<div style="font-size:32px;color:#111;margin:0 0 8px 0">Large</div>
<div style="font-size:14px;color:#111;margin:0">Normal</div>
""")

def bad_color():
    # Unrestrained color: rainbow headings
    colors = ["#dc2828", "#28a028", "#2850dc", "#e68c14", "#9628c8", "#14aaaa"]
    items = "".join([f'<div style="font-size:20px;color:{c};margin:0 0 8px 0">Rainbow heading</div>' for c in colors])
    render("html_bad_color", items)

def bad_hierarchy():
    # Flat hierarchy: all same size, no emphasis
    items = "".join([f'<div style="font-size:16px;color:#333;margin:0 0 8px 0">Flat section {i} with same visual weight</div>' for i in range(8)])
    render("html_bad_hierarchy", items)

if __name__ == "__main__":
    good_clean()
    good_dark()
    bad_contrast_faint()
    bad_clutter()
    bad_spacing()
    bad_margin()
    bad_align()
    bad_type()
    bad_color()
    bad_hierarchy()
    print("done")
