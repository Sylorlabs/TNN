# REPORT: P2 OPERAND-SET — arms A and B, and the identifiability bound

Worker: p2operand. Date: 2026-10-03. Branch: `lane/p2operand`.
Governs: `PREREG.md` (`d69a87017`, committed alone, strictly before any
`os_*.zag`), `BASELINE-FROZEN.md` (`09818ed5f`), `PROCESS-DISCLOSURE.md`.
Reproduce: `sh build.sh` (fail-closed). Log: `build_log.txt`.
Claim IDs: **C601** (ARM A), **C602** (ARM B), **C603** (identifiability),
**C604** (ablation and baselines). C600 is the design/prereg.

---

## 1. Verdict

**ARM A: Level 2, mechanism demonstrated.** With one researcher-written
domain rule the frozen composer answers goals whose answer requires a
non-concatenating combination of two or more operand sets. All five ARM A
answers equal an independent oracle element for element. This establishes
that COMPOSE-DAG's missing invariant really was the blocker. It is L2 and is
labelled L2: I wrote the operator.

**ARM B: the rule is identifiable from evidence, and this is still Level 2.**
The learner picks the correct rule out of verified consequences, refuses to
answer when the evidence under-determines it, and carries the rule to a
held-out goal. **It is not L3**, for the reason asked for in advance and
confirmed in section 6: reading `os_arm.zag` before the run enumerates every
form the learner can emit.

**L3 remains 0.** Neither arm can move it, and the preregistration said so.

**The transferable result is the identifiability bound (C603):** a
hypothesis-class-free measurement that the largest set of *worlds*
indistinguishable from the presented evidence is **4, then 2, then 1** as
evidence items are added. No learner, of any construction, can do better on
single-source evidence, because the transcripts are byte-identical.

## 2. Substrate and delta

Frozen COMPOSE-DAG engine, byte-identical, plus **three** guarded insertions
(`DIFF-oslearn-vs-p2learn.txt`, +36 / -0 lines): `shape_desc` accepts the
domain form `nf = 2 + 3*ns`; `learn_bindings` gates a domain-form need on an
available rule; `exec_need` applies the reduction. `w_to_chain` is
**unchanged**, because the rule code is the goal's *last* field and the
frozen chain reader only touches fields 1..3*ns.

