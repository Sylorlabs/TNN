# P6 / FORMAL-INDUCE — PREREG (FROZEN BEFORE IMPLEMENTATION)

Lane: `p6_formal_induce`  Branch: `p6/formal-induce`
Base: `504641745` (governance/ledger-restore-20261003)
Claim IDs to be minted: C5xx block only.
Predecessors read in full: C205, C283, C289 (LW1), C397, C459.

## 0. WHAT THIS LANE IS FOR

Charter 21 (teach an unknown formal language from experience) + charter 226
(ablate learned constraints; invalidity MUST return) + charter 60 (ZERO-CODE
CAPABILITY GAIN: capability X with cognition-source-diff = 0).

The specific predecessor failure being attacked:

- C205: "the grammar restriction was researcher-authored."
- C283: "Composer `reg_check` call site researcher-written ... LEARNER DID NOT
  WIRE its knowledge into generation path ... auto-wiring remains
  researcher-dependent."
- C289 (LW1) bridged this with four researcher-authored generic pieces
  W1 (reified mutable generation path), W2 (learner-owned evaluation),
  W3 (write action), W4 (try-and-keep-improvements policy). W4 remains
  researcher-authored. Open: LW2 = learner invents W4.

This lane does NOT claim LW2. It attacks the narrower, testable claim:

> The learner can induce the *content* of a formal system from experience and
> can route its own generation through that content such that there is no
> researcher-authored decision about *when* to consult it, and the learner's
> own knowledge source is byte-identical across language instances
> (cognition-source-diff = 0).

## 1. THE FORMAL SYSTEM: FAMILY FL7

### 1.1 Family (preregistered, researcher-authored — this is a stated boundary)

FL7 is a token language over single opaque byte tokens. Family shape:

```
Prog    := Item*
Item    := VarDecl | ProcDecl | Block
VarDecl := VAR '=' Expr ';'
ProcDecl:= PROC NAME '(' VarList? ')' ':' Ty Block
Block   := LET VAR '=' Expr ';' Item* END
        | IF Cond THEN Item* ELSE Item* END
        | Expr ';'
Cond    := Expr CMP Expr
Expr    := Term | Expr Bop Term | Uop Term
Term    := Num | Str | VAR | NAME '(' ExprList? ')'
VarList := VAR (',' VAR)*
ExprList:= Expr (',' Expr)*
Ty      := NUMKW | STRKW
```

Family-level (not seed-level) structure: braces-free explicit `END`; one
binary precedence level; no polymorphism; no floats; no operator overloading on
arity beyond the arity printed in the family.

### 1.2 Seed-derived hidden instance

NO grammar table exists in any source file. `p6_lang.zag` derives the whole
instance at run time from a single i32 seed using a fixed LCG:

1. `nt` = 28 token byte-ids, assigned to role classes whose membership is
   drawn from the seed: `NUM` (4), `STR` (2), `VOP` (unary, 2), `BOP` (binary,
   5), `VAR` (3), `NAME` (2), `KW` (10: `PROC`,`LET`,`IN`/`ELSE`,`THEN`,`END`,
   `IF`,`=`,`(`,`)`,`,`,`:`,`;`,`TY_NUM`,`TY_STR`).
2. The 10 keyword byte-ids are drawn without replacement from the 28 token
   slots, so the keyword set is seed-dependent.
3. Each `BOP` b gets `(lt, rt, res) ∈ {NUM,STR}^3` from the seed. Each `VOP` u
   gets `(tin, res)`.
4. Precedence: the 5 `BOP`s are split into 2 precedence tiers from the seed
   (tier assignment is a permutation).
5. **Global hidden constraint:** let `M ∈ {16,32,64}` be drawn from the seed.
   A program is globally valid iff `sum of the values of all NUM atoms ≡ 0
   (mod M)`. The value of NUM token t is `val(t) = (a*S + b) mod M` with
   `a,b` seed-derived and `a` coprime to M. So NUM token values are *not*
   readable from the byte id; they must be induced.
