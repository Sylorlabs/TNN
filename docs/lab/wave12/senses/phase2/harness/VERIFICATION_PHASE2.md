# VERIFICATION — Senses Phase 2 (cross-cutting harness + independent modality verification)

Date: 2026-09-20. Verifier: independent subagent (harness track).
Branch: `tnn-native-lab`.
Measuring instrument: `../PROPOSED_QUALBAR_SENSES_2026-09-20.md` — **PROPOSED,
UNSIGNED**. Nothing below is declared QUALIFIED. Verdicts read
"meets proposed bar" or "ENDORSED"/"DISCREPANCY-found" for the independent
reproduction. Only Micah can qualify a modality.

## Verdicts

| Scope | Result |
|---|---|
| §F replay (2 checks) | **meets proposed bar: 2/2** |
| §G static prohibitions (2 checks) | **meets proposed bar: 2/2** |
| §H 1,000-cycle churn (4 checks) | **meets proposed bar: 4/4** |
| §I save/reload (5 checks) | **meets proposed bar: 5/5** |
| 155-count aggregation (A32/B18/C20/D48/E24/F2/G2/H4/I5) | **155/155 MEETS-PROPOSED-BAR** |
| Audio track (independent verification) | **ENDORSED** |
| Vision track (independent verification) | **ENDORSED** |

## How the independent verification was done

For each modality, the verifier copied the **committed** sources to a scratch
tree (`/tmp/va_audio2`, `/tmp/va_vision`), compiled with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, ran the battery
twice from clean state, diffed the runs, ran the save/reload verify mode, and
checked every counted check name (from the sibling frozen preregs) for
presence, uniqueness, and actual==expected. Sources were read for real
mechanisms (non-vacuous checks), pure Zag, banned constructs, and
computed-strength; ingress diffs vs phase 1 were compared to the preregs'
declared deltas.

### Audio — ENDORSED

- Sources verified: `se2a_ingress.zag`, `se2a_memif.zag`, `se2a_main.zag` at
  remote commit `766a51c12d9a` (includes the per-pair save-dir fix).
- Independent build reproduces the worker's reported binary hash **exactly**:
  `7e6ca60f447ebf16164d5dae082da565a2224a565b9906d1a63c6c080302ec76`.
- Two full runs: rc=0, byte-identical stdout. Verify mode: 9/9 pass, rc=0.
- Counted checks: **71/71** (A16/B9/C10/D24/E12), each present exactly once,
  all actual==expected. 79 total CL_CHECK lines (8 supplemental setup/gate
  lines, uncounted).
- Ingress delta vs phase 1 is exactly the prereg's two declared deltas
  (`SE_MAX_PAYLOAD` 4096→16384; new `SE_BAD_RESERVED` -7110 with the
  reserved-bytes check). Memif diff vs phase 1 is only the `@import` rename
  (verbatim gate contract). Substrate hashes match phase 1 byte-for-byte.
- Static scans clean (K-SE5/K-SE6). Mechanisms reviewed: twin fixtures are
  real one-controlled-item pairs (sign flip, +1 LSB, adjacent swap, silence
  vs ±1 dither, …); the §D ok-condition requires admits sequential, recalls
  full-length, bytes differ AND provenance-sha256 differ, per-pair
  save/reload round-trip — non-vacuous.
- The worker's results doc honestly discloses the pre-fix §D save-dir bug
  (22/24 failing with sv1=-7109, shared `se2a_dstore` + O_EXCL). The verifier
  independently reproduced this failure signature on the pre-fix source
  before the fix commit landed — the checks are live, not canned.
- Kill bars K-SE1..K-SE8: all probed, none fired.

### Vision — ENDORSED

- Sources verified: `se_ingress.zag`, `se_memif.zag`, `se2v_main.zag`
  (committed; prereg frozen at `01977cfa92a6`).
- Independent build reproduces the worker's reported binary hash **exactly**:
  `90b49b4b4ac2449a01e45efbf5e49128b14582a1182a7ebd91e8673f1ebc2610`.
- Independent runs are **byte-identical** to the worker's committed
  `logs/run_harness_a.txt` / `run_harness_b.txt` (107 CL_CHECK lines, rc=0,
  empty replay diff reproduced).
- Counted checks: **71/71** (A16/B9/C10/D24/E12), each present exactly once,
  all actual==expected, all 107 names unique. (Cosmetic note: the 12 §E names
  carry a trailing NUL from a 16-byte name buffer — `se2v-e-frame-00\0` —
  names stay unique, checks unaffected; the reporter NUL-strips.)
- Ingress delta vs phase 1 is exactly the prereg's CHANGE-V2 list (payload
  4096→12288, SE_CAP 32→64, RGB envelope 1..64, channels/bitdepth header
  fields, reserved[36..48] zero-required). Memif is byte-identical to
  phase 1. Substrate hashes match phase 1 byte-for-byte.
- Static scans clean (K-SE5/K-SE6). Mechanisms reviewed: twins are real
  pixel manipulations (px-plus1, histogram-identical px-permute/px-chan-rotate,
  row-swap, …); the twin ok-condition requires bytes differ AND provenance
  differ; §C probes are behavioral (kill pinned→-7206, recall read-only via
  buffer mutation, freed-slot provenance). Non-vacuous.
- Kill bars: K-SE1..K-SE6, K-SE8 probed clean; K-SE7 n/a (no save mode in
  the vision harness — out of scope per its prereg; save/reload is covered
  cross-cutting in §I).

## Cross-cutting harness (§F–§I)

