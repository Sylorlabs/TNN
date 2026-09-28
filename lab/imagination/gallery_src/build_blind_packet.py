#!/usr/bin/env python3
"""Three-way blind rating packet: v1 vs v2 vs field, same briefs.
Deterministic shuffle (sha256 of item id). Writes blind_packet.html + blind_key.txt.
Images/audio referenced by relative filenames (copied into the packet dir).
"""
import os, shutil, hashlib

F = "/home/hatch/workspace/your_files/imagination_fields"
V1G = "/home/hatch/workspace/your_files/imagination_gallery"
V2G = "/home/hatch/workspace/your_files/imagination_v2"
VID = "/home/hatch/workspace/your_files/imagination_video"
OUT = os.path.join(F, "packet")
os.makedirs(OUT, exist_ok=True)

# Provenance (pure-TNN mandate 2026-09-22): field-track images/audio/video below are
# emitted natively by field.zag (BMP/AVI/WAV writers in Zag). v1/v2 PNGs are still
# Python-rendered and will be swapped for native BMPs when their Zag rasterizer lands.
PROVENANCE = {
    "field": "Zag-native (field.zag f3_emit_bmp/f3_emit_wav/f3_emit_avi)",
    "v1-machine": "Python renderer (pending native Zag re-render)",
    "v1-human": "Python renderer (pending native Zag re-render)",
    "v2-machine": "Python renderer (pending native Zag re-render)",
    "v2-human": "Python renderer (pending native Zag re-render)",
}

# (brief label, kind, [(track_label, src_path)])
items = {
    "brief1": ("visual", [
        ("v1-machine", f"{V1G}/brief1_machine_H.png"),
        ("v1-human", f"{V1G}/brief1_human_E.png"),
        ("v2-machine", f"{V2G}/brief1_machine.png"),
        ("v2-human", f"{V2G}/brief1_human.png"),
        ("field", f"{F}/f3b1.bmp"),
    ]),
    "brief2": ("visual", [
        ("v1-machine", f"{V1G}/brief2_machine_I.png"),
        ("v1-human", f"{V1G}/brief2_human_F.png"),
        ("v2-machine", f"{V2G}/brief2_machine.png"),
        ("v2-human", f"{V2G}/brief2_human.png"),
        ("field", f"{F}/f3b2.bmp"),
    ]),
    "brief3": ("audio", [
        ("v2-machine", f"{F}/a1_machine.wav"),
        ("v2-human", f"{F}/a1_human.wav"),
        ("field", f"{F}/f3a1.wav"),
    ]),
    "brief4": ("audio", [
        ("v2-machine", f"{F}/a2_machine.wav"),
        ("v2-human", f"{F}/a2_human.wav"),
        ("field", f"{F}/f3a2.wav"),
    ]),
    "brief5": ("visual", [
        ("v1-machine", f"{V1G}/brief5_machine_G.png"),
        ("v1-human", f"{V1G}/brief5_human_K.png"),
        ("field", f"{F}/f3b5.bmp"),
    ]),
    "brief6": ("visual", [
        ("v1-machine", f"{V1G}/brief6_machine_J.png"),
        ("v1-human", f"{V1G}/brief6_human_L.png"),
        ("field", f"{F}/f3b6.bmp"),
    ]),
}

BRIEF_TEXT = {
    "brief1": "Brief 1 — bakery logo 'Crumb & Craft': grain motif, warm palette, legible small.",
    "brief2": "Brief 2 — jazz-night poster: night feel, date + venue text zones, cool palette + one warm accent.",
    "brief3": "Brief 3 — four-note welcoming shop-door chime (listen).",
    "brief4": "Brief 4 — three-note tense kiosk error buzz (listen).",
    "brief5": "Brief 5 — five blocks on a shelf: largest at bottom, no overhang.",
    "brief6": "Brief 6 — four stones in a garden square: asymmetric, one dominant, airy.",
}

key = {}
html = ["<html><head><meta charset='utf-8'><title>Imagination blind packet (v1/v2/field)</title>",
        "<style>body{font-family:sans-serif;max-width:900px;margin:auto} .item{border:1px solid #ccc;margin:12px;padding:12px} img{max-width:420px} audio{width:420px}</style></head><body>",
        "<h1>Blind rating packet — imagination tracks</h1>",
        "<p>Rate each render 1-10 for how well it matches its brief. Items are shuffled; the key is in <code>blind_key.txt</code> (do not open until after rating).</p>"]
