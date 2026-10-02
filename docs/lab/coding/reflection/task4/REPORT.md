# Task 4+ Coding-Reflection Battery — Final Report

**Date:** 2026-09-22
**Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Task:** frozen coding-reflection Task 4+ idiom battery, two arms × five items × five reps

---

## ⚠️ RECONSTRUCTED PREREG — READ FIRST

The frozen prereg `coding/reflection/PREREG.md` is **physically truncated**:
it ends at line 144, mid-sentence in §3a, its final bytes literally containing
`...[truncated 10769 chars]`. The Task-4+ §4 it references does not exist
anywhere under `coding/` or `docs/`. **No second copy was found.**

All "frozen" Task-4 definitions used here (vectors, I/O, checks, quality
formulas, arm-gap rule) come from a **reconstruction**
(`coding/reflection/task4/TASK4_SPEC.md`) built solely from the explicit
assignment text. It freezes only what the assignment states. Anything the
assignment did not specify — including one B1 check-count ambiguity
documented below — is a judgment call, flagged as such. **Treat every
"frozen" claim in this report as reconstruction-frozen, not prereg-frozen.**

---

## Result headline

| | INFORMED (coding KB + prior art) | FROM-SCRATCH (coding KB only) |
|---|---|---|
| B1 Huffman | **5/5 pass, 1st attempt, q=1.000** | 0/5, KB-MISS halt, q=0 |
| B2 SQL | **5/5 pass, 1st attempt, q=1.000** | 0/5, KB-MISS halt, q=0 |
| B3 Peephole | **5/5 pass, 1st attempt, q=0.988** | 0/5, KB-MISS halt, q=0 |
| B4 B-tree | **5/5 pass, 1st attempt, q=1.000** | 0/5, KB-MISS halt, q=0 |
| B5 SNAKE (control) | **5/5 pass, 1st attempt, q=1.000** | 0/5, KB-MISS halt, q=0 |

**Arm-gap (frozen metric, B1–B4):** gap_first = **100.0 pp** on all four;
mean gap_iters = **6.00**; gap_q ≈ **1.00** on all four.
**Meaningful = TRUE** by all three disjuncts (≥3 items ≥25pp ✓; ≥2.0 iters ✓;
≥2 items ≥0.25 q ✓).

**B5 control reading (frozen):** B5 also shows a 100pp gap. Per the frozen
spec this reads as **general impairment of the scratch arm** (it cannot
attempt *any* item without relevant idiom knowledge), not as a prior-art
effect on B5 specifically. B5 did not enter the meaningful-gap computation.

---

## Per-arm × per-item (5 reps each, canonical logs byte-identical)

### INFORMED arm (store: 74 entries, FNV `6af80e9355817834`)

| item | pass/5 | first-attempt/5 | mean iters_working | mean quality | mean secs |
|---|---|---|---|---|---|
| B1 Huffman | 5/5 | 5/5 | 1.00 | 1.0000 | 0.58 |
| B2 SQL | 5/5 | 5/5 | 1.00 | 1.0000 | 1.03 |
| B3 Peephole | 5/5 | 5/5 | 1.00 | 0.9881 | 0.44 |
| B4 B-tree | 5/5 | 5/5 | 1.00 | 1.0000 | 0.60 |
| B5 SNAKE | 5/5 | 5/5 | 1.00 | 1.0000 | 0.43 |

B3 quality 0.9881 (not 1.0) is mechanical, not a failure: p3's reference
reduction is 28.6%, so `min(1, 0.286/0.30) = 0.953`; mean over the four
programs = 0.9881. All four programs passed (semantics preserved, ≥20%
reduction).

### FROM-SCRATCH arm (store: 69 entries, FNV `a92e1031d460dbd9` ✓ control)

| item | pass/5 | first-attempt/5 | mean iters_working | mean quality | mean secs |
|---|---|---|---|---|---|
| B1 Huffman | 0/5 | 0/5 | 7.00 | 0.0000 | 0.00 |
| B2 SQL | 0/5 | 0/5 | 7.00 | 0.0000 | 0.00 |
| B3 Peephole | 0/5 | 0/5 | 7.00 | 0.0000 | 0.00 |
| B4 B-tree | 0/5 | 0/5 | 7.00 | 0.0000 | 0.00 |
| B5 SNAKE | 0/5 | 0/5 | 7.00 | 0.0000 | 0.00 |

Every scratch attempt: `gen` → `KB-MISS: no family entry matched spec` →
learner `diagnose` (GEN) → `class=GEN_FAILURE strategy=halt-genfail` →
loop terminates after 1 iteration. Per the frozen scoring,
iterations-to-working-build = 7 (never). **The scratch learner never
fabricated an algorithm it does not know** — the honest halt, not a
confabulated program, is the measured behavior.

---

## Exact arm-gap table (frozen metric)

| item | gap_first (pp) | gap_iters (working) | gap_q |
|---|---|---|---|
| B1 | 100.0 | 6.00 | 1.0000 |
| B2 | 100.0 | 6.00 | 1.0000 |
| B3 | 100.0 | 6.00 | 0.9881 |
| B4 | 100.0 | 6.00 | 1.0000 |

