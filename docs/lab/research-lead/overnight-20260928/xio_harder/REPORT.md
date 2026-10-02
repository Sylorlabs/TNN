# REPORT.md -- H-XIO-2: Typed I/O Adapters Generalize Unchanged to the Harder Pair

## Verdict: XIO-HARDER-COMPLETE (with handoff analysis)

All 8 frozen kill bars (PREREG.md, commit bea72f336, committed before
any implementation existed) pass. The XIO adapter mechanism from C229
is reused BYTE-VERBATIM (zero edits, zero copies: the assembly recipe
references ../xio_adapters/xio_core.zag directly, sha256
4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f
before and after) and rescues the harder pair (transform-then-navigate,
d09995951) that killed all three invention mechanisms (H1/H2/H3). The
only new source this wave is the driver (world facts, queries, arms):
206 lines. Runs are 3/3 byte-identical.

## What was ported (and what was not)

Nothing in the adapter machinery was ported, adapted, or tuned. The
port is exactly: same staged execution v2 = stage(m2, stage(m1, s)),
new world. The pair scan's first differing pair on Z1 is now
(count MAP, chain MAP) instead of C229's (chain MAP, count MAP), and
the XIO-BUILD line records the reversed signature o1=1, o2=0 with the
computed handoff value mid=4:

```
XIO-BUILD id=214 m1=44 m2=96 o1=1 o2=0 rel1=81 rel2=82 qr=93 mid=4 ans=52
```

m1=44 is the learner-promoted count MAP (r=91, s=11, ans=3);
m2=96 is the learner-promoted chain MAP (r=92, s=3, ans=32).
rel1=81 and rel2=82 are read from the MAPs' own DEP provenance edges,
not from any researcher table. mid=4 is count(21), a COMPUTED NUMBER
with no fact-store node behind it, fed as the chain stage's subject.
ans=52 is the verified composite answer.

## Kill-bar scorecard (all from xhio_run1/2/3.txt, 3/3 identical)

- K1 Z success: TREAT Z1 ans=52. Exactly one adapter built, first
  mismatched pair tried (tried=1 rejected=0), signature o1=1 o2=0,
  rel1=81 rel2=82, qr=93, mid=4, ans=52. PASS.
- K2 Reuse: TREAT Z2a (41,93) ans=52 via `XIO-REUSE id=214 ans=52`;
  adapter count stays 1. No rebuild: the same adapter re-derived
  both stages for the new subject (count(41)=4, chain from 4). PASS.
- K3 Generalization: TREAT Z2b (71,94) ans=32 via a second adapter
  `XIO-BUILD id=313 ... qr=94 mid=3 ans=32` (mid=3 = count(71),
  chain from 3 reaches 32); adapter count becomes 2. Same stage MAPs
  (44, 96) reused under a new composite relation with a different
  intermediate. PASS.
- K4 Ablation causality: ABL-XIO (adapters disabled) Z1=Z2a=Z2b=-2,
  adapters=0 throughout. The d09995951 harder negative reproduces
  exactly when the adapter stages are off. PASS.
- K5 No-MAP controls: ABL-X (count MAPs deleted), ABL-Y (chain MAPs
  deleted), FRESH (no training): Z1=Z2a=Z2b=-2 in all three,
  adapters=0. In ABL-X the gate fails at xio_has_typed (no oty-1
  MAP); in ABL-Y only same-type count pairs exist so the mismatch
  gate admits none. Adapters compose learned MAPs; they are not a
  hardcoded Z solver. PASS.
- K6 Competence preserved: TREAT X1=3, X2=2, Y1=32, Y2=42. Matches
  d09995951 exactly. PASS.
- K7 Learner-built evidence: census shows 2 count MAPs (plen -1,
  oty 1, ids 44, 69) and 2 chain MAPs (plen 4, oty 0, ids 96, 114);
  adapter fields reference learner-promoted MAP ids; core sha256
  unchanged from the freeze-time value; grep confirms no
  type-conversion table and no COUNT_CHAIN / CHAIN_COUNT template in
  xhio_driver.zag. PASS.
- K8 Determinism: 3/3 runs byte-identical, sha256
  6909ba0c576b3204c110e259411cbb71970f3caa39912f812a2d7761188ab51a.
  PASS.

## Handoff analysis (the key result)

Preregistered signature S1 observed; S2/S3/S4 not observed. The
number to subject handoff works, and the white-box trace shows
exactly why.

The xdomain-harder worker identified the hard step as the type
transition "computed value -> subject": k=4 is not a fact-store node,
and no chain machinery re-subjects a query to a computed value. The
adapter's staged execution performs this transition with no special
casing, because the transition was never a type transition in the
first place. Stage 2 is `xio_stage_exec(m2, v1)` with v1=4, and the
chain branch calls `t2_gather(W, 4, paths)`. t2_gather is a BFS over
fact nodes (tag 1) indexed by subject id (cx_core.zag:442): it
compares `ng(W,n,20)==lastv` with lastv an i32. There is no
node-vs-number check on subjects anywhere in the path; the fact store
keys subjects by integer id, and the facts (4,82,50),(50,82,51),
(51,82,52) are present. The computed 4 re-subjects exactly like a
taught subject 3 or 21 would. The plen-4 path (4,50,51,52) matches
the Y MAP's plen, t2_asm_chain rebuilds it, masked verify returns 52.

