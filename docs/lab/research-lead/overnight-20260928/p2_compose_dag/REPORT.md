# REPORT: COMPOSE-DAG — frozen generic composition on seven topologies

Worker: composition-p2. Date: 2026-10-03. Branch: `p2/compose-dag`.
Governs: `PREREG.md` (committed alone, `89828ca62`, strictly before
`p2_learn.zag` existed), `NAMECHECK.md`, `BASELINE-FROZEN.md`.
Reproduce: `sh build.sh` (fail-closed). Log: `build_log.txt`.

## 1. Verdict

**PASS at Level 1 and Level 2. FAIL (as predicted) at Level 3.**

Never say "composition passes". The three levels are scored separately in
Section 4. The headline scientific content is not the pass: it is the set
of **five missing structural invariants** found and fixed in Section 3, of
which three are not about topology at all.

Three preregistered bars fail and are reported as failures, not moved:
**X1** on four hand-derived digest values that were arithmetic errors in
the prereg itself (Section 6.1), **X2** on one goal where the independent
reference cannot model iteration (Section 6.2), **X6** on an off-by-one in
the preregistered pass count (Section 6.3).

## 2. Infrastructure finding, load-bearing for the whole repository

`_zag_raw_syscall` returns **-78 (ENOSYS)** on darwin/arm64 with
znc 2026.07.0-dev, for every selector tested (0, 1, 4, 5). Verified
directly. The frozen single-write output path used by every lane in this
repository therefore emits **zero bytes on this host**, including
GEN-REDIM. Replacing that one line with `_zag_print` over the same buffer
makes `c8_base + c8_world + c8_learn + c8_main` reproduce
`cogops_learnosc2/c8_run1.txt` **byte-identically**
(sha256 `ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7`,
3/3 identical). **This resolves blocker B13 for the C4xx-era COGOPS
lanes**: they are hash-re-verifiable on this host after all, through one
writer substitution. Kill bar C2.

## 3. Missing structural invariants found, and the fix

Each is stated without reference to any goal shape. None is a per-topology
branch; `p2_learn.zag` contains zero topology tokens (C10) and the only
conditional on structure is the operand-surface descriptor, which is
derived from a need's *field count*, not from its role.

**I1 CAPACITY.** The frozen arena hard-codes 4 needs in seven separate
places (`W=320`, `OUTS=640`, `SUBL=512`, `ord=16`, `dirty=16`,
`ind`/`placed=16`, 56-byte plan entries) plus an 8-entry binding table
and a 16-iteration pass cap. Fix: GEN-REDIM discipline — every stride and
base is an accessor of `NM=24`/`NPLAN=24`/`NBIND=32`/`PCAP=64`, chained by
exact size. Verified: `z_alloc((320|640|512|16))` appears nowhere in
`p2_learn.zag` (C6). Consequence: a 20-need goal composes correctly
(id 24, dig 40250, plan order 0..19).

**I2 PRODUCED VALUE.** A link may carry only values its source actually
produced. The frozen code has this rule (`apply_kind1_g`) on the iterated
entry point and *not* on the other (`apply_kind1`); at id 10 the frozen
`compose_iter` already agrees with the adapt reading (2003), while the
independent strict reading gives 0. Fix: made unconditional.

**I3 OPERAND SET — the real find.** A receiving need's operand set is the
union, in goal-record link order, over **all** incoming set-consuming
links, of the values the producers actually produced, deduplicated with
first-occurrence order. The frozen `fanin_src` returns on the **first**
match, so the second source is silently discarded. Measured at id 9 on
the frozen arm: receiver gets 20 subjects instead of 26, downstream count
40 instead of 52 — a confidently wrong number with no signal. Fix:
`apply_set` replaces both `fanin_src` and `apply_kind3` with one rule;
kinds 2 and 3 stop being distinguishable at execution time, which is
itself the finding (they were two code paths for one concept).

