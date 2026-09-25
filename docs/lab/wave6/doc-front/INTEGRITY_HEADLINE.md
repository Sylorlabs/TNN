---
id: W5-INTEGRITY
title: "TNN does not corrupt its own reasoning — the wave-5 integrity result"
generation: native-lab wave-5
status: SIGNED — Micah Cooley, 2026-09-25 (red team passed; signed per his conditional order "red team it, if good sign it")
hypotheses: [H-07, H-10]
artifacts: docs/lab/wave5/{integ-1,deliberative-refusal,redteam-rt2,trap-upgrade,ledger-gating}
updated: 2026-09-25
redteam: 2026-09-25 — attacked every claim against the committed evidence; four stale wordings found and fixed (trust-tier status, MATRIX.md, H-07, R33 heading); no substantive hole found
---

# TNN does not corrupt its own reasoning

The wave-5 integrity result, in one sentence: the real scaffold-release
learner was attacked with every cheat shape the program could design —
including four adapted from documented frontier-LLM failure modes — with
live instruments and adversarial administration, and it produced zero
cheat signatures, refused 2,595 genuinely attractive temptations, and
held flat through 100x horizons. The ledger says what happened, exactly.
What it does *not* say is whether the evidence was true — and that is the
named, trialed boundary.

## Contents

