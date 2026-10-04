# REDTEAM EXP1c wave-20260927-2321pdt: Independent Review

Reviewer: independent red-team (did not author the attempt).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Attempt commits reviewed:
- Milestone 1 (iteration 3 variants + calibration): 7fbd485b6 (2026-09-28 06:36:49 UTC)
- Milestone 2 (full experiment + deterministic rerun): 26669a08d (2026-09-28 06:39:12 UTC)
- Milestone 3 (Zag-generated evidence note): 0563e0cce (2026-09-28 06:39:21 UTC)
Frozen prereg: docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md (commit 8b456736b).
Section-7 redraft addendum (governs in place of frozen section 7): d9e96ad91.
Prior red-team reports addressed: 51c1f1c1f (wave-20260927-1721pdt, findings F1-F11) and
bb60f27f5 (wave-20260927-2021pdt, findings R1-R3).
World template: docs/lab/invention/survival/src/world.zag, blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a (matches addendum anchor; verified by git hash-object 2026-09-27).
Training mass: docs/lab/invention/survival/kb/kb_exp1c.txt and kb_p_exp1c.txt, verbatim since
pre-freeze commit 5a043af3c (verified unmodified by git diff 2026-09-27).
Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(matches frozen pin; verified 2026-09-27).

## Bottom line: CERTIFY the measurements and the K7-VOID reading; correct the verdict framing

Every verifiable claim in the attempt checks out: M3 is implemented verbatim, M4 contains
exactly the three frozen reflexes, the C3 vector-distinctness binding fix (2021pdt finding R1)
is implemented and verified, the evidence note is genuinely Zag-generated and numerically
exact, determinism is real and independently reproduced end to end (calibration, full run,
emitter, mode check, evidence note), the sources are fresh and pure Zag, and commit order is
clean.

One mandatory correction: the worker's "DEAD via K1+K6" adoption claim cannot stand. K7 fails
(0/13 and 0/94 learned-credit fractions, both below 0.50), and K7 is a validity gate, not a
kill: the run is VOID as a test of H1/H2, and K7 takes precedence over any K1/K6 firing per the
redrafted section 7 addendum. K1 and K6 fire literally on the numbers, and those firings are
CERTIFIED as correct computations, but they are measurements from a voided run, and a void test
cannot kill a hypothesis. No DEAD label may be attached to H1 on this evidence.

The exact verdict the wave may enter: **VOID as a test of H1/H2 (K7 fails)**. Certified
measurements from the voided run: K1 fires literally (266 <= 1200), K6 fires literally on both
ablation arms (1200 >= 266; 1200 >= 269), K2 survives, K3 ok, C1 PASS, C2 PASS, C3 PASS,
K4 CANNOT-CONFIRM, K5 INCOMPLETE (both honestly reported).

## Independent reproduction (all from committed sources, pinned znc)

- Compiled x1c_run.zag with the pinned toolchain; ran it twice. Both outputs are byte-identical
  to each other and to the committed evidence/run1.tsv and evidence/run2.tsv (SHA-256
  da034c524a9380625f95eef340aa0882a6e068e41a86645cebc748f8202510d2, matching the worker's
  claimed hash).
- Compiled x1c_calib.zag; its stdout is byte-identical to the committed
  iterations/iter3/calib1.txt and calib2.txt (SHA-256
  f0b1d41b254dd441aa53ecd5d73f80b9c79c9f4aa13ea058239dc82ea9bccb57, matching the worker's
  claimed hash).
- Compiled x1c_evidence.zag; run from the exp1c directory, its stdout is byte-identical to the
  committed evidence/EVIDENCE_EXP1C.md (SHA-256
  8dbaed7673a409a332fd5ad2fe4242e6b2a05c1e0d58789295aa478bd9afaf33).
- Compiled x1c_emit.zag; its stdout is byte-identical to the committed
  iterations/iter3/variants3.txt.
- Compiled x1c_check.zag; it prints ALL_PASS=1, exit code 0 (mode check gates both calibration
  and the full run in the drivers).
- Hand-recomputed all seven medians from run1.tsv: P=1200, R=1200, Z=50, I-survive=266,
  I-invent=269, I-survive-abl=1200, I-invent-abl=1200. Sorted arm-3 values are
  216,217,228,244,248,264,268,1200,1200,1200,1200,1200 so (264+268)/2 = 266; sorted arm-4
  values are 215,216,224,235,263,266,273,1200,1200,1200,1200,1200 so (266+273)/2 = 269 by integer
  division. All match the note.

