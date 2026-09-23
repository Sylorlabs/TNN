# EXPLORATORY — NOT EVIDENCE

# Cross-Thread Pattern Mining — Wide-Exploration Standing Watch

**Doc status:** EXPLORATORY WORKING PAPER. Nothing in this document is program evidence.
Nothing here changes, reinterprets, or softens any frozen bar, metric, or kill criterion.
All preregistered items remain exactly as Micah signed them (PREREG_FREEZE.md, 2026-09-21).
Anything here that contradicts a frozen assumption is routed to an **AMENDMENT PROPOSAL**
section — it has no effect until Micah signs it.

**Provenance discipline:** every finding below is labeled with exact file + line provenance
and a strength-of-evidence note. Most Phase-1 findings come from ONE old Python-era dataset
each — they are **hints, not findings**. The word "finding" in this document means "a
candidate pattern worth a preregistered test," never "an established result."

**Phase 1 (this document, now):** mine already-committed evidence for patterns nobody preregistered.
**Phase 2 (standing watch, §PHASE-2-PROCEDURE):** the pre-committed mining procedure to run as
R0 / Track-A / Track-B results land in committed evidence.

---

## §SOURCES (Phase 1)

| ID | Path (workspace) | Provenance of numbers |
|---|---|---|
| S1 | `units/archaeology_r31/R31_CHUNKING_TOURNAMENT_SUMMARY.json` | 8-arm chunking tournament, 5 seeds (3101–3105), Python shadow, REFERENCE_ONLY |
| S2 | `units/archaeology_r31/docs_generations_R31_R31_CHUNK_CAUSAL_ABLATION_REFERENCE_ONLY.json` | causal ablation, 3 routes × 6 seeds (9900–9905), REFERENCE_ONLY |
| S3 | `units/archaeology_r31/docs_generations_R31_R31_CHUNK_DOSE_CURVE.json` | dose curve, 1 seed (8101), doses 250–8000, REFERENCE_ONLY |
| S4 | `units/ALPHABET_A-F.md` | catalog arms A–F, 249 lines |
| S5 | `units/ALPHABET_G-L.md` | catalog arms G–L + K3, 647 lines |
| S6 | `units/ALPHABET_M-R.md` | catalog arms M–R, 320 lines |
| S7 | `units/ALPHABET_S-X.md` | catalog arms S–X, 322 lines |
| S8 | `units/ALPHABET_Y-Z.md` | catalog arms Y–Z, 538 lines |
| S9 | `units/METRICS.md` | M1–M9 metric operationalizations |
| S10 | `units/RISKS.md` | R1–R10 ranked risks |
| S11 | `units/ARCHAEOLOGY_R31.md` | archaeology verdict sheet (narrative summary of S1–S3) |

Note: `R31_CHUNK_CAUSAL_ABLATION_REFERENCE_ONLY.json`, `R31_CHUNK_DOSE_CURVE.json`, and
`R31_CHUNK_MASTER.json` in `archaeology_r31/` are **0 bytes** (empty placeholders); the
`docs_generations_R31_*` files carry the content. Flagged so a successor does not mistake
the empty files for missing evidence.

---

## §PHASE-1-FINDINGS

### HEADLINE-1 — The "grounded" signal bought ~nothing in the old tournament

**Pattern:** S1 contains a direct head-to-head of the same MDL chunker with and without the
grounded-consequence signal: `adaptive_mdl` vs `grounded_adaptive_mdl`. On the tournament's
own capability composite the delta is **+0.00019** (0.47155 → 0.47174) — a null to four
decimal places. Condition-level deltas: `matched_boundary_f1_evalonly` +0.0019,
`matched_grounded_acc` −0.0011, `hard_noise_grounded_acc` −0.0054, `paired_retrieval_20way`
+0.0088. Nothing exceeds one percentage point.

