# Utility Integration Report
## 2026-10-01 | Worker: Utility Integration (Micah Priority 6)

### Verdict: UTILITY-INTEGRATION-COMPLETE

Test 6 (redundancy) falsifies U-redundancy. Predictive utility connects to
learner-owned prediction success. Wrong-but-frequent case attacked.

---

## Experiment 1: Test 6 Redundancy (S2-style falsification)

**Claim:** U adds signal beyond bid+structure.
**Falsifier:** If U were redundant, U-order would match bid-order for MAP eviction.

**Design:**
- MAP A: promoted, used 10x (high U), aged 300 ticks (dormant).
- MAP B: promoted after aging, used 1x (low U), active (recent edges).
- Compare eviction order by U (ascending) vs by bid (ascending).

**Results (3/3 byte-identical per arm):**

| Arm | A (U, bid) | B (U, bid) | U-order first | Bid-order first | Verdict |
|-----|-----------|-----------|---------------|-----------------|---------|
| Fixed (ub) | (12, 2) | (3, 12) | B | A | DIFFER -> non-redundant |
| Predictive (ui) | (10, 1) | (1, 12) | B | A | DIFFER -> non-redundant |
| Control (no U) | (-1, 2) | (-1, 12) | tie | A | bid-only baseline |

**Interpretation:** In both U-arms, U orders B-before-A (low U evicted first),
while bid orders A-before-B (dormant evicted first). The orders are opposite.
U is not redundant with bid. The control arm (no U field) follows bid order,
confirming the baseline.

---

## Experiment 2: Wrong-but-Frequent Attack

**Design:**
- MAP W: promoted, queried 20x with ZERO observes (frequent, unverified/stale).
- MAP R: promoted later, queried 3x with correct observes (infrequent, verified).
- Compare U(W) vs U(R).

**Results (3/3 byte-identical per arm):**

| Arm | U(W) | U(R) | Rank | Pattern |
|-----|------|------|------|---------|
| Fixed | 22 | 5 | W > R | frequent wins |
| Predictive | 0 | 3 | R > W | verified wins |
| Control | -1 | -1 | tie | no U |

**Interpretation:** Fixed utility rewards USE (+1 per hit), so W (22) outranks
R (5) despite W never being verified. Predictive utility rewards CORRECT
PREDICTIONS (+1/-1 on resolve), so W (0, no evidence) ranks below R (3,
verified). The predictive variant correctly demotes the stale-but-frequent
structure.

**Note on supersession:** A MAP that is actively wrong on the same (s,r) gets
superseded after the first contradiction (type-3 self-edge), so sustained
wrongness cannot accumulate. The honest "wrong-but-frequent" case is
stale-but-frequent: use without verification. Fixed U cannot distinguish;
predictive U withholds reward without evidence.

---

## Mechanism: Predictive Utility

**Design decision:** MAP f12 is used for U by utility AND pred_score by
learner-success. The integration is natural: **U IS the prediction score.**

**Changes from fixed:**
- `promote_graph`: U=0 at birth (was +2). No trial bonus.
- `ev_query`: records PRED (tag-31) on shadow-FACT hit. No +1 for use.
- `ev_observe`: resolves PREDs. Correct -> U+=1. Wrong -> U-=1.
- Floor -8, ceiling +127 (unchanged). L updated on change (unchanged).

**Files:**
- `ui_pred.zag` (51 lines): PRED tag-31 mechanism.
- `ui_patch_pred.zag` (172 lines): predictive patches.
- `ui_util.zag` (230 lines): utility helpers (unchanged from ub).
- `ui_patch_ctl.zag` (98 lines): Test 6 control (no U).

---

## Standing Metrics

- **Researcher-owned decisions:** U update magnitudes (±1 predictive, +2/+1/-1/-2 fixed),
  FOSSIL_AGE=200, PRED tag-31 schema, battery designs (T6, WBF), activity model.
- **Learner-owned decisions:** U values (accumulated from experience), MAP promotions
  (via trial), eviction orders (computed from U/bid), prediction outcomes.
- **SUF:** Not measured in this worker (no LLM baseline).
- **Reuse/revision events:** MAPs reused via query hits (10x, 20x, 3x). No revision
  events in these batteries (supersession not triggered; WBF uses no-observe).
- **Cognition lines:** 697 (util 230 + pred 51 + patch_pred 172 + patch_ctl 98 + driver 146).
  Core files (ui_core_*) are verbatim base minus patched functions, not counted.
- **Modes/bridges/handlers/semantic cases:** 0. No new modes. No bridges. No
  task-specific handlers. No semantic cases. PRED is a generic mechanism.

---

## Honest Limits

1. **U is use, not truth (fixed).** A wrong-but-frequently-used MAP accumulates U.
   Predictive variant addresses this by requiring verification, but...
2. **Predictive U requires observes.** If the world never provides outcomes,
   U stays 0. This is honest (no evidence, no reward) but means unverified
   structures are indistinguishable from useless ones.
3. **FOSSIL_AGE=200 is scaffolded.** Not learner-adapted. (Inherited from utility build.)
4. **Supersession handles active wrongness.** The architecture already prevents
   sustained wrongness on one (s,r) via type-3 self-edges. The WBF attack targets
   the stale case, not the actively-wrong case.
5. **Test 6 uses simulated activity.** B's bid was boosted via direct link_edge
   to model "active vs dormant." A natural battery would derive this from
   real trial/query patterns.
6. **Does not bend DYN-1.** By design; decline/dedup is other workers' job.

---

## Reproducibility

- Base frozen TNN-2 SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
- Pinned compiler: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Binaries: `ui_tfixed_bin`, `ui_tctl_bin`, `ui_tpred_bin` (all exit 0)
- Transcripts: `ui_fixed_run{1,2,3}.txt`, `ui_ctl_run{1,2,3}.txt`, `ui_pred_run{1,2,3}.txt`
- All 3/3 byte-identical (sha256 verified).
- Safebin PATH active. `which python3` returns nothing. No contamination.

---

## Conclusion

Utility is now integrated with learner-owned predictive success. The fixed
+2/-2 bookkeeping is replaced by ±1 prediction-outcome updates to the same
U field. Test 6 falsifies redundancy. The wrong-but-frequent case is
addressed: predictive U ranks verified structures above stale ones, while
fixed U does the opposite.

**Verdict: UTILITY-INTEGRATION-COMPLETE**
