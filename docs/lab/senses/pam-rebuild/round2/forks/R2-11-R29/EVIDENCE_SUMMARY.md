# R2-11 EVIDENCE SUMMARY (compact, 2026-09-23)

Full run artifacts (954MB) are NOT committed. This file records the
verifiable scores and digests. Binaries (sense_a, sense_b) are NOT committed;
rebuild with the pinned toolchain:
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## Sources

- src/forkA/r2-11a.zag (Fork A, replay-only, R2-9 lineage)
- src/forkB/r2-11b.zag (Fork B, generative-emission, R2-9 lineage)
- R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag (substrate deps, both forks)

## Full battery r1 (11,840 trials, 2 shards x 5,920)

### Fork A r1
- percepts=11,778 failed=114 missing=62 installed=7,469
- B1 primary: 370 trials, acc=0.8622 (PASS)
- B2 delta vs Approach A (0.726): +0.1362
- B5 false installs: 1,427/11,840 = 0.1205 (FAIL)
- B3 percept ops: mean=655,764 max=3,648,000
- B3 artifact bytes: total=347,812,139 (nart=16,645)
- KB-E2: bad_sel_rows=0 empty_artifacts=0
- KB-E1: 16,315 OK, 0 BAD, 47 missing (correctly-skipped degenerate)

### Fork B r1
- percepts=11,778 failed=114 missing=62 installed=7,469
- B1 primary: 370 trials, acc=0.8622 (PASS)
- B2 delta vs Approach A (0.726): +0.1362
- B5 false installs: 1,427/11,840 = 0.1205 (FAIL)
- B3 percept ops: mean=664,781 max=3,660,800
- B3 render ops: mean=23,576 max=102,400
- B3 artifact bytes: total=347,812,139 (nart=16,645)
- KB-E2: bad_sel_rows=0 empty_artifacts=0
- KB-E1: FAIL by design (generative payload; declared, KB-E7 gated)

### A/B comparison
- Judgment/confidence/disposition differences: 0 (shared percept pipeline)
- B5 identical: renderer does not change beliefs.

## Human sample (frozen)

- work/human/sample200u.tsv (200 trials, unique IDs)
- SHA256: 3dc22df12b6e44b6f7d13928151b9cd54d877ca1268f4177999b2974026e5893
- 100 clean (R2N generated normal) + 100 adversarial (17 R2A families)
- Injections: R2A-COL-1, R2A-SHP-1, R2A-MOT-1, R2A-TMB-2 (all present)
- Packages: 197 built (3 failed trials skipped), 0 gate failures
- Key: work/human/key_sealed.tsv (SEALED, not for Micah)
- KB-E7: 288 fork-B artifacts checked, 0 undeclared divergences (PASS)

## Determinism

- B6: r1 complete for both forks. r2/r3 pending at time of commit.
- Ledger hash-chain: verifier passes on r1 (0 breaks).

## Deviations (documented)

1. Pool is 11,840 not 10,000 (frozen manifest arithmetic).
2. Workspace collision 2026-09-23 ~09:20; reconstructed at R2-11-R29/.
3. Harness trial IDs collide; human sample uses unique-ID generated trials.
4. Sample frozen after implementation began (honest timing note).
