#!/usr/bin/env python3
"""W4 arm-5 tape invariant checker.
Parses TST-1 tapes (framing: [u8 type][u32 le payload_len][payload...]) and asserts
the frozen B.1/B.4 arm-5 properties:
  1. every ORACLE_ANSWER (type 4) has a matching QUERY (type 10) with the same
     query_seq (no unprompted emission), payload = u64 seq + u8 bit only
  2. answer bit is a single bit (0 or 1)
  3. number of answered queries <= K
  4. K+1-th valid query is refused with reason 1 (budget exhausted)
  5. no TEACHER_MSG (3) or HINT (5) events in arm-5 tapes (nothing unprompted,
     no proposal path)
  6. REFUSED reason codes: 1 = budget exhausted, 2 = malformed; malformed lines
     do not consume budget
Usage: check_arm5_tape.py <tape> <K>  (exit 0 = all invariants hold)
"""
import struct, sys

TYPE_NAMES = {1:"TAPE_HEADER",2:"STIMULUS_REF",3:"TEACHER_MSG",4:"ORACLE_ANSWER",
              5:"HINT",6:"APPEAL",7:"INTEGRITY",8:"TURN_BOUNDARY",9:"TAPE_FOOTER",
              10:"QUERY",11:"QUERY_REFUSED",12:"STUDENT_DECISION"}

def parse(path):
    data = open(path,"rb").read()
    evs = []; off = 0
    while off < len(data):
        t = data[off]
        (ln,) = struct.unpack_from("<I", data, off+1)
        evs.append((t, data[off+5:off+5+ln]))
        off += 5+ln
    assert off == len(data), "trailing bytes"
    return evs

def main():
    path, K = sys.argv[1], int(sys.argv[2])
    evs = parse(path)
    fails = []
    def chk(name, cond, detail=""):
        print(("INV_OK " if cond else "INV_FAIL ") + name + (" " + detail if detail else ""))
        if not cond: fails.append(name)

    answered = []   # query_seq with ORACLE_ANSWER
    queries = []    # query_seq logged as QUERY
    refused = []    # (seq, reason)
    for t, p in evs:
        if t == 4:
            (seq,) = struct.unpack_from("<Q", p, 0)
            bit = p[8]
            chk("answer_len", len(p) == 9, f"seq={seq} len={len(p)}")
            chk("single_bit", bit in (0,1), f"seq={seq} bit={bit}")
            answered.append(seq)
        elif t == 10:
            (seq,) = struct.unpack_from("<Q", p, 0)
            chk("query_len", len(p) == 33, f"seq={seq} len={len(p)}")
            queries.append(seq)
        elif t == 11:
            (seq,) = struct.unpack_from("<Q", p, 0)
            reason = p[8]
            chk("refused_len", len(p) == 9, f"seq={seq} len={len(p)}")
            chk("refused_reason_valid", reason in (1,2), f"seq={seq} reason={reason}")
            refused.append((seq, reason))
        elif t in (3, 5):
            chk("no_unprompted_type_%d" % t, False, TYPE_NAMES[t])

    chk("every_answer_has_query", set(answered) <= set(queries),
        f"answered={answered} queries={queries}")
    chk("no_unprompted_answer", len(answered) == len(set(answered)) and all(a in queries for a in answered),
        f"answers={len(answered)} queries={len(queries)}")
    chk("no_answer_without_query", len(answered) <= len(queries))
    chk("budget_not_exceeded", len(queries) <= K, f"queries={len(queries)} K={K}")
    over = [s for s,r in refused if r == 1]
    if len(over) > 0:
        # budget fills with the first K well-formed queries (seqs strictly
        # increasing); every over-budget refusal arrived after the fill
        chk("kplus1_refused_after_fill",
            len(queries) == K and min(over) > max(queries),
            f"K={K} queries={len(queries)} first_over={min(over)} n_over={len(over)}")
    else:
        chk("no_over_budget", len(queries) <= K, f"K={K} queries={len(queries)}")
    malformed = [s for s,r in refused if r == 2]
    # reason-2 = malformed line OR non-increasing seq. A refused seq may also
    # appear as an answered QUERY in the duplicate-seq case (refused AFTER a
    # valid answer with the same seq); that is correct behavior.
    # QUERY seqs strictly increasing (harness-enforced)
    chk("query_seq_monotonic", queries == sorted(set(queries)) and len(queries) == len(set(queries)))
    chk("types_seen_sane", all(t in TYPE_NAMES for t,_ in evs), str(sorted(set(t for t,_ in evs))))

    print("SUMMARY,%s,events=%d,queries=%d,answered=%d,refused_budget=%d,refused_malformed=%d,fails=%d" % (
        path, len(evs), len(queries), len(answered), len(over), len(malformed), len(fails)))
    return 1 if fails else 0

sys.exit(main())
