# P6 / FORMAL-INDUCE — REPORT

Lane `p6_formal_induce`, branch `p6/formal-induce`, base `504641745`.
Substrate read in full before starting: `docs/ops/ZAG_LANGUAGE_AND_WORKER_BRIEF.md`
(sections 2, 3, 7), `l2_compose_chain3/learner_frozen.zag` (1524 lines,
sha256 `698be75b19e3d9a85b3b308aa4d1e645cbb4e386169bcb47d8b20dfb93877731`,
confirmed), and ledger entries C205 / C283 / C289 / C397 / C459.

## 1. STATUS

**BUILD-PARTIAL. No new claim minted. The primary objective was NOT achieved.**

What is finished, verified, and committed:

- A complete, 3/3-byte-identical **world**: a seed-derived formal system (no
  grammar table in source), a true checker for it, a type-directed program
  generator, and 14 training corpora (2 instances x 7 complexity stages,
  220 records each = 130 VALID + 90 INVALID).
- A **source-level separation audit** proving the learner-side files contain no
  seed and no reference to the instance deriver or the true checker
  (`NAMECHECK.md`).
- A prereg, frozen alone, plus two disclosed pre-data amendments.

What is **not** finished: the learner. `p6_learner.zag` and `p6_induce.zag`
contain the state layout, the statistics passes, the closing-token model
selection, the separator induction and the role induction, but they were never
compiled, never executed, and the following are **absent**: the
depth-class-conditioned transition model, the operator/operand typing table,
the scope rule, the hidden global-constraint solver, the learner's own checker,
the learner's generator, `p6_train.zag`, the held-out verification driver
`p6_check.zag`, and the `p6_stupid.zag` baseline.

Because none of that ran, **no numbers are reported for any criterion**, and no
claim ID is minted. K0 passed for the world; K1-K10 are UNMEASURED.

## 2. COMMITS

| commit | content |
|---|---|
| `33f3f0b98` | PREREG alone (seeds, predictions, K0-K10, ZD-1/2/3 operationalised) |
| `34009b48f` | PREREG AMENDMENT 1 alone (pre-data): global constraint moved from NUM role to ATOM role; no bar moved |
| `57db6a94d` | PREREG AMENDMENT 2 alone (pre-data): supervision channel becomes a corpus file so guard G2 holds literally; no bar moved |
| `d8a71c009` | World: instance deriver, true checker, generator, corpus builder, 14 corpora |
| `4b10061bc` | Corpus reader + incomplete learner scaffold + NAMECHECK + build script |

Determinism evidence: `p6_gencorpus` 3/3 byte-identical stdout,
sha256 `6507e7985a6fb4ffd8293ebe0a1930247e8bc5bc1e9e09898b68e07c543868bd`.
Independently, regenerating all 14 corpora after the commit left every corpus
file **byte-identical** to the committed version (`git diff` empty), so the
artifacts are deterministic across builds, not just across runs.

## 3. RESULTS (what actually exists)

### 3.1 The formal system is genuinely hidden from source

FL7 instances are a pure function of one i32 seed. `p6_lang.zag` contains no
grammar, no production, no keyword byte-id, no type table; it derives all of
them at run time from an LCG. The two frozen instances:

| set | seed | modulus M | residue c |
|---|---|---|---|
| A | 1009 | 64 | 17 |
| B | 2027 | 16 | 1 |

For set A the derived instance has: 31 opaque byte tokens; keyword subroles
scattered over 8 distinct token ids; the comparison operator is token 10;
binary operator signatures drawn from `{NUM,STR,BOOL}^3`; a 2-tier precedence
split; and 6 atom tokens whose integer values are a seed-derived injection into
`[0,M)`, non-monotone in token id. None of that is readable from any source
file.

### 3.2 The hidden global constraint is real and stage-0 live

`sum of the values of all atom tokens == c (mod M)`. Verified directly: of the
six single-atom programs at stage 0, exactly one is valid for set A, and the
five failures all carry error code 4 (global) — not a syntax or typing error.
The learner has no channel that reports this; it is recoverable only from the
one label bit per example.

