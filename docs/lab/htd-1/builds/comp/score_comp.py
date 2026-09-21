#!/usr/bin/env python3
# score_comp.py — E-DE2+E-DE4 composition head-to-head scorer.
# Parses the four legs' artifacts (R=5 each), computes frozen-cost C,
# divergence vs FULL-DELIB, KB1/KB2/COMP verdicts, and the interaction term.
# Frozen weights: w=[1,12,5,0.2,0.5,0.02,20,1000,0.05,30,3] (COST_MODEL_FROZEN §2).
import struct, sys, os, hashlib, json

W = [1.0, 12.0, 5.0, 0.2, 0.5, 0.02, 20.0, 1000.0, 0.05, 30.0, 3.0]
RUNS = os.path.expanduser("~/workspace/htd-1/builds/comp/runs")

def parse(path):
    d = open(path, "rb").read()
    magic = d[0:8]
    if magic == b"HTD1FDA1":
        kind = "fd"; reclen = 128; veclen = 72
    elif magic == b"HTD1E2A1":
        kind = "e2a"; reclen = 128; veclen = 80
    elif magic in (b"HTD1E41\x00",):
        kind = "e4n"; reclen = 144; veclen = 88
    elif magic == b"HTD1ECA1":
        kind = "comp"; reclen = 144; veclen = 88
    else:
        raise ValueError(f"bad magic {magic!r} in {path}")
    n = struct.unpack("<i", d[16:20])[0]
    recs = d[24:24 + n * reclen]
    winners = [struct.unpack("<i", recs[i*reclen+16:i*reclen+20])[0] for i in range(n)]
    masks   = [struct.unpack("<i", recs[i*reclen+24:i*reclen+28])[0] for i in range(n)]
    ap = 24 + n * reclen
    vec = struct.unpack("<9q", d[ap:ap+72])
    if kind in ("fd", "e2a"):
        n01, n02, n03, mr_pg, mw_pg, cst, cft, gate, led = vec
        n11 = struct.unpack("<q", d[ap+72:ap+80])[0] if kind == "e2a" else 0
        nvec = [n01, n02, n03, mr_pg*1024, mw_pg*1024, 64*led, led, led, gate, 0, n11]
    else:
        nvec = list(struct.unpack("<11q", d[ap:ap+88]))
    hits = None
    if kind in ("e4n", "comp"):
        hits = [struct.unpack("<i", recs[i*reclen+136:i*reclen+140])[0] for i in range(n)]
    C = sum(wi * ni for wi, ni in zip(W, nvec))
    sha = hashlib.sha256(d).hexdigest()
    return {"kind": kind, "n": n, "winners": winners, "masks": masks,
            "nvec": nvec, "C": C, "hits": hits, "sha": sha, "path": path}

def main():
    legs = {}
    rep = {}
    for tag in ("fd_p1", "fd_p2", "e2a_p1", "e2a_p2", "e4n_p1", "e4n_p2", "comp_p1", "comp_p2"):
        runs = []
        for r in range(1, 6):
            p = os.path.join(RUNS, f"{tag}_r{r}.bin")
            runs.append(parse(p))
        shas = {x["sha"] for x in runs}
        byteid = len(shas) == 1
        Cs = [x["C"] for x in runs]
        assert max(Cs) == min(Cs), f"non-deterministic C for {tag}"
        legs[tag] = runs[0]
        rep[tag] = {"byte_identical_5": byteid, "sha": runs[0]["sha"], "C": Cs[0],
                    "nvec": runs[0]["nvec"], "n": runs[0]["n"],
                    "hits": (sum(runs[0]["hits"]) if runs[0]["hits"] else None)}

    out = {"configs": rep, "verdicts": {}}
    # divergence vs FULL-DELIB (KB1: >2% kills)
    for bat in ("p1", "p2"):
        fd = legs[f"fd_{bat}"]
        for leg in ("e2a", "e4n", "comp"):
            w = legs[f"{leg}_{bat}"]["winners"]
            div = sum(1 for a, b in zip(fd["winners"], w) if a != b)
            out["verdicts"][f"{leg}_{bat}_divergence"] = {"n_div": div, "n": len(w),
                                                         "rate": div / len(w)}
    # savings vs FULL-DELIB (KB2: >=15% mean saving in full cost)
    for bat in ("p1", "p2"):
        Cfd = rep[f"fd_{bat}"]["C"]
        for leg in ("e2a", "e4n", "comp"):
            C = rep[f"{leg}_{bat}"]["C"]
            out["verdicts"][f"{leg}_{bat}_saving"] = {"saving": (Cfd - C) / Cfd,
                                                     "C": C, "C_fd": Cfd}
    # composition vs each parent alone + interaction term
    for bat in ("p1", "p2"):
        Cfd, Ce2, Ce4, Cc = (rep[f"{t}_{bat}"]["C"] for t in ("fd", "e2a", "e4n", "comp"))
        additive = Ce4 + Ce2 - Cfd   # independence prediction
        I = Cc - additive            # interaction term (>0 => sub-additive)
        out["verdicts"][f"comp_{bat}_vs_parents"] = {
            "C_comp": Cc, "C_e4": Ce4, "C_e2": Ce2, "C_fd": Cfd,
            "beats_e4_alone": Cc < Ce4, "delta_vs_e4": Ce4 - Cc,
            "additive_prediction": additive, "interaction_I": I,
            "saving_comp": (Cfd - Cc) / Cfd, "saving_e4": (Cfd - Ce4) / Cfd,
            "saving_e2": (Cfd - Ce2) / Cfd}
    json.dump(out, open(os.path.join(RUNS, "analysis.json"), "w"), indent=1)
    # human-readable summary
    L = []
    L.append("== E-DE2+E-DE4 composition head-to-head (frozen cost model) ==")
    for tag in ("fd_p1","e2a_p1","e4n_p1","comp_p1","fd_p2","e2a_p2","e4n_p2","comp_p2"):
        r = rep[tag]
        L.append(f"{tag}: n={r['n']} C={r['C']:.2f} vec={r['nvec']} hits={r['hits']} byteid5={r['byte_identical_5']}")
    L.append("")
    for k, v in out["verdicts"].items():
        L.append(f"{k}: {json.dumps(v)}")
    txt = "\n".join(L)
    open(os.path.join(RUNS, "score_summary.txt"), "w").write(txt + "\n")
    print(txt)

if __name__ == "__main__":
    main()
