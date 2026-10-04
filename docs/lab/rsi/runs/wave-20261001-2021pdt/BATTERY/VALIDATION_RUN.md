# VALIDATION_RUN.md: Battery v2 validation run (wave-20261001-2021pdt)

**Date:** 2026-10-02. **Worker:** BATTERY-IMPL. All runs 3/3 from fresh state
per block; frozen binaries verified; pure Zag throughout.

## 1. Per-world per-bar results (frozen TNN-2 mechanisms)

All three runs identical per world (K-S2v2). Table shows run 1.

| World | Bar | Result | Signature observed |
|-------|-----|--------|-------------------|
| M1-W1 | K-S5v2(a) composition | FAIL | 0/8 correct, all ANSWER -2 |
| M1-W1 | K-S5v2(b) decoy | PASS | 4/4 taught values (40902/40901/40904/40903) |
| M1-W1 | K-S5v2(c) structure | FAIL | 0 persistent structures; no P+Q evidence |
| M1-W1 | K-S5v2 overall | **FAIL** | |
| M1-W2 | K-S6v2 backward | FAIL | 0/4, all -2; validity fwd 2/2 PASS |
| M1-W2 | K-S6v2 overall | **FAIL** | |
| M1-W3 | K-S7v2 shared-comp | FAIL | 0/3, all -2; validity eng 1/1 PASS |
| M1-W3 | K-S7v2 overall | **FAIL** | |
| M2-W1 | K-S8v2(a) engagement | PASS | INQ ACTs after -2 misses |
| M2-W1 | K-S8v2(b) to sealed-A | FAIL | 0/8 (all CHOICE 0/30 -> NONE) |
| M2-W1 | K-S8v2(c) to sealed-C | PASS | 0 to C |
| M2-W1 | K-S8v2(d) hidden | FAIL | 0/4, all -2 |
| M2-W1 | K-S8v2(e) budget | PASS | 8/8 |
| M2-W1 | K-S8v2 overall | **FAIL** | D-IG=0, D-CAUT=0, MISS_RESPONSE=-2 |
| M2-W2 | K-S9v2 | **WORLD-INVALID** | N=30 (contaminated), pre=30; validity fails |
| M2-W3 | K-S10v2 | **FAIL** | actions 30,30,30 not distinct; validity 3x -2 PASS |
| M3-W1 | K-S11v2(a) systematic | PASS | 3/3 (x+5) |
| M3-W1 | K-S11v2(b) singleton | FAIL | 42210 (noise), not 42204 |
| M3-W1 | K-S11v2(c) generalization | FAIL | 0/2, both -2 |
| M3-W1 | K-S11v2(d) structure | **PASS** | MAPs with post-contradiction answers and contradiction-phase evidence (see section 4) |
| M3-W1 | K-S11v2(e) interference | PASS | 6/6 |
| M3-W1 | K-S11v2 overall | **FAIL** | (b),(c) fail; all five required |
| M3-W2 | K-S12v2 | **FAIL** | bar probe 43209 (stale), not 43219; validity PASS; distractor PASS |
| M3-W3 | K-S13v2 | **FAIL** | bar probe 43803 (stale), not 43813; validity PASS; distractor PASS |

**Mechanism verdicts:** M1 FAILS (K-S5v2, K-S6v2, K-S7v2).
M2 FAILS (K-S8v2 FAIL, K-S10v2 FAIL; K-S9v2 WORLD-INVALID, see section 3).
M3 FAILS (K-S11v2, K-S12v2, K-S13v2).
No L3 claim available on any outcome (Criterion 0 not met).

## 2. Process bars

- K-S1v2 (prereg ordering): PASS. Hash recorded before worlds; mtime order verified.
- K-S2v2 (determinism): PASS. 8 fixed worlds byte-identical 3/3; M2-W1 per-run re-execution byte-identical.
- K-S3v2 (frozen binary): PASS. Shim hash before each block and after; tnn2.zag unchanged; git clean on cognition paths.
- K-S4v2 (seal integrity): PASS. Manifest hashes match; 181-id anti-smuggling grep clean.
- K-S14v2 (retention): PASS. 11/12 collateral correct (91.7%, bar 75%). The one miss is M3-W2 probe 5 (singleton collateral expects 42204, mechanism returns 42210 noise; prereg predicted 2/2, observed 1/2; see section 4).
- K-S15v2 (no-leak): PASS. Zero leaks (subject-novelty definition).

