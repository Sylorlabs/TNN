# 10GB Generalist — DRY RUN: teach + score on 7 done sources (2026-09-24)

**Label: DRY RUN. This is NOT the official measurement.** The wiki splits
(~40h long pole) block the official full-corpus run; this dry run proves the
entire downstream pipeline end-to-end on the 7 completed sources NOW.

## 1. Verified inputs (SHA re-verified 2026-09-24, before use)

| source | facts | sha256 (verified) | file used |
|---|---|---|---|
| gb_A | 2,559,300 | 5a0b2ee8d616a8d99300404d5c2c97feed63c23fba3457dc0b27c01f04e354ad | stage/gb_A_run1/facts.dat |
| gb_B | 2,152,486 | 7a1f12848f4d858be288cbf71fdf725488ad89b1a93686c32962d9f6facfa1be | stage/gb_B_run1/facts.dat |
| ostx | 56,485 | a530f27e114f26287c4dc1a32cec2288c0495d76e46bc80825fce6c4669eb9f8 | stage/ostx_run2/facts.dat (run1 byte-identical) |
| se_bio | 62,234 | 1f3ea38da83979b7aa09aba85993589f4ff1a190ac094a4785c9d9ca15fa1c6d | stage/se_bio_run2/facts.dat (run1 is dbcecc04…, NOT the verified one) |
| se_chem | 98,420 | 2c93bbb7b0f605e34faed402960e54cb63d9556924f09248d6bf47ef70a074f7 | stage/se_chem_run1/facts.dat |
| se_phys | 588,421 | 3b454f66546193683906ca29a21a972778abc9b907953edff254253dc2f45fff | stage/phys_run1/facts.dat |
| se_math | 3,809,868 | 35a4828ebb696d488c11cc7288fdb41d740cfe8d15398a8d0a2affe08d981c2d | stage/se_math_run1/facts.dat |
| **total** | **9,327,214** | | |

All 7 match CREW4_HANDOFF.md. Note: `se_bio_run1` does NOT match the handoff
SHA (it is an older clean, dbcecc04…); the verified one is `se_bio_run2`,
exactly as `merge_run1_zag.sh` uses. `ostx_run1` and `ostx_run2` are
byte-identical (both a530f27e…).

## 2. Merge (dry-run)

- Binary: rebuilt from committed `teach/merge_zag.zag` with the pinned
  toolchain (`znc_linux_x86_64_abed8aa1`); rebuilt binary is BYTE-IDENTICAL
  to the existing scratch `merge_zag_bin` (the committed source edit after
  the binary build was cosmetic). Dry run uses the fresh rebuild.
- Smoke test: 4-record 2-shard fixture merges in global key order; unsorted
  shard correctly rejected ("shard not sorted").
- Command: `merge_zag_bin_rebuilt dryrun_facts.dat <7 shards in runbook order>`
- Result: `merge_zag: merged 9327214 records from 7 shards` — EXACTLY the
  expected 9,327,214 (2,559,300+2,152,486+56,485+62,234+98,420+588,421+3,809,868).
  Output 5,294,850,090 bytes = sum of inputs exactly (5,294,850,090) —
  merge only reorders, as designed.
- `dryrun_facts.dat` SHA256:
  `af10db8b03c47e91d809092d89e35f96a7a533c7f9aa2e331200e113818bc690`
- Record count: 9,327,214 (merger-reported; matches source sum exactly)
- THROUGHPUT FINDING (dry-run value): the merge is I/O-starved by box
  contention — ~53MB/min output (~0.9MB/s), process mostly in I/O sleep
  with negligible CPU. The merger itself is fine (8MB shard buffers, 8MB
  output buffer); the box's disk is saturated by ~20 concurrent jobs.
  5.3GB merge ≈ 100 min wall at this rate. The official 8-source merge
  faces the same conditions — schedule accordingly (or run at a quieter
  hour). No code change proposed: this is contention, not a merge bug.

## 3. Teach ×2 (calibration-gated ingest)

