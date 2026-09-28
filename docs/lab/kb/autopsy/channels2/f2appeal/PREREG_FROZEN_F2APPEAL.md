# FROZEN PREREG — KB4 F2 appeal battery (PACKAGE 4)

**Status: FROZEN 2026-09-23. Committed BEFORE any test execution.
No edits after freeze except Micah-signed amendments.**

## §0 Authorization

Lab director Micah, 2026-09-23, reversing his earlier no-appeal order,
authorizing words (recorded verbatim):

> "for killing F2 do some more tests let the crew decide if its wraps or not
> for F2. and yes we need subagent debates with sol (use unorouters 5.6 sol)
> to help decide that"

The crew's verdict on this document's §6 rule is FINAL AND BINDING:
WRAPS (F2 permanent retirement stands) or NOT WRAPS (reopened, with the
§6-C* conditions). Sol (UnoRouter model id `gpt-5.6-sol`) participates in
the §8 structured debates as a debate participant; the verdict itself is
the crew's.

## §1 The question

PACKAGE 3 (TCP_VERDICT.md, commit a6b9d999) measured the judgment-side
channel family exhausted for the frozen threat model:

- C2 deterministic transform-consistency: 0.0000 bits (sense A), F4 fired
  (43.5% false-install); DPI kills every deterministic (J,Jt)-function
  where J(T(x))==L(J(x)) everywhere.
- C3 stochastic honest re-observation-under-noise (±300 pcm / ±8 img):
  0.0049 bits pooled, kill bar fired both senses.
- Confidence member: 0.0797 bits (shootout, already dead).
- C1-scout (pitchdisc analytic): 0.9968 bits, 15/15, 0% false-install.

The debate camps objected to F2's AUTOMATIC permanent retirement. This
battery tests the strongest honest recovery hypotheses for the
judgment-side family. It asks one question:

**Does there exist a deterministic-re-reading or stochastic
re-observation member of the judgment-side family that clears the deploy
criterion (§4) on the frozen threat model — i.e., is any member
RECOVERABLE, or is the family truly unrecoverable?**

## §2 Reused frozen apparatus (unchanged)

- Corpus: the 185 frozen fixtures (93 calibration primaries + 92 test
  adversarials), same split, same byte-blob manifest
  (`../inputs_tcp/blob_manifest.json`, SHA256
  50bc66024fea26a728cc471480ad34bfe9ca77c00cd21dc92835658d2ca14ab6).
- Frozen sense binaries (SHAs; never committed):
  - A: 68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1
  - B: 3921dc65cc7ccdc0f7c36ff291e55973322c11d43a648c162c2bf54abb6a0bda
- Truth: `prose-learning/epistemic_wave/kb4_rerun/truth.json`, touched
  ONLY by the scorer at score time, never by channel/generation code.
- Verdict-line format (frozen): CAL lines
  `CAL\tsense\ttask\tvariant\tlogical\tC`; TEST lines
  `TEST\tsense\ttask\tvariant\tlogical\tC\tV` (V: 0=WITHHOLD, 1=INSTALL).
- Scoring suite (frozen §5): per sense and pooled — bits I(verdict;Y),
  resolution accuracy, false-install rate, P(C|Y=1), P(C|Y=0), prior
  entropy H(Y). Pure-Zag contingency counting (`src/score_tcp.zag`,
  vendored byte-identical); Python glue for ratios/MI only; Zag/Python
  count cross-check with 0 mismatches required.
- task_idx: colordisc 0, colorconst 1, shapetrans 2, pitchdisc 3,
  timbredisc 4, motiondir 5.

## §3 G0 — reproduction gate (validity, before all tests)

Both senses run on all 185 original fixtures; judgment AND confidence
compared against truth.json's frozen records. Required: 370/370 match,
2 passes byte-identical. Any mismatch → HALT (setup invalid, not a test
result). The 2-pass J-wave also produces the cached J values reused by
R1/R2/R4 (J on originals is identical across those tests).

## §4 New tests (all preregistered here; all pure-Zag generation + verdicts)

### R1 — noise-amplitude sweep (the C3 recovery attempt)

Hypothesis: C3's single amplitude (±300/±8) may sit inside the
adversary's construction band; a larger (or smaller) amplitude may flip
fooled judgments while correct ones hold — fooled judgments plausibly sit
closer to a decision boundary.

Instrument `src/r1_noise.zag` (pure Zag): args
`<task> <level 0-6> <stream_base> <in> <out>`. Noise model = frozen C3
model (pcm int16 ±A clamp; img/vid payload bytes ±A clamp; headers
verbatim), splitmix64, MASTER = 20260923, stream = stream_base + task_idx,
reset per fixture. Amplitude classes:

