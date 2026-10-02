# Step 6 Determinism: Byte-Identical Reruns

## Method

Two full runs from clean output directories, same binary, same inputs.
Pure Zag, zero RNG.

- Run A: `~/workspace/video-fusion-step6/runs/fuse6_A/`
- Run B: `~/workspace/video-fusion-step6/runs/fuse6_B/`
- Donor: `~/workspace/video-composer/runs/ingest_pig_A`
- Recipient: `~/workspace/video-composer/runs/ingest_bunny_A`
- Instruction: "merge the pig and the bunny together"
- Binary: `fusion4_bin` (512,050 bytes, built by pinned
  `znc_linux_x86_64_abed8aa1`, 0 external tools)

## Results

| Artifact                | Run A                | Run B                | Match |
|-------------------------|----------------------|----------------------|-------|
| frame_00.ppm … frame_23.ppm (24 frames) | — | — | BYTE-IDENTICAL (all 24) |
| Aggregate frame SHA-256 | 0ae668bf4b1bff43b6e2ab30536fabe2c010c6dd28ada0ad9367d35da41704a0 | (same) | YES |
| trace_fuse4.txt SHA-256 | 8f4bf5b63231f24a088ce7f1e651f025e9eb14b408b0596d90e550a30a7061b4 | (same) | YES |

All 24 frames compared with `cmp`: zero differences.
Traces compared with `cmp`: identical.

## Trace key values (both runs)

- `donor_neck=(119,76)`, `recipient_neck=(185,105)`
- `flip=0 snout->(144,-9) headside=1`
- `flip=1 snout->(225,219) headside=0`
- `flip_selected=0`
- `mode_selected=anisotropic cov_x1024=627` (61%)
- `transfer_kind=0` (identity-first)
- `RESULT: FUSION_COMPLETE`
- Valid donor anatomy frames: 10

## Note on run times

Run A took ~160s, Run B ~65s (system variance). The outputs are
byte-identical, proving the time difference is environmental, not
algorithmic. Zero RNG; the pipeline is fully deterministic.
