#!/usr/bin/env python3
"""FS-E4 feasibility measurement (analysis only, NOT results).

Parses frozen R2FX fixtures (R2-7/fixtures_R2A, manifest-covered) for the
three candidate tasks, wraps F/G spans into the payload layouts consumed by
the frozen naive front-ends (R2-3/src/mirror/judge.py, the Python twin of
R2-15's r2p_front.zag), and reports per-task availability for each FS-E4
family shape. Informs the frozen prereg's battery selection rule.
Zero RNG; deterministic.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.expanduser(
    "~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-3/src/mirror"))
import judge as J

FIX = os.path.expanduser(
    "~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-7/fixtures_R2A")
TASKS = ["colordisc", "shapetrans", "pitchdisc"]
TRUTH2CODE = {
    "colordisc": {"SAME": 0, "DIFFERENT": 1},
    "shapetrans": {"CIRCLE": 0, "TRIANGLE": 1, "SQUARE": 2},
    "pitchdisc": {"SAME": 0, "HIGHER": 1, "LOWER": 2},
}

def parse_r2fx(path):
    with open(path, "rb") as f:
        data = f.read()
    magic, task, index, family, fo, fl, go, gl = struct.unpack("<8I", data[:32])
    assert magic == 0x52324658, path
    fspan = data[fo:fo + fl]
    gspan = data[go:go + gl]
    assert len(fspan) == fl and len(gspan) == gl, path
    with open(path + ".truth") as f:
        truth = f.read().split("=")[1].strip().split()[0]
    return task, index, family, fspan, gspan, truth

def wrap(task, span, which):
    """Wrap a raw R2FX span into the payload layout the naive front-end reads."""
    if task == "colordisc":
        # F = 6144B (2x32x32 RGB); G first 6144B = neutral re-render pair
        rgb = span[:6144]
        assert len(rgb) == 6144
        return struct.pack("<IHH", 1, 64, 32) + rgb
    if task == "shapetrans":
        # u8 grayscale -> RGB image
        w = 96 if which == "F" else 48
        assert len(span) == w * w, (task, which, len(span))
        rgb = bytearray()
        for v in span:
            rgb += bytes((v, v, v))
        return struct.pack("<HH", w, w) + bytes(rgb)
    if task == "pitchdisc":
        # 32000 i16 @16kHz, two-tone layout
        assert len(span) == 64000, (task, which, len(span))
        return struct.pack("<II", 16000, 32000) + span
    raise ValueError(task)

def judge_of(task, payload):
    if task == "colordisc":
        return J.nf_colordisc(payload)
    if task == "shapetrans":
        return J.nf_shapetrans(payload)
    if task == "pitchdisc":
        return J.nf_pitchdisc(payload)
    raise ValueError(task)

def main():
    for task in TASKS:
        print("=" * 70)
        print("TASK", task)
        for split in ("r2n", "r2a", "r2a2"):
            d = os.path.join(FIX, split)
            files = sorted(f for f in os.listdir(d)
                           if f.startswith(("r2n_%s_" % task, "r2a_%s_" % task,
                                            "r2a2_%s_" % task))
                           and f.endswith(".r2fx"))
            n = len(files)
            f_ok = g_ok = both_ok = 0
            f_fooled = f_fooled_g_ok = f_fooled_g_fooled_same = 0
            fam_fooled = {}
            for fn in files:
                t, idx, fam, fs, gs, truth = parse_r2fx(os.path.join(d, fn))
                tc = TRUTH2CODE[task][truth]
                fj = judge_of(task, wrap(task, fs, "F"))
                gj = judge_of(task, wrap(task, gs, "G"))
                if fj == tc:
                    f_ok += 1
                else:
                    f_fooled += 1
                    fam_fooled.setdefault(fam, {}).setdefault(fj, 0)
                    fam_fooled[fam][fj] += 1
                    if gj == tc:
                        f_fooled_g_ok += 1
                    elif gj == fj:
                        f_fooled_g_fooled_same += 1
                if gj == tc:
                    g_ok += 1
                if fj == tc and gj == tc:
                    both_ok += 1
            print(f"  split={split} n={n} F_ok={f_ok} ({100.0*f_ok/max(n,1):.1f}%) "
                  f"G_ok={g_ok} ({100.0*g_ok/max(n,1):.1f}%) both_ok={both_ok} "
                  f"({100.0*both_ok/max(n,1):.1f}%)")
            if f_fooled:
                print(f"    F_fooled={f_fooled} of which G_ok={f_fooled_g_ok} "
                      f"G_fooled_same_lie={f_fooled_g_fooled_same}")
                for fam in sorted(fam_fooled):
                    print(f"    fam{fam} fool-targets: {fam_fooled[fam]}")

if __name__ == "__main__":
    main()
