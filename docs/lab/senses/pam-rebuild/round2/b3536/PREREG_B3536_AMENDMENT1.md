# PREREG_B3536 — AMENDMENT 1 (corrections before build)

**Date:** 2026-09-24
**Amends:** PREREG_B3536.md as frozen in `abbc35b29a337ed6a3ae3d3d0acf73867b7e48ab` (this crew's own checkpoint, minutes old, no build yet). This is a self-contradiction correction + scope clarification. No kill-bar weakening: the headline bars (each class ≤ 15/120 installs; any class ≥ 97/120 kills; B2/B3 all green; honest-loss ≤ 15%; 3× byte-identical) are unchanged.

## A1. §1 composition failure semantics — corrected

The frozen text reads: "an attack class installs only if it defeats BOTH the
typed sink barrier AND the independence check — i.e., the composition fails
open iff either half fails open." These two clauses contradict; the second is
a drafting error. Corrected rule:

> A composition trial INSTALLS iff the presentation defeats BOTH the H-35
> capability-typed sink gate AND the H-36 commit-then-sample gate on the same
> presentation — i.e., the composition fails open iff BOTH halves fail open on
> the same presentation. One half holding is enough to refuse. The gates are
> serial AND, not OR.

Operationally per trial:
1. Stage 1 (H-35 admission surface): the percept must reach `act_sink` /
   `premise_sink` as a `HighVal` whose capability tag verifies over the full
   64-bit preimage (repaired R-35 tag binding; tag commits tag content +
   verdict bit). Tag-forgery / verdict=0 → stage-1 refuses.
2. Stage 2 (H-36 independence gate): the fixture commits `cstep(bs, id,
   conf, meas)` (domains 5/6) over THE SAME percept the tag binds (no
   carve-out — D2 lesson); the harness draws sample `s` from the
   disjoint world channel under R-36's fresh-seed discipline
   (`ns_sha256` over the committed transcript; seed-reuse detector
   refuses loudly); admit iff the commitment binds AND the opening is
   world-consistent (`admit36` semantics).
3. Sink delivery iff stage 1 AND stage 2 admit.

Anti-interaction audit (composition-specific, WG3-style): the composition
source must keep the channels disjoint — exactly one `ns_sha256` call site
(`r36_derive_seed`); no `shi/slo/seedhex/material/digest/ledger` reaches any
attacker-side fixture function; no `forge`/tag-mint inside the H-36-side
paths; no world-step (`wstep`/W) reads inside the H-35 tag paths. Any
cross-half channel = KILL (composition opened what components held).

## A2. J-36 identity residual — documented carry, not kill-scored

Class semantics (§2) already record: "J-36: identity residual scope-confirm
(admit36 never checks id — not a kill of the stated claim)". The composition
adds no identity machinery (neither component claims identity; cf. the
H-OB-22 no-authenticated-registry caveat), so the J-36 composition
sub-battery (honest world readings, spoofed id, honest tag mint) is expected
at 120/120 installs — identical to H-36 alone. It is a **documented
identity-residual carry**: reported in B1 alongside the other sub-batteries,
and scored as CARRY iff it matches H-36's 120/120 exactly (composition
neither fixes nor worsens it). A mismatch (composition J36 ≠ H-36-alone J36)
is investigated as a possible interaction effect before any verdict.

Likewise L-36 is a metric battery, not an install battery: sample-sequence
match must equal 120/120 (independence PASS, same as original); divergence
is a KILL.

B1 kill scoring therefore applies to the install sub-batteries J35, K35,
L35, M35, J36(excepted as carry per A2), K36, M36: each ≤ 15/120 installs;
any ≥ 97/120 kills the composition. (J36 carry: ≥97 rule does not apply.)

## A3. No other changes

Build-from-script-extraction (§5), B2 (all original H-35 bars green), B3
(all original H-36 bars green incl. WG3 source audit CLEAN on the
composition sources), B4 (honest-loss ≤ 15% per class), B5 (3×
byte-identical), and the no-repair rule for compositions all stand.
