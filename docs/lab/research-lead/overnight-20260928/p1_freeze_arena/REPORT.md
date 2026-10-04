# REPORT: FREEZE-ARENA-1 (FA1) -- does age improve CORRECTNESS when facts arrive only by episode?

Branch `lane/p1freeze`. Lane `p1_freeze_arena/`. Claims **C567-C580**.
Attacks **C500-R1** (`lane/p1lifetime2`, df29e2b84 / 945ecb00a / 5e5ba93d5 /
368318d3a), certified verdict `LIFETIME-COST-ONLY`.

Binary `fa1`, stdout sha256
`1d2a268820f19d6534613711bb1529f41077857816bee8c4b0ef654b77c9b106`,
14106 bytes, **3/3 byte-identical** on this host.

---

## 1. HEADLINE

**The negative result survives the freeze. It is architectural, not an artifact
of the append-only schedule.**

C500-R1's confound was real and is now removed: under FROZEN, examples-to-
criterion rises from 0 to 44/17/21/31/12/24 at stages A,B,C,D,F,G, and a
zero-experience learner with an empty arena answers F **wrong** where the
lifetime answers **right**. So the gap `LIFETIME > FRESH0` that PREREG §11
designates as the adjudication test is **present and large**.

It is also present **identically without the freeze**, and the decisive row is
one C500-R1 did not report: a **zero-experience learner handed the arena
answers F correctly in both arms**, at 5.8x the cost.

Correctness is a function of *arena contents*. Experience changes only the cost
of reaching it. C500-R1's "cheaper, staler, never smarter" was correct, and its
stated cause was incomplete: it is not that the arena was append-only, it is
that the frozen generic procedures answer from the fact store by lookup.

## 2. KILL BARS

| bar | requirement | verdict |
|---|---|---|
| K1 | 3/3 byte-identical stdout | **PASS** `1d2a2688...` x3 |
| K2 | stdout bytes > 0 | **PASS** 14106 |
| K3 | oracle == declared | **PASS** `orc=8` (8/8: A,B,C,D,F,GG,GP,H) |
| K4 | LK4 channel invariant, 9 checkpoints | **PASS** `lk4_bad=0`, `eq=1` x9 both arms |
| K5 | LK1 arena purity 0 at 8 FROZEN entries | **PASS** FROZEN `lk1post=0` (LIVE 414) |
| K6 | LK2 memory purity 0 at 8 FROZEN entries | **FAIL on the literal bar** (`tot=4` at D, `26` at G); collision-excluded control is 0 at all 8. Cause and evidence in ERRATA2 E7 |
| K7 | LK3 `nfe_ok==0` | **PASS** `nfe_ok=0` after 416 episodes with the arena never written |
| K8 | LK5 arena equality LIVE==FROZEN, 9 cp | **PASS** `eq=1`, `firstdiff=-1` x9 -- **after fixing E5; it had never run** |
| K9 | frozen prefix sha256, one `fn main` | **PASS** `043b62b427e9...`, mains=1 |
| K10 | namecheck, 2 entry points, no hints | **PASS** `frz_episode`, `lt_query`; neither calls `frz_rbase`/`lt_nrel`/`lt_oracle`/`lt_decl`/`mk_goal` |
| K11 | anchor reproduces C500-R1 | **PASS** `09a09548b2675f99e86260da96cb39d9d8f74ffc7ebe3e1b38a896d1e5f15296` |
| K12 | LK7 midpoint | **PASS** arena == floor(n/2) at all 8 FROZEN (26,13,14,19,100,8,14,13 = 207); suffix-memory 0 at all 8 |

