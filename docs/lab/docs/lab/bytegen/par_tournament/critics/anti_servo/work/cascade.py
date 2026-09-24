#!/usr/bin/env python3
"""Count differing samples between two WAVs after a cut time (RT-CASCADE).
Also: first-diff time for RT-EDGE, RMS/peak in a window."""
import sys, wave
import numpy as np

def load(path):
    w = wave.open(path)
    n = w.getnframes(); sr = w.getframerate()
    s = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
    return s, sr

def load_raw(path):
    """Raw s32 LE mix dump (render_c 'mix'/'seqmix' modes): no header."""
    s = np.fromfile(path, dtype=np.int32).astype(np.float64) / 2147483648.0
    return s, 44100

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "postdiff":
        # postdiff <clean> <faulty> <cut_s>
        a, sra = load(sys.argv[2]); b, srb = load(sys.argv[3])
        cut = int(float(sys.argv[4]) * sra)
        n = min(len(a), len(b))
        d = int(np.sum(a[cut:n] != b[cut:n]))
        pre = int(np.sum(a[:cut] != b[:cut]))
        print(f"post-cut diffs (t>{sys.argv[4]}s): {d}   pre-cut diffs: {pre}")
    elif cmd == "firstdiff":
        # firstdiff <full> <trunc>
        a, sra = load(sys.argv[2]); b, srb = load(sys.argv[3])
        n = min(len(a), len(b))
        idx = np.where(a[:n] != b[:n])[0]
        if len(idx):
            print(f"first diff at sample {idx[0]} = {idx[0]/sra:.3f} s; diffs before 14.9s: {int(np.sum(idx < int(14.9*sra)))}")
        else:
            print("no diffs (identical)")
    elif cmd == "winstat":
        # winstat <wav> <t0> <t1>
        s, sr = load(sys.argv[2])
        seg = s[int(float(sys.argv[3])*sr):int(float(sys.argv[4])*sr)]
        print(f"RMS={np.sqrt(np.mean(seg**2)):.3f} FS  peak={np.max(np.abs(seg)):.3f} FS")
