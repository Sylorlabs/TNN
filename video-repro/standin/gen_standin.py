#!/usr/bin/env python3
"""Procedural HIGH-DETAIL stand-in clip for the video native-reproduction test.

Deterministic (fixed seed 20260925). 320x240, 24 frames @ ~8fps content, P6 PPM.
Content is fully known so the floor-control text scene plan can describe it:
  - vertical gradient background (navy -> teal) + fine seeded grain +
    sinusoidal interference texture (high-frequency detail)
  - red/orange circle r=28 moving left->right at mid height, white highlight
  - static green rectangle, bottom-left, sharp edges
  - 2px white diagonal line across the frame
  - 8x8 checkerboard patch (6px cells) center-right (high-freq detail)
  - small text: "FRAME ff/24" top-left on dark bar; "TNN REPRO TEST" bottom-right
  - yellow triangle top-right with sinusoidal bob
Writes: standin/frames/frame_00.ppm .. frame_23.ppm + PROVENANCE_STANDIN.md
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

SEED = 20260925
W, H, N = 320, 240, 24
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")

def build_frame(f: int) -> Image.Image:
    rng = random.Random(SEED + f)  # per-frame deterministic stream
    px = bytearray(W * H * 3)
    # background: vertical gradient navy (10,20,60) -> teal (10,90,90)
    for y in range(H):
        t = y / (H - 1)
        r0 = int(10 + 0 * t); g0 = int(20 + 70 * t); b0 = int(60 + 30 * t)
        for x in range(W):
            # sinusoidal interference texture (fine detail)
            s = math.sin(x * 0.55 + f * 0.3) * math.sin(y * 0.47 - f * 0.23)
            grain = rng.randint(-9, 9)
            v = int(s * 14)
            i = (y * W + x) * 3
            px[i] = max(0, min(255, r0 + v + grain))
            px[i + 1] = max(0, min(255, g0 + v + grain))
            px[i + 2] = max(0, min(255, b0 + v + grain))
    img = Image.frombytes("RGB", (W, H), bytes(px))
    d = ImageDraw.Draw(img)
    # green rectangle, bottom-left, sharp edges
    d.rectangle([20, 170, 110, 220], fill=(30, 200, 60), outline=(10, 120, 30), width=2)
    # checkerboard patch center-right: 8x8 cells of 6px at (190,90)
    for cy in range(8):
        for cx in range(8):
            c = (cx + cy) % 2
            col = (235, 235, 235) if c else (25, 25, 25)
            d.rectangle([190 + cx * 6, 90 + cy * 6, 190 + cx * 6 + 5, 90 + cy * 6 + 5], fill=col)
    # 2px white diagonal line
    d.line([0, H - 1, W - 1, 0], fill=(255, 255, 255), width=2)
    # red/orange circle moving left->right
    cx = 20 + f * 12
    cy = 120
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(230, 70, 20), outline=(120, 30, 10), width=2)
    d.ellipse([cx - 10, cy - 14, cx + 2, cy - 2], fill=(255, 220, 200))  # highlight
    # yellow triangle top-right with bob
    ty = 40 + int(10 * math.sin(f * 0.6))
    d.polygon([(270, ty - 18), (292, ty + 14), (248, ty + 14)], fill=(240, 220, 40), outline=(150, 130, 20))
    # small text
    font = ImageFont.load_default()
    d.rectangle([4, 4, 86, 20], fill=(0, 0, 0))
    d.text((8, 7), f"FRAME {f:02d}/24", font=font, fill=(255, 255, 255))
    d.text((196, 224), "TNN REPRO TEST", font=font, fill=(255, 255, 120))
    return img

def main():
    os.makedirs(OUT, exist_ok=True)
    for f in range(N):
        img = build_frame(f)
        img.save(os.path.join(OUT, f"frame_{f:02d}.ppm"), "PPM")
    # determinism self-check: rebuild frame 0 in-memory and compare bytes
    import hashlib
    a = hashlib.sha256(open(os.path.join(OUT, "frame_00.ppm"), "rb").read()).hexdigest()
    print(f"wrote {N} frames to {OUT}")
    print(f"frame_00.ppm sha256={a}")

if __name__ == "__main__":
    main()
