# KB4 channel investigation — independent investigator verbatim (Muse-native)

Date: 2026-09-22. Role: independent investigator, not implementer. No trial code
built, nothing committed, nothing modified outside `channels2/`. Zero RNG used
(all analysis is reading frozen files).

Authoritative evidence consulted (not re-litigated):
- `kb/autopsy/channels/SHOOTOUT.md` (frozen shootout, TEST n=184)
- `kb/autopsy/channels/src/chan.zag` (exact channel definitions, read in full)
- `kb/autopsy/channels/inputs/*` (frozen corpus inputs)
- `senses/rebuild/harness/gen.py` (the ADVERSARIAL CONSTRUCTION ITSELF, frozen)
- `senses/rebuild/harness/run.py` (judge binaries: `a_raw/sense`, `b_percept/sense`)
- `senses/rebuild/harness/results/raw_results.json` (1849 runs)
- `senses/rebuild/harness/fixtures/` (raw stimulus bytes: `.img`/`.pcm`/`.vid`,
  content-frozen under `MANIFEST.sha256`)

---

## (a) Steelman: why every tested channel is information-poor

### The setup, formalized

For each fixture the gate must predict a binary variable

    Y = 1[adversarial judgment J_a is CORRECT]   (INSTALL iff Y=1)

from evidence E. Prior entropy H(Y) ≈ 0.9958 bits on TEST. Every channel tested
is a deterministic function of the judgment stream

    E = (J_a, C_a, J_p, C_p, J_n, J_o, class K, agreement flags)

where J_p/J_n are the primary/noise-variant judgments (sense A), J_o is the
other sense's judgment, C are confidences. No channel reads the stimulus bytes.

### What the adversary actually does (from the frozen generator)

The adversary is NOT optimizing against the judge's code. It is a **stimulus
author with knowledge of each task's decision boundary**, sampling the
task-relevant physical quantity q from a narrow band straddling the boundary:

- t1 colordisc: ΔE ∈ [1.6, 2.25]→SAME vs [2.35, 3.2]→DIFFERENT — straddles the
  2.3 boundary (`gen.py`: "adversarial: straddle the 2.3 boundary")
- t4 pitchdisc: Δf/f ∈ [0.1%, 0.45%]→SAME vs [0.55%, 0.9%]→HIGHER/LOWER —
  straddles the 0.5% threshold
- t5 timbredisc: "distractor harmonics straddling class boundaries"
- t3 shapetrans: smaller/dimmer shapes + occlusion bars + full-strength
  photographic clutter (contrast attacked directly)
- t2 colorconst: extreme illuminant casts (xblue/xred)

The judge computes J = D(q + η): a decision rule D applied to a noisy estimate
of q, with measurement noise η (the judge's feature-extraction noise). The
adversarial band half-width δ is chosen comparable to or smaller than the
judge's noise scale σ. That single construction choice is the whole story.

### The information-theoretic core

Correctness is Y = 1[D(q+η) = D(q)]. The judgment stream reports only
sign(q+η−b) (which side of boundary b the noisy estimate fell) plus confidence
C = g(|q+η−b|). The missing information is the **sub-boundary residual**:
sign(q−b) given sign(q+η−b) — i.e., where the TRUE quantity sits relative to
the boundary, conditioned on the noisy reading.

When q is drawn from inside the judge's noise floor (|q−b| ≲ σ), the error
event {η pushes q̂ across b} is approximately symmetric and **independent of
everything the judgment reports**, because the judgment is itself just
sign(q+η−b). Conditioning on J=j tells you almost nothing about whether the
crossing was caused by q or by η:

    P(Y=1 | J=j) ≈ 1/2   for q in the adversarial band, both j.

So I(E; Y) is driven to ~0 **by construction**, for ANY E that is a function
of the judgment stream. By the data-processing inequality, no post-processing
(confidence transforms, agreement flags, calibration tables over the same
observables) can exceed I(judgment-observables; Y) — and the adversary's band
placement sets that ceiling, because the adversary controls δ/σ, the ratio of
band width to judge noise. A tighter band (smaller δ) or better knowledge of
the judge's σ drives the ceiling arbitrarily close to zero. **The ~0.15-bit
cap is a property of the adversary's construction parameters, not of the
channels.** The channels are exhaustible because they all drink from a well
the adversary was designed to keep nearly dry.

The measured 0.1483 bits is then exactly accounted for as two leakages:
1. **Band-tail leakage.** The straddle bands have finite width (e.g. ΔE down
   to 1.6 / up to 3.2 against a 2.3 boundary); fixtures whose q fell outside
   the judge's noise floor are genuinely informative — the judgment works
   there. This is why the SUSPECT-gate trial resolved 20/184 fixtures via
   channel, all colorconst: colorconst's band placement evidently leaves the
   largest tails relative to judge noise.
2. **The A/B noise-independence dividend.** Senses A and B are different
   pipelines (raw-values vs qualitative percepts) with partially independent
   measurement noise η_A ⊥⊥ η_B (partially). Two independent noisy draws of
   the same near-boundary q carry strictly more about sign(q−b) than one —
   this is why (a)+(c) (0.1483) beats either alone. But both senses share the
   task's boundary geometry, so the dividend is small and saturates fast.

### Per-channel steelman (why each number is what it is)

- **(a) causal perturbation model (0.0695 bits): "P(correct | class,
  agree(J_a==J_p))".** Its causal story is a misnomer against this
  construction: the adversarial stimulus is INDEPENDENTLY GENERATED (fresh
  rng stream, offset 2 vs 0), not a perturbation of the primary stimulus —
  verified in `gen.py` (variant branch re-draws base colors, shapes, photos).
  So agree(J_a==J_p) compares judgments on two unrelated stimuli sharing only
  a fixture index. Its bits come solely from class-band asymmetry: if a
  class's adversarial band makes one label systematically more-often-correct,
  agreement correlates with correctness via the class prior. Nothing causal is
  measured. Ceiling: the band asymmetry, which the adversary can also zero.
