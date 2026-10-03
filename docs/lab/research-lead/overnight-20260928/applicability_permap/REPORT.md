# REPORT.md: Per-Candidate (Per-MAP) Applicability

## Verdict: APPLICABILITY-PERMAP-COMPLETE (P1-P8 all PASS)

Per frozen PREREG (commit 1403e0b57, 2026-10-02):
"Verdict APPLICABILITY-PERMAP-COMPLETE requires P1-P8 all PASS. Any bar
failed: verdict is FAIL with the bar named, no reinterpretation."

All eight bars pass. The per-candidate gate recovers the win the
problem-level gate left on the table: after the C0 burn it identifies the
C0-promoted plen-4 MAP as reusable at 1 try each on C1..C5, for a C-block
total of 10, beating both the problem-level gate (49) and naive blind
search (59).

## Transfer matrix (verify-tries per problem; lower is better)

| Domain | PERMAP (per-candidate gate) | TREAT (problem gate) | NAIVE (no gate) | FRESH (no Phase1) |
|--------|---------------------------|---------------------|-----------------|-------------------|
| A' (related) | 1,1,1,1,1 (total 5) | 1,1,1,1,1 (total 5) | 1,1,1,1,1 (total 5) | 6,1,1,1,1 (total 10) |
| B (irrelevant) | 1,1,1,1,1 (total 5) | 1,1,1,1,1 (total 5) | 11,11,1,1,1 (total 25) | 1,1,1,1,1 (total 5) |
| C (misleading) | 5,1,1,1,1,1 (total 10) | 29,4,4,4,4,4 (total 49) | 29,26,1,1,1,1 (total 59) | 24,4,4,4,4,4 (total 44) |

All values measured 3/3 byte-identical (SHA-256 below). The three control
arms reproduce the frozen rerun values exactly, including byte-identical
run-output hashes, so the comparison is valid.

## Kill bars (frozen 2026-10-02)

- P1 C-block recovery: PERMAP_C=10 < TREAT_C=49 AND < NAIVE_C=59. PASS.
  (Also < FRESH_C=44.)
- P2 per-candidate identification: C1..C5 each total=1 with rb=1 and
  trial=0; the log shows the attempted candidate has plen=4 on each of
  C1..C5 (winplen=4, one CAND line `plen=4 gate=1 tried=1 ok=1` per
  problem); per-shape replay on saved C0 features under final weights:
  plen-5 gate=0, plen-4 gate=1, plen-3 gate=0. PASS.
- P3 A' no false negatives: PERMAP_A'=5; plen-5 attempted on all 5
  (each AP problem: gate=1, tried=1, winplen=5). PASS.
- P4 B neutral: PERMAP_B=5 <= 10; plen-5 never attempted on B (20 CAND
  lines on B0..B4, all `plen=5 gate=0 tried=0`; the 4 attempted
  candidates are plen-3, each `tried=1 ok=1`). PASS.
- P5 C0 burn bounded: PERMAP_C0=5 < 29. PASS.
- P6 determinism: 3/3 byte-identical runs per arm. PERMAP
  27b8d456cca9aae5fcd1c9a432fa86e6f03f663bed9f52da467edbc88b08c773;
  TREAT
  030fd9b50e423592e05682edcf485646d9c83bf1bc5916ff046b1be9ad449993
  (matches frozen rerun); FRESH
  afe2fff8dc5982ed93e621180822825d51d438d029d8ded75e3e20c0ffadee0d
  (matches frozen rerun and 2026-10-01); NAIVE
  97645756adead29e9d1fdc192c0a7e314ac0ae59d7d497799d06aa6050c3130f
  (matches frozen rerun). PASS.
- P7 process: pure Zag, safebin PATH, `which python3 python` empty at
  session start and re-checked after the runs. PASS.
- P8 architecture: 0 new modes/bridges/handlers; no researcher domain
  labels (features are gathered-path structure plus query relation;
  the shape key is rb_chain_plen computed from graph structure);
  researcher-owned: feature list, sim formula, 15-point margin, ETA=25,
  cap 800, optimism threshold 3, shape-partition rule, uniform priors;
  learner-owned: all weights, all records, all per-candidate decisions.
  PASS.

## What the per-candidate gate does (mechanism evidence)

The CAND log lines make the per-candidate judgments auditable:

- C-P0 (q=16): 4 plen-3 candidates skipped (`gate=0`), first plen-5
  candidate attempted (`gate=1 tried=1 ok=0`), the remaining 9 plen-5
  skipped (the single failure record at C features drives avf to 100),
  last plen-3 skipped. tried=1, skipped=14. Trial then costs 4 and
  promotes the plen-4 MAP. Total 5. The gate learns within the problem:
  one exploratory burn per shape, not 25.
