# REDTEAM_REVIEW: independent red-team review of RESULT_DEVANG2.md

Wave: wave-20261001-1721pdt. Lane: docs/lab/rsi/runs/wave-20261001-1721pdt/DEVANG2/
Reviewer role: independent red team (no implementation, no re-test; artifact
and source verification only). Pure Zag toolchain guard held throughout
(safebin PATH, no Python invoked, no .py files in lane).
Prereg under review: commit a2b567de5 (PREREG_DEVANG2.md, frozen before
implementation). Result under review: RESULT_DEVANG2.md, verdict BUILD-FAIL.

## Verdict: EVIDENCE HOLDS

The BUILD-FAIL verdict is correct under the frozen bars. The cold-start
hypothesis is genuinely falsified, and the falsification is stronger than
the result document states: the branch was architecturally incapable of
moving K1, not merely empirically inert. No confound, metric gaming, or
bar misapplication was found. One process observation (owned-path label)
is noted below; it is not a bar violation.

## 1. Cold-start hypothesis: genuinely falsified, confounds refuted

The prereg hypothesis (section 2): crash fix plus a minimal cold-start
tie-break is sufficient for K1 (word discovery) to recover. The result
reports K1 stayed at 3/10, with mechanism numbers byte-identical to the
no-cold-start overnight run (K1 3/10, train 43/100, test 13/20, C2 17/20).

I attacked each candidate confound by source inspection of devang2.zag:

(a) Temporary debug build (deleted, /tmp only). Its claim, that the
cold-start branch fires exactly once at t=0, is independently provable
from the frozen source and does not depend on the deleted build.
`bigram_total` sums the 676 bigram i32s at W[0..2704); W is freshly
allocated and zeroed, so at t=0 the total is 0 and `seg_online` returns
single-character segments without calling the DP. `learn_update` step 1
then adds bigrams, so the total is nonzero for every t>=1, and the test
loop (t=100..119) sees the full training total. The branch fires exactly
once, at t=0, by construction. The deleted build is corroborating, not
load-bearing.

(b) Ported baseline. I diffed the lane's devang2.zag against the
overnight implementation (commit 153e2af8e). The delta is exactly: header
comment updates, the `bigram_total` + `seg_online` block (32 lines), and
two call-site swaps (`seg_dp` to `seg_online` at the training and test
loops). 68 diff lines, all accounted for. The port is exact; there is no
hidden deviation that could suppress scores.

(c) The bigram_total==0 branch. It is live code (not dead), reachable,
and fires as claimed. Its downstream inertness is also provable, and
this is the stronger finding: `learn_update` step 1 counts bigrams from
the raw utterance bytes (`ep[48+k]`, `ep[48+k+1]`), never from the
segmentation. The DP's only inputs are those bigram counts. Therefore
segmentations at t>=1 are identical between the two variants, and the
only lexicon difference is the t=0 residue (single characters vs one
whole-utterance pseudo-word). Both residues are inert: single characters
cannot match any true word (all are 3-5 bytes) and stay at count 1, below
the grounding threshold of 2, so they never influence interpretation,
negator/comparative statistics, or the K1 snapshot; the overnight
pseudo-word likewise never recurs. Byte-identical downstream scores are
the necessary consequence of the code, not a coincidence. The
hypothesis was not just false but untestable in this architecture: no
t=0-only segmentation change could ever move K1, because the statistics
that drive the DP never depended on segmentation. Falsification stands,
with an architectural explanation that subsumes the result document's
DP-default account.

(d) Nondeterminism accidentally reproducing overnight numbers. Refuted:
3/3 runs byte-identical (independently verified, sha256
94856b34dfa590e1b2fee9aed5c34f253068c5b0915dffeb312edc26896ac564),
seeded LCG, no wall-clock; and the cross-binary reproduction (overnight
binary vs rebuilt new binary) matches exactly what the inertness proof
predicts.

## 2. Killing evidence: follows from the recorded runs

RUN1.out, RUN2.out, RUN3.out each contain exactly the table in
RESULT_DEVANG2.md (K1 3/10, K2 5/6, K3 1/3, K4 3/3, K5 1/3, K6 3/3,
K7 0/2, K9 6/10, train 43/100, test learner 13/20, C1 4/20, C2 17/20,
C3 0/20, K8 0 with best_c=17, sub-bars 3/7, BUILD-FAIL). I verified:
`cmp` clean 3/3, sha256 identical and equal to the recorded hash,
RUN1..3.err all 0 bytes, exit 0 assumed from the record and consistent
with outputs existing. The binary's own bar logic (emit section) applies
the prereg thresholds exactly (>=8, >=5, >=2 x4, >=1, >=7; K8 as
(test-best)*5>=15 percentage points; verdict requires K1, K8, sub>=4).
K1 FAIL (3<8), K8 FAIL (-20pp<15pp), sub-bars 3/7<4: BUILD-FAIL is
triply determined. Binary identity confirmed: the lane's `devang2`
binary (sha256 81a872abaac6f2c7b0f47d57a4847c36bd377942e157f881038afad6dfacdef1)
is byte-identical to my fresh deterministic rebuild from the lane's
devang2.zag. The overnight comparison numbers (3/10, 43/100, 13/20,
C2 17/20) were confirmed in commit 153e2af8e's RESULT_DEVANG2.md.
Alternative explanations (copied numbers, dead branch, broken port)
are refuted by the artifact evidence above.

