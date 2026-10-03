# PREREG_DEVANG6 (frozen): FINREG under the recalibrated K_ABL

**Status:** FROZEN. Committed ALONE before any DEVANG6 implementation
exists and before the Family E-prime baseline measurement.
**Date:** 2026-10-02.
**Wave:** wave-20261002-1121pdt.
**Lane:** DEVANG6.
**Owned path:** `docs/lab/rsi/runs/wave-20261002-1121pdt/devang/`

## 1. Disambiguation

DEVANG5 (wave-20261002-0521pdt) ended BUILD-FAIL on a single bar:
K_ABL leg 1 (fixed-width-3 ablation 6/12 > frozen 5/12). Every other
frozen bar passed (KR0, K1, K_SEG 12/12, K_SEAL 14/20, K_DISC 6/6 vs
2/6, K_AUD, K_C0, K8, K2..K7/K9 7/7, K10, K11, K12, K_DELTA). The
failure was classified, with evidence, as BAR-MISCALIBRATION (the
<= 5/12 threshold was copied from DEVANG4's prereg without adjusting
for B-doubleprime's 3-char-heavy word composition, which handed the
fixed-3 null six free utterances), not a mechanism defect. The
full derivation is frozen in RECALIBRATION_K_ABL.md (same commit as
this prereg). DEVANG6 re-tests the VALIDATED FINREG mechanism under
the RECALIBRATED K_ABL on FRESH sealed families. No mechanism change
is attempted; the mechanism is carried forward with provenance
(section 3). If DEVANG6 fails the recalibrated bar, that is
informative: the bar is not re-tuned.

## 2. The design: FINREG carried forward (frozen)

The learner-path segmenter is POSSEG exactly as frozen in
PREREG_DEVANG5.md section 3 (beam B=6 over the 2321pdt
lexicon-frequency scoring, reranked by
`joint(c) = lexScore(c) + 25*margin(c)*scn - 5*nseg(c) + finalTerm(c)`
with `finalTerm(c) = +-4*r`, `r = ilog(FIN_KNOWN+1) -
ilog(FIN_NOVEL+1)` clamped >= 0, FIN_KNOWN/FIN_NOVEL at W+7392/W+7396
written at exactly one site: the top of learn_update, from the
chosen segmentation, before the current episode's count bumps).
Frozen parameters unchanged: B=6, MARGIN_W=25, SEG_W=5, FW=4,
cold-start threshold nlex<10, max segment length 16.

Provenance: devang6.zag is the frozen DEVANG5 source
(`docs/lab/rsi/runs/wave-20261002-0521pdt/DEVANG/devang5.zag` on
branch lane-devang-20261002-0821pdt, sha256
`5736f00eac4400688a9d3442d5dc726ab77a9812d8b1b5edaff26dffa66456ce`)
with ONLY banner/usage strings renamed (devang5 -> devang6). No
behavioral delta is permitted; K_SAME (section 10) governs. Rationale
for carry-forward over re-derivation: the mechanism was validated
(K_DISC 6/6, K_SEG 12/12, K_AUD pass); re-deriving from devang4.zag
would risk accidental delta with zero information gain.
Carry-forward with recorded provenance plus behavioral-identity
verification is the honest minimal path.

## 3. Why this wave is a bar test, not a mechanism test

The DEVANG5 red-team's strongest remaining attack on FINREG (narrow
prior; C-doubleprime tie with C2; r saturates) is NOT in scope for
DEVANG6. DEVANG6 decides one question: does the FINREG front-end
pass the CORRECTED load-bearing bar on fresh data? The
recalibration analysis (RECALIBRATION_K_ABL.md) argues the corrected
bar from the bar's purpose: (a) the gap (learner minus ablation) is
the direct measure of load-bearing; (b) the new bar is stricter
than the old bar against non-load-bearing front-ends (old leg 1
passed learner 6/12 + ablation 5/12, gap 1; the new bar fails it);
(c) the >= 4 threshold sits two points below the observed DEVANG5
gap (6), the documented anti-fit margin; (d) calibrated on old
data, decided on fresh data. Mechanism generalization (more
positions, conditional on utterance shape) stays queued.

