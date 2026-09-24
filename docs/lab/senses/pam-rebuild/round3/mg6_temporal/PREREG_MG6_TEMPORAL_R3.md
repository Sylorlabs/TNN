# Preregistration — MG6 temporal-arm recalibration on stream geometry (Round 3, Crew 2)

Status: PROPOSED (awaiting build; prereg-alone commit precedes any build output).
Date: 2026-09-24 (PDT).

## §1. Question

The frozen D1 defense-stack verdict (Round 2) KILLED MG6 on two kill bars:
KB-D1a (0 false installs — PASS, 0 observed) and KB-D1b (≥26/34 true retention — FAIL, 0/34 observed).
The frozen CC1 guard verdict KILLED MG6 on throughput only (5/5 held; safety 0/9 false).

The user-required outcome for this round: recalibrate or replace MG6's **temporal arm**,
do NOT abandon the guard (the margin arm is proven), and test each candidate against
the frozen D1 stack battery (0 false installs AND ≥26/34 true retention) plus the
frozen CC1 MG6 battery (0/9 false installs, 5/5 throughput held).

## §2. Frozen sources (extracted by script, never memory)

| Artifact | Source | Pin |
|---|---|---|
| CC1 prereg | git object store | `a673da8aa9481194992a38963eb7b99074fe1f5e` |
| CC1 build/verdict/EXPECT | git object store | `dfe3d49f6d6be7ea99c3740320e475e667ec77b0` |
| D1 stack prereg | git object store (lazy-fetched) | `2b3a485fca5a1ce0953f8db243f976f398cd1cd9` |
| D1 stack build/verdict/EXPECT/evidence | local lab tree (build commit `7e4fb3a4` not in object store) | `~/workspace/tnn-lab/docs/lab/senses/pam-rebuild/round2/d1_stack/` |

Workdir copies (byte-verified against the frozen sources by the extraction scripts):
- `frozen_gen_guard.py` — the frozen CC1 `gen_guard.py` (cell table + 22-cell battery).
- `frozen_PREREG_CC1_GUARD.md` — the frozen CC1 guard prereg text.
- `frozen_stack_records.zag` — the frozen D1 `stack_records.zag` (trial/gatt init-functions).
- `frozen_EXPECT_D1.tsv`, `frozen_EXPECT_D1_CELL.tsv` — the frozen D1 expected tables.
- `/tmp/guard_main_frozen.zag` — the frozen CC1 `guard_main.zag` (build note: /tmp is scratch).

The D1 battery's 758 trials were re-parsed from `stack_records.zag` and the leg-3
sub-battery rows were diffed against the frozen CC1 generator rows: exact match (PASS).
The gatt recomputation reproduces 750/758 tags; the 8 mismatches are the frozen
spoofed-decoy trials (expected; they must NOT verify).

## §3. The frozen MG6 rule and the two batteries

MG6 (frozen): on a G1 gate proposal (stored, incoming) with corroborator margins
(mrg_s, mrg_t), corroborator spans (sa_s,sb_s),(sa_t,sb_t), and seqs (sq_s,sq_t):
veto iff (a) min(mrg_s,mrg_t) < 400 (margin arm), OR
(b) spans overlap: sa_s < sb_t AND sa_t < sb_s (span arm), OR
(c) |sq_s − sq_t| < 20 (temporal arm).
A vetoed proposal reverts to PROVISIONAL (PERM) / CHALLENGER (REV); no install.

D1 battery: 16 streams, 758 trials; G1 gate → MG6 guard → H6 hardening (R1–R4);
scored legs 1–4; kill bars KB-D1a (0 false installs anywhere) and KB-D1b (≥26/34
true retention on the 34 leg-1 withhold true candidates).

CC1 battery: 22 cells (9 scored CC1 variants + 13 observational W/V probes);
G1 gate → MG6 guard at the REV-formation point only; no H6; kill bars 0/9 false
installs and 5/5 throughput on the correct revisions. V9 is an unscored ceiling probe.

## §4. Candidate slate (exact, frozen by this prereg)

