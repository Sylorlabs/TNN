# PREREG_E3.md -- Discriminating experiment E3: blind composition probe with oracle withheld (tests H1d)

Wave: wave-20261001-2321pdt, lane BATTERY-E3.
Status: FROZEN DESIGN. This file is committed alone before any E3
world file, oracle file, or tool source is created. Kill bars never
move after freezing.

## 0. Freeze record and provenance

E3 is the third-prioritized discriminating experiment from
BATTERY-CLUSTER/CLUSTER_ANALYSIS.md. It tests hypothesis H1d for
Cluster 1 (DERIVATION SUBORDINATION):

"Oracle-verified traversal, not construction (locus: the
trial/oracle interface). Apparent composition is BFS reachability
checked against the QUERY-carried expected value; the trial
substitutes oracle matching for construction."

Evidence motivating H1d: the PF-A2 caveat (methods note in
CLUSTER_ANALYSIS.md). The 2/2 valid-composition probes were answered
via BFS traversal (60201->60911->60921) verified against the oracle
expected value carried on the QUERY line; the no-spurious probes
were answered via 1-hop BFS (60201->60931) matched to the oracle.
The PF prereg intended the oracle value for the scorer only, but
the frozen shim driver passes it as `expected` into
ev_query/mp_run/t2_trial, where t2_try_verify accepts a candidate
graph only when its executed output equals the expected value
(unmasked mode). The oracle is therefore load-bearing inside the
learner path in every PF composition observation to date. M1 0/8
composition (EVIDENCE count=0) and the PF-C2 transfer failures are
consistent with composition depending on oracle-supplied structure.

E3 removes the oracle and asks whether composition survives. This
is the load-bearing question for every construction claim in the
wave.

Frozen binary (no source edits permitted; the blind driver is a
transport shim with byte-identical cognition, see section 4):

- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  (path: docs/lab/research-lead/overnight-20260928/
  core_freeze_tnn2_shim/freeze_shim2_bin)
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Pure Zag for all research logic. Shell only: invoke znc, run
binaries, git ops, move/copy files, sha256sum manifests. No
em-dashes in any doc; check with check_no_dash.sh before commit.
Commits local only under
docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/; never push;
never git reset --hard; never rebase. Prereg committed alone first;
implementation in later commits (commit-order self-check).

## 1. World specification (exact streams)

ID block 80000-89999, disjoint from PF (60000-69999), v3
(50000-59999), and FW1-FW9. Fresh sealed worlds: generated after
this prereg freezes; SHA-256 hashes committed in MANIFEST_E3 before
any run. Two world families, each with exactly 2 target composites
(the 0/2 collapse signature is per family).

Exposure teaches only OBSERVE facts. Components are experienced
separately. The target composites are never named in exposure: no
OBSERVE ever carries the query relation, no type-15 LINK edges, no
compose_try demonstrations, no MAP relation sequences, no supplied
structure pointing at any answer. The query relation is novel in
every probe.

### 1.1 Family E3A: valid-first calibration family

Analog of PF-A2 in a fresh id block. The valid composition is the
first executable chain in the trial's deterministic search order.

```
OBSERVE 80201 80611 80911
OBSERVE 80202 80611 80912
OBSERVE 80911 80612 80921
OBSERVE 80912 80612 80922
OBSERVE 80201 80613 80931
OBSERVE 80202 80613 80932
QUERY 80201 80619
QUERY 80202 80619
QUERY 80201 80629
QUERY 80202 80629
```

Probes 0-1 are the bar probes (target composites 80921, 80922;
sealed scorer-side). Probes 2-3 are secondary observations: the
distractor relation 80629 is novel and D was never part of a valid
composition, so the sealed target is -2 (miss). They are not part
of the frozen bar; their blind behavior is recorded as evidence
about relation-agnostic enumeration.

Teach order is load-bearing: P facts (nodes 2-3), Q facts (nodes
4-5), then distractor D facts (nodes 6-7). BFS from 80201 yields
paths in node-id order, so the first length-3 path is the valid
chain (80201,80911,80921).

### 1.2 Family E3B: spurious-first adversarial family

The discriminating family. Two executable 2-hop chains leave each
query subject; the SPURIOUS chain is taught first so it precedes
the valid chain in the trial's deterministic BFS candidate order.
Nothing in the exposure marks either chain as the target; the
sealed oracle alone designates the valid composite.

