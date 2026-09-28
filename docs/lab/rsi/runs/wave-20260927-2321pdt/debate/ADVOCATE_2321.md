# Advocate brief: wave-20260927-2321pdt (five motions)

Role: advocate FOR the proposed adoption slate.
Wave: 20260927-2321pdt. Branch: tnn-native-lab.
Working copy: ~/workspace/tnn-rsi.
Records judged: exp1c/REDTEAM_EXP1C_2321.md (commit 3636d2fe4),
forks/FORK_RESULTS_2321.md (commit 9926b0860),
design_lane/HUNT_2321.md (commit 3dc45ca35),
INTERACTIVE_SURVEY_2321.md (commit 9c6646c04).
Binding precedent: the 2021pdt verdicts and judge rulings e97d1b9c0
("a void test cannot kill a hypothesis"; K6 operationalization R3
recorded as reasonable; the section-7 addendum d9e96ad91 ruled
judge-legitimate; K4 CANNOT-CONFIRM and K5 INCOMPLETE honestly
reported per frozen text).

Standing rules observed in this brief: pure Zag discipline (no code
in this brief, no Python), no em-dashes anywhere, nothing pushed,
the six governance rulings undecided and unrelitigated, all sealed
blind pairs untouched, Micah's frontier dirs untouched.

## M1: ENTER EXP1c iteration 3 as VOID as a test of H1/H2 (K7-VOID)

The advocate moves that iteration 3 enter the record as VOID as a
test of H1/H2 on K7, with K1 and K6 certified as correct literal
computations recorded as measurements from a voided run (no DEAD
label on H1), and C3 certified PASS with the binding distinctness
fix implemented. The evidence supports every element of this
verdict, and the verdict framing follows binding precedent exactly.

### 1. Independent reproduction is complete and byte-identical

The independent red team recompiled all four drivers from the
committed sources with the pinned znc and reproduced every committed
artifact byte-identically:
- x1c_run.zag ran twice; both outputs byte-identical to each other
  and to the committed evidence/run1.tsv and run2.tsv (SHA-256
  da034c524a9380625f95eef340aa0882a6e068e41a86645cebc748f8202510d2).
- x1c_calib.zag stdout byte-identical to the committed
  iterations/iter3/calib1.txt and calib2.txt (SHA-256
  f0b1d41b254dd441aa53ecd5d73f80b9c79c9f4aa13ea058239dc82ea9bccb57).
- x1c_evidence.zag stdout byte-identical to the committed
  evidence/EVIDENCE_EXP1C.md (SHA-256
  8dbaed7673a409a332fd5ad2fe4242e6b2a05c1e0d58789295aa478bd9afaf33).
- x1c_emit.zag stdout byte-identical to iterations/iter3/variants3.txt.
- x1c_check.zag prints ALL_PASS=1, exit code 0, and gates both
  calibration and the full run in the drivers.

This is not the worker's word; it is a second party's compile and
run. The determinism claim is verified, not asserted.

### 2. M3 verbatim and M4 exhaustive and exclusive, both verified

- M3: the scoring is the frozen formula verbatim (score = mean
  experienced delta-energy + B0/(1+n) with integer division),
  deterministic argmax with strict-greater tie-break so enumeration
  proceeds in M1 lex order (IDIAG n_distinct reaches 399 for I arms
  in 7 runs, confirming the 1721pdt F1 stall stays fixed); the only
  scoring constants anywhere are the two frozen B0 values (40 for
  arms 3 and 5, 120 for arms 4 and 6); grep confirms no
  per-composition bonuses exist.
- M4: the I arm contains exactly the three frozen reflexes and no
  others (storm flee on storm-active in-zone unsheltered, energy
  emergency below 25, H9 void refusal as the final gate on every
  step, plan step or reflex action). The H9 plank carve-out mirrors
  the frozen world's own void-fall rule and step clamp, which is
  fidelity to the frozen physics, not condition drift. The 1721pdt
  F2 mote-adjacent preemption stays gone. The P-arm storm
  anticipation is inherited taught content (kb_p_exp1c.txt Phase 4a
  verbatim), not an implementation-added reflex.

