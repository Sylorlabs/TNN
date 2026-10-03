# PREREG: Verify-H1 Integration (H1 learned typed contracts drive the verification loop)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
This prereg commit contains ONLY this PREREG.md. No kill bar below may be
weakened or reinterpreted after results are seen.

## Hypothesis

The composition_verify lane demonstrated a learner-owned verification loop
(commit with predicted outcome, world consequence, confidence update from
the consequence alone, later preference by earned confidence) with a
standalone parity-contract induction. H1 independently demonstrated typed
contract learning: I/O signatures (sig_in -> sig_out) induced from
observations via the kind probe (1=NODE iff value appears as a fact
subject, else 2=NUM), per-observation kind accumulation, and the majority
finalize rule (signature set once n>=2). The integration hypothesis: the
verification loop runs end to end with contracts produced ONLY by the real
H1 learning machinery. The learner commits to compositions whose predicted
outcome is computed from H1-learned signatures; a downstream world law
confirms or refutes; confidence moves on the consequence alone; a later
problem is solved by preferring the higher-confidence composition. No
harness expected answers anywhere; no hardcoded signatures anywhere.

## World (exact, frozen)

Facts, relation 91 (chain): (31,91,32), (32,91,33), (33,91,34).
Fact subjects: 31, 32, 33. Value 34 appears as object only.

Kind probe (real H1 logic): kind(v) = 1 (NODE) iff v appears as a fact
subject, else 2 (NUM). So kind(31)=1, kind(32)=1, kind(33)=1, kind(34)=2,
kind(35)=2, kind(2)=2, kind(12)=2.

Components (fixed true behaviors; the learner never sees these definitions,
only probe observations):
- C (id 0): chain-follow on r=91. C(31)=32, C(32)=33, C(33)=34, else -1.
- D (id 1): v+1. D(31)=32, D(32)=33, D(33)=34, D(34)=35.

Compositions (ids frozen): DD = (D,D) id 0; CC = (C,C) id 1.
Note the id assignment: the bad-history composition DD is id 0 so the
neutral tie-break (lowest id) favors it; the main arm must override the
tie-break by earned confidence (same reversal structure as the standalone
lane, where XD=0 was the tie-break default and XY=1 won by confidence).

Teaching observations (frozen probes; identical pairs for C and D, which
is the honest overgeneralization setup: D was probed only on 31,32):
- C: (31->32), (32->33).
- D: (31->32), (32->33).

H1 induction rule (exact copy of the l2_h1.zag logic, adapted only in
state layout):
- record_obs: in_sum += kind(vin); in_n += 1; out_sum += kind(vout);
  out_n += 1.
- finalize: if in_n>=2: sig_in=1, unless in_sum*2 >= in_n*3 then sig_in=2.
  Same for sig_out from out_sum/out_n.
- Signatures are written ONLY by finalize. Zero signature literals in
  source: no direct writes to signature cells outside h1_finalize.

Expected learned signatures (prediction P1): C: in kinds 1,1 (sum 2, n 2,
4>=6 false) -> 1; out kinds 1,1 -> 1. So C = 1->1. D: identical
observations -> D = 1->1. D's contract is overgeneralized: D's true
behavior on 33 gives 34 (NUM), outside the probed region. This mirrors the
standalone lane's D and is the honest error the loop must catch at the
composition level.

## Downstream world law (fixed, not per query)

The downstream machine accepts iff the final output kind equals the goal
kind. All three goals want NODE (kind 1), so the law is the fixed
statement "accept iff output is NODE". The gate latch is the only
consequence signal the learner may read. The learner never receives actual
output values; they appear in the transcript as labeled driver
instrumentation only.

## Phase plan (exact, frozen)

- TEACH: init world facts; observe C on (31,32) and (32,33); observe D on
  (31,32) and (32,33); finalize both; emit OBS lines (per-probe kinds) and
  TEACH lines (learned signatures).
- Z1: goal input=31, want NODE. Driver directs commit to CC. Contract
  prediction: kin=kind(31)=1 == sig_in(C)=1; seam sig_out(C)=1 ==
  sig_in(C)=1; predicted final kind = sig_out(C) = 1 = NODE. Commit
  recorded PENDING before execution. World executes: C(31)=32, C(32)=33.
  Downstream: kind(33)=1 -> gate=1 ACCEPT. Update: conf(CC) 0->1.
- Z2: goal input=33, want NODE. Driver directs commit to DD. Contract
  prediction: kin=kind(33)=1 == sig_in(D)=1; seam 1==1; predicted final
  kind = 1 = NODE (the learner genuinely predicts NODE; its D contract
  is wrong for this input). World executes: D(33)=34, D(34)=35.
  Downstream: kind(35)=2 -> gate=0 REJECT. Update: conf(DD) 0->-1.
