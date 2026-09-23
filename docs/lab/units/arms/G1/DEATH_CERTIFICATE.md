# G1 Death Certificate

**Arm:** G1 — Pressure-driven coarsening (family CUT)  
**Date:** 2026-09-21  
**Verdict:** KILLED  
**Fired criterion:** (iii) Junk fusion — "if ≥ 10% of superchunks are never recalled *nor* re-split (dead weight created by triage) → G1 dies."

## Evidence

**Run:** M3 (1x), frozen schedule: 1000 valuable (pinned) + 3000 fresh ingest / 3000 kill / 50 weaken / 4000 fresh ingest. Store capacity: 4000 slots (harness-fixed, G1_M3_CAP).

**Triage activity:**
- Phase 1 (3000 ingests on 1000 valuable): occupancy hit 95% (3800/4000), triage fired.
- Total triage merges (n_sup_create): 2404
- Live superchunks at end: 1102
- Superchunks ever recalled (F_TOUCH via g_recall): 0
- Superchunks ever re-split (deliberate revision): 0

**K3 calculation:**
- Untouched superchunks: 1102 / 1102 = 100%
- Threshold: ≥ 10%
- 100% ≥ 10% → **K3 FIRES**

**Other criteria (for the record):**
- K1 (thrash): 0 re-splits / 2404 superchunks = 0% < 5% → no fire.
- K2 (value-blindness): pinned recall 100.0% (1000/1000), control 100.0% (1000/1000), drop 0.0% ≤ 1% → no fire.
- M3 freeze: survival 100.0%, fresh recall 94.6%, mgmt 18590 (≥700), weaken 50/50 → no freeze.

## Mechanism analysis

The G1 implementation faithfully follows the frozen spec (ALPHABET_G-L.md §G1):
- At CRITICAL (95%), triage merges lowest-(value, slot) adjacent unpinned pairs.
- Pinned chunks immune; negative-value first; 2× mean cut policy under pressure.
- Bytes preserved in append-only corpus; OP_MERGE audits linkage/cut points.

Under M3's pressure (cap=4000, peak 4000 live), triage created 2404 superchunks from low-value fresh data. The M3 probe (per frozen schedule) recalls valuable (pinned, never merged) and fresh units by original serials. Merged fresh units' serials are dead (constituents killed by merge); recall does not follow merge linkage. Superchunk serials (new IDs) are never recalled by the probe. No deliberate revision occurs in M3.

Result: 1102 superchunks persist, containing the compressed fresh data, but nothing recalls or re-splits them.

## Ambiguity logged

**A1 — Probe vs arm defect:** The frozen M3 schedule does not specify recalling superchunk serials or following merge linkage on recall. K3 fires because the probe never exercises superchunks, not necessarily because the superchunks are "junk." The superchunks contain valid compressed data (byte-exact, reversible via re-split). A test that recalled superchunk serials (from OP_MERGE ledger entries) would touch them. Interpreted literally per prereg, K3 fires. Whether this reflects arm defect or probe gap is ambiguous.

**A2 — Denominator:** K3 says "≥10% of superchunks." Used live superchunks (1102) as denominator; total ever created (2404) gives the same result (100% untouched). No denominator minimum invented.

**A3 — Per-run vs arm-level:** K3 evaluated on the M3 run where superchunks were created. If evaluated arm-level across all runs, M4 (deliberate revision) might re-split some, but M3's 1102 untouched still satisfy "≥10%... never recalled nor re-split" for that run.

## Conclusion

Per the frozen kill criterion interpreted literally, G1 is KILLED. The pressure-driven coarsening mechanism works as specified (triage fires, merges are byte-exact, pinned data protected), but under the M3 churn schedule it accumulates superchunks that are never recalled nor re-split, meeting the junk-fusion kill bar.

**No 10x run.** Promotion stopped.
