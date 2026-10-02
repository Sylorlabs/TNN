# QUALITY-BUYING — FROZEN PREREGISTRATION

**Date frozen:** 2026-09-22 · **Order:** Micah — "im not trying to trade
quality for speed or compute im looking for the opposite" — as EXPERIMENTS,
not opinions (standing test-both law).
**Branch:** `tnn-native-lab` · **Dir:** `coding/speed-intel/quality-buying/`
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 0. The question, plainly

Speed-intel Arms 1–4 proved: 1x→2x buys coding 6/18→18/18 and epistemic
29/94→59/94; 4x/8x buy nothing (plateau confirmed on a fresh disjoint
battery); "2x at free speed mechanisms is the winner" (Micah's ruling,
2026-09-22). "More iterations" is DEAD — this experiment does NOT test
16x or any larger budget.

The open question is the opposite direction: can QUALITATIVELY DEEPER
deliberation — a different kind of compute, not more of the same — buy
quality PAST the knee (past 18/18 coding, past 59/94 epistemic)?

## 1. Design principle

All arms run at the KNEE budget (coding: 4 iterations; epistemic: the 2x
full pipeline). The ONLY thing that varies between arms is deliberation
structure. Any quality difference is therefore attributable to HOW the
learner deliberates, never to how LONG it deliberates. Budget is held
constant by construction; the dead budget question cannot confound this
experiment.

## 2. Batteries (frozen, reused verbatim — no new cherry-picked items)

- **Coding:** `coding/reflection/speed_intel/work_a1/battery_si.json`
  (20 items: 18 fixable + X3 ungenable + X4 unrepairable). Knee ceiling:
  **18/18** with 2/2 honest halts (X3→halt-genfail, X4→halt-no-patch).
- **Epistemic:** `coding/reflection/speed_intel/work_a1r/epi/`
  (`b12_false.txt`, `b12_true.txt`, `c70.txt`, intended verdicts in
  `battery_a1r_items.json`; 94 items, disjoint from the original 94).
  Knee: **59/94** at the 2x full pipeline (12/12 false, 12/12 true,
  35/70 weird-English).

The QB harness reuses these files byte-identical. Scoring reuses the
frozen intended-verdict mapping (falsehood→WITHHOLD, true→ENDORSE,
weird-nonfactual→WITHHOLD).

## 3. Arms

### D0 — knee baseline (calibration cell)

- Coding: `learner_si4.zag` + `driver_si4.py --budget 4 --mech combo`
  (the verified Arm 4 winner: 2x + 3a + 3b + 3c), rebuilt from the
  committed sources with the pinned toolchain.
- Epistemic: the 2x full-pipeline deliberation (same predicate set and
  staged decision as `delib_si.zag` at budget 2), re-implemented in the QB
  binary.

Expected (calibration gate): coding 18/18, 2/2 halts, 46 iters, 28 znc,
45 hyp-evals; epistemic 59/94 at 9.000 preds/item, canonical digest
identical to the A1R 2x digest (`57cefaa42100f695…`). **If D0 does not
reproduce these numbers, the QB harness is wrong — stop, do not interpret
D1–D5.**

### D1 — conflict-driven deliberation as the default path

Motivation: the new-mechanisms verdict (2026-09-22) — depth without
contradiction is wasted; depth WITH contradiction resolves 156/156 at
1.00× quiet cost.

- Epistemic: classify each item quiet/conflicted from the evidence ledger
  (conflicted = ≥1 pro marker AND ≥1 con marker, where pro = kf/ab/fired
  speech-act matchers, con = kt/CM2 assertion-form). Quiet → staged
  pipeline verdict (baseline cost). Conflicted → deep path: deliberate
  explicitly over WHICH markers fired and their specificity, resolve the
  conflict with recorded reasons, verdict = the deliberated resolution.
- Coding: in `diagnose`, conflict = top-2 class scores within the frozen
  margin (contested diagnosis). Uncontested → argmax as today. Contested →
  deep path: marshal the evidence for each competing class, deliberate a
  winner, record the deciding evidence.

### D2 — multi-round critique (K=3 critic rounds)

- Epistemic: after the staged verdict, run 3 critic rounds. Each round
  MUST produce a specific, ledger-grounded challenge (cite the evidence
  bits it disputes and why they overturn the verdict) or pass. A valid
  challenge per the frozen challenge-validity rule flips the verdict and
  rounds continue against the new verdict. Verdict = survivor after 3
  rounds. Challenge-validity rule (frozen): a challenge is valid iff it
  names ≥1 fired evidence bit whose removal/reinterpretation changes the
  staged pipeline's verdict under the frozen decision rule — no free-form
  second-guessing.
- Coding: after `diagnose` selects class+strategy and the learner drafts
  a revision, run 3 critic rounds against the DRAFT before compiling.
  Each round applies the learner's own cross-checks (brace balance,
  defined-name, arity-vs-definition, trigger-presence for the diagnosed
  class). A round that finds a defect forces a re-draft (bounded: max 2
  re-drafts per iteration, then proceed to compile regardless).

### D3 — hypothesis competition on every item (not just contested ones)