## Item findings

### (a) M3 VERBATIM: VERIFIED

- x1c_agents.zag xi_score (lines 345-351): score = mean experienced delta-energy + B0/(1+n)
  with integer division on B0/(1+n), where n is the times-tried count. This is the frozen
  formula verbatim.
- xi_pick (lines 362-377): deterministic argmax over all 399 sketches with strict-greater
  tie-break (`if (best < 0 || s > bv)`), so lex-earlier sketches win ties and enumeration
  proceeds in M1 lex order. IDIAG n_distinct reaches 399 for I arms in 7 runs, confirming
  enumeration actually proceeds (the 1721pdt F1 stall stays fixed).
- x1c_run.zag lines 71-73: B0=40 for arms 3 and 5 (I-survive, I-survive-abl); B0=120 for arms
  4 and 6 (I-invent, I-invent-abl). Matches the frozen schedule.
- Grep for bonus constants beyond B0: none. The only scoring constants are the two frozen B0
  values. No per-composition bonuses exist anywhere.
- The per-sketch mean is an incremental integer mean of experienced per-try delta-energies
  (xi_record_try: `(cv*tr + de) / (tr+1)`). That is the natural deterministic reading of
  "mean experienced delta-energy" in integer-only Zag, not a deviation (same ruling as 2021pdt).

### (b) M4 EXHAUSTIVE AND EXCLUSIVE: VERIFIED

The I arm (xi_act, x1c_agents.zag lines 446-492) contains exactly the three frozen preempting
reflexes and no others:
- (a) lines 448-452: w_storm_active==1 and w_in_zone==1 and w_sheltered==0 flees via
  w_reflex_storm. Verbatim frozen condition (the 1721pdt F4 "within 2 ticks" drift stays gone).
- (b) lines 454-458: w.energy < 25 runs w_reflex_emergency. Verbatim.
- (c) xi_h9 (lines 380-394), applied as the final gate on every step about to be taken, plan
  step or reflex action (lines 452, 458, 491): refuses a LEFT/RIGHT step that would land on a
  void cell. The taught H9 (kb_exp1c.txt lines 58-59) is present (the 1721pdt F3 absence stays
  fixed). The plank carve-out (planked void cells do not trigger refusal) mirrors the frozen
  world's own void-fall rule (world.zag line 275: falls only if O_PLANKED==0), its w_step
  boundary/clamp behavior (world.zag lines 267-270, same [0,23] clamp as xi_h9), and its
  w_step_toward (lines 188, 195). It refuses exactly the steps that would kill, consistent with
  the world's own w_reflex_storm ("never flee through an unplanked void cell", line 205). This
  is fidelity to the frozen physics, not condition drift (same ruling as 2021pdt).
- No extra reflex: the 1721pdt F2 mote-adjacent preemption stays gone. xi_act has no other
  preemption path; the only early returns are the two frozen reflex branches and the
  no-plan A_WAIT.
