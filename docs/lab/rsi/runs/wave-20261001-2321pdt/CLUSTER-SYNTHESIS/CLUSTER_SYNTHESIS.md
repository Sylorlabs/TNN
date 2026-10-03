# CLUSTER_SYNTHESIS.md -- Decided evidence from the post-freeze battery cluster discriminators

Wave: wave-20261001-2321pdt, lane CLUSTER-SYNTHESIS.
Frozen artifact under test: TNN-2, tnn2.zag
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
freeze_shim2_bin
9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954.
Analysis spec: BATTERY-CLUSTER/CLUSTER_ANALYSIS.md (committed at
55ee13a1c; JUDGE_BRIEF at 335b169ae), which clustered the
post-freeze sealed adversarial battery 1/6 PASS signatures
(PF-A1, PF-B1, PF-B2, PF-C1, PF-C2, v3 M1, v3 M2, v3 M3) into
two shared architectural causes and proposed discriminating
experiments E1-E8.

This document is a synthesis of decided evidence, not new
evidence. It adds no experiments, no repairs, and no claims
beyond what the cited verdicts establish. E8 (H2d, Cluster 2
output bandwidth) is still running; it is recorded as PENDING
throughout.

## 1. Cluster 1: DERIVATION SUBORDINATION

Original shared cause (mechanism-level claim from the analysis):
the answer and revision operators resolve through a flat
instance-fact layer with no privileged standing layer for
derived structures, so composed graphs, procedure abstractions,
and law-level representations are either absent or subordinated
in the read path. Four discriminating hypotheses were posed;
three have decided evidence, one in refined form.

### 1.1 H1a (read-path precedence inversion): CONFIRMED as pure read-path precedence

Verdict: E4-PRECEDENCE, lane BATTERY-E4. Runs committed at
61df738fe; tools committed at 67680ebb1 and f26ddb294; prereg
frozen at b63f80289 (prereg restored at 5a2c7c91c after an
unrelated accidental deletion, content unchanged, SHA-256
b3fd77c2c1c4037ded940072fa147d6fd0a1fd912ac0054038d487bbbca40b74).

Decided evidence: the precedence-reversal world (E4-W1) shows a
licensed derived structure (id=13, subj=72201, rel=72219,
answer=72295, both-hop licensed evidence) persisting fully
intact through the whole flat-fact/contradiction sequence. The
pre-contradiction probe returns the flat wrong fact 72299
(PREFLAT, subordination replicated) while the derived structure
exists underneath; after the licensed contradiction teaches the
derived value, the read path settles on the derived value 72295
(POST). The flat wrong fact leaves no trace in the derived
structure's evidence. The control world E4-W0 (no flat fact)
forms the same licensed structure and the probes return the
derived answer 72195. The only remaining account is ordering:
ev_query consults the flat fact lookup before
construction/consultation, so a flat hit preempts the derived
structure. The deeper-suppression alternative (flat/contradiction
machinery degrading the derived layer beyond ordering) is
disfavored by the untouched inspector record.

Status: H1a CONFIRMED, refined from a kill-or-confirm framing to
a pure read-path precedence account. Recorded confound carried
forward: the promotion probes run the trial, which verifies
against the QUERY-carried expected value (see H1d below); the
discriminating leg (DERIVED via the oracle-blind inspector) is
unconfounded.

### 1.2 H1b (instance-only write path): CONFIRMED at both the behavioral and state levels

Verdict: E5-INSTANCE-ONLY, lane BATTERY-E5. Runs committed at
8510feee6 (merged at 79cb53c08); tools committed at c8d9f14e1;
prereg frozen alone at 282c8301e (SHA-256
bc15a264293469319e8de3b63aee755e50410547c48648e08ab2ae963bffeefd).

