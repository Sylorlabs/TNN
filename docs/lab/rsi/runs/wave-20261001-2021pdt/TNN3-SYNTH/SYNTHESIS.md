# SYNTHESIS: the frozen TNN-2 core has no learner-reachable construction paths

Lane: TNN3-SYNTH, wave-20261001-2021pdt. Writing only; no implementation.
Frozen substrate referenced throughout: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag,
1591 lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
(hash verified character for character by the H2/H3/H4/H6/H7 prereg workers).
Documentation rule observed: no em-dashes in this document.

## 1. Central finding

The frozen TNN-2 core has no learner-reachable construction, update, or
standing-maintenance paths. All construction in the build (the trial loop,
the three assemblers, promotion, surgical revision) is researcher-written
and event-triggered. The learner contributes the persistent arena and
scalar values but chooses no structure. This is not a claim about one
mechanism; it is the same finding, independently reached, across five
hypotheses:

- **H2 (inversion):** `link_edge` (lines 121-131) is direction-neutral;
  the "forward-only restriction" the hypothesis proposed to lift does not
  exist. The forward-only property lives in the only constructors that
  exist (`t2_asm_chain` 362-376, `t2_asm_count` 379-395, `t2_asm_sum`
  398-410), all called only from the researcher-written trial loop. No
  path from ev_observe / ev_query / ev_act allocates executable cells or
  writes ET_SEQ edges between cells. Deleting the assemblers removes the
  only graph construction, forward and inverse alike.
- **H3 (procedure-as-operand):** allocation is already unified. Every
  cell constructor (`t2_lit`, `t2_cell`, lines 338-348) calls the generic
  `alloc_node` (lines 86-104), the same allocator facts use. There is no
  separate allocation path to fold and the measured deletion set is
  empty. No event-interface path stores a graph root as a fact operand;
  fact operand fields (field28) hold scalar answer values only.
- **H4 (projection authoring):** the constant action write exists exactly
  as hypothesized (`miss_inquire` line 808), but there is no
  learner-reachable path for authoring a cell, and the protected EXECUTE
  machinery (lines 192-215) is not reachable from ev_act on any cell:
  ev_act's action wire is a direct field read (line 896). Wiring EXECUTE
  into the action path would be an addition, not a deletion.
- **H6 (standing):** the 12-line `bid()` formula exists exactly as
  hypothesized (lines 237-248), but it is shared by three selectors
  (activate line 145, evict_node line 259, ev_act lines 872/884), and the
  substrate it would be replaced by does not exist: no path updates
  UNCERT nodes after creation, there are no CONFIRM/CONTRADICT events,
  there is no learner link affordance, and the closest confirmation
  instrument (`r_learn_confirm`) is test-battery scaffolding unreachable
  from the cognition path.
- **H7 (re-derivation):** `t2_revise_graph` (lines 706-751, exactly 46
  lines) is the only revision machinery and the deletion target is real.
  But "the learner's own construction process" that re-derivation would
  reuse has no referent: the six cell constructors are invoked only from
  the three researcher-written assemblers and from the deletion target
  itself. No contradiction-to-construction trigger exists: the ev_observe
  contradiction branch teaches the new fact but never invokes
  mp_run/t2_trial, so post-deletion re-derivation would never fire at
  all.

**H1's two failures are the same root cause at the naming layer:** sealed
evaluation found zero learner-created names, and the red-team fabrication
report established that the naming affordance (tag-904 handle cells,
type-11 NAME edges) was asserted in PREREG_H1.md but never verified, and
in fact never existed in the frozen baseline. The "0 added lines"
pure-deletion plan froze a test of an impossible event, and the dev
harness constructed the signature it then verified.

Pattern statement: in every lane, the prereg asserted a learner
affordance (naming, direction choice, graph-as-operand, projection
authoring, standing maintenance, re-derivation) and specified a deletion
that presupposed it. The verification-first process fix (verify the
substrate against the frozen build before freezing any bars) caught all
of them: the affordances were never in the substrate, and the deletions
remove capability rather than liberating it.

## 2. Why the net-negative TNN-3 program dissolved

The TNN-3 hypothesis backlog was framed as net negative: capability
would come from DELETING researcher code, with zero cognition-source
lines added. That framing presupposed that each deleted mechanism was a
restriction sitting on top of a learner affordance. The verification
evidence shows the presupposition was false in every case:

- Naming (H1): the deletion could not create naming machinery that was
  never in the baseline.
- Direction choice (H2): the direction restriction did not exist; the
  deletion removes the only graph construction.
- Graph-as-operand (H3): unification was already the case; the deletion
  set was empty.
- Projection authoring (H4): the constant write is real, but nothing
  learner-authored can replace it, and EXECUTE is unreachable from the
  action path.
- Standing maintenance (H6): the bid formula is real and exact, but the
  learner-maintained standing to replace it does not exist.
- Re-derivation (H7): the revision schema is real and exactly measured,
  but the learner construction process it would defer to does not exist,
  and no contradiction-to-construction trigger exists to fire it.

