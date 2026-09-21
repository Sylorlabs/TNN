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
| M9 (edit sweep) | cost plateaus at 727,848 ops (e200), rekey=0, hits=0 | bounded | PASS |

## Completed duel sweep (2026-09-21, post-fix)
The duel heisenbug was root-caused (silent i32 overflow in the edit-position
computation, not a layout issue — see AMBIGUITIES.md A8) and fixed with i64
arithmetic. The full sweep E=0..1000 now completes; both reruns are
byte-identical on stdout and stderr (rc=0). E=0..100 rows are unchanged vs
the pre-fix runs, confirming the fix is behavior-neutral where no overflow
occurred.

| E | cpu_u | cpu_d | total_u | total_d | winner | bad |
|---|-------|-------|---------|---------|--------|-----|
| 0 | 2,024,572 | 5,154,934 | 1,727,480,380 | 2,205,948,726 | U | 0 |
| 10 | 2,024,540 | 6,465,691 | 1,727,480,348 | 2,207,286,619 | U | 0 |
| 50 | 2,024,780 | 11,708,366 | 1,727,480,588 | 2,212,529,294 | U | 0 |
| 100 | 2,025,080 | 18,261,781 | 1,727,480,888 | 2,219,096,277 | U | 0 |
| 200 | 2,025,680 | 31,368,841 | 1,727,481,488 | 2,232,216,905 | U | 0 |
| 500 | 2,027,480 | 70,690,416 | 1,727,483,288 | 2,271,558,832 | U | 0 |
| 1000 | 2,030,480 | 136,225,681 | 1,727,486,288 | 2,337,128,017 | U | 0 |

Kills on the completed sweep: crossover E = none (U wins every leg);
kill_i = 0 (cpu_u_total = 14,182,612, cpu_d_total = 279,875,710 — U is
0.05× D, not >10×); kill_ii = 0 (at E=100, total_d = 2,219,096,277 >
total_u = 1,727,480,888); byte mismatches = 0. **No kill fires on the
completed sweep.** Determinism: M8 gate still PASS (10/10 byte-identical);
the duel's own two full runs are byte-identical.

## 10x status
NOT ATTEMPTED. The r10 corpus provenance is unverified (AMBIGUITIES.md A9).
Per the binding rule, an attempted arm without a 10x row is ATTEMPTED —
FAILED; however the formal status here is BLOCKED (not attempted), so the
10x rule does not trigger a FAILED verdict — the block does.

## Kill criteria (completed duel sweep E=0..1000, byte-identical reruns)
1. **CPU >10× D and B4 <10%**: At E=0, cpu_u=2,024,572 vs cpu_d=5,154,934
   (U is 0.39× D, not >10×). **Kill does NOT fire.**
2. **D-with-invalidation beats U on total cost at 100 edits**: At E=100,
   total_u=1,727,480,888 vs total_d=2,219,096,277 (U wins by 22%).
   **Kill does NOT fire.**
3. **Determinism fails**: M8 gate PASS (10/10 byte-identical); completed
   duel sweep byte-identical across both full reruns.
   **Kill does NOT fire.**

No kill fires on the completed E=0..1000 sweep (est=none, kill_i=0,
kill_ii=0, bad=0).

## Verdict
**BLOCKED** — provisional results are encouraging (all 1x bars pass, no
kills fire on available data, M8 deterministic), but the frozen dependencies
must be formally resolved before any result is accepted as U evidence.
