# P6 / PUSHDOWN — REPORT

Lane `p6_pushdown`, branch `lane/p6pushdown`, worktree
`/Users/Shared/micah/Documents/TNN/.worktrees/p6pushdown`, base `87a822426`.

Substrate read in full before starting: `docs/ops/ZAG_LANGUAGE_AND_WORKER_BRIEF.md`
(all 298 lines), `p6_formal_induce/PREREG.md`, `PREREG_AMENDMENT1.md`,
`PREREG_AMENDMENT2.md`, `REPORT.md`, and the world sources `p6_lang.zag`,
`p6_ckcore.zag`, `p6_gencorpus.zag`, `p6_gcmain.zag`.

## 1. STATUS

**BUILD-PARTIAL. The primary objective was NOT achieved. Prereg marked VOID.**
No new capability claim is minted. Claim IDs C520-C539 remain unminted.

What is finished, measured and committed:

- The frozen FL7 world rebuilt and verified reproducing byte-identically.
- **A pushdown learner with an explicit production/stack representation**, built
  as the load-bearing change this lane was chartered to make.
- **R1: hypothesis-free delimiter discovery** over opaque tokens.
- **Role induction** that recovers the true alphabet partition from the corpus
  alone — a real, verified induction.
- **R5: the `(M, c, val)` solver**, with the identifiability treatment the prior
  lane left as next-step-2.
- **A fixture audit that voids the complexity ladder**, with the root cause
  isolated in the world generator.

What is NOT finished: R2 productions, R3 typing, R4 scope, R6 generation and the
single accept fold; `p6_check`; `p6_stupid`; and therefore K1-K5, K7-K10, P1-P6
and ZD-1/2/3 are **UNMEASURED**. No arm was scored. Nothing here supports a
capability claim about any learner.

## 2. COMMITS

| commit | content |
|---|---|
| `ad335b60f` | PREREG alone, v2. Adopts prior prereg + AMD1 + AMD2 verbatim. Load-bearing change = explicit production/pushdown representation. K6 reported twice because disclosed measurement M2 shows set A's modulus is not uniquely recoverable. |
| `ebda445ba` | Reused frozen world + 14 corpora from `p6/formal-induce`; world diagnostics `p6_inspect` / `p6_ident` / `p6_ident2`. |
| `01665da19` | R1 + role induction, `NAMECHECK.md`, **`FIXTURE_AUDIT.md` (VOID disclosure)**. |
| `ef81ca30a` | R5 `(M,c,val)` solver; `rUNOP` / `rOUT` role refinements. |
| `fbaaea37c` | Two silent induction bugs found by R5, with measurements. |

Determinism: `p6_ladder` 3/3 byte-identical sha
`16f2132550fe7be783bf4297a9dabbe1a42691ebc0878d3179054bac6d02a076`. `p6_gsolve`
3/3 byte-identical. World `p6_gencorpus` 3/3 byte-identical sha `6507e798...`,
identical to the prior lane, and all 14 corpora regenerate `cmp`-clean.

## 3. WHAT THE LEARNER INDUCED

### 3.1 POSITIVE: the alphabet partition (verified against truth)

Measured by `p6_ladder.zag`, which links **only** the learner translation unit.

Set A, seed 1009, stage 0, all 220 records:

```
induced roles:  5=ATOM  11=ATOM  16=ATOM  19=ATOM  22=SEP  23=ATOM  28=ATOM
```

Independently derived true instance (`p6_inspect.zag`, world side, seed 1009):
atom tokens `{5,11,16,19,23,28}`, `SEMI = token 22`.

**They agree exactly.** The learner recovered the ATOM/SEP partition of an opaque
31-symbol alphabet from `(token sequence, one bit)` pairs, with no seed, no
grammar table, and no access to the checker. The predicates are:

- `rSEP` = the last symbol of some reduced VALID skeleton
- `rVAR` = occurs immediately after a delimiter opener
- `rATOM` = occurs as the first symbol of some reduced VALID skeleton, or
  immediately before an `rSEP`
- `rBINOP` = any remaining mid-skeleton symbol
- `rUNOP` = classified `rBINOP` but never preceded by an operand
- `rOUT` = occurs in INVALID but never in VALID, hence not in the language

This is the first time in this program that an opaque-token language's alphabet
partition has been recovered correctly from experience alone, and it is the one
substantive positive result of this lane. It also falsifies nothing and claims
nothing about syntax.

### 3.2 R1 delimiter discovery: implemented, finds nothing, and that is correct

