# PREREG_TA — Builder preregistration: Self-PAM text-approximate line, H-TA1 vs H-TA3 head-to-head

**Date:** 2026-09-28 (builder wave; authored 2026-09-27 PDT)
**Status:** RATIFIED by the builder crew. This is the enactment the protocol
requires: the KB-TA-1..4 starting bids (reconstructed in HYPOTHESES_TA.md §5
from the mission text — they are NOT in the G2 amendment) are ratified below
as law, sharpened per hypothesis, together with each hypothesis's three
mechanism-level kill bars from the hypotheses doc.
**Authority:** `AMENDMENT_2026-09-27_G2_PER_DOMAIN_SEMANTICS.md` (ENACTED per
Micah 2026-09-27 ~18:18 PDT) — text/intelligence claims use APPROXIMATE
equality. Build spec: `HYPOTHESES_TA.md` (PRE-EVIDENCE working doc, committed
with the build package).
**Scope:** wave-1 head-to-head H-TA1 vs H-TA3. **H-TA2 is DEFERRED to wave 2**
(blocked on the missing frozen native inference-step inventory — the builder
does not build it; its bars are restated as deferred in §4).
**Branch:** `tnn-native-lab` (sylorlabs/TNN).

**Amendment rule (from selfpam PREREG, binding here):** this prereg is frozen
at commit time. Any change to a kill-bar threshold, corpus, cell definition,
frozen constant, or decision rule requires a committed prereg amendment naming
the changed sections, committed BEFORE any affected measurement runs.
Post-hoc redefinition of a bar is a prereg violation and invalidates the run.

---

## 1. H-TA1 equivalence-belief finding (protocol step 3 — resolved in the build)

**Question:** does the learner already derive P⇔Q equivalence beliefs with
provenance, or is derivation-log instrumentation itself the first build?

**Answer (verified 2026-09-27):** the learner does NOT. Searched the entire
selfpam tree (`docs/lab/senses/pam-rebuild/selfpam/`, all `.zag`/`.md`/`.jsonl`):
no equivalence-derivation log exists, no P⇔Q edge store, no warrant-edge
machinery. The install machinery (`src/admit_claim.zag`) warrants *claims*,
never equivalences. **Derivation-log instrumentation is therefore the first
build.** Its warrant semantics are preregistered in §5 below — before H-TA1
scores anything, per HYPOTHESES_TA.md §8.

