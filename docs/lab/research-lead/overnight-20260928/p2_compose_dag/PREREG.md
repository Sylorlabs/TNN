# PREREG — COMPOSE-DAG (P2)

Worker: composition-p2. Date: 2026-10-03. Branch: `p2/compose-dag`.
Owned path: `docs/lab/research-lead/overnight-20260928/p2_compose_dag/`.
Governs: this file, `NAMECHECK.md`, `BASELINE-FROZEN.md`, committed ALONE
before any new engine source exists.

## 0. Disclosure of ordering

`BASELINE-FROZEN.md` measures the FROZEN object (byte-identical
`c8_learn.zag`). That is characterisation of the baseline, not
implementation of the hypothesis. Every kill bar in Section 9 that
constrains the NEW engine (`p2_learn.zag`) was written before `p2_learn.zag`
existed and is frozen here.

## 1. Substrate

Frozen COGOPS composition core, digest-pinned (`750cb01d086f…`): goal-record
parser, per-need binding by accepted shape, Kahn ordering, scalar / set /
aggregate link application, procedure-version selection from learned
coverage, plan table, change-driven iterated execution.

Three researcher-supplied generic procedures, unchanged:
`ret_gen` (RETRIEVE), `vfy_gen` (VERIFY), `cnt_gen` (distinct-object
COUNT). Capacity of `ret_gen` output is 32 values; `cnt_gen` distinct-set
capacity is 64.

Goal record `G`: `[goal_tag, nneeds, needs..., nlinks, links...]`, a need
is `[need_tag, nfields, fields...]`, a link is 28 bytes
`[kind, dst_need, dst_kind, dst_slot, src_need, src_kind, src_slot]`,
`src_kind` 0 = constructed field, 1 = produced record. Link kinds in the
frozen vocabulary: 1 = carry one scalar, 2 = feed a producer's record as
the receiving need's operand set, 3 = accumulate producers' records into
the receiver's operand set. No new link kind is introduced by this lane.

## 2. Capacity: the frozen dimension and the replacement discipline

The frozen arena hard-codes 4 needs. This lane uses the **GEN-REDIM
discipline** (C429/C434) as the replacement, not the old arena:
per-need regions are placed by exact size chaining from a declared
capacity `NM`, every stride and base is computed from `NM` by an
accessor, and no per-need count appears as a literal anywhere in the
cognition source.

Declared capacity for this lane: `NM = 24`, `NPLAN = 24`, `NBIND = 32`,
`PCAP = 64`. Every frozen 4-need literal is replaced by an accessor of
these. `NM = 24` is chosen because the deepest preregistered goal has 20
needs and 24 gives one slot of headroom; it is not tuned to any result.

Explicitly NOT done: no raising of a single constant to "just enough".

## 3. Hypothesis

**H-CAP.** The frozen generic composer is *topology-general but
capacity-bound*. The only structural invariant it violates beyond `NM = 4`
is the absence of a capacity parameter. If the arena is re-dimensioned by
the Section-2 discipline, every preregistered topology composes correctly
at `NM = 24` with **no change to any decision rule**.

**H-OP.** The operand set of a receiving need is the union, in
goal-record link order, over **all** incoming set-consuming links of the
values those producers actually produced, deduplicated with
first-occurrence order. (Frozen: first source only.)

**H-PROD.** A scalar-carrying link fires only when its source produced at
least one value. (Frozen: only on the iterated entry point.)

**H-ADM.** A link is admissible iff both endpoints' accepted shapes have a
compatible operand: a set-consuming link requires a set-valued producer
and a receiver with a set-shaped operand; an unsatisfied requirement makes
the goal REFUSED (declined), never a silently wrong number.

**H-CAN.** The answer's record sequence is emitted in a canonical order,
independent of the stored plan order.

Falsifier for the whole hypothesis: if re-dimensioning alone (no rule
change) already produces the adapt reading at ids 9/17, then H-OP/H-ADM
are false and the frozen limitation is not structural.