R1 measures, for every ordered token pair, the support of the single-bracket-pair
hypothesis over VALID examples, then greedily maximises
`(consistentCount, maxDepth)`. It is a statistic, not a table.

**It finds 0 delimiter pairs in all 14 corpora**, and stage 6 has *fewer*
distinct tokens (16) than stage 5 (27). See section 4: the fixture contains no
nesting at any stage, so there is nothing for R1 to find. R1's behaviour is
correct; its input is empty.

### 3.3 R5 `(M, c, val)` solver: implemented, criterion satisfiable, search incomplete

Searches `M` over `{2,4,8,16,32,64}`, `c` over `[1,M-1]`, injective `val` over
the induced ATOM tokens, with prefix feasibility bucketed by max-atom-index and a
1024-slot failed-node memo. Returns the **full accepted set**, not the first
member, and reports its size as `GLOBAL-AMBIGUITY`.

Measured, set A stage 0, **with the true value map injected**
(`5→30 11→57 16→38 19→3 23→43 28→0`, `M=64`, `c=17`):

```
admissible records = 202 of 220   (125 VALID, 77 INVALID)
r5_viol(64, 17)    = 0
```

**So an accepting hypothesis EXISTS and the criterion is satisfiable by the
truth.** The solver run without injection returns `AMBIG=0` at all 14 corpora,
which means the search is failing to find a solution that demonstrably exists.

**This is reported as UNRESOLVED, not as GLOBAL-FAIL.** Claiming GLOBAL-FAIL here
would be exactly the reinterpretation-of-a-miss the prereg forbids, because I
have direct evidence the criterion is satisfiable. The defect is in my searcher,
not in the identifiability argument. K6 is UNMEASURED.

## 4. THE VOID FINDING: THE FIXTURE HAS NO COMPLEXITY LADDER

This is the reason no arm was scored, and it is stated openly rather than worked
around.

`p6_ladder.zag` over all 14 corpora, measuring the complexity each corpus
actually contains:

| set | stage | distinct tokens | max len | mean len | **R1 delimiter pairs** |
|---|---|---|---|---|---|
| A | 0 | 20 | 16 | 10 | **0** |
| A | 1 | 22 | 18 | 10 | **0** |
| A | 2 | 22 | 18 | 10 | **0** |
| A | 3 | 23 | 31 | 11 | **0** |
| A | 4 | 23 | 31 | 11 | **0** |
| A | 5 | 27 | 32 | 10 | **0** |
| A | 6 | **16** | 16 | 10 | **0** |
| B | 0 | 18 | 16 | 8 | **0** |
| B | 1 | 24 | 15 | 8 | **0** |
| B | 2 | 21 | 16 | 8 | **0** |
| B | 3 | 24 | 22 | 8 | **0** |
| B | 4 | 24 | 22 | 8 | **0** |
| B | 5 | 26 | 21 | 8 | **0** |
| B | 6 | 21 | 16 | 8 | **0** |

Stage 6's valid examples include `1XWXWQW]WXWFWQWQW` (16 tokens) and its longest
program is 16 tokens, with no `LP`, no `LET`, no `END`, no `IF`, no `PROC`. **The
ladder does not rise; it collapses.**

### Root cause, isolated

`p6_genprobe.zag` calls the world generator directly, with no dedup, no repair
and no corpus assembly, 400 draws per stage:

```
stage 0  avglen=4  checkerOK=6    nested=0
stage 1  avglen=6  checkerOK=16   nested=0
stage 2  avglen=6  checkerOK=12   nested=0
stage 3  SEGFAULT
```

`gp_prog` segfaults at stage 3. Narrowing: `gp_expr` survives 200 calls,
`gc_bind`/`gc_unbind` survive 300, `gp_stmts` at depth 2 segfaults within 200, so
the defect is in the `gp_stmts → gp_stmt → gp_let` block recursion. The LCG was
verified in-range for 60 consecutive draws, so the RNG is not the cause.

In the committed corpora the draw loop survives, but `cr_dup` de-duplicates: once
shallow programs saturate the 130-slot VALID budget, every deeper candidate is
rejected as a duplicate and the corpus fills with flat programs of slightly
greater length.

### Why this voids the ladder

K9 asks for the highest stage meeting K2. P6 predicts the ceiling is at stage 4 or
5 from scope/block interaction. P8 predicts R1 recovers `{LP,RP}` and `{LET,END}`
by stage 3. **None is measurable.** The pushdown representation exists precisely
to capture unbounded nesting, and the fixture provides nesting at **no** stage.
A complexity ceiling reported from this fixture would be reporting a generator
buffer bug as a fact about induction.

