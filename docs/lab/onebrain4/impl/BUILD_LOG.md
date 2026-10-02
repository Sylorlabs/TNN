# BUILD_LOG.md — One-brain R4 machinery build (Crew M)

## Toolchain
- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Version string: `znc 2026.07.0-dev (edition 2026)`
- Matches the pinned toolchain SHA recorded in REDTEAM3 (truncated `498abcb5…1357e58ef`) and AGENTS.md.

## Source provenance
- Base source: `onebrain_v3.zag` extracted via
  `git archive hyptest-coord docs/lab/onebrain3` from
  `~/workspace/tnn-native-lab-work`.
- Base SHA-256 (verified before any edit):
  `f8abec7220cce17d4013160cff05c33785244a392b84db71b8b4a4b7ec1aa6b5` — MATCHES the task's pinned hash (post-fix-or-kill, commit a7f77b25b).
- v6.tsv SHA-256 (verified): `42d215ecebc9302141aaec93cc067a78effba79541059d2e60f6e165fe1139d0` — MATCHES the freeze hash.
- Ref tree: `~/workspace/onebrain4/ref/docs/lab/onebrain3/`
  (`impl/onebrain_v3.zag`, `impl/R33_NATIVE_IO_V1.zag`, `v6.tsv`,
  `MEASUREMENT3.md`, `redteam/REDTEAM3.md`).

## Edits (onebrain_v4.zag vs verified v3 source)
Full diff is comment-only except three behavioral deltas, all gated on new
neuter values and reachable only via the two new modes:
1. `ob_audit`: if `neuter==5 || neuter==6`, the two `audit_invalidate`
   calls (2a/2b) are skipped — exactly REDTEAM3 Attack 2.3's nodeny patch.
   Duel, bid cleanup, and re-scoring run unchanged. A trace line
   `AUDIT_NODENY denial deliberations 2a/2b skipped` marks the patch site
   (trace only; not part of VERDICT output).
2. `reint_delib`: `neuter==4 || neuter==6` takes the nG honest-null branch
   (lowest-hid alive bid) — so `nov4nG` = nov4 + nG at reintegration.
3. `main`: `nov4` → `run_full(mode,path,1,1,0,5)`; `nov4nG` →
   `run_full(mode,path,1,1,0,6)`. Usage string updated.
Everything else (all 9 existing modes, duel, V4, fork, GEN/ELIM/ARGMAX) is
untouched.

## Build commands (cwd = ~/workspace/onebrain4/impl; @import resolves rel. to cwd)
```
cd ~/workspace/onebrain4/impl
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 onebrain_v4.zag -o onebrain_v4
```
- Exit 0. Two pre-existing analyzer warnings (E0102 multiply-by-0, line 394
  in `led_init` — present verbatim in the pristine v3 source; not touched).
- `znc: wrote native binary onebrain_v4 (184868 bytes main, 0 external tools)`.

A pristine v3 control binary was built identically from the ref dir for the
decision-identity check:
```
cd ~/workspace/onebrain4/ref/docs/lab/onebrain3/impl
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 onebrain_v3.zag -o onebrain_v3
```
(exit 0, same 2 pre-existing warnings, 183816 bytes main).

## Binary / file SHAs
| file | SHA-256 |
|------|---------|
| `impl/onebrain_v4` (binary) | `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` |
| `impl/onebrain_v4.zag` | `bbb1752ec5ee0c8bc3871bb41c4cfe65bc0d8e27f9357883d1712dbb4b006874` |
| `impl/R33_NATIVE_IO_V1.zag` | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` |
| `impl/v6.tsv` | `42d215ecebc9302141aaec93cc067a78effba79541059d2e60f6e165fe1139d0` |
| pristine `onebrain_v3.zag` (ref) | `f8abec7220cce17d4013160cff05c33785244a392b84db71b8b4a4b7ec1aa6b5` |

## Run command shape
`./impl/onebrain_v4 <single|onebrain|ablate|poison|min|nF|nS|nA|nG|nov4|nov4nG> impl/v6.tsv`
~0.4 s per mode on v6 (44 problems). Trace files: `~/workspace/onebrain4/runs/`.
