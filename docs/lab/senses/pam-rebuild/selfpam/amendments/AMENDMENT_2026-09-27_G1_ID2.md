# Prereg amendment 2026-09-27-A — G1 registration: self-PAM candidate id 2

**Date:** 2026-09-27 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Amends:** `docs/lab/senses/pam-rebuild/selfpam/PREREG.md` §3.2;
`docs/lab/senses/pam-rebuild/round2/forks/R2-3/PREREG_R2-3.md` (registered-id set)
**Status:** Committed BEFORE any acceptance run under it (frozen-prereg
amendment rule, PREREG header). The acceptance runs follow in a later
commit; no run under this amendment exists at commit time.

## What changes

1. **PREREG §3.2 — candidate id fixed.** §3.2 planned registration of the
   self-PAM gate "as a candidate gate id in
   `round2/forks/R2-3/src/r2p_gates.zag`". The id is now concrete:
   **id 2 = `selfpam-fact-gate`** (formation span = draft-production
   context, src 0; gate span = independent re-measurement of the claim's
   subject, src 1). Judgment: the span's SPAN-SUM measurement quantized by
   the frozen FACT tolerance (starting bid 8, §8 item 3 open); the
   instrument withholds iff the two spans' judgments disagree.
2. **R2-3 instrument, `src/sense.zag` main.** Accepted `gate_id` range
   `0..1` → `0..2` (one-line range check plus the `gate_id:` comment).
   `gate_valid` remains the second check; both must pass.
3. **`src/r2p_gates.zag` — id-2 branches** in all five functions
   (`gate_name`, `gate_formation_src`, `gate_gate_src`, `gate_judge`,
   `gate_valid`), each delegating to `sp_gate_name` / `sp_gate_formation_src`
   / `sp_gate_gate_src` / `sp_gate_judge` / `sp_gate_valid` in
   `g1_candidate.zag`. The "Frozen ids" comment is updated to record id 2
   as registered under this amendment.
4. **Vendored sources.** `selfpam/src/g1_candidate.zag` and
   `selfpam/src/codec.zag` are copied **byte-identical** into
   `round2/forks/R2-3/src/` (SHA-256 recorded in the build record); the
   build additionally stages `R33_NATIVE_IO_V1.zag` +
   `R33_NATIVE_SHA256_V2.zag` from `selfpam/src/` (SHAs recorded) because
   znc resolves `@import` relative to CWD. A `build_g1.py` script in
   `R2-3/src/` assembles the build dir from these canonical sources and
   builds `sense_bin` with the pinned toolchain.

## What does NOT change

- **Ids 0/1 are untouched.** Their registration functions are not edited;
  regression is proven by rerunning ids 0/1 against the committed R2-3
  evidence (byte-identical reports/ledgers required).
- **The 1,200-pair corpus is untouched.** `round2/fixtures/r2p/`, verified
  against `MANIFEST.r2p.sha256` before every run. No new corpus, no
  reseeding.
- **§8 blockers: ALL REMAIN OPEN.** KB thresholds unsigned; probe charter,
  FACT tolerance table, marked-emission format, corpus manifests — none
  signed. This amendment authorizes the instrument change and the
  registration acceptance runs only.
- **CELL-A counting: NOT claimed.** Per PREREG §5.5 ("a measurement run
  against unsigned thresholds does not count"), the id-2 acceptance runs
  are **registration acceptance** — instrument-wiring verification — and do
  not count as CELL-A. The counting decision is deferred to Micah's §8
  sign-off. The 90% withhold bar is run as stated in PREREG §3.2 (starting
  bid; sign-off open per `G1_REGISTRATION.md`).
- **DEMO_ONLY scope: unchanged.** This registration puts the gate behind
  an admission instrument; it does not put it on a live TNN decision path
  (B1 open), does not clear the CC1 guard (B2, DEPLOY BLOCKER), does not
  build the write-once evidence partition (B4), and does not enact the
  channel-key ceremony (B5 — design only, companion document).
- **Install path: nothing changes.** G1 stays withhold-only. No install
  disposition is reachable through this registration.
- **The `sp_gate_*` implementations are frozen as vendored.** Any future
  change to `g1_candidate.zag` semantics needs its own amendment.

## Acceptance protocol (runs after this amendment commits)

- ×3 runs of `sense_bin 2` on the 1,200 pairs; reports and ledgers
  byte-identical across runs; hash chains verified with
  `R2-3/src/mirror/verify_ledger.py`.
- Regression: `sense_bin 0` and `sense_bin 1` rerun; outputs
  byte-identical to the committed evidence
  (`evidence/admission_report_reference_r1..r3.txt`,
  `evidence/ledger_reference_r1..r3.txt`,
  `evidence/admission_report_broken.txt`, `evidence/ledger_broken.txt`).
- Bars: B5 `pairs_withheld/1200 >= 90%` (starting bid); **kill: any pass
  with `overlap_pairs > 0` voids the instrument run**; B4 positive control
  id 1 must show 100% overlap and < 50% withhold, else the run is void.
- Evidence lands in `round2/forks/R2-3/evidence/` as
  `admission_report_selfpam_r{1,2,3}.txt`,
  `ledger_selfpam_r{1,2,3}.txt`, plus `BUILD_RECORD_G1_ID2.md`, with
  `LEDGER.md` appended. Binaries are never committed.

## Rationale

`G1_REGISTRATION.md` documented this exact patch as "planned, not applied"
and `DEMO_ONLY.md` §3 lists it as such. Applying it under a committed
amendment — before any run — is the lawful path per the frozen-prereg
amendment rule. The registration is wiring verification, not a verdict on
the candidate: whether id 2 clears the bar is the instrument's
measurement, and whether that measurement counts is Micah's §8 call.
