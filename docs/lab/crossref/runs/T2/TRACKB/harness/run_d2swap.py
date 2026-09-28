#!/usr/bin/env python3
"""D2: mid-stream curriculum swap WITHOUT resetting history (prereg §D2).

varB/varC: N turns on X, swap stimulus bytes, continue M turns, same history.
varA: session-locked by design -> new session on Y with same decision pattern
      (architectural difference documented as evidence, not a defect).
Measures: fraction of post-shift proposals with spans in Y's GT;
          turns-to-first-Y-GT-proposal.
"""
import json, os, sys, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
from harness import CURR, POLICIES, BIN_B, BIN_C, _bp, _ch

N_PRE, N_POST = 10, 20

def runB_swap(workdir, sess_id):
    os.makedirs(workdir, exist_ok=True)
    CX, CY = CURR["std"], CURR["shift"]
    fx = H.write_fixtures(workdir, "std")
    fx_abs = os.path.abspath(fx)
    # phase 1: N_PRE turns on X with gt policy (GT_X)
    pol = POLICIES["gt"]
    gtX = ("ab", set(CX["gt_ab"]))
    gtY = ("ab", set(CY["gt_ab"]))
    st = {}
    VMAP = {"ADOPT": 0, "REVISE": 1, "REJECT": 2, "DEFER": 3}
    records, pre_props, post_props = [], [], []
    turn = 0
    while turn < N_PRE:
        hist = os.path.join(fx, "b_d2.hist")
        _bp.write_history(hist, records)
        p = subprocess.run([BIN_B, fx_abs, "curr_raw.bin", "b_d2.hist", str(sess_id)],
                           capture_output=True, cwd=workdir)
        if p.returncode != 0:
            break
        try:
            props = _bp.parse_stream(p.stdout, len(CX["prose"]), expect_tid=3,
                                     expect_sess=sess_id, expect_seq0=len(pre_props))
        except ValueError:
            break
        if not props:
            break
        for pr in props:
            d = pol(pr, len(pre_props), len(CX["prose"]), gtX, st)
            v, r, span = d
            records.append((pr["seq"], pr["kind"], VMAP[v], r, pr["ss"], pr["se"]))
        pre_props.extend(props)
        turn += 1
    # SWAP: replace stimulus bytes with Y, keep history and session
    open(os.path.join(fx, "curr_raw.bin"), "wb").write(CY["prose"])
    st2 = {}
    turns_to_first_y = None
    post_turn = 0
    while post_turn < N_POST:
        hist = os.path.join(fx, "b_d2.hist")
        _bp.write_history(hist, records)
        p = subprocess.run([BIN_B, fx_abs, "curr_raw.bin", "b_d2.hist", str(sess_id)],
                           capture_output=True, cwd=workdir)
        if p.returncode != 0:
            break
        try:
            props = _bp.parse_stream(p.stdout, len(CY["prose"]), expect_tid=3,
                                     expect_sess=sess_id,
                                     expect_seq0=len(pre_props) + len(post_props))
        except ValueError:
            break
        if not props:
            break
        for pr in props:
            if turns_to_first_y is None and (pr["ss"], pr["se"]) in gtY[1]:
                turns_to_first_y = post_turn
            d = pol(pr, len(pre_props) + len(post_props), len(CY["prose"]), gtY, st2)
            v, r, span = d
            records.append((pr["seq"], pr["kind"], VMAP[v], r, pr["ss"], pr["se"]))
        post_props.extend(props)
        post_turn += 1
    in_y = sum(1 for pr in post_props if (pr["ss"], pr["se"]) in gtY[1])
    return dict(variant="B", n_pre=len(pre_props), n_post=len(post_props),
                frac_post_in_y=round(in_y / len(post_props), 3) if post_props else None,
                turns_to_first_y=turns_to_first_y)

def runC_swap(workdir, sess_id):
    os.makedirs(workdir, exist_ok=True)
    CX, CY = CURR["std"], CURR["shift"]
    fx = H.write_fixtures(workdir, "std")
    wd = os.path.abspath(os.path.join(fx, "wired"))
    hd = os.path.abspath(os.path.join(fx, "hist"))
    pol = POLICIES["gt"]
    gtX = ("c", set(CX["gt_c"]))
    gtY = ("c", set(CY["gt_c"]))
    st = {}
    VMAP = {"ADOPT": 1, "REVISE": 2, "REJECT": 3, "DEFER": 4}
    hist = _ch.new_history(sess_id)
    hpath = os.path.join(hd, "c_d2.hist")
    pre_props, post_props = [], []
    turn = 0
    while turn < N_PRE:
        with open(hpath, "wb") as f:
            f.write(hist)
        p = subprocess.run([BIN_C, "propose", "0", str(sess_id), wd, hd, "c_d2.hist"],
                           capture_output=True, cwd=workdir)
        if p.returncode != 0:
            break
        try:
            pr = _ch.parse_proposal(p.stdout)
        except ValueError:
            break
        pre_props.append(pr)
        hist = _ch.append_propose(hist, pr)
        d = pol(pr, len(pre_props) - 1, 65536, gtX, st)
        v, r, span = d
        rs, re_ = (span if v == "REVISE" else (0, 0))
        hist = _ch.append_decide(hist, pr["seq"], VMAP[v], r, rs, re_)
        turn += 1
    # SWAP slice bytes, keep history
    open(os.path.join(wd, "slice_S0.bin"), "wb").write(CY["slice"])
    st2 = {}
    turns_to_first_y = None
    post_turn = 0
    while post_turn < N_POST:
        with open(hpath, "wb") as f:
            f.write(hist)
        p = subprocess.run([BIN_C, "propose", "0", str(sess_id), wd, hd, "c_d2.hist"],
                           capture_output=True, cwd=workdir)
        if p.returncode == 20:
            break
        if p.returncode != 0:
            break
        try:
            pr = _ch.parse_proposal(p.stdout)
        except ValueError:
            break
        if turns_to_first_y is None and (pr["ss"], pr["se"]) in gtY[1]:
            turns_to_first_y = post_turn
        post_props.append(pr)
        hist = _ch.append_propose(hist, pr)
        d = pol(pr, len(pre_props) + len(post_props) - 1, 65536, gtY, st2)
        v, r, span = d
        rs, re_ = (span if v == "REVISE" else (0, 0))
        hist = _ch.append_decide(hist, pr["seq"], VMAP[v], r, rs, re_)
        post_turn += 1
    in_y = sum(1 for pr in post_props if (pr["ss"], pr["se"]) in gtY[1])
    return dict(variant="C", n_pre=len(pre_props), n_post=len(post_props),
                frac_post_in_y=round(in_y / len(post_props), 3) if post_props else None,
                turns_to_first_y=turns_to_first_y)

def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath("work/d2swap")
    out = {}
    # varA: session-locked -> new session on Y (already covered by d2/gt/shift); document
    out["A"] = dict(variant="A", note="session-locked by design; D2 = new session on Y "
                                      "with same decision pattern (see d2/gt/shift legs)")
    rb = runB_swap(os.path.join(root, "B"), 8101)
    out["B"] = rb
    print("B swap:", {k: rb[k] for k in ("n_pre", "n_post", "frac_post_in_y", "turns_to_first_y")}, flush=True)
    rc = runC_swap(os.path.join(root, "C"), 8102)
    out["C"] = rc
    print("C swap:", {k: rc[k] for k in ("n_pre", "n_post", "frac_post_in_y", "turns_to_first_y")}, flush=True)
    with open(os.path.join(root, "d2swap.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", os.path.join(root, "d2swap.json"))

if __name__ == "__main__":
    main()
