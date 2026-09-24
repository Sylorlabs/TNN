#!/usr/bin/env python3
"""Dev fixtures for CODEUI-1 judge repair (judge2).

PIL-synthesized UI screenshots (480x360, matching the frozen refs' hero-crop
geometry). Chrome headless is non-functional on this VM (no DOM output, no
screenshots, hangs), so fixtures are synthesized with real TrueType text
rendering (DejaVu Sans) -- the judge consumes .img pixels only, so the pixel
phenomena (antialiased glyphs, contrast, spacing, alignment) are identical
in kind to rendered HTML.

All content is fixed strings; gradients are sin-based (deterministic).
No RNG anywhere.

Fixture classes (14):
  good_clean, good_dark, good_varied, good_mild   (expect GOOD)
  bad_contrast_faint  (blind-spot class: near-invisible body, |dL|<48)
  bad_contrast_mid    (low-contrast body, detected as ink)
  bad_clutter, bad_spacing, bad_margin, bad_align,
  bad_type, bad_color, bad_hierarchy, bad_all
"""
import os, struct, math
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.expanduser("~/workspace/code-ui/judge-repair/calibration/fixtures")
os.makedirs(BASE, exist_ok=True)

W, H = 480, 360
FD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FDB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FDB if bold else FD, size)

def new(bg):
    return Image.new("RGB", (W, H), bg)

def text(d, x, y, s, size, fill, bold=False):
    d.text((x, y), s, font=font(size, bold), fill=fill)
    a = font(size, bold).getbbox(s)
    return a[3] - a[1]

def para(d, x, y, lines, size, fill, lh, bold=False):
    for s in lines:
        text(d, x, y, s, size, fill, bold)
        y += lh
    return y

def rule(d, y, fill=(230, 230, 230)):
    d.line([(0, y), (W, y)], fill=fill, width=1)

def button(d, x, y, bw, bh, fill, label, tfill=(255, 255, 255)):
    d.rectangle([x, y, x + bw, y + bh], fill=fill)
    f = font(15, True)
    bb = f.getbbox(label)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((x + (bw - tw) / 2, y + (bh - th) / 2 - 1), label, font=f, fill=tfill)

def photoblock(d, x, y, bw, bh, hue_shift=0.0):
    """Deterministic photo-like block: layered sinusoids, no RNG."""
    for yy in range(bh):
        for xx in range(bw):
            v = (math.sin(xx * 0.11 + hue_shift) + math.sin(yy * 0.23 + xx * 0.031)
                 + math.sin((xx + yy) * 0.061 + 1.7)) / 3.0  # -1..1
            r = int(120 + 90 * v + 40 * math.sin(xx * 0.53))
            g = int(130 + 70 * math.sin(yy * 0.41 + 2.0) + 30 * v)
            b = int(150 + 60 * math.cos((xx - yy) * 0.07))
            r = max(0, min(255, r)); g = max(0, min(255, g)); b = max(0, min(255, b))
            d.point((x + xx, y + yy), fill=(r, g, b))

def save(im, name):
    blob = struct.pack("<II", W, H) + im.tobytes()
    open(os.path.join(BASE, name + ".img"), "wb").write(blob)
    im.save(os.path.join(BASE, name + ".png"))
    print("wrote", name)

BODY3 = ["Start with a clean canvas and deliberate",
         "spacing. Every element earns its place",
         "through restraint and hierarchy."]

def good_clean():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    text(d, 32, 18, "Acme", 16, (20, 20, 20), True)
    text(d, 330, 21, "Products  Pricing  Docs", 13, (85, 85, 85))
    rule(d, 52)
    text(d, 32, 76, "Build something great", 38, (17, 17, 17), True)
    text(d, 32, 128, "The fastest way to ship beautiful interfaces.", 17, (68, 68, 68))
    para(d, 32, 162, BODY3, 15, (51, 51, 51), 24)
    button(d, 32, 244, 144, 36, (37, 99, 235), "Get started")
    text(d, 32, 300, "Fast", 15, (17, 17, 17), True)
    text(d, 32, 322, "Renders in milliseconds.", 13, (85, 85, 85))
    text(d, 256, 300, "Simple", 15, (17, 17, 17), True)
    text(d, 256, 322, "One API to learn.", 13, (85, 85, 85))
    return im