All candidates keep the margin arm (min mrgF ≥ 400) and the span arm (disjoint)
EXACTLY as frozen. Only the temporal arm (c) is replaced. A candidate's temporal
arm FIRES (vetoes) iff its stated condition fails; detail string `guard-veto:temporal`
covers every temporal-arm firing (pair-Δseq or set-statistic).

- **T0** — frozen MG6 control: temporal arm = |sq_s − sq_t| ≥ 20.
- **T1** — temporal arm REMOVED (margin ∧ span only). Included to isolate the
  temporal arm's exact contribution; it is NOT abandoning the guard (margin+span
  remain). Expected: the safest replacement, but insufficient retention.
- **T2lo** — temporal arm = |sq_s − sq_t| ≥ 2.
- **T2hi** — temporal arm = |sq_s − sq_t| ≥ 6.
- **T3** — corroborator-set temporal RANGE: let C be the set of distinct seqs of
  all trials in the stream history with the same (tcode, jcode) as the pair,
  plus the pair's own seqs. Temporal arm = (max(C) − min(C)) ≥ 20.
  (20 reuses the frozen MG4 corroboration-window constant; not tuned.)
- **T4** — corroborator-set MASS: with C as above, temporal arm = |C| ≥ 3.

Unscored ceiling probe (NOT a candidate; the task forbids abandoning the guard):
**TX** — allow-all guard (no vetoes). Preregistered to bound the maximum true
retention any guard can achieve under the frozen gate.

Constants 2/6/20/3 are preregistered and are not tuned after results are seen.

## §5. Preregistered ceiling analysis (the retention bar is unrecoverable at the guard layer)

Before any candidate was run, the validated Python mirror of the frozen battery
was used to establish the following structural facts (all derived from the frozen
inputs, §7):

1. Under frozen MG6, the G1 gate forms only FOUR true proposals among the 34 true
   leg-1 candidates (indices 4, 18, 26, 37); the other 30 never reach the guard
   because of gate re-anchoring (prov slot moves on when |Δmeas| > tol).
2. Under the allow-all probe TX (no guard at all), the full D1 stack installs
   exactly THREE true leg-1 trials (indices 4, 18, 37) and zero false.
   Therefore NO guard — however recalibrated — can exceed 3/34 true retention
   under the frozen gate + H6. KB-D1b (≥26/34) is UNREACHABLE by temporal-arm
   recalibration. The bottleneck is the GATE's proposal formation, not the guard.
3. The seven leg-1 proposals that ever form under frozen MG6 are, with their
   pair-Δseq and margins (hand-verified against `stack_records.zag`):

   | idx | seq | truth | Δseq | margins | T0 veto arm |
   |---:|---:|:---:|---:|:---|---|
   | 4 | 25 | true PERM | 5 | 60202/58070 | temporal |
   | 18 | 77 | true REV | 1 | 5000/4999 | temporal |
   | 19 | 78 | false PERM | 6 | 1958/1888 | temporal |
   | 22 | 83 | false PERM | 3 | 2320/2373 | temporal |
   | 25 | 86 | false PERM | 1 | 2024/1915 | temporal |
   | 26 | 87 | true REV | 3 | 4999/4999 | temporal |
   | 37 | 110 | true PERM | 2 | 138/142 | margin+temporal |

   The temporal arm is the SOLE veto on six of seven proposals (idx 37 also fails
   margin). True and false proposals are PAIR-INDISTINGUISHABLE on (Δseq,
   margins, spans): e.g. true idx 26 (Δseq 3) vs false idx 22 (Δseq 3).
   No Δseq threshold separates them.

4. Path-dependence (preregistered, hand-verified in §7): under permissive
   candidates, a true install RESETS the gate (prov=−1) and preempts later false
   proposals in the same tcode. T1/T4's 0-false/1-false outcomes depend on this
   ordering; a different trial order could change them. This is documented, not
   hidden.

Consequence: EVERY candidate is expected to be KILLED on KB-D1b (see §8), and
the experiment's deliverable is the precise safety/retention tradeoff of each
temporal replacement plus the proof that recovery requires gate-level retuning.

