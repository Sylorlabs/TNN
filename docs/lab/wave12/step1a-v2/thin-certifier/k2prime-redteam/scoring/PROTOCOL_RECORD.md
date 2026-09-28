# PROTOCOL RECORD — K2′ scoring run, 2026-09-20

## Certifier provenance

- Source: `thin-certifier/certifier/thincert.zag`
  sha256=`9b55fa2f158d98c31b4011c09f2f2a4394e740d9fa95450cad2ad5bdea9bbbd3`
  (matches the committed pre-amendment hash prefix `9b55fa2f…`).
- Built by the scorer at the start of the round with the frozen toolchain
  `toolchain/bin/znc_linux_x86_64_abed8aa1` → `/tmp/k2prime/certbuild/thincert_pinned`
  sha256=`d5e4de746a790b234726a3bcd5043bbfb7487fea203f7005e88b8c8012f2d3ca`
  (matches `BUILD_RECORD_THINCERT.md`). The frozen binary was copied and its
  hash re-verified before EVERY plant run (batch script aborts on mismatch —
  no mismatch occurred; the certifier was not modified during the round).
- The runner (`runner/run_thincert.sh`) also rebuilds `thincert` from source
  in the plant's scratch builddir and aborts (exit 3) if the rebuilt binary
  differs from the frozen binary — no exit 3 occurred in any of the 20 runs.
- Rule set: `PREREG_THIN_CERTIFIER.md` (frozen) + `AMENDMENT_2026-09-20_THINCERT_R3.md`
  (DRAFT — pending Micah approval; operative during this round: R3′, R1b, R4b).
  Attestations record both, plus `tripwire_v2` (informational; not a rule).

## Plant handling (fixed order 01–20)

- Each plant was copied unmodified from
  `thin-certifier/k2prime-redteam/plants/plantNN/` to scratch and built in
  the scratch copy only. Committed sources were never touched.
- `BIN variation.bin <sha256>` was appended to a working-copy
  `MANIFEST.work` in scratch; the working copy is committed here as evidence.
- Replay: the runner's interim 8-run matrix (same binary, fixtures state1
  × state2, MALLOC_PERTURB_ runs 3–4, TZ/ASAN/allocator runs 5–7) plus the
  phase-1 hardened N=8 deployment-condition matrix (per-run baked adversarial
  substrate tags 0–7, exec argv0 overrides on runs 2/5/7).
- Hardened harness adaptation (scripts committed here): the phase-1
  adversarial substrate (`replay-hardening/phase1/adv.zag`) replaces the
  plant's substrate; the plant's OWN `main` is the behavior under test, per
  the red-team harness contract (`CLASSIFICATION.md`: "test main calls
  entropy_mix"; all 20 plants share this contract). This mirrors the phase-1
  hardened driver faithfully (per-run baked tags, memory fill, env -i,
  argv0-exec matrix, 1MB state) except the print_hex final byte is not
  explicitly zeroed (template reads the unwritten byte — see scorecard note 5).
  A same-binary N=8 control was added for the argv0-isolated case
  (`k2_hardened_replay_fix.sh`), applied to plant 20.
- Plant 08: the hardened harness was deliberately not executed; the static
  gate (R6a) is the scored catch and the execution fault (8× SIGSEGV, exit
  139, in the interim matrix) is recorded as a harness problem, not a catch.
- Plant 15's hardened build fails (module calls `nio_clock()`, which exists
  only in its tampered substrate) — recorded N/A with the reason; the
  interim matrix (built on the plant's own tampered substrate) already
  demonstrated behavioral divergence.

## Commit hygiene

- This commit contains only text evidence: attestations, replay evidences,
  build logs, working-copy manifests, binary hashes, harness scripts,
  scorecard, and this record. No binaries, no `.zagd`, no `.zag-cache/`.
  (Verified by `find` before commit.)
- Binary hashes (`variation.bin.sha`) are included so any later party can
  rebuild and confirm byte-identical binaries from the committed plant sources.

## Resulting verdict

- 17/18 banned-idiom plants CAUGHT; plant 07 build failure (unscored);
  K2′ did not fire. 2 novel-class plants recorded for adjudication.
- Results are amendment-pending: no final K-bar is claimed until Micah
  approves `AMENDMENT_2026-09-20_THINCERT_R3.md`.
