#!/usr/bin/env python3
"""D3 edge-stimulus battery: graceful vs cliff classification."""
import json, os, sys, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legs import run_leg

VARIANTS = ["A", "B", "C"]
CURRS = ["edge_oneword", "edge_nowords", "edge_1byte"]
REPS = 2

def novocab_C(workdir, sess_id):
    """varC-specific: slice with zero vocabulary matches."""
    import harness as H
    from harness import CURR, POLICIES, BIN_C, _ch
    os.makedirs(workdir, exist_ok=True)
    C = CURR["std"]
    fx = H.write_fixtures(workdir, "std")
    wd = os.path.abspath(os.path.join(fx, "wired"))
    hd = os.path.abspath(os.path.join(fx, "hist"))
    # replace slice with bytes containing no vocab word (digits+punct)
    nov = (b"0123456789!@# " * 5000)[:65536]
    assert len(nov) == 65536
    open(os.path.join(wd, "slice_S0.bin"), "wb").write(nov)
    pol = POLICIES["gt"]
    gt = ("c", set(C["gt_c"]))
    st = {}
    VMAP = {"ADOPT": 1, "REVISE": 2, "REJECT": 3, "DEFER": 4}
    hist = _ch.new_history(sess_id)
    hpath = os.path.join(hd, "c_novocab.hist")
    props = []
    turn = 0
    term = "turn_cap"
    while turn < 64:
        with open(hpath, "wb") as f:
            f.write(hist)
        p = subprocess.run([BIN_C, "propose", "0", str(sess_id), wd, hd, "c_novocab.hist"],
                           capture_output=True, cwd=workdir)
        if p.returncode == 20:
            term = "session_cap"; break
        if p.returncode != 0:
            term = f"rc{p.returncode}"; break
        try:
            pr = _ch.parse_proposal(p.stdout)
        except ValueError:
            term = "parse_error"; break
        props.append(pr)
        hist = _ch.append_propose(hist, pr)
        d = pol(pr, len(props) - 1, 65536, gt, st)
        v, r, span = d
        rs, re_ = (span if v == "REVISE" else (0, 0))
        hist = _ch.append_decide(hist, pr["seq"], VMAP[v], r, rs, re_)
        turn += 1
    kinds = {}
    for pr in props:
        kinds[str(pr["kind"])] = kinds.get(str(pr["kind"]), 0) + 1
    return dict(variant="C", test="novocab_slice", n_proposals=len(props),
                kinds=kinds, terminal=term, turns=turn)

def bigstim_B(workdir, sess_id):
    """varB-specific: 1MB max-size stimulus."""
    import harness as H
    from harness import CURR, POLICIES, BIN_B, _bp
    os.makedirs(workdir, exist_ok=True)
    C = CURR["std"]
    fx = H.write_fixtures(workdir, "std")
    fx_abs = os.path.abspath(fx)
    big = (C["prose"] * ((1048576 // len(C["prose"])) + 1))[:1048576]
    assert len(big) == 1048576
    open(os.path.join(fx, "curr_raw.bin"), "wb").write(big)
    pol = POLICIES["gt"]
    gt = ("ab", set(C["gt_ab"]))
    st = {}
    VMAP = {"ADOPT": 0, "REVISE": 1, "REJECT": 2, "DEFER": 3}
    records, props = [], []
    turn = 0
    term = "empty_batch"
    while turn < 30:
        hp = os.path.join(fx, "b_big.hist")
        _bp.write_history(hp, records)
        p = subprocess.run([BIN_B, fx_abs, "curr_raw.bin", "b_big.hist", str(sess_id)],
                           capture_output=True, cwd=workdir)
        if p.returncode != 0:
            term = f"rc{p.returncode}"; break
        try:
            prs = _bp.parse_stream(p.stdout, len(big), expect_tid=3,
                                   expect_sess=sess_id, expect_seq0=len(props))
        except ValueError:
            term = "parse_error"; break
        if not prs:
            break
        for pr in prs:
            d = pol(pr, len(props), len(big), gt, st)
            v, r, span = d
            records.append((pr["seq"], pr["kind"], VMAP[v], r, pr["ss"], pr["se"]))
        props.extend(prs)
        turn += 1
    kinds = {}
    for pr in props:
        kinds[str(pr["kind"])] = kinds.get(str(pr["kind"]), 0) + 1
    return dict(variant="B", test="stimulus_1MB", n_proposals=len(props),
                kinds=kinds, terminal=term, turns=turn,
                rc=p.returncode)

def classify(m):
    # graceful: teacher ran, emitted >=0 proposals, terminal is a clean/known state
    # cliff: nonzero unexpected rc, parse errors, crash
    t = m["terminal"]
    if m.get("events", {}).get("parse_error"):
        return "CLIFF(parse_error)"
    if t.startswith("rc") and t not in ("rc13", "rc20"):
        return f"CLIFF({t})"
    return "GRACEFUL"

def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath("work/d3")
    table = []
    for curr in CURRS:
        for v in VARIANTS:
            shas = set()
            reps = []
            for r in range(REPS):
                wd = os.path.join(root, curr, v, f"rep{r}")
                m = run_leg(v, "gt", wd, 9000 + r, curr=curr)
                with open(os.path.join(wd, "metrics.json"), "w") as f:
                    json.dump(m, f, indent=1, sort_keys=True)
                reps.append(m)
                shas.add(m["canon_sha"])
            det = "IDENTICAL" if len(shas) == 1 else "DIVERGED"
            cls = classify(reps[0])
            table.append(dict(curr=curr, variant=v, reps=reps,
                              determinism=det, classification=cls))
            r0 = reps[0]
            print(f"{curr} {v} det={det} class={cls} n={r0['n_proposals']} "
                  f"kinds={r0['kinds']} term={r0['terminal']} rc={r0['terminal_rc']}",
                  flush=True)
    with open(os.path.join(root, "d3_table.json"), "w") as f:
        json.dump(table, f, indent=1)
    print("wrote", os.path.join(root, "d3_table.json"))

if __name__ == "__main__":
    main()