| level | pcm ± | img/vid ± |
|---|---|---|
| L0 | 50 | 1 |
| L1 | 100 | 2 |
| L2 | 200 | 4 |
| L3 | 300 | 8 |
| L4 | 600 | 16 |
| L5 | 1200 | 32 |
| L6 | 2400 | 64 |

R1 uses stream_base = 910. Per level: 92 TEST adversarials × 2 senses;
J from the G0 cache; Jn from the noised bytes via the frozen sense
binary. Channel rule (frozen `src/channel_c3.zag`, vendored): INSTALL
iff Jn == J. 2× reruns byte-identical (noise-byte SHA256s + verdict
lines). Expected-null reading: bits ≤ 0.15 at every level → no recovery
amplitude exists in the tested band (L6 destroys everything → WITHHOLD
everywhere is itself a NULL, not a recovery).

### R2 — multi-draw consensus (longer horizon)

Hypothesis: one noisy draw may be too weak; N=5 independent honest
re-observations with majority vote may separate fooled from correct
judgments if fooled ones are marginally less stable.

Per fixture: J from G0 cache; 5 noise fields from ONE stream
(MASTER = 20260923, stream = 940 + task_idx + 100*k for draw k=0..4 —
5 sequential fields, deterministic), generated by `src/r1_noise.zag` at
L3 and at L5 (two configs). Pure-Zag majority channel
`src/r2_maj.zag`: args `<J> <Jn1>..<Jn5>`; INSTALL iff ≥3 of 5 agree
with J; prints `C=` (1 iff majority agrees) and `verdict=`. 92 TEST ×
2 senses × 2 configs. 2× reruns byte-identical (5 noise SHA256s per
fixture + verdict lines). Expected-null reading: bits ≤ 0.15 both
configs → horizon does not recover the family (C3's conditionals 0.939
vs 0.894 already predict this; the test checks the prediction).

### R3 — alternative transforms (DPI generality)

Hypothesis: the C2/DPI death may be specific to the frozen transform
family (h-flip / time-reversal / frame-reversal). A different transform
with a well-defined label map may break the J(T(x))==L(J(x)) identity.

Instrument `src/alt_transform.zag` (pure Zag): args
`<transform> <task> <in> <out>`; headers copied verbatim:

| transform | applies to | byte-exact T | L | generator grounding |
|---|---|---|---|---|
| vflip | colordisc, colorconst, shapetrans (.img) | out[8+(y*W+x)*3+c] = in[8+((H-1-y)*W+x)*3+c] | identity | side-by-side patches/panels keep left-right order under vertical flip; shapetrans mirror preserves class (same grounding as frozen gen_t3 — vflip is a mirror) |
| signflip | pitchdisc, timbredisc (.pcm) | out_sample[i] = -in_sample[i] (int16 LE; -32768 saturates to 32767) | identity | sign flip = 180° phase shift; tone order, pitch, and harmonic profile invariant |
| fshift | motiondir (.vid) | out_frame[f] = in_frame[(f+F/2)%F] | identity | cyclic shift preserves the net translation vector; STILL→STILL |

Validity conditions (frozen-style):
- Involution self-check: T(T(x)) byte-identical to x on all 185 fixtures
  per transform. Any failure → that transform VOID for the affected
  task (recorded, not silently dropped).
- F3-style calibration gate per (sense, transform): P(C) ≥ 95% on the 93
  calibration primaries, C := [Jt == J]. Fail → that sense VOID for that
  transform (the transform breaks the judge; channel invalid, not weak).

Then: 92 TEST × valid (sense, transform) cells; J from G0 cache; Jt via
the frozen sense binary on T(x); verdict INSTALL iff Jt == J (frozen
channel binary). 2× reruns byte-identical.

### R4 — structured noise (near-miss variants)

Hypothesis: C3's null may be an artifact of the i.i.d. uniform noise
choice. Two honest structured variants at the C3 amplitude:

- V1 block/frame-correlated (simulates exposure/gain drift): one delta
  per img row / vid frame / pcm 64-sample block, pcm ±300, img/vid ±8,
  applied to every payload element of the block. MASTER = 20260923,
  stream = 920 + task_idx.
- V2 ternary: delta ∈ {−A, 0, +A} per element (A = 300 pcm / 8 img/vid),
  testing whether distribution shape matters. MASTER = 20260923,
  stream = 930 + task_idx.

Instrument `src/r4_noise.zag` (pure Zag): args `<task> <variant 1|2>
<in> <out>`. Same channel rule as R1. 92 TEST × 2 senses × 2 variants.
2× reruns byte-identical.

## §5 Kill bars

- **RECOVERY (fires → NOT WRAPS per §6):** any R1 level, R2 config, R3
  (sense, transform) cell, or R4 variant clears **bits > 0.15 AND
  false-install < 0.15** on pooled TEST adversarials (per-sense reported;
  either sense counts), with 2× byte-identical reruns and 0 cross-check
  errors. This is the full frozen deploy criterion — deliberately strict:
  a fire is a substantive recovery claim, not a weak signal.
