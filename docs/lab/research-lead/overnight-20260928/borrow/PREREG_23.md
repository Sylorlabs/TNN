# PREREG -- BORROW PHASE 2+3 C1541-C1570

Lane `ownership`. Implements `CHOICE.md`. Frozen before code.

## 0. THE ASYMMETRY UNDER TEST

The audited router (`route_line`) decides applicability from the
**surface form of the input**. Contract recruitment decides
applicability from the **structures themselves**, by probing them.

Therefore the two agree only while surface form happens to correlate
with meaning. Probing does not care about surface form.

That is the whole experiment. It is principled, not staged.

## 1. SUBSTRATE (minimal, honest, and declared)

This is a **minimal reproduction of the audited architectural shape**,
not a port of the frozen 4-op ISA. Declared explicitly:

Reproduced from the audit:
* frame with integer slots, input in slot 0 (`t2_exec`)
* programs as linked op sequences with an output slot (`t2_asm_*`)
* INC-chain programs where the value is computed (`t2_asm_count/sum`)
* guard/set selection programs (`t2_asm_chain`)
* signature learned by inspecting a structure's OWN graph, never by
  literals (`xio_oty`)

NOT reproduced: the frozen node store, DEP provenance layout, tag
numbers. Bit-compatibility is not claimed and is not needed.

Primitives are generic and finite. Structures are **assembled by
verified search and promoted**, never handwritten as named methods
(H16v3 requirement).

## 2. VALUE CLASSES ARE DERIVED, NOT DECLARED

No `CHECKER`, `GENERATOR`, `MEMORY`, `DECOMPOSER`, `CAUSAL`,
`PLAN` vocabulary anywhere in the cognitive path.

A value's class is computed from the fact table:

```
k_subj(v) = 1 if v appears as some fact's SUBJECT
k_obj(v)  = 1 if v appears as some fact's OBJECT
```

A value may be both. Classes are sets computed at runtime. The code
never says what a class *means*.

## 3. LEARNING IS REAL

For each training family the learner enumerates op sequences of
length 1..3 from the primitive set over a small literal range,
executes each on the training input, and promotes the shortest
sequence that reproduces the training answer.

Promotion stores: the op sequence and its output slot. Nothing else.

Consequence: the learner does not know, and is not told, that one
family computes and another selects. It must discover that by
probing.

## 4. CONTRACT LEARNING BY PROBING

For each promoted structure the learner executes it on probe inputs
drawn from each derived class, and records:

```
in_classes   = classes whose probe inputs were accepted
out_class    = class of the returned value
```

Probing uses only execution and the derived class sets. Zero
literals. This is the audited mechanism (`ci_h1`, `gc_h1`).

## 5. RECRUITMENT

A contract graph is built over promoted structures:

```
edge s1 -> s2 exists iff out_class(s1) intersects in_classes(s2)
```

To answer a query whose input has class C_in and whose target is a
value of class C_out, the learner searches this graph from structures
with `C_in in in_classes` to structures whose output class is
`C_out`, composing the chain and executing it.

This contains no role names. It cannot express "use the checker in
the generator's role".

## 6. ENCODINGS

Same semantics, two surface forms:

* **ENC-ALIGNED** -- the leading token indicates the input class.
* **ENC-NEUTRAL** -- no indicator; surface carries no class
  information.

The learner is given the facts and the query. It is NOT given the
encoding. The encoding exists only to decide what the *router* can
see.

## 7. ARMS

```
A1 ROUTER-ALIGNED      BRIDGE-ON.  Syntactic router, ENC-ALIGNED.
A2 ROUTER-NEUTRAL      BRIDGE-ON.  Same router, ENC-NEUTRAL.
A3 CONTRACT-ALIGNED    BRIDGE-OFF. Contract recruitment, ENC-ALIGNED.
A4 CONTRACT-NEUTRAL    BRIDGE-OFF. Contract recruitment, ENC-NEUTRAL.
A5 CONTRACT-NOPROBE    Ablation.   Contracts unavailable. ENC-NEUTRAL.
A6 IRRELEVANT          An extra structure whose syntax matches but whose
                       contract does not is present and must not be
                       recruited.
A7 ABL-STRUCTURES      Structures removed. Must fail.
A8 FRESH               No training. Must fail.
A9 PERMUTE             All ids renamed, store reordered. Must match A4.
A10 FO-FACTS           Facts and structure present but the learned
                       contract graph erased. Must fail or degrade.
```

## 8. TEMPORARY BRIDGE CONTROL

Exactly one, isolated, never counted as capability:

```
TEMPORARY_DELETE_ME_BRIDGE
```

Implements the audited behaviour (choose family by surface form, and
substitute a fallback when the primary fails). Used only in A1/A2.
Deleted for A3-A10. Listed in the report delete list.

## 9. BARS

B1  3/3 identical sha256
B2  no role vocabulary in source (grep-clean, R1)
B3  exactly one TEMPORARY_DELETE_ME_BRIDGE, referenced only by A1/A2
B4  A1 succeeds (baseline established)
B5  A2 fails  (router is surface-bound; load-bearing on neutral)
B6  A3 matches A1 (no capability lost by removing the router)
B7  A4 succeeds (recruitment is surface-independent)
B8  A5 fails (contracts are load-bearing)
B9  A6 does not recruit the irrelevant structure
B10 A7 fails
B11 A8 fails
B12 A9 == A4 under permutation
B13 A10 fails or degrades
B14 H16v3 audit: structures assembled by search, no handwritten method
B15 at least one declared falsifier died
B16 L3 printed as a value
B17 delete list printed

## 10. PREDICTIONS

```
P1  A2 fails while A4 succeeds.        (router surface-bound)
P2  A5 fails while A4 succeeds.        (contracts load-bearing)
P3  A6 does not recruit.               (contract gate real)
P4  A9 == A4.                          (no identifier dependence)
P5  A10 fails.                         (facts alone insufficient)
P6  H-ROUTER-NEEDED dies.              (treatment passes on neutral)
```

If P1 is false (router also solves neutral), the router is
incidental, the deletion claim drops to cosmetic, and that is
reported as the finding.

## 11. STOPPING RULE

If A4 fails, learned-contract recruitment does not work in this
substrate and the BORROW direction is closed here. If A4 succeeds and
A2 fails, BR-1/BR-2/BR-3 have a measured replacement.

## 12. DISCIPLINE

Pure Zag. `_zag_print`. 3/3. R3 lint must pass.
No role vocabulary. Structures learned by verified search.
No bar hardcoded in a label string.
Independent closed-form check on the router's expected behaviour
before interpreting A2.