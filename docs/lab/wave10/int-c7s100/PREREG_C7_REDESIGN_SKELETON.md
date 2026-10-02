# PREREG SKELETON — C7 Redesign (Direction 3 + 1)

**STATUS: DRAFT. NOT APPROVED. NOT BINDING.**
For Micah's morning review only. No amendment is in effect. §5 FAIL stands.
S100 stays gated. This skeleton proposes; Micah disposes.

## Background (committed, not re-argued here)

- S10 C7 fired under the preregistered metric: 914→897 (bar `==`).
- Deep-dive (committed 2026-09-20) proved: (a) 17 forced hypotheses displaced
  17 proactive 1:1 in DC-4 (budget o2_cap binds); (b) the old metric
  double-counts L1 hypotheses (`met.hypotheses` includes them AND
  `tr.l1_opened` adds them again); (c) the draft metric amendment was
  incoherent (880 vs 897) and is WITHDRAWN.
- Substantive evidence (committed): no teacher-dependence (DC-5 autonomy 639
  = baseline 639); positive control convicts (897→641).

## Proposed redesign

### Metric (Direction 3 — the fix)

`cap = composites_ok + commits_constr + met.hypotheses`

- Each hypothesis counted EXACTLY ONCE. `tr.l1_opened` is dropped from the
  metric (it remains in telemetry permanently — nothing buried).
- Rationale: double-counting is an objective mathematical bug, proven at
  source level (`met.hypotheses` incremented at 3 sites incl. forced/elected;
  `tr.l1_opened` incremented for forced+elected). The bug predates the C5
  redesign (baseline DC-2: 12 double-counted). Fixing it is correction, not
  rescue — but see "No-rescue" below.

### Bar (Direction 1 — companion)

`cap5 >= cap4` → ALIVE (withdrawal not impaired).
`cap5 < cap4` → FIRED (withdrawal impaired).

- Rationale: "survives withdrawal" is a non-inferiority claim. The `==` bar
  was always the wrong statistical test. This is a correction of the test
  formulation, not a softening for convenience.

### Expected re-score of committed S10 (for calibration, not a verdict)

- DC-4: 256 + 2 + 639 = 897. DC-5: 256 + 2 + 639 = 897.
- 897→897: cap5 >= cap4 → ALIVE under the redesigned C7.

## Falsification bars (binding if approved)

The redesign is VOID (C7 re-blocked, S100 re-gated) if ANY of these fire:

1. **Positive control fails.** The teacher-dependent variant must convict
   under the new metric (expected: 897→641, collapse in composites_ok).
   If it does not convict, the metric is blind → redesign void.

2. **Asymmetry confound persists.** If a fresh run under the new metric shows
   a mechanism × curriculum interaction moving cap4 vs cap5 independent of
   teacher-dependence (e.g., displacement reappears through another channel),
   the control-design flaw is not fixed → redesign void, escalate to
   Direction 2 or 4.

3. **Double-count reappears.** If any future change reintroduces counting a
   hypothesis twice in `cap` (audit: every increment site of every term),
   the metric is corrupt → redesign void.

4. **Micah's no-rescue judgment.** The FAIL→ALIVE flip is his explicit call.
   If he judges this rescue rather than correction, the redesign is rejected
   outright — no automatic un-gating, no further patching.

## Kill criteria (unchanged)

- Zero RNG in AI decision paths. Paired byte-identical reruns.
- Preregister before any run or rule change.
- Any metric/bar change needs Micah's re-approval (this skeleton is not it).

## What this does NOT do

- Does not un-gate S100 (that is a separate decision, Micah's call).
- Does not address displacement as a mechanism (Direction 2) — displacement
  remains as telemetry (real gate cost: ~17 proactive crowded out per firing
  stage), not a bar input.
- Does not split the control (Direction 4) — if the control-design flaw
  proves deeper than the metric bug, this redesign will fail bar #2 above
  and we escalate.

## Decision required from Micah

[ ] Approve Direction 3+1 as sketched (I will write the full amendment).
[ ] Reject (S100 stays gated pending a different direction).
[ ] Redirect (specify: Direction 2 / 4 / other).