## 4. Metrics, fixed now

`k` = the frozen fact-check counter (`K[0]`), the substrate's own cost
instrument; the only deterministic cost measure available because
`_zag_raw_syscall` is ENOSYS here so no clock is readable from inside the
binary. Process wall time is reported by the shell as a secondary,
non-deterministic figure.

`dig` = `sum over records of (1002 * record_length + sum(record_contents))`.

Plan order, per-need `(index, length, contents_sum)`, `r` (0 declined /
1 plan loaded / 2 plan built), pass count, and the frozen stats block
(`plans_built`, `plans_loaded`, `trials`, `declines`) are reported for
every query.

## 5. Goals (all literals in `p2_world.zag`; ids are opaque)

| id | goal | nn | links | structural reading |
|----|------|----|-------|--------------------|
| 1 | g901 | 2 | 1 | two needs, second operand carried from the first |
| 2 | g902 | 3 | 2 | three needs, two carries |
| 6 | g906 | 3 | 2 | two producers, one accumulator fed by both |
| 7 | gbro k=3 | 5 | 6 | one producer, three receivers, one accumulator over the three |
| 8 | gbro k=2 | 4 | 4 | as 7 with two receivers |
| 9 | g909 | 4 | 4 | ONE receiver fed by TWO producers, one accumulator |
| 10 | g910 | 2 | 1 | scalar carry out of a producer that produced nothing |
| 11 | g911 | 2 | 1 | set link out of a scalar producer |
| 12 | g912 | 10 | 8 | ten needs: three roots, chain of 3 carries, three receivers, two accumulators |
| 13 | g913 | 6 | 5 | longest link path 3; one accumulator with two producers |
| 14 | g914 | 3 | 2 | contains a 3-field need no procedure accepts |
| 15 | g915 | 3 | 2 | contains a 3-field need with an unaccepted 2nd field |
| 16 | g916 | 1 | 0 | contains a 5-field need |
| 17 | g917 | 3 | 2 | set link into a need with no set-shaped operand |
| 18 | g918 | 2 | 1 | one producer inside the learned index, one outside |
| 19 | g919 | 3 | 2 | a need carrying from its own produced record |
| 20 | gseq d=2 | 2 | 1 | depth curve point |
| 21 | gseq d=3 | 3 | 2 | depth curve point |
| 22 | gseq d=5 | 5 | 4 | depth curve point |
| 23 | gseq d=10 | 10 | 9 | depth curve point |
| 24 | gseq d=20 | 20 | 19 | depth curve point |

## 6. Preregistered expected values, by hand

Digest arithmetic: `1002*len + sum`. World derivations are in
`p2_world.zag`; the key sets are
`R901(1000+i) = {1001+i}` (i = 0..19),
`R902(3000+i) = {1000+i}` (i = 0..20),
`R903({1000..1019})` = 40 distinct objects, `R903({1100..1105})` = 12
with disjoint object ranges so 26 subjects give 52,
`R905(7000)` = 26 subjects, `R906(9000+i)` = `{1000+i}` (i = 0..7),
`R911(7000)` = 6 subjects `{1100..1105}`, `R912(7000)` = 20 subjects
`{1000..1019}`, `R913(7300+i)` = `{1200+i}`.

**Strict reading** = frozen semantics: carries always fire; a set link
uses the first matching producer only, an aggregate link concatenates all
without dedup; no type admission.

**Adapt reading** = H-OP + H-PROD + H-ADM.

