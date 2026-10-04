# REPORT: LT3 (FREEZE-ARENA-2) -- the harder third lifetime

Branch `lane/p1freeze`. Lane `p1_freeze_arena/`. Claims **C585-C596**.
Prereg `PREREG_LT3.md` (`222907a39`), committed alone, pre-implementation.
Harness errata and defects: `ERRATA_LT3.md`.

Binary `lt3`. stdout sha256
`555792382303bb090403ce7152f77eba9388c1e9d088b3e7b64757d7ce76e4c9`,
20363 bytes, **3/3 byte-identical**. All kill bars **K20-K32 pass** (35 checks,
`run_lt3.sh`, exit 0).

Attacks **C500-R1** and **FA1/C567-C580**.

---

## 1. HEADLINE

**The negative result survives a genuinely load-bearing 3-stage composition.
It is architectural.**

LT3 fixed the exact weakness FA1 admitted about itself. FA1's 2-stage join was
load-bearing on **A only**; C's facts could be deleted and the goal still
answered. So FA1's world never actually forced a composition. LT3's `GACF` goal
(A + C + F) is load-bearing on **all three stages** -- verified, not asserted:

```
J3 NOFACT A C F      arm 0:  0  0  0        arm 1:  0  0  0
```

Delete A's 52 facts -> wrong. Delete C's 52 -> wrong. Delete F's 52 -> wrong.
**Q6 passes for the first time in this line.** The world now forces the join.

And with the join genuinely forced, the preregistered adjudication cell is
reached, and it is the negative one:

| | measured |
|---|---|
| (a) `LIFETIME` answers `GACF` correctly? | **YES** (`j3lifetime ok=1`, cost 38464) |
| (b) `FRESH_ARENA` -- **zero** experience, full arena -- also correct? | **YES** (`ok=1`, cost 42720) |

`PREREG_LT3` section 11 fixes that cell in advance as:

> age improves correctness over an empty arena, but **not** over the same facts.
> Verdict: **NEGATIVE for "smarter with age"** -- the gain is data, not age.

## 2. THE POSITIVE CONTROL (primary artifact) -- PASSES

A silently-failing freeze reproduces C500-R1 for the wrong reason, so the
controls are the primary artifact. All seven hold, mechanically, in `run_lt3.sh`:

```
LK1 arm st nf pre post mem_pre  1 0 52 0  0 0    FROZEN stage A entry: 0 of 52 present
LK1 (sum over 10 FROZEN entries)                  = 0        (LIVE = 1068, all present)
LK2 (sum over 10 FROZEN entries)                  = 0        learner memory clean at entry
LK7 arm st mid arena mem_suffix sig  1 0 26 26 0 0   FROZEN midpoint: exactly floor(52/2)
LK7 (sum of midpoint arena over 10 FROZEN stages) = 534 = sum floor(n/2)
LK4  20 checkpoints, arena count == episode count at every one, both arms
LK5  FROZEN eq=1 AND firstdiff=-1 AND live_n==frz_n at all 10 checkpoints
LK3 nfe_ok=0 arena=0 memL=82 memLT=494     1068 episodes delivered, arena never written
```

Four independent facts, no shared code path: at stage entry the FROZEN arena
holds **0** of the stage's triples while LIVE holds **all 1068** by the end; at
each midpoint FROZEN holds **exactly half**; arena count equals episode count at
all 20 checkpoints; and **deleting the arena's write path entirely** (LK3) yields
**zero** correct answers after all 1068 episodes. Information does not arrive
early, and a freeze that failed *closed* would have been caught too.

**The freeze works.** K24, K25, K26, K27, K28, K29 all pass.

## 3. RESULTS

### 3.1 Examples-to-criterion (Q1, Q2)

```
stage                A   B   C   D   E   F   G   H   I   J
LIVE  (TTC)          0   0   0  -1  -1   0   0   0  -1   0
FROZEN(TTC)         37  37  37  -1  -1  28   0   0  -1  28
```