**I4 LINK ADMISSION — the second real find.** A link is admissible iff both
endpoints' accepted shapes have a compatible operand; otherwise the goal
is REFUSED. Two distinct silent-wrong failures are removed:
- id 17: a set-consuming link into a need with no set-shaped operand is
  *ignored* by the frozen code; the engine answers `0`. The frozen arm's
  answer digests 41232; the adapt reading refuses.
- id 11: a set-consuming link out of a **scalar** producer is executed by
  feeding the scalar in as a subject. The frozen answer is `0`, which is
  indistinguishable from a legitimately empty result — this case is *not*
  answer-discriminating by construction, which is why a refusal
  (a new negative signal) rather than a different number is the only
  honest fix.

**I5 CANONICAL EMISSION.** The frozen `topo` scans for a zero-indegree
node without breaking, so the **last** ready node wins; measured plan
orders on the frozen arm are `1,0,2` (id 6), `2,0,1,3` (id 8),
`1,0,2,3` (id 9), `1,2,0` (id 19). Answers are therefore plan-order
dependent, two structurally equivalent compositions of the same goal do
not produce comparable answers, and order-sensitive equality testing
reports false mismatches (this lane measured `eq=0` on six goals before
the fix, purely from reordering). Fix: lowest-index tie-break plus
emission in need-index order. Measured after: every plan order is
`0,1,…,n-1` and every comparison is order-free.

**I7 PLAN IDENTITY — found by the L2 probe, not by a topology test.**
The frozen plan table is keyed by **goal tag alone**. Presenting tag 912
with six needs, then with ten needs, silently loads the six-step plan and
emits a six-record answer for a ten-need goal. The missing invariant is
not about capacity: it is that **a stored plan's identity is its tag AND
the shape signature it was built from**. Fix: `gsig` folds the need count,
every need tag and field count, and every link kind and endpoint into the
plan entry; `plan_find` verifies it. Measured (SEC-C): `C2-build-6`
nn=6 builds; `C2-extend-10` nn=10 **rebuilds** (r=2) and returns the
correct 56282; `C2-extend-10-again` loads (r=1) with the same answer;
`C3-truncate-6` correctly *loads* the previously stored six-need plan.
Without I7 the ten-need case would have been silently wrong.

### 3.1 Disclosed defect in my own committed baseline

`BASELINE-FROZEN.md` and the first `f_base_run*.txt` commit used a
**malformed goal constructor**: `gbro` emitted its k-th set link with
destination index `i` instead of `i+1`, so all k receivers were fed from
source 0 and the accumulator received the same source k times. The frozen
arm's id-8 digests in the committed baseline (45238-era) are therefore
wrong. `gbro` is fixed; the frozen arm was re-measured; the corrected
frozen digests are 45241 (id 8) and match the new engine exactly. Both
the defective and the corrected artifacts are in the repository.

## 4. Levels, scored separately

### Level 1 — exact reuse: **PASS**

`C1-build` r=2 (plan built, `plans_built`+1), `C1-load` r=1 (plan loaded,
`plans_loaded`+1), identical dig 4007, `trials` unchanged at 6. Same for
ids 12 (`C0-build-10` / `C0-load-10`, dig 56282 both) and 20-24.

### Level 2 — adaptive reuse: **PASS on all seven preregistered variants**

| variant | probe | result |
|---------|-------|--------|
| extended | `C2-extend-10` | rebuilds, dig 56282 correct |
| truncated | `C3-truncate-6` | loads the stored six-need plan, dig 12021 correct |
| substituted | `C4-substitute` | dig 6012 correct |
| rebound (same tag, new fields) | `C4-same-tag-b`, `-c` | **loads** the plan (r=1) and returns the *new* fields' answer: 4017, 4021 |
| specialized | `D3-warm-*` vs `D3-lin-*`, `E3` | version 2 chosen from learned coverage; `k` drops 5310 → 688 on id 12 |
| interface-adapted | id 10 (empty producer), ids 11/17 (refused) | 2003 / declined / declined |
| combined | id 12, one 10-need goal | dig 56282, `k` 688 |

The rebound result is the substantive one: the stored plan is a skeleton
(need order + per-need procedure), not a memorised answer, so a
same-tag/different-field query reuses it and still answers correctly.