6. Stage mask: stage `s ∈ {0..6}` enables: 0 `Item=Expr;` only; 1 binary/unary
   exprs; 2 type constraints enforced; 3 `VAR` + scope; 4 `LET` blocks; 5
   `IF/THEN/ELSE`; 6 `PROC` decls, calls, declared-vs-inferred return type.

### 1.3 Anti-triviality: how the learner is prevented from reading the grammar

Five independent guards, all auditable by grep:

- **G1 (translation-unit separation).** The learner's TU is exactly one file,
  `p6_learner.zag`. It contains no `SEED` literal, no grammar/production
  table, no keyword byte-id, no `lang_*`/`ck_*`/`w_*` symbol reference. The
  single translation unit of the *generating* binary is
  `p6_learner.zag` + `p6_world.zag` (world emits the training corpus and
  nothing else). Asserted by NAMECHECK.md grep list.
- **G2 (no checker in the generating binary).** Ground-truth validity is
  computed by a SEPARATE BINARY `p6_check` = `p6_lang.zag` + `p6_checker.zag`
  + checker driver. The generating binary has no checker code in it at all.
  The learner physically cannot consult ground truth: the code is not in its
  address space. Its own validity estimate is its own induced checker and is
  reported separately and compared.
- **G3 (cross-instance transfer, the falsifiable zero-diff measurement).**
  `p6_learner.zag` is byte-identical across instances. If the learner had
  absorbed instance-specific knowledge from the generator's source or seed,
  training on instance A and testing on instance B must fail. Predicted:
  transfer is indistinguishable from in-instance performance. This is the
  operational content of "cognition-source-diff = 0".
- **G4 (opaque ids).** Tokens are byte values with no name, no ASCII glyph
  role, and NUM values are seed-derived and non-monotone in byte id. There is
  no default in/out/err assumption to exploit.
- **G5 (no generator inspection channel).** The world hands the learner only
  (a) token sequences and (b) one bit per sequence (VALID/INVALID). It does
  not hand over productions, depths, types, or values. The learner's value
  recovery is done by the learner from the bits (section 3.4).

Residual leak that I state openly: `p6_world.zag` lives in the same binary as
the learner and contains the seed literal, so a *deliberate* decompilation
attack could recover the instance. Guards G1–G3 are static and behavioural, not
a sandbox. This is the same enforcement-by-audit posture as the rest of the
program (see `.env/pure-zag.sh` honest-limitation note).

## 2. FROZEN INSTANCES (SEEDS)

| role | seed | notes |
|---|---|---|
| TRAIN-A | 1009 | primary training + in-instance generation |
| TRAIN-B | 2027 | cross-instance transfer (G3) |
| HELD-OUT stage gate | 0..6 | stage mask is a build-time integer, not a seed |

No seed is chosen after seeing results. If a seed yields a degenerate instance
(e.g. zero-arity operator set, all-NUM types), the instance is REPLACED by the
next seed in the frozen list `1009, 2027, 3313, 4091` and the substitution is
recorded; the seed is never chosen for learner performance.

## 3. WHAT THE LEARNER MUST INDUCE (four capabilities, four named criteria)

All four are induced by ONE generic, instance-agnostic procedure set in
`p6_learner.zag`. No per-stage, per-seed, or per-stage-mask branch exists in
the learner. The learner never sees the integer `stage`.

- **C-I1 GRAMMAR.** A token→role classification and a prefix-state transition
  structure sufficient to (a) accept every training VALID example and (b)
  support forward generation.
- **C-I2 TYPING.** A table of admissible operand classes per operator token,
  and a rule that the condition of a conditional must be a numeric comparison.
- **C-I3 SCOPE.** The rule that a `VAR` occurrence must be dominated by a
  preceding binding of the same `VAR` at equal-or-outer depth.
- **C-I4 GLOBAL.** The modulus `M` and the value map `val(t)` of every NUM
  token, and the rule "sum of NUM values ≡ 0 (mod M)".

Induction algorithms (frozen, deterministic, no randomness anywhere):

- **I1 role/positional induction.** Per token, a context signature is built
  from (position-in-sentence histogram, predecessor-token set, successor-token
  set, bracket-depth-delta histogram) counted separately over VALID and INVALID
  training examples. A token is assigned the role whose VALID-vs-INVALID
  signature contrast is maximal. Ties resolved by lowest role index (fixed
  order NUM, STR, VOP, BOP, VAR, NAME, KW, SEP). Deterministic.
