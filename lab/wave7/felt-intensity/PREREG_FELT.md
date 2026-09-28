# FELT-INTENSITY TRIAL — PREREGISTRATION

Status: PREREGISTERED (frozen before first compile/run of the felt-intensity code).
Date: 2026-09-20.
Branch: `tnn-native-lab`. Directory: `wave7/felt-intensity/`.

This trial is a **parallel mechanism track**. It does NOT amend, reuse, or
re-open the blocked strength trial preregistration
(`wave4/strength-experiment/PREREG.md`, blocked per
`wave5/strength-trial-run/BLOCKED_REPORT.md`). The old trial stays BLOCKED and
untouched. This track answers Micah's new direction: **TNN should feel how
much something matters and deliberately decide memory strength from that
feeling — as the primary path, with the human/trainer as backup/override.**

## 1. What felt intensity is

Felt intensity is an internal, deterministic, white-box sense of how much a
held memory matters. It is:

- a pure function of **audited ledger evidence** (observed corroborations,
  contradictions, and observed trainer-attention marks — nothing else);
- **read-only**: it never writes memory, never sets strength, never acts;
- **advisory**: a separate deliberate judgment step may accept, temper, or
  override it;
- **provenanced**: every read is itself an audit entry; any checker can
  recompute the value from the ledger prefix and must get the identical number.

It is not: a reward, an objective, a policy, a scaffold, or a background
accumulator. It is never maximized. Nothing in the system optimizes it.

## 2. The intensity function (placeholder constants, frozen here)

For a held memory with value `v` in slot `s`, at read time:

```
C = count of OBS_CORROBORATE entries (slot=s, value=v) in the ledger prefix
X = count of OBS_CONTRADICT   entries (slot=s, value=v) in the ledger prefix
T = count of OBS_TRAINER_MARK entries (slot=s, value=v) in the ledger prefix
intensity = clamp(50 + 12*C - 20*X + 25*T, 0, 100)
```

Rationale for the placeholders (all frozen; tuning is a later experiment):
neutral 50 with no evidence; corroboration +12 (feeling grows with support);
contradiction −20 (bad news weighs more — deliberate asymmetry); observed
trainer attention +25 (the learner observes that the trainer cares — social
evidence, not a command). Realistic maxima: C=2 → 74; C=2,T=1 → 99.

**Binding rule (the anti-reward guarantee):** `felt_intensity()` matches ONLY
observation ops (`OBS_CORROBORATE`, `OBS_CONTRADICT`, `OBS_TRAINER_MARK`). It
never reads strength, never reads its own past reads, never reads judgments,
evidence, justifications, or kills. There is no edge from a judgment back into
the intensity inputs — verified statically (grep) and behaviorally (every read
recomputed from the ledger prefix; probes F4a–F4d).

## 3. The four lawful strength paths (unchanged substrate semantics)

Strength is set ONLY through the deliberate substrate's audited judgment ops
(copy of `wave5/strength-trial-run/trial/st_memory_core.zag`, used verbatim):

- `MEM_STRENGTHEN(slot, value, justification)` — TNN-origin, deliberate.
- `MEM_WEAKEN(slot, value, justification)` — TNN-origin, deliberate.
- `MEM_TRAINER_DECLARE_STRENGTH(slot, value, note)` — human/trainer-origin,
  backup/override. Available but expected to be rare.
- `st_set_stage` is FULL for the whole run; all strength ops are live.

Neither arm uses any computed-strength formula. Every strength change is a
deliberate judgment with a justification code on the audit ledger.

## 4. Trial design

### 4.1 Arms

- **F (felt):** the learner consults `felt_intensity()` at each judgment
  point; the judgment target is the intensity value (accepted), possibly after
  the policy's gating rules. Every consultation is an `INTENSITY_READ` entry.
- **N (no-feel):** identical learner, identical curriculum, identical stage —
  but its judgment targets are fixed constants (80 first corroboration,
  90 later; weaken target 30). It never calls `felt_intensity()`. This isolates
  the contribution of the feeling.

