#!/usr/bin/env python3
"""Normalizer: EN-arm stdout -> grade.py contract (run.out + run.err).

WHY IT EXISTS (2026-09-26): the EN binary (english_arm.zag) emits everything on
stdout -- prose trace lines (OBSERVATION:/KNOWLEDGE:/INFERENCE:/CONCLUSION:),
then `A <answer>`, then `T <did> <turn> PASS|FAIL` per turn; only a wall-clock
timing line goes to stderr. grade.py's contract (frozen in PREREG.md) requires:
  - stdout (run.out): per-turn `T <did> <turn> PASS|FAIL` + `A <answer>` lines
  - stderr (run.err): per-turn trace blocks, each opening with exactly one
    `TR turn=<turn> ut=<utype>` line, followed by `TR <trace text>` lines.

Usage: normalize_en.py <en-stdout> <run.out> <run.err> <battery.txt>
NOTE: utype is taken from the frozen battery's DIALOGUE type token
(mechanical convention, documented below); the EN arm never emits a type.

This script performs ONLY that mechanical split. It does not edit, reorder, or
reword any answer or trace text; every emitted byte comes verbatim from the EN
binary's stdout. It does NOT change grade.py's scoring semantics.

Handled lines (EN stdout vocabulary, from traces_run2.txt):
  - `DIALOGUE <did> <type>` : sets current did + utype (mapping below); not emitted.
  - `TURN <did> <n>`        : opens a new trace block; not emitted.
  - `U <question>`          : copied to the trace block as `TR U ...` (context).
  - `OBSERVATION:/KNOWLEDGE:/INFERENCE:/CONCLUSION:` : copied verbatim as `TR <line>`.
  - `A <answer>`            : copied verbatim to run.out.
  - `T <did> <n> PASS|FAIL`: copied verbatim to run.out.
  - `X <expected>`          : EXPECTED-ANSWER ECHO on self-FAIL turns. DELIBERATELY
                              DROPPED: on flip-probe runs the battery E-line is the
                              NEW correct answer, which contains the flipped token --
                              letting it into the trace would pass the faithfulness
                              token check spuriously.
  - `RESULT ...` / `DIGEST ...` : run summaries; dropped.
  - blank lines             : dropped.

utype mapping (cosmetic; grade.py only requires the `TR turn=N ut=` shape):
  TOPIC->0 FOLLOWUP->1 CORRECTION->2 CONTRADICT->3 COMPOSE->4 (default 0).
"""
import re, sys

UT = {"TOPIC": 0, "FOLLOWUP": 1, "CORRECTION": 2, "CONTRADICT": 3, "COMPOSE": 4}

def main():
    src, out_path, err_path, battery_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    # utype comes from the FROZEN battery's DIALOGUE type token (mechanical
    # convention: the EN arm never emits an utterance type; NAT uses ut=0/1/3
    # internally. grade.py only requires the `TR turn=N ut=` shape.)
    ut_of = {}
    did = None
    for raw in open(battery_path):
        line = raw.rstrip("\n")
        if line.startswith("DIALOGUE "):
            parts = line.split()
            did = parts[1]
            ut_of[did] = UT.get(parts[2] if len(parts) > 2 else "", 0)
    out_lines, err_lines = [], []
    cur_block = None          # list for current turn's trace lines
    cur_did = None
    ut = 0
    t_count = a_count = 0
    for raw in open(src):
        line = raw.rstrip("\n")
        if line.startswith("DIALOGUE "):
            cur_did = line.split()[1]
            ut = ut_of.get(cur_did, 0)
            continue
        if line.startswith("TURN "):
            n = line.split()[2]
            cur_block = [f"TR turn={n} ut={ut}"]
            err_lines.append(cur_block)
            continue
        if not line.strip():
            continue
        if line.startswith("A "):
            out_lines.append(line); a_count += 1; continue
        if re.match(r"^(?:NOVEL=1 )?T \S+ \d+ (PASS|FAIL)$", line):
            out_lines.append(line); t_count += 1; continue
        if line.startswith("X ") or line.startswith("RESULT ") or line.startswith("DIGEST ") \
                or line.startswith("ENGLISH-ARM ") or line.startswith("TRAINING ") \
                or line.startswith("KB facts="):
            continue
        # trace prose / U lines
        if cur_block is None:
            raise ValueError(f"trace content before first TURN: {line!r}")
        cur_block.append("TR " + line)
    if t_count != a_count:
        raise ValueError(f"T lines ({t_count}) != A lines ({a_count})")
    if len(err_lines) != t_count:
        raise ValueError(f"trace blocks ({len(err_lines)}) != T lines ({t_count})")
    open(out_path, "w").write("\n".join(out_lines) + "\n")
    with open(err_path, "w") as f:
        for blk in err_lines:
            f.write("\n".join(blk) + "\n")

if __name__ == "__main__":
    main()