Decided evidence: contradicting two instances of a two-hop
derived law (+20 on two instance keys) never lifts revision to
the law level. The unseen third instance returns the old law's
derived answer (72323) and the analogous relation is untouched
(72421), unanimously across 3 fresh-state runs in both the
oracle-present and blind driver conditions. The white-box
inspector shows five licensed derived structures (ids 21, 32,
43, 62, 73, each with both-hop licensed evidence), including one
on the held-out third instance (id=62); the contradiction facts
(72301,72809,72341) and (72302,72809,72342) left no persistent
structure and did not revise the derived structures. Instances 1
and 2 keep their original derived answers (72321, 72322) in
state while behavior returns the flat revised values (72341,
72342), the E1-W2 subordination pattern. LAWSTRUCT=0 on all
runs: zero cross-instance aggregation at the law relation. The
discriminating probes ran blind per the E3 mandate (see section
3): the oracle-present condition demonstrates masking (the
oracle-carried composed values verify-accept the stale chain),
while the blind condition carries the verdict.

Status: H1b CONFIRMED. This is now the best-supported locus in
Cluster 1: even with a genuine two-hop derived law and licensed
per-instance structures present, revision writes stay
instance-flat. Joined to PF-C2 (no cross-relation transfer) and
v3 M3 (generalization 0/2, per-key patching). The law-level
write path remains unobserved in frozen TNN-2.

### 1.3 H1c (no standing derived structure): KILLED

Verdict: E1-FIRSTCLASS, lane BATTERY-E1. Runs committed at
f5b1bab41; tools committed at 4afcd9f3b; worlds committed at
aa38427b8; prereg frozen alone at 793abbf65 (SHA-256
7632cf5a870ac0a71934fbac8274fc5950756d2f93c6d9be127ab827bd84e03c).
Notably, this was a prereg prediction miss (predicted
E1-ABSENT); the white-box inspector falsified the prediction.

Decided evidence: licensed derived structures persist in frozen
TNN-2 state. E1-W2 carries exactly one persistent structure
(id=13, subj=71201, rel=71709, answer=71203, both chain hops
licensed, the derived answer never taught on 71709) that
survives a contradiction while the bar probe returns the flat
direct fact (71213): the clean "present but subordinated"
signature E1 was built to discriminate. E1-W4 carries two
licensed derived structures (id=15, id=26) and the probes return
the derived answers 71595/71596 (FIRSTCLASS per the frozen
rule). E1-W1 shows the flat fact answering (71999) with zero
persistent structures of any kind, and E1-W3 shows
per-instance promoted structures only (ids 20, 34, single
evidence each, no law-level derived structure), supporting H1b.

Status: H1c KILLED by white-box evidence, consistent across 3
runs per world. H1c was the only hypothesis whose death was the
cluster's riskiest possible outcome; its death is what forced
the refined shared cause in section 1.5. Recorded confound
carried forward: E1-W4's behavioral leg (probes returning
derived answers) cannot distinguish structure-driven answers
from oracle-verified BFS traversal; that is H1d's question,
decided by E3. The structural leg (licensed derived structures
exist in persistent state) is unconfounded and is what kills
H1c.

### 1.4 H1d (oracle-verified traversal, not construction): SUPPORTED in refined form

Verdict: E3-ORACLE-DEPENDENT, lane BATTERY-E3. Implementation
committed at ce46b327a; prereg frozen at a17a276c8; sealed
worlds, oracles, manifest, and the 12 sealed runs committed
after (E3_RUN.md and JUDGE_BRIEF.md).

Decided evidence: the naive H1d prediction ("blind composition
emits nothing") does not hold. With the oracle withheld at the
transport (e3_blind_driver_bin, QUERY arity enforced, ev_query
with expected=-2 and masked=1), the trial still assembles
executable 4-op ISA graphs at runtime, licenses each step with
ET_DEP edges to taught facts, promotes them as MAP nodes, and
executes them (E3A blind bar probes 2/2, assembly intact; E3B
blind emits answers 80971/80972, exactly the pre-registered
spurious prediction). What fails blind is SELECTION: with two
executable chains available, the trial's masked policy (accept
first executable candidate) emits the first chain in
deterministic BFS order. E3B blind scores 0/2 with the exact
predicted spurious outputs; E3B oracle-present scores 2/2
(validity gate: the sealed target is reachable and
oracle-selectable). Byte-identical transcripts across 3
fresh-state runs per condition. The blind distractor probes show
the trial cannot withhold composition either: it enumerates
chains relation-agnostically (MAP(80201,80629) in state, spurious
80921/80922 emitted on the novel relation).