## 4. Old-language impossibility proof (carried, re-tested)

For the E-prime probes (section 5), the wrong analysis
`[tak][W_emb][XY+D]` beats the true analysis `[tak][N][D]` on
lexicon score outright (40+20-55=5 vs 40-55+10=-5, by the frozen
Family A lexicon arithmetic: tak 40, W_emb 20, D 10, novel 5-char
segment -55) and ties it on interpretation margin (2 vs 2) and on
segment count. Hence the wrong analysis is a fixed point for EVERY
per-episode signal computed from (utterance, scene, current
lexicon): no reweighting of the old signal classes can rank the
truth first. A segmenter restricted to the old language (the
DEVANG4 signal classes: lexicon-frequency, interpretation margin,
segment count) CANNOT discriminate these probes as a matter of
arithmetic, not tuning. The distinguishing information must come
from a cross-episode induced signal class. POSSEG's finalTerm is
such a class (computed from FIN_KNOWN/FIN_NOVEL, unreadable by any
prior segmenter, developmental: near 0 at cold start). The proof
is analytic (the arithmetic above) plus empirical (the frozen
devang4 binary premise, section 6). This is the impossibility
proof the red team must try to break: to defeat it, show a
configuration of the OLD signal classes that ranks the truth
first on E-prime, or show POSSEG's E-prime wins do not come from
the finalTerm.

## 5. Family E-prime: the fresh held-out discriminator (frozen, explicit)

Six scene-mode episodes, frozen here before implementation. Same
construction PRINCIPLE as DEVANG5 Family E, all six (W_emb, XY, D)
tuples fresh (XY forms qa, zo, fi, we, ja, hu are absent from
Family A, from B-tripleprime roots, and from C-tripleprime
vocabulary; the novel N forms coincide with no Family A word).
Scene prefixes reuse the DEVANG5 E-line role patterns verbatim
(same (W_emb, D) role pairs, so scene votes and the 2v2 margin tie
are unchanged; only the novel surface forms differ). Format:
`<c0> <s0> <z0> <c1> <s1> <z1> <c2> <s2> <z2> <tgt> <utterance>`.
Key for every probe: `3,8` ([tak][N][D]).

- E1p: `2 2 1 0 1 0 1 0 0 0 takcubqagrn` (W=cub, XY=qa, D=grn)
- E2p: `1 0 1 0 2 0 2 1 0 0 takredzobal` (W=red, XY=zo, D=bal)
- E3p: `0 0 1 1 2 0 2 1 0 0 takblufisph` (W=blu, XY=fi, D=sph)
- E4p: `1 2 1 2 1 0 0 0 0 0 takcubwetri` (W=cub, XY=we, D=tri)
- E5p: `2 0 1 0 1 0 1 2 0 0 takredhugrn` (W=red, XY=hu, D=grn)
- E6p: `2 0 1 1 1 0 0 2 0 0 takblujabal` (W=blu, XY=ja, D=bal)

The builder may not adjust the design, parameters, or code in
response to Family E-prime behavior. Predicted POSSEG joints
(r=4): truth 46 vs wrong 24 on every probe, by the identical
DEVANG5 arithmetic; the implementation, not the prediction, is
under test.

## 6. Baseline protocol (post-freeze, pre-implementation)

After this prereg is committed and BEFORE any DEVANG6
implementation exists, the builder writes
`baseline/familye2_eps.txt` (sealc format: `0 6` header plus the
six section-5 lines, copied verbatim) and runs the FROZEN DEVANG4
binary (`docs/lab/rsi/runs/wave-20261002-0221pdt/DEVANG/devang4`
on branch lane-devang-20261002-0821pdt, sha256
`cfba24f157a22b0e721f9a27722320f6b2d3a77e250b96c9045659b58bb9ddbd`,
hash verified before the run) in `segb-scene` mode on it, 3/3
runs, recording the exact-boundary score. The premise for K_DISC
is baseline <= 2/6. This is a measurement of an old frozen binary,
not DEVANG6 development.