| id | strict per-need (len,sum) | strict dig | adapt per-need (len,sum) | adapt dig | adapt refuses? |
|----|--------------------------|-----------|-------------------------|-----------|----------------|
| 1 | (1,1001)(1,1002) | 4007 | same | 4007 | no |
| 2 | (1,1001)(1,1002)(1,1003) | 6012 | same | 6012 | no |
| 6 | (20,20190)(1,1000)(1,40) | 43274 | same | 43274 | no |
| 7 | (20,20190)(1,1000)(1,1001)(1,1002)(1,6) | 54542 | same | 54542 | no |
| 8 | (20,20190)(1,1000)(1,1001)(1,4) | 44238 | same | 44238 | no |
| 9 | (20,20190)(6,6615)(20,20190)(1,40) | 94129 | (20,20190)(6,6615)(26,26805)(1,52) | **106768** | no |
| 10 | (0,0)(0,0) | 0 | (0,0)(1,1001) | **2003** | no |
| 11 | (1,2)(0,0) | 1004 | same | 1004 | **YES (producer scalar)** |
| 12 | (1,1001)(1,1002)(1,1003)(1,1000)(1,1002)(1,1000)(1,1001)(1,6)(20,20190)(1,20) | 145077 | same | 145077 | no |
| 13 | (20,20190)(1,1000)(1,1000)(1,1001)(1,4)(1,20) | 74661 | same | 74661 | no |
| 14 | — | — | — | — | **YES (need 1 unbindable)** |
| 15 | — | — | — | — | **YES (need 2 unbindable)** |
| 16 | — | — | — | — | **YES (need 0 unbindable)** |
| 17 | (20,20190)(0,0)(1,0) | 41232 | — | — | **YES (receiver has no set operand)** |
| 18 | (20,20190)(0,0) | 40230 | same | 40230 | no |
| 19 | iteration, see bar X6 | — | — | — | no |
| 20-24 | d records of (1, 1000+i) | `2004+2000*d` | same | same | no |

Verification arithmetic for the derived numbers:
`2004+2000d`: d=2 → 6006… but the table entries above for ids 1 and 2 are
4007 and 6012 because ids 1 and 2 are hand-built, not `gseq`. For `gseq`
the records are `{1001+i}` for i = 0..d-1, sums `d*1001 + d(d-1)/2`, so
`dig = 1002*d + d*1001 + d(d-1)/2`. d=2 → 2004+2002+1 = 4007. d=3 →
3006+3003+3 = 6012. d=5 → 5010+5005+10 = 10025. d=10 → 10020+10010+45 =
20075. d=20 → 20040+20020+190 = 40250.

Correcting the table: **id20 4007, id21 6012, id22 10025, id23 20075,
id24 40250**, identical under both readings (a chain of carries has
exactly one producer per receiver and every producer is set-valued and
produces).

**Bar X1 (per-need vector).** For every id, the engine's per-need
`(len, sum)` vector, after canonical emission, equals the table's vector
for its arm, byte for byte on the printed line.

**Bar X2 (independence).** For every id, the engine's answer equals the
independent reference under the SAME reading, element for element.

**Bar X3 (refusal).** Ids 11, 14, 15, 16, 17 return `r = 0` under the
adapt arm and increment `declines`. Ids 1,2,6,7,8,9,10,12,13,18,20-24
return `r in {1,2}` and do not increment `declines` beyond id 16's.

**Bar X4 (capacity).** Id 12 (nn=10) and id 24 (nn=20) compose correctly.
Ids 22, 23, 24 also satisfy Bar X1.

**Bar X5 (canonical emission).** Two goals with identical per-need results
and different stored plan orders emit identical canonical vectors. Falsify
if the emission order still tracks the plan order.

**Bar X6 (iteration).** Id 19 halts and reports pass count `>= 1`; with the
frozen pass cap 16 the walk is truncated, and with a capacity-parameterised
pass cap of 64 the same goal reaches its quiescent fixed point and reports
`passes = 22`. Preregistered: the new engine exposes the pass cap as a
parameter and reports the value it used.

**Bar X7 (inertness).** The re-dimensioned engine, run on the frozen COGOPS
battery's own goals (`../cogops_learnosc2/c8_world.zag` goal
constructors) with `NM = 24`, reproduces the frozen lane's `dig` for
those goals and the frozen pass count for the cyclic one.

## 7. Levels, scored separately, never collapsed

**Level 1 — exact reuse.** A stored plan is found by goal tag and
executed with no re-derivation. Measured by `plans_loaded` and by
`trials` not increasing.

