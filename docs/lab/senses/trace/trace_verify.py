#!/usr/bin/env python3
"""trace_verify.py — verifier for SENSE-TRACE v1 logs.

Checks:
  1. Grammar: version line, RUN, STAGE lines, HELD, END.
  2. RUN src == STAGE 0 out.
  3. Provenance closure: every non-fork stage's `in` equals the RUN src or
     some earlier stage's `out`. Fork stages must declare fork_of=<earlier
     stage>; their `in` is the checksum of the declared slice (recorded, and
     reproducible by rerunning the traced driver).
  4. HELD sha == last STAGE out, HELD len == last out_len.
  5. END rc=0.
  6. Optional goldens file (lines `name=sha`): any stage whose full name
     matches a golden key must have out == golden sha.

Usage:
  trace_verify.py <trace.log> [--goldens goldens.txt]

Exit 0 PASS, 1 FAIL (first failure printed).
"""

import re
import sys

STAGE_RE = re.compile(
    r"^STAGE (\d+) (\S+) in=(\S+) out=(\S+) in_len=(\d+) out_len=(\d+) params=(.*)$")
RUN_RE = re.compile(r"^RUN sense=(\S+) format=(\S+) src=(\S+) params=(.*)$")
HELD_RE = re.compile(r"^HELD sha=(\S+) len=(\d+) desc=(\S+)$")
END_RE = re.compile(r"^END rc=(-?\d+)$")


def fail(msg):
    print("FAIL:", msg)
    return 1


def main():
    path = sys.argv[1]
    goldens = {}
    if "--goldens" in sys.argv:
        gf = sys.argv[sys.argv.index("--goldens") + 1]
        for line in open(gf, encoding="utf-8"):
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                goldens[k.strip()] = v.strip().lower()
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8")]
    if not lines or lines[0] != "# SENSE-TRACE v1":
        return fail("missing/invalid version line")
    run = None
    stages = []
    held = None
    end = None
    for ln in lines[1:]:
        if not ln:
            continue
        m = RUN_RE.match(ln)
        if m:
            run = m.groups()
            continue
        m = STAGE_RE.match(ln)
        if m:
            stages.append(m.groups())
            continue
        m = HELD_RE.match(ln)
        if m:
            held = m.groups()
            continue
        m = END_RE.match(ln)
        if m:
            end = m.groups()
            continue
        return fail("unparseable line: %r" % ln[:80])
    if run is None:
        return fail("no RUN line")
    if not stages:
        return fail("no STAGE lines")
    if held is None:
        return fail("no HELD line")
    if end is None:
        return fail("no END line")
    sense, fmt, src, rparams = run
    if end[0] != "0":
        return fail("END rc=%s (nonzero)" % end[0])
    # seq numbers strictly increasing from 0
    for i, s in enumerate(stages):
        if int(s[0]) != i:
            return fail("stage seq out of order at index %d (got %s)" % (i, s[0]))
    # RUN src == STAGE 0 out
    if stages[0][3].lower() != src.lower():
        return fail("RUN src != STAGE 0 out")
    # provenance closure
    known = {src.lower(): "RUN.src"}
    for s in stages:
        seq, name, ih, oh, ilen, olen, params = s
        ih, oh = ih.lower(), oh.lower()
        is_fork = "fork_of=" in params
        if ih == "-":
            if int(seq) != 0:
                return fail("STAGE %s: in=- only allowed for stage 0" % seq)
        elif is_fork:
            m = re.search(r"fork_of=([^,]+)", params)
            if not m:
                return fail("STAGE %s: fork without fork_of target" % seq)
            target = m.group(1)
            targets = [t[1] for t in stages[:int(seq)]]
            if target not in targets:
                return fail("STAGE %s: fork_of=%s not an earlier stage" % (seq, target))
        elif ih not in known:
            return fail("STAGE %s %s: in=%s... not produced by any earlier stage"
                        % (seq, name, ih[:16]))
        known[oh] = name
        # golden check
        if name in goldens and oh != goldens[name]:
            return fail("STAGE %s %s: out=%s... != golden %s..."
                        % (seq, name, oh[:16], goldens[name][:16]))
    # HELD binding
    last = stages[-1]
    if held[0].lower() != last[3].lower():
        return fail("HELD sha != last STAGE out")
    if int(held[1]) != int(last[5]):
        return fail("HELD len != last STAGE out_len")
    if "held" in goldens and held[0].lower() != goldens["held"]:
        return fail("HELD sha != golden held")
    print("PASS: %s (%d stages, sense=%s format=%s)" % (path, len(stages), sense, fmt))
    print("  provenance closure ok; HELD=%s...%s" % (held[0][:16], held[0][-8:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
