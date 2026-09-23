# T2-SPEECHACT crossref replication — RUNLOG (HEAVY crew)

Family T2-SPEECHACT: speech-act wave replication. Type A (full independent rerun,
clean environment). Date: 2026-09-23 (PDT).

## 1. Frozen prereg verification (before any work)

- Source: `~/workspace/tnn-lab/crossref/PREREG_TIER2.md`
- Section: `## T2-SPEECHACT — speech-act wave (Type A)` extracted with sed, recorded verbatim in scratch file `prereg_section.txt`.
- sha256(PREREG_TIER2.md) = `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`
- tnn-native-lab branch head: (recorded after clone)

## 2. Evidence pins (frozen BEFORE any run)

| pin | commit | topic |
|---|---|---|
| PoC | `fabb003e263c` | 7.1%→50.0% weird-English; both arms 12/12 falsehood withholds; markers hand-specified |
| volume | `291bbf75785b` | 60/60 cells byte-identical ×3; peak-and-decline curve 7/61/76/67/60/51/50 @0/1/2/4/8/16/32 |
| decline | `188e9a6ad068` | count rule flips 2→32 decline→rise; corrected monotone 5→8→21→24→30→32→38; 12/12 controls intact |

Transfer control, implicature, and WHY_SARCASM figures re-derived from committed sources as well.

## 3. Environment

- Clean clone: `git clone --branch tnn-native-lab https://github.com/sylorlabs/TNN.git` → `~/workspace/scratch-crossref/T2-heavy/T2-SPEECHACT/clean/`
- Build dir: `.../crew/build/`; runs: `.../crew/runs/`; scratch only, never /tmp; TMPDIR=~/workspace/tmp_commit
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- Zero RNG / pure Zag for mechanisms; Python only for glue/analysis
- ≥3 byte-identical runs per battery; SHAs recorded

(log continues below)

## 3. Prereg record

- Prereg section extracted verbatim to `prereg_section.txt` (7 lines, the full
  `## T2-SPEECHACT — speech-act wave (Type A)` section).
- sha256(`~/workspace/tnn-lab/crossref/PREREG_TIER2.md`) =
  `90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f`
- Section matches the task spec; no drift vs the frozen text.

## 4. Branch state (vanishing-tree anomaly watch)

- Full clone `https://github.com/sylorlabs/TNN.git --branch tnn-native-lab` into
  `scratch-crossref/T2-heavy/T2-SPEECHACT/clean/` (36,395 files, completed
  2026-09-23 ~02:56 PDT; took ~20 min, 3.5G).
- Local HEAD at clone finish: `b09df71bf6c273a6bde77881fa72c72415f54797`
  ("imagination/img: RESTORE r10 files dropped by 308bf3655575"). Working tree CLEAN.
