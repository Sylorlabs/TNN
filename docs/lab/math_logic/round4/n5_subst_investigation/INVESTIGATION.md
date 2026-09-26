# N5 white-box investigation: PB4 substitution failure (F1) + PB1 engine crashes (F2)

Micah order 2026-09-25 ~23:41 PDT. Investigator: white-box subagent.
Date: 2026-09-26. Sealed evidence NOT modified; all experiments in scratch.

## 0. Method and provenance

- Engine: `n5_bin` from the repo checkout `math_logic/round4/engines/n5/` — SHA-256
  `c13243cb7834fb4c044143277b33ba65fa7ee975a20739cd2359f92c6205a219`,
  byte-identical to the sealed-recovery binary (MANIFEST.md). Source `n5.zag`
  SHA-256 `c2c105d8d14799fa0655b80f4391a1e083ce47d07d9e98d3f3ed922e63817598`
  (matches sealed MANIFEST). Binary run read-only; nothing written to the repo
  checkout or to `~/workspace/n5_recovery/`.
- Knowledge store: R4 `KNOWLEDGE_STORE_NL.md` (fingerprint `e8846333...`).
- Scratch workdir: `~/workspace/n5_subst_investigation/` (this package).
- Protocol: every run executed twice, outputs `cmp`-verified byte-identical;
  `rc=0` unless noted. CWD for runs: `math_logic/round4/engines/n5`
  (imports/store paths resolve relative to it, per n5.zag header).
- Line references below are to the frozen `n5.zag` (2588 lines), quoted as
  `n5.zag:<line>`.

---

## 1. F1 minimal reproduction: SUBST_MIN1

Smallest instance of the canonical failure: premise `n=2k`, goal `n^4=16k^4`.

Problem file `SUBST_MIN1.txt`:
```
# SUBST_MIN1

Domain: number_theory
Type: derivation

S1. n=2k.
S2. Prove that n^4=16k^4.

TARGET: n^4=16k^4.
```

Run (×2, byte-identical):
```
./n5_bin SUBST_MIN1.txt ../../batteries/knowledge/KNOWLEDGE_STORE_NL.md <cache> <stage>
```

Result: `VERDICT: WITHHELD`, `FLAGS: BUDGET-EXHAUSTED`, `CLAIM: n^4=16k^4.`
Threads: T0 CONTRA 1 proposal, T1 FORWARD 25 proposals, T2 GOAL **0 proposals**.

Full trace (`SUBST_MIN1_r1.out`, in this package). The ledger shows the premise
as S1 (`src=premise: n=2k.`), the contra-assumption as S39
(`src=assume: It is not the case that n^4=16k^4.`), then 25 rounds in which the
FORWARD thread does exactly one thing — definition expansion of cited store
sentences (L3 `construct-expand`):

```
R1 T0 CONTRA L0 contra-assume p=[0,-1,-1] -> S39 APPEND
R1 T1 FORWARD L3 construct-expand p=[4,6,-1] -> S40 APPEND
R2 T1 FORWARD L3 construct-expand p=[4,14,-1] DUP-SKIP
...
R25 T1 FORWARD L3 construct-expand p=[24,7,-1] -> S47 APPEND
WITHHOLD BUDGET-EXHAUSTED rounds=25
```

The derived states S40–S47 are all verbatim bodies of cited definitions
(commutativity, prime-number definition, triangle definitions, …). **The premise
`n=2k.` is never combined with anything, by any rule, in any round.** The GOAL
thread proposes nothing. The engine burns 25 rounds expanding definitions and
withholds. This is the F1 failure in miniature, deterministic and
byte-identical across reruns.

---

## 2. Hypothesis (a) — logic error in the chainer: EXCLUDED

There is **no substitution routine to misfire**. Exhaustive audit:

- `grep -n -i "subst\|rewrite\|unif\|leibniz" n5.zag` returns only the design
  comment at **n5.zag:21-24**:
  > `// ANTI-BRIDGE posture (unchanged): no typed variables, no scope,`
  > `// no unification, no formal syntax, no NL->schema translation. Native byte`
  > `// spans only.`
  The engine was deliberately built without unification/substitution.
