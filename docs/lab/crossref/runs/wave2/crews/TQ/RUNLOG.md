# T2-TQ RUNLOG — replacement crew (2026-09-22/23 PDT)

Crew: T2-TQ (REPLACEMENT). Predecessor crew was killed mid-run by a runtime
daemon restart (~2026-09-22 night). This log records inherited state, resume
decisions, frozen pins, and every step taken by the replacement crew.

## 0. Inherited state (found 2026-09-23 ~04:30 PDT)

- `~/workspace/scratch-crossref/T2/TQ/clean/` — git repo, working tree at
  `dbabd53e9ef0266f56a26bda217ac2acb4fc84bc` (NOT the frozen commit), with a
  stale `.git/index.lock` (predecessor's git process crashed mid-checkout),
  and 35k+ files showing as deleted in `git status` (working tree partially
  wiped by the interrupted checkout).
- `~/workspace/scratch-crossref/T2/TQ/crew/` — empty (predecessor wrote
  nothing there).
- `~/workspace/scratch-crossref/T2/TQ/frozen.tar.gz` — 33,423,360 bytes,
  timestamped 04:18. **CORRUPT**: `gzip -t` fails with "unexpected end of
  file"; `file` reports a bogus original size (2994765359). Not used.
- `git fsck --full` on clean/: clean, one dangling commit
  (`3edd14867296d73bfc0606227c3770127157e22e`). No corruption.
- The frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f` exists as an
  object in clean/'s store (`git cat-file -t` → commit).

## 1. Resume decision

Re-clone was unnecessary: the frozen commit's full object graph is present
locally. Removed the stale `.git/index.lock`. A `git checkout -f` of the
frozen commit was attempted but wedged under I/O contention (~34 orphan
`git clone` processes from the daemon restart, other crews', saturating disk;
new exec sessions timing out for ~40 min). The background checkout was
SIGTERM'd after ~16 min with no progress (HEAD still dbabd53).

Pivot (recorded here): instead of fighting for a full working-tree checkout,
all inputs were extracted **directly from the frozen commit's object store**
with `git show <frozen>:<path>` — byte-verified against the tree. The
prereg's Type-A requirement is "rerun ... from committed sources"; the
extracted files are exactly the committed sources, spot-verified by SHA-256.

## 2. Frozen pins (frozen before running)

| Pin | Value |
|---|---|
| Frozen prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch tnn-native-lab, verified as object in clean/) |
| TQ-CONFLICT commit (expected `107f6ca1`) | `107f6ca108fbe9a6bf30a8c22dd168b798a8f791` — PRESENT. `git log -1`: "Q1C teacher self-contradiction leg: PASS — 17/17 false assertions killed (R1), 0 withheld, learner end-state byte-identical to Q1B" |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`, `znc 2026.07.0-dev (edition 2026)` |
| TMPDIR | `~/workspace/tmp_commit` (never /tmp) |

The expected TQ-CONFLICT pin `107f6ca1` HOLDS → no STOP.

## 3. Prereg extraction (from frozen commit, object store)

Read `docs/lab/crossref/PREREG_TIER2.md` §"T2-TQ" verbatim from
`7b2100d09911c5c10252c5756c7def288e70bd1f` (quoted in full in VERDICT.md).
Leg sources located in the frozen tree:

- TQ-CONFLICT → `docs/lab/q1c-teacher-conflict/` (driver `src/q1c_driver.zag`)
- TQ-NOISY25 → `docs/lab/tq-noisy25/` (driver `src/tqn_driver.zag`)
- TQ-NOISY50 → `docs/lab/q1tq-noisy50/` (driver `src/q1tq_driver.zag`)
- TQ-NOISY10 → `docs/lab/q1n-noisy-teacher/` — PRESENT in tree, **EXCLUDED**
  per frozen prereg ("run1 complete (verdict pending — excluded)"). Not run.
- Q1B control → `docs/lab/q1b-teacher-bakeoff/` (driver `src/q1b_driver.zag`)

## 4. Source extraction

`git archive` hung (same I/O episode); extracted file-by-file with
`git show`. 77 files total across the 4 leg dirs:
q1b 17/17, q1c 24/24, tqn25 18/18, tqn50 18/18 (counts match `git ls-tree`).
Spot-verified: all 4 driver files byte-identical (SHA-256) to the frozen
tree blobs.

## 5. Builds (pinned znc, from each leg's `src/` dir, `--no-analyze`)

- `q1b_driver.zag` → `crew/bin/q1b` (239,239 bytes main; analyzer lint
  warnings only — A0102 unused-return notes, no errors)
- `q1c_driver.zag` → `crew/bin/q1c`
- `tqn_driver.zag` → `crew/bin/tqn25`
- `q1tq_driver.zag` → `crew/bin/tqn50`

No `.zagd` caches or binaries committed anywhere. Build binaries kept only
in `crew/bin/` (scratch, never committed).

## 6. Runs (all N=5, stdout captured, zero RNG in decision paths)

| Leg | stdout SHA-256 (×5, byte-identical) | vs committed `evidence/n5_sha256.txt` | run1 vs committed `evidence/run1_stdout.txt` |
|---|---|---|---|
| q1b (control) | `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151` | MATCH | `cmp` → identical |
| q1c (TQ-CONFLICT) | `5f81826a65a73aed7579f8d7dc4d663aa28b92ebca97c6310b70ff72b592532e` | MATCH | identical |
| tqn25 (TQ-NOISY25) | `e8983ac4e3e0b42360442015c45dc51b18267d5753a518c5b79784d337fd63d4` | MATCH | identical |
| tqn50 (TQ-NOISY50) | `7aa4c7861682660723a1423ba015b75d8e0ecf224b64aedc9aaae8bcb6b3a0a3` | MATCH | identical |

All runs rc=0. Run dirs: `crew/runs/{q1b,q1c,tqn25,tqn50}/run{1..5}.txt`.

## 7. Claim-by-claim verification

### Q1C (TQ-CONFLICT)
- `Q1C_P2,<seq>,<fid>,<val>,<verdict>,<reason>`: 17 lines, all
  verdict=3 (`TB_V_REJECT`), reason=1 (`TB_R1_INSUFFICIENT`) — enum decoded
  from `src/q1_types.zag` (TB_V_REJECT=3, TB_R1_INSUFFICIENT=1). **17/17
  REJECTed at R1.** 0 other verdicts.
- `Q1C_PASS2,conflicted,17,0,183,0,0` (17 false assertions killed, 0 other,
  183 true re-assertions R5-redundant).
- `Q1C_WITHHOLD,conflicted,17,0,17,0,0,3,0` (0 withheld, 17 commit-true,
  0 commit-false; 3 never-taught facts trivially absent).
- `Q1C_UNCONFLICTED_MASTERY,conflicted,183,183`.
- `Q1C_DIGEST,conflicted,learner,6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`
  == my independent Q1B control rerun's
  `Q1B_DIGEST,learned,learner,6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`.
  **Byte-identical end state to Q1B.**
- 102 `CL_CHECK,` lines in stdout (all matched; summary records 102/102).
- Teacher digest `6f387ee3e6fddc7692d5138fd4c1106bd745f2ec0a837956196b07c3dee756b5`
  == Q1B learned-teacher digest (unmodified teacher).

### TQ-NOISY25
- `TQN_ABSORB,49,0,49,143,0` = absorbed=49, filtered=0, taught-false=49,
  true-mastery=143, true-bad=0 (field order read from
  `src/tqn_driver.zag:tqn_absorb`). **49/49 absorbed, 0 filtered.**
- §B.7: `TQN_SLICE` × 8 → 12/12 hits, score 120, pass=1, 0 tripwire on all 8
  slices = 96/96.
- Mastery vs world truth: 18,18,18,18,17,18,18,18 = **143/192**;
  vs teacher's claims 192/192 (per verdict; stdout byte-identical to
  committed evidence, whose per_slice.csv shows the same).