Status: H1d SUPPORTED in refined form. The refined claim:
construction (assembly plus execution) works blind; correct
composition observations in the PF battery depended on the
trial's unmasked verifier (t2_try_verify: accept iff executed
output equals the QUERY-carried expected value) to SELECT the
right candidate among multiple executable BFS chains. PF-A2's
2/2 valid-composition result is re-described as BFS enumeration
plus oracle selection, not selective construction.

### 1.5 Refined shared cause for Cluster 1

Before the discriminators, the shared cause was stated as "the
answer and revision operators resolve through a flat
instance-fact layer with no privileged standing layer for
derived structures." The decided evidence refines it to:

Derived structures exist (licensed, persistent, surviving
contradiction), but they have no privileged standing in the
read path. The flat instance-fact layer is consulted first and
wins whenever it has an entry (H1a, pure ordering, no layer
damage). Contradiction and promotion writes land only in the
flat instance layer; no operator writes to an abstraction or
law layer, so nothing aggregates per-instance patches into a
standing law representation (H1b, at both behavioral and state
levels). Where the flat layer is silent, construction runs
blind and emits (H1d refined): assembly plus execution are
real, but selection among competing candidate chains is
oracle-dependent, so every correct composition observation to
date is BFS enumeration plus oracle selection, not selective
construction.

The cluster name DERIVATION SUBORDINATION is vindicated as the
deeper cause; the subordination is now a decided, measured
property (precedence ordering plus instance-only writes plus
oracle-dependent selection), not a surmise.

## 2. Cluster 2: GUIDE CONTENT DECOUPLING

Original shared cause (mechanism-level claim from the analysis):
the ACT operator reads uncertainty guides only as a
presence/absence bit; guide content (which uncertainty is live,
how many are concurrent, whether one resolved) has no write path
into action selection. Four discriminating hypotheses were
posed; three have decided evidence, one is pending (E8).

### 2.1 H2a (absent content channel): REFINED by E6, not dead but no longer the root account

Verdict: E2-CONTENT-BLIND, lane BATTERY-E2. Runs committed at
6c9d96cef (RENDER_SHA recorded at 524eca821); tools committed
at 4900c177d; prereg frozen alone at 229cf5263 (SHA-256
bdb6eddce83d72a3273cf6e829cd56fab457a7cc98fffafa882b6c45746abd83).

Decided evidence: two single guides with materially different
content (different missing facts, different resolution-state
context), each run in isolation with no concurrency anywhere,
produce byte-identical CHOICE 30 actions across all 3
fresh-state runs. The degenerate control yields CHOICE 0, so the
presence bit reads correctly in this id block. The
constant-guide story is not a concurrency phenomenon: this
killed H2b for this instrument.