- Branch moved twice during the run (very active branch): at one point the
  GitHub API reported head `51e944390624942c167596c3feb1e46b2b003872` ("hell-hole
  v3 TRIAL COMPLETE"); after `git fetch`, remote head =
  `1cc0913c98e7dbdf48fbf19b1dacc4844b6df187` ("INTEGRATION: merge five round-2
  dialogue repair families"). All five pins verified as ancestors of BOTH local
  HEAD and origin/tnn-native-lab (`git merge-base --is-ancestor`, 5/5).
- Head tree at the API-checked point had NO `docs/lab/prose-learning/` (reorg
  deleted it; only crossref/imagination_discovery/knowledge/ops/rsi/senses/wave12
  remain under docs/lab/). The `contents` API 404'd on branch paths; git trees
  work fine. All evidence was therefore taken from PINNED HISTORY commits via
  `git archive`, never from head.
- History order of wave pins: fabb003e (PoC, 10:45) -> 291bbf75 (volume, 11:05)
  -> 188e9a6a (decline, 11:33) -> a761584b (why-sarcasm, 13:36) ->
  90ddad64 (implicature, 13:43), all 2026-09-22 PDT.

## 5. Evidence-pin verification (before any run)

Commits API-verified on GitHub (messages match the wave docs):

| pin | full sha | date | subject |
|---|---|---|---|
| PoC | `fabb003e263ca747c7c191c5a85bc7eab8ac4b34` | 2026-09-22 10:45 PDT | Speech-act knowledge experiment: Micah's hypothesis test |
| volume | `291bbf75785b5f0286a4bc17c7cad31bee9ffae5` | 2026-09-22 11:05 PDT | Volume experiment: the speech-act learning curve |
| decline | `188e9a6ad068a40cc67fa5996be3d1924cc131e5` | 2026-09-22 11:33 PDT | Decline investigation: why more examples hurt |
| why-sarcasm | `a761584bbbe395133e1a307b85d9f63c75ef72f4` | 2026-09-22 13:36 PDT | why-sarcasm wave (RDTDT) — frozen prereg + evidence |
| implicature | `90ddad644fff893ccce3c2b7d76b49be743263e0` | 2026-09-22 13:43 PDT | Implicature with speaker/situation/goal/indirect-request context |

Driver blob SHAs (from `git ls-tree` at the pins, all verified again after
extraction with `git hash-object` on the extracted files — all OK):

| driver | blob sha | pin |
|---|---|---|
| delib_sa.zag | `6f08e0932ec0bc1052ee8624f8af23fcf1115a0a` | fabb003e |
| delib_vol.zag | `a5de27048ec5a22ead8650e1d674027f3802d0ba` | 291bbf75 |
| delib_cnt.zag | `3a7d813fb4b00f9e01f4bfd1b442ddf3eb03bb2d` | 188e9a6a |
| delib_sarc.zag | `20a5ae63ee54fe74115fe03b00fc50b7deb5d02f` | a761584b |
| delib_impl2.zag | `0434090ad9d1f310758ba00fc82f76919d733501` | 90ddad64 |

Substrate: `R33_NATIVE_IO_V1.zag` Linux port = blob `a6b440d256437de5e34faa77a0d73079e2755375`
(committed at the pins under `docs/lab/GROK47_OVERNIGHT/teacher/work/c3s_src/substrate/`;
byte-identical to the live `tnn-lab/prose-learning/epistemic_wave/src/` copy the
original crew built against — checked with git hash-object on the live file).
`R33_NATIVE_SHA256_V2.zag` = blob `5dd858fa1097451ee6164c015993fd5a434877db`
(committed R33 tree; also matches live). NOTE: the Darwin-variant R33_IO file
committed under `docs/generations/R33/...` does NOT match; the wave was built on
Linux, so the Linux-port copy is the correct one. The drivers `@import` them via
`../src/` relative to cwd, so each work tree mirrors: `work/src/{R33_*.zag}` +
`work/speechact_exp/` (the pinned tree), built from `work/speechact_exp` with the
pinned znc. All builds emitted only analyzer warnings (A0101/A0102/A0107/L0012
classes, same as the original builds) — no errors.

## 6. Runs

Toolchain for every build: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
No binaries or .zagd caches reused/copied between environments. All binaries
rebuilt from committed sources. Run dirs: `runs/{poc,vol,dec,sarc,impl}/`.

### 6.1 PoC (fabb003e) — REPRODUCED

`delib_sa.zag` -> `delib_sa_bin`. 6 cells (arm 1|2 x b12_false/b12_true/c70) x 3 reps.
- 6/6 cells byte-identical across 3 reps; rep1 byte-identical to committed
  scored_evidence (hashes match: arm1 c70 49c77be1…, arm2 c70 181032b1…).
- arm1 c70: 5/70 withheld = 7.1%; arm2 c70: 35/70 = 50.0%. Δ = +42.9pp. ✓
- Both arms: 12/12 falsehoods withheld, 12/12 trues endorsed. ✓
- Per-family arm2: joke 5/10, sarcasm 3/10, hypothetical 5/10, analogy 3/10,
  counterfactual 9/10, poetry 5/10, implicature 5/10 — matches RESULTS.md exactly.
- arm1 0/7 families ≥8/10; arm2 1/7 (counterfactual 9/10). Both fail frozen bar. ✓

### 6.2 Volume ladder (291bbf75) — REPRODUCED

`delib_vol.zag` -> `delib_vol_bin`. 7 rungs x 3 modes (all/sarconly/orderswap) x
3 sets (c70/b12_false/b12_true) x 3 reps = 189 runs.
- 63/63 cells 3/3 byte-identical; 180/180 committed cells byte-identical to
  committed scored_evidence (the 9 r0_orderswap cells were not committed; they
  are 3/3 identical and equal r0_all as expected since no examples exist at r0).
- Volume curve (mode=all, c70 withheld/70): r0=5 (7%), r1=43 (61%), r2=53 (76%
  peak), r4=47 (67%), r8=42 (60%), r16=36 (51%), r32=35 (50%). Peak-and-decline
  reproduces exactly as committed.
- r0 all_c70 == PoC arm1 c70 verdicts (byte-identical, 49c77be1…). ✓
- Transfer control: sarconly r32 withholds poetry (W089–W098) 10/10 AND all 12
  true controls (0/12 endorsed) — degenerate overgeneralization confirmed. ✓

### 6.3 Decline investigation (188e9a6a) — REPRODUCED

`delib_cnt/b2/b3/f2/f3.zag` -> fresh binaries; `delib_vol_bin` rebuilt in this
tree too. 110 cells x 3 reps = 330 runs (runs/dec_runner.sh; ~4 min).
- 330/330 files byte-identical to committed scored_evidence. Zero diffs.
- Bar-variant c70 (withheld/70): cnt = 5/8/17/27/32/27/38; b2 = 5/55/53/49/44/37/35;
  b3 = 5/43/53/63/65/67/69 — all match the committed H-D1/H-D3 tables.
- Corrected curve (diverse ordering + count rule): 5→8→21→24→30→32→38 — strictly
  monotone, no adjacent-rung decline. The decline does NOT reappear under the
  count rule (r2=17 → r32=38, rise). ✓
- Controls: cnt 12/12 false + 12/12 true at r2 and r32 ✓; b2 12/12 both ✓;
  b3 breaks the true leg at r32 (7/12 — as documented, reported broken, not a win) ✓.
- f2 implicature 2–5/10 peak 5/10 with legs intact (12/12 r2+r32); f3 true leg
  4/12 @r2 and 10/12 @r32 (broken as reported). ✓
- Orders legs (diverse/redundant/proto/outlier × 7 rungs × 3 reps, all
  byte-identical to committed): diverse 18-item decline under max diversity —
  H-D2 stays killed on substance.
- Kill-bar dispositions rechecked against committed DECLINE_INVESTIGATION.md:
  H-D1 SURVIVES, H-D2 KILLED, H-D3 REDIRECTED, H-D4 KILLED (as preregistered).

### 6.4 WHY_SARCASM wave (a761584b) — REPRODUCED

`delib_sarc.zag` -> `delib_sarc_bin`. 16 cells x 3 reps = 48 runs.
- 16/16 cells 3/3 byte-identical; 48/48 files byte-identical to committed.
- Dispositions (all match the committed table):
  - H3 markers: marked_marked 10/10 vs base_marked 0/10 (SURVIVES)
  - H3 context: ctx_ctx 10/10 vs base_ctxutt 3/10 (SURVIVES)
  - H4 speaker: speaker_spk 10/10 (5 K-withholds ALIX + 5 endorses BRAM) vs
    base_spkutt 5/10 (SURVIVES — only fix for genuine-vs-sarcastic ambiguity)
  - H5 inversion opacity: best genuine discrimination 5/10 in every mode (SURVIVES)
  - H1 layering: layered_bare 3/10 == base_bare 3/10, Δ=0 (KILLED)
  - H2 "blocks": notruth_bare item-identical to base_bare (KILLED); litfalse 10/10
    withheld all reason F — wrong-reason masking confirmed, benchmarks inflated.
- repro_bare reproduces PoC arm2 c70 verdicts 70/70 (diff empty).

### 6.5 Implicature context wave (90ddad64) — REPRODUCED

`delib_impl2.zag` -> `delib_impl2_bin`. `impl_ctx.txt` x 3 reps.
- 3/3 byte-identical; byte-identical to committed impl_ctx_rep1.
- 12/12: 6 REQUEST (odd items, correct target objects: salt, heater, trash,
  wrap-up/meeting, package, baby) + 6 LITERAL (even items).
- I1 12/12 ≥ 10/12 ✓; I2 all 6 same-utterance pairs discriminate ✓;
  K-IM1 no-hardcode ✓ (verify_impl.py passes — Python used only for verification
  plumbing, as the original); K-IM2 determinism 3/3 ✓.

## 7. Frozen-rule check

- 7.1%→50.0% PoC: YES (5/70 → 35/70, byte-identical).
- Monotone corrected curve 5→8→21→24→30→32→38: YES (strictly monotone).
- 12/12 controls intact: YES (cnt and cntdiv, false+true legs, r2 and r32).
- H3/H4/H5-survive + H1/H2-killed dispositions: YES, all six hold byte-for-byte.
- Decline reappears under the count rule: NO (17→38 rise; original-bar decline
  still reproduces under b2 score-only, confirming the bar mechanism).

VERDICT: **REPRODUCED**. Nothing partial, nothing missing.