- Epistemic: maintain ENDORSE and WITHHOLD as competing hypotheses on
  EVERY item. Each hypothesis is scored against the full ledger by a
  separately-written scoring path (not a copy of the staged pipeline).
  Winner takes the verdict; exact ties → WITHHOLD (the safe default,
  matching the pipeline's bias).
- Coding: diagnose's top-3 classes each produce a candidate patch; a
  competition round scores each candidate against the evidence envelope
  (trigger presence, strategy fit, cross-check cleanliness); the winner
  is applied. Per iteration, within the knee budget.

### D4 — one-brain sub-deliberations sharing one ledger

- Epistemic: structure deliberation as explicit phases over ONE shared
  evidence ledger: (1) GATHER — all predicates evaluated, ledger filled;
  (2) CHALLENGE — a challenger sub-deliberation argues the opposite of
  the staged verdict FROM the shared ledger, writing its arguments back
  to the ledger; (3) SYNTHESIZE — a synthesis step resolves, with the
  challenger's arguments visible. No sub-deliberation sees a private
  copy; one brain, one ledger.
- Coding: structure each repair iteration as sub-deliberation phases
  sharing one ledger: HYPOTHESIZE (class scoring) → CRITIQUE (attack the
  leading hypothesis from the shared evidence) → COUNTER-HYPOTHESIZE
  (best surviving alternative) → COMMIT. A finding by one phase (e.g.
  "NAME trigger absent") is written to the shared ledger and visible to
  the others.

### D5 — combined

D1 + D2 + D3 + D4 all wired in simultaneously. Run once (3 reruns).
Interpreted only if D0 quality is preserved (no regression); otherwise
reported as a regression, not a quality result.

## 4. What the deeper arms may NOT do

- No new predicates, no new knowledge triggers, no new KB entries. The
  predicate/knowledge set is IDENTICAL to the knee config in every arm.
  This experiment tests whether deliberation STRUCTURE alone buys
  past-knee quality. (New knowledge is a different experiment.)
- No budget change: coding stays at 4 iterations, epistemic at the 2x
  predicate set per item. Deeper forms add deliberation STEPS, never
  budget.
- No weakening of gates or halt honesty (see §6).

## 5. Metrics (per arm, per domain)

- Coding: Q_c (/18), honest halts (/2), iterations, znc invocations,
  hypothesis-evaluations, wall-clock, CPU time.
- Epistemic: Q_e (/94), per-family tallies, pred-evals/item, wall-clock,
  CPU time.
- Determinism digests drop wall/CPU timings (canonical form, per
  INTERFACE.md).
- Quality-per-cost curve: for each arm, ΔQ vs D0 and Δcost vs D0, plus
  the marginal price of quality: extra cost per +1 correct item.

## 6. Kill bars and verdict rules (frozen)

- **QB-DET:** 3 reruns per cell; canonical logs byte-identical within
  every cell; zero RNG in any decision path. A non-deterministic cell
  is not interpreted.
- **QB-CAL:** D0 must reproduce the knee numbers (§3). Failure = harness
  defect; stop.
- **QB-NOREG:** Q_c must stay 18/18 AND X3/X4 honest halts preserved in
  every arm. Any arm that converts a correct halt into a fabricated pass,
  or drops Q_c below 18/18, FAILS outright — it is not scored for
  quality, regardless of epistemic gains.
- **QB-GATE:** 6/6 gate battery per coding arm (REFUSE G1/G2/G4/G5 +
  ALLOW ×2), as in Arms 1–4.
- **QB-QUALITY:** an arm SCORES iff Q_e > 59/94 with QB-NOREG and
  QB-GATE satisfied.
- **QB-WORTH:** a scoring arm is WORTH IT iff its marginal price per +1
  epistemic item is < 10× the knee's per-item cost (10 × 9.000 =
  90 pred-evals per +1 item). A scoring arm at ≥90 pred-evals per +1 item
  is reported honestly as NOT WORTH IT.
- **QB-CEILING:** if no arm scores, the verdict is CEILING-CONFIRMED:
  "the knee is the ceiling of deliberation; further quality must come
  from new mechanisms or new knowledge, not more compute."

## 7. Honest limits (declared before results)

1. The coding battery saturates at 18/18 — the maximum achievable. The
   coding cells therefore test non-regression + cost, not quality gains.
   The quality-buying verdict rests on the epistemic battery.
2. The epistemic misses are substantially KNOWLEDGE gaps, not
   deliberation gaps: 35/70 weird-English items fire no nonfactual
   predicate by construction, so their ledgers are indistinguishable from
   true controls to any deterministic function of the ledger. §4 forbids
   new predicates, so the deeper arms test whether deliberation structure
   alone recovers any miss. The realistic best case is small (the rare
   conflicted item, e.g. the A1R W152 class).
3. Arm 1's 8x leg already showed independent re-derivation flips 0/188
   items across both batteries. D1–D4 are DIFFERENT deeper forms (not
   re-derivation), so this test is not redundant — but the prior is
   ceiling, and CEILING-CONFIRMED is a finding, not a failure.
4. Single-threaded substrate: "sub-deliberations" in D4 measure saved /
   added evaluations, not wall-clock parallelism.
5. The SI coding battery is 20 synthetic items; real-world repair is
   unmeasured (carried from the SI honest limits).

## 8. Deliverables

1. This prereg (committed BEFORE any result is generated).
2. `delib_qb.zag` (epistemic: modes d0–d5) + `learner_qb.zag` +
   `driver_qb.py` (coding: modes d0–d5) — originals untouched; learner
   changes purely additive (as in Arm 4); driver changes plumbing-only
   (grep-verified per INTERFACE.md).
3. Quality-per-cost curve table (all arms × both domains).
4. All canonical logs + determinism digests (3 reruns per cell).
5. Commit to `sylorlabs/TNN`, branch `tnn-native-lab`, under
   `coding/speed-intel/quality-buying/` (lab-relative paths); verify via
   GitHub API; report head SHA.
