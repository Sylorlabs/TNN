# PREREG: L3-SUF-1 Red Team (SUF-K10)

Status: PREREG-FROZEN 2026-10-03, before any red-team analysis exists.
This document is never edited after freezing. Any change requires a new
prereg. Commit-order self-check: the freeze commit contains ONLY PREREG.md
and NAMECHECK.md. No analysis, no .zag, no binary, no log exists under
l3_suf_redteam/ at freeze time.

Worker: L3-SUF-1-REDTEAM (subagent, 2026-10-03, distinct instance from
designer, builder, and adversary per parent prereg section 12). Non-ledger
task (claim minting paused).

Parent prereg: l3_suf_intermediate/PREREG.md (frozen at 6c70c3198),
sections 6 (kill bars), 8 (adversary instructions), 12 (sequencing).
Adversary: l3_suf_adversary/ (REPORT.md, sealed KEY.md held under seal).

## 1. Objective

Independently attack the L3-SUF-1 claim ("the learner invented the
resolution record representational level") per the audit classes below,
with emphasis on adjudicating the adversary's R-SUF-1 finding
(over-marking defect in `l_surviving` rule (ii): W0 decoys marked
UNRESOLVED(3) despite staged TEST-ACCEPTs, discarding positive evidence).

Deliver a verdict: REDTEAM-SURVIVES or KILL (SUF-K10). The verdict names
the exact frozen bars that governed it.

## 2. Frozen red-team bars (any single FAIL kills the L3 claim)

- RT-K1 (A-LIT): learner source contains no sealed-world literals and no
  researcher-authored element that determines record marking CONTENT by
  encoding the solution. A marking conditional is a BAR BREAK iff it
  (i) encodes sealed content, or (ii) is load-bearing for a passing
  SUF-K bar while contradicting the disclosed generic principle, or
  (iii) constitutes the trigger. A conditional that is provably
  redundant for all correct markings, or safe-direction-only
  (ABSTAIN, never confident-wrong), is recorded as a defect finding,
  not a bar break.
- RT-K2 (A-TRACE): the white-box trace replays the invention: MARK,
  PROBE, FORM_TRY, REVISE, COMMIT, DEFER, ABSTAIN events with monotonic
  SEQ and parent pointers; the first UNRESOLVED-mark is strictly after
  the first committed-prediction REJECT in trace order (T0(i)).
- RT-K3 (A-SEARCH): on the invention world, >= 2 non-marking operator
  compositions show FORM_TRY with FAIL verdicts before the marking
  composition's adoption (T0(ii)); and the same frozen escalation shows
  differential behavior (a non-marking composition adopted) on at least
  one other world (F-G TRY2). Otherwise the search is theater (F-MENU).
- RT-K4 (A-TRIGGER): no counter, no failure-rate threshold, no
  world-property branch exists on any source path leading to the first
  UNRESOLVED-mark (F-TRIGGER).
- RT-K5 (A-INFO): no expected value reaches the learner process
  (protocol log + channel source inspection). Any leak is VOID-class.
- RT-K6 (A-ORDER): the verdict-determining computations (surviving-set
  masks, replay consistency, escalation outcome) are order-independent
  functions of the consequence-log multiset; the T0 verdict reproduces
  under training-order permutation (static proof, plus a computational
  spot check on a fresh non-sealed world if feasible without breaking
  the seal).
- RT-K7 (R-SUF-1 adjudication): the over-marking defect is FATAL
  (kills SUF-K10) iff any of: (a) it produces a confident-wrong
  prediction; (b) it breaks a frozen SUF-K1..K9 / SUF-KC0 bar;
  (c) it shows record marks are not experience-derived (enumerable
  from source without the consequence log); (d) the UNRESOLVED state
  is researcher-triggered rather than evidence-triggered on a passing
  bar. Otherwise it is BOUNDED: a confirmed safe-direction defect
  recorded as a limitation on the claim, with fix direction.
- RT-K8 (verdict integrity): SUF-K10 = REDTEAM-SURVIVES requires
  RT-K1..RT-K7 ALL green (with RT-K7 allowed BOUNDED). Any FATAL is
  KILL with reclassification by evidence. No partial credit.

## 3. Attack plan (frozen)

1. A-LIT source audit: grep the frozen learner sources for resolution
   schema, marking rules, abstention policy, trigger conditions,
   sealed literals. Adversarial focus: `l_surviving` rules (i)/(ii) --
   is rule (ii) a prohibited marking rule? Load-bearing test via
   direct computational probing of the FROZEN `l_surviving` on
   synthetic consequence logs (U-full-probe, U-partial-probe,
   decoy-with-ACCEPTs, X-CTX-like, observed).
2. A-TRACE/A-SEARCH/A-TRIGGER: link the FROZEN learner + FROZEN builder
   DEV world (non-sealed) read-only; dump the full W0 T0 trace;
   verify FORM_TRY 1..4 sequence with TRY_FAIL/TRY_OK, MARK SEQ
   ordering vs first committed REJECT, decoy MARK masks, and F-G
   differential (TRY2 adopted, no lift).
3. A-INFO: verify the learner-visible channel carries only
   ACCEPT/REJECT (no expected values); verify learner sources never
   reference w_truth / w_undet / w_stakes_meta.
4. A-ORDER: static order-independence proof over the
   verdict-determining computations; computational spot check if
   feasible without touching sealed material.
5. R-SUF-1: computational characterization of rule (ii) --
   mechanism, redundancy, fix-direction behavior -- then adjudicate
   per RT-K7.

## 4. Toolchain and boundaries (frozen)

- Pure Zag for all computational verification; safebin mandatory
  (`export PATH="$HOME/safebin"`); Step 0 records `which python3`
  returning nothing. Any forbidden-interpreter invocation is
  PROCESS-FAIL (results stay exploratory).
- Do NOT modify the builder's frozen code or the adversary's sealed
  worlds. Frozen sources are linked read-only (sha256 re-verified).
- KEY.md stays sealed: it is read for adjudication, never copied
  into this lane, never included in REPORT.md; referenced only.
- Commits local, never push, explicit pathspecs.

## 5. Known boundaries (honest)

- The red-team worker is a follow-up worker under procedural
  firewalls, not an external party. Documented as a limitation.
- The sealed battery emits summaries only; deep trace verification
  uses the builder's non-sealed DEV worlds, which are structurally
  similar but not the sealed instances.
- N = 10 entities per world: mechanism demonstration, not a
  generality proof. FW1-FW9-style overclaiming is disallowed.
- This prereg asserts no verdict in advance.