### Level 3 — novel intermediate form: **FAIL, zero, as preregistered**

Ids 14, 15, 16 all return `r1=0` and increment `declines`. They contain
needs whose shapes no accepted procedure covers: a 3-field form with an
unrecognised 2nd field, a 3-field form with a distinct-subject-count
operator, and a 5-field form. The frozen repertoire is three
researcher-written procedures with three accepted shapes; `learn_bindings`
scans exactly that fixed set, so the learner cannot invent a form, and
this lane deliberately did **not** author one (doing so would be a
researcher-authored template, brief S9 / charter 17).

**The missing Level-3 form, named.** The vocabulary has exactly two
intermediate shapes: a *scalar* and a *subject list*. Every generalisation
that failed above is a consequence of that binary. What is missing is a
first-class **operand set as a materialised intermediate with its own
identity** — something a receiver can hold, pass on, and intersect, and
that can be *combined by an operation other than concatenation*. The
minimal witness is a receiver that needs the intersection of two operand
sets: expressible in the current vocabulary only as a procedure with a new
shape, which the learner has no mechanism to discover. Note the partial
credit: invariant I3 makes the operand set a real, deduplicated,
first-occurrence-ordered intermediate rather than an implicit read — but
it is still a transport, not an object.

## 5. Per-topology outcome

Arms: **F** = frozen `c8_learn.zag`, byte-identical. **R** = re-dimensioned
engine. `dig` is order-normalised, so F and R are directly comparable.

| topology | goal | nn | F (frozen) | R (new) | outcome |
|----------|------|----|-----------|---------|---------|
| sequential, 2 | id 1 | 2 | 4007 | 4007 | works frozen already |
| sequential, 3 | id 2 | 3 | 6012 | 6012 | works frozen already |
| two-source aggregate | id 6 | 3 | 43274 | 43274 | works frozen already (C433 evidence reproduced) |
| 3 receivers + aggregate | id 7 | 5 | **not runnable** (nn>4) | 47247 | capacity was the only blocker |
| one source / 2 receivers / aggregate | id 8 | 4 | 45241 | 45241 | works frozen already |
| **one receiver, TWO sources** | id 9 | 4 | **94129 (wrong: 20/40)** | **106768 (26/52)** | **I3 required** |
| carry out of an empty producer | id 10 | 2 | 2003 | 2003 | frozen iterated path already had I2 |
| set link out of a scalar producer | id 11 | 2 | 1004 (undetected) | **refused** | **I4 required; answer not discriminating, refusal is** |
| set link into a need with no set operand | id 17 | 3 | 41232 (confident 0) | **refused** | **I4 required** |
| **10-structure DAG** | id 12 | 10 | **not runnable** | **56282, k=688** | **capacity only** |
| 6 needs, link path 3, 2-source aggregate | id 13 | 6 | **not runnable** | 48265 | capacity only |
| unboundable shapes (3) | ids 14,15,16 | 3,3,1 | declined | declined | agrees; L3 = 0 |
| depth 2 / 3 / 5 / 10 / 20 | ids 20-24 | 2..20 | not runnable past 4 | 4007 / 6012 / 10025 / 20075 / 40250 | capacity only |
| self-carry + iterated | id 19 | 3 | 42248, **pa=16 (cap-truncated)** | 41232, **pa=23 (fixpoint)** | I1 on the pass cap |

## 6. Bars that fail, reported not moved

**6.1 X1, four hand-derived digests in the prereg were wrong.**
Prereg: id 7 = 54542, id 8 = 44238, id 12 = 145077, id 13 = 74661.
Measured and independently confirmed by the reference evaluator (Bar X2):
47247, 45241, 56282, 48265. Hand re-derivation agrees with the measured
values; the prereg's own arithmetic did not. (id 8's prereg value 44238
was in fact the *malformed-`gbro`* value, which is how the defect was
found.) X1 passes on the other 18 entries.

