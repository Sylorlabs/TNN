# PREREG — P2 OPERAND-SET (arms A and B)

Worker: p2operand. Date: 2026-10-03. Branch: `lane/p2operand`.
Owned path: `docs/lab/research-lead/overnight-20260928/p2_operand_set/`.
Claim IDs: **C600+** (the C500 block is contested; C590-C592 taken).

Governs this file, committed **ALONE**, before any `os_*.zag` exists.

---

## 0. What this lane is executing, and the tension it must not resolve dishonestly

`../p2_compose_dag/REPORT.md` section 4 found the L3 frontier off zero and
named the missing Level-3 form: **a first-class operand set, combined by an
operation other than concatenation**. Section 12 proposed: give a need the
ability to *hold* an operand set and *combine* two of them, and test whether
the learner can *discover* the combination from evidence rather than have it
written.

The obvious implementation is that **I** write the combining operator. That
disqualifies the result from L3 by construction: the researcher authored the
final structural form, so the form is enumerable from source (brief section 9;
charter 7). It is a mechanism demonstration, i.e. **L2**.

Therefore **both arms are preregistered and both are reported**:

| arm | what is in the source | what the learner supplies | admissible L |
|-----|----------------------|---------------------------|-------------|
| **A** | the domain rule, chosen by the researcher and carried in the goal record | nothing | **L2** |
| **B** | the domain rule as an unnamed code with **two provenances**: the goal record (A) or a rule table the learner fills from verified consequences (B) | the **choice** of which code | L2 or lower; see section 9 |

The two arms share **one** implementation of the reduction. They differ only in
**where the rule code comes from**. That is deliberate: it isolates the
epistemic question ("can the rule be *identified* from evidence?") from the
engineering question ("does the reduction work?").

