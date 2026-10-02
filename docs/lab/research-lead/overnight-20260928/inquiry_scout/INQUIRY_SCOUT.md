# Learner-Driven Inquiry Scout

Date: 2026-09-30. Worker: Learner-Driven Inquiry Scout (subagent).
Status: scout only. No implementation proposed or written.
Verdict label target: INQUIRY-SCOUT-COMPLETE.

## Context

The frontier scout (commit `edcb364e3`) ranked learner-driven
inquiry #2 by information gain, behind DEVINT-CLA2. The ranking
rationale: H-EXP2 v2 will show the learner can execute a
researcher-designed inquiry loop; this frontier asks whether the
learner can originate one. This is the difference between L2
(executing an inquiry procedure) and L3-ish (constructing the
inquiry from experienced uncertainty). It is also the direct
answer to the W6 B4 ruling.

This scout specifies the gap precisely, designs the discriminating
experiment, and shapes the prereg. Analysis only.

## 1. What "learner-driven inquiry" means

**Researcher-designed inquiry loop** (what H-EXP2 v2 tests):
The researcher specifies (a) the hypothesis family, (b) the probe
space, (c) the scoring rule that ranks probes, and (d) the
execution trigger. The learner enumerates, scores, and executes.
The inquiry strategy is the researcher's ranking function running
on the learner's hardware. If the hypothesis family changes, the
researcher rewrites the enumeration. If the scoring rule is wrong,
the researcher fixes it. The learner optimizes within a
researcher-supplied frame.

**Learner-driven inquiry** (this frontier): The learner
experiences uncertainty as workspace content (a -2 admission
reified as an UNCERTAINTY node by its own event-loop process),
constructs an inquiry guide (an ACTION-GUIDE anchored at that
uncertainty, selecting an information-seeking act) via its own
workspace process using generic primitives, and the ACT mechanism
executes it. No researcher specifies which uncertainty maps to
which inquiry action. No researcher writes the guide. The inquiry
strategy is determined by structures the learner built from its
own experience of not knowing.

The W6 B4 bar governs both readings: "the inquiry strategy is
learner-determined, no source logic branches on world identity."
The frozen core failed B4 because CHOICE was constant 0 emitted at
file positions (W6W7_ANALYSIS.md, commit `e7bb3d0bc`). The ACT
implementation passes B4 structurally: `act_event` takes no
positional input, zero world/task branches, and the red team
confirmed zero tag checks in the ACT path (commit `73d06a6d4`,
Vector 4 ATTACK-PASS). But structural passage is not the same as
the learner originating inquiry. The current tests prove the
mechanism can execute uncertainty-anchored guides; they do not
prove the learner creates them.

## 2. The two missing pieces

The ACT prereg (commit `51a818141`, section 3) names reference
derivation D2: "from a live UNCERTAINTY record, write an
ACTION-GUIDE anchored at that record selecting the inquiry
action." D2 is explicitly "a reference example of the general
requirement, not a frozen algorithm." No learner-side process has
ever performed D2. The test scaffolding (`mk_uncert`,
`mk_guide` in the ACT build) performed it instead.

Decomposing D2 into its load-bearing steps reveals two distinct
missing pieces, not one:

**Piece A: uncertainty reification.** The learner-side event loop
must create UNCERTAINTY nodes from -2 admissions automatically,
as part of normal operation. Currently `mk_uncert` (test
scaffolding) does this. The prereg (section 2c) specifies the
convention: "Created when a QUERY returns -2 (the admission of
ignorance). ref[0] = the queried key context." But no frozen
learner-side process implements this creation. Without Piece A,
there is no workspace content for inquiry guides to anchor to
except researcher-placed nodes.

**Piece B: inquiry guide construction.** Given a live
UNCERTAINTY node, a learner-side workspace process must write an
ACTION-GUIDE anchored at it (ref[0] = the uncertainty node),
selecting an information-seeking act (payload[0] = the inquiry
CHOICE value), using only generic primitives (ALLOC, WRITE,
LINK, READ, ACTIVATE). Currently no such process exists. This is
the D2 derivation proper.

Both pieces must be learner-side workspace processes, not core
code and not test scaffolding. If either piece lives in core
source as task cases, the implementation fails K-ACT2 (per the
ACT prereg section 5: "Not a second policy learner in disguise").

A third piece exists but is already built: **Piece C: the ACT
read path** (the five-step protocol). This is done and red-teamed.
The scout therefore scopes to Pieces A and B only.

