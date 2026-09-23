#!/usr/bin/env python3
"""R2-11 human package builder.

For each of the 200 frozen trials:
  - copies the source fixture -> viewable (PNG/WAV/GIF)
  - fork A artifact (replay)    -> viewable, blind-labeled P or Q
  - fork B artifact (render)    -> viewable, blind-labeled Q or P
  - per-trial brief: claim, boundaries, warrant, divergence declaration
Runs the audio-consistency gate and visual-boundary sanity checks.
Writes the sealed key (P/Q -> fork mapping, truth, judgments).

P/Q assignment: splitmix64(SEED+1) bit per trial (documented, deterministic).
"""
import os, struct, subprocess, wave

LAB = os.path.expanduser("~/workspace/tnn-lab")
WORK = os.path.join(LAB, "senses/pam-rebuild/round2/work/r2-11")
PKG = os.path.join(WORK, "human_pkg")
SEED = 20260923
os.makedirs(PKG, exist_ok=True)
os.makedirs(os.path.join(PKG, "briefs"), exist_ok=True)

VIEW = {"img": "png", "pcm": "wav", "vid": "gif"}
EXT_OF = {"colordisc": "img", "colorconst": "img", "shapetrans": "img",
          "pitchdisc": "pcm", "timbredisc": "pcm", "motiondir": "vid"}

def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = x
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return z ^ (z >> 31)

def read_raw(path):
    with open(path, "rb") as f:
        return f.read()