- Items with gap_first ≥ 25pp: **4/4** (needs ≥3) ✓
- mean gap_iters = **6.00** (needs ≥2.0) ✓
- Items with gap_q ≥ 0.25: **4/4** (needs ≥2) ✓

---

## Directional inventions audit

**None.** All informed-arm generations are byte-identical recalls of the
frozen prior-art templates (stable `src_sha256` across all 5 reps; the only
variation is slot-fill of frozen parameters: ALPHABET=256, MAXOPS=4096,
ORDER=4, W=10, H=8). The learner selected entries and filled slots — it
invented no novel algorithms, data structures, or optimizations. The
scratch arm emitted `KB-MISS` on all items (no fabrication, no
confabulation). The deliberate `diagnose` machinery (argmax classification
with trace) was exercised on the scratch GEN path; no COMPILE/TEST
diagnoses were needed (informed first attempts all passed).

---

## Method (how the trial was built)

1. **Prior-art corpus** (`corpus/`): five pure-Zag templates
   (Huffman, SQL, peephole, B-tree, SNAKE), each independently verified
   against `src/oracle4.py` before freezing. Corpus entries contain
   algorithm descriptions + templates + slot declarations — **no frozen
   expected outputs** (audited).
2. **Stores** (`stores/`): scratch = 69-entry base KB rebuilt with
   `kb_install` (FNV `a92e1031d460dbd9`, SHA-256 `1531fda8108d867e` —
   exact control match); informed = base + 5 prior-art entries (74
   entries, FNV `6af80e9355817834`).
3. **Learner** (`src/learner4.zag`): the tested loop learner (teach, gate,
   deliberative diagnose, all repair patches) **plus** a store-driven
   battery path — `gen <kb.dat> <spec>` scores `E-*` entries in-Zag and
   slot-fills the winner; `KB-MISS` sentinels on no-match. Same binary,
   same code path for both arms; only `kb.dat` differs.
4. **Driver** (`src/driver4.py`): deterministic plumbing only —
   compile/run/byte-compare/verifier dispatch/logging. Zero coding
   decisions (no diagnosis, no source edits, no repair choice); all of
   those live in the Zag learner.
5. **Teach audit**: the five prior-art entries were installed through the
   learner's `teach` (`logs/teach_audit.jsonl`, 5 `AUDIT op=INSTALL`
   records).
6. **Expected outputs** (`expected/`, `battery.json`): frozen from the
   independent oracle *before* scored runs; templates cross-checked
   byte-exact.
7. **Scored runs**: 2 arms × 5 items × 5 reps, budget 6 attempts/item.
   Canonical logs byte-identical across reps (verified with `cmp`).

## Kill/void conditions — all clear

- Scratch digest = `a92e1031d460dbd9` ✓ (comparison valid)
- No coding decisions in the driver (plumbing only; diagnosis/repair in Zag) ✓
- Canonical logs byte-identical across all 5 reps, both arms ✓
- Zero gate refusals on battery specs ✓
- Zero RNG in any decision path (pure Zag learner; Python is plumbing) ✓

---

## Limitations & judgment calls

1. **Reconstructed prereg** (see top): every "frozen" definition is
   reconstruction-frozen, not prereg-frozen.
2. **B1 check-count ambiguity:** the frozen text says "Checks (16)" with
   sanity "(4)" but lists five sanity conditions (v1==0; v2==8;
   v3,v5,v6 < 8·len). Implemented as 6+6+4=16, counting v1, v2, v5, v6
   (v3's inequality excluded as the weakest compression signal; v3 is
   still covered by its 12 round-trip/framing checks). Any other
   resolution changes q1's denominator.
3. **Scratch arm cannot attempt the tasks.** This is the honest behavior
   of a recall-based learner with no relevant idiom — it halts rather
   than confabulates. The gap therefore measures *necessity* of prior
   art for this architecture, not a graded skill difference. A learner
   with compositional synthesis might show a smaller gap; this trial
   does not test that.
4. **B3 quality < 1.0** is the mechanical `min(1, reduction/0.30)` term
   on p3 (28.6% < 30%), not a defect.
5. Templates were human-written prior art installed via `teach`; the
   trial measures recall+application, not de-novo invention.
6. Timing is wall-clock on shared lab hardware (informative only; not
   part of the canonical log or the gap metric).

## Provenance

- Pinned toolchain: `znc_linux_x86_64_abed8aa1`
- Base KB: 69 entries, FNV `a92e1031d460dbd9`, SHA-256 `1531fda8108d867e`
- Informed KB: 74 entries, FNV `6af80e9355817834`, SHA-256 `fba3a87ea12b66bb`
- Corpus: `corpus/entries.txt` (5 entries, 70,900 bytes)
- Spec: `TASK4_SPEC.md` (reconstruction — see warning)
- Battery: `battery.json`; expected: `expected/`
- Logs: `logs/canonical_<arm>_r<rep>.jsonl` (byte-identical ×5), `logs/summary_*.json`, `logs/teach_audit.jsonl`
- Learner: `src/learner4.zag` (built from `loop/learner.zag` + KB-store section via `src/build_learner4.py`)
- Driver: `src/driver4.py`; analysis: `src/analyze4.py`; oracle: `src/oracle4.py`
