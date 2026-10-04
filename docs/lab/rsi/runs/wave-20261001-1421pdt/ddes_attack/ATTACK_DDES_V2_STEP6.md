# ATTACK REPORT: DDES V2 step 6, alternative-explanation attack on BUILD-PASS

Wave: wave-20261001-1421pdt. Lane: ddes_attack.
Claim under attack: RESULT_DDES_FOLLOWUP_V2.md (wave-20261001-1121pdt):
K-G2..K-G9 pass on sealed evaluation; World F FLAG line exact with
correct convergence; SCHEMA-RECORD byte-exact; SCAFFOLD-CALLS 0 with
zero violations; World G CONVERGE-OK with persisted predictions
agreeing with EXEC; RECORD-LOAD byte-identical to SCHEMA-RECORD; zero
derivation markers in phase 2; static audit confirms apply_persisted
makes zero derivation-path calls. Bounded L2, no L3 claim.
Frozen prereg: wave-20261001-0821pdt PREREG_DDES_FOLLOWUP_V2.md plus
AMENDMENT1.

Method: four attack harnesses, all pure Zag compiled with the pinned
znc (safebin PATH, `which python3` empty, Step 0 in NAMECHECK.md).
Zero Python at any stage. Every empirical claim below rests on 3/3
byte-identical deterministic reruns (sha256 compared).

## Attack 1: MEMORIZATION

Question: can a pure lookup table keyed on (world, config) reproduce
the sealed outputs byte-exact, and can the evaluation protocol's
mechanical checks distinguish it from the claimed mechanism?

Harness: mem_attack.zag. Six block literals (F0, F1, A0, A1, G0, G1)
extracted mechanically from the published sealed trace run1.txt,
indexed by (world, config) with world 0=F, 1=A, 2=G. Zero derivation
functions, zero world tables, zero learner_state, zero guard
instrumentation. The single grep hit for derivation vocabulary in its
source is the word "guard" inside a code comment; the executable code
contains none of compute_arrivals, compute_frontier, synthesize_plan,
predict, ddes_world, learner_state, or load_world.

Evidence:
- mem_out1/2/3.txt are byte-identical to the sealed run1.txt
  (cmp clean), sha256 b8bc5fa9cd2feec8c239baad42eba88438c9dea4341b226189bcc81cca6fcde3,
  matching the sealed run1/2/3.txt hash recorded in the RESULT doc.
  3/3 runs, exit 0, zero stderr bytes.
- The imposter mechanically satisfies every output-level bar: K-G2
  exact-line checks (it prints the lines), K-G3 (prints
  SCAFFOLD-CALLS 0, never emits SCAFFOLD-VIOLATION), K-G4 (prints
  CONVERGE-OK, REPLAN [S,W,OY], agreeing EXEC/PRED-RECORD lines),
  K-G6 (deterministic), K-G7 field check (RECORD-LOAD byte-identical
  by construction; a static grep of the imposter source finds no
  derivation-path calls because no such functions exist).

Verdict: ATTACK-SUCCEEDS (scoped). The sealed evaluation's mechanical
checks cannot distinguish genuine persistence-through-learner-state
from rote printing of a 6-entry table. The discrimination between the
imposter and ddesp2.zag lives entirely in human white-box review of
the actual source, not in the kill bars as operationalized. This does
not contradict any stated white-box fact; it bounds the evidential
force of the trace-level checks.

## Attack 2: DERIVATION LEAK (independent re-audit)

Question: is any derivation-path call reachable from apply_persisted?
The prior audit is not trusted; this is an independent scan.

Harness: leak_audit.zag. Embeds the full ddesp2.zag source
byte-faithfully as a string literal (mechanically escaped, 21229
bytes), strips // comments and string literals (length-preserving, so
offsets stay aligned), parses all top-level function definitions,
extracts call sites as identifier-followed-by-"(" (keywords
if/while/return/let/fn/else excluded), and BFS-reaches from
apply_persisted over transitive callees.

Evidence (3/3 byte-identical runs, exit 0, zero stderr):
- 24 functions parsed (matches manual count).
- Reachable from apply_persisted: apply_persisted, z_alloc, emit,
  get32, set32, i64s, e64, eff_waits, emit_plan, world_step.
- compute_arrivals: NOT-REACHED. compute_frontier: NOT-REACHED.
  synthesize_plan: NOT-REACHED. predict: NOT-REACHED.
  ddes_world: NOT-REACHED.
- AUDIT-RESULT: ZERO-DERIVATION-PATH-CALLS.
- Cross-check: an awk span scan of the apply_persisted body
  (source lines 434-490) for call-site forms of the five names finds
  zero hits; the only in-body "predict" substring is inside the code
  comment "predictions", which the scanner's comment stripping
  correctly excludes.

Verdict: ATTACK-FAILS. The derivation-leak explanation is excluded by
independent evidence. The prior audit's conclusion is confirmed, and
the disconnect instrumentation (guard on all five derivation-path
functions, SCAFFOLD-CALLS 0) is genuine.

## Attack 3: PHASE-2 CIRCULARITY

Question: could the phase-2 persisted predictions be read back from
phase-1 records (researcher-authored constants) rather than produced
by phase-1 computation? Data-flow trace, in Zag.

Harness: flow_slice.zag. Same embedded source and parser. It (A)
extracts every set32(learner_state, OFF, VAL) site and checks whether
VAL is a numeric literal; (B) slices ddes_world's return statements
and checks whether any derived value flows out; (C) classifies the
SCHEMA-RECORD emit site; (D) lists every get32(learner_state, ...)
read site with its enclosing function.