One reduction implementation, two provenances, selected by `domrule_of`:
an explicit forced code (ARM B's hypothesis trials, on a scratch learner),
then the learner's rule table, then the goal record. The arms differ only in
where the integer comes from.

Regression: with both arms off, all 21 COMPOSE-DAG SEC-A goals reproduce
their `id / nn / r1 / dig` from `../p2_compose_dag/r_run1.txt` byte for byte
(**K6 PASS**). `os_base` still reproduces `cogops_learnosc2/c8_run1.txt`
byte-identically (**C2 PASS**).

## 3. Preregistered bars that fail, reported not moved

**3.1 Five of the seventeen hand-derived digests in PREREG section 5 were
arithmetically wrong.** Cause: my sums for the reduced domains. I wrote
`sum{1305..1309} = 13035`; it is **6535**. I wrote a producer record
`(10,13115)` as digest 23115; it is `10020+13115 = 23135`. The qualitative
predictions (which rules collide, where the survivor sets land) were all
right; the arithmetic was not.

| entry | prereg | measured | held |
|-------|--------|----------|------|
| id 30, rule 1 | 64225 | **57725** | no |
| id 31, rule 2 | 87335 | **80835** | no |
| id 32, rule 3 | 92363 | **87765** | no |
| id 33, rule 0 | 92380 | 92380 | yes |
| id 34, rule 4 | 70317 | 70317 | yes |
| id 41, rule 1, 4 sources | 110550 | **93482** | no |
| id 44 (1 source), rules 0-3 | 46130 | 46130 | yes |
| id 44, rule 4 | 24067 | 24067 | yes |
| id 45, rule 0 | 69245 | 69245 | yes |
| id 45, rule 1 | 64225 | **57725** | no |
| id 45, rules 2, 3 | 64200 | **57700** | no |
| id 45, rule 4 | 47182 | 47182 | yes |
| id 46, rule 0 | 92380 | 92380 | yes |
| id 46, rule 1 | 85345 | **76245** | no |
| id 46, rule 2 | 87335 | **80835** | no |
| id 46, rule 3 | 92363 | **87765** | no |
| id 46, rule 4 | 70317 | 70317 | yes |

The IIT matrix's `E2` and `E3` columns shift with these; the `E1` column does
not. **The preregistered class-size table `[4, 2, 1]` holds exactly** and
K14 is unaffected, because the errors are monotone within each column.

The implementation follows the preregistered *design* and the measured
values, and the ARM B "verified answer" literals are the world's true
verified digests (reproduced at run time by the independent oracle). No bar
was moved: the digests the learner is shown are defined by the world, not by
my arithmetic.

**3.2 The held-out goal's derivation was wrong in a way that matters.** I
preregistered `A∩B∩C∩D = {1310..1314}`. It is **empty**: `A∩B∩C =
{1307,1308,1309}` and `D = {1310..1319}` are disjoint. So under the true
rule the held-out goal's correct domain is empty. Two consequences, both
reported rather than smoothed:

- the held-out answer 93482 is **not digest-discriminating** between
  "identified rule 1" and "the receiver ran before any source", because both
  produce an empty domain;
- the exhaustive baseline on the 4-source goal reports `found=1` under
  ARMA=0 (preregistered `found=0`). This is an **artifact, not a solution**:
  `EXH` compares digests only and never consults the goal's rule field, and
  one of the 29160 enumerated orders happens to run the receiver before its
  sources, yielding the same digest. The id-30 case, where the correct
  domain is non-empty, is clean: `found=1` with the mechanism, `found=0`
  without it, both while **complete** over the whole 162-point space.

**3.3 C7 as preregistered is infeasible jointly with C3.** The banned
tokens ("union", "operand set", "concat") already appear in COMPOSE-DAG's own
published comments inside `p2_learn.zag`, and C3 forbids altering them. The
bar is applied to comment-stripped source instead, which is what the bar was
for. Reported as a preregistering error.

**3.4 C3 says two insertions; there are three.** Published in full anyway.

**3.5 One process failure**, self-reported: a stray `python3` with an empty
heredoc in a shell command whose edit I then made with the Edit tool. See
`PROCESS-DISCLOSURE.md`. It computed nothing and no result depends on it, but
it is a PROCESS-FAIL under brief section 0 and is not hidden.

## 4. ARM A — mechanism (C601), **Level 2**

`ARMA=1, ARMB=0`. Five goals, five authored rule codes, all answered
`r=2`, all `eq=1` against `domref_eval` (an independent straight-line
evaluator sharing no plan machinery, no learner state, no descriptor
function and no reduction code with the engine).

| id | sources | code | dig | oracle | eq | k |
|----|---------|------|-----|--------|----|---|
| 30 | A,B | 1 | 57725 | 57725 | 1 | 70 |
| 31 | A,B,C | 2 | 80835 | 80835 | 1 | 80 |
| 32 | A,B,C | 3 | 87765 | 87765 | 1 | 110 |
| 33 | A,B,C | 0 | 92380 | 92380 | 1 | 200 |
| 34 | A,B,C | 4 | 70317 | 70317 | 1 | 40 |
| 40 | A,B,C,D | 1 | 93482 | 93482 | 1 | 50 |

- **K1 PASS** on all six, including the record's own code matching the oracle.
- **K2 PASS**: the five codes 0-4 give five pairwise distinct digests on
  identical structure.
- **K3 PASS**: code 0 gives 92380, and the ablation arm (reduction removed)
  also gives 92380 with `eq=1` — code 0 *is* the substrate's pre-existing
  behaviour and contributes nothing new.

**Independent-oracle agreement is 20/20** across the whole (goal, code)
matrix: `E id=40..43 force=0..4` all `eq=1`, zero disagreements.

## 5. ARM B — identification (C602), **Level 2**

`ARMA=0, ARMB=1`. The learner is shown a goal record and a verified answer
digest, never a rule code. For each surviving candidate it runs the
composition on a scratch learner with that code forced and kills the
candidate if the digest differs.

| step | action | survivors | rule | held-out answer |
|------|--------|-----------|------|-----------------|
| B1 | item 44, verified 46130 | `{0,1,2,3}` (4) | -1 | — |
| B2 | **held-out id 41, no verified answer** | 4 | -1 | **r=0, DECLINED** |
| B3 | item 45, verified 57725 | `{1}` (1) | 1 | — |
| B4 | item 46, verified 76245 | `{1}` (1) | 1 | — |
| B5 | held-out id 41 again | 1 | 1 | **r=2, dig 93482, eq=1** |
| AB3 | rule table cleared | — | -1 | **r=0, DECLINED** |
| B6 | whole stream on a fresh learner | 4/1/1 | 1 | 93482, identical |
| B7 | same stream, evidence from world code 0 | 4/1/1 | **0** | **dig 115545, eq=0 — WRONG** |

- **K7 PASS**: with 4 survivors the learner refuses the held-out goal. It
  declines rather than guessing.
- **K8 PASS**: after identification it answers 93482, and that equals ARM A's
  answer on the same four-source structure (`A-armA id=40`). **Same number,
  two provenances**: one authored in a goal record, one selected from
  verified consequences.
- **K9 PASS as a confidence failure, not a pass**: under evidence consistent
  with a different world, the same mechanism identifies code 0 and answers
  the held-out goal **115545** against a truth of 93482, with no signal at
  all. Identification is only as good as the evidence.
- **AB3 PASS**: emptying the rule table restores the refusal, so the answer
  at B5 is caused by the learned rule and not by a cached plan.

## 6. The SUF answer for ARM B: **NOT L3**

Required test: *if I read your source before the experiment, can I enumerate
every form the learner could produce?*

**Yes.** `dom_reduce` in `os_arm.zag` is a switch on five
researcher-chosen integers, stated in a comment block that names what each
code does, and the declared class `H1` is those same five integers. The
learner's entire output space is `{0,1,2,3,4}` composed with the three frozen
procedures. This is selection over a researcher-written menu, which brief
section 9 and the ledger's C285 / C287 / C335 / C397 pattern exclude from
L3. **ARM B is L2 on its success path.** It was preregistered as L2 (PREREG
section 9) and the SUF audit does not overturn that.

What ARM B *is* entitled to say: the rule is identifiable from verified
consequences, the identifiability boundary is measured, and the negative
verdict is robust to the hypothesis class. That is a claim about the
**evidence**.

## 7. The identifiability bound (C603) — the hypothesis-class-free part

Five worlds `W0..W4`, identical except for their true rule. Transcript of an
evidence prefix = `sum_i (i+1)*D_i` over its items' verified digests. This
construction mentions no hypothesis class at all.

| prefix | W0 | W1 | W2 | W3 | W4 | distinct | largest class |
|--------|----|----|----|----|----|----------|---------------|
| E1 = {single source} | 46130 | 46130 | 46130 | 46130 | 24067 | 2 | **4** |
| E2 = {+ 2 sources} | 184620 | 161580 | 161530 | 161530 | 118431 | 4 | **2** |
| E3 = {+ 3 sources} | 461760 | 390315 | 404035 | 424825 | 329382 | 5 | **1** |

- **K13 PASS**: the measured matrix equals the table.
- **K14 PASS**: class sizes **[4, 2, 1]**, exactly as preregistered.

**Why this is the real result.** Four worlds present byte-identical
transcripts on single-source evidence. Any learner — mine, yours, one that
does not exist yet — receives the same information and must behave the same
way on all four. This is a bound on the **evidence**, not on an
implementation, and it cannot be engineered away by a better learner. One
two-source item is necessary to break the first degeneracy; a second is
necessary to separate codes 2 and 3, which are indistinguishable on two
sources and separate on three.

Declared-class survivors, the H-dependent part:

| evidence | H1 `{0..4}` | H2 `{0..3}` | H3 `{0,1,2,3,5,6}` |
|----------|-------------|-------------|--------------------|
| 1 item (single source) | 4, not identified | 4, not identified | 6, not identified |
| 2 items | 1, identified | 1, identified | 2, **not** identified |
| 3 items | 1, identified | 1, identified | 2, **not** identified |

- **K10 PASS**: every survivor set is exactly the preregistered one.
- **K11 PASS**: the single-source **not-identified** verdict holds for all
  three declared classes, so that negative is class-robust.
- **K12 PASS as a disqualifier**: the multi-source **identified** verdict
  holds for `H1` and `H2` and **fails** for `H3`. Because the positive is
  class-dependent it carries no L3 weight — which is exactly why section 6
  lands on L2.

## 8. Ablation (C604) — the required one

**AB2, shape accepted and reduction removed (`RED=0`).** This is the load-bearing
test: the need still binds, still consumes an operand set, still answers with
no signal of trouble, and is **silently wrong**.

| id | rule | with reduction | without | oracle | eq |
|----|------|----------------|---------|--------|----|
| 30 | 1 | 57725 | **69245** | 57725 | 0 |
| 31 | 2 | 80835 | **92380** | 80835 | 0 |
| 32 | 3 | 87765 | **92380** | 87765 | 0 |
| 33 | 0 | 92380 | 92380 | 92380 | 1 |
| 34 | 4 | 70317 | **92380** | 70317 | 0 |

Every removed reduction collapses to the unreduced concatenation answer. The
reduction, not the new shape, is what carries the answer: accepting the shape
without the reduction buys nothing and costs correctness silently. **K4
PASS.**

**AB1, the form absent (`ARMA=0, ARMB=0`).** All five goals return `r=0` and
`declines` rises by exactly 5 (5 to 10). **K5 PASS.**

**AB3**, rule table cleared, held-out goal declines. **AB4/B7**, the
wrong-world control, answers confidently wrong. Both above.

## 9. Baselines (charter 79)

**B0 MEMO — the baseline that wins, reported as the winner.** Repeat call
`k=0` against the composer's 70-200: memo wins on cost. Same goal tag 930
re-presented with a different rule code and one more source: memo returns the
**stale 57725**, the composer returns **92380**. Memo loses correctness. No
flattening.

**B1 EXHAUSTIVE — the load-bearing baseline.**

| id | nn | space | trials | complete | ARMA=1 found | ARMA=0 found |
|----|----|-------|--------|----------|--------------|--------------|
| 30 | 3 | 162 | 162 | yes | **1** | **0** |
| 41 | 5 | 29160 | 29160 | yes | 1 | 1 (artifact, section 3.2) |

The id-30 pair is the result: **the entire frozen repertoire, enumerated to
exhaustion, cannot produce the answer.** That is the formal sense in which
the domain form lies outside the enumerable repertoire of the three frozen
procedures. It does not say the form is unlearnable; it says it is not
reachable by search over what is already there.

**B2 GENERIC-ONLY (linear scan).** Every coverage word cleared.

| goal | warm k | generic-only k | ratio | answers |
|------|--------|----------------|-------|---------|
| id 30 | 70 | 1589 | 22.7x | identical |
| id 41 | 240 | 5448 | 22.7x | identical |

Passes, at a much larger ratio than COMPOSE-DAG's 7.7x, because these goals
have 10- and 20-value operand sets and the domain reduction is itself a
multi-pass scan.

## 10. Verification summary

| bar | result |
|-----|--------|
| C1 prereg alone, before all impl | PASS — `d69a87017` touches 1 file; strict ancestor of all five impl files |
| C2 frozen battery equivalence | PASS — `ae0ae3bf…`, 3/3, stderr empty |
| C3 published delta | PASS in substance, **three** insertions not two; +36/-0, full diff published |
| C4 determinism | PASS — 3/3 byte-identical, `b3eaa4f8…`, stderr empty, both binaries |
| C5 one `fn main` | PASS |
| C6 non-empty output | PASS — 31085 bytes, markers `IITMATRIX` `IITCLASS` `ARMA=` `ARMB=` all present |
| C7 no semantic token | PASS **after re-scoping** (section 3.3) |
| C8 K1..K14 | K2,K5,K6,K7,K9,K10,K11,K12,K13,K14 PASS as written. **K1, K3, K4, K8 and PREREG section 5 FAIL against the preregistered numeric literals** (section 3.1); the qualitative content of each holds |
| C9 baselines | PASS, with the id-41 exhaustive result reported as an artifact |
| C10 ARMB does not read the record | PASS by construction: `domrule_of` checks `arm_b` before `arm_a`, and both ARM B goals carry code 0 in the record |
| C11 levels separate | PASS — sections 4, 6, 7 |
| C12 purity | PASS — `PURE-ZAG-CLEAN`, build/run log audit clean; one stray interpreter recorded in `PROCESS-DISCLOSURE.md` |
| C13 frozen artefacts | PASS — regenerated from committed sources in the same commit as the sources' consumers |

## 11. Boundaries

- One world family, one fact representation, **three researcher procedures,
  unchanged**. One new need shape, one reduction, both researcher-written.
- **The five domain rules are the lane's central disclosed defect.** They are
  in the source, in a comment, in a switch. That is what caps ARM A and ARM B
  at L2.
- "Identified" is judged against declared hypothesis classes. Only the
  **negative** verdict is claimed class-robust (K11); only the
  **world-transcript matrix** (K13/K14) is claimed class-free.
- Verified answers enter as integer literals in `os_main.zag`, hand-checked
  against the world's derivations and reproduced at run time by
  `domref_eval`. The learner is never shown a rule code during training.
- One held-out goal, four sources, and its correct domain is empty
  (section 3.2). Five or more sources, and non-empty held-out domains, are
  unmeasured.
- ARM B's evidence is a stream of three presents with verified digests.
  Whether the learner can *generate* its own discriminating query, rather
  than receive one, is untested and is the obvious next step.
- `gsig` folds need tags and field counts but not field values, so two goals
  differing only in the rule code share a plan identity. Not exercised here
  (all goals carry distinct tags except the deliberate pair, which is
  separated by `clear_plans`).
- In-process wall clock is unavailable (`_zag_raw_syscall` is ENOSYS); `k` is
  the cost metric, as in COMPOSE-DAG.
- **L3 = 0.** Unchanged.

## 12. Next experiment

**The one thing this lane points at: give the learner the ability to
manufacture the evidence it is missing, and measure whether it can.**

Section 7 shows the blocker is not the learner's search, it is the
information in the transcript. Four worlds are indistinguishable on
single-source evidence. The concrete next experiment is therefore not
another operator and not another shape: it is whether the composer can
**issue its own discriminating query** — construct a candidate code, compose
a probe goal whose answer differs between two surviving worlds, present that
probe, and read the verdict — and whether the probe it invents is one that
actually separates the survivors. That is the first mechanism in this
programme whose success would not be a selection over a written menu,
because the probe is chosen by the state of the learner's own uncertainty
rather than by the researcher.

Two secondary items, cheap and high value:

1. **Re-run the COMPOSE-DAG L2 battery with a non-empty held-out domain.** The
   empty-domain coincidence in section 3.2 cost this lane its cleanest
   held-out test; a four-source world with a non-empty intersection would
   restore it, and would also let the exhaustive baseline's `found=0` claim be
   stated without the caveat.
2. **Independence audit of the identifiability battery** by a second party:
   the claim "four worlds are indistinguishable on this evidence" is a claim
   about constructions, and a second reader should check the two worlds
   really are distinct worlds and not two names for one.