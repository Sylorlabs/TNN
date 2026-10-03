# OP-RECRUIT v2 Design: Learner-Driven Runtime Operator Recruitment

Date: 2026-09-30.
Status: DESIGN ONLY. No implementation. No Python used at any stage.
Lane: directive priority 2 (runtime operator recruitment and learner-authored semantics).

## 1. Background and gap

OP-RECRUIT v1 (prereg `9d9c78cbd`, result RECRUITMENT-TESTED MIXED) built
ALLOCATE_OP on the GENEXEC2 VM and validated the C0-A substrate claim:
a recruited opcode's semantics can reside entirely in learner-created
bytes, executed by one generic interpreter case, with no dedicated
source case per recruited op. SANITY_OP32 scored 17/17.

v1 left four gaps that keep the semantics researcher-driven rather than
learner-authored:

1. `recruit_op` is invoked by the driver between tasks. The learner
   never decides to recruit.
2. The recruitment target (T1 ABS bytes) is fixed by the prereg and
   verified by byte comparison. The learner never detects what is worth
   recruiting from its own experience.
3. Recruited ops are unary only.
4. Program-invoked recruitment (self-extending opcode set at runtime, as
   a cognitive action of the learner) is future work.

v2 closes gaps 1, 2, and 3, and specifies 4 as the RECRUIT instruction.
The primitive alphabet, the detection criterion family, and the numeric
thresholds remain researcher-authored and are disclosed below. v2 is
therefore a stronger L2 structural mechanism, not an L3 claim.

## 2. Architecture

### 2.1 Persistent learner state (additions)

All of the following live in the learner's persistent state, written at
runtime by learner code, surviving save/load byte-identically:

```
nrec: u8                    # recruited op count, initially 0
rec_idx: [u16; 32]          # byte offsets into rec_buf
rec_arity: [u8; 32]         # inputs popped, 1..4
rec_len: [u8; 32]           # body length in instructions
rec_buf: [u8; 2048]         # flat bodies, GENEXEC2 fragment format
rec_buf_top: u16            # next free offset
rec_use: [u16; 32]          # per-episode usage counters
rec_idle: [u16; 32]         # consecutive zero-use episodes
stage_len: u8               # staged candidate length (0 = none staged)
stage_arity: u8             # staged candidate arity
stage_buf: [u8; 64]         # staged candidate body (max 8 instructions)
stage_valid: u8             # 1 after validation passes
```

Caps (32 ops, 2048 body bytes, 8-instruction staging) are generic, not
task-specific. Hitting a cap emits a CAP_REACHED event as an honest
signal; it is never silently ignored.

### 2.2 Generic interpreter case (the only source-side addition)

Opcode range 32..63 is reserved. Exactly one dispatch case exists:

```
op in [32, 64):
  ri = op - 32
  if ri >= nrec: NOP and log event NOP_DEAD_OP
  a = rec_arity[ri]
  pop a values from the data stack (missing values read as 0)
  bind them as in0..in(a-1)
  execute rec_buf[rec_idx[ri]] as a program on a fresh data stack
    and a fresh return stack, recursion depth guard 8
  push back every value left on the fresh data stack (at most 4)
  rec_use[ri] += 1
```

There is no case for any particular recruited meaning. The source never
names ABS, SQUARE, or any other recruited semantic. The C0-A audit is a
source grep: opcode literals 32..63 may appear only in the range check
above. If the learner recruits different bytes, the same opcode means
something else. Meaning is data, not source.

### 2.3 RECRUIT as a learner cognitive action

RECRUIT is a control-level instruction available to the learner's own
cognitive loop (the between-task consolidation routine), not to VM
programs and not to the driver. Its semantics are fully generic:

```
RECRUIT:
  require stage_len > 0 and stage_valid == 1, else NOP
  require nrec < 32 and rec_buf_top + stage_bytes <= 2048,
    else emit CAP_REACHED and NOP
  copy stage_buf into rec_buf at rec_buf_top
  rec_idx[nrec] = rec_buf_top
  rec_arity[nrec] = stage_arity
  rec_len[nrec] = stage_len
  rec_use[nrec] = 0; rec_idle[nrec] = 0
  rec_buf_top += stage_bytes; nrec += 1
  log RECRUITED(opcode = 32 + nrec - 1, arity, len, gain)
  rewrite the program store, replacing occurrences of the staged
    subsequence with the new opcode (section 4.4)
  clear staging (stage_len = 0, stage_valid = 0)
```

The driver never calls recruit_op in v2. If no RECRUITED event appears
in a run's trace, no recruitment happened. This makes learner-authored
recruitment falsifiable (falsifier F-DRIVER, section 6).

## 3. Learner-executed recruitment pipeline