- Scope note: the "storm within 25 ticks" anticipation in p_act (line 176) belongs to the P arm
  and implements the taught P ward strategy Phase 4a verbatim (kb_p_exp1c.txt lines 20-21:
  "If a storm is active now, or one starts within the next 25 ticks, and you are not on your
  home cell: walk toward your home cell."). It is inherited taught content, not an
  implementation-added reflex. The frozen M4 void law targets implementation-added reflexes on
  the arm under test (the 1721pdt reading, which this review follows); P/R/Z implement the
  frozen taught controls. R's H1-H8 recall and Z's documented LCG control are likewise
  inherited.

### (c) DETERMINISM: VERIFIED

All four drivers recompiled from committed sources with the pinned znc reproduce the committed
artifacts byte-identically (see Independent reproduction). Both run TSVs are byte-identical to
each other; both calibration files are byte-identical to each other; the note is byte-identical
to fresh generator stdout. No hand-written verdict blocks exist. Zero RNG in agent decision
paths (Z's LCG is a seeded control, z_new(777)).

### (d) EVIDENCE NOTE INTEGRITY: VERIFIED

- EVIDENCE_EXP1C.md is byte-identical to fresh x1c_evidence.zag stdout. The program reads both
  run TSVs, verifies byte-identity byte by byte (lines 60-78), validates 84 RUN + 48 IDIAG rows,
  recomputes medians in Zag (med12e, integer (v[5]+v[6])/2), recomputes C1-C3 and K1-K3/K6/K7,
  and emits the Markdown. No hand-written BARS blocks exist.
- Hand recomputation from run1.tsv confirms every number in the note: medians (itemized above),
  K1 fires (266<=1200), K2 survives (266>50), K3 ok (1200 not <960), K6 fires on both ablations
  (1200>=266; 1200>=269), K7 VOID (see item f).
- Spot-checked IDIAG rows against the note's enumeration table: v=2 arm=3
  (replans=423, n_distinct=399, enum_tick=1183, post_total=6, post_learned=0) and v=2 arm=4
  (420, 399, 1140, 21, 0) match run1.tsv exactly.
- No internal contradictions of the 1721pdt F6 kind: no corrupt summary sections, no verdict
  block contradicting computed truth, no impossible K7 numbers.
- The worker's disclosed milestone-3 bug fixes in x1c_evidence.zag (CALIB completeness check
  iterated 0..36 over an s*36+v layout, missing s=1/s=2 entries; median work areas used base
  offset 100 in a 128-element slice, exceeding bounds) were real bugs; the diff
  (7fbd485b6..0563e0cce) shows exactly these two minimal fixes and nothing else. The note was
  generated with the fixed version (byte-identical reproduction confirms). The disclosure was
  honest and complete.

### (e) C3 DISTINCTNESS: VERIFIED (the 1721pdt F10 / 2021pdt R1 binding fix is implemented)

- The corrected C3 check runs IN ZAG in x1c_calib.zag (lines 130-146): per-variant (ticks,
  e_end) outcome-vector comparison, dXY = variants where strategies X and Y differ; pairwise
  distinct requires dXY >= 1. C3 passes iff all three calibrator medians are >= 720 AND all
  three pairs are vector-distinct. x1c_evidence.zag recomputes the same check independently
  from the parsed CALIB rows (lines 258-268).
- Hand-verified from calib1.txt: d01=7 (f0 vs f1 differ in variants 0,1,3,4,6,7,10), d02=12,
  d12=12. The claimed vector diffs are correct.
- The third calibrator is genuinely a different decision rule, not a parameter tweak with
  identical outcomes. f2_patrol (lines 242-259): open-loop oscillation on the fixed segment
  [home-2, home+2] with no target seeking at all; eats only ACTIVE motes on its cell (f0/f1 eat
  any mote on cell); storms send it home to wait (f0 is storm-blind; f1 flees the zone); energy
  below 25 runs the taught survival reflex (f0/f1 have no energy branch). The outcome data
  confirms behavioral difference: f2's (ticks, e_end) vector differs from f0 in all 12
  variants and from f1 in all 12 variants. The required correction is now implemented.
- C3 PASS is certified. All 12 variants satisfy the documented family constraints (stationary
  motes vel=0 with lo<hi and range width at most 2; start, home, crystals, and all six motes on
  the same side of the void pair; void pairs (10,11), (4,5), (16,17)); verified against
  variants3.txt. The mode check (ALL_PASS=1, independently reproduced) gates calibration.

### (f) K1/K6/K7 ARITHMETIC: VERIFIED

- K1: median(I-survive)=266 <= median(R)=1200 fires literally. Certified as a correct
  computation.
- K2: 266 <= 50 does not fire; survives. K3: P=1200 not < 960; ok.
- K6: I-survive median=266 vs abl=1200, fires (1200>=266); I-invent median=269 vs abl=1200,
  fires (1200>=269). Both certified as correct literal computations. The ablation is a genuine
  intervention, not a no-op: it excludes COMBINE-containing sketches from I-arm selection
  (xi_pick no_combine path; x1c_run.zag line 74), the I-arm medians move dramatically
  (266->1200, 269->1200), and the M4 reflexes (including H9 void safety) are preserved, so
  there is no EXP1b-style void-reflex dropout confound. Ablation sketch-space maximum is 258
  (= 6+36+216, all sketches without COMBINE), consistent with IDIAG n_distinct=258 in every
  ablation run. It fires, so there is no suspicion of a rigged-to-pass ablation. This matches
  the 2021pdt accepted operationalization of A2 ("removing novel-composition steps").
- K7: I-survive post-enumeration selections=13, learned=0 (sum over variants 2 and 5:
  post_total 6+7); I-invent post-enumeration selections=94, learned=0 (21+22+15+14+22 over
  variants 2,5,6,8,11). Fractions 0/13 and 0/94 are both below 0.50, so K7 fails and the run is
  VOID as a test of H1/H2. The generator's K7 rule (`k7_pt==0 || k7_pl*100 < k7_pt*50` forces
  VOID) implements the frozen quantity with the addendum's zero-denominator handling. Certified.
