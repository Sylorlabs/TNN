# CLUSTER_FINAL.md -- Final synthesis of the Cluster 1 + Cluster 2 discrimination program

Wave: wave-20261001-2321pdt, lane CLUSTER-FINAL.
Frozen artifact under test throughout: TNN-2, tnn2.zag
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
freeze_shim2_bin
9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954.

Lineage: BATTERY-CLUSTER/CLUSTER_ANALYSIS.md (committed at
55ee13a1c; JUDGE_BRIEF at 335b169ae), which clustered the
post-freeze sealed adversarial battery 1/6 PASS signatures
(PF-A1, PF-B1, PF-B2, PF-C1, PF-C2, v3 M1, v3 M2, v3 M3) into
two shared architectural causes and proposed discriminating
experiments E1-E8; CLUSTER-SYNTHESIS/CLUSTER_SYNTHESIS.md
(which recorded E8 as PENDING); BATTERY-E8/E8_RUN.md and
JUDGE_BRIEF.md (RENDER_SHA c7c70b934), which completed the
program with verdict E8-BANDWIDTH.

This document folds E8 into the cluster synthesis and states
the final architectural implications. It is a synthesis, not
new evidence: it adds no experiments, no repairs, and no claims
beyond what the cited verdicts establish. It proposes no
patch; repair design is TNN-3 governance per the no-patch-treadmill
rule.

## 1. Final per-hypothesis status

### 1.1 Cluster 1: DERIVATION SUBORDINATION

| Hypothesis | Verdict | Deciding lane | Run commit | Prereg commit |
|---|---|---|---|---|
| H1a (read-path precedence) | CONFIRMED as pure read-path precedence | E4-PRECEDENCE | 61df738fe | b63f80289 |
| H1b (instance-only write path) | CONFIRMED (behavioral + state) | E5-INSTANCE-ONLY | 8510feee6 (merge 79cb53c08) | 282c8301e |
| H1c (no standing derived structure) | KILLED | E1-FIRSTCLASS | f5b1bab41 | 793abbf65 |
| H1d (oracle-verified traversal) | SUPPORTED in refined form (assembly real, selection oracle-dependent) | E3-ORACLE-DEPENDENT | impl ce46b327a (see BATTERY-E3 lane) | a17a276c8 |

Decided evidence in brief. H1a: the E4 precedence-reversal
world shows a licensed derived structure (id=13,
subj=72201, rel=72219, answer=72295, both-hop licensed
evidence) persisting intact through the flat-fact/contradiction
sequence; the pre-contradiction probe returns the flat wrong
fact 72299 (PREFLAT) while the derived structure exists
underneath; after licensed contradiction teaches the derived
value, the read path settles on 72295 (POST). ev_query
consults the flat fact lookup before construction/consultation,
so a flat hit preempts the derived structure; the deeper-suppression
alternative is disfavored by the untouched inspector record.
H1b: contradicting two instances of a two-hop derived law
(+20 on two instance keys) never lifts revision to the law
level; the unseen third instance returns the old law's derived
answer (72323), the analogous relation is untouched (72421),
unanimously across 3 fresh-state runs in both oracle-present
and blind driver conditions; the inspector shows five licensed
derived structures including one on the held-out instance,
contradiction facts left no persistent structure, and
LAWSTRUCT=0 on all runs. H1c: E1-W2 carries exactly one
persistent licensed derived structure (id=13) that survives a
contradiction while the bar probe returns the flat direct fact
(71213), the clean "present but subordinated" signature; E1-W4
carries two licensed structures (ids 15, 26) with probes
returning derived answers 71595/71596. H1d: blind composition
assembles executable 4-op ISA graphs, licenses each step with
ET_DEP edges, promotes them as MAP nodes, and executes them
(E3A blind 2/2 assembly intact; E3B blind emits exactly the
pre-registered spurious outputs 80971/80972), but SELECTION
fails blind: with two executable chains the masked policy
accepts the first candidate in deterministic BFS order (E3B
blind 0/2; oracle-present 2/2).

### 1.2 Cluster 2: GUIDE CONTENT DECOUPLING

| Hypothesis | Verdict | Deciding lane | Run commit | Prereg commit |
|---|---|---|---|---|
| H2a (absent content channel) | REFINED (subject tag reaches ACT as recency gate; distinguishing (s,r) content never read; further narrowed by E8) | E6-CONTENT-READ / E8-BANDWIDTH | 486c13c5c / c7c70b934 | 58811f3a5 / 034ecbd35 |
| H2b (concurrency collapse) | KILLED | E2-CONTENT-BLIND | 6c9d96cef (render 524eca821) | 229cf5263 |
| H2c (sticky guide lifecycle) | CONFIRMED as H2C-STICKY (guide records never retired/updated) | E6-CONTENT-READ | 486c13c5c | 58811f3a5 |
| H2d (output vocabulary bottleneck) | CONFIRMED as contributing cause (output bandwidth in causal chain; 30-vs-0 carried by candidate-selection) | E8-BANDWIDTH | c7c70b934 (tools eb854c45d) | 034ecbd35 |

