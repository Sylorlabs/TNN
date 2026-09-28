# RUNLOG — R1-CROSS (D-family distillation, Track 5 cross-check)

Crew: R1-CROSS (independent cross-check, Type C independent re-derivation).
Scope doc: `docs/lab/crossref/SCOPE.md` @ frozen prereg commit.
Frozen prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch `tnn-native-lab`).
Family: R1 — D-family distillation (Track 5).

Rules in force:
- Clean clone into `~/workspace/scratch-crossref/R1/clean-cross/repo` — never `/home/hatch/workspace/tnn-lab`.
- Evidence pins frozen from the branch before any run; pins recorded below.
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Pure Zag for reasoning/verification (Python glue only). Zero RNG.
- All heavy work in `~/workspace/scratch-crossref/R1/`; TMPDIR=/home/hatch/workspace/tmp_commit; never /tmp.
- Slices < 2^25 bytes; never commit binaries/.zagd.
- Non-interference with other workstreams; zero trust in R1-PRIMARY code/outputs (its scratch not read).

## Log

### 2026-09-22 15:56 PDT — environment setup
- Created `~/workspace/scratch-crossref/R1/{clean-cross,cross}`.
- Verified znc binary present and responding (`--help` OK).
- Started fresh clone: `git clone --branch tnn-native-lab --single-branch https://github.com/sylorlabs/TNN.git` into `clean-cross/repo`.

### Verification plan (per frozen task)
Claims to re-derive (family R1, Track 5 D-family distillation):
1. B (learned-only) mastery 0.9911 > A (planted) 0.6552; C (hybrid) 0.9893 as control.
2. K-T3 fired; K-Q1 fired; K-Q2 never fired (0 transcription errors).
3. D2 0.9911 vs D1 0.6551.
4. Learned-teacher end-state == planted-teacher end-state (byte-identical digests).
5. Teacher noise legs 10%/25%/50% fully absorbed — no knee.
Method: Type C — independent Zag re-derivation.
- Independent Zag: read committed result/ledger files from the frozen branch, recompute
  mastery = correct/total from committed per-item records, recompute SHA-256 digests of
  committed end-state artifacts, re-apply the frozen K-bar rule texts to committed
  records. Never reuse the original crews' Zag; my code lives in cross/r1check/.
- Tolerance: mastery ±0.005 vs committed; digests byte-exact.
- ≥3 byte-identical runs of each verification binary where applicable.
Verdict rule: REPRODUCED iff every claim re-derives; else NOT REPRODUCED naming the failure.

### 2026-09-22 ~16:00 PDT — frozen pin + evidence freeze
- Clean clone into `~/workspace/scratch-crossref/R1/clean-cross/repo` completed (59,534 files).
- `git checkout --detach 7b2100d09911c5c10252c5756c7def288e70bd1f` — HEAD verified == frozen pin.
- Frozen pin SHA: `7b2100d09911c5c10252c5756c7def288e70bd1f` ("crossref: scope + frozen preregs").
- Read `docs/lab/crossref/SCOPE.md` and family R1 section of `docs/lab/crossref/PREREG_TIER1.md`.
- Committed claim sources identified:
  - A/B/C composites + K-T3: `docs/lab/wave12/track5-binding/analysis/TRACK5_VERDICT_SHEET.md` (evidence `track5-binding/evidence/logs/`, 75 configs x 2 runs, SHA256SUMS.txt).
  - D1/D2 + K-Q1/K-Q2: `docs/lab/wave12/q2-distillation/Q2_DISTILLATION_VERDICT.md` (evidence `q2-distillation/evidence/logs/`).
  - Learned-teacher == planted-teacher end-states: `docs/lab/q1b-teacher-bakeoff/Q1B_TEACHER_BAKEOFF_VERDICT.md` (evidence `q1b-teacher-bakeoff/evidence/`).
  - Noise legs 10/25/50%: `docs/lab/q1n-noisy-teacher/Q1N_NOISY10_VERDICT.md`, `docs/lab/tq-noisy25/TQ_NOISY25_VERDICT.md`, `docs/lab/q1tq-noisy50/Q1TQ_NOISY50_VERDICT.md`.

### 2026-09-22 ~16:10 PDT — frozen evidence pins (tree SHAs)