- C-P1 (q=17): 10 plen-5 skipped, 5 plen-3 skipped, the single plen-4
  candidate (the C0-promoted MAP, 0 records so the optimistic rule
  fires) attempted: `plen=4 gate=1 tried=1 ok=1`. Total 1.
- C-P2..C-P5: the newest linked plen-4 MAP is tried first and succeeds;
  tried=1, skipped=0 each. Total 1 each.
- B-P0..B-P4: every plen-5 candidate `gate=0` (the shape's A/A' success
  records are too dissimilar to B features: avs<=14.3 < 15); plen-3
  candidates attempted optimistically then on accumulating success
  records, 1 try each. Total 5.
- A-P1..AP-P4: plen-5 candidates attempted on shape success records,
  1 try each. Total 5.

Weight trace: w_cx moves 100->150 on the C0 plen-5 failure (same
consequence-driven update as the problem gate), then freezes; later
successes find the C0 failure record at distance 0 and add nothing.
The learned weights, not record counts, drive the rejections (plen-5
replay gate=0 with avf=100 vs avs=14.3 under final weights).

## Why this beats both baselines on C

- vs the problem-level gate (49): the problem gate conflates "rebind of
  prior structures failed" with "no reuse possible" and pays trial cost 4
  on each of C1..C5. The per-candidate gate partitions consequences by
  candidate shape, so the plen-5/plen-3 failures on C features vote only
  against plen-5/plen-3, while the plen-4 shape keeps its clean record
  and is reused at 1 try each. It also shortens the C0 burn itself
  (5 vs 29) by refusing the 2nd..Nth same-shape attempt inside the burn.
- vs naive (59): naive pays 25 failed rebinds on C0 and 25 more on C1
  before the C0-promoted MAP surfaces by blind order. The per-candidate
  gate pays 1 failed rebind on C0 and goes straight to the plen-4 MAP
  on C1.

## Honest boundaries

- The C0 exploratory burn is not eliminated (optimism under 3 records
  per shape is by design, preregistered). The gate does not prevent the
  first misleading attempt of a shape.
- Shape is an exact-match partition on rb_chain_plen. Two MAPs of the
  same shape share one consequence history; ordering among them stays
  recency/id order. Per-identity records would be a further refinement;
  shape was chosen because rebind itself matches candidates to paths by
  exact plen, and because a MAP id is an allocation index, not an
  observable structural feature.
- The per-shape gate is still a gate over the same reuse operation; it
  adds no new cognitive subsystem, mode, bridge, or handler. This is L2
  structural learning (consequence-driven per-shape weight/record
  adaptation), not L3 representational invention.
- Control-arm output hashes match the frozen rerun hashes byte for byte,
  confirming the setup reproduced the rerun before the new arm was
  compared. (Note: the rerun REPORT's K7 hashes are run-output hashes,
  not binary hashes; the rebuilt control binaries are byte-identical to
  the rerun's binaries on disk.)

## Determinism

3 runs per arm, byte-identical outputs, SHA-256 recorded above.

## Files

- `ma_base.zag`: verbatim copy of the rerun's unfrozen base (with the
  t2 reclaim fix). Diffed against the rerun copy: identical.
- `ma_patch.zag`, `ma_driver.zag`: verbatim rerun copies for the
  TREAT/NAIVE/FRESH control arms. Diffed: identical.
- `ma_patch_permap.zag`: APPL-PERMAP (per-candidate gate). New.
- `ma_driver_pm.zag`: permap driver (4096-byte AP, 32-byte ST,
  per-shape replay). Problem sequence verbatim; only AP/ST/replay/stat
  differ (diff verified).
- `build.sh`: 4-arm stamp/compile flow.
- `pm_full_*.zag`: concatenated build inputs.
- `pm_*_bin`: compiled binaries.
- `run_*_{1,2,3}.txt`: 12 run outputs, byte-identical per arm.
- `permap/treat/fresh/naive_compile.txt`: build logs.
- `PREREG.md`: frozen preregistration (commit 1403e0b57, before
  implementation).
- `NAMECHECK.md`: toolchain guard, ordering, verdict rule.

## Architecture accounting

Cognition lines added: the per-candidate gate (~150 lines of Zag in
`ma_patch_permap.zag`, mostly the shape-partitioned record accessors
and per-candidate loop). New hardcoded semantic cases: 0. New modes /
bridges / handlers: 0. New learner-state structures: the 64-record
shape-keyed consequence table (extends the existing APPL record layout;
same 8 features, same weight rule). Capability-source delta: the C-block
win comes from learner-owned per-shape records and decisions, not from
researcher-authored domain knowledge.