Deleting researcher code cannot create learner capabilities. A deletion
removes the researcher's construction and leaves zero construction, not
learner construction. The net-negative program therefore cannot be
executed on this substrate: it would converge on a smaller binary with
zero learner capabilities, which is not architecture, it is subtraction.
H7's own falsifiable prediction names the end state of the program:
"re-derivation without a changed construction process is a treadmill
that re-learns the same wrong thing, and revision cannot be fixed
independently of construction."

## 3. The positive implication: TNN-3 requires additions, with architecture accounting

The finding inverts the program's framing but preserves its discipline.
TNN-3 requires ADDITIONS to the frozen substrate, recorded with positive
cognition-source delta and justified under the one-system rule. The
concrete missing affordances, named by the verification failures:

1. **A learner-reachable construction primitive.** A code path from the
   event interface by which experience can allocate executable structure
   (cells over the protected ISA) with learner-chosen content: guard/set
   slot orientation, topology, literal values from experience. This is
   the missing piece in H2, H3, H4, and H7.
2. **A contradiction-to-construction trigger.** A generic trigger by
   which supersession of a structure causes construction machinery to
   run against the live fact store, rather than leaving the stale
   structure silent. This is the missing piece in H7 (verification item
   c) and is load-bearing for H5's re-derivation story.
3. **Learner-writable standing.** A generic, learner-addressable
   standing instrument on UNCERT nodes (or their successor) that
   experience updates through the event interface, with an explicit
   replacement for all three `bid()` selectors (fact selection,
   eviction, guide selection). This is the missing piece in H6, and H9
   and H11 must be re-verified against this finding before any bars are
   frozen for them, since they assume learner-fed standing instruments.

This abandons the net-negative framing. It does not abandon the
architectural discipline that motivated it. Every addition must satisfy:
no modes, no bridges, no routers, no handlers, no task-specific semantic
cases; the pending protected-core ISA ruling still forbids
domain-regularity detectors (no FIND_THRESHOLD, no BUILD_CAUSAL_RULE,
no benchmark equivalents); the addition must be generic machinery
(comparable to ALLOC, LINK, EXECUTE), never intelligence. The one-system
rule's accounting stands: cognition-source delta is recorded and
positive deltas must be justified, with fewer special mechanisms and
lower delta rewarded. The verification-first process fix stays: a future
prereg must demonstrate the affordance by committed-source grep and
white-box dump BEFORE freezing any kill bar, per the rule the H1
red-team report established.

## 4. Relation to CONTLEARN (qualified)

CONTLEARN returned INTEGRATION-DEMONSTRATED: all of K0 through K6 pass,
30 white-box cross-phase citations (R1C 6, R2C 3, R3C 3, R4C 12, R5C 6)
on the fixed 149-event script, control parity on P1-P5, 0/18 on the
cross-phase negative control, 3/3 byte-identical determinism across 21
runs. The machinery integration is real: one learner, one process, one
build, no task labels, frozen ISA boundary intact, zero cognition-source
delta.

The independent red-team review qualifies the verdict: the learner's
causal contribution to every counted citation is zero. All integration
decisions are made by frozen researcher-written machinery, triggered by
researcher-authored events, with answer keys passed in the open
(`ev_query(W,s,r,exp,0)`, accepted iff the executed value equals
`expected` in `t2_try_verify`). The prereg's own non-claims (no L3, no
generality, no architecture claim) are honored.

**H10 must beat the qualified baseline, not the nominal one.** The
standing question for H10 is unchanged in form but raised in substance:
demonstrate cross-phase integration where the LEARNER does the
integrating, meaning structures created in one phase are
learner-reused in a later phase with the causal trace running through
learner-authored state, not through fixture-supplied answer keys. The
CONTLEARN measurements (REUSE_COUNT 30, zero interference loss, byte
determinism) are the machinery floor; H10's bars must discriminate
learner-owned reuse from machinery-triggered reuse.

## 5. Relation to H5: what survives and what is separate

Two distinct findings, which the red-team dissent keeps separate:

1. **The R-family guide-supersession fix is genuine and survives.**
   `supersede` is one generic protected edge-write (COMPARE plus LINK),
   used for UNCERT nodes, guides, MAPs, and facts; three pre-existing
   special cases were folded into it or deleted, net minus 22 cognition
   lines. The sealed behavioral delta is real (ev_act 30 to 0 on resolved
   guides; 12/12 retention; wrong-key selectivity). The trigger scans are
   researcher-written per-type rules over learner-accumulated structural
   state, so the "driven by learner-maintained standing" half of the
   hypothesis is not evidenced; that half belongs to H6/H11 territory.
   The dissent kills H5's wave verdict on KB-B2, not the R-family
   evidence.
