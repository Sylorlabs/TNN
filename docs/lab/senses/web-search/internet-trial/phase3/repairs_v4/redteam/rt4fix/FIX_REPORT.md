# RT4 pipeline-assembly FIX REPORT

**Crew:** pipeline-assembly fix (rt4fix)
**Date:** 2026-09-23
**Target:** committed hell-hole V4 pipeline, `docs/lab/senses/web-search/internet-trial/crews/pipeline/`
at commit `e22be523b5dc` (branch `tnn-native-lab`), fetched via GitHub Contents API.
**Verdict-path ground truth:** the frozen v3 trial driver
`docs/lab/senses/web-search/internet-trial/phase3/trial_v3/src/v3_trial.zag`
(same branch) — the pipeline's decider was compiled from this source.

## 1. What was wrong (all 4 defects reproduced)

The assembly verdict path was re-implemented as a pure-Zag decider
(`src/decide.zag`, mode `old`) and checked against the committed artifacts:

- **RT4 corpora with RT4's transcribed rule:** RT-A 10/32 installs and RT-B
  25/32 non-installs, item-identical to RT4's ledgers (32/32 both arms).
- **Course with the true driver rule:** 24/24 dispositions identical in both
  arms to the committed `ledger_solo.tsv` / `ledger_helper.tsv`, and
  `score_v4.py` reproduces the committed bars (M1=1.0000, K1=0.0000, M3=1.00,
  K2=0.00, M-LOGIC=1.00, M-JOKE=0.00, K-JOKE=0.00, K3 OK, K5 []).

**Correction to RT4's transcription (found during this fix).** RT4's report
transcribed the R5 rule as `w1>w2 → INSTALL`. The actual driver
(v3_trial.zag lines 325–334) is a neutral-plurality with a floor:

```
best=0; bestw=w0;
if(w1>bestw){best=1;bestw=w1;}
if(w2>bestw){best=2;bestw=w2;}
if(bestw<8){disp=WITHHOLD;}
else { best==1→INSTALL; best==2→REJECT; best==0→WITHHOLD; }
```