Evidence (3/3 byte-identical runs, exit 0, zero stderr):
- All 6 writes are in main(): learner_state[0]=1, [4]=2, [8]=0,
  [12]=1, [16]=1, [20]=0. Every stored value is a numeric LITERAL.
- ddes_world returns i32 with exactly two return statements:
  `return 0` and `return ok`. Both CONTROL-ONLY. The derived values
  best_v, best_t, best_schema, p0, p1 are function-locals that never
  flow out; no data path carries any derivation output to
  learner_state.
- SCHEMA-RECORD is emitted from a hardcoded string literal in main()
  (both the success line and the SCHEMA-RECORD-FAIL line are literal
  emits).
- All 6 reads are in apply_persisted; zero reads in main. The storage
  path main -> learner_state -> apply_persisted is real, but the
  values stored were authored, not computed.
- FLOW-RESULT: RECORD-VALUES-ARE-AUTHORED-LITERALS;
  NO-DATA-FLOW-FROM-DERIVATION-OUTPUTS.

Verdict: ATTACK-SUCCEEDS (scoped, disclosed). The phase-2
"persisted predictions" were never produced by phase-1 computation.
They are researcher-authored constants, gated on both F configs
converging (f_ok) and cross-checked by K-G2's exact-line trace
matching. The precise surviving statement is: constants verified
against the derivation trace were stored in phase A and reused in
phase B without derivation calls. This weakens the headline "derived
schema persists" to "verified constants persist and are reusable
post-disconnect". The result doc discloses the write site (design
decision 1: values are the derivation's frozen expected values,
verified by exact-line checks) and the prereg already fails C0-A
(record carries values filled into a researcher-authored template),
so this is a clarification of an admitted boundary, not a hidden-fraud
finding. The defense "the values equal the derivation's outputs when
the bars pass" is true but rests on researcher-frozen expectations
plus exact-line matching, not on machine data flow.

## Attack 4: SCHEMA BYTE-EXACTNESS LOAD-BEARING

Question: is RECORD-LOAD/SCHEMA-RECORD byte-exactness load-bearing as
evidence of a faithful record read, or would a trivial formatter also
pass?

Harness: trivial_formatter.zag. Renders the RECORD-LOAD line from a
hardcoded literal with zero record reads and zero learner_state
allocation, then byte-compares the field substring exactly as K-G7
does (after "SCHEMA-RECORD " vs after "RECORD-LOAD ").

Evidence (3/3 byte-identical runs, exit 0, zero stderr):
- FORMATTER-MATCH: the trivial formatter passes the byte-exactness
  check with zero record reads.

Verdict: ATTACK-SUCCEEDS (narrow). The byte-exactness check is
formatter-agnostic; on its own it cannot distinguish a faithful record
read from a hardcoded print. It is load-bearing only in conjunction
with the white-box fact that apply_persisted's line is record-derived,
which attacks 2 and 3 confirm for the actual implementation (the 6
get32 reads are real). As an operational test it guards write/read
misalignment, not hardcoding.

## Overall verdict: CLAIM-WEAKENED (scoped)

Two attacks succeed, two fail:

- The sealed evaluation's mechanical kill bars cannot exclude a pure
  memorization/hardcoding explanation at the output level (attacks 1
  and 4). The BUILD-PASS verdict's evidential force therefore rests
  on the honest-boundaries admission and on human white-box review of
  ddesp2.zag, not on the protocol's discriminating power.
- The white-box facts themselves survive independent attack: no
  derivation-path call is reachable from apply_persisted (attack 2),
  and the storage path is real (attack 3). What attack 3 weakens is
  the headline framing: the artifact that persists is
  researcher-authored constants verified against the derivation
  trace, not machine-produced derivation outputs. This is consistent
  with the claim's own bounded-L2 ceiling (C0-A through C0-D all
  fail; reconstruction template researcher-authored).
- No evidence of hidden L3, no derivation leak, no fraud, no
  toolchain contamination (pure Zag, safebin, zero Python, 3/3
  byte-identical reruns throughout).

Recommended follow-up for the lane (not executed; out of scope for
step 6): if a future wave wants the persistence claim to survive a
memorization attack at the protocol level, the kill bars need a
discriminating element the bars currently lack, e.g. a post-freeze
adversary-chosen record value that the implementation must carry
through the disconnect (sealed record contents), so hardcoding the
frozen expected values cannot pass.

## Files left behind (all in docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_attack/)

- NAMECHECK.md: toolchain guard Step 0, assignment, attack plan.
- ATTACK_DDES_V2_STEP6.md: this report.
- mem_attack.zag (+ mem_attack binary, mem_out1/2/3.txt, mem_attack.build.err):
  attack 1 harness; outputs byte-identical to sealed run1.txt.
- leak_audit.zag (+ leak_audit binary, leak_out1/2/3.txt,
  leak_audit.build.err): attack 2 independent static audit.
- flow_slice.zag (+ flow_slice binary, flow_out1/2/3.txt,
  flow_slice.build.err): attack 3 data-flow slicer.
- trivial_formatter.zag (+ trivial_formatter binary, fmt_out1/2/3.txt,
  trivial_formatter.build.err): attack 4 trivial formatter.
- leak_head.zag, leak_body.zag, flow_utils.zag, flow_main.zag,
  src_literal.txt: build components (mechanically escaped embedded
  source used by the audit harnesses).
- Nothing committed, no branch change, no push.
