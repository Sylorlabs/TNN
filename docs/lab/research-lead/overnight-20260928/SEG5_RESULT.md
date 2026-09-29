# SEG5 RESULT: H-SEG5 Frontier Report

**Date:** 2026-09-29
**Researcher:** H-SEG5 Frontier Researcher (subagent)
**Prereg:** PREREG_SEG5.md (commit a59adaba3, frozen before any
implementation edit, build, or test run)
**Parent:** H-SEG4 SURVIVES (13/13); H-SEG4 red team SURVIVES all 4
attacks with residual #2 (off-route-clamp theoretical hole in the
per-run saturation flag) and a documentation correction (H1-T true
count 2^29, not Fib(31)).
**Implementation:** seg5_learn.zag (SEG-LEX-E)
**Differential harness:** seg5_diff.zag (OLD vs NEW vs REF)
**Raw evidence:** SEG5_RAW_OUTPUT.txt (md5
bb8b3ddfb939131959f4c1dd24ae3326, 3/3 byte-identical),
SEG5_DIFF_RAW.txt (md5 2bd3e6ce97534183929366175c63fc1e, 2/2
byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere (implementation, harness,
builds, runs, greps, md5, cmp).

## Verdict: H-SEG5 SURVIVES 5/5

All five frozen kill bars PASS. The H-SEG4 red-team residual #2 is
closed by construction: the per-run saturation flag is replaced by
per-position saturation propagation, for which the exact honesty of
the 999+ cap label is PROVEN by induction (frozen in PREREG_SEG5.md),
not merely searched. The H1-T true count is corrected to 2^29 =
536870912 in all affected docs, the old number marked SUPERSEDED with
lineage. All 13 H-SEG4 frozen checks still pass; output is
byte-identical to SEG4 except the two banner lines.

Classification: bounded L2 structural-learning repair (provable
honesty of a saturation label). Not L3: MAXL=5, MINC=2, the
containment family, the len^2 shape, FBPEN=20 remain authored; the
sentinel bound is instance-derived; the sat proof concerns label
honesty, not representational invention.

## What H-SEG5 changes (R1, frozen)

seg5_learn.zag = seg4_learn.zag plus exactly these edits (verified by
diff; nothing else):

1. `relax`, strict-improvement branch: added
   `set32(sat,np*4,get32(sat,i*4))` so the saturation bit follows the
   new optimal predecessor set when a strictly better score resets it.
2. `relax`, tie branch: added `if(get32(sat,i*4)==1){
   set32(sat,np*4,1); }` so saturation propagates only along optimal
   predecessors; the clamp line now sets the per-position bit
   `set32(sat,np*4,1)` instead of the per-run `set32(sat,0,1)`.
3. `run_exp`: `sat` is now `(n+1)` i32 cells, zeroed in the init loop;
   the 4-byte per-run flag is gone.
4. Label: `get32(sat,0)` became `get32(sat,n*4)`.
5. Banner strings v4 -> v5. No fixture changes. seg4_learn.zag
   untouched.

## The frozen proof (why the label is now exactly honest)

Definitions: T_i = true number of optimal-score paths to position i
(T_0 = 1); OptMoves_i = (p, m) pairs with dp[p] + score(m) = dp[i];
every move advances >= 1 (fallback len 1, chunks len >= MINC = 2), so
all p < i. After the DP, nopt[i] = min(sum of nopt[p] over OptMoves_i,
999) and sat[i] = [sum > 999] OR (OR of sat[p] over OptMoves_i);
sat[p] is final when p is processed as a source.

Induction on i (hypothesis at all p < i: sat[p]=1 iff T_p > 999, and
nopt[p] = min(T_p, 999)):

- Claim A: min(sum min(T_p,999), 999) = min(T_i, 999). If all T_p <=
  999 both sides equal sum T_p capped; if some T_p > 999 both sides
  are 999. Hence nopt[i] = min(T_i, 999).
- Claim B: sat[i] = 1 iff T_i > 999. Forward: clamp fired implies
  T_i >= subtotal > 999; sat[p]=1 implies T_p > 999 so T_i >= T_p >
  999. Backward: T_i > 999 with some T_p > 999 gives sat[p]=1 by IH;
  with all T_p <= 999 the subtotal equals T_i > 999 so the clamp
  fired.

Label theorem at n, with no = nopt[n] = min(T_n, 999):
- no < 999: T_n = no exactly; printed exact.
- no == 999 and sat[n] = 1: T_n > 999; "999+" honest.
- no == 999 and sat[n] = 0: T_n <= 999 and min(T_n,999) = 999, so
  T_n = 999 exactly; "999" printed exact.

No case mislabels. An off-route clamp sets sat at its own position
but cannot reach sat[n] unless it lies on an optimal route to n, in
which case T_n > 999 genuinely. The residual is closed by
construction.

## Kill bar results

**K-SG5-1 (doc correction): PASS.** 1346269 / Fib(31) no longer appear
as the H1-T true count in SEG3_ADV_RESULT.md or PREREG_SEG4.md; every
remaining mention sits inside an explicit SUPERSEDED note stating the
corrected 2^29 = 536870912 with lineage to SEG4_ADV_RESULT.md
"Correction" section via H-SEG5 R2. SEG4_RESULT.md was checked and
never contained the wrong number (the red-team follow-up listed it,
but grep confirms zero hits; noted here so the checklist is honest).
Independent computational confirmation: the differential harness
reference DP yields CALIB-REF-H1T = 536870912 for "ab" x 30 on the
frozen H1 corpus.

**K-SG5-2 (implementation per frozen spec + proof): PASS.** Diff
seg4_learn.zag -> seg5_learn.zag shows exactly the five frozen edit
groups (R1 a-e), nothing else. The proof above is the frozen
correctness argument from PREREG_SEG5.md, reviewer-checked.

**K-SG5-3 (all 13 frozen checks): PASS.** seg5_learn output is
byte-identical to committed SEG4_RAW_OUTPUT.txt except the two banner
lines (H-SEG4 -> H-SEG5). Verified frozen values: EXP-A SCORE 132
NOPT 1; EXP-C 100/1; EXP-D -30/1; EXP-B 22/2 AMBIGUOUS NCAND 2;
ADV1-T1 50/1; ADV1-T2 100/1; ADV2-T2 100/1; ADV3 (120-char) and
SENT60 (60000-char) SCORE -20*n NOPT 1 SEGMENTED (SENT60:
-1200000); LONG60 SCORE 600000 NOPT 1; H1-T SCORE 0 NOPT 999+
VERDICT AMBIGUOUS NCAND 5. H1-T still prints "999+" because T =
2^29 > 999 implies sat[60] = 1 by the proof; the mechanism behavior
on non-saturating inputs is unchanged.

**K-SG5-4 (determinism): PASS.** 3/3 runs byte-identical (cmp), md5
bb8b3ddfb939131959f4c1dd24ae3326.

**K-SG5-5 (differential honesty battery, >= 2000 cases): PASS.**
2130 cases, zero NEWDISAGREE. Battery composition:
- Block 1 (800): exact replication of the red-team X-SG4-2b battery
  (5 families x (40 structured + 120 LCG-random), seed 12345).
  Reproduces their result exactly: 30 cases with sat = 1, all with
  T_n > 999 (powers of two 2048..536870912); 0 MISLABEL-FP, 0
  MISLABEL-FN. This validates the harness against the frozen red-team
  evidence.
- Block 2 (1000): 5 families x 200 fresh LCG-random cases, seed
  99991, lengths 6..60.
- Block 3 (40): long combs "ab" x k, k = 41..80, on the H1-like
  corpus (T up to 2^79, REF reports HUGE past 1e9).
- Block 4 (90): decoy inputs, "ab" x 12 comb prefix (T_24 = 2048 >
  999, clamp fires mid-comb) plus tails over {a,b,c} (60 random) and
  c-only tails (30).
- Block 5 (200): comb-rich random strings over {a,b}, lengths
  20..48, on the H1-like corpus.
For every case with T_n <= 1e9, the NEW label was checked against
the honest truth (T_n > 999 -> "999+"; T_n == 999 -> "999"; T_n <
999 -> exact): 2130/2130 agree. 161 saturated cases (satn = 1) all
confirmed T_n > 999. Self-check NOPTDIFF (OLD vs NEW nopt): 0
differences across all 2130, confirming the count logic is unchanged
and only the sat plumbing differs. The differential harness itself
is deterministic: 2/2 byte-identical runs.

**OLD-mechanism mislabel hunt (honest report, not a bar):** 0
MISLABEL-FP, 0 MISLABEL-FN across all 2130 cases. No fixture was
found that breaks the superseded per-run-flag label. 0
SAT-OFFROUTE-CAND: in every searched case where a clamp fired, the
final count also saturated, so no off-route clamp was directly
observed either. The hunt outcome does not affect the verdict: the
NEW mechanism is covered by proof, and the OLD mechanism is
superseded.

## Failures, repairs, and negative evidence

- No implementation failures: the first build compiled clean and the
  first run reproduced SEG4 output modulo banners.
- One proof-review pass before freezing: the initial backward
  direction of Claim B ("clamp fires at i iff T_i > 999") was found
  to be FALSE as stated (single saturated predecessor gives subtotal
  exactly 999, no clamp at i, yet T_i > 999); the induction was
  restructured so the "some T_p > 999" case is discharged by the IH
  on p rather than by the clamp at i. The frozen prereg contains the
  corrected version. This is exactly the class of subtle error the
  prereg-before-implementation rule is meant to catch in the
  argument before it reaches code.
- Negative evidence preserved: the 2130-case battery found no
  OLD-mechanism mislabel and no observed off-route clamp; both
  non-findings are recorded, not hidden.

## Boundaries and honest limits

1. The proof covers label honesty only. DP time O(n*nch) and memory
   O(n) remain allocation-bound (engineering, not correctness).
2. The count above 999 remains unrecoverable by the mechanism (the
   REF DP is an adversary instrument, not part of the learner).
3. The genuine-morpheme-inside-longer-chunk discount boundary is
   unchanged from H-SEG3. enum_bwd host-stack recursion bound
   unchanged.
4. The memory cost of honesty is one i32 per position (sat array);
   the per-run flag cost 1 i32 total. Negligible.
5. Bounded L2 at most, not L3. The sat proof is about the honesty of
   a saturation label, not about invention.

## Governance disclosures

- Prereg PREREG_SEG5.md committed alone (a59adaba3) before any
  implementation edit, build, or test run. No Python at any stage.
- Only H-SEG5-owned files staged and committed; concurrent agents'
  files untouched. No binaries committed (all builds ran in /tmp/sg5).
- No em dashes in loop documentation (grep verified 0 in prereg).
- seg4_learn.zag and all prior evidence untouched.
- The K-SG5-1 correction preserves frozen history: original prereg
  text is kept visible inside SUPERSEDED notes with lineage, not
  silently rewritten.
- One pre-freeze proof correction is disclosed above (Claim B
  restructuring); it happened before the prereg commit, so the
  frozen proof was never wrong in-commit.

## Files and commit lineage

- docs/lab/research-lead/overnight-20260928/PREREG_SEG5.md
  (commit a59adaba3, prereg alone)
- docs/lab/research-lead/overnight-20260928/seg5_learn.zag (new)
- docs/lab/research-lead/overnight-20260928/seg5_diff.zag (new)
- docs/lab/research-lead/overnight-20260928/SEG5_RAW_OUTPUT.txt
  (md5 bb8b3ddfb939131959f4c1dd24ae3326, 3/3 byte-identical)
- docs/lab/research-lead/overnight-20260928/SEG5_DIFF_RAW.txt
  (md5 2bd3e6ce97534183929366175c63fc1e, 2/2 byte-identical)
- docs/lab/research-lead/overnight-20260928/SEG5_RESULT.md (this file)
- docs/lab/research-lead/overnight-20260928/SEG3_ADV_RESULT.md
  (H1-T correction, SUPERSEDED notes)
- docs/lab/research-lead/overnight-20260928/PREREG_SEG4.md
  (H1-T correction, SUPERSEDED notes)

## Recommended follow-ups (for the parent, not this lane)

1. An independent red team should attack H-SEG5 (the proof is
   reviewer-checked here; an adversary should try to break the
   implementation against the proof, e.g. differential fuzzing of
   relax edge cases, and audit that sat follows resets correctly).
2. The research paper's segmentation section needs the H-SEG5 line
   (left for the paper lane to avoid edit conflicts).
3. CANONICAL_STATE.md rebuild (parent lane).
