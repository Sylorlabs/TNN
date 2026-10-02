# PREREG H-SEG5 RED TEAM FROZEN

**Date:** 2026-09-29
**Researcher:** H-SEG5 Red Team (subagent)
**Target:** H-SEG5 SURVIVES (5/5). Per-position saturation propagation
with frozen induction proof. seg5_learn.zag, SEG5_RESULT.md,
SEG5_RAW_OUTPUT.txt, seg5_diff.zag, SEG5_DIFF_RAW.txt.
**Status:** FROZEN. Committed alone before any attack fixture, build,
or run. Pure Zag. No Python. No em dashes in loop documentation.

## Mission

Assume the H-SEG5 claim is false. Four preregistered attacks. If any
attack meets its kill criterion, H-SEG5 is KILLED or DOWNGRADED.
Report honestly including failed attacks.

## Attack X-SG5-1: Proof audit (induction)

**Method:** Step-by-step audit of the frozen proof in PREREG_SEG5.md
against the actual `relax` code in seg5_learn.zag. Check:
(a) base case nopt[0]=1, sat[0]=0;
(b) the ordering claim (all relaxes into i come from p < i, so
nopt[i]/sat[i] final when i is processed as source);
(c) strict-improvement reset matches the proof's "discard earlier
accumulations" (sat[np] := sat[i] valid only because the new
OptMoves_np is the singleton {(i,m)} and nopt[i] <= 999 so CF=0);
(d) tie accumulation computes the running sum over exactly the final
OptMoves_np (no double-counting of any (p,m), no stale level mixing);
(e) clamp monotonicity (running v exceeds 999 iff final sum > 999);
(f) Claim A and Claim B logic, including the corrected backward
direction;
(g) the label theorem's three cases against the actual label code.

**Kill criterion:** Identify a specific logical gap: a wrong base
case, an invalid IH application, an ordering violation constructible
in the code, a counterexample to Claim A or Claim B, or a label-code
path the theorem does not cover. A vague "the proof is hard to read"
is not a kill.

## Attack X-SG5-2: Differential fuzz, real relax vs brute force

**Method:** Build a harness in /tmp (never committed) containing:
(a) the REAL `relax` function copied byte-verbatim from committed
seg5_learn.zag (verified by cmp of the extracted function text);
(b) an INDEPENDENT brute-force reference that does NOT use DP
counting: enumerate all segmentations of small inputs, compute each
segmentation's score from the same chunk table, find the max score,
count exact optimal tilings T_n by enumeration, and derive the honest
label directly (T_n > 999 -> "999+"; T_n == 999 -> "999"; else T_n).
Fuzz over small random corpora and test strings (lengths 2..14,
alphabets {a,b} and {a,b,c}, several LCG seeds) plus the frozen H1
corpus on short "ab" repetitions. For every case compare the real
mechanism's (nopt[n], sat[n], label) against brute-force truth.

**Kill criterion:** Any case where nopt[n] != min(T_n,999), or
(nopt[n]==999 and sat[n]==1) with T_n <= 999, or (nopt[n]==999 and
sat[n]==0) with T_n != 999, or the printed label disagrees with the
honest label. One reproducible case kills.

## Attack X-SG5-3: Targeted tie/reset stress

**Method:** Hand-construct small lexicons and inputs that maximize
adversarial interactions in `relax`:
(a) positions receiving many ties from predecessors with MIXED sat
values (some sat=1, some sat=0);
(b) strict-improvement resets interleaved with tie accumulations,
where the reset source and the tied sources have differing sat;
(c) a reset that discards a previously saturated accumulation, then
re-saturates (or not) via later ties;
(d) multiple optimal moves from the SAME source (fallback + chunk
tying).
Verify each against the brute-force reference from X-SG5-2.

**Kill criterion:** Same as X-SG5-2: any reproducible disagreement
between the real mechanism and brute-force truth on a targeted case.

## Attack X-SG5-4: Regression and silent-change audit

**Method:**
(a) Rebuild committed seg5_learn.zag with znc 2026.07.0-dev, run 3x,
cmp against committed SEG5_RAW_OUTPUT.txt (must be byte-identical);
(b) re-verify diff seg4_learn.zag -> seg5_learn.zag contains only the
five frozen R1 edit groups (no other logic changes);
(c) verify the harness's `relax_new` in seg5_diff.zag is logic-identical
to seg5_learn.zag's `relax` (comment-only differences allowed);
(d) confirm nopt identity OLD vs NEW on the fuzz battery (count logic
unchanged; only sat plumbing differs).

**Kill criterion:** Any byte-difference in (a) not explained by
banners, any non-frozen logic change in (b), any logic difference in
(c), or any nopt difference in (d).

## Verdict rule

H-SEG5 is KILLED if any attack meets its kill criterion with a
reproducible case. H-SEG5 is DOWNGRADED if an attack reveals a
material weakness that does not break the frozen 5/5 bars (e.g. a
proof gap that does not yield a failing case, or a boundary narrower
than claimed). Otherwise H-SEG5 SURVIVES this red team.

## Governance

- Prereg committed alone before any attack code, build, or run.
- Pure Zag: fixtures, builds, runs, greps, hashes, cmp. No Python.
- Attack harnesses live in /tmp only; only the prereg, result report,
  and raw evidence are committed, on adversary-owned paths.
- Target binary built from committed seg5_learn.zag, verified
  unmodified (cmp against git show).
- On .git/index.lock contention: wait, never remove.