**Why surprising:** the program's flagship (Arm D) is built on the thesis that grounded
consequence consistency is a load-bearing cut signal (ALPHABET_A-F, Arm D §1: compression
"admissible but cannot dominate grounding"; ARCHAEOLOGY_R31 §"Boundary signals" lists it as
signal #2). The old evidence the thesis cites (S11) leans on the *ablation* (S2) and the
mechanism story — but the tournament's own grounded-vs-ungrounded comparison says the
grounding term did not move the needle.

**Honest caveats (must be read with the headline):**
- N=5 seeds, one synthetic acoustic-stream dataset, REFERENCE_ONLY. This is a hint.
- The composite may be retrieval-dominated (see HEADLINE-adjacent finding F-1 below), which
  could mask a real grounding effect on other axes.
- The ablation (S2) DOES show the dual route's value, but it tests dual-vs-raw routing, not
  grounded-vs-ungrounded cutting.

**What it suggests to test (proposal, not change):** the native redo (R0) should include the
grounded-vs-ungrounded ablation as an explicit preregistered comparison inside Arm D's
build, with the preregistered expectation being the null or near-null from S1 — i.e., make
the old tournament's own number the prediction D has to beat. If grounding really is
load-bearing, this is where it should show up first.

---

### HEADLINE-2 — The dual route is insurance, not additive: its gain concentrates where raw fails

**Pattern:** S2 aggregate: dual_active `near_twin` = 0.8363 vs raw_active = 0.8186 (+0.0177)
— S11 reports these numbers. The unreported pattern is per-seed (S2 `rows`):
seed 9900: raw 0.9415, dual 0.9338 (−0.0077, raw wins); 9901: +0.0238; 9902: +0.0138;
9903: +0.0208; 9904: +0.0100; 9905: +0.0454. The dual-minus-raw gain is **largest where raw
is weakest** (seed 9905: raw 0.6731 → dual 0.7185) and negative where raw is strongest
(seed 9900: raw 0.9415). Rank correlation between raw level and dual gain is strongly
negative — the chunk route rescues hard cases and slightly degrades easy ones.

**Secondary unreported detail from the same file:** dual costs *more* evidence requests
(`request_rate` 0.4110 vs raw 0.3974, +0.0136) while hard grounding is dead even
(`hard_mean` 0.9209 vs 0.9213, −0.0004). The 0.8525 compression gain is bought at a small
but real evidence-request surcharge — "adding chunks cost nothing" (S11's gloss) is true
for accuracy and false for evidence traffic.

**Why it matters for the prereg:** METRICS.md M3's churn protocol and the scenario-fit
dimension "pressure regime" already score recall under stress. HEADLINE-2 predicts the
dual route's value will show up *as a pressure × difficulty interaction*: dual ≫ raw on
the hardest slices, dual ≈ raw or slightly worse on easy slices. If the native R0 redo
reports only mean accuracy, it will average away exactly the effect S2 shows. Proposal:
preregister a difficulty-binned analysis (performance as a function of baseline/raw
performance) — a positive slope on "dual gain vs raw weakness" would turn this hint into
a finding.

---

### HEADLINE-3 — The dose curve dips before it flattens: a recruitment-overshoot transient

**Pattern:** S3 (`rows`, one seed 8101): `hard_mean` at dose 250 → 500 **drops** for all three
kinds — adaptive 0.3886 → 0.3629, grounded 0.3811 → 0.3686, hierarchical 0.3903 → 0.3714
(about −0.02 each) — then recovers slowly, reaching 0.3989/0.3983/0.3994 by dose 8000.
S11's summary ("flat ~0.36–0.40 from 250 → 8000 — no dose effect") is correct at coarse
grain but misses the consistent early dip and the monotonic-ish recovery: it is a small
U-shape, not a pure flatline. Meanwhile `units_per_micro` is essentially constant across
32× dose (adaptive 0.655–0.659, grounded 0.651–0.667, hierarchical 0.613–0.618) and
`mean_chunk_len` is constant (adaptive 1.52–1.53): the vocabulary's compression profile
saturates by dose 250 and never moves again.

**Why surprising:** the program's cold-start story (ALPHABET_A-F, P-D3: "D crosses C-W
between 1x and 3x") assumes early growth then crossover. S3 suggests the opposite shape
for self-recruited vocabularies: an **early overshoot** (the recruiter admits junk at
low evidence, accuracy dips) followed by stabilization — the crossing point is not when
the vocabulary *grows into* competence but when it *recovers from* over-recruitment.

**Caveat:** N=1 seed, single old dataset, REFERENCE_ONLY. The dip could be seed noise.
**Proposal for R0:** the redo's dose/scale legs should log per-dose promotion counts and
revision counts (not just accuracy), preregistered against this hint: if the native redo
shows accuracy-dip-at-2×-dose with a spike in promotions, HEADLINE-3 graduates from hint
to finding. This is cheap — it is just two extra logged series on legs already planned.

---

### F-1 — Tournament ranking is retrieval-dominated; boundary F1 and grounded accuracy barely discriminate

**Pattern (S1):** `capability_composite` ranks predictive_surprise (0.7376) ≫ random_chunks
(0.4988) ≈ fixed_window_4 (0.4928) > hierarchical_mdl (0.4731) > grounded_adaptive (0.4717)
> adaptive_mdl (0.47155) > raw_micro (0.4489). The composite spread is driven almost
entirely by `paired_retrieval_20way`: predictive_surprise 0.94 vs everyone else 0.058–0.101.
On `matched_grounded_acc` the whole field sits in 0.52–0.62 — raw_micro (no chunking)
scores **0.6189, the best of any non-oracle arm**. On `matched_boundary_f1_evalonly` the
MDL learners (0.293–0.308) do NOT beat random_chunks (0.4155) or fixed_window_4 (0.4618).

**Two things the catalog authors under-weighted:**
1. **Metric × granularity interaction:** boundary F1 peaks at mean chunk length ~4
   (fixed_window_4: 0.4618; random_chunks at 4.83: 0.4155) and falls on both sides
   (adaptive_mdl at 1.58: 0.2931; predictive_surprise at 32.3: 0.1566; raw_micro at 1.0:
   0.1946). Grounded accuracy shows no such peak — it slightly *favors* short chunks.
   METRICS.md's M1 already splits content recall from boundary fidelity (good), but no
   arm's prediction set (S4–S8) states the expected F1-vs-length curve. The old data
   predicts an inverted-U, not "longer is more cognitive."
2. **Learning chunks hurt retrieval:** raw_micro's `paired_retrieval_20way` (0.1013) exceeds
   all three MDL learners (0.0638–0.0737). Recruiting a vocabulary *degraded* retrieval
   relative to raw microfeatures. Only the giant-span exploit (predictive_surprise, mean
   len 32.3, retr 0.94) beat raw — and S11 already flags that arm's win as partly a
   compression exploit the docs rejected. The honest reading: the old tournament never
   showed a learned chunker beating raw features on retrieval, which is the exact
   capability Micah's "caching territory" thesis needs (ALPHABET_G-L §"Cross-cutting laws"
   prices dedup as the caching claim; ALPHABET_M-R Arm M's M7 dedup bar is ≥0.4).

---

### F-2 — `novel_composition` is the hardest probe axis in both old batteries, by a wide margin

**Pattern:** S3 dose curve, all doses × kinds: `novel_composition` mean = 0.2829 vs the
next-hardest condition `hard_noise` = 0.3946 — an 11-point gap, and the ordering
(novel_composition dead last) holds at every single dose for every kind. In S1's
tournament, `novel_composition_grounded_acc` is also the lowest grounded-acc condition
for every arm (e.g., fixed_window_4: 0.5214 vs 0.5457–0.5726 elsewhere; oracle latent
itself drops to 0.8366 on novel_composition vs 0.9429–0.9551 elsewhere — even the oracle
feels it).

**What the catalog missed:** none of S4–S8's falsifiable predictions names
novel-composition robustness as a predicted strength *or* weakness; METRICS.md M1/M4
probe recall and revision but nothing isolates "compose a unit never seen before from
familiar parts" as its own axis. The old data says this is the most discriminating
condition in the battery — the new program's M9 (composition) exists in S7's battery
(B9) but S9's M1–M8 do not carry it as a metric. Proposal: when R0/Track-A report,
score novel-composition probes separately rather than folding them into aggregate
accuracy — S1/S3 say the fold hides the sharpest signal.

---

### F-3 — The 53-arm catalog collapses to ~20 distinct mechanisms; the catalog names most of the redundancy itself

**Pattern (S4–S8 cross-read):** counting genuinely distinct mechanism families rather
than lettered arms:
- **Identity axis (what the ID means):** counter (M), content-hash (K1/K2), position
  (L1/L2), composition-proof (M2), versioned-lineage (Y3), recipe/program (Z5),
  epoch-relative (L2), negotiated/witness/contract (Y1/Z1/Z2 — process-bound),
  fuzzy-bounded (Z8), provenance-tiered (Z7), dialect-namespaced (Z4) → ~8 families.
- **Cut-signal axis (where boundaries fall):** statistical recurrence (D/F-B/P/S/R),
  prediction-surprise (F-S), compression-optimal (R), deliberative (H1/H2/Y1/Z1/R2),
  taught/imposed (O/C-W/C-P/V/B), pressure-triggered (G1/G2), economic (Z3),
  history-scarred (Z6), query-lazy (Y4), episode-acts (T), recompute-no-store (U/E),
  none (A/X) → ~10 families.
- **Structure axis (how chunks relate):** tree (I1), DAG (I2), tilings (J1/J2),
  multi-granularity (W), span-sets (Y5), tombstone-refcounted (Y6) → ~5 families,
  plus annotation (N) and acquisition (O/P/Q) which cross the axes.

The catalog **itself proposes** redundancy merges: R2↔Z1 (S6), F-B↔F-S (S4, kill rule),
H1↔H2 (S5), I1↔I2 (S5), J1↔J2 (S5), K1↔K2 (S5), L1↔L2 (S5), G1↔G2 (S5),
D↔D-T↔D-R (S4), U↔D (S7, storage-only difference), E↔D (S4, "D with extra steps"),
S≈D-crystallization (S7's rule = S4's acquisition made explicit), Y3≈M2
(both re-ID on revision; S6/S8 name the near-neighbor), Z5≈U (S8 names it).

**Why it matters for Phase 2:** the pruning structure is already half-specified by the
authors' own kill rules. The mining watch should track **family-level** verdicts, not
just arm-level: if e.g. all three statistical-recurrence cut signals (D, F-B, R) fail the
same boundary bar while deliberative ones survive, that is one thesis-level signal, not
three independent arm deaths. Conversely, correlated failure within a named redundancy
pair (H1 and H2 both dying on cost) is *expected* — it should not be reported as two
surprises.

---

### F-4 — Dose-curve flatness predicts nothing about arm families — but that is itself informative

**Pattern:** S3 shows flat dose response (Δhard_mean ≈ +0.01 over 32× dose) for all three
MDL kinds simultaneously, while their tournament composites are near-identical too
(0.4715–0.4731). The catalog's predicted strength/weakness sets (S4–S8) never use dose
response as a discriminator, and the old data suggests they are right not to: dose
flatness held across the adaptive/grounded/hierarchical split. The one place the catalog
*does* lean on dose — P-D3's cold-start crossing prediction (S4) — is exactly where S3's
dip-transient (HEADLINE-3) complicates the story.

---

## §AMENDMENT-PROPOSALS (frozen-assumption tensions — NO EFFECT until signed)

None of the Phase-1 hints contradict a frozen bar or metric. The following are *procedure*
proposals that would need Micah's sign-off if the watch ever acts on them:

1. **AP-1:** Add a difficulty-binned dual-vs-raw analysis to the R0 redo (HEADLINE-2).
   Needs sign-off because it adds a preregistered analysis to a frozen workstream.
2. **AP-2:** Log per-dose promotion/revision counts on R0 scale legs (HEADLINE-3). Adds
   logged series; does not change bars.
3. **AP-3:** Score novel-composition probes as a separate reported axis in Track-A/B
   results (F-2). Adds a reporting column; does not change any metric's definition.
4. **AP-4:** Track family-level verdict rollups alongside arm-level verdicts in the
   mining watch (F-3). Watch-internal only; affects no arm's fate.

---

## §PHASE-2-PROCEDURE (pre-committed mining discipline for incoming evidence)

This procedure is committed **now**, before R0/Track-A/Track-B results exist, so that
later mining is disciplined rather than p-hacked.

### P2.1 — Trigger and scope
- The procedure runs each time a **committed** evidence artifact lands (results committed
  to the repo under the prereg; provisional/draft numbers are never mined).
- Mining NEVER produces evidence: its outputs are labeled EXPLORATORY and may only
  propose amendments or new preregistered tests. A mined pattern may not be cited in
  any verdict sheet as support.

### P2.2 — Frozen analysis family (the only computations permitted without a new amendment)
1. **Catalog-prediction audit table.** For every arm, translate its predicted strengths
   (S1/S2/…) and weaknesses (W1/W2/…) from S4–S8 into checkable yes/no/partial cells
   against the reported numbers. Compute per-arm hit rate and, more importantly,
   **sign errors** (predicted strength observed as weakness or vice versa). Sign errors
   are the highest-priority mining output.
2. **Metric co-movement matrix.** Spearman rank correlations across arms for every
   metric pair (M1–M7 as applicable; M9 descriptors as ordinals), computed separately
   per corpus and per scale leg. Report the matrix in full — including near-zero and
   negative entries — never just the large ones.
3. **Family-signature vectors.** For each mechanism family (§F-3), the vector of its
   arms' section-champion counts and kill-bar distances; test whether family membership
   predicts outcomes better than chance (descriptive; no p-values at N=arms).
4. **Dose/scale response shapes.** Per arm: fit no curves; report raw per-leg numbers
   plus the S3-derived descriptors (early-dip depth, saturation dose, late slope sign).
   Compare against the HEADLINE-3 hint explicitly: did the dip replicate?
5. **Difficulty-binned treatment effects.** For every dual/ablated comparison, bin by
   baseline difficulty and report the treatment effect per bin (HEADLINE-2 template).

### P2.3 — "Interesting" thresholds (flags, not conclusions)
A pattern is flagged for the watch report iff it meets **all** of:
- **(a) Cross-condition replication:** appears on both corpora OR both scale legs
  (single-corpus, single-leg patterns are logged but not headlined).
- **(b) Effect size:** |rank correlation| ≥ 0.5 for co-movement; sign error on a
  catalog prediction (any magnitude); ≥ 10-point swing or rank-order reversal for
  dose/scale effects; family-level hit-rate deviation ≥ 2 arms from the arm-level
  expectation.
- **(c) Non-redundancy:** not already predicted by the catalog (check S4–S8 first —
  a "discovery" that the catalog predicted is a confirmation, reported as such).
- **(d) Honest N:** the report states the N (arms, seeds, legs) behind the pattern
  and the sentence "N=<k> — this is a hint, not a finding" appears verbatim for k < 8.

### P2.4 — Anti-p-hacking rules
1. The analysis family (§P2.2) is frozen; any computation outside it needs a dated
   watch amendment noted in this doc before it runs.
2. **Report nulls:** every watch report includes "patterns checked and not found"
   (at minimum: the five Phase-1 headlines re-tested against new data).
3. **No peeking-driven re-analysis:** thresholds (§P2.3) may not be lowered after
   seeing the data. If a near-miss looks important, it is logged as a near-miss and
   proposed as a preregistered test for the next round — never promoted by moving
   the bar.
4. **Separation of miner and judge:** the watch proposes; verdict sheets and kill
   bars are executed by the preregistered rules only. A mined pattern never
   accelerates, delays, or reinterprets a kill.
5. **One exploratory corpus rule:** if any analysis choice (bin edges, family
   boundaries, correlation metric) is changed mid-program, the changed analysis is
   re-run from the first committed evidence artifact with the new choice and both
   versions are reported.

### P2.5 — Watch report format (per evidence drop)
1. Header: EXPLORATORY — NOT EVIDENCE; evidence artifact mined (commit hash).
2. Catalog-prediction audit: sign errors first, then hit rates.
3. Flagged patterns (each with §P2.3 a–d satisfied, file/line provenance of the
   numbers used, verbatim N-hint sentence where required).
4. Nulls checked and not found.
5. Amendment proposals (if any) — clearly marked as needing Micah's signature.

---

*End of pattern-mining working paper. Phase 1 complete on committed evidence S1–S11.
Standing watch armed for R0/Track-A/Track-B evidence drops.*
