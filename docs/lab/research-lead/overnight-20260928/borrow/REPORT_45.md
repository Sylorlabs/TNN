# REPORT -- BORROW PHASE 3-SELECTION / 4-TRANSFER / 5-REVISION

Lane `ownership`. Follows `REPORT_23.md`, attacking the boundary it
isolated. 3/3 sha256
`5830bc9f3ed3e221697f8bd2c47b150195f9e9000c7e98417edfcedeb7489a58`
R3 lint CLEAN. R1 role-name grep: 0 hits.

## THE QUESTION

C1541 proved applicability contracts are **necessary but not
sufficient**: a legitimately learned structure producing a class-valid
but wrong answer was recruited and accepted. So:

> Can the learner choose correctly *among* applicable structures, using
> its own consequence history, without any researcher-owned answer?

Competing hypotheses, not a shopping list:

```
H-CONTRACT-ONLY   contracts alone, no consequence    <- expected to FAIL
H2 / H7           consequence-adapted selection       <- under test
```

Design: the mechanism receives values, facts, contracts, and a scalar
consequence token per trial. It never receives the answer.
Structures are learned by verified search (`MAXQ=3`, declared).

## RESULTS

```
structures: s0 in=3 out=2 (110)   s1 in=3 out=1 (12)   s2 in=3 out=3 (11)

H-CONTRACT-ONLY           ans=11   expected=12   chain=(2,-1)
H2/H7 first_correct=1     wrong=1 of 12
support after:            s0=11 s1=11 s2=-1
final selection           ans=12   chain=(0,1) len=2

PHASE4 TRANSFER q=(20,111) expected=22  ans=22  chain=(0,1)

PHASE5 REV-A consequences change, facts fixed
         first_correct=12   wrong=21 of 40
         correct after first = 7 of 28   STABLE_90pct=0
PHASE5 REV-B facts change, gate invalidates
         first_correct=0    wrong=0

FO support_erased          ans=11
```

## WHAT WORKS

**Selection by consequence works, and fast.** One wrong trial
(`11`), then correct forever. Support moves `s2` to −1 and `s0/s1` to
+11 each. With support erased (FO) the same system reverts to `11`,
so support is load-bearing and facts alone do not reproduce the
choice.

**Transfer works with no source change.** A fresh query
`(20,111)` on the same structures and the same support state returns
`22` via the same chain `(0,1)`. This is genuine structural transfer,
not memorisation of one query.

**Gate invalidation is immediate.** REV-B: when the fact landscape
changes so the stale chain yields a class-0 value, the correct chain is
selected on trial 0. Worth 0 trials.

## WHAT FAILS: REVISION IS UNSTABLE

REV-A is the honest revision test: **consequences change, facts do
not.** The stale recruitment stays class-eligible, so only consequence
support can dislodge it.

It eventually does — first correct at trial 12 — but then **oscillates**:
only 7 of the following 28 trials are correct.

### Root cause, identified from the source

Support is summed over chain elements. Once `s2` is positive, the
chain `(s2,s2)` scores `2*s2`, which strictly beats the length-1
chain `(s2)` scoring `s2`. `(s2,s2)` produces `12`, the *old* answer,
now wrong. Each wrong trial decrements `s2` twice (it appears twice in
the chain), which drops it below zero, at which point `(s2)` wins
again. The system ping-pongs.

> **Naive additive support over chain elements rewards self-composition
> and longer chains, so it oscillates instead of converging.**

This is a design defect in the *scoring rule*, not in the structures
and not in the contracts. Support that accumulates per structure and is
summed along a chain is not a valid preference measure over chains.

### Two gate failures, honestly recorded

1. **My first revision arm was invalid.** I built a revised fact table
   that made the intended answer `11` class-2, so it was unreachable
   and the correct answer could never be produced. The arm measured
   nothing. Rebuilt.