- Complete inference inventory (all 12 licenses in `n3_propose`, n5.zag:1992-2005):
  - L0 `n3_prop_contra` (1552): contra-assume — fixed prefix + verbatim goal copy.
  - L1/L3 `n3_prop_contra`/`n3_prop_construct` (1552/1619): definition expansion —
    if a licensed definition's key word occurs in another state, **append the
    definition body verbatim** (`p.*.olen=n3_wcpy(s,yo,yl)`).
  - L2 `n3_prop_contra` (1604): conditional MP — antecedent matched by
    word-coverage (`n3_match_conj`, 1184), **consequent appended verbatim**
    (`n3_wcpy(s,qo,ql)`).
  - L4 `n3_prop_construct` (1646): iff-elimination — right side appended verbatim.
  - L5 `n3_prop_lemma` (1676): in-problem conditional lemma — antecedent
    word-coverage match, **consequent appended verbatim** (1693-1694).
  - L6/L7/L8 `n3_prop_goal` (1886): definition splice (verbatim body),
    antecedent planted as subgoal (verbatim), subgoal closed by word-coverage
    (verbatim state copy).
  - L9 `n5_prop_univ` (1376): universal "instantiation" — emits the **fixed
    concatenation** `<instance-subject-span> + <universal-VP-span>` (1417-1427).
    Text splicing of two existing spans; no variable binding.
  - L10 `n5_prop_ds` (1480): disjunctive syllogism — right disjunct appended verbatim.
  - L11 `n5_cache_fire` (1786): cached lemma span appended verbatim.

**Every inference rule produces only byte spans that already exist as contiguous
spans in the ledger** (or the fixed concatenation of two such spans). No rule
edits, rewrites, or synthesizes sub-spans. There is no substitution/unification/
pattern-match-with-binding code path anywhere in the 2588-line source, so (a) —
"a misfiring substitution routine, broken unification, missed pattern-match" —
cannot be the diagnosis.

---

## 3. Hypothesis (b) — missing knowledge: TRUE but insufficient (discriminating tests)

The R4 knowledge store genuinely lacks substitution knowledge:
`grep -n -i "substitut\|leibniz\|equals for equals"` on `KNOWLEDGE_STORE_NL.md`
returns **zero hits**. No equality-substitution rule, no power-distribution
lemma `(ab)^n = a^n b^n`.

Discriminating tests (hand-fed knowledge as extra premises, all 2×
byte-identical):

**B1** (`SUBST_B1.txt`): S1 `n=2k.` + S2 `If n=2k, then n^4=16k^4.`
→ **VERDICT: DERIVED**. Trace:
```
R1 T0 CONTRA L0 contra-assume p=[0,-1,-1] -> S40 APPEND
R1 T1 FORWARD L5 lemma-apply p=[2,1,-1] DISCHARGE assum=[S40] -> S41 APPEND
```
S41 = `n^4=16k^4.`, fired by L5 word-coverage of the antecedent `n=2k` against
S1, consequent copied verbatim, contradicting the contra-assumption → discharge
→ DERIVED.

**B2** (`SUBST_B2.txt`): S1 `n=2k.` + S2 `If n=2k, then n^4=(2k)^4.` +
S3 `If n^4=(2k)^4, then n^4=16k^4.` → **VERDICT: DERIVED** (two chained L5
firings: `n^4=(2k)^4.` then `n^4=16k^4.`, discharge against the assumption).

**B3** (`SUBST_B3.txt`): S1 `n=2k.` + S2 `Leibniz law of substitution: if a=b
then any expression containing a equals the same expression with a replaced
by b.` → **VERDICT: WITHHELD**, `BUDGET-EXHAUSTED rounds=25`. The general
principle sat in the ledger for 25 rounds and no rule ever touched it.

