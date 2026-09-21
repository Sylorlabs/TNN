#!/usr/bin/env python3
"""mkdec.py — iterative decision-script authoring for the varA teacher.

The teacher computes every proposal in-teacher from (spec, stimulus, history).
The D lines are the *student side*: scripted student judgments, one per emitted
proposal, in order. The first proposal is emitted with no prior decision (it
starts the dialogue); proposal i (i>=1) is emitted only after D_{i-1} — the
student's judgment on proposal i-1 — is read, logged, and applied. This helper
builds exact-match D lists for a given decision *pattern* by iterating the
teacher binary:

  1. write script with current D prefix
  2. run teacher; read VARA_PROP lines + VARA_END + tape footer verdict
  3. footer "OK"                    -> done (exact match)
     footer "OK:DECISIONS_EXHAUSTED" -> append pattern decisions for the new
                                        proposals and rerun
     footer "OK:PROPOSAL_CAP"        -> fatal (should not happen in tests)

Because proposals are a pure function of the decision prefix, extending the
prefix never changes already-emitted proposals, so the loop converges.

Patterns (deterministic functions of (index, kind, span, conf)):
  adopt_all   - always ADOPT
  mixed       - exercises R1/R2/R5/REVISE/DEFER/ADOPT paths
  hostile_r1  - always REJECT R1 (maximal appeal chains -> R6 exhaustion)
  hostile_r3  - always REJECT R3 (final, no appeal)

Usage: mkdec.py <pattern> <session_id> <stimfile> <out_script>
"""
import os
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "teacher_bin")


def pattern_decide(pattern, i, kind, s, e, conf):
    if kind == 5:  # RETRACT: acknowledge
        return "D %d ADOPT 0" % i
    if pattern == "adopt_all":
        return "D %d ADOPT 0" % i
    if pattern == "hostile_r1":
        return "D %d REJECT 1" % i
    if pattern == "hostile_r3":
        return "D %d REJECT 3" % i
    if pattern == "mixed":
        if i % 7 == 2:
            return "D %d REJECT 1" % i
        if i % 7 == 4:
            if e - s >= 2:
                return "D %d REVISE 1 %d %d" % (i, s, e - 1)
            return "D %d ADOPT 0" % i
        if i % 11 == 5:
            return "D %d DEFER 0" % i
        if i % 13 == 6:
            return "D %d REJECT 5" % i
        if i % 17 == 8:
            return "D %d REJECT 2" % i
        return "D %d ADOPT 0" % i
    raise ValueError("unknown pattern " + pattern)


def tape_footer_verdict(tape_path):
    with open(tape_path, "rb") as f:
        data = f.read()
    # TST-1 framing: [u8 type][u32 le len][payload]; find last event (footer, type 9)
    off = 0
    last = None
    while off + 5 <= len(data):
        etype = data[off]
        plen = struct.unpack_from("<I", data, off + 1)[0]
        payload = data[off + 5:off + 5 + plen]
        if len(payload) != plen:
            break
        last = (etype, payload)
        off += 5 + plen
    if last is None or last[0] != 9:
        return "NOFOOTER"
    p = last[1]
    # ev_footer: u64 0 || 32 chain || u64 count || u32 vlen || verdict
    vlen = struct.unpack_from("<I", p, 8 + 32 + 8)[0]
    return p[8 + 32 + 8 + 4:8 + 32 + 8 + 4 + vlen].decode()


def main():
    pattern, session_id, stimfile, out_script = sys.argv[1:5]
    # stim_len from the GT file's GT1 line
    stim_len = None
    with open(os.path.join(HERE, stimfile)) as f:
        for line in f:
            if line.startswith("GT1 "):
                stim_len = int(line.split()[1])
    assert stim_len, "no GT1 line in stimfile"
    tape = out_script + ".tape"
    d_lines = []
    props = {}  # idx -> (kind, s, e, conf)
    for it in range(300):
        with open(out_script, "w") as f:
            f.write("SESSION %s %d\n" % (session_id, stim_len))
            f.write("STIMFILE %s\n" % stimfile)
            for dl in d_lines:
                f.write(dl + "\n")
            f.write("END\n")
        # tape345's tape_write_file uses O_CREAT|O_EXCL: the tape must not exist
        tpath = os.path.join(HERE, tape)
        if os.path.exists(tpath):
            os.remove(tpath)
        r = subprocess.run([BIN, "teach", out_script, tape],
                           cwd=HERE, capture_output=True, text=True)
        if r.returncode != 0:
            print("TEACHER FAILED rc=%d\n%s\n%s" % (r.returncode, r.stdout, r.stderr))
            sys.exit(1)
        for line in r.stdout.splitlines():
            m = re.match(r"VARA_PROP,(\d+),(\d+),(\d+),(\d+),(\d+)", line)
            if m:
                idx = int(m.group(1))
                props[idx] = tuple(int(x) for x in m.groups()[1:])
        m = re.search(r"VARA_END,proposals=(\d+),consumed=(\d+)", r.stdout)
        n_prop, consumed = int(m.group(1)), int(m.group(2))
        verdict = tape_footer_verdict(os.path.join(HERE, tape))
        print("iter=%d proposals=%d consumed=%d dlines=%d footer=%s" %
              (it, n_prop, consumed, len(d_lines), verdict))
        if verdict == "OK":
            assert consumed == len(d_lines), "OK but dlines mismatch"
            assert n_prop == consumed or (n_prop == 0 and consumed == 0)
            print("MKDEC_DONE,%s,proposals=%d" % (pattern, n_prop))
            return
        if verdict == "OK:DECISIONS_EXHAUSTED":
            # the teacher emitted proposal(s) but has no decision for the last
            # one: append pattern decisions for every undecided proposal.
            assert consumed == len(d_lines) and consumed < n_prop
            for idx in range(consumed, n_prop):
                kind, s, e, conf = props[idx]
                d_lines.append(pattern_decide(pattern, idx, kind, s, e, conf))
            continue
        print("UNEXPECTED footer: " + verdict)
        sys.exit(1)
    print("MKDEC FAIL: no convergence")
    sys.exit(1)


if __name__ == "__main__":
    main()