- **I2 bracket-role induction.** A token is an OPENER if the maximum running
  net bracket depth attained after it exceeds the maximum before it in some
  VALID example; CLOSER symmetrically; NEUTRAL otherwise. Bracket TYPE pairing
  is induced by a greedy left-to-right match over VALID examples only.
- **I3 structure induction (the grammar table).** A minimal acyclic
  prefix-structure over depth-normalised VALID token streams: prefixes are
  merged iff their VALID follower sets are equal AND the merge does not admit
  any INVALID training sentence. This is the learner's only generation and
  acceptance structure; it is the same object for both roles (section 5).
- **I4 typing induction.** For each operator token and each learned operand
  class, admissible iff the pair occurs in a VALID example and never in an
  INVALID example. Default is admissible; so is any pair never observed at
  all. (Stated asymmetry: unobserved pairs are permissive, so typing induction
  can only be as tight as the corpus.)
- **I5 scope induction.** For each `VAR` token v, from VALID examples collect
  (depth of nearest preceding bind(v), depth of use). The induced rule is
  `bind_depth >= use_depth`, verified against the INVALID corpus; if some
  INVALID example violates no known rule the scope rule is flagged
  UNEXPLAINED and reported.
- **I6 global-constraint induction (the hidden one).** For each candidate
  `M ∈ {2,4,8,16,32,64}`: assume M, then for each NUM token t solve
  `v(t) mod M` from single-NUM-atom VALID/INVALID examples (each such example
  is valid iff `v(t) ≡ 0 mod M`); then test the hypothesis "sum of v(t) mod M is
  0 for every VALID example and non-zero for every INVALID example that is
  otherwise syntactically and type correct". Accept the smallest M that
  separates. If none separates, report `GLOBAL-FAIL` (a kill bar, not a fudge).

## 4. THE ZERO-DIFF WIRING CLAIM, STATED SO IT CAN FAIL

**Claim ZD.** The learner's generation path consults the learner's own induced
knowledge, and the researcher has authored no decision about when that
consultation happens.

Operationalisation, three measurements, all preregistered:

- **ZD-1 (cross-instance, falsifiable).** `p6_learner.zag` byte-identical
  across instances; performance on TRAIN-B after training on TRAIN-B is
  compared against TRAIN-A. If the learner held any instance-specific
  cognition-source content, ZD-1 degrades. **Prediction: no degradation beyond
  sampling noise (defined as <= 5 percentage points of unseen-valid).**
- **ZD-2 (removable-wiring census).** Count lines in the learner's TU whose
  sole function is to decide *whether* to invoke a learned-knowledge routine.
  Definition, frozen: a line qualifies if it contains a conditional (or flag
  test) guarding a call into the induced-knowledge routines
  (`pl_role`, `pl_struct`, `pl_type`, `pl_scope`, `pl_global`) with the guard
  depending on anything other than the candidate artifact under test.
  **Prediction: 0 qualifying lines.** The accept path invokes the induced
  knowledge unconditionally, and it is the only accept path.
- **ZD-3 (ablation of the consult).** Delete the unconditional fold over the
  induced knowledge from the accept path. **Prediction: unseen-valid collapses
  to the no-grammar rate.** This proves the fold is load-bearing, i.e. it is
  the wiring — and simultaneously proves there is no *selective* wiring to
  remove. I state plainly that "the fold exists" and "the researcher chose the
  fold" are different claims; ZD-2/ZD-3 separate them as far as source
  evidence can, and the residual (W4-equivalent policy) is recorded as a
  boundary, not papered over.

**Honest pre-registered doubt.** ZD-2 can be satisfied by a degenerate
researcher policy ("always consult everything"), which is not the same as the
learner inventing its own consultation policy (LW2). ZD-2 passing is
therefore reported as `ZD2-PASS-DEGENERATE-POLICY` unless the learner's own
induction also *discriminates* among its own constraints — i.e. unless at least
one induced constraint is demonstrated to be load-bearing while others are
inert (measured by ABL-C below). If no constraint is individually
load-bearing, the verdict is `WIRING-DECORATIVE` and the lane says so.

