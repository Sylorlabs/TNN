# Video Fusion Step 6: Neck-Anchored Warp

## Goal

Repair Step 5 white-box failure #2: the donor head was centroid-anchored
(sitting on the bunny's forehead/face). Step 6 maps the donor's measured
neck-cut point onto the recipient's measured neck line, so the head ATTACHES
at the neck instead of sitting centroid-on-face.

## What changed (from Step 5)

### Neck anchoring (the workstream)

- `src/chunks/v4c.zag` — `v4_warp` inverse mapping changed from
  `p = donor_centroid + Ainv*(q - slot_centroid)` to
  `p = donor_neck + Ainv*(q - recipient_neck)`.
  The anchor is now the neck joint on both sides.
- `src/chunks/v4c.zag` — `v4_slot` now also measures `neck_x` (x-centroid of
  the recipient subject pixels on the neck-line row). Slot info grew 32→40
  bytes (offsets: 0=neck row, 8=threshold, 16=head area, 24=neck x).
- `src/chunks/v4e.zag` — reads the recipient neck point `(neck_x, neck_row)`,
  computes the donor neck exactly from Step 5 landmark fields
  (`neck = dark_snout - d_neck*facing`), and maps donor neck → recipient neck.
  The upright test and all reference-mode warp calls use the neck anchor.

### Flip criterion corrected (found during this workstream)

Step 5's "upright" rule ("snout below = upright, nose-down grazing pose")
was BACKWARDS. A 180° flip inverts dorsal-ventral too. Verified from the
donor's ear (dorsal landmark, up-left of the head axis in the donor frame):
flip=0 maps the ear up-right (dorsal-up, upright); flip=1 maps it down-left
(dorsal-down, upside-down). Step 5 selected flip=1 — the upside-down flip.

The corrected criterion: the warped snout must lie on the HEAD side of the
recipient's neck line (above it, where the swapped head goes). For a 180°
flip pair, "snout above neck" and "dorsal up" select the same flip. This
selects flip=0, which puts the head in the head position AND is upright.

See `FLIP_CORRECTION.md` for the full dorsal analysis.

## Preserved from Step 5

- Two-direction facing (forward/backward facing deliberation)
- Measured neck cut (donor neck from dark snout − d_neck × facing)
- Whole-part enforcement (head must be one connected region)
- Identity-first transfer (donor pixels overwrite; transfer_kind=0)
- Cover mode (mode deliberation; selected anisotropic here, 61% coverage)
- Pure Zag, zero RNG, pinned compiler

## Build

```bash
cd src
bash build_fusion4.sh
# uses ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
# emits fusion4_bin (native, 0 external tools)
```

## Run

```bash
./fusion4_bin fuse4 <donor_dir> <recipient_dir> <instruction_file> <out_dir>
# donor:     ~/workspace/video-composer/runs/ingest_pig_A
# recipient: ~/workspace/video-composer/runs/ingest_bunny_A
# instruction: "merge the pig and the bunny together"
# out: 24 PPM frames (320x240) + trace_fuse4.txt
```

## Result

- 24/24 frames render, trace shows `RESULT: FUSION_COMPLETE`.
- Donor neck (119,76) → recipient neck (185,105). Exact anchor mapping.
- flip=0 selected by the corrected head-side rule (snout→(144,-9), above neck).
- Mode: anisotropic, 61% slot coverage (vs 2% for the upside-down flip=1).
- **Verdict: still a sticker.** The head is now attached at the neck, in the
  head position, upright — but it renders as an unreadable black blob (Step 5
  failure #3 persists) and the bunny's own head/face is still visible
  underneath (Step 5 failure #4 persists). See `VERDICT_STEP6.md`.

## Files

- `src/` — full source (chunks + assembled fusion4.zag + build script)
- `evidence/trace_fuse4.txt` — full deliberation trace from the verified run
- `evidence/instruction.txt` — the instruction used
- `VERDICT_STEP6.md` — honest visual verdict
- `DETERMINISM.md` — byte-identical rerun evidence
- `FLIP_CORRECTION.md` — the dorsal analysis that corrected the flip rule
