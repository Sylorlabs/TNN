# FROZEN PREREG — KB4 SUSPECT-gate channel shootout (PACKAGE 2)

**Status: FROZEN 2026-09-22. Authorization and freeze recorded below.
No edits after freeze except Micah-signed amendments.**

## §0 Authorization

Lab director Micah, 2026-09-22, authorizing words (recorded verbatim):

> "now that we know it's an info problem try more info go ahead and run test accordingly."

This is the PACKAGE 2 more-info channel shootout for KB4's SUSPECT state,
authorized against the KB4 autopsy
(`kb/autopsy/AUTOPSY.md`, frozen result commit `d22de06b7ee85a01a27adecde0165ac2e79a1112`):
the install gate is Bayes-optimal for its inputs yet fails 41–46% because
"fooled sense" vs "world genuinely changed" are observationally identical on
the judgment stream (0.02–0.03 bits measured vs ~1 bit needed). Micah's
standing rule for this line: SUSPECT resolves ONLY through a causally
independent channel (§1.3 of `PREREG_DRAFT_SUSPECT_GATE.md`).

## §1 Frozen corpus and split

- Corpus: `prose-learning/epistemic_wave/kb4_rerun/` —
  `batch_A.txt`, `batch_B.txt` (frozen gate input, NO truth column;
  line format `stim_idx \t judg_idx \t confidence \t source_id`),
  `truth.json` (scorer-only; carries per-line: stim, stim_idx, truth,
  correct, variant ∈ {primary, noise, adversarial},
  task ∈ {colordisc, colorconst, shapetrans, pitchdisc, timbredisc,
  motiondir}, judgment, confidence — NEVER visible to channel code),
  `mappings.json` (stim_idx → "task/p000"; task name = perturbation class,
  legitimate input).
- Frozen split rule: within each task, the stims BEARING ADVERSARIAL
  FIXTURES sorted by stim_idx ascending; even 0-based positions →
  CALIBRATION (93 stims), odd → TEST (92 stims); both senses.
- Manifest: `kb/autopsy/SPLIT_MANIFEST.json`. Independently recomputed
  from truth.json 2026-09-22: canonical-JSON SHA256
  `bce15d30eb7294361949a84cfd0173110bf8f5aec60792165bf82def7f998368`
  matches the committed file's canonical content exactly (raw-byte SHA256
  differs only in indent whitespace; semantic content byte-identical).
  RESULT: MANIFEST VERIFIED. Not altered. A sibling crew shares this
  manifest.

### Corpus limitation (frozen note, affects channel (b))

The noise variant re-observes the PRIMARY stimulus under independent
sensor noise (verified: every noise line's truth == its primary line's
truth, both senses). There is NO delayed re-observation of the
ADVERSARIAL stimulus in this corpus. A true cross-time consistency
channel ("re-observe the disputed stimulus later") is untestable here;
channel (b) measures the closest available proxy and is expected to carry
~0 bits (autopsy: noise agreement ~no signal).

### Recon facts (read-only, frozen context)

- Adversarial fixtures: A 184, B 185 (per task/class per sense, see §5).
- P(truth preserved | class) on CALIBRATION (both senses pooled):
  colordisc 0.867, colorconst 1.000, shapetrans 0.489, pitchdisc 0.400,
  timbredisc 0.267, motiondir 0.133. The perturbation class carries real
  signal; preservation is sense-independent.
- Calibration sizes per class ≈ 20–46 fixtures (both senses pooled;
  per-sense per-(class×agreement) cells ≈ 5–12 samples — small,
  documented as a limitation).

## §2 Consultant step (pre-freeze)

Two outside consultants were asked (prompt kept the §1.3 constraints)
for concrete, implementable, causally-independent resolution channels.
Verbatim responses committed at:
- `kb/autopsy/channels/consult_sol_verbatim.txt` (gpt-5.6-sol)
- `kb/autopsy/channels/consult_grok46_verbatim.txt` (grok-4.6; labeled
  explicitly — never 4.7)
- grok failure count: 0 (first attempt succeeded). Sol: 0 failures.

## §3 FROZEN CHANNELS

All channels train/calibrate on CALIBRATION only; test truth never
visible to channel code. Scoring unit: each (sense, test adversarial
fixture) — pooled A+B, per-sense rows reported (§5). Channel verdicts:
0=WITHHOLD, 1=INSTALL, 2=SUSPECT.

