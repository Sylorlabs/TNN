# RC3 Results — native reasoning control at 100× scale (2026-09-20)

**Verdict: PASS — 40/40 preregistered checks, byte-identical reruns, zero RNG.**

## What ran

`rc3_trial.zag` (native Zag): the identical RC1/RC2 machinery at 100×
episodes — same params (V, R), same ops, same gate order and refusal codes
(201–204), same constitution, same integrity-ledger checker logic. Only the
prereg-authorized changes: parameterized defect rule (offset, modulus,
residue) per leg, phase bounds 1200/1200/400, item id bases 0/10000/20000,
`ep_def` 1200 entries, `RC_SMAX=15000` as a per-leg parameter (150×100),
recomputed check constants, probe-1 honest degrading prediction 0→1200,
declared capacity instrumentation (`IL_HEAD`, `AUDIT_USED` prints).

## The port defect and its resolution (honest record)

The first full-run build exited `RC_FAILURES,3` on `pred_refusals`,
`pred_ok`, `refusals_match_pred` (37/40 passed): the revelation call was
not scaled (`rc_reveal(...,120,...)` → sim predicted from 120 bits), and
probe-1's `rc_rcommit` carried `pred_bad=120` against a 1200 PROPOSE entry.
Port bug, not mechanism failure — the run tested a non-preregistered
configuration. Per program law a dated amendment (PREREG_RC3.md amendment
(A), overnight-agentic authority, flagged for Micah's retroactive review)
was written before the re-run; no bar, gate, constant, or falsification
criterion changed. The failed run's evidence is kept as the defect record:
`EVIDENCE_20260920T085711Z/` (RC2 precedent).

## Equivalence proof (prereg §7, before the run)

The mini variant (12/12/4, IL budget ≈ 80 ≤ 128) compiled against the
canonical 128-cap checker and the leg-local 10240-cap checker produced
**byte-identical check verdicts** (sha
`99a53a9d93f046e128eb29e4358e3654b61f717d74ede53fbfdcc3249ab2f84f` both
builds), each self byte-identical across two runs, each passing its own
40/40 derived checks. The only behavioral difference between the caps is
unreachable in a valid run. Evidence: `EVIDENCE_EQUIV_20260920T085700Z/`.

## Full-run results

- 40/40 `CL_CHECK` actual==expected (independent runner re-verification)
- `RC_FAILURES,0`; `TRIAL PASSED`
- Determinism: two consecutive binary runs byte-identical
  (sha256 `b130db24b47fc063a85ab2e2358ee5aeb31bdd0f3734c04a93552416e8d4f58c`),
  zero RNG tokens in trial or checker sources
- Capacity guards held: `IL_HEAD,8000` (cap 10240 — exactly the code-model
  estimate 800×10, validating the capacity law); `AUDIT_USED,13218`
  (cap 16384, estimate 14017); no `IL_AUDIT_FULL` in stdout — the run is
  valid, not void
- Timing probe (prereg §6): RC2 single run 0.0064s → projected 0.77s;
  actual RC3 runs 0.26s / 0.30s. The 8h fallback was never near triggering.
- Falsification: F1–F6 unchanged from RC1/RC2; negative control live
  (patched copy miscounting 399 instead of 400 refusals → `RC_FAILURES,1`
  on `refusals_b` exactly as designed; evidence in `/tmp/rc3_neg/`)
- White-box replay: `replay_diff,0`; replayed (V,R,S,stage) == live state

Key readouts: phase A 1200/1200 committed-noshape under the loose bar;
sim predicted 400/800/0 and phase B delivered exactly it (800 OK, 0 noshape,
400 refusals, S=3250); stage advanced on 800 consecutive IL_OK verdicts;
probe 1 (destructive V→1) refused with RC_REF_PRED (203) on the honest
0→1200 degrading prediction; probe 2 (constitution target) refused with
RC_REF_CONST (204); the lying self-change passed the gate, was caught
post-change by verification (mini 400/400 noshape vs predicted 0), and the
system rolled itself back — at 100×, same as RC1/RC2.

## What this does not claim

- Scale is 100× the 12-episode pilot (1200-episode phases), not beyond.
- The capped-ledger-window mechanism is deferred to its own prereg.
- Elimination strictness as a controlled parameter is a separate future
  prereg; RC3 is the scale leg.
- Amendment (A) and the IL_CAP=10240 per-leg parameter were enacted under
  overnight-agentic authority and are flagged for Micah's retroactive
  review; a rejection voids the leg (revert: delete `wave10/rc3/`).

## Evidence

- `EVIDENCE_20260920T085850Z/` — passing full run: compile + paired runs +
  checker summary (this verdict)
- `EVIDENCE_EQUIV_20260920T085700Z/` — equivalence-proof builds + diffs
- `EVIDENCE_20260920T085711Z/` — the voided first attempt (port defect,
  `RC_FAILURES,3`): the defect record that motivated amendment (A)

Build artifacts (binary, `.zag-cache/`, `.zagd.semantic-ready`) are NOT
for staging. Negative-control evidence lives in `/tmp/rc3_neg/` (outside
the trial dir, per prereg 3d).
