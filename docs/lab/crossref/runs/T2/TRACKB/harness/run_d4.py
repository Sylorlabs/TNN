#!/usr/bin/env python3
"""D4: adversarial history/evidence per prereg (defer storm, contradictory
verdicts, forged-but-well-formed history, truncated final record)."""
import json, os, sys, subprocess, struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
from harness import CURR, POLICIES, BIN_A, BIN_B, BIN_C, _bp, _ch, _dline_a

def policy_defer_storm(p, i, stim_len, gt, st):
    if i < 20:
        return ("DEFER", 0, None)
    return ("ADOPT", 0, None)

def policy_contra(p, i, stim_len, gt, st):
    span = (p["ss"], p["se"])
    if span in st:
        return ("REJECT", 2, None)
    st[span] = 1
    return ("ADOPT", 0, None)

H.POLICIES["defer_storm"] = policy_defer_storm
H.POLICIES["contra"] = policy_contra

def d4a_defer(variant, workdir, sess_id):
    from legs import run_leg
    m = run_leg(variant, "defer_storm", workdir, sess_id)
    return m

def d4b_contra(variant, workdir, sess_id):
    from legs import run_leg
    m = run_leg(variant, "contra", workdir, sess_id)
    # count contradictory pairs: same span ADOPTed then REJECTed
    cj = json.load(open(os.path.join(workdir, "canon.json")))
    dj = json.load(open(os.path.join(workdir, "decisions.json")))
    seen_adopt = set()
    contra_n = 0
    for (seq, kind, ss, se, conf), d in zip(cj, dj):
        span = (ss, se)
        if d[0] == "ADOPT":
            seen_adopt.add(span)
        elif d[0] == "REJECT" and d[1] == 2 and span in seen_adopt:
            contra_n += 1
    m["contradictory_pairs"] = contra_n
    return m

def d4c_forged_B(workdir, sess_id):
    # forged-but-well-formed HIST: 6 records for seqs the teacher never emitted
    os.makedirs(workdir, exist_ok=True)
    fx = H.write_fixtures(workdir)
    fx_abs = os.path.abspath(fx)
    recs = [(100 + i, 1, 0, 0, 10 * i, 10 * i + 4) for i in range(6)]
    hp = os.path.join(fx, "forged.hist")
    _bp.write_history(hp, recs)
    p = subprocess.run([BIN_B, fx_abs, "curr_raw.bin", "forged.hist", str(sess_id)],
                       capture_output=True, cwd=workdir)
    out = p.stdout.decode(errors="replace")
    nprop = out.count("V3PROP")
    return dict(variant="B", test="forged_history", rc=p.returncode,
                n_proposals=nprop,
                stderr=p.stderr.decode(errors="replace")[:200],
                stdout_tail=out[-200:])

def d4c_forged_C(workdir, sess_id):
    # forged varC history: propose+decide records for seqs never emitted
    os.makedirs(workdir, exist_ok=True)
    fx = H.write_fixtures(workdir)
    wd = os.path.abspath(os.path.join(fx, "wired"))
    hd = os.path.abspath(os.path.join(fx, "hist"))
    hist = _ch.new_history(sess_id)
    for i in range(4):
        fake = {"seq": 50 + i, "kind": 1, "ss": 100 * i, "se": 100 * i + 5,
                "conf": 150, "nbytes": 70, "aux": [(0, 5)], "gnd": [(0, 5)]}
        hist = _ch.append_propose(hist, fake)
        hist = _ch.append_decide(hist, 50 + i, 1, 0, 0, 0)
    hp = os.path.join(hd, "forged.hist")
    open(hp, "wb").write(hist)
    p = subprocess.run([BIN_C, "propose", "0", str(sess_id), wd, hd, "forged.hist"],
                       capture_output=True, cwd=workdir)
    out = p.stdout.decode(errors="replace")
    return dict(variant="C", test="forged_history", rc=p.returncode,
                stdout_head=out[:200],
                stderr=p.stderr.decode(errors="replace")[:200])

