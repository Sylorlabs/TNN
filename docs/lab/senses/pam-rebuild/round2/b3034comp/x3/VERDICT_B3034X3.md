# VERDICT_B3034X3 — 2026-09-25

**DEMOTED** — machine-computed in `RUNLOG_B3034X3.md` from the frozen outputs.

## What was tested

The second rebuild of the PAM 30+34 composition driver (build
`7d7fd6c71f0e00f76e072683efd8f8a2b6774541`, prereg `b05d307c`): the driver
owns the queue, K counting, clocks, gap authentication, digests, trajectory,
ledger, and the sink call; fixtures present percepts and epochs only.

## Why not TESTED-killed

No kill bar fires on any of the 3 byte-identical runs:

- Every safety row is 120/120 correct with its exact rc (E0→10, E1/E2→14,
  G0→10, G1→14, T0→11, CLONE→14 with dup→4 at enqueue, SEED-SPLIT→13,
  P0→7, NOP-OMIT→13, C12→13; G2/P1/R0/ID-POISON/FIRST-WINS promote 120/120;
  FIRST-WINS2→6 ×120). Zero safety-row failures — the ≥97/120 kill
  threshold is nowhere near met.
- Honest bars: H0 120/120 promote (bar ≥115); contradicted percepts
  withheld 120/120; honest loss 0% (bar ≤15%); gapped-honest X3a delivery
  (G2) 120/120 (bar ≥115).
- Structural inexpressibility: none. The X2 presenter-authority transcripts
  (caller K, presenter time, verdict bounds) are inexpressible BY
  CONSTRUCTION, which the prereg expressly allows where the attack is made
  unavailable (C-E0/C-TEMP/C-SEED); the attacks they represented are closed,
  not evaded — the battery's refusal rows confirm it.
- Determinism: 3 full runs byte-identical (`b1e6b4e3…`), 3 nop runs
  byte-identical (`e55889eb…`); pure Zag, zero RNG.

## Why not MECHANISM-ABSENT

The preregistered 34-half ablation moves all seven required classes by
120/120 (bar ≥97): E0, E1, E2, G0, G1, CLONE flip refuse→promote; T0 moves
rc 11→13. The full and nop batteries are not byte-identical. The 34-half's
refusals are load-bearing — under the nop, zero-evidence and short windows
promote vacuously (the documented cost of removing K-counting), and the
epoch world disappears (G2/T1/P1/H0 → rc=13 on the flipped epoch-2 label).

## Why DEMOTED (not SURVIVED — which the prereg forbids printing)

The §0 claim holds only in its scoped, test-valued form:

1. **Sink scope note (carried):** the sink fires on true extra-consistent
   goals only when every admitted percept meets `conf >= 95` (B-3034COMP §6
   scope note, carried by the prereg). Measured: H0 fires 24/120, C4 38/120,
   C8 52/120. The bare words "the sink fires on true extra-consistent
   goals" are demoted to the threshold-gated form — the fired condition is
   the call, and the call is threshold-gated.
2. **Test values, not governance:** CAP=40, K=3, TOL_C=10, TOL_M=50, the gap
   seal, and MAX_AGE=64 are preregistered test values; their governance
   values await Micah's call (prereg §6). The claim is demoted to "holds
   under the preregistered test values."
3. **Q0 liveness is SCOPE-CARRY** (prereg C-Q0): measured (enqueue→rc=2,
   decide→rc=10), not killed on.
4. **R0 is carried with the construction proof** (prereg C-R0, frozen
   choice): no reset symbol exists in the decision API (source-inspected);
   the R0 class scores the intact decision path (120/120 promote).

The driver refuses every attack class in the B-OBJ4 battery, admits honest
percepts at 120/120, and its 34-half is a proven-real mechanism — but the
composition has not earned an unqualified SURVIVED. It stands DEMOTED to
the scoped claim above.

## Exploratory (non-frozen, reported as measured)

J 0/120 promote & sink silent; K 120/120 promote, 0 fired; L 114/120
withheld (6 toy-world collisions); M 0/120; N 0/120; O 120/120 (order-free
by construction); P 0/120 remint refused, P2 120/120 own-triple control.
See the runlog for the L-class toy-world artifact note.

## Commits (branch `tnn-native-lab`, repo `sylorlabs/TNN`)

- prereg `b05d307c` (frozen, pre-existing)
- build `7d7fd6c71f0e00f76e072683efd8f8a2b6774541`
- evidence: this commit (runlog, verdict, six outputs, SHA manifest)
