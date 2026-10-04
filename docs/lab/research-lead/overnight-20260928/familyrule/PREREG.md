# PREREG — FAMILY-RULE (C730-C759)

Lane `familyrule`, branch `lane/familyrule`. **Preregistered BEFORE any
implementation. No result observed at the time of writing.** Kill bars frozen.
A design flaw discovered later is marked **VOID** in `ERRATA.md` and
re-preregistered openly. **A miss is never reinterpreted as a pass.**

## 0. THE PRECONDITION, STATED HONESTLY AND FIRST

**This experiment adds a capability to the substrate.** That is exactly the
change the ONE-SYSTEM RULE warns against. I am doing it deliberately, because
`lane/p1falsifier` closed with the instruction *"a second family rule permitted
to read the store — the only overturn route that doesn't change the world"* and
that instruction cannot be obeyed without changing the code.

What that costs, stated before any measurement:

1. **The p1falsifier negative is no longer tested against the substrate it was
   measured on.** Any negative I report is about *my* substrate. It cannot
   retroactively weaken theirs; it can only narrow the scope of their claim.
2. **A new procedure is new researcher contribution.** The regularity the new
   procedure exploits is a regularity of the worlds unless the procedure's own
   evidence test is generic. Section 7 states the hand-holding position in full
   and section 7.3 names the exact regularity class I chose.
3. **Charter 108 (no code whose semantics correspond to a test name).** The new
   rule therefore contains no relation id, no stage index, no goal tag, no need
   tag, no subject id, no width, no count, and no string. It reads one
   argument, the store, and a goal record. If that cannot be achieved, that is
   itself a finding and I will report it rather than smuggle a literal in.

## 1. WHAT IS FROZEN AND WHAT IS NEW

Copied **byte-identical** into this lane from `lane/p1falsifier` commit
`4e45abd8e` (`docs/lab/research-lead/overnight-20260928/p1falsifier/`), sha256
asserted by `run.sh`:

| file | role |
|---|---|
| `sup.zag` | LT3 lifetime support: template store, bind store, `lt_fresh`, `lt_query` |
| `wld.zag` | frozen world W-LT3 writers, `lt3_goal4`, declared answers |
| `life.zag` | FREEZE-ARENA episode layer: `frz_episode`, the only arena writer |
| `hlp.zag` | harness formatting helpers |

`frz.zag` is copied to `frz3.zag` and **edited**, with every edit listed in
`DIFF.md` and each one marked by a `//FR3:` comment. No frozen procedure body
is modified: families 0/1/2 and every executor branch for them are byte
identical. The edits are exactly:

* **E1** `try_family`: one added dispatch `if(fam==3){ return fx_sx_bind(...); }`.
* **E2** `learn_bindings`: family trial order becomes `3,0,1,2` **only when the
  runtime switch `L[13276]==1`**; with the switch 0 the loop is byte-for-byte
  the original `0,1,2` three-iteration loop.
* **E3** `exec_step_iter`: one added branch `if(fam==3){ fx_sx_exec(...); }`.

New files: `sx.zag` (the rule's primitives, concatenated **before** `frz3.zag`
because Zag is concatenated with no forward declarations) and `fr_main.zag` (the
harness). `compose`/`execute_plan` in `frz3.zag` are **unreachable dead code**
(grep: no call site outside themselves) so they are not edited; documented.

The learner is reached only through `frz_episode` and `lt_query`. No file of
any other lane is touched. The runtime switch lives in the learner state array
at offset **13276**, in the 6-cell gap 13276..13296 that the frozen file
documents as unused. Cells used: `13276` switch, `13280` SX consumed,
`13284` SX refused-store-has-it, `13288` SX rejected-no-regularity,
`13292` SX predicted width sum.

## 2. THE HYPOTHESIS

**H0 (as p1falsifier left it).** No configuration in which age improves
correctness; scoped to a value-indexed store, frozen templates, <=1200 triples,
<=4 needs, one world, one gap.

