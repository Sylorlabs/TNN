#!/usr/bin/env python3
"""Build R2-10 human-judgment packages (train + eval samples).

Pure packaging glue — no TNN decisions. For each of the 400 frozen sample
trials (200 train + 200 eval, disjoint manifests):
  1. runs the FROZEN sense binary in emit mode -> judgment + emission artifact
  2. converts source fixture -> viewable media (PNG / WAV / animated GIF)
  3. converts emission artifact -> viewable media (WAV / PNG)
  4. runs the pre-delivery consistency gate (audio waveform checks calibrated
     on human reference WAVs; visual boundary sanity)
  5. writes a blinded per-trial brief (claim + emission + source only;
     NO confidence, disposition, truth, or family)
  6. deterministic double-blind presentation order (splitmix64, fixed seed)
  7. index.html for viewing + verdict_sheet.tsv for recording

The judge's verdicts are used as:
  - TRAIN sample: "witnessed correctly" (human verdict == fork judgment)
    disciplines the install gate via `sense revise` (deliberate audited
    revision, constitutional veto, then freeze).
  - EVAL sample: KB-E6 = gate INSTALL/WITHHOLD agreement with
    "witnessed correctly" >= 90%.
"""
import hashlib
import os
import struct
import subprocess
import sys

R2 = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10")
FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures")
SENSE = os.path.join(R2, "src", "sense")
EV = os.path.join(R2, "evidence")
HUM = os.path.join(EV, "human")
REFDIR = os.path.expanduser("~/workspace/goals/tnn-real-ai-architecture/files/imagination_audio")

TASK_EXT = {"colordisc": "img", "colorconst": "img", "shapetrans": "img",
            "pitchdisc": "pcm", "timbredisc": "pcm", "motiondir": "vid"}
TASK_PLAIN = {"colordisc": "color discrimination", "colorconst": "surface color constancy",
              "shapetrans": "shape identification", "pitchdisc": "pitch discrimination",
              "timbredisc": "timbre classification", "motiondir": "motion direction"}
CHOICES = {"colordisc": "SAME / DIFFERENT",
           "colorconst": "SAME_SURFACE / DIFFERENT",
           "shapetrans": "CIRCLE / SQUARE / TRIANGLE",
           "pitchdisc": "SAME / HIGHER / LOWER",
           "timbredisc": "PURE / DARK / RICH / BRIGHT",
           "motiondir": "E / NE / N / NW / W / SW / S / SE / STILL"}
CLAIM_WORDS = {
    ("colordisc", "SAME"): "the two color patches are the SAME color",
    ("colordisc", "DIFFERENT"): "the two color patches are DIFFERENT colors",
    ("colorconst", "SAME_SURFACE"): "the surface is the SAME under the two lights",
    ("colorconst", "DIFFERENT"): "the surfaces are DIFFERENT",
    ("shapetrans", "CIRCLE"): "the shape is a CIRCLE",
    ("shapetrans", "SQUARE"): "the shape is a SQUARE",
    ("shapetrans", "TRIANGLE"): "the shape is a TRIANGLE",
    ("pitchdisc", "SAME"): "the two tones are the SAME pitch",
    ("pitchdisc", "HIGHER"): "the second tone is HIGHER than the first",
    ("pitchdisc", "LOWER"): "the second tone is LOWER than the first",
    ("timbredisc", "PURE"): "the tone's timbre is PURE (a clean sine-like tone)",
    ("timbredisc", "DARK"): "the tone's timbre is DARK (mellow, few harmonics)",
    ("timbredisc", "RICH"): "the tone's timbre is RICH (many harmonics)",
    ("timbredisc", "BRIGHT"): "the tone's timbre is BRIGHT (strong high harmonics)",
    ("motiondir", "E"): "the motion goes EAST (right)",
    ("motiondir", "NE"): "the motion goes NORTHEAST",
    ("motiondir", "N"): "the motion goes NORTH (up)",
    ("motiondir", "NW"): "the motion goes NORTHWEST",
    ("motiondir", "W"): "the motion goes WEST (left)",
    ("motiondir", "SW"): "the motion goes SOUTHWEST",
    ("motiondir", "S"): "the motion goes SOUTH (down)",
    ("motiondir", "SE"): "the motion goes SOUTHEAST",
    ("motiondir", "STILL"): "there is NO motion (still)",
}
TASK_OF_FIXTURE = {}
for _t, _e in TASK_EXT.items():
    TASK_OF_FIXTURE[_e] = _t