**6.2 X2, one goal.** id 19 is the only answered SEC-A goal whose answer
differs from the independent adapt reference (41232 vs 44236). Cause is
in the *reference*, not the engine: `ref_eval` evaluates one topological
pass and cannot model a self-carry, while the engine iterates to
quiescence. The reference agrees with the engine's *first* pass
(need1 = {1001}) and the engine's fixpoint is need1 = {} (17 successive
values 1001…1020 then empty). X2 holds on 21 of 22 answered goals.

**6.3 X6, off-by-one.** The prereg predicted 22 passes for id 19;
measured 23. The prereg arithmetic omitted the final quiescence-detection
pass, in which the changed need re-runs, produces no change, and the pass
counter still increments. The substantive half of X6 holds: with the pass
cap parameterised to 64 the walk reaches its quiescent fixed point
(23 < 64) instead of being truncated at 16.

## 7. Causality (charter 18)

Component parts of Z = the ten-need composition of id 12. X = the chain
of carried steps at needs 0-2 and the receivers at 4-6; Y = the
independent roots at need 3 and 8 and their receivers/accumulators. Both
are inside one plan because the substrate has no plan-as-plan mechanism;
the honest statement is therefore about *execution-time* causality inside
Z, tested by single-cell lesions.

**Held constant in every lesion below:** the fact store and its 177 facts,
the world, the goal record byte-for-byte (same `id`, same `nn`, printed on
the same line for the lesioned and unlesioned stages), all three procedure
indices, all other bindings, all other plan entries, and every stats cell
except the ones a lesion is defined to move. Each lesion is one `i32`
write immediately before exactly one query, restored immediately after.