## §6. Batteries and run plan (pure Zag, zero randomness)

- **D1 battery (r3_main.zag)**: the frozen `stack_main.zag` with the guard
  section parameterized by candidate (argv: stream, candidate). One invocation
  processes one stream under all six candidates (gate state reset per candidate).
  Output: `R3|cand|stream|trial_idx|seq|disp|install|detail` per trial.
  16 streams × 3 runs = 48 invocations; 758 trials × 6 candidates per run.
  Trial/gatt tables are the frozen `stack_records.zag` reused VERBATIM
  (byte-identical copy); no regenerated fixtures.
- **CC1 battery (r3_cc1.zag)**: the frozen `guard_main.zag` with the guard
  parameterized by candidate, same six candidates. 22 cells × 3 runs.
  Cell table regenerated by the frozen `gen_guard.py`; byte-identity with the
  frozen `guard_records.zag` is verified before use.
- Three complete runs of each battery; byte-identical output required.
- Scoring: `score_r3.py` compares run outputs against EXPECT_R3*.tsv
  (byte-exact line match) AND independently recomputes kill-bar verdicts
  (false-install counts, retention, throughput) from the run output.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Commits via `TMPDIR=~/workspace/tmp_commit ~/workspace/commit_racefree.py`
  with lab-relative paths. No binaries, no `.zagd` in commits.

## §7. Kill bars (frozen for this round)

- **KB-R3a**: ANY false install through the full D1 stack (legs 1–4, any
  candidate) → KILL the candidate.
- **KB-R3b**: leg-1 true retention < 26/34 → KILL the candidate.
- **KB-R3c**: CC1 battery — ANY false install on the 9 scored CC1 variants
  OR correct-revision throughput < 5/5 → KILL the candidate.
- A candidate SURVIVES iff it passes KB-R3a AND KB-R3b AND KB-R3c.

## §8. Preregistered expectations (from the validated mirror; the Zag runs must reproduce them)

The Python mirror was validated BEFORE expectations were frozen:
D1 mirror(T0) reproduces frozen EXPECT_D1.tsv 758/758; CC1 mirror(T0) reproduces
frozen EXPECT_GUARD.tsv's MG6 column 79/79. The mirror is hand-verified on every
install trial listed below (gate proposal formation, guard arm arithmetic,
H6 R1–R4), including the path-dependent preemptions.

D1 battery expectations per candidate:

| cand | false installs (D1) | true retention | KB-R3a | KB-R3b |
|---|---|---|---|---|
| T0 | 0 | 0/34 | PASS | **FAIL** |
| T1 | 0 | 2/34 (idx 4, 18) | PASS | **FAIL** |
| T2lo | 1 (idx 19, false PERM) | 2/34 (idx 4 T, 19 F, 26 T) | **FAIL** | **FAIL** |
| T2hi | 1 (idx 19, false PERM) | 0/34 | **FAIL** | **FAIL** |
| T3 | 0 | 1/34 (idx 4) | PASS | **FAIL** |
| T4 | 1 (idx 22, false PERM) | 2/34 (idx 4 T, 22 F, 26 T) | **FAIL** | **FAIL** |

Key hand-verified mechanics behind the table:
- T1 idx 18 (true REV, pair Δseq 1) installs; the install resets t4's gate, so
  the false PERM proposals at idx 19/22/25 never form (they become chal/reanchor
  instead). T1's safety is order-dependent (§5.4).
- T2lo/T2hi admit idx 19 (false PERM, Δseq 6 ≥ threshold); the false install
  then resets the gate and a LATER true REV (idx 26) revises over it — the false
  install still counts under KB-R3a.
- T3 admits only idx 4 (t3-HIGHER C-range 25 ≥ 20); all t4 proposals veto
  (C-range 1–14 < 20). idx 37 vetoed by margin (138 < 400) under every candidate.
- T4 admits idx 22 (false PERM) because the sustained RICH run built |C|=4 ≥ 3 —
  historical mass backfires against a persistent attacker.