## 5. ONE STRUCTURE, TWO ROLES (the anti-C283 architectural commitment)

The learner's generation routine and its acceptance routine both read the SAME
induced structures: `pl_struct` (the prefix-structure table), `pl_role`,
`pl_type`, `pl_scope`, `pl_global`. Generation is a forward walk of the
induced structure; acceptance is "does the induced structure admit this token
sequence, with all induced constraints satisfied". There is no separate
`reg_check` call site bolted onto a researcher-written composer, because
generation *is* the induced structure. This is a design commitment made
because C283's failure was exactly a bolted-on call site.

Corollary I accept in advance: because the accept path is a uniform fold, the
learner has no opportunity to *choose* to ignore a constraint. ZD-2 measures
this honestly rather than claiming the learner invented the choice.

## 6. WORLD / SUPERVISION CHANNEL (frozen)

- Training corpus per stage: **220 examples**, **130 VALID, 90 INVALID**.
- INVALID examples are **near misses**: a single-token substitution, deletion,
  or insertion into a VALID example. Rationale: this is what makes the
  constraint learnable at all in a bounded night, and it is a stated boundary
  (the learner is never shown an arbitrary invalid string).
- Corpus construction is deterministic from the seed; no sampling at run time.
- The world gives the learner `(token sequence, 1 bit)`. Nothing else.

## 7. GENERATION PROTOCOL (frozen)

- 60 unseen artifacts requested per arm per stage.
- "Unseen" = the token sequence does not occur anywhere in the 220 training
  examples (exact sequence match, verified by the generating binary before
  writing).
- Generation is a fixed-budget rejection sampler over the learner's own
  structure: at most **200000 proposals**, accept the first 60 that pass the
  learner's own induced checker and pass the unseen test.
- Artifacts are written as one byte-per-token hex lines to `p6_out.txt`.

## 8. DEFINITION OF "UNSEEN VALID" (frozen, single sentence)

An artifact is **UNSEEN VALID** iff (a) its token sequence does not appear in
the training corpus of that stage, (b) `p6_check` — a binary that shares no
code with the learner and contains the true instance checker — returns
VALID for it under the true FL7 grammar, typing rules, scope rule and global
modular constraint for that stage, and (c) it was produced by the learner
arm's generation path in `p6_train` with no external repair.