```
OBSERVE 80301 80631 80961
OBSERVE 80961 80632 80971
OBSERVE 80302 80631 80962
OBSERVE 80962 80632 80972
OBSERVE 80301 80611 80911
OBSERVE 80911 80612 80921
OBSERVE 80302 80611 80912
OBSERVE 80912 80612 80922
QUERY 80301 80619
QUERY 80302 80619
```

Sealed targets: probe 0 -> 80921, probe 1 -> 80922.

Trial-order analysis (from frozen source, pre-registered): fact
node ids follow teach order (n2..n9 as listed). BFS from 80301:
p0=(80301); head expansion finds n2 -> p1=(80301,80961),
n6 -> p2=(80301,80911); then p1 expands via n3 ->
p3=(80301,80961,80971); p2 expands via n7 ->
p4=(80301,80911,80921). The k=2 chain phase tries length-3 paths
in order: p3 (spurious) before p4 (valid).

### 1.3 Oracle files (sealed, scorer-side only)

e3a.oracle (probe order): 80921, 80922, -2, -2.
e3b.oracle (probe order): 80921, 80922.
These files are never passed to any learner-path binary. The blind
world files carry QUERY lines with exactly 2 integer fields
(subject, relation); a third field is a transport-level parse
error in the blind driver.

### 1.4 Oracle-present control worlds

e3a_oracle.txt and e3b_oracle.txt: identical streams to the blind
worlds except each QUERY carries its oracle expected value as the
third field (E3A probes 2-3 carry -2). These run under the frozen
freeze_shim2_bin (flags=0, unmasked), replicating the PF oracle
condition. They are validity/calibration controls, not part of the
frozen bar.

## 2. Oracle withholding: the blind driver (enforced in the shim)

A new transport driver, e3_blind_driver.zag, is built as:
byte-identical cognition region of freeze_shim2.zag (everything
before the CORE-FREEZE-TNN2 DRIVER SHIM marker; verified by diff
and SHA-256 in the K-C0A audit) plus a new driver section. The new
driver section is transport only: it parses integers and
dispatches to the unchanged public interface. Its QUERY branch:

- requires exactly 2 integer fields after QUERY (a third field is
  a parse error; the run fails closed),
- calls ev_query(W, subj, rel, -2, 1): expected=-2 (no oracle),
  flags=1 (masked=1),
- emits ANSWER subj rel v (the learner's answer; no oracle).

Masked mode is TNN-2's own no-oracle trial path (used by the frozen
t_f2 masked test): t2_try_verify accepts the first candidate graph
that executes successfully (v not -2/-999999) without comparing
against any expected value. The cognition is untouched; only the
transport stops delivering the oracle to the learner. This is what
"withheld from the learner path (scorer-side only, enforced in the
shim)" means operationally.

The K-C0A audit (section 7) verifies zero new semantic cases,
modes, bridges, or handlers, and that the probe does not smuggle
the answer.

## 3. What counts as a blind composition (frozen)

A bar probe counts as a blind COMPOSITION iff all three hold:

(i) Value match: the transcript ANSWER equals the sealed target
    for that probe (scorer-side oracle comparison).
(ii) Constructed and used: the post-run state.bin contains a
    type-20 MAP node with field8 == probe subject and
    field4 == query relation and field28 == the ANSWER value,
    whose graph root walks (SEQ edges plus BRANCHEQ true-targets)
    to a GUARD/SETREG cell sequence carrying ET_DEP edges to
    type-1 fact nodes whose (s,r,o) triples are exactly taught
    component facts from the exposure stream. The e3 inspector
    reports this white-box evidence.
(iii) No retrieval shortcut: no OBSERVE in the world taught
    (subject, query-relation, *), so a direct-fact hit on the
    query relation is impossible by construction (also audited).

If (i) holds without (ii), the probe is reported as
RETRIEVAL-OR-OTHER, not as a composition. If (i) fails, the probe
fails regardless of (ii).

## 4. Conditions and runs

- BLIND (the bar): e3_blind_driver_bin on e3a_blind.txt /
  e3b_blind.txt, 3 fresh-state runs per family (state.bin removed
  before each run). Transcripts must be byte-identical across the
  3 runs (determinism gate, PF-K2 analog); any mismatch is
  RUN-INVALID and investigated, not scored.
- ORACLE-PRESENT (validity/calibration control): frozen
  freeze_shim2_bin (hash verified before running) on
  e3a_oracle.txt / e3b_oracle.txt, 3 fresh-state runs per family,
  byte-identical transcripts required.
- Validity gates (must pass or the family run is WORLD-INVALID):
  E3B oracle-present = 2/2 on both bar probes in all 3 runs
  (proves the sealed target is reachable and oracle-selectable);
  E3A oracle-present = 2/2 on bar probes in all 3 runs.
