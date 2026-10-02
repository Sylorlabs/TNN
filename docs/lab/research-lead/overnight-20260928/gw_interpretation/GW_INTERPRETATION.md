# GW1-GW8 Interpretation

**Status: DRAFT interpretation of a committed evaluation.** The evaluation itself is
`GW-EVAL-COMPLETE` at `881fbb3d4`. This document interprets it; it does not alter it.

**Score: 2/8 WORLD-PASS (GW6, GW7).** Predictions from the sealed adversary
(`e409f5eea`) matched in 5 of 8 worlds exactly; GW3 came out worse than predicted;
GW4 and GW8 were uncertain by design and failed in the informative direction.

---

## 1. What does 2/8 mean, relative to the freeze 4/9?

2/8 and 4/9 are different rulers and should not be compared as fractions.

- FW1-FW9 are a **regression battery**: TNN-2 was designed after seeing TNN-1's
  failures, so FW measures whether the three new mechanisms fixed known gaps. The
  audit-corrected result is 4/9, byte-identical at the world level to TNN-1
  (re-clustering draft `ed2357141`): zero fixes, zero regressions, diagnosis falsified.
- GW1-GW8 are an **independent generality battery**: eight worlds designed
  post-freeze from the public architecture claim only, attacking the three
  mechanisms in shapes the builder never demonstrated.

The right comparison is at the cluster level, not the score level. The six GW
failures do not introduce a new cause. They are the same revised causes (R1
enumerated construction, R2 non-contingent inquiry, R3 single-schema revision,
plus the C0-D shadow) manifesting in fresh shapes:

| GW failure | Maps to |
|---|---|
| GW1 depth ceiling | R1: researcher-fixed gather bound (depth 4 literal) |
| GW2 no cyclic graphs | R1: DAG-family constructor, fixed topology menu |
| GW3 revision fails with dependents | C0-D shadow + R3 (provenance/DEP confusion) |
| GW4 no guard retarget | R3: single value-patch schema, no topological repair |
| GW5 shadow masks inquiry | C0-D shadow interacting with the inquiry trigger |
| GW8 one-shot revision | R3: fixed replace-the-SET-step topology |

The two passes are equally consistent with the re-clustering: GW6 (primary 7/7)
and GW7 (11/11) exercise exactly the demonstrated narrow capabilities (fire on
true miss; compose without interference in the non-hierarchical case). No GW
result contradicts the "fixed templates with variable content" characterization.
2/8 is therefore not a second independent bad number; it is the same architectural
story told by an independent witness, in shapes the builder did not anticipate.

The freeze-interpretation draft (`a1295cb22`) noted that a disconfirming GW pass
would be the most valuable outcome of the cycle. No disconfirmation occurred:
every failure was in the predicted direction, and GW3 was worse than predicted.

---

## 2. The three new findings, explained architecturally

### 2a. Revision fails end-to-end in the presence of dependents (GW3)

The phase-3 probe contradicted the level-1 terminal value and queried the
level-1 relation: expected 200, got the stale 100. The demonstrated
single-level value-revision pattern did not work through the query path here,
even though it worked in GW7 probe 5. The difference is the presence of a
level-2 dependent MAP at contradiction time.

The likely mechanism is the C0-D shadow (`8bfb80fdd`): `promote_graph` writes
a MAP and then teaches an exact-match answer fact; `ev_query` answers from
facts via `activate` and never re-executes MAPs. The revision may have updated
the MAP, but the query returned the stale shadow fact. With a dependent MAP in
play, the DEP-edge revision targeting may also have misfired, but the shadow
alone is sufficient to explain the stale answer. This is R3 meeting C0-D: the
single-schema patcher operates on structures that are causally inert at query
time, so even a correct patch is invisible. It also confirms the C0-D standing
caveat: no score on a battery that answers from facts can establish revision
that works through execution, because the MAP is never on the query path.

### 2b. The shadow masks inquiry (GW5)

Phase A contradicted the chain's first hop, leaving the composed relation
unanswerable; the diagnostic probe should have missed. It returned the stale
100 instead, so ACT returned `CHOICE 0` (no inquiry fired), the responder
released the control arm (B2), and the treatment reveal was never earned.

