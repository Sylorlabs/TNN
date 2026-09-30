# PREREG: C0INTEG Phase A Implementation

Date: 2026-09-30.
Status: PREREGISTRATION. No implementation exists at commit time.
Design: `9aa1fb0b5` (`c0_integ/C0INTEG_DESIGN.md`, 401 lines).
Lane: H-NEW-1 (C0INTEG Phase A, after OP-RECRUIT v2 landed).

Dependencies (all committed, verified present):
- `67a2c7e42` OP-RECRUIT v2 implementation (BUILD-PASS, non-adversarial battery; T-ADV pending).
- `1df644256` v2 prereg (frozen before v2 implementation).
- Q4 discovery substrate: `q4_impl/q4.zag` (beam, scoring, evidence, keep logic).

## 1. Phase split (frozen)

Phase A (this build): the integrated substrate.
- Tree evaluator with exactly one generic dispatch for recruited opcodes 32..63.
- Beam menu extension: base operators plus recruited opcodes.
- Learner consolidation routine: DETECT, PROPOSE, VALIDATE, RECRUIT, RETIRE over kept-variable trees, with the F-LEAK information barrier.
- Tests: T-RV1 (I1a), T-Q4REG (I1b), T-NOFIRE (I3), T-RETIRE, T-MENU.
- Hard gates: F-BREAK, F-LEAK, F-SOURCE, F-DRIVER.

Phase B (later worker, not this build): three-phase discovery runs
(Phase 1 base menu, consolidate, Phase 3 grown menu), I2, I4, I5
adversary. F-MENU and F-NOGAIN are frozen here as Phase B gates and
are not evaluated in Phase A.

## 2. Frozen constants (disclosed, researcher-authored)

K_FREQ=3, COST_INSTALL=3, N_VAL=16, W_IDLE=3,
MIN_FRAG_OPS=2, MAX_FRAG_OPS=6, MAX_ARITY=4,
MAX_REC=32 (opcodes 32..63), beam width 32, node bound 7,
complexity penalty 200 per operator node (0.02 on the *10000 scale),
keep margin 0.15, simplicity epsilon 0.02, N_VAL=16.

## 3. Architecture (frozen)

3.1 Tree DAG. Adapted from `q4_impl/q4.zag`: 28-byte nodes,
64-bit truth signatures (lo, hi) over the 64 X1..X6 input combos,
signature table dedup for base nodes. Terminals 0..5 = X1..X6,
6 = const 0, 7 = const 1. Base ops 0..3 = AND, OR, NOT, XOR.

3.2 Recruited bodies are trees, not stack programs. Adaptation of
v2 (which recruits GENEXEC2 instruction bodies) to the Q4 tree
substrate, per design 3.3 (DETECT over tree fragments). A body is a
node array with placeholder terminals P0..P(a-1). Evaluation binds
child values to placeholders positionally and evaluates the body
tree. This preserves v2's arity-generic (1..4) wrapper semantics;
the stack-polymorphism restriction (v2 A7) maps to: bodies contain
only base ops and placeholders, never raw program terminals (the
free terminals become the placeholders).

3.3 Exactly one generic dispatch point for opcodes 32..63 in the
tree evaluator. Recruited-op nodes are never signature-deduped
(always fresh nodes) so kept trees genuinely contain the recruited
opcode; their signature is computed by body evaluation on child
signatures (bitwise composition). Scoring counts a recruited-op
node as 1 operator node (design 3.2).

3.4 DETECT. For each kept tree, enumerate subtrees of 2..6
operator nodes containing no recruited-op nodes. Canonicalize by
renaming free terminals to P0..P(k-1) in first-appearance
pre-order. Count each distinct canonical shape once per kept tree
(design 9.2 over-counting guard). Candidates require freq >=
K_FREQ and gain = (ops-1)*freq - COST_INSTALL > 0. Rank by
(gain desc, ops desc, first occurrence asc), deterministic.
Growth-trace fragments are Phase B; Phase A uses kept trees only
(disclosed).

3.5 PROPOSE. arity = number of distinct free terminals in the
fragment. Reject if arity < 1 or arity > MAX_ARITY. Reject if the
fragment contains a recruited-op node (Phase A restriction,
disclosed).

3.6 VALIDATE. Provisional install of the staged body. Generate
N_VAL input tuples by cycling deterministically through the
experience buffer's observed x values. For each tuple: INLINE =
body tree evaluated with placeholders bound to the tuple's
terminal values; WRAPPED = recruited-op node applied to the
corresponding terminal nodes, evaluated at the tuple's x.
Require exact equality on all N_VAL tuples. On failure:
uninstall, try the next ranked candidate. The experience buffer
contains only learner-observed x values; the sealed function is
never queried by validation (F-LEAK barrier).

3.7 RECRUIT. Finalize install as opcode 32+nrec. Rewrite every
kept tree: replace subtrees matching the body pattern (consistent
terminal renaming) with recruited-op nodes. F-BREAK gate:
re-evaluate every kept variable on its validation inputs;
require byte-identical outputs pre/post rewrite. Log RECRUITED.