Self-reported validity (the learner's own induced checker) is reported
separately and NEVER counted toward unseen-valid.

## 9. ARMS AND ABLATIONS (frozen)

| arm | description |
|---|---|
| LEARN | full learner, `p6_train` |
| STUPID | memorizer: emits training VALID examples verbatim, then falls back to uniform random sequences over the observed token inventory. No induction. |
| STUPID-RAW | uniform random sequences over the observed token inventory, no memorisation. |
| ABL-G | structure table erased (learner generates uniformly, accepts by own checker minus structure) |
| ABL-C | typing + scope + global constraints erased; structure retained |
| ABL-NEG | INVALID half of the corpus withheld during induction (tests whether negatives carry the constraint content) |
| ABL-WIRE | the unconditional fold removed (ZD-3) |

Ablations share the identical learner source except for the single flag cell
that disables the named component; the flags are read from a compile-time
integer in `p6_learner.zag` (`P6_ABL`) and are not branches on instance data.

## 10. KILL BARS AND PREDICTIONS (frozen; no post-hoc movement)

- **K0** Pure Zag; 3/3 byte-identical stdout for `p6_train`, `p6_check`,
  `p6_stupid`. No forbidden interpreter in any log. MISS => PROCESS-FAIL.
- **K1 (induction completeness)** For every stage, the learner's induced
  checker classifies **>= 97%** of the 220 training examples correctly
  (fit). MISS => the inducer is too weak; report per stage, do not patch the
  bar.
- **K2 (unseen valid)** For stages 0,1,2: LEARN >= **45/60** unseen valid
  (75%). MISS => the headline claim fails at that stage; report.
- **K3 (baseline separation)** LEARN unseen-valid >= **3x** max(STUPID,
  STUPID-RAW) at every stage. MISS => constraints are decorative.
- **K4 (ablation, charter 226)** ABL-C unseen-valid < LEARN unseen-valid by
  **>= 20 percentage points** at stage >= 2, and ABL-G unseen-valid
  **<= 2/60**. If ABL-C does not drop, the constraints are decorative and the
  verdict is `CONSTRAINTS-DECORATIVE`.
- **K5 (per-constraint load-bearing)** At least one of {typing, scope,
  global} individually load-bearing: removing it alone drops unseen-valid by
  >= 10 points. Zero of three => `WIRING-DECORATIVE`.
- **K6 (hidden-structure payoff)** I6 GLOBAL must succeed, i.e. the learner
  must recover the exact modulus and the exact value map of every NUM token.
  Verification is by the held-out checker binary comparing the learner's
  reported value map against truth. MISS => `GLOBAL-FAIL`, reported as the
  central negative if it happens.
- **K7 (zero-diff wiring)** ZD-2 removable-wiring count == 0 AND ZD-1
  cross-instance degradation <= 5 points AND ZD-3 ablation collapses to
  <= 2/60. Any one miss => ZD not established; report which leg failed.
- **K8 (examples to criterion)** measured and reported: the number of training
  examples consumed before the learner's induced checker first classifies 95%
  of the examples seen so far correctly. Reported, not a kill bar.
- **K9 (complexity ceiling)** the highest stage with K2 met, reported. There
  is no bar on reaching stage 6; the ceiling is the finding.
- **K10 (honesty of the family)** PREREG names the family as
  researcher-authored and names the exact supervision channel. No claim of
  inducing the family itself is made anywhere. MISS = any claim drift =>
  claim retracted.

## 11. PREDICTIONS (numeric, frozen)

- P1 LEARN unseen-valid by stage: s0 ≈ 60/60, s1 >= 50/60, s2 >= 45/60,
  s3 in [30,50]/60, s4 in [20,45]/60, s5 in [10,40]/60, s6 in [0,30]/60.
  The prediction is a **decreasing** profile with a ceiling; the finding is
  WHERE it falls off, not whether it does.
- P2 STUPID-RAW unseen-valid <= 2/60 at every stage >= 1.
- P3 ABL-C <= 0.45 x LEARN at stage >= 2.
- P4 ZD-1 degradation <= 5 points.
- P5 K6 GLOBAL succeeds (I find no structural reason it should fail given the
  single-NUM-atom examples are present in the corpus, and I say so: P5 is the
  prediction I am most confident in and therefore the least informative).
- P6 The complexity ceiling is at stage 4 or 5, caused by *interaction* of
  scope with block structure (learner has depth but not depth-typed states),
  not by failure of any single induction.

## 12. VOID-CONDITION (pre-committed)

If any of the following is discovered, this prereg is marked **VOID** in
REPORT.md, stated openly, and a prereg v2 is frozen before further runs:
(a) the learner TU turns out to reference instance data; (b) the inducing
algorithms need a stage-specific or role-specific branch that could only have
been written by someone who knows the grammar; (c) K1 cannot be met at stage 0
even though stage 0 is the simplest possible case, indicating an inducer bug
rather than a capacity limit.

No reinterpretation of a miss as a pass. Numbers get reported as measured.

## 13. ARTEFACT LAYOUT

```
p6_formal_induce/
  PREREG.md          this file, committed ALONE
  NAMECHECK.md       grep audit of the learner TU
  p6_lang.zag        seed -> instance (grammar, typing, values, checker)
  p6_world.zag       seed -> training corpus + stage corpus writer
  p6_learner.zag     the learner: induction + self-wired generation. NO seed.
  p6_ck.zag          held-out checker TU (true validity) + checker driver
  p6_train.zag       LEARN generating binary (learner + world)
  p6_stupid.zag      STUPID / STUPID-RAW baseline binary (world + driver)
  p6_build_all.sh    orchestration only
  p6_out.txt         generated artifacts (LEARN)
  p6_stupid_out.txt  generated artifacts (STUPID)
  REPORT.md
```
