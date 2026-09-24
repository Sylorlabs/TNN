# D-1 DEBATE RECORD — PROPOSER CASES (native crew, strongest case for each hypothesis)

Date: 2026-09-24. Crew: D-1 (debate: intervention-family hypotheses H-PAM-7/8/10).
Objector: grok-4.7 at highest reasoning (independent steelman; response filed in OBJECTOR_GROK47.md).

---

## H-PAM-7 (interventional perturbation-response warrant) — PROPOSER

The wall (KB4) killed every second check that re-reads the same bytes: G2, G5, R2-4 all dead, 12+
forks down. H-PAM-7 is the first proposal in this program whose gate evidence is *causally
different* from the percept bytes, not a second copy of them. The gate chooses the perturbation
*after* the percept arrives — crop shift, gain change, temporal re-crop — so the adversary cannot
pre-compute a consistent lie; it must respond in real time to a probe it did not choose.

The steelman's "wall one level down" framing understates the quantitative asymmetry. Spoofing a
static frame is O(1): paste bytes into a buffer. Spoofing a *lawful response function* to a
gate-chosen perturbation requires a world model that can render the percept's features under an
arbitrary affine/photometric transform with sub-tolerance error — and it must do it inside the
sensor round-trip latency, every time, for perturbations drawn from a repertoire the adversary
never sees in advance. The perturbation can even be *composed*: shift-then-gain, gain-then-shift;
the lawful-response model is checked on the composition, and composition multiplies the adversary's
rendering cost while costing the gate one extra read. The wall killed *zero-cost* second opinions;
this one is priced, and the price is set by the gate, not the attacker.

F7b (non-lawful honest transforms) is a calibration problem, not a death: the lawful-response model
is learned per sensor and per percept class from honest traffic, with a named "complex-scene"
abstention class — abstention routes to H-PAM-11 provisional, never to blind install. F7c (latency)
is bounded by the same delay bar F5-fullmech already passed (20.0%): one extra sensor read is
strictly cheaper than three temporal crops. The backtest is concrete: the 8/9 KB4 wrongs from the
F5 backtest were *static-frame* injections; a crop-shift response check withholds them because the
injected bytes carry no lawful response function at all — the attacker would have had to inject a
response renderer, not a frame.

Concession (preregistered, not assumed away): F7a-class attacks — driver-level spoof that fakes
the perturbation response — MUST be in the battery. The proposer's claim is that they are *priced*,
not impossible. If the price measures zero, the hypothesis dies honestly.

---

## H-PAM-8 (cross-modal independent-path warrant) — PROPOSER

R2-3 — the evidence-independence admission law — is ALIVE: 1,200/1,200 withheld. It is the only
surviving law from the round-1 wreckage, and it is a law *without a mechanism*. H-PAM-8 is that
mechanism: it operationalizes "independent evidence" as a *causal-path* property, checkable at
build time by construction (separate drivers, separate buffers, separate buses — shared-driver
pairs disqualified at build time, not hoped away at runtime).

The proposer grants the steelman's F8c point *structurally*: that is why path-independence is a
build-time construction property with an adversarial audit of the claim itself, not a runtime
assertion. And the defense is cost multiplication, not metaphysical independence: a bimodal spoof
must solve a *consistency* problem across two sensor models in real time — visual claim "object X
at L" must carry an acoustic/thermal/temporal signature consistent with X at L in the same
episode. The unimodal tax (F8a) is handled the honest way: a *named* fallback with its own
preregistered kill bar, not a silent carve-out. The fallback is H-PAM-7's perturbation-response —
which is exactly why D1 pairs them: each is the other's audit.

The key number the proposer commits to: the independence premium must be *measurable and
positive* on the bimodal-spoof vs unimodal-spoof quadrants. If it is zero, the hypothesis dies —
no "defense in depth" hand-waving. The wall said same-evidence second opinions are zero
information; H-PAM-8 never reads the front-end's stream at all, so the wall's logic does not
apply to it — the objection must be to the independence claim itself (F8c), which is why the
audit is part of the mechanism, not an afterthought.

---

## H-PAM-10 (act-to-check world-action warrant) — PROPOSER

H-PAM-7 probes the *sensor*; H-PAM-10 probes the *world*. That is a strictly stronger locus: the
adversary's spoof lives in the byte path, but the outcome of a world action lives in physics.
To defeat a discriminating action the adversary must spoof physics, not bytes — and the
discriminating parameter is gate-chosen and *state-dependent* (derived from ledger state the
adversary does not hold), so the echo cannot be pre-computed even through a fully spoofed sensor
path. No randomness anywhere: the parameter is deterministic given ledger state, unpredictable
given only the spoof.