Six of the seven freeze-integrity bars (K4,K5,K7,K8,K12, and K6's intent) hold.
**The freeze works.**

## 3. THE POSITIVE CONTROL (primary artifact)

A silently-failing freeze reproduces C500-R1 for the wrong reason, so:

```
LK1 arm st nf pre post mem_pre 1 0 52 0  0 0     FROZEN, stage A entry
LK1 arm st nf pre post mem_pre 1 5 16 0  0 0     FROZEN, stage F entry
LK1 arm st nf pre post mem_pre 0 5 16 0 14 0     LIVE,   stage F entry: already full
LK7 arm st mid arena mem_suffix sig 1 5 8 8 0 0   FROZEN at F midpoint: 8 of 16
LK7 arm st mid arena mem_suffix sig 0 5 8 14 0 0  LIVE   at F midpoint: already 14
LK3 nfe_ok=0 arena=0                              416 episodes, arena never written
LK4 arm cp arena eps eq 1 8 414 414 1             arena count == episodes, always
LK5 arm cp 1 8 eq=1 live_n=414 frz_n=414 firstdiff=-1
```

Four independent facts, no shared code path: at stage entry the FROZEN arena
holds **0** of the stage's triples while LIVE holds **all**; at the midpoint
FROZEN holds **exactly half** and LIVE holds all; the arena count equals the
episode count at all 9 checkpoints in both arms; and deleting the arena's
writes entirely (LK3) yields **zero** correct non-decline answers despite all
416 episodes being delivered. Information does not arrive early.

## 4. RESULTS

### 4.1 Examples-to-criterion (LK6 / P1 / P2)

```
stage            A   B   C   D   E   F   G   H
LIVE (TTC)       0   0   0   0   0   0   0   0
FROZEN (TTC)    44  17  21  31   0  12  24   0
```

P1 confirmed: LIVE reproduces C500-R1 exactly. P2 confirmed to the letter:
FROZEN >0 at A,B,C,D,F,G and 0 at E,H, and the E and H zeros are the
preregistered *legitimate* retention zeros.

### 4.2 The correctness table at goal F (identical in both arms)

| row | episodes | arena | F answer | cost |
|---|---|---|---|---|
| **LIFETIME** | 416 | full | **correct** (22 slots) | 2240 |
| `FRESH0` (§11 primary) | 0 | **empty** | **wrong** | 0 |
| `FRESH_ARENA` (= C500-R1's published row) | 0 | full | **correct** | 12896 |
| `FRESHs` | F's 16 only | F only | wrong | 96 |
| `RECENCY16` | 0 | last 16 | wrong | 96 |
| `ABL-NOSTRUCT` | 416 | full | wrong (1 slot) | 2080 |
| `ABL-SNAPSTALE` | 416 | full | wrong | 2232 |
| `ABL-SNAPCTRL` | 416 | full | correct | 2240 |
| `ABL-NOFACT-A` | 416 | minus A's 52 | **wrong** | 0 |
| `ABL-NOFACT-C` | 416 | minus C's 28 | **correct** | 2100 |

### 4.3 Positive / negative transfer, forgetting

`D-reprobe-A = 1`, `E-reprobe-A = 1` (200 distractors do no damage),
`G-reprobe-B = 1` (the revision does not damage B), `H = 0` (correct decline
under invention pressure). P11 confirmed.

**But** `H-retain-GA = 0` and `H-reprobe-GF = 0`, in **both** arms. In the
C500-R1 anchor those same two rows are `GAret=1 GFret=1`. Adding the 416-episode
stream turned retention at H from intact to broken, and simultaneously
suppressed the functional-arity violation signal (`fviol` 1 -> **0**, P8
**fails**). Plan drops rose 1 -> 7, `memL` 492 -> 511, `memLT` 214 -> 551.
More experience made the learner *worse* at retention and *blind* to the
contradiction. This is interference with age, and it is arm-independent.

### 4.4 Spontaneous reuse (charter 25) -- **not observed at F**

Cumulative, identical in both arms:

```
stage          A  B  C  D  E  F  G  H
xw             0  0  0  1  1  1  3  4     cross-stage reuse fires
rr             0  0  0  1  2  2  2  5     reused-template fires
tmplb          1  2  3  3  3  4  4  4     templates built
bhit           0  2  4  4  4  8  8  8     bind-store hits
```

P9 is satisfied in the weak form (`xw=4>=1`, `rr=5>=1`). But the world was built
so that **F** requires A's structure, and at F both counters are **flat**
relative to E (`xw` 1->1, `rr` 2->2, `tmplh` 3->3): the learner built a new
template at F but recorded no reuse event for it. Reuse fires at D, G and H.
**The learner did not spontaneously decide that A applies to F.** Charter 25
fails at the goal it was designed for.

## 5. ABLATION OF THE REUSED STRUCTURE (charter 18)

`ABL-NOFACT-A` (delete all 52 stage-A facts) -> F **wrong**. `ABL-NOFACT-C`
(delete all 28 stage-C facts) -> F still **correct**. So the composition is
causally dependent on **A-era facts only**. P6's second preregistered branch
fires: the goal was declared to need A+C, but C's facts are not load-bearing,
and I report that rather than the prediction.

`ABL-NOSTRUCT` breaks F (`ok=0`), which naively says structure is
load-bearing. It does not, because `FRESH_ARENA` -- **zero** templates, zero
bindings, zero coverage, zero episodes -- answers F **correctly**. Per ERRATA2
E8, NOSTRUCT is a hybrid state (episode-derived `L` + wiped `LT`) whose failure
does not isolate structure. The clean discriminator is the pair:

> `FRESH_ARENA` correct at 12896 vs `LIFETIME` correct at 2240.

Same answer, **5.8x cheaper**. Age bought **cost**, not correctness. The §11
data-vs-structure question resolves to **data**: the gain is entirely the
accumulated facts, and the learner's own structures are a *cache* over them.

## 6. VERDICT ON CHARTER 24

**No. TNN does not become more intelligent with age in this architecture, and
this is now demonstrated in the one configuration where it could have been
true.** The freeze removed the confound and the negative result held.

Localization, in the order the evidence forces:

1. The answer is computed from the fact store by the frozen generic procedures
   `ret_gen/vfy_gen/cnt_gen`. `ABL-NOFACT-A` removes 52 facts and the answer
   dies; `FRESH_ARENA` adds zero experience and the answer is perfect.
2. The learner's accumulated structures (`specialize_*` indexes, coverage
   arrays, templates, bindings) index and route into that store. They change
   the number of fact-checks and nothing about the answer.
3. `try_family` decides family from field SHAPE alone and never consults the
   arena; `learn_bindings` memoizes a total function of shape. All "learning
   credit" for bindings is memoization, so no binding can be wrong.
4. Consequently episodes cannot add knowledge the procedures cannot already
   derive, and age cannot buy correctness. `costep` 110226 (LIVE) vs 86736
   (FROZEN) -- P10 predicted FROZEN would cost *more*; it costs **less**,
   because under the freeze the specialize indexes have fewer stages' worth of
   facts to cover at query time.

## 7. WHAT THE FREEZE DID AND DID NOT CHANGE

Only two things moved, and neither is correctness: `lk1post` 414 -> 0,
`lk7arena` 414 -> 207, `costep` 110226 -> 86736, `memLT` 550 -> 551.
**Every one of the 34 correctness, transfer, forgetting, reuse, revision and
capacity fields is bit-identical between LIVE and FROZEN.** The freeze changed
the *schedule*; it did not change a single answer.

## 8. BOUNDARIES

* Nothing clears L3. RETRIEVE/VERIFY/COUNT are researcher-frozen templates
  (C397). Every learner-created object is enumerable from source.
* The correctness gap that IS present (`LIFETIME > FRESH0`) is the weaker
  claim "the learner retains and can use what it has seen". It is **not**
  evidence of increased intelligence, and PREREG §13 said so in advance.
* The `LIFETIME > FRESH0` gap appears in **both** arms, so it is not produced
  by the freeze. §11's adjudication is answered YES, but the LIVE arm answers
  it identically, which is why the verdict is negative.
* K6 fails on its literal text; the collision-excluded control is what carries
  the claim. A reader who rejects the collision explanation should read K6 as
  failed and treat the freeze-integrity claim as resting on K4, K5, K7, K8, K12
  and LK3 -- all of which pass.
* One lifetime, one finite triple store (capped at 512 by `lt_add`; 416 used),
  no perception, no noise, no drift, every episode researcher-authored.
* One host, one compiler build (`znc 2026.07.0-dev`, macos-arm64).
* The compiler was **not** blamed for anything. Two instrument defects (E5,E6)
  were found and both were in *this lane's own harness*, located by reading
  output against source. No defect is attributed to the compiler without a
  memory-free oracle, and none was needed.

## 9. NEXT EXPERIMENT

`LT3`, per PREREG §12: 16 subjects and 10 relations per stage, 600 distractors,
six goal shapes against the frozen 4-slot PLAN table to force saturation
mid-lifetime, a 3-stage join (A+C+F) so the composed goal cannot be satisfied by
one prior stage, a second revision at stage I contradicting **both** A's and
B's arity rules, and a final stage J requiring a structure first assembled at
I. Same two arms, same seven controls.

The question LT3 must answer, sharpened by this report: §4.5 showed the F goal
was load-bearing on **A only**, not A+C, so the world did not in fact force a
composition. LT3's 3-stage join must be verified by `ABL-NOFACT` on **each**
contributing stage before any reuse claim is made. If a 3-stage join still
answers correctly for a zero-experience learner handed the arena, the
architectural verdict is confirmed at higher difficulty rather than overturned.