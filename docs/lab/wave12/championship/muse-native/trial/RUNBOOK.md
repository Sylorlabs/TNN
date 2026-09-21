# MUSE-NATIVE Runbook — Championship Classes 3 & 4

## Status (2026-09-21 ~20:10 UTC)
- Gate: 0/40 raw batch files (watcher `proc_a6280286b04d` polling every 90s).
- All preparation COMPLETE. Drivers written, uncompiled (gate prohibits
  compile/run before DATA commit).

## File inventory (all under ~/workspace/championship/muse_team/)
- `freeze_corpus.py` — mechanical freeze (imports Q2 parser). NOTE: add
  `"retries": []` to meta before running (structure must mirror Q2).
- `gate_watch.sh` — polls raw/ every 90s.
- `tnn/build_gen.py` — generates `muse_corpus.zag` from frozen corpus.
  Usage: `python3 build_gen.py <output-path>` (one per leg src/).
- `tnn/shared/muse_teach.zag` — D2 teaching library (static).
- `tnn/legA/src/muse_trial.zag` — Track 5 M2 arm (mechanical port).
- `tnn/legA/analysis/analyze_m2.py` — M2 metrics + integrity gate.
- `tnn/legB/src/muse_b7_direct.zag` — class-4 direct §B.7 (tid=20).
- `tnn/legC/src/muse_teacher_leg.zag` — class-3 teacher leg (tid=21).
- Leg B/C src: Q1 machinery + MUSE-CLASS tid deltas (documented in files).

## When the 40 files land
1. `cd ~/workspace/championship/muse_team && python3 freeze_corpus.py`
   (add `"retries": []` to meta first). Verify 240/240 parse, 0 failures.
2. Record corpus SHA256 + per-file SHA256SUMS.
3. Faithfulness inventory (mechanical):
   - 5 buckets (faithful/contradicted-with-flag/unresolved-but-flagged/
     unresolved-unflagged/false-claim) using t5_plant_claim as reference.
   - DISTRACT_VALUE != OBS_VALUE for all 240.
   - Integers in OBS_TEXT/PROBE_TEXT/DISTRACT_TEXT agree with fields.
   - OBS_VALUE vs PROBE_VALUE agreement.
   - Classify each false id {3,29,55,71,80,103,117,139,163,178,205,231}:
     reproduce vs flag/correct.
4. Commit DATA to `sylorlabs/TNN`, branch `tnn-native-lab`:
   - Mirror under `~/workspace/tnn-lab/wave12/championship/muse-native/corpus/`
     (40 raw + SHA256SUMS.txt + corpus.json + SHA256.txt).
   - Message: `DATA: muse-native frozen corpus (240 facts, <sha>)`.
   - Verify commit/tree on tnn-native-lab.
5. Generate: `python3 tnn/build_gen.py tnn/legA/src/muse_corpus.zag`,
   then copy to `tnn/legB/src/` and `tnn/legC/src/`.
   (Or run build_gen 3x with different outputs.)
6. Compile legs with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
   - Leg A: main is muse_trial.zag. NOTE: it still has the `_zag_argc()` gate
     from Q2 — REMOVE it (argc=0 always; read _zag_arg unconditionally).
     Actually check: the port kept Q2's main. Must fix before running.
   - Leg B: main is muse_b7_direct.zag (no args).
   - Leg C: main is muse_teacher_leg.zag (no args).
7. N=5 byte-identical runs per leg. Diff outputs.
8. Leg A: `python3 tnn/legA/analysis/analyze_m2.py` → Track 5 composite.
9. Cross-check: MUSEB_TEACH_DIGEST == MUSEC_TEACH_DIGEST.
10. Static no-RNG scan on all .zag sources.
11. Verdict doc + append to `~/workspace/NIGHT_RUN_2026-09-21.md`.
12. Commit evidence/source/docs (no binaries).

## Design decisions (documented)
- Leg A M2 = Q2 D2 route, 12 reps, held-outs (proper Track 5 metrics).
- Leg B/C teaching = D2 route, rep-0 order, NO held-outs (teacher must hold
  full curriculum). 228-id overlap digest-verified vs leg A rep 0.
- Teacher id 21 (20s range). Direct probe id 20. Frozen §P wire unchanged.
- Leg C: teacher's store gates clean emissions (t5_slot_find); flaws are the
  teacher-administered exam. Fresh learner follows Q1 pattern exactly.
- Class-4 composite = leg A Track 5 (30/25/25/10/10) + leg B §B.7 direct.
- Class-3 = leg C §B.7 (fresh learner taught by M2) + Track 5 on fresh learner
  (if time; the §B.7 is the required score).

## Known issues / TODOs
- `muse_trial.zag` main() still has Q2's `_zag_argc()` gate — must remove
  before running (ZNC-2026-09-21-007).
- The 40 files have NOT arrived (0/40 as of 20:10 UTC, 70+ min). Producers
  may be blocked. ESCALATE to parent if not landed by 21:00 UTC.
