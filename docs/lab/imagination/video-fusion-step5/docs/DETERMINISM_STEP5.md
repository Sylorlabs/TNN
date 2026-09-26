# Determinism Manifest — Step 5 (fuse4_E)

- Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
- Source: ~/workspace/video-fusion-v5/src/fusion4.zag (assembled from composer_base.zag + chunks/fz1..fz4 + chunks/v4a..v4e + main_tail.zag)
- Instruction: "merge the pig and the bunny together" (instr/merge.txt)
- Donor: ~/workspace/video-composer/runs/ingest_pig_A (24 frames)
- Recipient: ~/workspace/video-composer/runs/ingest_bunny_A (24 frames)

## Byte-identity (two runs: fuse4_E and fuse4_E2)

- All 24 frames: byte-identical across runs (cmp -s, all 24).
- Deliberation trace: byte-identical (cmp -s).
- Frame SHA-256 (aggregate): 9e8cfe648742d4d83b4d8e482607a96ccacbbd13d613bd40ae83395e422d5547
- Trace SHA-256: ab402c54a7a76788653db24f32c14a8af180bbe9e416e1d72993a455b5d4c544
- Frame 12 SHA-256: 3efa424e388d06f932b6c65ed9e928d8e5f063ab2a2fa46f83d4bb393f1ff930

## Guarantees

- Pure Zag (native binary, no external tools).
- Zero RNG in TNN decision paths (all selections by measured max/min).
- No timestamps, PIDs, or nondeterministic inputs in the trace or frames.