LIVE reproduces the C500-R1 artefact exactly: **TTC 0** wherever the goal is
answerable at all. Under the freeze competence is genuinely episode-gated.

The zeros and the `-1`s are all interpretable and none is a freeze failure:
* **G = 0** -- `G3` joins B and C, both already delivered before G starts.
* **H = 0** -- the invention-pressure goal must be *declined*, which requires no
  facts. The legitimate retention zero, as preregistered.
* **D, E = -1** -- those stages probe **F's** goal, which cannot be answered
  before F's facts exist. **I = -1** -- probes **J's** goal, same reason.
  `-1` means "never correct within the stage", which is the correct behaviour
  and is itself evidence the probe is gated.

### 3.2 The correctness table at the 3-stage join `GACF` (identical in both arms)

| row | episodes | arena | `GACF` | cost |
|---|---|---|---|---|
| **`LIFETIME`** | 1068 | full | **correct** | **38464** |
| `FRESH0` | 0 | **empty** | **wrong** | 0 |
| **`FRESH_ARENA`** | **0** | **full** | **correct** | **42720** |
| `FRESH_F` (stage F only) | 0 | 52 | wrong | 208 |
| `RECENCY16` | 0 | last 16 | wrong | 64 |
| `ABL-NOFACT-A` | 1068 | minus A's 52 | **wrong** | -- |
| `ABL-NOFACT-C` | 1068 | minus C's 52 | **wrong** | -- |
| `ABL-NOFACT-F` | 1068 | minus F's 52 | **wrong** | -- |
| `ABL-NOSTRUCT` | 1068 | full, templates+bindings wiped | wrong (declines) | 2136 |
| `ABL-SNAPSTALE` | 1068 | full, refresh off | correct | 38464 |
| `ABL-SNAPCTRL` | 1068 | full, refresh on | correct | 38464 |

**Zero experience plus the full arena reproduces the lifetime's answer exactly,
at 1.11x the cost.** Age buys almost nothing here -- not correctness, and now
almost not cost either.

### 3.3 The cost advantage of age is DECAYING (new finding)

Same measurement, three worlds, same architecture:

| world | facts | `FRESH_ARENA` / `LIFETIME` cost |
|---|---|---|
| C500-R1 (8 stages, 416 facts) | 416 | **62x** |
| FA1 (8 stages, join not load-bearing) | 416 | **5.8x** |
| **LT3 (10 stages, 1068 facts, real 3-stage join)** | 1068 | **1.11x** |

The older the learner, the less its accumulated structure is worth. At LT3 the
lifetime holds exactly **one** template (`tmplb=1`, `tmplh` 0->8) and 2 bind-store
hits; there is almost nothing for age to amortise. Extrapolating the trend, the
cost advantage of accumulated structure reaches zero. This is the sharpest
quantitative statement this line can make about *why* age does not help.

### 3.4 Positive / negative transfer, forgetting, interference, revision

Reprobes of stage A's goal at **D**, **E** and **I** are all `ok=1`: no negative
transfer, no forgetting. 600 distractors at E cost memory and time
(`memLT` 314 -> 519, `costep` 21736 -> **326836**, 15x) but **zero** accuracy.

Decline at H is correct in both arms (`code=0`, `declines=1`).

Revision/`fviol` rises monotonically `0,1,2,2,3,3,4,5,6,7` and does step at
stage I (`5 -> 6`), so the second revision is detected -- but by **one**
violation, not the two preregistered.

**Q12 FAILED.** FROZEN costs **less** than LIVE in aggregate
(`costep` 570846 vs 762480), because under the freeze the specialize indexes
have fewer stages' worth of facts to cover at query time. Same as FA1's P10.

### 3.5 Spontaneous reuse (charter 25) -- fires, but is NOT join-discriminating

`xw`/`rr` at each goal, both arms identical:

```
goal          A-GA  B-GB  C-GC  D-re  E-re  F-GF  G-G3  H-GH  I-re  J-GIJ
xw             0     1     1     0     0     1     1     0     0     1
rr             0     0     1     1     1     1     1     0     1     1
```

