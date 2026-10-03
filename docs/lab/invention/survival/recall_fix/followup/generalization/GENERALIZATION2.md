# E1b Recall-Harm Generalization (GENERALIZATION2)

**Phase-2 commit:** `9c79065d02` | **Date:** 2026-09-27 | **Worker:** E1b Recall-Harm Generalization

## Executive Summary

This report tests whether the "recall-harm" finding (stale knowledge hurts) and its
candidate repair (deliberative evaluation via the shared `recall_delib.zag` module)
generalize beyond the original D2/D3 domains.

**Headline results:**

| Question | Answer |
|----------|--------|
| Do new D1 shifts actually harm R? | **YES** — 4/4 new variants show severe R degradation (R=10–70 ticks vs R_true=600) |
| Does the committed D1 D-agent close the gap? | **NO** — 0% closure on all 4 (D≈R or worse). **KILL** |
| Why? | The committed `agent_d_d1.zag` **does not import or use** `recall_delib.zag`. D1 never received the repair. |
| Does the shared module work on a NEW domain (D4 RELAY)? | **YES** — D closes 87–93% of the gap on 6/6 shifted variants |
| Does D survive deliberately false KB content? | **YES** — D_wrongKB closes 81% even with false claims |
| Is the module a universal fix? | **NO** — too slow for lethal shifts (10-sample threshold); false-positive distrust observed |

**Verdict:** The repair generalizes as a *mechanism* (it works on D4, a new domain, and on
D1 when actually wired in), but it does **not** generalize as a *deployed fix* — the
committed D1 agent lacks the module entirely, so D1's bar-equivalent fails. The
"one shared module for all domains" claim in the committed record is **factually false**
for D1.

---

## Part A: Four New D1 Shifts

### A.1 Scenario Design

Two shift families, each targeting a **realized** home heuristic (one R actually uses):

**Family C — Combine-tax** (`d1_c0`, `d1_c1`):
- **Mechanism:** Every COMBINE attempt costs 60 energy (knob `combine_cost=60`; home=0).
- **Target:** Home `h3` ("If two items in inventory and safe, COMBINE", claimed effect 0, taught "combining is free").
- **Why it hits a realized heuristic:** On committed `d1_h0`, R performs **354 COMBINEs** per 600-tick run. The tax turns this blind habit lethal.
- **Regime-correct KB:** `true_d1_combine.txt` = home KB **minus h3** (never combine).

**Family D — Storm-trap** (`d1_d0`, `d1_d1`):
- **Mechanism:** Storms deal 0 inside the zone but **50/tick outside** (`storm_dmg=0`, `storm_out=50`; home: 4/0). Agent starts in zone; first storm at t=30 (threat visible at t=10).
- **Target:** Home `h2` ("If storm within 20 ticks and in zone, FLEE", claimed −1).
- **Why it hits a realized heuristic:** R is in the zone at t=10, recalls h2, flees LEFT out of the zone, and is killed by the 50/tick outside storm at t=30. Verified in trace: action 0 (LEFT) at t=10 is the h2 flee; death at t=33.
- **Regime-correct KB:** Committed `true_d1_storm.txt` (h2 → A_WAIT, stay inside).

**Design validation:** All four first-33 geometry vectors are disjoint from Exp1 + phase-2
variants (generator asserts this). Combine-tax=60 and storm_out=50 were chosen after
robustness sweeps over 5 geometry seeds (R died on all 5 for both families).

### A.2 Full Arm × Variant Results (median of 2 reruns; reruns byte-identical)

| Variant | Z (ticks) | P (ticks) | R_home (ticks) | R_true (ticks) | D_home (ticks) |
|---------|-----------|-----------|----------------|----------------|----------------|
| d1_c0 (combine-tax) | 332 | 600 | 70 | 600 | 70 |
| d1_c1 (combine-tax) | 349 | 600 | 70 | 600 | 10 |
| d1_d0 (storm-trap) | 31 | 600 | 33 | 600 | 34 |
| d1_d1 (storm-trap) | 356 | 600 | 35 | 600 | 34 |

