# F1 SEALED SEED-SENSITIVITY VERDICT (orphan branch record)

Date recorded: 2026-10-03. Recorder: ORPHAN-EXECUTE (maintenance worker; claim minting paused).
Source branch: `lane-f1-20261002-0821pdt` (tip `655c8d7d6`, local only, never pushed).
Triage reference: `../orphan_triage/ORPHAN_TRIAGE.md` (DOCUMENT-THEN-DELETE, verdict previously captured nowhere).

## What this was

The clean pure-Zag re-freeze and re-run of the wave-20261002-0521pdt F1 seed-sensitivity battery, which went PROCESS-FAIL under the worker toolchain guard after a single no-op python3 invocation. Per governance (no de-minimis exception), every measurement from the 0521pdt lane is quarantined; this lane reproduces the battery cleanly with fresh sealed fixtures and a fresh frozen prereg. The sealed5 fixtures and run outputs from the quarantined lane were not reused; the frozen constructor binary is hash-pinned, so reusing the identical verified binary is not reuse of quarantined science.

Governing prereg: `PREREG_SEEDSENS_REFREEZE.md`, frozen alone at commit `7eb914323` before any methodology, fixture, or run artifact existed in this lane.

All 1577 lane files live under `docs/lab/rsi/runs/wave-20261002-0821pdt/F1/` on the branch. The verdict itself is `SEED_SENSITIVITY_REFREEZE.md` in that directory; this file records its substance so the verdict survives branch deletion.

## Candidate claim (new constructor finding, not a verdict change)

Greedy-trial seed-sensitivity is a constructor property with measured magnitude X: the F1 greedy depth-1 trial constructor exhibits seed-dependent trial outcomes on the sum2 family on a fresh sealed battery. This is a finding about the constructor, not a promotion, not an L3 claim, not a repair, and not a second attempt at the failed 10-percent claim.

Prior verdicts stand untouched:
- F1 (wave-20261002-0221pdt) BUILD-PASS on POLICY-C.
- F1-FOLLOWUP (wave-20261002-0221pdt) BUILD-FAIL on the 10-percent floor claim (R = 3/40 missed the frozen floor).

## Execution record

- Binary hash-verified: `f1_learn` sha256 `6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847` (matches frozen sha; read-only, never modified by any lane).
- Toolchain guard Step 0: safebin activated and verified before any other work; `which python3` empty throughout; all work pure Zag compiled by the pinned znc.
- Methodology committed at `ae9036bf5` (dev sources + pinned-znc binaries + run scripts) after the frozen prereg and before any fixture generation.
- NC-HARNESS: PASS. Generator copy regenerated prior Part 2 fixtures i = 0..5 byte-identically (cmp); 3/3 byte-identical reruns; hidden accuracies matched known outcomes exactly (i in {2,3,5}: 5/30, 0/30, 2/30; i in {0,1,4}: 30/30); hidden preds byte-identical to the prior lane's runs2/1 preds.
- Sealed fixture manifest committed at `86cbc3a73` before any sealed run (40 sum2 worlds, 55xx series, seeds 5500+2i train / 5501+2i hidden, all entering every denominator).
- K-DET: PASS. All 40 seeds completed with 3/3 byte-identical reruns (cmp-verified); DETERMINISM_SHA256.txt written.

## Measured magnitude X

- N = 40, R = 13, T = 2, D_ops = 9, Cmax_ops = 15.
- Overfit rate: 13/40 = 0.325 on this fresh battery.
- Structural concentration: 15/40 = 0.375 on the largest shared op/operand path.
- Pooled overfit rate across unquarantined sealed batteries (prior Part 2: 6/24; 0221pdt: 3/40; this lane: 13/40): 22/104 = 0.212. The rate moves across batteries (0.25, 0.075, 0.325); it is reported, never reified as the constructor's rate.

## Frozen kill bars

- K-SS-TRIAL (T >= 2): PASS. T = 2 distinct first-trial classes (ADD_X0_X0, ADD_X1_X1). The constructor does not always build the same first trial across seeds.
- K-SS-OVERFIT (R >= 1 AND white-box compounding check): PASS. R = 13. White-box check on raw train traces:
  - Seed 0 (acc 0/30): `CONSTRUCT 1 0 op=ADD p1=0 p2=9 p3=9 err_before=14 err_after=6` then `CONSTRUCT 1 1 op=ADD p1=0 p2=0 p3=9 err_before=6 err_after=2`. The id=1 trial strictly reduces buffer error (6 -> 2) while re-adding X1 (register 9, already consumed by id=0) to the accumulator, compounding the incorrect partial law R0 = 3*X1 instead of 2*(X0+X1).
  - Seed 5 (acc 0/30): `CONSTRUCT 1 0 op=ADD p1=0 p2=8 p3=8 err_before=14 err_after=4` then `CONSTRUCT 1 1 op=ADD p1=0 p2=0 p3=8 err_before=4 err_after=1`. Same compounding signature with X0 (register 8).
  Both show a trial that strictly reduces seed-driven buffer error yet compounds an incorrect partial law, exactly the documented greedy-compounding failure mode.
- K-SS-CONV (D_ops >= 2 AND Cmax_ops <= 32): PASS. D_ops = 9 distinct structural convergence paths; no single path taken on more than 80 percent of seeds (largest share 15/40 = 37.5 percent).

## Verdict

FINDING CONFIRMED. The constructor finding is filed: greedy-trial seed-sensitivity is a constructor property of the F1 greedy depth-1 trial constructor with measured magnitude X = (0.325 overfit rate, 2 first-trial classes, 9 structural paths, 0.375 structural concentration) on a fresh sealed 55xx battery. No promotion, no L3 claim, no change to any prior verdict.

## Builder report

BUILD-PASS (coordinator-run lane; the 0521pdt lane is PROCESS-FAIL and quarantined; this lane is a clean re-freeze and re-run with no toolchain violations).

## Architecture accounting

0 cognition-substrate source lines added; no file outside this lane touched; the 2321pdt F1 lane and the frozen constructor binary are read-only. New hardcoded semantic cases 0; new modes 0; new bridges 0; new routers 0; new task-specific handlers 0.

## Record status

This verdict was not in the canonical CLAIM_LEDGER.md (main ledger ends at C376) and not in any retained wave archive; it existed only on the orphan branch. Recorded here per the DOCUMENT-THEN-DELETE triage recommendation. The 1577 evidence files (sealed fixtures, runs, dev sources, analysis) remain unmerged on the branch; the verdict above stands without them.
