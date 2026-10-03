# PREREG_DEVANG4 (fresh): Co-segmentation by Interpretation Coherence

**Status:** DRAFT. Not yet frozen. The coordinator commits this file ALONE
before any .zag implementation exists in the lane.
**Date:** 2026-10-02.
**Wave:** wave-20261002-0221pdt.
**Lane:** DEVANG4.
**Owned path:** `docs/lab/rsi/runs/wave-20261002-0221pdt/DEVANG/`

## Disambiguation

Prior DEVANG lanes: DEVANG1 (overnight devlang, training crash, BUILD-FAIL);
DEVANG2 retry (wave-20261001-1721pdt, triply determined BUILD-FAIL:
cold-start repair architecturally inert because bigram statistics were
segmentation-independent by construction; red-team EVIDENCE HOLDS);
DEVANG3 wave-20261001-2021pdt (segmentation-dependent statistics as a design
requirement, K_AUD PASS, but K_SEG 8/12 and K_SEAL 11/20: segmenter quality
insufficient, judged a mechanism result); DEVANG3 wave-20261001-2321pdt
(one-line fix: novel-segment length bonus to linear penalty, BUILD-PASS:
K_SEG 12/12, K_SEAL 20/20 on fresh sealed families, regression clean).
The 2321pdt result supersedes the 2021pdt merge pathology. This prereg
therefore discriminates against the CURRENT best mechanism (2321pdt),
not the superseded 2021pdt build; discriminating against a superseded
build would be a strawman. The 2021pdt binary is still run as a secondary
baseline for continuity.

## 1. Standing problem

The 2321pdt segmenter is purely distributional: it maximizes
lexicon-frequency scores and never sees the scene. It is therefore blind
to a whole signal class: whether a candidate segmentation yields a
coherent interpretation of the observed scene. Concretely, when a novel
word contains a frequent known word as a substring (e.g. novel "balta"
containing frequent "bal"), the lexicon DP shatters it ("bal"+"ta")
because the frequent piece outscores the novel whole, even when the
shattered pieces vote for a distractor object and the whole word would
leave a clean interpretation. The segmenter cannot prefer the
interpretation-coherent analysis because interpretation never feeds back
into segmentation. This wave attacks that bottleneck with a
structurally different segmentation mechanism.

## 2. The design: COSEG (frozen)

COSEG = beam proposals + interpretation-coherence reranking.

1. Proposal: beam DP (beam width B=6, frozen) over the EXACT 2321pdt
   lexicon-frequency scoring (seen: `ilog(c)*10-30+ilog(L+1)*5`, minus 40
   if L==1; novel: `-50-1*L`; max segment length 16). The beam keeps the
   top 6 distinct full analyses by lexicon score at each position.
2. Cold start: unchanged from DEVANG3 (3-char chunks while nlex<10,
   inside the segmenter, feeds the same statistics update).
3. Rerank (scene mode only, i.e. whenever the episode carries a scene):
   for each beam candidate c, compute
   `joint(c) = lexScore(c) + 25*margin(c) - 5*nseg(c)`,
   where `margin(c)` = best minus second-best object score from the
   existing interpret-style scoring (segments 1.., same action-marker
   skip rule as `interpret`), and `nseg(c)` = number of segments.
   Select argmax joint; ties broken by beam order (deterministic).
4. No-scene mode (bare utterances, e.g. sealed Family B): the scene is
   absent so coherence is undefined; COSEG reduces EXACTLY to the 2321pdt
   DP (the existing `seg_dp` is called unchanged). This is documented
   non-regression, not a second mechanism.
5. The chosen segmentation is the SOLE input to `learn_update`. All
   statistics tables (lexicon counts, grounding, negator, comparative)
   update exclusively from the chosen segmentation. The scene/margin
   signal flows ONLY into the segmentation decision, never directly
   into any statistics table. Segmentation-dependence (the DEVANG3
   design requirement) is preserved.

Frozen parameters: B=6, MARGIN_W=25, SEG_W=5, cold-start threshold
nlex<10 with 3-char chunks. Rationale for MARGIN_W=25: a single
novel-word shatter typically moves lexScore by 30 to 40 points (the
-50-L novel penalty versus the split saving); a confident
interpretation (margin >= 2, i.e. the analysis picks out the target
with a 2-vote lead) contributes 50, enough to override a
frequency-driven shatter, while a marginal interpretation (margin 1,
contributing 25) cannot override a confident lexicon gap. SEG_W=5 is a
parsimony tie-break strictly smaller than one margin unit, so
interpretation confidence always dominates segment-count preference.

