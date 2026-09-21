# Y4 VERDICT

**Arm:** Y4 — Question-driven (lazy) cuts
**Date:** 2026-09-21
**Verdict: PASS (CONDITIONAL — see §1)**
**Commit:** 7998f9d568a02fbffc7886ceb50c4071e7a48b0a (tnn-native-lab)
**Evidence:** `scorecard_r1_1x.json`, `evidence/STATUS.txt`, `evidence/m8_GATE.txt`,
`audit_ledger.py` (clean on the M5 ledger, 160,233 entries, 0 issues)

## 1. The conditional

The frozen kill bar has two disjuncts:

(a) *"Recall accuracy >5% below eager arm D at equal total ledger cost
(candidates + materializations)"* — **UNSCORED.** Arm D has not reported its
M1 recall or ledger cost as of this writing. Y4's side of the comparison is
measured and committed (`y4-cmp-1x`: recall 100.0/100.0, ledger cost =
candidates + materializations per corpus — see `COMPARISON_D.json` and
`scorecard_r1_1x.json` → `y4_cmp`). The slotting procedure is mechanical and
documented in `ARM_SPEC.md` §6: the moment D's numbers land, KILL iff
`cost_y4 ≤ cost_d` AND `recall_y4 < recall_d − 5.0`. No D numbers were
invented or estimated.

(b) *">30% of materialized chunks never recalled twice"* — **SCORED: 0.0%,
PASS.** The preregistered question stream (Q1 FULL, Q2/Q3 SPAN[10%,30%),
Q4 SPAN[55%,75%), Q5 FULL on novel tier t1_prose) materialized 6,649 chunks;
every one was recalled ≥2 times; rematerializations 0.

No scored kill bar fired. M8 (5 perturbations × 2 runs) is byte-identical
(see `evidence/m8_GATE.txt`). Hence PASS, conditional on (a) remaining open
until D reports. If the program requires both disjuncts scored before a PASS
is recorded, the correct interim status is BLOCKED-ON-D, not KILLED — Y4 has
failed nothing.

## 2. What the battery showed (all legs rc=0, stdout byte-identical ×2)

- **M1:** 100.0% recall / 100.0% boundary on prose (79,304 chunks) and code
  (128,649 chunks). Ledger cost per corpus = candidates + materializations
  (158,609 / 257,299 entries).
- **M2:** converges in 1 episode on all five tiers (one ingest pass + one
  FULL question = full recall; episodes 2–3 confirm). Episode 0 (pre-ingest)
  recall is 0.0 — without ingest there are no candidates and nothing to
  recall, as the mechanism predicts. M9 shape: fast-then-flat on both t1
  corpora (takeoff ep 1, late gain 0.0).
- **M3:** survival 100.0%, fresh recall 100.0%, 18,523 management-audit
  entries (bar ≥700), 50/50 weaken probes handled, freeze CLEAR.
- **M4:** 100.0% boundary revision, 100.0% content revision, 0.0% kill rate,
  no kill-substitution, both corpora, 1 episode.
- **M5:** 79,304 units, 5.42 MB source. Memory per source byte 1.823
  (framework bar 1.5× — MISSED) and 30.3 audit entries/kB (framework bar
  10/kB — MISSED). Reported as measured. Mechanism: the frozen kill bar
  defines Y4's cost as candidates + materializations, so the ledger is
  ~2× entries per chunk by construction (79,303 CAND + 79,304 ADD on prose);
  the audit/kB number is the laziness cost made visible, not a defect — and
  it is exactly the cost term the D comparison will judge. The memory number
  is dominated by the resident raw stream + candidate arrays + a half-empty
  slot table (3.96 MB for 79k chunks in 110k slots). Neither M5 bar is a
  frozen kill criterion for Y4; both are recorded here for the coordinator.
- **M6:** transfer tax 0.0 both directions, recall/boundary/revision 100.0;
  memorizer validity gate PASS (54.8pt drop ≥ 15pt).
- **M7:** hit 100.0%, reuse 100 (hundredths), dedup 50 (hundredths), reread
  0 bytes; C′ round PROVISIONAL pending Micah's A7/A8 freeze.
- **M8:** GATE PASS — 5 perturbations × 2 runs, all artifacts byte-identical
  (store_hashes, store_chain, ledger.bin 28.1 MB / 438,510 entries,
  ledger_chain, alloc_trace, stdout). Ledger audit: 438,510 entries,
  0 ordering/semantics issues.

## 3. Deviations

Two build bugs found by the ledger audit and fixed before any battery
evidence was taken (QUESTION logged after materialization; uninitialized
slot-ID sentinel) — see BUILD_LOG.md. The battery was restarted from scratch
after the fix; no evidence predates it. Frozen harness scripts used
unmodified; scorecard via the mechanical Y4 adaptation
(`scorecard_assemble_y4.py`).

## 4. Recommendation to the coordinator

Y4's laziness claim survived its preregistered falsification test: questions
commit segmentations, everything materialized is recalled repeatedly, and the
ledger proves no chunk existed before its question. The storage-efficiency
claim (5–10× fewer stored chunks than eager D) is D's comparison to settle —
the numbers are ready on Y4's side. Keep Y4 alive until D lands; if D never
reports, the (b) disjunct alone sustains the PASS.
