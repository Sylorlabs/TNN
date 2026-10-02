# R33 N17 V92 native R27 V4 state-image qualification

This directory qualifies the already-authored R27 V4 native continuing-state image without changing canonical R27.

The lane is native Zag only. The build uses `/Users/Shared/micah/Documents/zag/znc`. No Python execution, pickle, NumPy, PyTorch, historical Python verifier, or foreign ML runtime participates in qualification.

## Scope

`state_image_qual_v92.zag` checks:

- exactly 33 learner sections and the exact 245472-byte V4 image size;
- every section's directory identity, contiguous offset, encoded size, header, element count, payload values, and encode/add/get round trip;
- semantic admission of both active-pending and inactive-pending images;
- all eight pending delayed-credit fields in order: active, cause trace event, action, entity, issued world step, due world step, observation sequence, update token;
- builder refusal for wrong image size, out-of-order section insertion, and incomplete finish;
- image truncation/overlength refusal and corruption of image header, directory entries, section headers, pending-credit validity, pending trace relation, pending entity relation, and restart semantics;
- checksum-bound learner-packet pack/check/extract identity, truncated-packet refusal, arbitrary learner-payload corruption refusal, and restoration after the corruption fixture.

The V4 image format deliberately provides structural/semantic validation while whole-payload corruption detection is supplied by the existing checksum-bound continuing-learner packet. V92 tests both layers rather than changing the V4 wire format and invalidating its admitted 245472-byte contract.

## Fresh frozen evidence (2026-09-15)

Current evidence: `FROZEN_20260915T173148Z_49937/`. Historical `BUILD`, `FRESH_PROCESS`, older harnesses and receipts are witnesses only, not fresh qualification evidence.

Exact launch from `/Users/Shared/micah/Documents/TNN/TNN`:

```sh
zsh Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL/run_v92_state_image_qual.zsh
```

Launch exit code: 0. `commands.txt` records each exact compiler/runtime command, working directory and redirection; `exit_codes.csv` records all 15 command exit codes (all 0). `SHA256SUMS` covers the copied compiler, complete local source import closure, runner, binary, all stdout/stderr, packet/image fixtures, sizes and receipts. The manifest excludes only itself.

The runner builds the frozen current source with `--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache` and invokes each mode as a separate process: `selftest`, `write`, `read`, `write-corrupt`, `read-corrupt`, `write-truncated`, `read-truncated`, `write-packet`, `read-packet`, `write-packet-corrupt`, `read-packet-corrupt`, `write-packet-truncated`, `read-packet-truncated`. The optional third argument routes fixture I/O into the new evidence runtime directory; existing fixtures are not overwritten.

Direct results: 339 selftest PASS records and `V92_STATE_IMAGE_QUAL_FAILURES,0`; valid fresh packet checks confirm exact length, packet integrity, semantic validation and byte identity with a newly constructed expected image. Corrupt and truncated readers report `packet_fresh_invalid_refused,PASS` and zero failures. Refusal-test exit 0 means expected rejection succeeded, not corrupt data admission. Image fixtures are 245472 bytes (truncated 245471); packet fixtures are 245536 bytes (truncated 245535). Selftest also proves that re-signing a tampered outer transaction leaves outer integrity valid while inner learner-packet integrity refuses it.

SHA-256 pins:

- Compiler: `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956` (before/after identical).
- Current harness: `26bd768b2871cc21a5dd6c8a6354fc27c3ba389a4522b896bc36f59ba427a451`.
- Binary: `50a52a7ea483f895c88fe5e92a7fcb5b5bf28bf74fb5a934e8c67dc9ab0c7b83`.

`state_image_qual_v92_baseline_probe.zag` is retained only as a compiler-regression witness and **excluded from final V92 qualification**. It was not compiled or executed in this campaign. The older continuing-life fresh-process supervisor was not run here; no claim about its fork/exec or torn-write campaign is made from these receipts.

## Claim boundary

V92 is an engineering qualification of the V4 state-image and persistence mechanics. It does not establish complete historical R27 behavioral projection, does not open `learn`, does not grant learner authority, does not create scientific exposure, and does not promote a successor.

No V4 implementation defect was found; directly supporting N17 sources were not edited. Only the qualification harness gained optional fixture-root routing, and the runner/README were updated. Top-level N17 `STATUS.json` was not edited. Canonical R27 was not opened for mutation; the canonical boundary remains step 60423 and newborn restarts 0. The tested state is a synthetic fixture with those values, not a fresh verification of the canonical payload. Historical behavioral projection, learner authority, scientific exposure and successor promotion remain excluded. No genuine in-scope qualification row is blocked.

## Final integrated closeout — 2026-09-15

Current fresh stable evidence: [Research/R33_FINAL_INTEGRATION_20260915T2145Z](../../R33_FINAL_INTEGRATION_20260915T2145Z/final_closeout.json).339 expanded selftest checks and all12 separate-process image/packet modes pass; exact245472/245536-byte contracts and corrupt/truncated refusal remain unchanged. Complete import sources, stable compiler/binary and stdout/stderr hashes are frozen there. The V92 runner remains the local native entry point above and allocates new physical rooted runtime paths.

The continuing-life bridge consumes this campaign's fresh packet root and independently checks both layers before publication. It passes atomic refusal, world/ingress/pending-credit/delayed-continuation/reload and learn-refusal65. V68/V73 original intended shapes now pass after explicit imported constant evaluation; stable compiler is preserved. N17 still has26 source-row blockers plus V91 actual native generator parity, and full lineage/fixture/admission/scientific prerequisites remain closed. Historical evidence is witness-only. Scientific exposure0; canonical mutation and learner authority false.