## 3. Why this is structurally different (not a parameter tweak)

DEVANG3 (both builds) decides segmentation by ONE signal class:
lexicon-frequency of segment identities. Interpretation runs AFTER
segmentation and never influences it; the scene never reaches the
segmenter (the `seg_dp` signature takes only bytes and the lexicon).
COSEG adds a SECOND signal class: interpretation coherence conditional
on the observed scene. The decision rule is joint optimization over
proposals, not a rescored DP: the winner is the analysis that best
explains the scene, with lexicon frequency as one term. Consequences
that a parameter tweak cannot produce: (a) the same byte string can be
segmented differently in different scenes (scene-conditioned
segmentation, impossible for any scene-blind DP); (b) segmentation
quality improves as grounding improves (co-learning loop: better
grounding -> more informative margins -> better segmentation -> better
statistics), whereas DEVANG3's segmentation never benefits from what
the learner has understood. The self red-team (REDTEAM_SELF.md) must
attack this claim directly, including constructing a case where the
two mechanisms MUST disagree and checking which one COSEG follows.

## 4. Family D: the held-out discriminator (frozen)

Six scene-mode episodes, frozen here before implementation. Each pairs
an utterance containing a NOVEL word (fresh form, absent from Family A)
that embeds a FREQUENT grounded Family A word, with a scene where the
embedded word votes for a distractor object while the true analysis
interprets cleanly. Format per line (sealc episode format):
`<c0> <s0> <z0> <c1> <s1> <z1> <c2> <s2> <z2> <tgt> <utterance>`.
Colors 0=red 1=blu 2=grn; shapes 0=ball 1=cube 2=tri; sizes 0=smal 1=big.

- D1: `2 2 1 0 0 0 1 1 0 0 takbaltagrn`, key `3,8` ([tak][balta][grn]).
  Shatter [tak][bal][ta][grn]: "bal" votes for the red ball distractor.
- D2: `2 0 1 0 1 0 1 2 0 0 takredbogrn`, key `3,8` ([tak][redbo][grn]).
  Shatter [tak][red][bo][grn]: "red" votes for the red cube distractor.
- D3: `2 0 1 1 1 0 0 2 0 0 takblupabal`, key `3,8` ([tak][blupa][bal]).
  Shatter [tak][blu][pa][bal]: "blu" votes for the blu cube distractor.
- D4: `2 2 1 0 1 0 1 0 0 0 takcublagrn`, key `3,8` ([tak][cubla][grn]).
  Shatter [tak][cub][la][grn]: "cub" votes for the red cube distractor.
- D5: `2 0 1 1 2 0 0 1 0 0 taktrixobal` (utterance `taktrixobal`),
  key `3,8` ([tak][trixo][bal]). Shatter [tak][tri][xo][bal]:
  "tri" votes for the blu tri distractor.
- D6: `2 1 1 0 0 0 1 2 0 0 taksphlagrn`, key `3,8` ([tak][sphla][grn]).
  Shatter [tak][sph][la][grn]: "sph" votes for the red ball distractor.

In every probe the lexicon-best analysis is the shatter (paper analysis
in the lane BUILD-LOG records the per-probe lexicon arithmetic; the
post-freeze baseline run establishes it empirically), the shatter's
interpretation margin is 0 (its grounded piece cancels against the
true descriptor, leaving a 0,0,-2 tie), and the true analysis has
margin 2. The novel words (balta, redbo, blupa, cubla, trixo, sphla)
are absent from the Family A lexicon. Family D is held out from
implementation tuning by this freeze: the builder may not adjust the
design, parameters, or code in response to Family D behavior.

## 5. Baseline protocol (post-freeze, pre-implementation)

After this prereg is committed and BEFORE any DEVANG4 implementation
exists, the builder runs the FROZEN 2321pdt binary
(`docs/lab/rsi/runs/wave-20261001-2321pdt/DEVANG3/devang3`,
sha256 `36f5047dd123a144569adaba5d7d86efcdf2126fa762790fe083ef620525151d`)
in `segb` mode on the six Family D utterances (bare utterance file),
3/3 runs, and records the exact-boundary score. Expected: 0/6 (all six
shatter). The premise for K_DISC is baseline <= 2/6. The 2021pdt binary
is run the same way as a secondary baseline (expected 0/6; its merge
pathology also shatters or merges these). This is a measurement of old
frozen binaries, not DEVANG4 development.

## 6. Seal protocol for the fresh families (self-seal, solo worker)

No independent adversary is available in this wave, so the sealed
families use a solo approximation, documented honestly as weaker than
an independent adversary:

