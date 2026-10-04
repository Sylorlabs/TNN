# Broker method — native-authorship trial 1 (P2 honest broker)

## Role and constraints

Independent honest broker. No contact with implementer/generator; no re-tuning;
frozen sources only; pure-Zag harnesses; zero RNG; deterministic order; one
isolated process per (arm, question); crashes count incorrect.

## Frozen pins (all extracted via `git show`; sparse worktree never touched)

| Artifact | Commit | Path |
|---|---|---|
| Prereg (frozen) | `50fb8ff86e5a1966eecdc03c829e3b972b055c1b` | `docs/lab/native_authorship/PREREG.md` |
| Arm L (frozen lookup) | `e74271015` | `docs/lab/mg_chunking_promote/intake.zag` |
| Arm D (deliberative chooser) | `ab79f1a5c7d` | `docs/lab/native_authorship/chooser/` (`chooser.zag`, `dlib.zag`, `DESIGN.md`, `battery_d.zag`, `R33_NATIVE_IO_V1.zag`, `evidence/`) |
| Battery + oracles (sealed) | `af629be25` | `docs/lab/native_authorship/battery/` (`battery.zag`, `oracles.txt`, `ORACLE_MANIFEST.md`) |

SHA-256 (verified 2026-09-27):
- Toolchain `znc_linux_x86_64_abed8aa1`: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- D chooser source `chooser.zag`: `6f8b1db09b53a062860cc3606dfba753c464bff6e47048bcc34d692f5a2188d3`
- IO source (both arms): `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- Oracle manifest digest (sealed): `57177f6e3f9772332bfe57ebeaf78dac27047d074dbe841da81afac52d4ad582`
  (recomputed from frozen `oracles.txt`: match)

D source grep: clean for `policy_winner` / `policy_why`; no rng/random/seed/getpid/
gettime/rdtsc on the choice path (only "Zero RNG" comments).

## Broker drivers (in `broker/src/`)

`drvL.zag` = carrier(IO) + frozen `intake.zag` + L driver main.
`drvD.zag` = carrier(IO) + frozen `chooser.zag` + frozen `dlib.zag` + D driver main.
Both read a 2-byte `param.bin` = `[qid, forced_candidate]` from the process cwd
(`0` = use the arm's own chooser; `1–9` = force candidate for oracle measurement).
Each prints `# BROKER qid=.. fc=.. correct=..` plus a result line
`R ans=".." exp=".." correct=..`. A panic → nonzero exit → scored incorrect.

Neuters (source patches on the D driver composition, §6):
- `drvD_feat.zag`: constant-folds all 14 features after `d_features`
  (kind=5, shape=2, nwords=3, nbytes=20, nlines=1, lenclass=2, ans_unit=2,
  count_unit=2, addr_depth=2, edge=0, last_anchor=0, needle_hit=1, relative=1,
  anchor_third=0).
- `drvD_def.zag`: `w=3;` after `d_deliberate`, before `cand_answer`
  (deliberation still runs and is traced; only the executed choice is overridden).
- `drvD_trace.zag`: early-return in the chooser's trace emitters
  (`emit_feat`/`emit_ev`/`emit_elim`/D-CHOICE/D-REFUSE); choice execution untouched.

## Sweeps

`run/sweep_L`, `run/sweep_D`, `run/sweep_D{feat,def,trace}`, `run/oracle_{L,D}_c{1..9}`:
26 qids × each, isolated processes, `param.bin` per dir, `exitcode` + `run.out`
recorded. 520/520 runs integrity-verified (2-byte param echo, `# BROKER`
qid/fc match, parseable result line or recorded crash).

Scoring is **oracle-grounded**: correct ⟺ `ans == exp` against sealed
`oracles.txt` — not the arm's self-reported flag (D's refusal path hardcodes 0;
the oracle blesses `?` for D1/D4, so q14/q17 refusals score correct).

## K5/K6

`k5L/` and `k5D/`: frozen `battery1.zag` / `battery_d.zag` extracted via
`git show`, rebuilt with the pinned toolchain, run → 57/57 both, 0 fallback.
K6: two D runs byte-identical (`RUN_K5D_1.out` == `RUN_K5D_2.out`,
SHA-256 `756ec52b…`), rebuild-from-source reproduces byte-identical output.

## K7

- Binary grep of rebuilt `battery_d_bin` (308070 bytes,
  SHA-256 `f964b6e2…`): trap-unique strings (`w0 w1`, `the  quick`,
  `2nd (second)`, `abc def contain bcd`, `how many .'s`, `101010`, `APPLES`)
  absent. `strawberry`/`the cheese wheel`/`the quick brown fox` present but also
  present 8/9/16× in the frozen 57Q `battery_d.zag` source — shared production
  vocabulary, not oracle leakage.
- Frozen D source (`chooser.zag`+`dlib.zag`): zero trap-string hits.
- Timestamps: seal `af629be25` 2026-09-27 01:27:24 -0700;
  D impl `ab79f1a5c7d` 2026-09-27 01:33:13 -0700 (seal 5m49s earlier);
  `git merge-base --is-ancestor af629be25 ab79f1a5c7d` → yes.

## Disk-crisis incident (2026-09-27)

Home filesystem hit 100% during the oracle sweeps: 73 `oracle_D_c{7,8,9}` runs
wrote empty `param.bin` (silent ENOSPC) and were invalidated — never trusted,
re-run cleanly after space recovered. One K6 rebuild under ENOSPC produced a
0-byte binary (discarded); clean rebuild reproduces. /tmp was reaped mid-task
(ephemeral); all durable artifacts live under `~/workspace/native_auth_broker/`.