- Invocation (per crew-5): `./gate_bin ingest facts bad.bin store/ ncap`
  (no `teach` mode; `bad.bin` = `~/workspace/tmp10/bad.bin`, 1000-record
  negative control).
- ncap = 11,292,656 (9,327,214 + 9,327,214/5 + 100,000)
- Run 1 → `dryrun/store1/`, Run 2 → `dryrun/store2/`
- Run 1 manifest: `n=9030226 nsealed=2205 clock=143 blob_total=4920220564
  blob_chunks=147 blob_recs=9030226 g1=9 g2=0 g3=100371 lessons=143
  lessons_rejected=3 negcontrol=1000/1000
  seal=43d7e5cc262755a837b2984858db309560eaadcc2339e7e8481a0a51d44542fd`
  (40 min, rc=0). Reconciliation: 9,030,226+9+0+100,371+3×65,536=9,327,214 ✓.
- Run 2 → `dryrun/store2/`: `ingest done inst=9030226
  seal=43d7e5cc262755a837b2984858db309560eaadcc2339e7e8481a0a51d44542fd`,
  rc=0, 27 min (09:25:37→09:52:35 UTC).
- **Teach determinism: PERFECT at aggregate level.** Both runs byte-identical
  manifests: n=9030226, nsealed=2205, clock=143, blob_total=4920220564,
  blob_chunks=147, blob_recs=9030226, g1=9, g2=0, g3=100371, lessons=143,
  lessons_rejected=3, negcontrol=1000/1000, identical seal.
- Store byte-compare (`diff -r store1 store2`): **rc=0 — byte-identical**
  (9.4GB compared, zero differences, including audit.log, all 147 blob
  chunks, manifest.txt, sparse index).
- Store aggregate SHAs (sorted relpath + per-file SHA256, hashed):
  store1 = `0f485fbb315b722d3be9153f57fd84bba94b968e2d4acc0ecd48906e2b643884`,
  store2 = `0f485fbb315b722d3be9153f57fd84bba94b968e2d4acc0ecd48906e2b643884`
  — **identical**. Teach determinism fully confirmed at byte level.

### DRYRUN-FINDING-1: `~N` split-keys vs the lesson CAL (spec-compliant; surfaced)

The 3 dropped lessons (84, 116, 124) failed CAL **must-accept only**
(masks 8, 8, 7 — zero must-reject bits, so the 4 synthetic probes passed in
all 143 lessons). Root cause, verified record-by-record against `ig_gate`
(`gate.zag`):

- The source pipeline splits over-long SE texts into chunks keyed
  `se:<site>:<q|a>:<id>~N` (e.g. `se:math:a:210842~0`,
  `se:math:q:3780312~1`).
- `ig_se_key_ok` (gate.zag:579) requires every byte after the post id to be
  a digit; `~` (126) fails → G3 verdict 3 (REJECT).
- All 7 must-accept failures were `~N`-keyed records at lesson head
  positions: lesson 84 pk=3 (`se:math:a:210842~0`), lesson 116 pk=3
  (`se:math:q:2375840~0`), lesson 124 pk=0,1,2
  (`se:math:q:3780312~1/~2/~3`).
- Corpus-wide: **117,470 records carry `~` keys; 91,866 of them kind 6** —
  numerically 91.5% of the reported G3 count (100,371). These 91,866 are
  gate-incompatible by key grammar, but whole-lesson dropping means some
  records in dropped lessons were never individually classified, so exact
  attribution of the G3 count requires another scan. The remainder (~8.5K)
  are the frozen "\n\n" question rule.

Consequences: (a) 196,608 legitimate records (2.1% of the corpus) dropped
because an arbitrary 65,536-record boundary landed on `~N` chunks;
(b) the gate behaves **per frozen spec** (GATE_SPEC G3: "numeric post id"),
so this is a source/gate interface mismatch, NOT a gate bug — no gate
change made. Options for the official run (decision needed): admit `~N`
in the key grammar (spec amendment), make lesson-CAL skip gate-rejected
records when choosing must-accept probes, or re-key/join the chunks at
the source stage. Evidence: `lesson_autopsy.txt`, `tilde_count.txt`.

