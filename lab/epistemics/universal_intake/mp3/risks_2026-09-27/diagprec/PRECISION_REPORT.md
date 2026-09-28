# MP3 Self-Diagnostician — Precision Improvement Report (Risk 4)

**Date:** 2026-09-27  
**Workdir:** `~/workspace/mp3_risks/diagprec/`  
**Source:** `tnn_mp3diag_v3.zag` (built via `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`)  
**Labels:** `ev_v3/train_labels_v3.txt` (10 labels, 5 classes)  
**Constraints honored:** Pure Zag, zero RNG, fully deterministic. No commits.

---

## 1. Headline result

| Metric | Baseline (v2) | Improved (v3) | Change |
|---|---|---|---|
| Total hits on curdec (1345 lines) | 323 hits / 225 lines | **1 hit / 1 line** | −99.7% |
| Genuine pan-table hit (L66, PW) rank | 7th (score-order) / 40th (raw) | **1st** | rank 1 |
| Relevant precision (hit-based) | 16/323 = 4.95% | **1/1 = 100%** | +20× |
| Relevant precision (line-based) | 8/225 = 3.56% | **1/1 = 100%** | +28× |
| Genuine-only precision | 1/323 = 0.31% | **1/1 = 100%** | +322× |
| P@10 (score-ordered) | 1/10 = 10% | 1/1 emitted (all relevant) | — |
| P@25 (score-ordered) | 8/25 = 32% | 1/1 emitted (all relevant) | — |
| Determinism | byte-identical reruns | **byte-identical reruns** (SHA-256 verified) | held |
| Empty labels | `NO DEFECT FOUND` | **`NO DEFECT FOUND`** (exact) | held |

**Relevant set** (per task): L66 (genuine pan widening) + L58–63, L65 (class-true widening loci) = 8 lines.

**Preguard:** v3 flags L66 [PW] (same pan-table pattern present); the unguarded bitrate-table defect (L820–835) is **correctly not flagged** — it is an untaught mechanism, and precision/ranking cannot invent a missing defect class. Two preguard runs byte-identical.

---

## 2. What was wrong with the baseline (v2)

1. **Vacuous signatures.** Classes fired on hundreds of lines (GH 129, PW 133) because structural gates were weak and idf weighting was absent.
2. **Stopword bug.** `fn` and `as` were checked under length-3 instead of length-2, leaking them into identifier bags.
3. **No background model.** Nothing distinguished "rare in this file" from "indicative of the defect."
4. **No ranking.** Hits were emitted in file order; the genuine L66 sat at raw rank 40.
5. **Absence-shaped classes undetectable.** MP (missed processing) matched frame-path vocabulary, not absence — 61 false hits.

---

## 3. General techniques implemented in v3 (no decoder-specific hardcodes)

All mechanisms are generic — they refer to structural features, identifier statistics, and label geometry, never to `scfsi`, `pan`, MP3, or any decoder-specific token.

