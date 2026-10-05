# REPORT -- BORROW PHASE 2+3 C1541-C1570

Prereg `bf1be353e`. Pair frozen in `CHOICE.md` (`4969b3d46`).
Audit: `BRIDGE_MAP.md` (`418da5377`).
3/3 sha256 `60568c3f30ddff1518b37446a9a47680756b82b7332b4cd9f969817024fa5eef`
R3 lint: CLEAN.

## WHAT WAS BUILT

A minimal, declared reproduction of the audited architectural shape
(frame with integer slots, programs as linked op sequences with an
output slot, INC-chain computed values, guard/set selection programs,
signatures learned by inspecting a structure's own graph).

Not a port of the frozen 4-op ISA. Bit-compatibility not claimed.

Structures are **assembled by verified search** over a generic
primitive set (search lengths 1..4) and promoted. No handwritten
method. The learner is never told which structure computes and which
selects; it discovers that by probing.

Value classes are **derived from the fact table**
(`bit0 = occurs as subject`, `bit1 = occurs as object`). No
`CHECKER` / `GENERATOR` / `MEMORY` / `DECOMPOSER` / `CAUSAL` /
`PLAN` vocabulary anywhere in the cognitive path.

```
derived class:  10 -> 3   110 -> 2   12 -> 1   121 -> 2   -1 -> 0

structure 0  in=3 out=2  ops=[ADD(0,100) OUT(0)]     learned from (10,0)->110 (11,0)->111
structure 1  in=3 out=1  ops=[ADD(0,-98) OUT(0)]     learned from (110,0)->12 (120,0)->22
```

Query: values `(10,121)`, answer must have derived class exactly 1.
Hand-derived expectation: `10+100 = 110`, then `110-98 = 12`.
**Expectation derived by hand before running, and used only by the
scorer** -- `recruit()` never sees it.

## RESULTS

```
A1  ROUTER-ALIGNED      ans=12    chain=(0,1) chain_len=2
A2  ROUTER-NEUTRAL      ans=FAIL
A3  CONTRACT-ALIGNED    ans=12    chain=(0,1) chain_len=2
A4  CONTRACT-NEUTRAL    ans=12
A5  CONTRACT-NOPROBE    ans=FAIL
A6  IRRELEVANT          ans=11    chain_used=(2,-1) accepted_len1=1
A6R ROUTER-ALIGNED+distractor  ans=11  accepted_len1=1
A7  ABL-STRUCTURES      ans=FAIL
A8  FRESH               ans=FAIL
A9  PERMUTE             ans=12
A10 FO-FACTS            ans=FAIL
```

## PREDICTIONS

| | Prediction | Outcome |
|---|---|---|
| P1 | router fails on neutral, contracts do not | **CONFIRMED** (A2 FAIL, A4=12) |
| P2 | contracts load-bearing | **CONFIRMED** (A5 FAIL, A7/A8 FAIL) |
| P3 | irrelevant structure not recruited | **FALSIFIED** (A6=11) |
| P4 | permutation invariant | **CONFIRMED** (A9=12) |
| P5 | facts alone insufficient | **CONFIRMED** (A10 FAIL) |
| P6 | H-ROUTER-NEEDED dies | **CONFIRMED** (treatment passes on neutral) |

## POSITIVE RESULT: THE ROUTER IS SURFACE-BOUND, AND IT IS NOT NEEDED

`TEMPORARY_DELETE_ME_BRIDGE(aligned) = 1`, `(neutral) = 0`.

The bridge substitutes **surface form** for type information. When
the surface stops carrying type information, the bridge withholds and
the capability is lost (A2). Removing it and deriving arg0's class
from the fact table costs nothing on the aligned encoding (A3 = A1 =
12) and **fully recovers on the neutral encoding** (A4 = 12).

So BR-1 has a measured replacement, and the deletion claim is
**load-bearing, not cosmetic**:

```
B4 router_aligned_ok=1
B5 router_neutral_fails=1
B6 no_loss_vs_router=1
B7 contract_neutral_ok=1
B8 contracts_loadbearing=1
B10 abl_structures_fails=1
B11 fresh_fails=1
B12 permute_matches=1
B13 fo_fails=1
```

Nine of ten bars pass. Deleting the router is safe, and the surface
dependence it introduced was pure loss.

## NEGATIVE RESULT, AND IT IS THE IMPORTANT ONE

**P3 is falsified.** A third structure, learned from *its own* training
data (`(10,0)->11 (11,0)->12`, promoted as `ADD(0,1); OUT(0)`), is
recruited as a length-1 answer and returns **11** instead of 12.

The distractor is not planted. It is a legitimately learned structure.
Its output `11` has derived class exactly 1 -- it really is a
subject-only value. Every criterion available to the mechanism is
satisfied. **There is nothing in this substrate that could reject it.**

### Localization: this is NOT a bridge-removal regression

```
A6  CONTRACT + distractor  -> 11
A6R ROUTER   + distractor  -> 11
```

Both arms break identically. The defect lives in the **shared
recruitment machinery**, not in anything the bridge was doing. Removing
BR-1 neither causes nor fixes it.

### The architectural boundary this exposes

> **Applicability contracts are necessary but not sufficient.**

The mechanism can decide *whether a structure could apply*. It cannot
decide *which of several applicable structures is the right one*.
Everything available to it -- class membership, chain length,
producing a value of the required class -- is satisfied by a wrong
answer.

This sharpens the audit conclusion rather than reversing it:

* BR-1/BR-2/BR-3 (applicability) have a measured generic replacement:
  learned contracts derived from facts and from probing the structures.
* **Selection among applicable structures is a separate capability and
  remains researcher-owned.** In current TNN that is the verifier and
  the trial/acceptance machinery.

So the honest statement of progress is: **one researcher-owned decision
(applicability) was removed; the next one (selection) is now named and
unclaimed.**

### What would close it, and why it is not attempted here

Closing it requires a selection criterion the learner owns: consequence
history, verified trial against outcomes, or preference among structures
learned from past results. Each of those is a real mechanism, not a
patch, and each risks being exactly the researcher cognition this
program is trying to remove. PHASE 3 lists these as competing
hypotheses (H2, H5, H7, H9) precisely so that the next candidate is
chosen as a hypothesis rather than as a fix. **Not attempted in this
lane**, and reported as an open boundary rather than papered over.

## FOUR SELF-CAUGHT DEFECTS (all mine)

1. **Out-of-bounds write.** `trA`/`trB` allocated 8 bytes; the code
   wrote 24. No bounds checking exists, so the training data was
   silently corrupted and *nothing was learned*. Symptom: promoted=0.
2. **Stale root.** `learn` for B reused the scratch region, destroying
   A's graph before `promo` ran. Both structures came out identical.
   Fix: promote each structure immediately after learning it.
3. **Promotion collision.** `promo` always wrote to the same base node
   address, so every structure overwrote the first. Symptom: two
   structures with identical ops. Fix: per-structure node slots.
4. **Mislabelled bar field.** The chain-length report read the wrong
   trace slot and printed `len=0` for a length-2 chain. Fixed to
   derive length from whether the second structure index is present.

A design flaw was also caught **before** running: matching classes by
bit overlap admits a value that is both subject and object for a
subject-only target. Changed to exact class match.

Every one of defects 1-3 produced a *plausible-looking* wrong answer
rather than a crash, and none would have been visible without checking
the promoted graphs against the training data by hand.

## H16v3 AUDIT

* No named cognitive mode in source (grep-clean).
* Exactly one `TEMPORARY_DELETE_ME_BRIDGE`, referenced only by the
  router arms; deleted for the contract arms.
* Structures assembled by verified search over generic primitives;
  no `grown()`-style handwritten method.
* No facts leak: `recruit()` receives values, the fact table and the
  contract table; it never receives the expected answer. A10 confirms
  erasing the contract table destroys the capability, so the answer is
  not recoverable from facts alone.
* **L3 = 0.** Applicability moved, but selection did not, and a system
  that can pick the wrong applicable structure has not demonstrated
  method ownership.

## DELETE LIST

```
TEMPORARY_DELETE_ME_BRIDGE   (1 item)
```

Audit-level candidates now with a measured replacement:

```
BR-1  unified_learn.zag:734 route_line        deletable, replacement measured here
BR-2  unified_learn.zag:423 bridge_apply      NOT deletable until selection is solved
BR-3  unified_learn.zag:1008 kind taxonomy   deletable once BR-1/BR-2 are
BR-4  xio_core.zag:95-99 count re-derivation NOT deletable -- representation loss
```

## VERDICT

**BORROW PHASE 2+3: PARTIAL SUCCESS WITH A NEW BOUNDARY.**

Success: BR-1 is replaced by learned contracts; the replacement is
surface-independent, permutation-invariant, facts-only-resistant, and
costs no capability.

Killed: the hypothesis that contracts alone are a sufficient
replacement. A legitimate learned structure producing a class-valid but
wrong answer is recruited and accepted.

New frontier: **selection among applicable structures.** That is now
the precise next ownership question, and it is narrower and more
useful than "learn the finder".