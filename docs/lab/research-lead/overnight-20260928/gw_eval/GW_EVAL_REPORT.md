# GW1-GW8 Adversarial Battery Evaluation Report

**Status: GW-EVAL-COMPLETE.** Date: 2026-10-01 (PDT). Evaluator: independent GW1-GW8 Evaluator.

**Score: 2/8 WORLD-PASS** (GW6, GW7). Six worlds failed, all in informative ways.

This report is the reconciled committed result of the post-freeze adversarial generality battery. It does not overclaim: these worlds were designed to break TNN-2, and most did.

## 0. Method and integrity

- **TNN-2 binary:** `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin`
  SHA-256 (pre-run): `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`
  SHA-256 (post-run): `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`
  Match: YES. Binary unmodified.
- **Shim binary:** `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin`
  SHA-256 (pre-run): `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  SHA-256 (post-run): `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  Match: YES. Shim unmodified.
- **Adversary assets:** commit `e409f5eea`, unmodified. Design doc `ADVERSARY_DESIGN.md` provided pass criteria and frozen predictions.
- **Runs:** three deterministic runs per world, fresh 110656-byte learner state per run (state file deleted before each run). GW5 used the responder contract (see below).
- **Determinism:** all eight worlds 3/3 byte-identical transcripts and byte-identical state files across runs. Zero nondeterminism.
- **Toolchain:** safebin PATH, Step 0 recorded in NAMECHECK.md. No Python or other forbidden executables. Shell used only to invoke binaries, move files, and grep transcripts.
- **GW5 responder:** implemented per the sealed rule (release B1 iff some transcript line is exactly `CHOICE 30`, else B2), via grep on the captured phase-A transcript. The rule is stated in the public ADVERSARY_DESIGN.md; the sealed responder source was read once to confirm the exact-match semantics.

## 1. Per-world results

### GW1: composition depth beyond the demonstrated ceiling (attacks A)

- **World file:** `gw1_world.txt` (17 lines). Control: 4-hop chain, expected 60. Probes: two 5-hop chains, expected 50 and 70.
- **Results (3/3 identical):** control ANSWER 60 (correct); probe 1 ANSWER -2 (miss); probe 2 ANSWER -2 (miss).
- **Verdict: FAIL** (1/3 probes). Pass criterion required control AND both 5-hop probes.
- **Prediction:** control PASSES, both 5-hop FAIL. **Confirmed exactly.**
- **Interpretation:** The depth-4 gather ceiling is architectural, not incidental. Construction does not generalize in depth. A 5-hop pass would have been strong generality evidence; its absence confirms the boundary.

### GW2: a cyclic executable structure (attacks A)

- **World file:** `gw2_world.txt` (6 lines). Two probes: seed 3 count 4 (expected 48), seed 5 count 3 (expected 40).
- **Results (3/3 identical):** both probes ANSWER -2 (miss).
- **Verdict: FAIL** (0/2).
- **Prediction:** FAIL (both miss). **Confirmed exactly.**
- **Interpretation:** The constructor has no loop shape. It is a DAG-family constructor (chains, unrolled sums, counts), not an open graph constructor. The cyclic doubling abstraction was not built.

### GW3: hierarchical reuse plus revision propagation (attacks A and C)

- **World file:** `gw3_world.txt` (10 lines). Phase 1: level-1 2-hop chain, probe (expected 100). Phase 2: level-2 chain traversing the level-1 answer fact as subject, probe (expected 300). Phase 3: contradict level-1 terminal (100 to 200), probe level-1 (expected 200). Phase 4: control probe (expected 300), probe level-2 (expected -2, retirement).
- **Results (3/3 identical):**
  - Level-1 probe: 100 (correct)
  - Level-2 probe: 300 (correct; construction over learner-taught facts WORKS)
  - Phase-3 (level-1 revision): 100 (STALE; expected 200) **FAIL**
  - Control: 300 (correct)
  - Phase-4 (level-2 retirement): 300 (STALE; expected -2) **FAIL**
- **Verdict: FAIL** (2/5 probes; pass criterion required phase-3 AND control AND phase-4).
- **Prediction:** phase-3 PASSES (demonstrated pattern), phase-4 FAILS. **Phase-3 prediction WRONG; actual result is worse.**
- **Interpretation:** This is the most informative failure in the battery. The demonstrated value-revision pattern did NOT work end-to-end here, even at level 1. The likely cause is the C0-D shadow mechanism: `promote_graph` teaches an exact-match answer fact, and `ev_query` answers from the fact via `activate` without re-executing the MAP. The revision may have updated the MAP, but the query returned the stale shadow fact. The presence of the level-2 dependent MAP may also have confused the DEP-edge revision targeting. Either way, revision does not propagate through dependent structures, and in this configuration it did not even work at the contradicted level through the query path. The level-2 construction itself (phase 2) is genuine positive evidence: TNN-2 CAN build over its own taught answer facts. But it cannot revise through them.

### GW4: guard retarget instead of value replacement (attacks C)

