# MEM8_RESULT.md -- H-MEM8 builder result: BUILD-PASS

Verdict label: **BUILD-PASS** (builder report only). Under the 2026-09-29
reorientation, builders report BUILD-PASS/BUILD-FAIL and do NOT promote
to SURVIVES. Frontier promotion (SURVIVES/BOUNDED/DOWNGRADED/KILLED)
requires the full pipeline: independent reproduction, baseline attack,
OOD test, ablation, transfer, independent adversary. This document
reports that the frozen prereg bars were met as specified; it does not
claim a frontier verdict.

Classification under the 2026-09-29 finding taxonomy:
- X-M7-3 (short-window preservation lemma false): **CRITICAL REPAIR**.
  The frozen "preserved by construction" claim was wrong for nq < 20;
  a frozen claim was corrupted. Repaired by the uniform lemma (R7b).
- X-M7-2 (merit/harm inversion): **BOUNDED EDGE**. The inversion is
  bounded by theorem (<= 4), non-destructive, and outside the major
  claim. Documented with a proven bound; move on.
- R7a (harm unification): **negative evidence**. Tested, rejected for
  breaking frozen K-M2-5. Not adopted. Preserved here so no future
  worker re-tests it blind.

This is a targeted repair of red-team downgrades, not an automatic
vN+1 treadmill step.

## 1. What was built

H-MEM8 (R7b) = H-MEM7 (R6) with ONE mechanism change: decmerit()
weights are top-aligned (measured from the present) instead of
bottom-aligned (measured from the window start). Weight(i) =
win - (nq-1-i). For nq >= 20 this is arithmetically identical to R6.
For nq < 20, recency is history-length-invariant. All other code
(elig, winuses, replay_cost, victim, pressure, all fixtures) is
unchanged. MTHRESH=25, win=20 unchanged.

Source: mem8_learn.zag (md5 696cfb780a991413a8c4cbfe17e85973 for the
copied base; modified as specified in PREREG_MEM8.md section 3).

## 2. Frozen bars and outcomes

Prereg: PREREG_MEM8.md, committed alone at 3314b8c240 BEFORE any
implementation existed. The prereg commit is a strict ancestor of
the implementation (verified below).

### K-M8-1a: short-window fresh pair protects (X-M7-3 repair)

Frozen expectation: nq=9, seq=9, decmerit(slot7)=39, elig=0.
Observed: "short-window pair: nq=9 seq=9 decmerit(slot7)=39 elig=0".
K-M8-1a PASS. The X-M7-3 instance (which read 8+9=17, evictable,
under R6) now reads 19+20=39, protected. The uniform age-window
lemma holds for the downgrade instance.

### K-M8-1b: short-window single newest query does NOT protect

Frozen expectation: decmerit(slot7)=20, elig=1.
Observed: "short-window single: nq=9 seq=9 decmerit(slot7)=20 elig=1".
K-M8-1b PASS. The "single query is never merit" principle holds
uniformly in short windows (max weight 20 < 25).

### K-M8-2: inversion bound (X-M7-2 fixture, reconciled)

Frozen expectation: decmerit(slot7)=25, elig=0, decmerit(slot0)=21,
elig=1, winuses(slot7)=2, winuses(slot0)=6, LFU protected victim
slot0, LFU unprotected victim slot7, replay_cost 6 and 2,
(6-2)<=4, decmerit(slot7)>decmerit(slot0), both age-open.

Observed:
"inversion: decmerit(slot7)=25 elig=0 decmerit(slot0)=21 elig=1"
"harm: winuses(slot7)=2 winuses(slot0)=6 LFUvp=slot0 LFUvu=slot7 c0=6 c7=2"
K-M8-2 PASS. The count-scale inversion (2 < 6) materializes exactly
as the red team measured (honest, not hidden). The theorem bound
holds: 6-2=4 <= 4. The mass scale is not inverted: 25 > 21. Both
slots age-open (seq=105 < prot=109, verified in-code).

### K-M8-3: regression

Frozen expectation: diff(MEM8_RAW_OUTPUT.txt, MEM7_RAW_OUTPUT.txt)
shows EXACTLY the MEM7 trailing "ALL BARS PASS" replaced by the
K-M8-1a, K-M8-1b, K-M8-2 sections and "ALL BARS PASS". No other
differences.

Observed: diff yields exactly one hunk, 222,231d221 (10 added
lines: the three K-M8 sections). Zero other differences across all
222 inherited lines. K-M8-3 PASS. This confirms the frozen
arithmetic fact (R7b = R6 for nq >= 20) empirically: every inherited
fixture has nq >= 20, and none changed.

### K-M8-4: determinism

Three consecutive runs: byte-identical
(md5 b4346f800d3d5cb343b73b8f07fcc59c x3), exit 0, zero FAIL lines
(grep -c FAIL = 0), 30 PASS lines (vs 27 in MEM7, the 3 new bars).
K-M8-4 PASS.

## 3. Methodology

- Pure Zag: no Python anywhere (editing via file tools, build via
  znc, verification via shell diff/cmp/md5sum/grep). Scratch
  pre-freeze work used only the Zag compiler and shell in /tmp.