- Learner digest `54c32f6f017c800117f0fb5e820ab4a3b964e815525260bd91b81519231bb63f`
  (matches verdict's `54c32f6f…f19231bb63f`; differs from Q1B as expected).
- Untaught false claims: 10 (59 noisy − 49 taught; per verdict accounting,
  stdout byte-identical to committed evidence).

### TQ-NOISY50
- `Q1TQ_ABSORB,noisy50,99,0,19` = **99/99 absorbed, 0 filtered, 19 untaught.**
- §B.7: 96/96 hits (12/12 × 8), 8/8 slices pass, 0 tripwire.
- Mastery vs truth: 12,11,12,12,10,13,12,11 = **93/192**.
- Learner digest `1d56c852877431900ed33020263f30e321a922ed458d9fe7479c9e6b40ee29bd`
  (matches verdict's `1d56c852…ee29bd`; differs from Q1B as expected).

### Curve / knee check
- Absorbed/taught-false: 0% → 0/0, 25% → 49/49, 50% → 99/99. Absorption is
  total at every tested level — linear through the origin, no filtering
  regime anywhere → **no knee**.
- §B.7 flaw battery: 96/96 at 0%, 25%, AND 50% noise — score does not move
  while knowledge corrupts 0% → 25.5% → 51.6%. **Blind to value noise.**

### Static scan
`grep -iE "rand|clock_gettime|gettimeofday|rdtsc|getrandom|_zag_time|wallclock"`
on the six new decision-path files
(q1c_teacher/driver, tqn_teacher/driver, q1tq_noisy/driver): all CLEAN.
Empirical determinism: 5/5 byte-identical runs on all four legs.

## 8. Notes / deviations from plan

1. Predecessor's `frozen.tar.gz` was corrupt; not used. Everything came from
   the frozen commit's object store (byte-verified).
2. Full working-tree checkout was abandoned (I/O wedge from ~34 orphan
   clones); extraction-from-object-store is equivalent-or-cleaner for the
   Type-A requirement and is recorded here rather than hidden.
3. TQ-NOISY10 was NOT rerun (frozen prereg excludes it). Its verdict doc is
   present in the tree; its committed numbers (19/19 at 10%) were not used
   in the knee analysis — the linearity claim rests on 0/25/50 only.
4. "PARTIAL" in the prereg's "TQ-NOISY50/N25/PARTIAL committed": no file or
   commit named PARTIAL exists in the TQ dirs; I read this as the series'
   committed SCOPE-§5 status (the DOC-SWEEP corrections 2026-09-22 propose
   N2/N3/N4 bars — retroactive TRIP under proposed N2, §B.7 citations INVALID
   without the triple under proposed N3 — none frozen/signed, so the
   verdicts' governance status is partial). All preregistered headline bars
   I reran matched, so PARTIAL does not apply to the replication decision.
5. No box commit made by this crew. Deliverables are in the run dir;
   committing VERDICT.md to the crossref box is left to the parent
   (commit races are live tonight; `commit_racefree.py` from
   `~/workspace/tnn-lab` if desired).
