# CREW C — CONTROL VERDICT

Per `PREREG_AUDIO_PRINCIPLES.md` Section 6. No ear claims anywhere in this
document — measurements only.

## Provenance

- Prereg: `audio_principles/PREREG_AUDIO_PRINCIPLES.md` (frozen f9748042bfbb).
- Sealed held-out targets: `SEALED_TARGETS.md` — committed 5841d4337bf1
  BEFORE the control path's target handling was written (prereg 5.5).
- Test manifest + frozen C1 derangement: `TEST_MANIFEST_C.json` — committed
  048e294085d9.
- Frozen scorer: `scorer_c.py` — committed dc82c4870fcb BEFORE any test run
  (prereg 5.2); validated 18/18 on disjoint dev targets with wide margins.
- Control path: `control.zag` — pure Zag, zero RNG, this toolchain. The
  intent path is genuinely parametric: descriptor string -> parsed synthesis
  parameters (frequency, envelope class, rhythm pattern, vibrato depth) ->
  per-sample synthesis. No lookup tables keyed to targets; no fitted
  parameters of any kind.
- Battery: 270 scored renders (80 targets x 3 arms + 10 C-R1 + 20 C-R2),
  every render executed 3x with byte-identical SHA-256 required
  (`SHA_LOG.txt`; all matched). Harness argv log: `ARGV_LOG.jsonl`
  (830 invocations audited: every descriptor is a manifest intent descriptor
  or the literal `C0`; zero measured values passed to the binary).
- Dither spot check: 20/20 stable (`DITHER_C.json`).
- SHA-memorization grep (§5.1): 8 descriptor-equality collisions disclosed
  below; no unexplained collisions.

## Results

| Axis | n | Intent hits | Bar | Pass | C0 hits | C1 hits | C1 ≤ 25% | z (intent vs C0) | p (one-sided) |
|---|---|---|---|---|---|---|---|---|---|
| Pitch | 40 | 40 | ≥ 28 | YES | 0 | 0 | YES | 8.94 | < 1e-300 (≈0) |
| Envelope | 20 | 20 | ≥ 14 | YES | 7 | 0 | YES | 4.39 | 5.7e-06 |
| Rhythm | 20 | 20 | ≥ 14 | YES | 10 | 0 | YES | 3.65 | 1.3e-04 |

Diagnostics:

| Check | n | Hits | Bar / rule | Result |
|---|---|---|---|---|
| C-R1 compositionality (novel pairs) | 10 | 10 | diagnostic | not table-suspect |
| C-R2 prosody (CV in [0.3%, 25%]) | 20 | 20 | ≥ 14 diagnostic | PASS |
| Dither ×1.001 gain stability | 20 | 20 stable | ≥ 19/20 | PASS |

## C-PASS conditions (all three required — prereg 2.2)

1. All three axes ≥ 70%: YES (100%, 100%, 100%).
2. All three C1 arms ≤ 25%: YES (0%, 0%, 0%) — no VOID; the scorer is strict.
3. Intent-vs-C0 significant at one-sided p < 0.01 per axis: YES
   (p ≈ 0, 5.7e-06, 1.3e-04).

**Verdict: C-PASS.**

## Kill table (prereg 2.4)

