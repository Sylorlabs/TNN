# STEP 2 results — measured per-episode audit cost (2026-09-20)

Gating measurement for Track 4 (slice 20 §6). All numbers measured, not
modeled. Runner: `run_step2.sh` — 35/35 checks pass (log: run_step2.log).

## Verdict: GO — K1 did NOT fire

Slice 20's K1 bar: measured audit bytes/episode at 1x exceeding 4 KiB for any
curriculum falsifies the cost model. **Maximum measured over 600 dry-run
episodes (3 harnesses × 200): 768 B — 5.3× under the 4 KiB cap.** The cost
model survives. The 1 KiB nominal is conservative: measured medians are
256 / 256 / 448 B, i.e. the model overestimates typical episodes by 2–4×.
Per slice 20 §3, the 10x budgets below scale from the measured medians.

## Measured histograms (bytes/episode; 1 entry = 64 B)

| harness | n | median | min | max | p90 | mean | >1024 B |
|---|---|---|---|---|---|---|---|
| code | 200 | 256 | 192 | 768 | 512 | 321 | 0 |
| english | 200 | 256 | 256 | 640 | 448 | 312 | 0 |
| messy | 200 | 448 | 320 | 768 | 512 | 455 | 0 |

Byte distributions (episodes):

- code: 192B×57, 256B×57, 320B×11, 384B×24, 448B×25, 512B×15, 576B×4, 640B×4, 704B×2, 768B×1
- english: 256B×121, 320B×20, 384B×36, 448B×15, 512B×3, 576B×4, 640B×1
- messy: 320B×40, 384B×40, 448B×40, 512B×61, 640B×7, 768B×12

Op-class mix, totals over 200 episodes
(order: add, revise, manage, kill, deliberation, verify, governance, trust-tier, other):

- code: 200, 29, 22, 49, 703, 0, 0, 0, 0 (total 1003 entries)
- english: 200, 40, 20, 24, 691, 0, 0, 0, 0 (total 975 entries)
- messy: 200, 0, 0, 19, 643, 0, 0, 560, 0 (total 1422 entries)

Reading the mix: every episode in all harnesses = 1 deliberate add + 1
trace/binding review record + 1 post-change-verification record
(st_replay_check + st_audit_clean_refusals, read-only, logged as JUSTIFY;
verify_fail = 0 on all 600 episodes). Code episodes add near-miss
counterexamples (ep%3), fault-localization elimination records (ep%5),
deliberate revisions (49 evidenced kills, all gates passed, kill_fail = 0),
strength re-judgments and promotions. English episodes add disambiguating
evidence per binding and gavagai-ambiguity strengthens. Messy episodes are
trust-tier heavy: 560 TT_OP-family entries (2.8/episode) — CITE rings, ORIGIN
tags, T0_T1_HOLD hold/release paths, CHANNEL_DISTRUSTED — matching the slice-20
model's "0–5 trust-tier ops (MRC)" term. `other` class = 0 everywhere: every
appended op fell in a known class. No ROLLBACK entries: no post-change
verification ever found a defect worth rolling back in the dry runs.

## Calibrated 10x budgets (from measured medians, per slice 20 §3)

- Code 10x (39,500 eps × 256 B): **≈10 MB** (model said 39.5 MB nominal)
- English 10x (34,000 × 256 B): **≈8.7 MB** (model said 34 MB)
- Messy 10x (90,000 × 448 B): **≈40 MB** (model said 90 MB)
- 10x program total: **≈59 MB** vs 170 MB nominal / 675 MB at the 4 KiB cap.
  At p90 bytes: ≈81 MB. 100x code leg (395,000 × 256 B): ≈101 MB — no
  2^25-slice pressure (chunked replay already validated).

## Method notes and honest caveats

- Counter: `hist.zag` scans the append-only ledger between per-episode
  `audit_n` markers; the append path is untouched and `st_memory_core.zag` is
  vendored byte-identical to wave10/debate-norecord (cmp-checked in-run).
  Every EP line independently re-verified from the transcript: bytes ==
  entries×64 and class counts sum to entries on all 600 lines.
- Determinism: each harness run twice with identical args; transcripts
  byte-identical (cmp). Zero RNG (static-grepped).
- One setup op per run (ST_OP_SETSTAGE, 64 B, opening the stage gate) sits
  OUTSIDE the episode windows and is not counted — real pilots have setup too;
  it does not affect per-episode K1.
- Representativeness limits (PREREG_STEP2.md §4): these are minimal dry runs,
  not the curricula. Real episodes could run hotter where the specs demand
  volume: fault-localization elimination records scale with suspect count,
  trust-tier CITE rings scale with source count, adversarial classes 3–5 are
  not yet exercised. The measured numbers calibrate the 1x pilot budgets; if a
  real pilot's traffic shape differs, re-measure — do not re-model.
- K1 was evaluated at 1x dry-run scale per the prereg. The 10x legs inherit
  slice 20's C1 bar (audit bytes/episode at 10x > 2× measured 1x median,
  sustained over a full leg → the arm is re-preregistered smaller).

## Artifacts

- `PREREG_STEP2.md` — frozen prereg (committed pre-build as a7f50a8d)
- `hist.zag` — the counter module; `harness.zag` — the three dry-run harnesses
- `st_memory_core.zag`, `substrate/` — vendored substrate (byte-identical)
- `run_step2.sh`, `run_step2.log` — runner and its 35/35 log
- `run_code_a.txt`, `run_english_a.txt`, `run_messy_a.txt` — measurement transcripts
