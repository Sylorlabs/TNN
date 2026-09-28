# Amendment 2026-09-28 — D2-4 (PROPOSED): K1 chance = max(NULL, SINGLE-RULE)

**Status: PROPOSED 2026-09-28. NOT SIGNED. NOT LAW.** This amendment takes
effect only if Micah signs it. Until then the frozen text (as amended by
D2-1..D2-3) governs, and any K1 adjudication must state which chance
definition was used.

## What it changes

Frozen A1 (enacted 2026-09-27 via `AMENDMENT_2026-09-27_A1.md`) defines
`chance = max(NULL, SINGLE-RULE, WRONG-ORDER)` episode-pass rate, measured
on the D2 instrument. This amendment removes WRONG-ORDER from the max:

> **chance = max(NULL-D2, SINGLE-RULE-D2)** episode-pass rate on the D2
> instrument, per A1's principle.

## Frozen text reference

`docs/lab/composition/d2spec/D2_INSTRUMENT_SPEC.md` §7 and §9 (K1):

> - **K1 — chance kills composition:** P2 episode pass rate ≤ chance + 0.10
>   → composition claim KILLED. `chance` = max(NULL-D2, SINGLE-RULE-D2,
>   WRONG-ORDER-D2) pass rate measured on the D2 instrument (§7), per A1.

## Enacted change (if signed)

For D2 only, replace the chance definition with:

> `chance` = max(NULL-D2, SINGLE-RULE-D2) pass rate measured on the D2
> instrument, per A1. The +0.10 margin is unchanged.

## Why

The spec's §10 gate assumed the scripted ward-first policy (WRONG-ORDER-D2:
competent sub-skills applied in a fixed S2→S3→S1 order) would fail every P2
scenario. It does not. Measured on the frozen scenarios: **WRONG-ORDER
passes 24/24 P2 scenarios** (`docs/lab/composition/d2/evidence/BUILD_LOG.md`,
"WRONG-ORDER: P2 24/24 — DEVIATION"). Ten ticks of ward-first ordering does
not break passability on these scenarios; the wrong order is merely
inefficient, not fatal.

With WRONG-ORDER in the max, chance = 24/24 = 1.0, and K1's kill line becomes
1.0 + 0.10 = 1.10 — a pass rate no agent can exceed. K1 could never fire:
the battery could neither confirm nor kill the composition claim. That is
not a conservative bar; it is a vacuous one.

NULL-D2 (all-WAIT) and SINGLE-RULE-D2 (forage-only, never builds a ward)
both fail all 24 P2 scenarios by construction (starvation; the WARD-placed
criterion). They are genuine chance-level arms: they represent what an
agent that does not compose sub-skills achieves. max(NULL, SINGLE-RULE) =
0/24 on the frozen scenarios, giving K1's kill line at 0.10 — a real,
reachable bar.

## What it does NOT change

- The K1 +0.10 margin, the K1 kill direction, and A1's max-of-arms
  principle are preserved exactly. Only the arm set is corrected.
- The WRONG-ORDER scripted policy stays in the battery as a reference
  mode (it still exercises the instrument and documents the
  order-robustness finding). It is removed from the *chance* computation
  only.
- No other bar, threshold, taxonomy code, or D1 behavior changes.
- D2-1 (criterion scoring), D2-2 (K6), D2-3 (P4) are untouched.

## Evidence

- `docs/lab/composition/d2/evidence/BUILD_LOG.md` — WRONG-ORDER 24/24
  deviation, documented 2026-09-27 with the spec's §10 gate assumption
  shown false.
- This re-run's `results.json` (all runs): NULL-D2 0/24, SINGLE-RULE-D2
  0/24, WRONG-ORDER-D2 24/24 — re-measured on the rebuilt instrument,
  byte-identical across runs.

## Adjudication note

Until signed, K1 must be reported both ways: (a) under the frozen
max-of-three definition (chance = 1.0, kill line vacuous), and (b) under
the proposed max(NULL, SINGLE-RULE) definition (chance = 0.0, kill line
0.10). The verdict in this re-run is VOID under K2 either way; the
amendment matters for the first non-VOID D2 run.
