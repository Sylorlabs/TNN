# RESULTS.md — FL2 default engineering crew (2026-09-23)

Assignment: install FL2 as the canonical default guided-learning (gl) path,
deprecate the old E38/392 scaffold arm, kill the per-episode heartbeat audit
across `training_paradigms/scaffold_release/forks/` (g1–g7), verify
deterministic behavior + exact replay, commit to `tnn-native-lab`.

Ruling applied throughout: Micah 2026-09-23 — terminology "guided learning
(gl)", FL2 is the default, old scaffold deprecated, per-episode heartbeat
auditing dead.

## 1. Canonical default: `gl_default/`

New directory `training_paradigms/scaffold_release/gl_default/`:

| file | content |
|---|---|
| `gl_substrate.zag` | canonical memory substrate (store, audit, episode schedule, sim twins) + frozen guided-learning op codes `TN_OP_PINSTALL=16`, `TN_OP_PROMOTE=17`, `TN_OP_UNINSTALL_PROVISIONAL=18` |
| `gl_learner.zag` | reference learner `arm_gl` (FL2) + in-binary teaching baseline `arm_a`; `fl2_*`→`gl_*`, check prefixes `glh_`/`gll_` |
| `run_gl.sh` | no-RNG grep, select/simulation region token check, no-accumulation check, compile, 2-run byte-identity, all checks, headline totals |
| `README.md` | design, frozen numbers, known limitation, crew guidance |
| `evidence_run1/2.txt`, `evidence_compile.txt` | verification artifacts |

Adaptation fidelity: comment-stripped, rename-reversed token diff of
`gl_learner.zag` vs the frozen FL2 `fl2.zag` is empty (792/792 tokens);
same for `gl_substrate.zag` vs `tn.zag` (482/482) apart from the moved op
codes. Zero logic change.

Verification (2026-09-23): compile OK; 78/78 `TN_CHECK` lines match;
`TN_FAILURES=0`; two runs byte-identical
(sha256 `c45ea5cccff592039e3a970eadc6bccb750067381c0ae62580bf2857b87b90ba`);
honest audit total **269**, lying **271**; deliberate-teaching baseline 267.
No randomness (static grep), no signal reference in select/simulation regions,
no csum/ccnt accumulation.

Mechanism (frozen): trainer installs rule provisionally (`TN_OP_PINSTALL`);
action selection reads only committed-survivor-else-provisional; on each
world episode the learner simulates the two alternatives with no-audit twins
and revokes the provisional install on contradiction by its own observation
(`TN_OP_UNINSTALL_PROVISIONAL` + commit); survivors are promoted at release
(`TN_OP_PROMOTE`); learner-initiated disconnect ends scaffolding.

Known limitation (carried over): FL2 acts the lie during E15–E29 until
contradictory world evidence arrives; a never-contradicted lie remains
installed. Revocation is world-evidence-driven by design.

## 2. Heartbeat kill — method

P2's proven event-driven pattern applied to every live heartbeat site: a
scaffold entry is written only when (a) the episode is the
disconnect-transition (`trans`, tracked via `fire_step==ep`), or
(b) the signal is an actual contradiction (`signal == -1`, the episodes that
drive elimination). Null/sentinel periodic reads removed. Hint/probe markers
that carry real information kept (`s2` identity hint h3, `s5` ADV_OK probe).
`g4`'s shared `d3s_episode` gates its per-episode signal record on
`signal==-1` (its disconnect is already audited as `D3_OP_DISCONNECT`).

Replay safety: no fork's replay routine reads scaffold entries
(`tn_b_replay_diff`, `d3s_replay`, `mp_b_replay`, `d2_b_replay_diff` verified),
so removing heartbeat entries preserves exact control-state replay.
Behavior is otherwise untouched: the gating only suppresses audit writes;
all streak/elim/select logic is byte-identical.

Before editing, all 20 target files were byte-compared against branch
`tnn-native-lab` via `gh-api` — all matched. Edits applied by exact-match
script with per-pattern count assertions (no silent partial edits).

## 3. Heartbeat kill — per-variant results

All re-verified 2026-09-23 with each fork's own runner: compile OK, two runs
byte-identical, every check matched, `*_FAILURES=0`.

