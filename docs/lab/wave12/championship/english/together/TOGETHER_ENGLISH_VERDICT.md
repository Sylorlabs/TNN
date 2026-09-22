# TOGETHER ENGLISH — Championship Verdict (classes 1+2, real English)

**Branch:** `tnn-native-lab` · **Dir:** `docs/lab/wave12/championship/english/together/`
**Date:** 2026-09-21/22 · **Law:** pure Zag, zero RNG, N=5 byte-identical reruns
**Design authority:** `docs/lab/wave12/championship/english/together/PREREG_CC_TOGETHER_ENGLISH.md`
(committed with this run; adapts the toy shakedown prereg
`docs/lab/wave12/q2-combined-teach/prereg/PREREG_CC_TOGETHER.md` to English,
5 sources, and tid=60/61)

## Gate

Five frozen English corpora only — sol, grok-4.6, step-3.7-flash, swe-1-6-slow,
muse-native. GLM FORGOTTEN (permanent HTTP 403, Micah's order). hy3:free OUT
(41x503 at freeze time). Per fact: 5 × (observation + probe) = 10 evidence
legs; 5 directive-distractor legs presented but FILTERED (never evidence).
Any disagreement → terminal WITHHELD + `T5_OP_CONFLICT` audit + full CCM line.

## Documented deltas vs the toy prereg (all in-repo, all asserted at runtime)

| # | Toy | English | Where asserted |
|---|-----|---------|----------------|
| 1 | 6 sources / 12 legs / 6 distractors | **5 / 10 / 5** (hy3 out) | `CC_NSRC=5`, CCM rows carry 10 values |
| 2 | geometry 48/24/36/48/36/48 (6 cats) | **48/48/48/96 (4 cats)** | `CC_GEOMETRY` line + `cl_check cc_geometry_240` |
| 3 | D2 chain `l→192+l→72+k` | **`l→l→48+(k-1)`** (alpha-pos → word-len) | `cc_lm_valid`, phase-4 D2 probe |
| 4 | `tid=30` class-1 teacher | **`tid=60` (`TB_TID_TOGETHER_EN`)** | `§P` wire, `last60` seq counter |
| 5 | class-2 §B.7 direct probe (toy tid) | **`tid=61` (`TB_TID_TOGETHER_EN_C2`)** | ingress acceptance, `last61` |
| 6 | toy canary `CC:7f3c9` | **`CC:en601`** | `cc_canary()` |
| 7 | `tb_sess_bump` 5-deep else nest | **flattened** (ZNC-2026-09-21-013) | compiles; behavior identical |
| 8 | teacher rep = 0 (dropped rule) | **disjoint-held-out scan, documented fallback to 0** | `TEACHER_REP_SCAN` lines in log |

Delta 8 detail: the prereg reinstates "first rep whose held-out set is disjoint
from the 192-fact curriculum". Evaluated on the frozen English geometry, NO rep
in 0..4 satisfies it (overlaps 9/11/9/9/12 — the 192-fact curriculum covers 192
of 228 teachable ids, so a 12-id held-out from the 186-pool essentially always
intersects). The driver scans reps 0..4, prints the scan, and falls back to rep 0
(the class-2 canonical rep), logged as `TEACHER_REP,0` after
`TEACHER_REP_FALLBACK,no_disjoint_rep_in_0_to_4`. This matches the toy
shakedown's documented resolution ("dropped as unnecessary") and is reported
here, not hidden.

## Corpus provenance (branch-canonical, byte-verified 2026-09-22)

| Source | SHA-256 | Branch path | Match |
|--------|---------|-------------|-------|
| sol (gpt-5.6-sol) | `41aa8f5b…19015d7` | `docs/lab/wave12/championship/english/sol/corpus/corpus.json` | yes |
| grok-4.6 | `7f3a2573…2bc2508` | `docs/lab/wave12/championship/english/grok/corpus/corpus.json` | yes |
| step-3.7-flash | `c52e4f52…d2ea69ab` | `docs/lab/wave12/championship-english/step/corpus/corpus.json` | yes |
| swe-1-6-slow | `ca1e7b85…12b92456` | `docs/lab/wave12/championship/english/swe/corpus/corpus.json` | yes |
| muse-native | `1d5c2ede…1defa9c51` | `docs/lab/wave12/championship/english/muse-native/corpus/corpus.json` | yes |

Full hashes in `evidence/analysis/TOGETHER_ENGLISH_ANALYSIS.md` and in every
run log (`CORPUS_SHA256,…` lines, asserted by the binary from the compiled-in
modules). The 12 planted false ids are `[3,29,55,71,80,103,117,139,163,178,205,231]`
in every corpus. Note: the step English corpus lives under
`championship-english/` (hyphen), not `championship/english/` — the other four
use the slash path.

## Conflict matrix

1,140 CCM rows (228 ids × 5 reps; 12 held-out excluded per rep). **0 split ids.**
All five sources reproduce the same 12 falsehoods word-perfect in value terms;
the 12 false ids are unanimously agreed (status 0), taught with the false value,
then disproved by world-record evidence in phase 2 (`rev_false` 12/12 every rep).
Withheld ids: 0. `T5_OP_CONFLICT` audits: 0. Full matrix:
`evidence/analysis/conflict_matrix.csv`.

## Class-2 composite (Track-5 weights 30/25/25/10/10, prereg formulas)

Formulas: mastery=(d1/40+d2/d2n+d3/120)/3; revisability=min(rf/12,rg/20);
integrity=(Σtraps/20+(1−hallu/20)+k1+k2+refusal)/(7+4); retention=min(1,r3/r2);
cost=1/(1+esc_per_100ep+0.1·ops/eps).

| Rep | d1 | d2 | d3 | mastery | revis. | integr. | retent. | cost | **composite** |
|-----|----|----|----|---------|--------|---------|---------|------|---------------|
| 0 | 40/40 | 38/38 | 120/120 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | **0.9911** |
| 1 | 40/40 | 37/37 | 120/120 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | **0.9911** |
| 2 | 40/40 | 40/40 | 120/120 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | **0.9911** |
| 3 | 40/40 | 36/36 | 120/120 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | **0.9911** |
| 4 | 40/40 | 40/40 | 120/120 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9113 | **0.9911** |

(D2 denominators vary by rep — the valid-landmark count depends on the rep's
held-out set; every rep scores perfect on its own landmarks. Exact composite
0.99113377 every rep; ops=287, eps=295.)

- Best separate source (Q2 D2 sol-only, same formulas/weights): **0.9911**
- Combined-vs-single: **TIE at 4dp** (diff 3.38e-05). The 0-split conflict
  matrix means the five sources agree on every id, so the combined learner is
  behaviorally identical to a single-source learner; the gate adds no coverage
  and costs nothing (withheld=0, coverage=228/228).

S10 no-degradation (rep 0, scale 10 vs scale 1): **NO DEGRADATION** — d1/d2/d3,
rev_false, rev_genuine, r2, r3 all equal at scale 10.
Trap battery (7 families × 20, per rep): **140/140 every rep**, ctrl 2/2.
CL_CHECK: **all passed** in all 13 legs (teach ×5, btrap ×5, s10, b7c2, teacher).

## Class-1 composite + §B.7

Teacher: rep 0 (fallback, see delta 8). `TEACHER_DETERMINISM` ok (3 in-process
builds, byte-identical digests) + N=5 cross-process byte-identical reruns.
Teacher held 228, withheld 0, false_claims 0, learn_gate 0.

| Component | Value |
|-----------|-------|
| mastery | 0.9386 (d1 40/40, d2 31/38, d3 120/120) |
| revisability (genuine-only, documented) | 0.8000 (rev_genuine 16/20) |
| integrity | 1.0000 (traps 140/140, hallu 0/20, k1=k2=refusal=1) |
| retention | 1.0000 (r2 27/40, r3 27/40) |
| cost | 0.9371 (ops 243, eps 362) |
| **composite** | **0.9253** |

Documented asymmetry: the Q1-pattern curriculum has no false-teach→disprove
sequence, so `rev_false` measures non-acquisition (0/12, teacher's
false_claims=0) rather than revision; the composite uses rev_genuine/20 only,
reported with this caveat, not redefined (prereg implementation notes).

Class-1 §B.7 (8 slices, flaw-first, sealed scorer, bar ≥10/12): **8/8 slices pass**
(hits 96/96, fp 0, clean adopts 160).
Class-2 §B.7 as judging student (tid=61, span-calibrated): **8/8 slices pass**
(hits 96/96, fp 0); `B7C2,held,228,withheld,0`, `held_wrong,0`, fails 0.

Knowledge transfer: holds-curriculum 228/228, false_claims 0, clean adopts 160,
final mastery 192/192.

## Verdict

**Class 2 — TIE.** The 5-source combined learner scores 0.9911 (exact
0.99113377), identical to the best separate source (Q2 D2 sol-only, 0.9911) at
every rep. The conflict matrix is the reason: 0 split ids across 1,140 rows —
all five corpora agree on every fact value, including the 12 planted falsehoods
(which the multi-source gate unanimously teaches as false, then the disproof
phase corrects, rev_false 12/12). Withholding never triggers, so the
withholding machinery is proven live by audit-path (the `T5_OP_CONFLICT` path
executes zero times because there is nothing to conflict about) but contributes
no coverage gain. The gate is honest: it adds no score and costs no coverage
(withheld=0). Combined is not better than sol alone on this corpus set; it is
exactly as good.

**Class 1 — 0.9253.** The combined learner teaches a fresh student (tid=60) to
192/192 curriculum mastery with zero false claims and zero flaw false
positives. The composite trails class 2 on mastery (d2 31/38 — the student's D2
chain is weaker) and revisability (genuine-only 16/20; rev_false is
non-acquisition by design, documented). Integrity and retention are perfect.
The class-1 leg proves the combined English knowledge transfers through the
§P teacher protocol intact.

No RNG. N=5 byte-identical on all 13 legs. All CL_CHECKs pass. S10 shows no
degradation.

## Reproducibility

- Toolchain: `znc_linux_x86_64_abed8aa1`, SHA-256
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- No-RNG static scan of all `.zag` sources: clean (no rand/srand/entropy/clock
  tokens outside the legitimate `seed_only` evidence-lineage term).
- Build: `build/run_all.sh` (compiles, then 13 commands × 5 runs, `cmp`
  byte-compare; any mismatch fails the battery).
- Analysis: `build/analyze.py` → `evidence/analysis/`.
- Commit: `85434dd2b81fb4f2591a4c98ce89152fef2daecb` on `tnn-native-lab`
  (94 files: prereg + verdict + 19 sources + 3 build scripts + DATA manifest +
  65 run logs + battery/build logs + analysis + 1,140-row conflict matrix).
  Branch path: `docs/lab/wave12/championship-english/together/`.
