#!/usr/bin/env python3
"""B7 artifacts for fork H1 (TEST GLUE).

Event-lattice overlay PNGs on representative fixtures + native witness-span
audio excerpts (bit-exact source spans) + BRIEF_B7.md.
Human verdicts are Micah's call -- this script only builds the artifacts.

Selection (from evidence/runs/h1_run1.jsonl), per task:
  (a) one primary fixture: disp=INSTALL and judgment==truth (clean case)
  (b) one h1_adv fixture: prefer disp=WITHHELD (contract caught a trap);
      else a false INSTALL (honest failure); else first h1_adv.
"""
import json, os, struct, subprocess, sys, wave

HOME = os.path.expanduser("~")
FORK = os.path.join(HOME, "workspace/tnn-lab/senses/pam-rebuild/forks/H1")
H1 = os.path.join(FORK, "build/h1")
RUN1 = os.path.join(FORK, "evidence/runs/h1_run1.jsonl")
OUT = os.path.join(FORK, "evidence/b7")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc",
         "timbredisc", "motiondir"]

def read_img(p):
    with open(p, "rb") as f:
        d = f.read()
    w, h = struct.unpack("<II", d[:8])
    px = d[8:8 + w * h * 3]
    return w, h, px

def read_pcm(p):
    with open(p, "rb") as f:
        d = f.read()
    sr, n = struct.unpack("<II", d[:8])
    sm = struct.unpack("<%dh" % n, d[8:8 + 2 * n])
    return sr, n, sm

def read_vid(p):
    with open(p, "rb") as f:
        d = f.read()
    nf, w, h = struct.unpack("<III", d[:12])
    frames = []
    o = 12
    for _ in range(nf):
        frames.append(d[o:o + w * h * 3]); o += w * h * 3
    return nf, w, h, frames

def parse_ev(line):
    # "ev id=.. span=a:b ent=.. pred=P attr=lo:hi wit=m:ws:wl[;..] sup=n con=n alt=.."
    parts = line.split()
    d = {}
    for p in parts[1:]:
        k, v = p.split("=", 1)
        d[k] = v
    wits = []
    for w in d["wit"].split(";"):
        m, ws, wl = w.split(":")
        wits.append((m, int(ws), int(wl)))
    s0, s1 = d["span"].split(":")
    return {"pred": d["pred"], "span": (int(s0), int(s1)),
            "attr": d["attr"], "wit": wits,
            "sup": int(d["sup"]), "con": int(d["con"]), "alt": d["alt"]}

def h1_out(task, fixture):
    r = subprocess.run([H1, task, fixture], capture_output=True, timeout=300)
    assert r.returncode == 0, (task, fixture, r.stderr[:200])
    kv, evs = {}, []
    for line in r.stdout.decode().split("\n"):
        if line.startswith("ev "):
            evs.append(parse_ev(line))
        elif "=" in line and line and not line.startswith(" "):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv, evs