def good_dark():
    im = new((11, 13, 16)); d = ImageDraw.Draw(im)
    text(d, 32, 18, "Acme", 16, (245, 245, 245), True)
    text(d, 330, 21, "Products  Pricing  Docs", 13, (170, 170, 170))
    rule(d, 52, fill=(40, 42, 48))
    text(d, 32, 76, "Build something great", 38, (245, 245, 245), True)
    text(d, 32, 128, "The fastest way to ship beautiful interfaces.", 17, (201, 201, 201))
    para(d, 32, 162, BODY3, 15, (181, 181, 181), 24)
    button(d, 32, 244, 144, 36, (59, 130, 246), "Get started")
    text(d, 32, 300, "Fast", 15, (232, 232, 232), True)
    text(d, 32, 322, "Renders in milliseconds.", 13, (153, 153, 153))
    text(d, 256, 300, "Simple", 15, (232, 232, 232), True)
    text(d, 256, 322, "One API to learn.", 13, (153, 153, 153))
    return im

def good_varied():
    """Tricky-good: intentionally varied section rhythm, photo block,
    two accent hues, footer text inside the bottom margin."""
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    text(d, 32, 14, "Fieldnotes", 15, (20, 20, 20), True)
    rule(d, 44)
    text(d, 32, 58, "Notes from the road", 32, (17, 17, 17), True)
    photoblock(d, 0, 108, W, 92, hue_shift=0.7)
    text(d, 32, 216, "Dispatch 12", 13, (37, 99, 235), True)
    para(d, 32, 238, ["Crossed the valley before dawn.", "The light did all the work."], 14, (51, 51, 51), 22)
    text(d, 32, 296, "Dispatch 11", 13, (22, 163, 74), True)
    text(d, 32, 318, "Rain on the tin roof, mapped.", 14, (51, 51, 51))
    text(d, 32, 342, "colophon \u00b7 about \u00b7 rss", 11, (136, 136, 136))
    return im

def good_mild():
    """Superior page with mild deviations: slightly irregular gaps, footer
    in margin, hero band ~85% mass, one extra type size. Must stay GOOD
    with no FIRED defects."""
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    text(d, 32, 18, "Acme", 16, (20, 20, 20), True)
    rule(d, 52)
    text(d, 32, 76, "Build something great", 38, (17, 17, 17), True)
    text(d, 32, 132, "The fastest way to ship beautiful interfaces.", 17, (68, 68, 68))
    para(d, 32, 168, BODY3, 15, (51, 51, 51), 26)
    button(d, 32, 252, 144, 36, (37, 99, 235), "Get started")
    text(d, 32, 306, "Fast \u00b7 Simple \u00b7 Yours", 13, (85, 85, 85))
    text(d, 32, 344, "\u00a9 2026 Acme", 11, (150, 150, 150))
    return im

def bad_contrast_faint():
    """BLIND-SPOT CLASS: body text #d8d8d8 on white (|dL|=39 < 48, ratio
    ~1.17:1 -- near-invisible). Headings stay solid so solid ink exists."""
    F = (216, 216, 216)
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    text(d, 32, 18, "Acme", 16, (20, 20, 20), True)
    rule(d, 52)
    text(d, 32, 76, "Build something great", 38, (17, 17, 17), True)
    text(d, 32, 128, "The fastest way to ship beautiful interfaces.", 17, F)
    para(d, 32, 162, BODY3, 15, F, 24)
    button(d, 32, 244, 144, 36, (37, 99, 235), "Get started")
    text(d, 32, 300, "Fast", 15, F, True)
    text(d, 32, 322, "Renders in milliseconds.", 13, F)
    text(d, 256, 300, "Simple", 15, F, True)
    text(d, 256, 322, "One API to learn.", 13, F)
    return im

