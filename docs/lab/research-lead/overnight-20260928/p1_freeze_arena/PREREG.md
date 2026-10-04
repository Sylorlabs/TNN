# PREREG: FREEZE-ARENA-1 (FA1) -- facts delivered ONLY through episodes

Branch: `lane/p1freeze`
Lane dir: `docs/lab/research-lead/overnight-20260928/p1_freeze_arena/`
Claim block: **C540-C559**. C377-C466 never minted.

Committed ALONE, before any implementation file exists in this lane.

Attacks: **C500-R1** (`lane/p1lifetime2`, commits df29e2b84 / 945ecb00a /
5e5ba93d5 / 368318d3a), certified verdict `LIFETIME-COST-ONLY`.

---

## 0. The negative result being attacked, verbatim from C500-R1

> "The lifetime does NOT beat a fresh learner on correctness, EVER. It beats
> fresh on COST 62x, and loses when the snapshot goes stale. Cheaper, staler,
> never smarter."

and its own localization of the cause:

> "TTC = 0 at every stage because the generic procedures read a live
> append-only arena. **Break the arena-is-the-answer confound.** Re-run with
> the arena *frozen* at stage entry and facts delivered only through episodes.
> That is the only configuration in which 'more intelligent with age' could
> differ from 'cheaper', and it is the experiment this whole line has been
> unable to run."

C500-R1 itself names the confound: in `lt_main.zag` the call order is
`w_stageX(A)` then `feed_stage(...)` then `mk_goal(...)` then
`lt_query(...)`. The whole stage's world is written into the arena `A` BEFORE
any episode of that stage and before the goal is posed, and the frozen
generic procedures `ret_gen / vfy_gen / cnt_gen` read `A` live. The learner
is handed the answer before being asked the question. The verdict may be
correct about the architecture and still be an artifact of the schedule.

## 1. THE QUESTION

Under the only configuration where competence is episode-gated, does
accumulated age make a LATER goal's answer **better** (intelligence), or only
cheaper (cost), or worse (interference / staleness)? Charter 24.

Preregistered answer is allowed to be negative. A failed bar is reported as a
failed bar. **No bar is moved after implementation.**

## 2. Design: two arms, ONE difference

Both arms run the identical world, the identical stage sequence, the identical
goal records, the identical episode stream (same count, same payloads, same
order), the identical declared answers, and the identical fresh-clone
baselines. They differ in exactly ONE line of control flow: whether the
stage's facts are written into the arena at stage entry.

| arm | arena writes | arena content at stage-s goal |
|---|---|---|
| **LIVE** (`frz=0`) | `frz_fill(A,s)` at stage entry, PLUS one append per episode (idempotent) | stages 0..s, all of them, **before any episode of s** |
| **FROZEN** (`frz=1`) | **one append per episode, and nothing else, ever** | stages 0..s, all of them, **only after s's last episode** |

So `LIVE` is "the same lifetime WITHOUT the freeze" and the comparison
isolates the schedule from the content, not from the stream.

Three invariants make that claim checkable rather than asserted, and they are
kill bars K4, K8, K9 below.

## 3. FROZEN implementation, and why there is no second channel

The only function in the whole program that writes the learner's arena is
`frz_add(A,s,r,o)` (append-if-absent). Its sole call site is inside
`frz_episode`, the single episode entry point, immediately BEFORE the frozen
`ret_episode / vfy_episode / cnt_episode` observation step that consumes the
same fact. `w_stageX` is not called anywhere in this lane's binaries except
inside `frz_fill`, which the LIVE arm calls and the FROZEN arm does not.

Episode k of stage s asserts exactly the k-th triple of stage s in the world's
own literal order, on modality `k mod 3`:

| k mod 3 | modality | payload | why |
|---|---|---|---|
| 0 | RETRIEVE (`ret_episode`) | (s,r,o) | "looked up (r,o), found s" |
| 1 | VERIFY (`vfy_episode`) | chain [(s,r,o)] | the explicit triple |
| 2 | COUNT (`cnt_episode`) | (s,r,o) | "counted s under r, one more: o" |