| variant | scaffold old → new | audit total old → new | run sha256 (run1=run2) | checks |
|---|---|---|---|---|
| g1/r1 | 128 → 3 | 392 → 267 | 2a72e219221386878635c2e2bfb693afb491b929df92665c8fb347d7058c3630 | 40 |
| g1/r2 | 128 → 3 | 392 → 267 | e5075f93b0b23924910abb55fd8680cdbdc3d3674165ba394953f6c23ffa7385 | 41 |
| g1/r3 | 128 → 2 | 387 → 261 | 650034fc07905898bbe6b64a1f5cddc0204ded4a5cc3d66b766d1a77637ef4f6 | 44 |
| g1/r4 | 128 → 3 | 392 → 267 | 1500eeb8571e6b3e1be4ca5fd78d9388b234f334ae6f2720b114d5f772829c5b | 40 |
| g1/r5 | 128 → 2 | 396 → 270 | 75e28a577c4fc911e8108f6b83a89fd3dbc926a2d33664385653ddf4c9f2d687 | 40 |
| g2/s1 | 128 → 3 | — | 70dbcdf23a321312df29fbad5c4c5885a2a730fa563fe1f148228933776e97d5 | 39 |
| g2/s2 | hints 102/102/1 → 3/3/1 (7 total) | — | 72d673f80adcc70b00619aa2e022f271c486ecf7f81be2775acab541091e67b3 | 43 |
| g2/s3 | 128 → 3 | — | aa51c2ced6a5529e022f74cde16c5526b258d31e44dc9f772b6256515e4a95ae | 41 |
| g2/s4 | 2 → 0 | — | 5c719cdded0f75b305b2418f5bc22ee377c6555deb1168d9bfea68a10e021a38 | 38 |
| g2/s5 | 128 → 4 (3 events + ADV_OK) | — | 58487e6c78672e24df09c3bd8d4050bfdfa87a772be54bf0192c027355186711 | 41 |
| g3/l2 | 128 → 3 | — | 11dfbd3db3c6e1f4a40dc0487d12c48055233ff84175ae2fd7f7cfe49b37f349 | 25 |
| g3/l3 | 128 → 3 | — | e451b090ca2ab71fc3fe2f170b6c92893a2a0579bd368406aa5f0eee03af9177 | 26 |
| g4/r1 | per-ep → signal==-1 only | — | bf291a96a383ea31c99f436dbf20cab5d31db0f82af24db013e57ca7a7dc518c | 23 |
| g4/r2 | per-ep → signal==-1 only | — | b3f113eab28a4a44648cb9922cc8327291534e86b585ad5da040a8e916ddc31c | 19 |
| g4/r3 | per-ep → signal==-1 only | — | c7abdbca05b253923d17e29a443db50a0b1b0fa7f64c7f7dc34b07cf262424ad | 21 |
| g6/p1 | 848 → 3 | 2588 → 1743 | 7a235ff033c6a9e4b880088062f8fb671d92a3ae3e8c9cb07c9c525ae882a60a | 56 |
| g6/p2 | 850 → 3 | 2815 → 1968 | e18c2b831d386e4df4585689acf8ea44496df037281fe7bc76aa964324f46ec5 | 54 |
| g7/profiler/p1 | 128 → 3 | 392 → 267 | 2635df2db5281f782f86596191124e879a150a456a3875511f57c41ba2baabc7 | 57 |
| g7/fl4 | 128 → 2 | 398 → 272 (both arms) | 750fd356afa5d3bf39a0515741312217ddf8b41b8cbd3b672b4c8fd16462a6f28 | 74 |
| g7/rematch/r2_d1b | 128 → 3 | 399 → 274 | 2875348039cd867b80a1d5ebe1da575c8d614aefa7fdd2c4dd764e4ffb90f684 | 100 |
| g7/rematch/r3_d2 | 128 → 3 | 392 → 267 | 254540a0f599452b1c1f1a0dcb99093b37b3961033e19ce70b44521ceb5bb82d | 100 |

Notes: r3 never fires (trans never occurs → heartbeat vanishes entirely,
correct per "log only on actual events"). s4's heartbeat was 2 teach-sentinel
entries → 0. g6/p1's full op-profile check `p1_total` updated 392→267
(profile sums exactly). d1b/d2task dual-arm files: only the old arms edited;
their FL2 arms untouched (still 270/272 and 269/271). New explicit scaffold
count checks added to every converted arm.

## 4. Deprecation

- `forks/g7_slowness/profiler/p0_baseline/DEPRECATED.md` — old E38/392 arm
  SUPERSEDED, frozen byte-identical for reference/reproducibility. This is
  the one documented exception to the everywhere-kill: its 392-entry ledger
  (128 heartbeat) is the historical G7 slowness baseline the free-lunch
  investigation measured against. Exact pre-kill code also in git history.
- `DEPRECATED_SCAFFOLD_ARM.md` — top-level pointer old → `gl_default/`.

## 5. Inspected, no change (with reason)

- `forks/g7_slowness/freelunch/fl2_provisional_revoke/` — already event-driven
  (source of `gl_default/`); untouched.
- `forks/g7_slowness/freelunch/fl1_teach_disconnect/` — no scaffold appends.
- `forks/g7_slowness/rematch/r1_d1/` — FL2 event-driven already.
- `forks/g7_slowness/profiler/p2/`, `p3/` — already event-driven (3 events each).
- `forks/g3_lying_teacher/l1_mistaught_teaching/` — no scaffold appends.
- `forks/g5_dialogue/f1_fadefast`, `f2_fadeslow` — no scaffold signal; no heartbeat.
- `forks/g4_outcome_domain/baseline_teaching/` — no scaffold audits at all.
- `forks/g8_fl2_variants/` — sibling crew's active FL2-variant work; already
  event-driven (2 gated scaffold audits per file). Out of scope; untouched.

## 6. Commits

- `c93b9d48b6c7ff2a2bf28bd527e7ba30578dbdc2` on `tnn-native-lab`
  (parent `78aba063df86`): gl_default/ (7 files), 19 modified .zag files,
  40 regenerated evidence files, HEARTBEAT_KILL.md, DEPRECATED markers.
  71 files, lab-relative paths, no binaries/.zagd committed.
- This RESULTS.md: second commit (below).

## 7. Limitations / open notes

- FL2 boundary (carried): acts the lie E15–E29 until contradictory world
  evidence; a never-contradicted lie remains installed.
- p0_baseline deliberately exempted from the heartbeat kill (frozen reference).
- `gl_default` check prefixes renamed (`glh_`/`gll_`); behavior identical,
  totals unchanged (269/271).
- g8 variants were not swept (sibling crew's active tree); verified already
  event-driven, no action needed.
