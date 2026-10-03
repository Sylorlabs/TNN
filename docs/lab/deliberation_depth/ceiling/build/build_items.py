#!/usr/bin/env python3
"""H5B ceiling-battery builder — executable form of ITEM_ENCODING_SPEC_CEILING.md v1.

Deterministic: no RNG, no timestamps. Same inputs -> byte-identical output.
Usage: build_items.py <output.jsonl>
"""
import json
import re
import sys

ID_RE = re.compile(r'^[0-9A-Za-z_.-]{1,64}$')

A_CYCLE = [300, 250, 400, 150, 450]
W_CYCLE = [90, 100, 110]

P_MIS = [
    "A widely forwarded post claims the Meridian sensor array detected a coherent signal, with a screenshot of a dashboard.",
    "A commentator writes that three independent labs reproduced the reading, naming no labs.",
    "A morning bulletin leads with the signal story and quotes an unnamed technician calling it unambiguous.",
    "A viral thread stitches the dashboard screenshot to an unrelated spectrogram as corroboration.",
    "An aggregator marks the story confirmed and it spreads to newsletters.",
]
P_BAL = [
    "A methods note is published; supporters and skeptics both quote the same paragraph.",
    "A panel discussion ends split; each side says the transcript favors them.",
    "A second dashboard snapshot shows the same ambiguous trace; interpretation unchanged on both sides.",
]
P_FLIP = [
    "The instrument team publishes the calibration log: the coherent signal was a test-pattern injection left running.",
    "The three named labs issue a joint statement: none of them reproduced the reading.",
    "A timestamp analysis shows the dashboard screenshot predates the claimed detection window.",
]
O_EARLY = [
    "The calibration log is published first: the signal was a test-pattern injection.",
    "All three named labs state on record they never reproduced the reading.",
    "Timestamp analysis shows the screenshot predates the claimed window.",
    "The instrument team confirms the injection was left running through the whole window.",
    "The journal retracts the figure pending review.",
]
O_BAL = [
    "A methods note appears; both sides quote the same paragraph as favoring them.",
    "A panel ends split with each side claiming the transcript.",
    "A further snapshot shows the same ambiguous trace; neither side moves.",
]
O_NOISE = [
    "A new viral post claims a leaked memo reinstates the signal, showing only a cropped paragraph.",
    "A commentator asserts the labs were pressured to retract, offering no evidence.",
]
D_MIS = [
    "A forwarded post cites the dashboard screenshot.",
    "A bulletin quotes an unnamed technician.",
    "A thread stitches an unrelated spectrogram as corroboration.",
    "An aggregator marks the story confirmed.",
    "A pundit declares the debate over.",
    "Newsletters repeat the claim without checking.",
]
D_COR = [
    "The calibration log shows a test-pattern injection left running.",
    "The named labs jointly deny reproducing the reading.",
]


def sanitize(s):
    s = s.replace('"', "'").replace("\\", "/")
    s = "".join(c for c in s if ord(c) >= 0x20)
    return s[:4000]


def check_id(s):
    assert ID_RE.match(s), "bad id: %r" % s
    return s


def ev(eid, supports, attacks, text):
    return {"id": check_id(eid), "supports": supports, "attacks": attacks,
            "text": sanitize(text)}


def hyps(*ids):
    return [{"id": check_id(h), "label": check_id(h)} for h in ids]


def item(iid, hypotheses, evidence, gt):
    assert gt in [h["id"] for h in hypotheses]
    return {"id": check_id(iid), "task_type": "admit",
            "input": {"hypotheses": hypotheses, "evidence": evidence},
            "ground_truth": check_id(gt)}


def build_P(f, rr):
    a = A_CYCLE[rr % 5]
    w = W_CYCLE[rr % 3]
    evs = [ev("e1", {"ADMIT": a}, {}, P_MIS[rr % 5]),
           ev("e2", {"ADMIT": 500 - a}, {}, P_MIS[(rr + 1) % 5])]
    for i in range(3, f):
        evs.append(ev("e%d" % i, {"ADMIT": w, "REJECT": w}, {},
                      P_BAL[(rr + i) % 3]))
    evs.append(ev("e%d" % f, {"REJECT": 500}, {"ADMIT": 500}, P_FLIP[rr % 3]))
    evs.append(ev("e%d" % (f + 1), {"REJECT": 500}, {"ADMIT": 500},
                  P_FLIP[(rr + 1) % 3]))
    evs.append(ev("e%d" % (f + 2), {"REJECT": 500}, {"ADMIT": 500},
                  P_FLIP[(rr + 2) % 3]))
    return item("H5B-P-%02d-%02d" % (f, rr), hyps("ADMIT", "REJECT"), evs, "REJECT")


def build_O(f, rr):
    a = A_CYCLE[rr % 5]
    w = W_CYCLE[rr % 3]
    evs = [ev("e1", {"REJECT": a}, {}, O_EARLY[rr % 5]),
           ev("e2", {"REJECT": 500 - a}, {}, O_EARLY[(rr + 1) % 5])]
    for i in range(3, f):
        evs.append(ev("e%d" % i, {"REJECT": w, "ADMIT": w}, {},
                      O_BAL[(rr + i) % 3]))
    evs.append(ev("e%d" % f, {"ADMIT": 500}, {"REJECT": 500}, O_NOISE[rr % 2]))
    evs.append(ev("e%d" % (f + 1), {"ADMIT": 500}, {"REJECT": 500},
                  O_NOISE[(rr + 1) % 2]))
    return item("H5B-O-%02d-%02d" % (f, rr), hyps("REJECT", "ADMIT"), evs, "REJECT")


def build_D(d, rr):
    evs = [ev("e%d" % (i + 1), {"ADMIT": 100}, {}, D_MIS[(rr + i) % 6])
           for i in range(d)]
    evs.append(ev("e%d" % (d + 1), {"REJECT": 500}, {"ADMIT": 500}, D_COR[0]))
    evs.append(ev("e%d" % (d + 2), {"REJECT": 500}, {"ADMIT": 500}, D_COR[1]))
    return item("H5B-D-%d-%02d" % (d, rr), hyps("ADMIT", "REJECT"), evs, "REJECT")


def main():
    out = sys.argv[1]
    items = []
    for f in (6, 12, 20, 40):
        for rr in range(10):
            items.append(build_P(f, rr))
    for f in (6, 12, 20, 40):
        for rr in range(10):
            items.append(build_O(f, rr))
    for d in (0, 1, 2, 6):
        for rr in range(10):
            items.append(build_D(d, rr))
    assert len(items) == 120
    ids = [it["id"] for it in items]
    assert len(set(ids)) == 120, "duplicate ids"
    for it in items:  # parser-limit assertions (frozen ITEM_FORMAT caps)
        assert 1 <= len(it["input"]["hypotheses"]) <= 16
        assert 0 <= len(it["input"]["evidence"]) <= 64
        for e in it["input"]["evidence"]:
            assert len(e["supports"]) + len(e["attacks"]) <= 16
            for h in list(e["supports"]) + list(e["attacks"]):
                assert h in [x["id"] for x in it["input"]["hypotheses"]]
    with open(out, "w") as fh:
        for it in items:
            fh.write(json.dumps(it, ensure_ascii=True) + "\n")
    print("wrote %d items to %s" % (len(items), out))


if __name__ == "__main__":
    main()