**Exploratory generator patches were written and then REVERTED.** The committed
world is byte-identical to `p6/formal-induce` and all 14 corpora still regenerate
`cmp`-clean. Repairing the generator would have silently changed the frozen
experience set this lane's prereg adopted.

## 5. TWO PRIOR-LANE CLAIMS CORRECTED (both measured, both disclosed)

**M1. `p6/formal-induce/REPORT.md` §3.2 is FALSE for set A.** It states "of the
six single-atom programs at stage 0, exactly one is valid". For seed 1009
(`M=64`, `C=17`, atom values `30,57,38,3,43,0`) **none** is valid — no atom value
is congruent to 17 mod 64. The VALID atom-count histogram at stage 0 is
`2:2 3:4 4:8 5:10 6:51 7:37 8:18`: there is **no 1-atom VALID example at all**.
The claim is true for set B (`M=16`, `C=1`, atom value 1 exists), which is
presumably where it came from. This matters because AMENDMENT 1 A2 rests on
1-atom VALID examples existing; for set A they do not.

**M2. Set A's modulus is not uniquely recoverable.** For `m=32, c=17` with the
true `val` map reduced mod 32, `VALIDviol = 0` and `GLOBALinvalid_sat = 0` at
every stage — it separates the corpus exactly as well as the truth `m=64`. `m=16`
fails (3 satisfied), `m=8` (13), `m=4` (14), `m=2` (32). For set B the true
`m=16` is the unique separator. So set A is recoverable only up to `{32, 64}`.
This is why K6 is preregistered to be reported twice: K6-PRIMARY as written
(`recovered modulus == true modulus`) **cannot** be met at set A by any learner,
and K6-SECONDARY (a separating triple, plus the size of the accepted set) is
supplementary and is not allowed to overwrite it. Both are UNMEASURED here.

## 6. FOUR MORE REAL DEFECTS FOUND IN MY OWN CODE

All four produced plausible-looking output rather than crashing. They are written
down because the symptom in each case was a number that looked like a result.

1. **Arena stride bug in the token alphabet.** Fields were addressed at
   `t_nv()+t*4` while seven fields were written at 4-byte spacing, so writing
   `role` for token 3 overwrote `nv` for token 4. Every role came out `rE()`.
   Fixed by giving the record a 32-byte stride (`TOKSTR()`).
2. **`r1_induce` left the closer-set table holding the last candidate it scored**
   rather than the accepted set, because the rebuild was placed after an early
   `return`. With `R1pairs=0` the table still classified token 23 as `rCLOSE`,
   which removed it from the ATOM set and left R5 with **5 atoms instead of 6**.
   The symptom was a plausible `nAtoms=5`.
3. **`r5_admissible` required strict ATOM/non-ATOM alternation**, which is wrong:
   an expression operand may be a prefix operator applied to an atom, so operand
   positions are not uniformly ATOM. It rejected **112 of 130** VALID records,
   leaving 68 of 220 admissible and making every violation count **vacuous** — and
   the truth-injected probe then reported a clean `viol=0`. An over-tight
   evidence filter does not produce a visible error; it produces a confident
   wrong pass. Replaced with: no `rOUT` token anywhere, and the record ends on a
   non-ATOM. After the fix, 202 of 220 admissible.
4. **Negative-strand MOD in the world's `lg_m32`**: `a-(a/b)*b` truncates toward
   zero and returns a **negative** remainder for `a<0`, and `lang_build` seeds the
   LCG with `lg_m32(seed, 9973)` which is negative for both frozen seeds. Not
   committed (the world was restored), recorded because the symptom is a
   plausible corpus rather than a crash.

The lesson, and it is the transferable part: **three of these four were
invisible without an explicit count of how much evidence a filter admitted.** That
count is now reported by `p6_gsolve`.

## 7. ABLATION (charter 226)

**Not run.** No arm was executed, so "does invalidity return when the learned
constraints are ablated" is UNMEASURED. No claim about constraint decorativeness
is made in either direction.

## 8. COMPLEXITY CEILING (charter 21)

**Not measurable, and the reason is a finding.** See section 4. The ceiling
cannot be reported from a fixture whose ladder collapses at stage 3.

## 9. ZERO-DIFF WIRING

**Not established, and not attempted to completion.** ZD-1, ZD-2 and ZD-3 are all
UNMEASURED because there is no generation path: R2/R3/R4/R6 were not written, so
there is no accept fold to census and nothing to ablate. The prior lane's
pre-committed label `ZD2-PASS-DEGENERATE-POLICY` is **not** claimed, because
ZD-2 was never evaluated.