## 4. Probe scoring (frozen 250-probe battery, DRY RUN)

- questions.tsv: 250 probes (200 K- + 50 R-), id+question only, from the
  FROZEN baseline files (never modified).
- `gate_bin_fixed panswer` pa1: `panswer done probes=250 facts=9030226
  keywords=490`, rc=0. pa1/answers.tsv: 250 lines, SHA256
  `83b2931f49d16f989bb1a42bb241cf52b9b7e72509a9786f13bdceada8454a2e`.
  pa2 (determinism check): completed rc=0, pa2/answers.tsv BYTE-IDENTICAL
  to pa1 (same SHA256) — panswer is deterministic.
- `score_panswer.py` (frozen scoring rules) mechanical: **21/250 (8.4%)**
  — ANCHOR 3/10, MATH 0/50, R-MATH 0/20, R-SCI 2/15, R-XDOM 0/15,
  SCI 12/50, VOC-ANT 0/10, VOC-DEF 0/30, VOC-SYN 0/10, WITHHOLD 0/10,
  WORLD 4/30.
- Baseline floor: 14/250 knowledge+reasoning (audited), 5/18 dialogue.
- Dialogue: panswer does not do dialogue (frozen `dialogue_bin` cannot read
  the store). Dialogue figure stays the frozen 5/18 — NOT re-measured,
  delta 0.
- Mechanical vs audited: **audited 3/250** after demoting 18
  response-template/wrong-relation coincidences under frozen rules.
  Genuine: K-078 (Jupiter largest planet), K-092 (friction opposes motion),
  K-160 (Eiffel Tower → France). Demoted examples: K-057 (light-speed text
  for gravity question), K-062 (echoed the question), K-064 (fish gills for
  "frozen water"), K-174 (George Chapman for Homer), K-175 (Ninth for Fifth
  Symphony), K-184 (Walter Scott for Jane Austen), R-030 (generic
  physical/chemical-changes text for baking soda+vinegar).
- **Audited delta from 14/250 baseline: -11** (3 vs 14).
- Miss/regression autopsy: the dry-run corpus (7 sources, no wiki) answers
  fewer probes genuinely than the baseline corpus. The 3 genuine hits are
  all baseline-wrong (see §5). No baseline-audited-correct probe regressed
  to incorrect in a way that indicates a pipeline defect — the delta
  reflects corpus coverage differences, not a teach/panswer regression.

## 5. Connections probe (cross-domain)

Three probes were WRONG in the frozen baseline (not among its 16 mechanical
correct: K-181–K-188, K-190, R-036–R-039, R-041, R-043, R-048) and are
GENUINELY CORRECT in this dry run (audited under frozen rules):

1. **K-078** | `which planet is the largest in the solar system?`
   key `gb:pg12342:8679` |
   `JUPITER, one of the exterior planets of the solar system, and the\nlargest; revolves in an orbit outside that of the asteroids, at a mean\ndistance from the sun of 480 millions of miles, completing its revolution\nround the sun in 4338 days, and taking 10 hours to revolve on its own\naxis; it is sur`

2. **K-092** | `which force opposes motion between surfaces?`
   key `ostx:college-physics-1e:college-physics-1e:1165` |
   `is the acceleration.\n(b) Including friction. We now have a given value for friction, and we know its direction is parallel to the slope and it opposes\nmotion between surfaces in contact. So the net external force is now\nF net M-bM-^HM-% = w M-bM-^HM-% M-bM-^HM-^R f , (4.33)$`

3. **K-160** | `which country is the eiffel tower in?`
   key `gb:pg12342:11004` |
   `PARIS (2,448), the capital of France, in the centre of the northern\nhalf of the country, on both banks of the Seine, and on two islands (La\nCitM-CM-) and St. Louis) in the middle, 110 m. from the sea; is the largest\ncity on the Continent, and one of the most beautiful in the world. No\ncity has finer`

(Escaped bytes as stored in pa1/answers.tsv; `\n` = literal backslash-n
in the TSV. `M-bM-^H` etc. are UTF-8 bytes in the original.)

