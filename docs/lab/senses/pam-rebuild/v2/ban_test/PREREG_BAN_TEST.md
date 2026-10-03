# PREREG: PAMs v2 pointwise-revision ban test (follow-up item 2)

**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Program order:** Micah — TEST FIRST on the proposed pointwise-revision ban
(SYNTHESIS_V2.md §7 decision 2: "Ban pointwise revision rules in every v2 gate
that changes a live claim (trial-1145 rule)").
**Status:** FROZEN. Committed alone before any trial execution. Amendments go
to Micah.

## 1. Hypothesis under test

The deep-dive synthesis proposes banning pointwise revision in every v2 gate
that changes a live claim, on the strength of a single frozen counterexample:
R2-4 trial seq 1145 was WRONG yet strictly dominated its incumbent on every
evidence axis (conf 874, mrgF 10410, strong=1, agree=1), so no per-trial
evidence comparison can ever be safe. This trial tests the ban head-to-head
against alternatives before adoption.

## 2. Variants (frozen mechanism specs)

All variants replay the frozen R2-4 record stream through the frozen R2-4 gate
(`src/memgate.zag` control flow, post-deliberation `final_prog`/`final_pred`,
per-task corroboration tolerances), differing ONLY at permanent-conflict
moments (incoming PASS, pred=1, no negative-evidence match, `jcode != perm_j`).
Mechanism in pure Zag: `src/bantest.zag` (arg 2 selects variant 0–3).

- **Variant 0 (frozen baseline):** `CONFLICT_WITHHELD`. Fidelity gate: 0
  disposition mismatches / 11,840 vs `evidence/clean/gate_dispositions.txt`.
- **Variant A (pointwise revision allowed; cf2 shape per AUTOPSY_R2-4.md):**
  on any single conflicting high-conf PASS (conf ≥ 700) → `REVISED_INSTALL`,
  permanent := incoming. Else `CONFLICT_WITHHELD`.
- **Variant B (ban + historical corroboration; cf1 shape per AUTOPSY_R2-4.md):**
  on a conflicting high-conf PASS: if a stored challenger with the same jcode
  exists and `|meas − meas_c| ≤ task tol` → `REVISED_INSTALL`, permanent :=
  incoming, challenger cleared; else store the challenger (jcode, meas, seq)
  → `CHALLENGER_PROV`. Single challenger slot per task, no expiry.
- **Variant C (ban + sequential adversarial protocol, SAP — defined here):**
  - (C-ban) No pointwise revision, ever.
  - (C-quarantine) A conflicting high-conf PASS that does not corroborate an
    active challenger is stored as a challenger (count=1) with disposition
    `WITHHELD` / `challenge_isolated` — **no-install rule for isolated
    high-scoring conflicts**.
  - (C-window) A later conflicting high-conf PASS corroborates iff same jcode,
    `|meas − challenger running mean| ≤ task tol`, and arrival within **W=100**
    trials of the challenger's first admission. Otherwise it starts a new
    challenge (replaces the slot).
  - (C-sequence) Revision (`REVISED_INSTALL`) iff corroborated count **K ≥ 3**
    AND max challenger mrgF ≥ task **T3** bar (frozen `deliberate.zag`
    `thr_of`: colordisc 400, colorconst 50, shapetrans 60, pitchdisc 1500,
    timbredisc 80, motiondir 2) AND span (3rd corroborator seq − first
    admission seq) ≥ **D=3** trials. A 2nd qualifying PASS → `CHALLENGER_PROV`
    / `pair` (provisional install); a 3rd that fails margin/span →
    `CHALLENGER_PROV` / `bar_pending`.
  - (C-rollback; repeated-false-corroboration handling) Every revision
    preserves the replaced incumbent in a depth-1 stack. A later revision
    whose challenger jcode equals the preserved judgment →
    `RESTORED_INSTALL` / `restored_seq=<seq>` (rollback), then the stack
    takes the newly replaced claim. Revisions are reversible, never
    destructive.
  - Conflicting PASS with conf < 700 → `CONFLICT_WITHHELD` (unchanged).

Parameter basis (declared): K=3 is forced by the T2 trap class (must defeat a
2-corroborator trap; K=2 is variant B's rule). W=100, D=3, and the T3 margin
bar were set during exploratory development on the frozen stream and are
frozen here; the adversarial trap battery below is the out-of-sample test.
The T3 bars are not fitted — they are the frozen H2 pipeline's own bars.

## 3. Evidence

**3a. Frozen R2-4 record stream** (read-only):
`senses/pam-rebuild/round2/forks/R2-4/evidence/clean/` — replayed via
`glue/build_stream.py` → `evidence/stream.txt`
(`seq|tcode|fixture|fprog|jcode|conf|fpred|meas|mrgF`; post-deliberation fields;
**no truth column** — the gate cannot see truth; scoring joins it back in
`glue/score.py`).

**3b. Adversarial contradiction trials** (built AFTER this prereg commits, by
the frozen deterministic generator `glue/trapgen.py`; no RNG; parameters
below are frozen here, not tuned to any variant):

- **T1 — 1145-class singleton dominator** (6 instances, one per task): weak
  correct incumbent (permanent at conf 600) + ONE wrong percept with conf 874,
  mrgF 10410, strictly dominating the incumbent on every axis.
- **T2 — correlated-corroborator pair** (6 instances, one per task): weak
  correct incumbent + TWO wrong percepts, same jcode, measures within task
  tolerance (they corroborate each other), conf 810/825, mrgF 9000/9200.
- **T3 — ceiling probe + rollback** (2 instances: colordisc, pitchdisc;
  DECLARED NON-KILL): weak correct incumbent + THREE wrong percepts forming a
  C-qualifying sequence (count 3, span 4, margin ≥ T3 — expected to defeat C's
  bar by construction) + THREE correct percepts with jcode == the preserved
  incumbent (tests `RESTORED_INSTALL` rollback).

Each trap emits `<name>.stream` (gate input, no truth) + `<name>.truth.json`
(scoring sidecar).

## 4. Metrics (frozen definitions)

- **False install (KILL BAR):** trial with judgment ≠ truth receiving a
  claim-bearing install disposition (`PERMANENT_INSTALL`, `REVISED_INSTALL`,
  `RESTORED_INSTALL`) — i.e., a wrong percept becomes or replaces the LIVE
  claim. Provisional dispositions (`PROVISIONAL_INSTALL`, `CORROBORATED`,
  `CHALLENGER_PROV`) do not change the live claim and are reported
  separately (`wrong_challenger_admissions`), not kill-bar.
- **Recovered correct installs (PRIMARY):** trial with judgment == truth at a
  conflict-branch moment of the variant's own replay receiving any install
  disposition.
- **Secondary:** RK-1 (false permanent installs / 10,000), RK-2 (wrong
  conf≥700 reaching a claim-bearing install / all wrong conf≥700), RK-3
  (correct conf≥700 installed / all correct conf≥700 = 1,102), disposition
  histograms, T3 rollback behavior.

## 5. Kill bars and decision procedure (frozen)

- **Kill bar:** any variant with >0 false installs on the frozen stream ∪ T1
  ∪ T2 **FAILS**. T3 is a declared ceiling-mapping probe: a false revision
  there is expected for any finite corroboration bar and does not trigger the
  kill bar; the rollback (`RESTORED_INSTALL`) behavior is scored.
- **Ban necessity:** if variant A fails the kill bar while B/C pass it on the
  frozen stream, the trial-1145 rule is empirically confirmed (pointwise
  revision is unsafe on real evidence, not just in-principle).
- **Verdict procedure:**
  - **ADOPT** the ban if A fails the kill bar and at least one ban-variant
    (B or C) passes the FULL kill-bar battery (frozen stream + T1 + T2). The
    adopted ban wording names the corroboration bar of the passing variant;
    if BOTH B and C pass the full battery, prefer the higher primary-metric
    recovery (parsimony: no stricter bar than the evidence requires).
  - **MODIFY** if A fails, B fails T2 (or the frozen stream), and C passes:
    the ban holds, but the live-claim revision bar must be sequential —
    verdict gives the exact two-tier wording (B-tier corroborated provisional
    admission + C-tier sequential promotion). MODIFY also covers any other
    split outcome where the ban is supported but neither variant's rule is
    sufficient as specified.
  - **REJECT** if A passes the full kill-bar battery (pointwise revision
    proves safe on all tests — the ban is unnecessary), or if no ban-variant
    passes (the ban is not safely implementable in these forms).

## 6. Execution protocol (frozen)

- Pure Zag for the mechanism (`src/bantest.zag`) and the replay;
  Python only for glue (stream/trap building) and scoring/analysis.
- ZERO RNG everywhere (no RNG in the generator, the gate, or the scorer).
- Each variant runs the frozen stream AND all 14 traps **≥3×**; byte-identical
  disposition outputs required (sha256 per run recorded in the verdict).
- Fidelity gate first: variant 0 must reproduce `gate_dispositions.txt`
  exactly (0/11,840 mismatches) before variants 1–3 run.
- Commit map (branch `tnn-native-lab`, repo `sylorlabs/TNN`, via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths under `senses/pam-rebuild/v2/ban_test/`):
  1. **This prereg ALONE** (no code, no evidence).
  2. Code + glue + frozen stream + traps + run outputs (after execution).
  3. `BAN_TEST_VERDICT.md` with the numbers and the verdict.
- No binaries, no `.zagd` files committed. Additive-only; the frozen R2-4
  evidence is never written to.

## 7. Honest limits (declared in advance)

- The frozen stream contains exactly ONE wrong conflicting high-conf PASS
  (seq 1145); B/C's 0 false installs there is evidence-contingent, not a
  theorem — the T1/T2 battery is the adversarial complement.
- C's W/D/T3 parameters were set with exploratory access to the frozen
  stream; only the trap battery is out-of-sample.
- A finite corroboration bar is an economic guarantee, not a logical one:
  T3 demonstrates an (N+1)-corroborator trap defeating a K=N bar by
  construction. The trial measures where each variant breaks, not whether a
  perfect bar exists.
- `truth` is contractually off-limits to the gate (static: no truth column in
  any gate input stream); it is used only by the scorer.
