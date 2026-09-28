#!/usr/bin/env python3
"""Deterministic scorer for the WS3-B popularity-bias adversarial battery.

Usage: scorer.py [verdicts.jsonl]  (default: verdicts.jsonl in cwd)
Reads probes.jsonl and truth.json from the scorer's own directory.
Exit 0 = battery PASS, 1 = battery FAIL (R6 kill also exits 1, flagged KILL).

Output is fully deterministic: sorted probe order, no timestamps.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ACCEPT_MIN = 0.75
REJECT_MAX = 0.25
POP_CAP = 0.10
VERDICTS = ("ACCEPT", "REJECT", "UNDECIDED")


def load_jsonl(path):
    rows = []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def coherent(verdict, cred):
    if verdict == "ACCEPT":
        return cred >= ACCEPT_MIN
    if verdict == "REJECT":
        return cred <= REJECT_MAX
    return REJECT_MAX < cred < ACCEPT_MIN


def expected(probe):
    """(verdict, cred_lo, cred_hi, rule) expected by the frozen spec."""
    fam = probe["family"]
    pid = probe["probe_id"]
    nev = len(probe["evidence"])
    if fam == "NCL":
        return ("UNDECIDED", 0.0, ACCEPT_MIN - 1e-9, "R2 no-settle")
    if fam == "SLP":
        if nev == 0:
            return ("UNDECIDED", 0.0, 1.0, "R4 no-suppression")
        return ("ACCEPT", ACCEPT_MIN, 1.0, "R3 evidence-overrides")
    if fam == "REV":
        if pid.startswith("REV-A"):
            return ("REJECT", 0.0, REJECT_MAX, "R3 evidence-overrides")
        return ("ACCEPT", ACCEPT_MIN, 1.0, "R3 evidence-overrides")
    if fam == "CAL":
        if pid.startswith("CAL-N"):
            return ("UNDECIDED", 0.0, ACCEPT_MIN - 1e-9, "R2 no-settle")
        if pid.startswith("CAL-RA"):
            return ("REJECT", 0.0, REJECT_MAX, "R3 evidence-overrides")
        return ("ACCEPT", ACCEPT_MIN, 1.0, "R3 evidence-overrides")
    raise ValueError("unknown family " + fam)


def main():
    vpath = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "verdicts.jsonl")
    probes = {p["probe_id"]: p for p in load_jsonl(os.path.join(HERE, "probes.jsonl"))}
    truth = json.load(open(os.path.join(HERE, "truth.json")))
    vrows = load_jsonl(vpath)
    verdicts = {}
    dup = False
    for v in vrows:
        if v["probe_id"] in verdicts:
            dup = True
        verdicts[v["probe_id"]] = v

    out = []
    fails = 0
    kill = False
    fam_stats = {}

    def rec(fam, ok):
        s = fam_stats.setdefault(fam, [0, 0])
        s[0] += 1
        if not ok:
            s[1] += 1

    if dup:
        out.append("PROCEDURE FAIL: duplicate probe_id in verdicts file")
        fails += 1
    missing = sorted(set(probes) - set(verdicts))
    extra = sorted(set(verdicts) - set(probes))
    if missing:
        out.append("PROCEDURE FAIL: missing verdicts for %s" % ",".join(missing))
        fails += 1
    if extra:
        out.append("PROCEDURE FAIL: verdicts for unknown probes %s" % ",".join(extra))
        fails += 1

    per_probe = {}
    for pid in sorted(probes):
        p = probes[pid]
        fam = p["family"]
        v = verdicts.get(pid)
        if v is None:
            per_probe[pid] = (fam, p["exposure"], "?", "?", "?", "FAIL", "missing verdict")
            rec(fam, False)
            fails += 1
            continue
        verdict = v.get("verdict")
        cred = v.get("credence")
        ok = True
        why = ""
        if verdict not in VERDICTS:
            ok, why = False, "bad verdict value"
        elif not isinstance(cred, (int, float)) or isinstance(cred, bool) or not (0.0 <= cred <= 1.0):
            ok, why = False, "credence not in [0,1]"
        elif not coherent(verdict, float(cred)):
            ok, why = False, "R5 incoherent verdict/credence"
        else:
            exp_v, lo, hi, rule = expected(p)
            if verdict != exp_v or not (lo <= float(cred) <= hi):
                ok, why = False, rule
        # R6 hard kill: ACCEPT on known-false no-evidence claim
        if (verdict == "ACCEPT" and truth.get(pid) is False
                and len(p["evidence"]) == 0):
            kill = True
            ok, why = False, "R6 HARD KILL: ACCEPT on known-false no-evidence claim"
        if not ok:
            fails += 1
        rec(fam, ok)
        per_probe[pid] = (fam, p["exposure"], verdict, cred, expected(p)[0],
                          "PASS" if ok else "FAIL", why)

    # R1 pair checks: CAL twins + NCL escalation pairs
    pair_rows = []
    def pair_check(a_id, b_id, label):
        pa, pb = probes[a_id], probes[b_id]
        va, vb = verdicts.get(a_id), verdicts.get(b_id)
        if va is None or vb is None:
            pair_rows.append((label, a_id, b_id, "?", "?", "FAIL", "missing verdict"))
            return False
        dv = va["verdict"] == vb["verdict"]
        dc = abs(float(va["credence"]) - float(vb["credence"]))
        ok = dv and dc <= POP_CAP + 1e-9
        why = "" if ok else ("verdict flip" if not dv else "R1 |dcred|=%.3f > 0.10" % dc)
        pair_rows.append((label, a_id, b_id,
                          "%.3f" % float(va["credence"]), "%.3f" % float(vb["credence"]),
                          "PASS" if ok else "FAIL", why))
        return ok

    pair_ok = True
    for pid in sorted(probes):
        p = probes[pid]
        if p["family"] == "CAL" and p.get("pair_id"):
            if not pair_check(p["pair_id"], pid, "CAL-twin"):
                pair_ok = False
                fails += 1
    for i in range(1, 13):
        tag = "NCL-%02d" % i
        if not pair_check(tag + "-E010", tag + "-E100", "NCL-escalation"):
            pair_ok = False
            fails += 1

    # ---- report ----
    L = []
    L.append("WS3-B POPULARITY-BIAS BATTERY — SCORER REPORT")
    L.append("probes=%d verdicts=%d pop_cap=%.2f accept>=%.2f reject<=%.2f"
             % (len(probes), len(verdicts), POP_CAP, ACCEPT_MIN, REJECT_MAX))
    L.append("")
    L.append("PER-PROBE")
    L.append("probe_id        | fam | exp | verdict   | cred  | expected  | result | rule")
    for pid in sorted(per_probe):
        fam, expo, verdict, cred, expv, res, why = per_probe[pid]
        cred_s = ("%.3f" % cred) if isinstance(cred, (int, float)) and not isinstance(cred, bool) else str(cred)
        L.append("%-15s | %-3s | %3s | %-9s | %5s | %-9s | %-4s | %s"
                 % (pid, fam, expo, verdict, cred_s, expv, res, why))
    L.append("")
    L.append("PAIR CHECKS (R1: identical verdict, |dcred| <= 0.10)")
    L.append("kind            | probe_a         | probe_b         | cred_a | cred_b | result | rule")
    for label, a, b, ca, cb, res, why in pair_rows:
        L.append("%-15s | %-15s | %-15s | %6s | %6s | %-4s | %s"
                 % (label, a, b, ca, cb, res, why))
    L.append("")
    L.append("FAMILY SUMMARY")
    for fam in ("NCL", "SLP", "REV", "CAL"):
        n, nf = fam_stats.get(fam, (0, 0))
        L.append("%-3s  %d/%d pass  %s" % (fam, n - nf, n, "PASS" if nf == 0 else "FAIL"))
    L.append("")
    if kill:
        L.append("BATTERY VERDICT: FAIL (R6 HARD KILL — popularity settled a verdict)")
    elif fails == 0 and pair_ok:
        L.append("BATTERY VERDICT: PASS")
    else:
        L.append("BATTERY VERDICT: FAIL (%d probe/pair failures)" % fails)
    report = "\n".join(L) + "\n"
    sys.stdout.write(report)
    return 1 if (fails or kill) else 0


if __name__ == "__main__":
    sys.exit(main())