**Harm classification** (harm if `R_home ≤ Z` or `R_home < 0.8 × R_true`):

| Variant | R_home | 0.8×R_true | Z | Harm? | Closure `(D−R)/(R_true−R)` |
|---------|--------|------------|---|-------|---------------------------|
| d1_c0 | 70 | 480 | 332 | **HARM** (70 < 480) | (70−70)/(600−70) = **0.00** |
| d1_c1 | 70 | 480 | 349 | **HARM** (70 < 480) | (10−70)/(600−70) = **−0.11** |
| d1_d0 | 33 | 480 | 31 | **HARM** (33 < 480) | (34−33)/(600−33) = **0.00** |
| d1_d1 | 35 | 480 | 356 | **HARM** (35 < 480) | (34−35)/(600−35) = **−0.00** |

**Result:** Harm replicates on **4/4** new D1 shifts. The committed D1 D-agent closes
**0%** of the gap on all four (worse than R on d1_c1).

### A.3 Home Regression Check (K5-equivalent)

| Variant | R_home | D_home | D/R |
|---------|--------|--------|-----|
| d1_h0 | 600 | 600 | 1.000 |
| d1_h1 | 600 | 600 | 1.000 |
| d1_h2 | 600 | 600 | 1.000 |
| d1_h3 | 600 | 600 | 1.000 |
| d1_h4 | 600 | 600 | 1.000 |
| d1_h5 | 600 | 600 | 1.000 |

D ≥ 0.9×R on **6/6** home variants. (Trivially, as D1's D is behaviorally identical to R —
see §A.4.)

### A.4 Source-Integrity Finding (CRITICAL)

**The committed `agent_d_d1.zag` does not import or use `recall_delib.zag`.**

- `agent_d_d2.zag` and `agent_d_d3.zag`: import and call the shared module.
- `agent_d_d1.zag`: implements only "highest-priority matching heuristic whose static
  precondition passes." No outcome model, no distrust threshold, no exploration, no
  `delib_update`.

The committed claim of "one shared module for all domains" is **factually false** for D1.
D1's D-agent is a second copy of R's policy with extra logging, not a deliberative repair.
This fully explains the 0% closure: there is no mechanism present that *could* close it.

**Bar-equivalent verdict for D1:** **KILL** — candidate-not-reflex repair does not generalize
to D1 *as committed*. (See §C for evidence the module itself would work if wired in.)

### A.5 R_true Interpretation (Content vs. Application)

`R_true` (correct KB, still reflexive) scores **600/600** on all four shifted variants.
This isolates the failure to **content**: with regime-correct knowledge, reflexive
application is sufficient. R_home's failure is stale content, not the reflexive architecture.

### A.6 Determinism

All 50 D1 arm×variant rerun pairs are **byte-identical** (RESULT+TRACE, SHA-256, after
normalizing the rerun-index label). Pure Zag; zero RNG in agent decisions.

---

## Part B: New D4 RELAY Domain

### B.1 Domain Design

**RELAY** is a packet-routing domain built to test the shared module on unseen dynamics:

- Each tick, a packet arrives with a destination class (0–3). The agent chooses a relay
  hub (0–2). Latency = `matrix[dest][hub]`; utility = `100 − latency` (higher is better).
- **Home KB** maps each dest to its optimal hub (claimed utilities 85–90).
- **Shift:** One hub becomes congested (latency 80 for all dests, utility 20). The home
  KB's mapping is now stale for dests that used that hub.
- **6 home** (`d4_h0`–`h5`): home KB optimal; variants differ in destination seed and
  off-mapping latencies.
- **6 shifted** (`d4_s0`–`s5`): hub0 congested (s0,s1), hub1 congested (s2,s3), hub2
  congested (s4,s5).