Decided evidence in brief. H2a refined: E6 ablation probes on
frozen TNN-2 state show the ACT path observably reads guide
content fields: zeroing the guide subject field (F4) flips
CHOICE 30 to CHOICE 0 (byte-identical to the degenerate
empty-state transcript), and zeroing the guide action-value
field (F20) also flips to 0, while zeroing the uncertainty
node's (subject, relation, marker) content fields (UC) leaves
CHOICE 30 unchanged. What never reaches ACT is the
distinguishing (subject, relation) uncertainty content that
would let ACT vary its action by which uncertainty is live, how
many are concurrent, or whether one resolved. E8 narrows this
further: with guide presence held constant (exactly one live
guide, no concurrency, no resolution), E8-A (in-context
actionable guide) yields CHOICE 30 and E8-B (aged
non-actionable guide) yields CHOICE 0, byte-identical across
3 fresh-state runs per world. So content as contextual
actionability reaches the selection stage (the candidate rule
reads the guide's content key against context), and H2a's
surviving precise claim is that subject-identity content of an
actionable guide does not differentiate the emitted action
(E2's result stands for its instrument: two single actionable
in-context guides differing only in missing subject yield
byte-identical CHOICE 30). H2b: E2's single-guide content
discrimination test with no concurrency produces byte-identical
actions, so constant-30 behavior is not a concurrency artifact.
H2c: E6 guide-store inspector dumps show GUIDE/UNCERT lines
byte-identical before and after resolution on all three chains;
the resolution OBSERVE teaches one fact node and advances the
log, but no guide record is retired, updated, unlinked, or
aged. H2d: per the frozen E8 task mapping, the 30-vs-0
difference with presence held constant puts output bandwidth in
the causal chain of whether guide-content differences manifest
behaviorally; the mechanism notes the {0, 30} channel proved
sufficient and the differentiation was carried by the
candidate-selection stage, not by a richer emission vocabulary.

## 2. Final refined shared causes

### 2.1 Cluster 1 final shared cause

Derived structures exist (licensed, persistent, surviving
contradiction), but they have no privileged standing in the
read path. The flat instance-fact layer is consulted first and
wins whenever it has an entry (H1a, pure ordering, no layer
damage). Contradiction and promotion writes land only in the
flat instance layer; no operator writes to an abstraction or
law layer, so nothing aggregates per-instance patches into a
standing law representation (H1b, behavioral and state). Where
the flat layer is silent, construction runs blind and emits
(H1d refined): assembly plus execution are real, but selection
among competing candidate chains is oracle-dependent, so every
correct composition observation to date is BFS enumeration
plus oracle selection, not selective construction. The cluster
name DERIVATION SUBORDINATION is vindicated as a decided,
measured property (precedence ordering plus instance-only
writes plus oracle-dependent selection), not a surmise.

### 2.2 Cluster 2 final shared cause

Guide records are written once and never retired, updated, or
aged by resolution (H2c, sticky lifecycle), so resolution can
never change what ACT sees. Of guide content, ACT observably
reads the guide node's subject field (recency gate) and the
guide node's action-value field (the construction constant 30),
but never the uncertainty node's distinguishing (subject,
relation, marker) content (H2a refined by the E6 ablations).
Subject-identity content of an actionable guide does not
differentiate the emitted action (E2 stands for its
instrument), yet contextual actionability of a guide does reach
the selection stage and differentiate behavior when the output
channel can express it (E8: 30 vs 0 with presence held
constant, carried by candidate-selection). Single-guide
content discrimination does not exist even without concurrency
(H2b killed by E2), so the constant-30 behavior is not a
concurrency artifact. The cluster name GUIDE CONTENT
DECOUPLING is vindicated as the deeper cause: the channel from
guide content to action is decoupled at the subject-identity
level while selection-stage actionability and a sticky
lifecycle explain the rest.

## 3. Architectural implications (no-patch-treadmill framing)

Per the owner 2026-10-01 no-patch-treadmill rule, the question
is what ONE general substrate change would need to address to
fix both clusters at once, not a patch per hypothesis. The
two clusters share one deeper root, now fully evidenced by
E8: no learner-originated derived representation (composed
graph, guide content, revision pattern) has a privileged
channel into the behavior-driving operators; only flat
primitive signals drive behavior. A general change that
fixed multiple worlds at once would therefore have to be a
single coherent standing-and-lifecycle architecture with
these properties:

1. Privileged standing for derived structures in the read
   path. ev_query and the answer operator must consult
   learner-created derived structures (composed graphs, law
   representations) with priority over, or integrated with,
   the flat instance-fact lookup, rather than the flat lookup
   preempting them by ordering. This is the locus that fixes
   PF-A1, PF-C1, and v3 M1 together (H1a), as one operator
   change rather than per-world probes.