### 3. The binding C3 distinctness fix is implemented and verified

This is the wave the 1721pdt F10 and 2021pdt R1 corrections were
binding on, and they are now done both ways:
- The corrected C3 check runs IN ZAG (x1c_calib.zag lines 130-146):
  per-variant (ticks, e_end) outcome-vector comparison, dXY counting
  variants where strategies X and Y differ, pairwise distinctness
  requiring dXY >= 1; C3 passes iff all three calibrator medians are
  >= 720 AND all three pairs are vector-distinct.
  x1c_evidence.zag recomputes the same check independently from the
  parsed CALIB rows (lines 258-268).
- Hand-verified from calib1.txt: d01=7 (f0 vs f1 differ in variants
  0,1,3,4,6,7,10), d02=12, d12=12. The claimed vector diffs are
  correct.
- The third calibrator is genuinely a different decision rule, not a
  parameter tweak with identical outcomes: f2_patrol is an open-loop
  oscillation on the fixed segment [home-2, home+2] with no target
  seeking at all; it eats only ACTIVE motes on its cell (f0/f1 eat
  any mote on cell); storms send it home to wait (f0 is storm-blind,
  f1 flees the zone); energy below 25 runs the taught survival
  reflex (f0/f1 have no energy branch). The outcome data confirms
  behavioral difference: f2's vector differs from f0 in all 12
  variants and from f1 in all 12 variants.
- All 12 variants satisfy the documented family constraints,
  verified against variants3.txt; the mode check (ALL_PASS=1,
  independently reproduced) gates calibration.

C3 PASS is certified on evidence, not on the false premise that
struck the 2021pdt C3 claim.

### 4. The verdict framing follows binding precedent exactly

- K7 fails: 0/13 and 0/94 learned-credit fractions, both below
  0.50. Under the frozen verdict mapping and the redrafted section
  7 addendum ("K7 takes precedence over any K1 firing"), a
  validity-gate failure voids the run as a test of H1/H2. The
  2021pdt judge confirmed the precedent: a void test cannot kill a
  hypothesis. No DEAD label may attach to H1 on this evidence.
- K1 fires literally (266 <= 1200) and K6 fires literally on both
  ablation arms (1200 >= 266; 1200 >= 269). The red team certified
  these as correct literal computations on correct data; the
  generator's K7 rule implements the frozen quantity with the
  addendum's zero-denominator handling; the ablation is a genuine
  intervention (COMBINE-containing sketches excluded from I-arm
  selection; I-arm medians move 266->1200 and 269->1200; M4 reflexes
  preserved, so no EXP1b-style void-reflex dropout confound; the
  sketch-space maximum 258 is consistent with n_distinct=258 in
  every ablation run). They fire, so there is no suspicion of a
  rigged-to-pass ablation. They are recorded as measurements from a
  voided run, exactly the 2021pdt reading.
- K4 is honestly CANNOT-CONFIRM (no audit attempted; with K7 VOID
  there is no learned strategy to audit) and K5 is honestly
  INCOMPLETE (no independent auditor; implementer cannot
  self-certify), exactly as the frozen text requires.
- New knowledge, first measured this wave in EXP1c: actual
  post-enumeration choice behavior under a decaying novelty bonus,
  and the choice phase is nearly absent (0/13 and 0/94
  learned-credit selections) even where enumeration completed, with
  enumeration-phase deaths dominating I-arm survival.

### 5. Honest reporting throughout

The worker disclosed the milestone-3 bug fixes in x1c_evidence.zag
(CALIB completeness check iterating 0..36 over an s*36+v layout,
missing s=1/s=2 entries; median work areas using base offset 100 in
a 128-element slice, exceeding bounds). The diff 7fbd485b6..0563e0cce
shows exactly these two minimal fixes and nothing else, and the
note was generated with the fixed version (byte-identical
reproduction confirms). There are no corrupt summary sections, no
verdict blocks contradicting computed truth, no hand-written BARS
blocks, no internal contradictions of the 1721pdt F6 kind. The
disclosure was honest and complete.

