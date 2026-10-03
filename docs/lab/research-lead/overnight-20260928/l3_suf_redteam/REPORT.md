# L3-SUF-1 RED-TEAM REPORT (SUF-K10)

**Worker:** L3-SUF-1-REDTEAM (distinct instance from designer, builder,
adversary; separate subagent session)
**Date:** 2026-10-03
**Prereg:** frozen at `9b93dba01` BEFORE any analysis (this lane)
**Status:** REDTEAM-SURVIVES (bounded). One confirmed mechanism defect
(R-SUF-1); adjudicated non-fatal per frozen RT-K7.

## Verdict

**SUF-K10 = REDTEAM-SURVIVES.** The red team tried to kill the L3-SUF-1
claim through all six audit classes and a computational dissection of
R-SUF-1. No audit breaks a frozen SUF-K1..K9 / SUF-KC0 bar. R-SUF-1 is a
genuine defect in researcher-authored aggregation machinery, but it is
safe-direction, bar-neutral, and provably redundant for every correct
marking on the tested worlds. It bounds the claim; it does not kill it.

RT-K1 green (with noted exception) | RT-K2 green | RT-K3 green |
RT-K4 green | RT-K5 green | RT-K6 green | RT-K7 BOUNDED | RT-K8 green.

## What was done (pure Zag, safebin; Step 0 verified)

1. Re-verified frozen learner sources sha256-identical to the
   adversary's build-time record (`l3_suf_adversary/build/frozen_src.sha256`).