- Z3: new problem, goal input=31, want NODE. Learner selects among
  contract-admissible compositions (kin==sig_in(first), seam
  sig_out(first)==sig_in(second), sig_out(second)==goal kind) by argmax
  confidence, tie -> lowest id. Both CC and DD are admissible.
  conf(CC)=1 > conf(DD)=-1 -> choice CC. Execute CC on 31 -> 33, gate=1.
  Update: conf(CC) 1->2.
- ABL: fresh learner state, fresh world, IDENTICAL teaching (contracts are
  required for admissibility; the only state difference vs MAIN is the
  empty confidence ledger and no commit history). Select for goal
  input=31, want NODE with the same selection function: both admissible,
  conf 0,0 -> tie -> lowest id -> choice DD. No execution; the selection
  alone is the evidence.

## Frozen predictions

- P1: TEACH lines read C sig=1->1 and D sig=1->1.
- P2: gate sequence over Z1,Z2,Z3 is 1,0,1.
- P3: Z3 SELECT choice=CC, rule=argmax-conf, confCC=1 confDD=-1.
- P4: ABL SELECT choice=DD, rule=tie->lowest-id, confCC=0 confDD=0.
- P5: final ledger conf(CC)=2, conf(DD)=-1.
- P6: 3/3 runs byte-identical.

## Kill bars

- K-VH-1 (H1 learns signatures from probes, real H1 logic): transcript
  TEACH lines show C=1->1 and D=1->1; OBS lines show the per-probe kinds
  consumed by the rule; source implements probe_kind (1=NODE iff fact
  subject else 2=NUM), per-observation accumulation, and the majority
  finalize (n>=2, sum*2>=n*3 -> kind 2); zero hardcoded signature writes
  (grep: no direct signature-cell writes outside h1_finalize; the only
  signature writer is the generic finalize step).
- K-VH-2 (commit with contract-predicted outcome): in run1.txt, both
  COMMIT lines show status=PENDING and precede their EXEC line which
  precedes their CONSEQUENCE line (line-number ordering); the COMMIT
  predicted value equals h1_predict computed from the learned
  signatures (contract chain shown on the line); Z1 predicts NODE for
  CC, Z2 predicts NODE for DD.
- K-VH-3 (world consequence confirms/refutes): the gate cell has exactly
  one write site in the program (inside world_downstream, the fixed
  accept-iff-NODE law); CONSEQUENCE lines read gate=1 after Z1 (actual
  33, NODE) and gate=0 after Z2 (actual 35, NUM), consistent with that
  law and with nothing else.
- K-VH-4 (confidence updates from consequence only): transcript UPDATE
  lines read (source=gate); the full learner_update body reads only
  world_gate, takes no actual output value, references no answer key,
  and is the sole writer of the confidence cells; grep -ci 'expected'
  over both sources returns 0; conf transitions are CC 0->1 (Z1),
  DD 0->-1 (Z2), CC 1->2 (Z3).
- K-VH-5 (later problem prefers higher-confidence composition): Z3
  SELECT line reads confCC=1 confDD=-1 choice=CC rule=argmax-conf; ABL
  SELECT line (same selection function, fresh ledger, identical
  teaching) reads confCC=0 confDD=0 choice=DD rule=tie->lowest-id;
  exactly one learner_select definition exists; the main-arm choice
  (id 1) overrides the neutral tie-break default (id 0).
- K-VH-6 (determinism): 3/3 runs byte-identical (sha256 equal, cmp
  pairwise).

## Architecture accounting (frozen constraints)

Pure Zag, safebin PATH, no Python (guard re-verified in build.sh). Zero
new modes, zero bridges, zero handlers, zero new opcodes, zero new
MAP/edge types (standalone program). The ABL arm is a driver-level entry
point calling the same selection function, not a mode. Output via one
preallocated buffer and a single raw syscall write (no _zag_print for
dynamic content). State cells u8-backed with little-endian pack/unpack
(no as *i32 slice construction).

## Known boundaries (not flaws in the claim)

- D's component contract stays wrong in learner state; the bars test
  composition-level verification (trust in (D,D) drops), not component
  contract revision. Contract revision is a separate experiment.
- (D,D) would in fact succeed on input 31; the Z3 preference for CC is
  earned distrust from Z2, which is exactly the learned-preference
  phenomenon under test, not objective per-input correctness.
- Toy scale; mechanism demonstration with frozen bars, not a generality
  or SURVIVES claim.