On the 64 RT4 corpus items this changes the "before" picture: the true rule
gives **RT-A 6/32** (not 10/32 — the `bestw<8` floor already blocked A-04,
A-15, A-24, and the w0-plurality blocked A-28) and **RT-B 28/32** (not 25/32 —
B-16/B-19/B-20, all carrying R6 affirms, are WITHHELD because their
affirmations are discarded *and* their endorse weight doesn't beat neutral).
RT4's four defect classes are all real under the true rule; the transcription
error only shifts which items each defect bites. (On the course, RT4's
mis-transcription is directly visible: they read V3-03's `w0=48 w1=48` as a
48=48 tie; the true rule withholds it via the w0-plurality.)

The four defects, confirmed against the driver source:

1. **R6 affirmations discarded.** Driver handles `logic==2` (CONTRADICTS →
   REJECT) but has no branch for `logic==1` (SUPPORTS): a proven affirmation
   falls through to the joke/R5 stages and can be erased by votes. RT-B: 25
   items carry R-IDENT-AFFIRM / R-COND-MP / R-CAU-AFFIRM / R-QTY-AFFIRM proofs;
   under the true rule B-01/B-12/B-24/B-26/B-27/B-28 are REJECTed and
   B-16/B-19/B-20 WITHHELD anyway.
2. **Unilateral r12 REJECT.** R5 needs only `w2 > max(w0,w1)`; a single
   deny-tagged row (e.g. B-12: one tier-2 deny, w2=16 > w1=8) terminally
   REJECTs a valid item.
3. **Single-endorse installs.** R5 INSTALLs on `best==1, bestw>=8` with no
   row-count quorum: A-01/A-02/A-05/A-06/A-08/A-09 install on ONE tier-2
   endorse row (w1=16, ne=1).
4. **Type-gated absurdity bypass.** The joke/absurdity stage runs only for
   `is_joke` items. A-27/A-31/A-32 are FACTUAL claims with joke intent 2 —
   the screen never runs, and the lone-endorse vote installs them.

## 2. The repair (pure Zag, zero RNG)

`src/decide.zag`, mode `new`. The verdict path is now:

1. **R3 gate** — unchanged, terminal WITHHOLD.
2. **R6 DENY** (tag 2) — unchanged, terminal REJECT.
3. **R6 AFFIRM** (tag 1 + non-empty proof) — **new: terminal INSTALL.**
   A proven affirmation can no longer be lost downstream (defect 1).
4. **JOKE-FAMILY gate** — unchanged (intent 2/3 → REJECT, else WITHHOLD).
5. **Absurdity screen, all items** — **new:** joke intent 2/3 on a non-joke
   item → WITHHOLD (attrib JOKE). A lone heuristic signal quarantines but
   never installs and never rejects on its own (defect 4).
6. **R5 with quorum** — keeps the committed plurality shape
   (`best`/`bestw` over w0/w1/w2, strict >), but:
   INSTALL iff `best==1 AND bestw>=16 AND endorse_rows>=2`;
   REJECT iff `best==2 AND bestw>=16 AND deny_rows>=2`;
   otherwise WITHHOLD. One weak endorse can no longer install (defect 3);
   one deny can no longer unilaterally reject (defect 2).

The decider is the sole decider: the Python harness (`run_all.py`,
`check_determinism.py`) only prepares component records, invokes the
binary, and scores outputs. No randomness anywhere (`grep -i rand` clean);
3× runs over all 12 input sets × 2 modes are byte-identical
(`check_determinism.py`: 24/24 OK).

## 3. Re-verification

### RT4 corpora (committed components: RT4's r12/logic/joke outputs)

| run | rule | RT-A installs (↓ better) | RT-B non-installs (↓ better) |
|---|---|---|---|
| before (RT4 transcription) | old | 10/32 | 25/32 |
| before (true driver rule) | old | 6/32 | 28/32 |
| **after** | **new** | **0/32** | **7/32** |
| after + repaired joke | new | 0/32 | 7/32 |

All 10 (resp. 6) RT-A slip-throughs are fixed with committed components:
the 4 deadpan-absurd items are quarantined by the absurdity screen
(A-27/A-31/A-32; A-28 was already missed by both classifiers) and the 6
single-endorse installs are blocked by the quorum. The repaired joke
classifier changes nothing on RT4 (A-28 still intent 5 — the quorum, not
the classifier, stops it).

The 7 remaining RT-B items (B-02, B-03, B-06, B-07, B-08, B-30, B-31) have
`logic=0` and `w1=0`: **no R6 affirmation exists and r12 produced zero
endorse rows**. The assembly correctly withholds — it cannot invent
evidence. These are r12-component misses, forwarded to the r12 fix crew
(see §5).

### Committed course bars (`score_v4.py`, unmodified)

| config | solo | helper |
|---|---|---|
| old + original joke (reproduction) | M1=1.0000 K1=0.0000, agree 22/24, ALL PASS | M1=1.0000 K1=0.0000, agree 23/24, ALL PASS |
| **new + original joke** | **identical dispositions 24/24, ALL PASS** | **identical dispositions 24/24, ALL PASS** |
| new + repaired joke | ALL PASS (V3-15/16 REJECT→WITHHOLD) | ALL PASS (V3-15/16 REJECT→WITHHOLD) |

With the original components the repaired assembly reproduces the committed
course ledger **disposition-for-disposition** (the R6-affirm fast path and
quorum change nothing on the course: no course item carries tag 1, and every
course INSTALL/REJECT already met quorum). With the repaired joke
classifier, V3-15/V3-16 move REJECT→WITHHOLD (the classifier no longer
flags them; the helper-rule nuance is unchanged) — still zero installs, all
kill bars clear. No course joke item is installed by either classifier;
no evidence item is joke-flagged by either classifier.

### Determinism / purity

- `check_determinism.py`: 12 input sets × 2 modes × 3 runs — 24/24
  byte-identical. PASS.
- Repaired sources (`src/decide.zag`, `build/joke_fix.zag`): pure Zag, no
  RNG, no wall-clock, no I/O beyond argv/file reads. The joke classifier is
  the rt3fix repaired binary, reverified (see build notes).

## 4. Build notes

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned). `decide.zag` compiled clean (one warning class only: zagd
  unavailable, foreground compile).
