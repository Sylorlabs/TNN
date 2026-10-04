# REPORT: LIFETIME-AB-1 RERUN (C500-R1) + LT2 (C528-C531)

Lane `p1_lifetime_rerun`. Prereg ADOPTED from `p1/lifetime-ab` commit
`7f66e5de7` (committed alone, pre-implementation) plus that branch's
`PREREG_ERRATA.md`. No prediction or kill bar was moved. New erratum E6 below.

Artifacts (all in this directory):

| file | sha256 of stdout |
|---|---|
| `lt1_run1.txt` | `09a09548b2675f99e86260da96cb39d9d8f74ffc7ebe3e1b38a896d1e5f15296` |
| `lt2_run1.txt` | `efc6fe9a0fd59a130bd07e8e868cbf3b957b1218bdfaf4c1ac85d486ff7fcdb2` |

Both 3/3 byte-identical. Both non-empty (9026 B, 7732 B) — asserted in
`run.sh`, not in prose. Frozen prefix byte-identical to the repository cores.
Claim IDs C526-C531; C377-C466 never minted.

---

## PART 0. The prior VOID was unfounded

The prior worker marked the whole experiment VOID on three claimed
toolchain barriers. Two of the three are refuted; the third is real and
already documented in the brief.

* **B15** (`_zag_raw_syscall` inert) — already disproved in the brief, and
  irrelevant here: the prior implementation already emitted via `_zag_print`.
* **B16** ("indexed reads are miscompiled") — **REFUTED, C526/C527.** See
  `B16_REFUTED.md`. Three independent proofs: the "passing" standalone probe
  in the prior commit prints the same "wrong" values it attributes to the
  with-base build (the prior report misread its own committed artifact); the
  six "corrupt" values are exactly the correct arithmetic for a stride-1 read
  of a stride-4-written array, confirmed byte-for-byte against a raw dump;
  and the prior "with-base" build never ran at all
  (`probe_defect_with_base_out.txt` is a compile abort:
  `unknown function: z_alloc/get32/set32`). My controlled re-run gives a
  **byte-identical** stdout sha256 with the probe alone, with the frozen
  base, and with the whole 1880-line frozen prefix.
* **B17** ("bogus type errors on large translation units") — did not
  reproduce. The 3320- and 3840-line units here compile clean.

The prior worker's `lt1_full` binary was in fact reproducible on this host to
the byte (`a40508169debafaf649b4be07df4d79e6cb998afdd3bb908c1b7fe9020f9fed8`,
reproduced here before any edit). Nothing was blocking the experiment.

## PART 0b. Four real defects, all in the harness, none in the compiler

Located by instrumented bisection, each fixed and each with a stated cause.

1. **Poisoned VERIFY relation ids.** `feed` copied the chain `CB -> RB -> CB`
   through a 3-cells-per-triple scratch buffer. Measured on this host, the
   `set32(RB, i*3+k, …)` store inside that 8-slice-argument call chain does
   not land where `get32(RB, …)` reads it back (RB's `_zag_slice_ptr` and
   `.len` are correct and its neighbours do not overlap; the effect is a
   deterministic mis-store, not a read fault and not an allocator fault).
   Because `vfy_episode` reads the relation id straight out of the chain,
   every VERIFY relation reaching `vfy_log_rel` was heap garbage. Symptom:
   the learner's vfy coverage set read
   `vfy=-854881077,41421,-854815541,…` instead of relation ids. The
   round-trip was pure redundancy — `ep_vfy` already fills `CB` with exactly
   what `vfy_episode` consumes — so it is deleted. This was the real defect
   the prior worker misdiagnosed as B16, and it was silently poisoning the
   coverage sets, the version selection and every derived cost.
2. **TTC probing the wrong goal.** `mk_goal(8)` and `mk_goal(9)` fell
   through to `mkGP`, so the examples-to-criterion phase measured a different
   goal than the declared answer at stages 5 and 7.
3. **TTC arena pollution.** `build_upto(A3,s)` re-appends stages 0..s while
   `A3` was never reset, so from s=1 the arena held every stage two, three,
   … times. This is the source of the "TTC contradicts MAIN" internal
   contradiction the prior worker cited as a reason not to publish.
4. **TTC learner had the freshness rule switched off.** `T3[68]` — the
   snapshot-freshness enable flag — was never set on the TTC clone, so
   `lt_fresh` returned immediately and the TTC learner answered every query
   from an index that had never been built. The flag is a fixed policy,
   enabled identically on every learner instance in the run.