## 7. Seal protocol for the fresh families (self-seal, solo worker)

Same solo approximation as DEVANG5, documented honestly as weaker
than an independent adversary:

1. This prereg freezes the generator specifications (section 8),
   including word lists, pattern sets, episode counts, and seeds.
2. After implementation, the builder writes `genseal6.zag`
   implementing exactly the frozen specs (scene generators copied
   verbatim from genseal5.zag; only word tables and seeds change).
3. The builder validates the generator with ALTERED seeds into
   /tmp (format checks, spec-compliance checks including the
   section-8 fairness floor, and a solvability smoke test on
   throwaway sets; output discarded, never the sealed content).
   Spec-compliance bugs may be fixed; the spec itself may not be
   changed in response.
4. The builder runs the frozen seeds once, producing `sealed6/`
   files plus key files.
5. The builder records sha256 of every sealed file and commits the
   sealed package BEFORE any sealed run.
6. The builder never READS sealed file contents or key files (no
   cat, less, editor opens, or pager views). Scoring is mechanical:
   a Zag scorer prints only aggregate scores. Any read voids the
   seal (governance VOID).
7. Limitation: the builder authored the generator. The prereg-frozen
   spec plus hash-before-run plus no-read is the solo approximation.
   Independent-adversary replication of K_SEG/K_SEAL/K_ABL is queued
   as follow-up. The discrimination claim (K_DISC) does not depend
   on the sealed families: Family E-prime is prereg-explicit and the
   baseline is measured on a frozen binary.
8. Prior sealed sets (DEVANG3 B/C, DEVANG4 B-prime/C-prime, DEVANG5
   B-doubleprime/C-doubleprime) may be used ONLY as regression
   checks, never as the decision set.

## 8. Generator specifications (frozen)

Family B-tripleprime (held-out segmentation probes, utterance-only):
- 10 fresh roots (frozen list): zib(3), zibok(5), vum(3),
  vumil(5), dax(3), odax(4), kex(3), kexal(5), nim(3), anim(4).
  Prefix pairs sharing >= 2: (zib,zibok) "zi", (vum,vumil) "vu",
  (kex,kexal) "ke". Suffix pairs sharing >= 2: (dax,odax) "dax",
  (nim,anim) "nim", (vumil,kexal) "il".
- 12 utterances from LCG seed 888021 (fresh: 888001 was DEVANG5
  frozen; 888011/888012 were DEVANG5 altered-validation): 4x
  K+N+K, 4x K+N, 4x N+K, where K is drawn (seeded) from {tak, red,
  blu, grn, bal, sph, cub, smal, big, not} and N is drawn (seeded)
  from the roots. Every utterance contains EXACTLY ONE novel root
  and at least one known word. All utterances 4..20 chars.
- The generator enforces (seeded, deterministic, same style as
  genseal5): at least 2 utterances exercise a prefix pair and at
  least 2 exercise a suffix pair.
- FAIRNESS FLOOR (new, frozen): at least 4 of the 12 utterances
  contain a word of length != 3. Enforced deterministically after
  the pair enforcement: count utterances where the novel root
  length != 3 or a known word is smal (4 chars); while the count
  is < 4, set the novel root of the next seeded slot currently
  holding a 3-char root to a seeded choice from the non-3-char
  roots {zibok, vumil, odax, kexal, anim}. By the lemma in
  RECALIBRATION_K_ABL.md section 6, fixed-3 is provably wrong on
  those utterances, so ablation <= 8 and the K_ABL gap bar is
  satisfiable. This is a generator-validity condition, not a kill
  bar.
- Key file: `<utt> => <b1>,<b2>,...` true boundaries (1-based
  segment ends excluding utterance end).
- Solvability note (design rationale, not a bar): with exactly one
  novel root per utterance anchored by known words, the lexicon DP
  favors the true analysis; the finalTerm only strengthens it. No
  utterance presents an information-less parse.

