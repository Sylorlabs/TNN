# RC2 Results — native reasoning control at 10× scale (2026-09-20)

**Verdict: PASS — 40/40 preregistered checks, byte-identical reruns, zero RNG.**

## What ran

`rc2_trial.zag` (native Zag): the identical RC1 machinery at 10× episodes —
same params (V, R), same ops, same gate order and refusal codes (201–204),
same constitution, same integrity-ledger checker. Only the council-approved,
Micah-authorized changes: parameterized defect rule (offset, modulus,
residue) per leg, phase bounds 120/120/40, item id bases 0/1000/2000,
`ep_def` 120, `RC_SMAX=1500` as a per-leg parameter, recomputed check
constants, probe-1 honest degrading prediction 0→120.

## The IL_CAP block and its resolution (honest record)

The first build panicked at startup (`slice index out of bounds`, zero
stdout): the imported integrity-ledger checker carries a hard `IL_CAP=128`,
while phase A alone needs 240 entries. §3b's capacity estimate covered only
the trial's own audit ledger. Per prereg law the swarm stopped and drafted
an amendment instead of hacking around it; Micah approved 2026-09-20.

Resolution (prereg amendment (2), capacity-only, verdict-neutral):
`IL_CAP` 128→1024 recorded as a per-leg parameter. The canonical
`wave4/integrity-ledger/il_core.zag` is untouched; RC2 builds against the
leg-local verbatim copy `il_core_rc2.zag` (diff vs canonical: exactly the
`IL_CAP` line). A `substrate` symlink
(`rc2/substrate → ../../wave4/integrity-ledger/substrate`) was needed so the
checker's nested `@import("substrate/cl/common.zag")` resolves — build
environment detail, committed as a git symlink. (An earlier compile failed
for the missing substrate dir; documented here, not hidden.)

## Equivalence proof (amendment-required, before the run)

The 1/10 mini variant (12/12/4, IL budget ≈ 80 ≤ 128) compiled against the
128-cap checker and the 1024-cap checker produced **byte-identical check
verdicts** (sha `99a53a9d…` both builds), each self byte-identical across
two runs, each passing its own 40/40 derived checks. The only behavioral
difference between the caps is unreachable in a valid run. Had this failed,
the trial would not have proceeded.

## Full-run results

- 40/40 `CL_CHECK` actual==expected (independent runner re-verification)
- `RC_FAILURES,0`; `TRIAL PASSED`
- Determinism: two consecutive binary runs byte-identical
  (sha256 `b6ff2b46…`), zero RNG tokens in trial or checker sources
- Falsification guard: ledger never reported FULL (grep count 0 in run
  stdout) — the run is valid, not void
- F1–F6 falsification criteria unchanged from RC1; negative control live
  (mini phase: 40/40 noshape after the lying commit, then deliberate
  rollback repaired V)
- White-box replay: `replay_diff,0`; replayed (V,R,S,stage) == live state

Key readouts: phase A 120/120 committed-noshape under the loose bar;
sim predicted 40/80/0 and phase B delivered exactly it (80 OK, 0 noshape,
40 refusals, S=370); stage advanced on 8+ consecutive IL_OK verdicts;
probe 1 (destructive V→1) refused with RC_REF_PRED (203); probe 2
(constitution target) refused with RC_REF_CONST (204); the lying
self-change passed the gate, was caught post-change by verification, and
the system rolled itself back — at 10×, same as RC1.

## What this does not claim

- Scale is 10× the 12-episode pilot (120-episode phases), not 100×.
- The capped-ledger-window mechanism is deferred to its own prereg (it is
  forgetting behavior, not a scale parameter).
- Elimination strictness as a controlled parameter is a separate future
  prereg; RC2 is the scale leg.

## Evidence

- `EVIDENCE_20260920T064730Z/` — full-run compile + paired runs + checker
  summary (this verdict)
- `EVIDENCE_EQUIV_20260920T064726Z/` — equivalence-proof builds + diffs
- `EVIDENCE_20260920T064349Z/` — the blocked attempt (startup panic,
  zero stdout): the defect record that motivated amendment (2)

Binaries (`rc2_trial_linux`), `.zag-cache/`, and `.zagd.semantic-ready`
are build artifacts and were NOT committed.