**(a) Causal perturbation model.** Per-(class × agreement) calibrated
P(J_a correct), where agreement = (J_a == J_p) on judg_idx equality
(same sense: J_p = that sense's primary-variant judgment, J_a = its
adversarial-variant judgment for the same stim_idx). The 12-cell table
(6 classes × 2 agreement values) is calibrated on that target sense's
CALIBRATION adversarial fixtures (correct column from truth.json —
calibration truth only, never test truth). Frozen verdict:
INSTALL iff p ≥ 0.60; WITHHOLD iff p ≤ 0.40; else SUSPECT (thresholds
frozen a priori). Empty cell → p := 0.5 → SUSPECT (frozen).
Bayesian interpretation (documented, not re-estimated): p ≈
P(truth preserved|class) [prior π(c), generator-audit component] ×
sense-tracking likelihood P(agree pattern | preserved/changed) [both
calibrated]; the calibrator also emits π(c),
P(agree|preserved), P(agree|changed), P(J_p correct|class) per class for
audit. This is "predict the observation under H_fooled vs H_changed,
then observe the agreement pattern."

**(b) Cross-time consistency (noise proxy).** Channel observation =
(J_noise == J_a) for the same sense and stim_idx (noise-variant
judgment vs adversarial-variant judgment). Frozen verdict: INSTALL iff
agree, WITHHOLD iff disagree. Corpus limitation per §1: the noise
variant re-observes the primary stimulus, not the adversarial one —
this is the closest available proxy; expected ~0 bits. No calibration
needed.

**(c) Multi-source agreement.** A and B adversarial judgments for the
same stim_idx; verdict = agree(A_Ja, B_Ja): INSTALL iff agree,
WITHHOLD iff disagree. This is autopsy probe P-A1 as a resolution
channel; expected to replicate the correlated-fooling failure —
reported honestly. No calibration needed.

**(d) Consultant-invented channels (frozen included/excluded lists).**

INCLUDED (implementable on the frozen corpus without test-truth
leakage, with frozen verdict rules):

