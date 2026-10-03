# CLUSTER_ANALYSIS.md -- Post-freeze battery failure clustering and hypotheses

Wave: wave-20261001-2321pdt, lane BATTERY-CLUSTER.
Scope: the post-freeze sealed adversarial battery (Part 2) 1/6 PASS on
frozen TNN-2 (tnn2.zag a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
freeze_shim2_bin 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954),
plus the v3 validation degenerate signatures (M1 0/8 composition, M2
constant CHOICE 30, M3 per-key patching with stale double-revision and
generalization 0/2). Source docs: BATTERY/PREREG_POSTFREEZE.md (prereg
SHA-256 dcf5e26ac3b095565f7c89926bd63ccb14efda3061cc6985e34c436a2de8037c),
BATTERY/POSTFREEZE_RUN.md, BATTERY/VALIDATION_RUN_V3.md. All transcripts
byte-identical across 3 fresh-state runs (PF-K2 PASS); no-leak clean
(PF-K6 PASS); calibration gates pass on all worlds.

Per the owner 2026-10-01 NO-PATCH-TREADMILL RULE: no patches proposed
here. This document clusters failures by shared architectural cause and
supplies discriminating experiments. No implementation.

## Methods note (not a cause cluster): PF-A2 weak discrimination

PF-A2 (selective composition with distractor) is a weak instrument, not
an architectural finding. Recorded caveat from POSTFREEZE_RUN.md: the
2/2 on the valid-composition probes appears to be via BFS traversal
from the grounded subject (60201->60911->60921) verified against the
oracle expected value carried on the QUERY line, not via selective
procedure abstraction; the 0/2 on the no-spurious probes was answered
via 1-hop BFS (60201->60931). The world as designed does not
discriminate BFS reachability from procedure composition because the
trial can consult the oracle value for verification. Evidentiary weight
for selectivity is therefore discounted; the mechanism (a) verdict
rests on PF-A1 and the v3 M1 results. No calibration gate was violated
(D FAIL, C PASS), so the world is not VOID, but nothing about selective
composition can be concluded from it. Its behavioral signature (flat
traversal plus oracle verification, no procedure abstraction) is
consistent with Cluster 1 below, but per lane instruction it is not
assigned to a cause cluster and carries no verdict weight.

## Cluster 1: DERIVATION SUBORDINATION (the flat layer always wins)

Members: PF-A1 (retrieval shadows construction), PF-C1 (PASS via
direct-fact shadowing, not graph revision), PF-C2 (per-key patch, no
cross-relation transfer), v3-M1 (0/8 composition; K-S5v3(c) struct
FAIL), v3-M3 (per-instance patching; singleton noise incorporated;
generalization 0/2; stale on double-revision/revert).

Shared architectural cause (mechanism-level claim about frozen TNN-2):
the answer and revision operators resolve through a flat
instance-fact layer that has no privileged standing layer for derived
structures. Composed graphs, procedure abstractions, and law-level
representations either do not persist or are subordinate in the read
path, so (i) a direct taught fact on the query relation preempts graph
traversal (PF-A1: taught 60999 returned instead of the 2-hop 60902,
pf_runs/pf_a1_r1.trans lines "ANSWER 60101 60609 60999"); (ii) a
contradiction written as a direct fact shadows the derived graph
instead of revising it (PF-C1: OBSERVED 60501 60909 60513 then
"ANSWER 60501 60909 60513", the promoted 60503 never revised);
(iii) revisions patch instances only, so an observed shift pattern
cannot transfer across relations (PF-C2: revised-relation probe
60621 correct, transfer probe 60711 not 60721). Corroborating: v3 M1
composition 0/8 (all -2, v3_runs/m1w1v3_r1.trans) with the inspector
finding only unlicensed structures (v3_runs/m1_inspect_r1.txt:
"STRUCTURE id=106 ... EVIDENCE count=0"); v3 M3 inspector shows
per-instance structures with per-instance evidence and no law-level
structure (v3_runs/m3_inspect_r1.txt: id=42 subj=52201, id=56
subj=52202, each with own evidence); v3 M3 generalization 0/2
(unseen subjects yield -2) and stale bar probes on double revision
(53209 not 53219; 53803 not 53813). This is a substrate property: the
write and read operators of the answer/revision path admit only
instance-level state, so derived learner representations can never
outrank flat ones.