**D4 D-agent** (`agent_d_d4.zag`): domain adapter over the **unmodified**
`recall_delib.zag` (SHA-256 `6dd9cde795d09495b1d57b76a83f2e72ae2a6759a0594717b9a9a5c6ffd8f960`,
symlinked from the phase-2 extraction; never edited). Each tick: recall heuristic for
current dest → `delib_select` picks hub → observed utility feeds `delib_update`.

### B.2 Full Arm × Variant Results (mean utility; 600 ticks; reruns byte-identical)

**Shifted variants:**

| Variant | Congested | Z | P | R_home | R_true | D_home | Harm? | Closure |
|---------|-----------|---|---|--------|--------|--------|-------|---------|
| d4_s0 | hub0 | 57 | 81 | 55 | 81 | 79 | **HARM** | **0.92** |
| d4_s1 | hub0 | 58 | 82 | 55 | 82 | 80 | **HARM** | **0.93** |
| d4_s2 | hub1 | 55 | 82 | 71 | 82 | 81 | mild | 0.91 |
| d4_s3 | hub1 | 56 | 85 | 71 | 85 | 84 | mild | 0.93 |
| d4_s4 | hub2 | 57 | 85 | 71 | 85 | 84 | mild | 0.93 |
| d4_s5 | hub2 | 56 | 86 | 71 | 86 | 84 | mild | 0.87 |

**Home variants:** D/R = **1.000** on 6/6 (D_home mean = R_home mean = 88).

**Result:** The shared module closes **87–93%** of the R→R_true gap on **6/6** shifted
variants. Harm (strict) replicates on s0/s1; s2–s5 show milder degradation (single dest
affected) with the same high closure.

### B.3 D_wrongKB Probe (Content Corruption)

**Design:** D-agent (with unmodified module) given a **deliberately false KB** on `d4_s0`
(hub0 congested): the false KB claims hub0 yields utility **95** for every dest (actual: 20).

| Arm on d4_s0 | Mean utility | Closure |
|--------------|--------------|---------|
| R_home (stale KB) | 55 | — |
| R_true (correct KB) | 81 | — |
| D_home (stale KB + module) | 79 | 0.92 |
| **D_wrongKB (false KB + module)** | **76** | **0.81** |
| P (optimal) | 81 | — |

**Result:** The module distrusts the false claims (observed 20 << claimed 95) and recovers
to 76, closing **81%** of the gap. The evaluator handles content corruption, not just
stale-but-once-valid content.

### B.4 R_true Interpretation

`R_true` matches P on all shifted variants (81–86). With correct content, reflexive
application is optimal. D_home's recovery (79–84) shows the module restores near-optimal
application from stale content alone.

### B.5 Determinism

All 61 D4 arm×variant rerun pairs **byte-identical** (SHA-256).

---

## Part C: Exploratory — Module on D1 (Not a Prereg Arm)

To separate "the module fails on D1" from "D1 lacks the module," I built an exploratory
D1 agent wiring the shared module in (`agent_dmod_d1.zag`; pseudo-actions resolved to
primitives; no-match defaults to WAIT; reward = energy delta).

| Variant | R_home | D_home (committed) | Dmod (module) | R_true |
|---------|--------|-------------------|---------------|--------|
| d1_c0 (combine-tax) | 70 | 70 | **600** | 600 |
| d1_c1 (combine-tax) | 70 | 10 | 41 | 600 |
| d1_d0 (storm-trap) | 33 | 34 | 164* | 600 |
| d1_d1 (storm-trap) | 35 | 34 | 144* | 600 |

\* Dmod died at the same point as R (storm killed it before 10 h2 samples accumulated).