1. This prereg freezes the generator specifications (section 7),
   including word lists, template sets, episode counts, and seeds.
2. After implementation, the builder writes `genseal4.zag` implementing
   exactly the frozen specs.
3. The builder validates the generator with ALTERED seeds into /tmp
   (format checks only; output discarded, never the sealed content).
4. The builder runs the frozen seeds once, producing `sealed4/` files.
5. The builder records sha256 of every sealed file in SEALED_B4.md /
   SEALED_C4.md and commits the sealed package BEFORE any sealed run.
6. The builder never inspects sealed file contents (hashes and sizes
   only). Any inspection voids the seal (governance VOID).
7. Limitation: the builder authored the generator. The prereg-frozen
   spec plus hash-before-run plus no-inspection is the solo
   approximation. Independent-adversary replication of K_SEG/K_SEAL is
   queued as follow-up (see section 12). The discrimination claim
   (K_DISC) does not depend on the sealed families: Family D is
   prereg-frozen and the baseline is measured on a frozen binary.
8. DEVANG3's worlds (2021pdt Families B/C) may be used ONLY as a
   regression check, never as the decision set.

## 7. Generator specifications (frozen)

Family B-prime (held-out segmentation ambiguity, utterance-only):
- 11 fresh words (frozen list): zok(3), zokan(5), natemo(6), nate(4),
  wex(3), wexil(5), fim(3), afim(4), grol(4), agrol(5), ol(2).
  Prefix pairs sharing >= 2: (zok,zokan), (nate,natemo), (wex,wexil).
  Suffix pairs sharing >= 2: (fim,afim), (grol,agrol), (ol,grol).
- 12 utterances from LCG seed 777001: 4x [Family A known word from
  {smal, sph, big, grn}] + [B-prime word] (either order, seeded);
  4x [B-prime word] + [B-prime word] drawn to exercise prefix/suffix
  ambiguity; 4x 2-3 random B-prime words. All utterances 1..24 chars.
- Key file: `<utt> => <b1>,<b2>,...` true boundaries (1-based segment
  ends excluding utterance end).
- Structural requirements mirror the DEVANG3 Family B spec (lengths
  2..6, >= 3 prefix pairs, >= 3 suffix pairs); the word list above
  satisfies them by construction.

Family C-prime (post-freeze adversarial, new surface vocabulary):
- 12 fresh words with frozen roles: action "vok"(3); negator "nibo"(4);
  colors "zak"(3) [=red], "fimi"(4) [=blu], "ug"(2) [=grn]; shapes
  "dax"(3) [=ball], "kubl"(4) [=cube], "triq"(4) [=tri]; sizes "bigo"(4)
  [=big], "smalu"(5) [=smal], "bigeru"(6) [=biger]. No Family A forms.
  Word lengths 2..6 with a different length distribution than Family A
  (fewer 3-char words), so boundary statistics differ materially.
- Templates (same semantics as Family A, new forms): DIRECT
  "vok <color> <shape>"; NEG "vok nibo <color>"; REL "vok bigeru
  <shape>"; SIZE "vok <size> <shape>". Scene generation mirrors the
  Family A gen_direct/gen_neg/gen_rel/gen_size distributions.
- 40 train episodes (16 DIRECT, 10 NEG, 7 REL, 7 SIZE), 20 test episodes
  (8 DIRECT novel, 4 NEG novel, 4 REL novel, 4 SIZE novel; novel =
  color+shape combos absent from training; at least 4 test utterances
  exercise the bigo/bigeru prefix ambiguity). LCG seed 777002.
- File format: sealc format (`<ntrain> <ntest>` header, then episode
  lines `<9 scene ints> <tgt> <utterance>`).

## 8. Sealed interface (harness, frozen)

The binary keeps the DEVANG3 argv interface (fama, segb, segb-abl,
sealc, sealc-fresh with learner|c0|c2|c1|c3 variants) and adds ONE
harness mode:

- `segb-scene <episode_file>`: trains on Family A (100 episodes, seed
  123456789, frozen) exactly like `segb`, then reads the episode file
  (sealc format: `<ntrain> <ntest>` header; ntrain lines skipped),
  segments each of the ntest utterances with the scene-mode segmenter
  (frozen statistics, no updates, no lexicon growth), and prints
  `<utt> => <b1>,<b2>,...` per line. This is evaluation harness, not
  cognitive machinery: it exposes the scene-mode segmentation
  decision for scoring. The architecture accounting records it as
  harness.

