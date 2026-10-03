#!/usr/bin/env python3
"""Frozen CAP filler-claim generator for the pending battery (prereg S8).

Index-derived text only: fully deterministic, no network, no clock reads.
The claim COUNT is derived from the machine's measured MemAvailable so the
presented pending bytes exceed floor(MemAvailable_bytes / 64) (prereg S7).

Claim text (parse-gate clean: no '|' anywhere, >= 4 tokens, <= 600 chars):
    The marker stone <i> stands <i> meters tall.

Authoring note: prereg S8 sketches the class as
`CAP|<i>|The marker stone <i> stands <i> meters tall.`; the frozen S3
claim-text field rule forbids '|' inside claim text and the parse gate
rejects such lines, so the committed claim text omits the pipe prefix.
The index still appears twice as digits ("digits exact").

Usage:
    python3 gen_cap.py [--count N] [--out FILE]
Without --count, reads /proc/meminfo MemAvailable and computes the minimum
count whose worst-case pending-line bytes exceed the budget. A missing
/proc/meminfo is a loud failure (no silent fallback constant), unless
--count is given explicitly.
"""
import sys


def mem_available_bytes():
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return None


def worst_line_cost(digits):
    # PENDING|<seq>|<claim>|DELIBERATE\n with claim =
    # "The marker stone <i> stands <i> meters tall."
    # claim bytes = 38 + 2*digits; line = 8 + digits + 1 + claim + 11 + 1
    # (fresh-state seqs 1..count, so seq width == index width)
    return 59 + 3 * digits


def min_count_for_budget(budget):
    d = 1
    while True:
        cost = worst_line_cost(d)
        count = budget // cost + 1
        if len(str(count)) <= d:
            return count, cost
        d = len(str(count))


def main(argv):
    count = None
    out = None
    i = 0
    while i < len(argv):
        if argv[i] == "--count":
            i += 1
            count = int(argv[i])
        elif argv[i] == "--out":
            i += 1
            out = argv[i]
        else:
            sys.stderr.write("unknown arg: %s\n" % argv[i])
            return 2
        i += 1
    if count is None:
        mav = mem_available_bytes()
        if mav is None:
            sys.stderr.write("gen_cap: /proc/meminfo MemAvailable unavailable "
                             "and no --count given; refusing to guess\n")
            return 3
        budget = mav // 64
        count, cost = min_count_for_budget(budget)
        sys.stderr.write("gen_cap: MemAvailable=%d bytes budget=%d "
                         "worst_line_cost=%d count=%d\n"
                         % (mav, budget, cost, count))
    fh = open(out, "w") if out else sys.stdout
    for n in range(1, count + 1):
        fh.write("The marker stone %d stands %d meters tall.\n" % (n, n))
    if out:
        fh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