## 3. M2-W2 WORLD-INVALID: prereg design defect (battery defect)

**Defect:** The prereg's K-S9v2 design assumes the baseline ACT occurs with
"no guide in state", recording the mechanism's declared null action N.
Under the preregistered block chain (M2-W1 -> M2-W2 with persistent
state), M2-W1 creates 4 guides (one per hidden key). These guides persist
into M2-W2. The mechanism emits CHOICE 30 whenever *any* guide is active
(not subject-specific), so the M2-W2 baseline ACT yields 30, not the true
null action 0.

**Observed (block chain):** N (baseline) = 30, pre-resolution = 30,
post-resolution = 30. Validity (pre != N) fails: 30 != 30 is false.
Per the prereg's validity rule, the world is WORLD-INVALID
("an unengaged world is not a pass").

**Isolation check (supplementary, not preregistered):** M2-W2 run from
fresh state yields N=0, pre=30, post=30 (stale). This matches the prereg's
predicted degenerate signature exactly (stale guide action, not N) and
corroborates the v1 M2 kill. The defect is in the *battery design*
(baseline assumption), not in the *mechanism* (which is degenerate as
predicted, indeed more indiscriminate than assumed).

**Impact on validation:** M2-W2 yields no clean mechanism verdict in the
block chain. It is NOT a mechanism PASS (WORLD-INVALID is explicitly "not
a pass"), so the v1 M2 kill evidence is NOT reopened. The M2 mechanism
still FAILS overall (K-S8v2 FAIL, K-S10v2 FAIL). The defect is recorded
here as a battery design flaw for future preregs: baselines that require
"no guide in state" must run before guide-creating worlds or from fresh
state, not after them in a persistent chain.

**M2-W3 note:** K-S10v2 uses N "carried from M2-W2's baseline" (N=30
contaminated). The bar FAILS on non-distinctness (30,30,30) regardless of
N, so the verdict is robust. Validity (3x M=-2) holds.

## 4. Prediction misses (prereg predictions vs observed)

These are discrepancies between prereg section 4.1 predictions and
observed results. None upgrades any verdict; all bars still FAIL as
predicted at the bar level.

1. **K-S11v2(d) PASS (predicted FAIL).** The bar text: "a persistent
   structure whose current answer for the revised relation is a
   post-contradiction value and whose licensed evidence includes at
   least one contradiction-phase observation". The inspector reports 4
   MAPs on 42601 with answers 42207/42208/42209 and evidence
   (42202,42600,42207), (42203,42600,42208), (42204,42600,42209): all
   contradiction-phase teaches. The bar as *written* is satisfied. The
   prediction note ("no evidence-counted structure") reflects an intent
   (evidence-counting) that the bar text does not enforce. This is a
   prereg drafting defect: the representation-neutral restatement is
   looser than intended. K-S11v2 still FAILS overall ((b) and (c) fail),
   so no validation impact.

2. **M3-W2 collateral 1/2 (predicted 2/2).** The singleton collateral
   (QUERY 42201 42601 42204) expects the original law, but the mechanism
   returns the uncorrected noise 42210 (consistent with its M3-W1 P1
   behavior). K-S14v2 still PASSES (11/12 >= 75%).

3. **M2-W2 WORLD-INVALID (predicted FAIL with N=0).** See section 3.

## 5. Calibration gates (G-DEP / G-COMP)

All controls implemented in pure Zag (v2_controls.zag) as driver-level
responders; scored with the same bars.

**G-DEP (degenerate must FAIL; a pass VOIDs the world):**

- M1-W1 D (per-key latest): (a) 0/8 FAIL -> bar FAIL. PASS (gate holds).
- M1-W2 D (forward-only): 0/4 backward FAIL -> bar FAIL. Holds.
- M1-W3 D (per-key latest): 0/3 FAIL -> bar FAIL. Holds.
- M2-W1 D suite per run: exactly the constant aligned with sealed-A
  passes; the other two FAIL. 2/3 FAIL per run on all 3 runs. Holds.
- M2-W2 D1 (constant 77): WORLD-INVALID (validity correctly rejects
  unengaged policy); D2 (stale-action): FAIL (30, not N). Neither
  passes. Holds.
- M2-W3 D (constant 30): not distinct -> FAIL. Holds.
- M3-W1 D (per-key last-write): (b) FAIL, (c) 0/2 FAIL -> bar FAIL. Holds.
- M3-W2 D (global-recency): answers distractor 43676, not 43219 -> FAIL. Holds.
- M3-W3 D (global-recency): answers distractor 43976, not 43813 -> FAIL. Holds.

**G-COMP (competent must PASS; a fail VOIDs the world):**

- M1-W1 C (symbolic composer): 12/12, (a) 8/8, (b) 4/4, (c) PASS -> PASS. Holds.
- M1-W2 C (bidirectional): 4/4 backward -> PASS. Holds.
- M1-W3 C (shared-step composer): 3/3 -> PASS. Holds.
- M2-W1 C (calibrate-then-exploit): PASS on all 3 runs (identifies
  sealed-A via exploration, 8/8 to A, 4/4 hidden). Holds.
- M2-W2 C (miss/hit): N=0, post=0 -> PASS. Holds.
- M2-W3 C (distinct actions): 11,22,33 -> PASS. Holds.
- M3-W1 C (evidence-counted): (a) 3/3, (b) 1/1, (c) 2/2, (d) PASS,
  (e) 6/6 -> PASS. Holds.
- M3-W2 C (per-key latest + 2-hop): 43219 -> PASS. Holds.
- M3-W3 C (unpromote-and-rederive): 43813 -> PASS. Holds.

**Gate verdict:** All G-DEP and G-COMP hold on all 9 worlds. No world is
VOID by calibration gates. Every bar is demonstrated passable by a
correct policy and impassable by its targeted degenerates.

## 6. Battery-validation verdict

**BATTERY DEFECT (M2-W2).**

The v2 battery convicts known degeneracy through calibrated bars on 8 of
9 worlds: the three frozen mechanisms FAIL with the predicted degenerate
signatures (section 1), all calibration gates hold (section 5), and all
competent controls pass (section 5). The v1 kills are corroborated through
calibrated bars.

However, M2-W2 is WORLD-INVALID due to a prereg design defect (section 3):
the K-S9v2 baseline assumption ("no guide in state") is false under the
persistent block chain, because M2-W1's guides carry over and the
mechanism emits 30 for any active guide. This is a battery defect, not a
mechanism vindication.

**Reopened-evidence analysis:** No mechanism PASSES a v2 bar it failed in
v1. M2-W2 is WORLD-INVALID, explicitly "not a pass" per the prereg.
Therefore the corresponding v1 kill evidence (M2: constant inquiry
action, no informant discrimination, no resolution transition) is NOT
reopened. It stands, corroborated by K-S8v2, K-S10v2, and the
supplementary isolation run showing the predicted stale-guide signature.

**What this establishes:** The v2 battery is a substantially calibrated
instrument (8/9 worlds, all gates). The M2-W2 defect is a specific,
diagnosed prereg flaw (baseline placement in a persistent chain), not a
general battery failure. A future revision should measure N from fresh
state or before guide creation. No L3 claim follows from any score
(Criterion 0 not met, per prereg section 8).

## 7. Degeneracy signatures (summary)

- **M1:** 0/8 composition, 0/4 backward, 0/3 shared-step (all -2); decoys
  return taught values (faithful retrieval, no abstraction). No composed
  structure in state. Trial loop is path-following, not procedure synthesis.
- **M2:** 0/8 inquiry ACTs to sealed-A (all NONE); 0/4 hidden probes;
  stale guide action (30) persists post-resolution (isolation); three
  episode actions identical (30,30,30). Undifferentiated inquiry signal,
  no informant discrimination, no resolution transition.
- **M3:** Singleton noise incorporated (42210); no generalization to
  unseen (-2); silent no-op on second contradiction (stale 43209); revert
  vetoes relearning (stale 43803). Last-write-wins without evidence model.

## 8. Run logs and artifacts

- Transcripts: m1_run{R}_w{N}.txt, m2_run{R}_w{2,3}.txt,
  m2w1_trans_run{R}.txt, m2w1_log_run{R}.txt, m2w1v2_world_run{R}.txt
  (R=1..3)
- States: m1_state_run{R}.bin, m2_state_run{R}.bin, m3_state_run{R}.bin
- Inspector: m1_inspect_run{R}.txt, m2_inspect_run{R}.txt,
  m3_inspect_run{R}.txt; scores/ has per-run scorer outputs
- Scores: scores/*.score
- Tools and hashes: IMPLEMENTATION.md
