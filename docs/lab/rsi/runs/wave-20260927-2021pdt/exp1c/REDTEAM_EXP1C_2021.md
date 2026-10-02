# REDTEAM EXP1c wave-20260927-2021pdt: Independent Review

Reviewer: independent red-team (did not author the attempt).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Attempt commits reviewed:
- Addendum: d9e96ad91 (2026-09-28 03:36:20 UTC)
- Milestone 2 (iteration 1): 9625c211a (2026-09-28 03:50:01 UTC)
- Milestone 3 (full experiment): f26d510f3 (2026-09-28 03:52:21 UTC)
- Milestone 4 (evidence note): 4750f1a19 (2026-09-28 03:52:24 UTC)
Frozen prereg: docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md
Prior red-team report addressed: 51c1f1c1f (wave-20260927-1721pdt).
World template: docs/lab/invention/survival/src/world.zag, blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a (matches addendum anchor;
verified by git hash-object 2026-09-27).
Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(matches frozen pin; verified 2026-09-27).

## Bottom line: VOID (uncertified attempt)

The attempt is not certifiable as written, on one material ground:
the C3 calibration claim is false (finding R1). Every other item
checks out, including all the defects that voided the 1721pdt attempt:
M3 is implemented verbatim, M4 contains exactly the three frozen
reflexes, the evidence note is genuinely Zag-generated and numerically
exact, determinism is real and independently reproduced end to end,
the sources are pure Zag, and commit order is clean.

The exact verdict the wave may enter: **VOID as a test of H1/H2**
(K7 fails; K7 takes precedence over K1/K6 per the addendum). The
K7-VOID verdict itself is VERIFIED and may be entered. **No kill
claim survives as an adopted kill**: K1 and K6 fire literally on the
numbers, but they are measurements from a voided run, and a void test
cannot kill a hypothesis. K4 is CANNOT-CONFIRM, K5 is INCOMPLETE,
both honestly reported.

The single blocking correction: strike or repair the false C3
"3 qualitatively distinct strategies" claim (finding R1). It does not
change any kill-bar verdict, but a frozen gate may not be recorded
PASS on a false premise.

## Independent reproduction (all from committed sources, pinned znc)

- Compiled e1c_run.zag with the pinned toolchain; ran it twice.
  Both outputs are byte-identical to each other and to the committed
  evidence/run1.tsv (SHA-256
  0e82ba093953da59e0d4d1de25cf75501b5108992857ae281607c9519281c288,
  matching evidence/HASHES.txt). The full experiment is reproducible
  end to end.
- Compiled e1c_evidence.zag; its stdout is byte-identical to the
  committed evidence/note1.md. The note is genuinely Zag-generated
  from the TSVs; there are no hand-written verdict blocks.
- Compiled e1c_calib.zag; its stdout is byte-identical to
  iterations/iter1/calib1.txt.
- evidence/run1.tsv and evidence/run2.tsv are byte-identical
  (SHA-256 match). evidence/note1.md and note2.md are identical.
  iterations/iter1 check/calib/variants 1==2 files are pairwise
  identical.
- Hand-recomputed all seven medians from run1.tsv: P=1200, R=1200,
  Z=24, I-survive=918, I-invent=920, I-survive-abl=1082,
  I-invent-abl=1200. All match the note. (Z uses the program's
  integer convention: sorted Z is 3,3,9,9,13,16,33,50,50,50,50,50;
  (16+33)/2 = 24 by integer division.)

## Item findings

### 1. M3 VERBATIM: VERIFIED

- e1c_agents.zag lines 303-309 (xi_score): score = mean experienced
  delta-energy + B0/(1+n) with integer division on B0/(1+n), where n
  is the times-tried count. This is the frozen formula verbatim.
- e1c_agents.zag lines 316-331 (xi_pick): deterministic argmax over
  all 399 sketches with strict-greater tie-break, so lex-earlier
  sketches win ties and enumeration proceeds in M1 lex order.
  IDIAG n_distinct reaches 399 for I-invent in 6 variants, confirming
  enumeration actually proceeds (the 1721pdt F1 stall is fixed).