3.8 RETIRE. Each consolidation where a recruited opcode is not
referenced by any kept tree increments its idle counter; any
reference resets it. At idle >= W_IDLE, re-expand references
(none, by construction) and remove the opcode, log RETIRED.
F-BREAK gate on retire.

3.9 Consolidation is the learner's routine. The driver (main)
calls consolidate() between tests; consolidate() is the only
caller of the recruit path. No RECRUITED event is emitted by
driver code (F-DRIVER).

3.10 Beam menu extension. beam_extend gains one expansion class:
for each recruited opcode ri with arity a, form nodes from beam
candidates (arity 1: all beam nodes; arity >= 2: top 8 beam nodes
by score, bounding combinatorics). Candidate buffer enlarged
accordingly. With nrec=0 the beam is bit-identical to the base
beam.

## 4. Test battery (frozen)

T-RV1 (I1a, substrate recruitment). Synthetic kept store: 4 kept
trees, each containing the 3-operator fragment
OR(AND(P0,P1),AND(P0,P2)) under distinct terminal renamings;
experience buffer holds observed x = 0..15. Run consolidate().
Bars: at least one RECRUITED event; first recruited opcode is
32; arity 3; INLINE == WRAPPED on all 16 validation tuples;
F-BREAK passes (all kept trees byte-identical on validation
inputs after rewrite); reported gain = 5, freq = 4.

T-Q4REG (I1b, discovery regression). F-CONJ and F-XOR discovery
through the integrated binary with nrec=0 (base menu only).
Bars (from q4_impl KB1/KB2): true accuracy 64/64 on both;
keep margin >= 0.15 on both; kept opc <= 7; 3/3 byte-identical
runs.

T-NOFIRE (I3, no-fire control). Synthetic kept store: 4 kept
trees with no shared fragment at freq >= 3. Run consolidate().
Bars: zero RECRUITED events; F-CONJ discovery afterwards still
reaches 64/64 true accuracy.

T-RETIRE. After T-RV1, replace the kept store with trees that do
not reference op 32; run consolidate() W_IDLE times. Bars:
RETIRED fires for op 32; nrec returns to 0; F-BREAK passes on
retire.

T-MENU (dispatch and menu check). After T-RV1, seed a beam with
terminals and run one beam_extend. Bars: at least one candidate
node carries opcode 32; its signature equals the body-applied
signature (generic dispatch correct); A1 source audit passes
(see section 6).

## 5. Falsifiers (frozen; none weakened after this prereg)

F-SOURCE: any dedicated semantic case for a recruited meaning in
source (a branch naming what op 32+ means beyond the generic
dispatch). Kills the C0-A strengthening. Checked by source grep
in T-MENU.

F-DRIVER: any RECRUITED event not emitted inside consolidate().
Kills the learner-authored claim.

F-BREAK: any kept-variable output change on validation inputs
after rewrite or retirement. Kills mechanism soundness.

F-LEAK: validation or recruitment queries the sealed function
outside the evidence path, or reads a truth table not derived
from observed samples. Kills every claim from the run; the run
is VOID.

F-MENU (Phase B gate): the beam never expands a recruited opcode
in any Phase 3 run. Frozen here, evaluated in Phase B.

F-NOGAIN (Phase B gate): recruited ops never reduce node count,
interventions, or evaluations versus control. Frozen here,
evaluated in Phase B.

## 6. C0-A audit plan (Phase A)

A1 (no dedicated cases): grep the committed source for numeric
literals 33..63 in opcode position; require zero hits outside
the single generic dispatch (which references the range base 32
only). Reported in T-MENU.

A2 (learner-triggered): every RECRUITED event is emitted inside
consolidate(); the driver never calls the recruit path. Verified
by code inspection of the committed source, reported in the
result file.

A3 (sound rewrite): F-BREAK gate in T-RV1 and T-RETIRE.

A4 (disclosed residue): the beam scoring rule, keep margin,
complexity penalty, intervention-selection policy, detection
criterion family, and all section-2 constants remain
researcher-authored and are listed verbatim in the result file.

B1-B4 (grown menu) are Phase B; Phase A makes no C0-B claim.

## 7. Honest scope

Even with all Phase A tests passing and no falsifier firing, the
result is integration substrate, not a C0 strengthening: no
Phase 3 grown-menu discovery is run here, so C0-B is untouched
and C0-D reuse is not demonstrated. The ceiling is bounded L2
infrastructure. The detection criterion family, beam driver,
base alphabet, and all thresholds remain researcher-authored
(section 2, A4).

## 8. Governance

Pure Zag (znc plus shell and git only). Zero Python at every
stage including verification and byte checks (grep only). Zero
em/en-dash bytes in all committed docs (verified by shell grep).
3/3 byte-identical runs, empty stderr, exit 0. This prereg is
committed strictly before any implementation file; verify by
commit order (prereg commit is an ancestor of the implementation
commit). Pathspec commits on owned paths only
(`docs/lab/research-lead/overnight-20260928/c0integ/`). Nothing
pushed.

## Verdict: PREREG-COMPLETE (pending commit)
