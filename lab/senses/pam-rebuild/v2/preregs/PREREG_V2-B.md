# PREREG V2-B — "interventional-port": pure-Zag port of R2-8 + R2-3 admission law

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Program:** PAMs v2 deep dive, Team 6 (v2 fork crew). Design target: ACCEPT TRUTHS.

## 1. Hypothesis under test

**V2-B — "intervention discriminates truth from spoof where passive gates can't."**
R2-8's interventional design (Grok-4.6's HC-6) showed strong safety in Python
orchestration (0.11% false installs, 99.5% high-conf wrong self-flag) but DIED
on the pure-Zag requirement (gate + ledger were Python). V2-B ports the
two-leg interventional program to pure Zag and pairs it with R2-3's
evidence-independence admission law as the install gate (ALIVE instrument):
the program must prove itself under intervention on the independent span, and
the gate withholds whenever the formation judgment disagrees with the
independent-span judgment. *What it tests:* whether the interventional
discriminator — executed natively, gated by the admission law rather than
R2-8's ultra-conservative INSTALL rule — keeps false installs at ~0% while
installing true judgments at a materially higher rate than R2-8's 0.3%.

**Predicted outcome (pre-registered):** the fork is HIGH-RISK; RK-3 is expected
to land well below 85% (the perturbation leg is strict by design) — probable
DEATH on RK-3. The hypothesis lives or dies on the preregistered ablation:
if the full two-leg program does not measurably reduce false installs vs the
admission-only ablation (≥0.2pp, R2-8's decider), the interventional leg adds
no safety and the hypothesis is falsified even if the safety bars pass.

## 2. What is built (pure Zag; Python only for glue/analysis/calibration)

- `src/vsense.zag` — R2-4's `sense_r24.zag` COPIED BYTE-IDENTICAL (SHA256 in
  evidence). Front-end frozen; the experiment varies the program/gate.
- `src/vgate_b.zag` — interventional program + admission gate + ledger:
  1. Per trial, reads vsense outputs for five spans: F (formation), G
     (independent holdout), P1..P3 (frozen perturbations of G, see §3).
  2. Program result: PASS iff (confG>=700) AND (every Pi FAILs cleanly), where
     FAIL_clean(Pi) = (j(Pi)!=jG) OR (|measureG-measurePi| > 3σ_task);
     else UNRESOLVED. (Pure-Zag port of R2-8's leg i + leg ii; the cross-span
     agreement check of R2-8's leg i is decomposed out — it lives in the
     admission law below, which is the load-bearing gate.)
  3. Install gate (R2-3's admission law): WITHHOLD iff jF!=jG; ADMIT iff
     jF==jG. INSTALL iff ADMIT AND program PASS.
  4. Memory-contract state: one permanent slot per task; a conflicting INSTALL
     vs a held permanent → CONFLICT_WITHHELD; agreeing → CORROBORATED.
     (Minimal slot so the contract is a memory contract; the INSTALL *decision*
     is the interventional+admission rule under test.)
  5. Ledger: sha256 hash chain, same construction as memgate.
- `src/deliberate.zag` — copied byte-identical (frozen); ratifies INSTALL
  escalations.
- `src/R33_NATIVE_IO_V1.zag`, `src/R33_NATIVE_SHA256_V2.zag` — byte-identical.
- Glue (Python): generate P1..P3 from G spans (frozen families §3, generator
  ledger committed); run vsense on F/G/P1..P3; calibrate 3σ_task on the harness
  NOISE split (§3); build records; run vgate_b; score bars.

## 3. Frozen perturbation families and 3σ calibration

Perturbations are deterministic byte transforms of the G span (no RNG anywhere):
- Images (colordisc, colorconst, shapetrans): P1 = channel-rotate
  (R,G,B)→(G,B,R); P2 = central-third horizontal stripe zeroed; P3 = XOR every
  payload byte with ((index*0x9E3779B9)>>16)&0xFF.
- Audio (pitchdisc, timbredisc): P1 = 1.2× pitch-shift by deterministic
  resampling; P2 = middle third of samples zeroed; P3 = XOR position mask
  (as images).
- Motion (motiondir): P1 = frame order reversed; P2 = central-third stripe
  zeroed; P3 = XOR position mask.
A truthful program is expected to react (judgment change or residual blowout);
a replaying/insensitive program will not — that is the discriminative signal.
Weak perturbations fail SAFE (UNRESOLVED → withhold), never unsafe.

3σ_task calibration (frozen BEFORE R2A evaluation): on the frozen harness
NOISE split (370 fixtures; used in no kill bar), per task,
3σ_task = max over noise fixtures and P∈{1,2,3} of |measure(f)−measure(P(f))|
in vsense's `measure` units. The threshold is the largest clean-data residual
ever observed; exceeding it means a detectable intervention. Frozen values
committed in `evidence/calibration_3sigma.json` before the battery runs.

## 4. Fixtures and trial plan (frozen, shared)

Same 11,840-trial battery and order as V2-A §3 (R2A 10,915 + harness 925).
Harness trials have no G span → program UNRESOLVED → WITHHELD (B1 accuracy
from F judgments is unaffected). No new fixtures except the P1..P3 derived
spans (generator ledger committed under `V2-B/evidence/`). No R2H.

## 5. Bars (frozen; applied mechanically)

- **RK-1**: false permanent installs / 11,840 ≤3%. (Permanent = INSTALL /
  CORROBORATED on the slot.)
- **RK-2**: wrong high-confidence percepts reaching permanent installation ≤1%.
- **RK-3**: correct high-confidence percepts reaching PASS-and-install ≥85%.
  (PASS = program PASS per §2; install = INSTALL/CORROBORATED.)
- **RK-5**: ≥90% of wrong high-conf percepts reach FAIL/UNRESOLVED over
  independent evidence (program result on the G span + perturbation legs).
- **B5**: false permanent installs on the adversarial battery ≤3%.
- **B6** (HARD KILL): 3 full runs byte-identical, ledger verified.
- **B1**: frozen-370 primary judgment accuracy ≥60%.
- Reported diagnostics: RK-4 (ablation installs ≥100), B4, and the
  preregistered **interventional-leg ablation**: admission-only gate (INSTALL
  iff jF==jG AND confF>=700 AND confG>=700, no perturbation leg) vs full gate;
  the full gate must reduce false installs by ≥0.2pp on the 11,840 trials or
  the interventional leg is declared non-load-bearing (hypothesis falsified).

## 6. Kill criteria

- Fail any of RK-1, RK-2, RK-3, RK-5, B5 → DEAD (deciding bar named).
- Fail B6 or B1 → DEAD (hard kills).
- Ablation fails (intervention adds <0.2pp safety) → hypothesis FALSIFIED
  (reported as the deciding finding even if bars pass).
- No retroactive bar changes. Amendments go to Micah.

## 7. Commit map

- This prereg: `senses/pam-rebuild/v2/preregs/PREREG_V2-B.md` (committed ALONE).
- Build: `senses/pam-rebuild/v2/forks/V2-B/`: PREREG copy, src/, evidence/
  (incl. perturbation generator + ledger, 3σ calibration), RUNLOG.md,
  VERDICT_V2-B.md.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths. No binaries, no `.zagd`.

**Laws:** pure Zag for mechanisms/learners/verification; Python only for
glue/analysis/calibration. Zero RNG in any decision path. Byte-identical
reruns required.