So: the existing machinery is sound — when the needed substitution steps are
hand-fed as explicit conditionals with **pre-computed consequents**, it derives
the goal deterministically. The proximate blocker was missing knowledge. **But**
the only knowledge that works is knowledge that already contains the answer:
B3 proves the *general* substitution principle is inoperative in N5's rule
idiom. You cannot "teach" substitution as knowledge, because a conditional's
consequent is fixed text — there is no capture variable for the rewritten term.
Covering F1 by knowledge would require pre-enumerating every substitution
instance per problem, i.e. handing the engine the answers. That is not a
knowledge fix; it is the engine's missing job.

---

## 4. Hypothesis (c) — architectural ceiling: ROOT CAUSE of F1

Mechanism-level characterization. Substitution of equals-for-equals requires
three things:

1. **Locate occurrences** of term `n` inside a larger span (`n^4`);
2. **Bind** `n → 2k` from the equality span;
3. **Synthesize a novel span** (`n^4=(2k)^4`) that appears nowhere in the input,
   rewriting all occurrences in one step.

N5's byte-span forward chainer cannot do any of the three:

- Matches are **whole-span word-coverage** (`n3_match_conj`, n5.zag:1184-1265):
  "every stemmed content word of the conjunct occurs in the state". There is no
  notion of an *occurrence position* or a *sub-term* — the engine never
  addresses bytes inside a span except as a whole unit.
- Conclusions are **verbatim copies** of existing spans (§2 inventory). The one
  span-constructor, L9, concatenates two fixed spans (`X` + `VP`); it cannot
  edit within a span.
- The conditional rule form (`if C then Q`) has a **fixed consequent Q** — it
  cannot be a template with bound variables, so even a perfectly worded general
  substitution rule (B3) can never fire productively.

Trace proof of the wall: in `SUBST_MIN1_r1.out`, 25/25 forward proposals are
`construct-expand` of unrelated definitions; the premise `n=2k.` has no rule
that can consume it together with anything else — there is no code path from
"equality span + term span" to "rewritten span". The chainer walks long chains
(H-CHAIN 6/6, 56–72 steps) precisely because chaining needs only whole-span
copying; substitution needs span *editing*, which the architecture excludes by
design ("no unification", n5.zag:21-24).

**Verdict for F1: (c) architectural — with (b) true-but-insufficient and (a)
excluded.** The engine is an honest deterministic *citation-expansion* chainer;
symbolic substitution is outside its reachable operation set.

**Concrete next step:** implement a genuine substitution/rewrite operation in
the chainer — term-aware span editing with variable binding (locate occurrences
of a bound term, emit the rewritten span as a first-class derived state).
This is a redesign of the rule idiom (a new license alongside L0–L11), not a
knowledge addition (B3 proves knowledge alone cannot express it) and not a bug
fix (no existing code is wrong; the operation is absent).

---

## 5. F2 triage — the 9 PB1 rc=-2 crashes: (a) CODE BUG, one shared root cause

Minimal reproductions (`CRASH_R3N_09_r1.out`, `CRASH_R3N_13_r1.out`,
`CRASH_R3N_23_r1.out`, each 2× byte-identical):
```
$ ./n5_bin .../r3n/R3N_09.txt .../KNOWLEDGE_STORE_NL.md <cache> <stage>
exit=4, stdout: "n5: engine error rc=-2"
```

Root cause, traced white-box. Exit 4 with `rc=-2` comes from exactly one
reachable site for these inputs: `n3_parse_prob` returning -2 at **n5.zag:946**
(`if(tp<0 || tl<1){return -2;}`) — no goal was extracted. The other -2 sites
(1014 premise-append overflow, 1064 store-append overflow, 1117 B5X-load
overflow) cannot fire on tiny R3N files with a store that parses fine for all
other problems.

The goal extractor (`n3_parse_prob`, n5.zag:930-946) recognizes only two goal
forms: a `TARGET:` line, or the fallback `- Prove that <goal>.` line. The 9
crashed problems are **exactly** the 9 R3N files with neither (verified by
grepping all 24 R3N files for `prove that`, case-insensitive — perfect
9↔9 correspondence):