- E3A blind is calibration: 2/2 on bar probes is expected (blind
  assembly intact). If E3A blind = 0/2, record CALIBRATION-FAIL and
  investigate before finalizing; the E3B verdict still follows
  from its own gates, with the anomaly reported.

## 5. Frozen decision rule and predicted signatures

Pre-registered predicted outputs (from frozen-source analysis;
the experiment tests these predictions):

- E3A blind bar probes: [80921, 80922] -> 2/2. E3A blind
  distractor probes (observation only): [80921, 80922], i.e.
  spurious composition on the novel relation (target -2).
- E3A oracle-present: [80921, 80922, -2, -2].
- E3B blind bar probes: [80971, 80972] -> 0/2. Both answers are
  predicted to be constructed spurious composites (criterion
  (ii)+(iii) satisfied for the spurious chain), not -2.
- E3B oracle-present: [80921, 80922] -> 2/2 (spurious candidate
  rejected by oracle verification, valid candidate accepted).

SIGNATURE-ORACLE-DEPENDENT: E3B blind = 0/2 with outputs exactly
[80971, 80972], E3B oracle-present = 2/2, E3A blind bar probes =
2/2, all transcripts byte-identical across 3 runs per condition,
construction criterion (ii)+(iii) confirmed for the blind outputs
via the inspector. Verdict: E3-ORACLE-DEPENDENT. Supports H1d in
refined form: the trial assembles executable graphs blind (the
construction machinery works without the oracle), but candidate
SELECTION among multiple executable chains is performed by oracle
verification; without the oracle the trial emits the
first-executable chain. This reframes every PF construction
observation: they are BFS enumeration plus oracle selection, not
selective construction. Every construction claim in the wave must
be re-examined under blind conditions.

SIGNATURE-COMPOSITION-HOLDS: E3B blind = 2/2 ([80921, 80922]) with
criterion (i)+(ii)+(iii) met on both probes, byte-identical
transcripts. Verdict: E3-COMPOSITION-HOLDS. Kills H1d: the learner
selected the valid composition with no oracle access, so a
selection mechanism beyond oracle verification exists.

Any other pattern (1/2 splits, -2 outputs where construction was
predicted, non-identical transcripts, or calibration failure):
verdict E3-INCONCLUSIVE; report the exact observed pattern; H1d
is neither confirmed nor killed.

## 6. What E3 does and does not establish

Establishes (within the frozen bar): whether the frozen TNN-2
trial's composition outputs depend on oracle verification for
candidate selection, measured on fresh sealed worlds with
byte-identical determinism and white-box construction evidence.

Does not establish: broad generality, L3, or progress toward L3.
Criterion 0 is not met by anything here; no L3 language is used.
A HOLD verdict kills H1d only; it does not validate construction
as a general mechanism (that would require the E1/E2 program and
fresh adversarial batteries). An ORACLE-DEPENDENT verdict
constrains all construction evidence to date but proposes no
repair (no-patch-treadmill rule).

## 7. K-C0A audit (pre-registered checks, run before scoring)

K1. Cognition identity: the cognition region of
    e3_blind_driver.zag (bytes before the driver marker) is
    byte-identical to the same region of freeze_shim2.zag
    (diff empty; SHA-256 recorded).
K2. Transport-only driver: diff of the driver sections shows the
    only behavioral changes are (a) QUERY requires exactly 2
    fields, (b) ev_query called with (-2, 1). No new semantic
    cases, no modes, no bridges, no handlers, no task identities.
K3. No smuggled answer: blind world files contain only OBSERVE and
    QUERY lines; QUERY lines have exactly 2 integer fields; the
    query relations (80619, 80629) never appear in any OBSERVE
    line; no LINK/COMPOSE/MAP tokens exist in any world file.
K4. Oracle separation: the blind driver source and run commands
    never reference the oracle files; oracle values reach the
    learner only as taught fact objects (disclosed, unavoidable:
    components must be experienced).
K5. Frozen binary integrity: freeze_shim2_bin SHA-256 verified
    before the oracle-present control runs.

## 8. No-leak and determinism audits

N1. Byte-identical transcripts across the 3 fresh-state runs per
    condition (sha256sum comparison).
N2. Blind transcripts contain no oracle values except as taught
    fact objects echoed in OBSERVED lines (the ANSWER lines carry
    only learner outputs).
N3. World and oracle file hashes in MANIFEST_E3 match the
    pre-run committed values at scoring time.
