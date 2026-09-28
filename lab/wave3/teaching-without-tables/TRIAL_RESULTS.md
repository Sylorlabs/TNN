# TWT-1 trial results — 2026-09-19

Native Zag, Linux x86-64, `znc 2026.07.0-dev` (pinned lab compiler).
Runner: `trial/run_twt.sh`. Evidence: `trial/EVIDENCE_20260920T001930Z/`
(full pass; the earlier `EVIDENCE_20260920T001919Z` holds the 207/208 run
that triggered the documented PREREG §8 amendment).

## Result: 208/208 checks pass, `TWT_FAILURES,0`, exit 0, byte-identical reruns.

## What the trial proves (PREREG — CONFIRMED, as amended)

1. **The verify gate holds.** VERIFY committed 6 items, every one with ≥2
   agreeing own observations and 0 contradicting. No false proposal was
   committed: all 6 false teacher claims (items 2,4,5,7,10,11 — the teacher
   adversarially claimed "all TRUE") were refused except item 5.
2. **Refusal works with reasons.** 6 refusals, all audited: 5 false claims
   `CONTRADICTED` by the learner's own evidence, 1 true claim (item 9,
   split own evidence) refused — the learner does not rubber-stamp even
   true claims it cannot verify.
3. **Teacher dependence after withdrawal: 0.** Post-withdrawal the VERIFY
   arm answered 5 items correctly, all with `SELF_VERIFIED` provenance —
   `v_dependent=0/5`. The COPY arm (banned-shape negative control) answered
   6 correctly, all `TEACHER_ONLY` — `c_dependent=6/6`. The metric
   discriminates (0 vs 1.0); the falsification criterion F3 is satisfied,
   so the 0 is measured, not decorative.
4. **The honest failure is real.** Item 5: the learner's own evidence was
   wrong (both probes read 1, truth 0), so it verified-and-committed a
   falsehood — with its own provenance. The mechanism's guarantee is "no
   copying," not "no error": taught knowledge becomes the learner's own
   *including this failure mode*, traceable to its own evidence channel.
5. **Withdrawal is structural.** Post-withdrawal `TWT_TEACH` refused
   `TEACHER_GONE` on both arms; the learner answered from committed slots
   only and abstained (recorded, structural — no committed slot, no
   answer) on the other 11 items. No silent fabrication: every
   post-withdrawal answer traces to a committed slot.
6. **Ledger == state.** Replay from genesis reconstructs exact live slots
   on both arms (`replay_v=0`, `replay_c=0`); every refused op left state
   byte-identical (covered by the replay + per-item expectation checks).
7. **Deterministic system, adversarial test.** Zero RNG in the system —
   the verify/commit/refuse/query logic is a pure function of recorded
   state — and zero RNG in the harness (designed curriculum). Two runs,
   byte-identical stdout. The verdict's two halves are separate: the
   *system* is deterministic; the *test* was adversarial (all-TRUE
   teacher, designed noise traps on items 5 and 9 — both fired).

## What it does NOT show (per the prereg)

- 16 items is a mechanism trial, not capability evidence. Scale argument
  is in TEACHING_DESIGN.md §5; the named next scale test is a 1000-item
  curriculum with designed adversarial blocks and two conflicting teachers.
- Own-evidence quality: item 5 shows verification inherits the learner's
  own perceptual noise. Two independent evidence channels (corroboration
  before commit) is the natural hardening.
- Multi-teacher adjudication and teaching of structured knowledge (traces,
  hypotheses — R27's actual learning atom) rather than beliefs.

## Notes for future agents

- Integer-only, playbook-proven subset; compiled and passed on the second
  source revision (first revision had the prereg's item-9 reason wrong,
  fixed via documented amendment — mechanism code untouched).
- `nio_alloc` is not zeroed — `twt_init` zeroes every buffer by hand.
- `twt_replay_check` treats QUERY/TEACH entries as non-mutating and
  refuses as identity; any future op that mutates state must be added to
  the replay's OK-mutation list or the invariant silently weakens.
- Binary `twt_trial_linux` removed after the run; `run_twt.sh` rebuilds it.
- The COPY arm is the banned copy shape run **only** as the labeled
  negative control that validates the dependence metric (PREREG.md §5).
  It is not a candidate mechanism; do not build on it.
