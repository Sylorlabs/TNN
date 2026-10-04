## L2 — workspace sweep (complete)
cmd: find tnn-lab/history tnn-lab/brain workspace/user your_files -iname name-patterns (pam/sens/vision/hearing/audio/percept/retina/cochlea/spectrogram/phoneme)
result: zero filename hits
cmd: find ~/workspace -iname *.pt/*.pth/*.onnx/*.npz
result: zero hits
cmd: grep -rliE PAM|perceptual|retina|cochlea|spectrogram|phoneme|formant|auditory cortex|edge detect|feature map --include=*.md/*.txt over tnn-lab/history tnn-lab/brain t7-senses your_files user
results:
  - tnn-lab/brain/STATE_SCHEMA.md §7-8: names PAM organs (visual_pam, audio_pam, speech_pam, speech_core_pam, speech_noise_pam) and documents 76 torch Parameters (32 Conv1d, 32 Linear, 8 GRU, 2 Embedding, 2 LayerNorm) inside ConvWordNet x4, EntityHeadNet, RawConvSpeechPAM x2, speech/video PAMs; provenance explicitly undocumented (open question #2)
  - tnn-lab/wave3/perceptual-origins/: prior recovery effort (see ORIGINS.md/RECOVERY_SPEC.md/NATIVE_PERCEPTION.md) — proven-negative search; not new evidence
  - wave11/t7-senses/findings/*.md: the protocol and requalification specs themselves — not artifacts
  - your_files/tnn-research-review.md: one passing mention of phoneme boundaries (review doc, not PAM design)
cmd: find . -maxdepth 6 -iname *pam*/*percept*/*retina*/*cochlea*/*spectrogram*/*phoneme* (excl repos/.git/node_modules)
result: only ./tnn-lab/wave3/perceptual-origins (+ t7-senses protocol docs, excluded)
cmd: find . -maxdepth 4 -iname *.pdf -> zero; wave*/ dir listing inventory complete
cmd: grep -rliE PAM|percept|retina|cochlea|spectrogram|phoneme|formant|auditory cortex|edge detect|feature map across tnn-lab/wave1..wave11 (all file types, excl t7-senses, repos)
result: 28 files — reviewed; all incidental mentions (prereg/trial-result prose, ht2_learner.zag, felt-rebuild script) or prior recovery docs (wave3/perceptual-origins, wave3/recovery/RECOVERY_DIG.md). None contain a PAM pipeline design.
cmd: grep -rliE (code file types: *.py *.zag *.json) over tnn-lab/brain tnn-lab/history user your_files -> zero hits
