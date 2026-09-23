#!/usr/bin/env python3
"""sol-H3 machine test: spatially frozen long-scene world beds.
Per PREREG_ROUND2.md: 12 scene pairs (4 familiar/4 dense/4 novel) x standard/
control bed; 4 primary measures (1 s novelty, 10 s novelty, repeated-segment
similarity, event-conditioned bed response); paired Wilcoxon signed-rank,
Holm-corrected; plus boundary floors vs kids median 0.0418."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_common import read_wav, rms_10ms, bandpass
from scipy.stats import wilcoxon

R = "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/renders/h3"
SR = 44100
KIDS_MEDIAN = 0.0418
BED_CLASSES = {5, 10}  # wash, wind

# grain index -> class id (from dumpgrains)
GRAINCLS = {}
def load_graincls():
    import subprocess
    out = subprocess.run(
        ["/home/hatch/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/r2g/r2g_bin",
         "dumpgrains",
         "/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_gamma/study_out/gamma.grpk"],
        capture_output=True, text=True, cwd="/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_gamma")
    for line in out.stdout.splitlines():
        p = line.split()
        if len(p) == 3:
            GRAINCLS[int(p[0])] = int(p[1])

def spec_frames(x, hop_s, win_s=0.046):
    win = int(win_s * SR); hop = int(hop_s * SR)
    w = np.hanning(win)
    nfr = 1 + (len(x) - win) // hop
    S = np.empty((nfr, win // 2 + 1), dtype=np.float32)
    for i in range(nfr):
        seg = x[i * hop:i * hop + win] * w
        S[i] = np.log10(np.abs(np.fft.rfft(seg)) + 1e-9)
    return S

def spectral_novelty(x, hop_s):
    S = spec_frames(x, hop_s)
    d = np.diff(S, axis=0)
    return float(np.sqrt((d ** 2).sum(axis=1)).mean())

def repeated_segment_sim(x):
    S = spec_frames(x, 5.0, win_s=10.0)  # 10 s windows, 5 s hop
    n = len(S)
    norms = np.sqrt((S ** 2).sum(axis=1)) + 1e-12
    best = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            c = float((S[i] * S[j]).sum() / (norms[i] * norms[j]))
            if c > best:
                best = c
    return best

def load_log(path):
    ev = []
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) < 3:
                continue
            ev.append((int(p[0]), int(p[2])))  # (start_ns, grain idx)
    return ev

def bed_response(x, events):
    """Pearson r between per-1 s bed-band (200-800 Hz) energy and per-1 s
    foreground event count. Foreground = placements whose class is not
    wash/wind (bed)."""
    bed = bandpass(x, 200, 800)
    n1 = SR
    m = len(bed) // n1
    energy = (bed[:m * n1].reshape(m, n1) ** 2).mean(axis=1)
    counts = np.zeros(m)
    for start, gi in events:
        c = GRAINCLS.get(gi, -1)
        if c not in BED_CLASSES:
            s = start // n1
            if 0 <= s < m:
                counts[s] += 1
    if energy.std() == 0 or counts.std() == 0:
        return 0.0
    return float(np.corrcoef(energy, counts)[0, 1])

def bridge_spans(cls):
    secs = [0, 60, 120, 180, 240]
    if cls == 0:
        return [(s + 0.0, s + 1.6) for s in secs]
    if cls == 1:
        return [(s + 0.0, s + 1.6) for s in secs]
    return [(s + 30.0, s + 31.6) for s in secs]

def check_foreground_identity(ev_std, ev_ctl, spans):
    """Non-bed placements outside bridge spans (the kids/dream foreground
    streams) must be identical across conditions. Bed classes (wash/wind)
    legitimately differ everywhere; bridge-interior thump/laugh differ
    inside bridge spans."""
    def key(ev):
        out = []
        for start, gi in ev:
            if GRAINCLS.get(gi, -1) in BED_CLASSES:
                continue
            t = start / SR
            if any(a - 0.5 <= t <= b + 0.5 for a, b in spans):
                continue
            out.append((start, gi))
        return sorted(out)
    return key(ev_std) == key(ev_ctl)

def check_bed_nonadjacency(ev_std, ev_ctl):
    """Report bed-class source-grain overlap between conditions. NOTE: the
    ocean corpus holds only 19 wash + 21 wind grains, so the salt+700000
    control necessarily reuses the same source grains in a different
    order/timing — the prereg's nonadjacency assumption is unachievable.
    Returns (overlap_fraction, counts)."""
    def bedgis(ev):
        d = {}
        for _, gi in ev:
            c = GRAINCLS.get(gi, -1)
            if c in BED_CLASSES:
                d.setdefault(c, set()).add(gi)
        return d
    s, c = bedgis(ev_std), bedgis(ev_ctl)
    tot_o = tot_u = 0
    info = {}
    for cls in BED_CLASSES:
        o = len(s.get(cls, set()) & c.get(cls, set()))
        u = len(s.get(cls, set()) | c.get(cls, set()))
        tot_o += o; tot_u += u
        info[cls] = (len(s.get(cls, set())), len(c.get(cls, set())), o)
    return (tot_o / tot_u if tot_u else 1.0), info

def analyze_scene(cls, idx):
    ws = f"{R}/h3_c{cls}_i{idx}_d0.wav"; ls = f"{R}/h3_c{cls}_i{idx}_d0.log"
    wc = f"{R}/h3_c{cls}_i{idx}_d1.wav"; lc = f"{R}/h3_c{cls}_i{idx}_d1.log"
    if not all(os.path.exists(p) for p in (ws, ls, wc, lc)):
        return None
    xs, xc = read_wav(ws), read_wav(wc)
    evs, evc = load_log(ls), load_log(lc)
    spans = bridge_spans(cls)
    ident = check_foreground_identity(evs, evc, spans)
    overlap, bedn = check_bed_nonadjacency(evs, evc)
    res = {}
    for tag, x in (('std', xs), ('ctl', xc)):
        r = {
            'nov1': spectral_novelty(x, 1.0),
            'nov10': spectral_novelty(x, 10.0),
            'repsim': repeated_segment_sim(x),
            'bedresp': bed_response(x, evs if tag == 'std' else evc),
        }
        # boundary floors: min 10 ms RMS in +-250 ms around each bridge midpoint
        r10 = rms_10ms(x)
        floors = []
        for a, b in spans:
            mid = (a + b) / 2
            i0 = int((mid - 0.25) * 100); i1 = int((mid + 0.25) * 100)
            floors.append(float(r10[max(0, i0):i1].min()))
        r['floors'] = floors
        res[tag] = r
    return res, ident, overlap, bedn

def holm(ps, alpha=0.05):
    order = np.argsort(ps)
    sig = [False] * len(ps)
    for rank, i in enumerate(order):
        if ps[i] <= alpha / (len(ps) - rank):
            sig[i] = True
        else:
            break
    return sig

def main():
    load_graincls()
    print(f"loaded {len(GRAINCLS)} grain classes")
    # (measure, predicted direction of std-ctl diff, one-sided alternative)
    primaries = [('nov1', 'less'), ('nov10', 'less'),
                 ('repsim', 'greater'), ('bedresp', 'less')]
    diffs = {m: [] for m, _ in primaries}
    all_floors_ok = True
    for cls, cname in ((0, 'familiar'), (1, 'dense'), (2, 'novel')):
        for idx in range(4):
            got = analyze_scene(cls, idx)
            if got is None:
                print(f"c{cls}({cname}) i{idx}: MISSING", flush=True)
                continue
            res, ident, overlap, bedn = got
            print(f"c{cls}({cname}) i{idx}: fg_identical={ident} "
                  f"bed_source_overlap={overlap:.2f} bedn={bedn}", flush=True)
            for m, _ in primaries:
                d = res['std'][m] - res['ctl'][m]
                diffs[m].append(d)
            fr = [f / KIDS_MEDIAN for f in res['std']['floors']]
            ok = all(r >= 3.0 for r in fr)
            all_floors_ok = all_floors_ok and ok
            print(f"   std floors ratios: {[f'{r:.2f}' for r in fr]} all>=3x: {ok}")
            print(f"   std: nov1={res['std']['nov1']:.4f} nov10={res['std']['nov10']:.4f} "
                  f"repsim={res['std']['repsim']:.4f} bedresp={res['std']['bedresp']:+.4f}")
            print(f"   ctl: nov1={res['ctl']['nov1']:.4f} nov10={res['ctl']['nov10']:.4f} "
                  f"repsim={res['ctl']['repsim']:.4f} bedresp={res['ctl']['bedresp']:+.4f}")
    ps = []
    print("\nmeasure  med_diff  W       p(one-sided, predicted dir)")
    for m, alt in primaries:
        d = np.array(diffs[m])
        nz = d[d != 0]
        if len(nz) == 0:
            W, p = 0.0, 1.0
        else:
            W, p = wilcoxon(nz, alternative=alt)
        ps.append(p)
        print(f"{m:8s} {np.median(d):+9.4f} {W:7.1f} {p:.4f}")
    sig = holm(ps)
    print(f"\nHolm-corrected significant: {[m for (m, _), s in zip(primaries, sig) if s]}")
    any_sig = any(sig)
    kill = (not any_sig) and all_floors_ok
    print(f"all 60 standard boundary floors >=3x: {all_floors_ok}")
    print(f"machine verdict: {'KILLED' if kill else 'SURVIVES'}")

if __name__ == '__main__':
    main()
