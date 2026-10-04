#!/usr/bin/env python3
"""Debate-trial transport (NOT TNN-side): assembles frozen evidence into the
Zag decision program's input format, runs the Zag pipeline (opine/rubric),
and maintains the hash-chained ledger via debate_bin chain/verify.

All decisions are the Zag program's. This script only moves bytes.
"""
import hashlib
import json
import os
import subprocess
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab/senses/web-search/debate-trial")
SRC = os.path.join(LAB, "src")
BIN = os.path.join(SRC, "debate_bin")
EVDIR = os.path.join(LAB, "evidence")
LEDGER = os.path.join(LAB, "ledger", "debate.htsv")

STANCE_MAP = {"SUPPORTS": 1, "REFUTES": 0, "NEUTRAL": 2}
SOURCE_MAP = {"web": 1, "helper": 2, "debate": 3}
CLAIMS = ["D1", "D2", "D3", "D4", "D5"]


def run_bin(*args):
    r = subprocess.run([BIN, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"debate_bin {' '.join(args)} failed: {r.stderr[:500]}")
    return r.stdout


def load_envelopes(claim):
    path = os.path.join(EVDIR, claim, "envelopes.jsonl")
    recs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            recs.append(json.loads(line))
    return recs


def assemble_phase1(out_path):
    """envelopes.jsonl -> phase1.tsv (ev_id claim source stance)."""
    n = 0
    with open(out_path, "w") as out:
        out.write("# debate-trial phase1 evidence v1\n")
        for claim in CLAIMS:
            for e in load_envelopes(claim):
                if e.get("source", "web") == "debate":
                    continue
                ev = e["ev_id"].replace(" ", "_")
                src = SOURCE_MAP[e.get("source", "web")]
                st = STANCE_MAP[e["stance"]]
                out.write(f"{ev} {claim} {src} {st}\n")
                n += 1
    return n


def assemble_debate(out_path):
    """Admitted debate evidence -> debate.tsv. Starts as header-only."""
    n = 0
    with open(out_path, "w") as out:
        out.write("# debate-trial admitted debate evidence v1\n")
        apath = os.path.join(EVDIR, "admitted_debate.jsonl")
        if os.path.exists(apath):
            with open(apath) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    e = json.loads(line)
                    ev = e["ev_id"].replace(" ", "_")
                    out.write(f"{ev} {e['claim_id']} 3 {STANCE_MAP[e['stance']]}\n")
                    n += 1
    return n


def opine_x3(ev_path):
    outs = [run_bin("opine", ev_path) for _ in range(3)]
    if not (outs[0] == outs[1] == outs[2]):
        raise RuntimeError("opine reruns NOT byte-identical")
    return outs[0]


def rubric_x3(p1, db):
    outs = [run_bin("rubric", p1, db) for _ in range(3)]
    if not (outs[0] == outs[1] == outs[2]):
        raise RuntimeError("rubric reruns NOT byte-identical")
    return outs[0]


# ---- ledger ----

def ledger_prev():
    if not os.path.exists(LEDGER):
        return "00" * 32, 0
    last_new, seq = None, -1
    with open(LEDGER) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#") or not line.startswith("EVT\t"):
                continue
            parts = line.split("\t")
            seq = int(parts[1])
            last_new = parts[3]
    if last_new is None:
        return "00" * 32, 0
    return last_new, seq + 1


def ledger_append(op, payload):
    """Append one EVT line. payload must contain no tabs/newlines."""
    assert "\t" not in payload and "\n" not in payload, "payload must be tab/newline-free"
    prev, seq = ledger_prev()
    tmp = "/home/hatch/workspace/tmp_commit/debate_payload.bin"
    with open(tmp, "wb") as f:
        f.write(payload.encode())
    new = run_bin("chain", prev, tmp).strip()
    line = f"EVT\t{seq}\t{prev}\t{new}\t{op}\t{payload}\n"
    with open(LEDGER, "a") as f:
        f.write(line)
    return seq, new


def ledger_verify():
    out = run_bin("verify", LEDGER)
    print(out.strip())
    if not out.startswith("VERIFY OK"):
        raise RuntimeError("ledger verify failed")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "assemble":
        n1 = assemble_phase1(os.path.join(EVDIR, "phase1.tsv"))
        n2 = assemble_debate(os.path.join(EVDIR, "debate.tsv"))
        print(f"phase1.tsv: {n1} records; debate.tsv: {n2} records")
    elif cmd == "opine":
        out = opine_x3(os.path.join(EVDIR, "phase1.tsv"))
        print(out, end="")
    elif cmd == "rubric":
        out = rubric_x3(os.path.join(EVDIR, "phase1.tsv"),
                        os.path.join(EVDIR, "debate.tsv"))
        print(out, end="")
    elif cmd == "verify":
        ledger_verify()
    else:
        sys.exit(f"unknown cmd {cmd}")