Reuse fires at **every** goal from B onward -- including `C-GC`, a purely
stage-local goal that needs nothing from A or B. The reprobes (which need
nothing new) correctly show `xw=0`. So the counters do distinguish "new stage
facts arrived" from "nothing new", but they do **not** show the learner
choosing A and C *because* `GACF` needs them.

**Q10 therefore fails in its discriminating form.** The learner reuses prior
structure whenever prior structure exists; it does not decide that a particular
prior stage applies to a particular new goal. Charter 25 is unmet at the join
goal, as it was at FA1's F -- now measured at a join that is genuinely
load-bearing on three stages, which makes the negative stronger rather than
weaker.

### 3.6 Plan-table saturation (Q9)

`plans` 1->10 and `pld` (plan drops) `0,1,2,3,4,5,6,6,7,8` against a frozen
4-slot table with 8 goal shapes. **First branch confirmed** (saturation is
real). **Second branch not observed**: all goals still answered correctly, so
saturation cost no goal its plan at this scale.

## 4. ABLATION OF THE REUSED STRUCTURE (charter 18)

`ABL-NOFACT-{A,C,F}` each break `GACF`, and the coverage-cleared variants agree
(`0,0,0`), so the dependence is on the **facts** of all three stages and not on
a stale index over them. This is the composition ablation FA1 could not make.

`ABL-NOSTRUCT` breaks `GACF` (`ok=0`, the learner declines), which naively says
learner-owned structure is load-bearing. **It is not**, for the reason FA1 gave:
NOSTRUCT is a hybrid state (episode-derived `L` + wiped `LT`). The clean
discriminator is the pair

> `FRESH_ARENA` correct at 42720 vs `LIFETIME` correct at 38464.

Same answer, 1.11x the cost, **zero** experience. The gain is entirely the
accumulated facts; the learner's structures are a thin cache over them, and at
LT3 the cache is nearly empty.

## 5. VERDICT ON CHARTER 24

**No. TNN does not become more intelligent with age.** Now demonstrated on a
composition that is verifiably load-bearing on three separate stages, with
facts provably delivered only by episode, and with a freeze certified by seven
controls including a positive control.

Localization, in the order the evidence forces:

1. **The answer is a lookup over the fact store.** `FRESH_ARENA` -- no
   experience, full arena -- reproduces it exactly. `ABL-NOFACT-{A,C,F}` each
   destroy it. Data in, answer out.
2. **The fan-in is arithmetic, not inference.** `GACF`'s three needs each reduce
   to `ret_gen`/`vfy_gen` over intersecting witness sets. No need consults the
   learner's memories; the learner is not in the loop at all.
3. **Accumulated structure is a cost cache that is nearly empty.** One template,
   2 bind hits, 8 plan drops against 10 goals. It changes the number of
   fact-checks and nothing about the answer -- and its value has decayed from
   62x to 1.11x as the world grew.
4. **Consequently episodes cannot add knowledge the frozen generic procedures
   cannot already derive from the same triples**, and age cannot buy
   correctness. The only thing age buys is the ability to *re-call* facts, and
   `RECENCY16` shows even that requires the facts to be present.

## 6. PREDICTION SCORECARD

| | prediction | verdict |
|---|---|---|
| Q1 | LIVE TTC 0 everywhere answerable | **CONFIRMED** |
| Q2 | FROZEN TTC > 0 at stage-local stages | **CONFIRMED** 37/37/37/28/28 |
| Q3 | FROZEN `FRESH0` wrong at `GACF` | **CONFIRMED** |
| Q4 | FROZEN `LIFETIME` correct at `GACF` | **CONFIRMED** |
| Q5 | gap present in **both** arms => not produced by the freeze | **CONFIRMED** |
| Q6 | `ABL-NOFACT-{A,C,F}` each break `GACF` | **CONFIRMED -- first time** |
| Q7 | `FRESH_ARENA` correct, large cost multiple | **CONFIRMED** (1.11x) |
| Q8 | `ABL-NOSTRUCT` breaks it (non-decisive alone) | **CONFIRMED**, non-decisive |
| Q9 | saturation `pld>0`; costs a goal its plan | **half** -- `pld=8`, no goal lost |
| Q10 | reuse counters flat at the join goal | **FAILED** in discriminating form |
| Q11 | 2nd revision raises `fviol` at two arity rules | **PARTIAL** -- raises by 1 |
| Q12 | FROZEN costs more than LIVE | **FAILED** -- costs less |

