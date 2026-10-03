#!/usr/bin/env python3
"""Assemble the R2-9 human-verdict package (prereg §9, Debate C protocol).
Frozen 200-trial sample (100 clean / 100 adversarial, double-blind order from
freeze_sample.py) -> source+emission viewable pairs + claim cards + brief.
Truth/kind/family NEVER enter the judged package (kept in the crew manifest).
Pure glue — no TNN decisions.
Usage: assemble_human_package.py <sample_manifest.tsv> <sense_binary> <outdir>
cwd must be ~/workspace/tnn-lab (fixture paths are lab-relative).
"""
import os, struct, subprocess, sys, wave, hashlib
from PIL import Image

LAB = os.getcwd()

def read_img(p):
    d = open(p, "rb").read()
    w, h = struct.unpack("<II", d[:8])
    return w, h, d[8:8 + w * h * 3]

def read_pcm(p):
    d = open(p, "rb").read()
    rate, cnt = struct.unpack("<II", d[:8])
    samp = struct.unpack("<%dh" % cnt, d[8:8 + cnt * 2])
    return rate, samp

def read_vid(p):
    d = open(p, "rb").read()
    nf, w, h = struct.unpack("<III", d[:12])
    frames = []
    o = 12
    for _ in range(nf):
        frames.append(d[o:o + w * h * 3])
        o += w * h * 3
    return nf, w, h, frames

def write_wav(path, rate, samp):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(struct.pack("<%dh" % len(samp), *samp))

def write_png(path, w, h, rgb):
    Image.frombytes("RGB", (w, h), rgb).save(path)

def write_gif(path, w, h, frames):
    ims = [Image.frombytes("RGB", (w, h), f) for f in frames]
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=100, loop=0)

def convert_source(src_rel, out_base):
    """Convert a fixture to viewable form. Returns the output filename."""
    p = os.path.join(LAB, src_rel)
    if src_rel.endswith(".img"):
        w, h, rgb = read_img(p)
        fn = out_base + ".source.png"
        write_png(fn, w, h, rgb)
    elif src_rel.endswith((".pcm",)):
        rate, samp = read_pcm(p)
        fn = out_base + ".source.wav"
        write_wav(fn, rate, samp)
    elif src_rel.endswith(".vid"):
        nf, w, h, frames = read_vid(p)
        fn = out_base + ".source.gif"
        write_gif(fn, w, h, frames)
    else:
        raise ValueError("unknown fixture ext: " + src_rel)
    return fn

def convert_artifact(ap, out_base, k):
    """Convert a sense emission artifact to viewable form."""
    d = open(ap, "rb").read()
    if ap.endswith(".aud"):
        rate, cnt = struct.unpack("<II", d[:8])
        samp = struct.unpack("<%dh" % cnt, d[8:8 + cnt * 2])
        fn = "%s.e%d.wav" % (out_base, k)
        write_wav(fn, rate, samp)
    elif ap.endswith(".img"):
        w, h = struct.unpack("<II", d[:8])
        fn = "%s.e%d.png" % (out_base, k)
        write_png(fn, w, h, d[8:8 + w * h * 3])
    elif ap.endswith(".vid"):
        nf, w, h = struct.unpack("<III", d[:12])
        frames = []
        o = 12
        for _ in range(nf):
            frames.append(d[o:o + w * h * 3])
            o += w * h * 3
        fn = "%s.e%d.gif" % (out_base, k)
        write_gif(fn, w, h, frames)
    else:
        raise ValueError("unknown artifact ext: " + ap)
    return fn

