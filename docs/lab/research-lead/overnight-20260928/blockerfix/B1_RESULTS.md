# B1 RESULTS — node-id / frame-slot namespace collision

Claim IDs **C577-C585**. Prereg: `PREREG.md` K8-K13.

## VERDICT: B1 IS NOW INVARIANT-BACKED ACROSS THE CONSTANT SPACE, AND THE
## MISSING C267 9-PHASE VERIFICATION PASSES.

---

## K8 — THE TWO LANES AGREE. No conflict.

| | `lane/scalingp8` 310a8a2d6 | `lane/eviction` 8f3a289fc/ec0f54aca |
|---|---|---|
| node-ref predicate | `if(op<0){return fr_get(W,f,(-op)-1);}` | **identical** |
| slot formula | `(-op)-1` | **identical** |
| legacy `op>=100000` left anywhere | 0 sites | 0 sites |
| adds counted guard battery | no | yes (`nsok_node`/`nsok_frame`, 11 sites) |

**The two fixes agree semantically and do not conflict.** `lane/eviction` is
a strict superset: same encoding, plus counted guards and a canary. This lane
independently reimplements the encoding from the specification (not by
cherry-picking either lane's file) and obtains the same thing.

## K9 — THE FROZEN C267 CORRECTNESS WAS AN ACCIDENT, CONFIRMED

Frozen `scaling_5000/s5000_full.zag`: `NN()=65536`, `res_op` reads
`op>=100000` as a frame slot. The collision condition is
`max_live_node_id >= FRAME_BASE`. Max legal node id is `NN-1 = 65535`, and
`65535 >= 100000` is **false** — unreachable. So the canonical 5k answers were
correct by accident of two unrelated constants, asserted nowhere.
`lane/eviction`'s threshold analysis is **confirmed**.

**Refinement this lane adds, which matters for interpreting K13:** `NN` is a
CAPACITY, not a USAGE. Raising `NN` from 65536 to 131072 does not by itself
cause the collision, because the 5000-MAP world only allocates ~35,500 nodes
(~7.1 nodes/MAP, the frozen lane's own measured ratio). The collision needs
the *live* node count to cross 100000, i.e. roughly **14,000+ MAPs**. `NN` is
what makes the crossing *possible*; the live count is what makes it *actual*.

## K10/K11 — THE INVARIANT, EXHAUSTIVELY SWEPT (the deliverable)

`b1_fuzz.zag`. Sweep of **24 combinations**: 6 arena sizes
(1024, 65536, 131072, 262144, 524288, 1048576) x 4 legacy thresholds
(0, 1000, 10000, 100000). For each, the highest legal node id (`NN-1`) is
pushed through the encoder with a distinguishing probe (node reads 111, frame
reads 222), so a misread is directly observable as a wrong answer.

```
B1F combos=24 legacy_collisions=21 disjoint_collisions=0
B1F inj_total=8 inj_bad=0 K11a_disjoint_zero_collisions=PASS K11b_legacy_test_has_teeth=PASS
```

**K11a PASS — the disjoint encoding has ZERO collisions at every one of the 24
combinations.** **K11b PASS — the legacy encoding collides in 21 of 24**, so
the test has teeth and is not vacuous.

The three legacy combinations that do *not* collide are exactly those where
`NN-1 < FRAME_BASE`: `(1024,10000)`, `(1024,100000)`, `(65536,100000)`. The
last of these is the canonical C267 configuration. Every arena size at or
above 131072 collides under every legacy threshold tried, including the
`FRAME_BASE=100000` that C267 relied on.

**Malformed-reference injection, 8/8 PASS**, each returning a defined value
and never a wrong answer:

| injected `op` | got | want | |
|---|---|---|---|
| -1 | 222 (frame) | 222 | PASS |
| -2 | 222 (frame) | 222 | PASS |
| -2147483647 | 222 (frame) | 222 | PASS |
| 0 | 111 (node) | 111 | PASS |
| 65535 | 111 (node) | 111 | PASS |
| 65536 (= NN) | **-999999** | -999999 | PASS |
| 131071 | **-999999** | -999999 | PASS |
| 2147483647 | **-999999** | -999999 | PASS |

**Why this is an invariant and not an argument.** Under the sign encoding the
integer line is partitioned by sign: node refs occupy `[0, NN)`, frame refs
occupy `(-inf, 0)`. These sets are disjoint for **every** `NN` by
construction, and `FRAME_BASE` is **not a parameter of the encoding at all** —
there is no constant left to get wrong. The 24-point sweep is the empirical
confirmation of a structural property, and the legacy column is the control
that proves the sweep detects the failure it is designed to detect.

## K12 — THE MISSING C267 9-PHASE BYTE-IDENTITY: **PASS**

`lane/eviction` REPORT2 §8.5 listed this as NOT DONE. It is now done.

The full 9-phase battery (`S1000L, S1000I, S5000L, S5000I, EML, EMI, EMM,
FAL, FAI` — `s5000_driver.zag:184-192`) was rebuilt from the frozen sources
with an NN-parameterised generator whose layout is **derived**, not copied:

```
nodes [64, 64+NN*40) | edges 16B each | log 32B x 128
NN=65536 -> edgebase 2621504, logbase 3670080, WSZ 3674176   (frozen values)
NN=131072 -> edgebase 5242944, logbase 7340096, WSZ 7344192
```

The generator's `NN=65536 legacy` output is **byte-identical to the frozen
canonical assembly**, so the generator introduces nothing.

**K12a PASS:**

| build | sha256 of stdout | vs canonical |
|---|---|---|
| frozen legacy NN=65536 (control) | `382e913a1ada...` | **byte-identical** |
| **disjoint NN=65536** | `382e913a1ada...` | **BYTE-IDENTICAL** |
| **disjoint NN=131072** | `382e913a1ada...` | **BYTE-IDENTICAL** |

Canonical `scaling_5000/s5000_run1.txt` is 64 lines, sha
`382e913a1ada196ac858de10644f1a3d2060f734c6b9dfa34be974c334fdc4d6`.

So the disjoint encoding **survives the exact rebuild that `lane/eviction`
identified as the thing that would have destroyed the accident**, and changes
no answer at either arena size. K12b (determinism) was asserted on every run;
K12c (non-empty output) holds — 64 lines every time.

## K13 — the accident survives this particular rebuild; the 20k boundary is
## INCONCLUSIVE (blocked by B2, not by the namespace)

**Preregistered prediction was that legacy at NN=131072 would break. It did
not.** `legacy NN=131072` is byte-identical to canonical. Reported honestly as
the prereg required. Per K9's refinement this is expected: at 5000 MAPs the
live node count is ~35,500, far below 100000, so enlarging the arena changes
nothing observable.

To push the live count past `FRAME_BASE` I attempted a 20000-MAP battery at
`NN=262144`:

* full 9-phase at D=19995: **both** legacy and disjoint **TIMEOUT at 900 s**,
  inside the `S5000L` build phase;
* indexed-only (D=19995, linear phases skipped): **both** legacy and disjoint
  **TIMEOUT at 600 s**, in the same decoy-build phase.

Both encodings time out identically and in the same place, so the obstacle is
**B2 (superlinear build), not the namespace**. Per prereg discipline the limit
was **not** extended; these are recorded as TIMEOUT. The empirical crossing
point therefore remains **unmeasured in this environment**.

This does not weaken the deliverable. The exhaustive 24-point sweep plus the 8
injections establish the invariant across the constant space *directly*, which
is a stronger statement than one 20000-MAP instance would have been. What is
missing is only an illustrative end-to-end instance of the collision.

## DISCLOSED DEVIATIONS

1. `c267_dis131` and `c267_leg131` were run **concurrently**, not serially as
   the prereg said. Two processes on 10 cores; the kill bars are byte-identity
   and determinism, not timing, so no bar is affected. Load average was
   18-54 throughout (foreign).
2. The 20000-MAP runs exceeded the prereg budget and were **not** re-run
   longer. Recorded as TIMEOUT.
3. The namespace battery in this lane's build uses pure guards returning the
   engine's existing `-999999` sentinel rather than `lane/eviction`'s counted
   `nsok_*` counters: all 16 arena header slots are occupied in the C267 base,
   so counters would have required re-dimensioning the header. Counting is done
   instead in `b1_fuzz.zag`, which is where the invariant is actually
   discharged. `lane/eviction`'s counted battery is the stronger instrument for
   the live engine and is not superseded by this one.
4. Machine was heavily loaded (load 18-54, foreign). All elapsed times are wall
   clock on a contended host and are not comparable across lanes.

## WHAT IS AND IS NOT CLAIMED

**Claimed:** the disjoint encoding is collision-free at all 24 swept
`(NN, FRAME_BASE)` pairs and under all 8 injected malformed references; the
C267 9-phase battery is byte-identical to canonical at both arena sizes; the
two prior lanes' fixes agree; the frozen 5k correctness was an accident of
`NN=65536` vs `FRAME_BASE=100000`.

**Not claimed:** that the legacy encoding is unsafe at 5000 MAPs — measured
byte-identical at `NN=131072`. Not claimed: the exact live-node count at which
the legacy encoding first breaks (unmeasured, B2-blocked). Not claimed:
anything about learning quality or L3. Nothing here measures intelligence.