### 3.3 Supervision channel is exactly what the prereg specified

220 records per stage per instance, 130 VALID / 90 INVALID, INVALID examples
are single-token substitutions / deletions / insertions of a valid example,
construction deterministic from the seed, and the learner receives only
`(token sequence, one bit)`. Corpus files are committed so the exact
experience set is auditable.

### 3.4 Source separation verified

`NAMECHECK.md` section 2: across `p6_corpus.zag`, `p6_learner.zag`,
`p6_induce.zag`, the counts of seed literals, instance symbols
(`lg_ L_role L_val L_M L_C`), checker symbols (`ck_`), world-generator symbols
(`gp_ gc_ bd_`), role codes, type codes and keyword subroles are **all 0**.
This is guards G1 and G2 in their amended form, established statically.

## 4. THE PRIMARY QUESTION: DID THE LEARNER SELF-WIRE WITH ZERO-DIFF?

**No. Not attempted to completion, therefore not achieved, and not claimed.**

The precise answer to "why can the learner not currently self-wire", stated as
the honest deliverable the charter asks for:

1. **The gap is not a knowledge gap; it is an absent mechanism.** The learner
   has no executable generation path at all. There is nothing to wire. This is
   an incompleteness of my build, not a discovered invariant.
2. **The invariant that is missing is a shared acceptance/generation
   structure inside the learner.** PREREG section 5 committed to making the
   learner's generation routine and its acceptance routine read the *same*
   induced tables, so that "consulting the constraints" is not a call site but
   the generation rule itself. That design requires the induced structure to be
   usable in both directions (forward walk for generation, membership test for
   acceptance). The representation I committed to in the learner scaffold is a
   **statistical** one (bigram tables with back-off, a typing table, a scope
   rule, a value map). A statistical model is naturally usable forward but only
   probabilistically usable backward, so it does **not** give the shared
   structure the zero-diff argument needs. The representation has to be
   rewritten — toward productions / a stack-structured model — before ZD-2 can
   even be evaluated. That is the finding: **the zero-diff claim is not
   reachable from a statistical induction, only from a structural one.**
3. **Even a perfect structural induction would not settle LW2.** ZD-2 as
   preregistered can be satisfied by a degenerate "always consult everything"
   policy, which is researcher-authored. PREREG section 4 said this in advance
   and pre-committed the verdict label `ZD2-PASS-DEGENERATE-POLICY`. So the
   best available outcome tonight's design could have produced is *not* the
   C289 closure: it is "the learner's content is behaviour-constraining and the
   consult is unconditional, but the consult policy is still mine". The missing
   invariant for real closure remains **W4**: the learner inventing its own
   consult/keep policy. Nothing tonight moved W4.

## 5. WHAT WAS BUILT AND WHAT IS MISSING, FILE BY FILE

Complete and verified:
`p6_io.zag`, `p6_lang.zag`, `p6_ckcore.zag`, `p6_gencorpus.zag`,
`p6_gcmain.zag`, `p6_corpus.zag`, the 14 corpora, `p6_build_all.sh`.

Present but never compiled or run:
`p6_learner.zag` (state layout, list helpers, counters),
`p6_induce.zag` (statistics pass, closing-token model selection, separator
induction, atom/variable/assign/term-close/unary/binary role induction).

Missing: depth-class transition model; operator-x-operand typing table; bind
pattern and scope rule; the `(M, c, value-map)` solver; the learner's checker;
the learner's generator; `p6_train.zag`; `p6_check.zag`; `p6_stupid.zag`.
`p6_build_all.sh` therefore only exposes the `gcsource` and `corpus` targets,
and says so in its own header comment.

Note for the successor: `p6_induce.zag` contains two dead no-op expressions
(`if(aft(LS,a2,0)>=0){ }` and `if(l_get(LS,l_xt()+(a2*31)*4)>=0){ }`) left over
from the variable-token rule. They are harmless but must be deleted, and the
variable rule they sit in was never validated.

