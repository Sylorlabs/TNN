# REPORT -- DISCRIMINATING THE RULES, AND H-SC C1621-C1650

Follows `REPORT_46.md`. 3/3 sha256
`cf8f72cfc2a1e15764a3d92e9a0f9b407912816c6a3106e2572e45a8a02a35c0`
bars lint CLEAN, loop lint CLEAN.

## PART 1 -- SEPARATING THE THREE-WAY TIE

C1601 left MAX, NONSELF and DAMPED identical because every viable chain
had length <= 2. Two probes, both predicted in advance.

### S1 -- the only viable chain is `(s,s)`

Facts `(10,1,110)`, `(110,2,210)`, so `class(10)=1`, `class(110)=3`,
`class(210)=2`. Target class 2, answer 210. The learned structure is
`s = ADD(0,100); OUT(0)`:

```
(s)    -> 110   class 3   not target
(s,s)  -> 210   class 2   IS target      the only viable chain
```

| rule | ans | chain | correct |
|---|---|---|---|
| SUM | 210 | (0,0) | 1 |
| MAX | 210 | (0,0) | 1 |
| **NONSELF** | **FAIL** | none | **0** |
| DAMPED | 210 | (0,0) | 1 |

**NONSELF is killed.** It forbids the only route to the answer. This was
the prediction.

### S2 -- a mixed chain against a singleton

Support `s0=10 s1=0 s2=7`, target class 1, answer 11 (the singleton
`(s2)`).

```
(s2)     -> 11   MAX=7   DAMPED=7
(s0,s1)  -> 12   MAX=10  DAMPED=5
```

| rule | ans | chain | correct |
|---|---|---|---|
| SUM | 12 | (2,2) | 0 |
| **MAX** | **12** | (0,1) | **0** |
| NONSELF | 12 | (0,1) | 0 |
| **DAMPED** | **11** | (2,-1) | **1** |

**MAX is killed.** `max(10,0)=10` lets a weak mixed chain beat a good
singleton, which is the same length-blindness that caused the
oscillation, just without the self-composition step. Also as predicted.

SUM picked `(s2,s2)` -- the self-composition inflation again.

**Only DAMPED survives both probes.** A single survivor is progress from
a three-way tie, not a validated rule: it is correct on two worlds and
has been tested on two worlds. More worlds could still kill it.

## PART 2 -- H-SC, PROVENANCE-SCOPED CREDIT

Credit is earned per regime rather than globally. The regime key is
`class(arg1)`, a property the learner derives from the fact table --
not a mode label.

Two arms, distinguished by whether the regime change is **observable**.

```
ARM-OBS    regime changes: class(arg1) 2 -> 3, while class(12) stays 1
            so the stale chain (s0,s1)->12 stays ELIGIBLE and the gate
            cannot rescue it. Only credit scoping can.
ARM-UNOBS  consequences change, nothing observable changes.
```

After phase 1 (12 trials, answer 12) global support is `s0=11 s1=11 s2=-1`.

| arm | first_correct | wrong |
|---|---|---|
| ARM-OBS, global credit | 12 | 21 |
| ARM-OBS, scoped credit | **0** | 14 |
| **ARM-OBS, scoped + DAMPED** | **0** | **0** |
| ARM-UNOBS, global credit | 12 | 21 |
| ARM-UNOBS, scoped credit | 12 | 21 |

## FINDINGS

**1. Scoping removes revision latency, and only when the regime change
is observable.** `12 -> 0` trials in ARM-OBS. In ARM-UNOBS scoped and
global credit are *the same numbers*, so they behave identically
(12/21), exactly as predicted. Scoping needs a signal; where there is
no signal it is not a weaker mechanism, it is a no-op.

**2. Scoping and damping are orthogonal and both are needed.**
Scoped credit alone fixes *latency* but still oscillates (14 wrong),
because it was combined with SUM. Scoped + DAMPED is
**first_correct=0, wrong=0** -- immediate and stable.

That is the candidate mechanism:

```
credit scoped to the regime that earned it   ->  removes latency
chain score damped by chain length            ->  removes oscillation
```

**3. The regime key must be learner-derivable.** `class(arg1)` is
computed from the fact table by the same code that computes every other
class. Nothing declares it a regime. That is what keeps this inside the
no-named-modes rule.

## WHAT THIS DOES NOT ESTABLISH

* DAMPED is **not** validated. Two probes, one survivor, and the probe
  set was designed to break rules, so a survivor is weak evidence.
* The combined mechanism was tested on **one** revision scenario. It has
  no transfer test, no ablation, and no adversary.
* `DAMPED` is `(sup[a]+sup[b])/len`. That is a few characters of
  researcher code inside the scoring rule, and it is doing real work.
  By RULE R5 and by H16v3's purpose, that is exactly the shape that must
  be attacked rather than adopted.
* **L3 = 0.**

## DEFECTS FOUND IN THIS LANE

Two, both mine, both in the arms rather than the substrate:

1. **Out-of-bounds scoped-table index.** I indexed the scoped support
   table by the regime *class value* (`3`) instead of a regime index,
   reading past the buffer. Symptom: scoped and global gave *identical*
   numbers, which looked like a clean null result rather than a bug. The
   fix produced the opposite conclusion, so the "null" was an artifact.
2. **ARM-UNOBS started from zero credit** instead of the phase-1 global
   support, so it was not the control it claimed to be. Symptom:
   `first_correct=0`, which contradicted the 12 predicted and should have
   been caught immediately.

Both were found by asking whether the arm could produce the numbers its
design predicted, which is now habit.

## STANDING

```
C1541  applicability  -> learner-owned
C1571  preference     -> learner-owned in effect, scoring rule not
C1601  oscillation    -> root-caused to length/self-composition inflation
C1621  NONSELF killed, MAX killed, DAMPED sole survivor
C1621  H-SC: removes latency iff the regime change is observable
C1621  scoped + DAMPED: 0 trials, 0 wrong, on one scenario
```

The remaining ownership gap is now stated as a single question:

> Can the learner derive its own credit scope and its own chain
> damping, rather than inheriting `class(arg1)` as a regime key and
> `/len` as a damping rule?

Those two are the last researcher-written pieces in the selection path,
and they are small enough to be plausible candidates for learner
ownership. That is the next experiment, and it is a better-posed
question than anything in the finder direction.