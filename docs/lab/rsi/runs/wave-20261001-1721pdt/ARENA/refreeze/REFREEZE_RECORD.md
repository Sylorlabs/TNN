# REFREEZE RECORD: Arena v6 (wave-20261001-1721pdt, ARENA lane)

Date: 2026-10-01 PDT
Worker: ARENA lane replacement worker (no child subagents)
Prereg: docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/PREREG_LANGUAGE.md
  + PREREG_LANGUAGE_AMEND1.md (frozen; NOT modified by this worker)
Parent result being refrozen: v6 candidate 0.794 (54/68), C16 1.000 (6/6),
  8/8 bars PASS under the amended prereg (wave-20261001-1421pdt/arena_igl/).

## 1. Records located

- v6 prereg (as amended): arena_igl/PREREG_LANGUAGE.md,
  arena_igl/PREREG_LANGUAGE_AMEND1.md (1421pdt lane).
- v6 contestant source: arena_igl/devint1_contestant_v6.zag (copied byte-identical
  to this lane as refreeze/devint1_contestant_v6.zag).
- v6 re-frozen binary: arena_igl/sealed/bin/v6 (built 2026-10-01 21:38 PDT).
- 3 fresh sealed runs under amended prereg: arena_igl/sealed/run2, run3, run4.
- v4 0.676 baseline: docs/lab/research-lead/overnight-20260928/arena_conflict/
  ARENA_CONFLICT_REPORT.md (46/68) + devint1_contestant_v4.zag.

## 2. Binary identity verification (recomputed by this worker)

| Artifact | SHA-256 | Matches canonical |
|---|---|---|
| v6 source (this lane refreeze/devint1_contestant_v6.zag) | c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89 | YES (identical to arena_igl source) |
| v6 binary (this lane refreeze/sealed/bin/v6_refreeze, prior worker build) | 5d2be6acf4d98ef2118e2e1f2e52d87d38a9f848cb83e04d8b252199ce966f15 | YES (identical to arena_igl/sealed/bin/v6) |
| v6 binary (this worker rebuild from the source, pinned znc) | 5d2be6acf4d98ef2118e2e1f2e52d87d38a9f848cb83e04d8b252199ce966f15 | YES (build deterministic) |
| arena scorer (rebuilt from committed arena.zag) | 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076 | YES |
| world_gen (rebuilt from committed world_gen.zag) | c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211 | YES |
| Pinned znc | src/tools/toolchain/znc_linux_x86_64_abed8aa1 | (toolchain of record) |

Rebuild used the pinned znc at /home/hatch/safebin/znc with zero source
changes. git status confirms zero modifications under
docs/lab/research-lead/overnight-20260928/competitive_arena/ (K5).

## 3. Refreeze runs (3 fresh sealed runs, this worker)

Driver: refreeze/run_refreeze.sh (bash sequences verified binaries only;
no rebuild per run; identical protocol to arena_igl/run_sealed.sh).
World: deterministic seed 71503461337030; turns.jsonl sha256
0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469
on all 3 runs, identical to the canonical 1421pdt sealed world.

Per-capability scores (all 3 runs identical):

| Cap | n | v4 baseline | v6 refreeze |
|-----|---|-------------|-------------|
| 1 | 6 | 1.000 | 1.000 |
| 2 | 4 | 1.000 | 1.000 |
| 3 | 6 | 1.000 | 1.000 |
| 4 | 4 | 1.000 | 1.000 |
| 5 | 6 | 1.000 | 1.000 |
| 6 | 3 | 1.000 | 1.000 |
| 7 | 3 | 1.000 | 1.000 |
| 8 | 4 | 0.000 | 0.000 |
| 9 | 3 | 0.000 | 0.000 |
| 10 | 2 | 0.000 | 1.000 |
| 11 | 2 | 1.000 | 1.000 |
| 12 | 6 | 0.000 | 0.000 |
| 13 | 6 | 1.000 | 1.000 |
| 14 | 6 | 1.000 | 1.000 |
| 15 | 1 | 0.000 | 0.000 |
| 16 | 6 | 0.000 | 1.000 |
| TOTAL | 68 | 0.676 | 0.794 |

Total: 54/68 = 0.794 on all 3 runs. Gain: +8 items (C16 +6, C10 +2).

## 4. Kill bar verdicts (amended prereg)

- K1 (C16 above zero, target 1.000): PASS. 1.000, 6/6.
- K2 (total above 0.676): PASS. 0.794 (54/68) on all three runs.
- K3 (amended; no regression, no leakage): PASS. All capabilities except
  C16/C10 byte-identical to the v4 baseline. C10's 2 items answered by the
  preregistered zemprod mechanism (replies "0,1,2", learned A/B templates
  visible in state); no other mechanism contributes.
- K4 (pure Zag): PASS. Zero python invocations in this lane (safebin guard;
  `which python3` empty; only znc-built binaries, bash, safebin coreutils).
  Zero em-dash bytes in lane docs (byte scan).
- K5 (sealed arena): PASS. competitive_arena/ unmodified (git status clean).
  Contestant source unchanged from the canonical audited v6 (worlddir
  arg-presence-checked only; answer_key/idmap/proofs never opened).
- K6 (determinism): PASS. 3/3 runs: identical per-capability scores;
  replies.jsonl byte-identical across runs after stripping ms/rss_kb timing
  fields (sha256 03a29ce6d69d9c54d13ad6586a01c8f51d6f2af8c82a8690a843faedd42f2bd9),
  and identical to the canonical 1421pdt run2 replies under the same strip.
  results.txt differs only in max_rss_kb (3292 vs 3288), a timing field in
  the exclusion class.
- K7 (no-gaming / generality): PASS. Source byte-identical to the canonical
  v6 that passed the K7 audit and generality probe in the 1421pdt lane.
  Re-audit by this worker: zero occurrences of any sealed-world Zem word
  name (befise, bekoka, berate, berite, fite, narate, nataka, pekodo,
  peruzo, ruguka) in source; the single "transform" substring is the word
  "transformed" in a handler comment, not a transform-id constant.
- K8 (architecture): PASS. Source unchanged; no new modes, bridges,
  routers, or admission gates; 2 question-type handlers in existing
  dispatch; 0 hardcoded semantic cases.

BUILD-PASS: K1 through K8 all PASS (8/8).

## 5. Refreeze confirmation

The v6 0.794 (54/68) reproduces cleanly with zero contamination: fresh
independent rebuild from the canonical source is byte-identical to the
re-frozen binary; three fresh sealed runs on the deterministic sealed world
reproduce the exact per-capability scores and the exact reply stream
(byte-identical replies.jsonl to the 1421pdt re-freeze runs). No deviation
from the amended-prereg record. This is a refreeze confirmation of the
CANDIDATE score. It does not move the canonical 0.573 (only a clean
refreeze reproducing composition without contamination can do that, per
the standing rule). No TNN-beats-LLM claim is made.

## 6. Files

- refreeze/NAMECHECK.md (appended; toolchain re-activation Step 0)
- refreeze/devint1_contestant_v6.zag (canonical v6 source, hash-verified)
- refreeze/sealed/bin/v6_refreeze (hash-verified v6 binary)
- refreeze/sealed/bin/world_gen, refreeze/sealed/bin/arena (hash-verified)
- refreeze/sealed/rebuild/ (this worker's independent rebuild; hashes match)
- refreeze/sealed/run1, run2, run3 (fresh sealed runs: world/, pilot/)
- refreeze/run_refreeze.sh (sealed evaluation driver)
- refreeze/REFREEZE_RECORD.md (this file)

Nothing committed, nothing pushed (per task). .wave_lock untouched.