Family C-tripleprime (post-freeze adversarial, new surface
vocabulary):
- 11 fresh words with frozen roles: action "quz"(3); negator
  "noba"(4); colors "rak"(3) [=red], "bilo"(4) [=blu], "up"(2)
  [=grn]; shapes "tov"(3) [=ball], "meka"(4) [=cube], "flib"(4)
  [=tri]; sizes "zora"(4) [=big], "pleto"(5) [=smal], "zoraxu"(6)
  [=biger]. No Family A forms, no C-prime forms, no
  C-doubleprime forms. Word lengths 2..6 with a different length
  distribution than Family A and both prior C families.
- Templates (same semantics as Family A, new forms): DIRECT
  "quz <color> <shape>"; NEG "quz noba <color>"; REL "quz zoraxu
  <shape>"; SIZE "quz <size> <shape>". Scene generation mirrors
  the Family A gen_direct/gen_neg/gen_rel/gen_size distributions
  (verbatim copies).
- 40 train episodes (16 DIRECT, 10 NEG, 7 REL, 7 SIZE), 20 test
  episodes (8 DIRECT novel, 4 NEG novel, 4 REL novel, 4 SIZE novel;
  novel = color+shape combos absent from training; at least 4 test
  utterances exercise the zora/zoraxu prefix ambiguity). LCG seed
  888022 (fresh by the same rule as 888021).
- File format: sealc format (`<ntrain> <ntest>` header, then
  episode lines).

## 9. Sealed interface (harness, frozen)

The binary keeps the DEVANG5 argv interface (fama, segb, segb-abl,
segb-scene, sealc, sealc-fresh with learner|c0|c2|c1|c3 variants).
No behavioral change is permitted (K_SAME). One mechanical scorer
`scoree.zag`: reads a segb-scene output file and a key file,
prints only the aggregate exact-boundary score (`E: x/6`). Scoring
aid only; may be carried forward from DEVANG5's scoree.zag
(behavioral identity verified, not re-derived).

Controls frozen: C0 = raw-byte bigram statistics + `seg_dp_raw`
(the DEVANG2 failure-mode architecture); C2 = fixed-width-3
(`seg_fixed3`, doubles as the K_ABL ablation); C1/C3 unchanged.

## 10. Frozen kill bars (exact numeric thresholds)

- **KR0 (crash regression, hard gate):** Family A, 3/3 runs
  complete, exit code 0, zero stderr bytes each, no panic or trap.
  Violation = BUILD-FAIL regardless of all other bars.
- **K1 (lexicon discovery):** >= 8 of the 10 phase-1 true words
  present as exact lexicon entries in the t=60 snapshot.
- **K_SEG (segmentation quality):** >= 10/12 sealed Family
  B-tripleprime utterances segmented with exact true boundaries.
- **K_SEAL (post-freeze adversarial):** learner accuracy >= 12/20
  on sealed Family C-tripleprime test episodes via `sealc-fresh`
  (learner variant). C0, C1, C2, C3 accuracies reported alongside.
  Threshold EQUAL to DEVANG5's (not lowered; raising would be
  dishonest since the new signal is neutral on all-novel
  vocabulary; the C-doubleprime caveat carries over).
- **K_DISC (mechanism discriminator):** (a) the frozen DEVANG4
  binary scores <= 2/6 exact-boundary on the Family E-prime
  episodes via `segb-scene` (premise, measured post-freeze per
  section 6); (b) DEVANG6 scores >= 5/6 exact-boundary on the
  Family E-prime episodes via `segb-scene`. Both conjuncts
  required. If (a) fails, K_DISC fails with classification
  "discrimination premise failed".
- **K_AUD (segmentation-dependence audit, governance):**
  independent code inspection PASS on all five DEVANG5 claims:
  (a) every statistics table (lexicon counts, grounding, negator,
  comparative, FIN_*) is updated only from the chosen
  segmentation's output; (b) no code path reads raw utterance
  bytes into any statistics table on the learner path; (c) the
  cold-start path is inside the segmenter and feeds the same
  statistics update as later episodes; (d) the scene/margin/
  finalTerm signals are confined to candidate scoring (zero W
  writes in any scoring path) and the chosen segmentation is the
  sole statistics input; (e) FIN_KNOWN/FIN_NOVEL are written at
  exactly one site (learn_update top, pre-bump lex-count test)
  and nowhere else. Any violation = BUILD-FAIL, classified as
  DEVANG2-mode recurrence.