For the record, the design commitment stands and is unchanged: the accept path is
specified as an unconditional conjunction of the induced structures, with no
guard deciding whether to consult any of them. If that is ever built and ZD-2
passes while the fold remains uniform, the verdict is
`ZD2-PASS-DEGENERATE-POLICY`, **not** closure. The missing invariant for real
closure remains **W4**: the learner inventing its own consult/keep policy. This
lane does not claim to close W4 and does not claim LW2.

## 10. VERDICT

**VERDICT: NO CLAIM. Prereg VOID. Primary objective not met.**

What is established:

(a) An opaque-token language's **alphabet partition is recoverable from
experience alone**, verified against an independently derived truth, with zero
seed/grammar/checker symbols in the learner TU (all six NAMECHECK greps = 0).
(b) A **pushdown representation** with hypothesis-free delimiter discovery,
role induction, and a bounded `(M,c,val)` solver is implemented and runs
deterministically.
(c) The **FL7 fixture contains no complexity ladder**, root-caused to a
segfault in the world's `LET`-block generator recursion plus dedup saturation.
The pushdown representation therefore has nothing to push down on this fixture.
(d) **Two prior-lane claims are false** (M1, M2), both measured.
(e) The prior lane's stated next step 2, the `(M,c,val)` solver, is implemented
and its identifiability treatment is sound: the criterion is satisfiable by the
truth, and my searcher does not find it.

What is not established: anything about generation quality, unseen-valid counts,
ablation, baselines, zero-diff wiring, or the complexity ceiling.

## 11. BOUNDARIES

- **No criterion K1-K10 and no prediction P1-P8 is evaluated.** Nothing here
  supports a capability claim about any learner.
- The family FL7 is researcher-authored (PREREG 1.1, K10). Only the instance is
  hidden, and only from the learner's translation unit.
- Instance derivation is deterministic given the seed, so the "hidden" instance is
  recoverable by anyone reading `p6_lang.zag` and the seed. Guards G1-G3 here are
  static separation plus behavioural checks, not cryptographic secrecy — the same
  posture as the program-wide pure-Zag shim.
- The corpus is near-miss negatives by world design; the learner is never shown an
  arbitrary invalid string.
- The R5 evidence filter (`r5_admissible`) is a researcher-chosen restriction on
  which examples count as evidence for the congruence. Its necessity is measured
  (18 inadmissible INVALID records otherwise become unsatisfiable for the truth),
  but the choice of filter is mine and is a boundary on K6.
- Seed A draws `M = 64`, the harder modulus. Not re-seeded, per the prior lane's
  boundary.
- **The fixture void is a property of the committed corpora, not of the learner.**
  Any successor must re-verify the fixture before drawing conclusions about
  induction.

## 12. NEXT EXPERIMENT (priority order)

1. **Repair the world generator's `LET`-block recursion** (`gp_stmts → gp_stmt →
   gp_let`), verify with `p6_genprobe.zag` that stages 3-6 emit real `LP`/`RP`
   and `LET`/`END` structure, regenerate the 14 corpora under a **new disclosed
   fixture version**, and only then re-run R1 and check it recovers the 4 bracket
   pairs the family uses. That is a new prereg, not a continuation of this one.
   **Nothing about induction is measurable until this is done.**
2. **Fix the R5 searcher.** The criterion is satisfiable (truth-injected
   `r5_viol(64,17)=0`); the search returns nothing. Prime suspects, in order:
   the memo key must include the full assigned prefix and be verified not to
   collide across distinct prefixes at the same depth; and the search should be
   re-checked against a hand-computed small case before being trusted on
   `M=64`. Report `GLOBAL-AMBIGUITY` only once the searcher is shown to find a
   known-present solution.
3. **Add an admissible-record count to every constraint's report**, not just R5.
   Three of my four bugs were invisible without it, and a filter that silently
   admits 18 of 220 records will look like a pass.
4. **Then** build R2/R3/R4/R6, `p6_check` as the only unseen-valid authority,
   `p6_stupid` (memoriser / uniform / bigram), and evaluate ZD-1/2/3 and the
   ablations. Only after that is a complexity ceiling a fact about induction.
5. Independently of the fixture: the **alphabet-partition result in section 3.1 is
   a real capability gain and deserves its own lane** — it needs no nesting, so it
   is testable on a repaired stage-0/1/2 corpus, and it is the piece of this lane
   worth carrying forward.
