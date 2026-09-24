# KBCONTROL PREREG — KB-control three-arm cost measurement (consciousness bill)

**Frozen:** 2026-09-24T05:53:27Z (UTC). **Status:** FROZEN — never edit after
runs start; amendments go in a new file.
**Question:** How much of MA1's deliberate-memory-agency outcome comes from
the deliberate STRUCTURE (op set + audit + refusal gates) vs the TRAINED
judgment (calibrated promotion/protection/eviction decisions)?

## Arms (all pure Zag, zero RNG, byte-identical reruns ≥3, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`)

- **A1 DELIBERATE-TRAINED** = MA1 op set (`MEM_ADD/KILL/PIN/UNPIN/PROMOTE/
  DEMOTE/ROLLBACK`, every mutation+refusal audited, stage gates, CORE/PINNED
  refusals from `wave2/memoryagency/trial/memory_core.zag`) + trained
  judgment policy (§Judgment). Two measurements: (a) rerun of the MA1 trial
  driver `trial.zag` (58/58 checks, 28 audit entries); (b) A1 policy on the
  shared curriculum.
- **A2 SILENT/AUTOPILOT** = the R27 harness-style auto arm (`psm.zag`
  mode=0: timer scan every 10 episodes, promote on raw exposure
  (ver+unv)≥6, last-wins slow overwrite, lowest-confidence eviction, NO
  audit). Rerun of the existing `evidence/scratch/trial_auto.zag` verbatim.
  This is the "mutation happens to the system" arm.
- **A3 DELIBERATE-UNTRAINED** = the SAME MA1 op set + audit machinery as A1,
  but an UNTRAINED judgment policy (§Judgment): naive, uncalibrated,
  deterministic. Real mechanism, no learning.

## Shared curriculum / probe set

The R27 frozen episode sequences, copied verbatim (C1=848, C2=640, C3=3392
episodes; total 4880/arm): phases A true skills verified → B1 impostor burst
(same ids, wrong values, UNVERIFIED) → B2 fabricated decoys (UNVERIFIED) →
C late true skills verified → D return to true verified. Ground truth
(id→true value) is world-side; the evaluator is blind.

Tier mapping (declared, not hidden): psm slow tier ↔ MA live store — each
arm's long-term memory. Probe (identical inputs for all arms): for each
true id t (nt=20/20/80) × 4 contexts: find t in long-term memory.
correct = true value recalled; wrong = other value recalled; abstain = t
absent. spurious = live long-term slots whose (id,value) is not a true
skill's true form. A2 reports its native `spurious_slow`; A1/A3 report the
harmonized spurious over the live store (same definition).