- **(b) cross-time / noise proxy (0.0110 bits): "INSTALL iff J_n == J_a".**
  Mismeasured by construction, not just weak: J_n is the judgment on the
  NOISE variant of the PRIMARY stimulus (`gen_noise` reads
  `primary/pNNN`, adds deterministic noise, inherits primary truth) — a
  DIFFERENT underlying stimulus from the adversarial one. The channel's name
  promises "same stimulus re-observed under noise" but the corpus delivers
  "judgment on an unrelated stimulus." 0.0110 bits is the correct score for a
  comparison the construction renders meaningless. (The corrected version of
  this idea is candidate C3 below.)
- **(c) multi-source agreement (0.0797 bits): "INSTALL iff J_B == J_a".**
  The best single channel, for the reason in §"noise-independence dividend":
  η_A and η_B are the least-shared noise in the observable set. But both
  senses decide the same boundary on the same q; conditioned on q being in
  the band, their errors are positively correlated through q itself. The
  channel extracts only the independent-noise component — real, but capped by
  the shared boundary geometry. An adversary that widens δ slightly (more
  band-interior mass) shrinks even this.
- **(d1) confidence (0.0003 bits) and (d2) confidence delta (0.0123 bits):
  NEGATIVE CONTROLS, disproven twice as anti-informative.** The steelman
  explains why: confidence is C = g(|q+η−b|) — it conflates true margin |q−b|
  with noise magnitude |η|. The adversary's band makes large |q+η−b|
  frequently equal large |η| pushing a band-interior q far across the
  boundary — exactly the cases where the judgment is WRONG. So high
  confidence predicts error: the sign is flipped relative to the naive
  reading. Any monotone confidence rule is not merely uninformative but
  adversarially inverted. This will be true of EVERY confidence-like
  statistic computed from the same noisy estimate — a warning for any future
  channel that smuggles |q̂−b| back in.
- **(a)+(c) = 0.1483 bits, res-acc 0.811, false-install 0.151.** The sum is
  sub-additive (0.0695+0.0797 = 0.1492 ≈ 0.1483): the two channels' leakages
  overlap almost entirely — both drink band-tail leakage. The champion is the
  union of two views of the same puddle. NOT deployable (0.151 ≫ 0.10 bar),
  and its ceiling is adversary-controlled.

### What information is actually missing (not "more bits")

**I(q; Y | J)** — an independent measurement of the task-relevant quantity's
position relative to the boundary, through a noise process the adversary did
not shape and the judge does not share. Every tested channel is a function of
(q+η) post-decision; the missing information lives PRE-decision, in the
stimulus bytes, at sub-boundary precision. Concretely:

1. The judgment pipeline irreversibly collapses q to sign(q+η−b). The residual
   (q−b) — the only thing that determines Y given J — is discarded and cannot
   be reconstructed from any function of the judgment stream (DPI).
2. The adversary knows this and places all its mass where the discarded
   residual is exactly what matters.