- §F: two builds → identical SHA256; two clean-state runs → byte-identical
  stdout (empty diff); both rc=0. 2/2.
- §G: whole-phase-2 static scan (harness + audio + vision mechanism sources):
  no RNG/wall-clock/threads/floats; strength caller-declared only (indexed
  writes are direct `<ident> as u8`, no observation-byte arithmetic in admit
  paths); bare `@import`s present. 2/2.
- §H: 1,000 deterministic OBSERVE/KILL cycles against a parallel
  expected-operation log; audit entry count equals operations issued;
  byte-for-byte audit comparison; silent-admission scan; fresh-store
  equivalence; eight exact refusal re-probes. 4/4.
- §I: save → fresh-process reload; records/slots/audit hashes byte-identical;
  twin distinction survives reload for 4 audio + 4 vision pairs. 5/5.
- Negative controls (all fired as designed): one flipped byte in persisted
  `memif.bin` → `se2i-slots` 0 (rc≠0), records/audit independently still
  passing; one flipped payload byte in a twin record → `se2i-records` and
  `se2i-audio-twins` 0 while slots/audit/vision-twins stay 1; reporter fed a
  corrupted check → 154/155 DOES-NOT-MEET with the exact FAIL line.

## §I fixture provenance (AMENDMENT-01, committed pre-implementation)

Per the assignment ("read their files, don't invent"), the §I twin pairs
reproduce **exact committed sibling fixtures**, verified byte-for-byte:

- Audio: the harness's admitted §I records (8..15) are **byte-identical** to
  the audio worker's own §D battery records (`se2a_d00`=d01, `se2a_d01`=d02,
  `se2a_d04`=d05, `se2a_d06`=d07 — 336 B records, compared from the worker's
  persisted per-pair stores).
- Vision: the harness's admitted §I records (16..23) are **byte-identical**
  to records built from the vision worker's committed fixture formulas
  (px-plus1, px-permute, row-swap, size-1x1-vs-2x2), via an independent probe
  using the vision ingress's `se_build`. (The vision CHANGE-V2 header fields
  channels=3@28 / bitdepth=8@32 are set post-build to match; the harness's
  vendored phase-1 ingress admits them — phase 1 has no reserved-byte check.)

## 155-count reporter

`count_phase2.sh <audio_log> <vision_log> <crosscut_logs...>` is
manifest-driven: `manifest_audio.tsv` / `manifest_vision.tsv` list the exact
71+71 counted names per sibling frozen prereg; F2/G2/H4/I5 are hardcoded.
Supplemental setup/gate lines are informational, never counted. Duplicate
identical lines count once; conflicting duplicates fail. A–E inputs are the
verifier's independent reproductions in `evidence/` (vision byte-identical
to the worker's committed logs; audio has no committed logs yet — the
reproduction used the committed fixed sources and reproduces the worker's
reported binary hash). Current output: **155/155 MEETS-PROPOSED-BAR**.

## Issues for Micah

1. **Audit capacity (MI_AUDIT_CAP 256 → 2048).** The cross-cutting harness
   vendors the phase-1 memif with one delta: the audit ledger 256 → 2048
   entries, because §H issues 1,990 audited operations and the 256-entry
   ledger silently stops recording, making "audit entries == operations
   issued" unprovable. No operation, refusal-code, gate, or slot semantic
   changed. Either the canonical audit ledger should be enlarged or the
   proposed bar amended — needs Micah's eyes.
2. **The proposed qual bar is unsigned.** Everything above reads
   "meets proposed bar", never qualified.
3. **No live devices.** All fixtures are deterministically authored encoded
   files; no microphone/camera qualified, no classifier admitted, no S2
   perception, no performance claims. Scope matches the preregs.
4. **Audio worker's logs/ not committed.** The audio track has a results doc
   and fixed sources committed, but no committed run logs yet; the 155-count
   uses the verifier's independent reproduction (which reproduces their
   reported binary hash exactly).

## Addendum 2026-09-20 — vendoring commit + full re-verification

- The vendored files missing from the remote harness tree (`VENDORING.md`,
  `se_ingress.zag`, `se_memif.zag`, `substrate/`) were committed as
  `694b1058868b37939ff95dbc6fe061053efb916d` (parent `e6e83706738b`).
  Remote tree verified complete: all 14 files/dirs present, no binaries,
  caches, or stores.
- Prereg `448e1e21` and amendment `fa01e4b9` verified as ancestors of the
  branch tip.
- Audio re-verified from committed sources: binary hash
  `7e6ca60f447ebf16164d5dae082da565a2224a565b9906d1a63c6c080302ec76`
  matches the reported hash; two clean runs rc=0, byte-identical replay,
  79/79 CL_CHECK actual==expected, 71/71 counted names present and passing,
  static scans clean.
- Vision re-verified from committed sources: binary hash
  `90b49b4b4ac2449a01e45efbf5e49128b14582a1182a7ebd91e8673f1ebc2610`
  matches the reported hash; two clean runs rc=0, byte-identical replay,
  output byte-identical to the worker's committed logs, 107/107
  actual==expected, 71/71 counted names present and passing, static scans
  clean. Vision memif is byte-identical to canonical phase 1 (`3bd7e2cd…`).
- Full harness runner re-executed from the complete tree: rc=0,
  **155/155 MEETS-PROPOSED-BAR**. Runner artifacts (binaries, store,
  caches) removed afterwards.
- Audio **ENDORSED**. Vision **ENDORSED**. Bar remains proposed/unsigned;
  nothing above is a qualification claim.