Learner-path segmenter selection (frozen): wherever an episode scene
is available (fama train/test, sealc/sealc-fresh train/test variant 0,
segb-scene), the learner uses `seg_coseg` (beam + coherence rerank).
Where no scene exists (`segb` on bare utterances), the learner uses
the unchanged 2321pdt `seg_dp`. Controls are frozen: C0 = raw-byte
bigram statistics + `seg_dp_raw` (the DEVANG2 failure-mode
architecture, byte-identical to 2321pdt); ablation/C2 = fixed-width-3
(`seg_fixed3`); C1/C3 unchanged.

## 9. Frozen kill bars (exact numeric thresholds)

- **KR0 (crash regression, hard gate):** Family A, 3/3 runs complete,
  exit code 0, zero stderr bytes each, no panic or trap. Violation =
  BUILD-FAIL regardless of all other bars.
- **K1 (lexicon discovery):** >= 8 of the 10 phase-1 true words
  (tak, not, red, blu, bal, sph, cub, big, biger, smal) present as
  exact lexicon entries in the t=60 snapshot.
- **K_SEG (segmentation quality):** >= 9/12 sealed Family B-prime
  utterances segmented with exact true boundaries (no missing, extra,
  or shifted boundaries). Threshold equal to DEVANG3's (at least as
  strict).
- **K_SEAL (post-freeze adversarial):** learner accuracy >= 12/20 on
  sealed Family C-prime test episodes via `sealc-fresh` (learner
  variant). C0, C1, C2, C3 accuracies reported alongside. Threshold
  equal to DEVANG3's (at least as strict).
- **K_DISC (mechanism discriminator):** (a) the frozen 2321pdt baseline
  scores <= 2/6 exact-boundary on the Family D utterances (premise,
  measured post-freeze per section 5); (b) DEVANG4 scores >= 5/6
  exact-boundary on the Family D episodes via `segb-scene`. Both
  conjuncts required. If (a) fails, K_DISC fails with classification
  "discrimination premise failed".
- **K_AUD (segmentation-dependence audit, governance):** independent
  code inspection PASS on all four claims: (a) every statistics table
  is updated only from the chosen segmentation's output; (b) no code
  path reads raw utterance bytes into any statistics table on the
  learner path; (c) the cold-start path is inside the segmenter and
  feeds the same statistics update as later episodes; (d) the
  scene/margin signal is confined to candidate scoring (no W writes
  in the margin/coherence path) and the chosen segmentation is the
  sole statistics input (no scene-to-statistics path beyond the
  pre-existing target-supervised learn_update). Any violation =
  BUILD-FAIL, classified as DEVANG2-mode recurrence.
- **K_ABL (ablation, load-bearing front-end):** the ablation variant
  (frozen learner source with the whole scene-mode segmenter replaced
  by fixed-width-3 chunking; statistics machinery, lexicon, grounding,
  detection, interpretation identical) must score <= 5/12 on sealed
  Family B-prime AND satisfy (learner K1 - ablation K1) >= 2. If the
  ablation passes either leg, the front-end is not load-bearing =
  BUILD-FAIL.
- **K_C0 (trap exclusion):** control C0 (frozen 2321pdt failure-mode
  architecture) must trail the learner by >= 15 percentage points on
  Family A test accuracy AND by >= 3 words on K1.
- **K2..K7, K9:** K2 DIRECT novel >= 5/6; K3 NEG novel >= 2/3;
  K4 REL novel >= 2/3; K5 SYN novel >= 2/3; K6 SIZE novel >= 2/3;
  K7 3WAY novel >= 1/2; K9 last-10 phase-2 >= 7/10. At least 4 of 7
  required.
- **K8 (beats controls):** Family A learner test accuracy exceeds the
  best of C1/C2/C3 by >= 15 percentage points.
- **K10 (true online, governance):** code audit PASS: strictly
  sequential processing; updates for episode t occur after episode t
  is segmented and interpreted; no structure built from future data.
- **K11 (no future leakage in segmentation, governance):** code audit
  PASS: the statistics used to segment episode t exclude episode t;
  the scene used is episode t's own observed scene (an input, not
  future data), consistent with interpretation's existing scene use.
- **K12 (determinism):** 3/3 byte-identical outputs (sha256 recorded)
  on every family and every variant (learner, C0, ablation,
  segb-scene); exit 0, zero stderr each.

**Verdict rule:** BUILD-PASS requires KR0, K1, K_SEG, K_SEAL, K_DISC,
K_AUD, K_ABL, K_C0, K8, K10, K11, K12, plus at least 4 of
{K2, K3, K4, K5, K6, K7, K9}. Otherwise BUILD-FAIL. No bar may be
altered after results are observed. A bar may not be weakened to force
a pass. Report BUILD-PASS/BUILD-FAIL only.