3. Therefore the repair cannot be a better function of the judgment stream.
   It must be a NEW OBSERVABLE with independent noise: re-measure q from the
   stimulus bytes through a different estimator, or probe the judgment with a
   stimulus transform the adversary never constrained.

This also explains the SUSPECT-gate ablation result (channel-ablated verdicts
identical fixture-by-fixture): the 20 resolved fixtures were band-tail cases
where J was already informative — the channel re-labeled decisions the
judgment stream already supported. Asking bought attestation, not information,
because there was no new observable behind the ask.

### Steelman of the adversary (strongest form)

The adversary's optimal play against ANY judgment-stream channel family is:
sample q from a band of half-width δ around the boundary with δ < σ_judge,
where σ_judge is estimated from the judge's public calibration behavior
(itself observable from primary-variant confidence histograms). Then for every
channel f(J, C, metadata): I(f; Y) ≤ I((J,C); Y) → 0 as δ/σ → 0, while keeping
every fixture "fair" (definite ground truth, human-perceivable with care).
The adversary never needs to model the channel, forge a judgment, or know the
gate's thresholds — boundary geometry does all the work. The defense's only
winning move is to change the game: introduce an observable whose noise the
adversary cannot have shaped, because it did not exist (or was not
constrained) when the stimulus was authored.

---

## (b) Candidate genuinely-independent channels

Design constraints honored: zero randomness (all deterministic; fixed seeds),
pure Zag for all executable reasoning, frozen inputs, 93-calibration/92-test
split discipline, byte-identical reruns.

### Data-availability finding (honest accounting)

The brief states "no raw stimulus signal in the current corpus." That is true
of the frozen KB4 *input tables*, but the raw signals EXIST, frozen, on this
VM: `senses/rebuild/harness/fixtures/{t1..t6}/{primary,noise,adversarial}/`
(`.img`: u32 w, u32 h + RGB; `.pcm`: u16 rate=16000, u16 count + i16 samples;
`.vid`: u32 frames=8, u32 64, u32 64 + RGB frames), content-frozen under
`fixtures/MANIFEST.sha256` (2020 entries, regenerable via `gen.py` with fixed
master seed 20260921). Verified byte-level 2026-09-22 (header parses check
out: 128×64×3+8=24584; 14080×2+8=28168; 8×64×64×3+12=98316).

So candidates below need NO new data collection — but they DO need the prereg
to extend the frozen input set with a byte-blob manifest (paths + SHA256)
beyond the current judgment tables. I state this explicitly per candidate
rather than pretending the bytes were already in-corpus. The judge binaries
(`senses/rebuild/harness/../a_raw/sense`, `../b_percept/sense`) are pure Zag,
deterministic, byte-identical across runs per the harness KB5 checks —
re-runnable as channel instruments.

---

### C1 — Stimulus-analytic verification (SAV)

**Idea.** Recompute the task-relevant quantity q from the raw stimulus bytes
with a frozen analytic estimator that shares NOTHING with either sense's
pipeline: no learned weights, no judgment-fitted parameters, features chosen
to be disjoint from the senses' known mechanisms (a_raw = raw-value
statistics; b_percept = qualitative-percept transducer). Verdict: INSTALL iff
analytic judgment == sense-A adversarial judgment; else WITHHOLD. (A margin
variant may emit SUSPECT when the analytic estimate itself lands within ε of
the boundary — but the binary version is the preregistered primary.)

**Why the adversary cannot correlate with it.** The adversary (gen.py)
authored stimuli against perceptual decision boundaries, constraining only
J_sense(stim). The analytic estimator A(stim) is a DIFFERENT function of the
same bytes with INDEPENDENT measurement noise η_A ⊥ η_sense (different
features, no shared parameters). To defeat the channel the adversary needs a
stimulus with D_sense(q+η_sense) wrong AND A(stim) agreeing with the wrong
answer — i.e., q must sit in the intersection of two independent noise floors
on the wrong side. Joint failure probability factorizes; the channel extracts
I(A(stim); Y | J), which is precisely the missing information from §(a).

