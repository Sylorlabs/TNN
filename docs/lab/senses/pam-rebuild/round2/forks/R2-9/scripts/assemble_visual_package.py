#!/usr/bin/env python3
"""Assemble the R2-9 human judge package (VISUAL ONLY).
Audio trials are gate-blocked (full waveform gate with real field-recording
calibration not implemented); they are listed but their audio is withheld.
Creates: evidence/human_package/
  - trials/  (151 visual trials, double-blind randomized order)
    - <judge_id>/source.png, emission.png (or source.gif/emission.gif for video)
    - <judge_id>/claim.txt (the fork's claim, no truth)
  - manifest.tsv (judge_id -> sample_idx, sealed)
  - brief.md (judge instructions + audio gate-blocked notice)
  - audio_gate_blocked.tsv (49 audio trials, listed not packaged)
Pure glue.
"""
import os, sys, shutil, hashlib, struct
from PIL import Image

LAB = os.path.expanduser("~/workspace/tnn-lab")
FORK = os.path.join(LAB, "senses", "pam-rebuild", "round2", "forks", "R2-9")
EVID = os.path.join(FORK, "evidence")
PKG = os.path.join(EVID, "human_package")
SAMPLE_OUT = os.path.join(FORK, "work", "sample_out")

# visual tasks
VISUAL = {"colordisc", "colorconst", "shapetrans", "motiondir"}
AUDIO = {"pitchdisc", "timbredisc"}

def read_rows(path, header=True):
    with open(path) as f:
        if header: f.readline()
        return [l.rstrip("\n").split("\t") for l in f]

def img_to_png(src, dst):
    """Convert .img (u32 w,h header + RGB) to PNG."""
    with open(src, "rb") as f:
        d = f.read()
    w, h = struct.unpack("<II", d[:8])
    px = d[8:8+w*h*3]
    assert len(px) == w*h*3, (src, w, h, len(px))
    im = Image.frombytes("RGB", (w, h), px)
    im.save(dst)