## 3. How this differs from H-EXP2 v2

H-EXP2 (commit series, PREREG_EXP2.md) is Level D
(self-directed evidence): the learner identifies which missing
observation would resolve its own uncertainty, without being
told. The algorithm enumerates states, simulates predicted
outcomes under each competing hypothesis via the learner's own
`pred_under()`, and ranks by disagreement (ndiff DESC, state
index ASC). The frontier scout characterizes v2 as "the learner
prunes 16 hypotheses, scores 1654 probes by predicted-outcome
distinctness, executes the top probe" and classifies it as
"researcher-specified probe scoring over a researcher-enumerated
hypothesis family."

The classification is precise about what is researcher-supplied
in H-EXP2 v2:

(a) The hypothesis family is researcher-enumerated (the
    ambiguous-entry bitmask over a fixed variable set).
(b) The probe space is researcher-enumerated (12 states in v1;
    1654 probes in v2).
(c) The scoring rule is researcher-specified (ndiff DESC, then
    index ASC). The learner does not choose what makes a probe
    good; the researcher told it that disagreement is good.
(d) The execution trigger is researcher-specified (ambiguity
    detected implies run the invention routine).

What is genuinely learner-side in H-EXP2: the predictions
themselves (`pred_under()` uses the learner's own learned
groups), and the honest abstention (no ambiguity implies no
pick). This is real Level D behavior and it matters. But the
inquiry strategy, the mapping from "I am uncertain" to "execute
this probe," is the researcher's ranking function.

Learner-driven inquiry as specified here differs on exactly
points (c) and (d): the learner's own uncertainty structures
(UNCERTAINTY nodes it reified itself) drive action selection
through guides it constructed itself. There is no scoring rule
in source. There is no enumerated probe space in source. There
is a generic ACT read path and whatever the learner built.

The relationship is complementary, not competitive. H-EXP2 v2
tests whether the learner can compute good probes given a
frame. This frontier tests whether the learner can originate
the inquiry frame from its own uncertainty. A system that does
both would be strictly stronger than either alone. The
discriminating experiment below is designed so that H-EXP2-style
machinery, if present, cannot pass it by itself.

## 4. The discriminating experiment

### Design principle

The experiment must separate two hypotheses:

- H0 (researcher-driven): the learner executes inquiry because
  the researcher supplied the uncertainty-to-action mapping
  (guides, scoring rule, or equivalent).
- H1 (learner-driven): the learner constructs the
  uncertainty-to-action mapping from its own experience,
  and the mapping tracks the learner's actual uncertainty.

Any test the researcher can pass by pre-writing the right
guides fails to discriminate. The experiment therefore uses
**novel uncertainties**: uncertainty types the researcher never
specified a mapping for. If the learner constructs working
inquiry guides for uncertainties it was never taught to inquire
about, H0 is rejected.

### Phase 1: Uncertainty reification (Piece A)

Setup: a CLA-2 workspace with the ACT read path active
(POLICY_ROOT set, per the ACT build). The learner is exposed to
queries it cannot answer in a fresh domain (novel relation,
novel entities; the researcher specifies the domain but NOT any
inquiry mapping).

Check 1A: after -2 admissions, UNCERTAINTY nodes exist in the
workspace with ref[0] = the queried key context.

Check 1B (origin audit): white-box trace proves the
UNCERTAINTY nodes were created by the learner-side event-loop
process, not by test scaffolding or core code. Every
UNCERTAINTY node must carry a creation trace: the -2 event
that triggered it, the process that wrote it.

Check 1C (ablation): with the reification process disabled
(and only that process), no UNCERTAINTY nodes appear after
-2 admissions. The reification is load-bearing, not
decorative.

Falsification F-INQ-A: UNCERTAINTY nodes appear only when the
researcher places them, or the creation trace shows
scaffolding authorship. Piece A is then not learner-side.

### Phase 2: Inquiry guide construction (Piece B)

Setup: Phase 1 complete; live UNCERTAINTY nodes exist that the
learner reified itself. The world offers a non-degenerate
action interface: at least two distinguishable actions, one of
which is information-seeking (produces an OBSERVE that resolves
the uncertainty) and one of which is not (decoy).

Check 2A: ACTION-GUIDE nodes appear anchored at the learner's
own UNCERTAINTY nodes (ref[0] = the uncertainty node address),
selecting the information-seeking act.

