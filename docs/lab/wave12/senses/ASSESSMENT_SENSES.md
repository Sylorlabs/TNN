# Senses assessment — SALVAGE / REFERENCE-ONLY / DROP (2026-09-20)

Standing laws applied: pure Zag; no RNG in decision paths; strength is
judgment-set (never formula/computed); deliberate memory ops only
(add/kill/pin/promote/demote/strengthen/weaken); CORE/USER separation;
state-dependent variation architecture; memory-interface contract required
for any classifier; audio/vision NOT_QUALIFIED until contract exists.

## Verdicts

### SALVAGE (rebuild natively in the redo)

1. **R33 S0/S1/S2 qualification contract** (`R33_SENSOR_QUALIFICATION_PLAN.md`).
   The three-gate structure, paired-counterexample S1 method, four-route
   factorial, and "never silently convert out-of-envelope input" rule are the
   qualification law for the redo. Salvage the contract, not any fixture.
2. **RawRecord architecture** (B001 review §"Recommended architecture change"):
   `RawRecord = owned immutable bytes + exact physical metadata + provenance +
   integrity + order identity`; transactional ingress (validate → reserve →
   commit atomically); protected-memory "no legal victim" refusal; codebook
   digest bindings. This is the ingress design the redo implements.
3. **N06/N14 native encoded-file ingress path** (`sensor.zag` + `R33_B001_RAW_RECORD.zag`):
   byte-originated, SHA256-bound, generic observer with no semantic labels.
   Salvage as the proven S0/S1 engineering base. NOTE: phase 1 re-implements a
   bounded equivalent rather than importing N06's durable-blob machinery, to
   keep the build self-contained and auditable; N06 remains the cited prior.
4. **B001 falsification battery** (tests 1–9, confounds 1–7): adopted as the
   phase-1 harness requirements (byte-vs-array confound, sign preservation,
   metadata inconsistency, capacity atomicity, aliasing, protected selection,
   stale codebooks, ordering, derived-loss raw-bypass).
5. **R32 deterministic-comparison DECISION**: their own result retired the
   neural gate-as-sensory-bottleneck and retained the frozen raw temporal
   route (seed-stable). This independently supports the redo's raw-first
   direction. Salvage the *decision*, not the GRU.

### REFERENCE-ONLY (log, do not build from)

6. **R32 acoustic PAM reference JSONs** (V39, segmental, dual-segmental,
   local-hypothesis): task-framing ideas worth keeping — "retained ordered
   grounded evidence", "no tokenizer/word boundaries", "soft recurrent change
   points under resource pressure", paired near-twin evaluation. The
   machinery (GRU hidden state, gradient training, seed-selected) is not
   carried forward.
7. **R51–R54 vision preregs + honest NO_GO results**: the occlusion-failure
   trajectory is real evidence about what doesn't work (hand geometric
   summaries → local templates all failed the 0.75 occluded floor). Reference
   for the future vision track; do not re-implement the Python.
8. **R34 memory lifecycle/association/hypothesis/provenance Zag files**:
   reference for the delayed-credit *idea*. The mechanism (linear predictor
   setting retention value) contradicts judgment-set strength law → mechanism
   is DROP (see below); idea is reference.
9. **R32 TTS PAM material**: output-side speech synthesis; not sensory
   ingress. Reference only if an output track opens later.
10. **R33 N14/N06 run evidence folders**: cited as prior executed evidence;
    N14/N06 are consumed and must not be rerun.

### DROP (contradicts standing law or unrecoverable)

11. **R32 acoustic classifier machinery (all PAM .pt + GRU/segmental designs)**:
    GUILTY on the memory-interface contract question — proven by their own
    reference JSONs: memory is hidden recurrent state, no deliberate
    add/kill/pin/promote ops, no judgment-set strength, no CORE/USER
    separation, no citation episodes, seed-dependent training. Directly
    contradicts deliberate-memory law and the no-RNG decision-path law
    (seed-selected winners). The old work is not repaired; the contract is
    built greenfield and classifiers must meet it or stay out.
12. **R32_TTS_VOICE_DIVERSITY_RANDOM**: random-voiced synthesis; contradicts
    no-RNG law by construction.
13. **R34 `r34m1` retention-value predictor as mechanism**: formula-computed
    retention value contradicts judgment-set strength (MA1 law: strength is
    declared judgment, never computed). DROP the mechanism; keep the
    delayed-credit idea as reference.
14. **R51–R54 Python implementations**: Python cannot enter the canonical
    build (pure-Zag law). The .py files are design references only.
15. **B001 C01 driver as qualification evidence**: unexecuted, 11 filed bugs
    (C01-01 self-verification absent … C01-11 log-integrity overclaim). Not
    evidence of anything until executed against an independent oracle.
16. **Any claim that N06/N14 qualify live sensing or S2**: the closeout docs
    themselves forbid it. Audio/vision remain NOT_QUALIFIED.

## What the redo therefore is

Greenfield native-Zag: byte-originated sensor ingress (RawRecord) →
**deliberate memory-interface contract** (the missing piece — observations
enter memory ONLY through deliberate judged ops with declared strength,
citation episode, CORE/USER region, provenance to the sensor record) →
qualification harness (B001 falsifiers). Phase 1 builds the ingress +
contract skeleton + harness. No classifier is admitted until the contract
exists — that is the gate the old work failed.