| Path | tree SHA |
|---|---|
| `docs/lab/wave12/track5-binding/evidence/logs` | `ec89a683762d62d929001d4d08fdd3eba7f561e9` |
| `docs/lab/wave12/q2-distillation/evidence/logs` | `dbe58e6a6bb19a03c4ea606eef6cc5cb34c29081` |
| `docs/lab/wave12/q2-distillation/corpus` | `f1150160733f9770ad795c094e914ad2c5fafbc8` |
| `docs/lab/q1b-teacher-bakeoff/evidence` | `d8e34ba711cf3acf47a1070c271d4e65e22fda7c` |
| `docs/lab/q1n-noisy-teacher/evidence` | `1a6ca9c81c09e28a0ebaf3cde31f839f1724e50b` |
| `docs/lab/tq-noisy25/evidence` | `8c0f7d2f720f68001a801de6463e844ed7ffbb81` |
| `docs/lab/q1tq-noisy50/evidence` | `aec083beb796f53d541ca11fc4a2c6e05c9dd37e` |
| `docs/lab/wave12/track5-binding/analysis` | `39af3556e57fdebd58180a939bcdfc6cbb22d8c5` |
| `docs/lab/wave12/q2-distillation/analysis` | `001b047585ba0a6ff2516e77e859e8619aa2038a` |
| `docs/lab/wave12/track5-binding/prereg` | `ebb9eeee84e63a98dcd03d5c4be698e554c918c9` |
| `docs/lab/wave12/q2-distillation/prereg` | `9525031860c296206cc59557908acecccead9869` |
| `docs/lab/crossref` | `7791b9b452b11378b4fea715a5411f5dd9c48c1f` |

Evidence inventory found in the frozen clone:
- track5 logs: 139 files (bind_X/Z/D trap pairs; `btrap_Y_*.run1.log` absent — 63 configs
  with both runs, not 75). domain hash `7cd0baf8…3f92ee8` in all 36 bind logs.
- q2 logs: 100 files (50 configs × 2 runs, complete). corpus.json 91,487 bytes,
  sha256 `42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada`.
- q1b / q1n / tq25 / q1tq50 evidence dirs: each `run1_stdout.txt`, `per_slice.csv`,
  `n5_sha256.txt`.

### 2026-09-22 16:30–18:32 PDT — independent verifier sources

Wrote independent Zag verifiers in `cross/r1check/` from the frozen prereg rule
texts and the evidence files' observable formats only (R1-PRIMARY scratch never
read). Common substrate copied: `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`.
- `r1c.zag` — file I/O, metric/digest-line extraction, rational metric parser,
  integer micro-unit arithmetic, SHA-256 hex, tiny JSON. Metric definitions per
  prereg: mastery=mean(d1,d2,d3); revisability=min(rev_false,rev_genuine);
  integrity=mean(applicable trap fracs,1−hallu,k1,k2,refusal); retention=min(1,r3/r2);
  cost=1/(1+esc/eps·100+0.1·ops/eps); composite=30/25/25/10/10.
- `r1_t5.zag` — Track 5 A/B/C metrics, gates, K-T3, SHA256SUMS chain.
- `r1_q2.zag` — Q2 D1/D2 metrics, gates, K-Q1, corpus error re-derivation, K-Q2,
  SHA256SUMS chain.
- `r1_q1b.zag` — Q1B digest equality, per-slice tables, n5 hash chain.
- `r1_noise.zag` — noise 10/25/50 counts, fractions, mastery, §B.7 battery, no-knee.
- `probe.zag`, `dbg.zag`, `dbg2.zag` — format-exploration probes, not evidence.

