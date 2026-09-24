# VERDICT_B3536 — PAM composition: H-PAM-35 capability-typed sinks + H-PAM-36 commit-then-sample

**Crew:** B-3536 (PAM round-2 swarm, composition build crew — second replacement; fresh start)
**Date:** 2026-09-24
**Prereg:** PREREG_B3536.md (`abbc35b29a3`) + Amendment 1 (`fed0d98e`) — frozen before build
**Verdict: SURVIVED** — all 17 bars green, 3× byte-identical both modes.

## Build

- Mechanisms by script extraction only (no retyping): H-35 repaired source
  from `1fa4ae58` (SHA `da10a482…`), H-36 repaired source from `6a30f5f9`
  (SHA `ba0cf689…`); 13 shared helpers asserted byte-identical, kept once.
- Dead-code removal (build v2): h35's pre-repair `m36` (hardcoded-seed
  mode-36 battery, uncalled) dropped from the lib — old seed now survives
  ONLY inside the marked M36-ATTACKER-CLASS fixture (the R-36 invariant).
- Class identity verified by script against RT-JKLM's frozen evidence
  `ec8d5d13` (25/25 constant checks, no drift).
- `b3536.zag` SHA-256 `1602247d7c9f1e96ba0f9df30a7b197f6a9ff71884df67c1cfb93c1807280029`
  (build commits `7fe177ae`, `7a1a8422`).
- Toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`; pure Zag, zero RNG.

## B1 — composition attack battery (install = stage1 AND stage2 on the same presentation)

| Class | Installs | S1 (typed sinks) | S2 (independence) | Bar |
|---|---|---|---|---|
| C35J (tag-replay/high-32) | 0/120 | 0 | 0 | ≤15 PASS |
| C35K (NT, 6 paths) | 0/120 | 0 | 0 | ≤15 PASS |
| C35L (guessed tags/replay) | 0/120 | 0 | 0 | ≤15 PASS |
| C35M (tag fit) | 0/120 | 0 | 0 | ≤15 PASS |
| C36K (blind guesses) | 0/120 | 0 | 0 | ≤15 PASS |
| C36M (precomputed chain) | 0/120 | 120 | 0 | ≤15 PASS |
| C36J (identity residual) | 120/120 | 120 | 120 | SCOPE-CARRY (expected 120) |
| C36L (independence) | MATCH 120/120 | — | — | PASS (bar 120) |

No class ≥ 97/120 (falsification rule not triggered). C36M is the D1-lesson
demonstration: stage1 alone would admit 120/120 (honest mint on attacker
content); stage2 alone refuses 120/120; the serial AND holds. C36J carries
the documented identity residual — identical to H-36 alone (composition
neither fixes nor worsens it; identity was never claimed).

## B2 — all original H-35 bars green (vs composition sources)

- `BAR_35_a_no_low_to_sink=PASS` (0/760 admitted)
- `BAR_35_c1_verdict_gates=PASS` (H2 0/40)
- `BAR_35_c2_honest_latency=PASS` (H1 60/60, delay 0)

## B3 — all original H-36 bars green (vs composition sources, fresh seed)

- frozen 0/60, RC 0/60 + 0 W-recoveries, WG1 120/120, WG2 0/200000, honest 60/60

## B4 — honest loss

- 35-side honest through both gates: 120/120 admitted (loss 0%, bar ≥102/120)
- 36-side honest (B3): 60/60

## B5 — determinism

- comp mode 3× byte-identical: SHA `a321d59d150377228c1c0d24c41b5239975873d813347e6db8191f0c2990afe4`
- b2b3 mode 3× byte-identical: SHA `007aa9c6b86027b7754f5fc16f57db058229c8b9153f2fdae731610c3824b9c6`

## Anti-interaction audit (composition-specific, per Amendment 1 A1)

- Exactly 1 `ns_sha256` call site (`r36_derive_seed`).
- Old hardcoded seed literals survive ONLY inside the marked M36-ATTACKER-CLASS fixture.
- No attacker-side percept construction mentions world/seed material
  (whi/wlo/shi/slo/seedhex/material/digest/ledger) — CLEAN.
- Seed-reuse detector exercised: a re-run against a used ledger is refused
  loudly (`REFUSED_SEED_REUSE`, rc=1, no trials).

## Composition-specific notes

1. Serial-AND semantics confirmed operationally: an install requires both
   gates to fail open on the same presentation; one half holding refuses.
2. The composition adds no carve-out: stage2 commits THE SAME percept the
   tag binds (cstep over the sink-verified content fields).
3. Honest world-consistent readings pass both gates at 120/120 — the
   composition is usable, not just inert.

## Verdict

**SURVIVED.** The composition holds the inertness boundary on all
kill-scored classes, keeps every original component bar green, loses 0%
honest percepts, and is deterministic 3×. Residuals carried forward:
identity (C36J, documented), and the R-36 open construction question (real
deployment needs a physical/organizational disjoint channel).