So the diagnosis refines: the chain-bound mechanisms failed not
because a computed value cannot be a subject (it can; the substrate
never distinguished), but because their search spaces had no
value-level handoff step at all. H1 extends staged chains, H2 chains
subject-anchored fragments, H3 searches fact chains from the query
subject. None of them ever computes v1 = X(s) and re-submits it as a
fresh subject. The adapter contributes exactly one new operation to
the substrate: typed function composition with value handoff
(stage(m2, stage(m1, s))), gated on learner-observed output-type
mismatch. Everything else (the stage assemblers, the verify, the
provenance reads) is the learner's own trial machinery.

Failure-localization check (preregistered): had Z1 failed with
tried>=1 rejected>=1 and no BUILD (S2), the failure would have been
in the stage assemblers (t2_gather refusing subject 4), not the
adapter. Had tried=0 (S4), it would have been oty misclassification
or the pair scan. Neither occurred: the adapter gate fired on the
first differing pair and both stages executed.

## Ablation interpretation (causal reuse)

- Adapters off -> -2 on all Z queries (K4): the adapter stages are
  causally necessary for the harder pair, same as C229.
- Count MAPs deleted -> -2, adapters 0 (ABL-X): the oty-1 stage is
  necessary; without a typed MAP the gate cannot fire.
- Chain MAPs deleted -> -2, adapters 0 (ABL-Y): the oty-0 stage is
  necessary; same-type pairs are never adapter candidates.
- Adapter present, new subject, same relation -> reuse, no rebuild
  (K2): the adapter is a general procedure over the pair's type
  signature, not a memorized answer. It teaches no fact; Z2a could
  not have been answered by lookup.
- New composite relation -> second adapter built from the same stage
  MAPs (K3): the pairing (44, 96) is reused; only the relation key
  and the intermediate differ.

## Why this matters for the composition program

On 2026-10-02 composition was promoted to a core frontier with the
question whether mechanisms A, B, C collapse into one general
composition operation. This result adds a data point: the SAME
unmodified typed-composition operator now covers chain-then-count
(C229, o1=0 o2=1, node to count handoff) and count-then-chain
(this wave, o1=1 o2=0, number to subject handoff). The operator is
direction-agnostic: it pairs MAPs by observed output-type mismatch
and hands values between stages, regardless of which domain comes
first. That is evidence for the operator being general rather than
pair-specific, though still only over the chain/count stage types.

## Honest boundaries

1. Only chain/count stage types (inherited unchanged from C229).
2. Masked xio_try (expected=-2) returns -2, untested (inherited).
3. Two cross-domain pairs now covered (chain x count, count x
   chain-on-numbers); further pairs untested.
4. Pair search is brute-force over ordered MAP pairs (inherited).
5. oty via INC-cell scan is the inherited structural proxy.
6. The adapter does not invent stage procedures; the invention is the
   pairing and the typed handoff (inherited).
7. The em dashes in xhio_compile.txt are znc's own warning text
   (also present in the sibling's compile log); all worker-authored
   docs, code, and run outputs are dash-free (byte-checked).

## Standing metrics

- Cognition lines added: 0 to the adapter mechanism (byte-verbatim
  reuse); ~206 new driver lines (world/arms/census, unfrozen).
- Modes / bridges / handlers / new core semantic cases: 0 / 0 / 0 / 0.
- Hardcoded pair templates: 0 (grep-verified).
- Researcher-owned: world facts, queries, arm definitions, driver
  census layout. (Stage re-derivation, adapter layout, and the
  oty-difference gate remain C229's researcher-owned list,
  unchanged.)
- Learner-owned: all MAP graphs, oty labels (computed), stage
  relations (provenance-read), paired MAPs (44, 96), intermediate
  values (4, 3), both adapter nodes and their DEP edges.
- Capability-source delta: the Z capability comes from new learner
  state (2 adapter nodes + 4 DEP edges), not new researcher
  machinery. The mechanism delta for the harder pair is exactly
  zero lines.

## Deliverables (all in xio_harder/)

- PREREG.md (frozen bea72f336, before implementation)
- NAMECHECK.md (toolchain guard Step 0, commit-order self-check,
  build/run log, scorecard)
- REPORT.md (this file)
- xhio_driver.zag (new, unfrozen: harder-pair world, arms, census)
- xhio_full.zag (assembled: composition_A/cx_core.zag verbatim +
  xio_adapters/xio_core.zag verbatim + xhio_driver.zag)
- xhio_bin (pinned znc build), xhio_compile.txt (warnings only)
- xhio_run1.txt, xhio_run2.txt, xhio_run3.txt (3/3 byte-identical)

Pure Zag, safebin PATH, zero em/en dashes in worker-authored content
(byte-verified), paper untouched, committed locally, nothing pushed.