**H1 (the overturn claim under test).** *The learner fails the spec-gap goal
because the substrate lacks a generalisation mechanism (p1falsifier cause (c)),
not because the derivation is unavailable. Give the substrate ONE additional
procedure family whose acceptance test and whose output both read the store,
and the learner answers spec-gap goals correctly from the store alone.*

**H2 (the falsifier of H1 that must also be reported).** *If the added rule
succeeds on derivable gaps AND answers confidently on non-derivable gaps, it is
an oracle, not a derivation, and H1 is void regardless of the score on
derivable gaps.*

## 3. THE NEW FAMILY RULE, SPECIFIED WITHOUT REFERENCE TO ANY TEST

Called family 3, `SX` (store-extrapolate). Given a need it first extracts the
`(relation, object)` pair the need names: `(f0,f1)` when `nf==2`; the pair of
the **unique** chain step whose subject field is `0` when `nf==1+ns*3` with
`ns>=1`; otherwise it refuses (a COUNT need names no object, so no object can
be predicted for it).

Then, reading **only the store**:

* **C0 present.** If the store already witnesses the pair for at least one
  subject, **REFUSE.** SX can never override present evidence. This makes SX a
  strict no-op on every need whose facts are present.
* **C1 prefix regularity.** For every witnessed `(r,o)` pair in the store, let
  `S(r,o)` be its witness subjects and `w=|S|`. Require `S = {m, m+1, ..., m+w-1}`
  with `m = min S`, for **every** witnessed pair. Any violation: REFUSE.
* **C2 band alignment.** Find the maximal run of *consecutive integer object
  ids* containing the target object `o`, expanded only through object ids that
  are witnessed in the store; call its ends `omin, omax`. Every witnessed pair
  whose object lies in `[omin,omax]` must share one constant `c = r - o`.
  Otherwise REFUSE.
* **C3 slot identity.** `k = o - omin` and `rbase = min` relation over that
  band; require `rbase + k == r`. Otherwise REFUSE (the two ids do not name the
  same slot of the band).
* **C4 subject base.** `b0 = min` subject over the target band's witnessed
  pairs. If the band has no witnessed pair, REFUSE.
* **C5 unanimous width.** Collect, over **every** witnessed pair `q` in the whole
  store whose own band is defined the same way and whose own minimum subject
  equals `b0` and whose own slot index equals `k`, the widths `w_q`. If the
  collection is empty, or the values are not all equal, **REFUSE.**
* **C6 prediction.** Otherwise predict the witness set
  `{b0, b0+1, ..., b0+W-1}` where `W` is the unanimous width, and CONSUME the
  need as family 3.

**Every clause is a statement about the store.** C1..C6 mention no world, no
stage, no relation id, no width, no count and no test.

**Why C1..C6 constitute a derivation and not a guess.** C5 is a
generalisation across bands: the answer for an absent pair is transferred from
structurally analogous present pairs, by slot index, within a subject band. It
can be wrong, and section 5 builds worlds where it is.

**Why SX is tried FIRST (order 3,0,1,2).** Because of C0: on any need whose
pair is witnessed, SX refuses immediately and families 0/1/2 bind exactly as
before. The order change is therefore behaviour-preserving except on precisely
the unwitnessed needs. Bar **E1** tests that empirically.

## 4. WORLDS

Six worlds. `W0` is the frozen canonical world W-LT3 (1068 triples, ten stages,
stage E a 600-fact distractor band), used so the overturn attempt is first made
on p1falsifier's own case. `W1..W5` are built by my own generator
`fr_world(w)`: stages share subject base 100, stage `s` owns relations
`1001+100s .. 1001+100s+KR-1` and objects `2001+100s .. 2001+100s+KR-1`, slot
`k` of stage `s` is the pair `(1001+100s+k, 2001+100s+k)` witnessed by a prefix
of the subject band of width `prof(w,k)`.