**Level 2 — adaptive reuse.** Each variant is tested by an explicit
mutation and must produce the correct new answer:

| variant | mutation | must hold |
|---------|----------|-----------|
| extended | same tag, more needs (id 12 re-presented as id 22) | correct |
| truncated | same tag, fewer needs | correct |
| substituted | same tag/shape, different relations and objects (ids 1 → 2 → 18) | correct |
| rebound | same tag, one constructed field re-pointed by a link | correct |
| specialized | procedure version 2 chosen because the relation is inside the learned index (id 18 need 0) | `k` strictly less than the generic-only run |
| interface-adapted | a link whose source produced nothing (id 10); a refused link (ids 11, 17) | correct / declined |
| combined | all of the above inside one 10-need goal (id 12) | correct |

**Level 3 — novel intermediate form.** Requires that a new intermediate
FORM was created, and that the form is not enumerable from the frozen
source. The frozen repertoire is three researcher-written procedures with
three accepted shapes and three link kinds. Preregistered expectation: the
learner binds by shape and can invent nothing, so ids 14, 15, 16 decline
and **L3 = 0**. This lane will NOT author a new procedure or need shape to
make L3 non-zero; doing so would be L1/L2 work by a researcher (brief S9,
charter 17). If the learner declines all three, L3 is reported as FAIL and
the missing form is named in Section 12.

## 8. Causality (charter 18)

For the composed structure Z of id 12 (10 needs) with component parts X
and Y chosen by disjoint need sets, and for the cost instrument `k`:

**A1 — single-cell lesion on one plan step's family cell.** Held constant:
facts, world, goal record, all procedure indices, all bindings, all other
plan steps, all other plans, all stats. Mutated: exactly one i32 in the
plan table. Prediction: that step produces no record; every step
downstream of it in the link graph produces no record; `dig` changes; the
steps not downstream are byte-identical.

**A2 — same lesion on a different step**, held constant identically.
Prediction: a different, non-overlapping `dig` change. If A1 and A2 give
the same `dig`, the ablation is confounded and the bar fails.

**A3 — index-coverage lesion (cost causality).** Held constant as in A1,
mutated: the retrieve coverage word only. Prediction: every affected step
drops from version 2 to version 0, answers are **unchanged**, and `k`
strictly increases. This is the sharpest test of whether specialisation
is causally load-bearing.

**A4 — both lesions.** Prediction: `k(A3+A1) >= k(A3)`.

**A5 — fresh learner.** Same world, same goal, zeroed learner state.
Prediction: `trials` > 0, `plans_built` increments, and `k` is not lower
than the warm `k`. Reported, not asserted as a bar.

**A6 — persistence and reuse.** The same tag re-presented. Prediction:
`plans_loaded` increments, `dig` identical, `trials` unchanged.

**A7 — revisability.** `plan_drop(tag)`, re-present. Prediction:
`plans_built` increments, `dig` identical. Then, with one constructed
field changed, Prediction: the re-presented answer reflects the new field
(the plan is a skeleton, not a memorised answer).

**Ablation validity statement (required by the brief).** Every lesion is a
single-word or single-cell write into one arena, applied immediately
before exactly one query, with the query's world, goal record and every
other arena byte unchanged. `build.sh` re-runs the unlesioned stage in the
same binary, in the same order, and the lesioned stage's inputs are
printed on the same line so a reviewer can confirm the goal record digest
and fact count are identical between the two.

**Caveat on binding causality — preregistered negative expectation.** The
frozen `learn_bindings` accepts a need on SHAPE alone. Zeroing a binding's
family cell does not cause a decline; the next query re-derives the same
family from the shape. Preregistered: ablating a binding cell does NOT
break composition. This is reported as a NEGATIVE causality result: the
plan's per-step family is a *record*, not a *cause*, except that A1 shows
it is load-bearing at execution time. The genuinely evidence-driven part
is version selection (A3).

