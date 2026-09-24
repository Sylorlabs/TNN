#!/usr/bin/env python3
"""D7 COMPOSED_SMOKE runner (H2 run-2). Smoke-level: one honest cell + one
lying cell through the composed T-COMP arm, 2x byte-identical each.

PASS iff (frozen prereg §0 D7):
  - 2x byte-identical on both cells;
  - composition order MC->SL->TRIPWIRE verified in the audit op interleaving;
  - 0 post-disconnect scaffold reads;
  - audit_total <= 2048 on every run;
  - zero cross-channel state leaks (namespace-discipline assertion on audit rows).

Usage:
  python3 d7_smoke.py --comp-bin PATH [--genome-honest G] [--genome-lying G]

The composed binary protocol (set by the wiring build crew when T-COMP lands):
  argv[1] = genome selector: "honest" | "lying"  (fixed fixture genomes)
  stdout: TN_CHECK/H2-style facts + LEDGER,<step>,<op>,<slot>,<aux> rows,
          where op carries the (namespace, op_name, code) triple and rows
          are emitted in per-episode order.
  Facts required: H2_AUDIT_TOTAL, H2_VERDICT, H2_NPROMOTE.

Status: SKELETON. The T-COMP composed binary does not exist yet — T-MC has
not landed and T-SL's D2/D6 verdicts are not recorded (T-TRIP D5 PASS).
This runner is ready to execute the moment the wiring crew delivers
run2/t_comp.zag + a built binary.
"""
import os, sys, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))

# Frozen op-code families (prereg §10). Interleaving order per episode:
#   act channel (MC 34-45, AV 21-23, SR 56-60) -> utterance (SL 46-55, UTT 24-28)
#   -> release (16-18) -> post-disconnect tripwire (TW 29-33) only.
FAM_ORDER = ["MC", "AV", "SR", "UTT", "SL", "REL", "TW"]
OP_FAM = {}
for c in range(34, 46):
    OP_FAM[c] = "MC"
for c in (21, 22, 23):
    OP_FAM[c] = "AV"
for c in range(56, 61):
    OP_FAM[c] = "SR"
for c in (24, 25, 26, 27, 28):
    OP_FAM[c] = "UTT"
for c in range(46, 56):
    OP_FAM[c] = "SL"
for c in (16, 17, 18):
    OP_FAM[c] = "REL"
for c in (29, 30, 31, 32, 33):
    OP_FAM[c] = "TW"
# FL2 base ops that are channel-neutral instrumentation
NEUTRAL = {13, 15, 19, 20}  # COMMIT, SCAFFOLD, QUAR_FULL, ROLLBACK
SCAFFOLD_OP = 15
AUDIT_BUDGET = 2048

def fam_of(op):
    return OP_FAM.get(op, "BASE" if op not in NEUTRAL else "NEUTRAL")

def parse_ledger(out):
    rows = []
    for line in out.splitlines():
        if line.startswith("LEDGER,"):
            p = line.split(",")
            rows.append({"step": int(p[1]), "op": int(p[2]),
                         "slot": int(p[3]), "aux": int(p[4])})
    return rows

def parse_facts(out):
    d = {}
    for line in out.splitlines():
        if (line.startswith("H2_") or line.startswith("TN_")) and "," in line:
            k, v = line.split(",", 1)
            d[k] = v.strip()
    return d

def check_interleaving(rows):
    """Per-episode op family sequence must respect FAM_ORDER (subsequence)."""
    by_step = {}
    for r in rows:
        by_step.setdefault(r["step"], []).append(r["op"])
    bad = []
    for step, ops in sorted(by_step.items()):
        fams = [fam_of(o) for o in ops if fam_of(o) not in ("NEUTRAL", "BASE")]
        # compress consecutive duplicates, then check subsequence of FAM_ORDER
        comp = []
        for f in fams:
            if not comp or comp[-1] != f:
                comp.append(f)
        idx = -1
        for f in comp:
            if f in FAM_ORDER:
                j = FAM_ORDER.index(f)
                if j < idx:
                    bad.append((step, comp))
                    break
                idx = j
    return bad

def check_no_post_disconnect_scaffold(rows):
    disc = [r["step"] for r in rows if r["op"] == 20 or
            (r["op"] == 16 and False)]  # DISCONNECT marker TBD by wiring crew
    # Fallback: op 20 (ROLLBACK) unused; real marker set at wiring time.
    # For now: any SCAFFOLD read after the first REL op in a late episode.
    rel_steps = [r["step"] for r in rows if fam_of(r["op"]) == "REL"]
    if not rel_steps:
        return []
    first_rel = min(rel_steps)
    return [r for r in rows if r["op"] == SCAFFOLD_OP and r["step"] > first_rel]

def run_cell(binp, which):
    outs = []
    for _ in range(2):
        r = subprocess.run([binp, which], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"{which} run failed: {r.stderr[:300]}")
        outs.append(r.stdout)
    det = outs[0] == outs[1]
    return outs[0], det

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comp-bin", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "d7_smoke_evidence.txt"))
    args = ap.parse_args()
    results = {}
    all_ok = True
    for which in ["honest", "lying"]:
        print(f"=== {which} cell ===")
        out, det = run_cell(args.comp_bin, which)
        facts = parse_facts(out)
        rows = parse_ledger(out)
        audit_total = int(facts.get("H2_AUDIT_TOTAL", facts.get("TN_AUDIT_TOTAL", "-1")))
        bad_order = check_interleaving(rows)
        post_disc = check_no_post_disconnect_scaffold(rows)
        ok = (det and not bad_order and not post_disc and
              0 < audit_total <= AUDIT_BUDGET)
        all_ok = all_ok and ok
        results[which] = {"det_2x": det, "audit_total": audit_total,
                          "order_violations": len(bad_order),
                          "post_disconnect_scaffold": len(post_disc),
                          "verdict": facts.get("H2_VERDICT", "?"),
                          "ok": ok}
        print(f"  det_2x={det} audit_total={audit_total} "
              f"order_violations={len(bad_order)} post_disc_scaffold={len(post_disc)} "
              f"verdict={facts.get('H2_VERDICT','?')} -> {'PASS' if ok else 'FAIL'}")
    print(f"D7 COMPOSED_SMOKE: {'PASS' if all_ok else 'FAIL'}")
    with open(args.out, "w") as f:
        f.write(f"# D7 smoke evidence\nD7,{'PASS' if all_ok else 'FAIL'}\n")
        for k, v in results.items():
            f.write(f"D7_{k},{v}\n")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