### Hypotheses (4, structurally different loci)

H1a. Read-path precedence inversion (locus: the answer operator).
(H) The answer operator consults 1-hop direct lookup on the query
relation before (or instead of) graph traversal; construction is
downstream and unreachable whenever a flat hit exists.
(E) PF-A1: 60999 preempts 60902 on probes 0-1 while validity probes
2-3 confirm the taught P and Q facts are retrievable, so the
traversal targets were present but unused. PF-A2: traversal reached
2/2 only where the compose relations (60619/60629) carried no taught
facts, i.e. where no flat hit could preempt. v3 M1 decoy 4/4 PASS
shows direct retrieval of taught structure is intact.
(D) Precedence-reversal world (frozen bar sketch): teach the flat
wrong fact on the compose relation as in PF-A1, then
contradict/remove it, then probe. H1a predicts construction appears
after removal (probe returns 60902). If the probe still misses,
construction is absent entirely and H1a is killed in favor of H1c.
Bar: post-removal probe returns the composed answer; worlds in a
fresh id block (70000+), 3 fresh-state runs, byte-identical
transcripts, degenerate/competent controls as in the PF battery.

H1b. Instance-only write path (locus: the revision/contradiction
operator). GENERAL substrate property.
(H) Contradiction and promotion writes go only to the instance
layer (last-write-wins facts, per-instance patches); no operator
writes to an abstraction or law layer, so there is nothing for a
revision pattern to transfer through.
(E) PF-C1 transcript: the contradiction becomes a direct fact and
the bar is satisfied without any graph change. PF-C2: the +20 shift
is written per key (60621, 60622 observed) but the analogous
relation keeps its law (60711). v3 M3 inspector: six STRUCTURES,
each keyed to one instance with its own evidence; no structure
keyed to a law. v3 M3 systematic 3/3 PASS (patching works
per-instance) with generalization 0/2.
(D) Double-revision law world: contradict two instances of one law
(+20 shift on two keys), then probe an unseen third instance of the
same law and an analogous relation. H1b predicts -2 or the original
law on the unseen instance (no law layer received the write); a
law-write predicts the revised value. Bar: unseen-instance probe
returns the revised value; PASS kills H1b, FAIL confirms the
instance-only write path. Fixing H1b (a law-level write path) would
change PF-C2, v3 M3 generalization, and the double-revision staleness
at once.

H1c. No standing derived structure (locus: persistent learner
state). GENERAL substrate property.
(H) No persistent representation of composed procedures or laws
exists at all; every multi-hop answer is recomputed per query
(BFS) or absent. Transfer, law-level revision, and procedure
composition are impossible as structures, not merely unwired.
(E) v3 M1 K-S5v3(c) struct FAIL: no persistent structure with
both-phase licensed evidence after composition attempts.
m1_inspect_r1.txt shows 2 STRUCTURES with EVIDENCE count=0
(unlicensed, inert). v3 M3 generalization 0/2: unseen subjects
yield -2, exactly what recompute-per-query predicts.
(D) White-box licensed-structure probe: teach a composition, then
run the v3_struct_check lineage inspector keyed on the composed
relation. H1c predicts zero licensed persistent structures; if
licensed structures exist and are unused on query, H1a wins and H1c
is killed. Bar: inspector returns at least one structure with
both-phase licensed evidence whose ablation degrades composition;
PASS kills H1c, FAIL confirms it. A standing derived-structure
layer would be the single substrate change behind construction,
revision transfer, and generalization.

H1d. Oracle-verified traversal, not construction (locus: the
trial/oracle interface). GENERAL across all construction claims.
(H) Apparent composition is BFS reachability checked against the
QUERY-carried expected value; the trial substitutes oracle matching
for construction.
(E) PF-A2 caveat (methods note above): 2/2 valid composition via
BFS 60201->60911->60921 matched to the oracle; no-spurious probes
via 1-hop BFS. The PF prereg intended the oracle value for the
scorer only, but the trial demonstrably uses it for verification.
(D) Blind-probe composition world: identical to PF-A2 but with the
oracle expected value withheld from the learner path (scorer-side
only, enforced in the shim). H1d predicts collapse to 0/2 on the
composition probes; genuine construction predicts unchanged 2/2.
Bar: composition probes correct with no oracle access; PASS kills
H1d, FAIL confirms every composition observation to date is a
verification artifact and invalidates construction evidence across
all worlds, not just PF-A2.

