# PHASE 1 -- BORROW PAIR CHOICE (FROZEN)

Frozen before implementation. Source: `BRIDGE_MAP.md`
(commit 418da5377).

## CHOSEN PAIR

```
X = a learned single-slot structure returning a computed integer
Y = a learned two-slot structure returning a node

ROUTER between them = BR-1  unified_learn.zag:734 route_line
FALLBACK between them = BR-2 unified_learn.zag:423/445 bridge_apply/bridge_learn
ORIGIN DISPATCH       = BR-3 unified_learn.zag:1008 kind taxonomy
```

Families are named in this document only. In the implementation they
carry **no cognitive name at all**, satisfying ROLE-NAME-REMOVE: they
are identified only by their learned signatures (slot arity and
returned kind).

## WHY THIS PAIR, EVIDENCE-BASED

The user's preference order was 1. checker -> candidate-generator,
2. memory-organizer -> decomposer, 3. stronger empirical pair.

Neither 1 nor 2 was selected, because the audit found **no bridge at
all** for either. `checker -> candidate-generator` does not appear as
a bridged pair anywhere in the corpus; `memory-organizer ->
decomposer` likewise. Choosing either would have required
manufacturing a bridge, which PHASE 1 forbids.

The audit instead found a bridge cluster with strictly higher
information: BR-1/BR-2/BR-3 in the **canonical learner**, which are
one missing generic property in three disguises. Criterion 3 applies.

## CRITERIA CHECK

| Criterion | Status | Evidence |
|---|---|---|
| structures genuinely learned independently | YES | procedure store and causal store are separate; each family is learned by its own verified trial templates |
| structurally / functionally different | YES | arity 1 vs arity 2; integer-returning vs node-returning; the integer family emits pure INC chains with no guard/set cells, the node family emits guard/set chains |
| current system needs an actual bridge | YES | `route_line` is the only thing that decides; `bridge_apply` covers discovery failure; both on witnessed path |
| bridge deletion measurably hurts | **TO BE MEASURED** (PHASE 2) | this is the experiment, not an assumption |
| plausible generic recruitment path exists | YES, and already validated | learned typed contracts PASS on 3 real domain pairs, pruning search 6 tries -> 3, zero literals, signatures computed by scanning each structure's own graph |
| generalizes beyond the exact pair | YES | the mechanism is applicability-from-learned-properties, which is domain-blind by construction |

## THE DECISIVE TEST

A syntactic router and a contract-based recruiter agree whenever
surface form happens to indicate semantics. They diverge the moment
**the same meaning arrives in a different surface form**.

So the treatment arm is tested on two encodings of identical
semantics:

* **ENC-SYNTAX-ALIGNED** -- punctuation distinguishes the families.
  The router can win here. Both arms should succeed.
* **ENC-SYNTAX-NEUTRAL** -- identical meaning, punctuation carries no
  family information. The router should fail. Contract recruitment
  should not.

This is the falsifiable core:

```
PREDICTION  router fails on ENC-SYNTAX-NEUTRAL
PREDICTION  contract recruitment succeeds on both encodings
```

If the router *also* succeeds on the neutral encoding, the bridge is
incidental rather than load-bearing, and the deletion claim weakens
to "cosmetic". That outcome is preregistered as acceptable and will
be reported as such.

## WHAT COUNTS AS SUCCESS

Strong result requires ALL of:

1. BRIDGE-ON works on ENC-SYNTAX-ALIGNED (baseline established).
2. BRIDGE-OFF on ENC-SYNTAX-ALIGNED does not lose capability.
3. BRIDGE-OFF on ENC-SYNTAX-NEUTRAL loses capability relative to
   contract recruitment (the bridge is load-bearing there).
4. Contract recruitment solves both encodings with no source change.
5. IRRELEVANT-STRUCTURE: a structure whose *syntax* matches but whose
   learned contract does not is NOT recruited.
6. FACTS-ONLY: facts alone do not reproduce the recruitment; the
   structure must be present.
7. IDENTIFIER-PERMUTE: renaming all ids and reordering the store
   changes nothing.
8. ABL-CONTRACT: removing learned signatures forces failure.
9. No role vocabulary in the cognitive path.
10. H16v3 audit: structures are assembled from generic primitives by
    verified search, never by a handwritten named method.

## TEMPORARY BRIDGE CONTROL

Exactly one, isolated, clearly marked, never counted as capability:

```
TEMPORARY_DELETE_ME_BRIDGE
```

It exists only to answer "what would the researcher-written solution
accomplish?" and is deleted for the treatment arm. It is listed in
the report's delete list and is not relied on by any measurement.

## FALSIFIERS DECLARED IN ADVANCE

At least one hypothesis must die, or the lane has failed even if the
treatment works:

* **H-ROUTER-NEEDED** -- syntactic routing is genuinely required.
  Falsifier: treatment passes on ENC-SYNTAX-NEUTRAL. Predicted: dies.
* **H-CONTRACT-SUFFICES** -- learned signatures alone determine
  applicability. Falsifier: treatment needs extra researcher hints.
  Predicted: survives.
* **H-SYNTAX-CORRELATION** -- syntax and semantics genuinely coincide
  in this world. Falsifier: a neutral encoding exists. Predicted:
  dies by construction.
* **H-RECRUITMENT-NOT-TRANSFER** -- what works on the first pair will
  not generalize. Falsifier: a second, topologically different pair
  also recruits. Tested in PHASE 4.

## COMPETING SUBSTRATE HYPOTHESES (PHASE 3)

Treated as competing, not cumulative. At least several must fail.

```
H1 content-addressed interaction
H2 local consequence adaptation
H3 mismatch-driven restructuring
H4 attractor / settling
H5 learned transformations
H6 learned compatibility / contracts      <-- primary, has prior support
H7 consequence-derived dependency recruitment
H8 local co-use plasticity
H9 learned executable rewrites
H10 self-created addressing
```

Per the standing rule, none of these may become permanent named
architecture. Each is an experimental substrate, and a mechanism
that survives must be compressed toward generic operations rather
than retained as a specialist module.

## NOT IN SCOPE FOR THIS PAIR

BR-4 (numeric MAP count re-derivation) is a **different** defect with
a **different** root cause: learner state is lossy. It is queued for
PHASE 10 architecture subtraction, where the treatment is to make MAPs
retain provenance, not to recruit a foreign structure. Conflating the
two would hide both.