E6 then refined what H2a could mean. Verdict:
E6-CONTENT-READ, lane BATTERY-E6. Runs committed at 486c13c5c
(RENDER_SHA recorded at a95e8b05b); tools committed at
fbe5ab33e; prereg frozen alone at 58811f3a5 (SHA-256
80ea66f7f9cf292b0d15f5b586e968fea280a39d303c1698985a8d5f3c7f87a0).
The ablation probes on frozen TNN-2 state show the ACT path
observably reads guide content fields: zeroing the guide
subject field (F4) flips CHOICE 30 to CHOICE 0
(byte-identical to the degenerate empty-state transcript), and
zeroing the guide action-value field (F20) also flips to 0. But
zeroing the uncertainty node's (subject, relation, marker)
content fields (UC) leaves CHOICE 30 unchanged. So the naive
H2a claim ("guide content never reaches action selection in any
form") is too strong: the guide node's subject tag reaches ACT
as a recency gate and the action value 30 is a construction
constant read from the guide record. What never reaches ACT is
the distinguishing (subject, relation) uncertainty content that
would let ACT vary its action by which uncertainty is live, how
many are concurrent, or whether one resolved.

Status: H2a REFINED. The root cause is not literally absent
content, but a decoupled channel: the only content that reaches
ACT is a subject tag used as a recency gate plus a constant
action value, so the action is invariant under content,
concurrency, and resolution state. The cluster name GUIDE
CONTENT DECOUPLING is vindicated as the deeper cause.

### 2.2 H2b (concurrency collapse): KILLED

Verdict: E2-CONTENT-BLIND (same lane and commits as section
2.1). The discriminating test was exactly H2a versus H2b:
single-guide content discrimination with no concurrency. Two
different single uncertainties in separate fresh runs produce
byte-identical actions (30=30), which H2b's prediction of
cross-phase distinct actions fails. The constant-30 signature
is not a concurrency phenomenon.

Status: H2b KILLED for this instrument. The lane note that v3
M2-W2's single-guide no-resolution-transition weakened a pure
concurrency story is now corroborated: single-guide content
discrimination never existed.

### 2.3 H2c (sticky guide lifecycle): CONFIRMED (H2C-STICKY)

Verdict: E6-CONTENT-READ with H2C-STICKY, lane BATTERY-E6
(same commits as section 2.1).

Decided evidence: the guide-store inspector dumps show the
GUIDE/UNCERT lines byte-identical before and after resolution
on all three chains. The resolution OBSERVE teaches one fact
node (NODES 7->8->9, EDGES 5->7->9) and advances the log, but
no guide record is retired, updated, unlinked, or aged: every
field of both guide nodes and both uncertainty nodes persists
byte-identical through both resolutions. No overwrite, no aging
counter, no eviction, no retire operator fires. In parallel,
the natural sequence shows the action invariant (CHOICE 30 at
s2 with two live guides, s4 with one resolved, s6 with both
resolved), which is why PF-B1's post-resolution ACT stayed 30.

Status: H2c CONFIRMED as a lifecycle property
(H2C-STICKY). Guides are append-only in frozen TNN-2; because
no retire/update operator exists, resolution can never change
what ACT sees.

### 2.4 H2d (output vocabulary bottleneck): PENDING (E8 still running)

E8 is the orthogonal-signal ACT bandwidth probe, executed by
lane BATTERY-E8 (replacement worker; NAMECHECK.md records a
passed Step 0 and the discriminator mapping). At the time of
this synthesis, the E8 lane contains only NAMECHECK.md; no
worlds, tools, runs, or verdict are committed. The frozen bar
for H2d: ACT emits a third distinct action in any frozen-TNN-2
context; PASS kills H2d.

Status: PENDING. The E6 reading redirects Cluster 2 toward
H2d (the distinguishing uncertainty content has no read path
into ACT at all, and the only content that reaches ACT is the
subject tag plus the construction-constant action value 30,
which the output cannot vary), but that redirection is an
inference, not a decided verdict, until E8 lands.

### 2.5 Refined shared cause for Cluster 2

Before the discriminators, the shared cause was stated as
"ACT reads uncertainty guides only as a presence/absence bit;
guide content has no write path into action selection." The
decided evidence refines it to:

Guide records are written once and never retired, updated, or
aged by resolution (H2c, sticky lifecycle), so resolution can
never change what ACT sees. Of guide content, ACT observably
reads the guide node's subject field (recency gate) and the
guide node's action-value field (the construction constant 30),
but never the uncertainty node's distinguishing (subject,
relation, marker) content (H2a refined by the E6 ablations).
Single-guide content discrimination does not exist even without
concurrency (H2b killed by E2), so the constant-30 behavior is
not a concurrency artifact. The remaining open question is
whether the invariance is also an output-bandwidth limit at
the ACT operator (H2d), which E8 will decide.

## 3. Cross-cluster implications

1. The E3 mandate. Every construction claim whose evidence
   came from unmasked QUERY runs must be re-examined blind.
   The PF battery's mechanism (a) verdict (FAILS) stands and is
   sharpened: the failure is not merely retrieval-shadowing
   (PF-A1) but oracle-dependent selection (E3B 0/2 blind with
   the exact predicted spurious outputs). The E5 lane complied
   with this mandate: its discriminating probes ran blind and
   its oracle-present condition demonstrated the masking that
   blind probing removes.

2. The two clusters share one deeper root, now better
   evidenced. The analysis hypothesized that no
   learner-originated derived representation (composed graph,
   guide content, revision pattern) has a privileged channel
   into the behavior-driving operators; only flat primitive
   signals drive behavior. The decided evidence supports the
   first half precisely: derived structures exist but have no
   privileged standing in the read path (Cluster 1), and guide
   records persist but resolution never changes what ACT sees
   (Cluster 2). The clusters remain separate because their loci
   and discriminating instruments differ.