def task_of(fixture):
    ext = fixture.rsplit(".", 1)[1]
    for t, e in TASK_EXT.items():
        if e == ext and ("_%s_" % t in fixture or fixture.startswith("r2n_%s" % t) or fixture.startswith("r2a_%s" % t)):
            return t
    # fall back: match task infix
    for t in TASK_EXT:
        if "_%s_" % t in fixture:
            return t
    raise ValueError("unknown task for " + fixture)


def splitmix64(state):
    state = (state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return state, (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF


def det_shuffle(n, seed):
    idx = list(range(n))
    st = seed
    for i in range(n - 1, 0, -1):
        st, r = splitmix64(st)
        j = r % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return idx, st


def read_img(p):
    d = open(p, "rb").read()
    w, h = struct.unpack("<II", d[:8])
    return w, h, d[8:8 + w * h * 3]


def read_pcm(p):
    d = open(p, "rb").read()
    sr, cnt = struct.unpack("<II", d[:8])
    return sr, cnt, d[8:8 + cnt * 2]


def read_vid(p):
    d = open(p, "rb").read()
    nf, w, h = struct.unpack("<III", d[:12])
    fsz = w * h * 3
    frames = [d[12 + i * fsz:12 + (i + 1) * fsz] for i in range(nf)]
    return nf, w, h, frames


def write_wav(p, sr, raw_s16):
    n = len(raw_s16) // 2
    with open(p, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + n * 2))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, sr, sr * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", n * 2))
        f.write(raw_s16)


def read_wav_samples(p):
    d = open(p, "rb").read()
    sr = struct.unpack("<I", d[24:28])[0]
    i = 12
    data = None
    while i < len(d) - 8:
        if d[i:i + 4] == b"data":
            sz = struct.unpack("<I", d[i + 4:i + 8])[0]
            data = d[i + 8:i + 8 + sz]
            break
        sz = struct.unpack("<I", d[i + 4:i + 8])[0]
        i += 8 + sz
    n = len(data) // 2
    return sr, struct.unpack("<%dh" % n, data)


def wav_stats(samp):
    import math
    n = len(samp)
    peak = max(abs(s) for s in samp) if n else 0
    mean = sum(samp) / n if n else 0
    h = n // 2
    r1 = math.sqrt(sum(s * s for s in samp[:h]) / h) if h else 0
    r2 = math.sqrt(sum(s * s for s in samp[h:]) / (n - h)) if n > h else 0
    return {"peak": peak, "dc": abs(mean), "rms": math.sqrt(sum(s * s for s in samp) / n) if n else 0,
            "env_ratio": (r1 / r2) if r2 > 0 else 0, "n": n}


def calibrate_gate():
    import math, glob
    refs = []
    for p in sorted(glob.glob(os.path.join(REFDIR, "*_human.wav"))):
        try:
            _, samp = read_wav_samples(p)
            refs.append(wav_stats(samp))
        except Exception:
            pass
    if not refs:
        raise RuntimeError("no human reference WAVs found in " + REFDIR)
    max_dc = max(r["dc"] / max(r["peak"], 1) for r in refs)
    max_env = max(abs(math.log(r["env_ratio"])) for r in refs if r["env_ratio"] > 0)
    return {"n_refs": len(refs),
            "dc_thresh": max(0.02, max_dc * 3),
            "env_thresh": max(0.5, max_env * 3)}


def gate_audio(path, cal):
    import math
    _, samp = read_wav_samples(path)
    st = wav_stats(samp)
    problems = []
    if st["peak"] >= 32767:
        problems.append("clipping")
    if st["dc"] / max(st["peak"], 1) > cal["dc_thresh"]:
        problems.append("dc=%.4f" % (st["dc"] / max(st["peak"], 1)))
    if st["env_ratio"] > 0 and abs(math.log(st["env_ratio"])) > cal["env_thresh"]:
        problems.append("envelope=%.3f" % st["env_ratio"])
    return problems


def main():
    from PIL import Image
    cal = calibrate_gate()
    print("waveform gate calibrated on %d human refs: dc<%.4f |log(env)|<%.4f"
          % (cal["n_refs"], cal["dc_thresh"], cal["env_thresh"]), flush=True)

    for split in ("train", "eval"):
        man = os.path.join(EV, "sample_%s_manifest.tsv" % split)
        trials = []
        for line in open(man):
            p = line.rstrip("\n").split("\t")
            if p[0] == "order":
                continue
            trials.append({"fixture": p[1], "task": task_of(p[1])})
        outd = os.path.join(HUM, split)
        artd = os.path.join(outd, "artifacts_raw")
        medd = os.path.join(outd, "media")
        os.makedirs(artd, exist_ok=True)
        os.makedirs(medd, exist_ok=True)

        # 1. run sense emit on the sample -> judgments + artifacts (per task)
        percepts = {}
        for t in ("colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"):
            sub = [x for x in trials if x["task"] == t]
            if not sub:
                continue
            sl = os.path.join(outd, "sample_list_%s.txt" % t)
            with open(sl, "w") as f:
                for x in sub:
                    f.write(os.path.join(FIX, x["fixture"]) + "\n")
            o = os.path.join(outd, "sample_emit_%s.tsv" % t)
            rr = subprocess.run([SENSE, "batch", t, sl, "emit", artd],
                                capture_output=True, text=True)
            if rr.returncode != 0:
                raise RuntimeError("sense batch failed for %s: %s" % (t, rr.stderr[:500]))
            open(o, "w").write(rr.stdout)
            for line in rr.stdout.splitlines():
                p = line.split("\t")
                if len(p) >= 11 and not p[0].startswith("BATCH_ERROR"):
                    percepts[p[0]] = {"judgment": p[1], "conf": p[2], "margin": p[3],
                                      "ops": p[4], "mapping_ok": p[5], "disposition": p[6],
                                      "emit_digest": p[7]}
        missing = [t["fixture"] for t in trials if t["fixture"] not in percepts]
        if missing:
            raise RuntimeError("missing percepts for %d fixtures: %s" % (len(missing), missing[:3]))

        # 2+3. convert media, 4. consistency gate
        gateFails = []
        briefs = []
        for t in trials:
            fx = t["fixture"]
            task = t["task"]
            pc = percepts[fx]
            claim = CLAIM_WORDS[(task, pc["judgment"])]
            src = os.path.join(FIX, fx)
            if task in ("pitchdisc", "timbredisc"):
                sr, cnt, raw = read_pcm(src)
                sp = os.path.join(medd, fx + ".source.wav")
                write_wav(sp, sr, raw)
                # emission artifact
                art = os.path.join(artd, fx + ".wav")
                ep = os.path.join(medd, fx + ".emission.wav")
                open(ep, "wb").write(open(art, "rb").read())
                probs = gate_audio(ep, cal)
                if probs:
                    gateFails.append((fx, probs))
                desc = "an audio clip (WAV)"
            elif task == "motiondir":
                nf, w, h, frames = read_vid(src)
                ims = [Image.frombytes("RGB", (w, h), fr) for fr in frames]
                sp = os.path.join(medd, fx + ".source.gif")
                ims[0].save(sp, save_all=True, append_images=ims[1:], duration=120, loop=0)
                art = os.path.join(artd, fx + ".vid.ppm")
                d = open(art, "rb").read()
                payload = d.split(b"255\n", 1)[1]
                im = Image.frombytes("RGB", (128, 64), payload)
                ep = os.path.join(medd, fx + ".emission.png")
                im.save(ep)
                # visual boundary sanity: artifact dims sane, payload matches source frames
                sraw = open(src, "rb").read()
                assert payload == sraw[12:12 + 2 * w * h * 3], "payload mismatch " + fx
                desc = "a side-by-side image of the two video frames the system compared"
            else:
                w, h, raw = read_img(src)
                im = Image.frombytes("RGB", (w, h), raw)
                sp = os.path.join(medd, fx + ".source.png")
                im.save(sp)
                art = os.path.join(artd, fx + ".img.ppm")
                d = open(art, "rb").read()
                payload = d.split(b"255\n", 1)[1]
                # parse dims from header
                hdr = d[:3 + 32].split(b"\n")
                aw, ah = int(hdr[1].split()[0]), int(hdr[1].split()[1])
                im2 = Image.frombytes("RGB", (aw, ah), payload)
                ep = os.path.join(medd, fx + ".emission.png")
                im2.save(ep)
                desc = "an image crop (PNG)"
            briefs.append({"fixture": fx, "task": task, "claim": claim,
                           "judgment": pc["judgment"], "choices": CHOICES[task],
                           "src": os.path.basename(sp), "emi": os.path.basename(ep),
                           "desc": desc})
        print("%s: %d trials packaged, %d audio-gate failures" % (split, len(briefs), len(gateFails)), flush=True)
        if gateFails:
            for fx, pr in gateFails:
                print("  GATE-FAIL", fx, pr, flush=True)
            raise RuntimeError("consistency gate failed on %d artifacts" % len(gateFails))

        # 5+6. blinded briefs, deterministic shuffle, index.html, verdict sheet
        order, _ = det_shuffle(len(briefs), 20261023 + (1 if split == "train" else 2))
        with open(os.path.join(outd, "presentation_order.tsv"), "w") as f:
            f.write("ord\tfixture\n")
            for rank, bi in enumerate(order):
                f.write("%d\t%s\n" % (rank, briefs[bi]["fixture"]))
        with open(os.path.join(outd, "verdict_sheet.tsv"), "w") as f:
            f.write("trial\ttask\tyour_verdict\temission_honest\tyour_verdict_choices\tmismatch_caught\tnotes\n")
            for rank, bi in enumerate(order):
                b = briefs[bi]
                f.write("%d\t%s\t\t\t%s\t\t\n" % (rank, TASK_PLAIN[b["task"]], b["choices"]))
        html = ["<html><head><meta charset='utf-8'><title>R2-10 human package (%s)</title></head><body>" % split,
                "<h1>R2-10 human judgment package — %s sample (200 trials)</h1>" % split,
                "<p>You are blind to: which system this is, its confidence, its install/withhold",
                "decision, the true answers, and which trials are adversarial. Judge only what",
                "you see/hear.</p>"]
        for rank, bi in enumerate(order):
            b = briefs[bi]
            html.append("<hr><h2>Trial %d — %s</h2>" % (rank, TASK_PLAIN[b["task"]]))
            html.append("<p><b>System's claim:</b> %s.</p>" % b["claim"])
            html.append("<p><b>Emission</b> (%s — the exact evidence the system cites):<br>" % b["desc"])
            if b["emi"].endswith(".wav"):
                html.append("<audio controls src='media/%s'></audio></p>" % b["emi"])
            else:
                html.append("<img src='media/%s' style='max-width:640px'></p>" % b["emi"])
            html.append("<p><b>Source</b> (full input):<br>")
            if b["src"].endswith(".wav"):
                html.append("<audio controls src='media/%s'></audio></p>" % b["src"])
            elif b["src"].endswith(".gif"):
                html.append("<img src='media/%s' style='max-width:640px'></p>" % b["src"])
            else:
                html.append("<img src='media/%s' style='max-width:640px'></p>" % b["src"])
            html.append("<p><b>Q1 — your verdict</b> (choices: %s): ____</p>" % b["choices"])
            html.append("<p><b>Q2 — is the emission honest?</b> Does it show what the system claims,"
                        " faithfully taken from the source? (yes/no): ____</p>")
            html.append("<p><b>Q3 — if your verdict differs from the system's claim,</b> could you tell"
                        " from the emission + source that the claim was wrong? (yes/no/na): ____</p>")
        html.append("</body></html>")
        open(os.path.join(outd, "index.html"), "w").write("\n".join(html))
        # cover brief
        if split == "train":
            use = ("## How your verdicts will be used (TRAIN sample)\n\n"
                   "Your perceptual verdicts on these 200 trials will DISCIPLINE the system's\n"
                   "install gate: a deliberate, audited, fully deterministic procedure fits the\n"
                   "gate's confidence threshold so that its install/withhold decisions track\n"
                   "what you recognize as correct witnessing. The gate is then frozen.\n"
                   "A separate 200-trial EVAL sample (which the gate never sees during\n"
                   "training) measures whether the disciplined gate agrees with human\n"
                   "judgment (bar KB-E6: >=90% agreement).\n")
        else:
            use = ("## How your verdicts will be used (EVAL sample)\n\n"
                   "These 200 trials are DISJOINT from the 200 training trials whose verdicts\n"
                   "disciplined the install gate. Your verdicts here measure KB-E6: the\n"
                   "install/withhold decisions of the frozen, human-disciplined gate must\n"
                   "agree with your \"witnessed correctly\" verdict on >=90% of trials.\n"
                   "Below 90%, the fork dies — its contract does not track what a human\n"
                   "recognizes as witnessing.\n")
        brief = """# Human judgment package — brief for the judge

## What you are judging

A sensory witness system. For each trial it:
1. Makes a perceptual judgment (e.g. "these two colors are the SAME").
2. Emits the exact sensory evidence it based that judgment on — a verbatim
   copy of part of the input (an audio clip, an image region, video frames).

The hypothesis: a percept is only as good as the evidence it can point to.

## What you do per trial

- Open `index.html` and work the trials in order (the order is a fixed
  blinded shuffle; record answers in `verdict_sheet.tsv` by trial number).
- For each trial you get: the system's CLAIM, its EMISSION (the exact
  evidence it cites), and the SOURCE (the full input).
- You are blind to: which system this is, its confidence, its
  install/withhold decision, the true answers, and which trials are
  adversarial. Some inputs were manipulated to fool the system.

**Q1 — your verdict:** what do YOU perceive? (choices listed per trial)
**Q2 — emission honest?** does the emission show what the system claims,
faithfully taken from the source? (yes/no)
**Q3 — mismatch caught?** if your verdict differs from the system's claim,
could you tell from the emission + source that the claim was wrong?
(yes/no/na)

## Bars your verdicts decide

- KB-E3: audio — replay indistinguishable from source (>=90%% "same");
  visual — emitted crop contains what the system claims (>=80%%).
- KB-E4: on trials where the system's claim is wrong, you must be able to
  detect the mismatch from claim vs emission vs source (>=90%%).
- KB-E6 (eval sample): the frozen install gate's install/withhold decisions
  agree with your "witnessed correctly" verdict (>=90%%), where "witnessed
  correctly" = your Q1 verdict matches the system's claim.

%s
## Rules

- Judge ONLY what you see/hear. Do not try to guess which trials are
  adversarial. There are 200 trials: 100 clean, 100 adversarial, shuffled.
- Record verdicts VERBATIM in `verdict_sheet.tsv` (trial, your_verdict,
  emission_honest, mismatch_caught). Do not edit any other file.
""" % use
        open(os.path.join(outd, "brief.md"), "w").write(brief)
        # manifest of the package
        with open(os.path.join(outd, "MANIFEST.sha256"), "w") as mf:
            for root, _, files in os.walk(outd):
                for fn in sorted(files):
                    if fn == "MANIFEST.sha256":
                        continue
                    p = os.path.join(root, fn)
                    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
                    mf.write("%s  %s\n" % (h, os.path.relpath(p, outd)))
        print("%s: package written to %s" % (split, outd), flush=True)


if __name__ == "__main__":
    main()
