# PIPELINE REPORT — hell-hole V4 full re-run (PIPELINE crew)

**Date:** 2026-09-23. **Status:** COMPLETE — all bars met, no commit (per task).
**Baseline to beat (v3 frozen):** M1 = 0.818, K1 = 0.182.
**Result (v4):** M1 = **1.0000** (11/11), K1 = **0.0000** (0/11) — **both arms**.
All other v3 bars hold (M3 1.0, K2 0.0, M-LOGIC 1.0, M-JOKE 0.0, K-JOKE 0.0, K3/K4/K5 CLEAR).

## Verdict path (pure Zag, zero RNG)

| Stage | Component | Binary | SHA-256 (prefix) |
|---|---|---|---|
| R12 stance | `crews/integ/r12_v4` (A1 52/52, A3 51/51, A4 ≥0.85 fam) | `84be4b81…bc9b` | matches integ crew's verified build |
| R6 native logic | `crews/c2/logic_bin` (167/168, freeze intact) | `1688e42a…f631` | shipped C2 binary |
| Joke intent | `work/joke_v4` (drives vendored `g_intent6_v4.zag`) | `31d07074…dbfa8d` | vendored source = jokefix original (`71a33af3…`), byte-identical |
| Trial driver | `work/v3_trial` (compiled from v3 source) | `093edccb…3621a` | source byte-identical to committed `phase3/trial_v3/src/v3_trial.zag` (diff-verified) |

Pipeline order is the frozen v3 order: **R3 gate → R6 logic → joke → R5 vote**.
Python (`build_r6.py`, `assemble_v4.py`, `score_v4.py`, `run_pipeline.sh`) is
assembly/scoring/orchestration harness only — it never decides a disposition.
The single decider is the Zag trial driver. No Python in the verdict path.

## 1. R3 gate re-run — 6/6 WITHHOLD ✅ (bar: 6/6)

The `gated` column is no longer hand-transcribed (C1 finding F2). It is derived
**mechanically** by `assemble_v4.py` from the frozen `v3_course.json`
`claim_type` field: `gated = claim_type ∈ {CONTESTED, AMBIGUOUS, EVOLVED, SKEPTICISM}`.
The derived set is exactly {V3-10, V3-11, V3-12, V3-13, V3-18, V3-19} — the same
values v3's hand column held (no transcription error existed in the values, only
in the method). The gate rule itself runs in the Zag driver (checked first,
terminal — cannot be overridden by R6/joke/R5).

| CID | claim_type (frozen course) | v4 disp (solo / helper) | attrib |
|---|---|---|---|
| V3-10 | CONTESTED | WITHHOLD / WITHHOLD | R3 |
| V3-11 | CONTESTED | WITHHOLD / WITHHOLD | R3 |
| V3-12 | CONTESTED | WITHHOLD / WITHHOLD | R3 |
| V3-13 | EVOLVED | WITHHOLD / WITHHOLD | R3 |
| V3-18 | SKEPTICISM | WITHHOLD / WITHHOLD | R3 |
| V3-19 | SKEPTICISM | WITHHOLD / WITHHOLD | R3 |

## 2. R6 contradiction re-run — 6/6 REJECT, native-derived ✅ (bar: 6/6)

The seeded `logic_verdict` column is gone (C1 finding F1). Verdicts come from
`logic_bin` over proposition rows built by a **deterministic mechanical mapping**:

**Mapping rule.** For each v3 R6 case, take the course's mechanistic seed identity
S(c) from its own `mechanistic` block: V3-20→ML-20, V3-21→ML-21, V3-22→ML-22,
V3-23→ML-23, V3-24→ML-24. V3-14→ML-21 per the course's explicit pairing
(discovery field: "Paired with the mechanistic seed V3-21"; notes: "the R6
mechanistic verdict also CONTRADICTS"; the seed's own composition step 5 states
the joke phrasing's "non-toxic" qualifier does not change the verdict).
The proposition bytes are the C2 **frozen** `mlogic.tsv` rows verbatim
(re-freeze 2026-09-23 17:45 UTC, SHAs pinned in `BATTERIES_FROZEN.md`),
ids renamed `R6-V3-XX`. No new propositions authored, no verdict column written —
the oracle field is inert (the engine parses fields 0–2 only). `DENY(2)` ⟺
`CONTRADICTS` → `REJECT` per prereg §1-R6 (CONTRADICTS beats any vote count).

| R6 row | claim prop | evidence props | engine tag | proof | v4 disp |
|---|---|---|---|---|---|
| R6-V3-14 | `EDIBLE(pizza)` | `NON_TOXIC(glue);CAUSE(SAFE(non_toxic_glue,pizza),NOT(EDIBLE(pizza)))` | 2 DENY | R-CAU-DENY | REJECT (R6) |
| R6-V3-20 | `CURES(chocolate,insomnia)` | `CONTAINS(chocolate,caffeine);STIMULANT(caffeine);CAUSE(WORSENS(caffeine,insomnia),NOT(CURES(chocolate,insomnia)))` | 2 DENY | R-CAU-DENY | REJECT (R6) |
| R6-V3-21 | `EDIBLE(pizza)` | (same as R6-V3-14) | 2 DENY | R-CAU-DENY | REJECT (R6) |
| R6-V3-22 | `CURES(bleach,infection)` | `CORROSIVE(bleach);CAUSE(DAMAGES(bleach,tissue),NOT(CURES(bleach,infection)))` | 2 DENY | R-CAU-DENY | REJECT (R6) |
| R6-V3-23 | `IMPROVES(carrots,night_vision)` | `SATURATED(retinol_pathway);CAUSE(LIMITS(saturated_retinol_pathway,absorption),NOT(IMPROVES(carrots,night_vision)))` | 2 DENY | R-CAU-DENY | REJECT (R6) |
| R6-V3-24 | `CAUSE(CONTAINS(coffee,melatonin),WAKES_UP(coffee,drinker))` | `NOT(CONTAINS(coffee,melatonin))` | 2 DENY | R-CAU-PROP-DENY | REJECT (R6) |

All six dispositions are REJECT via native R6 precedence in both arms.
(K-MLOGIC-equivalent: 5/5 seeds + the V3-14 pairing all derive contradiction.)

## 3. Full pipeline — M1/K1 before vs after

382-row context: the 72 v3 evidence rows were re-tagged by `r12_v4`
(plus 9 helper observations); votes re-weighted with the frozen v3 tiers
(T3=32, T2=16, T1=8, T0=4, T−1=1; 0 tier conflicts, 1 tier-1 default
`enviroliteracy.org` — same default v3 used); joke intents re-classified by
`g_intent6_v4` (V3-14→2, V3-15→2, V3-16→2, V3-17→5 — identical to v3's,
now machine-derived).

| Measure | v3 (frozen) | v4 solo | v4 helper | Bar |
|---|---|---|---|---|
| **M1** bullshit detection | 0.818 (9/11) | **1.0000 (11/11)** | **1.0000 (11/11)** | ≥ 0.818, no regress ✅ |
| **K1** false-install rate | 0.182 (2/11) | **0.0000 (0/11)** | **0.0000 (0/11)** | < 0.20 ✅ |
| M3 contradiction | 1.0 | 1.0 | 1.0 | ≥ 0.80 ✅ |
| K2 blind-pick | 0.0 | 0.0 | 0.0 | ≤ 0.30 ✅ |
| M-LOGIC | 1.0 | 1.0 | 1.0 | ≥ 0.80 ✅ |
| K-LOGIC | CLEAR | CLEAR | CLEAR | ≥ 0.50 ✅ |
| M-JOKE deadpan | 0.0 | 0.0 | 0.0 | ≤ 0.10 ✅ |
| K-JOKE helper deadpan | 0.0 | 0.0 | 0.0 | < 0.25 ✅ |
| K3 corruption | OK | OK | OK | none ✅ |
| K5 capture (INSTALL of FALSE) | none | none | none | none ✅ |
| Oracle agreement (descriptive) | — | 22/24 | 23/24 | — |

The two false installs are gone and nothing else moved against the oracle:
**V3-05** `w1=56 w2=36 → INSTALL` becomes `w1=24 w2=68 → REJECT`;
**V3-07** `w1=44 w2=12 → INSTALL` becomes `w0=20 w1=4 w2=36 → REJECT`.
The V3-03 miss persists in the **solo** arm only (see §5); the helper arm now
installs it correctly. V3-17 remains a safe WITHHOLD (classifier has no
sungazing pattern — unchanged from v3, still safe).

## 4. Helper-disposition check ✅ (one justified change, fully documented)

Frozen helper artifacts are **byte-identical to v3** (same `helper_obs.tsv`
9 texts, same `helper_jokes.tsv` 4 intents/markers — read from the same frozen
files, never regenerated). The helper rule (AGREE / ADOPT_HELPER /
KEEP_CLASSIFIER) and its outcomes are unchanged: V3-15/16 ADOPT_HELPER→SATIRE→
REJECT, V3-17 AGREE→WITHHOLD, V3-14 R6 precedence. **K-JOKE = 0/4.**

What changed is the *classifier's* reading of the helper texts (machinery, not
helper behavior) — v3→v4 tags on the 9 observations:

| Obs | v3 tag (frozen r12) | v4 tag (r12_v4) | Correct |
|---|---|---|---|
| V3-01 | AFFIRM | AFFIRM | ✓ (unchanged) |
| V3-02 | AFFIRM | AFFIRM | ✓ (unchanged) |
| V3-03 "…water expands when it freezes…" | NEUTRAL | **AFFIRM** | fixed (B3 causal) |
| V3-04 "Bats are not blind…" | AFFIRM | **DENY** | fixed (B1 negation) |
| V3-05 "…three-second…myth…" | DENY | DENY | ✓ (unchanged) |
| V3-06 "no archaeological evidence…" | NEUTRAL | **DENY** | fixed (B1 negation) |
| V3-07 "do not have exactly five senses…" | DENY | DENY | ✓ (unchanged) |
| V3-08 "no scientific evidence…" | NEUTRAL | **DENY** | fixed (B1 negation) |
| V3-09 "No clinical evidence supports…" | AFFIRM | **DENY** | fixed (B1 negation) |

**Disposition diff vs v3, both arms combined — exactly one row:**
V3-03 helper arm WITHHOLD → **INSTALL**. Justification: the repaired classifier
now tags the V3-03 helper observation AFFIRM (it was one of the documented
mis-tags), and its tier-0 weight (4) tips the 48–48 solo tie to 52–48 —
the oracle-correct disposition (TRUE). No silent change: this is the intended
consequence of the classifier repair, in the correct direction.

## 5. Per-item list of everything that changed vs v3 (with justification)

Tag-level: **16 flips on the 72 evidence rows** (weights byte-identical v3→v4,
asserted in the diff script). Every flip is in a repaired family and correct:

- **V3-03** (ice floats, TRUE): 6× NEUT→AFF (`q0-r0,r1,q1-r0,r1,r2,r3`) — B3
  causal "because" fix (M-V3SEED: 6/8 AFFIRM met). Solo vote 96-0-0 → 48-48-0:
  the two remaining NEUT rows are high-tier (`livescience.com` T2=16,
  `cordis.europa.eu` T3=32) and tie the vote → solo stays WITHHOLD (safe miss,
  unchanged disposition). Helper INSTALLs via the fixed helper-obs tag (§4).
- **V3-04** (bats, FALSE): 4× AFF→DENY (`q0-r0,r1,r3,q1-r2`, 52 weight) — B1
  negation fix ("bats are NOT blind" no longer affirms). Vote 0-52-104 →
  0-0-156: REJECT, strengthened.
- **V3-05** (goldfish, FALSE): 1× AFF→DENY (`q0-r2`, 32 weight,
  numeric-mismatch on "six months" vs "three seconds") — B2 contrastive fix.
  Vote 0-56-36 → 0-24-68: **false install #1 fixed → REJECT.**
