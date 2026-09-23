# VERDICT — T2-DIALOGUE replication

**Family:** T2-DIALOGUE — dialogue rebuild 370/370 (Type A, full independent rerun)
**Crew:** T2-DIALOGUE, Wave 2 (Tier 2) cross-reference program
**Date:** 2026-09-22/23 PDT
**Verdict: REPRODUCED**

## Claim (frozen prereg, PREREG_TIER2.md §T2-DIALOGUE)

> Native dialogue rebuild/rerun passed 370/370 byte-identically with new digest
> beginning `35aaae8a`; the frozen verdict is stale and needs re-freeze/amendment
> (recorded, not re-litigated).

**Rule:** REPRODUCED if 370/370 byte-identical with digest `35aaae8a…`;
NOT REPRODUCED if the count or digest differs.

## Measured

| Check | Claimed | Measured | Match |
|---|---|---|---|
| Turn count | 370/370 | **370/370** (45+45+60+30+30+60+72+28, all PASS) | ✓ |
| Response digest | `35aaae8a…` | `35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b` (binary `DIGEST` line) | ✓ exact |
| Byte-identical reruns | 5/5 | **5/5** (log sha256 `33743aea…` ×5) | ✓ |
| Committed-evidence agreement | — | my logs **byte-identical** to committed `full_1..5.log` (`cmp` clean) | ✓ |
| Independent oracle | — | committed `verify_dialogue.py`: 8/8 sections 100%, 10/10 compose-novel ✓, weird-gap 0.0pp, **0 errors** | ✓ |

The frozen rule is satisfied exactly: 370/370, byte-identical, digest
`35aaae8a…`. **No divergence of any kind was found.**

## Method (Type A)

1. Fresh sparse clone of `sylorlabs/TNN` branch `tnn-native-lab` into
   `~/workspace/scratch-crossref/T2/DIALOGUE/clean/`, checked out at the frozen
   prereg commit (full fetch repeatedly failed — remote SIGKILL; blob-filtered
   fetch of the single commit succeeded, 1.2M).
2. Rebuilt `dialogue.zag` **from source** with the pinned znc
   (`znc dialogue.zag --no-zagd --no-analyze --no-foreground-cache -o dialogue_bin`,
   run from the build dir so `@import("R33_NATIVE_SHA256_V2.zag")` resolves).
   No `.zagd` caches or binaries copied.
3. Ran the **frozen committed `battery.txt`** 5× (`kb.txt`, `gaz.txt` read from
   cwd at runtime, all from the frozen commit).
4. Verified with the **committed independent oracle** `verify_dialogue.py`
   (replays `battery.txt`, recomputes PASS/FAIL vs expectations, checks novelty).
5. Zero RNG anywhere; all inputs pinned before running (below).

## Frozen pins (all from the prereg commit, verified by blob SHA)

| Input | Commit / blob | sha256 |
|---|---|---|
| Prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` (tnn-native-lab) | — |
| `docs/lab/dialogue/dialogue.zag` | blob `964b2bc2bd9c186bbd7efab56f9e68a231eb2c8d` | `acda81acb408c014d3a852711bbbd97fe04bed8728be4fea45b16724c5c8231f` |
| `docs/lab/dialogue/battery.txt` | blob `bf313e616122b9170ff4588883da7274f8352af9` | `3a4ebc83151792c3378aaf8e5c7d284f3c7fb16825f94ba0bba53773f28677e5` |
| `docs/lab/dialogue/kb.txt` | blob `68c86046277ecaf0b358bad30f474692d508d381` | `3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1` |
| `docs/lab/dialogue/gaz.txt` | blob `f09ec9c61403524bd7fbf6ef6e2de8305401e29dac` | `b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a` |
| `docs/lab/dialogue/verify_dialogue.py` | blob `c8bfae5f2db69851b79d3d7884df9dd6f657de9f` | — |
| `docs/lab/dialogue/morphology/runs/full_1..5.log` | blob `e60435c123f6f739ec998a1691e389b107ad0717` | `33743aead2f6457dce48653df1eff28e91cbf165208839ab86fad0e8c4bbb372` |
| `src/experiments/R33_NATIVE_SHA256_V2.zag` | blob `5dd858fa1097451ee6164c015993fd5a434877db` | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |
| `docs/lab/prose-learning/src/R33_NATIVE_IO_V1.zag` (Linux port) | blob `a6b440d256437de5e34faa77a0d73079e2755375` | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` |
| znc toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, `znc 2026.07.0-dev (edition 2026)` | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |
| Rebuilt binary (not committed, scratch only) | `crew/build/dialogue_bin` | `912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5` |

## Record notes (not re-litigated, per prereg)

1. **Digest semantics:** the claimed digest `35aaae8a…` is the binary's own
   `DIGEST` line (sha256 over the concatenated responses), not the sha256 of
   the run log file (`33743aea…`). Both matched the committed record exactly.
2. **IO substrate pin:** `src/experiments/R33_NATIVE_IO_V1.zag` at the frozen
   commit is the **macOS/Darwin** build — unusable on this Linux VM. The build
   used the committed **Linux x86-64 port** from `docs/lab/prose-learning/src/`
   (blob `a6b440d2…`, byte-identical to the substrate in the original crew's
   build dir and the toolchain dir). Any future pin of the dialogue build must
   name the Linux-port path explicitly.
3. **Stale SHA256SUMS:** `docs/lab/dialogue/SHA256SUMS` still lists the old
   `dialogue.zag` hash and the old `run_det_1.log` digest (`f07f26cf…`) —
   consistent with the prereg's "frozen verdict is stale, needs re-freeze/
   amendment (recorded, not re-litigated)". Not a replication finding; routed
   as-is.
4. **Clean environment:** fresh clone; all build inputs from pinned commits;
   no binaries or `.zagd` committed; work confined to
   `~/workspace/scratch-crossref/T2/DIALOGUE/`; sibling crews' dirs untouched;
   `TMPDIR=~/workspace/tmp_commit` throughout.

## Artifacts

- `~/workspace/scratch-crossref/T2/DIALOGUE/crew/RUNLOG.md` — full run log
- `~/workspace/scratch-crossref/T2/DIALOGUE/crew/build/` — build dir: frozen
  sources, build log, rebuilt binary (scratch only, never committed), 5 run
  logs `run_rep_1..5.log` + oracle copy
- `~/workspace/scratch-crossref/T2/DIALOGUE/clean/repo/` — fresh clone at
  `7b2100d09911c5c10252c5756c7def288e70bd1f`

## Bottom line

The committed claim survives cleanly: a from-source rebuild in a fresh
checkout reproduces **370/370** turns, **5/5 byte-identical** run logs
(byte-identical to the committed logs), and the exact claimed digest
`35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b`.
**Verdict: REPRODUCED.**