| world | NS | KR | profile | triples | purpose |
|---|---|---|---|---|---|
| `W0` | 10 | 10 | frozen 16,12,8,4,2x6, plus stage E band base 5000 width 60 | 1068 | continuity with p1falsifier's crux |
| `W1` | 10 | 10 | 16,12,8,4,2x6 | 520 | regular, nested |
| `W2` | 8 | 12 | 10,7,5,3,2x8 | 328 | regular, different size |
| `W3` | 6 | 8 | 12,12,12,12,2x4 | 336 | regular but NOT nested (C1 still holds, nesting not required) |
| `W4` | 10 | 10 | as W1 except stage 7 slot 2 has width 6 | 518 | **profile conflict**: C5 must fail |
| `W5` | 10 | 14 | W1 for k<10; stage 9 alone owns k=10..13 width 4 | 560 | **slot with no analogue**: C5's collection is empty |

A sixth construct, `WNP`, is not a world but a **variant flag**: it rewrites
every witness set so it is NOT a prefix (subjects `100,102,4,...`). C1 must
then fail everywhere and SX must refuse on every need in every case. This is the
negative control for the rule's own machinery: it must be possible for the rule
to say no.

## 5. GAP CONSTRUCTIONS

Seven, applied to every world (42 cases; `W0` uses the frozen `mkLT3_goal(5)`
for its middle/end shapes and the equivalent built goal elsewhere):

| id | construction | which relation absent | count missing | position | simult. gaps |
|---|---|---|---|---|---|
| `G1` | whole slot `k=2` of stage 2 deleted | one relation | all its triples | **middle** (need 2 only) | 1 |
| `G2` | whole slot `k=2` of stage 2 deleted, final need re-uses that slot | one relation | all | **end** (needs 2 and 3) | 1 |
| `G3` | whole slot `k=1` of stage 0 deleted | one relation | all | **first** (need 0 is the RETRIEVE) | 1 |
| `G4` | slots `k=1` of stage 1 and `k=2` of stage 2 deleted | two relations | all | middle+end | **2** |
| `G5` | last 3 triples of slot `k=2` of stage 2 deleted | one relation | **3 of 8** | middle | 1 |
| `G6` | 1 triple of slot `k=2` of stage 2 deleted | one relation | **1 of 8** | middle | 1 |
| `G7` | goal names a relation/object in **no band at all** | novel | all | middle | 1 |

`G5` and `G6` are the *partial* gaps: the pair is still witnessed, so C0 must
make SX refuse and the answer is the surviving witness set.

Additional **non-derivable** cases, appended:

| id | world | construction | why non-derivable |
|---|---|---|---|
| `N1` | `W5` | stage 9 slot 11 deleted | no other stage owns slot 11; C5's collection is empty |
| `N2` | `W4` | stage 2 slot 2 deleted | stage 7 slot 2 has width 6, stage 2 would have 8; unanimity fails |
| `N3` | any | goal names `(1999,2999)`, in no band | C2 finds no witnessed object run containing 2999 |

## 6. DERIVABILITY, DECLARED FROM THE WORLD, NOT FROM THE RULE

**H-REG (preregistered induction hypothesis, world level).** For all stages
`t` that share subject base `b` and own slot `k`, `width(t,k) = P_b(k)`.

A whole-slot deletion at `(s,k)` is **DERIVABLE** iff, after the deletion, the
remaining stages still determine `P_b(k)` unanimously, i.e. every remaining
stage sharing base `b` has the same width at `k`. Otherwise it is
**NON-DERIVABLE**.

Declared answer per case, three separate numbers, none of them chosen after
seeing a result:

* **`EXNG`** (strict): the answer equals `lt_oracle` over the **full
  pre-deletion arena** — mechanically computed, no hand table, no hand-declared
  constants. This is what the goal specifies.
* **`EXAB`** (abstention): the learner returned **code 0 (DECLINE)**. This is
  the declared correct behaviour for every NON-DERIVABLE case.
* **`FAITH`**: the answer equals `lt_oracle` over the **actual gap arena** —
  faithful execution of what the store supports, which is the metric p1falsifier
  showed can be 4/4 while the answer is wrong.

