# RESULT_TRANSFER.md: TRANSFER / REUSE sealed evaluation results

Wave: wave-20261001-1421pdt, lane B. Prereg: PREREG_TRANSFER.md (frozen
before implementation; no bar altered after results).

## What was done

1. Located arena records: the 15-capability baseline arena design
   (transfer = C6, score S = 1 - transfer_examples / fresh_examples) and
   the sealed 16-capability competitive arena (transfer = C12).
2. Drafted a frozen prereg defining transfer as "a structure learned in
   world A improves later cognition in world B", with materially different
   worlds (different surface: digits vs letter-code; different law family:
   arithmetic vs geometric), an exact sample-efficiency scoring rule, and
   frozen numeric kill bars K1..K8.
3. Implemented transfer_eval.zag (pure Zag, pinned znc, build exit 0) and
   ran the sealed evaluation: LEARN phase on A, TRANSFER phase on B, plus
   an ABLATED control (A-structure wiped) and a STORAGE control (verbatim
   lookup, pure memorization).

## Measured numbers (3/3 byte-identical runs, sha256
4344e9ddd4d98e33d9f830df6a253a4b1872a73795bc6f68db6cba6edbb9e3e0)

- A phase: criterion met in 5 examples (A_met=1). Learned structure S_A:
  checklist order [DIFF, RATIO, COPY, MEAN] (DIFF confirmed in A; COPY and
  MEAN tried and failed in A; RATIO untried). This ordering was constructed
  from A evidence during the run, not preset.
- T (transfer): B_examples = 4 (B_met=1).
- F (fresh): B_examples = 6 (B_met=1).
- X (ablated): B_examples = 6 (B_met=1).
- M (storage): B_examples = 24 (cap), lookup miss 24/24.
- Transfer score S = 1 - 4/6 = 0.3333 (reported x10000 = 3333).

## Per-bar verdicts

- K1 TRANSFER GAIN (S >= 0.25): PASS (0.3333).
- K2 ABLATION ATTRIBUTION (|X_B - F_B| / F_B <= 0.10 and X_B > T_B): PASS
  (0.00, 6 > 4). The gain vanishes when S_A is wiped, so it is attributable
  to the learned structure.
- K3 ANTI-MEMORIZATION (M_B >= F_B): PASS (24 >= 6; storage gain = 0).
- K4 DETERMINISM (3/3 byte-identical): PASS (cmp clean on run1/2/3.txt).
- K5 MATERIAL DIFFERENCE: PASS. Surface classes verified disjoint
  (digit/- tokens vs letter tokens, zero shared tokens); A-law rejected on
  all 36 B sequences; B-law rejected on all 36 A sequences.
- K6 CRITERION VALIDITY: PASS (A met in 5 <= 24; F met in 6 <= 24).
- K7 PURE ZAG: PASS (safebin toolchain guard Step 0; `which python3` empty;
  zero .py files in lane; shell used only for compile/run/cmp/sha256sum).
- K8 NO-CONFOUND: PASS by construction (identical B briefing, B training
  order, and B held-out set across T/F/X; only S_A differs entering B).

## Verdict: CANDIDATE

Transfer score S = 0.3333 on the frozen protocol, all kill bars PASS.
This is a CANDIDATE score for the arena composition, not an addition to
any contestant total.

## Explicit non-claims and limitations (do not overread)

- This does NOT move the canonical 0.573. Only a clean refreeze reproducing
  composition without contamination can move it. The actual contestant
  remains 0.676 (v4, 7/7 kill bars) per parent-provided prior state.
- The learner here is a minimal simulated learner (evaluator-only), not the
  frozen TNN-2 binary (no runnable TNN-2 binary was available to this lane).
  Nothing here establishes that TNN-2 itself transfers.
- The "learning" demonstrated is checklist reordering from experience
  (a weak structural update), not representational invention; no L3 claim
  is made or implied.
- The absolute effect size is conditional on the researcher-set default
  checklist order (simplest-first). S measures the value of A's experience
  relative to that default prior. The ablation (K2) shows the gain is
  attributable to S_A given the default, which is the honest scope.
- The world pair was fixed in the prereg; the measured numbers matched the
  pre-registered design walkthrough exactly, and no tuning followed.

## Architecture accounting

- TNN source touched: none. Cognition source lines added: transfer_eval.zag
  (about 380 lines), all inside this lane directory, evaluator-only.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New routers: 0. New task-specific handlers: 0.
- Learner-state structures created: the checklist order + current hypothesis
  in the simulated learner state (S_A). The B surface decoder is briefing
  interface machinery, identical across conditions, never counted as learned.

## Files left behind (all uncommitted, in this lane directory)

- NAMECHECK.md (toolchain guard Step 0, steps log)
- PREREG_TRANSFER.md (frozen prereg)
- RESULT_TRANSFER.md (this file)
- transfer_eval.zag (sealed evaluation source)
- transfer_eval (compiled binary)
- run1.txt, run2.txt, run3.txt (transcripts; byte-identical)

Recommended follow-up (for the parent, not decided here): the refreeze
protocol run of this exact frozen protocol against the actual frozen TNN-2
contestant binary, which alone can convert the CANDIDATE into an admissible
arena transfer score.