**Preregistered expectation on ARM B's L-level: L2, and not L3.** See section 9.
The preregistered expectation on ARM B's *behaviour* is a split result
(declines when the evidence under-determines the rule; answers correctly when
it does not; answers **confidently wrong** when the evidence is consistent but
the world's true rule is different). All three are frozen in section 7.

## 1. Substrate

Frozen COMPOSE-DAG engine, digest-pinned, copied **byte-identically**:
`../p2_compose_dag/p2_learn.zag` becomes `os_learn.zag`, with exactly two
guarded insertions recorded in full in `DIFF-oslearn-vs-p2learn.txt`
(kill bar C3). Base, driver helpers, world and the four `ref/c8_*.zag` files
are byte-identical copies.

Three researcher procedures are unchanged: `ret_gen` (RETRIEVE),
`vfy_gen` (VERIFY), `cnt_gen` (distinct COUNT). No new procedure.

Goal record `G`: `[goal_tag, nneeds, needs..., nlinks, links...]`; a need is
`[need_tag, nfields, fields...]`; a link is 28 bytes
`[kind, dst_need, _, dst_slot, src_need, src_kind, src_slot]`.

Capacity accessors unchanged: `NM=24`, `NPLAN=24`, `NBIND=32`, `PCAP=64`,
`STK=128`.

## 2. The one new need shape, and its single provenance switch

The lane adds **exactly one** accepted need shape, the **domain form**:

```
nf = 2 + 3*ns      ns = fields[0] in 1..16
fields = [ ns, R, (subj, obj, val) * ns ]
```

field `subj == 0` means "take this step's subject from the domain". This is
the frozen VERIFY shape (family 1) with one extra leading integer field `R`
that carries a **domain rule code**. It is accepted **iff**
`domrule(G,n) >= 0`.

`domrule` is the single provenance switch, and it is the entire researcher/
learner delta between the arms:

```
ARMA==1 : return need_f(G,n,1)          // ARM A: the rule is IN THE GOAL
ARMB==1 : return the learner's rule     // ARM B: the rule is INFERRED
otherwise: return -1                    // shape absent -> goal declines
```

The reduction is a **single implementation**, `dom_reduce`, used by both arms.

### The domain rules, declared once, as codes

Over the `m` incoming set-consuming links of a need, in goal link order, let
`A1..Am` be the value sets the sources actually produced:

| code | rule, stated without set-theoretic vocabulary |
|------|-------------------------------------------------|
| 0 | keep a value if **any** source produced it (the substrate default) |
| 1 | keep a value if **every** source produced it |
| 2 | keep a value if the **first** source produced it and **no later** source did |
| 3 | keep a value if an **odd** number of sources produced it |
| 4 | keep **no** value |

Emission order is first-occurrence order in the source scan. Values are then
filtered by the need's VERIFY chain, as family 1 already does.

**These five codes are researcher-authored. That is the honest defect of ARM A
and it is disclosed in the source comment at `dom_reduce`.**

## 3. World additions (data only, `os_world.zag`)

| relation | facts | set |
|----------|-------|-----|
| 920 | `1300+i -> 6000`, i=0..9 | A = {1300..1309}, len 10, sum 13045 |
| 921 | `1305+i -> 6000`, i=0..9 | B = {1305..1314}, len 10, sum 13095 |
| 922 | `1300+i -> 7000`, i=0..9 | V = {1300..1309} (the VERIFY truth) |
| 923 | `1307+i -> 6000`, i=0..9 | C = {1307..1316}, len 10, sum 13115 |
| 924 | `1310+i -> 6000`, i=0..9 | D = {1310..1319}, len 10, sum 13145 |

All 177 pre-existing facts are retained. Set sums: A 13045, B 13095, C 13115,
D 13145. Receiver chain in every domain-form goal is `(0, 922, 7000)`, so the
receiver's output is the domain intersected with V = {1300..1309}.

## 4. Goals

`nsrc(n)` = a goal with `n` set-producing needs (920, 921, 923, 924 in that
order) and one domain-form receiver, `nf=5`, fields `[1, R, 0, 922, 7000]`.

| id | goal | sources | R | role |
|----|------|---------|---|------|
| 30 | `g930` | A,B | 1 | ARM A, primary |
| 31 | `g931` | A,B,C | 2 | ARM A |
| 32 | `g932` | A,B,C | 3 | ARM A |
| 33 | `g930b` | A,B,C | 0 | ARM A, substrate-default control |
| 34 | `g933` | A,B,C | 4 | ARM A, empty-domain control |
| 41 | `g941` | A,B,C,D | field=0 | **held-out**, ARM B target |
| 44 | `g944` | A | field=0 | ARM B training item 1 (single source) |
| 45 | `g945` | A,B | field=0 | ARM B training item 2 |
| 46 | `g946` | A,B,C | field=0 | ARM B training item 3 |

The **held-out** goal 41 has four sources and appears **nowhere** in ARM B's
training stream. Goals 44-46 carry `R = 0` in the record; under ARM B the
record's value is ignored and the rule comes from the learner's table. Goal
33 carries `R = 0` legitimately, which is why 33 and 41 have **different tags**.

## 5. Preregistered answers, derived by hand

Digest convention, unchanged from COMPOSE-DAG:
`dig = sum over records of (1002*len + sum(values))`; a record is
`(len, sum)`.

Domains (before the V filter), with sums:

| sources | R0 | R1 | R2 | R3 | R4 |
|---------|----|----|----|----|----|
| A | A | A | A | A | {} |
| A,B | {1300..1314} | {1305..1309} | {1300..1304} | {1300..1304,1310..1314} | {} |
| A,B,C | {1300..1316} | {1307..1309} | {1300..1304} | {1300..1304,1307..1309,1315..1316} | {} |
| A,B,C,D | {1300..1319} | {1310..1314} | {1300..1306} | {1300..1304,1307..1309,1315..1319} | {} |

Receiver records `(len, sum)` after the V filter:

| sources | R0 | R1 | R2 | R3 | R4 |
|---------|----|----|----|----|----|
| A | (10,13045) | (10,13045) | (10,13045) | (10,13045) | (1,0) |
| A,B | (10,13045) | (5,13035) | (5,13010) | (5,13010) | (1,0) |
| A,B,C | (10,13045) | (3,13024) | (5,13010) | (7,26034) | (1,0) |
| A,B,C,D | (10,13045) | (5,13060) | (7,26034) | (11,39059) | (1,0) |

Note R4: an empty domain makes the receiver run its chain verbatim, subject
stays 0, `verify(0,922,7000)` is false, so the record is `(1,0)`. Recorded so
the digests below are checkable.

Producer records: A `(10,13045)` -> 23065; B `(10,13095)` -> 23115;
C `(10,13115)` -> 23135; D `(10,13145)` -> 23165.

**Preregistered digests.**

| id | sources | R | producer sum | receiver | **dig** |
|----|---------|---|--------------|-----------|---------|
| 30 | A,B | 1 | 46180 | 18045 | **64225** |
| 31 | A,B,C | 2 | 69315 | 18020 | **87335** |
| 32 | A,B,C | 3 | 69315 | 33048 | **92363** |
| 33 | A,B,C | 0 | 69315 | 23065 | **92380** |
| 34 | A,B,C | 4 | 69315 | 1002 | **70317** |
| 41 | A,B,C,D | 1 | 92480 | 18070 | **110550** |
| 44 | A | any of 0-3 | 23065 | 23065 | **46130** |
| 44 | A | 4 | 23065 | 1002 | **24067** |
| 45 | A,B | 0 | 46180 | 23065 | **69245** |
| 45 | A,B | 1 | 46180 | 18045 | **64225** |
| 45 | A,B | 2 | 46180 | 18020 | **64200** |
| 45 | A,B | 3 | 46180 | 18020 | **64200** |
| 45 | A,B | 4 | 46180 | 1002 | **47182** |
| 46 | A,B,C | 0 | 69315 | 23065 | **92380** |
| 46 | A,B,C | 1 | 69315 | 16030 | **85345** |
| 46 | A,B,C | 2 | 69315 | 18020 | **87335** |
| 46 | A,B,C | 3 | 69315 | 33048 | **92363** |
| 46 | A,B,C | 4 | 69315 | 1002 | **70317** |

Five-way distinctness on 2 sources (45): 69245, 64225, 64200, 64200, 47182.
**R2 and R3 collide on 2 sources** and separate on 3 (87335 vs 92363). This is
why the training stream has three items and not two, and it is a
preregistered prediction, not a surprise.

Cross-check: `dig(46,R) == dig(33/31/32/34, R)` for R in {0,2,3,4} because
46 has no rule code and 31/32/33/34 do, but both reduce the same 3-source
tuple under the same rule. 92380, 87335, 92363, 70317 respectively. Kill bar
K11 verifies this identity **from the two independent code paths**.

## 6. Kill bars for ARM A, frozen

- **K1 (mechanism).** With `ARMA=1`, ids 30,31,32,33,34 all return
  `r=2` and digests exactly 64225, 87335, 92363, 92380, 70317, and each
  equals the independent oracle `domref_eval(A,G,R)` for the record's own R.
- **K2 (five-way distinctness).** The five digests are pairwise distinct.
- **K3 (default control).** Id 33 (`R=0`) is byte-equal to what the same
  structure gives with no domain form at all, i.e. R0 is the substrate's
  pre-existing behaviour and contributes nothing new.
- **K4 (AB2, THE ABLATION).** With the domain form **accepted** but the
  reduction **disabled** (`RED=0`), id 30 must answer the **unreduced union**
  digest **69245**, not 64225; ids 31,32,33,34 likewise become their R0
  digests. Bar: id 30 gives 69245 and 69245 != 64225. This is the required
  "remove the combined operand set and the answers break" evidence, and it is
  a *silent wrong number* rather than a refusal.
- **K5 (AB1, feature removal).** With `ARMA=0` and `ARMB=0` all five ids
  return `r=0` and increment `declines` by exactly 5.
- **K6 (regression).** With `ARMA=0, ARMB=0`, COMPOSE-DAG's SEC-A ids
  1..24 reproduce their `id / nn / r1 / dig` fields byte-identically from
  `../p2_compose_dag/r_run1.txt`.

## 7. Kill bars for ARM B, frozen

Protocol, in this order, in one process:

| step | action | preregistered outcome |
|------|--------|-----------------------|
| B1 | present id 44 with verified digest **46130** | survivor set `{0,1,2,3}` (size 4) |
| B2 | present held-out id 41, no verified digest given | **r=0, DECLINE** (4 survivors) |
| B3 | present id 45 with verified digest **64225** | survivors `{1}` (size 1) |
| B4 | present id 46 with verified digest **85345** | survivors `{1}` (size 1) |
| B5 | present held-out id 41 again | **r=2, dig 110550** |
| B6 | same as B5 but on a fresh learner | dig 110550, `plans_built`=1 |
| B7 | **AB4, wrong-world control**: rebuild the evidence stream with the digests of world `W0` (`R=0`), repeat B1-B4, present id 41 | survivors `{0}`, and id 41 answers **113545**, which is **WRONG** (truth 110550) |

- **K7.** B2 declines. If ARM B answers at B2 it has guessed; bar FAILS.
- **K8.** B5 answers 110550, and equals ARM A's answer on the same structure.
- **K9.** B7 answers 113545. Preregistered as a **confidence failure, not a
  pass**: identification is only as good as the evidence, and an
  under-determined-then-consistent evidence stream yields a confidently wrong
  number. Bar fails if B7 declines instead.
- **K10.** The survivor sets are exactly the preregistered ones at every step,
  for all three declared hypothesis classes (section 8).

## 8. The identifiability battery (IIT), and its hypothesis classes

A hypothesis is a rule code. The learner keeps the codes that reproduce every
verified digest it has been shown. Three **declared** classes:

| class | members | notes |
|-------|---------|-------|
| `H1` | {0,1,2,3,4} | the five codes of section 2 |
| `H2` | {0,1,2,3,4} minus 4 | `H1` without the empty rule |
| `H3` | {0,1,2,3,5,6} | 5 is code 0 over sources in reverse link order, 6 is code 1 over sources in reverse link order; both coincide with 0 and 1 on every presented goal |

Preregistered survivor counts:

| evidence prefix | H1 | H2 | H3 |
|-----------------|----|----|----|
| after 44 (single source) | 4: {0,1,2,3} | 4: {0,1,2,3} | 6: {0,1,2,3,5,6} |
| after 45 | 1: {1} | 1: {1} | 2: {1,6} |
| after 46 | 1: {1} | 1: {1} | 2: {1,6} |

- **K11 (H-robustness, negative direction).** On **single-source** evidence
  the verdict NOT-IDENTIFIED holds for `H1`, `H2` **and** `H3`. This
  negative is therefore robust to the choice of hypothesis class.
- **K12 (H-dependence, positive direction).** On multi-source evidence the
  verdict IDENTIFIED holds for `H1` and `H2` but **fails for `H3`**. Preregistered
  as a *disqualifier of the positive*: because the verdict is H-dependent, the
  positive carries no L3 weight. Stated in advance so it cannot be reported as
  a discovery.

**The H-free construction (the part that does not depend on any hypothesis
class).** Build five worlds `W0..W4`, identical except that world `Wr` has true
rule `r`; the observable transcript of an evidence prefix is
`sum_i (i+1) * D_i` over its items' verified digests, in order. Preregistered:

| prefix | W0 | W1 | W2 | W3 | W4 | distinct classes | largest class |
|--------|----|----|----|----|----|------------------|---------------|
| E1 = {44} | 46130 | 46130 | 46130 | 46130 | 24067 | 2 | **4** |
| E2 = {44,45} | 184620 | 174580 | 174530 | 174530 | 140494 | 4 | **2** |
| E3 = {44,45,46} | 461760 | 430615 | 436535 | 451619 | 351445 | 5 | **1** |

- **K13.** The measured matrix equals the table above exactly.
- **K14 (the result, stated as a bound).** Largest indistinguishable class is
  **4 worlds** on single-source evidence and **1 world** once two multi-source
  items are present. This needs no hypothesis class: two worlds with
  byte-identical transcripts are indistinguishable to *any* learner, so it is a
  bound on the **evidence**, not on this implementation. Preregistered class
  sizes: **[4, 2, 1]**.

## 9. The SUF question, answered in advance

**Preregistered answer: ARM B is NOT L3, and I say so before running it.**

Required test: *"if I read your source before the experiment, can I enumerate
every form the learner could produce?"*

Yes. `dom_reduce` in the source is a five-way switch on a researcher-chosen
integer, and `H1` in the source is the same five integers. A reviewer reading
`os_arm.zag` before the run can enumerate every answer ARM B can produce, in
the sense that matters for L3: **the structural form the learner ends up
using is drawn from a researcher-written menu.** Even when ARM B succeeds
(K8) or when it identifies correctly, it is performing selection over
researcher-enumerated operators, which brief section 9 and the ledger's
C285/C287/C335/C397 pattern explicitly exclude from L3.

What ARM B is entitled to claim, and only this: **the rule is identifiable
from verified consequences, with a measured identifiability boundary, and
identification is H-robust in the negative direction.** That is a result about
the *evidence*, and it is the transferable content of this lane.

**L-level assignment, frozen before the run.**

| arm | L |
|-----|---|
| A | **L2** (mechanism demonstration) |
| B | **L2** on the success path, by the enumeration test above |
| identifiability battery | **not an L claim**; an information bound on the evidence |
| COMPOSE-DAG L1/L2/L3 | unchanged; L3 remains **0** |

**Preregistered expectation that L3 stays 0.** No arm can move it: ARM A by
construction, ARM B by section 9. The lane's contribution is not a frontier
move; it is a *mechanism proof that the missing invariant was the blocker*
(K1) plus a *quantified statement of what evidence would be required for any
learner to identify the form at all* (K13/K14).

## 10. Baselines (charter 79), frozen

- **B0 MEMO.** Tag -> answer, filled on first call. Preregistered: tag 930
  (id 30, R=1) is memoised at dig 64225 with `k` only on the first call; the
  same tag with `g930b` (id 33, R=0, 4 needs) returns the **stale 64225**,
  while the composer answers **92380**. Memo wins on cost, loses on
  correctness. Both reported, no flattening.
- **B1 EXHAUSTIVE.** Enumerate all `n! * 3^n` (order, family-assignment)
  pairs with the generic-only executor, compare to the target digest.
  Preregistered:
  - id 30 (nn=3, space 162): with `ARMA=1`, **complete** (162/162) and
    `found=1`;
  - id 30 with `ARMA=0`: **complete** (162/162) and **`found=0`** — the whole
    frozen repertoire, enumerated to exhaustion, cannot produce the answer;
  - id 41 (nn=5, space 29160): `found=1` with `ARMA=1`, **`found=0`** with
    `ARMA=0`.
  The `found=0`-while-complete pair is the load-bearing baseline result: the
  domain form is outside the enumerable repertoire of the frozen procedures.
- **B2 LINEAR / generic-only.** Every coverage word cleared. Bar: strictly
  higher `k` on ids 30 and 41, answers byte-identical to the warm runs.

## 11. Determinism, purity, output

- 3/3 byte-identical stdout, empty stderr, for every binary.
- Exactly one `fn main(` per translation unit.
- **C6 non-empty output assertion, fail-closed**: the run must exceed 20000
  bytes and contain the literal markers `IITMATRIX`, `ARMA`, `ARMB`,
  `IITCLASS`. A short or marker-free log is a FAIL, not a pass (brief 4.0:
  an inert output path made a prior worker's logs empty while reporting
  success).
- All dynamic output through one preallocated buffer and `_zag_print`.
  `_zag_raw_syscall` is never used for output.
- Pure Zag for all computation and statistics; shell/git orchestration only.

## 12. Kill bars, frozen, all of them

| id | bar |
|----|-----|
| C1 | PREREG.md committed ALONE, strictly before any `os_*.zag` exists |
| C2 | `os_base + ref/c8_world + ref/c8_learn + ref/c8_main` reproduces `../cogops_learnosc2/c8_run1.txt` byte-identically, 3/3 |
| C3 | `os_learn.zag` differs from `p2_learn.zag` **only** in the two guarded insertions published in `DIFF-oslearn-vs-p2learn.txt` |
| C4 | 3/3 byte-identical stdout, empty stderr |
| C5 | exactly one `fn main(` per binary |
| C6 | non-empty output asserted with the four markers |
| C7 | no semantic token (`UNION/INTERSECT/DIFFERENCE/SUBSET/EXCLUDE/OPERANDSET/...`) in `os_learn.zag`, `os_arm.zag`, `os_drv.zag`, `os_world.zag`, `os_main.zag` |
| C8 | K1..K14 hold, or the specific failure is reported with no bar moved |
| C9 | baselines B0/B1/B2 measured, including the `found=0` while complete result |
| C10 | ARMB never reads a rule code out of the goal record; verified by source grep |
| C11 | levels A/B/identifiability reported separately, never as a flat pass |
| C12 | no forbidden interpreter token in any build or run log |
| C13 | frozen-arm artefacts byte-identical to the ones in the implementation commit |

## 13. Boundaries, declared now

- One world family, one fact representation, three researcher procedures.
- The five domain rules are researcher-authored. **This is the lane's central
  disclosed defect**, and section 9 turns it into a stated L-ceiling rather
  than a hidden one.
- "Identified" is judged against declared hypothesis classes. Only the
  **negative** verdict is claimed H-robust (K11); only the **world-transcript**
  matrix (K13/K14) is claimed H-free.
- Verified answers are supplied to the learner as preregistered integer
  literals in `os_world.zag`. They are hand-derived from the world and
  independently reproduced at run time by `domref_eval`. The learner is never
  shown the rule code during training; only the digest.
- One held-out goal. Four sources is the widest domain-form goal; results at
  five or more sources are unmeasured.
- `gsig` folds need tags and field *counts*, not field *values*, so two goals
  differing only in the rule code would share a plan identity. All goals here
  carry distinct tags, so this is not exercised. Declared, not fixed.
- No new link kind, no new procedure, no change to any decision rule in the
  frozen engine.