- Toolchain: /home/hatch/workspace/tnn-forkbattery-1121pdt/
  local-tnn-native-lab/znc, version znc 2026.07.0-dev
  (edition 2026).
- Build: `znc build mem8_learn.zag -o /tmp/mem8scratch/mem8`
  (214430 bytes main, 0 external tools).
- Runs: three consecutive executions, stdout captured, md5sum
  compared.
- Regression: `diff` against the frozen MEM7_RAW_OUTPUT.txt
  (md5 79fdc6eea90c8ed9c019e6893e693bba).

## 4. Raw evidence

- MEM8_RAW_OUTPUT.txt (md5 b4346f800d3d5cb343b73b8f07fcc59c).
- mem8_learn.zag (source).
- PREREG_MEM8.md (frozen prereg, commit 3314b8c240).
- This file (MEM8_RESULT.md).

## 5. Failures and negative evidence

- R7a (harm = decmerit, full unification): tested in /tmp scratch
  (not committed), REJECTED. It broke frozen K-M2-5 (C2-ev0 winner
  FIFO->LRU) and dissolved F-M6-3b's :1 path. Documented in
  PREREG_MEM8.md section 6 and in the replay_cost() source comment.
  Do not re-test without newly frozen bars.
- R7b alone (top-aligned only): byte-identical to MEM7 on the
  inherited suite (pre-freeze scratch, md5 match). Confirmed again
  in the committed run (K-M8-3).
- No implementation failures. No bar was weakened or redefined.

## 6. Boundaries (what H-MEM8 does NOT claim)

- Classification remains bounded L2. No mechanism here establishes
  L3. The menu, the operating window, MTHRESH, and the linear decay
  weights are authored. The uniform lemma is a property of the
  authored weighting, not a learner invention.
- The merit/harm split is reconciled (bounded, principled), not
  unified. The X-M7-2 narrowing stands: the "strict improvement over
  the count cliff" reading is bounded by the theorem (<= 4).
- The red team's arithmetic slip is noted (PREREG_MEM8.md section 1):
  the X-M7-3 fresh-pair boundary under R6 is nq >= 13 (2nq-1 >= 25),
  not nq >= 20. The downgrade stands regardless; R7b eliminates the
  boundary entirely.

## 7. Causal interpretation

- X-M7-3 repair: bottom-aligned weights made recency
  history-length-dependent (the newest query weighed nq, not 20).
  Top-alignment anchors recency to the present, making the
  age-window lemma uniform. The cause was the weighting's reference
  point, not the threshold.
- X-M7-2 reconciliation: protection merit is forward-looking
  (recency predicts future activity); replay harm is backward-looking
  (literal re-learn count). The inversion is a yardstick mismatch,
  bounded by theorem (<= 4) because protection requires >= 2 queries
  (mass >= 25 needs 2) and evictability caps in-window count at 6
  (7 queries have mass >= 28 > 25). On the forward scale, protection
  is monotone (shields higher mass).

## 8. Governance disclosures

- Pure Zag: verified. No Python in editing, build, verification, or
  scratch. The pre-freeze scratch used only znc, shell, diff, cmp,
  md5sum, grep in /tmp.
- Prereg commit (3314b8c240) contains ONLY PREREG_MEM8.md and
  strictly precedes the implementation. Verified by git log order
  below.
- No frozen bar was weakened or redefined. The R7a rejection
  preserves K-M2-5.
- No em dashes in PREREG_MEM8.md, mem8_learn.zag, or this file
  (verified by byte grep for U+2014).
- Commits are local (tnn-native-lab). Nothing pushed without
  Micah's explicit approval. Only explicitly owned paths committed
  (PREREG_MEM8.md; then mem8_learn.zag + MEM8_RAW_OUTPUT.txt +
  MEM8_RESULT.md). No broad staging. No index.lock was removed.
- The red-team adversary executable was not re-run by this builder;
  K-M8-2 re-implements the X-M7-2 fixture from the frozen adversary
  prereg text (PREREG_MEM7_ADV.md). Independent red-team review of
  H-MEM8 is still required before any frontier verdict.

## 9. Commit lineage

- Prereg: 3314b8c240 "Prereg: H-MEM8 ..." (PREREG_MEM8.md only).
- Implementation + evidence: [this commit] "H-MEM8 BUILD-PASS ..."
  (mem8_learn.zag, MEM8_RAW_OUTPUT.txt, MEM8_RESULT.md).
- Ancestry: 3314b8c240 is a strict ancestor (git merge-base
  verification in the commit message / log).

## 10. What remains (not this builder's job)

- Independent reproduction of H-MEM8.
- Baseline attack and OOD test of the uniform lemma.
- Ablation of top-alignment (R6 vs R7b on short-window tasks).
- Transfer (does the uniform lemma matter for a downstream task?).
- Independent adversary review of H-MEM8.
- Only after those: a frontier verdict (SURVIVES/BOUNDED/
  DOWNGRADED/KILLED).
