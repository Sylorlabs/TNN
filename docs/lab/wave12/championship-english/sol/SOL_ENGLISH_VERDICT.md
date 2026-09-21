# SOL English Box — Verdict (2026-09-21)

**Headline: SOL ENGLISH CHAMPIONSHIP LEGS COMPLETE — class-4 composite 0.9911,
§B.7 96/96, class-3 teacher leg clean on all checks; corpus frozen at
sha256 `41aa8f5b…` with zero withholdings after the batch-18 per-ID
mechanical recovery.**

## 1. Corpus & withhold ruling

The source team left the box blocked at 39/40 captures (batch 18 FATAL,
batch 19 absent). Parent ruling 2026-09-21: batch-18 retry budget exhausted
(no 5th attempt), strict parsing stays, rows parse mechanically per-ID across
preserved attempts; a row unparseable after all attempts becomes a withheld
corpus row (`E_format`).

| Batch | Outcome |
|---|---|
| 19 (ids 228–239) | Captured clean on attempt 1 (gpt-5.6-sol, temp 0, seed 42; raw sha256 `6a6825e8b0b71ea4…`); id 231 reproduces supplied false value `7` (true `8`) |
| 18 (ids 216–227) | No 5th attempt. Per-ID union of preserved attempts: attempt 3 yields ids 216–225 + 222 (raw sha256 `d75a76b6d0a1ff69…`); id 226 is strictly parseable in attempt 3 despite failing attempts 1, 2, and the recovery run (`f0c8a36fa9495b06…`) |

**Withheld IDs: none.** Every id 216–227 has at least one strictly-parseable
raw row, so the `withheld: true` path never triggers; taught scope is
240/240. The withhold machinery (`withheld_ids.json`, `E_format`,
`muse_withheld_at`, teaching-leg withheld skips) is live in all three legs
with `MUSE_WITHHELD_N=0`.

| Corpus item | Value |
|---|---|
| Frozen corpus | `sol/corpus/corpus.json` |
| sha256 | `41aa8f5be15f778034cfce63250233468d364f52b318a02f63a87ac7459015d7` |
| Dump rows / teach rows | 240 / 240 |
| Withheld ids | [] |

## 2. Faithfulness (independent scorer, `ERROR_INVENTORY.md`)

| Measure | Result |
|---|---:|
| `E_dump` (dump rows malformed) | 0 / 240 |
| `E_obs` (obs ≠ trainer claim) | 0 / 240 |
| `E_prb` (probe ≠ trainer claim) | 0 / 240 |
| `E_format` (withheld rows) | 0 |
| False supplied values reproduced word-perfect | 12 / 12 (ids 3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231) |
| False values flagged or "corrected" | 0 |
| Retained quirk | id 185: distract_value == obs_value (64) while distractor text says 72 — preserved as captured |

## 3. Class-4 — leg A M2 (Track-5 weights 30/25/25/10/10)

12 reps @scale 1 + rep 0 @scale 10 + btrap reps 0–11, each N=5 byte-identical,
all exit 0. Real corpus SHA attested in every bind log; btrap logs from the
same binary.

| Metric | Mean (12 reps) |
|---|---:|
| Mastery | 1.0000 |
| Revisability | 1.0000 (rf=12/12, rg=20/20 every rep) |
| Integrity | 1.0000 (gate 12/12, corpus-replay 24/24) |
| Retention | 1.0000 |
| Cost | 0.9113 |
| **Composite** | **0.9911** |

S10 no-degradation: mastery 1.0000, revisability 1.0000 (identical to S1).
Escalations 0, ops 287, eps 295, e90 reached (210), d1=40/40, d2=40/40,
d3=120/120, r2=40/40, r3=40/40, hallu=0, k1=k2=k3=1, refusal=1, disconn=4.

## 4. Class-4 — leg B §B.7 (teacher_id=50, direct flaw-only)

5× byte-identical runs, exit 0, `MUSEB_COMPLETE`; corpus SHA attested.
Teacher digest matches the taught store on all 240 ids.

| Slice | hits / 12 | nears | misses | score / 120 | pass | tripwire |
|---|---|---|---|---|---|---|
| 0 | 12 | 0 | 0 | 120 | 1 | 0 |
| 1 | 12 | 0 | 0 | 120 | 1 | 0 |
| 2 | 12 | 0 | 0 | 120 | 1 | 0 |
| 3 | 12 | 0 | 0 | 120 | 1 | 0 |
| 4 | 12 | 0 | 0 | 120 | 1 | 0 |
| 5 | 12 | 0 | 0 | 120 | 1 | 0 |
| 6 | 12 | 0 | 0 | 120 | 1 | 0 |
| 7 | 12 | 0 | 0 | 120 | 1 | 0 |

