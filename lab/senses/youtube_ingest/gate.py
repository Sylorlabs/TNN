#!/usr/bin/env python3
"""gate.py — verdict-aware install/withhold gate (READINESS.md is the authority).

Usage: gate.py [percepts.jsonl] [gate_log.jsonl] [--counterfactual-ready]

Pipeline per window (stream order):
  percept (perceive.py: six sub-judgments + gate.zag ALL verdict)
    -> gate decision (CANDIDATE | WITHHOLD+reason)
    -> if CANDIDATE: shared memory rule (vendored verbatim from the KB4 trial's
       score_gates.py): INSTALL iff no installed contradictory judgment with
       confidence >= exists; else WITHHOLD (memory rule) + blocked_by detail.
    -> verdict layer (READINESS.md):
         READY    -> INSTALL intent (logged; no real-memory wiring in this task)
         GATED    -> PARKED: the gate spec's install criteria may pass, but the
                     verdict is GATED so nothing enters memory; the would-be
                     install is logged as an install-intent with its reason.
         NOT READY / missing / unparsable -> WITHHOLD everything.

Decisions: INSTALL-INTENT | PARKED | WITHHOLD. Every record carries a concrete
reason. No real memory is touched under any verdict in this scaffold.

--counterfactual-ready: evaluate the gate as if verdict were READY (used for
the YT1 held-out probe: adversarial false-install rate of the gate itself).

Deterministic: file + record inputs only. No RNG, no clock.
"""
import json, os, sys

WORK = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
LOOKUP = [
    os.path.join(WORK, "READINESS.md"),
    os.path.join(HOME, "workspace", "tnn-lab", "senses", "readiness", "READINESS.md"),
    os.path.join(HOME, "workspace", "tnn-lab", "senses", "kb4", "READINESS.md"),
]

def readiness_verdict():
    for path in LOOKUP:
        if not os.path.exists(path):
            continue
        verdict = None
        with open(path) as f:
            for raw in f:
                s = raw.strip()
                if s.startswith("## Verdict:"):
                    verdict = s.split("## Verdict:", 1)[1].strip().upper()
                    break
        src = "READINESS.md %s" % path
        if verdict == "READY":
            return "READY", src + " verdict=READY"
        if verdict == "GATED":
            return "GATED", src + " verdict=GATED"
        return "NOTREADY", src + " verdict=%r (not READY/GATED)" % verdict
    return "NOTREADY", "no READINESS.md in %d lookup paths" % len(LOOKUP)

# vendored verbatim from code/scripts/score_gates.py (shared round-1 rule);
# truth may be None (real video): false_install then recorded as None.
def apply_memory_rule(installed, judgment, confidence, truth, fixture):
    for (j, c, _fx) in installed:
        if j != judgment and c >= confidence:
            return ("WITHHOLD",
                    {"fixture": fixture, "judgment": judgment,
                     "confidence": confidence,
                     "blocked_by": {"judgment": j, "confidence": c}})
    installed.append((judgment, confidence, fixture))
    false_install = (judgment != truth) if truth is not None else None
    return ("INSTALL", {"fixture": fixture, "judgment": judgment,
                        "confidence": confidence, "truth": truth,
                        "false_install": false_install})

def main():
    percepts = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "percepts.jsonl")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(WORK, "gate_log.jsonl")
    counterfactual = "--counterfactual-ready" in sys.argv
    status, reason = readiness_verdict()
    eff = "READY" if counterfactual else status
    installed = []
    counts = {"INSTALL-INTENT": 0, "PARKED": 0, "WITHHOLD": 0}
    false_installs = 0
    n_adv = 0
    with open(percepts) as fi, open(out, "w") as fo:
        for line in fi:
            line = line.strip()
            if not line:
                continue
            p = json.loads(line)
            fx = "%s#%d" % (p["video_id"], p["window_idx"])
            truth = p.get("truth")  # present only for probe fixtures
            g = p["gate"]
            if g["decision"] != "CANDIDATE":
                decision, why = "WITHHOLD", "gate " + g["reason"]
                det = {}
            elif eff == "NOTREADY":
                decision, why = "WITHHOLD", "verdict NOT READY (%s)" % reason
                det = {}
            else:
                dec2, det = apply_memory_rule(installed, g["judgment"],
                                              g["confidence"], truth, fx)
                if dec2 == "WITHHOLD":
                    decision, why = "WITHHOLD", "memory rule: blocked_by " + json.dumps(det["blocked_by"], sort_keys=True)
                elif eff == "READY":
                    decision, why = "INSTALL-INTENT", "G-ALL passed, memory rule passed (intent only; no real-memory wiring in this scaffold)"
                else:
                    decision, why = "PARKED", "G-ALL passed, memory rule passed, but READINESS verdict=GATED: nothing enters memory"
            counts[decision] += 1
            if decision in ("INSTALL-INTENT",) and det.get("false_install"):
                false_installs += 1
            if truth is not None:
                n_adv += 1 if p.get("class") == "adversarial" else 0
            fo.write(json.dumps({
                "video_id": p["video_id"], "window_idx": p["window_idx"],
                "gate_judgment": g["judgment"], "gate_confidence": g["confidence"],
                "gate_reason": g["reason"], "decision": decision, "reason": why,
                "detail": det,
            }, sort_keys=True) + "\n")
    total = sum(counts.values())
    print("verdict: %s (%s)%s" % (status, reason,
                                  " [COUNTERFACTUAL READY]" if counterfactual else ""))
    print("decisions: %s (total %d)" % (json.dumps(counts, sort_keys=True), total))
    if n_adv:
        print("probe: adversarial fixtures=%d, false installs=%d" % (n_adv, false_installs))
    print("-> %s" % out)

if __name__ == "__main__":
    sys.exit(main())
