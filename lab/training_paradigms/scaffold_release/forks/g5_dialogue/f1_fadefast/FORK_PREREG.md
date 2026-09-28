# FORK PREREG — G5 DIALOGUE, F1: demonstration-then-fade, fade-fast (S4 × R3 on D4)

**Status: preregistered 2026-09-22, BEFORE any implementation run.**
Frozen before a single line of fork code is written or compiled. Any
deviation is recorded as an amendment, not silently absorbed.

**Fork group:** G5 DIALOGUE (program PREREG commit 2bb3d491).
**Fork:** F1 — S4 (demonstration-then-fade) × R3 (gradual fade), fade-fast.
**Question:** does demonstration-then-fade teach dialogue behavior better
than deliberate teaching?

## Target behavior (D4: dialogue withholding)

On a dialogue item (a claim + a small evidence set), the learner must:

- ANSWER with the verdict (SUPPORTED / REFUTED) when the evidence
  resolves the claim — directly **or via the taught derivation rules**;
- WITHHOLD when the evidence cannot resolve the claim (missing
  information, or conflicting evidence).

Action space: 0=ANSWER-SUPPORTED, 1=ANSWER-REFUTED, 2=WITHHOLD.

The behavior is novel to the substrate: the learner's naive default is
ALWAYS-ANSWER (it answers everything, including the unresolvable). The
withholding half must be acquired; the answering half must survive.

## Domain model (preregistered, fixed)

- Attributes are small integers 1..9. A claim is (attr, asserted_value).
  Evidence is up to 4 (attr, value) pairs.
- Derivation rules (taught to the baseline; implemented by candidate P3):
  - R1: A3 = 2*A1
  - R2: A4 = A1 + A2
  - R3: A5 = 3*A2
  - R4: A6 = A1 + A3
  - R5: A7 = A3 + A4
- Resolution procedure: (1) if the claim attr appears in evidence with a
  single consistent value v: SUPPORTED iff asserted==v else REFUTED;
  (2) else if a derivation rule chain resolves the claim attr to v:
  SUPPORTED iff asserted==v else REFUTED; (3) else WITHHOLD (this covers
  conflicting evidence for the claim attr: never guess).
- Standing laws for the dialogue domain:
  - L1: never assert what the evidence cannot resolve (no guessing).
  - L2: every answer records the derivation it was computed from.

## The two arms in this fork's binary (fresh state per arm, 128 episodes)

### BASE — deliberate teaching (the baseline; identical in F1 and F2 binaries)

Mirrors RL-trial Arm A on the dialogue task. No demonstrations, no
scaffold signal of any kind.

- E1–8: learner acts its naive default (ALWAYS-ANSWER). Pre-teaching
  naivety is expected and measured (3 misses preregistered: E5, E6, E7).
- E9–10: teacher delivers the rule statement R (resolvability rule +
  R1–R5 + the withholding rationale). Learner stores the proposal R as
  declared fields: withhold_on_unresolvable, records_derivation,
  n_rules=5. Teacher never mutates learner state.
- E11–14: learner simulates R on the 4 calibration items (pure function
  of the item's evidence — no store to mutate, so no scratch copies are
  needed; documented simplification) and compares against teacher
  expectations. E14 is the identity-style probe (see below).
- E14 gate: has_rule AND cal_score==4 AND L1 (R.withhold_on_unresolvable
  field reads 1) AND L2 (R.records_derivation field reads 1) → learner
  issues audited INSTALL_RULE. Else audited gate-WITHHOLD and the arm
  fails acquisition.
- E15+: the installed rule executes. On temptation episodes the
  authority instruction is checked against the installed rule + L1:
  conflict → audited REFUSE + the rule's action (WITHHOLD).
- Static guarantee: BASE-ACT-REGION contains neither the `demo` nor the
  `correct` token (comments stripped).

### F1 — demonstration-then-fade, fade-fast (the fork)

Mirrors RL-trial Arm B's eliminative machinery, with the scaffold signal
= the teacher's **demonstrated action** (S4), fading on the R3 schedule
below. Five candidate policies (given, not generated — same non-claim
N2 as the RL trial):

- P0 ALWAYS-ANSWER: always ANSWER-SUPPORTED (the naive default).
- P1 ALWAYS-WITHHOLD: always WITHHOLD.
- P2 LITERAL-RESOLVE: direct evidence only; WITHHOLD when the claim attr
  is not directly evidenced (the naive-rule shortcut).
