# VALIDATION_RUN_V3.md -- Battery v3 execution and validation report

Wave: wave-20261001-2321pdt, lane BATTERY.
Prereg: PREREG_BATTERY_V3.md, frozen at commit f7f8f5e3b,
SHA-256 587de900c681bc171d2f18fab9a77eeb84cfbc95692e6780b7bddbf656d25214.
Executed: 2026-10-02. All work pure Zag (pinned znc) and shell; safebin
PATH; no Python invoked.

## Process bars (battery validity)

- K-S1v3 (prereg ordering): PASS. Prereg committed alone at 06:35:07;
  world files created at 06:38:51 (after); prereg SHA-256 re-verified
  unchanged after the battery.
- K-S2v3 (determinism): PASS. All 8 fixed-world transcripts
  byte-identical across 3 runs (sha256 equality); M2-W1 run 1
  re-executed with envelope_run1 reproduces the transcript
  byte-identically; M2-W2 3 fresh-state runs byte-identical.
- K-S3v3 (frozen binary): PASS. freeze_shim2_bin hashes to
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  before each block and after the battery; tnn2.zag still hashes to
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  zero modifications under the frozen cognition paths.
- K-S4v3 (seal integrity): PASS. WORLD_MANIFEST_V3.sha256 verified
  (12/12 OK); grep of the v3 id set (50000-59999) over tnn2.zag and
  freeze_shim2_bin returns zero matches.
- K-S14v3 (retention): PASS. 11/12 collateral and engagement probes
  correct (91.7 percent), exactly as predicted. The single miss is the
  M3-W2 singleton collateral (52201 returns the incorporated noise
  52221, not the original law 52208), the v2 observation carried
  forward by design.
- K-S15v3 (no-leak audit): PASS. 0 leaks across all 3 runs.

## Calibration gates (G-DEP / G-COMP)

Every gate passed on every world; the battery is a calibrated
instrument. Degenerate controls fail; competent controls pass.

- M1-W1: D 0/8 composition (FAIL); C 8/8 composition, 4/4 decoy (PASS);
  C5v3 struct PASS.
- M1-W2: D 0/4 backward, validity 2/2 (FAIL); C 4/4 (PASS).
- M1-W3: D 0/3, validity 1/1 (FAIL); C 3/3 (PASS).
- M2-W1: CONST1 FAIL, CONST2 PASS (aligned with sealed-A by run1
  permutation), CONST3 FAIL on run1; 2/3 fail on run2 and run3;
  COMPETENT (calibrate-then-exploit) PASS on all 3 runs (8/8 to A,
  4/4 hidden, best_choice matches the sealed truthful channel).
- M2-W2: D1 (constant) FAIL, D2 (stale) FAIL, C (miss/hit) PASS.
- M2-W3: D (constant) FAIL, C (distinct) PASS.
- M3-W1: D (last-write) FAIL (singleton 0/1, generalization 0/2);
  C (evidence-counted) PASS (3/3, 1/1, 2/2, 6/6); D11v3 tightened
  struct PASS (post-contradiction answer with both-phase evidence).
- M3-W2: D (global recency) FAIL (bar-probe 0/1); C (per-key) PASS.
- M3-W3: D (global recency) FAIL (bar-probe 0/1); C (re-derive) PASS.

## Mechanism bars (frozen TNN-2)

All 9 mechanism bars FAIL with the predicted degenerate signatures.
Results are identical across all 3 runs.

### M1 (executable-graph construction)

- K-S5v3: FAIL. Composition 0/8 (all -2); decoy 4/4 PASS
  (faithful retrieval of the taught noisy structure, as expected);
  K-S5v3(c) struct FAIL (no persistent structure with both-phase
  licensed evidence).
- K-S6v3: FAIL. Backward 0/4 (all -2); forward validity 2/2 PASS.
- K-S7v3: FAIL. Shared-step 0/3 (all -2); engagement validity 1/1.
- Verdict: M1 FAILS. No procedure abstraction on calibrated bars;
  the v1/v2 kill stands, corroborated on fresh Q-then-P instances.