| problem | goal phrasing (last STATEMENT line) |
|---|---|
| R3N_09 | `- Find the length of the hypotenuse.` |
| R3N_11 | `- What is the measure of the angle directly opposite it?` |
| R3N_13 | `- Is the vault safe?` |
| R3N_16 | `- Was Dana photographed at the finish line?` |
| R3N_18 | `- Determine the type of each islander.` |
| R3N_19 | `- Is electric current flowing through the wire?` |
| R3N_20 | `- Does the train depart before the meeting starts?` |
| R3N_22 | `- Is the soil dry?` |
| R3N_23 | `- Prove the foundation was laid before the roof was added.` (missing "that"!) |

Discriminating test: rewording just the goal line to `- Prove that ...`
(`R3N_13_FIXED.txt`, `R3N_23_FIXED.txt`) converts exit 4 into a full run
(`rc=0`, 2× byte-identical). The crash is purely the front-end goal parser, not
the reasoning substrate.

**Correction to VERDICT_N5.md §3**, which speculates the 9 crashes are "the same
ceiling expressed as a crash: problems whose proof shape needs
discharge/arithmetic the substrate cannot represent." The white-box trace shows
otherwise: all 9 die in `n3_parse_prob` before a single inference step runs,
from one shared parser gap. (Whether N5 could *derive* them once parsing is
fixed is a separate question — e.g. `R3N_13_FIXED` still withholds, because the
antecedent `the alarm rings` vs the premise `The alarm is ringing.` fails exact
word match with stemming disabled, n5.zag:243-257. And `R3N_09`'s find-type
goal needs numeric computation N5 has no operation for. But those are
withhold-reasons, not crashes.)

**Verdict for F2: (a) logic error — a goal-extraction bug in the problem-parser
front end (`n5_parse_prob`, n5.zag:930-946), single shared root cause for all 9.**
Not (b) knowledge, not (c) architectural.

**Concrete next step:** extend the goal extractor to the R3N battery's actual
question forms — `Find…?`, `What is…?`, `Is…?`, `Was…?`, `Determine…?`,
`Does…?`, and `Prove <goal>` without "that" — and decide the intended semantics
of find-type goals (numeric answers are outside N5's operation set; those should
withhold with a reason, not crash with rc=-2).

---

## 6. Summary table

| failure | (a) logic error | (b) missing knowledge | (c) architectural | verdict |
|---|---|---|---|---|
| F1 substitution (PB4 0/20) | excluded — no substitution code exists to misfire (n5.zag:21-24; §2 inventory) | true but insufficient — B1/B2 derive with pre-computed conditionals; B3 proves the general principle is inoperative | **root cause** — no rule synthesizes novel spans by occurrence rewriting; matches are whole-span word-coverage, consequents are fixed text | **(c)** |
| F2 crashes (PB1 9× rc=-2) | **root cause** — goal parser only accepts `TARGET:` / `- Prove that` (n5.zag:930-946); all 9 lack both | no | no | **(a)** |

## 7. Files in this package

- `SUBST_MIN1.txt`, `SUBST_MIN1_r1.out` — F1 minimal repro + full trace
- `SUBST_B1.txt`, `SUBST_B1_r1.out` — discriminating test, pre-computed conditional → DERIVED
- `SUBST_B2.txt`, `SUBST_B2_r1.out` — discriminating test, chained conditionals → DERIVED
- `SUBST_B3.txt`, `SUBST_B3_r1.out` — discriminating test, general Leibniz law → WITHHELD
- `CRASH_R3N_09_r1.out`, `CRASH_R3N_13_r1.out`, `CRASH_R3N_23_r1.out` — F2 minimal crash repros (exit 4, `n5: engine error rc=-2`)
- `R3N_13_FIXED.txt`, `R3N_13_FIXED_r1.out`, `R3N_23_FIXED.txt`, `R3N_23_FIXED_r1.out` — F2 discriminating tests (goal reworded → rc=0)
- `INVESTIGATION.md` — this report

All `_r1.out` files are representative of byte-identical `_r2.out` runs
(`cmp`-verified; `_r2` copies omitted to avoid duplication).
