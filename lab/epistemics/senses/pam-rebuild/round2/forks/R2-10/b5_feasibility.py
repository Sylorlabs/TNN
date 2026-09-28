#!/usr/bin/env python3
"""B5 feasibility: can ANY gate on available signals reach <=3% false installs?
Truth oracle, full run1 data. Tests progressively richer gate spaces.
"""
import os

R2 = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10")
FX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures")
BAT = os.path.join(R2, "evidence", "battery")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TID = {t: i for i, t in enumerate(TASKS)}

rows = []  # (task, conf, margin, feat0, feat1, mok, ok)
for task in TASKS:
    p = os.path.join(BAT, "noemit_%s_run1.tsv" % task)
    if not os.path.exists(p):
        print("missing", p)
        continue
    for line in open(p):
        f = line.rstrip("\n").split("\t")
        if len(f) < 11 or f[0].startswith("BATCH_ERROR"):
            continue
        fid = f[0]
        conf, margin, mok = int(f[2]), int(f[3]), int(f[5])
        feat0, feat1 = int(f[8]), int(f[9])
        truth = open(os.path.join(FX, fid + ".truth")).read().strip().split("=", 1)[1]
        ok = 1 if f[1] == truth else 0
        rows.append((TID[task], conf, margin, feat0, feat1, mok, ok))
print("rows:", len(rows))


def evaluate(theta, veto):
    """theta: int or dict task->int. veto: 0..7 (4..7 add task-conditional)."""
    fi = ir = irc = 0
    for task, conf, margin, feat0, feat1, mok, ok in rows:
        th = theta[task] if isinstance(theta, dict) else theta
        v = 0
        if veto in (1, 3) and feat0 != 0:
            v = 1
        if veto in (2, 3) and margin < 100:
            v = 1
        # task-conditional vetoes (adversarial-family signals)
        if veto >= 4:
            if task == 3 and feat1 != 0:
                v = 1  # pitchdisc glide -> veto
            if task == 5 and feat0 != 0:
                v = 1  # motiondir reversal -> veto
            if task == 2 and feat0 != 0:
                v = 1  # shapetrans occlusion bar -> veto
            if veto in (5, 7) and margin < 100:
                v = 1
            if veto in (6, 7) and feat0 != 0:
                v = 1
        if mok == 1 and conf >= th and v == 0:
            ir += 1
            if ok:
                irc += 1
            else:
                fi += 1
    return fi, ir, irc


def report(name, theta, veto):
    fi, ir, irc = evaluate(theta, veto)
    rate = fi / len(rows) * 100
    print("%-45s fi=%4d ir=%5d irc=%5d rate=%6.3f%% %s" %
          (name, fi, ir, irc, rate, "PASS" if rate <= 3 else "FAIL"))

# Space 1: global theta, veto 0-3 (current design)
print("--- Space 1: global theta, veto 0-3 ---")
best = None
for th in range(500, 1000, 25):
    for vi in range(4):
        fi, ir, irc = evaluate(th, vi)
        if best is None or fi < best[0] or (fi == best[0] and irc > best[2]):
            best = (fi, ir, irc, th, vi)
report("best global (th=%d, veto=%d)" % (best[3], best[4]), best[3], best[4])

# Space 2: global theta, task-conditional vetoes
print("--- Space 2: global theta + task-conditional vetoes ---")
best = None
for th in range(500, 1000, 25):
    for vi in (4, 5, 6, 7):
        fi, ir, irc = evaluate(th, vi)
        if best is None or fi < best[0] or (fi == best[0] and irc > best[2]):
            best = (fi, ir, irc, th, vi)
report("best global+cond (th=%d, veto=%d)" % (best[3], best[4]), best[3], best[4])

# Space 3: per-task theta, veto 0 (upper bound on what thresholds alone can do)
print("--- Space 3: per-task theta (greedy) ---")
# greedy per-task: for each task, pick theta minimizing fi, tie-break max irc
pt = {}
for t in range(6):
    trows = [r for r in rows if r[0] == t]
    bt = None
    for th in range(0, 1000, 25):
        fi = sum(1 for _, c, _, _, _, m, ok in trows if m == 1 and c >= th and not ok)
        irc = sum(1 for _, c, _, _, _, m, ok in trows if m == 1 and c >= th and ok)
        if bt is None or fi < bt[0] or (fi == bt[0] and irc > bt[2]):
            bt = (fi, irc, th)
    pt[t] = bt[2]
    print("  task %s: theta=%d fi=%d irc=%d n=%d" % (TASKS[t], bt[2], bt[0], bt[1], len(trows)))
report("per-task theta, veto=0", pt, 0)
