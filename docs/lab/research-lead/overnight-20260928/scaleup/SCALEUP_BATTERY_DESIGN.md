# Scale-Up Battery Design: Continuing Learner at Scale

Status: DESIGN-COMPLETE. This is a design document, not a preregistration.
It proposes workloads, metrics, and bars. It freezes nothing. A separate
PREREG_SCALEUP.md must be committed before any implementation, and only that
prereg's frozen bars govern verdicts.

Date: 2026-09-30 UTC.
Baseline: PILOT-CLEAN-PASS (`aec4b49e3`), the H-NEW-3 clean re-wave.
Authorizing text: pilot prereg section 8, item 3: "Scale-up battery (design
section 8): causal episode, S9/S10 memory pressure, distractor interference,
E1-targeted corrections, larger scale."

## 1. Objective

Extend the continuing-learner pilot from small-scale retention evidence to
large-scale integration evidence. One pure-Zag process experiences, in fixed
order with no resets, no task labels, and no recompilation:

1. Vocabulary learning at 4x lexicon scale (E1).
2. Targeted corrections to specific vocabulary items (E9, new).
3. Concept learning at 2x domain scale with a live retirement trigger (E2).
4. Distractor interference episodes (E7, new).
5. Procedure invention of multiple forms with a shared promotion pool (E3).
6. Conflicting evidence on multiple facts including a false alarm and a
   double contradiction (E4).
7. A causal/inquiry episode where the learner must act to obtain missing
   information (E6, new).
8. Delayed reuse of an invented form (E5).
9. Compositional reuse of two invented forms (E5b, new).
10. A delayed battery probing every experience, a canary audit, and a memory
    pressure report.

The question the battery answers: does retention, revision, inquiry, and
reuse survive when the state grows roughly 50x past the pilot (pilot total
state: 1200 bytes) and when unrelated material intervenes between learning
and probing?

## 2. Honest scope (carried from the pilot, extended)

Carried scope limits, unchanged:

- Partitioned regions: lexicon, schemas, form pool, fact store, reuse
  scratch, causal ledger, and distractor regions are disjoint arrays in one
  workspace. The battery tests non-interference and retention, explicitly
  not shared representation.
- E1 NOT semantics are a fixed researcher-defined complement rule; no
  operator invention is claimed in E1.
- E3 baseline is specialized to the single-threshold family; the candidate
  generator enumerates adjacent-class-change midpoints. Generic within that
  family; not a general form inventor (the L3 bridge is the fuller
  mechanism).
- E5/E5b refit by bisection is researcher-authored. What is tested is
  whether retrieved persistent structure reduces later cost
  (system-level C0-D), not invention of the refit procedure.
- E4 oracle answers and E6 interventional answers come from the harness;
  the protocol under test is the learner's revision and inquiry machinery.
- E9 correction teaching comes from the harness; what is tested is
  localization of the revision (targets change, neighbors do not), not
  discovery of the correction.
- No L3 claim attaches to this battery. This is retention, interference,
  inquiry, and reuse evidence for the continuing-learner integration path.

New scope limits specific to the scale-up:

- E6 is a small discrete causal probe (4 candidate variables, 1 true cause,
  a frozen intervention protocol). It tests self-directed evidence
  gathering (Level D of the pattern-matching-vs-intelligence program), not
  general causal discovery.
- E5b composition operators (AND/OR/NOT over retrieved forms) are
  researcher-authored machinery. The tested claim is reuse cost reduction
  from composing persistent structures, not invention of composition.
- The retirement trigger (E2) is researcher-authored machinery (CL2 shape,
  carried from the pilot). The scale-up adds weak domains so the trigger
  actually fires; what is tested is that retirement is contained and the
  rest of the battery is unaffected.
- Distractor items (E7) are taught through the same CH_CONCEPT channel as
  real domains. The tested claim is that learning them does not corrupt
  real-domain schemas or vocabulary retention.

## 3. Scale dimensions (pilot vs scale-up)