Six confirmed, one confirmed-with-datum, two half/partial, three failed. The
failures are reported as found; no bar was moved.

## 7. WHAT THE FREEZE CHANGED

Only the schedule and the cost. `lk1post` 1068 -> 0, `lk7arena` 1068 -> 534,
`costep` 762480 -> 570846. **Every correctness, transfer, forgetting, reuse,
revision and plan field is identical between LIVE and FROZEN**, including all
seven `ok` values and the whole `J3` table. The freeze changed when competence
becomes available, and nothing about any answer.

## 8. BOUNDARIES

* **Nothing here clears L3.** RETRIEVE/VERIFY/COUNT are researcher-frozen
  templates (C397). The goal *shapes* are a single fixed four-need chain reused
  eight times; the learner creates one template. Every object is enumerable
  from source. A positive result would still be L2; there is none.
* The `LIFETIME > FRESH0` gap is the weak claim "the learner retains and can use
  what it has seen". It is **not** evidence of increased intelligence.
* The freeze and the LIVE arm give **identical** answers, so LT3 does not show
  the freeze *creates* competence. It shows the competence is in the facts.
* One lifetime, one finite store (1068 triples, capacity 1200), 16 subjects,
  10 relations/stage, no perception, no noise, no drift, every episode, goal and
  declared answer researcher-authored, and every answer hand-derived from the
  world definition and then cross-checked by the memory-free oracle (K22 7/7).
* **`GACF`'s three stages share a subject band.** That is what makes a fan-in
  join expressible; FA1's private-per-stage bands made a multi-stage join
  impossible, which is why FA1 could only be load-bearing on one stage. Relation
  and object bands remain private per stage, so per-stage attribution is
  unambiguous and the LK2 value-collision confound does not arise.
* **The compiler is not blamed for anything.** All four defects found were in
  this lane's own harness, located by reading output against source and fixed
  against the memory-free oracle. See `ERRATA_LT3.md`. No compiler defect is
  asserted, and none was needed.
* **PROCESS-FAIL, disclosed.** One shell command in this wave ran without
  sourcing `.env/pure-zag.sh` and so invoked `python3` by name. The script was
  empty and performed no computation; every number in this report comes from
  the `lt3` Zag binary. Recorded rather than omitted.

## 9. NEXT EXPERIMENT

The architectural verdict is now three-for-three (C500-R1, FA1, LT3) and each
time the localization was the same, so **more goal difficulty will not move
it**. The open question is the one LT3's section 3.3 exposes:

> If accumulated structure is a cost cache whose value decays from 62x to 1.11x
> as the world grows, **what would ever make it worth more than the facts?**

Concretely, `LT4` should stop enlarging the *world* and start attacking the
*mechanism*: measure the cost-cache curve as a function of store size at fixed
task, and test the one hypothesis that would make structure load-bearing --
that a structure should let the learner answer a goal whose facts are **not all
present** (a genuine abstraction over the store, e.g. a goal stated by a rule
learned earlier rather than by triples). Under the current architecture that
must fail, and `ABL-NOFACT` must be shown to fail with it. If a learned rule can
substitute for absent triples, the negative result is overturned and the
localization in section 5 is wrong.

Second, and cheaper: `xw`/`rr` do not discriminate joins. A goal-shape-sensitive
reuse measure -- one that fires when a *specific* prior stage's structure is
selected -- would let charter 25 be tested rather than asserted, and would
distinguish "reuses whatever exists" from "decides what applies".