- e1c_run.zag lines 69-70: B0=40 for arms 3 and 5 (I-survive,
  I-survive-abl); B0=120 for arms 4 and 6 (I-invent, I-invent-abl).
  Matches the frozen schedule.
- Grep for bonus constants beyond B0: none. The only scoring
  constants are the two frozen B0 values. No per-composition bonuses
  exist anywhere.
- Note: the per-sketch mean is an incremental integer mean of
  experienced per-try delta-energies. That is the natural
  deterministic reading of "mean experienced delta-energy" in
  integer-only Zag, not a deviation.

### 2. M4 EXHAUSTIVE AND EXCLUSIVE: VERIFIED

The I arm (xi_act, e1c_agents.zag lines 404-445) contains exactly the
three frozen preempting reflexes and no others:
- (a) lines 408-412: w_storm_active==1 and w_in_zone==1 and
  w_sheltered==0 flees. Verbatim frozen condition (the 1721pdt F4
  "within 2 ticks" drift is gone).
- (b) lines 414-418: w.energy < 25 runs the survival reflex.
  Verbatim.
- (c) lines 334-348 (xi_h9), applied as the final gate on every step
  about to be taken, plan step or reflex action (lines 412, 418,
  445): refuses a LEFT/RIGHT step that would land on a void cell.
  The taught H9 (kb_exp1c.txt lines 58-59) is present (the 1721pdt
  F3 absence is fixed). The plank carve-out (planked void cells do
  not trigger refusal) mirrors the frozen world's own void-fall rule
  (world.zag lines 274-275: falls only if O_PLANKED==0) and its
  w_step boundary/clamp behavior (world.zag lines 264-280, same
  [0,23] clamp as xi_h9). It refuses exactly the steps that would
  kill, consistent with the world's own w_reflex_storm
  ("never flee through an unplanked void cell", world.zag line 205).
  This is fidelity to the frozen physics, not condition drift.
- No extra reflex: the 1721pdt F2 mote-adjacent preemption is gone.
  xi_act has no other preemption path.
