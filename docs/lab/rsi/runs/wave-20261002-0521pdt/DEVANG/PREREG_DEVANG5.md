# PREREG_DEVANG5 (frozen): Learned utterance-final regularity (FINREG)

**Status:** FROZEN. Committed ALONE before any DEVANG5 implementation
exists and before the Family E baseline measurement.
**Date:** 2026-10-02.
**Wave:** wave-20261002-0521pdt.
**Lane:** DEVANG5.
**Owned path:** `docs/lab/rsi/runs/wave-20261002-0521pdt/DEVANG/`

## 1. Disambiguation

Prior DEVANG lanes: DEVANG1 (overnight devlang, training crash,
BUILD-FAIL); DEVANG2 retry (wave-20261001-1721pdt, triply determined
BUILD-FAIL: cold-start repair architecturally inert because bigram
statistics were segmentation-independent by construction; red-team
EVIDENCE HOLDS); DEVANG3 wave-20261001-2021pdt (K_SEG 8/12, K_SEAL
11/20, BUILD-FAIL, mechanism result); DEVANG3 wave-20261001-2321pdt
(one-line novel-length penalty fix, BUILD-PASS: K_SEG 12/12, K_SEAL
20/20); DEVANG4 wave-20261002-0221pdt (COSEG: beam plus
interpretation-margin rerank, BUILD-FAIL: K_SEG 4/12 on a
generator-flawed B-prime with 8 information-less all-novel utterances,
K_DISC 2/6 because the margin rewards confident WRONG interpretations).
This prereg discriminates against the CURRENT best mechanism (the
DEVANG4 COSEG binary, frozen), not any superseded build.

## 2. Standing problem

DEVANG4's K_DISC autopsy (REDTEAM_SELF.md, 0221pdt) established that
the `[tak][X][yyZ]` wrong analysis (e.g. `[tak][bal][tagrn]`) is a
perfect fixed point for every per-episode signal computed from
(utterance, scene, current lexicon): it ties the true analysis on
lexicon score, ties on interpretation margin (margin 2 for the
distractor versus margin 2 for the target), and ties on segment
count. Margin-maximization measures decisiveness, not correctness,
and no reweighting of per-episode signals escapes the tie. The
distinguishing information must come from a NEW signal class the
learner induces across episodes. The 0221pdt red-team queued two
directions: (a) coherence tied to a verifiable signal, or (b) a
different second signal class. This wave takes (b): induced positional
syntax, specifically the utterance-final regularity.

## 3. The design: FINREG (frozen)

POSSEG = DEVANG4's beam proposals (B=6, frozen) over the EXACT 2321pdt
lexicon-frequency scoring, reranked by a joint that adds ONE new term:

`joint(c) = lexScore(c) + 25*margin(c)*scn - 5*nseg(c) + finalTerm(c)`

where `scn` = 1 when a scene is present (margin defined), 0 otherwise,
and

`finalTerm(c) = +4*r  if the final segment of c is lexicon-known`
`finalTerm(c) = -4*r  if the final segment of c is novel`