The inquiry trigger is "true miss after trial and P-INV fail." A stale fact
means there is no miss, so the trigger cannot fire. The memoization layer
(taught answer facts) hides the learner's ignorance from its own
uncertainty machinery. This is the interaction-analysis finding made concrete:
inquiry cannot be load-bearing while facts answer queries that graphs should
have to earn. It is also an H2-adjacent problem: the facts taught under oracle
verification are trusted over current evidence, so the learner cannot even
notice that its world changed. The K-REUSE-1/K-REUSE-2 design (delete the
shadow teach-in; MAP-first query with fall-through) is the minimal fix that
would make this probe discriminating; without it, GW5-style worlds will always
take the control arm.

### 2c. Revision is one-shot (GW8)

Revision 1 (100 to 200) worked; revision 2 (200 to 300) returned the stale
200; the revert (to 100) returned 200. The operator cannot revise an
already-revised graph.

This is R3 precisely: the operator is the single fixed topology "replace the
DEP-tagged SET step under its guard, rewire the GUARD's field12 and SEQ edges."
Revision 2 requires locating the CURRENT step rather than the original one
(the provenance edges still point at the first patch), and the revert requires
re-admitting a tombstoned literal (the operator tombstones with tag 0 and has
no un-tombstone path). Neither is expressible in the fixed schema. The operator
is a patcher with learner-filled indices, not a graph rewriter: L1 parameter
filling on a researcher-authored topology. The GW8 result is the exact
behavioral signature the revision red team predicted for a single-schema
operator, and it closes the loop: the demonstrated revision was the one case
the schema was written for.

---

## 3. Prediction accuracy and what it says about the adversary's model

| World | Prediction | Outcome | Verdict |
|---|---|---|---|
| GW1 | FAIL (control passes, 5-hop misses) | Exact | Confirmed |
| GW2 | FAIL (both miss) | Exact | Confirmed |
| GW3 | phase-3 PASS, phase-4 FAIL | phase-3 FAILED | Worse than predicted |
| GW4 | UNCERTAIN (distinctive outcomes) | Stale value, no repair | Informative, in the predicted direction |
| GW5 | FAIL via control arm if no inquiry fires | Control arm taken | Confirmed |
| GW6 | Primary 7/7 PASS, retirement probe FAILS | Exact | Confirmed |
| GW7 | PASS | 11/11 | Confirmed |
| GW8 | UNCERTAIN (rev1 should pass) | rev1 passed, rev2 and revert failed | Informative, in the predicted direction |

Six of eight worlds behaved as the adversary modeled; the two "uncertain"
worlds were uncertain by design and both failed informatively. Only GW3
deviated adversely, and it deviated in the direction of the deeper cause
(the C0-D shadow poisoning even the demonstrated pattern).

The adversary built these worlds from the PUBLIC architecture claim only
(`TNN2_BUILD_REPORT.md` at `f4de7ff46`), without reading hidden builder
fixtures or sealed FW contents. That a public-claim-only model predicts
TNN-2's boundaries this accurately means the failure modes are architectural
facts, not hidden bugs: they are legible from the system's own documentation.
This is the same property the three red teams exploited (all ATTACK-SUCCESS
from white-box reading). For TNN-3, it is actually good news of a specific
kind: the boundaries are characterizable, so the next design can target them
directly instead of hunting ghosts. The re-clustering's R1/R2/R3 plus C0-D
is a sufficient causal vocabulary for every GW outcome; no new cause was needed.

---

## 4. The positive evidence: meaningful L2, inside the envelope

Three genuine positives survived the adversarial battery:

1. **Construction over learner-taught facts works (GW3 phase 2).** The level-2
   chain traversed the level-1 taught answer fact as a first-class edge and
   probed correctly. The learner built a structure on top of its own learned
   structure at construction time. This is real cross-level reuse, and it is
   the strongest construction-side evidence in the cycle.
2. **Single-level value revision works through the query path when no
   dependents exist (GW7 probe 5).** The 100-to-200 contradiction probed 200.
   The schema does what it was written for, in the configuration it was
   written for.
3. **Inquiry discriminates and re-fires correctly (GW6 primary, GW7).**
   Miss fires 30, non-miss returns 0, new ignorance re-fires 30. The miss
   detector and the act path are correctly wired for the demonstrated cases.

