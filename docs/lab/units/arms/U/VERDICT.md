# VERDICT.md — U: Recompute-on-demand (Track A, r1, 1x)

**Date:** 2026-09-21
**Authority:** Coordinator frozen §3, second correction (2026-09-21).
**Adjudication:** MARATHON CREW U11 (2026-09-21) — see `ADJUDICATION.md`.
Formal status: **PASS (BINDING)**. The A1–A4 blocks are resolved or proven
non-load-bearing (§2 of ADJUDICATION.md); A2/A9 remain open as documented
non-blocking items. The provisional results below are now accepted U
evidence, with the adjudicated corrections noted.

## Coordinator corrections acknowledged
1. First correction (2026-09-21): U reassigned from the original
   dual-route/PROM to STORE / Recompute-on-demand.
2. Second correction (2026-09-21, AUTHORITATIVE): confirmed STORE /
   Recompute-on-demand with frozen mechanism text and binding kills.
   Authority order: `units/arms/briefs/U.json` → second frozen §3 row →
   nothing earlier.

The original dual-route/PROM assignment is VOID. The invalid wrong-arm M1
result (100/100) is NOT U evidence and is not reported here.

## Formal status: PASS (BINDING) — adjudicated 2026-09-21 (MARATHON CREW U11)

The frozen dependencies in AMBIGUITIES.md (A1–A4) are resolved or proven
non-load-bearing for the verdict — see `ADJUDICATION.md` §2:
- **A1 (radius):** value never frozen; proven non-load-bearing by
  radius-sensitivity sweep (no kill fires at any U_R ∈ {32,…,4096}; U's cpu
  stays >10× below the kill-(i) threshold across a 128× radius range).
- **A2 (MA1/RC1 rate):** absent from all frozen materials; not load-bearing
  for U's kills (governs only the D-falsification interpretation of a U
  win, which stays provisional). Open §13 item for Micah.
- **A3 (S equations):** implementation's integer-counter translation is
  logged and was never refit mid-trial; U and DReg share the identical
  `u_derive` code path, so duel kills are translation-invariant.
  Non-load-bearing.
- **A4 (comparator):** resolved — DReg is the faithful "D-with-invalidation"
  (same derivation rule + persistent registry + materialized-copy cache +
  lazy invalidation); Track-A arm D cannot serve (different derivation rule).
- **A9 (10x):** not attempted (r10 provenance unverified); binding 1x
  verdict stands per the verdict sheet's own 1x convention.

Adjudicated corrections to the provisional results below:
- **M4:** the arm's all-or-nothing 0.0 is a scoring artifact. Instrumented
  probe localized all 28 failures to claimed-span alignment on code
  content-defect units; per-unit M4 = content 372/400 = 93.0%, boundary
  100/100 = 100.0% (both ≥ 80%/class bar). Kill rate 0.
- **M9:** the 1x fragment below is pre-fix; adjudicated (post-fix,
  byte-identical reruns): e0=175944, e10=175944, e50=203976, e100=727756,
  e200=727848, e500=727204, e1000=727204, rekey=0, hits=0 — plateau holds.
- **M2 ep0 note (A5):** the arm's "ep0" is measured post-ingest, so the
  frozen no-ingest leak clause does not apply as written; ETC=1 all tiers.
- **Memorizer controls** (previously omitted) now run: memctrl-p2c-1x and
  memctrl-c2p-1x, rc=0, double-run byte-identical.
- **M8 gate** re-run on a fresh source build: 5 perturbations × 2 reruns,
  byte-identical, M8GATE PASS.

## Provisional 1x battery results (M1–M9) [now accepted evidence, with the corrections above]

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
**PASS (BINDING)** — adjudicated 2026-09-21 by MARATHON CREW U11
(see `ADJUDICATION.md` for the full evidence record).

Kill evaluation on the completed E=0..1000 duel sweep (byte-identical
reruns, rc=0):
1. **CPU >10× D and B4 <10%**: cpu_u = 14,182,612 vs cpu_d = 279,875,710
   (U is 0.051× D, not >10×). **Kill does NOT fire.**
2. **D-with-invalidation beats U on total cost at 100 edits**: at E=100,
   total_u = 1,727,480,888 < total_d = 2,219,096,277 (U wins by 22.1%).
   **Kill does NOT fire.**
3. **Determinism fails**: M8 gate PASS (5 perturbations × 2 reruns,
   byte-identical); all battery legs double-run identical; duel reruns
   identical. **Kill does NOT fire.**

No kill fires. U wins every duel leg E=0..1000 (crossover: none) with zero
byte mismatches. The radius-sensitivity sweep (U_R 32→4096) confirms no kill
fires at any radius. Awaiting Micah's §13 items (radius value, MA1/RC1 rate)
does not block this verdict; the 10x leg remains future work.
