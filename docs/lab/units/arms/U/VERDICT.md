# VERDICT.md — U: Recompute-on-demand (Track A, r1, 1x)

**Date:** 2026-09-21
**Authority:** Coordinator frozen §3, second correction (2026-09-21).

## Coordinator corrections acknowledged
1. First correction (2026-09-21): U reassigned from the original
   dual-route/PROM to STORE / Recompute-on-demand.
2. Second correction (2026-09-21, AUTHORITATIVE): confirmed STORE /
   Recompute-on-demand with frozen mechanism text and binding kills.
   Authority order: `units/arms/briefs/U.json` → second frozen §3 row →
   nothing earlier.

The original dual-route/PROM assignment is VOID. The invalid wrong-arm M1
result (100/100) is NOT U evidence and is not reported here.

## Formal status: BLOCKED (provisional results below)

The frozen dependencies in AMBIGUITIES.md (A1–A4: derivation radius, MA1/RC1
rate, S equations, approved comparator) remain unresolved. Per the binding
rules, no run is accepted frozen evidence until these are formally resolved.
The results below are PROVISIONAL engineering results, not accepted evidence.

## Provisional 1x battery results (M1–M9)

| Metric | Result | Bar | Status |
|--------|--------|-----|--------|
| M1 (fresh recall) | 100.0% recall, 99.9% boundary | ≥99% | PASS |
| M2 (learning curve) | 100.0% throughout (store, no curve) | see A5 | PASS w/note |
| M3 (survival) | 100.0% survival, 100.0% fresh | ≥99% | PASS |
| M4 (interference) | 0.0% content, 0.0% boundary | see A6 | NOTED |
| M5 (footprint) | 0 corpus-buffer bytes | minimal | PASS |
| M6 (reversibility) | 100.0% rev, 0.0% tax | ≥99% | PASS |
| M7 (non-ID) | N/A, 319,937 reread bytes | N/A | N/A |
| M8 (determinism) | 10/10 byte-identical | M8GATE | PASS |
| M9 (edit sweep) | cost plateaus at 727,848 ops | bounded | PASS |

## 10x status
NOT ATTEMPTED. The r10 corpus provenance is unverified (AMBIGUITIES.md A9).
Per the binding rule, an attempted arm without a 10x row is ATTEMPTED —
FAILED; however the formal status here is BLOCKED (not attempted), so the
10x rule does not trigger a FAILED verdict — the block does.

## Kill criteria (provisional duel data, E=0..100)
1. **CPU >10× D and B4 <10%**: At E=0, cpu_u=2,024,572 vs cpu_d=5,154,934
   (U is 0.39× D, not >10×). **Kill does NOT fire.**
2. **D-with-invalidation beats U on total cost at 100 edits**: At E=100,
   total_u=1,727,480,888 vs total_d=2,219,096,277 (U wins by 22%).
   **Kill does NOT fire.**
3. **Determinism fails**: M8 gate PASS (10/10 byte-identical).
   **Kill does NOT fire.**

The E=200..1000 sweep is incomplete (duel heisenbug, AMBIGUITIES.md A8).
The E=0..100 trend shows U's total cost flat (~1.727B) while D's grows
with edits (2.206B→2.219B), so the kill conclusions are robust to the
missing sweep points.

## Verdict
**BLOCKED** — provisional results are encouraging (all 1x bars pass, no
kills fire on available data, M8 deterministic), but the frozen dependencies
must be formally resolved before any result is accepted as U evidence.