SHA-256 substrate smoke test: sha256("abc") =
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` ✓.

Arm identification done empirically from the logs (no label trust): sealed label
with revisability 0.0 → A; label with nonzero `explanted` → C; remainder → B.

### 2026-09-22 18:32 PDT — builds (pinned znc, TMPDIR set)

- `znc r1check/r1_t5.zag -o r1check/r1_t5` →
  `0b03aaf17b93d28ef5b99c8f84d9f314a825bd44baabc08e0453a59bb36a4788`
- `znc r1check/r1_q2.zag -o r1check/r1_q2` →
  `ab8029c44cd28c27a27f368e46dd200daec976b0af7ba917bf962d20c4403567`
- `znc r1check/r1_q1b.zag -o r1check/r1_q1b` →
  `55357a66288105ed538887a1eb30c90cd800497f74aec7ba90b699a44e776adb`
- `znc r1check/r1_noise.zag -o r1check/r1_noise` →
  `1a7a99ccadb0567d6a8b6da416c3e66fa79e5212cae44dc3dedc5e5be03af901`
- znc toolchain sha256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.

### 2026-09-22 18:33 PDT — verification runs (3× each, byte-identical)

| verifier | output sha256 (all 3 runs identical) | result |
|---|---|---|
| r1_t5 | `85c4a735b85d2f17f83283ccc3d3be07d2f21f9e93c946a09f4da9a8eec5f9b7` | PASS |
| r1_q2 | `93ef2e42391fc5bc9991b0600aefff85a2c7e3b0035024e73c8b21b5108f8636` | PASS |
| r1_q1b | `b6fa66d28fe7e151b287fa0aa98399eff290a3bada1f0165dd4c62bc7ad06aa0` | PASS |
| r1_noise | `2dafa828de017baa05aeba73dd33f2ead131b394a5232561238bb2038dac0fd1` | PASS |

Raw outputs: `cross/runs/` (`t5_{1,2,3}.txt`, `q2_{1,2,3}.txt`, `q1b_{1,2,3}.txt`,
`noise_{1,2,3}.txt`).

Track 5: X(B) comp 0.9910 vs 0.9911; Y(C) comp 0.9893 vs 0.9893; Z(A) comp 0.6552
vs 0.6552. All metrics within ±0.005 (max Δ 0.0001, fixed-point truncation).
K-T3 FIRED (|ΔM|=0.0000, ΔRv=1.0000, max_C−B=0.0000). Gates 0 failures 36/36.
SHA256SUMS 139/139; 63/63 committed run-pairs hash-equal. S10 m/rv equal S1 rep0.

Q2: D2 comp 0.9910 vs 0.9911; D1 comp 0.6551 vs 0.6551. K-Q1 FIRED (D2 gate pass,
ΔRv=1.0000, ΔM=0.0000). Corpus re-derivation: 240 input_claims parsed; E_dump=0,
E_obs=0, E_prb=0, inconsistent=0, CAUGHT_ERR=0; corpus sha256 matches recorded;
ERROR_INVENTORY.md and embedded inventory all n=0. K-Q2 never fired. SHA256SUMS
100/100; 50/50 run-pairs hash-equal.

Q1B: both legs' learner digests equal
`6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`;
teacher digests differ; each digest matches across both committed runs;
per_slice 16/16 rows, 96/96 battery + 192/192 mastery per leg; n5 5 identical
hashes = committed `407974c3…0151`.

Noise: 10% → 23/228 (10.09%), absorbed 19, filtered 0, untaught 4, mastery
173/192, battery 96/96; 25% → 59/228 (25.88%), absorbed 49, filtered 0, mastery
143/192, battery 96/96; 50% → 118/228 (51.75%), absorbed 99, filtered 0,
untaught 19, mastery 93/192, battery 96/96. No-knee: absorbed==taught-false at
all levels. All match committed numbers exactly.

### 2026-09-22 18:33 PDT — verdict

**REPRODUCED.** Every committed headline bar/verdict re-derived within the
preregistered tolerance; every committed byte-identical digest matched exactly;
K-T3 and K-Q1 FIRED and K-Q2 never fired under the frozen rules. Verdict written
to `cross/VERDICT.md` with full committed-vs-derived tables, all frozen pin
SHAs, and the recorded caveats:
- T5 committed evidence is 63/75 run-pairs (12 `btrap_Y` .run1.log files
  absent) — the coordinator's "75/75" determinism statement is overstated
  against the committed record; supporting statement only, no headline bar
  affected.
- Verifier prints fixed-point truncated values (max Δ 0.0001 vs committed).
- Committed record holds digest strings, not raw learner-state bytes; the
  end-state equality is verified via (a) both legs' recorded digests equal,
  (b) each digest identical across both committed runs, (c) 5-run hash chain
  identical.

Composite-vs-mastery note (preserved per task): the headline 0.9911 / 0.9893 /
0.6552 are the 30/25/25/10/10 composites; actual mastery is 1.0000 on all arms —
the composites encode revisability/cost differences, not capability differences.
