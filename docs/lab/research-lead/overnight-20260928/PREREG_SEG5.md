# PREREG H-SEG5 FROZEN

**Date:** 2026-09-29
**Researcher:** H-SEG5 Frontier Researcher (subagent)
**Parent:** H-SEG4 SURVIVES (13/13); H-SEG4 red team SURVIVES all 4 attacks.
**Status:** FROZEN. This document is committed alone before any
implementation edit, build, or test run. No Python at any stage.
No em dashes in loop documentation.

## Targeted residual

H-SEG4 red team (SEG4_ADV_RESULT.md) closed all four attacks but left
residual #2: the "exactly honest" 999+ cap label rests on a per-run
saturation flag. The flag is set if the 999 clamp fires at ANY
position. A clamp firing at a position off every optimal route to n,
combined with a genuine final count of exactly 999, would mislabel as
"999+". The red team searched 800 cases and found zero such fixtures;
the claim stands as "exactly honest on all 800 tested cases". The red
team recommended "a targeted off-route-clamp fixture attempt or a proof
that off-route clamps are impossible".

H-SEG5 closes the residual by construction: replace the per-run flag
with per-position saturation propagation, for which the exact-honesty
of the label is PROVEN (induction below), not merely searched. The
question of whether an off-route-clamp mislabel fixture exists for the
old mechanism becomes moot: the new mechanism cannot mislabel, by proof.

## Definitions (frozen)

Positions 0..n. Every move advances >= 1 (fallback len 1, chunks len >=
MINC = 2). dp[i] = optimal score to i. OptMoves_i = set of (p, m) pairs
(source position p < i, move m) with dp[p] + score(m) = dp[i] (the moves
relaxed into i at the final optimal score). T_i = number of
optimal-score paths to i = sum over (p,m) in OptMoves_i of T_p, with
T_0 = 1. nopt[i] = mechanism's clamped count. sat[i] = mechanism's
per-position saturation bit (new in H-SEG5).

The DP processes source positions in increasing order. relax(p -> i) is
called exactly once per (p, move). Final state at i after all relaxes:

- nopt[i] = min( sum over (p,m) in OptMoves_i of nopt[p], 999 ).
  (Strict-score-improvement resets discard earlier accumulations; the
  clamp v > 999 -> 999 is idempotent once hit; tie accumulation sums
  exactly the final optimal pred set.)
- sat[i] = CF_i OR (OR over (p,m) in OptMoves_i of sat[p]),
  where CF_i = [sum over (p,m) in OptMoves_i of nopt[p] > 999]
  (clamp fired during the final accumulation).
- Base: nopt[0] = 1, sat[0] = 0 (z_alloc zeroed; no relax targets 0).
  Every position is reachable via fallback, but unreached positions
  (dp = sent) are never relaxed from and contribute nothing; for them
  nopt = 0, sat = 0, T = 0, consistent with the claim.

sat[p] is final when p is processed as a source (all relaxes targeting p
come from sources < p, processed earlier). Induction is on i increasing.

## Frozen proof: sat[i] iff T_i > 999, and nopt[i] = min(T_i, 999)

Induction hypothesis at all p < i:
  (1) sat[p] = 1 iff T_p > 999.
  (2) nopt[p] = min(T_p, 999).

Step for i. Let P = OptMoves_i. T_i = sum_{(p,m) in P} T_p.
Let f = sum_{(p,m) in P} nopt[p] = sum_{(p,m) in P} min(T_p, 999) [by (2)].

Claim A: min(f, 999) = min(T_i, 999).
  If all T_p <= 999: f = T_i, done. If some T_p > 999: T_i > 999 so
  min(T_i,999) = 999; and f >= 999 (that term contributes 999), so
  min(f,999) = 999. Done. Hence nopt[i] = min(T_i, 999): proves (2).

Claim B: sat[i] = 1 iff T_i > 999, where sat[i] = [f > 999] OR (OR sat[p]).
  Forward: if f > 999, then T_i >= f > 999 (each min(T_p,999) <= T_p).
    If sat[p] = 1 for some (p,m) in P, then T_p > 999 by IH (1), so
    T_i >= T_p > 999.
  Backward: T_i > 999. If some T_p > 999, IH (1) gives sat[p] = 1.
    Else all T_p <= 999, so f = T_i > 999, the clamp fired. Done.
  Proves (1).

## Frozen theorem: the printed label is exactly honest, all cases

Let no = nopt[n] = min(T_n, 999) [by (2)].
- If no < 999: then T_n = no (min(T_n,999) < 999 implies T_n < 999).
  Printing no is exact.
- If no == 999 and sat[n] = 1: T_n > 999 [by (1)]. Printing "999+"
  is honest.
- If no == 999 and sat[n] = 0: T_n <= 999 [by (1)]; min(T_n,999) = 999
  forces T_n = 999. Printing "999" is exact.

No case mislabels. The off-route-clamp scenario is absorbed: an
off-route clamp sets sat at its own position, but sat[n] = 1 iff T_n >
999 regardless of off-route events. QED.

## Repairs (frozen, exact)