code_n = 0
for brief, (kind, lst) in items.items():
    order = sorted(lst, key=lambda t: hashlib.sha256((brief + t[0]).encode()).hexdigest())
    html.append(f"<h2>{BRIEF_TEXT[brief]}</h2>")
    for track, src in order:
        code_n += 1
        code = f"X{code_n:02d}"
        key[code] = f"{brief} {track}"
        ext = os.path.splitext(src)[1]
        dst = os.path.join(OUT, f"{code}{ext}")
        shutil.copy(src, dst)
        tag = f"<img src='{code}{ext}'>" if kind == "visual" else f"<audio controls src='{code}{ext}'></audio>"
        html.append(f"<div class='item'><b>{code}</b> <i>({PROVENANCE[track]})</i><br>{tag}<br>rating (1-10): ____</div>")
html.append("<h1>Field novel probes (field track only — not blind)</h1>")
html.append("<p>Novel combinations from M2f. All images/audio/video below are Zag-native (pure TNN). Rate 1-10 for brief fit.</p>")
NOVELS = [
    ("n11", "Glass staircase underwater at dusk"),
    ("n12", "Brass band in a library, zero gravity"),
    ("n13", "Thunderstorm inside a honey cathedral"),
    ("n14", "Robot drinking tea on a glacier at sunrise"),
    ("n15", "Thunderstorm with a distant church bell"),
    ("n16", "Music-box lullaby in the rain"),
    ("n17", "An entire short song (generative composition)"),
    ("n18", "A sound you have never heard"),
]
for code, label in NOVELS:
    html.append(f"<h2>{label}</h2>")
    bmp = os.path.join(F, f"f3{code}.bmp")
    if code in ("n11", "n12", "n13", "n14"):
        dst = os.path.join(OUT, f"novel_{code}.bmp"); shutil.copy(bmp, dst)
        html.append(f"<div class='item'><img src='novel_{code}.bmp'><br>rating (1-10): ____</div>")
    elif code in ("n15", "n16"):
        # f3wav names novel audio files by element number: n15 -> f3n5.wav, n16 -> f3n6.wav
        wav = os.path.join(F, f"f3n{code[2:]}.wav")
        dst = os.path.join(OUT, f"novel_{code}.wav"); shutil.copy(wav, dst)
        html.append(f"<div class='item'><audio controls src='novel_{code}.wav'></audio><br>rating (1-10): ____</div>")
    elif code == "n17":
        dst = os.path.join(OUT, "novel_n17_song.wav"); shutil.copy(os.path.join(F, "f3song.wav"), dst)
        html.append(f"<div class='item'><audio controls src='novel_n17_song.wav'></audio><br>does it sound like a song? (1-10): ____</div>")
    else:
        dst = os.path.join(OUT, "novel_n18_unheard.wav"); shutil.copy(os.path.join(F, "f3unheard.wav"), dst)
        html.append(f"<div class='item'><audio controls src='novel_n18_unheard.wav'></audio><br>genuinely novel? (1-10): ____</div>")
html.append("<h1>Audiovisual scenes (field track — Zag-native AVI)</h1>")
html.append("<p>24 frames @ 8fps, 240x240, with imagined soundtracks. Browsers cannot play AVI inline — download and open in VLC.</p>")
for v, label in ((1, "Glacier sunrise (wind + ice chimes)"), (2, "City of bells at night (bells + night noise)")):
    dst = os.path.join(OUT, f"scene{v}.avi"); shutil.copy(os.path.join(VID, f"f3vid{v}.avi"), dst)
    html.append(f"<div class='item'><b>{label}</b><br><a href='scene{v}.avi'>scene{v}.avi (4.2 MB, download + open in VLC)</a><br>rating (1-10): ____</div>")
html.append("<h1>Provenance</h1><p>Field track: pure TNN — every pixel, sample, and container byte emitted by field.zag. v1/v2 images: Python renderer (native Zag re-render pending); v1/v2 audio WAVs are Zag-native.</p>")
html.append("</body></html>")
open(os.path.join(OUT, "blind_packet.html"), "w").write("\n".join(html))
with open(os.path.join(OUT, "blind_key.txt"), "w") as f:
    for c in sorted(key):
        f.write(f"{c} {key[c]}\n")
print("packet items:", code_n)
print("key entries:", len(key))