Check 2B (origin audit): white-box trace proves the guides
were constructed by a learner-side workspace process using
generic primitives. The trace must show: which UNCERTAINTY
node triggered construction, which process wrote the guide,
and that no researcher code authored the uncertainty-to-action
mapping.

Check 2C (content check): the guide's payload[0] selects the
information-seeking act, not the decoy, not a random act.
This must hold for uncertainties the researcher never mapped.

Check 2D (ablation): with the guide-construction process
disabled (ACT read path intact, UNCERTAINTY nodes present),
no inquiry guides appear and ACT emits 0 at inquiry
opportunities. The construction is load-bearing.

Falsification F-INQ-B: guides appear only for
researcher-mapped uncertainty types, or the construction
process contains task-specific branches (verified by source
inspection: any branch on uncertainty content, domain, or
relation identity fails K-ACT2).

### Phase 3: The B4 attribution test (end to end)

Setup: W6-class world (designed to expose false positives in
inquiry attribution), non-degenerate action interface, Pieces
A and B active, ACT read path active. No researcher-supplied
guides. The world file contains ACT lines at both the genuine
inquiry position and a decoy position.

Check 3A (correlation): emitted actions correlate with the
learner's live UNCERTAINTY records, not with ACT line
position. Operational: swap the decoy and inquiry ACT
positions in the world file; actions follow the -2 admission,
not the file position. (This is P-ACT2 from the ACT prereg,
now with learner-constructed guides instead of scaffolding.)

Check 3B (uncertainty reduction): the inquiry actions the
learner selects actually reduce its uncertainty: after the
OBSERVE, subsequent queries on the same key return answers,
not -2. Inquiry is functional, not performative.

Check 3C (no pre-play): the learner's first inquiry action in
a novel domain occurs AFTER its first -2 admission in that
domain, never before. Pre-play (inquiring before
experiencing uncertainty) indicates a researcher-supplied
script.

Falsification F-INQ-C: actions correlate with file position
under the swap test (B4 fails directly), or inquiry precedes
uncertainty (scripted), or inquiry actions do not reduce
uncertainty (performative).

### Phase 4: Novel-domain transfer (the L3-ish test)

Setup: a second domain, disjoint relations and entities from
all prior phases, with a different uncertainty type (for
example: Phase 1-3 used missing-fact uncertainty; Phase 4
uses conflicting-evidence uncertainty, where two rules
disagree). The researcher specifies the domain and the action
interface. The researcher does NOT specify any inquiry
mapping for the new uncertainty type.

Check 4A: the learner reifies the new uncertainty type
(Phase 1 checks, applied to the new type).

Check 4B: the learner constructs inquiry guides for the new
uncertainty type without researcher mapping.

Check 4C: the guides select functional inquiry actions in the
new domain (Phase 3 checks, applied to the new domain).

This is the strongest discrimination in the battery. H0
(researcher-driven) predicts failure here by construction:
the researcher never supplied the mapping. H1
(learner-driven) predicts success if the construction
process is genuinely general. A pass here is L3-flavored
evidence under Criterion 0-C (multiple unforeseen forms)
applied to inquiry.

Falsification F-INQ-D: the learner handles the trained
uncertainty type but fails on the novel type, and the
failure analysis shows the construction process branches
on uncertainty type (i.e., it is a menu of researcher
cases, not a general process).

### Controls

Control C1 (scaffolding baseline): the current ACT build
configuration, researcher-supplied guides, same worlds.
Expected: passes Phases 3A-3B (it already does, per
ACT-BUILD-COMPLETE). This control calibrates the world
design: if the learner-driven configuration fails where
the scaffolding configuration passes, the failure is in
Pieces A/B, not the world.

Control C2 (no-inquiry baseline): POLICY_ROOT null. Expected:
constant 0, no inquiry actions. Verifies the world does not
leak inquiry through other channels.

Control C3 (random-guide baseline): guides with random
payload[0]. Expected: actions do not correlate with
uncertainty and do not reduce it. Verifies the checks are
not vacuous.

## 5. Prereg shape

A future prereg author (not this scout) would freeze:

**Predictions:**

- P-INQ1 (reification): after N -2 admissions in a fresh
  domain, exactly N UNCERTAINTY nodes exist with correct
  ref[0] linkage, all with learner-side creation traces.
- P-INQ2 (construction): for each live UNCERTAINTY node, one
  ACTION-GUIDE appears within K events, anchored at the
  uncertainty node, selecting the information-seeking act.
  (N, K frozen in prereg.)