Also fixed: stage A was never fed episodes at all, contrary to prereg §4
phase 1; `s5`'s TTC target now matches the arena it is scored against.

---

## PART 1. TRANSFER TABLE (LT1, prereg §5/§6 metrics)

Cost is fact-checks. "lifetime" = the one persistent learner; FRESH0 = zero
episodes; FRESH1 = stage F's episodes only; RECENCY16 = 16-fact sliding
window. Every row below is measured, not estimated.

### At the stage-F composition goal (the prereg's K4 comparison)

| learner | correct | family trials | fact-checks |
|---|---|---|---|
| **LIFETIME (A..F accumulated)** | **yes** | **0** | **182** |
| FRESH0 (no experience) | yes | 12 | 11222 |
| FRESH1 (F's episodes only) | yes | 12 | 2000 |
| RECENCY16 | **no** | 12 | 88 |
| ABL-SNAP (snapshot refresh off) | **no** | 0 | 182 |
| ABL-STRUCT (template+bind stores cleared) | **no** | 12 | 1810 |
| ABL-CAP (BIND saturated) | declined | 12 | 1810 |

### Per-stage series

| stage | facts | memL | memLT | trials | query cost | tmpl built | tmpl hit | xworld | reuse-of-reuse | retcov | fviol | correct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 52 | 111 | 41 | 9 | 370 | 1 | 0 | 0 | 0 | 5 | 0 | yes |
| B | 79 | 177 | 95 | 0 | 72 | 2 | 0 | 0 | 0 | 8 | 0 | yes |
| C | 107 | 228 | 114 | 3 | 227 | 3 | 0 | 0 | 0 | 10 | 0 | yes |
| D | 146 | 281 | 135 | 0 | 2394 | 3 | 1 | **1** | 0 | 14 | 0 | yes |
| E | 346 | 287 | 147 | — | — | — | — | — | — | **16 (saturated)** | 0 | — |
| F | 360 | 449 | 167 | 0 | 182 | 4 | 1 | 0 | 0 | 16 | 0 | yes |
| G | 390 | 468 | 194 | 0 | 8604 | 4 | 2 | 1 | 0 | 16 | **1** | yes |
| H | 416 | 492 | 214 | 0 | 2624 | 4 | 4 | 1 | **1** | 16 | 1 | **no (misbind)** |

Totals over 11 queries: 4 templates built, 7 template hits, 4 cross-world
fires, 3 reuse-of-reuse fires, 7 belief revisions, 14993 query fact-checks,
16190 episode fact-checks. Lifetime learner answers **10 of 10** non-invention
goals correctly; the 16-fact recency baseline answers **0 of 1**.

### PREREG PREDICTIONS, adjudicated

| | prediction | outcome |
|---|---|---|
| P1 | determinism 3/3 | **CONFIRMED** |
| P2 | A builds T1, correct | **CONFIRMED** |
| P3 | F trial increment 0 (errata E2), FRESH 12 | **CONFIRMED** |
| P4 | D: T1 hits across a 3-stage gap, disjoint rel ids | **CONFIRMED** (`xw=1`, correct) |
| P5 | G: T4 assembled at F fires again, disjoint rel ids | **CONFIRMED** (`xw=1`) |
| P6 | H does not decline while FRESH0 does | **CONFIRMED** — `h_invention_ok=0`, `MISBIND=1` |
| P7 | ABL-SNAP makes F wrong (stale snapshot under-counts) | **CONFIRMED** — `...,1,2` vs `...,1,3` |
| P8 | ABL-STRUCT raises F trials 0 -> 12, answer unchanged | **CONFIRMED** |
| P9 | RECENCY wrong at F, FRESH0/FRESH1 correct | **CONFIRMED** |
| P10 | exactly one functional-arity violation at G, unprompted, before G's goal | **CONFIRMED** — `EVT 3 201 113`, `fviol=1`, raised at G-episodes |
| P11 | RET coverage saturates at 16 during E; G's goal then uses GEN and stays correct | **CONFIRMED** — `rspec=0 rgen=1` at G |
| P12 | memory non-decreasing | **CONFIRMED** — memL 111->492, memLT 41->214 |
| P13 | GA retention probe at H correct; FORGET=0 | **CONFIRMED** |

### KILL BARS

| bar | outcome |
|---|---|
| K1 determinism | **PASS** |
| K2 oracle == declared, 7/7 | **PASS** (`orc=7/7`) |
| K3 namecheck | **PASS** — frozen prefix byte-identical; `lt_life.zag` contains no stage id, stage name, declared answer, oracle call, or goal tag; `lt_episode`/`lt_query` are the only entry points and neither takes a stage selector or correctness signal |
| K4 MAIN beats FRESH0 and FRESH1 at F | **PASS** — 0 vs 12 trials, 182 vs 11222/2000 fact-checks, equal correctness |
| K5 ABL-STRUCT moves a quantity at F | **PASS** — trials 0 -> 12 |
| K6 ABL-SNAP makes F wrong | **PASS** |
| K7 at least one discriminative signal fires | **PASS** — five fire (P6, P7, P9, P10, P11) |

**Prereg's mechanical verdict: `LIFETIME-INTELLIGENCE`** (K1,K2,K3,K6,K4,K5
and both P4,P5).