**No-smuggling declaration:** the *gate* never creates edges (protocol
violation if it did). The build is two separate binaries: `ta1_derive`
(installs edges from the derivation log; the learner's derivation machinery)
and `ta1_gate` (reads activated edges, canonicalizes, admits/withholds; the
gate). `ta1_gate` contains no edge-writing code path. The sealed-corpus edge
set is derived from the derivation log only — never from sealed drafts (§7).

---

## 2. Ratified shared kill bars KB-TA-1..6

Ratified UNCHANGED from HYPOTHESES_TA.md §5 (reconstructed bids → law):

| bar | corpus slice | threshold | meaning |
|---|---|---|---|
| KB-TA-1 confabulation withhold | CONFAB-GENUINE + CONFAB-NEAR-MISS + MEANING-SHIFT (440) | withhold ≥ 396/440 (90%) | the gate exists to stop confabulation |
| KB-TA-2 paraphrase admit | PARA-LEGIT (200) | admit ≥ 180/200 (90%) | else the gate is exact-identity in disguise |
| KB-TA-3 related-but-true admit | REL-SUBSET (90) | admit ≥ 77/90 (85%) | Micah's core demand as a number |
| KB-TA-4 adversarial-paraphrase withhold | ADV-PARA (100) | withhold ≥ 80/100 (80%) | else the gate is a fuzzy matcher |
| KB-TA-5 determinism | full corpus | 3/3 byte-identical reruns incl. allocator perturbation | any divergence kills the BUILD; if the mechanism cannot be made deterministic, the hypothesis dies with it |
| KB-TA-6 withhold-only | all runs | zero committed-memory revisions attributable to the gate | any revision kills the build on the spot (trial-1145 rule) |

**REL-ENTAIL (60) is scored per-hypothesis, not a shared bar:** H-TA1
WITHHOLDS by design (documented limitation — no inference in the hypothesis);
H-TA3 mixed (probes may or may not cover the entailed fact). This is the
discriminator the differentiation matrix names, not a kill.

**Kill semantics:** any shared bar fails → that hypothesis's build is dead; the
hypothesis may return only under a new prereg. No post-hoc bar redefinition.

---

## 3. Ratified mechanism-level kill bars

### H-TA1
- **H-TA1-K1 — transitivity collapse.** TRANS-CHAIN stress set (100 drafts whose
  only rewrite path to an evidence unit uses ≥2 chained edges). Audit every
  admitted confabulation's rewrite trace: if >5% of all admitted confabulations
  (across CONFAB classes) trace to a chained edge pair whose endpoints are not
  directly warranted equivalent → chaining semantics structurally unsound →
  **H-TA1 DIES** (not "tune the edges" — chaining *is* the mechanism).
  Builder's note: with claim-shaped units and sound subject-carrying edges, the
  expected outcome is 0 admissions (the subject bytes block cross-subject
  chains; sound edges preserve truth same-subject). The 0/100 is the SOUND
  outcome, not a vacuous test — the per-item rewrite traces (logged by the
  gate) prove chains were attempted and did not reach evidence.
- **H-TA1-K2 — recombination.** RECOMB stress set (200 false claims from
  predicate swaps across subjects). Admit rate >10% → unit granularity
  inadequate *as a mechanism* → **H-TA1 DIES**. Builder's proof obligation:
  claim-shaped units must yield ~0/200.
- **H-TA1-K3 — polarity erasure.** Any ADV-PARA/MEANING-SHIFT item admitted
  where the sole evidence difference is polarity/negation/quantifier and an
  edge erased it → that edge class is banned; if polarity-erasure cannot be
  excluded by the architectural edge constraint (§5) → **H-TA1 DIES**.

### H-TA3
- **H-TA3-K1 — silence-as-consent.** LOW-OVERLAP stress set (150 confabulations
  with <2 shared content tokens with any evidence). Admit rate >10% →
  falsification cannot serve a withhold-only gate → **H-TA3 DIES**.
- **H-TA3-K2 — extraction fragility.** For each PARA-LEGIT withhold, check
  whether grounding/detectors treated two human-audited same-meaning units
  differently for surface reasons. If >10% of paraphrase withholds trace to
  surface sensitivity → the probe comparison is byte-matching in disguise →
  **H-TA3 DIES**.
- **H-TA3-K3 — probe blindness.** Red team demonstrates a confabulation
  DIMENSION (systematic, ≥20 items) that no detector template can cover without
  reintroducing fuzzy matching. If the dimension cannot be covered by a new
  *narrow* detector → **H-TA3 DIES**.

### H-TA2 (DEFERRED, wave 2)
H-TA2-K1 (step slippage), H-TA2-K2 (depth cutoff), H-TA2-K3 (circularity) are
restated here as deferred — they bind the wave-2 build, not this one.

---

## 4. Corpus classification sharpening (builder-ratified)

TA-CORPUS v1: 950 sealed items (60 IDENT + 200 PARA-LEGIT + 90 REL-SUBSET +
60 REL-ENTAIL + 200 CONFAB-GENUINE + 120 CONFAB-NEAR-MISS + 120 MEANING-SHIFT
+ 100 ADV-PARA with trap_notes) against ~200 stipulated Atlas-7 evidence
claims; sealed stress sets RECOMB 200 / TRANS-CHAIN 100 / LOW-OVERLAP 150
(mechanism bars only); optional real-text extension (≤200 items, ecological validity
only, NEVER feeds a kill bar — may be omitted entirely); dual-label + adjudication, unresolved items dropped;
deterministic generators with regenerate-and-diff seal check.

Two sharpenings vs HYPOTHESES_TA.md §7.3 (ratified here as the builder prereg):

1. **REL-SUBSET = unit-subsets only.** The doc's "(subset/weakening)"
   parenthetical is split: REL-SUBSET (90) = draft units are a proper non-empty
   subset of a multi-unit evidence claim's units ("fewer units, all matching" —
   the mechanism-native reading of H-TA1's admission rule). Weakenings
   ("exactly N" → "at least N"; single-sentence "A and B" → "A") are
   *entailments*, not subsets — they are classified as REL-ENTAIL (see 2).
   Rationale: under unit-subset admission a weakening is directed inference,
   which H-TA1 refuses by design; scoring it under REL-SUBSET would punish
   H-TA1 for its documented limitation rather than testing Micah's demand
   (related-but-true admission), which the unit-subset construction tests
   directly.
2. **REL-ENTAIL (60) = entailed-but-novel surface forms:** comparative
   consequences ("X is 10m, Y is 5m" → "X is bigger than Y") AND weakenings
   ("exactly 12,000" → "at least 12,000"). Expected: H-TA1 WITHHOLDS (documented
   limitation, safe direction); H-TA3 mixed (weakening paraphrases admit —
   no detector fires; comparatives mostly withhold on low overlap).

---

## 5. H-TA1 warrant semantics (preregistered — the §8 open question)

What counts as "the learner warranted an equivalence":

- **Derivation episodes** (`episodes.jsonl`, committed with the corpus): each
  episode `ep = (ep_id, P, Q, kind, warrant)` where P is a committed evidence
  claim/unit and Q is a learner-experienced alternate form. Two kinds:
  - `SAME`: a teaching episode asserts Q where P is committed and the episode
    explicitly warrants same-meaning. warrant = 0.9.
  - `INTERCHANGE`: the learner's own audited recall treated P and Q
    interchangeably (logged recall event). warrant = 0.6.
- **Edge extraction** (deterministic, in `ta1_derive` and the reference Python
  implementation in `generators/`): tokenize P, Q on whitespace (case-sensitive);
  take the longest common token prefix and longest common token suffix; the
  middle spans (P_mid, Q_mid) form one candidate edge. Empty span on either side
  → no edge (insertion/deletion is not equivalence). P_mid == Q_mid → no edge.
- **Architectural polarity constraint** (checked at install; violating candidates
  REFUSED and logged): let neg(S) = multiset of frozen-negation-list tokens in
  S. Refuse iff neg(P_mid) != neg(Q_mid). Frozen negation list:
  `not n't never no none nobody nothing neither nor without`.
- **Activation:** edge activated iff warrant ≥ θ, **θ = 0.5 frozen** (both kinds
  activate; the threshold is load-bearing for future kinds).
- **Orientation:** each activated edge is oriented P→Q with Q the
  byte-lexicographically smaller of the two spans (canonical = byte-minimal;
  frozen). Rewriting applies oriented edges only.
- **Rewriting:** per unit, left-to-right scan; at each position, among oriented
  edges whose P matches at that position, take the longest P; ties → lowest
  edge id (frozen order). After a replacement, continue scanning after the
  inserted text. Repeat to fixpoint or **64 rewrites/unit** (frozen bound —
  determinism backstop). Same input bytes → same output bytes regardless of
  match discovery order (fixed scan order + frozen tiebreak).
- **Admission (unit-subset):** ADMIT iff for EVERY canonical draft unit there
  EXISTS a canonical evidence unit (any committed claim, canonicalized at gate
  time with the current edge set — committed bytes never modified) byte-equal
  to it. Otherwise WITHHOLD.
- **Not-a-synonym-table test:** edges carry provenance (deriving ep_id).
  Deleting all edges from episode X must change canonicalization output
  accordingly (procedure in BUILD.md: filter edges.tsv by ep_id, re-run gate,
  diff verdicts). A hardcoded table cannot do this.

---

## 6. Frozen constants (all hypotheses)

**Segmenter S** (shared, frozen, structural): split claim text into units at
sentence terminators `.` `!` `?`, then at clause punctuation `;` `:` `,`
and em-dash (U+2014, bytes E2 80 94). Units are maximal punctuation-delimited
spans, trimmed of surrounding whitespace; empty units dropped. No case folding,
no stopword removal, no stemming in S. **Unit-validity check** (at evidence
ingest): a unit is valid iff it has ≥2 whitespace-delimited tokens AND ≥1 token
not on the closed-class list; invalid units are counted and reported on stderr,
ingest continues (evidence is authored claim-shaped; the check is the
anti-sloppy-unit tripwire for RECOMB).

**H-TA3 frozen constants:**
- Closed-class list: ~200 English function words, frozen, disclosed in
  `lists.zag` (syntactic scaffolding, English-scoped; other languages need
  their own frozen lists — auto-deriving them from corpora is FORBIDDEN).
- Negation list: same 11 tokens as §5.
- Grounding: per draft unit, the evidence unit maximizing shared-token count
  (whitespace-delimited, case-sensitive tokens; closed-class tokens and
  digit-runs excluded from the count). Tiebreak: lowest claim id, then lowest
  unit index. A unit is *grounded* iff it shares ≥1 content token with its
  best evidence unit.
- **Zero-overlap rule:** <2 grounded units in the draft → WITHHOLD.
- **Detectors** run per grounded pair with ≥2 shared content tokens:
  - D1 polarity flip: strip negation-list tokens from both units; stripped
    skeletons byte-equal AND unstripped forms differ → WITHHOLD.
  - D2 quantity mismatch: replace maximal digit-runs with `#` in both units;
    skeletons byte-equal AND some aligned digit-run differs → WITHHOLD.
  - D3 entity substitution: LCS(tokens(d), tokens(e)) ≥ 60% × max(|d|, |e|)
    AND some aligned position i has d[i] ≠ e[i] with both entity tokens
    (non-closed-class, non-digit) → WITHHOLD.
- **Anti-span_sum bulkhead:** overlap NEVER licenses admission — it only
  selects probe sources. If overlap threshold ever decides an admit, the build
  is span_sum in disguise and dies.

---

## 7. No-bridge / no-shopping rules (binding)

1. The derivation log (64 teaching episodes) is built from Atlas-7 evidence
   claims + the style guide ONLY, with a seed independent of the sealed drafts.
   Sealed draft items are never consulted during episode authoring. Episodes
   cover transformation *styles*, not draft *instances*.
2. Builder-tunable constants (§5 θ, §6 lists/thresholds) are frozen on the OPEN
   dev set (≤50 items, `dev/`, never in the sealed corpus) — then frozen.
   Tuning against the sealed corpus is shopping and voids the run.
3. Corpus seal: regenerate-and-diff (scripts+seeds → byte-identical manifest)
   before commit. Post-seal, the corpus is read-only to the builder.
4. **The builder does NOT score the sealed corpus.** Smoke runs use the dev set
   only. The sealed battery is the tester crew's.
5. Optional real-text extension (≤200 items, may be omitted): scored for
   ecological validity only, NEVER feeds a kill bar.

---

## 8. Builder-wave run order (preregistered)

1. Ratify kill bars (this document) → commit BEFORE corpus seal.
2. Freeze constants on the open dev set.
3. Seal TA-CORPUS v1 (regenerate-and-diff check) → commit under
   `docs/lab/senses/pam-rebuild/selfpam/corpora/cell-ta/`.
4. Build H-TA3 (pure Zag) → smoke on dev.
5. Build H-TA1 (`ta1_derive` + `ta1_gate`, pure Zag) → smoke on dev.
6. Tester crew scores blind against the sealed corpus (separate wave).
7. Mechanism kill-bar stress sets scored (tester wave).
8. Red team the survivor's residual surface (separate wave).
9. Adoption discussion only after 8. No adoption talk before.

---

## 9. Preregistered predictions (bids, from HYPOTHESES_TA.md — ratified)

H-TA1: IDENT 60/60; PARA-LEGIT 188/200; REL-SUBSET 84/90; REL-ENTAIL withhold
~55/60 (documented); CONFAB-GENUINE withhold 195/200; NEAR-MISS 110/120;
MEANING-SHIFT 112/120; ADV-PARA withhold 88/100.
H-TA3: IDENT 60/60; PARA-LEGIT 186/200; REL-SUBSET 84/90; REL-ENTAIL ~45/60
mixed; CONFAB-GENUINE withhold 186/200; NEAR-MISS 104/120; MEANING-SHIFT
110/120; ADV-PARA withhold 82/100.
Shared-bar checks: H-TA1 confab set 417/440 = 94.8% ≥ 90% ✓; H-TA3 confab set
400/440 = 90.9% ≥ 90% ✓ (just above — disclosed).

**What "winning" means:** the hypothesis that passes all shared bars AND all
its mechanism bars with the larger margin on its weak cells (H-TA1: ADV-PARA +
PARA; H-TA3: confab set + ADV-PARA). Tiebreak: red-team cost-to-break. If
neither passes, both die; H-TA2's wave-2 prereg is revisited — no rescue builds.

---

*Ratified by the builder crew, 2026-09-28. Committed before the corpus seal.*