## Cluster 2: GUIDE CONTENT DECOUPLING (the presence bit)

Members: PF-B1 (no selective resolution under concurrent guides:
pre=30, post=30), PF-B2 (no discrimination under guide flood:
30,30,30), v3-M2 (constant CHOICE 30 inquiry; 0/8 routing to the
sealed truthful informant A; no resolution transition pre=30
post=30).

Shared architectural cause (mechanism-level claim about frozen
TNN-2): the ACT operator reads uncertainty guides only as a
presence/absence bit. Guide content (which uncertainty is live, how
many are concurrent, whether one resolved) has no write path into
action selection. The presence bit does reach ACT: PF-B1 baseline
CHOICE 0 after a hit becomes CHOICE 30 with two live guides
(pf_runs/pf_b1_r1.trans: "CHOICE 0" then "CHOICE 30" after the two
misses, then "CHOICE 30" again after one guide resolves). But
everything downstream of presence is constant: the action is
invariant under concurrency (PF-B1 post-resolution), under flood
(PF-B2 30,30,30 for three distinct uncertainties, pf_runs/
pf_b2_r1.trans), and under sequential episodes (v3 M2-W3:
30,30,30). v3 M2-W1: choice 30 maps to role NONE under every sealed
permutation, so no informant is ever consulted (0/8 to A).

### Hypotheses (4, structurally different loci)

H2a. Absent content channel (locus: the guide-to-ACT interface).
GENERAL substrate property.
(H) Guide content never reaches action selection in any form;
ACT receives only guide-live versus guide-absent.
(E) PF-B1: identical action (30) before and after partial
resolution of concurrent guides, with N=0 measured baseline
proving the presence bit is read. PF-B2: three distinct
uncertainties (distinct subjects and relations 60401/60801,
60402/60802, 60403/60803) produce three identical actions. v3
M2-W1: 8/8 inquiry actions constant 30 across sealed per-run
mappings, 0/4 hidden probes correct.
(D) Single-guide content world: two different single
uncertainties, each in its own fresh run, one ACT each. H2a
predicts identical actions (30=30); differing actions kill H2a
and implicate concurrency (H2b). Bar: actions differ across the
two single-guide runs; PASS kills H2a, FAIL confirms the root
cause. A content channel from learner-originated uncertainty to
action would change PF-B1, PF-B2, and all of v3 M2 at once.

H2b. Concurrency collapse (locus: the guide store under
concurrency).
(H) Content is available for a single guide but concurrent guides
collide or overwrite into one slot, destroying discrimination
only under concurrency.
(E) Constrained by v3 M2-W2: even a single guide showed no
resolution transition (pre=30 post=30), which weakens a pure
concurrency story; but single-guide *content* discrimination was
never directly tested, so H2b is not dead.
(D) Sequential two-guide world: create guide 1, ACT, resolve it
fully, then create guide 2, ACT. H2b predicts distinct actions
across the two single-guide phases but constant action within a
flood; H2a predicts constant everywhere. Bar: cross-phase actions
differ; PASS kills H2a and supports H2b, FAIL supports H2a.

H2c. Sticky guide lifecycle (locus: guide store create/update/
retire). GENERAL substrate property.
(H) Guides are append-only: no update or retire operator exists,
so post-resolution guide state equals pre-resolution state by
construction and ACT cannot change.
(E) PF-B1: after OBSERVED 60302 60701 60312 resolves one of two
guides, the post-resolution ACT is unchanged (30). v3 M2-W2:
post=30 stale after resolution. Same sticky-state family as v3
M3's silent no-op on second contradiction.
(D) Guide-store inspector world (analog of v3_inspect_state):
dump guide-store entries before and after a resolution OBSERVE.
H2c predicts the resolved guide entry persists unchanged; if the
entry is removed or updated yet ACT stays 30, the fault is
downstream (H2a) and H2c is killed. Bar: inspector shows the
resolved guide retired; PASS kills H2c, FAIL confirms it. A
learner-state lifecycle (create/update/retire) is the general
substrate change; it also bears on revision staleness.

