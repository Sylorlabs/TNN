# RUNLOG — MP3 Risk 4: Diagnostician Precision

**Task:** Improve TNN's MP3 self-diagnostician precision/ranking on the known defect set.  
**Constraints:** Pure Zag, zero RNG, deterministic. General techniques only (no pan-line or decoder-specific hardcodes). Do not commit. Evidence under `~/workspace/mp3_risks/diagprec/`. Fresh output filenames mandatory (writer retains existing files).

---

## 2026-09-27 — Baseline reproduction

- Recovered original assessment (`~/workspace/selfpam_run/tnn-lab/docs/lab/tnn-mp3-diagnostician/ASSESSMENT.md`) and source (`tnn_mp3diag.zag`).
- Recovered current decoder (`~/workspace/mp3_selfdiag/ev/curdec.zag`, 51,290 bytes, MD5 `b0e33cae9c9e0469b07822196e36425c`) and preguard (`~/workspace/mp3_selfdiag/ev/preguard.zag`, 50,594 bytes).
- Rebuilt baseline (`build_base/mp3diag_base`). Fresh baseline knowmap byte-identical to original.
- Baseline discovery on curdec: **323 hits** (GH 129, SP 0, PW 133, WN 0, MP 61). Score dist: 6:2, 5:4, 4:3, 3:46, 2:108, 1:160.
- Genuine: L66 [PW] score 4 (`load_f64tab,t_panb`). 7 class-true widening loci: L58–63, L65.
- Baseline metrics (from `hits_base.tsv`): L66 raw rank 40, score-rank 7; P@10=10%, P@25=32%; relevant 16/323 hits (4.95%), 8/225 lines (3.56%); genuine-only 1/323 (0.31%).

## 2026-09-27 — v3 implementation

Implemented in `tnn_mp3diag_v3.zag` (appended v3 machinery; v2 retained as dead reference; `main` dispatches to `do_train_v3`/`do_discover_v3`):

1. Fixed inherited stopword bug (`fn`/`as` length 3→2).
2. 10-bit feature packing; generic F8 `ALIAS_DECL` (`let x: T = y;`).
3. Forbidden = `511 ^ anym`.
4. Integer log-IDF discriminative identifiers; ≥4× background enrichment filter.
5. All 4 evidence files as background; specificity gate (>333/1000 → abstain); bar calibration (min train score, raise if >5% bg fires).
6. Deterministic ranking: `idf × (score−bar+1) × (1+cluster ±5 lines)`; tie-break rank↓ line↑ class↑.

Training labels: `ev_v3/train_labels.dat` (11 labels: G1–3, S1–2, P1–2, W1–2, M1–2).

## 2026-09-27 — v3 debugging

- Hit `panic: slice index out of bounds` in `read_knowmap_v3` DISC parsing (PW class).
- Root cause: custom v3 tokenizer mishandled token boundaries; replaced with v2's proven `find_byte` loop.
- Removed all `DBG:` prints; rebuilt clean (`build_v3/mp3diag_v3`, 268,833 bytes).

## 2026-09-27 — v3 results and label refinement

- v3 + 11 labels: **9 hits**, L66 at rank 5. (Allocation nouns `raw,_zag_malloc,n,src,f64` from P2's function-broad range leaked into DISC.)
- **P2 narrowed** (tab64 73–83 → 79–80, the widening loop body): **2 hits**, L66 at rank 2. MP L899 FP remained.
- **M2 dropped** (b1draft 572–575, `ch = ch + 1` bookkeeping — weak exemplar): **1 hit**, L66 at rank 1. MP silent (bar=632, gate_pm=42).
- Final labels: `ev_v3/train_labels_v3.txt` (10 labels).

## 2026-09-27 — Verification

- Training determinism: two knowmaps byte-identical (SHA-256 `f5774068dc01cb069966370c8054a831e20dc61b3bdc6e155b1087e7294de955`).
- Curdec discovery ×2: byte-identical (SHA-256 `51d475535f9b8f3f0494db3e2a4d483264123457636edfb51e3bdbe6b835061a`). 1 hit: L66 [PW] rank 1.
- Preguard discovery ×2: byte-identical (SHA-256 `acca0d7d7593a7de527efde639838c67802c738ed4396c2072c50ce02724c50c`). 1 hit: L66 [PW] rank 1. Bitrate-table defect (L820–835) correctly not flagged (untaught mechanism).
- Empty labels → exactly `NO DEFECT FOUND`.
- Reports written: `PRECISION_REPORT.md`, `RUNLOG.md` (this file).

## 2026-09-27 — Deliverables

- `tnn_mp3diag_v3.zag` — improved source
- `ev_v3/train_labels_v3.txt` — final training labels
- `ev_v3/knowmap_v3c.dat` — trained knowmap
- `ev_v3/trace_train_v3c.txt` — training trace
- `ev_v3/trace_v3_finalA.txt`, `trace_v3_finalB.txt` — curdec discovery (byte-identical)
- `ev_v3/trace_v3_preA.txt`, `trace_v3_preB.txt` — preguard discovery (byte-identical)
- `ev_v3/trace_empty_v3.txt` — empty-label regression
- `hits_base.tsv` — baseline hit table
- `PRECISION_REPORT.md` — full report
- `RUNLOG.md` — this file

No commits made.