Weak points conceded: the evidence note does not print the
addendum's explicit max-enum_tick comparison line (observation O1;
the per-run rows carry the data and the maximum 1183 is derivable,
so this is documentation completeness, not evidence corruption);
K4 and K5 are honestly unconfirmed and incomplete, which bounds what
this run can ever claim; the EXP2-K4 F2 amendment and the
redesign-or-retire call are Micah's decisions, not this wave's.

M1 stands on verified reproduction, verified verbatim mechanisms,
the corrected binding fix, honest limits, and a verdict framing
that matches binding precedent line for line.

## M2: CONFIRM the fork battery [clean]

The advocate moves confirmation of the fork battery as a process
confirmation (toolchain and extraction stability only):
- 56 named entries, 54 PASS, 0 FAIL, 2 UNTESTABLE. The two
  UNTESTABLEs are the expected rh-pull-1-head and rh-pull-2-head
  (non-TNN research-doc trees, pinned toolchain path absent,
  identical cause fourteen waves running, content-dependent and not
  a toolchain regression, never headlined without this caveat). No
  new FAIL; the 1721pdt probe-loss FAIL stays closed.
- Run-start HEAD pinned to baf48e474; read-only git throughout (no
  checkout, pull, push, fetch, reset). The harness was extracted
  read-only and rebuilt pure-Zag byte-identical to the frozen
  instrument (a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).
  The pinned znc (SHA-256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef)
  is uniform across all 54 tested entries; probe source, B1/B2/B3,
  both negative controls discriminating, and the tree probe
  (R32_ZNC_PROBE_OK) verified on all 54.
- The new live archive branch (tnn-native-lab-wave-archive-wave-20260927-2021pdt)
  was tested first in the batch at baf48e474 and PASSES; the moved
  local tip PASSES with the toolchain-dir repair intact (37d1d3cab
  is an ancestor of baf48e474, confirmed; the 12 restored files are
  byte-identical). No missing branches; all remote heads identical
  at run start and close.
- Unique-commit count 44 recomputed from this wave's own verdict
  table, per the standing hygiene rule (44 to 44: +baf48e474, minus
  the superseded fc1a43b8c). Coverage-delta accounting is in the
  report.