2. `rt_surv.zag`: linked FROZEN `prelude.zag` + `learner1.zag` read-only;
   called the FROZEN `l_surviving` directly on 8 synthetic consequence-log
   patterns (U full/partial probe, decoy-with-ACCEPTs, stakes-fabrej-only,
   observed, knowledge-REJECT, contradictory-ACCEPTs), plus a gated
   variant (adversary's fix direction). 3/3 byte-identical
   (`7fb5d85c267b18d4134a43cb746f4a286cf9ee6e0a1483fa1e2b94131719a65d`).
3. `rt_trace.zag` / `rt_trace07.zag`: linked FROZEN learner + FROZEN
   builder DEV world read-only; dumped the full W0 T0 white-box trace
   (565 lines) for A-TRACE / A-SEARCH / A-TRIGGER.
4. A-LIT grep audit of frozen learner sources; A-INFO channel audit
   (`w_test` source, learner references).
5. Read the sealed KEY.md under seal for adjudication. It is NOT copied
   into this lane and NOT included in this report; referenced only.

## R-SUF-1: computational dissection (the core finding)

`l_surviving` (frozen `learner1.zag`) computes the per-element mask.
Two `return 3` sites exist: rule (i) line 114 (both TEST values REJECTed,
neither ACCEPTed, no observations: the withholding inference) and rule
(ii) line 118 (`if(fabrej==1){return 3;}`: stakes fabrication-REJECT
with no observations, WITHOUT checking TEST-ACCEPTs).

Results on the frozen function (frozen / without-fabrej-entry / gated):

| pattern | frozen | no-fabrej | gated | correct |
|---|---|---|---|---|
| P1 U, full probe (both TEST REJECT) | 3 | 3 | 3 | 3 |
| P2 U, partial probe (one TEST REJECT) | 3 | 2 | 3 | 3 |
| P3 decoy (TEST-ACCEPT + fabrej) | 3 | 1 | 1 | 1 |
| P4 stakes-fabrej only | 3 | 3 | 3 | 3 |
| P5 observed + fabrej | 2 | 2 | 2 | 2 |
| P6 TEST-ACCEPT only | 1 | 1 | 1 | 1 |
| P7 knowledge-REJECT | 2 | 2 | 2 | 2 |
| P8 contradictory ACCEPTs + fabrej | 3 | 0 | 0 | 0 |

Established facts:

- **F1 (defect confirmed):** P3 reproduces R-SUF-1 with the frozen code:
  a TEST-ACCEPTed element is marked UNRESOLVED(3) when a stakes
  fabrication-REJECT exists, discarding positive evidence. The
  without-fabrej computation gives the correct 1.
- **F2 (defect reproduced naturally):** on the non-sealed DEV W0 trace,
  element (ctx100, pair 0-8) -- a determined, probeable pair with a
  staged TEST-ACCEPT(0) -- was marked 3 at S332 and ABSTAINed in
  round-2 stakes (S558) instead of correctly predicted. R-SUF-1 is not
  a decoy-specific artifact; it is systematic: any stakes-queried
  element with (no observations + TEST-ACCEPTs + fabrication-REJECT)
  is over-marked, because unabsorbed probe evidence lives in the log
  but not in the form.
- **F3 (rule (ii) is not pure harm):** P2 shows rule (ii) is load-bearing
  for the partial-probe-coverage U case (without it, mask 2: wrongly
  RESOLVED). It is a hedge against incomplete probing. The red team's
  initial "strictly dominated" hypothesis is REFUTED.
- **F4 (redundant on the sealed battery):** probe-budget analysis shows
  full coverage on W0 (DEV: 101/150 TESTs used; sealed: at most 144/150;
  all U pairs got both TEST values on DEV). With full coverage, U marks
  come from rule (i) (P1) and X-CTX-class marks from the bottom default
  (P4). On the sealed battery, rule (ii)'s SOLE observable effect is
  the decoy over-marking. It is never load-bearing for a correct
  marking there.
- **F5 (second evidence-discarding case):** P8: rule (ii) masks a genuine
  contradiction (both values TEST-ACCEPTed) to 3 instead of
  FALSIFIED-ALL(0). Behaviorally equivalent (both ABSTAIN via kind2
  predict), but the provenance is misrepresented.
- **F6 (fix direction verified):** gating rule (ii) on absence of
  ACCEPTs (the adversary's proposed fix, mirroring rule (i)) yields the
  correct mask on ALL 8 patterns, preserving the P2 hedge and fixing
  P3/P8. The fix changes no sealed verdict (all affected marks move
  toward correct predictions or stay ABSTAIN).

## R-SUF-1 adjudication (frozen RT-K7): BOUNDED, not fatal

Fatality required (a) confident-wrong, (b) a broken frozen bar,
(c) non-experience-derived marks, or (d) researcher-triggered
UNRESOLVED on passing-bar content. None holds:

- (a) Every rule-(ii) effect moves toward UNRESOLVED/ABSTAIN, never
  toward a predicted value. The cost is foregone correct predictions
  (decoys; DEV (100,0-8)), never fabrication. Safe direction.
- (b) No frozen bar depends on rule (ii). T0(iii) passes because
  ABSTAIN is protocol-neutral. Gating/removing it changes no verdict
  (F6).
- (c) Marks are computed from the consequence log; the defect is
  mis-aggregation of experience, not non-derivation. Record content is
  not enumerable from source without the log.
- (d) The passing U marks on the sealed battery come from rule (i)
  (withholding inference on full probe coverage) and the bottom
  default, not from rule (ii) (F4). The decoy marks are
  researcher-rule-driven but are not passing-bar content.

The defect BOUNDS the claim: the implemented record's UNRESOLVED state
conflates "no evidence" with "my fabrication was REJECTed" and is not
fully evidence-faithful. The researcher's aggregation rule contains a
pre-written "mark unresolved when..." conditional (see A-LIT) whose
miscalibration the next design must remove (fix direction: F6).

## Audit results

- **A-LIT (RT-K1): green with noted exception.** No sealed literals, no
  abstention policy beyond the disclosed generic evaluator (MAY 3f),
  no trigger counter/threshold. EXCEPTION: `l_surviving` line 118 is a
  researcher-authored "mark unresolved when (stakes fabrej and no
  observations)" conditional -- the source's own audit note ("NO
  marking rule") is inaccurate. Adjudicated per frozen RT-K1: not a bar
  break, because it (i) encodes no sealed content, (ii) is provably
  redundant for every correct marking on the tested worlds (F4) and
  therefore cannot have smuggled any passing verdict, and (iii) is not
  the trigger. Recorded as a defect finding (R-SUF-1).
- **A-TRACE (RT-K2): green.** DEV W0 trace replays the invention:
  COMMIT kind1 (S124) -> stakes REJECTs incl. first at S127
  (`SANS 100000001 1 0 0`) -> REVISE (S139) -> ESCALATE (S140) ->
  FORM_TRY 1..3 with TRY_FAIL (S141/S265/S267) -> FORM_TRY 4 ->
  MARKs from S270, first mask-3 at S310 (same element as the first
  REJECT) -> TRY_OK (S544) -> COMMIT kind2 (S545). No MARK before the
  first committed REJECT. Parent pointers intact throughout.
- **A-SEARCH (RT-K3): green.** Three non-marking compositions genuinely
  tried and rejected on W0 (op_fail=2; TRY_FAIL 1/2/3 in trace) before
  the lift's TRY_OK. Differential behavior confirmed: the sealed F-G
  arm adopts TRY2 (guard re-expansion absorbing the extras'
  TEST-ACCEPTs; commit_kind=1) with zero UNRESOLVED marks -- the same
  frozen enumeration avoids the lift where re-expansion suffices. Not
  theater. TRY2/TRY3 fail on W0 precisely because U has no
  TEST-ACCEPTs to absorb (verified: all U probe TESTs REJECT).
- **A-TRIGGER (RT-K4): green.** Path to first MARK: any single stakes
  REJECT (structural, not a threshold) -> revise -> escalate ->
  TRY1..3 fail -> TRY4 -> fill_record -> MARK. No counter, no
  failure-rate threshold, no world-property branch on the path. The
  kb-instantiate LIFT+fill path only re-marks from kb; the kb is wiped
  on the invention arm.
- **A-INFO (RT-K5): green.** `w_test` returns only ACCEPT(1)/REJECT(0);
  REJECT carries no expected value. Frozen learner sources contain zero
  references to `w_truth`, `w_undet`, or `w_stakes_meta`.
- **A-ORDER (RT-K6): green (static proof).** `l_surviving` accumulates
  boolean flags by commutative OR over log entries and returns a pure
  function of the flags: permutation-invariant. `l_replay_consistent`
  is a universal quantification: order-independent. Escalation
  outcomes are functions of these booleans. Form construction is set
  semantics (duplicates skipped). T0(i) is causally guaranteed
  (fill_record runs only after revise after stakes REJECTs). Caveat:
  probe-budget exhaustion order could affect staged coverage, but
  budgets do not exhaust on the tested worlds (101/150 DEV).

## Notes for the parent

- The R-SUF-1 fix direction (gate rule (ii) on absence of ACCEPTs,
  mirroring rule (i)) is verified correct on all 8 evidence patterns
  and verdict-neutral on the sealed battery. It is NOT implemented
  (code frozen); recorded for the next design.
- The builder's CODEFREEZE documents rule (ii) as intended ("audit
  mark, not silent"). The red team finds the intent miscalibrated: an
  audit mark that governs prediction (mask 3 -> ABSTAIN) and discards
  positive evidence is not "not silent" -- it is behavior-changing.
  The "audit" rationale does not survive the P3/P8 cases.
- SUF-K12 computation is the parent's: this report covers the red-team
  audits (A-LIT/A-TRACE/A-SEARCH/A-TRIGGER/A-INFO/A-ORDER). SUF-K1
  (A-LIT) carries the noted rule-(ii) exception, adjudicated non-fatal
  per the frozen RT-K1 standard; SUF-K4 (A-TRACE) and SUF-KC0A
  (A-TRIGGER) are clean.
- Nothing in this report changes the sealed PASS/FAIL verdicts. The
  builder receives nothing from this lane (per sequencing, the builder
  got only per-arm PASS/FAIL, counts, digests).

## Artifacts (this lane)

- `PREREG.md` (frozen `9b93dba01`), `NAMECHECK.md`
- `rt_surv.zag` -- frozen-`l_surviving` probe + gated variant
  (3/3 byte-identical;
  `7fb5d85c267b18d4134a43cb746f4a286cf9ee6e0a1483fa1e2b94131719a65d`)
- `rt_trace.zag`, `rt_trace07.zag` -- frozen trace-dump drivers
  (DEV worlds only; no sealed content)
- `REPORT.md` (this file)
