#!/usr/bin/env python3
"""R2-2 bar scorer. Reads a run dir (8 shard ledgers + self-collision probes)
and scores every preregistered bar mechanically.

False install := install==1 and class != truth.
Ablation (B4) := always-INSTALL with the same class judgment (derived, no
separate binary needed): ablation false installs = class != truth.

Usage: score2.py <rundir> <probes.json>
Prints a full bar table; exit 0 iff all kill bars pass.
"""
import os, sys, json
from collections import defaultdict

SIG_TARGETED = {"R2A-COL-1", "R2A-SHP-1", "R2A-SHP-2", "R2A-TMB-2", "R2A-MOT-1"}
NOVEL = {"R2A-PTC-2", "R2A-CCN-2", "R2A-MOT-2"}

def load(rundir):
    recs = []
    for s in range(8):
        with open(os.path.join(rundir, "ledger_shard%d.jsonl" % s)) as f:
            for line in f:
                recs.append(json.loads(line))
    return recs

def main():
    rundir, probep = sys.argv[1], sys.argv[2]
    recs = load(rundir)
    print("records: %d" % len(recs))

    def is_fi(r):  # false install
        return r["r22"]["install"] == "1" and r["r22"]["class"] != r["r22"]["truth"]

    def correct(r):
        return r["r22"]["class"] == r["r22"]["truth"]

    # ---- B1: judgment accuracy on frozen 370 primary
    prim = [r for r in recs if r["variant"] == "primary"]
    b1_all = sum(1 for r in prim if correct(r)) / len(prim)
    b1_task = {}
    for t in sorted(set(r["task"] for r in prim)):
        tr = [r for r in prim if r["task"] == t]
        b1_task[t] = sum(1 for r in tr if correct(r)) / len(tr)
    print("B1 primary judgment accuracy: %.3f (n=%d) bar>=0.60 %s" %
          (b1_all, len(prim), "PASS" if b1_all >= 0.60 else "FAIL"))
    for t, a in b1_task.items():
        print("    %-12s %.3f" % (t, a))

    # ---- retrieval accuracy (kill 2): installed & correct / installed, on primary
    inst = [r for r in prim if r["r22"]["install"] == "1"]
    retr = sum(1 for r in inst if correct(r)) / len(inst) if inst else 0.0
    print("retrieval accuracy: %.3f (%d/%d installed) bar>=0.90 %s" %
          (retr, sum(1 for r in inst if correct(r)), len(inst),
           "PASS" if retr >= 0.90 else "FAIL"))

    # ---- B2: vs Approach A on identical fixtures (primary set)
    a_corr = sum(1 for r in prim if r["approachA"]["judgment"] == r["r22"]["truth"])
    a_acc = a_corr / len(prim)
    print("B2 approach A accuracy: %.3f ; R2-2: %.3f ; delta: %+.3f (reported)" %
          (a_acc, b1_all, b1_all - a_acc))

    # ---- B3: ops/bytes per percept
    ops2 = [int(r["r22"]["ops"]) for r in recs]
    opsA = [int(r["approachA"]["ops"]) for r in recs if r["approachA"]["ops"]]
    print("B3 R2-2 mean ops: %.0f ; approach A mean ops: %.0f" %
          (sum(ops2) / len(ops2), sum(opsA) / len(opsA) if opsA else 0))
    print("B3 signature bytes: R2-2 32 (8xi32 feature vector) vs G3 datum 36")

    # ---- B4: contract vs ablation on adversarial
    adv = [r for r in recs if r["variant"] == "adversarial"]
    changed = sum(1 for r in adv if r["r22"]["install"] == "0") / len(adv)
    fi_contract = sum(1 for r in adv if is_fi(r))
    fi_ablation = sum(1 for r in adv if not correct(r))
    print("B4 decisions changed: %.3f bar>=0.10 %s" % (changed, "PASS" if changed >= 0.10 else "FAIL"))
    print("B4 false installs: contract %d < ablation %d %s" %
          (fi_contract, fi_ablation, "PASS" if fi_contract < fi_ablation else "FAIL"))

    # ---- B5: false-install rates
    targ = [r for r in adv if r["family"] in SIG_TARGETED]
    fi_targ = sum(1 for r in targ if is_fi(r))
    fi_all = sum(1 for r in adv if is_fi(r))
    print("B5 targeted false-install: %d/%d = %.4f bar<=0.01 %s" %
          (fi_targ, len(targ), fi_targ / len(targ), "PASS" if fi_targ / len(targ) <= 0.01 else "FAIL"))
    print("B5 overall false-install: %d/%d = %.4f bar<=0.02 %s" %
          (fi_all, len(adv), fi_all / len(adv), "PASS" if fi_all / len(adv) <= 0.02 else "FAIL"))
    # per-family targeted
    for fam in sorted(SIG_TARGETED):
        fr = [r for r in adv if r["family"] == fam]
        if not fr:
            print("    %-12s (no records yet)" % fam)
            continue
        nfi = sum(1 for r in fr if is_fi(r))
        print("    %-12s %d/%d = %.4f" % (fam, nfi, len(fr), nfi / len(fr)))

    # ---- kill 3a: novel families — any false install kills
    novel_fi = [(r["family"], r["fixture"]) for r in adv
                if r["family"] in NOVEL and is_fi(r)]
    print("kill-3 novel false installs: %d %s" %
          (len(novel_fi), "PASS (none)" if not novel_fi else "KILL"))
    for fam, fx in novel_fi[:10]:
        print("    %s %s" % (fam, fx))

    # ---- kill 3b: self-collision probes (15 bank fixtures must withhold)
    probes = json.load(open(probep))
    self_fi = [p for p in probes if p["install"] != "0"]
    print("kill-3 self-collision: %d/15 withhold %s" %
          (15 - len(self_fi), "PASS" if not self_fi else "KILL"))
    for p in self_fi:
        print("    INSTALLED:", p["name"])

    # ---- summary verdict
    kills = []
    if b1_all < 0.60: kills.append("B1")
    if retr < 0.90: kills.append("retrieval>=0.90")
    if changed < 0.10: kills.append("B4-change")
    if not (fi_contract < fi_ablation): kills.append("B4-fewer")
    if fi_targ / len(targ) > 0.01: kills.append("B5-targeted")
    if fi_all / len(adv) > 0.02: kills.append("B5-overall")
    if novel_fi: kills.append("novel-install")
    if self_fi: kills.append("self-collision")
    print("KILL BARS FAILED:", kills if kills else "none")
    sys.exit(1 if kills else 0)

main()
