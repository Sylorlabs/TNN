# VERDICT R2-9 — Witness-Emission PAM (FINAL)

**Fork:** R2-9 (C-EC1) — Witness-Emission PAM, replay-only selection-emitting percept pipeline.
**Status: DEAD — B5 kill (false permanent installs 719/10,000 = 7.19% > 3% kill threshold)**
**Date:** 2026-09-23 (completion crew)

## 1. What was built

Pure-Zag `sense` CLI (`forks/R2-9/src/r29.zag`, pinned `znc_linux_x86_64_abed8aa1`):
- Six task percept front-ends (colordisc ΔE76, colorconst linear-map residual, shapetrans radial-profile, pitchdisc autocorrelation f0, timbredisc Goertzel centroid, motiondir SAD candidate match), each emitting a judgment, confidence, install/withhold disposition, and 1–2 emission selections (exact audio byte spans / pixel rects / video regions).
- A read-only replay emitter: artifacts are verbatim copies of cited source bytes. The emission pass runs after the percept pipeline and cannot influence it.
- Hash-chained ledger (SHA-256) over per-trial entries; batch mode writes `percepts.tsv` + `LEDGER.jsonl` + `artifacts/`.
- Zero RNG in decision paths; deterministic given fixture bytes.

## 2. Deciding bar

**B5 (KB4 — false permanent installs ≤ 3% on 10,000 trials): FAIL — fork is DEAD.**

Measured on the frozen R2A suite (5,000 normal + 5,000 adversarial, trials.tsv sha256
`dad1d743fd4b9babcf5ebf0bda43f4b8172aaccc587c391384f050c0f86061c6`),
with the pipeline as built (binary `work/sense` byte-identical to a fresh build from
committed `src/r29.zag`, sha256 `ec7c7446e17b5197864cf46fbdeb82e25a88f0971c5d6c6cffebc904b08fd589`):

| metric | measured |
|---|---|
| false permanent installs (INSTALL ∧ judgment ≠ truth) | **719 / 10,000 = 0.0719 = 7.19%** |
| bar | ≤ 0.03 |
| result | **FAIL — exceeds the bar by 2.4×** |

Breakdown (`evidence/battery_10k/b5_breakdown.tsv`):

| task/split | n | installs | false installs | rate |
|---|---|---|---|---|
| colorconst / adversarial | 584 | 516 | 134 | 0.2295 |
| colorconst / normal | 681 | 556 | 41 | 0.0602 |
| colordisc / adversarial | 982 | 267 | 254 | 0.2587 |
| colordisc / normal | 1022 | 628 | 38 | 0.0372 |
| motiondir / adversarial | 854 | 502 | 60 | 0.0703 |
| motiondir / normal | 591 | 585 | 0 | 0.0000 |
| pitchdisc / adversarial | 982 | 296 | 0 | 0.0000 |
| pitchdisc / normal | 721 | 451 | 0 | 0.0000 |
| shapetrans / adversarial | 997 | 347 | 75 | 0.0752 |
| shapetrans / normal | 1264 | 820 | 79 | 0.0625 |
| timbredisc / adversarial | 601 | 534 | 38 | 0.0632 |
| timbredisc / normal | 721 | 721 | 0 | 0.0000 |
| **adversarial only** | 5000 | 2462 | **561** | **0.1122** |
| **normal only** | 5000 | 3761 | 158 | 0.0316 |

The defect: adversarial fixtures (decoys/metamers — worst families R2A-COL-2 colordisc,
R2A-CCN-2 colorconst) fool the judgment front-ends, and the disposition layer
installs the false percepts anyway (62.2% of all trials installed). This is the
same disease as round-1 KB4: a spoofed observation gets installed as a memory.
The witness contract (emission is read-only replay) was honored — the belief side,
not the emission side, is what died.

## 3. Bars B1–B7 (complete)

| Bar | Result | Evidence |
|---|---|---|
| B1 viability (≥60% on frozen 370 harness primary) | **PASS** — 0.8622 (319/370) | `evidence/percepts_370_emit.tsv` |
| B2 vs Approach A (0.726) | +0.136 (+13.6pp), R2-9 | same |
| B3 efficiency | 231,452,162 ops / 370 fixtures = 0.224× Approach A; 10k battery: 6,513,404,379 ops total (~651k/trial); emission bytes 11.87 MB / 370 | `evidence/battery_10k/b5_score_run1.log` |
| B4 no-interference (HARD KILL, KB-E5) | **PASS** — emit vs noemit percepts/dispositions byte-identical on **10,000/10,000 trials** | `evidence/battery_10k/kb_e5_10k.log` |
| B5 KB4 false installs (≤3% on 10,000) | **FAIL** — 719/10,000 = 7.19% | `evidence/battery_10k/b5_breakdown.tsv` |
| B6 determinism (HARD KILL) | **PASS** — 4 emit runs byte-identical (`cmp` on percepts.tsv + LEDGER.jsonl; sha256 9f54f0e5… / 8046238e…); binary byte-identical to fresh rebuild from committed src | `evidence/battery_10k/byteidentity.log`, `pipeline_provenance.log` |
| B7 beauty | (i) elegance — the witness contract is clean: replay is identity; (ii) KB-E3/KB-E4 human verdict — **MOOT, package WITHHELD** (fork dead; human verdict cannot rescue a mechanical-bar failure per §5(7)) | `evidence/human_package/WITHHELD_README.md` |

