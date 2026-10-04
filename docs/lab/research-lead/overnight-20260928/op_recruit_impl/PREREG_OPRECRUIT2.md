# PREREG: OP-RECRUIT v2 Implementation

Date: 2026-09-30.
Status: PREREGISTRATION. No implementation exists at commit time.
Design: `c6ef7ffcf` (`op_recruit/OPRECRUIT2_DESIGN.md`, 315 lines).
Lane: directive priority 2 (runtime operator recruitment and learner-authored semantics).

## 1. What is built

`oprecruit2.zag` (pure Zag): the GENEXEC2 VM (adapted from v1
`op_recruit.zag`) extended per the v2 design:

- Opcode range 32..63 with exactly one generic dispatch case.
- N-ary recruited ops: arity 1..4, pop/bind/push wrapper.
- Learner state: nrec, rec_idx[32], rec_arity[32], rec_len[32],
  rec_res[32], rec_buf[2048], rec_buf_top, rec_use[32],
  rec_idle[32], staging (stage_len, stage_arity, stage_buf[64],
  stage_valid), xorshift32 RNG state, program store (max 16
  programs, each max 32 ops), experience buffer (64 inputs).
- Learner consolidation routine: DETECT, PROPOSE, VALIDATE,
  RECRUIT, RETIRE. Called only by the test driver between tasks;
  the driver never invokes recruitment directly (F-DRIVER guard).
- New generic primitives IN2 (op 21) and IN3 (op 22), needed so
  recruited bodies can reference up to 4 bound inputs. These are
  generic VM primitives, not recruited semantics.

## 2. Frozen constants (disclosed, researcher-authored)

K_FREQ=3, COST_INSTALL=3, N_VAL=16, W_IDLE=3, MAX_STAGE_LEN=8,
MAX_OPS=32, REC_BUF_SIZE=2048, MAX_PROG_STORE=16, MAX_PROG_LEN=32.

## 3. Amendments to the design (transparent, pre-implementation)

A1. Wrapper disambiguation. Design 2.2 says "pop a values ...
bind them as in0..in(a-1); execute ... on a fresh data stack".
The worked example ([DUP, MUL] squares the stack top) requires
the popped values to be present on the fresh stack. Implemented
semantics: pop v[0..a-1] (v[a-1] was top); fresh stack is
initialized to [v[0], ..., v[a-1]]; in_k is bound to v[k] for
INk references; execute body; push back every value left on the
fresh stack (at most 4). Consequence, disclosed: IN0-style
bodies (e.g. the ABS program) retain their input on the stack,
so a recruited ABS-shaped op is 1-in/2-out with |x| on top.
Behavioral equivalence is checked on full stack contents.

A2. Staged subsequence length 2..8. Design 3.1 says 2..6;
design 5 (C0-B) says "2..8 instructions in staging" and the
stage_buf holds 8 instructions. 2..8 is implemented (needed
for the 8-op ABS body in R-V1).

A3. Candidate ranking tie-break. DETECT ranks candidates by
(max gain, max length, latest first-occurrence position,
lowest program index), all deterministic. Candidates are then
walked in rank order: the first candidate passing PROPOSE and
VALIDATE is staged; a PROPOSE/VALIDATE rejection moves to the
next candidate (STAGE_REJECTED / STAGE_INVALID events logged).

A4. CALL (op 19) is not allowed inside staged bodies
(STAGE_REJECTED). Rationale: inter-fragment control flow
breaks the stack-discipline simulation. Recruited ops
(32..63) ARE allowed inside staged bodies (hierarchical
composition); PROPOSE resolves them through rec_arity/rec_res.

A5. T-ADV is not run in this build. It requires a post-freeze
independent adversary; none is available to this builder.
The harness is structured so an adversary world can be
plugged in later. This is disclosed, not concealed.

A6. T-SELF(c) uses enumerative search, not beam search.
Metric: candidate evaluations to first exact solution,
enumerating programs by increasing length (1..5 control,
1..4 treatment) in fixed lexicographic primitive order.
If a task is unsolved within the length cap, evals are
censored at the cap total and reported as NOT-FOUND.

## 4. PROPOSE simulation (abstract interpretation)

For A in 1..4 (smallest first): reject if any INk with k>=A
appears. Worklist over (pc, d) where d is stack size relative
to A at entry. Per-op abstract effects with underflow guards
(d+A >= required). Jumps (JZ/JNZ/JMP) explore both targets;
visited (pc,d) pairs bound the search. Reject on: underflow,
CALL, multi-valued final d (data-dependent stack effect),
unbounded state growth. Accept: single final d on all paths.
arity = A, res = A + d_final (values pushed back, must be
1..4 else reject).

## 5. VALIDATE procedure

Provisional install of the staged body into the next free
slot (rec tables written, nrec incremented). Generate N_VAL
input tuples from the learner RNG and experience buffer.
For each tuple: INLINE = body bytes spliced as a main
program run on a pre-loaded stack through vm_run (not the
recruited dispatch); WRAPPED = single-op program [(32+ri,0)]
run through the real generic dispatch case. Require exact
full-stack equality on all N_VAL inputs. On failure: uninstall
(restore nrec and rec_buf_top), log STAGE_INVALID, try next
candidate. On success: keep the provisional install;
RECRUIT finalizes it (rewrite + RECRUITED log + clear staging).