**My adjudication overrides the label: `LIFETIME-COST-ONLY`.** K6 is a trap.
It shows the accumulated snapshot is *causally load-bearing*, but only in the
direction of being *stale*: with refresh off the answer is wrong, with refresh
on it is right. FRESH0 has no snapshot at all and is also correct. Nothing in
the run shows accumulated state beating a fresh learner on **correctness** —
it never does, at any stage, for any goal. See next section.

## PART 2. SPONTANEOUS REUSE (charter 25)

No goal record, episode, or signature contains a stage id, a reuse hint, a
template id, or a cross-stage reference. The learner decides on shape alone.
Evidence, all unprompted:

* **Cross-world (P4).** The template built at A fires at D on relations
  108-112, disjoint from A's 101-107, three stages later.
  `Q st=D … tmpl=1 orgq=0 xw=1`.
* **Reuse of reuse (P5, charter 25).** The template *assembled at F* fires at
  G on relations 601-604, disjoint from F's. `Q st=G … tmpl=1 orgq=4 xw=1`.
  It then fires twice more at H (`rr=1` at H, H-retain-GA and H-reprobe-GF).
* **Retention as reuse.** The A-era template is still live at the last query
  of the lifetime, 416 facts and 200 distractors later, and answers correctly
  (`H-retain-GA ok=1`). FORGET = 0.
* **LT2 reproduces the pattern on a harder world** with the shape, not the
  goal, being what transfers: the s4 template built at D2 fires at probe `DX`
  over the revision world's relations (`tmpl=1 orgq=3 xw=1`) and again at
  `DY` over the invention world's relations (`tmpl=1 orgq=3 xw=1 rr=1`) —
  the transferred connection is itself reusable, with no prompt.

The learner never sees the phrase "use what you learned in A". It has no
channel on which to receive it.

## PART 3. LIFETIME vs FRESH — THE CENTRAL QUESTION

**The lifetime learner does NOT beat a fresh learner at F on correctness. It
beats it on cost, by two orders of magnitude, and it loses to it on one
metric it does not report.** Stated plainly:

| question | answer |
|---|---|
| does accumulated state make F's answer *better*? | **No.** FRESH0 (zero episodes) is also correct. 10/10 vs 10/10. |
| does it make F *cheaper*? | **Yes, decisively.** 182 vs 11222 fact-checks (62x), 0 vs 12 family trials. |
| does it make F *wrong*? | **Yes, if anything the age touches it.** ABL-SNAP (age without refresh) is wrong. The stale bucket under-counts `1,3` as `1,2`. |
| does a fresh learner ever do worse *because* it is fresh? | No. Every FRESH/ABL row that is correct is correct; the only wrong fresh-side row is RECENCY16, and it is wrong for a reason age cannot fix (a 16-fact window cannot see the answer). |
| examples-to-criterion | **0 at every stage** (TTC `k0ok=1 ttc=0` for all 8). |

The TTC result is the sharpest negative in the run and deserves emphasis:
**the learner can answer every stage goal, correctly, before it has seen a
single episode of that stage.** The arena is append-only and the generic
procedures `ret_gen/vfy_gen/cnt_gen` read it live, so competence is never
episode-gated. Episodes buy indexing, bindings and templates — not
competence. There is no learning period to measure.