**H-REG is the same condition SX tests.** I say so plainly: success on
DERIVABLE cases is therefore expected by construction and is weak evidence.
The load-bearing measurement is bar **O1**, which is about NON-DERIVABLE cases.

## 7. ARMS

Six arms per case, one binary, one switch cell, identical bytes everywhere else.
State is reset to the post-lifetime snapshot before **every** query, so no case
can inherit another's bindings, plans or templates.

| arm | learner state | `L[13276]` SX | `LT[68]` rebuild |
|---|---|---|---|
| `AGED+SX` | post-lifetime | 1 | 1 |
| `AGED-SX` | post-lifetime | 0 | 1 |
| `COLD+SX` | all zero | 1 | 1 |
| `COLD-SX` | all zero | 0 | 1 |
| `AGEDSTL+SX` | post-lifetime | 1 | **0** |
| `AGEDSTL-SX` | post-lifetime | 0 | **0** |

`AGEDSTL*` is the stale-index condition: the freshness flag is off, so the
frozen `ret_spec/vfy_spec/cnt_spec` indices can address fact slots of triples
the arena no longer owns. **Stupid baselines, preregistered:**

* **`STUPID-CONST`** — the *constant* baseline: a rule that always answers the
  full band prefix `{100..115}` regardless of slot. Scored by the same three
  numbers on the same cases. If SX does not beat it, SX is worthless.
* **`STUPID-MODE`** — the *modal width* baseline: a rule that always answers the
  most frequent width observed in the store, ignoring slot index. If SX does not
  beat it, SX is doing slot-indexed transfer and not merely counting.
* **`STUPID-SXOFF`** — the frozen substrate, i.e. `AGED-SX`, as the
  "no new rule at all" baseline.

## 8. FROZEN KILL BARS

| id | bar | fail means |
|---|---|---|
| **E1** | with `L[13276]=0`, on the `W0`/`G1` case, `AGED-SX` reproduces p1falsifier's `exact`, `famv`, `ansn` and `reads` for `AGED_REB` on `GGAP` | my edit changed the frozen path; every `-SX` cell is void |
| **E2** | with `L[13276]=0`, `famv` is `0112` on `W0/G1` and identical to the `+SX` arm on every case whose needs are all witnessed | SX is not a strict fallback; it perturbs present-fact behaviour |
| **E3** | `SX consumed` count on `COLD-SX` is 0 for every case | the switch is not wired |
| **V0** | `lt_oracle` answers (does not decline) on the full arena for every case | declared answer unavailable; that case is VOID |
| **V1** | `EXNG`, `EXAB`, `FAITH` are identical on 3 deterministic permutations (reverse, stride-7, sort-by-relation) of the gap arena, for the `AGED+SX` arm | the metric is order-sensitive; VOID |
| **V2** | the goal record's named `(relation,object)` set equals the harness's declared gap set for every case | the gap is not the one declared; VOID |
| **O1** | **THE ORACLE CONTROL.** Over all NON-DERIVABLE cases, `SX+` has `EXAB=1` (code 0) in **every** case, and `EXNG=0` in every case. If `SX+` returns `EXNG=1` on ANY non-derivable case, the rule is an oracle | **H1 VOID**, the result is memorisation, and no positive may be claimed |
| **K1** | **`CRUX / H1`.** Over all DERIVABLE cases, `AGED+SX` `EXNG=1` in **every** case | H1 **REFUTED** on that subset; the scope of the negative is narrowed to whatever the failures are |
| **K2** | **`WITH/AGAINST`.** `AGED+SX` `EXNG` > `AGED-SX` `EXNG` on the DERIVABLE set, counted over the same cases | the rule is what helped; otherwise the substrate change bought nothing |
| **K3** | **`AGE`.** `AGED+SX` `EXNG` > `COLD+SX` `EXNG` | **H0 OVERTURNED**: a configuration in which age improves correctness. If `AGED+SX == COLD+SX`, H0 survives *with the new capability present*, which is a strictly stronger negative |
| **K4** | **`STUPID`.** `AGED+SX` `EXNG` > `STUPID-CONST` `EXNG` and > `STUPID-MODE` `EXNG` | the rule is doing something a constant or a count cannot |
| **K5** | **`STALE`.** on cases where the aged stale arm `EXNG=1`, at least one *witnessed* need in the same answer vector disagrees with `lt_oracle` over the same arena | the stale index cannot restore one relation without corrupting the rest; the hit is not a correctness improvement |
| **K6** | **`STALE-FRESH`.** the SX binding cached on a gap arena, reused after the relation is restored with a **non-prefix** witness set, answers differently from a learner with no cached SX binding | tests whether the new capability introduces a new staleness defect |
| **K7** | **LEAK.** every `-SX` cell has `preW=0` learner cells before its query and `rebuilds=0` for `COLD-SX` | contamination not eliminated; VOID |
| **K8** | **COST.** the 1068-episode setup cost of `AGED+SX` is reported against its correctness gain | reported, not a bar |
| **K9** | **DETERMINISM.** 3/3 byte-identical stdout from three watchdog runs; `tnn_pure_zag_report` = `PURE-ZAG-CLEAN` | required |

