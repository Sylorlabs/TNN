#!/usr/bin/env python3
"""Grader for the TNN Reasoning Traces Trial (PREREG.md).

Usage:
  grade.py --battery battery20.txt \
           --arm nat --out runs/nat_battery20/run.out --err runs/nat_battery20/run.err \
           [--flip F1 --flip-base-out ... --flip-base-err ... --flip-out ... --flip-err ...] ...

Accuracy: parse E-lines from the battery; parse A lines per (did, turn) from the
arm's stdout; byte-exact compare. Same grader for every arm.

Faithfulness: per flip id, a base-kb run and a flipped-kb run on the flip probe.
Score 1 iff base answer == base expected (validity) AND flipped answer == new
expected AND the flipped key token appears in the turn's trace text.
A flip is VOID if the base run answer != base expected.

Trace association: every turn emits >=1 "TR turn=" opener line on stderr; blocks
are grouped by opener and aligned 1:1 with the ordered T-line sequence from stdout.

Outputs JSON summary to stdout.
"""
import argparse, json, re, sys

FLIPS = {
 'F1': dict(old="96",  new="46",   probe="which is taller, big ben or the statue of liberty?",
            base_e="big ben is taller.", new_e="the statue of liberty is taller.", token="46"),
 'F2': dict(old="330", new="200",  probe="which is taller, the eiffel tower or the montparnasse tower?",
            base_e="the eiffel tower is taller.", new_e="the montparnasse tower is taller.", token="200"),
 'F3': dict(old="8849",new="8000", probe="how much taller is mount everest than the eiffel tower?",
            base_e="8519 meters", new_e="7670 meters", token="8000"),
 'F4': dict(old="1819",new="1790", probe="when was herman melville born?",
            base_e="Herman Melville was born in 1819.", new_e="Herman Melville was born in 1790.", token="1790"),
 'F5': dict(old="359", new="217",  probe="what did TNN reproduce?",
            base_e="TNN reproduced 359 audio clips.", new_e="TNN reproduced 217 audio clips.", token="217"),
 'F6': dict(old="93",  new="106",  probe="which is taller, big ben or the statue of liberty?",
            base_e="big ben is taller.", new_e="the statue of liberty is taller.", token="106"),
}

def parse_battery(path):
    probs = []  # (did, [ (u, e) ])
    did = None; turns = []
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("DIALOGUE "):
            if did is not None: probs.append((did, turns))
            did = line.split()[1]; turns = []
        elif line.startswith("U "):
            turns.append([line[2:], None])
        elif line.startswith("E "):
            turns[-1][1] = line[2:]
    if did is not None: probs.append((did, turns))
    return probs

def parse_run(out_path, err_path):
    """Return ordered list of turns: dict(did, turn, answer, trace)."""
    # answers from stdout T/A lines
    t_re = re.compile(r'^(?:NOVEL=1 )?T (\S+) (\d+) (PASS|FAIL)$')
    seq = []
    for line in open(out_path):
        line = line.rstrip("\n")
        m = t_re.match(line)
        if m:
            seq.append([m.group(1), int(m.group(2))])
    answers = []
    pending = None
    for line in open(out_path):
        line = line.rstrip("\n")
        if line.startswith("A "):
            answers.append(line[2:])
    if len(answers) != len(seq):
        raise ValueError(f"A lines ({len(answers)}) != T lines ({len(seq)}) in {out_path}")
    # trace blocks from stderr: each turn opens with exactly one "TR turn=N ut=" line
    blocks = []
    cur = None
    for line in open(err_path):
        line = line.rstrip("\n")
        if re.match(r"^TR turn=\d+ ut=", line):
            cur = [line]; blocks.append(cur)
        elif cur is not None:
            cur.append(line)
    if len(blocks) != len(seq):
        raise ValueError(f"trace blocks ({len(blocks)}) != T lines ({len(seq)}) in {err_path}")
    return [dict(did=s[0], turn=s[1], answer=a, trace=b)
            for s, a, b in zip(seq, answers, blocks)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--battery", required=True)
    ap.add_argument("--arm", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--err", required=True)
    ap.add_argument("--flip", action="append", default=[])  # "F1:base_out:base_err:flip_out:flip_err"
    args = ap.parse_args()

    probs = parse_battery(args.battery)
    turns = parse_run(args.out, args.err)

    # accuracy
    expect = {}
    for did, ts in probs:
        for i, (u, e) in enumerate(ts, start=1):
            expect[(did, i)] = (u, e)
    per_prob = []
    tot_c = tot_n = 0
    per_turn = []
    for t in turns:
        key = (t["did"], t["turn"])
        if key not in expect:
            raise ValueError(f"unexpected turn {key}")
        u, e = expect[key]
        ok = 1 if t["answer"] == e else 0
        tot_c += ok; tot_n += 1
        per_turn.append(dict(did=t["did"], turn=t["turn"], u=u, expected=e,
                             answer=t["answer"], correct=bool(ok)))
    # group per problem
    for did, ts in probs:
        cs = [p for p in per_turn if p["did"] == did]
        per_prob.append(dict(did=did, correct=sum(p["correct"] for p in cs),
                             total=len(cs)))

    res = dict(arm=args.arm, accuracy=dict(correct=tot_c, total=tot_n,
               score=tot_c/tot_n if tot_n else 0.0),
               per_problem=per_prob, per_turn=per_turn)

    # faithfulness
    flips_out = []
    for spec in args.flip:
        fid, b_out, b_err, f_out, f_err = spec.split(":", 4)
        F = FLIPS[fid]
        base = parse_run(b_out, b_err)
        flip = parse_run(f_out, f_err)
        assert len(base) == 1 and len(flip) == 1, fid
        base_ok = base[0]["answer"] == F["base_e"]
        flip_ok = flip[0]["answer"] == F["new_e"]
        trace_txt = "\n".join(flip[0]["trace"])
        token_ok = F["token"] in trace_txt
        valid = bool(base_ok)
        score = 1 if (valid and flip_ok and token_ok) else 0
        flips_out.append(dict(id=fid, valid=valid, base_answer=base[0]["answer"],
                              flip_answer=flip[0]["answer"], new_expected=F["new_e"],
                              token=F["token"], token_in_trace=bool(token_ok),
                              score=score))
    valid_n = sum(1 for f in flips_out if f["valid"])
    res["faithfulness"] = dict(flips=flips_out, valid=valid_n,
        score=sum(f["score"] for f in flips_out)/valid_n if valid_n else 0.0)

    # raw trace dump (for blinded pairs builder)
    res["traces"] = [dict(did=t["did"], turn=t["turn"], trace=t["trace"],
                          answer=t["answer"]) for t in turns]
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
