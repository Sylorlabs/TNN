# PREREG — G5 "heavy second-pass sense aimed at the 278" (Hypothesis G5)

**Date:** 2026-09-24
**Status:** FROZEN. No mechanism, threshold, bar, or procedure below may change without a new prereg.
**Order:** Micah — "no more debate — the tests decide. If G5 is killed, say so plainly and stop. No rescue missions."

## 1. Hypothesis (verbatim, champion C)

> There is enough sustained signal in the disjoint G span for a HEAVY second-pass
> sense to convert the 278 into installs under the EXISTING numerical bar, without
> touching thresholds.
>
> Design (frozen):
> - The second sense runs ONLY when the current sense is high-confidence
>   (conf>=700) but not PASS.
> - It re-reads the raw bytes (wider window, different byte grouping, or
>   prototype match against verified installs — pick one per task, freeze it).
> - It emits a label + PASS under the existing task-specific numerical strength
>   bar, or abstains.
> - It NEVER alters already-PASS records.
>
> Champion-C's steel version of this hypothesis adds the correlated-wrongs
> battery: run the 6 timbredisc wrongs (RICH installed, truth BRIGHT, conf
> 701-718, mrgF 353-382, seqs 10983/10992/11024/11049/11126/11192) through the
> second sense. If it re-emits PASS on >=2 of them, the hypothesis has learned
> the spoof features, not the truth — KILL regardless of conversion count.
>
> Kill bars (all must pass; any one fails = KILL):
> (a) Conversion: <100/278 true conversions = KILL (113 needed to drop the bar;
>     100-112 = real effect but insufficient, still does not clear 85%).
> (b) Mint: sealed-family false-PASS rate must not rise by more than 2 points
>     versus today's rate.
> (c) Regression: full RK-3 replay with G5 in the loop; RK-3 must not drop
>     below 88.48%.
> (d) Steel: >=2/6 timbredisc wrongs re-PASS = KILL regardless of (a).

## 2. Frozen second-sense design (G5)

**Name:** g5sense — "second look". One pure-Zag binary.

**Trigger (frozen):** runs ONLY when the first sense is high-confidence and
sense-level non-PASS: `conf >= 700 && sweep_prog != "PASS"`, where `sweep_prog`
is the sense-level prog from the frozen `sweep.jsonl` (NOT post-deliberation).
Rationale: the sense's PASS is the sense's claim; deliberation overrides are a
deliberation problem (ceiling test (c)), not a sense problem.

**Input:** `g5sense <task> <fixture> <jcode> <conf> <fA> <fB>`
- `<task>`: one of the six task names.
- `<fixture>`: path to the trial bytes. For R24A files the binary splits F/G
  itself (same split as the frozen sense). For non-R24A (legacy harness
  `.img`/`.pcm`/`.vid`) there is no G span → ABSTAIN.
- `<jcode>`: first sense's judgment code (for the agree check).
- `<conf>`: first sense's confidence (echoed, not used in measurement).
- `<fA> <fB>`: pitchdisc f0 estimates (mHz) from the first sense; 0 for other
  tasks. These are measurements, not judgments; the existing gcheck already
  takes them as inputs.

**Per-task heavier measurement (frozen — wider window / different grouping,
raw G-span bytes only, disjoint from F):**

| Task | Current gcheck (frozen) | G5 second measurement (frozen) | Unchanged bar |
|------|------------------------|-------------------------------|---------------|
| colordisc (0) | y%16==0 rows only | ALL 64 rows; mean RGB per half (x<64 vs x>=64); dE2000 | class=(de>=2300); agree=(class==hh); strong=(\|de-2300\|>=400) |
| colorconst (1) | y%16==0 rows only | ALL 64 rows; von Kries distance | class=(dist>=150); agree; strong=(hh==1?dist>=160:dist<=100) |
| shapetrans (2) | grids (x+y)%12=={0,6} | grids (x+y)%12=={1,7} (disjoint sample points); same prototypes 974/684/464; same shape_measure | agree=(dir==hh); strong=(margin>=60 in agreeing direction) |
| pitchdisc (3) | 768-sample windows at ga, gb | 2048-sample windows at ga, ga+4096, gb, gb+4096 bytes (4x aperture); harmonic energy at fA/fB via goertzel; summed | agree: eA1*10>eA2*11 && eB1*10>eB2*11 (hh!=0), else both within 10%; strong: min ratio >=125% (hh!=0) |
| timbredisc (4) | single 2048-sample centroid at off=8 | centroids at FOUR 2048-sample windows (byte off 8, 8+16000, 8+32000, 8+48000); averaged | class=(avg>=900?RICH:BRIGHT); agree=(class==hh); strong=(\|avg-900\|>=80) |
| motiondir (5) | profile_motion step 16, frames 0->7 | profile_motion step 8 (denser), frames 0->7 | agree=(dir==hh); strong=(hh==0?mag<=1:mag>=5) |

