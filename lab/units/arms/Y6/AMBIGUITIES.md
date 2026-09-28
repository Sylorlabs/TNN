# Arm Y6 — Ambiguities (literal readings logged, not reinterpreted)

Date: 2026-09-21. Author: ARM CREW Y6.

Per program law, ambiguous readings of the frozen prereg are logged
literally; the frozen text is never reinterpreted to convenience.

## A-Y6-1. "The same curriculum" (kill criterion, half 1)

The frozen row says "Ledger write volume > 10× arm D on the same
curriculum". The arms do not run identical M3 curricula: Y6's M3 (like
B-64's) ingests 1,000 valuables + 7,000 fresh-churn units, while arm D's
M3 ingests both full corpora plus churn. Literal reading adopted: compare
per-mode (M3, M5, M8) ledger write volumes as each arm defines the mode,
report the structural difference, and require the bar to fire on none.
Under every per-mode comparison the ratio is ≤ 1.0 (M3: 0.057) — the
ambiguity does not affect the verdict.

## A-Y6-2. Arm D's uncompilable source

D's committed source does not build in the pinned toolchain, so no
same-binary D measurement exists. Literal options were: (a) repair D's
source (changes D's behavior — invalid comparison and out of mandate);
(b) analytic derivation from D's source (adopted); (c) no comparison
(dereliction of the kill criterion). D's tree was restored byte-identical
after inspection. If D's crew later produces a compiling binary with
different volumes, this comparison must be re-run.

## A-Y6-3. M7 "ID references" definition

The spec defines reuse = "ID references / distinct live IDs" without
enumerating which operations count. Adopted: every resolution through the
ID→slot mapping — round-0 ingests (n) + round-1 re-ingests (n) + round-2
defect patches (n/100, each resolves its ID) + 5,000 lookups. Excluding the
defect patches would give 2.06 → 2.06 (indistinguishable at 2 decimals for
this n); the bar (≥1.5) passes under every reasonable definition.

## A-Y6-4. M7 fragment field names

The harness schema names the field "m7_dedup_savings_bytes" but the spec
defines dedup as the ratio 1 − distinct/total (2 decimals). Y6 emits the
measured ratio under `m7_dedup_ratio_hund` and reuse under
`m7_reuse_rate_hund`; per ARM_INTERFACE.md the `_tenths`/`_hund` suffixes
are historical — the values are already decimals (p_dec2 emits 2.06, not
206). The Y6-specific assembler uses the values directly. No byte figure
is fabricated to fit the misnomer.

## A-Y6-5. M5 memory/audit "bars"

`scorecard_assemble.py` annotates `memory_bar_1_5x` and `audit_bar_10_per_kb`
as FAIL for Y6 — and identically for the B-64 validator null control
(1.719 and 16.2 in the harness's own reference battery). They are recorded
as harness annotations, not as Y6 kill criteria and not as 10x gates; the
frozen §3 row is the only binding kill criterion.

## A-Y6-6. M7 provisional status vs bars

A7/A8 (C′ edit bytes, lookup schedule) are not frozen by Micah, so Y6's M7
runs the validator's proposed procedure as PROVISIONAL-PENDING-FREEZE. The
three numeric bars (hit ≥ 90, reuse ≥ 1.5, dedup ≥ 0.4) are stated
unconditionally for ID arms and all pass; the provisional qualifier is
carried in the TAG line, the JSON `na_reason`, and the scorecard.