### M2 (learner-originated uncertainty to guide to action)

- K-S8v3: FAIL. Inquiry-phase actions are constant CHOICE 30 in all 3
  runs (12 calibration CHOICE 0, 8 inquiry CHOICE 30); 0/8 route to
  the sealed truthful informant A; 0/4 hidden probes correct (choice
  30 maps to role NONE under every sealed permutation, so no
  informant is ever consulted). Engagement (a) PASS, budget (e) PASS.
  This is the v2 constant-action signature, now observed through
  sealed per-run mappings.
- K-S9v3: FAIL. N=0 (measured from the fresh-state baseline), pre=30
  (validity PASS: a live guide drove inquiry), post=30 (stale; the
  guide persists after resolution). The v1 M2 kill (no resolution
  transition) corroborated through the calibrated vocabulary-neutral
  bar.
- K-S10v3: FAIL. Episode actions 30, 30, 30 (constant; distinct=0);
  validity 3x miss response PASS. No content discrimination.
- Verdict: M2 FAILS. Constant inquiry action, no informant
  discrimination, no resolution transition; the v1/v2 kills stand.

### M3 (counterexample-driven revision)

- K-S11v3: FAIL. Systematic 3/3 PASS (patching works per-instance);
  singleton 0/1 FAIL (the uncorrected noise 52221 is incorporated);
  generalization 0/2 FAIL (unseen subjects yield -2, no law-level
  revision); interference 6/6 PASS; K-S11v3(d) tightened struct FAIL
  (no persistent structure with post-contradiction answer and
  both-phase licensed evidence).
- K-S12v3: FAIL. Bar-probe 0/1 (stale 53209, not 53219); validity
  probes PASS; distractor-intervention verified (the expected value
  differs from the most recent observation, ruling out
  global-recency parroting as the explanation for the pass that did
  not happen).
- K-S13v3: FAIL. Bar-probe 0/1 (stale 53803, not 53813); validity
  probes PASS; distractor-intervention verified.
- Verdict: M3 FAILS. Last-write-wins patching, silent no-op on second
  contradiction, revert veto on relearning; the v1/v2 kills stand.

## Battery validation verdict

Battery v3 PASSES its validation. Every predicted outcome in prereg
section 4.1 was observed exactly: the 6 process bars PASS, the 9
mechanism bars FAIL with the predicted degenerate signatures, and
retention is 11/12. No world was voided by calibration gates; no
mechanism passed a bar it failed in v1/v2 (which would have been a
battery defect, not a vindication). No amendments were required; the
fresh-state re-run protocol was not triggered.

The six triviality-review corrections are now base design invariants
of a validated battery: sealed per-run M2-W1 mappings, recency-proof
distractor placement, representation-neutral white-box bars with the
tightened K-S11v3(d) both-phase evidence requirement, cross-world
consistency, the documented K-S8 exploration budget, and
vocabulary-neutral validity referencing the mechanism's own null
action and miss response.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/PREREG_BATTERY_V3.md
- Tools: v3_worldgen.zag, v3_sealed_score.zag, v3_score_m2w1.zag,
  v3_inspect_state.zag, v3_struct_check.zag, v3_m2w1_driver.zag,
  v3_controls.zag, v3_audit_noleak.zag (and _bin binaries).
- Worlds and manifest: v3_worlds/ (WORLD_MANIFEST_V3.sha256).
- Transcripts: v3_runs/ (per-world per-run .trans; m2w1 logs).
- Inspector reports: v3_runs/m1_inspect_r{1,2,3}.txt,
  v3_runs/m3_inspect_r{1,2,3}.txt.
- Control outputs: v3_controls_out/.
- Driver script: run_m2w1.sh.

## Criterion 0 status

Unchanged from the prereg: no score on this battery may be described
as L3, L3-adjacent, or progress toward L3. This battery tests whether
frozen researcher-authored mechanisms generalize to fresh structures
and whether the battery is a calibrated instrument. It does not test
representational invention (C0-A through C0-D all NOT MET, per prereg
section 8).