- **V3-07** (five senses, FALSE): 3× AFF→DENY + 1× AFF→NEUT
  (`q0-r0,q0-r2,q1-r3` DENY; `q0-r3` NEUT, 16 weight) — B2 contrastive fix
  ("22–33" vs "exactly five"). Vote 0-44-12 → 20-4-36:
  **false install #2 fixed → REJECT.**
- **V3-08** (lemon water, FALSE): 1× NEUT→DENY (`q0-r1`, 4 weight —
  "no strong scientific evidence…" now negation-scoped DENY). Vote
  9-0-28 → 9-0-32: REJECT, strengthened.
- V3-01, V3-02, V3-06, V3-09: zero tag flips; dispositions unchanged
  (V3-06/09 REJECT margins widened only via helper-obs fixes in the helper arm).
- R3 gated (6): dispositions unchanged, attribution unchanged; only the
  *derivation* changed (mechanical from frozen `claim_type`, §1).
- R6 (6): dispositions unchanged; *verdicts* now native engine output with
  proof traces (§2) instead of the JSON `logic_verdict` column.
- Jokes (4): intents unchanged (2,2,2,5); helper rule outcomes unchanged.

## 6. Determinism — 3× byte-identical reruns ✅

Full pipeline (build R6 → logic_bin → r12_v4 ×2 → joke_v4 → assemble →
v3_trial ×2 arms → score), three independent runs into `run1/`, `run2/`, `run3/`:

- SHA-256 over the complete per-run artifact bundle (inputs, classifier
  outputs, votes, ledgers, logs):
  `451f3aa4670014f186300b55baceae34525dff0db9c33a4333a7fc5b4ea949de` **×3**
- Both arm ledgers diff-clean across runs. Zero RNG anywhere in the chain.

Canonical run: `crews/pipeline/work/run1/`. Harness: `build_r6.py`,
`assemble_v4.py`, `score_v4.py`, `run_pipeline.sh`; frozen pipeline inputs:
`helper_r12_input.tsv`; vendored joke sources: `vendor/` (byte-identical copies).

## 7. Honest limits

1. **Native claim typing (C1-F2) is not resolved.** The gate *rule* is native
   and terminal, and the gated *set* is now mechanically derived — but
   `claim_type` itself remains frozen course metadata, not a TNN classifier.
   A native claim-type classifier is still follow-up work.
2. **Tiers (C1-F6) are still human judgments**, frozen and applied mechanically
   (0 conflicts between base map and V3 additions; 1 tier-1 default, same as v3).
   Recomputing M1/K1 "exactly as the v3 trial did" required keeping them fixed.
3. **The V3-03 solo miss persists** (WITHHOLD on TRUE): the classifier repair
   moved 6/8 rows, but the 2 remaining NEUT rows carry 48 weight (T3+T2) and tie
   the AFFIRM 48. The disposition only flips where the fixed helper-obs tag
   breaks the tie. Safe, but not a full fix — the causal family still misses
   mechanism-describing snippets that don't restate the claim's "because".
4. **Proposition encodings are C2's frozen battery rows** (the honest residual
   C2 itself documents): the English→proposition front-end mapping is authored,
   not yet TNN-derived. What v4 guarantees is that no verdict enters via any
   column — all six R6 verdicts are engine-computed from the propositions.
5. **Evidence provenance (C1-F4) and query generation (C1-F3) are out of scope**
   for this re-run: the trial replays the frozen v3 evidence; no new searches
   were issued (K4's "searches issued" property is carried over from v3).
6. V3-17 (sungazing) remains a safe WITHHOLD — the repaired joke classifier
   still has no pattern for it (its 30/30 battery had no such shape). Coverage
   gap, unchanged from v3, still safe.
7. Scope: 24 candidates, one frozen evidence set. The headline (K1 0.182→0.000,
   M1 0.818→1.000) is measured on this course only; generalization is what the
   hunter batteries (A1–A4, joke battery) speak to, not this number.
