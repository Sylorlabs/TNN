# R2-8 Mapping Freeze — Verdict

**Date:** 2026-09-23  
**Task:** PAMs v2 follow-up item 5 (Micah: "TEST FIRST — freeze one mapping, re-run, compare")  
**Amendment:** `mapping_freeze/AMENDMENT_R2-8_MAPPING_FREEZE.md`  
**Amendment commit:** `f4ca485cbf0539cd8bf448db49f06b2ede167c8c` (committed alone before execution)

---

## 1. Mapping Proof (independent source)

An independent byte-level checker (not `eval_r28.py`) compared frozen fixtures
against exposed generator outputs:

| Check | Result |
|---|---|
| `p2 == expose(g, 1.25)` | **5815/5815** |
| `q2 == expose(F, 1.25)` | **5815/5815** |
| Exact-check failures | **0** |
| Mean p1~g distance | 80.01 |
| Mean p1~F distance | 5364.12 |
| Mean q1~g distance | 5364.13 |
| Mean q1~F distance | 79.98 |

Five cross-matches were motion-direction degeneracies where exposed g and F
became byte-identical.

`generators/gen_r2q.py` explicitly identifies Pi1..3 as perturbations of Gi
and Qi1..3 as perturbations of Fi.

**Settled mapping:** p-set perturbs **g/S** (the independent source); q-set
perturbs **F/X**. The frozen measured R2-8 battery already used the
preregistered p mapping. The claim that the measured evidence perturbed X is
**false**.

**Frozen verdict mapping:** p-set/S-g for the verdict; q-set/X-F as comparison only.

---

## 2. Pure-Zag Implementation

All mechanisms reimplemented in pure Zag (zero RNG):

| Component | File | Status |
|---|---|---|
| Percept (5 tasks) | `src/percept_r28.zag` | Complete, sin-lookup optimized |
| Monolithic gate+ledger | `src/gate_r28.zag` | Complete, reference implementation |
| Percept extractor | `src/dump.zag` | Complete |
| Staged gate+ledger | `src/gate2.zag` | Complete |

**Staged equivalence proven:** On a 20-trial subset, the two-stage pipeline
(`dump` → Python join glue → `gate2`) produces **byte-identical** results,
ledger, and summary to the monolithic `gate_r28`. The Python join is fixture
plumbing only; gate, ledger, and bars are pure Zag.

**Determinism proven:** 3 consecutive `gate2` runs on 3,975 visual trials
produce byte-identical outputs:
- results: `472d6c9f5b44bc00195a571158755bdd6481dfad84a31bbe24b728c28ea65849`
- ledger: `8a81c27a7b1d812f810d1b8fdd227179040a8db5187f24d754038920026fb39e`
- summary: `f5d1d7d429529c0d81ac7e35976210dbb84b1846ded3c6f62158ead302691739`

---

## 3. Re-run Results (visual tasks, pure Zag)

Visual tasks (colordisc, colorconst, shapetrans, motiondir): 3,975 trials/arm.
Audio tasks (pitchdisc, timbredisc): extraction in progress (see §5).

### p-arm (p-set perturbs g, frozen mapping)

| Bar | Result | Verdict |
|---|---|---|
| B5 false installs | 44/3975 = 1.107% | **FAIL** (<0.5% required) |
| B4 decisions changed | 2656/3975 = 66.82% | PASS |
| KB2 self-flag | 1984/2028 = 97.83% | PASS |
| Leg-(ii) ablation | 803 leg-i-only vs 44 full | PASS |
| Ledger final | `2b26b918ce72571411258315b00bda9ef325b4182c8be19fcda5e6dc4d9dabc5` | — |

### q-arm (q-set perturbs F/X, comparison)

| Bar | Result | Verdict |
|---|---|---|
| B5 false installs | 11/3975 = 0.277% | **PASS** |
| B4 decisions changed | 2953/3975 = 74.29% | PASS |
| KB2 self-flag | 2017/2028 = 99.46% | PASS |
| Leg-(ii) ablation | 803 leg-i-only vs 11 full | PASS |
| Ledger final | `943ea3643780c825c8a481b67dba4f5dfed9b929aef0f259e01407fa123f2a4d` | — |

### Deltas (q − p, visual)

| Metric | p-arm | q-arm | Delta |
|---|---|---|---|
| B5 false installs | 44 (1.107%) | 11 (0.277%) | **−33 (−0.830pp)** |
| B4 changed | 2656 (66.82%) | 2953 (74.29%) | **+297 (+7.47pp)** |
| KB2 flagged | 1984 | 2017 | +33 |

The q-arm (perturbing X) has **fewer false installs** than the p-arm
(perturbing g). This is consistent with the mapping: perturbing the
independent source g is harder for the gate to detect than perturbing X,
leading to more false installs under the p mapping.

### Recall (p-arm, visual only)

