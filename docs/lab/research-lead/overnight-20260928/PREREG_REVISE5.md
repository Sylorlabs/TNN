# PREREG H-REVISE5: two-phase diagnosis (propose + corroborate)

**Date:** 2026-09-29
**Branch:** tnn-native-lab
**Target:** H-REVISE4 DOWNGRADED (REVISE4_ADV_RESULT.md)
**Status:** FROZEN. This prereg is committed BEFORE any H-REVISE5
implementation or execution. If any frozen bar below is broken during
implementation, the prereg is amended transparently and re-frozen; the
bar is never weakened to force a pass.

## What is being repaired

The H-REVISE4 red team (X-RV4-1) proved the scored diagnosis
confidently misattributes on a unique wrong top: fixture
("zqy"->"zzz") with hidden truth IF input[2]=='y' THEN broadcast-first
yields unique top (0,122), a revision is appended, both held-outs fail.
No tie is required. The R1 tie protection only withholds on exact ties.

The red team also proved a structural degeneracy: in
`diagnose_scored`, the +1 output-relevance signal (v in fail_out) and
the +1 program-consistency signal (p in seq, seq from
pextract(fail, fail_out)) are the same signal. Proof: p appears in seq
iff some k has seq[k]==p iff out[k]==inp[p] iff v=fail[p] appears in
fail_out. Every discriminating candidate scores 0 or 2, never 1.
Empirically zero score=1 lines across all fixtures. The "two signals"
were one binary signal counted twice, and the documented honest limit
"near-ties (differing by 1) still resolve by lowest position"
described an impossible event.

Deeper: single-counterexample diagnosis is provably underdetermined.
X-RV4-1's wrong (0,122) and Phase C's right (0,120) are structurally
identical from the mechanism's view (incidental byte at pos 0 present
in the expected output, causal byte absent). No scoring function of
(fail, fail_out, passing set, P0) can separate them. The honest repair
is therefore not a better single-shot score but a second piece of
evidence.

## Repairs (frozen design)

**R1: honest single-signal propose.** `diagnose_propose` replaces
`diagnose_scored`. The +1 program-consistency term is DELETED (it was
the degenerate duplicate). The remaining +1 output-relevance term
(v appears in fail_out) is kept as the single honest binary signal.
Scores are 0 or 1. Tie at top returns -2 AMBIGUOUS (unchanged
semantics). No candidate discriminates returns -1 (unchanged). The
result doc will state plainly that phase 1 carries one bit of
evidence, not two.

**R2: corroboration gate.** New `diagnose_corroborate`: given the
proposed (p,v) and a SECOND counterexample (fail2, fail_out2),
returns 1 iff (a) fail2[p]==v (the condition fires on fail2),
(b) (p,v) discriminates fail2 from every passing input
(bounds-respecting, same rule as propose), and (c) the current
program VS mispredicts fail2. Otherwise 0. The caller appends a
revision ONLY on propose>=0 AND corroborate==1. On corroborate==0 the
caller emits UNCORROBORATED and withholds with new code -3; the
version store is unchanged. Corroboration is the independent second
signal: two counterexamples sharing an incidental byte is genuinely
stronger evidence than one.

**R3: honest documentation.** The result doc states: phase-1 scores
are 0/1 from one signal; the two independent evidences are propose
(output-relevance) and corroborate (second counterexample); the old
"near-tie" limit is replaced by the accurate statement; X-RV4-1 vs
Phase C indistinguishability is documented as the reason
single-shot confident append is abandoned.

What is NOT changed: the VS3 store, vs3_revise (explicit
refuse-with-warning, 4 slots), the discrimination rule, the
bounds-respecting guard, P1 discovery, dispatch order, determinism.

## Frozen kill bars

- **K-RV5-1 (unique-wrong-top withhold):** New Phase L replays the
  X-RV4-1 fixture exactly: P0=broadcast-last, passing
  "abc","def","ghi","jkl", fail1=("zqy"->"zzz"). Propose MUST return
  122 i.e. (0,122) (the wrong top is still proposed; the repair does
  not pretend phase 1 is fixed). Corroborate with
  fail2=("aqy"->"aaa") MUST return 0 (fail2[0]='a' != 122). The
  caller MUST emit UNCORROBORATED and withhold: vcount stays 0, no
  revision appended. Query "zqw" under the unchanged store MUST give
  "www" (P0 intact). If any revision is appended for (0,122),
  H-REVISE5 is KILLED.

- **K-RV5-2 (honest scoring):** The raw output MUST contain
  "score=1" candidate lines (the single binary signal takes value 1)
  and MUST NOT contain any phase-1 "score=2" line. If a phase-1
  score=2 appears, the degeneracy recurred and H-REVISE5 is KILLED.

- **K-RV5-3 (no regression):** All of K-RV4-1 (Phase J: tie ->
  AMBIGUOUS -2, vcount 0), K-RV4-2 (Phase K: R5 refused rc=-1,
  VS3FULL emitted, vcount 4, earlier revisions intact), and the
  Phase C/G/H/I/F behaviors hold, now via propose+corroborate:
  C appends (0,120) corroborated by ("xqw"->"xxx");
  G appends (0,121) corroborated by ("yqw"->"yyy");
  H appends (1,113) corroborated by ("aqc"->"qqq");
  I appends (2,120) corroborated by ("cbx"->"ccc");
  F withholds (UNRESOLVABLE, vcount unchanged, P0 intact).
  Expected total: 62/62 named checks PASS. No bar is superseded.

- **K-RV5-4 (determinism):** 3/3 runs byte-identical (cmp).

- **K-RV5-5 (corroboration liveness):** The four genuine second
  counterexamples (C/G/H/I) MUST corroborate (return 1). The
  mechanism must not degenerate into withholding everything. This
  is checked by the 62/62 total (checks 10, 26, 36, 46).

## Method

Pure Zag. No Python at any stage: no generators, no verifiers, no
analysis scripts, no scratch computation. Shell file utilities
(md5, cmp) only. Toolchain znc 2026.07.0-dev (edition 2026).
New file revise5.zag in
docs/lab/research-lead/overnight-20260928/; revise4.zag untouched.
Only owned paths are staged. No em dashes in loop documents.

## Honest limits (preregistered)

1. Corroboration needs a second counterexample; in a deployment this
   comes from continued monitoring, which the harness supplies
   directly. A lone first failure now waits instead of guessing.
2. Two counterexamples sharing an incidental byte can still
   misattribute; the residual risk is documented, not eliminated.
3. P1 is still discovered from the first counterexample alone; the
   corroborating pair is not yet used to improve P1.
4. Capacity remains 4 with explicit refuse-with-warning (unchanged).
5. Bounded L2+ revision. Not L3: the condition vocabulary
   (position, byte value) and the propose+corroborate protocol are
   researcher-designed; the mechanism does not invent representations.

## Commit lineage

- Prereg: this file (single-file commit, before implementation).
- Target: revise4.zag as committed.
- Red team: REVISE4_ADV_RESULT.md (4021d99eb prereg).