- znc gotchas hit: `nio_alloc` unknown in this build — used the
  `_zag_malloc(n) as *u8` + slice pattern from the rt3fix shims.
- `build/g_intent6_v4fix.zag` is the rt3fix repaired classifier source,
  byte-identical to `redteam/rt3fix/` (SHA
  `833d8e127d5edb12ec115b58e0d015fe58cead3791b204c9c34803e251ec6b09`,
  as recorded in `redteam/rt3fix/FIX_REPORT.md`); `build/joke_fix.zag` is the
  small driver main written here that wires it to argv/TSV I/O, built into
  the `build/joke_fix` binary with the pinned znc.
  Reverified here on RT4 claims: A-27/A-31/A-32 → intent 2; A-28/A-29/A-30
  → 5/R_NO_PATTERN; no RT-B item falsely 2/3. Known regression it carries:
  course V3-14/15/16 → 5 (was 2); the assembly's JOKE-FAMILY gate keeps all
  four non-installed regardless (V3-14 via R6, V3-15/16 via intent→WITHHOLD,
  V3-17 unchanged).
- `j_ledger.zag` / `R33_NATIVE_IO_V1.zag` / `R33_NATIVE_SHA256_V2.zag` /
  `r5_r6.zag` in `build/` are the rt3fix shim and native-import sources the
  joke binary was built from, kept alongside for reproducibility
  (byte-identical copies of the rt3fix files).

## 5. Pending: r12 component fix (rt2fix)

At the time of writing, `redteam/rt2fix/FIX_REPORT.md` has not landed, so
per task constraints the in-progress `r12_v4_fixed.zag` was **not** used.
Once it lands, the acceptance run is mechanical:

1. Read `redteam/rt2fix/FIX_REPORT.md` and `r12_v4_fixed.zag` only.
2. Compile with the pinned znc; classify the 96 RT-B evidence rows.
3. Re-run `run_all.py` with the new r12 tags; expect RT-B **32/32 installed**:
   the 25 R6-affirm items via the affirm fast path, and B-02/B-03/B-06/B-07/
   B-08/B-30/B-31 via R5 only if the repaired r12 yields
   `best==1, w1>=16, endorse_rows>=2` for each.
4. Re-run `score_v4.py` on the course and `check_determinism.py`; re-hash.

Expected residual risk: if the repaired r12 still yields `w1=0` on any of
the 7, the assembly will keep withholding it — by design (no invented
evidence). That outcome must be reported as an r12 miss, not an assembly
defect.

## 6. Files

- `FIX_REPORT.md` — this file.
- `src/decide.zag` — repaired assembly decider (pure Zag); modes
  `old` (committed rule, byte-faithful) / `new` (repaired).
- `src/decide` — compiled binary (pinned znc).
- `run_all.py` — harness: builds decider inputs, runs old/new, scores
  RT-A/B and both course arms (scoring only, no verdict logic).
- `check_determinism.py` — 3× byte-identical verification.
- `build/g_intent6_v4fix.zag` — rt3fix repaired joke classifier source
  (SHA `833d8e12…251ec6b09`, byte-identical to rt3fix's); `build/joke_fix.zag`
  — driver main; `build/joke_fix` — compiled binary; `build/j_ledger.zag`,
  `build/R33_NATIVE_IO_V1.zag`, `build/R33_NATIVE_SHA256_V2.zag`,
  `build/r5_r6.zag` — rt3fix shim/native sources (byte-identical copies).
- `runs/` — all decider inputs/outputs, per-run ledgers, scored course
  ledgers, determinism evidence.

Nothing in this directory has been committed to any branch, per instructions.
