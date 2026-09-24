#!/usr/bin/env python3
"""Render a site directory to a 1280x800 RGB24 .img fixture via WeasyPrint.

Usage: render.py <sitedir> <out.img>
Deterministic: fixed @page size, local files only, no network.
"""
import os, struct, subprocess, sys
from weasyprint import HTML

PAGE_CSS = "<style>@page{size:1280px 800px;margin:0}html,body{width:1280px;min-height:800px}</style>"

def render_png(sitedir, png_path):
    html = open(os.path.join(sitedir, "index.html")).read()
    html = html.replace("</head>", PAGE_CSS + "</head>")
    pdf = os.path.join(sitedir, "_render.pdf") if False else png_path + ".tmp.pdf"
    HTML(string=html, base_url=sitedir + "/").write_pdf(pdf)
    subprocess.run(["pdftoppm", "-png", "-r", "96", "-f", "1", "-l", "1",
                    "-W", "1280", "-H", "800", pdf, png_path + ".pg"],
                   check=True, capture_output=True)
    os.replace(png_path + ".pg-1.png", png_path)
    os.remove(pdf)

def png_to_img(png_path, img_path):
    from PIL import Image
    im = Image.open(png_path).convert("RGB")
    if im.size != (1280, 800):
        im = im.resize((1280, 800))
    with open(img_path, "wb") as f:
        f.write(struct.pack("<II", 1280, 800) + im.tobytes())

if __name__ == "__main__":
    sd, out = sys.argv[1], sys.argv[2]
    png = out + ".png"
    render_png(sd, png)
    png_to_img(png, out)
    os.remove(png)
    print("wrote", out)