All steps run in the learner's consolidation routine, in Zag, between
tasks. The researcher supplies the criterion family and the disclosed
constants; the learner computes everything else from its own experience.

### 3.1 DETECT: what is worth recruiting

```
for each promoted program P in the program store:
  for each subsequence S of P with 2 <= len(S) <= 6:
    freq[S] += 1            # counted once per distinct program
gain(S) = (len(S) - 1) * freq[S] - COST_INSTALL
candidates = { S : freq[S] >= K_FREQ and gain(S) > 0 }
if candidates nonempty: stage the S with maximal gain
```

This is an MDL-style compression criterion: recruit S when replacing
its occurrences with one opcode shrinks the program store. K_FREQ and
COST_INSTALL are frozen, disclosed researcher constants. The choice of
S, and whether any S qualifies, is computed by the learner from its
own promoted programs.

### 3.2 PROPOSE: arity by generic simulation

The staged body's net stack effect is computed by simulating it on
symbolic stack depths with the generic primitive semantics (the same
simulator the interpreter uses; no new semantics). arity = max depth
consumed, capped at 4. If simulation shows unbounded or data-dependent
effects, the candidate is rejected (STAGE_REJECTED event). Only
well-disciplined stack functions are recruitable.

### 3.3 VALIDATE: learner-generated behavioral equivalence

```
generate N_VAL test inputs from the learner's experience buffer
  using its own persistent RNG state
for each input x:
  out_inline = execute S as an inline instruction sequence on x
  out_wrapped = execute staged body through the pop/bind/push wrapper on x
  require out_inline == out_wrapped exactly
require N_VAL exact matches; else discard (STAGE_INVALID event)
set stage_valid = 1
```

The test inputs come from the learner's experience, not from a
researcher-supplied suite. N_VAL is a frozen, disclosed constant.

### 3.4 PROMOTE: install and rewrite

RECRUIT (section 2.3) installs the validated body and rewrites the
program store. After rewriting, the learner re-executes every rewritten
program on its validation inputs and requires exact output match
(falsifier F-BREAK guards this). The rewrite is what converts the
recruited op from a stored curiosity into cognitive reuse: subsequent
search and execution use the opcode.

### 3.5 RETIRE: revision of the operator set

```
at each episode end:
  for each ri:
    if rec_use[ri] == 0: rec_idle[ri] += 1
    else: rec_idle[ri] = 0
    rec_use[ri] = 0
    if rec_idle[ri] >= W_IDLE:
      re-expand programs referencing ri to the stored body bytes
      compact the table; log RETIRED(ri)
```

W_IDLE is frozen and disclosed. Retirement keeps the operator set
honest: an op that stops earning its keep is removed, and programs
remain correct because re-expansion is byte-exact. This satisfies the
revise/retire requirement for recruited structure.

## 4. Worked example

Tasks repeatedly reward programs containing [DUP, MUL] (square the
stack top). The learner's program store accumulates promoted programs
containing this subsequence. DETECT computes freq = 5, len = 2,
gain = (2-1)*5 - COST_INSTALL. With COST_INSTALL = 3, gain = 2 > 0 and
freq >= K_FREQ = 3, so [DUP, MUL] is staged. PROPOSE simulates: arity
1. VALIDATE: N_VAL = 16 inputs from experience; inline vs wrapped agree
16/16. The learner's consolidation routine executes RECRUIT: opcode 32
installed, program store rewritten, RECRUITED(32, 1, 2, 2) logged.
Later search treats 32 as one atomic choice; programs shrink; the
square operation is now a named, reusable cognitive object the
programmers did not supply as an opcode.

## 5. C0 mapping

- C0-A (runtime-defined semantics): strengthened relative to v1. The
  semantics of each recruited op reside in rec_buf, written by the
  learner at runtime. The recruitment decision (detect, propose,
  validate, recruit, retire) is executed by learner code. The source
  contains: the generic dispatch case, the generic RECRUIT instruction,
  the generic pipeline scaffolding, the primitive alphabet, and the
  disclosed constants K_FREQ, COST_INSTALL, N_VAL, W_IDLE, and the caps.
  No dedicated semantic case for any recruited meaning exists.
- C0-B (open structural form): bodies are variable-length compositions
  (2..8 instructions in staging, arity 1..4); the opcode set grows
  0..32 incrementally. The final operator inventory is not enumerated
  by the researcher.
- C0-C (multiple unforeseen forms): untested until the post-freeze
  adversary world (section 6, T-ADV). The design requires at least one
  adversary-designed family needing a materially different recruited
  op (different arity or different composition shape).
- C0-D (cognitive reuse): measured by program-store compression and by
  search-cost reduction on later tasks versus the frozen
  no-recruitment control (section 6, T-SELF).

