# M2 adversarial-heap differential — verdict
Date: 2026-09-25. Evidence root: `evidence/m2/`.
Frozen inputs: `PREREG_GATE_EXPANSION.md`, `M2_HEAP_DIFFERENTIAL.md`.

## Method (frozen)

- Pinned compiler `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
- Audit allocator wraps every target binary with 6 dirt patterns
  (D0 `00`, D1 `FF`, D2 `AA`, D3 `55`, D4 offset-counter, D5 `DE AD BE EF`)
  × 3 environment shapes (E0 empty, E1 1KB pad, E2 64KB pad) = 18 runs.
- `argv[0]` length varies across runs (M2-ARGV).
- Instruction-counted busy-wait (550,000,000 iterations) between runs 9,10.
- Driver: `build/driver/m2_driver`
  (SHA-256 `4461a02298204f0c27dac1171d3e3a6996908b988a044ddfa924f335948dc032`).
- Layout proof: `build/proof/layout_proof` PASS (SHA-256
  `df9aad3bb72e8ace113c1cc4f77986413695262f6042e79579374181a818d2ca`),
  record in `doc/LAYOUT_PROOF.md`.

## Results (3 complete schedule rounds, runs/r1 r2 r3)

| module | r1 | r2 | r3 | divergent runs (r1) | first-diff byte |
|---|---|---|---|---|---|
| p01_getrandom | FAIL | FAIL | FAIL | 1–17 | 9 |
| p02_clock | FAIL | FAIL | FAIL | 1–17 | 9 |
| p03_urandom | FAIL | FAIL | FAIL | 1–17 | 9 |
| p04_uninit | FAIL | FAIL | FAIL | 3–17 (D1+) | 9 |
| p05_envflag | FAIL | FAIL | FAIL | 1,4,7,10,13,16 (=E1 runs) | 10 |
| p06_aslr | FAIL | FAIL | FAIL | 1–5,7–14,16,17 | 9 |
| p07_rdtsc | FAIL | FAIL | FAIL | 1–17 | 9 |
| p08_hashorder | PASS | PASS | PASS | — | — |
| p09_innocent_tables | PASS | PASS | PASS | — | — |
| p10_machineid | PASS | PASS | PASS | — (out-of-scope) | — |
| p11_argv | FAIL | FAIL | FAIL | 1–17 | 6 |
| p12_invoke_discard | PASS | PASS | PASS | — (out-of-scope) | — |
| c01_clean | PASS | PASS | PASS | — | — |
| c02_phrasing | PASS | PASS | PASS | — | — |
| c03_seeded | PASS | PASS | PASS | — | — |
| c04_fileio | PASS | PASS | PASS | — | — |
| c05_instrcount | PASS | PASS | PASS | — | — |
| c06_fixedmap | PASS | PASS | PASS | — | — |

Notes:
- p05 diverges exactly on the six E1 (1KB-pad) runs — the environment
  instrument isolates as designed.
- p06's divergent-run set varies slightly round to round (ASLR noise in
  the low address byte); the verdict is stable FAIL in all 3 rounds.
- All verdicts stable across r1/r2/r3 (no cross-round instability).

## Kill-bar evaluation

- **K-CATCH: 9/10.** 8/8 dirty plants caught (P01–P07, P11); P09 innocent
  tables correctly PASSes (counts as correctly classified); P10/P12
  out-of-scope and excluded. The single miss is **P08 hash-order**, the
  frozen pre-registered AT-RISK case (§3 predicted it "may miss"; §5
  "hash map iteration" known hard problem). The miss is real: P08's
  fixed-order fully-initialized map produces byte-identical output under
  every dirt pattern — the differential heap cannot see it. Counted
  honestly per the frozen "AT-RISK counts normally" rule.
- **K-DET: 6/6.** All six clean controls byte-identical across 3 complete
  schedule rounds (driver schedule reports identical byte-for-byte).
  Dirty modules' per-round outputs vary by design (true nondeterminism);
  their verdicts are stable.
- **Controls:** C01, C02, C04, C05, C06 PASS; C03 PASS (fixed seed).
- **Expected-outcome check:** zero mismatches vs the frozen expectations
  (including the predicted P08 AT-RISK outcome).

## Honest limitations (methodological)

1. M2 flags anything whose OUTPUT is dirt-sensitive, including
   deterministic-but-dirt-coupled formatting (two latent zero-fill
   dependencies were found and repaired during build: `nio_cstr` in the
   substrate and `print_hex` in the K2′ plants — see doc/).
2. P08 demonstrates the hard limit: a fixed-order, fully-initialized
   structure is invisible to heap-dirt differential analysis.
3. P09's exact v3 artifact was not locally present; the tested P09 is a
   disclosed structural twin rebuilt from the v1 plant18 description.
4. The driver treats identical outputs as PASS even if all 18 runs crash
   identically (class recorded; verdict compares output hashes only).
   No module exercised this path in the final battery (all binaries ran
   clean, rc=0).

## Verdict

M2 achieves K-CATCH 9/10 and K-DET 6/6. The single K-CATCH miss is the
pre-registered AT-RISK case P08. All frozen expectations met; zero
deviations from the expected outcome table.

Per-module 18-run hash tables: `runs/r1/`, `runs/r2/`, `runs/r3/`
(driver logs). Build/source SHAs recorded in this file's Method section.
Coverage: 18 modules × 18 runs × 3 rounds = 972 target executions.