def main():
    manifest, sense_bin, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    trials_dir = os.path.join(outdir, "trials")
    os.makedirs(trials_dir, exist_ok=True)

    sample = []
    with open(manifest) as f:
        header = f.readline()
        for line in f:
            q = line.rstrip("\n").split("\t")
            # sample_idx, trial_id, task, fixture, truth, kind, family
            sample.append({"idx": int(q[0]), "tid": q[1], "task": q[2],
                           "fixture": q[3], "truth": q[4], "kind": q[5],
                           "family": q[6]})

    # batch-run the fork on the sample (200 trials) with emission on
    tsv = os.path.join(outdir, "_sample_trials.tsv")
    with open(tsv, "w") as f:
        for s in sample:
            f.write("%s\t%s\tsample\t%s\t%s\t%s\n" % (
                s["tid"], s["task"], s["family"], s["fixture"], s["truth"]))
    rundir = os.path.join(outdir, "_run")
    r = subprocess.run([sense_bin, "batch", tsv, rundir, "emit"],
                       capture_output=True, text=True, timeout=1200)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(no stdout)")
    if r.returncode != 0:
        print("SENSE FAILED", r.stderr[-2000:], file=sys.stderr)
        sys.exit(1)

    percepts = {}
    with open(os.path.join(rundir, "percepts.tsv")) as f:
        f.readline()
        for line in f:
            q = line.rstrip("\n").split("\t")
            percepts[q[0]] = q
    adir = os.path.join(rundir, "artifacts")

    index_lines = ["idx\ttrial_dir\ttask\tsource\temissions\tjudgment\tconf"]
    for s in sample:
        i = s["idx"]
        base = os.path.join(trials_dir, "trial_%03d" % i)
        src_view = convert_source(s["fixture"], base)
        row = percepts[s["tid"]]
        # trial, task, fixture, judgment, conf, disp, ops, nsel, sel, claim, warrant, ledger
        nsel = int(row[7])
        em_files = []
        for k in range(nsel):
            for ext in (".aud", ".img", ".vid"):
                ap = os.path.join(adir, "%s.e%d%s" % (s["tid"], k, ext))
                if os.path.exists(ap):
                    em_files.append(convert_artifact(ap, base, k))
                    break
        # claim card — NO truth, NO kind/family (double-blind)
        with open(base + ".claim.txt", "w") as f:
            f.write("trial: %03d\n" % i)
            f.write("task: %s\n" % s["task"])
            f.write("system judgment: %s\n" % row[3])
            f.write("confidence: %s\n" % row[4])
            f.write("claim: %s\n" % row[9])
            f.write("warrant: %s\n" % row[10])
            f.write("source file: %s\n" % os.path.basename(src_view))
            f.write("emission files: %s\n" % ", ".join(os.path.basename(x) for x in em_files))
        index_lines.append("%d\ttrial_%03d\t%s\t%s\t%s\t%s\t%s" % (
            i, i, s["task"], os.path.basename(src_view),
            ",".join(os.path.basename(x) for x in em_files), row[3], row[4]))

    with open(os.path.join(outdir, "trial_index.tsv"), "w") as f:
        f.write("\n".join(index_lines) + "\n")

    # brief
    import shutil
    shutil.copy(os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-9/evidence/human_brief.md"),
                os.path.join(outdir, "BRIEF.md"))

    # waveform gate on the raw emission audio artifacts (.aud) that the
    # package WAVs were converted from (lossless 16-bit PCM conversion)
    gate = subprocess.run(
        [sys.executable,
         os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-9/work/waveform_gate.py"),
         adir],
        capture_output=True, text=True, timeout=600)
    gate_report = "waveform gate (scripts: work/waveform_gate.py)\n"
    gate_report += "calibration: 6 human-produced reference WAVs (NOT field recordings)\n"
    gate_report += "checks: peak headroom, DC offset, envelope stationarity\n"
    gate_report += ("NOTE: prereg §5.3 also names spectral drift, loop-periodicity, "
                    "transient regularity, THD — not implemented in this gate version.\n")
    gate_report += "exit=%d\n%s\n%s\n" % (gate.returncode, gate.stdout, gate.stderr)
    with open(os.path.join(outdir, "gate_report.txt"), "w") as f:
        f.write(gate_report)
    print(gate.stdout.strip().splitlines()[-1] if gate.stdout.strip() else "(gate no stdout)")

    # package manifest (blinded: no truth)
    files = []
    for dp, dn, fn in os.walk(outdir):
        for x in fn:
            if x.startswith("_"):
                continue
            files.append(os.path.relpath(os.path.join(dp, x), outdir))
    files.sort()
    with open(os.path.join(outdir, "PACKAGE.sha256"), "w") as f:
        for rel in files:
            h = hashlib.sha256(open(os.path.join(outdir, rel), "rb").read()).hexdigest()
            f.write("%s  %s\n" % (h, rel))
    print("packaged %d trials -> %s" % (len(sample), outdir))

if __name__ == "__main__":
    main()
