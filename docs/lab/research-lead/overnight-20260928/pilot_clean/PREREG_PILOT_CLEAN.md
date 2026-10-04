# PREREG: H-NEW-3 Pilot Clean Re-wave

Status: PREREG. Frozen before any re-wave run. No builds executed.
Baseline: `fed72668c` (PILOT-FAIL, F-PYTHON fired; wave void).
Prior prereg: `76878a918` (PREREG_PILOT.md) + `f77e733f5` (amendment).
Date: 2026-09-30 UTC.
Worker: H-NEW-3 Pilot Clean Re-wave Worker.

## 1. Purpose

The v1 pilot wave (fed72668c) implemented the full H-NEW-3
continuing-learner integration protocol, debugged two harness bugs,
and produced exploratory measurements in which every frozen floor
held and no falsifier except F-PYTHON fired. The wave was voided
solely because the implementer invoked Python once for a mechanical
regex text transformation. This clean re-wave replays the identical
build and run protocol with zero Python at any stage. No redesign,
no workload change, no floor change, no falsifier change.

## 2. Baseline adoption

The implementation is adopted verbatim from the baseline commit:

- Source: `docs/lab/research-lead/overnight-20260928/pilot_impl/pilot.zag`
  at `fed72668c` (833 lines, []u8 workspace with w_get/w_set
  accessors, MODE_PH placeholder).
- Build script: `docs/lab/research-lead/overnight-20260928/pilot_impl/BUILD.sh`
  at `fed72668c` (shell only; sed MODE injection; znc compile).
- Both adopted byte-for-byte into `pilot_clean/` for a
  self-contained re-wave directory. Any difference found between
  the adopted files and the baseline bytes before the first build
  voids this re-wave.

The two v1 harness bugs (B1 mode-4 prerequisite, B2 p2_transfer
finalize) were already fixed in the baseline source and remain
fixed. The []u8 + w_get/w_set pattern (124 accessor sites) replaces
the unreliable []i32-from-malloc pattern, per the baseline
toolchain finding.

## 3. Frozen protocol (transferred from 76878a918 + f77e733f5)

All eight sections transfer verbatim. Summary of frozen content:

- Five experiences in one process (Arm A, mode 0): E1 vocabulary
  (48 teach episodes + 16 composition episodes; P1 16 items),
  E2 concepts (4 domains, schema + exception masks; P2 a/b/c and
  transfer gate), E3 procedure invention (baseline form-inventor,
  residual candidates, greedy gain, promotion IF_LT t=13,
  verification halving), E4 conflicting evidence (flag latency,
  exactly one HEDGE, one re-observation, RESTORED), E5 delayed
  reuse (condition R retrieve form kind+param, refit by bisection;
  condition F masked full pipeline).
- Arm B: modes 1..5 from the same source via MODE injection.
- Immediate floors F-E1..F-E4x, delayed floors F-D1/F-D2/F-D4/F-D5,
  relative floors F-REL-P1/P2/P4, capacity F-CAP, all with the
  exact bars frozen in the prior prereg (unchanged; not restated
  here to avoid transcription drift; the frozen text in
  PREREG_PILOT.md + PREREG_AMEND1.md governs).
- Falsifiers F-INTERFERE, F-CORRUPT, F-REUSE-FAIL, F-FLOOR,
  F-LABEL, F-NONDET, F-PYTHON, transferred verbatim.
- Disclosures D1 (channel tags), partitioned regions,
  scope limits, unchanged.

## 4. Re-wave procedure

1. Adopt `pilot.zag` and `BUILD.sh` from `fed72668c` into
   `pilot_clean/`. Byte-verify against the baseline with sha256.
2. Run BUILD.sh (shell only). Six binaries: pilot_m0..m5.
3. Run each mode 3 times; capture stdout; record md5 of each run.
4. Judge every floor and falsifier exactly as the baseline result
   report did, against the same frozen bars.

No source edits are permitted during this re-wave. If a build
fails or a floor breaches, the re-wave reports the observed
outcome; no mid-wave patching.

## 5. Kill bars (clean re-wave)

- K1: this prereg committed strictly before any re-wave build.
  (Self-check at report time.)
- K2: Mode 0 runs E1..E5 in one process, no resets, no
  recompilation between experiences, D1 discipline held
  (F-LABEL silent).
- K3: all floors in section 3 hold (immediate, delayed,
  relative, capacity).
- K4: pure Zag at every stage (compile, run, verify, byte
  checks via shell only); 3/3 byte-identical per mode; zero
  em-dash bytes; canaries intact (F-CORRUPT silent).
- K5: Arm B modes 1..5 run and compared per the frozen Arm B
  section.

Builder verdict: PILOT-CLEAN-PASS (K1..K5 hold, no falsifier
fired) or PILOT-CLEAN-FAIL (naming the fired falsifier and
breached floor). Per-floor results reported even on pass.

## 6. Expected values (from baseline exploratory runs; not bars)

For protocol sanity only; floors and falsifiers govern. Baseline
observed: P1 16/16, P2b 4/4, E3 fit 12/12 with t=13 promoted and
halving 6/6, E4 latency 0 with exactly one hedge and one reobs,
E5 reuse 6 interventions vs 12 fresh, delayed probes all intact,
canaries 5/5, state 1200 bytes. Baseline stdout md5s (run 1):
mode 0: b301d100df41656e58cfc531c0d82c49
mode 1: 7d33987a19dbf2079bd27917742d4530
mode 2: 95a15999c05f7ac2246b0ef2bdd8394e
mode 3: 3f0238a842bc30e02958a8c9d15b4eeb
mode 4: d8d948cb38707394b52cbdefab2c0c90
mode 5: 4407c9763589332a8ca3d19af34e87dc

Identical md5s would confirm a faithful replay; differing md5s
are not a failure (nondeterminism would be, per F-NONDET;
changed bytes are judged by floors).

## 7. Prereg self-check

- [x] Frozen protocol transferred verbatim (section 3).
- [x] Baseline cited with commit hash (section 2).
- [x] Floors not restated (avoids transcription drift).
- [x] No builds executed before this commit.
- [x] Zero em-dash bytes (shell-verified before commit).
- [x] No Python at any stage of prereg preparation.

Builder label: PREREG-COMPLETE (pending commit).