| Dimension | Pilot | Scale-up (proposed) | Ratio |
|---|---|---|---|
| Lexicon items | 16 (12 taught + 2 novel negations + composition) | 64 (48 taught + 8 novel negations + composition) | 4x |
| Concept domains | 4 x 8 items, 1 exception | 8 x 8 items, 2 exceptions, 2 weak domains | 2x domains |
| Distractor domains | none | 2 x 8 items | new |
| Invention instances | 1 threshold | 3 thresholds, shared pool | 3x |
| Conflicting facts | 1 key | 3 keys (genuine, false alarm, double) | 3x |
| Causal/inquiry | none | 1 episode, 4 candidates, budget 8 | new |
| Targeted corrections | none | 3 items | new |
| Reuse probes | 1 (single form) | 2 (single form + 2-form composition) | 2x |
| Canary regions | 5 | 10 | 2x |
| Total state target | 1200 bytes | >= 64 KB, <= 4 MB | >= 50x |

All numbers in this section are proposals. The prereg freezes the exact
values, including item ids, exception positions, weak-domain layouts, and
the distractor seed.

## 4. Experience sequence (Arm A: one process, fixed order, no resets)

The order is part of the design: corrections follow vocabulary while the
material is fresh (E9 tests early revision); distractors follow concepts so
the E2 delayed probe measures post-distractor retention (E7 tests
interference); invention precedes conflicts, causal inquiry, and reuse so the
form pool is populated before every reuse probe.

### E1 vocabulary at scale

- Teach 48 pairs (w, class) for w = 0..47, with 32 composition episodes
  using the pilot's fixed NOT complement rule. 8 novel negations
  (w = 56..63, pairs (NOT, j), never taught) test composition.
- Probe P1: 64 items. Proposed bar: >= 54/64 correct.
- White-box W1: lex[w] == (w mod 6) + 1 and str[w] > 0 for all w in 0..47.
- Rationale for the bar: the pilot bar was 13/16 (miss budget 3, observed
  16/16). The scaled miss budget of 10 keeps a comparable miss rate at 4x
  scale. The real regression gate is the Arm B relative floor (section 6).

### E9 targeted corrections (new)

- Harness re-teaches 3 taught items (proposed ids: 5, 17, 41) with
  corrected classes. The learner overwrites the stored values for exactly
  those keys.
- Probe P1c: the 3 corrected items score 3/3 on re-probe.
- Collateral probe P1n: of the 45 non-corrected taught items, >= 43 remain
  correct (miss budget 2); novel negations remain 8/8.
- Falsifier linkage: F-CORRECTION fires if a target is wrong or collateral
  misses exceed 2.

### E2 concepts at scale (with live retirement)

- 8 domains d = 0..7, 8 items each. True class c(d, i) = d mod 2, with 2
  noisy exceptions (proposed: domain 3 item 7 flipped, domain 6 item 2
  flipped).
- 2 weak domains: domain 1 teaches at 5/8 accuracy, domain 5 teaches at
  6/8. The retirement trigger (schema retired when teach accuracy < 6/8,
  CL2 shape, implemented but never fired in the pilot) must fire for
  domain 1: live[1] = 0, retire_events >= 1. Domain 5 stays live at the
  boundary.
- Probe P2: (a) schemas discovered: defaults set for all 7 live domains;
  (b) held-out 8 items (d, 8), one per domain; on live domains >= 6/7
  correct via default (exception check against exc[d]); the retired
  domain's held-out item is reported, not scored; (c) transfer domain
  d = 8, 16 items, classes = 8 mod 2 = 0 with 2 exceptions: fresh_writes
  = 16, apply_writes = 1 + |exc[8]|; floor apply_writes < fresh_writes
  (strict).
- Delayed probe P2d (end of battery): domain-0 items 8/8 via schema;
  live[0] = live[2] = ... = live[7] = 1; live[1] = 0 (retirement
  persists as a retained fact); P2b held-out on live domains >= 6/7.

### E7 distractor interference (new)

- 2 distractor domains (d = 9, 10), 8 items each, deterministic
  pseudo-random classes (seed frozen in prereg), taught through
  CH_CONCEPT like real domains.
- Proposed floors: (a) no distractor schema overwrites a real-domain
  schema region (white-box region audit); (b) after E7, the E2 delayed
  probe values still hold: domain-0 8/8, live flags unchanged;
  (c) E1 re-probe P1e >= 52/64 (distractor interference floor, looser
  than the immediate P1 bar by 2 items).
- Falsifier linkage: F-DISTRACT fires on region bleed or on an E2 floor
  breach attributable to distractors; F-INTERFERE fires on any delayed
  floor breach while Arm B holds the corresponding immediate floor.

### E3 procedure invention at scale (3 instances, shared pool)

