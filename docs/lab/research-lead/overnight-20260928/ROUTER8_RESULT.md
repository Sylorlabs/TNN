# H-ROUTER8 RESULT: SURVIVES (all frozen kill bars pass)

**Date:** 2026-09-29
**Researcher:** H-ROUTER8 Frontier Researcher (independent subagent)
**Target:** H-ROUTER7 SURVIVES (builder) / DOWNGRADED (red team `37ce0d271`,
X-R7-1 exploratory V2: capacity defeat of the total-table headline plus
a trace-transparency defect at capacity).
**Verdict:** SURVIVES. All four frozen kill bars PASS. Classification:
bounded L2+ structural learning with provenance diagnostics and honest
capacity signaling. Not L3.

## Lineage

- Prereg `PREREG_ROUTER8.md` committed alone as `ada8db14d` BEFORE any
  implementation edit, build, or run. No amendments.
- `router8_learn.zag` = `router7_learn.zag` copied verbatim
  (cmp-verified) plus exactly the frozen R8-1..R8-4 change set.
  `router7_learn.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (`git merge-base --is-ancestor ada8db14d HEAD`).
- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp. Zero Python at any stage.
- Toolchain pinned: `znc 2026.07.0-dev (edition 2026)`.

## Repairs implemented (exactly per frozen prereg)

**R8-1 (entry-loop emit gate).** The `TABLE-RULE` emit in
`build_table_rest` now fires only when `rt_add` actually inserted the
rule (`nrt` before/after comparison). On the normal path the emit is
byte-identical to before; on a capacity refusal nothing is printed for
the dropped entry. The `TABLE OVERFLOW` emit inside `rt_add` is
unchanged and already loud.

**R8-2 (fallback emit gate + loud warning).** The R1 explicit-fallback
emit is gated on actual insertion. When the fallback append is refused
at the 24-rule cap, the harness now emits
`TABLE-NON-TOTAL: explicit [any]->WITHHOLD fallback refused (TABLE
OVERFLOW at 24 rules); route3 may return -1 for uncovered triples;
table is NOT total`
instead of the old phantom `[any]->WITHHOLD` line. A route3 -1 at
capacity is now declared, never silent.

**R8-3 (narrowed claim).** Comments and banner state the
evidence-backed C1: the compiled table is total iff the explicit
fallback is actually appended, i.e. iff fewer than 24 rules were
compiled before it.

**R8-4 (test section).** New `CAPACITY-HONESTY (X-R7-1 V2 replay)`
section replays the red team's 40-mark V2 fixture verbatim (s0=1 block
W@1 PL@{2,4,6,8} CL@{3,5,7,9}; s0=2 block W@1 CL@{2,4,6,8}
PL@{3,5,7,9}; s0=3 block W@1 PL@{2..9}; s0=0 block W@1 PL@{2,4,6,8}
CL@{3,5,7,9}; 4 query marks), using a `rep_seg` helper copied verbatim
from the committed adversary harness and attributed. Adversary evidence
reused as regression fixture, not presented as new discovery.

**Explicitly declined:** raising the 24-rule cap or evicting
lowest-specificity rules. The cap is a frozen capacity bound (192-byte
table, 8 bytes/rule); changing it alters frozen semantics and every
downstream bar. Honest signaling replaces the false totality claim.
Cap/eviction remains future work.

## Frozen kill-bar evidence

Raw: `ROUTER8_RAW_OUTPUT.txt` (1004 lines, md5
`bc4019ee7e44438a839de5c6584fc4c8`), program output only (direct
binary execution, empty stderr).

- **K-R8-1 PASS (capacity honesty, in-code):** `CAP-TABLE-SIZE 24`
  (want 24), `CAP-ANY-RULE present=0` (want 0),
  `CAP-PROBE (0,10,0) -> -1` (want -1, disclosed non-total).
  `K-R8-1 (capacity honesty): PASS [size=24 any=0 probe=-1 want 24,0,-1]`.
  The induction is untouched by R8, so the V2 structural facts reproduce
  exactly; only the trace changed.

- **K-R8-2 PASS (honest trace, external greps):** within the
  CAPACITY-HONESTY section:
  - `^TABLE-NON-TOTAL` count = 1 (loud warning fired exactly once)
  - phantom `TABLE-RULE [any]->WITHHOLD (explicit fallback` count = 0
    (under R7 this is 1)
  - `^TABLE-RULE .* (from H` count = 24 = CAP-TABLE-SIZE (under R7 this
    is 25: the stale 25th emit)
  - `^TABLE OVERFLOW$` count = 2 (25th entry drop + fallback refusal)
  Whole run: phantom-text line count = 1, exactly the real fallback
  line from the normal-path fallback-loss section (TABLE-SIZE 7),
  proving R8-2 did not break the normal path.

- **K-R8-3 PASS (no regressions):** zero FAIL lines in the raw;
  `H-ROUTER8 AUTOMATED BARS PASS`. All prior bar conditions hold:
  K-R7-1 (`FALLBACK-PROBE (3,1,0) -> 10`, `FALLBACK-ANY-RULE present=1`),
  K-R7-2, K-R6-1, K-R6-2, K-R5-1, K-R5-2a/b/c, K-R4-1..5.

- **K-R8-4 PASS (determinism):** 3 consecutive full runs byte-identical
  via `cmp`, exit code 0, zero FAIL lines, md5
  `bc4019ee7e44438a839de5c6584fc4c8` x3.

Final tally: **H-ROUTER8 SURVIVES.**

## Honest residuals (disclosed, not repaired)

- The 24-rule capacity bound remains. At capacity, uncovered triples
  route to -1; the TABLE-NON-TOTAL warning now declares this loudly at
  compile time, but the per-probe return path is still -1 (unchanged
  `route3` semantics).
- The narrowed C1 stands: total iff <24 rules before the fallback
  append. No claim beyond it.
- The red team's R3 recommendation (a dedicated merge-soundness pass
  over V2's `[s0=1]->CAUS_LEARN` / `[s0=2]->PROC_LEARN` overgeneralized
  entries, harmless only via first-match ordering) is not addressed
  here; it is untouched behavior, flagged for a future red team.

## Governance disclosures

1. Prereg committed alone before any implementation; ordering verified
   by merge-base --is-ancestor.
2. Pure Zag throughout. Zero Python at any stage.
3. No binaries committed (builds in /tmp/r8 only).
4. Only the three owned files staged/committed (PREREG_ROUTER8.md was
   committed separately beforehand). No other worker's files touched.
   Pathspec-restricted staging used throughout.
5. No em dashes in loop documentation (byte-checked: 0 in prereg,
   source, and result).
6. H-ROUTER7's own governance status is unresolved (pre-prereg pilot;
   H-ROUTER6 ancestry; result files untracked after the `981459ee3`
   reset). H-ROUTER8 does not cure those issues; the R7 lineage caveat
   is carried forward for coordinator adjudication. The base source was
   the red-team-verified blob, byte-identical to the working tree copy.
7. One transient build invocation emitted no binary (rerun with full
   logging succeeded, znc-exit 0); disclosed, not evidence.
8. The `TABLE OVERFLOW` grep subtlety: the TABLE-NON-TOTAL warning text
   itself contains the substring "TABLE OVERFLOW", so the frozen count
   of 2 genuine overflow emits was verified with the anchored pattern
   `^TABLE OVERFLOW$`.

## Suggested follow-ups for parent

1. Independent red team on H-ROUTER8 (natural attacks: merge-soundness
   of the V2 overgeneralized entries per the R7 red team's R3; warning
   spoofing; capacity gaming via threshold-compiled rules).
2. Coordinator adjudication of the carried R7 governance caveat before
   H-ROUTER8 is treated as canonical.
3. The research paper's ROUTER lane should carry the narrowed C1 and
   the H-ROUTER8 survival.
