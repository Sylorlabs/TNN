#!/usr/bin/env python3
"""adv2_ret_det.py — LH-ADV-2 dedicated ADV-RET / ADV-DET runs.

Result-side, decision-free measurement tooling (NOT trial machinery).
Reuses the FROZEN LH-ADV-2 pipeline (adv2_run.run_stage) verbatim against
the committed LH-ADV-2 artifacts:

  ADV-RET: re-run 10 stages (incl. all 5 recovered/injected cases) under
           identical conditions; final_spec + binary_output + accept state
           must be BYTE-IDENTICAL to ledger2.json. 10/10 required.
  ADV-DET: 5 stages x 5 reps (incl. a recovered stage, D6); final spec,
           emitted source, compiled binary, and binary output must be
           byte-identical across reps.

Pure decision-free harness: no choices, no heuristics, no RNG.
The sealed envelope (envelope.json) is read locally and NEVER committed.
"""
import json, subprocess, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import adv2_run

TMP = os.environ.get("ADV2_TMP", os.path.join(HERE, "tmp_rd2"))
REF_LEDGER = os.path.join(HERE, "ledger2.json")
ENVELOPE = os.environ.get("ADV2_ENVELOPE", os.path.join(HERE, "envelope.json"))
KB_PATH = os.path.join(HERE, "adv_kb.txt")

RET_STAGES = ["D6", "B7", "D5", "C7", "D8", "A1", "A5", "C1", "J1", "E9"]
DET_STAGES = ["D6", "A1", "A5", "J2", "E9"]
DET_REPS = 5

def sha(b):
    return hashlib.sha256(b).hexdigest()

def artifacts(rec, src_path, bin_path):
    a = {}
    a["spec"] = rec.get("final_spec", "")
    a["output"] = rec.get("binary_output", "")
    a["source_sha"] = sha(open(src_path, "rb").read()) if src_path and os.path.exists(src_path) else None
    a["binary_sha"] = sha(open(bin_path, "rb").read()) if bin_path and os.path.exists(bin_path) else None
    return a

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "ret"
    os.makedirs(TMP, exist_ok=True)
    adv2_run.TMP = TMP
    env = json.load(open(ENVELOPE))
    kb_orig = open(KB_PATH).read()
    ref = json.load(open(REF_LEDGER))
    ref_by = {s["stage"]: s for s in ref["stages"]}
    out = {"mode": mode, "trial": "LH-ADV-2", "stages": [], "pass": False}

    if mode == "ret":
        ledger_stages = []
        upstreams = {}
        for st in RET_STAGES:
            inj = next((f for f in env["failures"] if f["stage"] == st), None)
            if inj and inj["type"] == "DEP-CORRUPT" and inj["upstream_stage"] not in upstreams:
                urec, _, _ = adv2_run.run_stage(inj["upstream_stage"], env, kb_orig, ledger_stages)
                ledger_stages.append(urec)
                upstreams[inj["upstream_stage"]] = urec
        ok = 0
        for st in RET_STAGES:
            rec, sp, bp = adv2_run.run_stage(st, env, kb_orig, ledger_stages)
            ledger_stages.append(rec)
            r = ref_by[st]
            spec_match = rec.get("final_spec") == r.get("final_spec")
            out_match = rec.get("binary_output") == r.get("binary_output")
            accept_match = rec.get("stage_accept") == r.get("stage_accept")
            m = spec_match and out_match and accept_match
            ok += 1 if m else 0
            out["stages"].append({
                "stage": st, "match": m, "spec_match": spec_match,
                "output_match": out_match, "accept_match": accept_match,
                "cycles": rec.get("cycles"),
                "injected": st in [f["stage"] for f in env["failures"]],
            })
            print(f"RET {st}: {'MATCH' if m else 'MISMATCH'} "
                  f"(spec={spec_match} out={out_match} accept={accept_match} cycles={rec.get('cycles')})",
                  flush=True)
        out["ret_n"], out["ret_ok"] = len(RET_STAGES), ok
        out["pass"] = (ok == len(RET_STAGES))
        print(f"ADV-RET: {ok}/{len(RET_STAGES)} byte-identical -> {'PASS' if out['pass'] else 'FAIL'}")

    elif mode == "det":
        ok_stages = 0
        for st in DET_STAGES:
            reps = []
            for i in range(DET_REPS):
                ledger_stages = []
                rec, sp, bp = adv2_run.run_stage(st, env, kb_orig, ledger_stages)
                reps.append(artifacts(rec, sp, bp))
            agree = all(r == reps[0] for r in reps[1:])
            ok_stages += 1 if agree else 0
            out["stages"].append({"stage": st, "reps": DET_REPS, "agree": agree,
                                  "spec": reps[0]["spec"][:60],
                                  "binary_sha16": (reps[0]["binary_sha"] or "")[:16]})
            print(f"DET {st}: {'IDENTICAL x5' if agree else 'DIVERGED'} "
                  f"bin={ (reps[0]['binary_sha'] or '')[:16]}", flush=True)
        out["det_n"], out["det_ok"] = len(DET_STAGES), ok_stages
        out["pass"] = (ok_stages == len(DET_STAGES))
        print(f"ADV-DET: {ok_stages}/{len(DET_STAGES)} stages x5 identical -> {'PASS' if out['pass'] else 'FAIL'}")

    json.dump(out, open(os.path.join(HERE, f"result2_{mode}.json"), "w"), indent=1)
    return 0 if out["pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
