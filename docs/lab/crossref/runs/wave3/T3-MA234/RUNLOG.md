# T3-MA234 RUNLOG — crossref crew
## Step 1 — frozen prereg verification
- Prereg file: ~/workspace/tnn-lab/crossref/PREREG_TIER3.md
- sha256: 538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1
- Section "## T3-MA234 — MA2 falsified, MA3 mixed, MA4 answered" extracted via grep+sed (grep hit line 14)
- tnn-native-lab branch head (GitHub API, 2026-09-24): 16400e32cdcdbc519a9bdce2277f192a5c57d0a9
## Step 2 — section orientation
Section "## T3-MA234 — MA2 falsified, MA3 mixed, MA4 answered" read from the file (authority):
- MA2 FALSIFIED 32/32 — staged training vs gifted full power gave identical refusal profiles (stages dropped as restraint-training, kept only as destruction firewall during early training).
- MA3 MIXED — deliberate memory agency crushes the standard curriculum (30/30 vs 0–12 held) but loses the adversarial one (cannot express negative judgments about memories).
- MA4 ANSWERED — signed memory values: 18/18, 30 vs 9 on the adversarial curriculum.
- Verdict commit = code state.
- Prereg blob on tnn-native-lab (docs/lab/crossref/PREREG_TIER3.md, blob 943ab5c984cd16b4a618bbc94329780b2d425a68) sha256 == local file sha256 (538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1). MATCH — proceeding.
## Step 3a — verdict commits (API + git)
- MA2/MA3 verdict commit: 624f6e33c141 (2026-09-19, "lab(wave2): MA2 falsified (staging != restraint), MA3 mixed") — resolves on tnn-native-lab; TRIAL_RESULTS_MA2/Ma3 blob SHAs verified via tree descent.
- MA4 verdict commit: 6dc7fcd0c379 (2026-09-20, "lab(wave3): 20 post-toy investigations ...") — resolves; TRIAL_RESULTS_MA4.MD blob verified.
- Damage/repair: 308bf365 (2026-09-23 bad surgery) damaged both; 3b011ef18e0a restored. Verified byte-identical restore: ma2_trial.zag b59ddcb274f9, ma3_trial.zag 1e6a645c2b1c, ma_common.zag 58e90e7b392e, memory_core.zag 90c8777b57b2, run_ma2/3.sh SHAs all equal between verdict commit 624f6e33c141 and branch head. MA4: ma4_trial.zag d7764197db2e, run_ma4.sh 57d97b8cbf14 equal between 6dc7fcd0c379 and head. Substrate tree 6dc76e02461d identical in both locations.
- Branch head moved during work: was 16400e32cd at prereg check; clone fetched 8eb94a4cbe9665a43beed1061867dce91bcb0da4 (new commits landed while cloning).
- Clean checkout: git clone --filter=blob:none --sparse of Sylorlabs/TNN, sparse-checkout docs/lab/wave2/memoryagency + docs/lab/wave3/signed-memory-values, checked out tnn-native-lab; all 8 trial blobs re-hashed locally (git hash-object) and match the verdict-commit SHAs above.
## Step 3b — spot reruns (committed sources, clean checkout)
- Compiled ma2_trial.zag and ma4_trial.zag with the pinned znc (both exit 0). Binaries kept in work/ scratch only, never committed.
- MA2: 2 runs, exit 0, stdout byte-identical (sha256 584ee02dec4b542f3310bcf99ad8659a9ee356eb5f336c27a8206de2359908c7). 5/5 CL_CHECK pass; MA2_STAGED == MA2_GIFTED on (rate_per100=0, pinret=195/195, replay=0, kills_total=3); unlock step 162 deterministic; MA2_VERDICT=FALSIFY_IDENTICAL_DROP_STAGES.
- MA4: 2 runs, exit 0, stdout byte-identical (sha256 a1d86dd2b4931f2d339f1b32bf2904b8619195e7b23d2ff2654669a6757f6b32). 18/18 CL_CHECK pass; MA4_FAILURES=0; MA4_VERDICT=CONFIRM_SIGNED_SUPERIOR. Adversarial cells: BASE 9/9/9 held vs SIGNED 30/30/30 (30-vs-9 reproduced). Standard: 30/30 vs 30 held (non-inferior). Static no-RNG grep passes.
- Ancestor checks: both verdict commits are ancestors of checkout HEAD 8eb94a4c.
- Verdict: SPOT-REPRODUCED.
