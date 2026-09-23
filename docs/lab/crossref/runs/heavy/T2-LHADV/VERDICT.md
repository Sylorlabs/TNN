# VERDICT — T2-LHADV crossref heavy crew: coding LH-ADV-2 replication

**Verdict: REPRODUCED.** Full rerun of the 54-stage battery with seeded
failures from committed sources in a clean scratch checkout, built with the
pinned toolchain (`znc_linux_x86_64_abed8aa1`, sha prefix
`498abcb5ab346f8cb246222a1ca63699`). **3/3 byte-identical battery runs**;
every run produced a ledger byte-identical to the committed result
(`12487b93756ac66e9b1ec3d0262d8f00b50ccc3a`).

## Numbers

| Check | Result |
|---|---|
| Battery runs | 3/3 byte-identical; each `a97df78e374dec1bb6a350e2c76ab49b14e2fe4a3341140f025908982a1c16dd` = committed REF ledger byte-for-byte |
| Accepted | 52/54 in every run |
| Honest halts | 2/54 in every run: **D9 UNRECOVERABLE** (KB-MISS after quarantine, zero candidates, zero fabrication), **F1 KB-MISS** (unseeded control) — same stages, same reasons as frozen |
| ADV-DS | PASS — 47/47 unseeded ACCEPT, 0 defects |
| ADV-REC | PASS — 6/6 diagnosed; 5/5 recovered ≤1 extra cycle (D6/B7 3 cycles; D5/C7/D8 2 cycles); D9 honestly halted; fabrication=0 |
| ADV-HH | PASS — F1 emits `HALT KB-MISS`; 54/54 terminated |
| ADV-CRIT | PASS — structural: 50 critic fns / 32 emitter / 64 delib, 0 shared symbols beyond `main`, CONTAMINATION_LOG.md present (`audit_critic_indep2.py` AUDIT-PASS); behavioral: **51/51 calibration ACCEPT, 1/1 seeded bug REJECTED** (`CRITIC-REJECT EMITTER-BUG op=substr` on D8), **0 false rejects** |
| ADV-DIAG | PASS — D5→UPSTREAM D4, C7→UPSTREAM C6, D8→LOCAL D8, all from symptom-only evidence; HINT-LEAK audit clean (no evidence names any upstream, no corruption labels) |
| NO-RNG | PASS — no randomness constructs in any `.zag` source or driver |
| NO-SOLUTION | PASS — machinery embeds no contract TEST-out vectors |
| ADV-RET (dedicated rerun) | PASS — 10/10 byte-identical (spec+output+accept), per-stage cycles identical to committed reference |
| ADV-DET (dedicated rerun) | PASS — 5/5 stages × 5 reps byte-identical (spec/source/binary/output) |

**Fabrication: 0.** No seeded failure went undiagnosed. No kill criterion
tripped (no true-upstream hints, no wrong halt reasons, critic rejected the
seeded bug, D9 emitted zero candidates).

**Caveat carried through (unchanged from frozen):** the critic was authored
in-session under clean-room discipline (contamination log + symbol audit),
not by a separate sibling crew. This replication does not re-litigate that;
it re-ran the frozen structural audit and the behavioral calibration, both
PASS.

## Method
- Frozen prereg section verified against the task brief (sha256
  `cb3823ee2bd62bac587e68b7f809e308207898ad4ca00f4525d98b6b14a3b39a`,
  lines 107–111 of `crossref/PREREG_TIER2.md`, sha256
  `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f` —
  byte-identical to the committed blob on `tnn-native-lab`).
- Pinned commits resolved: Part A `e4d666fc20ccb8b0b6b17fe9287794236f6c59ab`,
  prereg `beb00397224ae5ae24df9766ac8f65210d9bab87`,
  result `12487b93756ac66e9b1ec3d0262d8f00b50ccc3a`.
- Clean-checkout: 54/54 contract files byte-match the prereg commit's git
  blobs; all three machinery `.zag` files, `adv2_run.py`, `adv_kb.txt` match
  frozen SHAs; `envelope.json` absent from the prereg commit tree (sealed
  plaintext never committed, as required) with local hash matching the
  commitment `22f6d1142a18ae5db00ea26025ad4908eb9fcd5c548cae3f459524f3bc9cee26`.
- Ran in an isolated scratch copy; original committed artifacts untouched
  until this verdict.

## Anomalies
None. No vanishing-tree event; branch head re-verified before commit.
Early harness-side hiccup (a redirect target dir created one call too
late) cost one no-op attempt; the no-op attempt never executed the driver
(no state touched). No compiler issues; all three binaries built on first
attempt with `--no-analyze --no-zagd`.

## Artifacts committed
`crossref/runs/heavy/T2-LHADV/` — VERDICT.md, RUNLOG.md, ledger2_run1.json,
ledger2_run2.json, ledger2_run3.json (each `a97df78e…`, byte-identical to
the committed trial ledger).