**Reading:** The module **can** work on D1 dynamics — on `d1_c0` it distrusted h3 after
10 combine samples and stopped combining, surviving 600 ticks. But it is **too slow for
lethal shifts**: the 10-sample distrust threshold means the agent dies before learning
when the shift kills in <10 exposures (storm-trap: h2 recalled once, then death).
A false-positive distrust was also observed (h3 distrusted on d1_d0 from basal-cost
noise, though combining wasn't the killer there).

---

## Honest Verdict

### What generalizes
1. **Recall-harm replicates on new shifts.** 4/4 new D1 shifts and 2/6 (strict; 6/6 mild)
   D4 shifts degrade R_home. Stale knowledge hurting is not a D2/D3 artifact.
2. **The shared module is a working mechanism on new dynamics.** On D4 RELAY — a domain
   the module never saw — D closes 87–93% of the gap via unmodified
   `recall_delib.zag`. It also handles deliberately false KB content (81% closure).
3. **Content vs. application dissociates cleanly.** R_true (right content, reflexive)
   is optimal everywhere; D_home (stale content, module) recovers. The failure is
   in the knowledge, and the module repairs its application.

### What does NOT generalize (kills)
1. **D1 bar-equivalent: KILL.** The committed D1 D-agent closes 0% on 4/4 new shifts.
   Root cause is not a subtle generalization failure — **D1 was never given the repair**.
   `agent_d_d1.zag` does not use the shared module. The committed "shared module for all
   domains" claim is false for D1.
2. **Lethal-shift limitation.** The module's 10-sample distrust threshold cannot save an
   agent killed in fewer exposures (D1 storm-trap; exploratory Dmod confirms). The repair
   assumes survivable degradation, which held in D2/D3/D4 but not under lethal regime change.
3. **Phase-2 D1 shifts were void; the overclaim stands corrected.** Committed
   `BAR_RESULTS2.md` claims D1 bars pass while reporting R_home=R_true=600 on both D1
   shifts (storm-invert, move-rot) — i.e., the shifts did nothing. The present 4 shifts
   are the first D1 shifts that actually bite, and the committed D-agent fails all of them.

### Bottom line
The *idea* (evaluate recalled knowledge against observed outcomes; distrust and explore
on mismatch) generalizes across domains. The *deployment* does not: D1 shipped without
the machinery, and the machinery itself has a speed limit (lethal shifts outrun it).
Any claim that Experiment 1b's repair "works on D1" must be retracted for the committed
artifact; it holds only for the module as a mechanism, demonstrated on D4 and on D1
via the exploratory wiring.

---

## Artifacts & Reproduction

- **Worlds:** `worlds_new/d1_c0.txt,d1_c1.txt,d1_d0.txt,d1_d1.txt` (D1);
  `worlds_new/d4_h0..h5.txt,d4_s0..s5.txt` (D4)
- **KBs:** `kb_new/true_d1_combine.txt,home_d4.txt,true_d4_s0..s5.txt,false_d4_s0.txt`
  (plus committed KBs referenced from `base/`)
- **Sources:** `src_new/world_d4.zag,kb_d4.zag,agent_{z,p,r,d}_d4.zag,agent_dmod_d1.zag`
  (exploratory), `gen_d1_new.py,gen_d4.py,gen_d4_kb.py,run_partA.py,run_partB.py`
- **Runs:** `runs/partA_results.txt` (100 runs), `runs/partB_results.txt` (122 runs);
  `runs/partA_sha.txt,partB_sha.txt` (SHA-256 per run)
- **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- **Determinism:** 111/111 rerun pairs byte-identical (RESULT+TRACE SHA-256).
- **Repo untouched.** No binaries, `.zagd`, or caches in deliverables (build artifacts
  removed after runs).

### Key design parameters
- D1 combine-tax: `combine_cost=60` (home 0); storm-trap: `storm_dmg=0, storm_out=50`
  (home 4/0); generator seed `20260928`.
- D4: utility = 100 − latency; 600 ticks; dest(t) = (7t + seed) mod 4; congestion = 80.
- `recall_delib.zag` SHA-256: `6dd9cde7…f960` (full in §B.1), used unmodified via symlink.