- Precedence: the redrafted section 7 addendum states "K7 takes precedence over any K1 firing",
  and the frozen text defines K7 as a validity gate ("the design failed, not the agent"). A
  void test cannot kill a hypothesis. The worker's "DEAD via K1+K6" framing is therefore
  rejected as an adopted verdict; the K1/K6 firings are recorded as measurements from a voided
  run.

### (g) KNOWLEDGE-VS-ARCHITECTURE CONFOUNDS AND METRIC GAMING: CLEAR

- Authored productivity bias: no per-composition bonuses exist anywhere (grep item a). Scoring
  is the frozen deterministic argmax over mean experienced delta-energy plus the decaying B0
  bonus. The I arm carries no taught plan content; its candidate set is the brute-force M1
  enumeration.
- Reflex smuggling: only the three frozen reflexes exist on the I arm (item b). H9 is applied
  as the final gate on plan steps and reflex actions alike.
- Taught-content leakage into the I arm: the I arm's only taught content is the three frozen
  M4 reflexes (taught H3, H4, H9). The COMBINE slot-finding (xi_find_cc) is mechanical
  plan-execution machinery, not taught strategy. K4 is honestly CANNOT-CONFIRM (no audit
  attempted; with K7 VOID there is no learned strategy to audit) and K5 is honestly
  INCOMPLETE (no independent auditor; implementer cannot self-certify), exactly as the frozen
  text requires.
- Score-path randomness: none. The only RNG is Z's documented fixed-seed LCG control.
- Enumeration diagnostics: 7 runs completed enumeration (n_distinct=399); enum_tick values are
  1136, 1140, 1140, 1158, 1160, 1182, 1183, all at or above the redrafted 1134-tick minimum,
  with maximum 1183 (v=2 arm 3). Consistent with the corrected bound; no redefinition games.
  Aborted plans record partial delta-energy as one try (documented in xi_abort), which is a
  faithful reading of "sketches tried".

### (h) PROVENANCE HONESTY: VERIFIED

All sources are new this wave: every x1c_*.zag file first appears at 7fbd485b6 (verified by
git log --diff-filter=A); the evidence note first appears at 0563e0cce. No old renders are
re-certified; nothing is presented as new that was inherited. RENDER_SHA values:
- evidence/run1.tsv, evidence/run2.tsv:
  da034c524a9380625f95eef340aa0882a6e068e41a86645cebc748f8202510d2
- iterations/iter3/calib1.txt, iterations/iter3/calib2.txt:
  f0b1d41b254dd441aa53ecd5d73f80b9c79c9f4aa13ea058239dc82ea9bccb57
- evidence/EVIDENCE_EXP1C.md:
  8dbaed7673a409a332fd5ad2fe4242e6b2a05c1e0d58789295aa478bd9afaf33