## 9. Baselines (charter 79) — preregistered, including the prediction
that one of them WINS

**B0 MEMO.** Table of goal tag → answer, filled on first call. No
planning at all. Preregistered: B0 wins on raw `k` for a repeated tag
(it does zero work on the second call), and loses on ids 1 vs 2, 18, and
20-24 (same tag, changed fields), which it answers from a stale record.
Preregistered prediction: **B0 wins the cost comparison and loses the
generalisation comparison; both are reported; no flattening.**

**B1 EXHAUST.** Enumerate every ordering of the needs and every assignment
of a procedure to each need, execute each with the generic-only executor,
compare against the preregistered answer, count trials. Trial count is
`n! * 3^n`. Preregistered: 24 (n=2), 162 (n=3), 5832 (n=4), 29160 (n=5),
524880 (n=6), then > 1.1e7 at n=7. Bar: B1 must complete n <= 5 within
the trial cap and must be reported as INFEASIBLE for the 10-need goal
from the closed form alone, with the n=6 measurement as the last feasible
point. The composer must solve the 10-need goal with a trial count equal
to its `trials` counter (<= 4*n) — i.e. it must be at least 3 orders of
magnitude cheaper in trials.

**B2 LINEAR.** The same engine with every version forced to the generic
procedure (no learned index). Bar: the warm engine must achieve strictly
lower `k` than B2 on at least ids 6, 7, 8, 12, 13 and must match answers.

## 10. Depth and latency

Depth points 2, 3, 5, 10, 20 (ids 20-24), plus the structural depths of
ids 7 (2), 12 (3), 13 (3). Report `dig`, `k`, `trials`, and process wall
time for each. Preregistered expectation: `k` grows **linearly** in depth
under the specialised path because each step reads a bounded index bucket,
and **superlinearly** under B2 because each step scans all facts. The
composition must not degrade superlinearly. Report the measured ratios.

## 11. Determinism and purity

3/3 byte-identical stdout for every binary. One `fn main` per binary. No
interpreter. All dynamic output through one preallocated buffer and one
`_zag_print`.

## 12. Kill bars, frozen

| id | bar |
|----|-----|
| C1 | PREREG.md + NAMECHECK.md + BASELINE-FROZEN.md + frozen-arm artifacts committed ALONE, strictly before any `p2_learn.zag` |
| C2 | `p2_base + ref/c8_world + ref/c8_learn + ref/c8_main` reproduces `../cogops_learnosc2/c8_run1.txt` byte-identically |
| C3 | `cmp` of all four `ref/c8_*.zag` against `../cogops_learnosc2/` |
| C4 | 3/3 byte-identical stdout, empty stderr, for every binary |
| C5 | exactly one `fn main(` per binary |
| C6 | no per-need count literal in `p2_learn.zag`; all strides from `NM` |
| C7 | Bars X1..X7 hold, or the specific failure is reported as a failure with no bar moved |
| C8 | Baselines B0, B1, B2 measured and reported, including B0's win |
| C9 | Causality A1..A7 measured; A1 and A2 give non-identical `dig` |
| C10 | no topology token in `p2_learn.zag` |
| C11 | levels 1/2/3 reported separately, never as a flat pass |
| C12 | no forbidden interpreter in any build or run log |
| C13 | frozen-arm artifacts byte-identical to the ones in this commit |

A FAIL on any bar is reported as a FAIL. Bars are not moved.

## 13. Boundaries, declared now

- One world, one fact representation, three researcher procedures.
- No new procedure, no new need shape, no new link kind is authored.
- The pass cap and the capacities are parameters, so results at `NM > 24`
  are unmeasured.
- Level 3 is expected to be zero; reporting a non-zero L3 would require
  the novel form to be non-enumerable from source, which the frozen
  repertoire forbids.
- In-process wall-clock is unavailable (ENOSYS); `k` is the cost metric.
- The 10-need goal is the only 10-STRUCTURE DAG exercised; deeper
  structures are chains of depth 10 and 20, not wider DAGs.