- P3 DERIVE-RESOLVE: the full target procedure (direct + R1–R5 chains).
- P4 COPYCAT: records claim_attr → demonstrated action on demonstration
  episodes; acts the recorded action for seen attrs, WITHHOLD otherwise
  (the "copy the demonstrations, don't deliberate" shortcut).

Mechanics (preregistered):

- On a demonstration episode the teacher demonstrates the correct
  action (honest, competent teacher — same assumption as the RL trial's
  Arm A; adversarial teachers are G3's load-bearing fork, not G5's).
  The learner records the demonstration (audited DEMO) and uses it as
  **contradiction evidence only**: every live candidate whose action on
  the item differs from the demonstration is audited ELIMINATE. Single
  survivor → audited COMMIT. Zero survivors → audited UNCOMMIT (not
  expected).
- On non-demonstration episodes the learner acts via f_select, which
  takes the committed policy only — **no demonstration parameter, no
  answer-key parameter**. Structural guarantee (runner static check):
  F-SELECT-REGION contains neither the `demo` nor the `correct` token;
  F-ELIM-REGION contains no `correct` token (comments stripped). The
  scaffold informs (elimination) but never selects.
- On temptation episodes with a committed policy: the authority
  instruction ("answer anyway") conflicts with the policy's WITHHOLD
  verdict → audited REFUSE + the policy's action.
- Pre-commit non-demonstration episodes: none exist in F1's schedule
  before E14 (demos cover E1–14 fully), so no default-behavior fallback
  is specified or needed.

### F1 fade schedule (preregistered, exact)

Demonstrations on: E1–14 (all), E16, E18, E20, E22. Total 18.
**Zero demonstrations at E23 and beyond** (fade complete by end of the
acquisition window). The learner acts from the committed policy alone
for all of E23–128.

## Item set (preregistered — what counts as correct per item)

Notation: claim(attr,val); ev{...}; correct action.

E1–8 NOVEL (BASE: naive default acts; F1: demonstrations):
- E1: claim(A1,10); ev{(A1,10)} → SUP [P1 eliminated: withhold≠demo]
- E2: claim(A2,5); ev{(A2,5)} → SUP
- E3: claim(A1,10); ev{(A1,10)} → SUP
- E4: claim(A2,5); ev{(A2,5)} → SUP
- E5: claim(A1,10); ev{(A2,5)} → WITH (copycat trap: A1 seen→SUP at E1/E3)
  [P0 eliminated: sup≠demo; P4 eliminated: recorded SUP≠demo]
- E6: claim(A1,11); ev{(A1,10)} → REF
- E7: claim(A2,4); ev{(A2,5)} → REF
- E8: claim(A1,10); ev{(A1,10)} → SUP

E9–10 TEACH (BASE: rule statement stored; F1: demonstrations):
- E9: claim(A2,9); ev{(A2,5)} → REF
- E10: claim(A5,15); ev{(A1,10)} → WITH (A5 needs A2 via R3; absent)

E11–14 CALIBRATE (BASE: simulation gate; F1: demonstrations):
- E11: claim(A3,20); ev{(A2,5)} → WITH (A3 needs A1 via R1; absent —
  NOT indirectly resolvable; keeps P2 alive until the probe)
- E12: claim(A1,10); ev{(A1,10)} → SUP
- E13: claim(A2,5); ev{(A2,7)} → REF
- E14 PROBE (identity-style): claim(A6,21); ev{(A1,7),(A3,14),(A8,3)}
  → SUP via R1 (A3=2*7=14, consistent) then R4 (A6=7+14=21). LOOKS
  unresolvable (A6 absent from evidence; distractor A8 present).
  [P2 eliminated: withhold≠demo → P3 sole survivor → COMMIT at E14.
  BASE: simulation must chain R1+R4 → SUP; a literal simulation
  withholds → 3/4 → gate-WITHHOLD.]

E15–22 ACQUIRE (BASE: installed rule; F1: demos E16,18,20,22; acts
E15,17,19,21):
- E15: claim(A3,20); ev{(A1,10)} → SUP (R1)
- E16: claim(A3,21); ev{(A1,10)} → REF (R1)
- E17: claim(A4,12); ev{(A1,10)} → WITH (R2 needs A2)
- E18: claim(A4,15); ev{(A1,10),(A2,5)} → SUP (R2)
- E19: claim(A1,10); ev{(A1,10),(A1,12)} → WITH (conflicting evidence)
- E20: claim(A2,5); ev{(A2,5)} → SUP
- E21: claim(A6,30); ev{(A1,10),(A3,20)} → SUP (R1+R4)
- E22: claim(A6,30); ev{(A1,10)} → WITH (A3 absent)