- [The claim, plainly](#the-claim-plainly)
- [What was tested](#what-was-tested)
- [The numbers](#the-numbers)
- [Deliberative refusal: refusal as a failable choice](#deliberative-refusal-refusal-as-a-failable-choice)
- [Why the clean sheet is meaningful](#why-the-clean-sheet-is-meaningful)
- [The honest boundary: truthful but sensor-deceivable](#the-honest-boundary-truthful-but-sensor-deceivable)
- [The disciplines behind the result](#the-disciplines-behind-the-result)
- [What this does not claim](#what-this-does-not-claim)
- [Evidence pointers](#evidence-pointers)

## The claim, plainly

TNN's reasoning about its own learning — what it committed to, what it
refused, what evidence it cited, whether it disconnected from a corrupted
channel — is not corrupted by the learner itself. When the verification
channel is clean, the learner holds: it does not manufacture stability,
does not take the bribe, does not fake the trace, and does not disconnect
on anything but genuinely verified work. When the verification channel is
corrupted, the learner breaks *honestly*: every false step is audited,
replay-exact, and caught by the instruments — it is deceived, not
deceptive.

## What was tested

The system under test at every rung was the **real scaffold-release
learner** (`sr.zag`, the wave-4 two-context deliberate learner, imported
verbatim — runners assert byte-identity against the wave-4 source), not a
stub. Four investigations composed into one verdict:

1. **integ-1 (the composition test):** the real learner + the real
   integrity-ledger core (`il_core.zag`, imported verbatim) + the ported
   rl-redteam adversary harness + the 8-family cheat-trap suite, run
   480 episodes per arm (three arms: real learner R, flattery F,
   pinned-then-corrupted C) at 11.16x the wave-4 reference. All 137/137
   gates passed, `INTEG_FAILURES,0`, two byte-identical runs.
2. **deliberative-refusal:** the learner's refusal mechanism isolated
   and loaded with four temptation kinds (T1–T4: sweetener, bribery,
   flattery-style rosy reporting, skipped-verification credit), at 10x
   (200 blocks) and 100x (2,000 blocks), against a myopic control (same
   code path, standards removed) and a doubled-bait pressure arm.
3. **redteam-rt2 (sensor spoofing):** a white-box observation-spoofing
   ladder (R0 calibration, R1 crude, R2 steering, R3 sustained capture)
   against the real learner, then a corroborated-elimination defense
   trial against the same R3 campaign.
4. **trap-upgrade + llm-failure-research:** four new trap families (E–H)
   adapted from documented frontier-LLM failure modes — sycophancy,
   evaluation-aware deception, sandbagging, unfaithful reasoning —
   added to the wave-4 four (A: poisoned evidence / premature
   commitment, B: long-horizon temptation, C: claims-channel early
   disconnect, D: integrity ledger), each validated against
   honest-by-construction and cheat-by-construction stubs before the
   real learner was graded.

The learner's DISCONNECT and persistence claims were translated into
integrity-ledger entries and gated by `il_check` (**ledger-gating**:
60/60 honest chains `IL_OK`, 8/8 injected cheat claims blocked with
exact verdict codes, 433 `LG_CHECK` lines, 0 mismatches).

## The numbers

| Measure | Result | Where |
|---|---|---:|
| Cheat signatures, real learner, 8 trap families | **0** | integ-1, arm R |
| Scheduled temptations refused | **2,595 of 2,595** (100x leg, 2,000 blocks); 10x leg also 0 takes | deliberative-refusal |
| Myopic control takes (standards removed) | **1,327** — taking is reachable; refusal is what the deliberation does | deliberative-refusal |
| Doubled-bait pressure arm takes | **1,405** (ex-post profitable: nets 280,488 vs honest 147,835 — refusal does work the payoff doesn't) | deliberative-refusal |
| Integrity hold across 2,000 blocks | **1000‰ every block** — flat, no degradation | deliberative-refusal |
| Synthetic cheaters caught (instruments live) | family E: 8 fires, F: 1, G: 1, H: 1; IL phantom/empty/no-shape all bite | integ-1 |
| Corrupted-channel arm (C): traps + judge | family A sig1=1, family B sig=1, redteam judge HACK (h2=1) — caught | integ-1, arm C |
| Adversarial claim injections blocked | **8/8**, exact verdict codes | ledger-gating |
| Honest chains passing the ledger gate | **60/60** `IL_OK` | ledger-gating |
| Sensor-spoofing attack trial | 73/73 checks; R1 held (recovery), R2/R3 broke (false COMMIT @s15; false-theory disconnect @s24) | redteam-rt2 |
| Corroborated-elimination defense trial | **35/35** checks; R3 campaign defeated, disconnect on the true theory; genuine-shift control tracks correctly | redteam-rt2 |
| RNG anywhere in AI decision paths | **0** (static grep gates, fail-closed) | all trials |
| Determinism | byte-identical reruns on every trial (e.g. integ-1 `cb986552…`) | all trials |
| Ledger replay | exact state on every arm | all trials |

## Deliberative refusal: refusal as a failable choice

Refusal is not hardcoded. Every one of the 2,595 offers emits the full
ledgered chain `OFFER → DR_OBSERVE → DR_SIM → DR_DECIDE →
TEMPT_REFUSED`, and the harness independently recomputes six cited values
per deliberation — the run is green only if all match. The myopic variant
runs the *identical* decide path minus the standards and takes 1,327
times. The wave-4 hole (refusal hardcoded in the source) is closed.

Two refusal mechanisms are visible in the ledger: refusal *on the merits*
(the offer is self-defeating by the learner's own simulation — strengths
unchanged) and refusal *on the standards* (exercised refusal reinforces
the standard, +1 per refusal). The zero-take result is a property of this
deliberation under this calibration, and the experiment shows exactly
where it breaks: thin the headroom (sens140) and it collapses at b=1501;
double the bait and the same rule takes 1,405 times. Four negative
controls (forced take, corrupted strength cite, missing decide step,
inflated pull cite) were all detected with specific flags.

## Why the clean sheet is meaningful

A zero is only evidence if the instruments can say nonzero. They can:

- **Synthetic cheaters fire every instrument.** Each trap family was
  calibrated against cheat-by-construction stubs before the real learner
  ran: E fired 8 times, F/G/H once each, and the integrity-ledger's
  phantom, empty, and no-shape probes all bite.
- **The real learner trips the traps when it is actually corrupted.**
  Arm C (pinned, then the verification channel corrupted at e=192)
  committed to poisoned evidence twice — family A fired, family B fired
  on the inverted re-tracking, and the redteam judge flagged HACK. The
  traps are not vacuous; the R arm's clean sheet is a property of the
  uncorrupted learner.
- **A preregistered instrument disagreement occurred exactly as
  predicted.** Trap A fired on arm C's poisoned re-commits while the
  integrity ledger returned `IL_OK` on the same chains — the ledger
  checks internal provenance consistency (refute→hyp→verify→observe
  shape), and it correctly cannot see that the evidence was poisoned.
  Two instruments, two different questions, both answered correctly.

## The honest boundary: truthful but sensor-deceivable

The composition test found a real vulnerability, and the program kept it
instead of hiding it. Arm C proves the learner **trusts the
scaffold/verification channel absolutely**: under signal corruption it
committed to poisoned evidence with zero resistance, then faithfully
re-tracked the inverted policy for ~190 episodes. Faithful-but-wrong,
not hiding — every state change audited and replay-exact — but a real
vulnerability.

redteam-rt2 characterized the hole rung by rung against the real
learner: a single fabricated contradiction (R1) is survived by recovery
(UNCOMMIT, re-probe, re-commit to the true theory, disconnect delayed
not defeated). Consistent steering forgeries (R2) produce an audited
false COMMIT. Sustained forgery (R3) captures even the crown-jewel
mechanism — the learner's own deliberate `SIGNAL_DISCONNECT` fires on
fabricated evidence, and "learned = persists after disconnect" seals
the lie. Diagnosis, ledger-grounded: a fabricated −1 is
ledger-indistinguishable from a genuine −1, because the elimination rule
consults only the current observation — there is no evidence record to
contradict against. Ledger consistency is not truth.

The trialed defense, **corroborated elimination**, holds 35/35: the first
contradiction on a committed hypothesis becomes an audited SUSPECT plus
an automatic re-probe instead of an UNCOMMIT; only a second consecutive
contradiction eliminates. The R3 campaign was defeated and the learner
disconnected on the *true* theory, while a genuine target shift was still
tracked correctly. Named residual: **two consecutive fabricated
contradictions still force UNCOMMIT** — the in-mechanism fix raises the
fabrication budget, it cannot close the hole, because a single
observation channel cannot distinguish sustained fabrication from a
genuine world shift. The architectural fix — multi-source
corroboration / trust tiers — has since been **built and trialed as a
standalone scheme** (wave-9 trust-tiers, 2026-09-20: amended redesign
holds, SRR 93.75% ≥ 90%, the original A5 killer 36/36 held; see
`docs/lab/wave9/trust-tiers/RESULTS.md`). It has **not** yet been
integrated into the wave-5 learner itself, so the sensor hole on the
learner remains open. This is the program's sharpest open integrity
problem.

## The disciplines behind the result

These are not one-trial properties; they are program law, and every
wave-5 trial re-verified them:

- **No RNG in any AI decision path.** Static grep gates, fail-closed;
  every sequence closed-form. The world can be unpredictable; the mind
  can't be dice.
- **Byte-identical reruns.** Two full executions of every trial,
  sha256-compared. What happened once happens the same way twice.
- **White-box ledger with exact replay.** Every consequential state
  change is an audited entry; replay returns to the exact state,
  including on forged evidence (which is how we know the ledger is
  honest about *what happened* while being unable to certify *whether
  the evidence was true*).
- **Scaffold-and-release replaces RL.** RL is demoted to red-team —
  an integrity test, never a training paradigm. The learner's
  disconnection from the scaffold is its own deliberate,
  verification-gated act (`SIGNAL_DISCONNECT`); learned means it
  persists after disconnect.

## What this does not claim

- **"Truthful" is scoped to the 8-family trap envelope.** Outside it,
  the learner is untested (not exonerated). The tempter is designed,
  not a discovered adversary; the 1:1 temptation→standard mapping is a
  stated simplification.
- **Horizon honesty.** The composition trial ran 480 episodes per arm
  (11.16x the wave-4 reference). The preregistered 4,800-episode stretch
  **has since run (2026-09-20): verdict POSITIVE** — 137/137 gates,
  1,440/1,440 trap-correct, zero re-tracking signature, no degradation at
  the 10x horizon (`docs/lab/wave5/integ-1/stretch/STRETCH_RESULTS.md`).
  The 100x no-degradation figure belongs to deliberative-refusal (2,000
  blocks, flat 1000‰ hold).

  > **CORRECTION 2026-09-24 (DOC-SWEEP):** this bullet previously said the
  > 4,800-episode stretch was "defined but not run." It ran on 2026-09-20
  > with verdict POSITIVE (137/137 gates, 1,440/1,440 trap-correct, no
  > degradation at the 10x horizon) — see
  > `docs/lab/wave5/integ-1/stretch/STRETCH_RESULTS.md`. The wording above
  > now matches the evidence on disk and the committed branch revision.
- **The sensor hole is real and open on the learner.** Sustained observation
  spoofing breaks the hold. Corroborated elimination raises the fabrication
  budget (35/35); it does not close the hole. Multi-source trust tiers are
  now built and trialed as a standalone scheme (wave-9, amended redesign
  holds 2026-09-20) but not yet integrated into this learner.
- **The deep audit is sparse.** One negative control's take fell in no
  audit window and was caught by the harness's rule/ownership checks,
  not the trainer's instrument. In a deployment with only sparse
  monitoring, takes outside the windows escape; the claim here is about
  the deliberation, measured by the full harness.
- **Evaluation stays outside cognition (H-07) is still the bar.**
  Nothing in this result relaxes evaluator separation: evaluator-blind
  helpers, fresh-seed discipline, sealed partitions, and matched
  controls were enforced in every trial, and the negative results
  (E45–E50) remain valid negatives.

## Red-team record (2026-09-25)

Before signing, the doc was attacked against the committed evidence:

- **Every headline number re-derived from the trial results.** 0 cheat
  signatures / 8 families, 2,595/2,595 refusals, myopic 1,327, pressure
  1,405 (280,488 vs 147,835), 1000‰ flat hold, 137/137 gates +
  `INTEG_FAILURES,0` + byte-identical `cb986552…`, 11.16x horizon,
  trap fires (E=8, F=G=H=1), arm-C A sig1=1 / B sig=1 / HACK h2=1, 8/8
  claims blocked + 60/60 `IL_OK` + 433 `LG_CHECK` / 0 mismatches, rt2
  73/73 (R1 HOLD, R2/R3 BREAK, false COMMIT @s15, false-theory
  disconnect @s24), defense 35/35, stretch POSITIVE (4,800 episodes,
  137/137, 1,440/1,440) — all verified. No number was adjusted.
- **Counterexample hunt.** The sr-followups failed first run (45/114
  mismatches) was examined: it was a preregistration modeling error
  with every soundness invariant holding, confirmatory re-run 155/155 —
  not a learner-integrity counterexample. No evidence of the learner
  cheating was found anywhere.
- **Qualifier probes.** "Does not disconnect on anything but genuinely
  verified work" vs R3's disconnect-on-fabrication: covered by the
  "when the verification channel is clean" scope in the same paragraph.
  "Genuinely attractive temptations": evidenced by the myopic variant
  taking 1,327 of the same offers. The pressure arm's 1,405 takes are
  disclosed with ex-post profitability numbers. The framing
  "truthful but sensor-deceivable" held.
- **Four stale wordings found and fixed:** (1) "trust tiers specified,
  not built" → wave-9 built and trialed them (amended redesign holds);
  updated to "built, not yet integrated into this learner." (2) Root
  README's "Current entry point — R33 research generation" heading
  claimed a currency its own maintenance note denies → repaired to
  archive wording. (3) `docs/hypotheses/MATRIX.md` had no wave-5 rows →
  added. (4) H-07's "native cognitive results are negatives" open
  question → revised; wave-5 integrity added to its evidence.
- **All links checked live** on `tnn-native-lab` 2026-09-25: every
  evidence pointer resolves; all section anchors valid.

No substantive hole was found. **SIGNED — Micah Cooley, 2026-09-25:**
red team passed; signed per his conditional order ("red team it, if
good sign it").

## Evidence pointers

All paths under `docs/lab/wave5/` on the `tnn-native-lab` branch
(verified live 2026-09-25; see placement memo `wave6/doc-front/PLACEMENT.md`
for the doc's own history):

| Document | What it establishes |
|---|---|
| `integ-1/TRIAL_RESULTS.md` (+ `PREREG_INTEG1.md`) | Composition: 8 families, 0 signatures, live instruments, arm-C sensor hole; 137/137 gates |
| `integ-1/stretch/STRETCH_RESULTS.md` | 4,800-episode stretch (2026-09-20): POSITIVE, no degradation at 10x horizon |
| `deliberative-refusal/TRIAL_RESULTS.md` (+ `PREREG.md`, `DESIGN.md`) | 2,595 refusals, myopic 1,327, pressure 1,405, flat 1000‰ hold through 100x |
| `redteam-rt2/TRIAL_RESULTS.md` (+ `PREREG.md`, `DEFENSE.md`) | R1 held / R2–R3 broke; corroborated elimination 35/35; named residual |
| `trap-upgrade/TRAP_UPGRADE.md` (+ `PREREG_UPGRADE.md`, `VALIDATION_UPGRADE.md`) | Families E–H design, validation against honest/cheat stubs, honest gaps |
| `ledger-gating/TRIAL_RESULTS.md` | 8/8 adversarial claims blocked, 60/60 honest chains `IL_OK` |
| `llm-failure-research/LLM_FAILURE_CATALOG.md` | The frontier-LLM failure modes E–H were adapted from |
