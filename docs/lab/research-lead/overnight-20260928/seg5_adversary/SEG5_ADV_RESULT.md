# SEG5 ADVERSARY RESULT: H-SEG5 Red Team Report

**Date:** 2026-09-29
**Researcher:** H-SEG5 Red Team (subagent)
**Prereg:** seg5_adversary/PREREG_SEG5_ADV.md (commit 1fea0fb6f,
frozen before any attack code, build, or run)
**Target:** seg5_learn.zag (committed, verified unmodified via cmp
against git show)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python at any stage.

## Verdict: H-SEG5 SURVIVES this red team

All four preregistered attacks failed to meet their kill criteria.
No reproducible counterexample, no proof gap, no regression, no
silent change. The 5/5 H-SEG5 survival claim stands.

## X-SG5-1: Proof audit -- FAILED (no flaw found)

Conducted an exhaustive step-by-step audit of the frozen induction
in PREREG_SEG5.md against the actual `relax` code:

(a) **Base case:** nopt[0]=1=min(T_0,999), sat[0]=0, T_0=1 not > 999.
Holds.

(b) **Ordering:** Every relax targeting position i comes from a
source p with p = i - len(m) < i (all moves advance >= 1: fallback
len 1, chunks len >= MINC = 2). The main loop processes sources in
increasing order, so when iteration i begins, all relaxes into i are
complete and nopt[i]/sat[i] are final. Verified in code: the main
loop reads dpi/nopt[i]/sat[i] once per iteration, and relax only
writes positions np > i. Airtight.

(c) **Strict-improvement reset:** On ns > cur, the code sets
nopt[np] := nopt[i], sat[np] := sat[i], and resets the move list.
This is correct because the new OptMoves_np is the singleton
{(i,m)} and nopt[i] = min(T_i,999) <= 999 by IH, so the clamp
factor CF = 0 and sat[np] = sat[i] matches the proof formula.
Earlier accumulations are correctly discarded (they scored lower).

(d) **Tie accumulation:** On ns == cur, the code adds nopt[i] to the
running sum. Verified: each (p,m) pair is relaxed exactly once
(fallback once per i; each chunk-table entry visited once per i;
the table deduplicates by (len,bytes) so no two entries represent
the same move). The running sum therefore equals the sum over
exactly the final OptMoves_np. No double-counting, no stale-level
mixing (resets clear on strict improvement).

(e) **Clamp monotonicity:** The running sum v only grows (adding
non-negative nopt values), so v exceeds 999 at some step iff the
final unclamped sum > 999. The sat bit is set exactly in this
case. Verified.

(f) **Claim A / Claim B:** Both verified logically, including the
corrected backward direction of Claim B (the "some T_p > 999"
case discharged by IH, not by the clamp). No gap.

(g) **Label code:** The three cases (no<999 exact; no==999,sat=1
-> "999+"; no==999,sat=0 -> "999") match the label theorem. The
code reads sat[n*4] (per-position), not the old per-run flag.
Verified.

**No logical gap found.** The induction is valid.

## X-SG5-2: Differential fuzz -- FAILED (0 disagreements)

Built a harness (/tmp/sg5adv, never committed) with the REAL
`relax` copied byte-verbatim from committed seg5_learn.zag and an
INDEPENDENT brute-force reference that enumerates all segmentations
(no DP counting whatsoever), computes each score from the same
chunk table, finds the max, and counts exact optimal tilings.

**Random fuzz:** 240 cases (6 corpus families x 40 tests, lengths
2..14, alphabets {a,b} and {a,b,c}, LCG seeds). Compared
mechanism (nopt[n], sat[n]) against brute-force truth on every
case. **0 disagreements.** The counting logic is exactly right.

**H1 saturation family:** Brute-force confirms T = 2^(k-1) for
"ab" x k at k = 1..7 (T = 1,2,4,8,16,32,64), mechanism matches
exactly with sat = 0. At k = 10 (T = 512 <= 999): mechanism gives
nopt = 512, sat = 0. Correct. At k = 11 (T = 1024 > 999, brute
force infeasible at n = 22): mechanism gives nopt = 999, sat = 1.
Correct. The saturation boundary is exact.

**Honest limitation:** Brute-force enumeration cannot reach sat = 1
(exponential blowup; T > 999 requires n >= 22 on the H1 family).
Sat = 1 is validated via the analytical H1 family (pattern verified
for k = 1..7, mechanism checked at the k = 10/11 boundary), not by
brute force. The proof covers the general case.

## X-SG5-3: Targeted tie/reset stress -- FAILED (0 disagreements)

The tie-branch sat propagation (`sat[np] |= sat[i]`) and the
strict-improvement reset (`sat[np] := sat[i]`) were stress-tested
via:
(a) the 240-case random fuzz, which naturally generates tie-heavy
and reset-heavy DPs;
(b) the H1 family, which exercises deep tie chains with saturation;
(c) manual code review of the four interleavings (strict-then-tie
with sat 0/1 in each position).

No targeted case produced a disagreement. The reset correctly
discards saturated accumulations when a strictly better score
arrives, and the tie branch correctly ORs saturation along optimal
predecessors only. (Same honest limitation as X-SG5-2: sat = 1
cannot be brute-forced at small n.)

## X-SG5-4: Regression and silent-change audit -- PASSED (defense holds)

(a) Rebuilt committed seg5_learn.zag: 3/3 runs byte-identical (cmp),
and byte-identical to committed SEG5_RAW_OUTPUT.txt. Determinism
holds.

(b) Diff seg4_learn.zag -> seg5_learn.zag contains exactly the five
frozen R1 edit groups (header comment, strict-branch sat copy,
tie-branch sat OR + per-position clamp, (n+1)-cell sat array,
sat[n] label, banner strings). No other logic changes.

(c) The harness's `relax_new` (seg5_diff.zag) is logic-identical to
seg5_learn.zag's `relax`; diff shows comment-only differences.
The K-SG5-5 battery therefore validates the real mechanism logic.

(d) H1-T prints "SCORE 0 NOPT 999+" as required. The 2^29 correction
is present; remaining "1346269"/"Fib(31)" mentions sit inside
explicit SUPERSEDED notes with lineage. K-SG5-1 holds.

## Governance disclosures

- Prereg committed alone (1fea0fb6f) before any attack work.
- Target binary built from committed seg5_learn.zag, verified
  unmodified (cmp against `git show HEAD:...`).
- All attack harnesses in /tmp/sg5adv only; never committed.
- Pure Zag throughout. No Python.
- No .git/index.lock issues encountered.

## Files

- docs/lab/research-lead/overnight-20260928/seg5_adversary/PREREG_SEG5_ADV.md
  (commit 1fea0fb6f)
- docs/lab/research-lead/overnight-20260928/seg5_adversary/SEG5_ADV_RESULT.md
  (this file)

## Recommended follow-ups (for the parent, not this lane)

1. The proof is now both reviewer-checked (builder) and
adversary-audited (this red team). A machine-checked proof remains
out of scope for the Zag toolchain.
2. The H-SEG5 line still needs to reach the research paper (paper
lane).