- T2hi/T3/T4 veto idx 18 (the true REV), so they retain fewer true trials than T1.
- No candidate (and not even TX) recovers idx 26's true REV except via the
  path-dependent revision-after-false-install; TX installs 4, 18, 37 only.

CC1 battery expectations per candidate:

| cand | false (9 scored) | throughput | KB-R3c |
|---|---|---|---|
| T0 | 0/9 | 5/5 | PASS (reproduces frozen) |
| T1 | 0/9 | 5/5 | PASS |
| T2lo | 0/9 | 5/5 | PASS |
| T2hi | 0/9 | 5/5 | PASS |
| T3 | 0/9 | 5/5 | PASS |
| T4 | 0/9 | 0/5 | **FAIL** |

Rationale: in the scored CC1 family the temporal arm is never the sole veto
(margin and/or span already veto all 8 wrong proposals that form; V3 forms no
corroboration), and all 5 correct pairs pass every replacement (Δseq 68–427;
C-range ≥ 68; |C| ≥ 2 — but T4 needs |C| ≥ 3 and a CC1 cell holds exactly 2
same-judgment trials, so T4 vetoes all 5 correct revisions).

Preregistered verdicts: **ALL SIX CANDIDATES KILLED.** T0/T1/T3 on KB-R3b;
T2lo/T2hi on KB-R3a (+KB-R3b); T4 on KB-R3a (+KB-R3b) and KB-R3c.
Best local tradeoff: T1 (0 false D1, 0/9 false CC1, 5/5 throughput, 2/34) —
reported as the safest temporal replacement, still KILLED under the frozen bar.

## §9. Determinism and purity

- Pure Zag. Zero RNG in generators, batteries, and scorer. No timestamps, no
  PIDs, no map iteration in any output path.
- EXPECT_R3.tsv / EXPECT_R3_CELL.tsv / EXPECT_R3_CC1.tsv are generated by
  `gen_r3.py` from the validated mirror (deterministic; dict iteration only over
  insertion-ordered stream lists).
- The Zag runs must be byte-identical across 3 runs AND byte-identical to the
  EXPECT tables (modulo the run-header, if any — none planned).

## §10. Honest limits

- This round tests GUARD-layer recalibration only. §5 proves the frozen D1
  retention bar cannot be recovered at this layer; recovering it requires
  gate-level retuning (proposal formation), which is OUT OF SCOPE and is the
  recommended follow-up, not a conclusion smuggled in here.
- T1/T4 safety is path-dependent (§5.4): the battery's fixed trial order is part
  of the frozen input; a reordered battery could change the false-install
  counts. The verdicts apply to the frozen battery as specified.
- The D1 build commit `7e4fb3a4` is absent from the git object store; the frozen
  D1 artifacts used here are the complete local lab-tree copies, verified
  758/758 against EXPECT_D1.tsv by the mirror.
- CC1's V9 remains an unscored observational ceiling, as frozen.

## §11. Artifacts in this (prereg-alone) commit

- `PREREG_MG6_TEMPORAL_R3.md` (this file)
- `gen_r3.py` — deterministic generator: re-parses frozen inputs, runs the
  validated mirror for all six candidates, emits EXPECT_R3*.tsv; copies the
  frozen `stack_records.zag` byte-verbatim; regenerates `guard_records.zag`
  via the frozen generator and asserts byte-identity.
- `EXPECT_R3.tsv` — per (candidate, stream, trial): disp, install
- `EXPECT_R3_CELL.tsv` — per (candidate, stream): installs, false installs
- `EXPECT_R3_CC1.tsv` — per (candidate, cell, trial): disp
- `sweep_guards.py`, `sweep_cc1.py`, `analyze_geometry.py`, `trace_leg1.py`,
  `set_stats.py` — the validated mirror and hand-verification scripts
  (supporting evidence for §8; frozen at prereg time)

Build artifacts (`src/r3_main.zag`, `src/r3_cc1.zag`, `score_r3.py`, evidence/,
RUNLOG, VERDICT) come in a LATER commit, only after this prereg-alone commit
lands.