- Trials: 1008 (visual subset of 1728)
- Installed: 193
- Verdict: FAIL (≥70% required)

The 193 installs match the frozen absolute count (193/1548 = 12.47% on the
full set), indicating all installs are in visual tasks.

**q recall delta: N/A** — frozen recall fixtures contain g+p1..p3 but no
q-set companions (per amendment).

### Primary (visual only)

- B1: 179/250 = 71.6% → PASS (frozen: 274/370 = 74.05% PASS)

---

## 4. Fidelity Check

The frozen p-arm full-battery results (from Python implementation):
- B1: 274/370 = 74.05% PASS
- B4: 3189/5815 = 54.84% PASS  
- B5: 59/5815 = 1.0146% FAIL
- KB2: 2034/2093 = 97.18% PASS
- Recall: 193/1548 = 12.47% FAIL
- Overall: **DEAD**

The pure-Zag visual re-run reproduces the **same pattern**: B5 FAIL, B4 PASS,
KB2 PASS, recall FAIL. The absolute numbers differ because the visual subset
(3,975 trials) excludes audio tasks (1,840 trials), but the **verdict pattern
is preserved**.

The frozen p-arm ledger hash (`4ddd9aef55c7a0b84ed1dc7d4f6d309bc935c89d5d3b07d474b4bdb3087c4ee5`)
is for the full 5,815-trial battery. The visual-subset hash differs as expected
(different trial set). Full-battery hash verification awaits audio completion.

---

## 5. Limitations

**Audio percept extraction incomplete.** The pitchdisc/timbredisc percepts
perform O(n) f0 estimation (zero-crossing interpolation, autocorrelation)
which is slow in the current implementation (~0.9s CPU per fixture). With
18,320 audio fixtures and a heavily loaded VM (load ~15 on 2 cores), full
extraction exceeds the available time.

**What was completed:**
- All 36,840 visual fixtures extracted in pure Zag
- Staged equivalence proven (byte-identical)
- Determinism proven (3 byte-identical runs)
- Visual re-run demonstrates the pipeline end-to-end

**What remains:**
- Audio fixture extraction (pitchdisc: 9,200; timbredisc: 9,120)
- Full-battery gate runs (5,815 trials/arm)
- Full-battery ledger hash verification against frozen
  `4ddd9aef55c7a0b84ed1dc7d4f6d309bc935c89d5d3b07d474b4bdb3087c4ee5`

The mapping verdict does **not** depend on audio completion. The mapping is
a property of the fixture generation (proven in §1), not the percept values.

---

## 6. Verdict

**Mapping:** p-set perturbs **g** (the independent source S); q-set perturbs
**F/X**. **FROZEN.**

**Battery verdict:** **DEAD** (unchanged). The p-arm fails B5 (false installs
1.01% ≥ 0.5%) and recall (12.47% < 70%). The pure-Zag re-run reproduces the
DEAD pattern on the visual subset.

**q comparison:** The q-arm (X-perturbation) shows fewer false installs
(0.28% vs 1.11% visual) and higher B4 change rate (74.3% vs 66.8% visual)
than the p-arm (g-perturbation). This is consistent with X-perturbations
being easier for the gate to detect than independent-source perturbations.

**Mechanism compliance:** The frozen battery used Python for gate and ledger.
This work reimplements both in pure Zag with hash-chained ledgers, staged
equivalence proof, and 3× byte-identical determinism. The mechanism-compliance
gap is closed for the visual subset; audio remains to fully close it.

---

## Artifacts

| Path | Description |
|---|---|
| `mapping_freeze/AMENDMENT_R2-8_MAPPING_FREEZE.md` | Frozen prereg amendment |
| `mapping_freeze/trials/` | Frozen trial lists (p, q, recall, primary) with SHAs |
| `mapping_freeze/src/` | Pure-Zag sources (percept, gate, dump, gate2) |
| `mapping_freeze/scripts_gen/` | Python fixture glue (join, chunked dump wrapper) |
| `mapping_freeze/percepts/` | Extracted visual percepts (36,840 fixtures) |
| `mapping_freeze/results_visual/` | Visual re-run outputs (results, ledgers, summaries) |
| `mapping_freeze/MAPPING_VERDICT.md` | This document |

**Trial list SHAs:**
- `trials_p.tsv`: `1d04e384c1b8084ec50532e4300d7d291e276c3eaa8147de3a93e1d88fcaf7fb`
- `trials_q.tsv`: `02535cbda34c88cdc8c30994721b8ab4facca6660fa234078ce41871619e5dae`
- `recall_p.tsv`: `1172dc631bd7f221ac0466f99da650f21291d439ecb3084740d7ef2e1d754a2b`
- `primary.tsv`: `c27bc9569ec68a1030ac69deb86557afcb8103d6eb38725a5f804ea3a8646e02`