This is meaningful L2 structural learning: runtime assembly of structures
from experience, with variable content bound at runtime, in configurations
the source did not hard-code per-instance. It is also firmly inside the
enumerated envelope: the level-2 chain is still a fixed chain template; the
revision is still the single schema; the inquiry is still the constant act.
None of the positives required learner-originated form, so none of them
threaten the re-clustering's meta-cause. They confirm the honest summary:
TNN-2 is "fixed templates with variable content," a real L2 advance over
TNN-1's "fixed templates with fixed content," and the envelope is unchanged
in kind. The positives matter for TNN-3 as the floor to preserve, not as
evidence the ceiling moved.

---

## 5. What would change the score: addressable vs architectural

Of the six failures, ordered by how much machinery a fix requires:

**Most addressable (mechanism-level, no new form needed):**

- **GW6 retirement probe.** Guides are append-only; after the ignorance is
  resolved the stale guide still fires 30. A guide lifecycle (retire on
  resolution) is a bounded addition, but note it touches H3: the retirement
  decision must be learner-owned to be more than another researcher literal.
  This is H3-lite territory (policy node for guide state), and it is the
  cheapest failure to close.
- **GW8 revision 2.** Tracking the current step across successive revisions
  requires the operator to follow its own patch provenance. This is an
  extension of the existing schema, not a new schema; but the revert
  (re-admitting tombstoned literals) already strains the single-schema
  framing, and a third lifecycle stage would strain it further.

**Addressable via the reuse path (designed, not implemented):**

- **GW5 shadow-masking.** The K-REUSE-1/K-REUSE-2 design (delete the shadow
  teach-in at promotion; MAP-first query with fall-through to facts) would
  make the diagnostic probe miss as intended, letting the inquiry trigger
  fire. This is the minimal fix that makes GW5-class worlds discriminating.
  It does not fix inquiry's constant act (R2), but it unblocks the trigger.

**Architectural (require learner-originated form; the meta-cause):**

- **GW1 depth ceiling.** The gather bound is a researcher literal (depth 1-4).
  Removing it is not a parameter change; it requires the constructor to
  decide its own search depth, which is H1 genuine widening plus H3 policy.
- **GW2 cyclic graphs.** The constructor is a DAG-family assembler. A loop
  shape is not a bigger menu item; it is a new topology the learner must
  originate. This is the H1 hard case.
- **GW3 phase-3 with dependents.** Even with the reuse path, revision through
  dependents requires retargeting contradictions at the MAP level and
  propagating through DEP edges, which the current provenance design does
  not support compositionally. This needs the full reuse path plus
  general revision (H3 structural mutation), i.e., Micah's protected-core
  decision.
- **GW4 guard retarget.** No value-patcher can fix a wrong guard. Topological
  repair requires the learner to select or construct a repair operator based
  on the failure mode: R3's exact gap, and the H3 structural fact.

**Recommended order** follows the TNN-3 roadmap (`67a420cca`): H2 probes
first (the shadow-masking and oracle trust in GW5 are H2-adjacent), then
H3-lite (guide lifecycle, revision targeting as learner-state policy),
then the reuse path in parallel, and genuine H1 widening only after H2 is
addressed. The no-patch-treadmill rule applies throughout: a repair that
moves GW8-rev2 without moving GW4 or GW3-phase-3 is suspect; fixes must move
cluster mates.

---

## 6. What the battery does not establish

- No GW score, even 8/8, would establish L3 or broad generality: eight
  targeted probes against three mechanisms are not a generality proof. The
  2/8 is honest evidence of bounded mechanisms, per the evaluator's own
  no-overclaim section.
- Mechanism attribution for GW4 (revision vs re-trial vs shadow) remains
  with the revision red team; this battery establishes the behavioral
  boundary only.
- The GW3 phase-3 internal cause (shadow vs DEP-edge confusion) needs
  white-box confirmation; the behavioral evidence is conclusive, the
  internal attribution is inferred from the C0-D analysis.

---

**Verdict: GW-INTERPRETATION-COMPLETE.**

Committed files: `NAMECHECK.md` (Step 0 guard), `GW_INTERPRETATION.md`
(this document). Owned path:
`docs/lab/research-lead/overnight-20260928/gw_interpretation/`.
Interpretation only; the committed evaluation at `881fbb3d4` is untouched.
