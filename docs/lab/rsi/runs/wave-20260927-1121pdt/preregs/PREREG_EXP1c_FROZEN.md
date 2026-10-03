# PREREG EXP1c: Invent-to-Survive Compositional-Choice Design (FROZEN 2026-09-27)

Wave: wave-20260927-1121pdt, candidate lane (freeze).
Status: FROZEN. Kill bars and mechanism text below are sealed. Numbers may
not change by post-freeze edit.
Prereg design commit (lane 3, wave-20260927-0821pdt): 59b9df4b0b45ffef23704ad971ae9029e14d7126.
Training-mass extension commit (pre-freeze, EXP1c M4): 5a043af3c.
Freeze commit: recorded in docs/lab/rsi/runs/wave-20260927-1121pdt/candidates/CANDIDATE_LANE_1121.md
(the commit that adds this document). Commit-order self-check: this prereg
freeze commit strictly precedes any implementation commit (no implementation
exists at freeze time; the implementing wave records the order check).
Pre-run assertion: pre-run, no scores seen. No runs, no analysis, and no
Python contact preceded this freeze.

Redraft changes at freeze time (draft was a draft; numbers change by redraft
only, never by post-freeze edit):
- M4(c) said void-safety was "taught H5". kb.txt already defines H5 as the
  EAT rule (H1 through H8 are all taken). The taught void-safety heuristic
  is H9, appended in the new EXP1c training mass, quoted verbatim in M4.
- The inherited world-physics template path said "src/world.zag". The actual
  committed template is docs/lab/invention/survival/src/world.zag
  (bounce-fixed by commit 938d188cb). Pinned below by commit.
- The training mass is the new EXP1c pair (kb_exp1c.txt, kb_p_exp1c.txt),
  verbatim EXP1b inheritance with documented deltas (horizon, H9). The
  EXP1b mass files are untouched.

## 1. Provenance header (machine-checkable)

COMPONENT_LINEAGE:
- EXP1 invent-to-survive, wave-20260926-2321pdt: DISCARDed. H1 killed on K1
  (I-survive median 574 vs R median 600). K4 killed the invention claim
  independently (candidate scoring carried authored bonuses encoding
  productive compositions).
- EXP1b retune, wave-20260927-0221pdt: invention claim DEAD. K1 PASS 380 vs
  376 recorded as computed arithmetic WITH the mandatory prereg-deviation
  dependency (the implementation added a void-safety reflex absent from the
  frozen M2 text; the reviewer's counterfactual without it gives I median
  102 with 9 of 12 void deaths, so the frozen experiment as written would
  have killed H1 at K1). K4 KILL and K6 KILL verified. K5 AUDITED/NOT FIRED
  with the contamination caveat. "Complete, honest negative" certification
  WITHHELD pending six red-team corrections plus the WAVE_NOTES_EXP1B.md
  deliverable. All six corrections plus the deliverable are committed
  (wave-20260927-0221pdt coordinator commit 463b115b6), verified by the
  freezing wave before this seal:
  (1) evidence_exp1b/A2_ABLATION.md rewrite (clean ablation, drop 0 in all
      12 variants; void-reflex dropout confound documented);
  (2) false "never builds" claims corrected (EVIDENCE_EXP1B.md records I
      builds a LAMP in 6/12 variants, places in 5/12; emergent accidents,
      causally inert);
  (3) heuristic label fixes in evidence_exp1b/NOVELTY_AUDIT.md;
  (4) reflex-dependency record (9/12 void-death counterfactual, I median
      102 without the reflex) in EVIDENCE_EXP1B.md;
  (5) retune-2 verifiability note (retunes 1-2 unverifiable; K1-shopping
      cannot be ruled out) in EVIDENCE_EXP1B.md;
  (6) bounce-bug correction appended to EXP1's BAR_RESULTS.md
      (identity-reflection bug from 74565859f, not original EXP1);
  plus WAVE_NOTES_EXP1B.md itself. Gate a of the freeze-gate check is
  thereby SATISFIED by committed corrections; no "reasons to proceed
  without them" were needed.
- The decisive EXP1b finding this design answers: the B0 novelty bonus
  always exceeded experienced mean delta-energy within 600 ticks, so H2
  (invention instruction vs implicit pressure) was null by construction,
  and the plan logs confirmed pure lex-order enumeration (I-survive and
  I-invent traces byte-identical across all 12 variants). EXP1b measured
  enumeration, not choice.

