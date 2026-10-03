# REPORT: COGOPS-EXPECTEDCOST (expected-cost strategy selection)

Date: 2026-10-03. Worker: COGOPS-EXPECTEDCOST.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_expectedcost/`
Prereg: frozen commit b061f1604 (PREREG.md + NAMECHECK.md +
c14_predicted.txt, committed alone before any implementation file
existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (K1..K14 all PASS)

Expected-cost selection is implemented, and the battery answers
the follow-up question directly: **expected-cost selection does
not beat optimistic efficiency on this battery, and the reason is
mechanism-level, not a tuning artifact.**

The headline results:

1. **The cost model collapses (P0).** Under the learner's
   Laplace estimates, the task's formula E[cost] =
   P(success)*E[cost|success] + P(fail)*E[cost|fail] reduces
   algebraically to (c+2)/(u+2), the smoothed mean comparisons
   per turn. The success-probability terms cancel because the
   learner pays comparisons whether the turn succeeds or fails.
   No new table cells were needed; `cx_wins` is now defined but
   never called by selection. The implementation reads only uses
   and cost.

2. **The optimistic promotion survives in cost form (K4).** The
   untried strategy's cost prior is (0+2)/(0+2) = 1.0, the
   cheapest possible, so S8's ALT still leads strictly
   (cross-multiplication 6 < 8 vs PW, 6 < 12 vs NEED) and the
   6-event ALT tax persists unchanged. Pricing cost did not price
   away the over-exploration.

3. **Exactly one behavioral divergence in 14 stages (K9).** At
   S12 the lesioned table reads PW -> EC 1.5, NEED -> EC 11/7,
   WHOLE/ALT -> EC 2.0. PW is the strict argmin (42 < 44), so
   chosen=1, NOT the hedged 4: the 3/5 efficiency tie is not a
   cost tie (44 != 42), and the hedge correctly does not fire.
   PW fails (2 CMP), SWITCH 1->3, NEED wins at pass 3
   (4 NCMP, HYP lag=2 p=3 q=1). Cost-neutral vs percontext
   (6 events either way), different lead, different winner.

4. **No event reduction (P5).** Battery total S3..S13 (logged
   comparisons, eq=-1 skips excluded): 62 under expected-cost,
   62 under per-context optimistic efficiency. The preregistered
   aggregate prediction (NO, EC does not beat optimistic on
   fewer events) is confirmed.

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: cold (3,606) -> chosen=1 | byte-exact | PASS |
| K2 | S5: cold (3,613) -> chosen=1; PW wins 1 CMP; HYP p=2 q=0 | byte-exact | PASS |
| K3 | S7: cold (4,613) -> chosen=1; PW fail; SWITCH 1->2; WHOLE fail; SWITCH 2->3; NEED wins | byte-exact | PASS |
| K4 | S8: ALT untried EC 1.0 strict cheapest -> chosen=4; 6 events; NEED-form wins | byte-exact | PASS |
| K5 | S9: cold (3,615) -> chosen=1; PW fail; SWITCH 1->2; WHOLE wins lag 3 | byte-exact | PASS |
| K6 | S10: cold (3,604) -> chosen=1; cascade PW->WHOLE->NEED->ALT; 19 events; fallback; AGREE=1 | byte-exact | PASS |
| K7 | S9B: two DET-APPLY match=3/3; how=2; OSC-REUSE | byte-exact | PASS |
| K8 | S11: zeroed -> chosen=1; prior=3; PW->WHOLE->NEED; NEED wins | byte-exact | PASS |
| K9 | S12: PW strict EC argmin (42<44) -> chosen=1 NOT 4; no hedge (44!=42); PW fail; SWITCH 1->3; NEED wins pass 3; 6 events | byte-exact | PASS |
| K10 | S13: WHOLE untried 1.0 strict argmin -> chosen=2; WHOLE fails; SWITCH 2->4; ALT wins lag 3 | byte-exact | PASS |
| K11 | S14: WHOLE strict argmin -> chosen=2; wins 1 CMP | byte-exact | PASS |
| K12 | 3/3 byte-identical stdout; stderr empty; cmp vs frozen c14_predicted.txt silent x3 | sha256 03c8a42a x3; .err 0 bytes | PASS |
| K13 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction, proven nesting shape | verified | PASS |
| K14 | prefix/base/world cmp-identical; additive diff = header comment + strat_sel only (region-verified); main comment-only (non-comment lines identical); zero world/goal/relation/need literals | all verified | PASS |

No errata. The frozen prediction matched on the first build;
no transcription slips (the S13 nph=2 slip was caught by the
worker's own pre-freeze byte-comparison of the PREREG block
against c14_predicted.txt and fixed before the freeze commit).

## Evidence detail

Stage-by-stage vs COGOPS-PERCONTEXT (lead chosen / logged
comparison events, eq=-1 skips excluded):

| stage | pc lead | ec lead | pc events | ec events |
|-------|---------|---------|-----------|-----------|
| S3 | 1 (PW) | 1 (PW) | 2 | 2 |
| S5 | 1 (PW) | 1 (PW) | 1 | 1 |
| S7 | 1 (PW) | 1 (PW) | 8 | 8 |
| S8 | 4 (ALT) | 4 (ALT) | 6 | 6 |
| S9 | 1 (PW) | 1 (PW) | 4 | 4 |
| S10 | 1 (PW) | 1 (PW) | 19 | 19 |
| S9B | reuse | reuse | 0 (+2 APPLY) | 0 (+2 APPLY) |
| S11 | 1 (PW) | 1 (PW) | 12 | 12 |
| S12 | 4 (ALT, hedged) | 1 (PW) | 6 | 6 |
| S13 | 2 (WHOLE) | 2 (WHOLE) | 4 | 4 |
| S14 | 2 (WHOLE) | 2 (WHOLE) | 1 | 1 |

Totals S3..S13: 62 (percontext) vs 62 (expected-cost).

The two rules agree on 13/14 stages because (a) the untried
strategy scores extremally under both (1.0 = max efficiency =
min cost), so all cold-context behavior is identical, and
(b) on tried strategies in this battery, wins-per-cost and
cost-per-turn order the strategies the same way except where
the S12 lesion engineered an efficiency tie (3/5 vs 3/5) that
is not a cost tie (6/4 vs 11/7).

Calibration notes (observed, not kill-barred): neither rule is
calibrated on untried strategies by construction (S8: ALT
estimated 1.0, realized 6, under both rules). On tried
strategies, EC's S12 estimates show mean-cost smoothing
under-pricing an expensive win (NEED estimated 11/7 ~= 1.57,
realized win-cost 4; PW estimated 1.5, realized fail-cost 2).
The lesion cells are harness-written synthetic history, so
these readings are illustrative only.

Final context tables differ from percontext's in exactly one
line (slot 2, from the S12 divergence):
`CTX2 sig=4,613 pw=3,2,6 who=1,0,4 need=6,6,13 alt=1,0,4`
(percontext: `pw=2,2,4 who=1,0,4 need=5,5,9 alt=2,1,10`).
CTX0/1/3/4 are byte-identical to percontext's.

## What this establishes (and does not)

Establishes: a concrete, learner-estimated cost model for the
task's expected-cost formula, with the non-obvious preregistered
derivation that P(success) cancels at the turn level; an
implementation that selects by (c+2)/(u+2) argmin with exact
integer arithmetic; the finding that expected-cost selection
preserves the optimistic promotion (K4), diverges from
optimistic efficiency on exactly one stage of the battery
(S12, cost-neutrally), and does not reduce total events
(62 = 62). The S8 6-event tax is NOT priced away by turn-level
expected cost: the untried strategy's optimistic cost prior
makes it the cheapest option by construction.

Does not establish: that expected-cost is better calibrated in
general (the battery is not designed to measure calibration);
that a rescue-aware extension (E[turn] + P(fail)*E[rescue],
where P(success) would NOT cancel) behaves the same; that a
pessimistic cost prior (untried = expensive) preserves the
promotion; L3 representational invention; a learner-invented
cost model (the expectation form is researcher-supplied; only
the table values are learner-written).

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; `which python3` / `which python` return nothing
before, during, and after; verified this session). Pinned znc
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev, byte-identical to the tnn-rsi copy per `cmp`)
for the single build. All computation pure Zag; shell only for
znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations, no near-misses. New Zag
scanned for the `while.*!(` negated-conjunction pattern: clean
(the only `!` hits are `!=` comparisons). The new `strat_sel`
keeps the proven COGOPS-PERCONTEXT nesting shape exactly
(while -> if(ist==0) -> if(best!=0) -> comparison on hoisted
locals; hedge block tried==0 -> best!=0 -> c1>0 -> c3>0 ->
exact ==); only the score terms changed. Git writes via
/usr/bin/git absolute path, explicit pathspecs, current branch
(`tnn-native-lab`) only, nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_expectedcost/`:
PREREG.md (frozen, commit b061f1604), NAMECHECK.md (Step 0),
c14_predicted.txt (frozen byte-exact prediction),
c14_base.zag (cmp-identical to c13_base.zag), c14_world.zag
(cmp-identical to c13_world.zag), c14_strat_additive.zag (c13's
with `strat_sel` replaced by the expected-cost rule),
c14_learn.zag (assembled; lines 1..1331 cmp-identical to the
c12 prefix), c14_main.zag (c13_main with comment-only updates;
non-comment lines verified identical), c14_build.sh,
c14_full.zag (assembled; exactly one `fn main`), c14_bin,
c14_compile.txt, c14_run1/2/3.txt (sha256 03c8a42a x3) + .err
(empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Rescue-aware expected cost: E[turn_s] + P(fail_s)*E[rescue],
   where P(success) does NOT cancel and wins re-enter the
   selection. This is the variant that could actually price
   S8's ALT tax (untried P(fail)=1/2 times a rescue estimate).
2. Pessimistic cost prior: untried = expensive (e.g. max
   observed cost); tests whether the promotion is load-bearing
   or incidental. K4-style bar would discriminate.
3. Per-context + pure efficiency (costaware base): still open
   from COGOPS-PERCONTEXT follow-up #1; orthogonal to this
   worker's rule change.
4. Learner-composed proposal orders (follow-up #4): choosing
   among four given forms is still selection, not invention.
