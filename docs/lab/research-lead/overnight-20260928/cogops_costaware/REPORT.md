# REPORT: COGOPS-COSTAWARE (cost-aware strategy selection)

Date: 2026-10-03. Worker: COGOPS-COSTAWARE.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_costaware/`
Prereg: frozen commit 3abbd4371 (PREREG.md + NAMECHECK.md,
committed alone before any implementation file existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (K1..K13 all PASS, with transparent erratum E1)

The strategy table's cost column now drives selection:
`strat_sel` picks by EFFICIENCY (wins per logged comparison,
exact integer cross-multiplication) instead of win-rate. The
landscape changes measurably: on the fresh partial goal 823 (S8)
PW leads on efficiency (0.4 > 0.25), fails, and NEED rescues (6
logged comparisons vs 4 when NEED led first under win-rate); on
the period-3 goal 821 (S9) PW leads (2/7 > 2/8), fails, and NEED
rescues at lag 3 (8 events vs 6). The hedge survives on an
efficiency tie (S12: PW[2,2,4] and NEED[1,1,2] both 0.5 ->
ALT chosen). And WHOLE wins for the first time in the program's
history (S13): lesioned table, PW leads on efficiency and fails
at pass 2, efficiency-ordered rescue surfaces WHOLE ahead of
scoreless NEED, and WHOLE's lag-direct order verifies the lag-3
oscillation in 2 comparisons. The preregistered structural
prediction holds: WHOLE never EARNS THE LEAD under pure
efficiency (zero wins -> zero score while any strategy has
wins), but it CAN win when rescue order surfaces it.

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: cold table, DET-STRAT chosen=1 | byte-exact | PASS |
| K2 | S5: PW leads (eff 1/2), 1 DET-CMP | byte-exact | PASS |
| K3 | S7: PW leads (2/3), fail; SWITCH 1->2; WHOLE fail; SWITCH 2->3; NEED wins mask=7 | byte-exact | PASS |
| K4 | S8: PW leads (DET-STRAT chosen=1, NOT NEED); PW 2 CMP fail; SWITCH 1->3; NEED 4 NCMP win; HYP lag=2 p=3 q=1; passes=5 | byte-exact | PASS |
| K5 | S9: PW leads (2/7>2/8); 2 CMP fail; SWITCH 1->3; NEED 6 NCMP, HYP lag=3 p=3 q=0; passes=5 | byte-exact | PASS |
| K6 | S10: PW leads (28>27 cross-mult); cascade PW->NEED->WHOLE->ALT all fail; passes=9; AGREE=1 | byte-exact | PASS |
| K7 | S9B: 2 DET-APPLY match=3/3; OSC-CYCLE = S7's | byte-exact vs corrected (see E1) | PASS |
| K8 | S11: zeroed -> chosen=1; cascade; 15 comparisons; NEED wins | byte-exact | PASS |
| K9 | S12: efficiency tie -> DET-STRAT chosen=4 (hedge); ALT wins via NEED-form | byte-exact | PASS |
| K10 | S13: PW[3,2,6] leads (chosen=1); PW 2 CMP fail; SWITCH 1->2; WHOLE wins (2 CMP, HYP lag=3 p=3 q=0); prior=3 | byte-exact | PASS |
| K11 | 3/3 byte-identical stdout, stderr empty | sha256 c8211890 x3; .err 0 bytes | PASS |
| K12 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction, proven nesting shape | verified | PASS |
| K13 | prefix cmp-identical; base cmp-identical; additive diff = strat_sel only; zero literals | all verified | PASS |

SUMMARY-DET: `agree=1 plans_built=7 plans_loaded=4 trials=6
declines=0 prior=3 strat_pw=4,2,8 strat_who=1,1,2 strat_need=2,0,8
strat_alt=0,0,0` (byte-exact as predicted).

## Erratum E1 (transparent; prereg NOT silently amended)

S9B OSC-STATE src: the PREREG Section 7 carried `src=1` from
COGOPS-STRATEGY's prereg TEXT, but COGOPS-STRATEGY's own erratum
E2 had already corrected the observed value to `src=0`
(`dump_osc_state` prints the outcome record's src field, 0 at
store time, not R's src flag). The binary produces `src=0`,
byte-identical to COGOPS-STRATEGY's actual S9B output. This is
the worker's transcription slip, not a mechanism defect; the
design, the selection rule, and every substantive bar condition
are unaffected. One line, one character.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported per
invocation; `$HOME/safebin` verified directly: 49 entries, no
python3/python; the lane's safebin_setup script does not exist in
this checkout, same finding as the predecessor workers).
`which python3` / `which python` return nothing before and after;
pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure Zag;
shell only for znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations, no near-misses. New Zag scanned
for the `while.*!(` negated-conjunction pattern: clean; the new
`strat_sel` keeps the exact nesting shape of the proven
COGOPS-STRATEGY version (only compared columns change).
Git writes via /usr/bin/git absolute path, explicit pathspecs,
current branch only, nothing pushed.

## Evidence detail

The right cost metric (preregistered 2.1, confirmed by the run):
logged comparison events (DET-CMP + DET-NCMP). Wall-clock was
rejected before implementation (nondeterministic; breaks K11);
pass count was rejected (too coarse to see the PW/WHOLE order
difference); substrate fact-check counters were rejected (they
measure generic machinery, not the strategy choice). The metric
is deterministic, learner-observable, and exactly the work unit
whose order differs between the forms.

Landscape change, measured (K4/K5): under win-rate, S8 was
"NEED leads first, 4 comparisons" (the strategy-transfer bar)
and S9 was "NEED leads, fails, PW rescues". Under efficiency,
S8 is "PW leads (0.4 > 0.25), fails (2 CMP), NEED rescues (4
NCMP)": 6 comparisons, transfer via rescue. S9 is "PW leads
(2/7 > 2/8), fails (2 CMP), NEED rescues at lag 3 (6 NCMP)": 8
events vs 6. Cost-aware selection does NOT minimize this
episode's comparisons: efficiency rewards historically cheap
wins, so the historically-cheap PW is tried first and fails,
adding its failure cost. The learner has no per-goal cost
model; the table is global. That is the honest, non-obvious
finding: "cost-aware" here means cheap-per-win over history,
not cheapest-now.

WHOLE's first win (K10/S13): with PW[3,2,6] (eff 1/3) leading
and NEED[2,0,8] (eff 0) scoreless, PW fails at pass 2 ((2,0),
(2,1) both eq=0; lag 3 inapplicable), the rescue rule picks
among zero-efficiency WHOLE/NEED/ALT by id -> WHOLE, and
WHOLE's lag-direct order proposes (3,1) eq=0 then (3,0) eq=1:
hypothesis at lag 3, verified, in 2 comparisons. PW's
recency order needed 3 comparisons for the same detection (S9
pattern). WHOLE's order advantage is real and now has a win to
its name: strat_who=1,1,2.

The preregistered structural "no" also held: at no point does
WHOLE earn the LEAD. Under pure efficiency a zero-win strategy
scores zero while any strategy has a win, and untried scores
zero by preregistered choice; WHOLE is tried only in rescue.
S10's close call (PW 2/9 vs NEED 3/14, cross-mult 28 > 27)
kept PW leading and reproduced the E1-corrected cascade
order exactly.

Causal/lesion bars intact: S11 (zeroed table -> cold PW
default, 15-comparison cascade) and S12 (efficiency-tie lesion
-> hedge -> ALT, DET-STRAT chosen=4, not the id tie-break)
both behave as the table state dictates under the new rule.

Structural non-use (K13): c11_learn.zag lines 1..1331 are
cmp-identical to c10_learn.zag lines 1..1331; c11_base.zag is
cmp-identical to c10_base.zag; diff of the additive sections
shows exactly the `strat_sel` replacement (comments plus
wins/cost for wins/uses); zero world/goal/relation/need
literals in the additive section and driver outside the
harness lesion fns (goal constructors live in c11_world.zag).

## What this establishes (and does not)

Establishes: folding the tracked cost into selection as
efficiency (wins/comparison) changes which strategy leads and
the rescue order, with byte-exact, lesion-responsive behavior;
WHOLE can win when efficiency-ordered rescue surfaces it, and
its lag-direct order verifies cheaper (2 vs 3 comparisons) than
PW's recency order on lag-3 full oscillations; the right cost
metric for this substrate is logged comparisons, not
wall-clock, passes, or fact-checks.

Does not establish: learner-invented cost-awareness (the
efficiency rule is researcher-provided, like the win-rate rule
was; only the table values are learner-written); WHOLE earning
the lead (structurally impossible under pure efficiency;
predicted and confirmed); L3 representational invention;
per-context selection (table still global); optimality of
efficiency among cost-aware rules. The optimistic variant
(score (w+1)/(c+1)), which WOULD let untried WHOLE lead on
fresh full oscillations, is explicit future work, not
implemented here.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_costaware/`:
PREREG.md (frozen, commit 3abbd4371), NAMECHECK.md (Step 0),
c11_base.zag (cmp-identical to c10_base.zag), c11_world.zag
(c10_world.zag plus mk_goal824_E2), c11_strat_additive.zag (only
strat_sel changed), c11_learn.zag (prefix cmp-identical plus
additive), c11_main.zag (driver plus S13, retied S12 lesion,
strat_lesion_s13), c11_build.sh, c11_full.zag (assembled; exactly
one `fn main`), c11_bin, c11_compile.txt, c11_run1/2/3.txt
(sha256 c8211890 x3) + .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Optimistic efficiency ((w+1)/(c+1)): test whether untried
   WHOLE earns the lead on fresh full oscillations; compare
   exploration cost vs pure efficiency's exploitation.
2. Per-context strategy tables (COGOPS-STRATEGY follow-up 1):
   the S8/S9 finding (cost-aware costs MORE this episode)
   comes from the global table; a learner-computed context
   signature could keep PW's cheapness where it suffices.
3. Expected-cost selection: fold P(fail)*rescue-cost into the
   score so the rule prices the failure it is about to cause
   (S8's 2 wasted CMP are currently invisible to the rule).
4. Learner-composed strategy forms (COGOPS-STRATEGY follow-up
   3): assembling proposal orders from primitives, the actual
   invention step above choosing among given forms.
