# B6 evidence — determinism and ledger verification

## Stateless determinism (3 full sweeps)

- `evidence/runs/h1_run{1,2,3}.jsonl` — 1165 fixtures each, every fixture's
  full stdout SHA-256 compared across all three runs: **1165/1165 identical**.
- Binary (test-only, not committed): `build/h1`,
  SHA-256 `a5f54c81c42842e5d0cf0563615a73196f2a6b41af404007d97711bb5c0b6b61`.
- Built from frozen `src/h1.zag` with the pinned znc toolchain; three builds
  (incl. one after a VM reboot) were byte-identical.

## Adversarial stream ledgers (12 streams, 850 entries)

Each of the 6 tasks × 2 modes (gate / --ablate) ran the misleading fixtures
(sorted, store reset, unique stream ID `B4_<task>_<mode>`) through the memory
contract. Every resulting ledger chain was re-verified with an independent
from-scratch Python SHA-256 checker (`eval/eval_h1.py ledger-verify`) that
recomputes each entry's hash over the exact stored field layout:

- colordisc gate 70/70 valid, ablate 70/70 valid
- colorconst gate 50/50 valid, ablate 50/50 valid
- shapetrans gate 90/90 valid, ablate 90/90 valid
- pitchdisc gate 70/70 valid, ablate 70/70 valid
- timbredisc gate 70/70 valid, ablate 70/70 valid
- motiondir gate 75/75 valid, ablate 75/75 valid

**850/850 entries valid, 12/12 chains valid.** Stream result JSONLs are in
`evidence/streams/<task>_{gate,ablate}.jsonl`; per-mode store dirs
`evidence/streams/work_<task>_<mode>/` contain the ledger files.

## B4/B5 stream summary (425 misleading fixtures)

- Disposition differs gate-vs-ablate: **160/425 = 37.6%** (bar ≥10% ✓)
- Gate false installs: **118** < ablate false installs: **224** (strictly lower ✓)
- Gate false-install rate: **118/265 = 44.53%** (kill bar: ≤5% ✗)
- Gate correct-install recall: **73.13%** (kill bar: ≥85% ✗)

## Scale (prereg §3 prerequisite)

- Total event records: **9,486** (requirement ≥10,000 — MISSED by 5.1%)
- Misleading records: **3,298 / 9,486 = 34.8%** (requirement ≥30% — PASS)

## Baseline fidelity note

The Approach A binary was rebuilt from frozen `a_raw/sense.zag` after a VM
reboot wiped the test-only build. Verified 108/108 (judgments, confidence,
ops, harness-normalized stdout SHA) against the frozen harness's own
`raw_results.json`. The harness's single recorded error (A, shapetrans
adversarial p042.img, `task_failed`) is reproduced identically by the rebuild
and excluded from scoring exactly as the frozen harness excludes it
(`run.py` files error records under "errors", never in "runs").