2. **My second revision arm was invalid in a subtler way.** Making
   `12` class-0 gated the stale chain out, so revision appeared at
   trial 0 — but that was *gate invalidation*, not consequence-driven
   revision. Two different mechanisms were being conflated. Split into
   REV-A and REV-B, and only REV-A counts as revision.

Both were caught by asking whether the arm could produce its own
expected answer, and by noticing that a suspiciously perfect result
usually means the test was rigged.

### My hand prediction was wrong first

I predicted first-correct at trial 24. Measured 12. My model wrongly
assumed `s2` decayed while it was unused; it does not, because support
updates only for structures a trial actually used.

Corrected derivation: only `(s0,s1)` and `(s2,−1)` can produce a
class-1 value. `s2` overtakes when `−1 > 22−2k`, i.e. `k ≥ 12`.
**Corrected prediction 12, measured 12, exact agreement.**

Recorded because the misprediction is the evidence that the
measurement was actually predicted rather than rationalised after the
fact.

## FIVE SELF-CAUGHT DEFECTS

1. **Out-of-bounds write** (`trA`/`trB` 8 bytes allocated, 24 written).
2. **Stale root** — `learn` for B clobbered A's scratch before promotion.
3. **Promotion collision** — every structure wrote to the same base node.
4. **Exclusions written into persistent state** — within-call scratch
   (`sup -= 1e6`) was written into the learned support array and never
   restored, destroying it. Symptom: the distractor stayed permanently
   preferred. Fixed with a separate scratch array.
5. **Two missing loop increments** — `while(s<ns)` print loops with no
   `s=s+1`. Infinite loop grew the output cursor past the buffer, and
   `_zag_print(ob[0..c])` then read out of bounds: a segfault with zero
   output. Found by auditing every loop for an increment after the
   symptom proved layout-dependent.

Plus one design flaw caught before running: class matching by bit
overlap admits a class-3 value for a class-1 target. Changed to exact
class match.

**Defect 5 is the one worth institutionalising.** A missing increment
in a logging loop produced a *segfault*, not a wrong number, and the
segfault moved whenever I changed code layout. Any infinite loop that
feeds the output buffer is indistinguishable from memory corruption.
Every future program should audit loops for increments mechanically.

## WHAT THIS DOES AND DOES NOT ESTABLISH

Established:

* Consequence-weighted selection solves a problem that contracts
  provably cannot (C1541's counterexample).
* The learned selection **transfers** to a fresh query with no source
  change.
* Two different invalidation mechanisms exist and must not be
  conflated: **gate invalidation** (instant, structural) and
  **consequence revision** (slow, behavioural).
* Additive support over chain elements is unsound: it rewards
  self-composition and oscillates.

Not established:

* Stable revision. `STABLE_90pct=0`.
* Anything about L3. **L3 = 0.**

## THE NEXT QUESTION, NOW NAMED

The scoring rule is the researcher-owned part. Concretely, the next
candidates are competing hypotheses about how support should be
credited, each of which must be able to avoid self-composition
inflation:

```
H-SC            support is per-context (provenance-scoped credit)
H-DAMPED        updates are normalised/decayed, not raw sums
H-MAX           chain score is max, not sum, so length cannot inflate
H-NONSELF       a structure may not be reused within one chain
```

None is implemented here. Per the standing rules, these are competing
experimental substrates, not architecture to be added.

## STANDING UPDATES

```
BR-1  unified_learn.zag:734 route_line         REPLACEABLE (C1541)
BR-2  unified_learn.zag:423 bridge_apply       still blocked on selection
BR-3  unified_learn.zag:1008 kind taxonomy    deletable once BR-1/BR-2 are
BR-4  xio_core.zag:95-99 count re-derivation NOT deletable -- representation loss
```

Progress on the frontier question, stated precisely:

* Applicability: **moved to learner state.**
* Selection: **partially moved** (consequence-weighted, transfers) but
  the scoring rule is researcher-owned and demonstrably unsound.
* That is now the single narrowest, best-defined ownership gap found
  in this program.