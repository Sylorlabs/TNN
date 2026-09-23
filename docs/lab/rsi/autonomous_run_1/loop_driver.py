#!/usr/bin/env python3
"""Autonomous RSI Run 1 — the loop driver (hands only; all decisions are Zag).

Reads state.json, invokes the TNN deliberation (proposer.zag), executes what
it proposes (subject.zag prop mode), scores with the frozen verifier
(verify_prop.py), applies keep/discard per RUN_PREREG.md, commits each round,
and halts on TNN's HALT or the 1-hour clock. Zero steering: the driver never
invents a candidate, a prediction, or a decision.
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
STATE = os.path.join(WORK, "state.json")
CKPT = os.path.join(WORK, "checkpoints.log")
SUBJ = os.path.join(WORK, "subject")
PROP = os.path.join(WORK, "proposer")
VERIFY = os.path.join(HERE, "verify_prop.py")
BATCSV = os.path.join(HERE, "battery_r4c.csv")
SUBJSRC = os.path.join(WORK, "subject.zag")
CLOCK = 3600

def log(msg):
    line = f"[t+{int(time.time()-T0)}s] {msg}"
    print(line, flush=True)
    with open(CKPT, "a") as f:
        f.write(line + "\n")

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r

def slots(names):
    out = []
    for c in ("c1", "c2", "c3", "c4", "c5"):
        out.append(c if c in names else "-")
    return out

def load_state():
    with open(STATE) as f:
        return json.load(f)

def save_state(s):
    with open(STATE, "w") as f:
        json.dump(s, f, indent=1)

def parse_prop(out):
    d = {}
    for line in out.splitlines():
        if line.startswith("PROP_DECISION,"):
            kv = dict(p.split("=", 1) for p in line.split(",")[1:])
            d["decision"] = kv.get("decision")
            d.update(kv)
        elif line.startswith("PROP_CAND,"):
            kv = dict(p.split("=", 1) for p in line.split(",")[1:])
            d["cand"] = kv.get("cand"); d["track"] = kv.get("track")
        elif line.startswith("PROP_PRED,"):
            kv = dict(p.split("=", 1) for p in line.split(",")[1:])
            d["pd_a"] = int(kv["dacc"]); d["pd_w"] = int(kv["dwrong"]); d["pd_c"] = int(kv["cost"])
        elif line.startswith("PROP_RUN,"):
            kv = dict(p.split("=", 1) for p in line.split(",")[1:])
            d["extra"] = kv.get("extra")
    return d

def commit_round(paths, message):
    with open(os.path.join(WORK, "commit_msg.txt"), "w") as f:
        f.write(message + "\n")
    r = run(["python3", os.path.expanduser("~/workspace/commit_racefree.py"),
             "tnn-native-lab", os.path.join(WORK, "commit_msg.txt")] + paths,
            cwd=os.path.expanduser("~/workspace/tnn-lab"),
            env={**os.environ, "TMPDIR": os.path.expanduser("~/workspace/tmp_commit")})
    if r.returncode != 0 or "COMMIT" not in r.stdout:
        log("COMMIT-WARN: " + (r.stdout + r.stderr)[-500:])
    else:
        log("COMMIT: " + r.stdout.strip().splitlines()[-1])

    print("FINAL-STATE:", json.dumps(st))
T0 = time.time()
st = load_state()
rnd = len(st["rounds"])
log(f"LOOP START. champion={st['champion']} kept={st['kept']} "
    f"intuition={st['hits']}/{st['total']}")

while True:
    el = time.time() - T0
    if el > CLOCK:
        log("HALT: 1-hour clock expired")
        st["halt"] = "timeout"; break

    argv = (slots(st["kept"]) + slots(st["tried"]) + slots(st["retired"]) +
            [f"b{st['barren']}", f"web{st['web']}"])
    outs = {run([PROP] + argv).stdout for _ in range(3)}
    if len(outs) != 1:
        log("FATAL: proposer non-deterministic"); st["halt"] = "nondeterministic"; break
    p = parse_prop(next(iter(outs)))
    dec = p.get("decision")
    log(f"ROUND {rnd}: deliberation -> {dec} " +
        (f"cand={p.get('cand')} track={p.get('track')} "
         f"pred(dacc={p.get('pd_a')},dwrong={p.get('pd_w')},cost={p.get('pd_c')})"
         if dec == "PROPOSE" else f"info={p}"))

    if dec == "HALT":
        st["halt"] = p.get("reason", "tnn-declared"); log(f"HALT: {st['halt']}"); break

    if dec == "BARREN":
        st["barren"] += 1
        log(f"BARREN round accepted (barren=b{st['barren']})")
        save_state(st)
        commit_round(["rsi/autonomous_run_1/work/state.json",
                      "rsi/autonomous_run_1/work/checkpoints.log"],
                     f"autonomous run 1 round {rnd}: BARREN (b{st['barren']})")
        rnd += 1; continue

    if dec == "WEBQUERY":
        # The deliberation identified a knowledge gap. The driver cannot browse;
        # it pauses so the operator performs the single targeted search, then
        # resumes with web=1 (V3 thin-win gate waived per prereg, all else held).
        log("WEBQUERY emitted — pausing for operator search")
        qf = os.path.join(WORK, f"webquery_{rnd}.md")
        with open(qf, "w") as f:
            f.write("# WEBQUERY round %d\n\nQuestion (from TNN deliberation): do thin-margin "
                    "proxy wins (+1 acc on 24 items, <2 improved items) transfer to the "
                    "real battery?\n\nStatus: PENDING operator search.\n" % rnd)
        st["halt"] = "webquery-pending"
        save_state(st)
        commit_round([f"rsi/autonomous_run_1/work/webquery_{rnd}.md",
                      "rsi/autonomous_run_1/work/state.json",
                      "rsi/autonomous_run_1/work/checkpoints.log"],
                     f"autonomous run 1: webquery round {rnd} — paused for operator search")
        print("WEBQUERY-PENDING")
        break

    if dec != "PROPOSE":
        log(f"FATAL: unknown decision {dec}"); st["halt"] = "bad-decision"; break

    # ---- execute the proposal exactly as emitted ----
    cand, track = p["cand"], p["track"]
    tag = f"prop_{cand}"
    rdir = os.path.join(WORK, f"round{rnd}_{tag}")
    os.makedirs(rdir, exist_ok=True)
    sub_argv = [SUBJ, "prop", cand] + slots(st["kept"]) + ["x"]
    for rep in range(5):
        r = run(sub_argv, cwd=WORK)
        with open(os.path.join(rdir, f"{tag}_{rep}.log"), "w") as f:
            f.write(r.stdout)
    ch = st["champion"]
    v = run([sys.executable, VERIFY, rdir, BATCSV, tag,
             str(ch["acc"]), str(ch["wrong"]), str(ch["cost"]),
             str(p["pd_a"]), str(p["pd_w"]), str(p["pd_c"]), SUBJSRC])
    vout = v.stdout + v.stderr
    m = re.search(r"SCORES: acc=(\d+)/24 wrong=(\d+)/24 cost=(\d+)", vout)
    meas = {"acc": int(m.group(1)), "wrong": int(m.group(2)), "cost": int(m.group(3))} if m else None
    noreg = "NO-DEGRADATION: PASS" in vout
    hit = (v.returncode == 0)
    st["total"] += 1
    if hit:
        st["hits"] += 1

    rec = {"round": rnd, "cand": cand, "track": track,
           "pred": {"dacc": p["pd_a"], "dwrong": p["pd_w"], "cost": p["pd_c"]},
           "measured": meas, "verdict": ("HIT" if hit else "MISS") if v.returncode != 2 else "BAR-FAIL",
           "noreg": noreg, "log": vout[-1500:]}
    if v.returncode == 2:
        # constitution/metric bar failed on real items: retire + halt per prereg
        rec["disposition"] = "RETIRED+HALT"
        st["retired"].append(cand); st["tried"].append(cand)
        st["rounds"].append(rec); st["halt"] = f"g4-violation-{cand}"
        log(f"ROUND {rnd}: BAR-FAIL -> {cand} RETIRED, loop HALTED for red-team review")
        save_state(st)
        commit_round([f"rsi/autonomous_run_1/work/round{rnd}_{tag}/{tag}_{i}.log" for i in range(5)] +
                     ["rsi/autonomous_run_1/work/state.json"],
                     f"autonomous run 1 round {rnd}: {cand} BAR-FAIL, retired, halt")
        break

    keep = False
    if hit and noreg:
        keep = True
    rec["disposition"] = "KEPT" if keep else "DISCARDED"
    st["tried"].append(cand)
    if keep:
        st["kept"].append(cand)
        st["champion"] = meas
        log(f"ROUND {rnd}: {cand} ({track}) HIT, no degradation -> KEPT. "
            f"champion now {meas}. intuition {st['hits']}/{st['total']}")
    else:
        log(f"ROUND {rnd}: {cand} ({track}) {rec['verdict']} -> DISCARDED. "
            f"champion unchanged {st['champion']}. intuition {st['hits']}/{st['total']}")
    st["rounds"].append(rec)
    save_state(st)
    commit_round([f"rsi/autonomous_run_1/work/round{rnd}_{tag}/{tag}_{i}.log" for i in range(5)] +
                 ["rsi/autonomous_run_1/work/state.json"],
                 f"autonomous run 1 round {rnd}: {cand} {rec['verdict']} -> {rec['disposition']}")
    rnd += 1

save_state(st)
log(f"LOOP END. halt={st.get('halt')} kept={st['kept']} champion={st['champion']} "
    f"intuition={st['hits']}/{st['total']}")
commit_round(["rsi/autonomous_run_1/work/state.json",
              "rsi/autonomous_run_1/work/checkpoints.log"],
             f"autonomous run 1: loop end ({st.get('halt')})")
print("FINAL-STATE:", json.dumps(st))