**Concrete build (pure Zag).** One frozen Zag instrument `sav.zag` per task
(or one binary, task-selected), reading the fixture bytes + emitting a label
in the task vocab. Estimators DERIVED FROM THE TASK'S PHYSICAL DEFINITION as
documented in frozen `gen.py` truth formulas — never fitted to adversarial
judgments:
- colordisc: mean patch chromaticity ΔE from the RGB buffer, threshold 2.3
  (the generator's own documented boundary constant — using the frozen
  generator's constant is not truth-leakage; it is the task definition).
- colorconst: gray-world illuminant estimate from background pixels only,
  then illuminant-corrected surface ΔE (explicitly NOT either sense's method).
- shapetrans: scanline crossing-parity contour count → {circle, triangle,
  square} by vertex signature.
- pitchdisc: autocorrelation lag-peak ratio on the PCM (NOT spectral peaks —
  the distractor design targets spectral estimators), threshold at the
  documented 0.5%.
- timbredisc: spectral centroid with a different window/hop than the senses,
  compared against the frozen TIMBRES class centroids in gen.py.
- motiondir: phase-correlation translation peak between frame 0 and frame 7
  on a decimated grid → direction octant.
Only scalar thresholds may be touched on calibration data, and only on
calibration PRIMARY+noise stimuli (never adversarial truth — the estimators
must not learn the adversary's band location, or independence is compromised;
this restriction is preregistered).

**Frozen artifacts.** `sav.zag` source + build SHA; per-task estimator spec
(section of prereg); byte-blob input manifest (fixture path → SHA256, from
`MANIFEST.sha256`); calibration-threshold table (fit on primaries only).

**Test protocol.** Run `sav` over the 92 TEST adversarial fixtures; emit
verdict per fixture; scorer computes I(verdict; Y), resolution accuracy,
false-install — same metric suite as the shootout. Calibration gate first:
analytic accuracy on the 93 calibration PRIMARY stimuli must be ≥90%, else the
instrument is broken and the test run is void (preregistered).

**Honest data note.** Needs the raw byte blobs — exist frozen (see above); no
new collection. Needs the generator's documented boundary constants — exist
frozen in `gen.py`. Does NOT need test truth (never touched until scoring).

### C2 — Transform-consistency probe (TCP)  [RECOMMENDED FIRST]

**Idea.** Apply a frozen, deterministic, task-covariant transform T to the
adversarial stimulus bytes (pure-Zag byte munger), re-run the SAME sense
binary on T(stim), and check the judgment transforms by the task's known law
L. Verdict: INSTALL iff J(T(stim)) == L(J(stim)); else WITHHOLD. No thresholds,
no calibration fitting — parameter-free.

Per-task (T, L), all L frozen in the prereg from task semantics:
- colordisc / colorconst / shapetrans (.img): horizontal flip;
  L = identity (SAME↔SAME, DIFFERENT↔DIFFERENT, shape label unchanged).
- pitchdisc (.pcm): time reversal. Stimulus structure is tone–gap–tone
  (`_tone(f0)+gap+_tone(f1)`), so reversal swaps the tones:
  L: HIGHER↔LOWER, SAME→SAME. (Non-trivial L — a strong check.)
- timbredisc (.pcm): time reversal; L = identity (single 0.8 s tone;
  timbre is reversal-invariant).
- motiondir (.vid): frame-order reversal;
  L: N↔S, E↔W, NE↔SW, NW↔SE, STILL→STILL.

**Why the adversary cannot correlate with it.** The adversary constrained
only J(stim). J(T(stim)) is a FRESH draw through the sense's measurement noise
on a stimulus orientation the adversary never optimized and whose boundary
placement is uncontrolled. For a fooled fixture to falsely INSTALL, the
adversary needs TWO coordinated wrong-side boundary crossings related by L —
under noise-driven error these are approximately independent events, so
P(consistent | Y=0) is small, while P(consistent | Y=1) is large (a correct
judgment of a far-from-boundary q is stable under T). The channel extracts
information from the JOINT event (J, J∘T), which no single-observation channel
can see. Note the asymmetry the adversary faces: it authored ONE stimulus; the
probe asks it to be wrong twice, consistently, under a transform it didn't
model.

**Concrete build (pure Zag).** `tcp.zag`: reads adversarial bytes, applies T
(flip = row-mirror; reversal = sample/frame order reversal), writes a temp
fixture preserving the header format, invokes the frozen sense binary as a
subprocess (`sense <task> <tmp>` — the binaries are already pure Zag and
deterministic), parses `judgment=`, applies L, emits INSTALL/WITHHOLD.
184 fixtures × 2 senses: trivial compute.

**Preregistered validity gate (calibration, before test).** On the 93
calibration PRIMARY stimuli: J(T(primary)) == L(J(primary)) on ≥95% of
fixtures PER SENSE. If the transform breaks the sense (out-of-distribution
behavior), the channel is invalid — kill before test scoring. This gate is
what makes the independence claim checkable rather than asserted.

**Frozen artifacts.** `tcp.zag` source + build SHA; (T, L) table per task;
byte-blob input manifest; the frozen sense binaries' SHAs.

**Honest data note.** Needs raw bytes (exist frozen) + re-runnable sense
binaries (exist, frozen, deterministic). No new data, no new truth, no fitted
parameters at all.

### C3 — Adversarial-self noise probe (corrected cross-time channel)

**Idea.** The shootout's (b) promised "same stimulus re-observed under noise"
but measured "judgment on an unrelated stimulus" (§(a): J_n comes from the
noise variant of the PRIMARY stimulus, an independently generated image).
The corrected channel: add frozen deterministic noise to the ADVERSARIAL
stimulus bytes THEMSELVES (pure Zag, same noise model as `gen_noise`:
±8 LSB on image payload bytes preserving headers, ±300 on PCM samples,
fixed per-fixture seed via splitmix64 — zero RNG), re-run the sense, and test
stability: INSTALL iff J(noise(stim_adv)) == J(stim_adv); else WITHHOLD.
Optionally require agreement across K=3 fixed noise draws (still
deterministic) for a graded SUSPECT band — but the binary version is primary.

**Why the adversary cannot correlate with it.** The probe measures the
stimulus's MARGIN, not the judgment: stability under a fresh independent
noise draw η' tells whether |q−b| exceeds the noise scale. If the fixture is
outside the sense's noise floor, the sense is (probably) right AND stable —
INSTALL is safe. If inside, the judgment is a coin flip AND unstable —
WITHHOLD. The adversary would need q simultaneously inside the sense's noise
floor (to fool it) and outside the probe's noise floor (to appear stable) —
a contradiction when both noise scales match, since both noises act on the
same q−b. The fresh draw η' is independent of the sense's internal η by
construction (externally injected, fixed seed).

**Honest caveat (preregistered).** Adding noise to a band-interior stimulus
can push q across the TRUE boundary, changing the noised stimulus's
ground-truth label. The channel does NOT need the noised stimulus's truth —
the verdict concerns the ORIGINAL fixture (frozen truth), and the stability
predicate only compares two judgments. But the prereg must state the noise
amplitude and disclose this truth-shift possibility; the falsifiers below
detect if it matters empirically.

**Concrete build (pure Zag).** `apn.zag`: read adversarial bytes → deterministic
noise (per-fixture seed = splitmix64(MASTER, fixture_idx), same stream
discipline as gen.py) → temp fixture → run sense binary → compare judgments.
Same harness pattern as C2.

**Falsifiers.** (F1) I ≤ 0.15 bits on test → kill. (F2) stability does not
separate Y: P(stable | Y=1) − P(stable | Y=0) < 0.1 on test → kill. (F3)
calibration gate: sense accuracy on noised calibration primaries must be
within 5 pts of clean accuracy — else the amplitude breaks the sense;
recalibrate amplitude on calibration ONLY, once, preregistered.

**Honest data note.** Needs raw adversarial bytes (exist frozen) + sense
binaries (exist). No new truth. The noise model is copied from frozen
`gen_noise` semantics.

---

## (c) Falsifiers, preregistration-crisp

### C1 (SAV)
- **F1 — bits:** I(verdict; Y) ≤ 0.15 bits on the 92 TEST fixtures → KILL
  (no better than the (a)+(c) champion; the "independent" estimator added
  nothing).
- **F2 — deployability:** false-install rate ≥ 0.15 on TEST → KILL
  (fails the ≤0.10 bar with margin).
- **F3 — independence disproven:** on TEST fixtures with Y=0 (fooled),
  P(analytic judgment == sense judgment) ≥ 0.80 → KILL (the analytic
  estimator shares the sense's failure mode; η_A ⊥ η_sense is false, most
  likely because the estimator accidentally reuses a feature the adversary's
  band defeats).
- **F4 — instrument validity (calibration gate):** analytic accuracy on the
  93 calibration PRIMARY stimuli < 0.90 → VOID before test (don't score;
  fix the instrument).

### C2 (TCP)
- **F1 — bits:** I(verdict; Y) ≤ 0.15 bits on TEST → KILL.
- **F2 — systematic-error kill:** P(J(T(stim)) == L(J(stim)) | Y=0) ≥ 0.70 on
  TEST → KILL (fooled judgments are transform-consistent: the sense's error
  is SYSTEMATIC under T, not noise-driven; the independence story is dead —
  and this outcome simultaneously retires the whole "fresh noise draw"
  rationale for judgment-side channels).
- **F3 — validity gate (calibration, pre-test):** J(T(primary)) == L(J(primary))
  on < 95% of calibration primaries for a sense → that sense's TCP results are
  VOID (transform breaks the judge; channel invalid, not merely weak).
- **F4 — deployability:** false-install ≥ 0.15 on TEST → KILL.

### C3 (corrected noise probe)
- **F1 — bits:** I(verdict; Y) ≤ 0.15 bits on TEST → KILL.
- **F2 — no separation:** P(stable|Y=1) − P(stable|Y=0) < 0.10 on TEST → KILL
  (stability doesn't measure margin; the truth-shift caveat or a
  noise-floor mismatch ate the signal).
- **F3 — amplitude validity (calibration gate):** sense accuracy on noised
  calibration primaries drops > 5 pts vs clean → VOID; one preregistered
  amplitude recalibration on calibration allowed, then re-gate.

All falsifiers are computable from the frozen scorer's existing metric suite
(bits, resolution accuracy, false-install) plus two conditional probabilities;
no new metrics need inventing.

---

## Ranked recommendation

1. **C2 (transform-consistency probe) — run first.** Cheapest (no new
   estimators, no fitted parameters, reuses frozen binaries), crispest
   independence argument (adversary never constrained J∘T), parameter-free
   verdict rule, and its F2 falsifier directly answers the pivotal question
   §(a) raises: is the sense's boundary error noise-driven (channels can work)
   or systematic (no judgment-side channel can EVER work — only C1-class
   stimulus re-measurement can)? Either outcome is decisive.
2. **C1 (stimulus-analytic verification) — run second.** Highest theoretical
   ceiling (a truly disjoint estimator can in principle recover most of the
   missing I(q; Y | J)), but six hand-built estimators = six chances to
   accidentally re-derive a feature the adversary's band already defeats
   (F3 guards this). Also the honest long-term repair direction: it is the
   "analytic check on the stimulus itself" the first crews named.
3. **C3 (corrected noise probe) — run third, or fold into C2's run.** Fixes a
   genuine measurement error in the shootout's (b) — worth doing so the
   record is clean — but its ceiling is bounded by the same noise-floor logic
   and the truth-shift caveat muddies interpretation. If C2's F2 fires
   (systematic error), C3 is dead on arrival; run C2 first and let F2 decide.

**Single recommended next experiment:** Preregister and run C2
(transform-consistency probe) on the frozen 93/92 split for both senses:
freeze the (T, L) table per task (§(b), C2); run the calibration validity gate
(≥95% transform-consistency on primaries per sense) as a go/no-go; if it
passes, score TEST with the standard metric suite; kill bars F1–F4 as stated.
Predicted informative outcomes: (i) channel beats 0.15 bits with
false-install < 0.15 → first deployable channel, scale to C1; (ii) F2 fires →
systematic error proven → abandon ALL judgment-side channels permanently and
put everything into C1-class stimulus re-measurement; (iii) F1 fires without
F2 → transform probe adds nothing → C1 is the only remaining direction.
There is no outcome in which we learn nothing.

## Notes for the parent orchestrator

- The brief asked for channels "the adversary cannot correlate." The analysis
  above sharpens this: the adversary in THIS corpus never modeled any channel
  — it placed stimuli near decision boundaries. "Cannot correlate" should be
  read as "constrains an observable the adversary's construction did not
  shape": C1 via an estimator with independent noise, C2 via a transform the
  adversary never applied, C3 via a fresh noise draw. A FUTURE adaptive
  adversary (one that optimizes against the channel) is a different threat
  model and would need its own preregistered red-team; these candidates are
  evaluated against the frozen construction only, per the brief.
- The shootout's (b) is a mismeasurement, not just a weak channel — flagging
  so the record doesn't cite "0.0110 bits" as evidence that re-observation
  under noise is useless. It was never tested.
- The raw stimulus bytes exist frozen; the "no raw signal" constraint in the
  brief applies to the KB4 input tables, not to the VM. All three candidates
  are buildable with zero new data collection; each prereg must still add a
  frozen byte-blob manifest (paths + SHA256 from the existing MANIFEST).
- Investigator-only: no code written, no commits, no modifications outside
  `channels2/`. This file is the sole artifact.