All three are sound reports of the same fact, so modality choice cannot change
whether the fact is knowable, only which coverage bucket receives the relation.
`k mod 3` is a fixed positional rule; it inspects no goal, no stage, no
relation. Over a stage of >= 3 facts every relation receives all three
modalities. **This is a new episode stream in BOTH arms**, so the LIVE/FROZEN
contrast is not contaminated by an episode-stream change.

Fact counts, from `w_stageX` as written in C500-R1's `lt_world.zag` and
cross-checked against the certified `STAGE ... facts=` log line:
A 52, B 27, C 28, D 39, E 200, F 14 (+2 in `w_stageF_ext`), G 28, H 26.
Total 414 + 2 = **416**, matching C500-R1's `EVT 1 8 416`.

The `w_stageF_ext` facts are delivered as the last two episodes of stage F,
AFTER F's goal has been answered and after the snapshot clone, so the
staleness probe (ABL-SNAPSTALE) keeps its meaning.

## 4. Frozen core, unchanged

Concatenated byte-identical, never edited:
`cogops_rescueaware/c15_base.zag` + `cogops_learnosc2/c8_learn.zag` (1331-line
frozen prefix, sha256[:12] `750cb01d086f`) + `hook_phase1/hq_module.zag`
(sha256[:12] `4200e21f`). No frozen function is edited. The additive lifetime
layer is a byte-identical copy of C500-R1's `lt_life.zag` except for
`lt_episode` -> `frz_episode` (documented in `NAMECHECK.md`). `lt_query` is
byte-identical, so every cost, reuse, coverage and revision number is
comparable with C500-R1.

**Anchor build.** `lt1.zag` is reassembled from the frozen prefix plus C500-R1's
`lt_world.zag`+`lt_life.zag`+`lt_main.zag` and must reproduce
`09a09548b2675f99e86260da96cb39d9d8f74ffc7ebe3e1b38a896d1e5f15296`
byte-for-byte. Verified in this lane before this prereg was written.

## 5. No labels, no feedback, no reset, no recompilation

One `L` (16384 B) + one `LT` (8192 B) per lifetime, allocated once in `main`,
threaded unchanged. `frz_episode(L,LT,A,K,kind,fs,fr,fo,RB,CB,TO,SE)` and
`lt_query(L,LT,A,G,K,R,ANS)` are the only two entry points. Neither receives a
stage id, a stage name, a goal tag, a cross-stage reference, a reuse hint, or
a correctness signal. `kind` is the modality channel the frozen core itself
requires. Verified by NAMECHECK grep and by the signatures. Output via
`_zag_print` on one formatted buffer; `_zag_raw_syscall` is never used for
output (it is inert on this host, brief section 4.0).

## 6. THE LEAK CONTROLS. This is the primary artifact.

A freeze that silently fails reproduces C500-R1's result for the wrong reason.
Seven controls, all evaluated in-Zag, all kill bars.

**LK1 -- arena purity at stage entry.** For each stage s, at the instant
immediately after stage s-1's last query and before stage s's first episode
and before stage s's goal is posed, count how many of stage s's `n_s` triples
are already present in the FROZEN arena. Frozen expectation **0** at all 8.

**LK2 -- learner-memory purity at stage entry.** At the same instant, scan
all 4096 i32 cells of `L` and all 2048 cells of `LT`; count cells whose value
is one of stage s's relation ids. Relation ids are stage-unique in this world
(101-107, 201-208, 301-304, 108-112, 500-509, 305, 601-604, 701-704, 104, 207,
202, 204, 206, 208, 703, 704). This is a byte-level test on the learner's own
memory, not on the harness. Frozen expectation **0** at all 8. The LIVE arm's
value at the same instant is reported for contrast.

**LK3 -- no-episode control (`NFEPS`).** Run the entire MAIN protocol with the
arena NEVER written by anything. Frozen expectation: no non-decline goal is
answered correctly. Any correct non-decline answer here would exhibit a second
leak channel. `nfe_ok` must be 0.

