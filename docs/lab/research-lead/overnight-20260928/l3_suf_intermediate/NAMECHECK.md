# L3-SUF-INTERMEDIATE NAMECHECK

Lane: `docs/lab/research-lead/overnight-20260928/l3_suf_intermediate/`
Branch: `tnn-native-lab` (local only, never pushed)
Worker: L3-SUF-INTERMEDIATE (subagent, 2026-10-03)
Task: non-ledger (claim minting paused). Design-only worker: produce the
L3-SUF-1 design and frozen prereg. No implementation in this task.

## Provenance

- Prior line: L3-INR sealed L3-KILLED (C409, reclassified L2+);
  L3-RX K10 = KILL (three confident-wrong COMMITs, RK-A/B/C).
  Both kills terminal, not revisited.
- This lane's hypothesis: the shared root cause is ungraded epistemics;
  the next L3 intermediate is the learner-invented resolution record
  (explicit unresolvedness). See L3_SUF_DESIGN.md.
- Task description staleness noted: the assignment said "sealed
  evaluation pending" for L3-INR; both sealed evaluations have completed
  (kills above). This lane builds on the completed evaluations.

## Step 0 — Toolchain guard (design worker; no implementation)

- No implementation, binary, or run log is produced by this worker, so
  no toolchain activation was required for research computation.
- The follow-up BUILDER worker MUST, before writing any lane source:
  (1) run `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  and `export PATH="$HOME/safebin"`; (2) verify `command -v python3 python`
  returns nothing under the safebin PATH; (3) record the verification in
  its own NAMECHECK Step 0; (4) implement learner, worlds, harness, and
  scorer in pure Zag compiled only by the pinned safebin znc, honoring
  the pinned-znc workarounds in AGENTS.md.
- If a forbidden interpreter is invoked in any lane of L3-SUF-1, that
  wave is PROCESS-FAIL per the governance ruling; results stay
  exploratory until a clean safebin reproduction.
- C453 (L3-RX) artifacts are NOT inherited as canonical (builder
  disclosed 2 python3 invocations; PROCESS-FAIL ruling pending). The
  L_old baseline is re-derived cleanly under this prereg.

## Freeze record

- L3_SUF_DESIGN.md committed first (design rationale, falsification
  framework). Commit: (recorded at freeze time).
- PREREG.md + NAMECHECK.md frozen in a commit containing ONLY these two
  files, added with explicit pathspecs. No .zag, no binary, no log
  exists under this lane at freeze time. The prereg is never edited
  after freezing; any change requires a new prereg.

## Worker separation (frozen)

Designer (this worker), builder, adversary, red-team: four distinct
instances, blind except through the authorized evaluator (digests only).
The builder has seen no sealed content; the adversary designs post-freeze.

## Constraints honored by this worker

- Pure documentation: no research computation performed, no interpreter
  invoked for research logic.
- Commits local, never push, explicit pathspecs.
- No ledger entries (non-ledger task).