The F10c objection (the check becomes a behavior-manipulation surface) is real but *bounded by
design*: interventions are budgeted (max N per episode), reversible actions preferred, and the
repertoire is preregistered with known discriminating power per percept class. A spoof designed to
elicit a specific action is itself a preregistered attack class in the kill bar — the bar is
"manipulation succeeds zero times", and the repertoire's blind spots (F10b) are *named as
uncovered* with a reported coverage metric, never hidden. Honesty about coverage is part of the
mechanism.

The proposer's strongest point: H-PAM-10 is the only hypothesis in this family whose evidence the
front-end provably could not have seen — the front-end saw bytes; the gate sees *what the world
does when poked*. It is the admission contract's interventional form taken literally. Where the
outcome path is fully spoofable, the class is marked uncovered and the fallback (H-PAM-7
sensor-perturbation, which is unaffected by F10c because it acts on no repertoire the adversary
can drive) takes over. D4's discrimination-per-cost metric decides the locus; the proposer
commits to losing on cost and winning on attacker-unpredictability.

---

*Proposer cases closed. Objector response: OBJECTOR_GROK47.md. Adjudication: DEBATE_RECORD.md.*
# D-1 DEBATE — NATIVE STEELMAN OBJECTOR (objector cases at full strength)

Date: 2026-09-24. Crew: D-1. Status: NATIVE objector (external round deferred —
UnoRouter down for the session: grok-4.7 HTTP 524 ×3, claude-fable-5.1 HTTP 524,
gpt-5.6-sol `choices:null`/0 tokens. External prompt preserved at
`objector_prompt.txt`; re-run when the connector recovers).
Proposer cases: PROPOSER_CASES.md. Probe evidence: PROBE_PREREG.md + probe
outputs (3× byte-identical, SHA 182040ff1a7e5b3ea214a589678c6af63155f420e6d52963c7da6d67fd40f064).

---

## H-PAM-7 vs F7a: the driver-level spoof faking the perturbation response

**The attack, at full strength.** The proposer's asymmetry — "the adversary must
answer a gate-chosen perturbation in real time" — assumes the perturbation is
unobservable until the sensor answers it. It is not. The gate issues the
perturbation through the same driver stack the Class-B adversary controls; the
perturbation command (crop k, gain g, temporal offset) is visible on the bus
*before* the sensor responds. The adversary does not need a world model. It
needs a perturbation-consistent renderer: a pure function of (spoofed frame,
perturbation params) → lawful-looking response. That function is built ONCE, at
spoof-build time, and then every probe is answered in O(1). The H-B crews'
coherent-spoof kill battery already proves this adversary class exists:
temporally stable false percepts reproduce identically across all 3 crops — a
crop-consistent renderer IS a perturbation-response faker.

Composition does not save the proposer: composing perturbations composes the
renderer function; the cost is paid once at build time, never per probe. And the
latency the proposer counts as attacker cost is actually attacker *observation
time* — the driver sees the perturbation command first, then renders.

The probe measured this exactly: Class B (perturbation-consistent renderer)
installs 120/120 = 100%, and the install rate is τ-inert (τ=1 and τ=4 both
120/120) — no tolerance tuning escapes F7a. The "priced, not impossible" claim
is now a measured price: **zero** against a perturbation-consistent renderer.

**Conceded.** Against static-frame injection (Class A: 0/120 installs) the
mechanism is perfect. The proposer's asymmetry holds against adversaries who
cannot answer in real time. The claim narrows to "defense against non-adaptive
injectors" — which the program already had, cheaper, in the F5 predicate.

**Survival condition.** The intervention channel must be unobservable and
unanswerable by the adversary — a trusted-path assumption. That assumption needs
its own preregistered audit, or H-PAM-7 is priced only against weak adversaries.

**Mind-changer.** A Class-B battery where the faked response is caught —
measured, not asserted. The probe says it will not be.

---

## H-PAM-8 vs F8c+F8a: independence theater + the unimodal-fallback hole

**The attack, at full strength.** "Disjoint by construction" is asserted at build
time and audited against the design — but the deployed instance shares firmware,
clocks, power rails, physical mounting, and, decisively, a single adversary with
access to both drivers. The cheapest hidden common cause defeats the mechanism
without touching either path's integrity: inject the lie at the
sensor-fusion/world-model layer, ABOVE the modality split. One lie, consistent
in both modalities by construction. The "consistency problem across two sensor
models" the proposer prices is solved once, not twice — the adversary never
solves it per-modality at all.