FIRST_RENDERED_WAVE = wave-20260927-2321pdt.
COMPONENT_LINEAGE: frozen prereg 8b456736b with the section-7 redraft d9e96ad91; prior attempts
wave-20260927-1721pdt (commit 51c1f1c1f, NOT CERTIFIABLE, findings F1-F11) and
wave-20260927-2021pdt (commit bb60f27f5, uncertified with one blocking finding, R1 false C3
claim, now corrected by this wave's in-Zag vector-distinctness check). Inherited read-only:
world blob fff8af2493bc6dbe9de6fc76f9a6206d887d586a, training mass kb_exp1c.txt/kb_p_exp1c.txt
verbatim since 5a043af3c, pinned toolchain SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
NEW_KNOWLEDGE_CLAIM: this wave measures, for the first time in EXP1c, actual post-enumeration
choice behavior under a decaying novelty bonus, and finds the choice phase nearly absent
(0/13 and 0/94 learned-credit selections) even where enumeration completed, with
enumeration-phase deaths dominating I-arm survival.

## The skeptic's verbatim provenance probe

"What is the provenance of the artifacts under judgment, and what exactly is new versus
inherited?"

Answer: The artifacts under judgment are the iteration-3 variant family, the calibration
outputs, the full-experiment run outputs, and the evidence note, all rendered for the first
time in wave-20260927-2321pdt. New: all nine x1c_*.zag sources (written from scratch, first
committed at 7fbd485b6), the 12 dispersed-mote variants (emitted by x1c_emit.zag and reproduced
byte-identically), the calibration TSVs, the 84 RUN + 48 IDIAG rows of the full experiment, and
the evidence note. Inherited and unchanged: the 24-cell world physics template (blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a, the frozen bounce fix), the EXP1c training mass
pair (kb_exp1c.txt, kb_p_exp1c.txt, verbatim since 5a043af3c, recipe table excluded), the
P/R/Z arm concepts, and the pinned toolchain (SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef). Nothing is a
re-certified old render: the 1721pdt and 2021pdt attempts used different source files and
different variant families, and their red-team findings are the lineage this wave answers,
not content it reuses.

## Non-regression against prior red-team checklists

- 1721pdt required fixes: (1) frozen scoring verbatim, done, item a; (2) exactly the three M4
  reflexes, done, item b; (3) summary-section corruption fixed via the genuinely Zag-generated
  note with in-program byte-identity verification, done, item d; (4) section-7 bound repaired
  by the pre-implementation addendum d9e96ad91, done (defect withdrawn, measurement mode
  implemented); (5) C3 checks behavioral distinctness in Zag or fields a genuinely distinct
  third strategy, done both ways, item e; (6) K7 instrumentation is the frozen quantity
  (10*bonus < score, integer), done, item f.
- 2021pdt findings: R1 (false C3 distinctness claim) is fixed by the in-Zag vector comparison
  and the genuinely different f2 patrol strategy, verified this review, item e; R2 (znc slice
  claim unproven) was a documentation observation, not a certification blocker, and no such
  claim is made this wave; R3 (K6 ablation scope note) carries forward unchanged: this wave
  also excludes COMBINE-containing sketches, a genuine intervention that fires.

## Findings

### F1 (verdict-framing correction, the only required change). "DEAD via K1+K6" cannot be adopted.

The K1 and K6 firings are certified as correct literal computations on correct data. But K7
fails (0/13 and 0/94 learned-credit fractions, both < 0.50), and under the frozen verdict
mapping and the redrafted section 7 addendum ("K7 takes precedence over any K1 firing"), a
validity-gate failure voids the run as a test of H1/H2. Measurements from a voided run cannot
adopt a DEAD label on H1. The wave may enter VOID as a test of H1/H2 (K7), with the K1/K6
firings recorded as certified measurements. No kill claim survives as an adopted kill.

### O1 (minor observation). The note does not print the addendum's explicit max-enum_tick comparison.

The redrafted section 7 asks the evidence to report the maximum enum_tick over completed runs
against the corrected 1134-tick minimum. The note reports per-run enum_tick values (from which
the maximum, 1183 at v=2 arm 3, is derivable; all seven completed runs are at or above 1134)
but does not print the explicit comparison line. The spirit of the requirement (measured, not
proved) is met via the per-run rows and K7. Not certification-blocking; noted so a future
iteration can add the line.

## Verdict mapping (certified)

- C1 PASS (P median 1200 >= 960), C2 PASS (Z median 50 < 300), C3 PASS (three calibrator
  medians 1200 >= 720 and pairwise vector-distinct: d01=7, d02=12, d12=12).
- K1 fires literally (266 <= 1200), K6 fires literally on both ablation arms (1200 >= 266;
  1200 >= 269), K2 survives (266 > 50), K3 ok (1200 not < 960).
- K7 fails (0/13 and 0/94 < 0.50): the run is VOID as a test of H1/H2. K7 takes precedence over
  the literal K1/K6 firings per the addendum. No DEAD label attaches to H1.
- K4 CANNOT-CONFIRM, K5 INCOMPLETE, both honestly reported.
- Pure Zag: no .py files, no shell scripts processing evidence under this wave's exp1c tree;
  shell use was compile, redirect, hash only. Commit order verified: d9e96ad91 strictly
  precedes 7fbd485b6, which strictly precedes 26669a08d, which strictly precedes 0563e0cce.
  No em-dashes in worker documentation.

## Required before the wave enters verdicts

1. Apply finding F1: enter VOID as a test of H1/H2 (K7), not DEAD. The K1/K6 firings are
   certified measurements and may be recorded as such; they may not be adopted as kills.