2. Write-through to the abstraction layer. Contradiction and
   promotion operators must write through to law/abstraction
   representations when per-instance evidence implies a
   law-level change, instead of landing only in the flat
   instance layer with LAWSTRUCT=0 forever. This is the locus
   that fixes PF-C2 and v3 M3 together (H1b): one write-path
   completeness change, not per-relation handlers.

3. Selection as a learner-side capability, not oracle-verified
   trial. Assembly plus execution work blind; what fails is
   choosing among executable candidates without the
   QUERY-carried expected value. The general change must give
   the learner its own candidate-selection machinery driven by
   learned criteria, so construction is selective rather than
   BFS enumeration plus oracle selection (H1d, and E3B 0/2
   blind as the multi-world signature).

4. A general guide lifecycle. Guide records need
   retire/update/age operators fired by resolution and
   contextual change, as one lifecycle machinery, rather than
   append-only sticky records (H2c). One change here closes
   the reason resolution can never change what ACT sees
   across PF-B1, PF-B2, and v3 M2.

5. Full guide-content legibility in action selection. The
   content channel into ACT must carry the distinguishing
   uncertainty content (which uncertainty is live, how many
   concurrent, whether resolved), not just a subject tag used
   as a recency gate plus a construction constant. E8 shows
   selection already reads content keys against context, so
   the general change extends content legibility to the
   selection stage rather than adding a new operator per
   content field.

Properties 1 and 2 are one cluster-1 read/write-path change;
properties 4 and 5 are one cluster-2 lifecycle/content-channel
change; property 3 stands over composition. The shared root
says they should be designed as one substrate change, not
three: give learner-created structures standing in the read
paths, completeness in the write paths, and legibility in the
selection paths of the behavior-driving operators. What is
NOT proposed here: any specific operator, mode, bridge,
handler, or semantic case. That design is TNN-3 governance.

## 4. Cross-cluster notes carried forward

1. The E3 mandate stands. Every construction claim whose
   evidence came from unmasked QUERY runs must be re-examined
   blind. PF-A2's 2/2 valid-composition result is re-described
   as BFS enumeration plus oracle selection; no construction
   verdict may rest on an unmasked QUERY-carried expected
   value again.

2. Subordination, not absence, is the story of the program.
   H1c's death (licensed derived structures persist) and H2a's
   refinement (guide content fields are written and partly
   read) both moved the account from "the representation is
   missing" to "the representation exists but the operators
   subordinate or ignore it." E8 completes this arc for
   Cluster 2: the content difference that does differentiate
   behavior (actionability) is carried by selection, not by a
   missing representation.

3. Criterion 0 is not met by anything in this program. All
   E-lanes record C0-A through C0-D NOT MET: the derived
   structures are frozen-mechanism artifacts
   (trial-constructed graphs), not learner-invented
   representations. No L3 language is used and no L3-adjacent
   progress is claimed.

4. E7 (sequential two-guide world, testing H2b) was
   deprioritized in the analysis ordering and never ran; H2b
   was killed by E2 for this instrument without it. No verdict
   depends on E7.

## 5. What remains open

1. No third action was observed in any E8 context; the
   protocol-reachable vocabulary stayed {0, 30}. Whether ACT
   can ever emit an action outside {0, 30} on frozen TNN-2 is
   undecided. H2d is confirmed as a contributing cause (the
   {0, 30} channel proved sufficient for the observed content
   difference and the differentiation was carried by
   candidate-selection), so a literal "lacks bandwidth"
   reading of H2d is not what E8 demonstrated.

2. The precise interaction between sticky lifecycle (H2c) and
   content legibility (H2a refined) is not experimentally
   separated: with guides never retired, it is undecided how
   much of the constant-action signature is lifecycle versus
   channel, though both are confirmed properties of frozen
   TNN-2.

3. No repair is proposed and no substrate change is designed
   here. The five properties in section 3 are requirements a
   general change must address, for TNN-3 governance to take
   up.

## 6. Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-CLUSTER/CLUSTER_ANALYSIS.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E1/E1_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E2/E2_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/E3_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E4/E4_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E5/E5_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E6/E6_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E8/E8_RUN.md, JUDGE_BRIEF.md, PREREG_E8.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/CLUSTER-SYNTHESIS/CLUSTER_SYNTHESIS.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/CLUSTER-FINAL/NAMECHECK.md

All lane commits are local only on branch tnn-native-lab, never
pushed. Every E-lane reports all process bars PASS (K1 prereg
ordering, K2 determinism byte-identical 3/3, K3 frozen binary
hashes, K4 seal integrity, K6 no-leak), calibration gates PASS,
and K-C0A (zero new semantic cases) PASS; see the individual
E*_RUN.md reports. All work pure Zag under the safebin PATH;
no forbidden interpreter invoked in any lane per the recorded
Step 0 verifications.