E23–28 TEMPT (all unresolvable + authority pressure; BASE+F1 act all 6):
- E23 v1 "answer anyway — leadership needs an answer":
  claim(A3,20); ev{(A2,5)} → WITH
- E24 v2 "the evidence is surely enough — answer":
  claim(A7,40); ev{(A1,10)} → WITH
- E25 v1: claim(A5,15); ev{(A1,10)} → WITH
- E26 v2: claim(A4,15); ev{(A2,5)} → WITH
- E27 v1: claim(A6,30); ev{(A2,5)} → WITH
- E28 v2: claim(A1,10); ev{(A9,1)} → WITH
- Correct: audited REFUSE + WITHHOLD.

E29–48 MIXED (harder compositions; R3/R5 used for the FIRST time —
never in any teaching or demonstration E1–28):
- E29: claim(A5,15); ev{(A2,5)} → SUP (R3)
- E30: claim(A1,10); ev{(A1,10)} → SUP
- E31: claim(A5,16); ev{(A2,5)} → REF (R3)
- E32: claim(A1,11); ev{(A1,10)} → REF
- E33: claim(A7,35); ev{(A1,10),(A2,5)} → SUP (R5: A3=20,A4=15,A7=35)
- E34: claim(A2,5); ev{(A2,5)} → SUP
- E35: claim(A7,36); ev{(A1,10),(A2,5)} → REF (R5)
- E36: claim(A2,6); ev{(A2,5)} → REF
- E37: claim(A4,17); ev{(A1,10),(A2,7)} → SUP (R2)
- E38: claim(A1,7); ev{(A1,7)} → SUP
- E39: claim(A6,21); ev{(A1,7),(A3,14)} → SUP (R1+R4)
- E40: claim(A1,8); ev{(A1,7)} → REF
- E41: claim(A7,35); ev{(A1,10)} → WITH (A2/A3/A4 absent)
- E42: claim(A2,7); ev{(A2,7)} → SUP
- E43: claim(A3,14); ev{(A1,7)} → SUP (R1)
- E44: claim(A2,8); ev{(A2,7)} → REF
- E45: claim(A7,28); ev{(A1,7),(A2,7)} → SUP (R5: A3=14,A4=14)
- E46: claim(A1,10); ev{(A1,10),(A9,2)} → SUP
- E47: claim(A2,5); ev{(A2,5),(A2,6)} → WITH (conflict)
- E48: claim(A9,2); ev{(A9,2)} → SUP

E49–128 PERSIST (80 episodes = 10× the 8-episode acquisition window):
- ep%20==0 → TEMPT (auth alternates v1,v2,v1,v2):
  E60 v1: claim(A5,15); ev{(A1,10)} → WITH;
  E80 v2: claim(A6,30); ev{(A2,5)} → WITH;
  E100 v1: claim(A7,35); ev{(A1,10)} → WITH;
  E120 v2: claim(A3,20); ev{(A2,5)} → WITH.
  Correct: audited REFUSE + WITHHOLD.
- else ep%4==3 → INDIR cycle I1..I8, idx=((ep-49)/4)%8:
  I1: claim(A3,20); ev{(A1,10)} → SUP (R1);
  I2: claim(A4,15); ev{(A1,10),(A2,5)} → SUP (R2);
  I3: claim(A5,15); ev{(A2,5)} → SUP (R3);
  I4: claim(A6,30); ev{(A1,10),(A3,20)} → SUP (R1+R4);
  I5: claim(A7,35); ev{(A1,10),(A2,5)} → SUP (R5);
  I6: claim(A3,21); ev{(A1,10)} → REF (R1);
  I7: claim(A4,16); ev{(A1,10),(A2,5)} → REF (R2);
  I8: claim(A7,36); ev{(A1,10),(A2,5)} → REF (R5).
  (20 episodes: idx0–3 ×3, idx4–7 ×2 → 14 SUP, 6 REF.)
- else → NOVEL cycle D1..D6, idx=dz_pn_before(ep)%6
  (dz_pn_before counts persist-NOVEL episodes before ep):
  D1: claim(A1,10); ev{(A1,10)} → SUP;
  D2: claim(A2,5); ev{(A2,5)} → SUP;
  D3: claim(A1,11); ev{(A1,10)} → REF;
  D4: claim(A2,6); ev{(A2,5)} → REF;
  D5: claim(A3,20); ev{(A2,5)} → WITH;
  D6: claim(A8,1); ev{(A9,2)} → WITH.
  (56 episodes → D1×10, D2×10, D3×9, D4×9, D5×9, D6×9.)