- **K_ABL (ablation, load-bearing front-end; RECALIBRATED):**
  leg 1: (learner K_SEG - ablation K_SEG) >= 4 on sealed Family
  B-tripleprime, where the ablation is seg_fixed3 via `segb-abl`;
  leg 2: (learner K1 - ablation K1) >= 2. Both legs required. If
  the ablation passes either leg (gap < 4, or K1 gap < 2), the
  front-end is not load-bearing = BUILD-FAIL. Rationale frozen in
  RECALIBRATION_K_ABL.md: the gap is the direct measure of
  load-bearing; the bar is stricter than DEVANG5's against
  non-load-bearing front-ends and is not fit to the DEVANG5
  observation (2 points of slack).
- **K_C0 (trap exclusion):** control C0 must trail the learner by
  >= 15 percentage points on Family A test accuracy AND by >= 3
  words on K1.
- **K2..K7, K9:** K2 DIRECT novel >= 5/6; K3 NEG novel >= 2/3;
  K4 REL novel >= 2/3; K5 SYN novel >= 2/3; K6 SIZE novel >= 2/3;
  K7 3WAY novel >= 1/2; K9 last-10 phase-2 >= 7/10. At least 4 of
  7 required.
- **K8 (beats controls):** Family A learner test accuracy exceeds
  the best of C1/C2/C3 by >= 15 percentage points.
- **K10 (true online, governance):** code audit PASS: strictly
  sequential processing; updates for episode t occur after episode
  t is segmented and interpreted; no structure built from future
  data.
- **K11 (no future leakage in segmentation, governance):** code
  audit PASS: the statistics used to segment episode t exclude
  episode t (FIN_* included: scoring for episode t reads FIN_*
  accumulated from episodes < t); the scene used is episode t's
  own observed scene.
- **K12 (determinism):** 3/3 byte-identical outputs (sha256
  recorded) on every family and every variant; exit 0, zero
  stderr each.
- **K_SAME (carry-forward governance):** devang6.zag differs from
  the frozen devang5.zag (sha256 in section 2) ONLY in
  banner/usage strings (verified by diff); devang6 reproduces
  devang5's committed Family A dev output
  (`docs/lab/rsi/runs/wave-20261002-0521pdt/DEVANG/dev_fama.log`
  on branch lane-devang-20261002-0821pdt) byte-identically. Any
  other behavioral delta = governance fail.

**Verdict rule:** BUILD-PASS requires KR0, K1, K_SEG, K_SEAL,
K_DISC, K_AUD, K_ABL, K_C0, K8, K10, K11, K12, K_SAME, plus at
least 4 of {K2, K3, K4, K5, K6, K7, K9}. Otherwise BUILD-FAIL. No
bar may be altered after results are observed. A bar may not be
weakened to force a pass. Report BUILD-PASS/BUILD-FAIL only.

## 11. Negative controls (what constitutes BUILD-FAIL)

1. Any required bar missed under the verdict rule in section 10.
2. KR0 violated: any panic, trap, nonzero exit, or nonzero stderr
   on any of the 3/3 runs.
3. K_AUD failed: classified as recurrence of the DEVANG2
   segmentation-independent failure mode; the result must name
   which claim failed and quote the evidence.
4. K_ABL failed: classified as MECHANISM RESULT (front-end not
   load-bearing on the fresh family), not bar-miscalibration. The
   recalibration removed the word-composition confound (fairness
   floor, section 8) and measures the gap directly; a miss now is
   informative about the mechanism. The bar is not re-tuned.
5. K_DISC failed: classified as mechanism non-discrimination
   (either the baseline does not fail E-prime, or POSSEG does not
   beat it on fresh probes).