def d4d_trunc_B(workdir, sess_id):
    # valid history, truncated mid-final-record
    os.makedirs(workdir, exist_ok=True)
    fx = H.write_fixtures(workdir)
    fx_abs = os.path.abspath(fx)
    recs = [(i, 1, 0, 0, 10 * i, 10 * i + 4) for i in range(5)]
    hp = os.path.join(fx, "trunc.hist")
    _bp.write_history(hp, recs)
    data = open(hp, "rb").read()
    open(hp, "wb").write(data[:len(data) - 7])  # cut mid-record
    p = subprocess.run([BIN_B, fx_abs, "curr_raw.bin", "trunc.hist", str(sess_id)],
                       capture_output=True, cwd=workdir)
    return dict(variant="B", test="truncated_history", rc=p.returncode,
                stderr=p.stderr.decode(errors="replace")[:200],
                stdout=p.stdout.decode(errors="replace")[:200])

def d4d_trunc_C(workdir, sess_id):
    os.makedirs(workdir, exist_ok=True)
    fx = H.write_fixtures(workdir)
    wd = os.path.abspath(os.path.join(fx, "wired"))
    hd = os.path.abspath(os.path.join(fx, "hist"))
    hist = _ch.new_history(sess_id)
    fake = {"seq": 0, "kind": 1, "ss": 0, "se": 5, "conf": 150, "nbytes": 70,
            "aux": [(0, 5)], "gnd": [(0, 5)]}
    hist = _ch.append_propose(hist, fake)
    hist = _ch.append_decide(hist, 0, 1, 0, 0, 0)
    hp = os.path.join(hd, "trunc.hist")
    open(hp, "wb").write(hist[:-11])  # cut mid-record
    p = subprocess.run([BIN_C, "propose", "0", str(sess_id), wd, hd, "trunc.hist"],
                       capture_output=True, cwd=workdir)
    return dict(variant="C", test="truncated_history", rc=p.returncode,
                stderr=p.stderr.decode(errors="replace")[:200],
                stdout=p.stdout.decode(errors="replace")[:200])

def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath("work/d4")
    out = {}
    for v in ["A", "B", "C"]:
        wd = os.path.join(root, "defer_storm", v)
        m = d4a_defer(v, wd, 8201)
        with open(os.path.join(wd, "metrics.json"), "w") as f:
            json.dump(m, f, indent=1, sort_keys=True)
        out[f"defer_{v}"] = {k: m.get(k) for k in ("n_proposals", "kinds", "terminal", "converged", "turns", "rounds", "canon_sha")}
        print(f"D4a defer {v}: n={m['n_proposals']} term={m['terminal']}", flush=True)
    for v in ["A", "B", "C"]:
        wd = os.path.join(root, "contra", v)
        m = d4b_contra(v, wd, 8202)
        with open(os.path.join(wd, "metrics.json"), "w") as f:
            json.dump(m, f, indent=1, sort_keys=True)
        out[f"contra_{v}"] = {k: m.get(k) for k in ("n_proposals", "kinds", "terminal", "converged", "turns", "rounds", "contradictory_pairs", "canon_sha")}
        print(f"D4b contra {v}: n={m['n_proposals']} contra_pairs={m['contradictory_pairs']} term={m['terminal']}", flush=True)
    out["forged_B"] = d4c_forged_B(os.path.join(root, "forged", "B"), 8203)
    print("D4c forged B:", {k: out["forged_B"][k] for k in ("rc", "n_proposals")}, flush=True)
    out["forged_C"] = d4c_forged_C(os.path.join(root, "forged", "C"), 8204)
    print("D4c forged C:", {k: out["forged_C"][k] for k in ("rc",)}, flush=True)
    out["trunc_B"] = d4d_trunc_B(os.path.join(root, "trunc", "B"), 8205)
    print("D4d trunc B:", {k: out["trunc_B"][k] for k in ("rc",)}, flush=True)
    out["trunc_C"] = d4d_trunc_C(os.path.join(root, "trunc", "C"), 8206)
    print("D4d trunc C:", {k: out["trunc_C"][k] for k in ("rc",)}, flush=True)
    with open(os.path.join(root, "d4_table.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", os.path.join(root, "d4_table.json"))

if __name__ == "__main__":
    main()