- Scope note: the "storm within 25 ticks" anticipation in p_act
  (e1c_agents.zag line 142) belongs to the P arm and implements the
  taught P ward strategy Phase 4a verbatim (kb_p_exp1c.txt:
  "If a storm is active now, or one starts within the next 25 ticks,
  and you are not on your home cell: walk toward your home cell.").
  It is inherited taught content, not an implementation-added reflex.
  The frozen M4 void law targets implementation-added reflexes on the
  arm under test (the 1721pdt reading, which this review follows);
  P/R/Z implement the frozen taught controls. R's H1-H9 recall and
  Z's documented LCG control are likewise inherited.

### 3. EVIDENCE NOTE INTEGRITY: VERIFIED

- note1.md is byte-identical to fresh e1c_evidence.zag stdout (see
  reproduction above). The program reads both TSVs, verifies
  byte-identity byte by byte (e1c_evidence.zag lines 30-48),
  validates 84 RUN + 48 IDIAG rows, recomputes medians in Zag
  (med12e, integer (v[5]+v[6])/2), recomputes C1-C3/K1-K3/K6/K7, and
  emits the Markdown. No hand-written BARS blocks exist.
- Hand recomputation from run1.tsv confirms every number in the
  note: medians (itemized above), K1 KILL (918<=1200), K2 survive
  (918>24), K3 ok (1200>=960), K6 KILL on both ablations
  (1082>=918; 1200>=920), K7 VOID (see item 6).
- No internal contradictions of the 1721pdt F6 kind: no corrupt
  summary sections, no verdict block contradicting computed truth,
  no impossible K7 numbers. The IDIAG K7 inputs sum correctly:
  I-survive post_total=0 across all variants; I-invent post_total =
  11+18+22+10+16+12 = 89, post_learned = 0 throughout.

### 4. COMMIT ORDER: VERIFIED

- git merge-base --is-ancestor confirms: d9e96ad91 strictly precedes
  9625c211a, which strictly precedes f26d510f3, which strictly
  precedes 4750f1a19.
- git log d9e96ad91..9625c211a shows no intervening commits.
- First appearance of docs/lab/rsi/runs/wave-20260927-2021pdt/exp1c/src/
  files is at 9625c211a.
- d9e96ad91 contains only
  ADDENDUM_SECTION7_REDRRAFT_2021.md (1 file), committed alone
  before any implementation file existed, as its message claims.

### 5. RUN COUNT AND DETERMINISM: VERIFIED

- Actual inventory: 84 RUN rows per TSV (12 variants x 7 arms) plus
  48 IDIAG rows (12 x 4 I-arms). Both TSVs byte-identical by
  SHA-256 (0e82ba09...), matching evidence/HASHES.txt.
- The 7 arms are the frozen 5 (P, R, Z, I-survive, I-invent) plus
  the two K6 ablation arms (I-survive-abl, I-invent-abl). The
  ablation runs are prereg-authorized: frozen K6 mandates an A2
  ablation ("ablation (A2) shows removing novel-composition steps
  does not reduce survival"). The frozen "5 arms" budget line counts
  the primary arms; K6 requires the ablation instrument. The worker's
  "84 runs" is 12x7 per determinism run, correct.
- Determinism is independently confirmed: my rebuild from committed
  sources reproduces run1.tsv byte-identically, twice.

### 6. K7 COMPUTATION: VERIFIED (K7-VOID stands; precedence confirmed)

- Frozen K7: the fraction of post-enumeration I-arm plans selected
  with novelty bonus contributing less than 10% of the winning score
  is below 0.50, else VOID as a test of H1/H2.
- Instrumentation (e1c_agents.zag lines 420-429) implements the
  frozen quantity correctly (the 1721pdt F7 inversion is fixed):
  among post-enumeration selections only (enum_done==1), counts
  10*bonus < score, using the tried/mean values that produced the
  winning score.
- Data: I-survive 0 post-enumeration selections / 0 learned;
  I-invent 89 post / 0 learned. Fraction = 0 < 0.50. K7 verdict
  VOID is correct.
- Zero-denominator case (I-survive, 0 post-enumeration selections):
  handled per the redrafted section 7 addendum ("if no
  post-enumeration plans are observed, K7 fails and the run is VOID
  as a test of H1/H2"), implemented in e1c_evidence.zag
  (k7_pt3==0 forces VOID). Matches the addendum.
- Precedence: the addendum states "K7 takes precedence over any K1
  firing", and the frozen text defines K7 as a validity gate ("the
  design failed, not the agent"). A void test cannot kill a
  hypothesis, so K7's VOID takes precedence over the literal K1 and
  K6 firings. The worker's milestone-4 message records this
  correctly.

### 7. K1/K6/K2/K3 NUMBERS: VERIFIED (computations correct; kills not adopted)

- Medians hand-verified from run1.tsv: I-survive=918, I-invent=920,
  P=1200, R=1200, Z=24, I-survive-abl=1082, I-invent-abl=1200. K1 is
  computed on the frozen arms (I-survive vs R). All match the note.
- K1: 918 <= 1200 fires literally. K2: 918 <= 24 does not fire.
  K3: P=1200 not < 960, run not void on K3. All correct.
- K6: the literal rule (ablation median >= original median kills)
  fires on both arms (1082>=918; 1200>=920). The ablation is a
  genuine intervention this wave, not a no-op: it excludes
  COMBINE-containing sketches from I-arm selection
  (e1c_agents.zag xi_pick no_combine path; e1c_run.zag lines 71-72),
  medians move, and the M4 reflexes (including H9 void safety) are
  preserved, so there is no EXP1b-style void-reflex dropout
  confound. The K6 KILL computation is correct. It differs
  narrowly from EXP1b's A2 (which replaced all T/C/D tokens on
  replay); excluding COMBINE plans is a reasonable operationalization
  of "removing novel-composition steps", and it fires, so there is
  no suspicion of a rigged-to-pass ablation.
- Effect: K1 and K6 fire literally, but under item 6's precedence
  the run is VOID as a test of H1/H2. The firings are recorded as
  measurements from a voided run, not adopted kills. No kill claim
  survives.

### 8. THE ZNC SLICE CLAIM: MIXED (reference verified; exact pattern unproven; workaround effective)

- "The frozen harness references a znc multi-slice workaround":
  VERIFIED. docs/lab/invention/survival/src/agent_i.zag line 13,
  runner.zag line 8, exp1b_agent_i.zag line 17, exp1b_runner.zag
  line 9, and the 1421pdt iteration files all carry the
  "znc multi-slice workaround" comment.
- The specific claim in ITERATION1.md ("a single pdat[0] = 16
  corrupted indices 32, 35, 38, 41, 44", non-deterministically):
  UNPROVEN. Three purpose-built probes compiled with the pinned znc
  could not reproduce that pattern or any non-determinism. The
  closest scenario (zero a 64-element i32 slice, store at index 0,
  read back) was clean for both 64- and 1024-element slices.
- What I did confirm independently: a real allocator-overlap
  anomaly with the pinned znc. After an interleaved _zag_malloc,
  index 32 of a live 64-element i32 slice deterministically read
  back as 64 instead of 0 (three runs identical). Same bug family
  as claimed, different signature; deterministic in my probes,
  not non-deterministic as the worker described it.
- The workaround is EFFECTIVE regardless: all worker drivers use
  1024-element (or larger) slices allocated up front, and the
  end-to-end reproduction above shows fully deterministic,
  byte-identical outputs. What would verify the worker's exact
  claim: the original failing probe program and its observed
  outputs, which were not committed.

### 9. PURE ZAG: VERIFIED

- No .py files anywhere under docs/lab/rsi/runs/wave-20260927-2021pdt/.
- No shell scripts process EXP1c evidence. The forks/*.sh files are
  the fork-battery driver (pure shell invoking znc); they do not
  touch exp1c evidence.
- The nine .zag sources are pure Zag. Shell use (compile, redirect
  stdout, hash) is within frozen item 7. The .zag-cache and
  .zagd.semantic-ready files in src/ are untracked build artifacts,
  not committed.

### 10. C1/C2/C3: C1 VERIFIED, C2 VERIFIED, C3 REFUTED (finding R1)

- C1: median P = 1200 >= 960. PASS. (Calibration forage = 1200
  corroborates.)
- C2: median Z = 24 < 300. PASS, verified in the full experiment
  itself. (The iteration-1 "separate Zag probe" is not committed,
  but the full run settles C2.)
- C3: REFUTED. Frozen C3 requires ">= 3 qualitatively distinct
  scripted strategies each reaching median >= 720/1200". The worker
  claims all three calibrators are "qualitatively distinct" and
  "behaviorally distinct by construction" (ITERATION1.md;
  e1c_calib.zag comment; note1.md "3 distinct strategies, all
  median 1200"). The worker's own calibration data refutes this:
  calib1.txt shows f0 (forage) and f2 (homebody) with IDENTICAL
  (ticks, e_end) in all 12 variants (e.g. variant 0: 1200/145 and
  1200/145; variant 1: 1200/161 and 1200/161; identical across all
  twelve). They are behaviorally identical in this variant family,
  not distinct. Only two distinct surviving behaviors are
  demonstrated (the forage/homebody cluster and stormflee). The
  in-Zag C3 check (C3_DISTINCT=3) counts medians only and never
  tests distinctness. This repeats 1721pdt finding F10, whose
  required correction ("make C3 check behavioral distinctness, not
  just median counts, or field a third genuinely distinct surviving
  strategy") was not implemented this wave.
- Consequence: the stop-at-iteration-1 decision's "C3 PASS"
  citation is not satisfied on the frozen "qualitatively distinct"
  qualifier, so the M5 stop rule (retune until C1-C3 pass) was not
  fully met as claimed. Mitigating nuance: the full run's P arm
  (taught ward strategy, median 1200) and R arm (heuristics, median
  1200) are behaviorally distinct surviving scripted strategies, so
  the underlying sim-diversity concern C3 guards is substantially
  met in practice; but that does not repair the worker's specific
  false claim about the three calibrators. This finding does not
  change any kill-bar verdict.

### 11. K4/K5: VERIFIED HONEST

- K4 CANNOT-CONFIRM: the novelty audit was not attempted; the note
  discloses this ("requires manual audit of taught strategies vs
  learned behavior"). With K7 VOID there is no learned strategy to
  audit. Honest.
- K5 INCOMPLETE: no independent auditor; the implementer states the
  limitation exactly as the frozen K5 text requires
  ("no independent auditor; implementer cannot self-certify").
  Honest.

## Findings

### R1 (major). C3 "qualitatively distinct" claim is false. Repeat of 1721pdt F10; required correction not implemented.

ITERATION1.md asserts the three calibration strategies are
"qualitatively distinct" and describes f2 as "does not roam";
calib1.txt proves f0 and f2 behaviorally identical across all 12
variants. The in-Zag C3 gate counts medians, not distinctness.
The 1721pdt red team required exactly this to be fixed before any
future certification; it was not. The C3 PASS claim and the
stop-at-iteration-1 decision's reliance on it must be corrected
(strike the distinctness claim or field a genuinely third distinct
strategy) before the calibration section can be certified. No
kill-bar verdict changes.

### R2 (minor). ZNC slice-smearing claim unproven in its specifics.

Recorded as UNPROVEN with the exact verification path stated in
item 8. The workaround itself is validated by byte-identical
reproduction. Not certification-blocking.

### R3 (observation). K6 ablation scope differs narrowly from EXP1b A2.

This wave excludes COMBINE-containing sketches from selection;
EXP1b's A2 replaced all TAKE/COMBINE/DROP tokens on replay. The
narrower scope is a reasonable operationalization of "removing
novel-composition steps", it is a genuine intervention, and it
fires. Not a deviation; recorded for continuity.

## What the worker got right (credited)

- M3 implemented verbatim (the 1721pdt F1 binary-bonus stall fixed;
  enumeration provably proceeds in lex order).
- M4 exactly the three frozen reflexes with verbatim conditions
  (F2 extra reflex removed, F3 missing H9 restored, F4 condition
  drift corrected).
- K7 instrumentation corrected to the frozen quantity (F7 inversion
  fixed); K7 VOID correctly computed with the addendum's
  zero-denominator handling.
- Evidence chain fully reproducible: sources rebuild with the pinned
  toolchain and reproduce every committed evidence byte.
- Commit ordering, M5 per-iteration commits, pure-Zag discipline,
  and the pre-implementation addendum are exemplary.
- K4/K5 limitations stated honestly; no self-certification.

## Verdict mapping

- K7 fails: the run is VOID as a test of H1/H2. K7 takes precedence
  over the literal K1 and K6 firings per the addendum and the frozen
  validity-gate principle. No DEAD label may be attached to H1 on
  this evidence; no kill claim survives as adopted.
- K1 KILL (918<=1200) and K6 KILL (ablation does not reduce survival)
  are correct literal measurements, recorded as such from a voided
  run.
- K2 survive, K3 ok, C1 PASS, C2 PASS are verified.
- K4 CANNOT-CONFIRM, K5 INCOMPLETE are honest.
- C3 may not be recorded PASS as written (finding R1).

## Required before certification of this attempt

1. Correct finding R1: strike or repair the C3 "3 qualitatively
   distinct strategies" claim (and the "behaviorally distinct by
   construction" comment in e1c_calib.zag), or field a third
   genuinely behaviorally-distinct surviving calibrator and
   re-record C3 on behavior, not median counts.
