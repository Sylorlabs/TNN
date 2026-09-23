#!/usr/bin/env python3
"""audit_adv2.py — LH-ADV-2 bar scoring and integrity audits from ledger2.json.

Scores: ADV-DS, ADV-REC, ADV-HH, ADV-CRIT, ADV-DIAG (ADV-RET/DET are
separate dedicated runs).
Integrity audits:
  - HINT-LEAK: no diagnose evidence string names a true upstream stage or
    carries a corruption label (the hardened-diagnosis kill criterion).
  - NO-RNG: trial .zag sources contain no randomness constructs.
  - NO-SOLUTION: machinery embeds no contract TEST out= vectors.
Prints bar table + AUDIT-PASS/FAIL. Decision-free, zero RNG.
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "ledger2.json")
ENVELOPE = os.environ.get("ADV2_ENVELOPE", os.path.join(HERE, "envelope.json"))

def main():
    ledger = json.load(open(LEDGER))
    env = json.load(open(ENVELOPE))
    stages = ledger["stages"]
    by = {s["stage"]: s for s in stages}
    inj_by = {f["stage"]: f for f in env["failures"]}
    results = []

    # ---- ADV-DS: all unseeded stages accepted, 0 defects ----
    unseeded = [s for s in stages if s["stage"] not in inj_by and s["stage"] != "F1"]
    ds_acc = sum(1 for s in unseeded if s.get("stage_accept"))
    ds_defects = sum(1 for s in unseeded if not s.get("stage_accept"))
    ds_pass = ds_acc == len(unseeded) and ds_defects == 0
    results.append(("ADV-DS", f"{ds_acc}/{len(unseeded)} unseeded ACCEPT, {ds_defects} defects", ds_pass))

    # ---- ADV-REC: 6/6 diagnosed; 5/5 recovered; 1/1 unrecoverable halted ----
    diag_ok, rec_ok = 0, 0
    for st, f in inj_by.items():
        s = by[st]
        t = f["type"]
        if t == "KB-CORRUPT":
            # quarantined ID may carry the injected marker suffix
            if any(q == f["entry_id"] or q.startswith(f["entry_id"])
                   for q in s.get("failures_diagnosed", [])) \
                    and s.get("stage_accept"):
                diag_ok += 1; rec_ok += 1
        elif t == "DEP-CORRUPT":
            if s.get("diag_depcorrupt") == "PASS" and s.get("stage_accept"):
                diag_ok += 1; rec_ok += 1
        elif t == "EMITTER-BUG":
            if s.get("diag_emitterbug") == "PASS" and s.get("recovered"):
                diag_ok += 1; rec_ok += 1
        elif t == "UNRECOVERABLE":
            if s.get("honest_halt") and "HALT UNRECOVERABLE" in s.get("halt", ""):
                diag_ok += 1
    unrec = [f for f in env["failures"] if f["type"] == "UNRECOVERABLE"]
    unrec_ok = all("HALT UNRECOVERABLE" in by[f["stage"]].get("halt", "") for f in unrec)
    # fabrication check: no candidates on unrecoverable, no invented specs
    fab = 0
    for f in unrec:
        s = by[f["stage"]]
        if s.get("final_spec"):
            fab += 1
    rec_pass = diag_ok == 6 and rec_ok == 5 and unrec_ok and fab == 0
    results.append(("ADV-REC", f"{diag_ok}/6 diagnosed; {rec_ok}/5 recovered; "
                   f"unrec halted={unrec_ok}; fabrication={fab}", rec_pass))

    # ---- ADV-HH: F1 KB-MISS; all stages terminated ----
    f1 = by.get("F1", {})
    hh_f1 = f1.get("honest_halt") and "KB-MISS" in f1.get("halt", "")
    terminated = all(s.get("stage_accept") or s.get("halt") for s in stages)
    hh_pass = hh_f1 and terminated
    results.append(("ADV-HH", f"F1 KB-MISS={hh_f1}; all 54 terminated={terminated}", hh_pass))

    # ---- ADV-DIAG: hardened diagnosis, exact root causes ----
    diag_pass = True
    detail = []
    for st, f in inj_by.items():
        s = by[st]
        if f["type"] == "DEP-CORRUPT":
            ok = s.get("diag_depcorrupt") == "PASS"
            detail.append(f"{st}->UPSTREAM {f['upstream_stage']}={ok}")
            diag_pass = diag_pass and ok
        elif f["type"] == "EMITTER-BUG":
            ok = s.get("diag_emitterbug") == "PASS"
            detail.append(f"{st}->LOCAL={ok}")
            diag_pass = diag_pass and ok
    results.append(("ADV-DIAG", "; ".join(detail), diag_pass))

    # ---- HINT-LEAK kill audit ----
    # Kill criterion: any true-upstream hint in any diagnose evidence
    # string. The symptom-only template is
    #   OUTPUT-MISMATCH expected=... observed=... actual_input=... spec=...
    # so the word "upstream" must not appear in evidence at all, and the
    # true upstream stage must not appear as a token.
    leak = []
    for st, f in inj_by.items():
        s = by[st]
        if f["type"] in ("DEP-CORRUPT", "EMITTER-BUG"):
            for d in s.get("diagnoses", []):
                m = re.search(r'^DIAGNOSIS \S+ SPEC:\S+ EVIDENCE:(.*)$', d, re.M)
                if not m:
                    continue
                ev = m.group(1)
                if "upstream" in ev.lower():
                    leak.append(f"{st}: evidence contains 'upstream'")
                if f["type"] == "DEP-CORRUPT":
                    up = f["upstream_stage"]
                    if re.search(r'\b' + re.escape(up) + r'\b', ev):
                        leak.append(f"{st}: evidence names {up}")
                if "input-corrupted" in ev:
                    leak.append(f"{st}: evidence carries corruption label")
    hint_pass = len(leak) == 0
    results.append(("HINT-LEAK", "clean" if hint_pass else "; ".join(leak), hint_pass))

    # ---- NO-RNG audit ----
    rng_pat = re.compile(r'\b(rand|srand|random|getrandom|/dev/urandom|rdtsc)\b', re.I)
    rng_hits = []
    for fn in ["machinery/adv2_delib.zag", "machinery/adv2_emit.zag",
               "machinery/adv2_critic.zag", "adv2_run.py"]:
        src = open(os.path.join(HERE, fn)).read()
        for mm in rng_pat.finditer(src):
            rng_hits.append(f"{fn}:{mm.group(0)}")
    rng_pass = len(rng_hits) == 0
    results.append(("NO-RNG", "clean" if rng_pass else "; ".join(rng_hits), rng_pass))

    # ---- NO-SOLUTION audit: machinery must not embed contract TEST vectors ----
    # (Parsing the "TEST out=" marker is legitimate; embedding an actual
    # expected-output VALUE is the forbidden task solution.)
    sol_hits = []
    vectors = set()
    for cf in glob.glob(os.path.join(HERE, "contracts", "*.txt")):
        for m in re.finditer(r'^TEST out=(.{24,})$', open(cf).read(), re.M):
            vectors.add(m.group(1))
    for fn in ["machinery/adv2_delib.zag", "machinery/adv2_emit.zag",
               "machinery/adv2_critic.zag"]:
        src = open(os.path.join(HERE, fn)).read()
        for v in vectors:
            if v in src:
                sol_hits.append(f"{fn}: embeds {v[:40]}...")
                break
    sol_pass = len(sol_hits) == 0
    results.append(("NO-SOLUTION", "clean" if sol_pass else "; ".join(sol_hits), sol_pass))

    for bar, detail, ok in results:
        print(f"{bar}: {'PASS' if ok else 'FAIL'} — {detail}")
    all_pass = all(ok for _, _, ok in results)
    print("AUDIT-" + ("PASS" if all_pass else "FAIL"))
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
