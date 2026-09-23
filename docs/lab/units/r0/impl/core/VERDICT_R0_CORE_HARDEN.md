# VERDICT — R0 CORE-HARDEN (ZNC-2026-09-19-001 surgical hardening)

**Track:** R0, prereg `PREREG_FREEZE.md` §2 (FROZEN — correctness fix only, no design change)
**Date:** 2026-09-21
**Crew:** R0 CORE-HARDEN
**Outcome: NO CORRUPTION FOUND — no core rewrite performed.** (Task-briefed valid outcome.)

## What was done

1. **Readback probe** (`r0_probe.zag`, new): STORESEQ-style probe driving every
   3+ sequential `[]i32` store site in the committed core with known sentinel
   values and reading them back against **expected values** (not byte identity —
   a deterministic miscompile is byte-identical across reruns, so M8 alone
   proves nothing). Standalone entry `r0_probe_main.zag`; exit code = fails.
2. **Probed the current binary as compiled** — 9 sites, all with sentinels
   including negatives, i32 extremes (2147483647 / -2147483648), and high-bit
   values (65536-class, the harness's observed corruption signature):
   | site | store sequence | location | fails |
   |---|---|---|---|
   | INIT | 6 leg-config stores + 3 trailer | `r0_init` | 0 |
   | LEDGER | 16 ledger-word stores | `r0_ledger_emit` | 0 |
   | PROPOSE | 5 proposal-header stores | `r0_observe_span` | 0 |
   | PROMOTE | 7 bank-header stores | `r0_promote` | 0 |
   | SPLIT | 7 new-slot header stores | `r0_split_at` | 0 |
   | MERGE | 7 merged-slot header stores | `r0_merge_ids` | 0 |
   | RECRUIT | 7 new-slot header stores | `r0_support_gap_recruit` | 0 |
   | PAIR | 4 pair-slot stores | `r0_observe_pair` | 0 |
   | SMOKE_LABSET | 6 sequential stores | `r0_smoke.zag` Arena-B labset | 0 |
   **Total: 0 fails.** Stable across 3 standalone runs.
3. **Probe sensitivity is demonstrated, not assumed:** during development the
   MERGE probe reported fails=4 — investigation showed the *probe's* expectation
   was wrong (promotion sorts equal-utility ties by hash ascending, so the
   parent byte order was MGBB+MGAA, not MGAA+MGBB); the actual stored words were
   all correct. The probe was fixed to capture parent bytes dynamically and now
   reports 0. The comparator provably detects mismatches.
4. **Probe wired permanently into the smoke suite** (`r0_smoke.zag` imports
   `r0_probe.zag` and runs `r0_probe_run()` as a hard gate before the M8 body;
   `run_smoke.sh` also builds/runs the standalone probe and greps every smoke
   run for `R0_PROBE,total_fails=0`). Probe output is perturb-invariant, so M8
   byte-identity is preserved. Any future znc rebuild that miscompiles a store
   site now fails loudly instead of silently.
5. **M8 re-run** (N=5 + 5 adversarial perturbation modes × 2 legs):
   **M8_SMOKE_PASS** — byte-identical within leg, zero stderr on all 14 runs,
   probe gate fails=0 in all 12 smoke runs + standalone. All canonical metric
   values match the previously committed `SMOKE_EVIDENCE.txt` exactly
   (e.g. LEDGERHASH 251160451 / 473218425, PROMOTED 224 / 6).

## What was NOT changed (frozen surface intact)

- `r0_core.zag`: **byte-identical to the committed core** — no rewrite was
  warranted; rewriting working code on a frozen prereg would be gratuitous churn.
- `API.md`: **unchanged** — signatures, ledger layout (16 words,
  op@0/slot@4/rc@8/stage@52/d1@56/d2@60), ID semantics, both legs' parameters
  all untouched.
- Mechanism, API, and both parameter legs are exactly as specified.

## Files (this commit)

- `r0_probe.zag` (new) — 9-site STORESEQ readback probe, `r0_probe_run()`
- `r0_probe_main.zag` (new) — standalone probe entry point
- `r0_smoke.zag` (modified) — imports probe, hard-gates on `r0_probe_run()==0`
- `run_smoke.sh` (modified) — builds/runs standalone probe, gates every run
- `SMOKE_EVIDENCE.txt` (regenerated) — probe-gated canonical outputs
- `VERDICT_R0_CORE_HARDEN.md` (this sheet)

No binaries, no `.zagd`, no `.zag-cache` committed.

## Notes for the record

- The ledger region sits at arena index ≥ 91168, past the ZNC-2026-09-21-004
  large-index store-fault threshold (~61440); the LEDGER probe wrote and read
  back 16-word entries there cleanly — no 004-class fault in this build either.
- Laws honored: pure Zag; zero RNG in any decision path (probe included);
  scale 1x only. No `_zag_raw_syscall`, no `zalloc` naming, no slice-`==`.
- If a future toolchain rebuild changes codegen, the permanent gate catches it;
  only then does the `[]u8`-backed LE cell rewrite (a32/hc_le32 pattern) become
  necessary — the probe file documents the intended rewrite sites.
