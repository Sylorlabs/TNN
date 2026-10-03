# PREREG_E4.md -- Discriminating experiment E4: precedence-reversal world for H1a

Wave: wave-20261001-2321pdt, lane BATTERY-E4.
Status: FROZEN DESIGN. This file is committed alone (with NAMECHECK.md
only) before any E4 world file, spec file, or tool source is created.
Kill bars never move after freezing.

## 0. Freeze record and provenance

E4 is the within-cluster discriminator for Cluster 1 (DERIVATION
SUBORDINATION) from BATTERY-CLUSTER/CLUSTER_ANALYSIS.md. It tests
hypothesis H1a (read-path precedence inversion) AFTER the E1 verdict.

E1 (BATTERY-E1/E1_RUN.md, verdict E1-FIRSTCLASS) killed H1c as stated
("no persistent representation of composed procedures or laws exists
at all"): licensed derived structures persist in frozen TNN-2 state
(W2 id=13, W4 id=15/id=26, each with multi-hop licensed evidence and
derived answers never directly taught). Cluster 1's shared cause is
therefore refined to: "derived structures exist but have no privileged
standing in the read path; the flat instance-fact layer is consulted
first and wins." H1a wins for W1/W2 under this refinement.

E4 discriminates between two remaining accounts of that subordination:
- H1a as PURE PRECEDENCE: the derived structure is a fully intact,
  licensed answer source; the only reason it does not drive the
  answer is read-path ordering (the flat fact layer is consulted
  before construction/traversal, so a flat hit preempts it).
- DEEPER SUPPRESSION: the flat-fact and contradiction machinery
  degrades, blocks, or demotes the derived layer itself, beyond mere
  ordering. A SUPPRESSION finding redirects to a deeper suppression
  mechanism and reframes the refined H1a.

Frozen binary (no source edits permitted; the inspector is an
external probe):
- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  (path: docs/lab/research-lead/overnight-20260928/tnn2_build/
  tnn2.zag; re-verified by this worker before freezing)
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  (path: docs/lab/research-lead/overnight-20260928/
  core_freeze_tnn2_shim/freeze_shim2_bin; re-verified)
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (path: src/tools/toolchain/znc_linux_x86_64_abed8aa1; re-verified)

World id block: 72000-72999. Fresh and disjoint from v3
(50000-59999), the PF battery (60000-69999), and E1 (71000-71999).
Material differences from E1-W2/PF-C1 are stated per world in
section 4. No world is a trivial FW1-FW9 variant.

## 1. Global constraints

PURE ZAG ONLY for all research logic. Shell only: invoke znc, run
binaries, git ops, move/copy files, sha256sum manifests. Each world
runs 3 times from fresh state via `freeze_shim2_bin <world>
<state.bin>`; transcripts and state.bin saved per run. No em-dashes
in any doc; check with check_no_dash.sh before commit. Commits
local only under
docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E4/; never push;
never git reset --hard; never rebase. This prereg is committed
alone first (with NAMECHECK.md only); world generation, tool
building, and runs follow in separate commits (commit-order
self-check). The BATTERY, BATTERY-CLUSTER, and BATTERY-E1 lane
directories are read-only for this lane; their committed sources
were extracted with git show from the recorded commits (E1 prereg
793abbf65, worlds aa38427b8, inspector/tools 4afcd9f3b, runs
f5b1bab41).

## 2. Design constraints derived from E1 and the frozen source

These are preregistered facts about the instrument, not choices:

(a) Structure-first ordering is mandatory. E1-W1 proved that a flat
fact taught on the probe key BEFORE any probe blocks construction
entirely (inspector: STRUCTURES 0). Mechanism, read from the
committed shim source: ev_query calls activate (flat fact lookup)
before mp_run/t2_trial (construction); a flat hit returns without
ever running the trial, so promote_graph is never called. The task
premise ("the flat layer's wrong fact is the only thing suppressing
the derived structure") therefore requires the derived structure to
be constructed BEFORE the flat wrong fact is taught. E4-W1 teaches
the chain, probes (structure forms), then teaches the flat wrong
fact, then contradicts it, then probes.

(b) "Remove" is operationalized as supersession per the frozen
contradiction protocol. The world protocol (OBSERVE/QUERY/ACT) has
no deletion operator. Per ev_observe in the committed shim source,
a contradicting OBSERVE (s,r,o_new) with an existing fact node
(s,r,o_old): writes a type-3 CON self-edge on the old node
(is_superseded becomes true, so activate skips it), calls
revise_on_contradict (which revises only tag-20 graphs holding a
type-1 edge to the contradicted fact node), and teaches a new flat
fact (s,r,o_new). The wrong fact is thereby removed from the read
path. This is the E1-W2 precedent (contradiction 71213 honored by
direct-fact shadowing while derived structure id=13 persisted
untouched). In E4-W1 the contradicted node is the flat wrong fact,
whose teaching postdates the derived graph, so the derived graph
holds no edge to it and revise_on_contradict is a no-op on it.

(c) The contradiction is LICENSED because its value is the derived
answer D itself, not an arbitrary value. After supersession the
flat layer holds (S,RC,D): the value the licensed derivation
produces. The decision probe therefore tests whether the read path,
freed of the wrong fact, settles on the derived value, while the
inspector tests whether the licensed derived structure survived the
flat-fact teaching and the contradiction.

(d) Oracle-caveat scoping (the PF-A2/H1d instrument property). The
promotion probes (W0 ANSWER[0]/[1], W1 ANSWER[0]/[1]) run the trial,
which verifies against the QUERY-carried expected value; their
behavioral leg cannot distinguish structure-driven answers from
oracle-verified traversal (E3's question). The PREFLAT and POST
probes (W1 ANSWER[2]/[3]) are pure activate-path flat hits, which
ignore the expected value; they carry no oracle caveat. The
STRUCTURAL leg (DERIVED via the oracle-blind inspector) is
unconfounded in all worlds and is the actual discriminator between
PRECEDENCE and SUPPRESSION.

## 3. Inspector design (frozen)

The inspector is e1_inspect_state.zag reused byte-identical
(lineage: v3_inspect_state; the E1 K-C0A audit passed on it). It
reads only state.bin and the world's OBSERVE stream; QUERY lines
are never read. It contains zero world-id literals. For E4 it is
copied to e4_inspect_state.zag with no semantic change; the K-C0A
re-audit (section 8) verifies byte-identity and zero 72xxx
literals.

### 3.1 E4-DERIVED bars (frozen)

E4-DERIVED(w)=1 iff there exists a STRUCTURE in the inspector
report satisfying the per-world bar. Evidence licensing is the E1
machinery (OBSERVE triples whose object is reachable as a literal
in the structure's graph walk, any subject).

E4-W0 (control): STRUCTURE with subj=72101, rel=72119,
answer=72195, whose evidence contains (72101,72111,72191) [hop-A
role] AND (72191,72112,72195) [hop-B role], and contains no triple
(72101,72119,72195) [the derived answer is never taught on the
probe key in the control].

E4-W1 (precedence-reversal): STRUCTURE with subj=72201, rel=72219,
answer=72295, whose evidence contains (72201,72211,72291) [hop-A
role] AND (72291,72212,72295) [hop-B role]. The "never taught on
the derived key" condition is INTENTIONALLY DROPPED for W1: the
licensed contradiction teaches D on RC by design (section 2c), so
the triple (72201,72219,72295) is expected in evidence (its object
72295 is the structure's answer literal). Licensing rests on the
both-hop chain evidence, which a flat promotion of the
contradiction triple alone cannot supply (a flat fact node is
tag-1 and never emits a STRUCTURE line).

### 3.2 Behavioral bars (frozen)

Transcript ANSWER lines are indexed in order (ANSWER[0] first).

E4-W0: FIRSTCLASS=1 iff E4-DERIVED(W0)=1 and ANSWER[0]=72195 and
ANSWER[1]=72195 (the derived structure drives the probes with no
flat competition). VALID=1 iff ANSWER[2]=72191 and ANSWER[3]=72195
(the taught hops are retrievable).

E4-W1: PREFLAT=1 iff ANSWER[2]=72299 (the flat wrong fact wins the
pre-contradiction probe). POST=1 iff ANSWER[3]=72295 (the licensed
contradiction superseded the wrong fact; the read path settles on
the derived value). VALID=1 iff ANSWER[0]=72295 and
ANSWER[1]=72295 (promotion: the structure formed and drove the
early probes) and ANSWER[4]=72291 and ANSWER[5]=72295 (the taught
hops are retrievable).

## 4. Worlds (fresh sealed worlds; streams pinned verbatim)

World files are generated byte-exact from these streams after this
prereg freezes (e4_worldgen.zag); E4_MANIFEST.sha256 is committed
before any run. QUERY lines carry the oracle expected value for
the scorer lineage convention; the inspector never reads them.

### E4-W0: control (no flat wrong fact; baseline derived-answer retrieval)

Material difference from E1-W4: fresh id block (721xx), single
subject. This is the baseline: the derived structure must form and
drive probes here, or E4 has no premise.

```
OBSERVE 72101 72111 72191
OBSERVE 72191 72112 72195
QUERY 72101 72119 72195
QUERY 72101 72119 72195
QUERY 72101 72111 72191
QUERY 72191 72112 72195
```

### E4-W1: precedence-reversal (tests H1a)

Material differences from E1-W2/PF-C1: (1) structure-first
ordering per section 2a: the chain is taught and probed (structure
forms) BEFORE the flat wrong fact is taught; (2) the contradiction
value is the derived answer itself (licensed contradiction per
section 2c), so supersession restores the derived value at the
flat layer; (3) the discriminator is the white-box inspector (does
the licensed derived structure survive the flat-fact teaching and
the contradiction?), with the behavioral legs as necessary
conditions.

```
OBSERVE 72201 72211 72291
OBSERVE 72291 72212 72295
QUERY 72201 72219 72295
QUERY 72201 72219 72295
OBSERVE 72201 72219 72299
QUERY 72201 72219 72295
OBSERVE 72201 72219 72295
QUERY 72201 72219 72295
QUERY 72201 72211 72291
QUERY 72291 72212 72295
```

## 5. Frozen decision rule

Process preconditions (any failure yields E4-INCONCLUSIVE, an
instrument failure, not an H1a verdict): both worlds x 3 runs
byte-identical transcripts per world (E4-K2); equal state.bin
SHA-256 per world across the 3 runs (E4-K2); E4-VALID=1 on every
run of both worlds; E4-DERIVED consistent across the 3 runs of
each world; E4-K1, E4-K3, E4-K4, E4-K6 all PASS; calibration
controls PASS.

- E4-PRECEDENCE iff W0 has DERIVED=1, FIRSTCLASS=1, VALID=1 on all
  3 runs AND W1 has DERIVED=1, PREFLAT=1, POST=1, VALID=1 on all 3
  runs. Confirms H1a as read-path precedence, a pure ordering
  phenomenon: the derived layer is fully intact through the
  flat-fact teaching and the contradiction (the licensed derived
  structure with both-hop evidence persists), so the only reason
  it did not drive the pre-contradiction probe is that the flat
  layer is consulted first. Decided evidence for the refined H1a;
  reported back into the cluster analysis.
- E4-SUPPRESSION iff W0 has DERIVED=1, FIRSTCLASS=1, VALID=1 on
  all 3 runs AND W1 has DERIVED=0, PREFLAT=1, POST=1, VALID=1 on
  all 3 runs. The subordination is not mere precedence: the world
  executed correctly (flat fact won, contradiction superseded, all
  validity probes hit, and the control proves the structure forms
  cleanly), yet no licensed derived structure survives the
  flat-fact/contradiction sequence. Redirects to a deeper
  suppression mechanism; reframes the refined H1a.
- E4-INCONCLUSIVE otherwise. In particular: W0 DERIVED=0 (baseline
  failure, no premise); any VALID=0 (world did not teach what it
  claims); POST=0 (the frozen contradiction protocol did not
  supersede, contradicting the E1-W2 precedent); any process bar
  failure.

Note: the task's literal behavioral SUPPRESSION signature ("the
probe still does not return the derived answer after the flat fact
is removed") is unobservable as a pure behavioral outcome in this
substrate, because the frozen contradiction protocol supersedes
rather than deletes (section 2b): after the contradiction the flat
layer holds the licensed value D, so a correct instrument must
return D at POST. The honest discriminator is therefore the
white-box leg: PRECEDENCE requires the licensed derived structure
to persist; SUPPRESSION is its absence under an otherwise
correctly executed world. This refinement is preregistered here,
not adjusted after seeing results.

## 6. Process bars E4-K1 through E4-K6

- E4-K1 (prereg ordering). PASS iff this file's commit strictly
  precedes the first commit containing any E4 world file, spec
  file, or tool source, and this file's SHA-256 is unchanged after
  the battery.
- E4-K2 (determinism). PASS iff both world transcripts are
  byte-identical across 3 fresh-state runs AND the per-world
  state.bin SHA-256 is equal across the 3 runs.
- E4-K3 (frozen binary). PASS iff freeze_shim2_bin and tnn2.zag
  match the section 0 hashes before and after the battery, and
  zero modifications under the frozen cognition paths.
- E4-K4 (seal integrity). PASS iff E4_MANIFEST.sha256 verifies
  (all files OK) and grep of 72000-72999 over tnn2.zag and
  freeze_shim2_bin returns zero matches (verified pre-freeze: zero
  matches in both).
- E4-K6 (no-leak). PASS iff e4_audit_noleak reports zero leaks.

## 7. Calibration

- Competent control: a synthetic inspector report containing a
  W1-conformant LICENSED DERIVED structure (subj=72201,
  rel=72219, answer=72295, evidence both hops) plus a synthetic
  transcript with ANSWER[2]=72299 and ANSWER[3]=72295; the checker
  must print DERIVED=1 PREFLAT=1 POST=1 VALID=1 for check E4W1. A
  synthetic W0-conformant report plus transcript must yield
  DERIVED=1 FIRSTCLASS=1 VALID=1 for check E4W0.
- Degenerate control: a synthetic report with only flat and
  per-instance structures; the checker must print DERIVED=0 for
  both checks.
- Inspector machinery cross-check: run e4_inspect_state_bin on
  the committed E1 W2 state bin (f5b1bab41) with the committed E1
  W2 world file; the STRUCTURE lines must match the committed
  e1_w2_inspect_r1.txt exactly (detection machinery unchanged).

## 8. K-C0A audit (zero new semantic cases in the inspector)

Frozen audit procedure, executed after the tools are built and
before runs:

1. e4_inspect_state.zag is byte-identical to the committed
   e1_inspect_state.zag (verified by cmp); therefore it contains
   zero integer literals in 71000-71999 (E1 K-C0A) and, by the same
   grep, zero literals in 72000-72999, and zero string literals
   naming a world, role, or relation. The inspector is fully
   generic over any state.bin plus any worldfile.
2. Predicate-vocabulary diff against e1_inspect_state.zag: empty
   (identical file).
3. The inspector collects OBSERVE lines only; QUERY lines are
   never read (oracle-blind by construction, inherited).
4. World parameters (id ranges, derived values, probe indices)
   appear only in e4_struct_check.zag as the frozen per-world bars
   of section 3 (scorer data, the v3_struct_check/e1_struct_check
   lineage), never in the inspector.
5. The audit prints K-C0A PASS/FAIL. K-C0A FAIL voids the
   inspector; rebuilding requires a new prereg section, never a
   silent fix.

## 9. Predicted outcome (recorded before execution)

E4-PRECEDENCE. Basis, read from the committed shim source before
any run: teaching the flat wrong fact creates only a tag-1 node
(ev_observe scans tag-1 nodes; the derived graph is tag-20 and is
never touched); contradicting it supersedes the old tag-1 node and
teaches a new one; revise_on_contradict revises only graphs
holding a type-1 edge to the contradicted fact node, and the
derived graph's licensing links are the chain-hop facts taught
before the flat fact existed. E1-W2 empirically confirmed a
licensed derived structure survives a contradiction untouched
(id=13, answer 71203, through the 71213 contradiction). The
derived structure should therefore persist with both-hop
evidence, and the behavioral legs should follow the activate path.

## 10. Criterion 0 status (binding)

This experiment probes frozen researcher-authored mechanisms with
a white-box inspector. C0-A through C0-D are NOT MET. No score
here may be described as L3, L3-adjacent, or progress toward L3.
Report as mechanism-targeted evidence for H1a only.