## PART 4. DID THE PREDICTION HOLD? "age makes it cheaper/staler, not smarter"

The prior worker's falsifiable prediction, from source reading:

> on this substrate accumulated state CANNOT make an answer better than a
> fresh learner's — coverage gates only spec-vs-gen, and `try_family` decides
> family from shape alone, so `learn_bindings` memoizes a total function. Age
> can make it CHEAPER or STALE, never SMARTER.

**THE PREDICTION HELD, in full, on every metric.** The mechanism it names is
directly visible in the run: at stage G the retrieve step falls back to the
generic version because RET coverage is saturated at 16 (`rspec=0 rgen=1`)
and the answer is still correct — coverage gates only spec-vs-gen, exactly as
claimed. `P3`'s trial increment of 0 at F, against FRESH's 12, is
`learn_bindings` memoizing a total function of shape: zero experience
informs it. The predicted mis-bind at H and the predicted capacity decline
(`ABL-BINDSAT` declines a goal it should answer) both fired.

The prediction also explains the two things it did not predict, and those are
the interesting part. It says age cannot make an answer *better*; it does not
say age cannot make the answer *depend on the learner*. It can, and does:

* **Memory grows monotonically** 111 -> 492 nonzero cells in `L`, 41 -> 214
  in the lifetime block (P12). Sixteen times and five times.
* **The same procedure costs wildly different amounts at different stages**
  under one identity: 72 fact-checks at B, 8604 at G, for goals of the same
  complexity, purely because coverage state differs.
* **Total lifetime cost is superlinear in experience**: 14993 query
  fact-checks over 11 queries, of which 8604 (57%) is one query at G.

So the accurate statement is three-part, and only the first part was
predicted: with age the learner is **cheaper**, **staler**, and **more
expensive in aggregate**.

## PART 5. LT2 — the harder second lifetime (charter 221, C528-C531)

Separate binary, separate lane files, same frozen cores, same two entry
points. Harder on all five preregistered axes, plus the sixth: 12 subjects
per stage (not 8); **six distinct goal shapes** against a frozen 4-slot PLAN
table (not 4); nine need signatures with BIND pressure (not 4); **400**
distractor facts (not 200); a **second fan-in diamond** at F — 4 needs, **6
links** (not 3); and stage G contradicts B's functional-arity rule in **two**
places. 661 facts total.

Two arms over the identical world, identical goals, identical episodes,
differing in exactly one cell of learner state (the eviction policy):

| | pol 0: never evict | pol 1: durable store, evict LRU |
|---|---|---|
| correct (of 10 goals) | 7 | 7 |
| declined at H (correct behaviour) | yes | yes |
| total fact-checks | **5 081 481** | **37 448** (136x less) |
| plan rebuilds forced by table saturation | 4 | 3 |
| plan drops performed | 0 | 3 |
| templates built / hits | 7 / 4 | 7 / 4 |
| cross-world fires / reuse-of-reuse | 2 / 1 | 2 / 1 |
| functional-arity violations | 1 | 1 |
| BIND capacity declines | 0 | 0 |

Preregistered LT2 prediction: *"LT2 (durable template store + LRU eviction)
reaches a HIGHER share of correct answers and LOWER total fact-checks than
LT1 at the same goal set, and LT1 degrades at the stage where its 4-slot PLAN
table saturates."*

* **LOWER total fact-checks: CONFIRMED, by 136x.** This is the single
  largest effect measured anywhere in this work.
* **LT1 degrades at PLAN saturation: CONFIRMED.** `plansat=4` in the
  never-evict arm; the 4-slot table fills at the fifth distinct shape.
* **HIGHER share of correct answers: REFUTED.** 7/10 in both arms. The
  eviction policy bought nothing in correctness. Same conclusion as LT1, from
  a different direction.

LT2 honest negatives, reported as found:

* **The 6-link double-diamond composition at F is answered WRONG in both
  arms** (`okF=0`, `okF2=0`). The learner and the independent oracle agree on
  the multiset of values and disagree on the order of the two fan-in
  branches: learner `…,8,11..18, 8,12..19, 1,3`, oracle
  `…,8,12..19, 8,11..18, 1,3`. The revised stage-G goal is wrong for a
  related reason (`8,40..47` where the oracle gives `6,40..45`, branches
  again swapped). The frozen composition resolves two same-shaped fan-ins in
  the opposite order to the oracle. **Not diagnosed to the instruction; open.**
