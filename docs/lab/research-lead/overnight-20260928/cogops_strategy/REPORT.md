# REPORT: COGOPS-STRATEGY (learner-chosen detection strategy)

Date: 2026-10-03. Worker: COGOPS-STRATEGY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_strategy/`
Prereg: frozen commit 28bd94089 (PREREG.md + NAMECHECK.md,
committed alone before any implementation file existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (K1..K12 all PASS, with transparent errata E1-E3)

The learner chooses the detection strategy from its own
verification history. On goal 822 (partial oscillation, world F)
the cold table defaults to PW; PW's whole-state proposals fail,
WHOLE's lag sweep fails, and NEED's per-need subset form wins,
storing a partial checker (mask 7). On the fresh goal 823 the
strategy table's win-rate (NEED 1.0 from S7) makes NEED lead
FIRST: 4 comparisons instead of S7's 8 before NEED ran. That is
the strategy-transfer bar, the direct analog of
COGOPS-DETECTION's prior transfer. On period-3 goal 821 NEED
leads but fails (lag 3 inapplicable at pass 2, lag 2 trivially
rejected) and PW rescues via recency reaching lag 3. On the
convergent goal 816 all four strategies fail and the generic
fallback reproduces the oracle (AGREE=1). Zeroing the table
(S11) restores the cold PW default with a full fail cascade
(15 logged comparisons vs 7 when NEED leads). A lesioned PW/NEED
tie (S12) triggers the alternation hedge: ALT is chosen and
detects via its NEED-form pass.

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3 block Sec 7: cold table, DET-STRAT chosen=1, PRIOR 0, 2 DET-CMP, HYP lag=2 mask=7, SET 2, Q how=1 passes=4 | byte-exact | PASS |
| K2 | S5 block: DET-STRAT chosen=1, PRIOR 2, exactly 1 DET-CMP (prior pair hits), HYP, Q how=1 passes=4 | byte-exact | PASS |
| K3 | S7 block: PW 2 CMP fail, SWITCH 1->2, WHOLE 2 CMP fail, SWITCH 2->3, NEED 4 NCMP win, HYP mask=7, Q how=1 passes=6 | byte-exact | PASS |
| K4 | S8 block: DET-STRAT chosen=3 FIRST (NEED 1.0 from S7), 4 NCMP, HYP, Q how=1 passes=4 | byte-exact | PASS |
| K5 | S9 block: NEED leads, 3 NCMP fail (lag-2 trivial, lag-3 inapplicable), SWITCH 3->1, PW wins via (3,0), HYP lag=3 q=0, SET 3, Q how=1 passes=5 | byte-exact | PASS |
| K6 | S10 block: all four fail, Q how=0 passes=9, AGREE=1 | byte-exact vs corrected Sec 7 (see E1) | PASS |
| K7 | S9B block: 2 DET-APPLY match=3/3, CYCLE byte-identical to S7's, OSC-REUSE, STATE mask=7 | byte-exact vs corrected Sec 7 (see E2) | PASS |
| K8 | S11 block: zeroed table, DET-STRAT chosen=1, cascade PW->WHOLE->NEED, 15 logged comparisons > S8's 7, Q how=1 passes=6 | byte-exact | PASS |
| K9 | S12 block: lesioned tie, DET-STRAT chosen=4 (hedge), ALT PW-form 2 CMP fail, NEED-form 4 NCMP win, 9 comparisons > S8's 7, Q how=1 passes=5 | byte-exact | PASS |
| K10 | 3/3 byte-identical stdout, stderr empty | sha256 316b1ccd x3; .err 0 bytes | PASS |
| K11 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction | verified | PASS |
| K12 | c10_learn prefix cmp-identical to c9_learn lines 1..1331; c10_base cmp-identical; zero osc_review in additive+main; zero literals in additive | all verified | PASS |

SUMMARY-DET: `agree=1 plans_built=6 plans_loaded=4 trials=6
declines=0 prior=2 strat_pw=2,2,4 strat_who=0,0,0 strat_need=2,2,8
strat_alt=1,1,6` (plans_loaded corrected per E3).

## Errata E1-E3 (transparent; prereg NOT silently amended)

These are hand-derivation slips by the worker in PREREG Section 7,
discovered by running the implementation. The mechanism implements
the frozen design faithfully; the corrected predictions below
match the binary byte for byte. None of the errata changes the
design, the selection rule, or any substantive bar condition.

**E1: S10 lead strategy (Section 7 line 138 and S10 block).**
The PREREG predicted `DET-STRAT chosen=3` (NEED leads on the
convergent goal). Observed `chosen=1` (PW leads). Cause: the
worker tallied PW at 2 wins when predicting S10, but PW won S3,
S5, AND S9 (3 wins, 4 uses, rate 0.75), while NEED has 2 wins,
3 uses (rate 0.67). 0.75 > 0.67, so PW correctly leads under the
frozen win-rate rule. The observed S10 trace (PW fails at pass 2
-> SWITCH 1->3 -> NEED fails at pass 3 -> SWITCH 3->2 -> WHOLE
fails at pass 4 -> SWITCH 2->4 -> ALT fails at passes 5,6 ->
fallback) is exactly what the design predicts given the correct
table. Every substantive K6 condition holds: all four strategies
fail, no false positive, Q how=0 passes=9, AGREE id=S10 a=1.

**E2: S9B OSC-STATE src (Section 7 line 172).** The PREREG
predicted `src=1` for the reused checker. Observed `src=0`. Cause:
the worker confused R's src flag (R+20=1 on the reuse path) with
the outcome record's src field (record+12, set to 0 at store
time); `dump_osc_state` prints the record's field, as in
COGOPS-DETECTION's own S9 (`OSC-STATE ... src=0`). Corrected
prediction (`src=0`) matches. Every substantive K7 condition
holds: masked APPLY match=3/3 over needs {0,1,2}, OSC-CYCLE
byte-identical to S7's, OSC-REUSE match=2.

**E3: SUMMARY plans_loaded (Section 7 line 214).** The PREREG
predicted `plans_loaded=3`. Observed `plans_loaded=4`. Cause: the
worker forgot that the fallback path's `compose_iter` also calls
`plan_find` and increments plans_loaded (frozen code; the same
reason COGOPS-DETECTION reported 4). S10's fallback contributes
the fourth (det_handle's find plus compose_iter's find).
Corrected prediction (4) matches.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported per
invocation; `$HOME/safebin` verified directly: 49 entries, no
python3/python; the lane's safebin_setup script does not exist in
this checkout, same finding as the predecessor workers).
`which python3` / `which python` return nothing before and after;
pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the builds. All computation pure Zag; shell
only for znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations, no near-misses. New Zag scanned
for the `while.*!(` negated-conjunction pattern: clean;
if-nesting kept at 3 or fewer with hoisted flags per the znc
defect notes. One implementation adjustment was made to meet the
frozen Section 7 event order (DET-STRAT before DET-PRIOR): the
design does not specify the order; the code now logs the choice
before the prior context. Git writes via /usr/bin/git absolute
path, explicit pathspecs, current branch only, nothing pushed.

## Evidence detail

Strategy transfer, not fixed order (K4): on goal 823 the table
holds NEED[1,1,4] (rate 1.0, from S7's win) vs PW[3,2,5] (0.67).
The learner's first selection is NEED (DET-STRAT chosen=3); 4
per-need comparisons, hypothesis, confirm, verified. S7 needed
8 logged comparisons before NEED ran (2 PW + 2 WHOLE + 4 NEED).
A researcher-written dispatch (always PW first) cannot produce
chosen=3 here.

Switching rescues failure (K3/K5): S7 shows PW->WHOLE->NEED with
DET-SWITCH lines driven by the table order (id tie-break among
untried). S9 shows NEED->PW: NEED's subset rule cannot see lag 3
at pass 2 (inapplicable) and rejects lag 2 as trivial (only the
carrier matches); PW's recency order reaches (3,0) and verifies
lag 3. The rescue order is the table's, not a fixed sequence.

Capability boundary (K3/K6): NEED is genuinely different from the
whole-state forms. On partial oscillation (need3 drifts), PW and
WHOLE cannot hit (12 proposals fail across S7's cascade); NEED's
subset {0,1,2} verifies at lag 2. On convergent 816, NEED's
non-triviality guard rejects the carrier-only match set, and all
four forms fail.

Causal lesion (K8): zeroing the strategy table restores the cold
PW default (DET-STRAT chosen=1) on goal 823; the full cascade
PW->WHOLE->NEED costs 15 logged comparisons vs 7 when NEED leads
(S8). The table's values causally drive the choice.

Hedge rule (K9): the lesioned table (PW[2,2,4], NEED[2,2,8],
tied at 1.0) triggers the PW+NEED tie hedge: DET-STRAT chosen=4,
not the id tie-break (which would pick PW). ALT's PW-form fails
(2 CMP), its NEED-form verifies lag 2 (4 NCMP). The choice
responds to the table state as specified.

Partial reuse (K7): the S7 checker (mask 7) applies on
re-presentation: only needs {0,1,2} are compared (DET-APPLY
match=3/3); the drifter's stale stored phases are excluded by
the mask. The mask is learner-state written at verification.

Structural non-use (K12): the additive section and main contain
zero `osc_review` references and zero world/goal/relation/need
literals (comments included); c10_learn lines 1..1331 are
cmp-identical to c9_learn lines 1..1331; c10_base is cmp-identical
to c9_base.

## What this establishes (and does not)

Establishes: the learner chooses the detection strategy from its
own verification history (L2 structural learning, one rung above
COGOPS-DETECTION's instance invention). The strategy table's
values (uses/wins/cost) are written only from the learner's
episodes; the first-choice strategy and the rescue order follow
from them; lesions change the choice with measurable cost
signatures; a genuinely different per-need form (subset
detection with a non-triviality guard and masked checkers) is
selected by experience, not by researcher routing.

Does not establish: learner-invented strategy FORMS (the four
forms, the hypothesis rules, the turn budget, the win-rate rule,
the id tie-break, the PW+NEED hedge, and the cold PW default are
researcher-provided); L3 representational invention (no new
primitive or representational form; the 12-criterion bar is not
claimed); per-context strategy selection (the table is global);
cost-aware selection (cost is tracked and reported but does not
drive choice; WHOLE never earns a win in this battery: it is
capability-identical to PW per pass, differing only in
proposal order and cost, and win-rate selection never prefers
it; see PREREG 2.6).

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_strategy/`:
PREREG.md (frozen, commit 28bd94089), NAMECHECK.md (Step 0),
c10_base.zag (cmp-identical to c9_base.zag), c10_world.zag
(c9_world.zag plus world F and goals 822/823),
c10_strat_additive.zag (the additive section source),
c10_learn.zag (c8 prefix cmp-identical plus the additive
strategy section), c10_main.zag (S1A..S12 driver),
c10_build.sh, c10_full.zag (assembled; exactly one `fn main`),
c10_bin, c10_compile.txt, c10_run1/2/3.txt (sha256 316b1ccd x3)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Per-context strategy tables: key the table by a
   learner-computed context signature so cheaper strategies
   (PW/WHOLE) are preferred where they suffice and NEED only
   where partial oscillation demands it.
2. Cost-aware selection: fold the tracked cost into the
   selection rule; test whether WHOLE's lag-direct order earns
   the lead on fresh full oscillations.
3. Learner-composed strategy forms: the next rung after choice
   among given forms is assembling new proposal orders from
   primitives (the actual strategy-invention step).
4. Exercise the retract path: a coincidental early match would
   test hypothesis-falsification inside a strategy turn.
5. Cross-goal analogy for strategies: whether a NEED win on one
   partial goal accelerates NEED's selection on a structurally
   similar but new partial goal beyond the global table.
