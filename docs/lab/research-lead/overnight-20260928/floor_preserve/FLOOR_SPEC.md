# TNN-3 Floor Spec: Capabilities to Preserve from TNN-2

**Status: DRAFT preservation spec, not a kill bar set.** These are regression
tests, not L3 bars. TNN-3 must not lose these while trying to gain new
capabilities. All thresholds below are transcribed from committed reports.

**Basis:**
- Freeze floor: FW1, FW2, FW4, FW5 (4/9 pass set, byte-identical TNN-1/TNN-2, audit `8959a7c14`, re-clustering `ed2357141`)
- GW floor: three positives from `GW-EVAL-COMPLETE` (`881fbb3d4`), interpreted in `GW_INTERPRETATION.md` (`42fa993ab`) section 4

**The honest summary line this spec protects:** TNN-2 is "fixed templates with
variable content," a real L2 advance. The seven capabilities below are the
floor. None of them establishes L3, learner-originated form, or reuse. They
are what TNN-3 must keep while climbing.

---

## 1. Freeze floor (from the 4/9 pass set)

### F1. Associative recall (FW1, FW2)

**Capability:** The learner stores taught (s, r, o) facts and returns them
on exact query, including after intervening unrelated teaching (retention).

**Verification test:** FW1 and FW2 probe sets, run per the freeze protocol
(fresh learner state, three deterministic runs, byte-identical transcripts).

**Pass thresholds (transcribed):**
- FW1: 10/12 probes minimum (TNN-1 bar), TNN-2 scored 12/12; retention 7/10 minimum, TNN-2 scored 10/10
- FW2: 7/8 minimum (TNN-1 bar), TNN-2 scored 8/8

**What breaking looks like:** Recall drops below the TNN-1 bars, or
retention degrades (earlier facts overwritten by later unrelated teaching),
or runs stop being deterministic. A TNN-3 that gains construction but can
no longer recall what it was taught has regressed, not advanced.

### F2. Law change and revert (FW4)

**Capability:** When a taught regularity is contradicted by a law change, the
learner answers with the new value; when the law reverts, it answers with
the restored original. The change propagates to queries without leaving
stale answers on the reverted key.

**Verification test:** FW4 probe sequence (change, probe, revert, probe),
freeze protocol.

**Pass thresholds (transcribed):** 12/12 on all three probe groups
(TNN-1 and TNN-2 both scored 12/12, 12/12, 12/12).

**What breaking looks like:** Stale answers after change or revert, partial
propagation (some queries updated, others not), or regressions below
12/12 on any group. Note: GW8 showed TNN-2's revision is one-shot for
MAP-level graphs (rev2 and revert failed there); the FW4 floor covers only
the fact-level change/revert path. TNN-3 must keep the fact-level behavior
while extending the graph-level behavior, not trade one for the other.

### F3. Targeted update without collateral damage (FW5)

**Capability:** A targeted contradiction updates the intended key and leaves
unrelated learned state intact. The learner distinguishes the update target
from its neighbors.

**Verification test:** FW5 probe sets, freeze protocol.

**Pass thresholds (transcribed):** 10/10, 3/3, 9/9 across the three probe
groups (TNN-1 and TNN-2 identical).

**What breaking looks like:** The update bleeds into neighboring keys
(collateral damage), or unrelated facts are disturbed, or any group drops
below its transcribed threshold. A TNN-3 with broader revision machinery
must be at least as surgical as TNN-2 on this battery.

---

## 2. GW floor (from the adversarial battery positives)

### G1. Construction over learner-taught facts (GW3 phase 2)

**Capability:** At construction time, the learner can traverse a
previously taught answer fact as a first-class edge. A level-2 chain built
over the level-1 taught answer (not the original observation) probes
correctly. This is cross-level reuse of learned structure during
construction, the strongest construction-side evidence in the cycle.

**Verification test:** GW3 phases 1-2 sequence: teach level-1 2-hop chain,
probe (expect 100); build level-2 chain traversing the level-1 answer fact
as subject, probe (expect 300). Three deterministic runs, fresh state.

**Pass threshold (transcribed):** Both probes correct, 3/3 byte-identical
runs (TNN-2 achieved this).

**What breaking looks like:** The level-2 probe misses or returns the
wrong value, indicating construction can no longer consume the learner's
own taught facts as edges. A TNN-3 whose new constructor only reads raw
observations and not learned state has lost a genuine L2 capability.

**Boundary note:** This floor does not include GW3 phase 3 (revision with
dependents failed) or phase 4 (retirement failed). The floor is
construction-over-facts, not revision-through-dependents.

### G2. Single-level value revision through the query path (GW7 probe 5)

**Capability:** A single contradiction of a promoted graph's terminal value
(100 to 200) is visible through the query path: the subsequent probe
returns 200. The revision schema does what it was written for, in the
configuration it was written for (no dependent MAPs at contradiction time).

**Verification test:** GW7 probe sequence through probe 5, or the minimal
equivalent: promote a graph, contradict its terminal value once, probe.
Three deterministic runs, fresh state.

**Pass threshold (transcribed):** Probe returns 200 after the 100-to-200
contradiction, 3/3 byte-identical runs (TNN-2 achieved this in GW7).

**What breaking looks like:** The probe returns the stale 100, indicating
the revision path regressed even in its demonstrated configuration. Note
that GW3 phase 3 showed this same pattern failing when a dependent MAP
existed; the floor is explicitly the no-dependent case. TNN-3 must keep
the no-dependent case working while fixing the dependent case, not by
breaking the former.