A bar that fails is reported as FAIL. **No bar moves after the fact.**

## 9. PREREGISTERED EXPECTATIONS

Stated so they cannot be adopted after the fact.

* `AGED-SX` / `COLD-SX` on `G1`/`G2`/`G3`/`G4` (whole-slot deletions): answer
  confidently, `FAITH=1`, `EXNG=0`, code 1. Expected.
* `AGED-SX` / `COLD-SX` on `G5`/`G6` (partial deletions): `FAITH=1` and
  `EXNG=1` **whenever the deleted triples are not load-bearing**, and `EXNG=0`
  when they are. Expected to be split.
* `AGED+SX` / `COLD+SX` on DERIVABLE whole-slot deletions: `EXNG=1`. Expected,
  and weak evidence by construction (section 6).
* `AGED+SX` on NON-DERIVABLE: `EXAB=1`. **This is the whole experiment.** The
  frozen substrate has never abstained once in this programme
  (p1falsifier: `ansn=5` at `reads=0` on an empty arena), so this is where the
  new rule is genuinely at risk.
* `K3` expected to FAIL, i.e. `AGED+SX == COLD+SX`: SX reads the store at bind
  time and its answer is a function of the store, so experience has nothing to
  add. If `K3` passes I will report it as the overturn of the central negative
  and spend the rest of the report on it.
* `K5` expected to PASS.

## 10. VERDICT RULE (frozen)

* **`H1 VOID (ORACLE)`** if `O1` fails.
* **`H1 CONFIRMED`** iff `O1` passes and `K1` passes.
* **`H0 OVERTURNED`** iff additionally `K3` passes.
* **`H0 NARROWED`** iff `O1` and `K1` and `K2` pass but `K3` fails: the
  capability was missing and adding it fixed correctness, but age still buys
  nothing. This is the expected outcome and it is a real narrowing, because
  cause (c) of p1falsifier's localisation is then confirmed as a substrate
  limitation rather than a fact about age.
* **`H0 SURVIVES`** iff `K1` fails.

## 11. EXECUTION

* Pure Zag for all computation; `. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`.
* `tools/zbuild.sh ./fr.zag` for every compile (removes any stale binary first).
* Every run through `tools/tnnwatch.sh reg familyrule 900 ./fr`. Limit 900 s,
  **frozen, never extended**. Timeout = FAIL.
* `_zag_print` single-buffer flush (brief 4.0/4.1: `_zag_raw_syscall` is inert on
  this host). Output asserted non-empty.
* `getc32`/`setc32` byte-offset wrappers, never `get32`/`set32` on odd offsets.
* No binary left unattended; `tnnwatch status` after every run.
* Explicit pathspecs, never `git commit -a`. PUSH after each step.