3. Subordination, not absence, is the story of this wave. H1c's
   death (licensed derived structures persist) and H2a's
   refinement (guide content fields are written and partly
   read) both moved the account from "the representation is
   missing" to "the representation exists but the operators
   subordinate or ignore it." A TNN-3 substrate change, when
   proposed, will be about privileged standing and write-path
   completeness (one general change covering PF-A1, PF-C1,
   PF-C2, v3 M1, v3 M3 in Cluster 1; and a lifecycle plus
   content-channel change in Cluster 2), not about adding a
   missing representation from scratch.

4. PF-A2's evidentiary status is settled. The analysis's
   methods note discounted PF-A2 as a weak instrument; E3
   supplies the mechanism (oracle-verified traversal) that made
   it weak, and the 2/2 valid-composition result is now
   re-described as BFS enumeration plus oracle selection. No
   construction verdict should ever rest on an unmasked
   QUERY-carried expected value again.

## 4. What is NOT decided

1. E8 is pending. H2d (ACT output vocabulary bottleneck) has
   no verdict; the E6 redirection toward H2d is an inference,
   not decided evidence. Cluster 2's synthesis is complete
   except for this one discriminator.

2. No repair is proposed. Per the owner 2026-10-01
   no-patch-treadmill rule and per every E-lane's
   no-patch-treadmill section, the discriminating experiments
   test substrate properties; confirmed hypotheses would
   motivate one general substrate change fixing multiple
   worlds at once, but that is TNN-3 business, not this
   synthesis.

3. Criterion 0 is not met by anything here. All E-lanes record
   C0-A through C0-D NOT MET: the derived structures are
   frozen-mechanism artifacts (trial-constructed graphs), not
   learner-invented representations. No L3 language is used in
   this synthesis, and no L3-adjacent progress is claimed.

4. E7 (sequential two-guide world, testing H2b) was deprioritized
   in the analysis ordering and never ran; H2b was killed by E2
   for this instrument without it. No verdict depends on E7.

## 5. Verdict and commit register

| Hypothesis | Verdict | Deciding lane | Run commit | Prereg commit |
|---|---|---|---|---|
| H1a (read-path precedence) | CONFIRMED (pure read-path precedence) | E4-PRECEDENCE | 61df738fe | b63f80289 |
| H1b (instance-only write) | CONFIRMED (behavioral + state) | E5-INSTANCE-ONLY | 8510feee6 (merge 79cb53c08) | 282c8301e |
| H1c (no standing derived structure) | KILLED | E1-FIRSTCLASS | f5b1bab41 | 793abbf65 |
| H1d (oracle-verified traversal) | SUPPORTED (refined: assembly real, selection oracle-dependent) | E3-ORACLE-DEPENDENT | E3 runs commit (see BATTERY-E3 lane) | a17a276c8 |
| H2a (absent content channel) | REFINED (subject tag read as recency gate, action value 30 constant; distinguishing content never read) | E6-CONTENT-READ | 486c13c5c (render 486c13c5c / a95e8b05b) | 58811f3a5 |
| H2b (concurrency collapse) | KILLED | E2-CONTENT-BLIND | 6c9d96cef (render 524eca821) | 229cf5263 |
| H2c (sticky guide lifecycle) | CONFIRMED (H2C-STICKY) | E6-CONTENT-READ | 486c13c5c | 58811f3a5 |
| H2d (output vocabulary bottleneck) | PENDING | E8 (running) | - | - |

All lane commits are local only on branch tnn-native-lab, never
pushed. Every E-lane reports all process bars PASS (K1 prereg
ordering, K2 determinism byte-identical 3/3, K3 frozen binary
hashes, K4 seal integrity, K6 no-leak), calibration gates PASS,
and K-C0A (zero new semantic cases) PASS; see the individual
E*_RUN.md reports for the full records. All work pure Zag under
the safebin PATH; no forbidden interpreter invoked in any lane
per the recorded Step 0 verifications.

Evidence paths:
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-CLUSTER/CLUSTER_ANALYSIS.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E1/E1_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E2/E2_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/E3_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E4/E4_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E5/E5_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E6/E6_RUN.md, JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E8/NAMECHECK.md (pending)