## 3. Frozen bars: applied correctly

Walked against prereg section 6 and the verdict rule:

- KR0: PASS. 3/3 runs completed, exit 0, zero stderr bytes (verified).
- K1: 3/10 vs >=8/10: FAIL, correctly. Snapshot taken at t==59 after
  update (end of phase 1, 60 episodes), per prereg 4.1.3; the 10 checked
  ids [0,1,2,3,5,6,7,9,10,11] have lengths 3,3,3,3,3,3,3,3,5,4 per
  `word_len`, matching the prereg word list (tak,not,red,blu,bal,sph,
  cub,big,biger,smal) with ids 4,8 as phase-2 words. Word bytes come from
  the generator, not source constants.
- K2..K7, K9: thresholds applied exactly as frozen; PASS/FAIL mapping
  correct (K2 5/6 PASS, K3 1/3 FAIL, K4 3/3 PASS, K5 1/3 FAIL,
  K6 3/3 PASS, K7 0/2 FAIL, K9 6/10 FAIL). Group-to-episode mapping in
  the test loop matches the prereg's novel-composition sets; K9 counts
  t=90..99, the last 10 phase-2 episodes, correctly.
- K8: learner 13/20 vs best control C2 17/20, diff -20pp vs required
  +15pp: FAIL, correctly.
- K10: PASS by audit, re-verified independently. Training loop order is
  segment (seg_online) -> lex lookup/add -> interpret -> learn_update;
  test loop calls seg_online + interpret only, no learn_update.
- K11: PASS by audit, re-verified independently. Bigram counts update
  inside learn_update step 1, strictly after episode t's segmentation;
  the cold-start branch reads pre-update totals (episodes 0..t-1 only).
- K12: PASS. 3/3 byte-identical outputs, sha256 recorded and
  independently re-verified.
- Verdict rule (KR0, K1, K8, K10, K11, K12 plus >=4 of K2..K7,K9):
  K1 FAIL and K8 FAIL each independently force BUILD-FAIL; sub-bars 3/7
  is a third independent failure. Verdict correct.

Process observation (not a flaw): the prereg's section 9 names the owned
path as the 1421pdt devang2/ directory, while this implementation lives
in the 1721pdt DEVANG2/ lane. No frozen bar governs the lane path, and
commit-order prereg-before-implementation holds (a2b567de5 predates all
lane files; the 1421pdt lane contains only the prereg and NAMECHECK, no
competing implementation). Safe to note, nothing to correct.

## 4. Metric gaming and knowledge-vs-architecture: none found

- No hardcoded word strings, negator strings, or comparative strings in
  source (grep for "tak","not","biger","red","blu" returns nothing; the
  negator/comparative detectors are statistical tests over segment
  pairs, per prereg 4.5/4.6).
- The learner loses to the trivial fixed-width-3 control (13/20 vs
  17/20); a gaming implementation would not leave its headline metric
  below a no-learning baseline.
- K1 is measured from an in-loop snapshot at t=60, not cherry-picked
  post-training state; the fallback path is documented and unreachable
  in practice.
- Classification as developmental L2 (structural learning attempt), not
  L3, matches the prereg's honest-boundaries section; no L3, generality,
  or transfer claim is made.
- K10/K11 rest on code audit, which I re-performed independently rather
  than trusting the builder's; both hold.
- Lane hygiene: zero em-dash bytes in lane files, zero .py files, no
  Python invoked (safebin guard), no git commits by the worker.

## Residual notes for the parent

1. The result document's causal account (DP single-segment default at
   t>=1) is correct but incomplete; the deeper cause is that bigram
   learning reads raw utterance bytes and is segmentation-independent,
   which made the cold-start repair architecturally inert. Recommend the
   DEVANG3 line treat segmentation-dependent statistics as a design
   requirement, not just a scoring-function fix.
2. The deleted debug build means the "fires exactly once" claim rests on
   my inspection rather than a preserved artifact. The inspection is
   decisive, but future workers should keep instrumented builds until
   the wave record is committed.
3. Nothing in this review weakens the BUILD-FAIL or reopens any bar.