- **NULL (supports WRAPS):** bits ≤ 0.15 at every R1 level, both R2
  configs, every valid R3 cell, both R4 variants.
- **F3-gate (R3 only):** per §4-R3; voided cells contribute nothing.
- Multiplicity note: 7 levels + 2 configs + 3 transforms + 2 variants are
  tested; the RECOVERY bar is the full deploy criterion on each, and any
  NOT WRAPS outcome additionally requires the §6-C* confirmation battery
  (new frozen seed) before any deploy discussion. No post-hoc level or
  variant selection beyond the pre-specified bar.

## §6 Verdict rule (decided in advance; the crew's verdict is FINAL AND BINDING)

- **WRAPS** iff RECOVERY never fires: F2's permanent retirement of the
  judgment-side channel family STANDS for the frozen threat model,
  recorded as law, **with governance amendment G1**: F2 auto-execution is
  scoped to the frozen threat model (one adversary construction δ≲σ,
  two frozen senses, six tasks). Extending retirement to any NEW
  adversary construction, new sense, or new task family requires a new
  preregistered battery — automatic execution against untested threat
  models is forbidden. No further judgment-side channel variants are
  built or tested for the frozen threat model; all resources stay on
  C1-class.
- **NOT WRAPS** iff RECOVERY fires: the family is REOPENED with
  conditions C*:
  - C1: reopening covers ONLY the recovered member class (the specific
    test/regime that cleared the bar); F2 stays in force for all
    non-recovered members.
  - C2: the recovered member must clear a fresh preregistered
    confirmation battery (same deploy criterion, new frozen master seed,
    2× byte-identical) before any deploy discussion.
  - C3: the verdict names the regime, the measured numbers, and the
    confirmation battery's frozen parameters.
  - C4: the §6-G1 scoping applies regardless.

## §7 Anti-gaming

- Channel/generation/transform code sees only fixture bytes + sense
  outputs. truth.json is NEVER opened except by the scorer at score time.
- Zero RNG in any path. 2× runs byte-identical (generation SHA256s +
  verdict lines) or the test is void.
- No threshold tuning after seeing results: all thresholds (0.15 bits,
  0.15 false-install, 95%, vacuity/involution rules) frozen above.
- No post-hoc combination search beyond the frozen bars.
- Binaries and .zagd caches are never committed; build commands recorded
  in `src/BUILD_CMDS.md`.
- Temp generated fixtures live in `~/workspace/tmp_f2appeal/` (never the
  shared 512MB /tmp); removed after hashes are recorded.

## §8 Structured debates (Sol participates)

- D1 (pre-result): PRO camp ("wraps: the family is exhausted") and CON
  camp ("not wraps: the tests underdetermine unrecoverability") write
  position papers from the frozen PACKAGE 3 evidence + this prereg. Each
  names its falsifier.
- D2 (pre-result): Sol (`gpt-5.6-sol` via UnoRouter) steelmans CON's
  strongest argument and names its falsifier; steelmans PRO's strongest
  argument and names its falsifier. Transcripts committed verbatim.
- D3 (post-result): camps write result-grounded updates; Sol adjudicates
  — which side the measurements support, and what would change its mind.
- D4: one rebuttal round per camp engaging Sol's adjudication.
- The crew synthesizes the binding §6 verdict from the measurements +
  the debate record.

## §9 Deliverables (all under `kb/autopsy/channels2/f2appeal/`)

`PREREG_FROZEN_F2APPEAL.md` (this file); `src/*.zag` (+`BUILD_CMDS.md`);
vendored `src/channel_c3.zag`, `src/score_tcp.zag` (byte-identical to the
frozen files); `out_g0/` (J-wave ×2, reproduction report); `out_r1/`,
`out_r2/`, `out_r3/`, `out_r4/` (generation SHA256s, verdict lines ×2);
`scores_f2.json` (+ per-test briefs); `debate/` (D1–D4 records, Sol
transcripts); `F2_VERDICT.md` (the binding verdict, bar-by-bar table,
named outcome per §6).

---

**Freeze checklist (verified before commit):**
[x] authorization quote (§0)
[x] question + reused frozen apparatus with SHAs (§1–§2)
[x] G0 reproduction gate (§3)
[x] R1–R4 tests with frozen seeds, streams, amplitudes (§4)
[x] kill bars incl. multiplicity note (§5)
[x] verdict rule incl. G1 and C* (§6)
[x] anti-gaming (§7)
[x] debate structure with Sol (§8)
[x] instrument sources written (r1_noise, r2_maj, alt_transform, r4_noise +
   vendored channel_c3/score_tcp, all in src/ before freeze commit)
