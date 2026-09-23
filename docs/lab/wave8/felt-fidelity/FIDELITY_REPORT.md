# Felt-Intensity Fidelity Investigation

**Question:** Micah challenged the wave-8 "feeling is inert" verdict: is the code
not true to his original idea — the wrong variation? This report recovers his
idea, traces `felt_intensity()` into actual decision code paths, names the
gaps, and answers whether F≡N comes from (a) feeling consulted-but-uninformative
or (b) feeling computed-but-structurally-irrelevant.

**Method:** transcript/memory recovery + code reading only. No new trials.
Code examined: `wave7/felt-intensity/felt.zag`, `felt_trial.zag`;
`wave8/felt-retrial/phase_e/felt_phase_e.zag`, `decides/decides_trial.zag`,
`develop/develop.zag`. Wave-8 decision structure is identical to wave-7
(same three call sites, same gates).

---

## 1. Micah's original idea (recovered)

**Honesty note:** the compacted transcript does not preserve his literal
original sentences about the feeling. What survives are contemporaneous
paraphrases recorded by the parent agent, quoted below and labeled as such —
plus his verbatim words from today.

His verbatim challenge, 2026-09-19:

> "i refuse to believe this this is a white box anything is possible maybe
> its time ti retire my feeling thing but i have high confidence itll work
> and wanna push trhough with it more maybe its not coded correctly like the
> right variation its not true to my idea"

Contemporaneous paraphrases of his original direction:

- `PREREG_FELT.md` (2026-09-20): *"TNN should feel how much something matters
  and deliberately decide memory strength from that feeling — as the primary
  path, with the human/trainer as backup/override."*
- Daily log (2026-09-19): *"memory strength primarily decided by TNN itself
  through a native, graded sense of 'felt intensity,' followed by a deliberate
  strength judgment."*
- `MEMORY.md`: *"TNN feels importance at different levels and deliberately
  decides strength from the feeling."*

The core of the idea, in his terms: **the feeling is the primary path by
which TNN itself decides memory strength.** Not a constant, not a formula,
not the trainer — the system's own graded sense of "how much this matters,"
followed by deliberate judgment.

---

## 2. How the implementation works

`felt_intensity()` (`felt.zag`, `felt_counts`): a pure function of audited
ledger observations —
`intensity = clamp(50 + 12*C − 20*X + 25*T, 0, 100)`
where C/X/T count corroborations, contradictions, trainer-marks for
(slot, value) in the ledger prefix. Read-only, audited (`INTENSITY_READ`
entries), never reads strength/judgments/kills. Constants acknowledged as
frozen placeholders ("tuning is a later experiment").

Per `PREREG_FELT.md` §7 it is consulted at exactly three sites
("the three lawful call sites"):

1. **Strengthen-target** — new corroboration, no contradictions: read
   intensity → deliberate `STRENGTHEN` to that target (if target > current).
2. **Weaken-target** — revision sweep (≥2 contradictions): read intensity →
   deliberate `WEAKEN` to that target (if target < current), then evidence,
   justification, evidence-gated kill.
3. **Pressure triage** — slots must be freed: read intensity per candidate →
   triage ascending (lowest felt importance first), then evidence-gated kill
   or abandon.

The N (no-feel) arm is identical except its targets are fixed constants
(80 first corroboration, 90 later; weaken 30) and triage orders by strength.

---

## 3. Decision-flow trace: does the feeling determine any outcome?

### 3a. Triage — feeling orders, the effort gate decides

`pick_victim` (`felt_phase_e.zag` ~line 260): F arm sets
`key=felt_unpack_intensity(p)`, picks the lowest key. **The feeling decides
only the ORDER in which candidates are considered.**

The kill itself (`try_kill_victim`, line ~308): the graded effort gate
`need=(cur+24)/25` distinct contradiction cites; kill proceeds only if
`cn>=need`. **This gate reads strength and contradiction counts. It has no
input from intensity.** If the victim isn't killable, it is abandoned
(slot NOT freed) and the next candidate is tried.

Consequence: a memory the feeling rates 99 is killed if evidence suffices;
a memory it rates 0 survives if evidence doesn't. The feeling is a spectator
at the execution — it sorts the waiting list, the gate swings the axe.

### 3b. Revision sweep — feeling sets a number, evidence decides the kill

Trigger is a COUNT: `xn>=2` contradictions (`felt_phase_e.zag` ~line 487).
F arm: `target=felt_unpack_intensity(p)`; weaken iff `target<cur` and new
contradictions. Then — identically in both arms — all contradictions are
cited, justification recorded, `st_kill_evidenced` attempted. **The kill
verdict is the evidence gate's, not the feeling's.**

The feeling does feed back weakly: the weaken target changes current
strength, which changes `need=(str+24)/25` for the kill. Worked example
(wrong memory: 2 corroborations then 4 contradictions):
- F: strengthen to 62→74; at xn=2, intensity=34, weaken to 34,
  need=(34+24)/25=2, cn=2 → KILL.
- N: strengthen to 80→90; at xn=2, weaken to 30, need=2, cn=2 → KILL.
Same binary outcome. The feeling changed the margin (spare contradictions),
never the verdict — because curriculum contradiction counts (4 for wrong,
3 for implants) always eventually exceed every `need` either arm produces.

### 3c. Corroboration strengthen — feeling sets a number, and a LOWER one