Two probe points (same for A1/A3; A2's existing binary probes end-only):
- **end** (PRIMARY, frozen): after the full curriculum — comparable across
  all three arms.
- **mid** (DIAGNOSTIC, frozen): right after the last adversarial block,
  before late-true phase (C1:e=608, C2:e=320, C3:e=2432) — measures judgment
  under adversarial pressure before phase D can heal.

Capacities: C1/C2 = 32 slots, C3 = 128 slots (match R27 ns).

## Judgment policies (frozen)

**A1 trained** (calibrated; the KB-control analog of MA1's deliberate
kill-low-value / pin-high-value / refuse-illegal):
- verified repeat of known true value: ver_count++, ctxmask|=ctx; PROMOTE
  iff ver_count≥6 AND ≥2 distinct contexts AND tier=SHORT.
- UNVERIFIED conflict with known id (impostor): suppress entirely
  (no overwrite, no ver_count change). Count `suppressed_imp`.
- unknown id + UNVERIFIED: never install. Count `suppressed_fab`.
- unknown id + verified: ADD; if full, victim = live unpinned USER slot
  with min ver_count (tie: oldest step, then lowest slot), audited
  KILL then ADD; if none killable, audited REFUSED_FULL.
- verified conflict vs weak stored entry (ver_count<6): audited KILL+ADD
  replacement. Verified conflict vs trusted entry (ver_count≥6):
  suppress observation, count `anomaly_suppressed`.
- PIN when ver_count≥12 (deliberate protection of strongly-verified
  knowledge; mirrors MA1's pin-high-value).
- Stage set to KILL once at start (audited SETSTAGE).

**A3 untrained** (naive; same ops, same audit):
- PROMOTE on FIRST verification (ver_count≥1 → promote immediately).
- KILL ON FIRST CONFLICT: any conflicting observation → ma_kill(stored) +
  ma_add(newcomer), regardless of verification standing. If kill refused
  (pinned), move on; count `conflict_kill_refused`.
- unknown id: ADD regardless of verification (install-first-ask-later);
  if full, victim = live unpinned USER slot with LOWEST RAW VALUE (fixed
  naive rule, ignores verification standing); tie: lowest slot.
- PIN the first 4 slots filled (fixed "protect early knowledge" rule).

## Metrics per arm

Wall-clock total + per-episode (python `resource` peak RSS of child +
wall); arena bytes allocated (deterministic); instrumented op counts
(ADD/KILL/PIN/UNPIN/PROMOTE/DEMOTE/ROLLBACK/SETSTAGE, refusals by code,
suppressed_imp, suppressed_fab, anomaly_suppressed,
conflict_kill_refused); probe correct/wrong/abstain at end+mid (A1/A3),
end (A2); spurious; `collateral_true_kills` (kills of established true
knowledge, ver_count≥6 with true value); silent overwrites (A1/A3: must
be 0 — every mutation via audited ops; A2: unaudited slow-tier installs);
audit completeness: audit_n vs ops issued, `ma_replay_check`,
`ma_audit_clean_refusals` (A1/A3); A2: no audit machinery (0% by
construction).

## Kill / decision bars

- **K1:** MA1 rerun must reproduce 58/58 (`MA_FAILURES,0`), 28 audit
  entries, replay+clean-refusals pass. Else halt: trained baseline broken.
- **K2:** C1 bill numbers reproduce: probe counts EXACT (A2 C3:
  128/128/64 correct/wrong/abstain + 64 spurious_slow; A1-analog delib C3:
  320/0/0/0), wall-clock within 25% (machine variance). Else halt:
  curriculum drift.
- **K3:** ≥3 runs/arm byte-identical (SHA256 of stdout). Else halt.
- **K4:** `grep -iE 'rng|rand\('` clean on all new sources. Else halt.
- **D1 (decision):** if A3 matches A1 on end-probe AND spurious==0 AND
  collateral==0 → verdict "trained judgment adds nothing measurable on
  this probe set" (falsifies the training-value hypothesis here).
- **D2:** the bill must state separately what STRUCTURE buys (audit
  completeness, replay-exactness, silent-overwrite count — expect A1==A3)
  vs what JUDGMENT buys (probe accuracy, spurious, collateral — expect
  A1≥A3>A2). If A1==A3 on judgment metrics too, say so plainly.

## Predicted (not asserted) outcomes

A1: end 80/80 (C1), 80/80 (C2), 320/320 (C3), 0 spurious, 0 collateral,
audit 100%, replay exact. A3: end-probe near-perfect on true recall
(phase D re-teaches) BUT >0 spurious (fabricated installed: C1:8,
C3:32), >0 collateral true-kills (C1:4, C3:28), mid-probe degraded;
audit 100%, replay exact, 0 silent overwrites — structure intact,
judgment visibly naive in the ledger. A2: bill numbers (C3 128/128/64,
64 spurious; C1 32/32/16, 16 spurious), 0 audit entries.

## Amendment policy

This file is never edited after 2026-09-24T05:53:27Z. Any change to arms,
curriculum, probes, or bars → new file
`KBCONTROL_PREREG_AMEND_<n>.md` with rationale; runs under an amended
prereg are labeled as such.