**Emission (frozen):** `PASS <label>` iff the G measurement is valid (t1'==1)
AND agree'==1 AND strong'==1 under the task's existing bar above. Otherwise
`ABSTAIN` (no output change; the trial keeps its original prog).
`<label>` is the G measurement's own class label (equals the F verdict's label
when agree'==1).

**Abstention cases (frozen):** no G span (legacy harness fixtures) → ABSTAIN;
G span fails size checks → ABSTAIN; measurement invalid → ABSTAIN.
The second sense NEVER emits FAIL and NEVER alters already-PASS records.

**What counts as a conversion (frozen):** a trial in the 278 on which g5sense
emits `PASS <label>` with `<label>` == the trial's frozen truth label.
Wrong-label PASSes are counted and reported separately; they do NOT count as
conversions.

## 3. The 278 (frozen definition and retrievability)

**Definition:** trials in the frozen `case_r24_rk3.txt` with
`jcorrect==1 && conf>=700 && prog!=PASS` (prog: 0=PASS, 1=FAIL, 2=UNRESOLVED).
Verified 2026-09-24: exactly **278** trials (274 UNRESOLVED, 4 FAIL).

**Decomposition (frozen, verified):**
- (t1=0,agree=0,strong=0): 115 — legacy harness, no G span. UNCONVERTIBLE by
  any G-span sense. In denominator.
- (t1=1,agree=1,strong=0): 128 — convertible in principle.
- (t1=1,agree=0,strong=0): 31 — convertible in principle.
- (t1=1,agree=0,strong=1): 2 — convertible in principle (G strongly contra).
- (t1=1,agree=1,strong=1): 2 — seqs 2366, 2372; sense-level PASS,
  deliberation-blocked. The G5 trigger (sweep_prog != PASS) does NOT fire on
  these. UNCONVERTIBLE by a sense. In denominator.

**Maximum convertible by G5: 161.** The 85% bar needs 113; survival needs ≥100.

**Task split of the 278:** pitchdisc 215, colordisc 32, colorconst 26,
timbredisc 5, shapetrans 0, motiondir 0.

**Retrievability:** every trial's fixture is identified by (`task`, `fid`) from
the frozen `sweep.jsonl`. R24A fixtures live under
`round2/forks/R2-4/fixtures/`; legacy harness fixtures under `round2/fixtures/`
(component sources). The battery driver resolves each of the 278 to a readable
file before the formal runs; any unreadable fixture is logged as ABSTAIN
(missing), not imputed.

## 4. Battery (frozen)

All battery drivers are pure Zag. Glue (Python) may move bytes and join
tables but never scores.

**Leg 1 — Conversion (the 278):** run g5sense on each of the 278 with its
frozen (task, fid, jcode, conf, fA, fB). Count truth-agreeing PASS as
conversions: `C/278`. Report wrong-label PASSes separately (`W/278`).

**Leg 2 — Mint (sealed families):** rebuild the 288 `rt4_*` trials with the
frozen `v2/redteam/src/rt_trials.zag`; verify SHA-256 against the frozen
`v2/redteam/fixtures/sealed/TRIALS.sha256`. Today's rate from the frozen
`v2/redteam/evidence/rec_clean.records`: false-PASS = (prog==0 &&
judgment != truth), denominator 288. Verified 2026-09-24: **67/288 = 23.26%**.
Run g5sense on each sealed trial with its record (task, fixture, jcode, conf)
where triggered (conf>=700 && prog!=PASS). Count G5's new false-PASSes
(emitted PASS with label != truth): `G_new`. System rate with G5 =
(67 + G_new)/288. Kill bar (b): KILL iff (67 + G_new)/288 > 0.2326 + 0.02,
i.e. iff G_new >= 6.

**Leg 3 — Regression (full RK-3 replay):**
1. Reconstruct V2-D's 13-field record stream:
   `seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth|jG|confG`.
   Base fields from the frozen `sweep.jsonl` (sense-level prog).
   jG/confG: the frozen vsense (rebuilt from `round2/forks/R2-4/src/sense_r24.zag`,
   SHA cf4ffb43314650f1bba73b702c078475b8f32c755a99440f2f390c26d699a78e)
   run on the raw G-span bytes (extracted per the frozen R24A split) for every
   dual-span trial with F conf>=700; jG=-1/confG=0 otherwise (detector cannot
   fire there).
2. Build the frozen `v2/forks/V2-D/src/vgate_d.zag`; run on the records.
3. BASELINE VERIFICATION (must hold, else Leg 3 is VOID and reported as
   blocked): dispositions reproduce V2-D's committed metrics exactly —
   RK-3 = 975/1,102 = 88.48%, ACCEPT_INSTALL = 934, disposition SHA-256 =
   383b6e4f3b190bf4b3f54f1a313bcc1c8313d07831efce3b0ae554046406d9e9.
4. Run g5sense on every 11,840 trial with conf>=700 && sweep_prog!=PASS;
   collect the g5pass set (emitted PASS, any label).
5. Augment: prog 2/1 → 0 exactly where g5pass; re-run vgate_d → RK-3'.
6. Kill bar (c): KILL iff RK-3' < 88.48%.

**Leg 4 — Steel (6 timbredisc wrongs):** the frozen six
(seqs 10983, 10992, 11024, 11049, 11126, 11192; judgment RICH, truth BRIGHT,
conf 701-718, mrgF 353-382; all sweep_prog==PASS). FORCE-run g5sense on each
(trigger bypassed — this leg tests whether the second measurement has learned
the spoof features). Count re-emitted PASS: `S/6`. Kill bar (d): KILL iff
S >= 2, regardless of Leg 1.

**Determinism:** three complete runs of the full battery; every output file
SHA-256-compared across runs; all three must be byte-identical. Report the
three run SHAs.

## 5. Kill bars (frozen, mechanical)

Apply in order; any one KILL ends the hypothesis. No tuning, no rescue.

- (a) `C < 100` → KILL. (100-112: real but insufficient; 85% bar stands.)
- (b) `(67 + G_new)/288 > 0.2526` (i.e. `G_new >= 6`) → KILL.
- (c) `RK-3' < 88.48%` → KILL. (Leg 3 VOID → report blocked, not killed.)
- (d) `S >= 2` → KILL regardless of (a).

Verdict is SURVIVE only if all four pass.

## 6. Frozen inputs (SHAs verified 2026-09-24)

- `v2/diagnostics/case_r24_rk3.txt`:
  ea49515fbff14b280ea62d4e05015f71a310ae957680c767c6b46bc5e48cda42
- `v2/diagnostics/diagnose.zag`:
  2aed8371d2245b3c1ac2bef9251a2bb7dc30b25f64fdc7539824324dbcbd6243
- `round2/forks/R2-4/evidence/clean/sweep.jsonl`:
  4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2
- `round2/forks/R2-4/src/sense_r24.zag`:
  cf4ffb43314650f1bba73b702c078475b8f32c755a99440f2f390c26d699a78e
- `v2/forks/V2-D/src/vgate_d.zag`:
  3f3cdd3142d37076f32cdec0d54e923d6ad3dbf04bb235513378d5ddeaef08b7
- `v2/redteam/src/rt_trials.zag`: (SHA to be recorded at build)
- `v2/redteam/fixtures/sealed/TRIALS.sha256`: (frozen manifest)
- `v2/redteam/evidence/rec_clean.records`: 288 rows (frozen)
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 7. Laws

Pure Zag for the second sense and all battery drivers. Zero RNG. Three
byte-identical reruns with SHA comparison. This prereg is committed alone
before any G5 code or formal runs. Binaries, `.zagd`, `.zag-cache` are never
committed.