| Result | "TNN can reason over audio" | "Shitty open-loop generator" (Micah's hypothesis) |
|---|---|---|
| C-PASS | survives on the control conjunct | **FALSIFIED as stated** |

An open-loop generator cannot hit shuffled held-out targets beyond its null
arm. The C0 arm — the same machinery with the intent path severed (frozen
constant descriptor) — scored 0/40 on pitch, 7/20 on envelope (the flat
items, by construction of the default), 10/20 on rhythm (the even items).
The intent arm scored 40/40, 20/20, 20/20 on the same targets through the
same machinery, and the frozen derangement (C1) scored 0 everywhere, which
is what a strict scorer plus a faithful renderer must produce. The
compositionality diagnostic (C-R1 10/10 on axis pairs never co-occurring in
dev) rules against axis-wise table lookup: the intent path combines
parameters it never saw combined.

## Plain-language verdict

TNN-native machinery can aim. Given a target descriptor it has never seen,
the control path parses it into synthesis parameters and renders audio that
hits the target — 80/80 on the main battery, 10/10 on novel feature
combinations, 20/20 on held-out prosody targets inside the re-anchor box.
The null arm (intent severed) and the shuffle arm both sit at or below
chance, so the hits are the intent path working, not the scorer being
lenient and not the machinery getting lucky. On the prereg's terms,
"shitty open-loop generator" is falsified: an open loop cannot do this.
What this does NOT show: the control path is an engineered parametric
synthesizer (parsing + closed-form synthesis), not a learned policy — it
proves deliberate parametric control exists as TNN-native machinery with
zero Python in the path, which is what the CONTROL prong operationalizes.
Whether a grown TNN mind aims this way is a separate question this battery
does not address.

## Section 4 bearings (INFORMING the four Round-3B calls — deciding nothing)

### 4a. G4c source-relative reading
Weak bearing (prereg-anticipated gap): the control battery's targets do not
include HF-band properties, so C-PASS says nothing about 8–16 kHz
controllability. Noted as a gap if cited.

### 4b. Gate re-anchor values (prosody box [0.3%, 25%])
C-R2: 20/20 held-out prosody targets produced on demand with measured CV
inside the box (hit = measured within 35% of target; worst observed error
~9%). Per the prereg's C-PASS bearing clause, the re-anchored prosody box
is a CONTROLLABLE property of TNN-native machinery, not merely a
descriptive one — this strengthens the re-anchor as a design target for
future forks. (Adoption remains Micah's call.)

### 4c. B-F2 reuse-penalized DP re-test
C-PASS on pitch (40/40 held-out targets, |error| ≤ 2%) shows the mechanism
can STEER pitch deliberately. Per the prereg's bearing clause, the B-F2
failure mode reads as SEARCH (the DP wouldn't diversify), not STEERING —
the reuse penalty addresses search, so a C-PASS makes the re-test
well-posed: the mechanism can steer; the penalty makes it steer diversely.

### 4d. B-F1 prosody-taming redesign
C-PASS alone is feedforward evidence: prosody CV is steerable without any
feedback loop (C-R2 20/20 open-loop). If crew L reports L-FAIL, the combined
bearing is "taming must be FEEDFORWARD (invest in the planner, not the
loop)" per the prereg's L-FAIL + C-PASS clause. Standing by crew L's result.

## Deviations and disclosures (§5.5)

1. **Dither-check adaptation (cause: prereg text is perception-flavored).**
   §5.3 speaks of "gain applied to the inputs" and "answer stability." The
   control analog applied: 20 intent renders (P00–P06, E00–E06, R00–R05,
   manifest order) were re-run with a deterministic ×1.001 gain applied to
   the PCM samples, then re-scored with the frozen scorer. Hit-verdict
   stability 20/20 (bar ≥ 19/20). A brittle scorer or byte-keyed path would
   have flipped; it did not.
2. **Descriptor-equality SHA collisions (disclosed, not hidden).** The
   renderer is deterministic, so identical descriptors give identical bytes.
   Eight test-render SHAs collide with dev/build WAVs, all by descriptor
   equality: (a) env/rhy class labels (`env:flat/rise/decay`, `rhy:even`)
   are shared between dev and held-out BY DESIGN — the battery tests the
   category distinction; documented pre-seal in `gen_targets.py`; (b) two
   post-seal pipeline smoke tests (`rhy:swing21`, `pitch:880+env:decay`)
   rendered held-out descriptor strings during development. No parameter was
   fitted to any of these (the design is parametric with zero fitted
   parameters; the scorer was tuned on dev descriptors only), the seal was
   intact (smoke tests post-date both seal commits), and C1/C-R1/dither are
   unaffected. Recorded here per §5.5 rather than treated as a void.
3. **C1 construction choice.** For the categorical axes the frozen
   derangement is class-level (env: flat→rise, rise→decay, decay→flat;
   rhy: even↔swing21), verified to have zero fixed points at the item
   level; pitch uses a cyclic shift by 17 (gcd(17,40)=1). Committed in the
   manifest before test runs.

## Evidence tree (committed with this verdict)

- `control.zag` — control-path source (already committed dc82c4870fcb)
- `scorer_c.py` — frozen scorer (already committed dc82c4870fcb)
- `BUILD_DOC_C.md` — frozen design doc (already committed dc82c4870fcb)
- `SEALED_TARGETS.md`, `gen_targets.py` (5841d4337bf1)
- `TEST_MANIFEST_C.json` (048e294085d9)
- `run_battery.py`, `analyze_c.py`, `dither_c.py` — harness (this commit)
- `test_wavs/RESULTS_C.json` — per-render measurements + verdicts (this commit)
- `test_wavs/STATS_C.json` — bars, z-tests (this commit)
- `test_wavs/DITHER_C.json` — dither check (this commit)
- `test_wavs/SHA_LOG.txt` — all 270 render SHAs, 3x-verified (this commit)
- `test_wavs/ARGV_LOG.jsonl` — all 830 harness→binary argv records, audited
- `VERDICT_C.md` — this file
- Renders themselves excluded as regenerable (SHAs logged); binaries excluded.