## 6. Test battery (frozen design; to be preregistered before build)

- R-V1 (regression): the v1 T1 scenario, but recruitment must be
  learner-driven: no driver recruit call. Bar: a RECRUITED event for a
  behaviorally ABS-equivalent op (equivalence checked, not byte
  identity) and SANITY 17/17 through the recruited opcode.
- T-NOFIRE (control): a world with no repeated substructure across
  promoted programs. Bar: zero RECRUITED events. Guards against
  indiscriminate recruitment.
- T-SELF: a world whose tasks share a repeated [DUP, MUL]-shaped
  regularity (surface-varied so it is not literally the worked
  example). The driver never mentions recruitment. Bars: (a) a
  RECRUITED event fires within the frozen episode budget; (b)
  program-store size strictly decreases after rewrite; (c) mean
  search cost (candidate evaluations to criterion) on held-out later
  tasks is lower than the frozen no-recruitment control.
- T-ARITY2: a world whose shared regularity is binary (arity 2).
  Bar: recruited op has arity 2 and composes correctly in later
  programs (behavioral check).
- T-RETIRE: distribution shift makes a previously recruited op
  useless. Bar: a RETIRED event fires within W_IDLE + 2 episodes of
  the shift, and all programs produce byte-identical outputs before
  and after retirement.
- T-ADV: post-freeze independent adversary designs a world requiring
  a materially different recruited form. Bar: RECRUITED fires and
  C0-D reuse is demonstrated, or the failure is diagnosed in the
  trace (which regularity was detected, why none qualified).

Falsifiers (any one kills the corresponding claim):

- F-SOURCE: source audit finds a dedicated semantic case for a
  recruited meaning. Kills C0-A.
- F-DRIVER: recruitment fires only in driver-prompted runs and never
  in autonomous runs. Kills the learner-authored claim.
- F-BREAK: any program output changes after rewrite or retirement.
  Kills mechanism soundness.
- F-NOCOMPRESS: a recruited op never reduces program-store size.
  Kills the utility claim.
- F-NOSELF: on T-SELF, no RECRUITED event within budget. Diagnoses
  detection inadequacy (as v1 diagnosed search inadequacy).
- F-SPURIOUS: RECRUITED fires on T-NOFIRE. Diagnoses criterion
  laxity.

Global controls: pure Zag, zero Python at any stage including scratch,
zero em/en-dash bytes, 3/3 byte-identical runs, exit 0, prereg
strictly before implementation (verified by merge-base).

## 7. Honest scope and limits

- The primitive alphabet is researcher-authored. v2 composes and
  recruits; it does not invent primitives.
- The detection criterion family (frequency plus compression gain) is
  researcher-designed. The learner computes it but did not invent it.
  A learner that invents its own recruitment criteria would be a
  further step toward L3; v2 does not claim it.
- v2 does not invent the operator concept itself. Classification if
  built and passing: stronger bounded L2 structural, not L3.
- The wrapper discipline (pop/bind/push on fresh stacks) is
  researcher-designed; the v1 CALL-difference analysis carries over.
- Performance: fresh-stack allocation per recruited-op execution; no
  performance claim is made in v2.
- This document is a design. No implementation, no measurements, no
  verdicts are claimed here.

## 8. Recommended build order

1. N-ary wrapper plus generic dispatch, with R-V1 regression first.
2. Learner detection loop: T-NOFIRE control before T-SELF, so
   laxity is caught before utility is claimed.
3. Validation plus rewrite, with F-BREAK as a hard gate before any
   C0-D measurement.
4. Retirement (T-RETIRE).
5. Post-freeze adversary world (T-ADV), then the source audit and a
   governance audit before any SURVIVES discussion.

## 9. Kill-bar self-check

- K1 (recruitment mechanism specified): sections 2.3 and 3 specify
  detection, proposal, validation, runtime recruitment, and
  retirement at buildable precision.
- K2 (semantics in learner state, not source): sections 2.1 and 2.2;
  the audit criterion is a concrete grep; v1 already demonstrated
  the substrate pattern.
- K3 (execution via generic interpreter): section 2.2; exactly one
  dispatch case for the recruited range; the pop/bind/push wrapper
  is meaning-agnostic.

## 10. Relation to prior work

v1 (OPRECRUIT_RESULT.md, RECRUITMENT-TESTED MIXED) validated the
substrate: learner bytes as opcode semantics through one generic
case, with C0-D weakly positive and confounded by beam-search
pruning. v2 keeps the substrate unchanged and moves the recruitment
decision into the learner. The v1 recommendation (P1 Redesign as a
precondition for a clean C0-D retest) still stands and is now joined
by a second precondition: the learner must self-trigger recruitment
(F-DRIVER), which is itself a cognitive capability to be tested.