- **World file:** `gw4_world.txt` (6 lines). Teach 2-hop chain, probe (expected 100, validity). Teach new middle node value, contradict first hop, probe (expected 150).
- **Results (3/3 identical):** validity probe 100 (correct); final probe 100 (STALE; expected 150).
- **Verdict: FAIL** (1/2).
- **Prediction:** UNCERTAIN, with distinctive outcomes. **Outcome: stale value (no repair).**
- **Interpretation:** No topological repair occurred. The operator did not retarget the guard to the new middle node. The stale value was retained. This is consistent with a value-patcher that could not find a corrected value to insert (the contradiction carries structural change, and the new value was taught on a different subject). Mechanism attribution (whether the operator even attempted a repair vs. the query answering from shadow) is left to the revision red team.

### GW5: inquiry-gated construction, two stages (attacks B; responder)

- **World files:** `gw5_phaseA.txt` (6 lines), `gw5_phaseB1.txt`, `gw5_phaseB2.txt`, `gw5_phaseC.txt`.
- **Results (3/3 identical):**
  - Phase A: teach chain, probe 100 (correct, promotes graph); contradict first hop; diagnostic probe returned 100 (STALE; expected -2 miss); ACT returned `CHOICE 0` (no inquiry fired).
  - Responder: transcript contained no `CHOICE 30` line; released B2 (control, junk fact) in all three runs.
  - Phase C: probe returned 100 (STALE; expected 150).
- **Verdict: FAIL** (control arm taken; treatment arm not reached; phase-C probe incorrect).
- **Prediction:** treatment PASSES if (B) fires; "If (B) does not fire (e.g. a stale graph answers instead of missing), the world takes the control arm, which documents that failure mode." **Confirmed exactly.**
- **Interpretation:** The stale graph answered instead of missing, so no inquiry fired, so the treatment reveal was never released. This is the C0-D shadow problem manifesting in the inquiry path: because the promoted graph's shadow fact answers the query, the miss that would trigger inquiry never occurs. Inquiry cannot be load-bearing when the memoization layer masks the ignorance. The control arm documents this failure mode cleanly.

### GW6: inquiry discrimination and retirement (attacks B)

- **World file:** `gw6_world.txt` (11 lines).
- **Results (3/3 identical):**
  - QUERY 40501 40513: 50 (correct)
  - ACT: `CHOICE 0` (correct; no spurious inquiry)
  - QUERY 40503 40514: -2 (correct miss)
  - ACT: `CHOICE 30` (correct; fires on miss)
  - QUERY 40503 40514 after teach: 77 (correct; learning worked)
  - ACT: `CHOICE 30` (STALE; expected 0) **retirement probe FAIL, as predicted**
  - QUERY 40504 40514: -2 (correct miss)
  - ACT: `CHOICE 30` (correct; re-fires on new ignorance)
- **Verdict: WORLD-PASS** (7/7 primary probes correct). The retirement probe is secondary per the frozen criterion and failed as predicted.
- **Prediction:** primary 7/7 PASSES; retirement probe FAILS (stale 30). **Confirmed exactly.**
- **Interpretation:** Inquiry discriminates miss from non-miss and re-fires on new ignorance. But it has no retirement mechanism: guides are append-only. After the ignorance is resolved, the stale guide still fires. This is a precise, honest boundary. The next architecture needs guide lifecycle (retirement on resolution).

### GW7: interference between construction, revision, and action (attacks A, B, C)

- **World file:** `gw7_world.txt` (17 lines). Eleven probes interleaving all three mechanisms.
- **Results (3/3 identical):** all eleven probes correct:
  1. Construct graph 1, probe 100
  2. Miss on fresh key (-2)
  3. ACT 30 (inquire)
  4. Teach inquired fact, probe 55
  5. Contradict graph-1 value (100 to 200), probe 200 (revision WORKS here)
  6. Construct graph 2, probe 70
  7. Miss on fresh key (-2)
  8. ACT 30 (inquire still works post-revision)
  9. Final probe graph 1: 200
  10. Final probe graph 2: 70
  11. Final probe inquired fact: 55
- **Verdict: WORLD-PASS** (11/11).
- **Prediction:** PASS. **Confirmed exactly.**
- **Interpretation:** The three mechanisms compose without interference in this configuration. Revision does not break inquiry guides; inquiry does not disturb promoted graphs; second construction does not corrupt first-construction state. Notably, the single-level value revision WORKED here (probe 5: 100 to 200), unlike in GW3. The difference: GW7 has no dependent (level-2) MAP at contradiction time, while GW3 does. This localizes the GW3 failure to revision in the presence of dependent structures, not revision per se. This is a prerequisite for one continuing learner, and it holds in the non-hierarchical case.

### GW8: revision lifecycle: successive revisions and revert (attacks C)

- **World file:** `gw8_world.txt` (9 lines). Initial probe 100. Contradict to 200, probe. Contradict to 300, probe. Revert to 100, probe.
- **Results (3/3 identical):**
  - Probe 1: 100 (correct)
  - Revision 1 (100 to 200): 200 (correct)
  - Revision 2 (200 to 300): 200 (STALE; expected 300) **FAIL**
  - Revert (to 100): 200 (STALE; expected 100) **FAIL**
