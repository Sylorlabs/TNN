# PREREG: Hypothesis D Implementation (MAP-Elites / Novelty Control)

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. Committed before any D implementation.
Authority: implements hypothesis D of `arch_review/ARCHITECTURE_REVIEW.md`
(commit 18be93c3e), evaluated under the frozen battery
`discovery_battery/PREREG_BATTERY.md` (commit 425f7276d).
Battery prereg 425f7276d is a strict ancestor of this commit (verified by
`git merge-base --is-ancestor` before results are accepted).

## D1. Mechanism (frozen)

MAP-Elites quality-diversity search over straight-line programs on the frozen
GENEXEC2 VM (exactly as in 8d5f58b89; the VM code is copied verbatim, no
semantic edits).

- Op universe (31 templates, fixed order): PUSH k for k in -9..9 (19),
  IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP, SWAP, OVER.
  No CALL, no comparisons (LT/EQ/GT), no jumps. Straight-line only.
  This matches the review: "the control has no conditional machinery".
- Archive: one elite program per niche. Niche = (length_bucket, score,
  behavior_hash) where length_bucket = min(prog_len, 12), score = exact
  matches on train episodes, behavior_hash = rolling hash of the discretized
  output sign vector (trit per episode: 0 for negative, 1 for zero, 2 for
  positive; h = (h*3 + trit) mod 256) over the train episodes.
  Max program length 16. Niche count = 13 * (n+1) * 256.
- Retention: a candidate is stored iff its niche is empty (novelty) or its
  score strictly exceeds the niche elite (per-niche elitism). Ties keep the
  incumbent. There is no global score ranking anywhere.
- Initialization: the empty program is evaluated and inserted (eval 1).
- Parent selection: round-robin over occupied niches in order of first
  occupation (fully deterministic).
- Mutation (deterministic cyclic order, per-parent persistent index): for a
  parent of length L, the mutation space in fixed order is
  (1) append each of the 31 templates (skipped when L >= 16),
  (2) replace position p (0..L-1) with template t (31 templates),
  (3) delete position p (0..L-1).
  Each parent stores next_mut_idx; after a parent is selected the indexed
  mutation is generated (invalid ones are skipped without consuming an
  evaluation, index still advances), the candidate is evaluated, and the
  index increments modulo the current space size.
- One candidate evaluation = one candidate program executed on the full
  train episode set.
- Budget per task: 1,000,000 candidate evaluations OR 300 s wall clock,
  whichever first (wall clock via clock_gettime, checked every 1024 evals).
  Design target: 1M evals completes within 300 s so the eval budget binds
  and all outputs are deterministic. A wall-clock timeout is reported as
  TIMEOUT and is void for battery purposes (non-deterministic stop point).
- Termination: SOLVE when a candidate scores n/n on all train episodes;
  otherwise FAIL at budget exhaustion.
- Determinism: the algorithm uses no RNG. 3 runs per task must be
  byte-identical on all committed outputs (wall-clock seconds are reported
  separately and excluded from the identity check).
- Persistent state: the archive (all occupied niches and elites) is carried
  across tasks T0..T5 in fixed order. T6 is sealed and not run here.
- Trace: every niche insertion is logged (eval number, niche, length,
  score, program). The deceptive prefix [IN0, PUSH 2, MUL, PUSH 1] is
  explicitly flagged on insertion, and the solving mutation (parent niche,
  mutation kind, appended op) is logged at SOLVE.

## D2. Frozen predictions (from the review, battery section 5)

- T0 2x+1: SOLVE. The deceptive prefix occupies its own niche and survives
  independent of score; mutation appends ADD.
- T1 abs: FAIL (no conditional machinery in the op alphabet).
- T2 mod3: SOLVE ([IN0, PUSH 3, MOD]).
- T3 parity: SOLVE (straight-line, e.g. via MOD/EQ or MOD/SUB/NEG).
- T4 nested abs: FAIL. T5 fragment composition: FAIL.
- Control validity: D-F1 fires iff D fails T0 (control misconfigured, must
  be fixed before serving as baseline). D-F2 fires iff D solves T4 or T5
  (invalidate and fix; inspect the found program for a task-design flaw or
  leaked machinery).

## D3. Kill bars for this implementation

- K1: D implemented per D1 (MAP-Elites, behavioral niches, deterministic
  mutation order, no global ranking, no CALL/comparison/jump ops).
- K2: T0 through T5 executed under the frozen battery protocol (frozen VM,
  frozen episodes, frozen budget, 12 metrics per task committed with raw
  logs). T4/T5 also rerun from fresh state for the transfer pair.
- K3: control predictions of D2 evaluated as CONFIRMED / UNCONFIRMED /
  control-invalid per battery section 5 (outcome match AND mechanism trace
  for T0; plain outcome for the FAIL predictions; D-F1/D-F2 checked).
- K4: pure Zag (no Python anywhere), no em dashes in committed files
  (byte-grep verified), 3/3 byte-identical runs on the deterministic
  outputs.

## D4. Governance

- This prereg commit contains only this file and strictly precedes the
  implementation commit (`git merge-base --is-ancestor` verified).
- Commits use pathspec (`git commit -- <owned path>`) to avoid sweeping
  concurrent workers. Owned path: `docs/lab/research-lead/overnight-20260928/hyp_d/`.
- No threshold weakening after results. If the control is misconfigured
  (D-F1), it is fixed and re-frozen transparently; results under the old
  design are void.
- Builder reports BUILD-PASS or BUILD-FAIL against K1..K4 above; battery
  confirmation is evaluated separately under the frozen battery.
