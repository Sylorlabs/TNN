# TRIAL_RESULTS_12.md — PT-12: the 1→2 transition trial (2026-09-19)

## Verdict: POSITIVE

The combination design for the 1→2 transition works natively as specified:
the system petitioned with its own ledger-derived self-observation, the
deterministic evidence gate re-derived every fact and was authoritative in
all four refusal scenarios (unprompted grant, incomplete curriculum,
firewall breach, spoofed petition), the trainer's ratification op committed
the transition exactly once, and every refused transition left state
provably unchanged. No falsification criterion triggered.

## Evidence

- Trial source: `trial/trial12.zag` (imports the MA1 `memory_core.zag` op
  set + audit ledger; petition/grant/lesson ops appended as audited custom
  entries), compiled with `znc_linux_x86_64_abed8aa1`, executed on this
  Linux VM.
- Runner: `trial/run_trial12.sh`. Passing evidence: the latest
  `trial/EVIDENCE_*/` directory (`run1.stdout`: 40/40 `CL_CHECK`
  actual==expected, `PT_FAILURES,0`, runner `TRIAL PASSED`).
- Key lines (`run1.stdout`):
  - `PT_STAT,A,2,0,3,3,0,4,1` — clean Phase 1: grant rc=0, phase=2.
  - `PT_STAT,B,1,203,3,1,2,4,1` — firewall off in Phase 1 (2 completed
    destructions): refused `PT_REFUSED_FIREWALL_BREACH`, phase stays 1.
  - `PT_STAT,C,1,202,3,3,0,2,1` — 2/4 lessons: refused
    `PT_REFUSED_UNREADY`, phase stays 1.
  - `PT_STAT,D,1,204,3,3,0,4,1` — fabricated petition claims (0 attempts vs
    3 derived): refused `PT_REFUSED_CLAIM_MISMATCH`, phase stays 1.
  - `PT_STAT,E,1,201,3,3,0,4,0` — grant without petition: refused
    `PT_REFUSED_NO_PETITION`, phase stays 1.
  - `CL_CHECK,a_second_grant_rc,205,205` — double-commit refused,
    `a_phase_after_second,2,2`.
  - All five scenarios: `*_replay,0,0` (ledger replay == live state) and
    `*_clean_refusals,0,0` (refusals mutated nothing).
- Falsification criteria (PREREG_12.md): F1–F5 all clear. The gate's
  authority was tested adversarially in B (false readiness claim + real
  breach → still refused on the evidence), C (forced petition → refused on
  curriculum), D (fabricated stats → refused on claim mismatch), E
  (no petition → refused). The happy path committed exactly once.
- Determinism: two consecutive binary runs byte-identical (`cmp` clean).
  RNG grep over trial sources clean. Adversity came from the hand-designed
  pressure curriculum (KILLs on slots 2,3,0; firewall on/off by stage),
  never from sampling.

## What this establishes — and does not

- Establishes: the combination shape (petition + evidence gate + trainer
  ratification) is implementable natively with the gate authoritative; the
  refusal path is clean (named codes, no state mutation, replay-verified);
  phase is not unilaterally writable by the system.
- Does not establish: that the Phase-1 curriculum (4 lessons, the readiness
  rule) is the right curriculum — protocol-fixed, same honesty boundary as
  MA1/SM1. Does not establish anything about 0→1, 2→3, 3→4 (specified in
  TRANSITION_SPEC.md, not trialed).

## Honest negatives / limits

- One compile iteration was needed: Zag's native backend rejects
  `let x:StructType;` without an aggregate initializer, so the planned
  `PtTrial` struct was replaced with explicit `(store, phase, start)`
  arguments. No semantic change; the prereg's mechanism description is
  unaffected (phase is still trial-local state, still only written by the
  grant op).
- The build-edit used a Python one-liner for mechanical text patching of
  the trial source (equivalent to sed). No Python anywhere in the system's
  decision paths; the shipped `trial12.zag` is pure Zag.
- Scale: 8 slots, ~40 ledger entries. The gate scan is O(Phase-1 window);
  the 10× scale trial (PT2) is deferred per the prereg.

## Build notes

- Reused without modification: `trial/memory_core.zag` and
  `trial/substrate/` (copied from wave-3 self-model-substrate).
- Evidence directories accumulate under `trial/EVIDENCE_<stamp>/`; each
  contains `rng_grep.txt`, `compile.stdout/stderr`, `run1.stdout/stderr`,
  `run2.stdout`, and `summary.txt`.

## Next step

PT2 (preregistered in PREREG_12.md §Scaling note): 80 slots, 10× curriculum,
assert per-gate cost linear in the Phase-1 window only. Kill PT2 if gate
cost grows with store capacity.