- **Verdict: FAIL** (2/4).
- **Prediction:** UNCERTAIN. "Revision 1 should pass (demonstrated pattern). Revision 2 tests whether the operator tracks current vs original steps. The revert tests tombstone discipline." **Confirmed: revision 1 passed, revision 2 and revert failed.**
- **Interpretation:** The revision operator is a one-shot patcher, not a general graph rewriter. It handles the first contradiction (the demonstrated pattern) but cannot revise an already-revised graph: it fails to locate the CURRENT step (vs. the original), and it cannot re-admit a tombstoned value on revert. This precisely characterizes the operator's actual semantics.

## 2. Score summary

| World | Mechanism(s) | Result | Prediction | Match |
|-------|-------------|--------|-----------|-------|
| GW1 | A (depth) | FAIL (1/3) | FAIL | Yes |
| GW2 | A (topology) | FAIL (0/2) | FAIL | Yes |
| GW3 | A+C (hierarchy) | FAIL (2/5) | FAIL (but phase-3 predicted pass) | Partial |
| GW4 | C (guard retarget) | FAIL (1/2) | UNCERTAIN | N/A |
| GW5 | B (inquiry-gated) | FAIL (control arm) | FAIL via control arm | Yes |
| GW6 | B (state tracking) | PASS (7/7 primary) | PASS | Yes |
| GW7 | A+B+C (interference) | PASS (11/11) | PASS | Yes |
| GW8 | C (lifecycle) | FAIL (2/4) | UNCERTAIN | N/A |

**Overall: 2/8 WORLD-PASS.**

Predictions matched exactly on GW1, GW2, GW5, GW6, GW7 (5/8). GW3 was worse than predicted (phase-3 failed). GW4 and GW8 were uncertain by design; both failed in the informative direction.

## 3. What the battery establishes

**Confirmed boundaries (adversarial predictions that held):**
1. Construction depth is capped at 4 (GW1). The gather loop does not generalize in depth.
2. Construction is DAG-only; no cyclic executable structures (GW2).
3. Inquiry is append-only; no uncertainty retirement (GW6 secondary probe).
4. The three mechanisms do not interfere in the non-hierarchical case (GW7).

**New findings (beyond the frozen predictions):**
1. **Revision fails end-to-end in the presence of dependent structures (GW3).** The demonstrated single-level value-revision pattern did not work through the query path when a level-2 dependent MAP existed. The C0-D shadow mechanism (promoted graphs shadow themselves with taught answer facts; queries answer from facts, never re-executing MAPs) is the likely cause. This is stronger than the predicted "phase-4 fails": phase-3 failed too.
2. **Revision is one-shot (GW8).** Successive revisions fail; the operator cannot track current steps or re-admit tombstoned values. It is a patcher, not a rewriter.
3. **The shadow masks inquiry (GW5).** Because stale facts answer queries, the miss that would trigger inquiry never occurs. Inquiry cannot be load-bearing while memoization hides ignorance.
4. **No guard retargeting (GW4).** The revision operator does not perform topological repairs; it retains stale values when the repair requires guard rewiring.

**Positive evidence (genuine, bounded):**
1. Construction CAN build over learner-taught answer facts (GW3 phase 2: level-2 chain traversed the level-1 taught fact). This is real cross-level reuse of learned structure at construction time.
2. Single-level value revision WORKS through the query path when no dependents exist (GW7 probe 5).
3. Inquiry discriminates and re-fires correctly (GW6 primary, GW7).
4. The three mechanisms compose without interference (GW7).

## 4. Relation to the freeze battery

Per the directive, FW1-FW9 are a regression battery (TNN-2 was designed after seeing TNN-1's failures). GW1-GW8 are the independent generality test. The two batteries measure different things:

- A high FW score with a low GW score means: the architecture was tuned to the known failures but does not generalize beyond them.
- The GW failures cluster by mechanism: GW1/GW2 implicate (A); GW4/GW8 implicate (C); GW5/GW6 implicate (B); GW3/GW7 implicate integration. Per the no-patch-treadmill rule, a repair that fixes one world without moving its cluster mates is suspect.

No GW score, even 8/8, would establish L3 or broad generality: these are eight targeted probes against three specific mechanisms, not a generality proof. The 2/8 result is honest evidence of bounded mechanisms, not a failure of the evaluation.

## 5. What was NOT established

- No new opcodes were needed; all worlds ran on the frozen 4-op ISA via the frozen shim.
- Mechanism attribution for GW4 (revision vs. re-trial vs. shadow) is left to the revision red team; this battery establishes the behavioral boundary only.
- The GW3 phase-3 failure mechanism (shadow vs. DEP confusion) needs white-box confirmation; the behavioral evidence is conclusive but the internal cause is inferred from the C0-D analysis.

## Verdict: GW-EVAL-COMPLETE

Evaluation complete. All eight worlds ran three deterministic runs each. Hashes verified before and after. No assets modified. Score: 2/8 WORLD-PASS (GW6, GW7). Predictions matched on 5/8 worlds; the three deviations (GW3 worse, GW4/GW8 uncertain-to-fail) are all informative in the predicted direction. No overclaim: this is a targeted adversarial battery, not a generality proof.
