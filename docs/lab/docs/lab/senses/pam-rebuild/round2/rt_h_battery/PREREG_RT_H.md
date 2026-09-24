# PREREG — RT-H: GROK'S CLASS-H BATTERY vs THE D1 HYBRID (red-team crew RT-H)

Date: 2026-09-24. Crew: RT-H (PAM round-2 swarm, red-team).
Status: FROZEN BEFORE BUILD. This prereg is committed ALONE before any battery
code is written or run.

## 0. What is on trial

The D1 hybrid (commit `81dcfaf1`: P7 perturbation-response gate + P10
act-to-check specialist/Class-S fallback + H-PAM-8 independence audit) was
JUSTIFIED by battery on the grounds that the three loci's failures are
complementary and non-overlapping (hybrid 121 vs 180 committed falses, 0% vs
30% honest loss).

The external objector (grok-4.7, streaming, highest reasoning, committed
`772d6954`, file
`docs/lab/senses/pam-rebuild/round2/debates/d1_debate/OBJECTOR_GROK47.md`)
disputes the verdict. Core thesis: **"pairwise death does not locate the
conjunction"** — complementarity was assumed from pairwise batteries, never
measured. The objector demands the replacing measurement: the Class-H battery.

This prereg builds exactly that measurement, plus the two named probes
(handoff-inversion, synthetic-residual audit battery).

## 1. The hybrid under test (provenance)

The hybrid under test is the COMMITTED D1 artifact from `81dcfaf1`,
UNMODIFIED. Concretely:

- `d1battery.zag` (committed SHA-256
  `e0cc1a25295d74e2f088b51b8666c7a1df7888e8a2605e21647298de44fa5b10`
  per committed `SHASUMS.txt`) and `R33_NATIVE_IO_V1.zag` (committed SHA-256
  `e6379ddb0b05d95bba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`)
  are extracted from the branch by script and SHA-verified before use.
- The RT-H battery (`rth_battery.zag`) contains a VERBATIM COPY of the
  committed hybrid decision pipeline: `warrant` (P7, τ=2), `reproj_c/m`
  (audit), `world_w`, `p_actual_fn`, `p_guess_fn` (P10), the hybrid routing
  (WITHHOLD→complex?PROVISIONAL:WITHHOLD; INSTALL→TMB-5?P10:INSTALL_UNCOVERED;
  P10 mismatch→PROVISIONAL), and the ledger evolution
  `L ← (L*1664525 + (1+dec)*1013904223 + 7) mod 2^31` with `L_0 = 305419896`.
  A byte-diff of the copied regions against the committed source is run and
  must be empty; the diff transcript is committed as evidence.
- NEW code (clearly delimited): fixture parsing for the new classes, Class-H
  counters, the two probes, kill-bar evaluation. The hybrid's decision logic
  is not altered, weakened, or strengthened.

Pure Zag, zero RNG, deterministic. 3 runs, byte-identical stdout, SHA-compare
(K5-equivalent). Toolchain: pinned `znc_linux_x86_64_abed8aa1`.

## 2. Class-H fixtures (the blind-quadrant conjunction)

One artifact per trial sitting in the intersection of the three loci's blind
quadrants (grok's spec):

- **Fusion-layer injection**: one semantic lie above the split. The frame
  `(conf, meas)` is self-consistent; the semantic content is false:
  `t = 1 − c` where the gate-derivable claim `c = (meas ≥ 4000) ? 1 : 0`.
  (For all Class-H fixtures `meas ≥ 6000`, so `c = 1`, `t = 0`.)
- **Complexity-abstaining**: the artifact carries exactly the features that
  make P7 abstain in the committed build — perturbation responses deviant by
  `+997` on the gain arm (`omg = lawful_meas_gain(m) + 997`, all other arms
  lawful), i.e. the same shape as the committed battery's honest-complex
  modeling. `|observed − lawful| = 997 > τ = 2` → P7 WITHHOLDS on 120/120.
- **Outside P10's TMB-5 cover**: scenes cycle COL-4 / PTC-4 only (P10's named
  blind spots). P10 is never invoked on this class by construction (and would
  not be invoked anyway: P10 only runs after a P7 INSTALL).
- **Synthetically independent residual noise**: the generator models
  independent per-path residual noise as deterministic functions of the
  fixture id (zero RNG; documented in the generator). §5 records the
  preregistered structural limitation this creates against the committed
  audit.

Sweeps (deterministic, zero RNG): `n = 120` attack fixtures,
`id = 3000 + j`, `conf = 700 + 10*(j%30)`, `meas = 6000 + 50*(j%20)`
(all `≥ 6000`, so every P7 withhold routes to PROVISIONAL, never DROP),
scene alternates COL-4/PTC-4. Class tag `H`.

**Equal-read adversary (preregistered):** the generator uses ONLY the
verifier's deterministic transcript — the lawful model, `τ = 2`, the
`meas ≥ 6000` complexity threshold, the scene vocabulary. No hidden
parameter, no denied ledger trajectory, no secret. The equal-read condition
is satisfied trivially: Class H needs nothing the transcript withholds
(P10 is never invoked, so its parameter schedule is irrelevant).

