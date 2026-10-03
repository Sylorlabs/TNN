# UNIFIED5 RESULT: H-UNIFIED5 SURVIVES (17/17)

**Date:** 2026-09-29
**Prereg:** PREREG_UNIFIED5.md (committed as `aba1056ae`, frozen before any implementation; strict-ancestor ordering verified below)
**Implementation:** unified5_learn.zag (this directory; `unified4_learn.zag` untouched)
**Raw evidence:** UNIFIED5_RAW_OUTPUT.txt (md5 `edb2cd39a07333b61416cc2fee4db31e`, 3/3 byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere.

## Verdict: H-UNIFIED5 SURVIVES (17/17)

The H-UNIFIED4 red-team follow-up (U4_ADV_RESULT.md suggestion 2) is
addressed: the `parse_ints` non-digit infinite-loop hazard is hardened
with a defensive guard that skips unexpected bytes with an explicit
trace. The capacity boundary (suggestion 3) is documented explicitly;
the refuse-with-warning policy is unchanged. No learned behavior
changes.

## What was built

`unified5_learn.zag` = `unified4_learn.zag` copied verbatim (cmp
verified), then exactly three additions (diff-verified, no other
changes):

**1. `parse_ints` defensive guard (the hardening).** A non-digit,
non-comma byte in a numeric field previously hung the parser: the
inner while broke immediately with `v=0` and `i` unadvanced, the comma
check failed, and the outer `while(i<hi)` repeated forever. The guard
checks `is_digit(b[i])==0 && b[i]!=44` at the top of each outer
iteration; on a hit it emits `PARSE_GUARD: skipped non-numeric byte N
in numeric field (H-UNIFIED5)` and advances `i` by one. Skipped bytes
are not stored and do not consume an output slot, so valid numbers
around them still parse. On valid inputs (digits and commas only) the
guard branch never executes, so behavior is byte-identical to
H-UNIFIED4.

**2. Capacity policy comment block.** A documentation-only comment
stating the refuse-with-warning policy, the DCOUNT/QCOUNT accounting,
the store limits, and the H-MEM eviction pointer. Comments do not
affect output bytes.

**3. K-U5-1 test block in `main()`.** White-box probe of the hardened
parser (see K-U5-1 below). The final tally becomes 17/17 and the
verdict line reads H-UNIFIED5.

## Frozen bar results

- **K-U5-1 PASS:** `parse_ints("1,0x,0",0,5,pt)` completed (no hang;
  completing at all proves the infinite loop is closed), emitted
  exactly one `PARSE_GUARD` trace naming byte 120, and recovered the
  parse as `[1,0,0]` (pv0==1, pv1==0, pv2==0). The valid control
  `parse_ints("1,0,0",0,5,pc)` parsed `[1,0,0]` with no guard trace.
  Output: `K-U5-1 parse recovered [1,0,0], valid control clean PASS`.
- **K-U5-2 PASS:** All 16 H-UNIFIED4 frozen checks (12 originals +
  K-U4-1 + K-U4-2 + K-U4-5 + K-U3-2) pass. Output lines 2-125 are
  byte-identical to UNIFIED4_RAW_OUTPUT.txt (diff clean); 16 PASS
  lines. The only output differences from H-UNIFIED4 are the header
  emit (v3 -> v5, by design) and the appended K-U5-1 block.
- **K-U5-3 PASS:** 3/3 runs byte-identical (cmp),
  md5 `edb2cd39a07333b61416cc2fee4db31e`.
- **K-U5-4 PASS:** `grep -c PARSE_GUARD` over the frozen 16 blocks is
  0. The guard never fires on valid inputs. (The two PARSE_GUARD
  string occurrences in the full output are both inside the K-U5-1
  block: the trace itself and the PASS line naming it.)

Total: 17/17 (16 frozen + K-U5-1).

## Source audit (self)

- Diff `unified4_learn.zag` vs `unified5_learn.zag` contains only: the
  header comment, the parse_ints guard, the capacity comment block,
  the main() header emit, the K-U5-1 block, and the verdict lines. No
  mechanism logic besides parse_ints is touched.
- `emit`, `i32s`, `is_digit` are all defined before `parse_ints`
  (lines 34, 35, 729 vs 905); the guard uses only in-scope functions.
- No test-answer literals in the guard; the byte-44 check is the
  structural comma constant already used by the original code.
- `unified4_learn.zag` is unmodified (cmp against the committed file
  is clean).

## Capacity boundary: explicit statement (H-UNIFIED5)

This section is the "document the capacity boundary more explicitly"
deliverable. No behavior changes; K-U3-2 passes unchanged.

**Policy.** Refuse-with-warning (H-UNIFIED3 Repair B, intact since).
When the causal store is full, `clearn` returns -1. Both
`handle_caus_learn` and `handle_caus_revise` then, per dropped episode:
emit a USTOREFULL line naming the episode and stating that verified
knowledge is kept; increment the cumulative drop counter at
W[DCOUNT()]; leave the store untouched. Quarantined episodes
(coherence-gate rejections) are counted separately at W[QCOUNT()] and
are never confused with drops. Nothing is silently lost: every episode
that does not change store state is either corroborated (counted),
quarantined (counted, traced), or dropped-full (counted, warned).

**Limits.** 16 causal rules. 16 procedure slots. 4 bridge slots. 128
pair descriptors. The unlabeled stream is first-writer-wins: once a
rule is ACTIVE, a contradicting stream episode is quarantined, never
applied. A full store does not evict, does not overwrite, does not
degrade old rules.

**What this costs.** A continuing learner that outlives its 16 causal
slots stops learning new causal regularities while preserving old
ones. The K-U3-2 test demonstrates the honest version of this: 16
distinct coherent states fill the store, the 17th and 18th are refused
with warnings, DCOUNT rises by exactly 2, the 16 verified rules stay
ACTIVE, and queries for the refused state withhold. Honest, but
bounded: the learner cannot trade old knowledge for new.

**Why eviction is not done here.** Replacing refuse-with-warning by
eviction would change the frozen K-U3-2 contract (refuse -> evict).
That is a cross-lane architectural decision: which rule to evict
(oldest? least-corroborated? least-queried?), how to trace the
eviction, and whether eviction composes safely with the coherence gate
and the operator revision channel are all open design questions owned
by the H-MEM eviction work. Adopting eviction inside a hardening
hypothesis, without a dedicated eviction prereg and its own kill
bars, would be scope creep and would force a K-U3-2 supersession on
non-evidential grounds. The principled path is a future H-UNIFIED6
(or H-MEM-driven) hypothesis whose prereg freezes an eviction policy
and whose kill bars include the K-U3-2 scenario re-run under eviction
semantics.

**Pre-existing parser shape hazard (documented, unchanged).** The
guard hardens against non-digit bytes, but a field with too many VALID
numbers (e.g. `"1,0,0,5"` into a 3-slot buffer) still overflows the
fixed out buffer exactly as in H-UNIFIED4. Classification upstream
guarantees the exact shape (3 ints left, 2 right), so this is
unreachable through every audited dispatch path. It is recorded here
so the hardening claim is not overread: the parser is now total
against byte-level anomalies, not against shape violations.

## Honest limitations (carried from prereg)

1. Deployment still needs a genuinely separate authenticated operator
   channel (H-UNIFIED4 limitation 1, unchanged).
2. The operator path is trusted by construction (H-UNIFIED4 limitation
   2, unchanged).
3. The unlabeled stream remains first-writer-wins (H-UNIFIED4
   limitation 3, unchanged).
4. Capacity remains refuse-with-warning; principled eviction is H-MEM
   lane future work (H-UNIFIED4 limitation 4, now documented above).

## Classification

Bounded L2 integration hardening, not L3. Makes the unified learner's
parser total against byte-level anomalies and its capacity boundary
explicit; changes no learned behavior. Recommended follow-up: a
dedicated eviction-policy hypothesis (H-MEM lane) with its own
preregistered kill bars.

## Commit lineage

- Prereg: `aba1056ae` (PREREG H-UNIFIED5 FROZEN, alone, before any
  implementation).
- This result: implementation + evidence + result doc (see commit
  message for hash).
- Ordering: verified via `git merge-base --is-ancestor aba1056ae
  <result>` before pushing the report upward.