- (d1) Confidence-threshold negative control (anticipated by sol's
  closing warning; autopsy already proves confidence anti-informative:
  wrong ≥ correct). Frozen rule: t = median adversarial confidence
  over the target sense's CALIBRATION adversarial fixtures (sorted
  ascending, lower-middle element on even n — deterministic); candidate
  rules "INSTALL iff conf ≥ t" and "INSTALL iff conf < t" scored on
  calibration resolution accuracy; the higher-accuracy orientation is
  frozen; ties → the anti-informative orientation ("WITHHOLD iff
  conf ≥ t"), documented. No SUSPECT output. Labeled NEGATIVE CONTROL.
- (d2) Confidence-delta negative control (grok-4.6 suggestion #4,
  reduced to its implementable core: "inspect cross-variant confidence
  deltas"). Frozen rule: delta = adv_conf − prim_conf per fixture;
  identical median/orientation/tie-break procedure as (d1) on
  calibration. No SUSPECT output. Labeled NEGATIVE CONTROL.

EXCLUDED (with reasons):

- sol #1 class-specific analytic causal checker — not implementable:
  the corpus carries no stimulus data (only judgment strings and ids);
  a checker operating "on the stimulus or physical trace" has nothing
  to operate on.
- sol #2 independent physical sensor basis — not implementable offline;
  no second physical sensor exists in this corpus.
- sol #3 human verification — not implementable in this run; no human
  in the loop (Micah-as-oracle is a governance step, not a channel).
- sol #4 physical counterfactual/reversal test — not implementable;
  stimuli cannot be re-rendered or intervened on from judgment batches.
- sol #5 causal provenance / generator audit — the implementable core
  (perturbation-class preservation verified against independent ground
  truth) is subsumed by channel (a)'s prior π(c); the code/seed audit
  remainder is not implementable offline.
- sol #6 external task outcome / instrumented consequence — not
  implementable; no downstream instrument exists in this corpus.
- sol #7 cross-modality replication — not implementable; the corpus has
  no genuinely different modality (A/B are two ML judgment pipelines;
  §1.3 forbids treating them as independent).
- grok-4.6 #1 human verification — excluded, same as sol #3.
- grok-4.6 #2 cross-modality sensor check — already channel (c);
  NOT counted as independent evidence.
- grok-4.6 #3 ground-truth stimulus reconstruction — not implementable;
  no raw stimulus/waveform/image data in the corpus.
- grok-4.6 #5 hand-engineered analytic detectors (Hough,
  autocorrelation) — not implementable; no raw signal to run them on.
- Any learned resolution model trained on frozen judgments,
  confidences, stimulus ids, or agreement patterns (explicitly warned
  against by sol's closing paragraph): EXCLUDED — apparent bits on the
  corpus, ~0 causal bits about the real question.

## §4 FROZEN COMBINATIONS (no-free-lunch)

- (a)+(c): INSTALL iff BOTH components say INSTALL; WITHHOLD iff BOTH
  say WITHHOLD; else SUSPECT.
- (a)+(b): INSTALL iff BOTH say INSTALL; WITHHOLD iff BOTH say
  WITHHOLD; else SUSPECT.
No other combinations. No post-hoc combination search.

## §5 FROZEN METRICS (pure Zag reasoning/measuring; Python glue for
file prep and scoring only)

Per channel and per combination, on the TEST split (pooled A+B
adversarial fixtures; per-sense rows also reported):

- **bits** = I(channel verdict; adv_correct), mutual information in
  bits, verdict alphabet {INSTALL, WITHHOLD, SUSPECT}. Correct action
  for a fixture = INSTALL iff the adversarial judgment is correct.
- **resolution accuracy** = P(verdict matches correct action |
  verdict ≠ SUSPECT).
- **false-install rate if installed-on-INSTALL-verdict** =
  P(adv judgment wrong | verdict = INSTALL). THE deployability number.
- **cost/latency class**: (a) immediate table lookup; (b) delayed
  re-observation (proxy); (c) immediate (second sense, same time);
  (d1),(d2) immediate table lookup; combos = max of components.
- **SUSPECT rate** and **SUSPECT precision** (operational: fraction of
  SUSPECT verdicts whose primary and adversarial judgments differ —
  the genuinely unresolvable cell per the autopsy).
- Denominator context: prior entropy H(adv_correct) on TEST (~1 bit),
  reported by the scorer.

## §6 FROZEN CHAMPION CRITERION

The champion is the channel (or combination) delivering the most bits;
tie-break = lower cost/latency. The false-install-after-resolution rate
is ALWAYS reported alongside. A high-bit channel that installs poison
is not deployable: if the bit-leader's false-install rate exceeds the
standing 10% memory-integration bar, the report names it
"champion-on-bits but NOT DEPLOYABLE" and names the best deployable
alternative (most bits among channels ≤10% false-install). If no
channel beats the judgment-only baseline's bits, the report names
"no champion" with why.

## §7 ANTI-GAMING

- Channel code sees only batch lines + class labels + variant maps +
  calibration-derived tables. truth.json is NEVER opened by channel
  code; calibration tables derive from calibration-split truth only,
  via the committed prep script (`prep_inputs.py`), which is audited
  to emit no test-truth fields.
- Zero RNG in any path. 3× runs byte-identical (SHA256) or the result
  is void.
- Pure Zag for all reasoning and measuring (calibration, verdicts,
  contingency counts). Python only for glue: consultant prompting,
  input file prep, scoring (MI arithmetic from Zag-emitted counts),
  report writing.
- No threshold tuning after seeing results: all thresholds frozen in
  §3. Calibration is mechanical (cell rates, medians, orientation by
  calibration accuracy) with no human choice points.
- The scorer cross-checks: every Zag-emitted contingency count against
  an independent recompute from verdict lines + truth.json; any
  mismatch voids the run.
- Binaries and .zagd caches are never committed; rebuild command
  recorded in `kb/autopsy/channels/`.

## §8 Deliverables (all under `kb/autopsy/channels/`)

`PREREF` this file (frozen reference copy);
`consult_sol_verbatim.txt`, `consult_grok46_verbatim.txt`;
`inputs/` (stimclass.txt, split.txt, variant_A.txt, variant_B.txt,
calrows_A.txt, calrows_B.txt) + `prep_inputs.py`;
`src/chan.zag` (+ substrate copy), build command;
`out/run1..3/` verdict outputs + SHA256s;
`score_channels.py`, `scores.json`;
`SHOOTOUT.md` — full metric table, named champion (or "no champion"
with why), consultant included/excluded accounting, and the SUSPECT-gate
consequence: which channel should resolve SUSPECTs.

---

**Freeze checklist (verified before commit):**
[x] authorization quote (§0)
[x] split rule + manifest verification result (§1)
[x] channels (a),(b),(c) with exact verdict rules (§3)
[x] channel (d) included list with frozen verdict rules + excluded
    list with reasons (§3)
[x] combinations with verdict rules (§4)
[x] metrics incl. prior-entropy denominator (§5)
[x] champion criterion incl. non-deployability clause (§6)
[x] anti-gaming (§7)