**A1 (lesion: plan step 0's family cell → -1).** `E1`: dig 56282 → **48264**,
`k` 688 → 668. Vector: need0 → empty, and *exactly* its dependants empty
(needs 1, 2, 4, 7), while the independent branch (needs 3, 5, 6, 8, 9) is
byte-identical. Non-overlapping, as required.

**A2 (lesion: plan step 5's family cell → -1).** `E2`: dig → **54278**,
`k` → 615. Vector: only need5 empties and its dependant need7 collapses to
the single remaining source. **A1 ≠ A2 (48264 ≠ 54278), so neither is
confounded with the other.** Restore (`E2b`) returns exactly 56282 / 688,
which confirms the lesion — not a state drift — produced the change.

**A3 (index-coverage lesion).** `E3`: dig **unchanged** 56282, `k`
688 → **5310** (7.7×). This is the sharpest result: specialisation is
causally load-bearing for *cost only*, not for correctness. Answers are
bit-identical with and without every learned index.

**A4 (A1+A3).** `E4`: dig 48264 (the A1 signature, unchanged by A3),
`k` 5133 ≥ `E3`'s 5310? No — 5133 < 5310. The preregistered prediction
`k(A3+A1) >= k(A3)` **fails**: removing a step *removes work*, so the
combined lesion is cheaper than the coverage lesion alone. Reported as a
fail; the correct reading is that the two lesions are not additive
because one of them deletes a computation.

**A5 (fresh learner).** `E6`: a zeroed learner state on the identical
goal: `plans_built` 1, `trials` 3 (vs 6 warm — warm state reuses bindings),
`k` **5310** vs 688, same dig 56282. The fresh learner costs 7.7× more
and must re-derive. Passes the preregistered prediction.

**A6 (persistence / reuse).** `E0-load`: `plans_loaded` +1, dig identical,
`trials` unchanged.

**A7 (revisability).** `C7-drop-rebuild`: `plan_drop(912)` then
re-present → `plans_built` 27→28, dig identical, `k` identical. Then
`C4-same-tag-b/c` show a dropped-and-rebuilt plan tracking new fields.

**Preregistered negative causality result — confirmed.** `E7-binding-lesion`:
zeroing a binding cell (need tag 801) then dropping the plan does **not**
break composition: the next query re-derives the same procedure from the
need's *shape*, `plans_built` +1, dig 56282 unchanged, `trials` 6→7.
`E8` restores. So the frozen learner's binding is **not evidence-caused**:
it is a shape classifier wearing a table's clothing. The genuinely
evidence-driven component of the system is **version selection** (A3).
This is reported as a negative causality result, not smoothed over.

## 8. Baselines (charter 79)

**B0 MEMO — the baseline that WINS, reported as the winner.**
`MEMO 201/202`: first call `k=40`, repeat call `k=0`, same dig 4007. On raw
cost the memoriser beats the composer 40:0, exactly as preregistered.
It loses on generalisation: `MEMO 203` builds for tag 920 variant a
(dig 4007); `MEMO 205` is then asked the *same tag* with different fields
and returns dig **4007** — the stale answer. The composer on the identical
query (`D1-composer-920b`) returns **4017**. No flattening: B0 wins cost,
loses correctness.

**B1 EXHAUSTIVE.** `n! × 3^n`, generic-only executor, answer compared to
the target digest.

| nn | space | trials run | complete | found |
|----|-------|-----------|----------|-------|
| 2 | 18 | 18 | yes | yes |
| 3 | 162 | 162 | yes | yes |
| 4 | 1944 | 1944 | yes | yes |
| 5 | 29160 | 29160 | yes | yes |
| 6 | 524880 | 40000 (cap) | **no** | no |
| 10 | **214,277,011,200** | 40000 (cap) | **no** | no |

The composer solves the ten-need goal with `trials` = 3 and `k` = 688.
Against B1's 2.14e11 space that is roughly **7e10 fewer trials**. The
preregistered "at least 3 orders of magnitude" is met by 10 orders.
Preregistered infeasibility for nn ≥ 7 is confirmed from the closed form
and the measured n=6 truncation.

**B2 GENERIC-ONLY (linear scan).** Same engine, every coverage cleared:

| goal | warm k | generic-only k | ratio |
|------|--------|---------------|-------|
| id 6 | 1068 | 3894 | 3.6× |
| id 7 | 1436 | 11328 | 7.9× |
| id 8 | 964 | 7611 | 7.9× |
| id 12 | 688 | 5310 | 7.7× |
| id 13 | 1005 | 7965 | 7.9× |
| id 24 (depth 20) | 400 | 3540 | 8.9× |

Answers byte-identical in every pair. The warm engine beats the
linear-scan baseline on every preregistered id. Passed.

## 9. Depth and latency

Cost instrument is the frozen fact-check counter `k`; in-process wall
clock is unavailable (`_zag_raw_syscall` is ENOSYS, no clock is readable).
Process wall time is reported as a secondary figure.

**Depth curve** (chain goals, one producer per receiver, all relations
inside the learned index):

| depth d | nn | dig | warm k | k/d | generic-only k | ratio |
|---------|----|-----|--------|-----|----------------|-------|
| 2 | 2 | 4007 | 40 | 20 | — | — |
| 3 | 3 | 6012 | 60 | 20 | — | — |
| 5 | 5 | 10025 | 100 | 20 | — | — |
| 10 | 10 | 20075 | 200 | 20 | — | — |
| 20 | 20 | 40250 | 400 | 20 | 3540 | 8.9× |
| 10-structure DAG | 10 | 56282 | 688 | — | 5310 | 7.7× |

**`k = 20·d` exactly at d = 2, 3, 5, 10, 20.** Composition cost is
**linear in depth, not superlinear**: each step reads a bounded index
bucket, and nothing in the path is O(N) in the fact store once the
indices exist. The generic-only path is also linear here (177·d) because
the fact count is fixed — the 8-9× ratio is the constant factor, and it
would grow linearly with the fact count, which is where blocker B2 lives.
The 10-need DAG costs 688, i.e. **1.7× a 10-deep chain**, so width is
priced by operands actually consumed, not by re-scanning.

Structural depths exercised: link-graph path length 1 (ids 1, 2, 6, 10,
11, 18, 20-24), 2 (ids 7, 8), 3 (ids 12, 13). The graph topologies
actually exercised: sequential chains of depth 2/3/5/10/20, one-source
multi-receiver, multi-source-single-receiver, multi-source-multi-receiver,
three-root ten-need DAG with a two-source join, and a self-carry cycle.

Process wall time: frozen arm < 10 ms; new arm 8.44 / 8.42 / 8.46 s for
three runs (the exhaustive baseline dominates; the composition battery
itself is milliseconds).

## 10. Verification summary

| bar | result |
|-----|--------|
| C1 commit order | PASS — prereg `89828ca62` is a strict ancestor of the implementation commit |
| C2 base equivalence | PASS — `p2_base` reproduces `c8_run1.txt` byte-identically, 3/3 |
| C3 frozen substrate | PASS — `cmp` against `../cogops_learnosc2` |
| C4 determinism | PASS — 3/3 byte-identical, empty stderr, both arms (`720c7665…`, `ad93e840…`) |
| C5 one main | PASS |
| C6 no literal stride | PASS |
| C7 X1 | FAIL on 4 of 22 (prereg arithmetic, Section 6.1); PASS on 18 |
| C7 X2 | FAIL on 1 of 22 (reference cannot iterate, Section 6.2); PASS on 21 |
| C7 X3 | PASS — refusals exactly ids 11, 14, 15, 16, 17 |
| C7 X4 | PASS — nn=10 and nn=20 compose |
| C7 X5 | PASS — all plan orders canonical, all comparisons order-free |
| C7 X6 | FAIL on the exact pass count (Section 6.3); the fixpoint claim PASSES |
| C7 X7 | PASS via C2 (stronger form: same-source binary reproduces the frozen battery) |
| C8 baselines | PASS — B0's win reported, B1 beaten by ~7e10 trials, B2 beaten on all ids |
| C9 causality | PASS except the A4 additivity prediction (Section 7) |
| C10 opacity | PASS — zero topology tokens in `p2_learn.zag`; the frozen core's own historical vocabulary listed informationally |
| C11 levels separate | PASS — Section 4 |
| C12 purity | PASS — `forbidden_count=0`, log audit clean |
| C13 frozen artifacts | PASS — artefacts regenerated from committed sources |

## 11. Boundaries

- One world, 177 facts, one fact representation, three researcher
  procedures. No new procedure, no new need shape, no new link kind.
- `NM=24` is the declared capacity; `NM > 24` unmeasured. The operand
  set is capped at 31 values per need (frozen `SUBL` stride).
- `ret_gen` output cap 32 values; `cnt_gen` distinct cap 64 (frozen).
- Depth beyond 20 unmeasured. Width beyond 10 needs unmeasured.
- The 10-structure goal is the only wide DAG; the depth-20 goal is a
  chain, so "depth 20" and "width 20" are not both claimed.
- `gsig` is a 20-bit-modulus fold; a deliberate collision would defeat
  plan identity. Not stress-tested.
- The independent reference models one topological pass and no
  iteration; ids with a self-carry are outside its scope.
- Level 3 = 0. No claim of novel intermediate form is made.
- Bash-level evidence discipline: another lane committed onto this
  branch's history during the lane (shared-checkout thrash, cf. the
  P4 disclosure). This lane's commits touch only
  `docs/lab/research-lead/overnight-20260928/p2_compose_dag/`.

## 12. Next experiment

**Make the operand set a first-class object with an operator.** The single
highest-value follow-up is the Level-3 witness named in Section 4: give a
need the ability to *hold* an operand set and *combine* two of them by an
operation other than concatenation, and test whether the learner can
*discover* the combination from evidence. Concretely: present goals whose
answer requires a set intersection or a set difference over two operand
sets, with no new procedure in the source, and measure whether
`learn_bindings` declines (current expectation, consistent with L3 = 0) or
whether any evidence-driven mechanism exists to invent the form. This is
the only experiment in the programme that can move L3 off zero without a
researcher writing the operator, and its preregistered negative outcome is
already the ledger's standing claim.

Second, cheapest and highest value: re-run GEN-REDIM and the other
ENOSYS-affected lanes with the `_zag_print` writer substitution. Section 2
implies every pre-existing lane's single-write evidence is currently
unreproducible on this host, and one substitution restores it. That is a
repository-wide reproducibility fact, not a COMPOSE-DAG result.