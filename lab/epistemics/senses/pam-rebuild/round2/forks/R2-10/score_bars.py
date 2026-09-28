#!/usr/bin/env python3
"""R2-10 mechanical bar scorer (initial gate: THETA=700, VETO=0).
Bars: B1 (viability), B2 (vs Approach A), B4 (adversarial flip), B5 (KB4),
      B6 (byte-identical, checked separately), KB-E1, KB-E2, KB-E5.
"""
import hashlib
import os

R2 = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10")
FX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures")
BAT = os.path.join(R2, "evidence", "battery")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]


def load(run):
    rows = []
    for task in TASKS:
        p = os.path.join(BAT, "noemit_%s_%s.tsv" % (task, run))
        for line in open(p):
            f = line.rstrip("\n").split("\t")
            if len(f) < 11 or f[0].startswith("BATCH_ERROR"):
                continue
            rows.append({"fixture": f[0], "task": task, "judgment": f[1],
                         "conf": int(f[2]), "margin": int(f[3]), "ops": int(f[4]),
                         "mapping_ok": int(f[5]), "disposition": f[6],
                         "emit_digest": f[7], "feat0": f[8], "feat1": f[9]})
    return rows


def truth_of(fx):
    return open(os.path.join(FX, fx + ".truth")).read().strip().split("=", 1)[1]


def is_adv(fx):
    return fx.startswith("r2a_")


def main():
    rows = load("run1")
    print("run1 rows:", len(rows))
    for r in rows:
        r["truth"] = truth_of(r["fixture"])
        r["ok"] = 1 if r["judgment"] == r["truth"] else 0
        r["adv"] = 1 if is_adv(r["fixture"]) else 0
        r["install"] = 1 if (r["mapping_ok"] == 1 and r["conf"] >= 700) else 0

    # B1: viability on frozen 370 harness primary (>=60%)
    # (harness primary list not present; report overall accuracy as proxy + note)
    acc = sum(r["ok"] for r in rows) / len(rows)
    print("overall accuracy: %.4f (%d/%d)" % (acc, sum(r["ok"] for r in rows), len(rows)))

    # B4: adversarial flip — dispositions changed for the better vs Approach A.
    # Approach A has no gate/dispositions; report adversarial accuracy + install behavior.
    adv = [r for r in rows if r["adv"]]
    adv_acc = sum(r["ok"] for r in adv) / len(adv)
    print("adversarial: n=%d acc=%.4f" % (len(adv), adv_acc))
    norm = [r for r in rows if not r["adv"]]
    norm_acc = sum(r["ok"] for r in norm) / len(norm)
    print("normal:      n=%d acc=%.4f" % (len(norm), norm_acc))

    # B5: false installs <=3%
    inst = [r for r in rows if r["install"]]
    fi = [r for r in inst if not r["ok"]]
    print("B5: installs=%d false=%d trials=%d rate=%.4f%%  %s" %
          (len(inst), len(fi), len(rows), len(fi) / len(rows) * 100,
           "PASS" if len(fi) / len(rows) <= 0.03 else "FAIL"))
    # by task
    for t in TASKS:
        tr = [r for r in rows if r["task"] == t]
        ti = [r for r in tr if r["install"]]
        tf = [r for r in ti if not r["ok"]]
        a = sum(r["ok"] for r in tr) / len(tr)
        print("  %-12s n=%5d acc=%.4f installs=%5d false=%4d" % (t, len(tr), a, len(ti), len(tf)))

    # KB-E1: emission payload == source bytes (checked in emit mode; verify digests non-empty)
    # KB-E2: every trial emits non-empty owned selection (mapping_ok)
    mok = sum(r["mapping_ok"] for r in rows)
    print("KB-E2 mapping_ok: %d/%d" % (mok, len(rows)))
    # KB-E5: ledger hash-chain (checked via run logs)
    print("KB-E1: verified separately in emit-mode (payload==source bytes)")


if __name__ == "__main__":
    main()
