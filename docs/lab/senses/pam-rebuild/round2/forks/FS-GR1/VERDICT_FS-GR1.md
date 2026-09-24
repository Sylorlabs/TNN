# VERDICT_FS-GR1 — 2026-09-24

Gate-redesign crew FS-GR1, PAM rebuild round 2. Frozen prereg: `6d23b45ca9d045492d8fbe4733061ee378dddb2b` (branch fs-gr1).

## Battery

- Pinned manifests: adv `f4f85194c4ee0cf157f7b155881a2c0797041beb5e2ee03bfb4ee7b70512e7a2`, ctrl `64798b244f90ddeaffe695ed4a43e361dbb397037da5595671c611cb01f6d22d`.
- File-level verification: 12000/12000 SHA-256 ok. Not redrawn.

## Redesigns (frozen in prereg, implemented in pure Zag)

- **CH-MOT-3**: ±8 search, boundary rejection (|bx|=8 or |by|=8 → skip), informativeness gate s_best/median < 0.4, strict-majority (>50%) decisive-evidence rule, else UNRESOLVED. No blur.
- **CH-TBD-3**: 2^20 coefficients (2065924/1973170/1821652), /32 input downscale, overflow-safe power, THEORY mapping (d1→BRIGHT, d3→RICH).

## Results (frozen battery, 2× byte-identical, hash chains verified)

### Adversarial FI

| Task | FI / n | FI rate | Wilson 95% UCB |
|---|---:|---:|---:|
| colordisc | 0/2330 | 0.0000% | 0.1646% |
| colorconst | 0/1380 | 0.0000% | 0.2776% |
| shapetrans | 0/2345 | 0.0000% | 0.1636% |
| pitchdisc | 0/2330 | 0.0000% | 0.1646% |
| timbredisc | 0/985 | 0.0000% | 0.3885% |
| motiondir | 1/630 | 0.1587% | 0.8936% |
| pooled | 1/10000 | 0.0100% | — |

### Control recall

| Task | Recall |
|---|---:|
| colordisc | 566/600 = 94.3333% |
| colorconst | 492/500 = 98.4000% |
| shapetrans | 259/300 = 86.3333% |
| pitchdisc | 193/200 = 96.5000% |
| timbredisc | 200/200 = 100.0000% |
| motiondir | 157/200 = 78.5000% |
| pooled | 1867/2000 = 93.3500% |

### Bars

1. **Motiondir FI UCB ≤1%**: 1/630, UCB=0.8936% — **PASS** (was 7/630, UCB 2.2756%).
2. **Timbredisc recall ≥85%**: 200/200 = 100% — **PASS** (was 25%).
3. **No-regression** (other four):
   - colordisc: FI 0% (≤1%) OK; recall 94.33% (≥91.00%) OK.
   - colorconst: FI 0% (≤1%) OK; recall 98.40% (≥97.40%) OK.
   - shapetrans: FI 0% (≤1%) OK; recall 86.33% (≥85.3333%) OK.
   - pitchdisc: FI 0% (≤1%) OK; recall 96.50% (≥92.50%) OK.
   — **PASS**.
4. **Byte-identical ×2**: formation TSV, gate raw, ledger all IDENTICAL x2 — **PASS**.
5. **Hash-chain verification**: all chains OK — **PASS**.
6. **No battery redraw, no post-freeze mechanism edits**: held — **PASS**.

## Determinism

- Eval driver: `run_eval_fsgr1.py` ran adv (n=10000) and ctrl (n=2000) twice.
- All stages byte-identical: formation TSV IDENTICAL x2, gate raw IDENTICAL x2, ledger IDENTICAL x2.
- Hash chains verified line-by-line.

## FINAL: ALIVE

All frozen bars pass. The gate redesigns eliminate the diagnosed defects:
- Motiondir: 7→1 FIs (UCB 2.28%→0.89%), via informativeness gating and decisive-evidence requirement.
- Timbredisc: 25%→100% recall, via corrected 2^20 front end and theory mapping.
- No regressions on the other four tasks.