## 6. RECRUIT rewrite and F-BREAK gate

Every program in the store: replace each occurrence of the
staged (op,arg) subsequence with (32+ri, 0). Before rewriting,
record each program's outputs on the fixed validation input
set; after rewriting, re-execute and require byte-exact match.
Any mismatch emits F_BREAK and fails the test.

## 7. RETIRE

At each consolidation episode end: for each ri, if
rec_use[ri]==0 then rec_idle[ri]+=1 else rec_idle[ri]=0;
rec_use[ri]=0. If rec_idle[ri]>=W_IDLE: re-expand every
(32+ri,0) occurrence to the stored body bytes in all
programs, compact the tables (slots above shift down,
opcodes rewritten), nrec-=1, log RETIRED(ri).

## 8. Test battery (each on fresh learner state, 3 runs)

R-V1 (regression, learner-driven ABS). Setup: 5 distinct
promoted programs, each = [IN0, ABS8, SUFFIX_i] where ABS8 =
[IN0 PUSH:-1 GT JZ:6 IN0 JMP:8 IN0 NEG] (v1's T1 solution
bytes) and SUFFIX_i are distinct tails. Stack alignment:
IN0 leaves the program input on top, so the recruited op is
behaviorally sound at that position. Bars: (a) a RECRUITED
event fires with no driver recruit call; (b) the recruited op
is behaviorally ABS-equivalent: top-of-stack equals |x| on
all 17 T1 inputs (x in -8..8); (c) SANITY [IN0, OP] scores
17/17 on T1.

T-NOFIRE (control). Setup: 6 promoted programs with pairwise
unique 2-grams (verified by construction). Bar: zero
RECRUITED events after consolidation. (F-SPURIOUS guard.)

T-SELF (shared squaring regularity). Setup: 5 distinct
promoted programs, each containing exactly one [DUP, MUL]
subsequence, with varied context so [DUP, MUL] is the unique
max-gain shared subsequence (freq 5, gain 2).
Bars: (a) RECRUITED fires within 1 consolidation episode;
(b) total program-store op count strictly decreases after
rewrite; (c) on held-out tasks H1 (x^2+x), H2 (2x^2),
H3 (x^2-1), enumerative search evals-to-first-exact-solution
is strictly lower with OP32 in the alphabet than without.
Alphabets: base = [PUSH:-1, PUSH:0, PUSH:1, PUSH:2, PUSH:3,
IN0, ADD, SUB, MUL, DUP] (10 ops); treatment adds OP32
(11 ops). Length caps: 5 control, 4 treatment. Episodes:
x in -4..4 (9 episodes).

T-ARITY2 (binary regularity). Setup: 5 distinct promoted
programs each containing [ADD, PUSH:2, MUL] exactly once,
varied context, unique max-gain. Bars: (a) RECRUITED fires;
(b) rec_arity of the new op == 2; (c) behavioral check:
[PUSH:3, PUSH:4, OP] leaves top == 14 on all of 9 probes
(a,b in -4..4 mapped deterministically).

T-RETIRE (distribution shift). Setup: recruit [DUP, MUL] as
in T-SELF, then 5 consolidation episodes whose program
stores contain no OP32 reference and no repeated
substructure. Bars: (a) a RETIRED event fires within
W_IDLE+2 = 5 episodes of the shift; (b) all program outputs
on a fixed 9-input probe set are byte-identical before and
after retirement; (c) nrec returns to 0.

T-ADV: NOT RUN (A5). Requires post-freeze independent
adversary.

## 9. Falsifiers (any one fails the corresponding claim)

F-SOURCE: source audit (shell grep) finds a dedicated
semantic case for a recruited meaning, or opcode literals
32..63 outside the single generic range check. Kills C0-A.
F-DRIVER: RECRUITED appears in any run where the learner
consolidation routine did not trigger it. Kills the
learner-authored claim. (Structural: only consolidate()
calls the install path; main() never does.)
F-BREAK: any program output changes after rewrite or
retirement. Kills mechanism soundness.
F-NOCOMPRESS: a recruited op does not reduce program-store
op count. Kills the utility claim.
F-NOSELF: T-SELF(a) does not fire within 1 episode.
Diagnoses detection inadequacy.
F-SPURIOUS: RECRUITED fires on T-NOFIRE. Diagnoses
criterion laxity.

## 10. Kill bars

K1: v2 implemented (generic dispatch, N-ary wrapper,
DETECT/PROPOSE/VALIDATE/RECRUIT/RETIRE, consolidation loop).
K2: battery run: R-V1, T-NOFIRE, T-SELF(a,b,c), T-ARITY2,
T-RETIRE all meet bars; T-ADV disclosed as not run.
K3: C0-A source audit passes (grep evidence in result doc).
K4: pure Zag (zero Python at every stage including scratch
and byte checks), zero em/en-dash bytes (shell-verified),
3/3 byte-identical runs (md5), exit 0.

## 11. Verdict rule

BUILD-PASS iff K1..K4 all pass with T-ADV explicitly
pending. BUILD-FAIL if any kill bar or falsifier fires.
No SURVIVES claim is made here: per the design, T-ADV plus
an independent governance audit precede any such discussion.
Honest scope (from the design): stronger bounded L2
structural, not L3; primitive alphabet, criterion family,
and thresholds remain researcher-authored.