NEW_KNOWLEDGE_CLAIM: none yet. This prereg proposes the first design in
which the compositional-choice question is non-null: a shrunk plan space,
a longer horizon, and a decaying novelty bonus, so that the enumeration
phase provably ends and the agent must choose among compositions on
learned credit.

Inherited: the 24-cell world physics template
docs/lab/invention/survival/src/world.zag (bounce-fixed by 938d188cb;
dangling "src/world.zag" reference in the draft corrected here), the
training mass (docs/lab/invention/survival/kb/kb_exp1c.txt and
kb_p_exp1c.txt, committed verbatim at 5a043af3c, recipe table excluded),
the P/R/Z arm concepts, and the pinned toolchain
src/tools/toolchain/znc_linux_x86_64_abed8aa1 (SHA-256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
New this design: the M1-M5 mechanism below, the K7 choice-reality bar, and
the frozen retune protocol.

## 2. Question

Can an agent under survival pressure genuinely CHOOSE among novel
multi-step compositions (as opposed to enumerating them in lex order), and
does that choice improve survival over taught single-step heuristics?

## 3. Mechanism (what changes; everything else inherits EXP1/EXP1b)

M1. Shrunk plan space. A plan is a sequence of at most 3 PRIMITIVE actions
from {LEFT, RIGHT, EAT, TAKE, DROP, COMBINE, WAIT}: the candidate set is
the full enumeration of 7^1 + 7^2 + 7^3 = 399 sequences in
length-ascending lex order (vs 2800 in EXP1b). Enumeration provably
completes early in the horizon (section 7 shows the bound).

M2. Longer horizon. 1200 ticks per run (vs 600). The post-enumeration
learned-credit choice phase is the majority of the run, so survival
differences compound on choice, not on enumeration speed.

M3. Decaying novelty bonus. Per-sketch bonus B0(n) = B0 / (1 + n), where n
is the number of times the sketch has been tried. The frozen schedule:
I-survive uses B0 = 40, I-invent uses B0 = 120 with the same decay rule.
After the enumeration phase, untried-composition bonuses are near zero and
the deterministic argmax must rank sketches on learned mean delta-energy.
This makes H2 non-null: the arms differ in how long enumeration dominates,
not in whether it dominates forever. The decay schedule is frozen text;
any implementation deviation voids K1/K2 for that arm.

M4. Reflexes frozen verbatim. The implementation may contain exactly the
following preempting single-step reflexes, and no others: (a) storm-active
and in-zone and unsheltered flees (taught H3); (b) energy below 25 runs
the survival reflex (taught H4); (c) void-adjacent step refusal
(void-safety, taught H9 in this design's training mass: "If the step you
are about to take would land on a void cell: refuse that step."). The
EXP1b lesson is written into law here: any implementation-added reflex not
listed in this frozen text voids the K1 and K2 gates for that run (the gate
that was run was not the gate that was frozen). The training mass carries
taught H9 (kb_exp1c.txt, committed verbatim at 5a043af3c).

M5. Frozen retune protocol (the 0221pdt judge's forward requirement). World
parameters may be retuned only within the frozen rules until C1-C3 pass.
Every retune iteration commits its variants and calibration medians before
the next iteration proceeds, so the stopping rule is checkable. A retune
discard reason must cite a frozen criterion (C1, C2, or C3); "R median
low" is not a frozen criterion and cannot discard a retune. Retune
shopping is thereby auditable.

## 4. Metric it moves

Primary: invent-to-survive margin, median survival ticks per arm over 12
variants (1200-tick horizon). Secondary: compositional-choice rate, the
fraction of post-enumeration plans selected on learned credit rather than
novelty bonus (the K7 guard makes this load-bearing, not decorative).

## 5. Calibration gates (validity; retune within frozen rules until met)

C1: median P >= 960/1200, else the run is VOID (sim broken), not a kill.
C2: median Z < 300/1200.
C3: >= 3 qualitatively distinct scripted strategies each reaching median
>= 720/1200.

## 6. Kill bars (frozen; never moved after the seal)

K1: median(I-survive) <= median(R) kills H1.
K2: median(I-survive) <= median(Z) kills H1 and triggers a sim
investigation.
K3: median(P) < 960 voids the run (sim broken), not a kill.
K4: novelty audit finds a key strategy step in the committed training
mass, or the winning strategy is a trivial recombination (per EXP1 PREREG
section 2): kills the invention claim.
K5: blind cuing audit derives I's key strategy from the training mass,
world rules, and goal statement alone: kills (cuing cannot be ruled out).
The auditor must not have authored the machinery; if no independent
auditor is available the implementer states the limitation honestly and
K5 stays incomplete (no self-certification).
K6: ablation (A2) shows removing novel-composition steps does not reduce
survival: kills the invention claim.
K7 (new, choice-reality): the fraction of post-enumeration plans in the
I arms selected with novelty bonus contributing less than 10% of the
winning score is below 0.50: the choice question is null again and the
run is VOID as a test of H1/H2 (the design failed, not the agent). K7 is
a validity gate, not a kill: it prevents re-measuring enumeration.

Verdict mapping (frozen): H1 (invention improves survival) is adopted only
if K1 passes with margin, K4/K5/K6 do not fire, and K7 passes. Any kill
bar firing means DEAD with killing evidence. K3 or K7 failure means VOID.

## 7. Enumeration-completeness bound (frozen arithmetic)

399 sketches, at most one plan try per replan. Worst case, enumeration
completes within 399 replans. With mean plan length <= 3 ticks plus
replan overhead, enumeration provably completes before tick 600 of the
1200-tick horizon even in the adversarial case, leaving >= 600 ticks of
learned-credit choice. The implementing wave must reproduce this bound
check in the evidence; a shorter actual completion only helps.

## 8. Cost budget

12 variants x 5 arms x 1200 ticks x 2 determinism runs = 144,000
agent-ticks of simulation, pure Zag, pinned toolchain. No wall-clock
budget is evidence; the run count is fixed. Cost is compute only.

## 9. Red-team confound list (considered before this freeze)

1. Knowledge vs architecture (taught content): the training mass is
committed verbatim (kb_exp1c.txt, kb_p_exp1c.txt at 5a043af3c); the
novelty audit (K4) searches the committed mass for each A1 sketch's
composed steps (the composition, not just the words). No multi-step plans
are taught to R, I-survive, or I-invent.
2. Authored productivity bias (EXP1 lesson): scoring is deterministic
argmax over (mean experienced delta-energy + decaying B0); no
per-composition bonuses exist anywhere. The red team greps the sources
for bonus constants beyond B0.
3. Retune shopping (EXP1b lesson): M5 freezes the retune protocol; every
retune's variants and calibration medians are committed; discard reasons
must cite frozen criteria.
4. Reflex smuggling (EXP1b lesson): M4 lists reflexes verbatim; any extra
reflex voids K1/K2. The red team diffs implemented reflexes against M4.
5. Null choice (EXP1b lesson): K7 mechanically guards that the choice
phase exists; the M3 decay schedule is frozen text.
6. Determinism: all 60 runs executed twice; SHA-256 of the full stdout
byte-identical across reruns. Zero RNG in agent decision paths (Z's LCG
is a documented control).
7. Pure Zag: all implementation, runs, and analysis in Zag; shell only to
invoke the compiler, redirect stdout, and hash outputs. No analysis of
any kind may run before the prereg freeze commit (the 0221pdt lesson).
Any Python or shell text-processing of evidence voids certification.

## 10. Standing rules applied

Pure Zag literally (no Python anywhere; any contact voids the evidence).
Frozen kill bars are never moved after the freeze. Missing evidence means
CANNOT-CONFIRM. The prereg freeze commit strictly precedes any
implementation commit (commit-order self-check, to be recorded by the
implementing wave). No em-dashes in this document. The six governance
rulings are untouched. The sealed blind judge queue is untouched. Micah's
frontier files are untouched. Nothing is pushed to GitHub; commits stay
local on tnn-native-lab.

## 11. Gate conditions (satisfied at freeze)

The draft waited on the six withheld EXP1b red-team corrections (or the
freezing wave's recorded reasons to proceed without them). The freezing
wave verified all six plus the WAVE_NOTES_EXP1B.md deliverable committed
in wave-20260927-0221pdt coordinator commit 463b115b6 (evidence itemized
in section 1). Gate satisfied by committed corrections; no governance
ruling gates this design. Implementing wave: prereg freeze commit,
then implementation, strictly.
