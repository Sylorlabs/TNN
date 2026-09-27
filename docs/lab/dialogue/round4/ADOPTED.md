# ADOPTED — Dialogue Round-4 Machinery (2026-09-27)

**Decision (Micah):** the round-4 dialogue system is adopted as TNN's
standing dialogue machinery. Future dialogue work builds on
`docs/lab/dialogue/round4/dialogue.zag`, not on a fork or rewrite.

## What is adopted

1. **G6 untaught-predicate gate** — if no stored fact teaches the question's
   demanded predicate (under any key), withhold and clarify instead of
   returning an unrelated entity match. (Root fix for "When did he die?" →
   birth year.)
2. **G7 role-order gate** — entity overlap with reversed agent/patient roles
   withholds instead of answering the wrong direction.
3. **Unified entity scanner** — one scanner for arithmetic and lookup;
   punctuation stripping; negated entity words no longer poison "the other
   one" resolution.
4. **Correction-state mirror** — rejected correction candidates are never
   installed as answered knowledge.
5. **Scoped deletion** — delete/erase/wipe applies to memory scope only.
6. **Units from taught facts** — unit extracted at install from the fact's
   own text; differences rendered in the taught unit; conversion only on
   explicitly taught conversion facts; withhold when unknown. Zero
   dimension/unit names in code.
7. **Non-repeating requests** — deterministic per-session serving of
   repeat-request stock ("another joke"); honest exhaustion message,
   never silent repeats.

## Evidence at adoption

| Battery | Result |
|---|---|
| Round 4 | 38/38 |
| Round 3 | 23/23 good |
| Round-2 F2 | 351/370 (same 19 pre-existing failures as baseline) |
| Round-2 integrated | 15/18 (same 3 old drifts as baseline) |
| Generality probes (units) | 8/8 — length, mass, temperature, time, real km→m conversion, honest withhold on kg-vs-°C |
| Determinism | byte-identical reruns on all batteries |

Characterization: core architecture fixture (general withhold machinery +
shared-scanner bug fixes), not edge-case patches and not
scaffold-and-release. Nothing temporary was erected and removed.

## Residuals carried forward (not blockers)

- Typo tolerance threshold is length-parameterized but still a tuned
  parameter, not a derived one.
- Delete-scope rule is policy-shaped; kept deliberately per Micah's
  standing delete semantics.
- Traces remain execution/dispatch logs, not native deliberative
  reasoning — owned by the genuine-deliberation workstream.

## Commits

- `75267f9df7` — round-4 root-cause repair
- `fb4961d96` — units + jokes hardcode completion