## 10. Negative controls (what constitutes BUILD-FAIL)

1. Any required bar missed under the verdict rule in section 9.
2. KR0 violated: any panic, trap, nonzero exit, or nonzero stderr on
   any of the 3/3 runs.
3. K_AUD, K_ABL, or K_C0 failed: classified as recurrence of the
   DEVANG2 segmentation-independent failure mode; the result must name
   which failed and quote the numbers.
4. K_DISC failed: classified as mechanism non-discrimination (either
   the baseline does not fail Family D, or COSEG does not beat it).
5. Any new mode, bridge, router, task-specific handler, or hardcoded
   semantic case in the implementation: governance fail, cannot
   BUILD-PASS regardless of scores. (Negator and comparative detection
   stay the generic statistical tests; no new word-specific logic.)
6. Cognition source lines added versus the 2321pdt DEVANG3 source
   reaching 120 or more new/changed lines: governance fail. Target is
   <= 80. (Cumulative versus the DEVANG2 baseline is reported for the
   record; the per-wave cap applies to this wave's delta.)
7. Python or any forbidden executable invoked at any stage: automatic
   PROCESS-FAIL for the wave.
8. Any implementation file predating the prereg freeze commit, or
   unverifiable commit ordering: this prereg is VOID.
9. Sealed inputs inspected before the sealed run: the sealed evaluation
   is VOID.
10. Any frozen bar weakened after results are observed: the verdict is
    VOID.

## 11. Architecture accounting (frozen expectations; builder fills actuals)

| Field | Frozen expectation | Actual (builder fills) |
|-------|-------------------|------------------------|
| Cognition source lines added vs 2321pdt DEVANG3 | target <= 80; hard cap < 120 new/changed | |
| New hardcoded semantic cases | 0 | |
| New cognitive modes / bridges / routers / handlers | 0 (one harness argv mode `segb-scene` for scene-mode segmentation eval; evaluation harness, not cognitive machinery) | |
| Learner-state structures created | 0 new persistent structures; beam buffers are transient per-episode | |
| Protected-core / ISA boundary | no new protected operations; frozen ISA respected; no benchmark-specific opcodes | |

Any nonzero entry in the semantic-case, cognitive-mode, bridge, router,
or handler rows invalidates the verdict regardless of scores.

## 12. Honest boundaries

**What a BUILD-PASS would establish:** crash-free execution; the
segmentation-dependence design requirement still holds with a
scene-conditioned segmenter (audit); the front-end is load-bearing
(ablation); the win is not an architecture-independent rescue (C0);
lexicon discovery >= 8/10 strictly online; exact segmentation >= 9/12
on sealed held-out ambiguity; >= 12/20 on a post-freeze adversarial
family with new surface vocabulary; and, via K_DISC, that the new
segmentation mechanism decides by interpretation coherence where the
best prior mechanism provably fails (scene-conditioned segmentation,
a capability the prior architecture cannot express). This is
developmental L2 structural-learning evidence, not representational
invention: no L3 claim is attempted.

**What a BUILD-PASS would NOT establish:** no generality proof (three
families over related worlds; per the standing ruling, sealed success
must not be overclaimed); no claim the coherence weights transfer to
other modalities; no claim against an independent adversary (the
self-seal limitation in section 6: K_SEG/K_SEAL replication by an
independent adversary is queued as follow-up and required before any
promotion argument).

**What a BUILD-FAIL would establish:** if K_DISC fails while K_AUD
passes, the coherence signal does not move segmentation decisions as
designed (mechanism result). If K_SEG/K_SEAL fail while K_DISC passes,
the new mechanism discriminates but does not yet carry the full
battery (partial mechanism result). If K_AUD/K_ABL/K_C0 fail, the
segmentation-independent failure mode recurs (architectural result).

## 13. Purity, determinism, commits

- Pure Zag only: implementation, compilation (pinned znc), execution,
  and analysis. No Python, C, or other languages at any stage.
- Seeded LCG; no wall-clock; no ASLR-dependent behavior in output.
- No em dashes in source or documentation (checked with
  check_no_dash.sh before every commit).
- This prereg is committed ALONE before any .zag implementation
  exists in the lane. The baseline measurement (section 5) runs after
  the freeze commit. Implementation, sealed package, and sealed
  evaluation are committed separately with explicit pathspecs. The
  builder records file creation order in BUILD-LOG.md.
- Owned path only
  (`docs/lab/rsi/runs/wave-20261002-0221pdt/DEVANG/`). Local commits
  only; nothing is pushed. No git reset, no rebase.
