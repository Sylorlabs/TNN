# BRIDGE RETIREMENT QUEUE -- PHASE 14

Lane `ownership`. Frozen ordering, with the blocker for each item stated.
**Zero deletions performed.** Nothing is deleted until a replacement is
committed to the canonical learner and the frozen battery is re-run.

Source: `BRIDGE_MAP.md` (`418da5377`).

## MEASUREMENT OF WHERE THE PROGRAM IS

```
explicit named bridges (_TO_ in code)     0
named cognitive modes in code             0
structural cognitive bridges              4
generic interface mechanisms              1
bridges deleted this session              0
bridges with a MEASURED replacement       2   (BR-1, BR-4)
bridges with a replacement IN THE CANONICAL LEARNER   0
```

The last line is the honest headline. Two bridges have been shown
*replaceable in isolation*; none has been replaced in TNN.

## QUEUE

### 1. BR-1 -- syntactic router
`unified_learn.zag:734` `route_line`

```
semantic routing branches   5 role-named route codes
researcher cognition        decides applicability from input shape
replacement                MEASURED (C1541)
                           derived-from-facts + probed contracts
                           surface-independent, permutation-invariant
blocker                    replacement not committed to the canonical
                           learner; frozen battery not re-run
deletion risk              LOW for capability, HIGH for regression
                           (other lanes may read route codes)
value of deleting           removes the researcher's authority to
                           choose which cognition runs
```

### 2. BR-3 -- candidate-origin taxonomy
`unified_learn.zag:1008` `kind: -1 none / -2 ambiguous / 0 proc / 1 bridge`

```
blocker                    depends on BR-1 and BR-2
note                       small but load-bearing: it makes "which
                           mechanism produced this" part of cognition
```

### 3. BR-2 -- failure-triggered conditional bridge
`unified_learn.zag:423,445`

```
condition (pos,val)        ALREADY LEARNED by search
failure policy             researcher-owned ("PROC_LEARN failure
                           automatically triggers bridge induction")
blocker                    SELECTION. C1681 showed the selection
                           mechanism does not yet beat a trivial
                           heuristic except under query-scoping with a
                           researcher-chosen key.
known defect               F-LEAK, recorded in the superseded header:
                           "bridge store full leaves leaked subset
                           procedures"
note                       deleting BR-2 before selection exists would
                           remove a leak source AND a capability.
                           Those must be separated: measure capability
                           loss with the leak closed first.
```

### 4. BR-4 -- numeric MAP count re-derivation
`xio_adapters/xio_core.zag:95-99`

```
root cause                 representation lossiness, not a routing error
replacement                MEASURED (C1651): MAP record carries its own
                           aggregation; one generic executor
evidence                   BASE 1 of 3 aggregations (SUM->2, the audited
                           bug; COUNT->3 by luck; MAX->2)
                           TREAT 3 of 3, FO fails loudly
blocker                    promotion format must change, which touches
                           every MAP consumer
open risk                  {COUNT,SUM,MAX} is a finite label vocabulary,
                           close to the menu pattern H16v3 kills.
                           Whether a MAP can retain a GENERAL
                           aggregation descriptor is untested and is a
                           prerequisite for safe deletion.
value of deleting           it is currently WRONG, not merely redundant
```

### 5. BR-5 -- generic operators replacing recipes
`l3_bridge_impl/bridge.zag`

```
action                     KEEP
evidence                   removed a signature enum + 3 recipe branches,
                           added 4 generic operators, every setnode call
                           inside one of the four (M3 verified)
note                       this is the compression TARGET for BR-1..4,
                           not a retirement candidate
```

## ORDER OF OPERATIONS, IF WORK CONTINUES

```
1. BR-4 provenance format change      (no dependency, currently wrong)
2. BR-1 replacement committed         (independent of selection)
3. selection mechanism validated      (blocks BR-2)
4. BR-2 + BR-3 deletion              (last; depends on 3)
```

Steps 1 and 2 are independent and neither waits on the open
method-ownership question. Step 4 does.

## WHAT EACH DELETION MUST RE-RUN

Per the retirement contract:

```
correctness      frozen battery byte-identical except the intended delta
transfer         no regression on witnessed transfer cases
lifetime         no state corruption introduced
H16              new mechanism audited BEFORE deletion, not after
scaling          where the mechanism sits in a hot path
```

And the metric set the program should report each cycle:

```
bridges                      4 -> target 0
semantic routing branches    5 -> target 0
researcher cognition LOC     (not yet measured; needs an instrument)
capability retained          must not fall
learner ownership            must rise
```

**`researcher cognition LOC` is not currently measurable.** Counting
lines in `unified_learn.zag` would count the substrate along with the
cognition, which is exactly the confusion this program exists to avoid.
An instrument for separating them is itself an open item, and it is
listed in the consolidated report as unstarted.

## HONEST STATUS

This queue is a plan, not progress. The session produced evidence that
two bridges are replaceable and zero evidence that TNN has been changed.
The gap between "replaceable in isolation" and "deleted" is a
commitment to the canonical learner plus a regression run, and no part
of that happened.