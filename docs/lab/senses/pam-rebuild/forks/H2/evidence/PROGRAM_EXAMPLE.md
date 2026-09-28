# H2 — Human-readable executable-program example (B7)

H2 has no sensory synthesis (no TNN-native renderer was built), so sensory
beauty does not apply. Below is one real, byte-exact percept program emitted
by the pure-Zag H2 pipeline, followed by a brief for non-specialist readers.

## The example (shapetrans, frozen fixture)

Stdout keys from `sense_h2 shapetrans t3_shapetrans/primary/p000.img`:

```text
approach=H2
task=shapetrans
judgment=CIRCLE
confidence=545
prog=PASS
pred=1
measure=949
program=H2/shapetrans|S1=shape:bbox=0,0,96,96|O1=grid((x+y)%12==0):ratio=968,area=1536|O2=grid((x+y)%12==6):ratio=930,area=1476|R=ratioavg=949,proto=c974/s684/t464|T1=1,T2=1,T3=1,P1=1|PRED=grid((x+y)%12==3):ratio=945,agree=1|result=PASS
ops=6593
cost=6593
```

Read the `program=` string left to right — it is the executable program:

- `H2/shapetrans` — which organ and task produced it (canonical header).
- `S1=shape:bbox=0,0,96,96` — **S**ensing: the shape occupies the full 96×96 frame.
- `O1=grid((x+y)%12==0):ratio=968,area=1536` — **O**bservation 1: a diagonal
  sampling grid over the shape reports a fill ratio of 968 (per-mille) with
  1536 grid hits.
- `O2=grid((x+y)%12==6):ratio=930,area=1476` — Observation 2: an independent
  second grid agrees (930 per-mille).
- `R=ratioavg=949,proto=c974/s684/t464` — **R**easoning: average ratio 949,
  compared against three shape prototypes (circle=974, square=684, triangle=464).
- `T1=1,T2=1,T3=1,P1=1` — **T**ests: three falsification tests all confirm the
  circle hypothesis; **P**rogram-integrity check passes.
- `PRED=grid((x+y)%12==3):ratio=945,agree=1` — **Pred**iction: the pipeline
  predicts what a *third, unseen* grid would report (ratio 945) and verifies
  it — the prediction agrees, so the percept is self-consistent.
- `result=PASS` — the program's executable verdict: it ran to completion and
  confirms the judgment.

`measure=949` is the re-executable scalar the memory gate uses to compare two
programs later (same-shape programs must agree within 150 per-mille);
`pred=1` says the program carries a verifiable prediction.

## The brief

Traditional perception software answers "what is it?" and throws away the
work. H2 answers "what is it, and here is the *recipe* that proves it" — a
short program that any part of the system can re-run, check, and compare
against later programs.

Concretely: when H2 sees a shape, it does not just output the word CIRCLE.
It outputs a program that says: "I measured this shape on two independent
grids, both agree it's mostly filled (about 95%), that fill matches a circle
far better than a square or triangle, three separate falsification tests
confirmed it, and I predicted a third measurement that also confirmed it."

That program is *canonical and bounded* (there is a hard cap on its length),
*deterministic* (the same bytes always produce the same program), and
*executable by the memory system*: the memory gate stores it, and when a
later, conflicting program arrives, the gate can compare the two programs'
measurements directly instead of trusting either judgment blindly. A wrong
program can be *reversed*; a right one, *corroborated* and eventually made
permanent; an unresolved one is *withheld* rather than guessed at.

The `ops=6593` / `cost=6593` lines are the honest compute receipt: H2 reached
this verdict in 6,593 elementary operations — about one quarter of what the
raw-values Approach A spent on the same fixture (27,651).