- The mid-run local HEAD move (baf48e474 to 9c6646c04, another
  lane's commit) was inert under pinned-commit extraction and is
  documented as an incident with the new commit left for the next
  wave's enumeration. Zero Python ran in the worker's work
  (attested).

## M3: CONFIRM the design lane NULLs

The advocate moves confirmation of the design-lane verdicts
(NULL on mechanisms and sensory, HELD on EXP2-K4, COMP2-P11, and
trades), because HUNT_2321.md meets the 1721pdt forward bar for an
honest NULL in full:
- Survey method with counts: 11-commit first-parent range,
  1,210 files changed, zero new frozen preregs in loop scope,
  term searches with hit classification (26 "mechanism" hits all
  resolved to non-candidates; B1-class terms resolved).
- Per-lane blocker evidence with commit ids: EXP2-K4 blockers 1-3
  with corpus state (27 round-3 run outputs, f71ff91f6; TA-CORPUS
  v1 seal 879bbb4cf closed), PREREG_EXP2_K4.md draft state
  (09bfaae63 header-only, text frozen at 59b9df4b0); B1 lane with
  the DISCARD chain (60a057997, 11a787da6, 7b5b694e0) and zero
  loop-owned changes to docs/lab/image_upscale/ since DISCARD;
  COMP2-P11 with ruling 6 still OPEN and the K-HA-3 distinction
  confirmed; trades with the cost-capability frame and the
  judge-flagged chaining noted.
- Explicit nothing-manufactured statement: no candidate invented,
  no knob costumed as a capability, no closed-frontier artifact
  ingested, no sealed blind pair touched, no verdict padded.
- The EXP2-K4 redesign-or-retire path is a RECOMMENDATION, not a
  decision: the technical track is loop-executable, the governance
  track (F2 spec-blindness, "real failures" acceptance, the
  retire/keep call) is Micah's, and a 3-wave expiry clause kills
  the permanent-HELD risk. Nothing here decides or pre-decides any
  of his six rulings.

## M4: CONFIRM the interactive survey NONE

The advocate moves confirmation of the NONE verdict, because
INTERACTIVE_SURVEY_2321.md surveys the merge range
fc1a43b8c..baf48e474 with a method and full hit accounting:
- 11 commits, all tnn-rsi-loop authored, zero Micah commits; 1,208
  files added, 222 of them *.zag; a 4,149-line added-file *.zag
  diff scanned for chat, repl, stdin, readln, readline, argv,
  interactive, tui, plus raw fd-0 reads; the 986 non-.zag files
  scanned separately.
- Zero genuine interactive hits; every keyword match enumerated as
  a false positive (repl = the n_replans field in fork-battery
  evidence; argv = the execve spawn helper in fork_battery.zag;
  tui/chat/stdin/readln/readline/interactive zero in new sources;
  fd-0 reads zero in all 222 added .zag files).
- The previously surveyed entries (Micah's h1/h2/h3 chat REPLs,
  wb3_nosynth/wb3_stringrule, d2bin tui) remain his closed frontier:
  read-only awareness only, never built, run, certified, or
  re-judged. No loop-owned interactive exists beyond the frozen
  batch probe instruments (batch-only). No Python used.

## M5: CONFIRM the commit-order self-check VALID

The advocate moves confirmation that the commit-order self-check is
VALID:
- The frozen prereg 8b456736b is a strict ancestor of every wave
  commit; verified chain d9e96ad91 < 7fbd485b6 < 26669a08d <
  0563e0cce, each strictly preceding the next (merge-base
  verified).
- The section-7 redraft addendum d9e96ad91 was committed alone
  before any EXP1c implementation file existed (judge-legitimate
  per the 2021pdt ruling: authorized by the 1721pdt binding
  forward requirement, pre-implementation, changing no bar, gate,
  mechanism, horizon, or bonus number).
- Iteration sources first appear at 7fbd485b6 (git log
  --diff-filter=A on the exp1c source tree); the evidence note
  first appears at 0563e0cce.
- Standing caveat carried: commit order evidences commit order
  only, never run order and never content identity.

## The skeptic's provenance probe, answered once

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

New this wave: all nine x1c_*.zag sources (written from scratch,
first committed at 7fbd485b6); the 12 dispersed-mote variants
(emitted by x1c_emit.zag, byte-identically reproduced); the
calibration TSVs; the 84 RUN + 48 IDIAG rows of the full experiment
(RUN SHA-256 da034c52..., CALIB SHA-256 f0b1d41b..., evidence note
SHA-256 8dbaed76...); the evidence note (first committed at
0563e0cce); the fork battery's fresh full execution; the design
lane HUNT_2321 report; the interactive re-survey report. Inherited
and unchanged: the frozen prereg 8b456736b (with the section-7
redraft d9e96ad91), the 24-cell world physics template (blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a, the frozen bounce fix),
the EXP1c training mass pair (kb_exp1c.txt, kb_p_exp1c.txt,
verbatim since 5a043af3c, recipe table excluded), the P/R/Z arm
concepts, and the pinned toolchain (SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Prior attempts are lineage, not content: the 1721pdt and 2021pdt
attempts used different source files and different variant
families, and their red-team findings are what this wave answers,
not material it reuses. Nothing is a re-certified old render; the
six governance rulings and all sealed blind pairs are inherited
and untouched.

## Adoption slate (moved)

M1: enter EXP1c iteration 3 as VOID as a test of H1/H2 (K7), with
K1/K6 certified as correct literal computations recorded as
measurements from a voided run and C3 certified PASS with the
binding distinctness fix. M2: confirm the fork battery (56 named,
54 PASS, 0 FAIL, 2 UNTESTABLE). M3: confirm the design lane NULLs
with the EXP2-K4 redesign-or-retire recommendation (not a
decision). M4: confirm the interactive survey NONE. M5: confirm
the commit-order self-check VALID.