- P-INQ3 (attribution): swap test passes; action-uncertainty
  correlation exceeds action-position correlation at p < 0.05
  (exact test frozen in prereg).
- P-INQ4 (functionality): post-inquiry query success rate on
  previously -2 keys exceeds 80 percent (threshold frozen).
- P-INQ5 (transfer): Phase 4 checks pass on the novel
  uncertainty type with zero researcher mapping.

**Falsification:**

- F-INQ1: any UNCERTAINTY node with scaffolding authorship.
- F-INQ2: any ACTION-GUIDE with researcher-authored mapping.
- F-INQ3: B4 swap test fails (position beats uncertainty).
- F-INQ4: novel-type transfer fails AND failure analysis
  shows type-branching in the construction process.
- F-INQ5: K-ACT2 violation found by source inspection
  (task/uncertainty/domain branches in core or in the
  learner-side construction process).

**Kill bars (frozen in prereg):**

- K-INQ1: prereg frozen alone before implementation; K1
  ordering verified.
- K-INQ2: zero researcher-authored uncertainty-to-action
  mappings anywhere in source, scaffolding, or fixtures;
  verified by source inspection and white-box creation
  traces.
- K-INQ3: determinism 3/3 byte-identical.
- K-INQ4: pure Zag; zero Python; contaminated paper
  untouched; commits local with explicit pathspecs.

## 6. Dependencies and ordering

- Requires: ACT read path (done, commit `f7d87938f`), CLA-2
  workspace (done, commit `e639904f2`).
- Independent of: COMP-1 (plan construction is not needed
  for single-act inquiry), MUL (no arithmetic needed),
  DEVINT-CLA2 (but S8 inquiry in DEVINT-CLA2 is the natural
  integration target once this frontier passes standalone).
- Recommended order: this frontier's Phases 1-3 standalone
  first; Phase 4 after; DEVINT-CLA2 S8 integration after
  Phase 3 passes.
- Does not require sealed FW1-FW9; uses fresh W6-class
  worlds designed for this experiment (W6 itself is sealed
  and must not be referenced).

## 7. What failure would teach

- Phase 1 fail: the event loop cannot reify its own
  ignorance as workspace content. This localizes a gap in
  the experience-to-structure path, upstream of all
  inquiry. It would indicate that -2 is a dead end in the
  current architecture: an output with no workspace
  consequence.
- Phase 2 fail with Phase 1 pass: uncertainty exists as
  content but no general process maps it to action. The
  D2 derivation is harder than the reference example
  suggests. Failure analysis here distinguishes "the
  process needs more experience" (fixable) from "the
  process needs researcher cases per uncertainty type"
  (fatal to the learner-driven claim).
- Phase 3 fail with Phase 2 pass: guides exist but do not
  track live uncertainty (stale anchoring, or position
  correlation). This would be a B4 failure with the full
  mechanism in place, the most informative possible
  negative: it would show the attribution gap is not
  about missing machinery but about the dynamics of
  guide maintenance.
- Phase 4 fail with Phase 3 pass: the construction process
  is real but narrow (a menu, not a general process).
  This is the bounded-L2 outcome: genuine learner-side
  inquiry within trained types, researcher-bounded
  outside them. Still valuable; still not L3.

## 8. One-System accounting (scout; measured at implementation)

- Cognition source lines: 0 in this scout. The future
  implementation adds two learner-side workspace processes
  (reification, guide construction). Both must use generic
  primitives only. No core changes authorized.
- New hardcoded semantic cases: 0 (any found fails K-INQ2).
- New modes: 0. New bridges: 0. New task-specific
  handlers: 0.
- Learner-state structures created by the experiment:
  UNCERTAINTY nodes and inquiry ACTION-GUIDEs (workspace
  content, learner-owned).

## Verdict

**INQUIRY-SCOUT-COMPLETE.** The gap is specified as two
missing learner-side pieces (uncertainty reification,
inquiry guide construction) behind the already-built ACT
read path. The difference from H-EXP2 v2 is precise:
researcher-specified scoring over a researcher-enumerated
family versus learner-constructed uncertainty-to-action
mapping with no scoring rule in source. The four-phase
discriminating experiment is designed so H-EXP2-style
machinery cannot pass it alone. Prereg shape, controls,
dependencies, and failure localizations are specified.
Zero source lines; zero modes, bridges, handlers, or
semantic cases; analysis only.