H2d. Output vocabulary bottleneck (locus: the ACT operator).
(H) ACT can emit only the null action and one guide action; the
operator lacks the output bandwidth to express content, count,
or resolution state even if it received them.
(E) Observed CHOICE vocabulary across all guide worlds is {0, 30}
(PF-B1: 0,30,30; PF-B2: 30,30,30; v3 M2-W1: 12 calibration 0,
8 inquiry 30).
(D) Orthogonal-signal probe: hold guide presence constant and
vary a signal ACT is known to read (e.g. post-hit versus
post-miss-with-no-guide ACT). If ACT varies there but not across
guide content, the bottleneck is guide-specific (H2a), not a
general output limit, killing H2d. If ACT never emits beyond
{0,30} in any frozen-TNN-2 context, H2d stands.
Bar: ACT emits a third distinct action in any context; PASS kills
H2d.

## Cross-cluster note (hypothesis, not a verdict)

Both clusters are consistent with one deeper root hypothesis:
no learner-originated derived representation (composed graph,
guide content, revision pattern) has a privileged channel into
the behavior-driving operators (answer selection, action
selection); only flat primitive signals (direct facts by
first-hit lookup, per-key patches, guide-presence bit) drive
behavior. The two clusters are kept separate because their loci
(the fact-store read/write path versus the guide-to-action
interface) and their discriminating experiments differ; the
deeper root is itself falsifiable by E1/E2 below and is not
assumed.

## Failures that cannot be clustered

None of the observed failure signatures require an independent
architectural cause beyond the two clusters above. Every
signature (PF-A1, PF-B1, PF-B2, PF-C1, PF-C2, v3 M1, v3 M2, v3
M3) is covered. The only unclustered item is the PF-A2 caveat,
which is a measurement/world-design limitation (methods note),
not an architecture failure; its behavioral signature is
consistent with Cluster 1 but it carries no verdict weight by
instruction. Stated plainly: the battery's failures reduce to
two shared causes, not eight independent ones.

## Prioritized discriminating experiments (by information gain)

All experiments run on the frozen binary (no source edits), pure
Zag, prereg-first per governance, 3 fresh-state runs,
byte-identical transcripts, degenerate/competent controls.

E1. Licensed-structure inspector for composition and law (tests
H1c). Cheapest and deepest: reuses the v3_struct_check /
v3_inspect_state lineage. Discriminates "derived structure absent"
from "present but subordinated" across all of Cluster 1. Kills or
confirms the substrate claim behind PF-A1, PF-C1, PF-C2, v3 M1,
v3 M3 in one run. Run first.

E2. Single-guide content discrimination (tests H2a vs H2b). Two
different single uncertainties in separate fresh runs, one ACT
each. If actions differ, the constant-guide story collapses to a
concurrency phenomenon and reframes PF-B1/PF-B2; if identical,
Cluster 2's root cause is confirmed. Run second.

E3. Blind composition probe with oracle withheld (tests H1d).
Decides whether any construction evidence is real or an
oracle-verification artifact. A FAIL (collapse to 0/2) reframes
PF-A2 and constrains every future construction claim across all
worlds, not just PF-A2. Run third.

E4. Precedence-reversal world (tests H1a): teach the flat wrong
fact, then contradict/remove it, then probe for the composed
answer.

E5. Double-revision law world (tests H1b): contradict two
instances of one law, probe an unseen third instance and an
analogous relation.

E6. Guide-store inspector before/after resolution (tests H2c).

E7. Sequential two-guide world (tests H2b).

E8. Orthogonal-signal ACT bandwidth probe (tests H2d).

Ordering rationale: E1-E3 each can kill a whole cluster's shared
cause (or reframe multiple failures at once) with minimal new
machinery, and each is frozen-binary compatible. E4-E8
discriminate within a confirmed cluster.

## No-patch-treadmill compliance

No repair is proposed for any single world. The discriminating
experiments above test substrate properties (standing derived
layers, content channels, lifecycle operators, trial interfaces);
a confirmed hypothesis would motivate one general substrate
change fixing multiple worlds at once, per the owner 2026-10-01
ruling, and only after root-cause confirmation. Criterion 0 is
not met by anything here; no L3 language is used.
