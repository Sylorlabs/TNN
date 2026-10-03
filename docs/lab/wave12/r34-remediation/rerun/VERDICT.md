# VERDICT — clean rerun of the wave-2 long-horizon battery (r34 remediation)

**Workstream:** RERUN (2026-09-20). **Prereg:** `PREREG_RERUN.md`, frozen and
committed alone as `9ed0203a1594` before any evidence run. **Apparatus:**
`3642f69ee9f7` (+ runner determinism-diff fix, committed with this verdict).
**Evidence:** `EVIDENCE_20260921T000109Z/` (this directory).

## Runner fix after apparatus commit (not a prereg amendment)

The first evidence attempt failed determinism diffs on all three campaign
legs for one reason only: the new `LH_RESOURCE` telemetry line embeds raw
wall-clock `cpu_us`, which is inherently non-repeatable. All scientific
state (fingerprints, traces, CL_CHECKs) was byte-identical between the two
runs. The runner now diffs stdout with `LH_RESOURCE` lines excluded —
telemetry stays in the bundle, the determinism bar covers scientific state.
Frozen bars are untouched.

## Kill criteria

- **K1 (determinism):** not triggered — every leg byte-identical across two
  full runs on scientific state (`lh1/lh2/lh3/lh5` `.determinism` all
  `deterministic_runs_equal=true`).
- **K2 (static audit):** not triggered — learner core shows zero forbidden
  terms, imports `observation.zag` only; harness forbidden terms confined to
  the two prereg-A6 evaluator devices plus documented `*seed` identifiers
  (see `audit.*.txt`, `isolation.txt`).
- **K3 (toolchain):** not triggered — clean compile, all runner exits 0.

## Per-leg verdicts (bars from the original protocol; no bar was bent)

### LH-1R (10 blocks, 480 updates) — PASS
`train_updates==480` ✓ · zero `LH_BLOCKFAIL` (all 20 block-probes 16/16) ✓ ·
return-A `ra=15`, `active=0`, zero weight updates ✓ · controls:
disabled-update B probe 12/24 with `updates==0` ✓, scrambled-reward A probe
0/16 ✓. Dynamics: 19 training switches + 1 return switch, 16 explores (all
in block 0; budget refilled but unspent afterwards), max |score| 22300
(tainted: 18900 — no clamp pathology at the 30000 limit). Headline dynamics
reproduce the tainted run exactly (same switch cadence, same return).

### LH-2R (40 blocks, 1920 updates) — PASS
`train_updates==1920` ✓ · zero `LH_BLOCKFAIL` (all 80 block-probes 16/16) ✓ ·
return-A `ra=15`, `active=0`, zero weight updates ✓ · controls same as LH-1 ✓.
Saturation finding reproduced: correct cells pin at +30000 during block 13
(tainted: block 16 — three blocks earlier, because zero steady-state
explores raise the net accumulation rate; ordering-based discrimination
survives with a larger margin). Wrong cells sink only via switch episodes
(−4700/−4800 at block 39 vs tainted −21100/−20100, which also absorbed
20% explore flips); no post-saturation rigidity in either run. 80 switches,
16 explores total.

### LH-3R (100 blocks, 4800 updates, drift seed 333) — PASS
`train_updates==4800` ✓ · zero `LH_BLOCKFAIL` ✓ · drift schedule reproduced
exactly as 1,1,2,0,0,2,1,2,2,1 (the tainted schedule) ✓ · all 60 mode-0/1
blocks 16/16 ✓ · all 40 mode-2 blocks at `ea=15/16, eb=16/16` — the
switch-cost probe artifact reproduced exactly (logged as `LH_FINDING`, 40
of them) ✓ · return `ra=16`, `active=1`, zero weight updates (mirror-context
assignment under B-first drift, same as tainted) ✓. Correct cells pin
during block 14 (tainted: block 16). Classification: **stable** —
no block below 15/16 in either regime at 100× horizon.

### LH-5R (noisy reward, 0/10/25/50% × 480 updates) — PASS
`LH5_FAILURES=0` ✓ · validity gate: 0% lineage 20/20 probes at 16/16,
zero collapsed probes ✓ · corruption channel bit-identical to tainted
(flips 0/46/124/241 over 480 training accepts at 0/10/25/50%) ✓.
The knee is **between 0% and 10%**, confirmed clean: 10% already produces
total per-block collapses (blocks 5-B and 9-A at 0/16 — the exact same
blocks and regimes as the tainted run); 25% collapses blocks 3-A, 4-B, 9-A
(also exact); 50% collapses most blocks with endpoint A=0,B=0 (tainted:
A=0,B=16 — delta: both regimes destroyed at endpoint vs one). Switch
explosion reproduced: 19 → 90 → 154 → 198 (tainted: 19 → 91 → 149 → 181).
Supplementary sensitivity: (10%,7777) 2 collapsed probes; (10%,4242) 6
(denser seed, still consistent with knee<10%); (25%,7777) 5 — all
consistent with the tainted pattern. Explores under corruption 38/61/76
(disappointment path engages, capped by the 8-per-phase budget).

## Restored vs suspended claims

| Claim | Tainted verdict | Clean verdict |
|---|---|---|
| C1 — delayed-credit rule stable at 10× (LH-1) | quarantined | **RESTORED** — LH-1R PASS |
| C2 — stable at 40×, saturation without rigidity (LH-2) | quarantined | **RESTORED** — LH-2R PASS |
| C3 — stable at 100× under schedule drift (LH-3) | quarantined | **RESTORED** — LH-3R PASS |
| C4 — noisy-reward fragility, knee between 0% and 10% (LH-5) | quarantined | **RESTORED** — LH-5R PASS |
| LH-4 (multi-return) | quarantined | **remains suspended** (out of scope) |
| LH-7 (rapid alternation) | quarantined | **remains suspended** (out of scope) |
| LH-6 (blocked) | blocked | **still blocked** |

## Headline

No clean leg failed a bar the tainted leg passed. All four quarantined
claims under test are restored by clean evidence, including two
byte-exact behavioral reproductions (LH-3's drift schedule and mode-2
artifact; LH-5's corruption flip counts and 10%/25% collapse pattern).
Documented deltas vs the tainted runs (earlier saturation pinning, slower
wrong-cell sink, LH-5 50% endpoint 0/0 vs 0/16, max|score| 22300 vs 18900)
are expected consequences of the remediation (bounded state-driven
exploration replacing 1-in-5 flips) and are reported, not smoothed over.
