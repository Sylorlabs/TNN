# RUNLOG.md — Build and run record

Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
All temp material under `~/workspace/tmp_commit` (`TMPDIR` set; unique `cl_*` prefixes).
Disk checked before heavy runs (`df -h ~`: 100 GB total, 2.8 GB free on 2026-09-27 — tight but sufficient; no heavy regenerable writes kept).

## v2 repair build & runs (2026-09-27)

Fixes: §7(c) entailment (`prov_select`), `disc_gate` verification tightening,
occupied-count consolidation scan (`psm_slow_occupied`). See RESULTS.md D9–D11.

| Step | Command | Result |
|---|---|---|
| Battery v2 | `znc battery.zag -o ~/workspace/tmp_commit/cl_repair/battery_v2` (cwd=`build/`, imports resolve relative to cwd) | exit 0; ~36 ignored-return warnings (A0102, reviewed) |
| Scorer v2 | `znc scorer.zag -o ~/workspace/tmp_commit/cl_repair/scorer_v2` | exit 0 (scorer.zag unchanged from v1) |

Battery output SHA-256 (v2, all legs): `5404a16551f74acd409ce77bfa54d76e3a26d7ca6d938ecc748e3f151ec22a22`

| Leg | Command | SHA-256 | Match |
|---|---|---|---|
| 1 normal | `battery_v2 full <fixtures>` | `5404a165…22a22` | — |
| 2 normal | `battery_v2 full <fixtures>` | `5404a165…22a22` | ✅ byte-identical |
| 3 `env -i` | `env -i battery_v2 full <fixtures>` | `5404a165…22a22` | ✅ byte-identical |
| 4 padded env | `env -i FOO=bar BAZ=qux PADDING=x×1000 battery_v2 full <fixtures>` | `5404a165…22a22` | ✅ byte-identical |
| 5 different cwd | `cd ~/workspace/tmp_commit/cl_repair/cwd && battery_v2 full <fixtures>` | `5404a165…22a22` | ✅ byte-identical |

`scorer_v2 <v2-output> <fixtures>` → `SCORE  phase1=6  phase3=12  phase4=3  conseq=2`

Key v2 run facts:
- `PROV  PV-1  EP-P1-A1  0`, `PROV  PV-2  EP-P2-E1  12`, `PROV  PV-3  EP-P1-C1  6` — all `chain=1 live=1 valuematch=1 entail=1`.
- `CONS_EVAL`/`CONS`: 6 promotions in pass 1 (dense 0,1,3,4,6,7), 6 in pass 2 (dense 9,10,12,13,15,16); `BREG PROM` ×12; all `rc=0`.
- `SUMMARY  18  18  18  39  12`.
- ANS/ANS4/CONSEQ lines byte-identical to v1 (retrieval unchanged).
- Independent checks: Python rescore `6/12/3/2` (matches Zag scorer); paraphrase leakage clean (max 333/1000); bridge hardcode audit clean (zero concept/item strings in `bridge.zag`/`battery.zag`/`psm.zag`); PREREG.md/REDTEAM.md hashes unchanged.

## v1 build & runs (preserved)

| Step | Command | Result |
|---|---|---|
| Battery | `znc build battery.zag -o ~/workspace/tmp_commit/cl_bin` | exit 0; ~32 ignored-return warnings (A0102, reviewed: discarded rc values are logged separately where load-bearing) |
| Scorer | `znc build scorer.zag -o ~/workspace/tmp_commit/cl_scorer` | exit 0 |

## Determinism battery (5 legs, SHA-256 of every output)

Battery output SHA-256 (all legs): `4ed896d1b471b758ac20a1c450587e2cdb7df0d2f231010e843a2a386272f1a5`

| Leg | Command | SHA-256 | Match |
|---|---|---|---|
| 1 normal | `cl_bin full <fixtures>` | `4ed896d1…f1a5` | — |
| 2 normal | `cl_bin full <fixtures>` | `4ed896d1…f1a5` | ✅ byte-identical |
| 3 `env -i` | `env -i cl_bin full <fixtures>` | `4ed896d1…f1a5` | ✅ byte-identical |
| 4 padded env | `env PADDING_AA…=1 cl_bin full <fixtures>` | `4ed896d1…f1a5` | ✅ byte-identical |
| 5 different cwd | `cd /tmp && cl_bin full <fixtures>` | `4ed896d1…f1a5` | ✅ byte-identical |

Zero randomness in decision paths; all five outputs byte-identical.

## Scoring

`cl_scorer <battery-output> <fixtures>` → `SCORE  phase1=6  phase3=12  phase4=3  conseq=2`

The scorer is pure Zag and the only module that reads expected-answer/synonym fields.

## Key run facts (from the frozen output)

- `SUMMARY  18  18  18  34  13` — 18 episodes taught, 18 registry entries, superordinate at slot 18, 34 substrate audit entries, 13 PSM consolidations.
- `H2  1  overwrite_ops=0  maxslot_p1=8  minslot_p2=9` — no Phase-2 overwrite of Phase-1 slots.
- `FORM  1  sig=thrush  code=ec627a47  slot=18  nev=3  nlab=3` — superordinate formed by the deliberation path with 3 `st_evidence` links (rc=0 each).
- `NOVAUDIT` — all 4 Phase-4 items: a=1 (zero verbatim overlap vs TEACH.md), b=1 (source section absent from teaching manifest), c=1 (no pre-verdict st_add/st_strengthen on Phase-4 ids).
- Bridge registry: 19 entries (18 facts + 1 superordinate), zero hash collisions, zero same-hash/different-bytes events.

## Notes

- One invalid smoke run was produced and DISCARDED during the build (offset/length slice bug in `tsv_field` consumers; fixed before any scored run). It is not cited anywhere.
- A temporary probe file was accidentally copied to shared `/tmp` during debugging and immediately deleted the same day; no experiment evidence came from it.
