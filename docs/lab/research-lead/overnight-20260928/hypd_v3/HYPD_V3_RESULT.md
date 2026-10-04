# Hypothesis D v3 Result

## Verdict: HYPD-V3-PASS

**Date:** 2026-09-30
**Prereg:** `PREREG_HYPD_V3.md` (committed alone at `3847065e2`, 2026-09-30)
**Implementation:** `hyp_d_v3.zag` (copied from D-v2 at `2500fd02b`, modified per prereg)
**Compiler:** pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`

## Kill Bars (from PREREG_HYPD_V3.md)

**K1 (prereg-first):** PASS. Prereg committed at `3847065e2`. Implementation
derived from v2 source after prereg. Verified via `git merge-base --is-ancestor`.

**K2 (v3-both T3 SOLVE):** PASS.
- v3-both (SEL_MODE=1, CARRY_MODE=1) T3 SOLVE on 3/3 runs, byte-identical.
- CARRY_BLOCK_CHECK clean on all 3 runs.
- Both fixes present in source (verified in header emits).
- No parity-specific mechanism (generic MAP-Elites, no parity code).

**K3 (purity):** PASS with note.
- Pure Zag (no Python anywhere; build and analysis via shell + znc only).
- 3/3 runs byte-identical (md5 `ab74f8b6781f446141b67a65955c241f`).
- Paper untouched (contaminated paper never opened).
- Note: frozen prereg line 142 contains an em-dash (author error during
  prereg writing, now immutable under freeze). Result document is clean.

**D-V3-FAIL conditions:** None triggered.

## Results by Configuration

### v3-both (SEL=1, CARRY=1) - the claim config - 3/3 runs

All three runs byte-identical (md5 `ab74f8b6781f446141b67a65955c241f`).

| Task | Verdict | Evals | Solution | Held-out |
|------|---------|-------|----------|----------|
| T0 2x+1 | SOLVE | 37,086 | `[PUSH:1 PUSH:-2 IN0 MUL SUB]` | 16/16 |
| T1 abs (P-VM) | FAIL | 1,000,000 | `[IN0]` (best) | 4/8 |
| T2 mod3 | SOLVE | 23,517 | `[IN0 PUSH:3 IN0 PUSH:6 SUB PUSH:-6 IN0 ADD MUL MUL PUSH:-9 MOD MOD]` | 17/17 |
| T3 parity | SOLVE | 556,548 | `[PUSH:-1 PUSH:1 IN1 PUSH:-9 IN0 DIV SUB ADD PUSH:-2 MOD DUP MUL DIV NEG]` | 31/39 |

**T3 details:**
- Solved at eval 556,548 (of 1M budget) via archive parent (niche 55811).
- 14-op solution, train 25/25, held-out 31/39.
- CARRY_BLOCK_CHECK: niche 17570 occupied=1,
  elite=`[PUSH:-9 PUSH:1 PUSH:-9 PUSH:2]`, carried_match=0.
- I-line confirms native generation:
  `I eval=1510 niche=17570 len=4 score=0 prog=[PUSH:-9 PUSH:1 PUSH:-9 PUSH:2]`
- No carried program at 17570. R5 poisoning eliminated.

**T0/T2 regressions:** Both SOLVE. T0 solution byte-identical to v2.
T0 slightly faster than v2 (37,086 vs 39,082 evals).

### v3-selection-only (SEL=1, CARRY=0) - diagnostic - 1 run

| Task | Verdict | Evals |
|------|---------|-------|
| T0 | SOLVE | 37,086 |
| T1 (P-VM) | FAIL | 1,000,000 |
| T2 | SOLVE | 230,711 |
| T3 parity | SOLVE | 165,976 |

**T3 details:**
- Solved at eval 165,976 with
  `[PUSH:-9 PUSH:-9 IN1 PUSH:-1 IN0 MUL SUB MUL ADD NEG ADD PUSH:2 MOD]`
  (12 ops), held-out 39/39.
- CARRY_BLOCK_CHECK: niche 17570 occupied=1,
  elite=`[PUSH:-9 PUSH:-9 IN0 PUSH:9]`, carried_match=1.
- NO I-line for 17570: the elite came from carry insertion (poisoning present).
- Despite poisoning, T3 SOLVED via alternative route (parent niche 55352).

**Prereg prediction was WRONG.** Predicted "selection-only T3 FAIL (R5 wall)".
Observed SOLVE. The v3 selection schedule routes around the poisoned niche.

### v3-carry-only (SEL=0, CARRY=1) - diagnostic - 1 run

| Task | Verdict | Evals |
|------|---------|-------|
| T0 | SOLVE | 39,082 |
| T1 (P-VM) | FAIL | 1,000,000 |
| T2 | SOLVE | 192,357 |
| T3 parity | FAIL | 1,000,000 (best `[PUSH:9 IN1 IN0 SUB MOD]`, 24/39) |

**T3 details:**
- CARRY_BLOCK_CHECK: niche 17570 occupied=1,
  elite=`[PUSH:-9 PUSH:-9 PUSH:-9 PUSH:2]`, carried_match=1.
- I-line present at eval 4384: native generation (coincidental byte-match
  with a carried program; carried programs never enter archive under
  CARRY_MODE=1).
- Prereg prediction CORRECT: carry-only FAILS (R4 dilution unaddressed).

## Interpretation

**Fix 1 (v3 selection schedule) is NECESSARY and SUFFICIENT for T3 SOLVE.**
- v3-both: SOLVE. Selection-only: SOLVE. Carry-only: FAIL. v2: FAIL.
- The deterministic four-source schedule (nursery 4/8, score bands 1/8,
  uniform 1/8, seed pool 2/8) cures the R4 dilution: new niches receive
  enough selection pressure to assemble the 144-alignment chain.
- Even with R5 poisoning present (selection-only), the schedule finds an
  alternative route. The poisoning is real but no longer fatal.

**Fix 2 (carry seed pool) is NOT strictly necessary for T3, but it is cleaner.**
- It prevents carried programs from occupying archive niches (v3-both:
  carried_match=0; selection-only: carried_match=1 with poisoning).
- Adopt as hygiene: carried experience should seed search, not squat niches.

**Prereg prediction error (selection-only):** The review hypothesized the R5
wall would block selection-only. It did not. The v3 selection is more robust
than predicted. This is reported as a prediction miss, not a bar failure
(K2 governs v3-both only).

## Scope

Bounded L2 (per prereg section 6). The v3 mechanism improves selection and
retention discipline within MAP-Elites. It does not invent representations,
and the solutions are found by deterministic search over a fixed template
set. Not L3. No L3 claim is made.

## ONE-SYSTEM RULE accounting

Per the 2026-09-30 standing directive, capability-source delta:
- Cognition source lines added: ~180 (nursery, score bands, seed pool,
  scheduled selection, CARRY_BLOCK_CHECK observer).
- New hardcoded semantic cases: 0 (no task-specific or parity-specific code).
- New modes: 2 (SEL_MODE, CARRY_MODE) as experimental ablation switches only;
  the claim config is v3-both. These are not cognitive modes.
- New bridges/handlers: 0.
- Learner-state structures created: nursery ring, 17 score bands, 17 seed
  bands (all mechanism-internal scheduling state, not learner-authored
  semantics).
- Verdict: bounded-L2 mechanism repair. The selection schedule is the key
  innovation; the carry seed pool is hygiene. Neither is learner-authored
  structure.

## Artifacts

- `hyp_d_v3.zag`: v3-both source (committed).
- `BUILD_V3.sh`: builds all three configurations (pure shell + znc).
- `ANALYZE_V3.sh`: extracts verdicts from raw logs (pure shell).
- `HYPD_V3_RAW_1.txt`, `HYPD_V3_RAW_2.txt`, `HYPD_V3_RAW_3.txt`:
  v3-both 3/3 (byte-identical).
- `HYPD_V3_SELDONLY_RAW.txt`: selection-only diagnostic.
- `HYPD_V3_CARRYONLY_RAW.txt`: carry-only diagnostic.
- `hyp_d_v3_bin`, `hyp_d_v3_selonly_bin`, `hyp_d_v3_carryonly_bin`: binaries.

## Conclusion

**HYPD-V3-PASS.** The v3 mechanism (both fixes) solves T3 parity 3/3 with
clean CARRY_BLOCK_CHECK, meeting all K2 bars. The ablation refines the
causal story: the v3 selection schedule is the critical fix (necessary and
sufficient); the carry seed pool prevents archive poisoning but is not
strictly required for T3. The prereg's selection-only prediction was wrong
and is reported as such. Scope remains bounded L2.
