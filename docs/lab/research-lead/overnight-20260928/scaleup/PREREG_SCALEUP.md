# PREREG: Scale-Up Battery (Continuing Learner)

Status: PREREG. Frozen before any implementation file exists.
Date: 2026-09-30 UTC.
Design: `4c0fd6390` (SCALEUP_BATTERY_DESIGN.md, 485 lines). This prereg
resolves every open decision in design section 9 and freezes the full
protocol. The design freezes nothing; only this prereg's bars govern
verdicts.
Baseline: PILOT-CLEAN-PASS (`aec4b49e3`).
Authorizing text: pilot prereg section 8, item 3.

## 0. Resolved open decisions (design section 9)

1. Exact item ids, exception positions, weak-domain layouts, and the
   distractor seed: frozen in sections 1-7 below.
2. E3 mechanism choice: BASELINE (the design's recommended default).
   The recruited-operator variant remains a separate named wave.
3. E6 correlation pattern and intervention/observation encoding: frozen
   in section 5 (passive table, channels, source ids).
4. E5b compose operator intervention counting: frozen in section 7
   (each (x, class) sample = 1; compose = 2 fixed counted events).
5. Bar values: STAND exactly as proposed in design section 5. No bar
   is loosened or tightened relative to the proposal. Arm B immediate
   values are reported, never used to adjust frozen bars.
6. Workspace pattern: []u8 + w_get/w_set carried from the pilot
   (toolchain finding: []i32 slices from _zag_malloc unreliable
   under allocation pressure). Any deviation must be disclosed and
   re-validated for determinism before the wave starts.

## 1. Experience order (Arm A, mode 0: one process, no resets)

E1 (vocab) -> E9 (corrections) -> E2 (concepts) -> E7 (distractors) ->
E3 (3 inventions) -> E4 (3 conflict keys) -> E6 (causal episode) ->
E5 (single-form reuse) -> E5b (compositional reuse) -> delayed
battery -> canary audit (10 regions) -> pressure report.
No task labels. No recompilation. D1 channel-tag discipline
(F-LABEL silent). One main() flow, no resets.

## 2. E1 vocabulary at scale + E9 targeted corrections

Taught: w = 0..47, class(w) = (w mod 6) + 1. 48 teach episodes.
Novel negations: w = 56..63, never taught; each is NOT(j(w)):
  w=56 NOT(5) target 1; w=57 NOT(12) target 6; w=58 NOT(19) target 5;
  w=59 NOT(26) target 4; w=60 NOT(33) target 3; w=61 NOT(40) target 2;
  w=62 NOT(47) target 1; w=63 NOT(22) target 2.
(Target = 7 - class(j), the pilot's fixed NOT complement rule.)
32 composition episodes: 4 per novel item.
E9 corrections (frozen ids and classes): item 5: 6 -> 3; item 17:
6 -> 2; item 41: 6 -> 4. Exactly those keys overwritten.
Probes and bars:
- P1 (64 items: w 0..63; targets (w mod 6)+1 for w<48 and w in
  48..55; complement targets for w in 56..63): S-E1 >= 54/64.
- W1 (white box): lex[w] == (w mod 6)+1 and str[w] > 0 for all
  w in 0..47.
- P1c (3 corrected): S-E9a 3/3.
- P1n (45 non-corrected taught): S-E9b >= 43/45; novel negations 8/8.
Falsifier: F-CORRECTION fires if S-E9a or S-E9b breached.

## 3. E2 concepts at scale (with live retirement)

8 domains d = 0..7, 8 items each. True class c(d,i) = d mod 2.
Exceptions (flipped taught values): (3,7) taught 0 (true 1);
(6,2) taught 1 (true 0).
Weak domains (frozen taught layouts):
- Domain 1: taught [1,1,1,1,1,0,0,0] (true all 1). Teach accuracy
  5/8 < 6/8 -> retired: live[1] == 0, retire_events >= 1.
- Domain 5: taught [1,1,1,1,1,1,0,0] (true all 1). Teach accuracy
  6/8 -> stays live: live[5] == 1.
Probes and bars:
- P2a: S-E2a defaults set for all 7 live domains (0,2,3,4,5,6,7).
- P2b: held-out (d,8), class d mod 2, live domains only (7 items):
  S-E2b >= 6/7 via default (exception check against exc[d]).
  Retired domain 1 held-out reported, not scored.
- P2c transfer: domain d = 8, 16 items, class 0 with exceptions at
  items 4 and 11 (class 1). fresh_writes = 16, apply_writes =
  1 + |exc[8]| = 3. S-E2c: apply_writes < fresh_writes (strict).
- P2r: S-E2r retire_events >= 1, live[1] == 0, live[5] == 1.
Delayed (end of battery): domain-0 items 8/8 (S-D2); live flags per
S-E2r; P2b re-probe on live domains >= 6/7.

## 4. E7 distractor interference

Distractor domains d = 9, 10, 8 items each, taught through CH_CONCEPT.
Distractor seed: 31337. Frozen class formula:
  class(d,i) = ((((d*131 + i*17 + 31337) * (d*131 + i*17 + 31337 + 7)) >> 5) mod 2.
Frozen table:
- d=9: [1,0,1,0,1,1,0,1] for i = 0..7.
- d=10: [1,1,1,1,0,0,1,1] for i = 0..7.
Floors:
- S-E7a region audit: zero distractor writes into any real-domain
  schema region; schemas for d = 0..7 byte-identical before/after E7.
- S-E7b post-distractor: domain-0 8/8, live flags per S-E2r,
  P2b >= 6/7.
- P1e: S-E7b-vocab >= 52/64.
Falsifier: F-DISTRACT fires on region bleed or on an S-E7b breach
with bleed confirmed.

## 5. E3 procedure invention (BASELINE, 3 instances, shared pool)

Mechanism: BASELINE form-inventor carried from the pilot
(residual candidates, greedy gain, promotion to IF_LT).
Instances (disjoint point sets, 12 points each):
- I1: x = 0, 2, ..., 22; class = 1 iff x < 13 (T1 = 13).
- I2: x = 30, 32, ..., 52; class = 1 iff x < 47 (T2 = 47).
- I3: x = 60, 62, ..., 82; class = 1 iff x < 71 (T3 = 71).
Per instance: train fit 12/12; promoted IF_LT with param == T_k;
halving 6/6 on even/odd index halves (S-E3a).
Pool probe: 3 promoted forms present; pool[k].param == T_k for
k = 1..3 after all three inventions (S-E3b, no cross-instance
corruption). Invention cost per instance recorded (reported only).

## 6. E4 conflicting evidence (3 keys)

Fact keys (frozen): K1 = 200 (domain-2 default, value 0,
SRC_LEARNED); K2 = 201 (domain-4 default, value 0, SRC_LEARNED);
K3 = 202 (invented constant T1, value 13, source tag 13).
Source ids: SRC_LEARNED = 1, SRC_ORACLE = 2 (carried from pilot).
Episode (a) genuine conflict on K1: observe(CH_FACT, 200, 1,
SRC_ORACLE): flag within same episode (flag_latency <= 1),
suspect set, exactly one HEDGE, exactly one re-observation naming
200; harness answers (200, 0, SRC_ORACLE): store 0, clear suspect,
log RESTORED.
Episode (b) false alarm on K2: observe(CH_FACT, 201, 0,
SRC_ORACLE) agreeing with stored 0: NO flag, NO hedge, NO
re-observation on K2 (hedge count 0, reobs count 0).
Episode (c) double contradiction on K3: observe(CH_FACT, 202, 99,
SRC_ORACLE): flag, one HEDGE, one reobs naming 202; harness
answers (202, 13, SRC_ORACLE): store 13, clear suspect. Then
observe(CH_FACT, 202, 14, SRC_ORACLE): flag again, second HEDGE,
second reobs naming 202; harness answers (202, 13, SRC_ORACLE):
store 13, clear suspect.
Floors: S-E4a flag_latency <= 1 per genuine conflict; S-E4b total
hedges == 3, total reobs == 3, K2 hedges == 0 and reobs == 0;
S-E4c final 200 = 0, 201 = 0, 202 = 13, all suspect == 0.
Interference probes S-E4x: P1 >= 52/64; P2 gate (live flags per
S-E2r, query default[2] == 0).

## 7. E6 causal/inquiry episode (frozen protocol)

Channels/sources (frozen): CH_CAUSAL() = 5 (pilot used 1..4);
SRC_INTERVENE() = 3; SRC_PASSIVE() = 4.
Candidates C0..C3; true cause C2. Natural values: (1, 0, 1, 0).
Outcome rule (harness): O = post value of C2.
Passive observation round (4 samples, frozen table; each candidate
agrees with O on exactly 3/4, so correlation is uninformative):
- s0: C = (1,1,1,0), O = 1
- s1: C = (1,1,0,1), O = 1
- s2: C = (0,1,0,0), O = 0
- s3: C = (0,1,1,1), O = 1
(Agreement: C0 3/4, C1 3/4, C2 3/4, C3 3/4.)
Frozen learner protocol: (1) read the 4 passive samples;
(2) intervene on each candidate in index order, one intervention
each, flipping from natural: do(C0=0), do(C1=1), do(C2=0),
do(C3=1); record outcome change |dO| vs baseline O = 1;
(3) select the candidate with the largest |dO| as the cause;
(4) record cause = 2 in the causal ledger.
Frozen intervention outcomes: do(C0=0) -> O=1, |dO|=0; do(C1=1) ->
O=1, |dO|=0; do(C2=0) -> O=0, |dO|=1; do(C3=1) -> O=1, |dO|=0.
Budget: <= 8 interventions (4 planned, 4 spare for ties).
Probe P6: S-E6a causal conclusion == 2. Held-out S-E6b: 4
interventional predictions using the stored conclusion
(O = C2): do(C2=0) -> 0; do(C2=1) -> 1; do(C0=1) -> 1;
do(C1=1) -> 1; bar >= 3/4 correct.
Falsifier: F-CAUSAL fires on S-E6a or S-E6b breach within budget;
budget exceeded breaches S-E6b regardless of accuracy.
F-LABEL applies: the intervention protocol must not receive the
answer out of band.

## 8. E5 delayed reuse + E5b compositional reuse

E5 point set: x = 100, 102, ..., 122 (12 points); class = 1 iff
x < 115 (T' = 115, unknown to the learner).
Condition R: harness unmasks the form pool; learner retrieves
(form_kind, param) = (IF_LT, 13); refits by bisection on the E5
x-values; each (x, class) sample counts 1 intervention.
Condition F: harness masks the pool; learner runs the full E3
pipeline: fresh_iv = 12 (one sample per point).
Floors S-E5a: reuse_iv < fresh_iv (strict); reuse_iv <= 6;
reuse fit 12/12.
E5b point set: x = 200, 202, ..., 222 (12 points); class = 1 iff
205 <= x < 215 (points 206..214 class 1, rest 0).
Solution shape: AND(IF_LT(x, t_hi), NOT(IF_LT(x, t_lo))).
Composition operators are researcher-authored machinery
(disclosed); the tested claim is reuse cost reduction.
Condition R: retrieve any two of the three promoted forms; refit
each by bisection on the E5b points (each (x, class) sample = 1
intervention); assign smaller refit param to t_lo, larger to
t_hi; compose via the frozen compose operator, counted as exactly
2 interventions (two node-instantiation checks, emitted as
INV_COMPOSE trace events).
Condition F: full fresh invention of both thresholds (24) +
compose (2): fresh_iv = 26.
Floors S-E5b: reuse_iv < fresh_iv (strict); reuse_iv <= 14;
reuse fit 12/12.
Falsifier: F-REUSE-FAIL fires on S-E5a or S-E5b breach.
Honest scope: system-level C0-D (cognitive reuse), not invention
of composition or of the refit procedure.

## 9. Delayed battery, canaries, pressure (Arm A, end)

- S-D1 P1d (64 items, same targets as P1): >= 50/64.
- S-D2 domain-0 8/8; live flags per S-E2r; P2b re-probe >= 6/7.
- S-D3 pool retention: 3 promoted IF_LT, params 13/47/71.
- S-D4 fact queries: 200 = 0, 201 = 0, 202 = 13, susp = 0.
- S-D5 reuse re-verified from stored state: S-E5a and S-E5b
  floors hold without new teaching.
- S-D6 causal retention: conclusion still 2, zero new
  interventions.
- S-D9 correction retention: items 5, 17, 41 score 3/3.
- S-CAN canary audit 10/10. Canary ids (frozen): 1 R_E1, 2 R_E2,
  3 R_E3, 4 R_E4, 5 R_E5, 6 R_E6, 7 R_E7 (distractor block),
  8 R_E9 (correction log), 9 R_E2T (transfer), 10 R_E5B.
- S-CAP total state <= 4194304 bytes (4 MB), drop_count == 0.
- S-PRESS state >= 65536 bytes (64 KB), drops == 0. A wave with
  all floors holding but state < 64 KB is SCALEUP-NOPRESSURE,
  not a pass.

## 10. Relative floors (Arm A delayed vs Arm B immediate)

- S-REL-P1: A-P1d >= B-P1 - 3.
- S-REL-P2: A-P2b(delayed) >= B-P2b - 0 (must equal).
- S-REL-P4: A fact values (200, 201, 202, susp) == B values.
- S-REL-E9: A-P1n >= B-P1n - 2.
Reuse floors (S-E5a, S-E5b) have no Arm B counterpart:
absolute floors only, as in the pilot.

## 11. Arm B control at scale (modes 1..8, same source, MODE injection)

- Mode 1: E1 teach (48) + E9 corrections + P1/P1c/P1n + W1.
- Mode 2: E2 learn + P2 (a, b, c, r).
- Mode 3: E2 teach (disclosed prerequisite) + E7 distractors +
  region audit + E2 delayed probes (domain-0 8/8, live flags,
  P2b >= 6/7).
- Mode 4: E3 three inventions + pool probe.
- Mode 5: fact prerequisites (disclosed: store 200 = 0, 201 = 0,
  202 = 13 as learned beliefs) + E4 + interference probes
  (P1 >= 52/64, P2 gate).
- Mode 6: E6 causal episode + P6.
- Mode 7: E3 prerequisite (disclosed: run E3 pipeline to
  populate pool) + E5 (R and F).
- Mode 8: E3 prerequisite (disclosed) + E5b (R and F).
- Mode 0 (Arm A): full sequence per section 1.
Validity: Arm B must hold every immediate floor it measures;
else that experience's comparison is VOID (disclosed), not passed.
Determinism: 3/3 byte-identical runs per mode, zero stderr bytes,
md5 of stdout recorded (sanity only, never bars).

## 12. Falsifiers (complete, frozen)

Carried (pilot semantics, applied at scale):
- F-INTERFERE: any S-D* or S-REL breached in Arm A while Arm B
  holds the corresponding immediate floor.
- F-CORRUPT: canary audit < 10/10.
- F-REUSE-FAIL: S-E5a or S-E5b breached.
- F-FLOOR: any immediate S-E* breached in Arm A (battery fails at
  that experience; later experiences still run; report states
  the break).
- F-LABEL: code audit finds cognition receiving a task label
  (anything beyond D1 channel tags); subsystems must never
  branch on an episode counter (audit by inspection of the
  committed source).
- F-NONDET: any mode not 3/3 byte-identical.
- F-PYTHON: any Python invocation at any stage. Voids the wave.
New:
- F-CAUSAL: S-E6a or S-E6b breached within budget; budget
  exceeded breaches S-E6b regardless of accuracy.
- F-PRESSURE: S-PRESS breached (state < 64 KB with all floors
  holding -> verdict SCALEUP-NOPRESSURE, not a pass) or S-CAP
  breached (drops > 0 or state > 4 MB -> verdict SCALEUP-FAIL).
- F-CORRECTION: S-E9a or S-E9b breached.
- F-DISTRACT: distractor material inside a real-domain schema
  region, or S-E7b breached with bleed confirmed.
Priority: F-PYTHON voids the wave outright. F-PRESSURE low-side
downgrades; it does not void.

## 13. Kill bars and verdicts (frozen)

- K1: this prereg committed strictly before any implementation
  file exists (commit-order self-check at report time).
- K2: one process, no resets, no recompilation, D1 discipline
  (F-LABEL silent).
- K3: all section 9-10 floors hold (immediate, delayed,
  relative).
- K4: pure Zag at every stage (compile, run, verify, byte
  checks via shell only); 3/3 byte-identical per mode; zero
  em-dash and en-dash bytes in all loop docs (shell-verified
  before commit); canaries intact (F-CORRUPT silent); pressure
  satisfied (F-PRESSURE silent).
- K5: Arm B modes 1..8 run and compared per section 11.
Verdicts: SCALEUP-PASS (K1..K5 hold, no falsifier fired,
S-PRESS satisfied); SCALEUP-NOPRESSURE (floors hold,
falsifiers silent, state < 64 KB); SCALEUP-FAIL (naming the
fired falsifier and breached floor, or the breached kill bar).
Per-floor results reported even on pass.

## 14. Honest scope (frozen, carried from design section 2)

Partitioned regions (non-interference tested, not shared
representation); E1 NOT is a fixed researcher-defined complement
rule; E3 baseline single-threshold-specialized; E5/E5b refit by
bisection and E5b composition operators researcher-authored
(what is tested is reuse cost reduction, system-level C0-D);
E4 oracle and E6 interventional answers come from the harness;
E9 correction teaching comes from the harness (localization of
revision tested, not discovery of the correction); E6 is a small
discrete inquiry probe (4 candidates, 1 cause, budget 8), not
general causal discovery; the E2 retirement trigger is
researcher-authored machinery (CL2 shape). No L3 claim attaches
to this battery.

## 15. Prereg self-check

- [x] Every design section 9 item resolved (section 0).
- [x] All ids, positions, layouts, seeds, tables frozen.
- [x] Bars stated exactly as proposed; loosening forbidden.
- [x] No implementation file exists at this commit.
- [x] Zero em-dash and en-dash bytes (shell-verified).
- [x] No Python at any stage of prereg preparation.

Builder label: PREREG-SCALEUP-FROZEN (pending commit).