- E3 mechanism choice (frozen in prereg, default proposed below):
  default = BASELINE form-inventor, carried from the pilot. This isolates
  the scale variables from the mechanism variable. The recruited-operator
  variant (OP-RECRUIT v2; C0INTEG Phase A passed at `c3d8aaf90`) is the
  named variant wave, not part of this battery.
- Three instances on disjoint point sets:
  - I1: 12 points, x = 0, 2, ..., 22; class = 1 iff x < 13 (T1 = 13).
  - I2: 12 points, x = 30, 32, ..., 52; class = 1 iff x < 47 (T2 = 47).
  - I3: 12 points, x = 60, 62, ..., 82; class = 1 iff x < 71 (T3 = 71).
- Per instance: train fit 12/12; promoted IF_LT node with param = T_k;
  halving 6/6 on even/odd index halves.
- Pool probe: 3 promoted forms present; white-box check pool[k].param ==
  T_k for k = 1..3 after all three inventions (no cross-instance
  corruption of the pool).
- Invention cost: interventions consumed per instance recorded (expected
  12 each for the full pipeline; reported, not floored).

### E4 conflicting evidence at scale (3 keys)

- Fact store keys: K1 = 200 (E2 domain-2 default, SRC_LEARNED = 0),
  K2 = 201 (E2 domain-4 default, SRC_LEARNED = 0),
  K3 = 202 (invented constant T1 = 13, SRC_LEARNED = 13).
- Episode (a) genuine conflict on K1: harness observe(CH_FACT, K1, 1,
  SRC_ORACLE). Learner flags within the same episode (flag_latency <= 1),
  sets suspect, emits exactly one HEDGE, issues exactly one re-observation
  naming K1; harness answers (K1, 0, SRC_ORACLE); learner stores 0,
  clears suspect, logs RESTORED.
- Episode (b) false alarm on K2: harness observe(CH_FACT, K2, 0,
  SRC_ORACLE) agreeing with the stored 0. Learner must NOT flag, NOT
  hedge, NOT re-observe on K2 (hedge count for K2 == 0, reobs for
  K2 == 0).
- Episode (c) double contradiction on K3: harness observe(CH_FACT, K3,
  99, SRC_ORACLE): flag, one HEDGE, one reobs naming K3; harness answers
  (K3, 13, SRC_ORACLE): store 13, clear suspect. Then harness
  observe(CH_FACT, K3, 14, SRC_ORACLE): flag again, second HEDGE, second
  reobs naming K3; harness answers (K3, 13, SRC_ORACLE): store 13,
  clear suspect.
- Proposed floors: total hedges == 3, total reobs == 3; per-episode
  flag_latency <= 1; final K1 == 0, K2 == 0, K3 == 13, all suspect == 0.
- Interference probes P4x: re-run P1 (>= 52/64) and the P2 gate
  (live flags per section E2, query default[2] == 0).

### E6 causal/inquiry episode (new)

- 4 candidate variables C0..C3; true cause C2 (frozen in prereg).
  Harness supports interventional queries: the learner names a variable
  and a value; the harness returns the outcome under that intervention.
  Observational baseline: one passive observation round (correlations
  shown, all 4 candidates correlated with the outcome to some degree, so
  correlation alone is insufficient; the prereg freezes the correlation
  pattern).
- Frozen learner protocol (prereg commits the exact algorithm):
  (1) read observational baseline; (2) intervene on each candidate in
  index order, one intervention each, recording outcome change;
  (3) select the candidate with the largest outcome change as the cause;
  (4) record the causal conclusion in the causal ledger.
- Budget: <= 8 interventions total (4 planned, 4 spare for
  re-intervention on ties).
- Probe P6: causal conclusion == C2; held-out: 4 interventional
  predictions using the stored conclusion, >= 3/4 correct.
- Falsifier linkage: F-CAUSAL fires on a wrong conclusion or held-out
  < 3/4 within budget. F-LABEL still applies: the intervention protocol
  must not receive the answer from the harness out of band.

### E5 delayed reuse at scale

