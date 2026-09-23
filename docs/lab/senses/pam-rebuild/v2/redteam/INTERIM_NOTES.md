# PAMs v2 red-team — interim notes (Team 8b)

Date: 2026-09-23. Status: fixture verification COMPLETE, attack harness
built, sense sweep in progress. Nothing in this file exposes sealed fixture
contents — only family names, counts, and hashes.

## 1. Sealed generator and fixture set — VERIFIED

- Generator source: `senses/pam-rebuild/v2/redteam/src/rt_gen.zag` (pure Zag).
- Built with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` at
  2026-09-23 19:07 UTC; regeneration of all 12 families x 24 cases into a
  scratch dir reproduced the landed tree byte-for-byte:
  - generator manifest digest:
    `c140013e76c520e3e04ca2f3d4283f56a3e8184cbac01d4e5509ff5fb4f56b9d`
    (matches the expected digest exactly)
  - regenerated `MANIFEST.sha256` byte-identical to the landed manifest
  - full file-by-file comparison: **mismatches = 0**
- Counts: 288 fixture payloads + 288 `.truth` sidecars + 1 manifest =
  577 files, ~14 MiB total, 576 manifest rows.
- Truth distributions (from `.truth` sidecars, observed 2026-09-23 19:09 UTC):

| family | truth distribution |
|---|---|
| PTC-4 | HIGHER 11, LOWER 10, SAME 3 |
| PTC-5 | HIGHER 11, LOWER 13 |
| TMB-4 | BRIGHT 9, DARK 6, RICH 9 |
| TMB-5 | BRIGHT 12, DARK 12 |
| COL-4 | DIFFERENT 12, SAME 12 |
| COL-5 | DIFFERENT 12, SAME 12 |
| CCN-3 | DIFFERENT 12, SAME_SURFACE 12 |
| CCN-4 | DIFFERENT 13, SAME_SURFACE 11 |
| SHP-4 | CIRCLE 8, SQUARE 8, TRIANGLE 8 |
| SHP-5 | CIRCLE 11, SQUARE 3, TRIANGLE 10 |
| MOT-4 | E 2, N 3, NE 2, NW 3, S 4, SE 3, SW 4, W 3 |
| MOT-5 | E 5, S 4, STILL 13, W 2 |

- Sealed fixture dimensions: images 128x64 RGB or 96x96 RGB; audio 16,000 Hz /
  16,000 samples; video 8 frames of 64x64 RGB.
- Generator bug fixes applied before sealing (per handoff): odd coefficient
  911 + xor-fold in the pitch path, and MOT-4 comet-tail grounding.

## 2. Fork survey (corrected 2026-09-23 20:40 UTC — supersedes the
19:09-19:28 "B/C empty" note)

- **V2-A**: landed `vsense.zag` + `vgate_a.zag` + `deliberate.zag` +
  IO/SHA sources. `vsense.zag`/`deliberate.zag` byte-identical to frozen
  R2-4. Landed sense still fails to build (missing `lut.zag`,
  `gcheck.zag` imports). `vgate_a.zag` builds and ran gate-only tests.
  Independent G signal can REVISE_INSTALL only after a conflict with a
  permanent install.
- **V2-B**: populated — `vsense.zag`, `deliberate.zag`, `lut.zag`,
  `gcheck.zag`, IO/SHA sources. `vsense.zag` byte-identical to V2-A/R2-4
  and builds cleanly. **No gate source landed** — gate UNTESTABLE; sense
  performance characterized via the diagnostic build.
- **V2-C**: populated — `vknow.zag`, `memgate.zag`, `test_vknow.zag`,
  `lut.zag`, `gcheck.zag`, IO source. `memgate.zag` does NOT build
  (imports missing `R33_NATIVE_SHA256_V2.zag`) — gate UNTESTABLE.
  `test_vknow.zag` builds; `vknow.zag` detectors swept over all 288 sealed
  fixtures with a pure-Zag driver (`src/rt_vknow.zag`, built with V2-C's
  own SHA source temporarily vendored and then removed): **0 fires on all
  288 fixtures** — K-CCN-1 dimension-gated to 128x128 images, K-CCN-2 /
  K-PTC-1 / K-TMB-1 are unimplemented stubs returning 0, K-SHP-1's
  occlusion threshold met by none of the sealed shapes. V2-C's detector
  layer is blind to the novel set. Per-fixture detector-list digest:
  `ae8a506c47f8cff092a3bf97dc1c5af4710919b8fc4c395317eb346558f2711f`.
- **V2-D**: landed `vsense.zag` + `vgate_d.zag` + `deliberate.zag` +
  IO/SHA sources. Landed sense still fails to build (missing imports);
  `vgate_d.zag` builds and ran gate-only tests. D installs immediately
  when its independent signal fires (ACCEPT_INSTALL; no conflict
  adjudication, no prog requirement).
- A temporary diagnostic sense build (canonical R2-4 `lut.zag`/
  `gcheck.zag` vendored into a scratch dir — does NOT repair the landed
  forks) built cleanly at 19:28 UTC and ran all 576 dual-span sense runs
  with 0 failures. Diagnostic evidence only for A/D attack streams.
- Signal in both A/D gates: `jG == jF && confF >= 700 && confG >= 700`.
- Gate record format (13 fields):
  `seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth|jG|confG`

## 3. Sibling autopsy audits

### R2-4 RK-3 (recomputed 2026-09-23)
- Recomputed from frozen `evidence/clean/sweep.jsonl` +
  `evidence/clean/gate_dispositions.txt`: correct high-confidence
  denominator **1,102**, installed **104**. Exact match to the autopsy
  claim **104/1,102**. Instrument: STRONG — frozen evidence includes sweep
  rows, records, dispositions, ledger, deliberation log, metrics; autopsy
  additionally reports 0 mismatches across 11,840 replayed dispositions.

### R2-10 veto firings (observed 2026-09-23)
- `VERDICT_R2-10.md` claims the constitutional veto fired **58/76** grid
  candidates. No persisted grid-search output or candidate-level log exists
  in evidence — only `evidence/human/train/revise_input_truth.tsv` and the
  source implementation. Record as **NOT RECOMPUTABLE / prose-only**
  (same finding as Team 8). This is an evidence-retention failure, not
  evidence the number is false.

### KB4 channel autopsy mechanism demo (rebuilt 2026-09-23)
- Pure-Zag `src/mech_demo.zag` rebuilt and rerun: two new runs match each
  other and the recorded output exactly. Output SHA-256:
  `eccf38999d434878a865691b16ffc06c150d20c3ac4a4877b67d0936e6a429bd`
- Recomputed MI: C2 = 0.0000 bits, C3 = 0.0025 bits, C1 = 1.0000 bits.
- Instrument: adequate as a deterministic mechanism illustration; not by
  itself direct empirical proof for all channel-family claims (those rest on
  the separately cited frozen appeal evidence).

## 4. Dual-span attack design (in progress)

- Task mapping: COL->colordisc (tcode 0), CCN->colorconst (1),
  SHP->shapetrans (2), PTC->pitchdisc (3), TMB->timbredisc (4),
  MOT->motiondir (5).
- Trial wrapper (R24A, magic `0x41343252`): `u32le magic, u32le tcode`,
  then F payload (sealed fixture bytes), then G payload (disjoint holdout
  span: partner fixture(s) of the same family with the same truth label).
- Judgment-code maps (from frozen R2-4): colordisc SAME 0 / DIFFERENT 1;
  colorconst SAME_SURFACE 0 / DIFFERENT 1; shapetrans SQUARE 0 / TRIANGLE 1 /
  CIRCLE 2; pitchdisc SAME 0 / HIGHER 1 / LOWER 2; timbredisc PURE 0 /
  DARK 1 / RICH 2 / BRIGHT 3; motiondir STILL 0 / N 1 / NE 2 / E 3 / SE 4 /
  S 5 / SW 6 / W 7 / NW 8.
- Audio G-span subtlety: frozen `gcheck_pitch`/`gcheck_timbre` require G
  audio payloads with exactly 32,000 samples, but sealed audio fixtures are
  16,000 samples. The trial builder constructs the G pcm by concatenating
  the samples of TWO same-truth partners under a rebuilt header
  (sr=16000, n=32000) — deterministic, documented, and F/G evidence stays
  distinct (no byte duplication of F).
- Toolchain: all attack harnesses pure Zag (`src/rt_trials.zag`,
  `src/rt_records.zag`, `src/rt_score.zag`); Python used only for
  orchestration glue and analysis. Zero RNG anywhere; every stage prints a
  sha256 digest of its outputs and reruns are diffed byte-for-byte.
- Trial set digest (TRIALS.sha256): `319f45e3...` (full value in
  VERIFICATION.md). 288 trials x (trial + g-span file + truth sidecar)
  + manifest = 865 files.
- One generator bug was caught and fixed during bring-up: a truth-label
  off-by-one truncated "HIGHER" to "HIGHE" in trial truth sidecars
  (`tn-7` then double-stripped the newline; fixed to `tn-6`). Caught by a
  smoke test before any scoring ran; all trials regenerated after the fix.

## 5. Bar-gaming results (observed 2026-09-23)

Sense judgment accuracy on the novel families: 154/288 (53%). Only 44/288
trials reached prog=PASS & conf>=700 (PTC-4: 4, PTC-5: 4, TMB-5: 20,
COL-4: 16; zero in the other eight families).

Clean stream (288 trials):
- V2-A: installs=26 (16 correct, 10 false), withholds=147, suppressions=11,
  revise_installs=11, corroborations=65, negative_evidence=39. False installs
  in TMB-5 (4), MOT-4 (4), COL-4 (2).
- V2-D: installs=50 (37 correct, 13 false), withholds=141, suppressions=10,
  corroborations=49, negative_evidence=38. False installs in TMB-5 (8),
  MOT-4 (4), COL-4 (1).

withhold-everything (288 trials, prog forced UNRESOLVED / pred 0):
- V2-A: 0 installs, 288 withholds — PASSES. Its signal only revises
  already-permanent conflicting installs.
- V2-D: **43 installs (34 correct, 9 false), 245 withholds — FAILS.**
  ACCEPT_INSTALL fires on UNRESOLVED trials (rule has no prog check),
  bypassing all withhold logic. 20.9% of fired installs are false —
  against the in-source calibration claim of 0.6%.

install-nothing (44 prog=PASS & conf>=700 trials, corroborating pairs
adjacent):
- V2-A: 8 installs + 35 corroborations + 1 revise — PASSES (installs).
- V2-D: 34 installs + 8 corroborations — PASSES (installs).

decoy (44 install-stream records + 8 synthetic wrong-judgment decoys with
jG/confG spoofed to agree):
- V2-A: 23 installs (8 correct, 15 false), 13 REVISE_INSTALL — WEAKENED:
  spoofed G agreement revises permanent installs to wrong judgments.
- V2-D: 42 installs (23 correct, 19 false), 40 ACCEPT_INSTALL — WEAKENED:
  overwrites permanent slots with no conflict adjudication.

Ledger audit: all 8 ledgers hash-chain-valid (genesis 32 zero bytes,
sha256(prev_raw32 || canonical) per link); disposition counts match gate
stdout exactly.

## 6. Pending

1. ~~Finish the sense sweep~~ — done (576 runs, 0 failures).
2. Run the full attack pipeline twice — DONE (2026-09-23 20:31–20:41 UTC):
   run 2 byte-identical to run 1 across sense outputs, records, gate
   stdouts, ledgers, and scores.
3. ~~Inspect ledgers~~ — done, all valid.
4. Update INTERIM_NOTES.md / VERIFICATION.md — DONE.
5. Write REDTEAM_V2.md — DONE (digests finalized).
6. Commit harnesses + evidence + REDTEAM_V2.md — pending; commit 1 (sealed
   fixtures + generator + first-draft notes) still uploading.