def main():
    # read sample manifest
    samples = read_rows(os.path.join(EVID, "human_sample_manifest.tsv"))
    # samples: sample_idx, trial_id, task, fixture, truth, kind, family

    # read percepts from sample run
    percepts = {}
    for row in read_rows(os.path.join(SAMPLE_OUT, "percepts.tsv")):
        # trial_id, percept, ...
        percepts[row[0]] = row

    # deterministic shuffle for double-blind order (seeded by manifest sha)
    with open(os.path.join(EVID, "human_sample.sha256")) as f:
        seed_hex = f.read().strip().split()[0]
    seed = int(seed_hex[:16], 16)
    # simple LCG for deterministic shuffle (glue only, not in TNN path)
    def lcg_shuffle(lst, seed):
        a, c, m = 6364136223846793005, 1442695040888963407, 2**64
        x = seed
        lst = lst[:]
        for i in range(len(lst)-1, 0, -1):
            x = (a*x + c) % m
            j = x % (i+1)
            lst[i], lst[j] = lst[j], lst[i]
        return lst

    visual = [s for s in samples if s[2] in VISUAL]
    audio = [s for s in samples if s[2] in AUDIO]
    print("visual: %d, audio (gate-blocked): %d" % (len(visual), len(audio)))

    visual_shuffled = lcg_shuffle(visual, seed)

    # clear and create package
    if os.path.exists(PKG):
        shutil.rmtree(PKG)
    os.makedirs(os.path.join(PKG, "trials"))

    # manifest (sealed: judge does not see this)
    with open(os.path.join(PKG, "manifest.tsv"), "w") as mf:
        mf.write("judge_id\tsample_idx\ttrial_id\ttask\tkind\tfamily\n")
        for ji, s in enumerate(visual_shuffled):
            idx, tid, task, fixture, truth, kind, family = s
            mf.write("J%03d\t%s\t%s\t%s\t%s\t%s\n" % (ji, idx, tid, task, kind, family))

    # audio gate-blocked list
    with open(os.path.join(PKG, "audio_gate_blocked.tsv"), "w") as af:
        af.write("sample_idx\ttrial_id\ttask\tkind\tfamily\treason\n")
        for s in audio:
            idx, tid, task, fixture, truth, kind, family = s
            af.write("%s\t%s\t%s\t%s\t%s\tfull waveform gate (envelope stationarity, spectral drift, loop periodicity, transient regularity, THD) with real field-recording calibration not implemented\n" % (idx, tid, task, kind, family))

    # copy visual trials
    # Need to find source fixture and emission artifact for each
    # Source: LAB/<fixture>, Emission: SAMPLE_OUT/artifacts/<trial_id>.*
    art_dir = os.path.join(SAMPLE_OUT, "artifacts")
    for ji, s in enumerate(visual_shuffled):
        idx, tid, task, fixture, truth, kind, family = s
        jdir = os.path.join(PKG, "trials", "J%03d" % ji)
        os.makedirs(jdir)
        # source
        src = os.path.join(LAB, fixture)
        # emission: find artifact for this trial_id
        em = None
        for fn in os.listdir(art_dir):
            if fn.startswith(tid + "."):
                em = os.path.join(art_dir, fn)
                break
        if not os.path.exists(src):
            print("WARN: source missing %s" % src)
            continue
        # convert source .img to PNG (or copy .vid as-is with note)
        if task == "motiondir":
            # video: keep .vid, judge can inspect frames via provided converter
            shutil.copy(src, os.path.join(jdir, "source.vid"))
            # also render first frame as PNG for quick viewing
            with open(src, "rb") as f:
                d = f.read()
            # .vid format: check header
            w, h = struct.unpack("<II", d[:8])
            # frames follow; extract first frame (w*h*3 bytes after header)
            px = d[8:8+w*h*3]
            if len(px) == w*h*3:
                Image.frombytes("RGB", (w, h), px).save(os.path.join(jdir, "source_frame0.png"))
        else:
            img_to_png(src, os.path.join(jdir, "source.png"))
        if em and os.path.exists(em):
            eext = os.path.splitext(em)[1]
            if eext == ".img":
                img_to_png(em, os.path.join(jdir, "emission.png"))
            else:
                shutil.copy(em, os.path.join(jdir, "emission" + eext))
        # claim card (from percepts, NO truth, NO trial_id, NO fixture path)
        if tid in percepts:
            cols = percepts[tid]
            # percepts columns: trial_id, task, fixture, percept, ops, disp, ...
            # Redact cols 0 (trial_id) and 2 (fixture path) for double-blind.
            redacted = ["[redacted]", cols[1], "[redacted]"] + cols[3:]
            with open(os.path.join(jdir, "claim.txt"), "w") as cf:
                cf.write("Trial %s\n" % ("J%03d" % ji))
                cf.write("Task: %s\n" % task)
                cf.write("Fork's percept/claim:\n")
                cf.write("\t".join(redacted) + "\n")
                cf.write("\nWhat do YOU perceive? Record your judgment.\n")
                cf.write("(Truth is sealed and not shown to the judge.)\n")
        else:
            print("WARN: no percept for %s" % tid)

    # brief
    with open(os.path.join(PKG, "brief.md"), "w") as bf:
        bf.write("""# R2-9 Human Judge Brief (KB-E3/E4)

You are judging whether R2-9's sensory emissions are faithful and beautiful.
This package contains 151 VISUAL trials in randomized double-blind order.

## What to do
For each trial J###:
1. Look at `source` (the original stimulus) and `emission` (R2-9's output).
2. Read `claim.txt` (what R2-9 claims it perceived).
3. Judge:
   - KB-E3 (fidelity): Does the emission faithfully represent the source?
   - KB-E4 (beauty): Is the emission beautiful / does it show imagination?
4. Record your verdict per trial.

## Audio trials: GATE-BLOCKED
49 audio trials (pitchdisc, timbredisc) are NOT included in this package.
Reason: The frozen protocol requires audio to pass a full waveform gate
(envelope stationarity, spectral drift, loop periodicity, transient regularity,
THD) calibrated against real field recordings. That gate is not implemented;
only a partial gate (peak/clipping, DC, envelope stationarity) exists,
calibrated against human-produced references, not field recordings.
Per the protocol: do not fake it. Audio is withheld until a compliant gate passes.
The 49 blocked trials are listed in `audio_gate_blocked.tsv`.

## Blinding
- Trial order is randomized. `manifest.tsv` (sealed) maps judge IDs back to
  sample indices; do not open it until judging is complete.
- `claim.txt` contains the fork's claim but NOT the ground truth.
- Clean/adversarial status and attack family are not revealed.
""")
    print("package assembled at %s" % PKG)
    print("trials: %d" % len(os.listdir(os.path.join(PKG, "trials"))))

if __name__ == "__main__":
    main()