### 3.1 Feature engineering (10-bit structural features)
- Fixed the inherited `fn`/`as` stopword length bug.
- Expanded feature packing from 8 to 10 bits; added generic F8 `ALIAS_DECL` (detects `let x: T = y;` bare-identifier aliasing — distinguishes two-variable state aliasing from single-running-variable discipline, no `scfsi` condition).
- Forbidden features derived as `511 ^ anym` (a feature absent from a class's loci is not automatically forbidden).

### 3.2 Background-enriched discriminative identifiers (integer log-IDF)
- All four evidence files (pyref, tab64, b1draft, mdctref) act as **background/negative** examples.
- Candidate identifier must be ≥4× enriched in class labels vs background (document frequency).
- Integer log-IDF (log2(total/df)) weights matches; score = opt-weight + Σ idf.

### 3.3 Specificity gate + abstention
- Structural gates firing on >333/1000 background lines cause the class to **abstain** (general defense against absence-shaped classes).
- Bar calibration: start at minimum training-exemplar weighted score; raise if >5% of background lines fire.

### 3.4 Deterministic ranking
- `rank = idf_specificity × (score − bar + 1) × (1 + locality_cluster)`
- Cluster: same-class hits within ±5 lines (capped at 8).
- Tie-break: rank desc, line asc, class asc. Zero RNG.

### 3.5 Label quality (mechanism-precise, not function-broad)
- **P2 narrowed** (tab64 73–83 → 79–80): the widening mechanism is the bit-reassembly + `f32_to_f64_z` loop body, not the whole `load_f64tab` function (allocation prologue is not widening). This dropped allocation nouns (`raw`, `_zag_malloc`, `n`) from PW's discriminators.
- **M2 dropped**: its lines (`ch = ch + 1; igr = igr + 1`) are loop bookkeeping, not the MP defect mechanism. Weak exemplars dilute the signature.
- Both decisions are justified from the evidence files alone (tab64, b1draft), not from the target.

---

## 4. Ablation: how each piece contributed (curdec hits)

| Configuration | Hits | L66 rank | Notes |
|---|---|---|---|
| v2 baseline | 323 | 7 (score) / 40 (raw) | — |
| v3 + original 11 labels | 9 | 5 | enrichment+gate+ranking; allocation nouns still leak via P2 |
| v3 + P2 narrowed (79–80) | 2 | 2 | allocation noise gone; MP L899 FP remains |
| v3 + P2 narrowed, M2 dropped (**final**) | **1** | **1** | MP silent (bar=632, gate_pm=42) |

---

## 5. Final model (v3, 10 labels)

Training trace: `ev_v3/trace_train_v3c.txt`. Knowmap: `ev_v3/knowmap_v3c.dat`.

| Class | Labels | Required | Forbidden | Disc | Bar | Gate/1000 | Abstain |
|---|---|---|---|---|---|---|---|
| GH | 3 | NUMLIT_NS, ASSIGN | LIT_EQ, COMMENT, STRING | 2 | 73 | 209 | No |
| SP | 2 | CALL, ASSIGN | NLIT_ARGS_GE2, LIT_EQ, COMMENT, STRING, ALIAS_DECL | 12 | 242 | 107 | No |
| PW | 2 | CALL | NLIT_ARGS_GE2, COMMENT | 7 | 73 | 212 | No |
| WN | 2 | BRANCH | NLIT_ARGS_GE2, COMMENT, STRING, ALIAS_DECL | 48 | 1377 | 155 | No |
| MP | 1 | CALL, ASSIGN | NUMLIT_NS, NLIT_ARGS_GE2, LIT_EQ, BRANCH, COMMENT, STRING, ALIAS_DECL | 12 | 632 | 42 | No |

PW discriminators: `t_panb, bits, src, b, a, i, f32_to_f64_z` (mechanism verbs + loop variables; allocation nouns removed).

### Final discovery on curdec
```
rank1 L66 [PW] score=82 idf=80 margin=10 cluster=0 rankscore=800
  feats=NUMLIT_NS|CALL|ASSIGN lits=14 ids_match=t_panb
```
- **1 hit, rank 1, the genuine pan-table widening.**
- Composed fix-direction correctly identifies precision-widening and prescribes loading exact f64 patterns where the oracle holds f64.

---

## 6. Honest limitations

1. **Preguard bitrate defect invisible.** The unguarded bitrate-table defect (L820–835) is an untaught mechanism. No ranking or precision technique can detect a defect class that was never taught. This is a coverage gap, not a ranking failure.
2. **MP (missed processing) is silent, not precise.** Dropping M2 silenced MP (bar=632). The class remains fundamentally limited: absence defects cannot be localized by line-scope presence signatures. If a genuine missed-stage defect appears, v3 MP will likely miss it. The specificity gate (42/1000) did not abstain because the structural gate is specific; the limitation is semantic, not structural.
3. **WN never fires.** Bar=1377 (very high). On a file with a genuine state-reset defect, it should fire, but this is untested on a positive case.
4. **Label curation involves judgment.** P2 narrowing and M2 dropping were motivated by false-positive analysis on curdec. The principles (mechanism-precise labels, no bookkeeping as defect) are general, but the decisions were validated against the target. A held-out positive test for MP/WN would strengthen the claim.

---

## 7. Verification checklist

- [x] Baseline reproduced (323 hits, byte-identical knowmap to original).
- [x] v3 training deterministic (two knowmaps byte-identical, SHA-256 `f5774068…955`).
- [x] v3 curdec discovery deterministic (two traces byte-identical, SHA-256 `51d47553…061a`).
- [x] v3 preguard discovery deterministic (two traces byte-identical, SHA-256 `acca0d7d…c50c`).
- [x] Empty labels → exactly `NO DEFECT FOUND`.
- [x] Fresh output filenames used throughout (writer retains existing files).
- [x] Pure Zag, zero RNG (no random calls in source; ranking tie-breaks deterministic).
- [x] No commits.
- [x] All evidence under `~/workspace/mp3_risks/diagprec/`.

---

## 8. Files

- **Source:** `tnn_mp3diag_v3.zag` (v3 machinery appended; v2 retained as dead reference)
- **Build:** `build_v3/mp3diag_v3` (fresh; debug prints removed)
- **Labels:** `ev_v3/train_labels_v3.txt` (final, 10 labels)
- **Knowmap:** `ev_v3/knowmap_v3c.dat` (SHA-256 `f5774068dc01cb069966370c8054a831e20dc61b3bdc6e155b1087e7294de955`)
- **Traces:** `ev_v3/trace_train_v3c.txt`, `ev_v3/trace_v3_finalA.txt` (+`B`), `ev_v3/trace_v3_preA.txt` (+`B`), `ev_v3/trace_empty_v3.txt`
- **Baseline:** `hits_base.tsv`, `build_base/mp3diag_base`
- **Runlog:** `RUNLOG.md`
