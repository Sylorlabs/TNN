# VERDICT.md — ARM X (Degenerate, CTRL)

## VERDICT: PASS

ARM X completed the 1x battery as the honest null arm. All 18 legs ran
with rc=0, byte-identical double runs, no FATALs. M8 determinism gate
PASSED (5 perturbations × 2 reruns, all artifacts byte-identical).

### Kill criterion A-44 (verbatim)

**"Floor bars (A-44): retired as candidate only if B2 ≥10× AND B5 ≥10×
(crew-4 battery). Universal floor rule text frozen at sign-off. If it
fires, the arm is KILLED — write the death certificate with evidence and
commit it. Dead arms die in public."**

**Status: DID NOT FIRE.** B2 and B5 are Crew-4 battery metrics. X's M1–M9
results alone cannot prove another arm is ≥10× better on both. No
M1–M9→B2/B5 mapping was invented. No death certificate required.
The arm lives.

## 1x Scorecard (M1–M9)

| Metric | Result |
|---|---|
| M1 prose | recall 100.0, boundary 0.0 (1 unit) |
| M1 code | recall 100.0, boundary 0.0 (1 unit) |
| M1 ID probe | N/A (no ID layer) |
| M2 T1/T2/T3 | etc 50+ censored, ep0 0.0, final 100.0, boundary 0.0 |
| M9 shape | fast-then-flat (takeoff 1, steepness 100.0, late 0.0) |
| M3 | survival 100.0, fresh 100.0, 7050 mgmt, 50/50 weaken, CLEAR, valuable 2 |
| M4 prose/code | rev_boundary 100.0, rev_content 100.0, kill 0.0, killsub false, 1 ep |
| M5 | 2 units, 5.45MB source, 1800B slots, 0 evicted; 2.002 B/B (FAIL vs 1.5 bar, expected null); 0.188 audit/KB (PASS) |
| M6 p2c/c2p | recall 100.0, boundary 0.0, revision 100.0, tax 0.0 |
| M6 memorizer gate | p2c drop 54.8 (PASS ≥15) |
| M7 | N/A; reread 2.7GB (500 full-stream scans, informational) |
| M8 | M8GATE PASS |

Full JSON: `scorecard_r1_1x.json`.

## 10x Status

**NOT RUN.** The 10x conditional ("run only after all 1x bars pass") is not
met: M1 boundary is 0.0 by frozen design (M-3), against a 100.0 bar. X is
the null control; the boundary "failure" is the mechanism, not a defect.

## Ambiguities logged (literal readings implemented)

1. **M-3:** boundary 0.0 by design for whole-stream blobs.
2. **A18:** M3 valuable set = 2 (all whole-stream units that exist).
3. **M3/M4 schedule collapse:** fixed-index selections hit the same monolith.
4. **M7:** 500 lookups (not 5000); each scans 5.4MB with no index.
5. **A-44:** B2/B5 unmapped; criterion cannot fire from M1–M9 alone.
6. **10x tiling:** frozen build_10x.py tiles without separators; not run.

## Reproducibility

- Frozen compiler: `toolchain/bin/znc_linux_x86_64_abed8aa1`
- Frozen prereg commit: `b0b9140c0eda`
- All legs: double-run byte-identical (see `logs/*/STATUS.txt`).
- M8: 10/10 runs byte-identical (see `logs/m8/GATE.txt`).
- Zero RNG in AI decision paths.