def span_bbox(ws, wl, W):
    xs = [(ws + i) % W for i in range(wl)]
    ys = [(ws + i) // W for i in range(wl)]
    return min(xs), min(ys), max(xs), max(ys)

def overlay_image(task, fixture, kv, evs, outpng, caption):
    from PIL import Image, ImageDraw
    w, h, px = read_img(fixture)
    im = Image.frombytes("RGB", (w, h), px).convert("RGB")
    scale = max(1, 640 // max(w, h))
    im = im.resize((w * scale, h * scale), Image.NEAREST)
    dr = ImageDraw.Draw(im, "RGBA")
    cols = [(255, 0, 0), (0, 255, 0), (0, 120, 255), (255, 200, 0)]
    for ei, ev in enumerate(evs[:6]):
        c = cols[ei % 4]
        for m, ws, wl in ev["wit"]:
            if m != "img":
                continue
            x0, y0, x1, y1 = span_bbox(ws, wl, w)
            dr.rectangle([x0 * scale, y0 * scale, (x1 + 1) * scale,
                          (y1 + 1) * scale], outline=c + (255,), width=2)
        dr.text((4, 4 + ei * 14),
                f"{ev['pred']} sup={ev['sup']} con={ev['con']} attr={ev['attr']}",
                fill=cols[ei % 4] + (255,))
    dr.text((4, h * scale - 16), caption, fill=(255, 255, 255, 255))
    im.save(outpng)

def audio_excerpts(task, fixture, kv, evs, outdir, tag):
    sr, n, sm = read_pcm(fixture)
    paths = []
    for ei, ev in enumerate(evs[:4]):
        for wi, (m, ws, wl) in enumerate(ev["wit"]):
            if m != "pcm":
                continue
            ws = max(0, min(ws, n - 1)); wl = max(1, min(wl, n - ws))
            seg = sm[ws:ws + wl]
            p = os.path.join(outdir, f"{tag}_ev{ei}_{ev['pred']}_wit{wi}.wav")
            with wave.open(p, "wb") as wf:
                wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
                wf.writeframes(struct.pack("<%dh" % len(seg), *seg))
            paths.append((p, ev['pred'], ws, wl, sr))
    # waveform PNG with witness spans shaded
    from PIL import Image, ImageDraw
    W, H = 900, 220
    im = Image.new("RGB", (W, H), (10, 10, 14))
    dr = ImageDraw.Draw(im, "RGBA")
    step = max(1, n // W)
    peak = max(1, max(abs(s) for s in sm[::step]))
    for x in range(W):
        s = sm[min(n - 1, x * step)]
        y = int(H / 2 - s / peak * (H / 2 - 10))
        dr.line([(x, H / 2), (x, y)], fill=(120, 160, 220))
    cols = [(255, 90, 90, 90), (90, 255, 120, 90), (90, 140, 255, 90),
            (255, 210, 90, 90)]
    for ei, ev in enumerate(evs[:4]):
        for m, ws, wl in ev["wit"]:
            if m != "pcm":
                continue
            x0, x1 = ws / n * W, (ws + wl) / n * W
            dr.rectangle([x0, 0, x1, H], fill=cols[ei % 4])
            dr.text((x0 + 2, 4 + ei * 14), ev["pred"],
                    fill=(255, 255, 255, 255))
    dr.text((4, H - 16),
            f"{os.path.basename(fixture)} sr={sr} n={n} "
            f"judg={kv['judgment']} conf={kv['confidence']} disp={kv['disp']}",
            fill=(255, 255, 255, 255))
    im.save(os.path.join(outdir, f"{tag}_waveform.png"))
    return paths

def overlay_video(task, fixture, kv, evs, outpng, caption):
    from PIL import Image, ImageDraw
    import math
    nf, w, h, frames = read_vid(fixture)
    mid = frames[nf // 2]
    im = Image.frombytes("RGB", (w, h), mid).convert("RGB")
    scale = max(1, 480 // max(w, h))
    im = im.resize((w * scale, h * scale), Image.NEAREST)
    dr = ImageDraw.Draw(im, "RGBA")
    # direction arrow from the DIR_* top event
    arrow = {"DIR_N": (0, -1), "DIR_NE": (1, -1), "DIR_E": (1, 0),
             "DIR_SE": (1, 1), "DIR_S": (0, 1), "DIR_SW": (-1, 1),
             "DIR_W": (-1, 0), "DIR_NW": (-1, -1), "DIR_STILL": (0, 0)}
    for ev in evs:
        if ev["pred"] in arrow:
            dx, dy = arrow[ev["pred"]]
            cx, cy = w * scale // 2, h * scale // 2
            L = 60
            dr.line([(cx, cy), (cx + dx * L, cy + dy * L)],
                    fill=(255, 60, 60, 255), width=4)
            dr.text((4, 4), f"{ev['pred']} sup={ev['sup']} con={ev['con']}",
                    fill=(255, 60, 60, 255))
            break
    for ei, ev in enumerate(evs[:7]):
        s0, s1 = ev["span"]
        dr.text((4, 20 + ei * 14),
                f"span {s0}:{s1} {ev['pred']} sup={ev['sup']} con={ev['con']}",
                fill=(255, 255, 255, 220))
    dr.text((4, h * scale - 16), caption, fill=(255, 255, 255, 255))
    im.save(outpng)

def main():
    os.makedirs(OUT, exist_ok=True)
    recs = [json.loads(l) for l in open(RUN1)]
    brief = []
    for task in TASKS:
        prim = [r for r in recs if r["task"] == task and r["variant"] == "primary"]
        adv = [r for r in recs if r["task"] == task and r["variant"] == "h1_adv"]
        a = next(r for r in prim
                 if r["kv"]["disp"] == "INSTALL"
                 and r["kv"]["judgment"] == r["truth"])
        withheld = [r for r in adv if r["kv"]["disp"] == "WITHHELD"]
        if withheld:
            b = withheld[0]
            note = "contract WITHHELD a misleading input"
        else:
            bad = [r for r in adv if r["kv"]["judgment"] != r["truth"]]
            b = bad[0] if bad else adv[0]
            note = "contract INSTALLED on an adversarial input (shown honestly)"
        for tag, r, tagnote in (
                ("clean", a, "clean primary fixture: correct judgment, "
                 "contract INSTALLED (baseline behavior)"),
                ("trap", b, note)):
            kv, evs = h1_out(task, r["fixture"])
            fn = os.path.basename(r["fixture"])
            cap = (f"{fn} truth={r['truth']} H1={kv['judgment']} "
                   f"conf={kv['confidence']} disp={kv['disp']}")
            if task in ("colordisc", "colorconst", "shapetrans"):
                p = os.path.join(OUT, f"{task}_{tag}_overlay.png")
                overlay_image(task, r["fixture"], kv, evs, p, cap)
                brief.append((task, tag, p, cap, tagnote,
                              f"{len(evs)} event records; witness rects = "
                              f"the exact spans H1 measured"))
            elif task in ("pitchdisc", "timbredisc"):
                paths = audio_excerpts(task, r["fixture"], kv, evs, OUT,
                                       f"{task}_{tag}")
                wavs = ", ".join(os.path.basename(p) for p, *_ in paths)
                brief.append((task, tag, wavs, cap, tagnote,
                              "bit-exact witness-span excerpts; waveform PNG "
                              "shows shaded spans H1 measured"))
            else:
                p = os.path.join(OUT, f"{task}_{tag}_overlay.png")
                overlay_video(task, r["fixture"], kv, evs, p, cap)
                brief.append((task, tag, p, cap, tagnote,
                              "middle frame; red arrow = DIR event; span "
                              "events listed"))
    with open(os.path.join(OUT, "BRIEF_B7.md"), "w") as f:
        f.write("# B7 artifacts — fork H1: Witnessed Event Lattice\n\n")
        f.write("Human verdict: **PENDING-MICAH** (never silently passed).\n\n")
        f.write("Preregistered human bars (PREREG_H1.md §8 B7 / §9):\n")
        f.write("- native audio replay must pass a human double-blind "
                "field-recording equivalence test at 90% agreement;\n")
        f.write("- visual reconstruction/imagery judged realistic by >=80% "
                "of raters.\n\n")
        f.write("What each artifact shows: the event lattice H1 actually "
                "built from the fixture (witness spans = the exact input "
                "regions measured; sup/con = integer support/contradiction; "
                "disp = the memory contract's disposition). Audio excerpts "
                "are bit-exact slices of the fixture's own samples -- "
                "what H1 heard, nothing synthesized.\n\n")
        for task, tag, art, cap, note, desc in brief:
            f.write(f"## {task} / {tag}\n\n{cap}\n\nnote: {note}.\n\n"
                    f"artifact: `{os.path.basename(str(art))}`\n\n{desc}\n\n")
    print("B7 done ->", OUT)

if __name__ == "__main__":
    main()