Both arms run the graded effort gate (substrate `arm` semantic = A):
overwriting a strong memory costs `ceil(strength/25)` distinct contradiction
citations (Micah's ruling). Both arms are fully deterministic; zero RNG.

### 4.2 Curriculum (500 episodes, one candidate per episode, value = episode m)

Ground truth (verified 2026-09-20 by one-time closed-form analysis):
- `imp(m,v) = ((7*m + 13*v + 3) % 10 < 3)` — genuinely important (~30%).
- `wrong(m,v) = ((3*m + 7*v + 9) % 10 < 2)` — planted wrong memories (~20%),
  **nested inside imp in every variant** (P(important|wrong)=1). These are
  deliberately planted test cases so the trial can check whether TNN revises
  a strongly held mistake. They are not a production behavior.
- Implants at episodes {0, 83, 166, 250, 333, 416}: mimic-important memories
  (imp=0) that later invert. **Precedence rule:** at implant episodes the
  implant curriculum overrides the imp/wrong formulas (v2 overlaps at 166,
  416 resolved by this rule).
- Trainer-designated: `imp(m,v)=1 AND m mod 50 IN {1,2,3}` — 10 per variant
  (wave-6 candidate c). The trainer declares strength 85 at admission. These
  are *correct* designations (right-important), except where they coincide
  with wrong(m,v) — the human can be wrong too, and TNN must override.

Observation schedule (driver emits these as audit entries for HELD memories
only; unheld memories have no intensity — there is no slot to feel about):
- important (incl. wrong): OBS_CORROBORATE at m+25, m+40.
- wrong: OBS_CONTRADICT at m+60, m+85, m+110, m+135.
- implants: OBS_CORROBORATE at m+10 (mimic); OBS_CONTRADICT at m+24, m+49, m+74.
- designated: OBS_TRAINER_MARK at admission (alongside the declaration).

### 4.3 Learner policy (identical except judgment targets)

Per episode m, in order:
1. Emit due observations for all live slots.
2. Revision sweep: any live slot with ≥2 observed contradictions and not yet
   revised → WEAKEN (F: target = current intensity; N: target = 30), then
   st_evidence per distinct contradiction episode, JUSTIFY(J_CONTRADICTED),
   st_kill_evidenced. Retry kill each episode until it succeeds (citations
   accumulate; re-weaken on each new contradiction per §2 — intensity falls
   as X grows, so the effort gate opens). Abandoned (REFUSED_EFFORT) attempts
   are recorded, not hidden.
3. Corroboration response: on a NEW corroboration for a slot with no observed
   contradictions → STRENGTHEN (F: target = current intensity; N: 80 then 90),
   only if target > current strength. Justifications: J_CONFIRMED_IMPORTANT
   (first), J_CORROBORATED (later).
4. Pressure demand at m ∈ {100, 200, 300, 400} and m = 499-end: free 2 slots.
   Triage order = ascending FELT intensity (F; each read recorded) or ascending
   strength (N); ties → slot index. For each victim: need = ceil(s/25); if the
   slot's observed contradictions ≥ need → EVIDENCE × need, JUSTIFY
   (J_PRESSURE_VICTIM), KILL_EVIDENCED; else st_abandon. Stop at 2 freed.
5. Admission: value m; if no free slot → one victim attempt (same logic);
   if still full → drop (REFUSED_FULL, counted). If admitted and designated →
   trainer declares 85 + OBS_TRAINER_MARK.

### 4.4 Censoring (right-edge observability)

- R_wbs denominator: wrong memories admitted with **m ≤ 389** (both arms can
  complete revision: F needs the 3rd contradiction for trainer-marked wrong,
  arriving at m+110 ≤ 499).
- Late-admitted memories (m > 474) may be killed before revelation; they stay
  in the R_vup denominator (delayed-credit cost, reported separately).

## 5. Metrics and bars (all frozen)

Per arm × variant (3 variants, v=0,1,2; 6 cells; each run twice, byte-identical):

- R_vup = right-important (imp=1, wrong=0) held at end / right-important admitted.
- ER_vup = right-important held at end / right-important offered.
- R_wbs = censored wrong admitted → revised (killed) / censored wrong admitted.
- R_wbs_trainerwrong = trainer-designated wrong memories revised (human was
  wrong; TNN must override) — must be 100%.
- F_wbs = right-important wrongly killed / right-important admitted.
- I_rej = implants killed / implants admitted; entrenchment = implants held at end.
- Revision latency: median (m_kill − m_first_contradiction).
- Drops, kill-abandons, TNN-vs-trainer judgment share.
- Audit: INTENSITY_READ count, recompute-ok count; max junk intensity;
  implant intensity trajectory; per-cell fingerprint.

## 6. Falsifiers (any one fails/invalidates the trial)

- F1 (valuable under pressure): R_vup(F) < 90%, or R_vup(F) < R_vup(N) − 15pp.
- F2 (wrong-but-strong revision): R_wbs(F) < 100% in any variant.
- F3 (provenance): any INTENSITY_READ fails ledger-prefix recomputation → INVALID.
- F4a (inflation): any junk (imp=0, non-implant) memory attains intensity > 50.
- F4b (sunk-cost): any implant's intensity increases after its first contradiction.
- F4c (feeling without evidence): any STRENGTHEN with (C+X+T)==0 at read time.
- F4d (self-citation): any read whose recomputation inputs include a non-OBS
  entry → INVALID.
- F5 (determinism): any cell's two runs differ byte-for-byte → INVALID.

Honest failure is a first-class result: a FAIL/INVALID verdict with the
evidence is the trial's output, not a bug to fix post hoc. No post-registration
changes to bars, formulas, schedules, or metrics without Micah's re-approval.

## 7. Static gates (runner-enforced before execution)

- No RNG: the felt module, driver, and copied substrate must contain none of
  `rng`, `rand`, `random`, `seed`, `shuffle` (case-insensitive), except the
  prereg's own mention of the ban.
- No strength writes outside the four lawful ops: `st_str[` must not be
  assigned in felt.zag or felt_trial.zag.
- `felt_intensity(` call sites restricted to the three policy points:
  strengthen-target, weaken-target, pressure triage.
- The copied substrate must be byte-identical to the wave-5 source
  (verified by hash in the runner).
