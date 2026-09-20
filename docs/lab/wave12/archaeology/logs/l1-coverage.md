## L1 — committed repo history (all 5 sylorlabs repos, full mirrors)
tool: git on bare --mirror clones at wave12/archaeology/repos/
note: mirror clones — reflog empty (expected), stash list n/a in bare repo (no work tree); fsck --lost-found clean for tnn (no dangling); rev-list --all --objects used for path mapping.

### tnn.git — COMPLETE
branches: main, reorg/phase-0-1, tnn-native-lab; tags: none; commits: 467; blobs: 13,442
path-filter log (pam/sens/vision/hearing/audio/percept/retina/cochlea/spectrogram, --full-history): 12 commits — hits are:
  - wave11 t7-senses protocol docs (the spec itself, not artifacts)
  - wave3/perceptual-origins/* (prior recovery effort, proven negative)
  - R32-era TTS PAM python scripts + .pt + TRAINING.log JSONs (later shadow research, synthetic TTS; see catalog PAM-ARC-005/006)
  - R33 native Zag sensor-trace runs (S0/S1 byte-ingress qualification; NOT PAM feature pipelines)
  - R33_B001_SENSORY_REVIEW.md + R33_SENSOR_QUALIFICATION_PLAN.md (qualification criteria docs; see catalog PAM-ARC-007)
blob content-grep (single-pass batch over 13,375 blobs <2MB; keywords: PAM percept retina cochlea spectrogram phoneme convolution 'feature map' 'edge detect' formant 'auditory cortex'): 320 hit blobs; mapped to 320 paths — all native-era research chatter (handoffs/journals/preregs), R27 results docs, R29/R32 python, R33 run snapshots. Keyword counts: PAM 947, percept 307, phoneme 157, convolution 66, feature map 10, formant 8, spectrogram 2, retina 2, cochlea 2, edge detect 1, auditory cortex 1.
commit-message grep: 1 hit (7fc67bfb 'Advance bounded P1/P2 language tools and perception research' — R50-R56 prereg JSONs, NO_GO experiments, already known).
CONCLUSION tnn.git: zero DESIGN-class hits. PAM-ARC-004/005/006/007 fragments only.

### zag.git — COMPLETE
branches: 19 (incl agent/*, codex/macos-arm64-v2, native-self-hosting-no-zig, zag-v2-machine-control, main) + PR refs; commits: 651; blobs: 3,562
path-filter hits: examples/sensor_pipeline.zag, audio_render.zag, embedded_sensor.zag (+ _bad variants) — Zag compiler examples, not TNN perceptual designs
blob content-grep: 93 hit blobs -> 3 distinct files: docs/V2_FINAL_VERIFICATION.md (formant, compiler doc), editors/vscode/package-lock.json (noise). ALL FALSE POSITIVES.
CONCLUSION zag.git: zero PAM-relevant content.

### ghost_engine.git — COMPLETE
refs: 35 (incl jules-*, agent-*, backup/*, main); commits: 264; blobs: 62,896
path-filter hits: src/invention/invent_sensors.zig (number-theory 'sensors' — false positive on *sens*), corpus_local_backup/cpython-* (false positives on *audio*/spam)
blob content-grep: 205 hit blobs; non-corpus paths: GUIDE_MATH.md, README.md, docs/*, ghost_sovereign/corpus/*, src/invention/*, src/vsa_core.zig, src/task_intent.zig, search/synthesis zig — all invention/VSA/number-theory content. ALL FALSE POSITIVES.
CONCLUSION ghost_engine.git: zero PAM-relevant content.

### ghost_cli.git — COMPLETE
refs: 1 (main); commits: 86; blobs: 486
path-filter: zero commits; blob content-grep: 0 hits.
CONCLUSION ghost_cli.git: zero PAM-relevant content.

### ghost_research.git — COMPLETE
branches: asi-intelligence, frontier-relational-spectral, main, master (4); PR refs incl pull/1; commits: 405; blobs <2MB: 4,877
path-filter log: 7 commits — hits: 07_agent_loop*/perception.zig + step1_perception_plan.txt (agent corpus-text ingestion — logged PAM-ARC-008), boundary_crossing/multi_sense.zig + multi_sense2.zig, docs/research/sense_genesis_round_w.md + sensorimotor_closure_round_af.md + results CSVs (Ghost Scientist sense-genesis/multi-sense research — logged PAM-ARC-009)
blob content-grep: 357 hit blobs; keyword breakdown: percept 287 (overwhelmingly "perceptron" in prose), convolution 33, phoneme 2. All mapped paths are Ghost Scientist agent-loop/invention-loop/perceptron content — zero TNN PAM relevance.
CONCLUSION ghost_research.git: zero TNN PAM-relevant content (separate program). Review docs of interest logged as PAM-ARC-008/009 non-candidates.