F: `target=intensity` = 62 after one corroboration, 74 after two.
N: fixed 80 / 90. Strengthen iff `target>cur`. **This is the one site where
the feeling genuinely changes a stored value — and it makes the feeling arm
a WEAKER strengthener than the arbitrary-constant arm.** Both arms' memories
are retained (no contradictions), so the binary outcome is identical anyway.

### 3d. Micro-evidence that the feeling is consulted but outcome-irrelevant

Wave-8 phase-E: F-H1 vs N-H1 identical on every headline metric — but
`aband` (abandonment attempts) differs: 2649 vs 2595. Different victim
ordering → different abandoned attempts → **same victims killed.** The
feeling moves internal bookkeeping, never a verdict.

---

## 4. Gaps between Micah's idea and the implementation

**Gap 1 — The decision vs. the amount.** His idea: "deliberately DECIDE
memory strength FROM that feeling." Code: every *decision* (whether to
strengthen / weaken / kill) is triggered by observation counts
(`d_newc`, `xn>=2`, pressure episodes at fixed m). The feeling supplies only
the *amount* written once the decision is already made — and even that amount
is downstream-overridden by the effort gate. The feeling never answers
"should I?"; it only answers "how much?" after someone else said yes.

**Gap 2 — "Drives nothing" vs. "decide from the feeling."** The design doc's
proudest anti-reward claim (`FELT_INTENSITY.md` §2): *"Drives nothing; only
informs a separate deliberate judgment"* — tabulated against reward's
"Drives action selection." This was the investigators' choice to prove
not-reward-by-another-name. But it is in direct structural tension with
"decide strength FROM the feeling": a signal engineered to drive nothing
cannot be the primary path to a decision. The white-box auditability Micah
wanted does not require inertness — but inertness is what got built.

**Gap 3 — Flat 50 exactly where guidance is needed.** "Feel how much
something matters" implies a graded sense for every held memory. Code: any
memory with zero observations reads exactly 50 — and triage candidates are
overwhelmingly unobserved memories. The feeling is blind precisely where it
is asked to guide; ties fall back to slot index (arbitrary). F4a ("junk never
exceeds 50") *guarantees* this blindness as a safety property.

**Gap 4 — The feeling is the weaker strengthener.** §3c: 62/74 vs the N arm's
80/90. If the feeling is supposed to be the PRIMARY path to strong memory,
the implementation makes it the weaker path. Nothing in the trial could
reward the feeling for this; the comparison arm's constants were simply set
higher.

**Gap 5 — Placeholder constants, never calibrated.** 12/20/25 are
acknowledged placeholders, frozen by the "no post-hoc tuning" rule. The
coupling knob R (the one mechanism that could amplify the feeling's voice)
stayed at 50 in every Phase-C window — the joint feeling+calibration system
was built but never exercised. Micah's confidence may be in the concept with
real calibration; that concept has not been tested.

**Gap 6 — Where the drift happened.** The code faithfully implements the
prereg, and the prereg sincerely attempted his idea ("the judgment target is
the intensity value (accepted)"). The drift is at DESIGN time, not code
time: operationalizing "decide from the feeling" as "feeling sets the target
number" preserved the letter while losing the mechanism — because in this
decision architecture, target numbers don't cross decision boundaries.

---

## 5. Verdict: (a) vs (b)

**Primarily (b): the feeling was never given a real job — with (a) as a
compounding factor.**

Evidence for (b) — computed but structurally irrelevant:
- Triage: intensity is an ordering key; the strength-based effort gate
  (`need=(cur+24)/25` vs contradiction counts) decides every kill. No
  intensity value can make an unevidenced kill happen or block an evidenced
  one (§3a).
- Weaken: intensity sets the target number; the subsequent kill is
  evidence-gated identically in both arms (§3b). Worked example shows margins
  change, verdicts don't.
- The one real numerical difference (strengthen 62/74 vs 80/90) never flips a
  binary outcome in the curriculum (§3c).
- Micro-proof of consultation-without-consequence: abandon counts differ
  (2649 vs 2595) while all headline outcomes are identical (§3d).

Evidence for (a) — consulted but uninformative where needed:
- Unobserved memories read flat 50 by construction; triage mostly chooses
  among unobserved memories (§Gap 3). Even where the feeling has signal, that
  signal is confined to amounts that don't cross boundaries.

The two compound: **the feeling is flat exactly where it holds ordering
power, and where it holds signal it is confined to amounts.**

## 6. What "the right variation" would structurally require

For the feeling to matter, a deliberate judgment's BINARY decision — not just
its amount — must be a function of intensity. Today the judgment's *whether*
comes from counts and the feeling fills in *how much*. The minimal faithful
variation: keep "feeling never directly writes strength" (program law), but
let the judgment policy decide strengthen-vs-hold and kill-vs-spare from
intensity thresholds (e.g., spare-vs-kill among evidence-eligible victims
ordered AND decided by felt importance), with the ledger recording the
intensity cited. That is a design change, not a bug fix — and it reopens the
reward question the investigators closed by making the feeling drive nothing,
so it would need its own preregistered anti-reward probes.

Micah's hypothesis is therefore **half-right**: the code is not buggy — it
implements its prereg exactly. But "the right variation" — one where the
feeling actually decides — was never built. What was built and tested twice
is a thermometer bolted next to a thermostat wired to other sensors.
