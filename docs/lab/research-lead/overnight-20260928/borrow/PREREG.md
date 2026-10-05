# PREREG -- BORROW C1531-C1600

Lane `ownership`. Architecture-principle program. Frozen before
implementation.

Not one experiment. Several **competing** architectural hypotheses,
run so they can kill each other.

Governed by STANDING RULES R1-R10, especially:
* R1 no named cognitive modes
* R2 no bridges
* R4 do not design against H16
* R5 steal principles, not subsystems
* R8 no bolt-ons, no LLM modules

---

## 0. THE TARGET, RESTATED FROM C1512

C1512 closed proposal ordering: on a graded family the entire gain
is argmax, which is L2 ranking already held; FO reproduces
everything; gradient reversal flips it completely.

So the open capability is not **choosing among researcher-generated
candidates**. It is:

> changing what gets generated, and how, in a way that survives
> facts-only rebuild and gradient reversal.

And the structural obstacle, per R2, is that we have no shared
substrate property that lets independently learned structures
interact. Every time two structures failed to interact we wrote a
bridge. That produced a bridge-per-pair architecture.

---

## 1. FIVE COMPETING HYPOTHESES

Each is a *substrate property* that, if present and learner-used,
would remove the need for bridges. Each is falsifiable.

### H1 CONTENT-ADDRESSED INTERACTION
Principle stolen from transformers: interaction should be
selected by content, not by a researcher-fixed route.

Substrate property: every learned structure can be referenced by a
**derived key computed from its own content**, and structures can
emit references to other structures by key.

Falsifier: keys are not useful, i.e. structures looked up by
derived key are no better than random lookup.

### H2 LOCAL CONSEQUENCE ADAPTATION
Principle stolen from Hebbian systems: organization should emerge
from local co-activation and consequence, not global constructors.

Substrate property: when two structures are active together and a
consequence follows, a **local** rule strengthens a link between
them. No global pass, no central organizer.

Falsifier: link weights do not predict future usefulness, or
organization does not beat random wiring.

### H3 MISMATCH-DRIVEN RESTRUCTURE
Principle stolen from predictive coding: local mismatch should
drive representational change. NOT a central REVISE_MODE.

Substrate property: a mismatch between predicted and observed
consequence locally modifies the structure that made the
prediction.

Falsifier: mismatch-driven change does not reduce future mismatch,
or only works with a researcher-chosen repair site.

### H4 ATTRACTOR-LIKE SETTLING
Principle stolen from Hopfield/attractor systems: distributed state
should settle toward stable configurations through local
interaction, rather than researcher lookup tables.

Substrate property: activation spreads locally until a stable
pattern is reached. Stability, not identity, is the unit.

Falsifier: settling is unstable, or converges to a fixed point
regardless of input (i.e. degenerates to a constant).

### H5 LEARNED TRANSFORMATIONS
Principle stolen from program synthesis and evolution: successful
structural transformations should become persistent
learner-owned structures, not a fixed researcher mutation menu.

Substrate property: a transformation that produced an improvement
is itself stored as a reusable structure, and can be applied to
new structures later.

Falsifier: stored transformations do not transfer, or degenerate
into an enumerated fixed set (which is H16v3's menu kill).

**These five are run as competing explanations, not as a shopping
list.** A substrate that supports all five trivially is suspicious;
we want to know which one is load-bearing.

---

## 2. FLAGSHIP TEST: BRIDGE-FREE RECRUITMENT

This is the experiment that decides R9.

> Can a structure learned in one functional context be recruited in
> another, without a bridge explicitly written for those two roles?

Design:

* Context 1: the structure is learned to do task role X, where X is
  determined by the substrate, not named in source.
* Context 2: the same structure is needed for task role Y.
* **No bridge, no Y-specific code, no adapter, no hint.**

Then subtract:

* SUBTRACT: the structure is not present. Task Y should fail.
* LEARN: the structure is present from context 1. Task Y should
  succeed without any Y-specific learner work.
* FO: facts about context 1 only, no structure. Should fail.
* TRANSFER-FREE: structure present but never used in context 1
  (fresh structure of the same kind). Distinguishes "the structure
  is generally good" from "experience with X made it fit Y".

Required: the role names X and Y must not appear in source. Roles
are described only in the report.

---

## 3. BRIDGE BASELINE (explicitly marked for deletion)

Per R2, one bridge **is** permitted, as a temporary baseline whose
only purpose is to show the bridge is unnecessary.

```
X_TO_Y_BRIDGE_TEMPORARY_DELETE_ME
```

It is not architecture. It is a control. It must be listed in the
report's delete list, and its existence must not be relied on by
any other measurement.

Purpose: if the bridged version works and the unbridged version
does not, the bridge is measuring the missing substrate property,
and we name that property instead of keeping the bridge.

---

## 4. SELF-DAMAGE CHECK (R7)

Every mechanism is checked for damage to TNN's own operation, not
just task score:

* does persistent state stay addressable after the mechanism runs?
* does the mechanism corrupt its own structures?
* does output production still work?
* does the mechanism's own bookkeeping survive repeated cycles?

A mechanism that raises task score while degrading any of these is
a failure.

---

## 5. BARS

B1  3/3 identical sha256
B2  no named cognitive mode in source (grep-clean; R1)
B3  exactly one bridge present and it is the TEMPORARY_DELETE_ME control
B4  flagship recruitment result printed for all four arms
B5  at least one hypothesis falsified (a program that cannot kill
    anything is not a test)
B6  self-damage check printed
B7  H16v3 audit printed
B8  delete list printed
B9  L3 printed as a value
B10 verdict printed

B5 is a real bar: if nothing is falsified, the lane has failed even
if the mechanism "works".

---

## 6. ORDER OF WORK

Phase 1: establish the flagship recruitment harness on the
simplest possible substrate, with the bridge control. Determine
whether unbridged recruitment is even possible today.
Phase 2: run H1-H5 against that harness.
Phase 3: whichever substrate property turns out to be load-bearing
gets deepened. The others get recorded as falsified or untested.

Phase 1 result decides whether Phases 2-3 are worth running. If
unbridged recruitment is impossible on the current substrate, the
finding is the specific missing property, named.

---

## 7. DISCIPLINE

Pure Zag. `_zag_print`. 3/3. R3 lint must pass.
No named modes in source. At most one TEMPORARY_DELETE_ME bridge.
Hypotheses are stated so they can be killed.