**LK4 -- channel invariant.** At 9 checkpoints (after each of the 8 stages and
after F's extension episodes), assert `get32(A,0) == number_of_episodes_
delivered_so_far`. Any prefill, any background writer, or any duplicated fact
breaks this. Frozen expectation: equality at all 9.

**LK5 -- arena equality across arms.** At the same 9 checkpoints, the FROZEN
arena and the LIVE arena must agree element-by-element on count and on every
(s,r,o). This is the content-isomorphism proof that makes the two arms
comparable. Frozen expectation: equality at all 9.

**LK6 -- TTC, the falsifier.** Examples-to-criterion per stage under both
arms. Under LIVE every stage must be 0 (C500-R1's result, re-derived). Under
FROZEN, stages whose goal depends on facts first delivered AT that stage
(A, B, C, D, F, G) must be > 0; stages E and H must be 0 and those zeros are
LEGITIMATE retention zeros (E's probe goal is stage A's goal, H's is F's, and
both stages' facts were fully delivered earlier). Frozen expectation:
LIVE `0 0 0 0 0 0 0 0`; FROZEN `>0 >0 >0 >0 0 >0 >0 0`.

**LK7 -- adversarial post-hoc sweep.** After the whole FROZEN lifetime, for
every stage s, assert that `L`'s three coverage arrays contain no relation id
belonging to a stage that had not yet been entered when the id was logged.
Simplified to the checkable form actually implemented: for each stage s, at
stage-s entry, no cell of `L` or `LT` holds a stage-s relation id (this is
LK2) AND no cell of the arena holds a stage-s triple (LK1). LK7 additionally
re-runs LK1/LK2 at the midpoint of each stage (after half the episodes) and
requires the partial count to be exactly `floor(n_s/2)` and 0 respectively:
partial delivery must be visible and strictly incomplete.

## 7. Arms, ablations, probes

Main protocol, identical in both arms (mirror of C500-R1's MAIN):

| stage | world | goal |
|---|---|---|
| A | procedural, 52 facts | GA = 3 needs |
| B | causal, 27 facts | GB = 2 needs |
| C | formal constraint, 28 facts | GC = 3 needs |
| D | misleading evidence, 39 facts | GD = 3 needs, then **re-probe GA** (interference) |
| E | distractor period, 200 facts | no goal; **re-probe GA** (retention through 200 distractors) |
| F | composition needing A-derived + F-local facts, 14 + 2 | GF, then clone, then 2 extension episodes |
| G | revision contradicting B, 28 facts | GG, then G-probe (needs B+C), then **re-probe GB** (forgetting) |
| H | invention pressure, 26 facts | HG (must decline), then **re-probe GA**, then **re-probe GF** |

Baseline/ablation set, run in BOTH arms at the F goal and (where meaningful) at
every stage goal:

| id | what it is |
|---|---|
| `LIFETIME` | the one persistent learner |
| `FRESH0` | learner cloned from the zero state, **zero episodes**, arena as the arm's arena is at that moment |
| `FRESHs` | learner cloned from the zero state, fed **only stage s's episodes** |
| `RECENCY16` | 16-fact sliding window over the arm's arena, refresh off |
| `ABL-NOSTRUCT` | clone of LIFETIME with template store and bind store zeroed (C500-R1's NOREUSE) |
| `ABL-SNAPSTALE` | clone of LIFETIME with the snapshot-refresh flag off |
| `ABL-SNAPCTRL` | clone of LIFETIME with refresh on (control for the above) |
| `ABL-NOFACT-A` | clone of LIFETIME, **every stage-A fact deleted from the arena**, query F |
| `ABL-NOFACT-C` | clone of LIFETIME, **every stage-C fact deleted from the arena**, query F |
| `NFEPS` | LK3 |

`FRESH0` in the LIVE arm is the row that reproduces C500-R1's central claim;
`FRESH0` in the FROZEN arm is the row that tests it.

## 8. Measurements, all required

1. examples-to-criterion per stage, both arms (TTC vector).
2. positive transfer: correctness of LIFETIME vs FRESH0 vs FRESHs vs RECENCY16, per stage, per arm.
3. negative transfer / interference: does stage D's misleading evidence damage GA? does G's revision damage GB? does 200 distractors damage GA? (`D-reprobe-A`, `E-reprobe-A`, `G-reprobe-B`, `H-retain-GA`)
4. forgetting: same three re-probes, plus `H-reprobe-GF`.
5. spontaneous reuse, **charter 25**: the learner must decide on its own that A's structure applies to F. Instrument: template built at A (`orgq=0`) fires at F; template assembled at F (`orgq=4`) fires at G and H (`rr=1`). No hint channel exists. Report `tmpl`, `orgq`, `xw`, `rr`, `bhit`, `bmiss`, `trials`, `pnew`, `pld`.
6. structure revision events: `rev` (index rebuilds), `fviol` (functional-arity violations), bind evictions, plan evictions, plan drops, declines, misbinds, capacity declines.
7. cost: fact-checks during plan execution and during family trials, per query and cumulative; episode cost.
8. memory: nonzero i32 cells in `L` and `LT` per stage.
9. For the F goal: the reuse ablation and the fact ablations, with the full answer vector printed, so the mechanism is localizable.

## 9. Preregistered predictions (all falsifiable, none movable)

| | prediction |
|---|---|
| **P1** | LIVE reproduces C500-R1: TTC `0` at all 8 stages; `FRESH0` answers F correctly; `LIFETIME` and `FRESH0` tie on correctness; lifetime beats fresh on cost. |
| **P2** | FROZEN TTC is `>0` at stages A,B,C,D,F,G and `0` at E,H (LK6). If any of the six is 0, the freeze failed at that stage and the whole FROZEN result is void. |
| **P3** | FROZEN `FRESH0` answers F **incorrectly**. This is the load-bearing prediction: with no experience the arena is empty and the A-derived needs cannot be satisfied. |
| **P4** | FROZEN `LIFETIME` answers F **correctly**, identically to LIVE `LIFETIME`, because the arena at F's goal is element-wise equal (LK5). So the freeze changes examples-to-criterion and the fresh-learner comparison, and changes nothing about the accumulated answer. |
| **P5** | Therefore FROZEN produces a strict correctness gap `LIFETIME > FRESH0` at F that LIVE does not. If that gap appears, "more capable with age" is TRUE under the freeze. |
| **P6** | `ABL-NOFACT-A` and `ABL-NOFACT-C` both make F wrong. Charter 18: the composed goal is causally dependent on A-era and C-era **facts**. Both branches are preregistered: if either ablation leaves F correct, the composition does not actually depend on that stage's facts and I report that instead. |
| **P7** | `ABL-NOSTRUCT` moves a cost quantity at F. Correctness is **not** predicted either way; both outcomes are preregistered and the mechanism is to be localized by printing the answer vector. C500-R1 observed `ok` flipping to 0, which would mean learner-owned structure is causally load-bearing for the composition, not merely a cost cache. |
| **P8** | FROZEN retains what C500-R1 retained: `fviol=1` raised at G's episodes from the contradiction of B's functional-arity rule, unprompted and before G's goal; `fviol=0` at H. |
| **P9** | FROZEN shows at least one spontaneous-reuse fire (`xw>=1` and `rr>=1`) with no hint, i.e. charter 25 survives the freeze. |
| **P10** | FROZEN costs MORE in aggregate than LIVE, because every stage's competence is now episode-gated and the `specialize_*` index rebuilds on far more queries. |
| **P11** | No negative-transfer regression is predicted from D, E or G: the re-probes stay correct. If any goes wrong, that is interference with age and is reported as a positive finding for the interference arm. |

## 10. Kill bars

| bar | requirement |
|---|---|
| **K1** | determinism: 3/3 **byte-identical** stdout for every binary, asserted by hash, not prose |
| **K2** | NON-EMPTY output: stdout byte count > 0 asserted in `run.sh`. (Brief section 4.0: a silent defect produced empty logs with rc=0 in earlier lanes.) |
| **K3** | oracle == declared for every goal in both arms, `orc=7/7` or better |
| **K4** | LK4 channel invariant holds at all 9 checkpoints in FROZEN |
| **K5** | LK1 arena purity == 0 at all 8 FROZEN stage entries |
| **K6** | LK2 learner-memory purity == 0 at all 8 FROZEN stage entries |
| **K7** | LK3 `nfe_ok == 0` |
| **K8** | LK5 arena equality LIVE == FROZEN at all 9 checkpoints |
| **K9** | frozen prefix sha256 == `043b62b427e97f0e5f59f8d0de9ec2b8cfa506ecf4b271d971cdfee07c1b177c`, and exactly one `fn main(` per translation unit |
| **K10** | namecheck: no stage id, stage name, declared answer, oracle call or goal tag appears in the learner-side files; `frz_episode` and `lt_query` are the only entry points and neither takes a stage selector or a correctness signal |
| **K11** | anchor build reproduces C500-R1's certified sha256 exactly |
| **K12** | LK7 midpoint check: partial count == floor(n_s/2) exactly at all 8 midpoints, and learner-memory purity still 0 |

If K4, K5, K6, K7, K8 or K12 fail, the freeze is declared BROKEN, no FROZEN
verdict is issued, and the failure is reported with the offending checkpoint.

## 11. Adjudication rule, fixed in advance

C500-R1 issued a mechanical prereg verdict and then overrode it. To avoid that,
the rule is fixed here:

* The mechanical verdict is the conjunction of K1-K12.
* The scientific verdict is a separate field, and it is **stated in words**
  from the measured table, not selected from a list of labels.

The scientific question is answered by one comparison, fixed here:

> Does FROZEN-LIFETIME answer the stage-F composition goal **correctly** while
> FROZEN-FRESH0 (identical arena-construction rule, zero episodes) answers it
> **incorrectly**?

YES => accumulated age improves correctness; the central C500-R1 negative does
not hold in the episode-gated configuration. NO => the negative result is not
an artifact of the append-only schedule, and P7/P6 plus the `ABL-NOSTRUCT`
answer vector are used to localize the limitation to the architecture.

Either way the report must ALSO answer, separately and without hedging:

> If the age-dependent correctness gap is real, is it attributable to
> accumulated **facts** in a learner-owned store, or to accumulated
> **structure** (templates, bindings, plans)?

The preregistered discriminator is `ABL-NOSTRUCT`: if clearing the learner-owned
structure leaves the answer unchanged, the gain is data; if it breaks the
answer, the gain is structure. Both outcomes are recorded.

## 12. Harder third lifetime (charter 221 continuation)

If and only if FA1 completes, build a third lifetime `LT3` on a harder world,
same two arms, same seven controls:

* 16 subjects per stage (not 8), 10 relation ids per stage
* SIX distinct goal shapes against the frozen 4-slot PLAN table, so table
  saturation is forced mid-lifetime
* a SECOND fan-in composition requiring a 3-stage join (A + C + F), so the
  composed goal cannot be satisfied by one prior stage
* a SECOND revision, at stage I, contradicting stage A's functional-arity rule
  as well as B's, so two arity violations must be detectable
* 600 distractor facts (not 200)
* a final stage J requiring reuse of a structure first ASSEMBLED at stage I

Frozen expectation for LT3: LIVE TTC still 0; FROZEN TTC > 0 at every
stage-local stage; the FROZEN correctness gap at the 3-stage join is at least
as large as at FA1's 2-stage join; plan-table saturation (4 slots, >= 5 shapes)
costs correctness in at least one arm.

## 13. Boundaries preregistered as expected (do not read as surprises)

* Nothing here clears the L3 bar. RETRIEVE / VERIFY / COUNT are
  researcher-frozen templates (C397). The learner-created objects are
  descriptive shape classes, a shape->tag memo, reusable plan templates, a
  functional-arity belief with revision, and a snapshot-freshness rule. Every
  one is enumerable from source.
* `try_family` decides family from field SHAPE alone and never consults the
  arena; `learn_bindings` memoizes a total function of shape. All "learning
  credit" for bindings is memoization.
* A correctness gain with age that is attributable to accumulated facts is
  **not** the same claim as "more intelligent". It is the weaker claim "the
  learner retains and can use what it has seen". Both are reported.
* One lifetime, one finite triple store, one subject population, no perception,
  no noise, no concept drift, no social input, every episode researcher-authored.
* Determinism is verified on ONE host and ONE compiler build
  (`znc 2026.07.0-dev`, macos-arm64).
* The compiler is SOUND for flat-arena indexed reads (C526/C527, 1928
  comparisons, 0 mismatches). No defect in this lane may be attributed to the
  compiler without a memory-free oracle. Known real toolchain traps used as
  defences: mandatory return type on `fn`, `if`-nesting <= 3, explicit `k*4`
  multipliers on every computed-offset i32 read, no `!` on compound `while`
  conditions, `[]u8 as *u8` forbidden.