with `r = ilog(FIN_KNOWN+1) - ilog(FIN_NOVEL+1)`, clamped at >= 0.
`FIN_KNOWN` / `FIN_NOVEL` are two new i32 learner-state words
(W+7392, W+7396): counts of chosen analyses whose final segment was
known (lexicon count >= 1 before this episode's update) versus novel
(lexicon count == 0, i.e. added by this episode's mapping). Both
update at exactly ONE site: the top of `learn_update`, from the
chosen segmentation, BEFORE the count bumps of the current episode.
No other code writes them. Candidate scoring only READS them.

The regularity is LEARNED, not hardcoded: the weight `4*r` is
frozen, but `r` is estimated from the learner's own segmentation
history and grows developmentally (near 0 during cold start, about 4
after Family A training: FIN_KNOWN about 96, FIN_NOVEL about 4).
The linguistic content: in the learner's experience, utterances end
with known words (the descriptor slot); a candidate ending in a novel
segment is therefore penalized, a candidate ending in a known word
rewarded. "Known" is evaluated by `lex_find` at scoring time, so the
term tracks the CURRENT lexicon.

Cold start is unchanged (3-char chunks while nlex<10, inside the
segmenter, feeding the same statistics update). Max segment length 16
unchanged. The no-scene path now uses the same POSSEG rerank with
`scn=0` (finalTerm active, margin inactive); unlike DEVANG4, the new
mechanism therefore engages WITHOUT a scene. This is a mechanism
change, documented here, not a silent harness change.

Frozen parameters: B=6, MARGIN_W=25, SEG_W=5, FW=4,
cold-start threshold nlex<10. Rationale for FW=4: after Family A
training r=4, so finalTerm is +-16, enough to break the Family E
ties (section 5 arithmetic: truth 46 vs wrong 24) while remaining
small relative to lexicon gaps that decide unambiguous cases
(typically 30 to 100).

## 4. Why this is structurally different (not a parameter tweak)

No prior DEVANG segmenter accesses positional information. DEVANG3
decides by WHAT the pieces are (lexicon identity). DEVANG4 adds HOW
WELL the pieces explain the scene (interpretation decisiveness).
DEVANG5 adds WHERE words occur (induced positional syntax). The
signal is computed from a learner-state statistic (FIN_KNOWN /
FIN_NOVEL) that DEVANG4's segmenter cannot read, and it is active in
the no-scene path where DEVANG4 provably reduces to the old DP. The
decision differs observably: on Family E (section 5) DEVANG4's joint
ranks the wrong analysis first on all six probes (40 vs 30, by the
frozen lexicon arithmetic, no tie involved), while POSSEG ranks the
truth first (46 vs 24). The mechanism is learned (r from the
learner's own history), variable (r changes with experience), and
segmentation-dependent (FIN_* update only from chosen analyses;
section 10, K_AUD claim e).

## 5. Family E: the held-out discriminator (frozen, explicit)

Six scene-mode episodes, frozen here before implementation. Each
utterance is `tak` + N + D where N = W_emb + XY is a NOVEL 5-char
word embedding a FREQUENT grounded Family A word W_emb (lexicon
score 20), and D is a 3-char grounded descriptor (lexicon score 10)
voting for the target. The embedded word votes unopposed for a
distractor in the `[tak][W_emb][XY+D]` analysis. By construction the
wrong analysis BEATS the true analysis on lexicon score (40+20-55=5
vs 40-55+10=-5) and ties on margin (2 vs 2), so DEVANG4's joint
ranks it first deterministically (40 vs 30). Format per line:
`<c0> <s0> <z0> <c1> <s1> <z1> <c2> <s2> <z2> <tgt> <utterance>`.
Key for every probe: `3,8` ([tak][N][D]).

- E1: `2 2 1 0 1 0 1 0 0 0 takcubxogrn` (W=cub, D=grn)
- E2: `1 0 1 0 2 0 2 1 0 0 takredombal` (W=red, D=bal)
- E3: `0 0 1 1 2 0 2 1 0 0 takbluevsph` (W=blu, D=sph)
- E4: `1 2 1 2 1 0 0 0 0 0 takcubaktri` (W=cub, D=tri)
- E5: `2 0 1 0 1 0 1 2 0 0 takredipgrn` (W=red, D=grn)
- E6: `2 0 1 1 1 0 0 2 0 0 takbluexbal` (W=blu, D=bal)

The six (W_emb, XY, D) tuples are fresh (none coincide with Family D's
tuples; the novel forms cubxo, redom, bluev, cubak, redip, bluex are
absent from Family A). The construction PRINCIPLE mirrors Family D's
(the adversarial structure DEVANG4 failed), which is the point: the
discriminator tests whether the new signal class generalizes to fresh
tuples. The builder may not adjust the design, parameters, or code in
response to Family E behavior. Predicted POSSEG joints (r=4):
truth 46 vs wrong 24 on every probe (section 3 arithmetic); the
implementation, not the prediction, is under test.

## 6. Baseline protocol (post-freeze, pre-implementation)

After this prereg is committed and BEFORE any DEVANG5 implementation
exists, the builder writes `baseline/familye_eps.txt` (sealc format:
`0 6` header plus the six section-5 lines, copied verbatim) and runs
the FROZEN DEVANG4 binary
(`docs/lab/rsi/runs/wave-20261002-0221pdt/DEVANG/devang4`, sha256
`cfba24f157a22b0e721f9a27722320f6b2d3a77e250b96c9045659b58bb9ddbd`,
hash verified before the run) in `segb-scene` mode on it, 3/3 runs,
recording the exact-boundary score. Expected: 0/6 (the wrong analysis
wins outright on lexicon, 40 vs 30). The premise for K_DISC is
baseline <= 2/6. This is a measurement of an old frozen binary, not
DEVANG5 development.

## 7. Seal protocol for the fresh families (self-seal, solo worker)

Same solo approximation as DEVANG4, documented honestly as weaker
than an independent adversary:

1. This prereg freezes the generator specifications (section 8),
   including word lists, pattern sets, episode counts, and seeds.
2. After implementation, the builder writes `genseal5.zag`
   implementing exactly the frozen specs.
3. The builder validates the generator with ALTERED seeds into /tmp
   (format checks, spec-compliance checks, and a solvability smoke
   test on throwaway sets; output discarded, never the sealed
   content). Spec-compliance bugs may be fixed; the spec itself may
   not be changed in response.
4. The builder runs the frozen seeds once, producing `sealed5/`
   files plus key files.
5. The builder records sha256 of every sealed file and commits the
   sealed package BEFORE any sealed run.
6. The builder never READS sealed file contents or key files (no
   cat, less, editor opens, or pager views). Scoring is mechanical:
   a Zag scorer prints only aggregate scores. Any read voids the
   seal (governance VOID).
7. Limitation: the builder authored the generator. The prereg-frozen
   spec plus hash-before-run plus no-read is the solo approximation.
   Independent-adversary replication of K_SEG/K_SEAL is queued as
   follow-up. The discrimination claim (K_DISC) does not depend on
   the sealed families: Family E is prereg-explicit and the baseline
   is measured on a frozen binary.
8. Prior sealed sets (DEVANG3 B/C, DEVANG4 B-prime/C-prime) may be
   used ONLY as regression checks, never as the decision set.

## 8. Generator specifications (frozen)

Family B-doubleprime (held-out segmentation probes, utterance-only):
- 10 fresh roots (frozen list): pib(3), pibok(5), yex(3), yexil(5),
  wam(3), awamo(5), jrep(4), jrepil(6), kiv(3), akiv(4). Prefix pairs
  sharing >= 2: (pib,pibok), (yex,yexil), (jrep,jrepil). Suffix pairs
  sharing >= 2: (wam,awamo), (kiv,akiv), (yexil,jrepil).
- 12 utterances from LCG seed 888001: 4x K+N+K, 4x K+N, 4x N+K,
  where K is drawn (seeded) from {tak, red, blu, grn, bal, sph, cub,
  smal, big, not} and N is drawn (seeded) from the roots. Every
  utterance contains EXACTLY ONE novel root and at least one known
  word (by construction of the patterns; this fixes the DEVANG4
  B-prime flaw where 8 of 12 utterances were all-novel and therefore
  information-less). All utterances 4..20 chars.
- The generator enforces (seeded re-draw, bounded retries): at
  least 2 utterances exercise a prefix pair (both members appear
  across the set) and at least 2 exercise a suffix pair.
- Key file: `<utt> => <b1>,<b2>,...` true boundaries (1-based
  segment ends excluding utterance end).
- Solvability note (design rationale, not a bar): with exactly one
  novel root per utterance anchored by known words, the lexicon DP
  favors the true analysis (paper arithmetic in the lane BUILD-LOG);
  the finalTerm only strengthens it. No utterance presents an
  information-less parse.

Family C-doubleprime (post-freeze adversarial, new surface
vocabulary):
- 12 fresh words with frozen roles: action "zek"(3); negator
  "nubo"(4); colors "zok"(3) [=red], "wimi"(4) [=blu], "ix"(2)
  [=grn]; shapes "dox"(3) [=ball], "plub"(4) [=cube], "sliq"(4)
  [=tri]; sizes "gabo"(4) [=big], "imlau"(5) [=smal], "gabexu"(6)
  [=biger]. No Family A forms, no C-prime forms. Word lengths 2..6
  with a different length distribution than both Family A and
  C-prime.
- Templates (same semantics as Family A, new forms): DIRECT
  "zek <color> <shape>"; NEG "zek nubo <color>"; REL "zek gabexu
  <shape>"; SIZE "zek <size> <shape>". Scene generation mirrors the
  Family A gen_direct/gen_neg/gen_rel/gen_size distributions.
- 40 train episodes (16 DIRECT, 10 NEG, 7 REL, 7 SIZE), 20 test
  episodes (8 DIRECT novel, 4 NEG novel, 4 REL novel, 4 SIZE novel;
  novel = color+shape combos absent from training; at least 4 test
  utterances exercise the gabo/gabexu prefix ambiguity). LCG seed
  888002.
- File format: sealc format (`<ntrain> <ntest>` header, then
  episode lines).

## 9. Sealed interface (harness, frozen)

The binary keeps the DEVANG4 argv interface (fama, segb, segb-abl,
segb-scene, sealc, sealc-fresh with learner|c0|c2|c1|c3 variants).
Behavioral changes, all mechanism (not harness):

- The learner-path segmenter is `seg_posseg` (section 3) wherever
  DEVANG4 used `seg_coseg`: fama train/test, sealc/sealc-fresh
  train/test variant 0, segb-scene, and segb TRAINING.
- `segb` PROBING (bare utterances, no scene) uses `seg_posseg` with
  `scn=0` (finalTerm active, margin inactive). DEVANG4 used the pure
  `seg_dp` here; the change is the point (the new mechanism engages
  without a scene).
- One new mechanical scorer `scoree.zag`: reads a segb-scene output
  file and a key file, prints only the aggregate exact-boundary
  score (`E: x/6`). Scoring aid only.

Controls frozen: C0 = raw-byte bigram statistics + `seg_dp_raw`
(the DEVANG2 failure-mode architecture); C2 = fixed-width-3
(`seg_fixed3`, doubles as the K_ABL ablation); C1/C3 unchanged.

## 10. Frozen kill bars (exact numeric thresholds)

- **KR0 (crash regression, hard gate):** Family A, 3/3 runs complete,
  exit code 0, zero stderr bytes each, no panic or trap. Violation =
  BUILD-FAIL regardless of all other bars.
- **K1 (lexicon discovery):** >= 8 of the 10 phase-1 true words
  present as exact lexicon entries in the t=60 snapshot.
- **K_SEG (segmentation quality):** >= 10/12 sealed Family
  B-doubleprime utterances segmented with exact true boundaries.
  Threshold RAISED from DEVANG4's 9/12 (honest: the generator flaw
  is fixed, every utterance is solvable in principle).
- **K_SEAL (post-freeze adversarial):** learner accuracy >= 12/20 on
  sealed Family C-doubleprime test episodes via `sealc-fresh`
  (learner variant). C0, C1, C2, C3 accuracies reported alongside.
  Threshold EQUAL to DEVANG4's (not lowered; raising would be
  dishonest since the new signal is neutral on all-novel
  vocabulary).
- **K_DISC (mechanism discriminator):** (a) the frozen DEVANG4
  binary scores <= 2/6 exact-boundary on the Family E episodes via
  `segb-scene` (premise, measured post-freeze per section 6);
  (b) DEVANG5 scores >= 5/6 exact-boundary on the Family E episodes
  via `segb-scene`. Both conjuncts required. If (a) fails, K_DISC
  fails with classification "discrimination premise failed".
- **K_AUD (segmentation-dependence audit, governance):** independent
  code inspection PASS on all five claims: (a) every statistics
  table (lexicon counts, grounding, negator, comparative, FIN_*) is
  updated only from the chosen segmentation's output; (b) no code
  path reads raw utterance bytes into any statistics table on the
  learner path; (c) the cold-start path is inside the segmenter and
  feeds the same statistics update as later episodes; (d) the
  scene/margin/finalTerm signals are confined to candidate scoring
  (zero W writes in any scoring path) and the chosen segmentation
  is the sole statistics input; (e) FIN_KNOWN/FIN_NOVEL are written
  at exactly one site (learn_update top, pre-bump lex-count test)
  and nowhere else. Any violation = BUILD-FAIL, classified as
  DEVANG2-mode recurrence.
- **K_ABL (ablation, load-bearing front-end):** the fixed-width-3
  ablation must score <= 5/12 on sealed Family B-doubleprime AND
  satisfy (learner K1 - ablation K1) >= 2. If the ablation passes
  either leg, the front-end is not load-bearing = BUILD-FAIL.
- **K_C0 (trap exclusion):** control C0 must trail the learner by
  >= 15 percentage points on Family A test accuracy AND by >= 3
  words on K1.
- **K2..K7, K9:** K2 DIRECT novel >= 5/6; K3 NEG novel >= 2/3;
  K4 REL novel >= 2/3; K5 SYN novel >= 2/3; K6 SIZE novel >= 2/3;
  K7 3WAY novel >= 1/2; K9 last-10 phase-2 >= 7/10. At least 4 of 7
  required.
- **K8 (beats controls):** Family A learner test accuracy exceeds
  the best of C1/C2/C3 by >= 15 percentage points.
- **K10 (true online, governance):** code audit PASS: strictly
  sequential processing; updates for episode t occur after episode t
  is segmented and interpreted; no structure built from future data.
- **K11 (no future leakage in segmentation, governance):** code
  audit PASS: the statistics used to segment episode t exclude
  episode t (FIN_* included: scoring for episode t reads FIN_*
  accumulated from episodes < t); the scene used is episode t's own
  observed scene.
- **K12 (determinism):** 3/3 byte-identical outputs (sha256 recorded)
  on every family and every variant; exit 0, zero stderr each.
- **K_DELTA (minimal-delta governance):** the implementation delta
  from `devang4.zag` is confined to the FINREG machinery
  (finalTerm scoring, FIN_* table and its single update site,
  `scn` plumbing at call sites, banner rename). Any other
  behavioral delta = governance fail. Cognition source lines
  added vs devang4.zag: target <= 60, hard cap < 120.

**Verdict rule:** BUILD-PASS requires KR0, K1, K_SEG, K_SEAL, K_DISC,
K_AUD, K_ABL, K_C0, K8, K10, K11, K12, K_DELTA, plus at least 4 of
{K2, K3, K4, K5, K6, K7, K9}. Otherwise BUILD-FAIL. No bar may be
altered after results are observed. A bar may not be weakened to
force a pass. Report BUILD-PASS/BUILD-FAIL only.

## 11. Negative controls (what constitutes BUILD-FAIL)

1. Any required bar missed under the verdict rule in section 10.
2. KR0 violated: any panic, trap, nonzero exit, or nonzero stderr
   on any of the 3/3 runs.
3. K_AUD, K_ABL, or K_C0 failed: classified as recurrence of the
   DEVANG2 segmentation-independent failure mode; the result must
   name which failed and quote the numbers.
4. K_DISC failed: classified as mechanism non-discrimination (either
   the baseline does not fail Family E, or POSSEG does not beat it).
5. Any new mode, bridge, router, task-specific handler, or hardcoded
   semantic case in the implementation: governance fail, cannot
   BUILD-PASS regardless of scores. (Negator and comparative
   detection stay the generic statistical tests; no new
   word-specific logic. The finalTerm weight FW=4 is a frozen
   scalar; the regularity strength r is learner-estimated.)
6. Cognition source lines added versus devang4.zag reaching 120 or
   more new/changed lines: governance fail.
7. Python or any forbidden executable invoked at any stage:
   automatic PROCESS-FAIL for the wave.
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
| Cognition source lines added vs devang4.zag | target <= 60; hard cap < 120 new/changed | |
| New hardcoded semantic cases | 0 | |
| New cognitive modes / bridges / routers / handlers | 0 | |
| Learner-state structures created | 8 bytes: FIN_KNOWN/FIN_NOVEL (2x i32 at W+7392); transient beam buffers unchanged | |
| Protected-core / ISA boundary | no new protected operations; frozen ISA respected; no benchmark-specific opcodes | |

Any nonzero entry in the semantic-case, cognitive-mode, bridge,
router, or handler rows invalidates the verdict regardless of scores.

## 13. Honest boundaries

**What a BUILD-PASS would establish:** crash-free execution; the
segmentation-dependence design requirement still holds with a
positionally-informed segmenter (audit); the front-end is
load-bearing (ablation); the win is not an architecture-independent
rescue (C0); lexicon discovery >= 8/10 strictly online; exact
segmentation >= 10/12 on sealed held-out probes; >= 12/20 on a
post-freeze adversarial family with new surface vocabulary; and, via
K_DISC against the frozen DEVANG4 binary, that the learned
utterance-final regularity decides cases where lexicon-frequency and
interpretation-margin provably fail (a new signal class doing
load-bearing work). This is developmental L2 structural-learning
evidence, not representational invention: no L3 claim is attempted.

**What a BUILD-PASS would NOT establish:** no generality proof
(three families over related worlds; sealed success must not be
overclaimed); no claim the final-regularity transfers to other
modalities or utterance shapes (it is induced from commands and
may not transfer to bare sequences, disclosed limitation); no claim
against an independent adversary (self-seal limitation, section 7;
independent replication of K_SEG/K_SEAL queued); the regularity is
one positional prior, not a syntax learner.

**What a BUILD-FAIL would establish:** if K_DISC fails with K_AUD
passing, the positional signal does not move decisions as designed
(mechanism result). If K_SEG fails, the generator fix or the
no-scene finalTerm is at fault (mechanism/test result). If
K_AUD/K_ABL/K_C0 fail, the segmentation-independent failure mode
recurs (architectural result). If the K_DISC premise fails
(DEVANG4 > 2/6 on Family E), the discriminator was misdesigned
(test-design result).

## 14. Purity, determinism, commits

- Pure Zag only: implementation, compilation (pinned znc),
  execution, generation, scoring, and analysis. No Python, C, or
  other languages at any stage.
- Seeded LCG; no wall-clock; no ASLR-dependent behavior in output.
- No em dashes in source or documentation (checked with
  check_no_dash.sh before every commit).
- This prereg is committed ALONE before any .zag implementation
  exists in the lane and before the Family E baseline measurement.
  The baseline, implementation, sealed package, and sealed
  evaluation are committed separately with explicit pathspecs. The
  builder records file creation order in BUILD-LOG.md.
- Owned path only
  (`docs/lab/rsi/runs/wave-20261002-0521pdt/DEVANG/`). Local commits
  only; nothing is pushed. No git reset, no rebase.
