# TNN-SELF-DIAGNOSIS: MP3 Decoder — Final Report

**Worker:** TNN-SELF-DIAGNOSIS | **Date:** 2026-09-27 | **Method:** diagnostician-v2, extended to MP3

## What was done

Adapted `tnn_diag2.zag` (diagnostician-v2) into `tnn_mp3diag.zag`: same induction machinery
(required/forbidden/optional features, discriminative identifiers, match bars, abstention),
new MP3-grounded vocabulary (GH/SP/PW/WN/MP), MP3 evidence files, MP3 per-class fix directions.
Extractors and induction logic are byte-identical to v2 — only names, file keys, and
class-specific wording changed.

## Training

| Item | Value |
|---|---|
| Evidence bytes (raw, pre-fix) | 91,114 bytes |
| Evidence lines | 1,735 lines (4 files) |
| Files | b1draft.zag (23,480 B / 637 ln), tab64.zag (28,544 B / 95 ln), pyref.py (30,967 B / 817 ln), runlog.md (8,123 B / 186 ln) |
| Labels taught | 11 (GH:3, SP:2, PW:2, WN:2, MP:2) |
| Labels validated | 11 / 11 |
| Training wall time | 0.23 s |
| Knowmap SHA-256 | `abb91006985e084eb0d44fd9553e7c16ba562167ff649bb529daf2ef23612df2` |

### Induced signatures

| Class | Required | Forbidden | Bar | Disc. identifiers |
|---|---|---|---|---|
| GH (granule-handoff) | NUMLIT_NS\|ASSIGN | LIT_EQ\|COMMENT\|STRING | 1 | scfsi_all, scfsi (2) |
| SP (state-persistence) | CALL\|ASSIGN | NLIT_ARGS_GE2\|LIT_EQ\|COMMENT\|STRING | 5 | ist_pos, decode_scalefactors, ... (12) |
| PW (precision-widening) | CALL | NLIT_ARGS_GE2\|COMMENT | 2 | load_f64tab, t_panb, f32_to_f64_z, ... (14) |
| WN (wrong-note) | BRANCH | NLIT_ARGS_GE2\|COMMENT\|STRING | 16 | 48 prose words |
| MP (missed-processing) | ASSIGN | NUMLIT_NS\|NLIT_ARGS_GE2\|LIT_EQ\|BRANCH\|COMMENT\|STRING | 1 | huffman, mst, ... (14) |

No class abstained (none vacuous). WN has the highest bar (16) — effectively silent on code.

## Discovery

| Target | Bytes | Lines | Wall | Raw hits | GH | SP | PW | WN | MP |
|---|---|---|---|---|---|---|---|---|---|
| curdec.zag (current) | 51,290 | 1,345 | 0.45 s | 323 | 129 | 0 | 133 | 0 | 61 |
| preguard.zag (pre-guard) | 50,594 | 1,335 | — | 321 | 128 | 0 | 132 | 0 | 61 |

**Before-control** (empty labels): 0 classes → "NO DEFECT FOUND" on curdec. PASS.

**Determinism:** Two curdec discoveries byte-identical.
Trace SHA-256: `b655e90c2c11002b7316084d8f1251bead61753d482e5fff3c23e95a55ad560c` (both runs).

## Findings: Genuine vs Noise

### GENUINE DISCOVERIES

| # | Class | Locus | Evidence | Verdict |
|---|---|---|---|---|
| 1 | PW | curdec L66 `d.*.pan = load_f64tab(t_panb(), 14);` | Score 4, ids=[load_f64tab,t_panb] — highest specificity | **GENUINE**: exact locus, exact class. Real 3.2e-08 deviation where oracle holds f64. |
| 2 | PW | curdec L58-63,65 (other load_f64tab calls) | Score 3, ids=[load_f64tab] | **CLASS-TRUE, BENIGN**: mechanism present but oracle is f32 there → no harm. Signature cannot distinguish harmful from benign widening. |

### NOISE (mechanism named)

| # | Class | Locus | Mechanism |
|---|---|---|---|
| 3 | GH | curdec L165,169,181,207 (fixed scfsi code) | **Instructive FP**: signature cannot represent variable discipline. The fixed single-variable code (mask→extract→shift) is structurally identical to the buggy two-variable code at this feature resolution. Fix ≡ bug to the extractor. |
| 4 | GH | 123 other hits (all score=1, no ids) | Bar=1 from sparse training (3 labels) → fires on any NUMLIT_NS\|ASSIGN line. Pure permissiveness. |
| 5 | MP | 61 hits | **Absence-defect collapse**: machinery cannot represent "missing stage"; signature latches onto nearby present features (huffman, mst) which recur throughout the fixed decoder. |
| 6 | PW | 125 other hits | Spurious discriminative identifiers (`fn`, `n`, `as`) from 2-label training → generic CALL lines match. |

### TRUE NEGATIVES (correct silence)

| Class | Hits | Why correct |
|---|---|---|
| SP | 0 | Fixed decoder hoists ist_pos to dec_init; no per-granule re-init. Signature correctly finds nothing. |
| WN | 0 | Prose class (bar=16) correctly silent on code. |

### UNTAUGHT DEFECT

| Locus | Finding |
|---|---|
| preguard L820-828 (unguarded brate table) | **INVISIBLE**: no taught class fires meaningfully. Vocabulary limitation, not method failure — the class was never taught. |

## Fix decision

**No fix applied.** The PW L66 deviation is genuine but **not actionable**:
- Documented as negligible (3.2e-08 relative, ~0.001 LSB, no feedback path — safe).
- The PREREG mandates f32→f64 widening for dr_mp3-sourced tables; "fixing" would violate it.
- The crew already judged it non-actionable. TNN's rediscovery validates detection, not repair.

No battery run (no code changed). Mono SHAs unchanged.

## Commits

None. Work in `~/workspace/mp3_selfdiag/` (not committed; no clone available due to disk).

## Open questions

1. **Precision**: 323 hits for 1 genuine defect. Can TNN learn to rank by identifier specificity, or does the method need a precision gate?
2. **GH resolution**: What feature would distinguish one-variable from two-variable state discipline? (Dataflow, not just lexical.)
3. **MP representation**: Can absence-defects be taught, or is the (file,line-range,class) label format inherently unable to represent "missing"?
4. **WN**: Prose classes induce spurious signatures (BRANCH="for"). Is there a prose-specific feature family, or should WN be code-only?
5. **File cache**: The Zag runtime caches file reads by name; reusing a filename returns stale content. (Workaround: fresh filenames. Lesson for AGENTS.md.)

## Anti-leakage notes

- curdec.zag and preguard.zag never in training. Extractors unchanged from v2.
- Caveat: b1draft.zag (training) shares dec_init with curdec.zag, including the unlabeled PW pattern at b1draft:66. The PW signature was induced solely from tab64.zag labels; curdec:66 was never labeled.
- Caveat: RUNLOG.md (training) mentions "f32 pan table precision" in prose; the locus was never labeled.
- Ground truth withheld until after discovery traces were generated.