The probe's analogue: two paths over the same record agree 600/600,
premium_bp=0, effective-n=1.0, and the audit correctly reports SHARED_SOURCE.
That is the mechanism's epitaph, not its defense: where the audit passes
honestly (truly disjoint paths), the warrant may have bite; where it is merely
asserted, the premium is zero BY CONSTRUCTION and no runtime check recovers it.

F8a is the deeper hole. The named fallback (P7) is a carve-out the adversary
CHOOSES: the rational adversary's dominant strategy is unimodal-spoof-into-the-
fallback, routing around P8 entirely. The fallback's own kill bar cannot close
this because the attacker selects the quadrant, not the defender. And the
premium quadrants assume the adversary bothers with bimodal spoof — the premium
measures the attacker's laziness, not the defender's strength.

**Conceded.** R2-3 (evidence-independence, 1,200/1,200) is real — independence
as a property matters, and H-PAM-8's contribution is making it a causal-path
property WITH an audit. The audit is the valuable part. The warrant is only as
strong as the audit, and the audit must be per-deployment and continuous, not
build-time.

**Survival condition.** Continuous per-deployment independence attestation, plus
the fusion-layer injection class (D1 Class C) in the battery as a named killer.
If Class C installs, the premium is theater.

**Mind-changer.** Measured premium > 0 on Class B vs Class A quadrants with the
F8c audit genuinely passing — not asserted.

---

## H-PAM-10 vs F10c+F10a: behavior-manipulation surface + cost

**The attack, at full strength.** The check is an actuator remote control, and
"manipulation succeeds zero times" is untestable: the adversary's win condition
is "make it move", which is satisfied BY THE CHECK FIRING AT ALL. Every
elicited action is an adversary win, and the bar cannot preregister the
adversary's objective function because the objective is the elicitation itself.
Budgeted and reversible does not bound harm: a reversible reach still displaces
objects and reveals intent; a probe emission is observable and localizes the
agent. The repertoire's blind spots are the adversary's farm: with measured
coverage at 25% (< 50% kill bar), three-quarters of the frozen classes are
uncovered — "named as uncovered" is honest bookkeeping, not a defense.

On cost the numbers are measured: 5.0× per check vs P7 (cost_ratio_x100=500),
discrimination-per-cost 11 vs 136. World actions are serial; the delay bar
(≤25% delayed >50) is the binding constraint — F5-fullmech barely passed at
20.0% with cheap re-inspections, and world actions are an order of magnitude
slower than re-inspections.

The state-dependent parameter is a read-access assumption the wall already
falsified: a driver-level adversary reads the ledger too, or infers the
parameter from the emitted action itself — the action is observable, and the
parameter must be derivable by the verifier, hence by anyone observing
action + ledger.

**Conceded.** On the driver-level spoof class (SB), P10 is the ONLY mechanism in
the family with non-zero discrimination: 5 bits vs P7's measured 0. The
world-outcome evidence is genuinely incomputable from a byte-spoof while the
parameter stays unpredictable. The proposer's locus claim is real but narrow:
P10 is a specialist for covered classes, not a general gate.

**Survival condition.** Coverage ≥ 50% with the F10c bar at literal zero, AND
the ledger-read-access assumption attacked as a named assumption, not a
background condition.

**Mind-changer.** A Class M battery with zero elicitations at full repertoire
coverage.

---

## Ranking: most likely to survive its objector

1. **H-PAM-7** — survives NARROWED. The objector's kill is scoped to Class B,
   not total: perfect vs static injection (0/120), dead vs adaptive renderer
   (120/120). A real mechanism with a measured boundary.
2. **H-PAM-10** — survives as a SPECIALIST. Unique SB discrimination (5 vs 0
   bits), but coverage-killed as a general gate (25% < 50%) and the F10c zero-bar
   is untestable-in-principle as formulated — the blocking test for any promotion.
3. **H-PAM-8** — weakest. The independence claim is the load-bearing part and it
   is the part defeated most cheaply: fusion-layer injection defeats the warrant
   without touching either path. What survives is the AUDIT, not the warrant.

## Are D1/D4 correctly designed?

D1: yes — Class B is exactly the F7a crux, the premium metric is the F8c crux.
One miss: Class C (fusion-layer injection) should be EXPLICIT in P8's battery,
currently folded into "F8c audit". Promote it.
D4: yes — discrimination-per-cost is the right deciding metric (probe: 136 vs
11, P7 wins locus, P10 the Class-S fallback — exactly the preregistered K4
rule). One miss: the ledger-read-access assumption behind the state-dependent
parameter should be a NAMED attacked assumption, not a background condition.
# D-1 DEBATE RECORD — adjudication (intervention family: H-PAM-7/8/10)