**§B.7 totals: 96/96 flaw hits, 8/8 slices passing, 0 check failures.**

## 5. Class-3 — leg C teacher leg (teacher_id=40)

5× byte-identical runs, exit 0, `MUSEC_COMPLETE`; corpus SHA attested.
Teacher/learner digests match on all 240 ids.

| Measure | Result |
|---|---:|
| Flaw hits | 96 / 96 (8/8 slices) |
| Slices passed | 8 / 8 |
| Clean adopted | 160 / 160 (20/20 per slice) |
| Mastery | 192 / 192 (24/24 per slice) |
| Blocked | 0 |
| Withheld skipped | 0 |
| Check failures | 0 |

## 6. Real English vs toy SOL baselines

| Run | Composite |
|---|---:|
| Toy SOL baseline A | 0.9909 |
| Toy SOL baseline B | 0.9933 |
| **SOL real English (this box)** | **0.9911** |

The real-English corpus lands squarely in the toy-SOL band. The learning
machinery is indifferent to the language switch: 12/12 false ids revised,
20/20 genuine hold, zero escalations, e90 reached at the same episode count.

## 7. FINDING — transcription behavior differs sharply between toy and real English

The toy-SOL teacher was a **flawless transcriber**: it emitted every row in
the required machine format with zero mechanical failures.

The real-English SOL teacher was **factually faithful but systematically
format-violating**: batch 18 produced four consecutive mechanically
unparseable DISTRACT_VALUE rows (`'To ensure integer. "90".'`, `'cent'`,
`'gross contains 120 items.'`, `'kl'`) across three attempts plus the
recovery run, exhausting the frozen retry budget and blocking the box at
39/40. The eventual factual transcript is 12/12 faithful (every planted
falsehood reproduced word-perfect, zero corrected, E_format=0) — the failure
mode is envelope, not content. Any future real-English championship teacher
should budget for format-level retries or a mechanically forgiving parse
frontier; the learning substrate itself is unaffected.

## 8. Mechanical repairs made during recovery (not bar changes)

1. **Category-3 width bug:** the port wrote `q2_cat_n`/`muse_t_cat_n` = 48
   for all categories, but the box is 48/48/48/96 (count-fact = ids
   144–239; the muse-native source returns 96 for cat 3). Pre-fix smoke run
   showed d1=33/40, rev_false=10/12, r2=35/40, e90 never reached — exactly
   ids 192–239 (incl. false ids 205, 231) never taught. Fixed in
   `muse_trial.zag` and `shared/muse_teach.zag` (re-copied to legB/legC).
2. Withheld skip added to legA `q2_teach` and the shared teach path
   (byte-identical copy discipline preserved).
3. legB/legC expectations changed to `240-MUSE_WITHHELD_N`; legC mastery
   denominator excludes withheld ids.
4. `analyze_m2.py`: parses only `if(id==N){return V;}` lanes from the
   generated domain (the bare `return 0;` fallback is not a 241st value).

## 9. Evidence & provenance

- Raws + SHA manifest: `sol/evidence/raw_SHA256SUMS.txt`
  (all 40 teach/dump raws, both failed batch-18 attempts, batch-19 metadata).
- Run logs: `sol/legs/{legA,legB,legC}/evidence/logs/` (25 + 1 + 1 logs,
  each N=5 byte-identical, with per-dir `SHA256SUMS.txt`).
- M2 analysis: `sol/legs/legA/evidence/ANALYSIS_M2.md`.
- No-RNG scan: `sol/evidence/norng_scan.txt` (PASS on all compiled sources).
- Sources committed: `sol/*.py`, `sol/corpus/*` (frozen corpus + raws),
  `sol/legs/*/src/*.zag`, `sol/legs/shared/muse_teach.zag`,
  `sol/legs/*/run_leg*.sh`, `sol/STATUS.md`, this verdict.
  Binaries and `.zagd` excluded.

**Commit:** branch `tnn-native-lab` of sylorlabs/TNN, path
`docs/lab/wave12/championship/english/sol/`, commit hash `TBD_COMMIT_HASH`
(recorded in `~/workspace/NIGHT_RUN_2026-09-21.md`).