## 4. Kill criteria KB-E1–KB-E5

- **KB-E1 byte-identity:** PASS on 370 (530 artifacts byte-identical to source, identical across 3 runs). Full 10,000-trial KB-E1 NOT RUN — battery halted at the B5 kill per prereg §5 (mechanical kill is decisive).
- **KB-E2 no phantom:** PASS on 370. Full 10k NOT RUN (same reason).
- **KB-E3 human equivalence:** NOT ATTEMPTED — fork dead; package withheld (151 visual artifacts labeled NEW, 49 audio gate-blocked; nothing ever shown to Micah).
- **KB-E4 spoof-catch:** NOT ATTEMPTED (same).
- **KB-E5 no-interference:** **PASS on 10,000** (emit vs noemit percepts/dispositions byte-identical; even the full percepts.tsv files are byte-identical, ledger hashes included).

## 5. Evidence and ledger

- `evidence/battery_10k/` — B5 scores (run1, run2), per-task/per-split breakdown, byte-identity log (4 runs), KB-E5 10k log, pipeline provenance (binary == fresh build), run logs, trials manifest sha
- `evidence/percepts_370_emit.tsv`, `evidence/LEDGER_370.jsonl` — frozen-370 battery (earlier crew)
- `evidence/human_sample_manifest.tsv` (+ `.sha256`) — frozen 200-trial human sample (superseded)
- `evidence/human_package/` — briefs + 151 visual artifacts, **WITHHELD** per `WITHHELD_README.md`

## 6. Deviations and notes

1. **Human sample frozen after fork build began** (prereg timing not met; documented by earlier crew; Goodhart protection preserved — fork was blind to the sample). Moot: fork died mechanically.
2. **Generator spec contradictions** (earlier crew's generator ledger): per-task distribution rows sum to 5,100 normal / 5,815 adversarial vs top-line 5,000/5,000; the realized frozen suite is exactly 5,000/5,000 (verified). Total 10,000 preserved.
3. **Completion-crew run4**: the task asked for two battery runs + cmp. Three identical runs already existed; the completion crew ran a 4th independent run (run4) and cmp'd it against run1 — byte-identical. A 5th run would add no information given 4 identical runs; deviation recorded honestly.
4. **Noemit battery**: completed (rc=0, 10,000 rows) before the kill halted further work; its output was used for the 10k KB-E5 check (PASS).
5. **Audio emission vs synth ban**: emitted audio is verbatim replay of fixture bytes (identity, not synthesis) — the hypothesis under test itself.

## 7. Reconciliation with R2-11-R29 (same lineage, independently killed on B5)

R2-11-R29 (R2-9 lineage reconstruction after a workspace collision) measured
**1,427/11,840 = 12.05% false permanent installs** and died on B5 with both forks.
The two findings corroborate rather than contradict:

- **Same B5 definition and bar** (verified in their `work/score_bars.py`): INSTALL ∧ judgment ≠ truth, denominator = all trials, bar ≤ 3%.
- **Near-identical code**: their `src/forkA/r2-11a.zag` contains all 60 of R2-9's top-level `fn` definitions; 57/60 bodies are byte-identical (differing: `p_shapetrans`, `p_motiondir`, `main`; one added helper `sel_ok`). The judgment→disposition path — the part that kills — is the same code.
- **Different fixture pools**: R2-9 ran the frozen R2A suite (10,000: 5,000 normal / 5,000 adversarial); R2-11-R29 ran its own realized pool (11,840: 5,840 normal / 6,000 adversarial).
- **Rate difference explained**: 7.19% vs 12.05% differ because the pools and two front-ends differ; both are ~2.4×–4× above the 3% bar. The mechanism fails the same way: fooled judgments on adversarial fixtures get permanently installed by an over-eager disposition (R2-9 installs 62.2% of all trials).

## 8. Verdict

**DEAD on B5 (KB4).** The witness-emission contract was honored — emission is
provably read-only (KB-E5 PASS on 10,000), byte-faithful (KB-E1 PASS), and the
pipeline is perfectly deterministic (B6 PASS, 4 byte-identical runs). But the
percept pipeline's disposition installs spoofed observations as permanent
memories at 7.19%, more than twice the 3% kill threshold. The failure is in the
belief side (judgment + disposition), which this fork did not change relative to
its lineage — R2-11-R29's independent reconstruction dies on the identical bar
with the same code.

No further work is authorized on this fork except the committed evidence.
