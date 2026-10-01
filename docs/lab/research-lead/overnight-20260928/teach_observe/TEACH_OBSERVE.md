# Teach-Observe Conflation Analysis

**Verdict: TEACH-OBSERVE-COMPLETE.**
**Scope:** Analysis only. Frozen source read-only. No implementation.
**Frozen source:** `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
(SHA-256 `a29972ca...`, verified).

## 1. The conflation, stated plainly

Five distinct knowledge sources are stored as indistinguishable tag-1 FACT
nodes. The learner's state contains no representation of where any FACT came
from. The only record of source is the event log's kind field, and the event
log is write-only theater (T4, zero readers, confirmed by grep).

The five sources, all producing tag-1 nodes with identical field layout
(fields 20/24/28/32 = s/r/o/tick):

| # | Source | Call path | Event log |
|---|--------|-----------|-----------|
| 1 | Harness teaching | `ev_teach` (line 297) | kind 1 |
| 2 | Environmental observation | `ev_observe` -> `ev_teach_in` (lines 852, 856) | kind 4 |
| 3 | Bootstrap inference (learner's own guess) | `bootstrap_miss` -> `ev_teach_in` (line 783) | none |
| 4 | Revision output (learner's own repair) | `t2_revise_graph` -> `ev_teach_in` (line 748) | none |
| 5 | MAP promotion shadow | `promote_graph` -> `ev_teach_in` (line 541) | none |

Sources 3, 4, and 5 do not even write to the event log. In learner state,
there is no difference between "the harness told me," "I saw it," "I guessed
it," "I repaired it," and "a MAP cached it."

## 2. How the two handlers differ (and where the difference dies)

**`ev_teach`** (line 297) does: tick increment, decay, context push, node
allocation, tag=1, `write_node(s,r,o,tick)`, edge type 9 self (protection
clock), a scan for the most recent other tag-1 node linked via edge type 5,
and `log_ev` kind 1.

**`ev_observe`** (line 836) does: tick increment, decay, context push, then
`activate(W,s,r)`:
- Match (`ng(W,n,28)==o`): edge type 7 (CFM) self, `ref_prot`, `log_ev` kind 4
  flag 1, return 1. No new node.
- Mismatch: edge type 3 (CON) self on the old node, `revise_on_contradict`,
  a tag-3 history node copying the old values with edge type 5 to the old
  node, then `ev_teach_in(W,s,r,o)` creating a new tag-1 FACT, edge type 4
  (DEP) from new to old, `log_ev` kind 4 flag 0, return 0.
- No existing FACT: `ev_teach_in(W,s,r,o)`, `log_ev` kind 4 flag 1, return 1.

**`ev_teach_in`** (line 310) does: node allocation, tag=1,
`write_node(s,r,o,tick)`, edge type 9 self. No decay, no context push, no
prev-scan, no event log.

The handlers differ in control flow (observation checks for contradictions;
teaching does not), in edge types written (CFM/CON/DEP vs SUP), and in the
event log kind (1 vs 4). But the resulting FACT node, the unit that every
downstream consumer reads, carries none of this. A tag-1 node has no source
field. The edge-type differences are per-node decorations that no consumer
queries by source: `activate` ranks by bid, `bootstrap_miss` scans by tag and
relation, and neither filters by provenance.

The distinction therefore lives and dies in exactly one place: the `log_ev`
kind field. `log_ev` (line 285) writes to a 128-entry ring at header offset
28. Grep for readers (`evlog`, `ev_log`, `read_ev`, `get_ev`) returns zero
hits. The event log is write-only. The teach/observe distinction is recorded
in a place nothing reads.

## 3. Consequences

### 3a. Bootstrap counts the learner's own guesses as independent evidence

`bootstrap_miss` (line 763) scans the 6 most recent live tag-1 nodes with
matching relation, collecting field 28 values, and requires unanimity at
threshold k=3. It does not check provenance. It does not check
`is_superseded`.

Two distinct corruptions follow.

First, self-reinforcement. When bootstrap finds unanimity it calls
`ev_teach_in(W,s,r,v0)` (line 783), teaching its own inferred value as a
tag-1 FACT. On a later miss for the same relation, the scan encounters this
self-generated FACT and counts it as an "observation." The k=3 threshold can
be satisfied partly or entirely by the learner's own prior guesses. The
P-INV rule is supposed to require independent environmental evidence; the
implementation lets the learner vote for itself. Each bootstrap success
plants a vote for the next bootstrap, a circular confidence loop with no
external anchor.

Second, the scan does not exclude superseded FACTs. When `ev_observe` finds a
contradiction it marks the old FACT with a CON self-edge (type 3), which
makes `is_superseded` return true. `activate` (line 143) checks
`is_superseded` and skips such nodes. `ev_act` (lines 868, 880) also checks.
But `bootstrap_miss` does not. A contradicted, superseded FACT, a value the
system has explicitly rejected, still counts toward bootstrap unanimity. The
rejection is visible to retrieval and action but invisible to the inference
rule that most needs it.

### 3b. The oracle/observation distinction has no representation

The verification criterion analysis (`c2a48bee6`) defines V4 `ev_observe` as a
"genuine prediction-error signal (stored vs observation)" and formalizes an
oracle vs observation distinction: oracle is harness-supplied `expected`,
observation is environmental signal.

But in learner state, the distinction collapses twice.

First, observations are stored as tag-1 FACTs identical to taught facts.
When a later `ev_observe` computes "prediction error," it compares the new
signal against `activate(W,s,r)`, the max-bid FACT, which may be a taught
fact, a bootstrap guess, a revision product, or a MAP shadow. The error is
computed against an undifferentiated store, not against "what I previously
observed." The analysis vocabulary (stored vs observation) describes a
distinction the system cannot make.

Second, the contradiction path cannot distinguish conflict types. When
`ev_observe` finds a mismatch, the old FACT might be: a harness teaching
(observation overrides instruction), a previous observation
(observation-vs-observation conflict, requiring a tie-break policy that does
not exist), a bootstrap guess (observation should win trivially), or a MAP
shadow (observation contradicts a cached procedure answer). All four are
handled identically: CON edge, `revise_on_contradict`, teach the new value.
The system has no policy for "my sensors disagree with each other" versus
"my sensors disagree with my teacher" because it cannot tell which case it
is in.

### 3c. Revision is source-blind

`revise_on_contradict` (line 685) receives the contradicted FACT node and
searches for MAPs with provenance edges to it, calling `t2_revise_graph`.
It never inspects the FACT's source. If the contradicted FACT was itself a
recent observation (taught via `ev_teach_in` from a previous `ev_observe`),
the "contradiction" is observation-vs-observation, but revision proceeds as
if a stable belief were overturned by new evidence.

Worse, `t2_revise_graph` on success calls `ev_teach_in(W,s,r,out)` (line 748),
teaching the repaired value as another tag-1 FACT. The repaired value, the
product of the learner's own surgical procedure, is now indistinguishable
from a harness teaching. A subsequent observation contradicting it will be
treated as overturning authoritative instruction rather than as evidence
against the learner's own repair. The provenance chain (taught -> observed ->
revised -> observed) is flattened to a sequence of identical FACTs.

### 3d. The shadow FACT poisons the well it was meant to fill

`promote_graph` inserts a shadow FACT via `ev_teach_in` (line 541) so that
`activate` finds the MAP's answer. But this shadow is now a tag-1 FACT like
any other, which means:
- `bootstrap_miss` can count it as an "observation" toward unanimity.
- A later `ev_observe` with a different value will "contradict" it and
  trigger `revise_on_contradict`, attempting to revise the MAP based on a
  conflict between the environment and the MAP's own cached answer, without
  knowing the FACT is the MAP's shadow.
- The execute-vs-cache analysis (`7186294cd`) found MAPs are closed replays;
  the shadow FACT is the cache. The cache entry is now eligible to serve as
  evidence for bootstrap inference, meaning the learner can bootstrap its
  own cached procedure outputs into "unanimous observations."

## 4. What separation would require

A principled teach/observe distinction needs three elements, all missing:

1. **Provenance storage.** Each FACT records its source: taught, observed,
   inferred, revised, promoted. This is a new field or tag discipline on
   the node itself, not the event log, because consumers read nodes.

2. **Production read paths.** Every consumer that currently scans tag-1
   nodes must have a source policy:
   - `bootstrap_miss`: which sources count as evidence? (Presumably
     observations only, excluding self-generated inferences and shadows.)
   - `activate`: does source affect ranking? (Should an observation
     outrank a stale teaching?)
   - `revise_on_contradict`: does the conflict type change the response?
     (Observation-vs-observation needs a tie-break; observation-vs-teaching
     needs an override policy.)
   - `ev_observe` match path: does confirming a bootstrap guess with an
     observation mean something different from confirming a teaching?

3. **Source-sensitive lifecycle.** Supersession currently excludes nodes
   from `activate` but not from `bootstrap_miss`. A separated system needs
   a coherent rule for which sources survive contradiction and which are
   demoted, per consumer.

## 5. What breaks: the conflation is load-bearing

The honest difficulty is that the conflation is not a bug sitting beside a
working system; it is structural to how the system functions at all.

- `activate` works because it does not need to know source. Adding source
  weighting requires a policy for source priority, which is a cognitive
  decision the researcher would be making, not the learner.
- `bootstrap_miss` reaches k=3 as often as it does partly because it counts
  self-generated and shadow FACTs. Restricting to genuine observations would
  make the threshold harder to reach, changing measured behavior on every
  existing battery. The current bootstrap hit rate is partly a measure of
  the conflation.
- The shadow FACT mechanism depends on `activate` finding the shadow. If
  shadows are marked as a distinct source, `activate` needs an explicit
  policy for them, which reopens the execute-vs-cache decision
  (`7186294cd`) that the current code resolves by accident.
- `ev_observe`'s contradiction path teaches the new value via `ev_teach_in`
  unconditionally. If observations must remain distinguishable from
  teachings, the "teach the observed value" step needs its own node
  discipline, and every downstream scan must handle it.

Separation is therefore not a local fix. It requires defining, for each of
five sources and each of four consumers, what the source means and how the
consumer should treat it. Those twenty policy cells are currently filled by
the single default "treat everything as a FACT." Any separation replaces
one researcher-invisible default with twenty researcher-visible choices,
each a potential treadmill surface. This is why the analysis stops at
characterization: the separation is a TNN-3 design problem, not a TNN-2
patch.

## 6. Relation to adjacent findings

- **Minus-two (`ede1060a5`).** The BOOTSTRAP_FEW dominance (62% of terminal
  -2s) is partly a measure of this conflation: the bootstrap's evidence
  pool is polluted by self-generated FACTs, so "insufficient observations"
  sometimes means "insufficient genuine observations after discounting my
  own guesses," a quantity the system cannot compute.
- **Verification criterion (`c2a48bee6`).** V3 (bootstrap) is described as
  "closest to learner-internal in TNN-2, but researcher-fixed rule." The
  conflation means V3's evidence base includes the learner's own prior
  outputs, so even the "learner-internal" check is partially self-referential.
- **Theater audit (`e0423538a`).** T4 (event log write-only) is the specific
  mechanism by which the source distinction is recorded nowhere readable.
  Fixing T4 alone (adding readers) would not fix the conflation, because
  the consumers scan nodes, not the log.
- **Execute-vs-cache (`7186294cd`).** The shadow FACT is source 5. The
  "accidental" always-cache policy depends on the shadow being found by
  `activate`, which depends on the shadow being an unmarked tag-1 FACT.

## 7. Summary for the coordinator

The teach/observe distinction exists in exactly one place: the `log_ev`
kind field (1 vs 4). Nothing reads the event log. In learner state, five
knowledge sources (taught, observed, bootstrap-inferred, revision-produced,
MAP-shadow) are stored as indistinguishable tag-1 FACTs. Consequences, all
verified read-only against frozen source `a29972ca`:

1. Bootstrap counts the learner's own prior guesses as independent evidence
   (self-reinforcing confidence loop, line 783 feeding lines 763-771).
2. Superseded (contradicted, rejected) FACTs still vote in bootstrap
   unanimity (`bootstrap_miss` does not check `is_superseded`; `activate`
   does).
3. The oracle/observation distinction from the verification analysis has no
   representation in learner state; prediction error is computed against an
   undifferentiated store.
4. Revision cannot distinguish observation-vs-teaching from
   observation-vs-observation; all contradictions get identical treatment.
5. The MAP shadow FACT (the cache) is eligible bootstrap evidence, letting
   cached procedure outputs masquerade as unanimous observations.

Separation requires provenance storage plus source policies for every
consumer, roughly twenty policy cells currently filled by the single
default "treat everything as a FACT." The conflation is load-bearing:
`activate`, `bootstrap_miss`, and the shadow mechanism all function because
they do not distinguish sources. This is a TNN-3 design problem, not a
TNN-2 patch. No implementation is proposed or built.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (analysis only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0
- MODES: 0
- BRIDGES: 0
- HANDLERS: 0
- SEMANTIC CASES: 0

**Verdict: TEACH-OBSERVE-COMPLETE.**