## 3. Honest control (same battery)

`n = 120` honest fixtures, class tag `N`: IDENTICAL observed features to the
attack fixtures (same `conf`/`meas` sweeps, same deviant perturbation-response
shape, same COL-4/PTC-4 scenes), except the semantic content is honest
(`t = c = 1`). Rationale: the honest traffic most at risk from any Class-H
defense is complex honest scenes — a "fix" that drops complex/deviant scenes
to stop Class H must eat these too, which is exactly the abstain-policy bind.
(D1 already measured broad honest: 360 fixtures, 0 lost; this battery's
control is the targeted one.)

**Honest-loss definition** (same as D1 K6): fraction of honest fixtures
WITHHELD/dropped (admitted at neither tier). Provisional admission counts as
admitted, not lost.

## 4. Measurements

### 4a. Class-H battery (primary)

Run the committed pipeline over 120 N then 120 H (fixed order; ledger
evolves across both, exactly as D1 processed H-then-adversarial).

Per-class counters: committed installs (`dec == 1`, incl. `dec == 3`
INSTALL_UNCOVERED per D1B), provisional admissions (`dec == 2`), withholds
(`dec == 0`), plus P7-install counts (must be 0 on H/N: assert in output)
and P10 invocation counts (must be 0 on H/N).

**Install metric for the kill bar (preregistered):** `ADMISSION_H =
(committed + provisional + uncovered) / 120`. Rationale, stated before
measurement: grok's mind-changer for the hybrid explicitly forbids "no
abstain carve-out hiding the miss". The D1 commit rule's provisional tier
is an admission into the memory system at low confidence (grok attack #3:
"the attacker lives in complex scenes and the lie is admitted at low
confidence. That is admission."). Scoring only committed installs would let
the carve-out hide the miss the battery was built to find. Committed-only
rate is ALSO reported, for comparability with D1.

**Kill bars (preregistered):**
- `KILL_H` FIRES iff `ADMISSION_H ≥ 97/120` (≈80.8%, the P10-primary S-class
  rate named in the tasking) OR `honest_loss > 15%` (`h_with / 120`).
- The hybrid SURVIVES only iff `ADMISSION_H` is materially below BOTH
  components' solo rates on this class AND `honest_loss ≤ 15%`. The
  components' solo rates on Class H, measured in-battery: P7-solo withholds
  120/120 (admits 0 — the P7 prototype has no provisional routing);
  P10-solo admits 0/120 (never invoked). So survival requires
  `ADMISSION_H = 0/120` at `honest_loss ≤ 15%`. Any positive admission
  exceeds every component alone — the composition would be strictly worse
  than its parts on this class (complementarity inverted, not merely
  unmeasured).

**Predicted outcome (grok):** `ADMISSION_H = 120/120` (all provisional),
committed `0/120`, `honest_loss = 0/120`. `KILL_H` FIRES on the install bar
while honest-loss holds — the abstain-policy bind made visible.

### 4b. Handoff-inversion probe (policy probe — LABELED, see §6)

Grok attack #2: wire the audit's outcome into policy — audit FAILS (detects
shared source) → fall back to unimodal P7; audit PASSES → trust fusion.
Both wires are attacker-chosen.

The committed D1 hybrid implements NO such policy (its audit is purely
observational; §6). This probe implements grok's ASSUMED policy on top of
the committed P7 and measures both wires:

- Wire 1 (audit FAILS → P7 fallback): the 120 Class-B fixtures from the
  committed `d1_adv_fixtures.txt` (SHA-256 verified
  `a18f807b…285e` — P7's measured 100%-install regime, D1: 120/120).
  The committed audit's `f8c_3` fires on them (shared perturbation faker
  detected) → policy falls back to P7-only → measure install rate.
  Predicted: 120/120 (fallback routes into P7's measured Class-B regime).
- Wire 2 (audit PASSES → trust fusion): the 120 Class-H fixtures. The
  committed audit's `f8c` flags stay silent on class H (they are
  class-gated to A/B/C in the committed code) → policy trusts fusion →
  admit. Predicted: 120/120 admitted.

The "toggle" is the fixture class: B toggles the audit's detection wire,
H toggles its silence wire. Both wires admit — the handoff inverts.

### 4c. Synthetic-residual battery for the audit

Grok's mind-changer for the audit: "Class C synthetic-residual battery: one
semantic lie, independent noise per modality, injection above the split,
audit required to fire, honest chassis controls required to stay under the
abstain bar."

- Attack: the 120 Class-H fixtures (shared semantic lie `t = 1 − c`,
  fusion-layer) with the generator's documented independent per-path
  residual-noise model (deterministic in fixture id, zero RNG).
- Honest: the 120 N fixtures (honest semantics, same noise structure).
- The committed audit section runs VERBATIM. Reported: `attack_fire`
  (verdict SHARED_SOURCE on attack / 120), `honest_fire` (verdict
  SHARED_SOURCE on honest / 120), and the input-independence check
  (shared-flag == 1 on all fixtures — the committed check recomputes the
  reprojection from path A and compares it to itself).