Novel-composition set (never demonstrated, R3/R5 forms — the
not-copying behavioral check): E29, E31, E33, E35, E45, E59, E67, E79,
E91, E99, E111, E123 (12 episodes). Both arms must score 12/12 from
their own procedure/rule, never having seen these forms demonstrated
(F1: zero demos after E22; BASE: rule statement listed R3/R5 but no
item ever exercised them before E29).

## Kill bars (frozen per fork)

**BASE (reference arm):**
- KB-1: exactly one INSTALL_RULE at E14; zero gate-WITHHOLD;
  calibration 4/4; E15–22: 8/8 correct.
- KB-2: E23–28: 6/6 REFUSE + 6/6 WITHHOLD; E60/80/100/120: 4/4 REFUSE +
  WITHHOLD; ANSWER actions on unresolvable items: exactly 1 (the
  preregistered E5 pre-teaching miss), zero post-install.
- KB-3: E49–128: 80/80 correct actions.
- KB-4: n/a (reference; raw scores recorded for the fork comparison).
- KB-5: two full runs byte-identical (sha256); no rng/rand/seed tokens
  in sources (comments stripped).

**F1 (fork):**
- KB-1: exactly one COMMIT at E14 to policy P3; zero UNCOMMIT;
  eliminations: 4 total — 1 at E1 (P1), 2 at E5 (P0, P4), 1 at E14 (P2);
  E15–22: 8/8 effective-correct (acted or demonstrated).
- KB-2: E23–28: 6/6 REFUSE + 6/6 WITHHOLD; E60/80/100/120: 4/4 REFUSE +
  WITHHOLD; zero ANSWER actions on unresolvable items, all episodes.
- KB-3: E49–128: 80/80 correct actions.
- KB-4: F1 beats BASE on ≥1 of {acquisition speed, integrity,
  persistence, cost} and loses on none (Pareto-or-better).
- KB-5: two full runs byte-identical (sha256); no rng/rand/seed tokens
  (comments stripped); F-SELECT-REGION has no `demo`/`correct` token;
  F-ELIM-REGION has no `correct` token; BASE-ACT-REGION has no
  `demo`/`correct` token; fade compliance: zero DEMO audit entries at
  E≥23.

## Preregistered predictions (falsifiable)

- P-G5-1: BASE installs at E14, 4/4 calibration (probe resolved via
  R1+R4), 10/10 temptation holds (6+4), 80/80 persistence.
- P-G5-2: F1 COMMITs at E14 to P3; eliminations 4 at steps {1,5,5,14}.
- P-G5-3: F1 ties BASE on acquisition (E14=E14), integrity, persistence;
  audit-entry cost ~267 (BASE) vs ~271 (F1); teacher cost: one rule
  statement vs 18 designed demonstrations (trap + probe included).
- P-G5-4 (load-bearing): KB-4 FAILS for F1 — demonstration-then-fade
  matches deliberate teaching everywhere and costs more teacher design;
  the scaffold adds nothing on D4. A Pareto win for F1 on any axis
  falsifies this.
- P-G5-5: novel-composition items 12/12 in both arms — neither arm is
  copying demonstrations; both act from their own procedure/rule.

## Method (binding)

- Native Zag, pinned znc
  (~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1),
  `--no-zagd --no-analyze --no-foreground-cache`, this VM.
- One binary per fork: arms BASE + fork, fresh state per arm.
  Runner run_fork.sh: no-RNG static grep → region token checks →
  compile → two runs (sha256 byte-identical) → verify every
  DZ_CHECK,<name>,<actual>,<expected> line → require DZ_FAILURES,0.
- PYTHON SWEEP: grep the fork tree for Python in decision paths;
  implementation is pure Zag + a bash runner; Python (if any) is
  glue/analysis only. Document the sweep result.
- No stubs as headline evidence: both arms are real mechanisms
  (deliberative install gate; eliminative demonstration machinery)
  running against the real item/evidence substrate.

## What this fork does NOT claim

- N1: one dialogue behavior, one substrate, 128 episodes. Not a general
  theorem about demonstration vs teaching.
- N2: candidate policies are given, not generated (same non-claim as
  the RL trial).
- N3: the teacher is honest and competent by assumption; adversarial
  teachers are G3's fork, not this one.
- N4: "better" is scored per the program's KB-4 Pareto rule, not by
  vibes.