## 6. ABLATION (charter 226)

**Not run.** No arm was executed, so "does invalidity return when the learned
constraints are ablated" is UNMEASURED. No claim about constraint
decorativeness is made in either direction.

## 7. COMPLEXITY CEILING (charter 21)

**Unknown.** The seven-stage ladder exists as world machinery (stage gates in
`lang_build` and `ck_check`, and seven corpora per instance were generated and
committed), but no learner reached stage 0, let alone stage 6. The finding is
"not measured", not "broke at stage k".

## 8. TOOLCHAIN AND INFRA FINDINGS (new, reusable)

1. **`_zag_raw_syscall(1,1,ptr,len,0,0,0)` compiles, links and returns, but
   produces no stdout on this host/znc pair.** Verified twice, with both the
   `*u8` pointer form and the `(_zag_slice_ptr(b) as i64)` form used by every
   existing lane (`cycles_generalize/gc_base.zag:61`,
   `cogops_leadership_transition/c20_base.zag:53`). The house single-write
   rule was preserved by building the whole report in one buffer and emitting
   it with a single `_zag_print(b[0..c])`, which does work. **The brief's
   section 4 output rule as written does not function on this host; other lanes
   reporting successful `_zag_raw_syscall` output should re-verify.**
2. **`fn f(b:[]u8,i:i32)c:i32` is rejected** ("unexpected token at top level:
   `c`") — the cursor-returning idiom in the brief's house style must be spelled
   with an explicit `let c:i32=0;`.
3. Zag tolerates a call to a function defined later in the same file
   (`gm_probes` calls `gm_push`), despite the brief's "no forward
   declarations". Do not rely on it.

## 9. PROCESS DISCLOSURES (required by charter 4)

1. **A forbidden interpreter was invoked once, outside any experimental wave.**
   While editing a file I ran a shell line that contained the literal text
   `python3 -c x` as a stray token. That command was issued **without**
   sourcing `pure-zag.sh`, so the shim layer was not active; `/usr/bin/python3`
   and `/opt/homebrew/bin/python3` both exist on this host and it resolved to
   one of them, so a Python process almost certainly ran and executed the
   no-op `x`. No scientific computation was performed by it, it produced no
   output, and it happened before any corpus or artifact existed — but by the
   brief's rule ("if one runs during an experimental wave that is a
   PROCESS-FAIL") this is disclosed as a near-miss at the process level. It did
   **not** occur during an experimental wave. Everything reported in section 3
   was produced by pinned `znc` builds of Zag sources, verified by the
   `--rep 3` harness.
2. No other interpreter, compiler, or package manager was invoked. All
   statistics, generation and checking in section 3 are computed inside the
   Zag binaries.

## 10. FOUR REAL DEFECTS FOUND IN MY OWN CODE (bug log, for the successor)

All four produced *plausible-looking* output rather than crashes, which is why
they are worth writing down.

1. **`gp_term` returned a token index where the caller expected a token
   count.** Every generated program was garbage and every write past the array
   was out of bounds. Symptom: corpus of 115 records instead of 220.
2. **The rng `s <- s*s mod 46337` collapses into a short orbit.** It enters the
   quadratic-residue subgroup, so the whole corpus degenerated onto a handful
   of distinct programs. Symptom: "the learner induces almost nothing" — which
   would have been reported as a scientific finding if not debugged. Replaced
   with `s <- (s*40014 + 12345) mod 32749` (product stays under 2^31).
3. **Unbounded block nesting in the generator** (`LET`/`IF` recursing into
   themselves with no depth cap) segfaulted at stage 5. Capped at `d < 3`.
4. **Option-slot collision in the generator's term chooser**: three
   availability flags defaulted to `0`, so a token absent from one option set
   could be selected as if present, and `lg_rn(L,0)` divided by zero. Fixed
   with `-1` sentinels.

Plus a fifth that is a design bug rather than a code bug: **repairing the
modular constraint by appending one atom token whose value equals the residual
fails whenever the residual is not one of the six atom values** — which is most
of the time at `M = 64`, giving 78% repair failure and a corpus with only 18 of
130 valid. Replaced by a per-instance table that decomposes every residue in
`[0,M)` into 1-3 atom values (`bd_build`).

## 11. VERDICT

**VERDICT: NO CLAIM. `BUILD-PARTIAL`, primary objective not met.**

The zero-diff wiring question is **unanswered, not refuted**. What is
established: (a) a formal system with genuine, source-irreconstructible hidden
structure, including a live global modular constraint at stage 0, exists and
is reproducible; (b) an audited supervision channel and an audited
translation-unit separation exist; (c) the honest blocker is identified — a
statistical induction cannot support the shared generation/acceptance structure
that the zero-diff argument requires, and even a structural one leaves W4
(researcher-authored consult policy) open.

## 12. BOUNDARIES

- No criterion K1-K10 or prediction P1-P6 is evaluated. Nothing here supports a
  capability claim about any learner.
- The corpus is near-miss negatives by world design; the learner is never shown
  an arbitrary invalid string. Any future validity rate is a statement about
  near-miss discrimination.
- The family FL7 is researcher-authored (PREREG 1.1, K10). Only the instance is
  hidden.
- Instance derivation is deterministic given the seed, so the "hidden" instance
  is recoverable by anyone who reads `p6_lang.zag` and the seed. Guards G1-G3
  are static/behavioural separation, not cryptographic secrecy — same posture
  as the program-wide pure-Zag enforcement.
- Seed A draws `M = 64`, the hardest case for a learner that has to satisfy a
  modular constraint by search. That was not chosen for or against the learner;
  it is what seed 1009 derives. A successor must not re-seed to make the
  constraint easier without preregistering that as a bar change.

## 13. NEXT EXPERIMENT (in priority order)

1. **Change the learner's representation before writing any more induction
   code.** Replace the bigram model with an explicit production/pushdown model
   so that one induced structure serves both forward generation and acceptance.
   Concretely: bracket-pair discovery (already working, `pl_pickclose`), then
   recursive production induction over the resulting depth profile, then
   negative-consistency pruning so that no INVALID training sentence is
   derivable. That last property is also what makes charter-226 ablation
   meaningful. Do this before anything else; it is the load-bearing change.
2. **Finish the hidden-constraint solver as specified** (`(M, c, value map)`
   over 6 atom tokens, candidates `M in {16,32,64}`, `c in [1,M)`, unit
   propagation plus bounded search, all-different enforced). The identifiability
   argument is in PREREG AMENDMENT 1 A2: the constraint family is symmetric under
   `val -> c - val` for 1- and 2-atom programs, so the corpus must contain valid
   3+-atom examples and the solver must reject any hypothesis that only fits
   them.
3. **Build `p6_check` as a separate binary reading `p6_seed.txt`, `corpus.txt`
   and `p6_out.txt`.** It must be the only thing that decides unseen-valid, and
   it must also re-verify the unseen test (no artifact may match a training
   sequence) so the learner's own claim to "unseen" is not trusted.
4. **Build `p6_stupid` (memorizer) and `p6_stupid_raw` (uniform sampling).**
   Charter 8 requires them and K3 is meaningless without them.
5. **Only then** evaluate ZD-1 (cross-instance transfer with a byte-identical
   learner), ZD-2 (removable-wiring census over the real generation path) and
   ZD-3 (delete the unconditional fold, expect collapse). Pre-commit to
   reporting `ZD2-PASS-DEGENERATE-POLICY` if ZD-2 passes while the consult
   remains a uniform fold, exactly as PREREG section 4 already requires.
6. Re-verify the `_zag_raw_syscall` finding on a second lane, and fix
   `docs/ops/ZAG_LANGUAGE_AND_WORKER_BRIEF.md` section 4, which currently
   prescribes an output path that does not work on this host.