### G3. Inquiry discrimination and re-fire (GW6 primary, GW7)

**Capability:** The miss detector and the act path are correctly wired for
the demonstrated cases: a query on a taught key returns the answer and
ACT returns `CHOICE 0` (no spurious inquiry); a query on an untaught key
misses (-2) and ACT returns `CHOICE 30` (fires); after the missing fact
is taught, new ignorance on a fresh key re-fires `CHOICE 30`.

**Verification test:** GW6 primary probe sequence (7 probes): correct
answer then `CHOICE 0`; miss then `CHOICE 30`; teach then correct answer;
fresh-key miss then `CHOICE 30` re-fire. Three deterministic runs.

**Pass threshold (transcribed):** 7/7 primary probes correct, 3/3
byte-identical runs (TNN-2 achieved this; the retirement probe is
secondary and failed as predicted, it is not part of this floor).

**What breaking looks like:** Spurious inquiry on known keys
(`CHOICE 30` when `CHOICE 0` is correct), failure to fire on true miss,
or failure to re-fire on new ignorance. A TNN-3 with a richer inquiry
mechanism must still get the basic discrimination right. This floor is
discrimination, not contingency: FW6's contingent-inquiry requirement
(variable act with epistemic state) remains failed and is not part of
the floor.

---

## 3. What is NOT the floor

The following are explicitly excluded, so that TNN-3 does not
"preserve" failure modes or mistake the floor for the ceiling:

- **FW3, FW7, FW8, FW9 (freeze failures).** Arithmetic invention,
  planning, novel utterance, relational DAG traversal. These are the
  symptom clusters to fix, not to preserve.
- **FW6 (freeze failure).** Contingent inquiry. The floor (G3) is
  discrimination with a constant act; FW6 requires the act to vary
  with epistemic state. Do not confuse the two.
- **GW6 retirement probe (failed as predicted).** Guide retirement on
  resolution. This is H3-lite territory, a gap to close, not a floor.
- **GW8 revision 2 and revert (failed).** Multi-step revision lifecycle.
  Gap to close, not floor.
- **GW3 phases 3-4, GW4, GW5 (failed).** Revision with dependents,
  guard retarget, shadow-masked inquiry. All gaps, not floor.
- **Depth-4 construction ceiling (GW1), DAG-only constructor (GW2).**
  Architectural boundaries to move, not to preserve.

Preserving a failure mode is the treadmill. The floor is seven
capabilities; everything else is either a target or out of scope.

---

## 4. Running the floor battery

The floor battery is the union of the seven verification tests above:

1. FW1 probe set (associative recall, retention)
2. FW2 probe set (associative recall)
3. FW4 sequence (law change/revert)
4. FW5 probe sets (targeted update, no collateral)
5. GW3 phases 1-2 (construction over taught facts)
6. GW7 through probe 5 (single-level revision, no dependents)
7. GW6 primary 7 probes (inquiry discrimination and re-fire)

Each runs under the freeze protocol: fresh learner state, three
deterministic runs, byte-identical transcripts required. The battery is
a regression gate: TNN-3 may add mechanisms, but all seven must pass at
their transcribed thresholds before any new-capability claim is evaluated.

Recommended placement in the TNN-3 preregistration: as a dedicated
regression section, separate from the kill bars, run before and after
the sealed evaluation. The prereg structure draft (`206499c03`) has a
10-section outline; the floor battery belongs in the verification
procedures section as a precondition.

---

## 5. Breaking criteria (what counts as a regression)

A TNN-3 build has regressed if any of the following holds:

1. Any of F1-F3 drops below its transcribed freeze threshold.
2. Any of G1-G3 fails its transcribed GW probe sequence.
3. Any floor test stops being deterministic across three runs.
4. A previously passing floor test passes only with a researcher-supplied
   crutch that was not needed for TNN-2 (e.g., extra teaching, manual
   state reset between probes, relaxed determinism).

Criterion 4 is the anti-gaming clause: the floor must be met by the
learner, not by the harness. If TNN-3 needs more scaffolding than TNN-2
to pass the same seven tests, that is a regression in learner autonomy
even if the scores match.

---

## 6. Provenance

| ID | Capability | Source | Threshold source |
|---|---|---|---|
| F1 | Associative recall | FW1/FW2 | TNN-1 FREEZE_REPORT.md line 34-35; TNN-2 draft via `ed2357141` sec 2 |
| F2 | Law change/revert | FW4 | Transcribed 12/12 x3 via `ed2357141` sec 2 |
| F3 | Targeted update | FW5 | Transcribed 10/10, 3/3, 9/9 via `ed2357141` sec 2 |
| G1 | Construction over taught facts | GW3 phase 2 | `881fbb3d4` sec 1 (GW3), `42fa993ab` sec 4 |
| G2 | Single-level revision, no dependents | GW7 probe 5 | `881fbb3d4` sec 1 (GW7), `42fa993ab` sec 4 |
| G3 | Inquiry discrimination and re-fire | GW6 primary, GW7 | `881fbb3d4` sec 1 (GW6/GW7), `42fa993ab` sec 4 |

Excluded items (section 3) are grounded in the same two committed
reports. No thresholds are invented; every number above is transcribed.

---

**Verdict: FLOOR-SPEC-COMPLETE.**

Seven capabilities, four from the freeze pass set, three from the GW
positives. The floor TNN-3 must keep while climbing.