def to_viewable(task, raw, outpath):
    """Convert raw fixture/artifact bytes to a viewable file. Returns (w,h,info)."""
    ext = VIEW[EXT_OF[task]]
    if task in ("colordisc", "colorconst"):
        w, h = struct.unpack("<II", raw[:8])
        px = raw[8:8 + w * h * 3]
        from PIL import Image
        im = Image.frombytes("RGB", (w, h), px)
        im.save(outpath)
        return (w, h, "%dx%d rgb" % (w, h))
    if task == "shapetrans":
        w, h = struct.unpack("<II", raw[:8])
        px = raw[8:8 + w * h * 3]
        from PIL import Image
        im = Image.frombytes("RGB", (w, h), px)
        im.save(outpath)
        return (w, h, "%dx%d rgb" % (w, h))
    if task in ("pitchdisc", "timbredisc"):
        rate, n = struct.unpack("<II", raw[:8])
        import numpy as np
        s = np.frombuffer(raw[8:8 + n * 2], dtype=np.int16)
        with wave.open(outpath, "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate)
            wf.writeframes(s.tobytes())
        dur = n / rate
        return (rate, n, "%.2fs mono" % dur)
    if task == "motiondir":
        nf, w, h = struct.unpack("<III", raw[:12])
        from PIL import Image
        frames = []
        for i in range(nf):
            px = raw[12 + i * w * h * 3:12 + (i + 1) * w * h * 3]
            frames.append(Image.frombytes("RGB", (w, h), px).resize((256, 256), Image.NEAREST))
        frames[0].save(outpath, save_all=True, append_images=frames[1:], duration=150, loop=0)
        return (w, h, "%d frames" % nf)
    raise ValueError(task)

def run_sense(fork, task, fixture, artifact):
    b = os.path.join(WORK, "zag", "sense" + fork)
    p = subprocess.run([b, task, fixture, "emit", "", artifact],
                       capture_output=True, text=True, timeout=120)
    line = p.stdout.strip().split("\n")[0]
    return line.split("\t")

trials = []
for line in open(os.path.join(WORK, "lists", "human_200.txt")):
    hid, task, path, kind = line.strip().split(" ", 3)
    trials.append((hid, task, os.path.join(LAB, path), kind, path))

rng = SEED + 1
key_lines = ["# SEALED - P/Q to fork mapping, truth, judgments. NOT for the judge."]
brief_index = []
gate_fails = []

for hid, task, fixture, kind, relpath in trials:
    rng = splitmix64(rng)
    p_is_a = (rng & 1) == 0  # 1 -> P=forkA, Q=forkB
    ext = VIEW[EXT_OF[task]]
    src_view = os.path.join(PKG, "%s_src.%s" % (hid, ext))
    p_view = os.path.join(PKG, "%s_P.%s" % (hid, ext))
    q_view = os.path.join(PKG, "%s_Q.%s" % (hid, ext))

    raw_src = read_raw(fixture)
    # fork A artifact (raw, then viewable)
    a_raw_path = os.path.join(PKG, "%s_A.raw" % hid)
    b_raw_path = os.path.join(PKG, "%s_B.raw" % hid)
    ta = run_sense("A", task, fixture, a_raw_path)
    tb = run_sense("B", task, fixture, b_raw_path)
    raw_a = read_raw(a_raw_path)
    raw_b = read_raw(b_raw_path)

    # viewables: source + blind P/Q
    to_viewable(task, raw_src, src_view)
    if p_is_a:
        to_viewable(task, raw_a, p_view); to_viewable(task, raw_b, q_view)
    else:
        to_viewable(task, raw_b, p_view); to_viewable(task, raw_a, q_view)

    # TSV columns A: trial seq task fixture truth judgment conf disp correct percept_hex ops cited_sha artifact_sha equal ledger_hash
    # TSV columns B: trial seq task fixture truth judgment conf disp correct percept_hex ops render_sha div_runs div_bytes div_first_start div_first_len ledger_hash
    truth, judg, conf, disp = ta[4], ta[5], ta[6], ta[7]
    assert tb[5] == judg and tb[4] == truth, (hid, "fork judgment mismatch")
    percept_hex = ta[9]
    div_runs, div_bytes = tb[12], tb[13]
    df_start, df_len = tb[14], tb[15]
    cited_len = {"colordisc": 24576, "colorconst": 24576, "shapetrans": 27648,
                 "pitchdisc": 25600, "timbredisc": 25600, "motiondir": 98304}[task]

    key_lines.append("%s P=%s Q=%s truth=%s judgment=%s conf=%s disp=%s div_runs=%s div_bytes=%s" % (
        hid, "forkA" if p_is_a else "forkB", "forkB" if p_is_a else "forkA",
        truth, judg, conf, disp, div_runs, div_bytes))

    # ---- gates ----
    fails = []
    if task in ("pitchdisc", "timbredisc"):
        import numpy as np
        for tag, raw in (("P", raw_a if p_is_a else raw_b), ("Q", raw_b if p_is_a else raw_a)):
            rate, n = struct.unpack("<II", raw[:8])
            s = np.frombuffer(raw[8:8 + n * 2], dtype=np.int16).astype(np.float64)
            peak = np.max(np.abs(s))
            if peak > 24575: fails.append("%s peak %d exceeds 0.75FS" % (tag, peak))
            if peak < 1000: fails.append("%s near-silent peak %d" % (tag, peak))
            dc = abs(np.mean(s))
            if peak > 0 and dc / peak > 0.02: fails.append("%s DC offset %.3f of peak" % (tag, dc / peak))
            wins = np.array_split(s, 8)
            rms = [np.sqrt(np.mean(w ** 2)) + 1e-9 for w in wins]
            if max(rms) / min(rms) > 3.0:
                fails.append("%s envelope non-stationary ratio %.2f" % (tag, max(rms) / min(rms)))
            if task == "pitchdisc":
                j = 6400
                dj = abs(s[j] - s[j - 1])
                if peak > 0 and dj / peak > 0.5:
                    fails.append("%s tone-join click %.3f of peak" % (tag, dj / peak))
    if task in ("colordisc", "colorconst", "shapetrans"):
        for tag, raw in (("P", raw_a if p_is_a else raw_b), ("Q", raw_b if p_is_a else raw_a)):
            w, h = struct.unpack("<II", raw[:8])
            px = raw[8:]
            exp = w * h * 3
            if len(px) != exp: fails.append("%s payload %d != %d" % (tag, len(px), exp))
            if len(set(px)) < 2: fails.append("%s degenerate single-value image" % tag)
    if task == "motiondir":
        for tag, raw in (("P", raw_a if p_is_a else raw_b), ("Q", raw_b if p_is_a else raw_a)):
            nf, w, h = struct.unpack("<III", raw[:12])
            if nf != 8: fails.append("%s frames %d != 8" % (tag, nf))
            import numpy as np
            sq = 0
            for i in range(nf):
                fr = np.frombuffer(raw[12 + i * w * h * 3:12 + (i + 1) * w * h * 3], dtype=np.uint8)
                if np.max(fr) > 128: sq += 1
            if sq < 8: fails.append("%s bright square missing in %d/8 frames" % (tag, 8 - sq))
    if fails:
        gate_fails.append((hid, fails))

    # ---- brief ----
    strat = "adversarial family " + kind if kind != "CLEAN" else "clean"
    with open(os.path.join(PKG, "briefs", "%s.md" % hid), "w") as bf:
        bf.write("# %s - %s (%s)\n\n" % (hid, task, strat))
        bf.write("Files: `%s_src.%s` (source), `%s_P.%s` (artifact P), `%s_Q.%s` (artifact Q).\n\n"
                 % (hid, ext, hid, ext, hid, ext))
        bf.write("## System claim about the source (shared percept, both forks)\n\n")
        bf.write("- judgment: **%s** (confidence %s/1000, disposition %s)\n" % (judg, conf, disp))
        bf.write("- warrant (percept bytes): `%s`\n\n" % percept_hex)
        bf.write("## Artifact P - maker's declaration\n\n")
        if p_is_a:
            bf.write("Byte-exact replay of the cited source span(s). Nothing synthesized,\n"
                     "nothing re-encoded. The only bytes not carried over are the container\n"
                     "header and, for pitchdisc, the 0.16 s inter-tone gap (excluded by the\n"
                     "citation by design).\n\n")
        else:
            bf.write("Resynthesized from the 64-byte percept alone - the maker never saw the\n"
                     "source bytes. Divergent payload bytes vs the cited source: **%s of %s**\n"
                     "in %s runs (first run at byte %s, length %s). Everything else is\n"
                     "reconstruction: panels/tones/shapes/square are canonical forms, not copies.\n\n"
                     % (div_bytes, cited_len, div_runs, df_start, df_len))
        bf.write("## Artifact Q - maker's declaration\n\n")
        if not p_is_a:
            bf.write("Byte-exact replay of the cited source span(s). Nothing synthesized,\n"
                     "nothing re-encoded. The only bytes not carried over are the container\n"
                     "header and, for pitchdisc, the 0.16 s inter-tone gap (excluded by the\n"
                     "citation by design).\n\n")
        else:
            bf.write("Resynthesized from the 64-byte percept alone - the maker never saw the\n"
                     "source bytes. Divergent payload bytes vs the cited source: **%s of %s**\n"
                     "in %s runs (first run at byte %s, length %s). Everything else is\n"
                     "reconstruction: panels/tones/shapes/square are canonical forms, not copies.\n\n"
                     % (div_bytes, cited_len, div_runs, df_start, df_len))
        bf.write("## For the judge\n\n")
        bf.write("1. Does artifact P sound/look the SAME as the source? (KB-E3)\n")
        bf.write("2. Does artifact Q sound/look the SAME as the source? (KB-E3)\n")
        bf.write("3. Is P's declaration honest about what changed? Is Q's?\n")
        bf.write("4. Does either artifact misrepresent what the source shows? (KB-E4/KB-E8)\n")
        bf.write("5. Head-to-head: which artifact would you trust as a witness of the source? (KB-E8)\n")
    brief_index.append((hid, task, kind, truth, judg))
    # remove raw intermediates (keep viewables + briefs)
    os.remove(a_raw_path); os.remove(b_raw_path)

with open(os.path.join(WORK, "sealed", "human_200_key.txt"), "a") as f:
    f.write("\n".join(key_lines) + "\n")

with open(os.path.join(PKG, "GATE_REPORT.md"), "w") as f:
    f.write("# R2-11 human-package gate report\n\n")
    f.write("Audio-consistency gate (peak/DC/stationarity/join-click) and\n"
            "visual-boundary sanity (dims/payload/degeneracy/square-presence)\n"
            "run over all 400 blind artifacts.\n\n")
    if gate_fails:
        f.write("## FAILURES (%d trials)\n\n" % len(gate_fails))
        for hid, fails in gate_fails:
            f.write("- %s: %s\n" % (hid, "; ".join(fails)))
    else:
        f.write("All 400 artifacts passed.\n")

print("trials packaged:", len(trials))
print("gate failures:", len(gate_fails))
for hid, fails in gate_fails[:10]:
    print(" ", hid, fails)