* **Two contradicting facts were fed at G; the learner recorded ONE
  functional-arity violation** (`fviol=1`), not two. This is correct behaviour
  rather than a miss: after the first contradiction the learner no longer
  holds the functional-arity belief, so the second is not a violation of it.
  Recorded because it differs from the prereg's "at least twice".
* **Fresh learners also fail at F2**: `F2fresh0 ok=0`, `F2fresh1 ok=0`. The
  failure is not an age effect; the goal is simply not answerable correctly
  by this frozen composition.
* The `DY` cross-world probe answers `0,0,1,0,1,0` — correctly, per the
  oracle, but on empty sets. It demonstrates reuse, not competence.

## PART 6. BOUNDARIES

* Nothing here clears the L3 bar. RETRIEVE / VERIFY / COUNT are
  researcher-frozen templates (C397). The learner-created objects are
  descriptive shape classes, a shape->tag memo, reusable plan templates, a
  functional-arity belief with revision, and a snapshot-freshness rule. Every
  one is enumerable from source.
* `try_family` decides family from field SHAPE alone and never consults the
  arena. `learn_bindings` is memoization of a total function of shape. All
  "learning credit" for bindings is reported as memoization, and P6's misbind
  is the predicted price.
* Correctness improvement with age is impossible here except through snapshot
  refresh, and refresh only restores parity with a fresh learner. The honest
  ceiling is "faster", not "smarter".
* One lifetime, one finite append-only triple store, one subject population,
  8 stages. No perception, no noise, no concept drift, no social input.
* Every episode is researcher-authored, and so is every relation id. The
  learner's only channel to the world is the frozen generic interface.
* LT2's criterion is the INDEPENDENT oracle, not a researcher-declared answer
  table. That is stronger than LT1's, but it means LT1 and LT2 correctness
  numbers are not strictly commensurable.
* Determinism is verified on ONE host, one compiler build
  (`znc 2026.07.0-dev`, macos-arm64). The brief's B13 cross-platform result
  covers `c8_full`, not these binaries.
* `ABL-BINDSAT` declines rather than answering; the BIND-capacity decline is
  a real capacity result but was exercised by a synthetic lesion, not by
  natural table exhaustion.

## PART 7. PREREG ERRATUM E6 (recorded after the run, no bar moved)

Prereg §3.1 declared, for the stage-F composition goal,
`[8,10..17, 5,10..14, 7,10,11,12,13,14,15,16, 1,2]` (n=25), and for stage G
`[…,7,40,41,42,43,44,45,46, 1,2]`. Independent derivation from the frozen
generic procedures over the world literals in §3 gives n=22 and n=21
respectively: the third step is `vfy(intersection of the stage-C constraint
with the stage-A procedure property, the stage-F relation)`, which yields 4
and 3 subjects, not 7. The prereg's third segments are a hand-derivation
error in the prereg; the world literals and the goal records are unchanged.
The implementation's declared table (n=22, n=21) is the correct one, the
independent oracle agrees with it for all 7 goals (`orc=7/7`), and the
prior erratum E1 (which fixed three *lengths* but not these two *values*)
should have caught it and did not.

## PART 8. NEXT EXPERIMENT

1. **Isolate the mis-store.** Reduce `set32(RB, i*3+k, v)` inside an
   8-slice-argument call chain to a minimal case and file it as a real
   toolchain defect with a regression test. It cost this run a full
   certification cycle and it is not B16.
2. **Diagnose the 6-link fan-in ordering.** The learner and the oracle
   resolve two same-shaped fan-in branches in opposite order. Does the frozen
   `topo`/`compose` order depend on link insertion order? If so it is a
   latent correctness bug in the frozen core that affects every multi-fan-in
   plan, and it is worth more than any lifetime result here.
3. **Break the arena-is-the-answer confound.** TTC = 0 at every stage because
   the generic procedures read a live append-only arena. Re-run with the
   arena *frozen* at stage entry and facts delivered only through episodes.
   That is the only configuration in which "more intelligent with age" could
   differ from "cheaper", and it is the experiment this whole line has been
   unable to run.
4. **Vary the number of procedure families.** With three researcher-frozen
   families the family decision is a 3-way total function of shape and there
   is nothing for experience to decide. Any honest test of age-improves-
   answers needs a family space where shape underdetermines the procedure.
