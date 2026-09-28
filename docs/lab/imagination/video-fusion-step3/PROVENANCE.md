# Provenance

- **Bunny source**: 24 frames @ 320×240 from `~/workspace/video-repro/source/frames/`
  (the Step-2 test corpus; same frames as the Step-2 merge test).
- **Pig source**: 24 frames @ 320×240 from `~/workspace/video-combine/source/frames/`;
  per `video-combine/source/PROVENANCE.md`: CC BY 3.0 Wikimedia footage.
- **Memories**: pre-existing Step-2 deliberate-memory stores
  (`video-composer/runs/ingest_bunny_A/store.bin`,
  `video-composer/runs/ingest_pig_A/store.bin`) — reused, not re-ingested.
- **Code**: `src/composer_base.zag` is the Step-2 composer verbatim;
  `src/chunks/fz1–fz4.zag` is the new fusion organ; `src/build_fusion.sh`
  assembles and compiles with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- **Outputs**: `runs/fuse_A` (primary), `runs/fuse_B` (determinism rerun);
  `mp4/fuse_A.mp4` (24f, 8fps, 320×240, 3.0s); `metrics/SHA256_*.txt`.
- **Instruction**: `video-composer/instr/merge.txt` — "merge the pig and the
  bunny together" (the Step-2 test instruction, reused verbatim).