Date: 2026-09-24. Crew: D-1. Proposer: PROPOSER_CASES.md (native).
Objector: OBJECTOR_NATIVE.md (native steelman; external round deferred —
UnoRouter down: grok-4.7 524×3, fable 524, sol choices:null; prompt preserved).
Evidence: d1probe (pure Zag, zero RNG), 3× byte-identical,
SHA `182040ff1a7e5b3ea214a589678c6af63155f420e6d52963c7da6d67fd40f064`.
Fixture basis: `fixtures_ledger.txt`
SHA `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0` (verified).
Preregs (frozen, committed alone before code): commit
`bfab522aba6dac2fd83dceb305e865cde34135d1` (PREREG_D1_DRAFT, PREREG_D4_DRAFT,
PROBE_PREREG_D1DEBATE).

## Probe results (all committed predictions held)

- P1 (perturbation-response warrant): honest install 252/360; complex-scene
  (F7b) withhold 108/108 → honest-loss 30.0% (EXCEEDS the D1 K6 bar of ≤15%:
  the proposer's complex-scene abstention is load-bearing, not optional).
  Class A (static injection) install 0/120. Class B (perturbation-consistent
  renderer, F7a) install 120/120 = 100%, τ-inert (τ=1 and τ=4 both 120/120).
- P2 (independence audit): 600/600 path agreement, premium_bp=0,
  effective-n=1.0, audit=SHARED_SOURCE.
- P3 (D4 metric): coverage 25% (< 50% → P10 K1 kills the general claim);
  cost_ratio 5.0×; discrimination-per-cost P7=136 vs P10=11 (P7 wins locus);
  P10 SB bits=5 vs P7 SB bits=0 (P10 wins attacker-unpredictability on the
  driver-level class).

## Verdicts

**H-PAM-7 — NARROWED, not killed.** The general "priced defense" claim is
probe-killed: the price measured zero against a perturbation-consistent
renderer (120/120 installs, τ-inert). What survives, perfectly, is the
static-injection defense (0/120) — the proposer's asymmetry holds against
non-adaptive adversaries. The objector's kill is scoped to Class B. D1
prescription: P7 keeps the static/unimodal locus; it needs P10 (or a trusted
intervention channel with its own audit) as its Class-B audit. F7b honest-loss
(30%) forces the abstention-to-provisional design — a withholding P7 fails D1 K6.

**H-PAM-8 — warrant claim WEAKENED to audit-only.** premium_bp=0 and
effective-n=1.0 are measured, not argued; the fusion-layer objection defeats
the warrant without touching either path's integrity. What survives is the
continuous per-deployment path-independence AUDIT — which becomes a component
of the D1 hybrid, not a warrant. D1 Class C (fusion-layer injection) is
promoted to an explicit battery class per the objector's design note.

**H-PAM-10 — NARROWED to specialist.** K1 (coverage < 50%) kills the general
gate claim as preregistered (25%). What survives is unique: the only non-zero
discrimination on the driver-level spoof class (5 bits vs P7's 0). D4 K4 fires
as written: P7 wins the intervention locus on discrimination-per-cost
(136 vs 11); P10 becomes the fallback for Class S (driver-level) cases within
its repertoire. The F10c zero-bar stands as the blocking test for any promotion
beyond specialist; the ledger-read-access assumption is now a named attacked
assumption in the D4 battery.

## Commit rules fired

- **D1 hybrid JUSTIFIED** (complementary, non-overlapping failures): P7
  (static-frame/unimodal locus) + P10-specialist (driver-level covered classes)
  + continuous independence audit (H-PAM-8's surviving component). P8-as-warrant
  is dropped from the hybrid; neither locus alone suffices (both die on
  Class B/C as measured).
- **D4 locus DECIDED**: P7 wins on discrimination-per-cost; P10 is the Class-S
  fallback. Matches preregistered K4 exactly.

## Open items for the build crews

1. P7's complex-scene abstention → provisional routing (H-PAM-11) must be in the
   D1 prototype, or D1 K6 kills it on honest traffic (measured 30% > 15% bar).
2. The intervention channel needs its own trust audit (objector's survival
   condition for any future general H-PAM-7 claim).
3. External objector round (grok47/fable) re-run when the connector recovers;
   prompt preserved at `objector_prompt.txt`.
4. F10c "zero elicitations" needs a testable formulation before P10 can be
   promoted beyond specialist — currently untestable-in-principle as written.
