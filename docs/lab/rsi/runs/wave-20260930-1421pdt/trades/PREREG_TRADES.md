# PREREG_TRADES.md wave-20260930-1421pdt trades (FROZEN)

Status: FROZEN before implementation. Written before any implementation file exists.
Wave: wave-20260930-1421pdt. Lane: trades. Run-start tip: d5984f313.
Worker toolchain guard: Step 0 recorded in NAMECHECK.md; python3 exists at
/usr/bin/python3 (system runtime, cannot be removed); never invoked; pure Zag only.
Compiler lesson honored: u8-backed cells with get32/set32 helpers; no
`as *i32` plus slice construction inside functions.

## Survey (what the subsystems currently do)

Deliberation: CLA-2 (continuing learner, 7 primitives, ACT 5-step protocol,
signed evidence bids, miss-policy, P-INV trial discovery) and CAM-1
(PROPOSE -> VERIFY -> PROMOTE -> APPLY; trial-based P-DEP). CAM-1 P-DEP tries
exactly 6 fixed single-operation templates (COPY_A, COPY_B, DBL_A, DBL_B,
ADD_AB, LITERAL): depth-1 search only. VERIFY corroborates on holdback.
Nobody runs multi-hypothesis deliberation ensembles.

Search: P-DEP trial search is depth-1. Nobody has tried compositional
depth-2 or depth-3 trial search over the frozen {EQ, ADD} basis, because the
candidate count blows up combinatorially (depth-2: 416 candidates;
depth-3: about 174k candidates, each EQ-verified over exemplars).

Sensory: the sensory lane this wave covers image realism conditioning; that
territory is staffed separately and is out of scope for this lane.

## Candidate selected: DEEP-TRIAL

Compositional depth-2 trial search in the CAM-1 style PROPOSE -> VERIFY loop,
built only from the frozen generic basis (ADD, EQ; constants 0 and 1;
enumeration machinery). No new body kind, no new semantic case, no new
core op, no modes, no bridges, no handlers. Rationale: the PROTECTED CORE
ISA ruling explicitly approves compositional discovery from the generic
basis ("test whether the learner can construct and persist MUL from the
generic basis"); depth-2 ADD composition is that mechanism generalized,
and it is the cheapest untested way to spend compute for genuinely new
discovered rules. It does not collide with the mul_from_add lane (no MUL
families here; only repeated ADD composites). Expected information gain is
the highest of the surveyed options: it tests whether compute buys
capability that depth-1 cannot reach at all, which an ensemble robustness
test would not discriminate.

## Design (frozen)

Exemplar triples (a, b, z), u8-backed i32 cells. Per family: 6 construction
exemplars, 4 holdback exemplars, 5 novel probes. Deterministic generation
(no randomness): a_i = isub(i,13,3*i+1)... implemented via helper imod
(repeated subtraction; no % or / operators used).

Families:
- F1 COPY: z = a
- F2 ADD: z = a + b
- F3 DBL: z = a + a
- F4 COMP1: z = a + a + b (depth-2; depth-1 must abstain)
- F5 COMP2: z = a + b + 1 (depth-2; depth-1 must abstain)
- F6 NEG-RANDOM: fixed table of z values with no small ADD regularity
  (must abstain: 0 promotions)
- F7 NEG-SPURIOUS: construction follows z = a + a + b, holdback follows
  z = a + b (VERIFY must reject: 0 promotions)

Baseline (replicates CAM-1 P-DEP semantics): templates in priority order
COPY_A, DBL_A, ADD_AB, COPY_B, DBL_B, LITERAL (constant = first exemplar z).
A template becomes a candidate iff it holds by EQ on EVERY construction
exemplar. VERIFY: must predict every holdback exemplar exactly; failed
candidates are discarded.

Deep search: candidate trees over leaves {A, B, 0, 1}; depth-1 = ADD(l1,l2)
(16 trees); depth-2 = ADD(t1,t2) with t1,t2 in leaves plus depth-1 trees
(400 trees); plus depth-0 identities a, b. Enumeration is simplest-first.
Value-signature dedupe: a candidate whose 6 construction-exemplar output
values exactly match an already-tried candidate is skipped (pure EQ
comparison of value vectors; generic, not a semantic case). Same EQ trial
on construction exemplars and VERIFY on holdback as the baseline. Promote
the first (simplest) verified candidate; APPLY to 5 novel probes.

Cost accounting: trials counter incremented on every candidate-vs-exemplar
EQ check; printed per family and totals. Wall time measured by shell `time`
on the binary. State bytes = fixed buffer sizes, printed. No other cost.

## Frozen kill bars

K1 capability (BUILD-PASS requires): deep search promotes a rule on BOTH
F4 and F5 with 5/5 novel-probe accuracy, while the baseline promotes
nothing on F4/F5 (0 promotions, abstains). If deep fails either family,
BUILD-FAIL.

K2 no regression (BUILD-PASS requires): F1, F2, F3 reach 5/5 novel accuracy
under BOTH baseline and deep; F6 and F7 produce 0 promotions under BOTH.
Any miss, BUILD-FAIL.

K3 cost honesty (BUILD-PASS requires): trials printed per family and as
totals; deep/baseline trial ratio reported; wall time and state bytes
reported. Unmeasured cost, BUILD-FAIL. (Expected: baseline about 36 trials
per family; deep about 2500 per family; ratio about 70x.)

K4 architecture (BUILD-PASS requires): 0 new semantic cases (only ADD and
EQ evaluation, constants 0 and 1, enumeration machinery), 0 modes,
0 bridges, 0 handlers; cognition source lines added recorded. Any
violation, BUILD-FAIL.

K5 determinism (BUILD-PASS requires): 3 consecutive runs produce
byte-identical stdout (sha256 compared). Fail, BUILD-FAIL.

K6 purity: any python/python3 (or C/C++/JS/Rust interpreter) invocation
is automatic PROCESS-FAIL with immediate self-report in NAMECHECK.md.

Anti-gaming: constants are limited to 0 and 1 (no coefficient fitting);
trees are learner-side data evaluated only by ADD and EQ; sealed FW1-FW9
assets are untouched; the prereg precedes the implementation (creation
order in ORDER.txt); the coordinator commits centrally.

## Verdict labels

BUILD-PASS only if K1 through K5 all hold. Anything else is BUILD-FAIL
(with the specific failed bar named). Report includes the cost/capability
ratio: trials per promoted rule and trials per correct novel prediction,
baseline vs deep.