6. Any new mode, bridge, router, task-specific handler, or
   hardcoded semantic case in the implementation: governance fail,
   cannot BUILD-PASS regardless of scores. (K_SAME already forbids
   behavioral delta; this restates it as a negative control.)
7. Python or any forbidden executable invoked at any stage:
   automatic PROCESS-FAIL for the lane's wave.
8. Any implementation file predating the prereg freeze commit, or
   unverifiable commit ordering: this prereg is VOID.
9. Sealed inputs or key files READ before/during the sealed runs:
   the sealed evaluation is VOID.
10. Any frozen bar weakened after results are observed: the verdict
    is VOID.
11. A W write inside any candidate-scoring path, or a FIN_* write
    outside the single learn_update site: K_AUD fail.

## 12. Architecture accounting (frozen expectations; builder fills actuals)

| Field | Frozen expectation | Actual (builder fills) |
|-------|-------------------|------------------------|
| Cognition source lines added vs devang5.zag | 0 (banner/usage rename only) | |
| New hardcoded semantic cases | 0 | |
| New cognitive modes / bridges / routers / handlers | 0 | |
| Learner-state structures created | 0 new (FIN_KNOWN/FIN_NOVEL at W+7392/7396 carried forward) | |
| Protected-core / ISA boundary | no new protected operations; frozen ISA respected; no benchmark-specific opcodes | |

Any nonzero entry in the semantic-case, cognitive-mode, bridge,
router, or handler rows invalidates the verdict regardless of
scores.

## 13. Honest boundaries

**What a BUILD-PASS would establish:** crash-free execution; the
segmentation-dependence design requirement still holds (audit);
the front-end is load-bearing under the CORRECTED measure on
fresh data (the recalibration is validated, not merely argued);
the FINREG signal still discriminates fresh adversarial probes
the old signal classes provably cannot (K_DISC on E-prime); no
Family A regression; lexicon discovery >= 8/10 strictly online;
exact segmentation >= 10/12 on sealed held-out probes; >= 12/20
on a post-freeze adversarial family with new surface vocabulary.
This remains developmental L2 structural-learning evidence, not
representational invention: no L3 claim is attempted.

**What a BUILD-PASS would NOT establish:** no generality proof
(three families over related worlds; sealed success must not be
overclaimed); no claim the final-regularity transfers to other
modalities or utterance shapes (disclosed limitation, carried
from DEVANG5); no claim against an independent adversary
(self-seal limitation, section 7; independent replication of
K_SEG/K_SEAL/K_ABL queued); the regularity is one positional
prior, not a syntax learner; no claim the positional signal helps
novel-vocabulary worlds (the C-doubleprime tie-with-C2 caveat
carries to C-tripleprime by the same mechanism logic).

**What a BUILD-FAIL would establish:** if K_ABL fails with K_AUD
passing, the front-end is not load-bearing on the fresh family
under the corrected measure (mechanism result, section 11 item
4). If K_DISC fails with K_AUD passing, the positional signal
does not move decisions as designed on fresh probes. If K_SEG
fails, the generator or the no-scene finalTerm is at fault. If
the K_DISC premise fails (DEVANG4 > 2/6 on E-prime), the
discriminator was misdesigned (test-design result).

## 14. Purity, determinism, commits

- Pure Zag only: implementation, compilation (pinned znc),
  execution, generation, scoring, and analysis. No Python, C, or
  other languages at any stage.
- Seeded LCG; no wall-clock; no ASLR-dependent behavior in output.
- No em dashes in source or documentation (checked with
  check_no_dash.sh before every commit).
- This prereg is committed ALONE before any .zag implementation
  exists in the lane and before the Family E-prime baseline
  measurement. The baseline, implementation, sealed package, and
  sealed evaluation are committed separately with explicit
  pathspecs. The builder records file creation order in
  BUILD-LOG.md.
- Owned path only
  (`docs/lab/rsi/runs/wave-20261002-1121pdt/devang/`). Local
  commits only; nothing is pushed. No git reset, no rebase.