**R1: per-position saturation propagation.** seg5_learn.zag =
seg4_learn.zag copied verbatim plus exactly these edits:
  a. Header comment: replace the H-SEG4 cap paragraph with the H-SEG5
     per-position scheme and proof reference.
  b. relax: on strict improvement (ns > cur) add
     set32(sat,np*4,get32(sat,i*4)) alongside the nopt copy.
     On tie (ns == cur): after computing v, add
     if(get32(sat,i*4)==1){ set32(sat,np*4,1); }
     and change the clamp line to set32(sat,np*4,1) (was set32(sat,0,1)).
  c. run_exp: replace let sat:[]u8=z_alloc(4) with
     let sat:[]u8=z_alloc((n+1)*4); zero it in the init loop alongside
     dp/nopt/mvc.
  d. Label: change get32(sat,0) to get32(sat,n*4); update the honesty
     comment to cite the frozen proof.
  e. main(): banner "H-SEG4 SEG-LEX-D" -> "H-SEG5 SEG-LEX-D";
     final "H-SEG4 COMPLETE" -> "H-SEG5 COMPLETE". No fixture changes.
  Nothing else changes. seg4_learn.zag untouched.

**R2: H1-T true-count documentation correction.** In SEG3_ADV_RESULT.md,
PREREG_SEG4.md, SEG4_RESULT.md: replace the wrong true count
Fib(31) = 1346269 with the corrected 2^29 = 536870912, mark the old
number SUPERSEDED with lineage to SEG4_ADV_RESULT.md ("Correction"
section). The saturation conclusion is unchanged (536870912 > 999);
only the cited count was wrong (the X-SG3-2 analysis missed zero-score
chunks "aba", "ba", "bab"). If the research paper cites Fib(31), note
it for the paper lane; do not edit the paper in this lane.

## Frozen kill bars

- **K-SG5-1:** grep verifies 1346269/Fib(31) no longer appear as the
  H1-T true count in SEG3_ADV_RESULT.md, PREREG_SEG4.md,
  SEG4_RESULT.md; each carries a SUPERSEDED note with lineage to
  SEG4_ADV_RESULT.md; 536870912 = 2^29 is stated.
- **K-SG5-2:** Per-position sat propagation implemented exactly per
  R1 (diff seg4 -> seg5 shows only the frozen edits). Frozen proof
  above is the correctness argument; it is reviewer-checked, not
  executed.
- **K-SG5-3:** All 13 frozen checks pass: K-SG4-1 (SENT60), K-SG4-2
  (LONG60), K-SG4-3 (H1-T prints "999+", VERDICT AMBIGUOUS, NCAND 5),
  K-SG4-4 (9 H-SEG3 checks byte-identical to SEG3 raw), K-SG4-5
  (determinism). Expected: output byte-identical to SEG4_RAW_OUTPUT.txt
  except the v4 -> v5 banner lines (mechanism behavior unchanged on
  non-saturating inputs; H1-T still "999+" since T = 2^29 > 999).
- **K-SG5-4:** 3/3 runs byte-identical (cmp), md5 recorded.
- **K-SG5-5 (differential honesty battery):** A harness implements three
  DPs sharing the real lexicon training: OLD (seg4 per-run sat),
  NEW (seg5 per-position sat), REF (unclamped reference counts, cap
  1e9, truth = T_n when <= 1e9). Battery >= 2000 cases: the red-team
  800 (5 families x 160) plus new targeted decoy families (comb prefix
  with T > 999 feeding a suboptimal bridge, random tails) plus fresh
  random cases. For every case with T_n <= 1e9: NEW label must equal
  the honest truth (T_n > 999 -> "999+"; T_n == 999 -> "999";
  T_n < 999 -> exact T_n). Any mismatch = FAIL. OLD labels recorded;
  any OLD mislabel (label "999+" with T_n <= 999, or "999" with
  T_n > 999) is reported honestly as a found fixture, or reported as
  not found.

**Verdict rule:** H-SEG5 SURVIVES iff all five bars PASS.
Classification: bounded L2 structural learning repair (provable
honesty of a saturation label). Not L3: MAXL=5, MINC=2, containment
family, len^2, FBPEN=20 remain authored; the sentinel bound is
instance-derived; the sat proof is about label honesty, not invention.

## Honest limits (frozen)

1. The proof covers label honesty only. DP time O(n*nch), memory O(n)
   remain allocation-bound (engineering, not correctness).
2. The count above 999 remains unrecoverable by the mechanism (the REF
   DP is an adversary instrument, not part of the learner).
3. The genuine-morpheme-inside-longer-chunk discount boundary is
   unchanged from H-SEG3.
4. enum_bwd host-stack recursion bound unchanged.
5. If the K-SG5-5 search finds an OLD-mechanism mislabel fixture, it is
   a demonstration against the SUPERSEDED mechanism only; the NEW
   mechanism is covered by proof, not by the search.

## Governance (frozen)

- Prereg committed alone before any implementation edit, build, or run.
- Pure Zag: fixtures, builds, runs, greps, md5, cmp. No Python anywhere.
- Only H-SEG5-owned files staged. No binaries committed (builds in /tmp).
- seg4_learn.zag and all prior evidence untouched.
- No em dashes in loop documentation.