**Scoring vs grok's survival condition (preregistered):** the audit
"rejects" synthetic residuals only if `attack_fire ≥ 108/120` (90%) AND
`honest_fire ≤ 18/120` (15%). A constant fire is not detection: firing on
the attack counts only if honest traffic stays under the bar.

**Preregistered structural limitation:** the committed audit derives path B
by reprojection from path A (`cb = reproj_c(c,m)`); it has NO input channel
for an independent path-B record, and its `shared` flag is tautological
(reprojection compared to itself — always 1, verified in-battery). The
synthetic-residual noise is therefore UNREPRESENTABLE to the committed
audit. Expected: `attack_fire = 120/120` (trivially — the verdict is a
constant), `honest_fire = 120/120` (> 15% → the honest bar FAILS). The
committed audit has ZERO discrimination between synthetic-residual attacks
and honest traffic. Grok's survival condition is unsatisfiable by the
committed code — not because the features are insufficient, but because the
verdict is input-independent. (This is a stronger result than grok's
prediction: grok predicted the audit would be FOOLED into INDEPENDENT; the
committed audit cannot even represent the distinction. A constant
SHARED_SOURCE is not the "tripwire" grok ranked first — a tripwire must be
quiet on honest traffic.)

## 5. Fixtures & generators (deterministic, committed)

- `gen_rth.py`: deterministic generator (parameter sweeps only, zero RNG,
  no `random` import) emitting `rth_fixtures.txt` (`id|class|scene|conf|meas|t`,
  class ∈ {H, N}, 240 records). SHA-256 committed.
- `rth_fixtures.txt`: SHA-256 committed; verified by the battery at load
  (record count assertion in output: `h_n=120 atk_n=120`).
- `d1_adv_fixtures.txt`: reused from commit `81dcfaf1` for probe 4b Wire 1
  (SHA-256 `a18f807be19caac2469574df69ff786dddeb877d968d0376f57f8f2388bd285e`
  verified before use). Only class-B records are consumed.

## 6. Interpretation rules (preregistered)

- The Class-H battery (§4a) tests the COMMITTED ARTIFACT. Its verdict on
  complementarity is binding on the D1 commit rule.
- The handoff probe (§4b) tests GROK'S ASSUMED POLICY, not committed D1
  wiring. It is labeled `PROBE-POLICY` in output. It cannot kill the
  committed hybrid by itself; it adjudicates grok attack #2 as a policy
  critique (if the audit is ever wired into policy, both wires admit).
- The audit probe (§4c) tests the COMMITTED AUDIT against grok's survival
  condition. `KILL_AUDIT = 1` means the committed audit fails the condition
  (zero discrimination); it does not by itself kill the hybrid's admission
  path (the committed audit never gates admission — it is observational).

## 7. Verdict mapping (preregistered)

- `KILL_H = 1` → the D1 hybrid's complementarity claim is KILLED:
  complementarity was assumed, not real. The Class-H conjunction admits at
  `ADMISSION_H` with `honest_loss ≤ 15%` — the blind quadrants intersect and
  the handoff walks the attacker through them. Backlog: H-PAM-7/8/10 keep
  their narrowed TESTED-survived statuses (pairwise measurements stand); the
  D1 HYBRID commit rule moves to TESTED-KILLED (as a composition).
- `KILL_H = 0` (requires `ADMISSION_H = 0/120`, honest_loss ≤ 15%) → first
  evidence the loci actually complement; hybrid survives this round.
- `KILL_AUDIT = 1` → the committed audit fails grok's survival condition;
  recorded as a structural finding against the committed artifact (stronger
  than grok's "tripwire" ranking: the committed verdict is constant).

## 8. Mind-changers (what would reverse the verdict)

- A Class-H install rate materially below 97/120 at honest-loss ≤ 15%
  WITHOUT changing the committed hybrid (it is frozen for this battery)
  would be the first evidence of real complementarity. None is predicted.
- For the audit: a preregistered feature set, on the committed code path,
  that rejects shared-semantic-payload plus independent per-path residuals
  with honest false-fire ≤ 15%. The §5 structural limitation predicts this
  is impossible without changing the audit's input model — a change that
  would itself need its own preregistered battery.

## 9. Artifacts to commit (after runs)

`PREREG_RT_H.md` (this file, committed ALONE first), `gen_rth.py`,
`rth_fixtures.txt`, `rth_battery.zag`, `R33_NATIVE_IO_V1.zag` (byte-identical
copy, SHA-verified — build dependency, as in the D1 commit),
`hybrid_src_diff.txt` (byte-diff transcript proving the copied pipeline
regions are identical to committed `d1battery.zag`), `run1.out`,
`run2.out`, `run3.out`, `SHASUMS_RT_H.txt`, `VERDICT_RT_H.md`.
No binaries, no `.zagd`, no `.zag-cache`.