2. **The MAP-key failure is a separate architectural gap.** The shadow
   diagnosis: `promote_graph` teaches a tag-1 shadow fact holding the
   promoted answer, and `activate` reads tag-1 facts only, so the shadow
   fact is the sole retrieval handle for the MAP key while the MAP node
   is a write-only ledger. On contradiction, MAP supersession writes are
   behaviorally inert: the MAP key always hits the live shadow fact,
   never misses, and re-derivation never runs (C1S bridge-query=100,
   C2S=900 after double contradiction, with mapCON-delta=1 on the same
   runs). Naive removal is not available: the shadow fact is load-bearing
   as the retrieval cache, and removing it would miss every promoted-key
   query and spam the inquiry machinery. The H5R lane is drafting a
   fresh prereg (VOID discipline: fresh prereg, fresh sealed worlds)
   with MAP-key-pinned bars, exact CON counts, and the query-path
   contract (Option A: MAP node as the retrieval structure; or Option B:
   provenance-linked shadow fact with cache invalidation) specified in
   the bars, never in prose.

## 6. Revised TNN-3 research direction

H8-H11 as framed are suspended, not killed: each presupposes a learner
affordance the substrate lacks (H9/H11 assume learner-fed standing,
per H6's finding; H8 inherits H1's construction dependency). The revised
direction is construction-first. Concrete next hypotheses, in dependency
order:

- **(a) Minimal learner-reachable construction primitive.** Design the
  smallest event-interface affordance by which experience allocates
  cells over the protected ISA with learner-chosen guard/set content.
  Verification target: the pending EXECUTE placement decision and the
  protected-core ISA ruling (the primitive must be machinery like
  ALLOC/LINK/EXECUTE, never a semantic case). This is the H2/H3/H4/H7
  successor; everything else depends on it.
- **(b) Contradiction-to-construction trigger.** A generic trigger by
  which supersession causes construction to run against the live fact
  store. Verification target: the trigger must fire on the frozen event
  interface and must not be a per-type handler. This is the H7/H5
  successor.
- **(c) Learner-writable standing.** A generic standing instrument that
  experience updates, with replacements specified for all three `bid()`
  selectors. Verification target: the standing reader must be callable
  from activate, evict_node, and ev_act. This is the H6 successor; H9
  and H11 are re-verified against it before any bars freeze.
- **(d) Procedure-as-operand, re-framed.** H3's successor, expressible
  only after (a) exists: a learner-constructed graph stored as a fact
  operand or edge target through the event interface. The prereg must
  demonstrate the construction path by grep before freezing bars.
- **(e) Naming, re-framed.** H1's successor, expressible only after (a)
  exists: learner-authored handle cells. The prereg must demonstrate the
  handle-cell machinery in committed source before any kill bar
  presupposes names can be created (the H1 red-team rule).

Process for each: (1) design the minimal addition; (2) verify it against
the protected ISA and the one-system rule; (3) preregister with the
substrate-verification section quoting exact source lines; (4) test on
sealed adversarial worlds designed post-freeze. No prereg freezes until
the verification section passes. The L3 criteria remain the evidence
standard: the final structure must not be in source, must be created
after experience, must be visible in white-box state with a causal
trace, must impair performance under ablation, must help on unseen cases
and transfer, and must survive an independent red team.

## 7. The skeptic's attack, and the answer

**Attack:** "This synthesis justifies adding researcher code, which is
the treadmill. Every failed evaluation will now be met with a new
affordance, and TNN becomes an accretion of researcher patches that the
one-system rule was meant to prevent."

**Answer, in three parts.**

First, the additions proposed here differ in kind from treadmill
patches. A treadmill patch is researcher code that performs the
cognition: a semantic case that detects the pattern, a handler that
builds the structure, a mode that switches behavior for the benchmark.
The construction primitive, the contradiction trigger, and the standing
instrument are researcher code that creates an affordance the learner
must then exercise itself. The researcher writes the possibility of
construction; the learner writes the construction. The discriminating
evidence is the standing L3 criterion set: the final structure must not
be in source, must be created after experience with a white-box causal
trace, must impair performance under ablation, and must survive sealed
adversarial worlds designed by an independent adversary. A treadmill
patch cannot pass these bars, because the structure would be in source.
If the primitive is built and sealed evaluation finds the learner still
authors nothing, the synthesis's prediction fails and the addition is
retired or redesigned. The process demonstrated this wave that it can
kill: H1 dead, H5's verdict dissented, five preregs stopped at
verification.

Second, the guardrails stay binding. Positive cognition-source delta is
recorded and must be justified; the one-system rule still rejects modes,
bridges, routers, and handlers; the protected-core ISA ruling still
forbids domain-regularity detectors; the pending EXECUTE placement
decision still constrains the machinery boundary. The question for every
addition remains the standing one: "Why can the existing general
architecture not learn this behavior?" The synthesis's answer for the
three named additions is concrete and falsifiable: because the frozen
core contains no path by which experience could produce the behavior at
all, verified by exhaustive grep across 1591 lines.

Third, the alternative is worse. The net-negative program, pursued
literally, was already producing vacuous tests: preregs freezing bars
against events the frozen binary cannot express, and dev harnesses
constructing the signatures the tests then "verify". A research program
that can only delete converges on a smaller binary with zero learner
capabilities and mistakes subtraction for architecture. That is decline
by another name, and the verification-first fix exists precisely to
prevent it.