def bad_contrast_mid():
    """Low-contrast body #b8b8b8 on white (WCAG ~1.9:1, clearly poor)."""
    F = (184, 184, 184)
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    text(d, 32, 18, "Acme", 16, (20, 20, 20), True)
    rule(d, 52)
    text(d, 32, 76, "Build something great", 38, (17, 17, 17), True)
    text(d, 32, 128, "The fastest way to ship beautiful interfaces.", 17, F)
    para(d, 32, 162, BODY3, 15, F, 24)
    button(d, 32, 244, 144, 36, (37, 99, 235), "Get started")
    return im

def bad_clutter():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    y = 6
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit"]
    wi = 0
    while y < H - 8:
        x = 6
        while x < W - 60:
            w = words[wi % len(words)]; wi += 1
            text(d, x, y, w, 12, (30, 30, 30), bold=(wi % 5 == 0))
            x += len(w) * 7 + 8
        y += 16
    return im

def bad_spacing():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    y = 20
    for i, (gap, s) in enumerate([(0, "Section one"), (90, "Section two"),
                                  (12, "Section three"), (70, "Section four")]):
        y += gap
        text(d, 32, y, s, 22, (17, 17, 17), True)
        text(d, 32, y + 30, "Some body copy under the heading.", 14, (51, 51, 51))
        y += 52
    return im

def bad_margin():
    """All content crammed into the outer 10% rows (y<36, y>324)."""
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    text(d, 32, 6, "Crammed header line one", 15, (17, 17, 17), True)
    text(d, 32, 24, "Header line two fills the top margin.", 13, (51, 51, 51))
    text(d, 32, 328, "Footer line one fills the bottom.", 13, (51, 51, 51))
    text(d, 32, 344, "Footer line two, also crammed.", 13, (51, 51, 51))
    return im

def bad_align():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    xs = [32, 120, 64, 180, 96]
    ys = [40, 100, 160, 220, 280]
    for i in range(5):
        text(d, xs[i], ys[i], "Misaligned block %d" % (i + 1), 18, (17, 17, 17), True)
        text(d, xs[i] + 14, ys[i] + 28, "body copy here", 14, (51, 51, 51))
    return im

def bad_type():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    y = 24
    for i, sz in enumerate([52, 8, 36, 10, 44, 14, 32, 12, 24, 9]):
        text(d, 32, y, "Mixed size line %d" % i, sz, (17, 17, 17))
        y += sz + 8
    return im

def bad_color():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    cols = [(220, 40, 40), (40, 160, 40), (40, 80, 220), (230, 140, 20),
            (150, 40, 200), (20, 170, 170), (210, 40, 140), (120, 120, 20)]
    y = 24
    for i, c in enumerate(cols):
        text(d, 32, y, "Rainbow heading %d" % i, 20, c, True)
        y += 40
    return im

def bad_hierarchy():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    y = 18
    for i in range(6):
        text(d, 32, y, "Equal section %d" % (i + 1), 20, (17, 17, 17), True)
        text(d, 32, y + 26, "Two lines of same-weight copy.", 14, (51, 51, 51))
        y += 56
    return im

def bad_all():
    im = new((255, 255, 255)); d = ImageDraw.Draw(im)
    cols = [(220, 40, 40), (40, 160, 40), (40, 80, 220), (230, 140, 20)]
    y = 8
    xs = [10, 90, 40, 140]
    for i in range(8):
        text(d, xs[i % 4], y, "kitchen sink %d" % i, 16, cols[i % 4], bold=(i % 2 == 0))
        y += 20
    para(d, 200, 180, ["faint trailing copy here", "barely there at all"], 14, (210, 210, 210), 20)
    text(d, 300, 330, "crammed footer", 12, (60, 60, 60))
    return im

if __name__ == "__main__":
    for name, fn in [
        ("good_clean", good_clean), ("good_dark", good_dark),
        ("good_varied", good_varied), ("good_mild", good_mild),
        ("bad_contrast_faint", bad_contrast_faint),
        ("bad_contrast_mid", bad_contrast_mid),
        ("bad_clutter", bad_clutter), ("bad_spacing", bad_spacing),
        ("bad_margin", bad_margin), ("bad_align", bad_align),
        ("bad_type", bad_type), ("bad_color", bad_color),
        ("bad_hierarchy", bad_hierarchy), ("bad_all", bad_all),
    ]:
        save(fn(), name)