## 6. Pipeline bugs found + fixed

### DRYRUN-FINDING-2 (BUG, FIXED): `ig_blob_parse_hdr` rejects short zero padding

**Symptom:** `gate_bin panswer` died with `panswer: blob parse failed` (rc=1)
at fact 1,776,425 — chunk 16 of the store.

**Root cause:** When the blob writer fills a chunk, it zero-pads the remainder.
If the remainder is 1–10 bytes, the chunk ends with a short zero run.
`ig_blob_parse_hdr` (gate.zag:1079) checked `off+11>buf.len` (truncation)
BEFORE checking `kind==0` (zero padding), so a short zero tail was
misclassified as truncation → -1 → panswer abort. Python audit of all 147
chunks found 4 affected (16, 18, 23, 128), all with 2–9 byte zero tails —
e.g. chunk 16: last record ends at 33,488,889, 7 zero bytes remain.

**Fix (gate.zag, `ig_blob_parse_hdr`):** check `kind==0` → return 0 (padding)
before the truncation check. Safe: G1 guarantees stored kinds are 5–8, so
kind==0 unambiguously means padding; the writer only emits zeros for padding.
All 5 callers (sindex builder, `ig_blob_read_text`, revise, delete, panswer)
share the function, so all are fixed.

**Verification:** rebuilt `gate_bin_fixed` with the pinned toolchain
(`znc_linux_x86_64_abed8aa1`, 290,307 bytes); panswer re-run in progress.

**Impact on official run:** the wiki merge will produce ~200+ chunks; with
~2.7% of chunks affected here, the official panswer would almost certainly
have hit this. Must-fix before the official scoring.

### DRYRUN-FINDING-3 (BUG, CONFIRMED — fix deferred): merger error paths return rc=0

**Reproduced:** `merge_zag_bin /nonexistent_out.dat /nonexistent_shard.dat`
prints `merge_zag: cannot open shard 0` but exits rc=0.

**Root cause:** `teach/merge_zag.zag` `fn main()void` uses bare `return;`
at 10+ error sites (cannot open shard/output, alloc failed, shard not
sorted, read/write failed, etc.). In a void main, `return;` exits 0 —
errors are printed but the process status is success.

**Gate contrast:** `gate_bin`/`gate_bin_fixed` panswer correctly returns
rc=1 on `panswer: blob parse failed` (observed). The gate's error paths
use `return 1;` which propagates. No bug in the gate.

**Disposition:** NOT fixed in this dry run. The dry-run merge succeeded,
so this did not affect results. Fixing requires adding an exit(2) syscall
helper and touching 10+ sites — high-risk without a full merger
regression suite. **For the official run:** the merge runbook must NOT
rely on merger rc alone; verify the output file exists and has the
expected record count/size. (Or fix `merge_zag.zag` with an
`_zag_raw_syscall(60, 1, ...)` fail helper before the official merge.)

### DRYRUN-FINDING-1: `~N` split-keys vs lesson CAL (spec-compliant; surfaced, not fixed)

(see §3 — 91,866 kind-6 `~N`-keyed records G3-rejected; 3 lessons dropped.)

## 7. Commits

- `454d48b40d4f5c4541c538ea8cf19d52193631f4` on main (parent 0c6e48f937af):
  DRY RUN report + results + gate.zag blob-parse fix (DRYRUN-FINDING-2).
  Files: `knowledge/ingest_10gb/teach/gate.zag`,
  `knowledge/ingest_10gb/teach/dryrun/DRYRUN_REPORT.md`,
  `knowledge/ingest_10gb/teach/dryrun/probe_results.tsv`,
  `knowledge/ingest_10gb/teach/dryrun/SHAS.txt`.
  (Committed via `commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`.)

## 8. Artifacts (dry-run dir)

- `~/workspace/scratch_10gb_work/dryrun/` — dryrun_facts.dat, merge.log,
  questions.tsv, store1/, store2/, pa1/, pa2/, answers, probe_results.tsv