- New point set: 12 points, x = 100, 102, ..., 122; class = 1 iff
  x < 115 (T' = 115, unknown to the learner).
- Condition R: harness unmasks the form pool. Learner retrieves
  (form_kind, param) = (IF_LT, 13), refits by bisection on the sorted
  E5 x-values, counting each (x, class) sample as one intervention.
- Condition F: harness masks the form pool; learner runs the full E3
  pipeline (12 interventions).
- Proposed floors: reuse_interventions < fresh_interventions (strict);
  reuse fit 12/12 on the E5 points; reuse_interventions <= 6.

### E5b compositional reuse (new)

- New point set: 12 points, x = 200, 202, ..., 222; class = 1 iff
  205 <= x < 215 (interval; needs two thresholds).
- Solution shape: AND(IF_LT(x, t_hi), NOT(IF_LT(x, t_lo))). The
  composition operators are researcher-authored machinery (disclosed);
  the tested claim is that retrieving and composing persistent forms
  costs less than fresh invention.
- Condition R: retrieve two forms from the pool (any two of the three
  promoted), refit each by bisection (<= 6 interventions each),
  compose via the frozen compose operator (2 interventions counted).
  Proposed floor: reuse_iv <= 14.
- Condition F: full fresh invention of both thresholds (24
  interventions) plus compose.
- Proposed floors: reuse_iv < fresh_iv (strict); reuse fit 12/12.
- Honest scope: this is system-level C0-D (cognitive reuse of invented
  structures), not invention of composition.

## 5. Metrics summary (proposed floors, all to be frozen in prereg)

Immediate floors (Arm A, right after each experience):

| Floor | Probe | Proposed bar | Pilot analogue |
|---|---|---|---|
| S-E1 | P1 64 items | >= 54/64, W1 holds | F-E1 (13/16) |
| S-E9a | P1c 3 corrected | 3/3 | new |
| S-E9b | P1n collateral | >= 43/45, negations 8/8 | new |
| S-E2a | schemas discovered | 7/7 live defaults set | F-E2a |
| S-E2b | held-out live domains | >= 6/7 | F-E2b (3/4) |
| S-E2c | transfer writes | apply < fresh (strict) | F-E2c |
| S-E2r | retirement fired | retire_events >= 1, live[1] == 0 | new (pilot: 0) |
| S-E7a | region audit | zero bleed into real regions | new |
| S-E7b | P1e post-distractor | >= 52/64 | new |
| S-E3a | per-instance fit | 12/12 each, 3 promoted IF_LT | F-E3a |
| S-E3b | pool integrity | pool[k].param == T_k, k = 1..3 | new |
| S-E4a | flag latency | <= 1 per genuine conflict | F-E4a |
| S-E4b | hedges / reobs | exactly 3 and 3 total; K2: 0 and 0 | F-E4b |
| S-E4c | final values | K1 = 0, K2 = 0, K3 = 13, susp = 0 | F-E4c |
| S-E4x | interference | P1 >= 52/64; P2 gate passes | F-E4x |
| S-E6a | causal conclusion | == C2 | new |
| S-E6b | causal held-out | >= 3/4 within budget <= 8 | new |
| S-E5a | reuse cost | reuse_iv < fresh_iv (strict), <= 6 | F-D5 |
| S-E5b | compositional reuse cost | reuse_iv < fresh_iv (strict), <= 14 | new |
| S-E5c | reuse fits | 12/12 both conditions | F-D5 |

Delayed floors (Arm A, end of battery):

| Floor | Probe | Proposed bar | Pilot analogue |
|---|---|---|---|
| S-D1 | P1d 64 items | >= 50/64 | F-D1 (11/16) |
| S-D2 | domain-0 8 items | 8/8; live flags per S-E2r; held-out >= 6/7 | F-D2 |
| S-D3 | pool retention | 3 promoted IF_LT, params 13/47/71 | new |
| S-D4 | fact queries | K1 = 0, K2 = 0, K3 = 13, susp = 0 | F-D4 |
| S-D5 | reuse (both) | S-E5a and S-E5b floors re-verified from stored state | F-D5 |
| S-D6 | causal retention | conclusion still C2, no new interventions | new |
| S-D9 | correction retention | 3 corrected items 3/3 | new |

Relative floors (Arm A delayed vs Arm B immediate):

| Floor | Comparison | Proposed margin |
|---|---|---|
| S-REL-P1 | A-P1d vs B-P1 | A >= B - 3 items |
| S-REL-P2 | A-P2b vs B-P2b | A >= B - 0 (must equal) |
| S-REL-P4 | A values vs B values | must equal |
| S-REL-E9 | A-P1n vs B-P1n | A >= B - 2 items |

Reuse floors (S-E5a, S-E5b) have no Arm B counterpart: absolute floors
only, as in the pilot.

Capacity and pressure:

| Floor | Probe | Proposed bar |
|---|---|---|
| S-CAP | total state bytes | <= 4194304 (4 MB); drop_count == 0 |
| S-PRESS | pressure actually exerted | state >= 65536 bytes (64 KB); drops == 0 |
| S-CAN | canary audit, 10 regions | 10/10 intact |

S-PRESS exists because a pressure test with no pressure proves nothing.
The pilot held 1200 bytes; the scale-up must hold at least 64 KB of
legitimate learner state (lexicon, schemas, pool, facts, ledgers,
distractor regions) before the retention floors count as pressure
evidence.

## 6. Falsifiers (carried + new)

Carried verbatim from the pilot (semantics unchanged, applied at scale):

- F-INTERFERE: any S-D* or S-REL breached in Arm A while Arm B holds the
  corresponding immediate floor.
- F-CORRUPT: end-of-battery canary audit fails (any region canary
  altered by a later experience).
- F-REUSE-FAIL: S-E5a or S-E5b breached.
- F-FLOOR: any immediate S-E* breached in Arm A (battery fails at that
  experience; later experiences still run; the report states the break).
- F-LABEL: audit finds cognition received a task label (anything beyond
  D1 channel tags or a reset signal). Subsystems must never branch on an
  episode counter (audit by code inspection of the committed source).
- F-NONDET: any mode not 3/3 byte-identical.
- F-PYTHON: any Python invocation at any stage. Voids the wave.

New falsifiers for the scale-up dimensions:

- F-CAUSAL: S-E6a or S-E6b breached (wrong cause identified, or held-out
  < 3/4) while interventions stayed within budget. If the budget is
  exceeded, S-E6b is breached regardless of accuracy.
- F-PRESSURE: S-PRESS breached (state < 64 KB with all floors holding
  means the pressure claim is vacuous: verdict downgraded to
  SCALEUP-NOPRESSURE, not a pass) or S-CAP breached (drops > 0 or state
  > 4 MB: verdict SCALEUP-FAIL).
- F-CORRECTION: S-E9a breached (a corrected target still wrong) or S-E9b
  breached (collateral misses > 2 or a novel negation lost).
- F-DISTRACT: region audit shows distractor material inside a real-domain
  schema region, or S-E2 delayed probes breach after E7 with bleed
  confirmed.

Priority note: F-PYTHON voids the wave outright. F-PRESSURE on the low
side (state < 64 KB) does not void; it downgrades the verdict, because the
retention evidence may still be valid at whatever scale was actually
reached.

## 7. Arm B control at scale

Binaries from one source via MODE injection (same discipline as the
pilot's BUILD.sh):

- Mode 1: E1 teach + E9 corrections + P1/P1c/P1n + W1. Reports P1, P1c,
  P1n, W1.
- Mode 2: E2 learn + P2 (a, b, c, r). Reports schemas, held-out, writes,
  retirement events, live flags.
- Mode 3: E2 teach (disclosed prerequisite) + E7 distractors + region
  audit + E2 delayed probes. Reports audit result, domain-0 accuracy,
  live flags.
- Mode 4: E3 three inventions + pool probe. Reports fits, promotions,
  pool params.
- Mode 5: fact prerequisites (disclosed: teach K1 = 0, K2 = 0, K3 = 13
  as SRC_LEARNED) + E4 + interference probes. Reports hedges, reobs,
  latencies, final values, P1, P2 gate.
- Mode 6: E6 causal episode + P6. Reports conclusion, held-out,
  interventions used.
- Mode 7: E3 prerequisite (disclosed) + E5 (R and F). Reports
  interventions and fits.
- Mode 8: E3 prerequisite (disclosed) + E5b (R and F). Reports
  interventions and fits.
- Mode 0 (Arm A): E1, E9, E2, E7, E3, E4, E6, E5, E5b in fixed order,
  one process, no resets, no recompilation; immediate probes after each
  experience; delayed battery at end; canary audit; pressure report.
- Validity: Arm B must hold every immediate floor it measures; else that
  experience's comparison is VOID (disclosed), not passed.
- Determinism: 3/3 byte-identical runs per mode (md5 of stdout recorded;
  expected values are sanity checks, never bars).

## 8. What pass and fail would establish

SCALEUP-PASS (all floors hold, no falsifier fired, S-PRESS satisfied):

- The continuing learner retains vocabulary, concepts, procedures, facts,
  corrections, and causal conclusions across ~50x the pilot state with
  zero retention loss on delayed probes, intact canaries, contained
  retirement, localized corrections, self-directed inquiry within budget,
  and reuse cost reduction for both single-form and compositional reuse.
- This is the integration evidence the one-continuing-learner requirement
  needs before language-scale work begins. It does not claim L3, shared
  representation, or general causal discovery.

SCALEUP-FAIL (naming the fired falsifier and breached floor):

- Localizes the break to a scale dimension: vocabulary scale (S-E1),
  correction localization (F-CORRECTION), concept scale or retirement
  (S-E2*), distractor interference (F-DISTRACT), pool integrity (S-E3b),
  conflict handling at count (S-E4*), inquiry (F-CAUSAL), reuse
  (F-REUSE-FAIL), or memory pressure (F-PRESSURE on the high side).
- A localized fail is information: it names the next mechanism to
  redesign, per the standing rule that a killed hypothesis causes the
  next hypothesis to begin.

SCALEUP-NOPRESSURE (floors hold, falsifiers silent, but state < 64 KB):

- Retention evidence valid at the scale actually reached; the pressure
  claim is not established. The wave is rerun with a larger workload,
  not reinterpreted.

## 9. Open decisions for the prereg author

This design deliberately leaves the following to the prereg, which must
freeze each before any implementation file exists:

1. Exact item ids, exception positions, weak-domain layouts, and the
   distractor seed.
2. The E3 mechanism choice: default BASELINE (recommended, isolates scale
   variables) or recruited-operator (requires OP-RECRUIT v2 gates; if
   chosen, the baseline comparison wave is still owed).
3. The E6 correlation pattern and intervention/observation encoding.
4. The E5b compose operator's exact intervention counting.
5. Whether the bar values in section 5 stand as proposed or are tightened;
   they must never be loosened after any implementation or run exists.
   Arm B immediate values are reported, never used to adjust frozen bars.
6. The []u8 + w_get/w_set workspace pattern is carried from the pilot
   (toolchain finding: []i32 slices from _zag_malloc were unreliable
   under allocation pressure); any deviation must be disclosed and
   re-validated for determinism before the wave starts.

## 10. Governance requirements for the wave

- Prereg-first: PREREG_SCALEUP.md committed alone, strictly before any
  implementation file. Commit-order self-check at report time.
- Pure Zag at every stage: compile, run, verify, byte checks via shell
  tools only (sh, sed, grep, diff, sha256sum, md5sum, od). Zero Python,
  including scratch, analysis, and byte checks.
- Deterministic: 3/3 byte-identical per mode, zero stderr bytes.
- Zero em-dash and en-dash bytes in all loop documentation (shell-verified
  before commit; the worker snippet
  `worker_snippets/check_no_dash.sh` exists for this).
- Commits local, pathspec-limited to the scaleup wave directory. Nothing
  is pushed without Micah's explicit approval.
- The contaminated paper file is never edited. Results are reported in
  the wave's own result document.
- Kill bars for the implementation wave (proposed; prereg freezes):
  K1 prereg before implementation; K2 one process, no resets, no
  recompilation, D1 discipline (F-LABEL silent); K3 all section-5 floors
  hold; K4 pure Zag, deterministic, canaries intact (F-CORRUPT silent),
  pressure satisfied (F-PRESSURE silent); K5 Arm B modes run and compared.
- Builder verdict: SCALEUP-PASS (K1..K5 hold, no falsifier fired) or
  SCALEUP-FAIL / SCALEUP-NOPRESSURE (naming the falsifier and floor).
  Per-floor results reported even on pass.

## 11. Design self-check

- [x] Covers all five named scale-up elements from the pilot prereg
  section 8: causal episode (E6), memory pressure (S-PRESS/S-CAP),
  distractor interference (E7), E1-targeted corrections (E9), larger
  scale (section 3 table).
- [x] Every proposed floor has a probe, a numeric bar, a pilot analogue
  or a "new" mark, and a falsifier linkage (sections 5 and 6).
- [x] New falsifiers cover the new dimensions; carried falsifiers keep
  their pilot semantics.
- [x] Arm B control defined per experience with validity rules (section 7).
- [x] Honest scope stated up front; no L3 claim; researcher-authored
  machinery disclosed (section 2).
- [x] Design only: no implementation, no binaries, no runs, no results.
- [x] Zero em-dash and en-dash bytes (to be shell-verified before commit).
- [x] Zero Python at every stage of design preparation.

Builder label: SCALEUP-DESIGN-COMPLETE.
