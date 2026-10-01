# GW1-GW8 Evaluator NAMECHECK

## Step 0: Toolchain Guard (mandatory)

Date: 2026-10-01 (PDT). Evaluator: GW1-GW8 Evaluator (independent of adversary, builder, FW evaluator).

Safebin setup executed at task start:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. `guard-check-done` printed. Safebin PATH active for all subsequent commands.

No forbidden executable (python3, python, cc, gcc, node, deno, java, rustc, cargo) was invoked during this evaluation. All world execution via the frozen prebuilt binaries only. Shell used only for: invoking binaries, file moves, git operations, grep/sed/awk text processing of transcripts.

## Scope

Evaluate frozen TNN-2 (binary SHA-256 `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`, verified before first run) on the sealed GW1-GW8 battery (adversary commit `e409f5eea`) via the frozen shim (binary SHA-256 `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`, verified before first run).

Constraints honored:
- TNN-2 source and binary NOT modified.
- Shim source and binary NOT modified.
- Adversary world files NOT modified.
- GW world contents used only as evaluator input (event streams fed to the shim); no tuning, no inspection beyond running.
- Three deterministic runs per world, fresh learner state per run.
- GW5 responder rule implemented as specified (release B1 iff transcript contains a line exactly `CHOICE 30`, else B2), using grep on the captured transcript. The sealed responder source was read to confirm the rule; the rule itself is in the public ADVERSARY_DESIGN.md.
- Hashes of TNN-2 binary and shim binary recorded before and after the evaluation.

## Provenance

- Adversary design: `docs/lab/research-lead/overnight-20260928/postfreeze_adversary/ADVERSARY_DESIGN.md` (commit `e409f5eea`)
- Seal record: `docs/lab/research-lead/overnight-20260928/postfreeze_adversary/SEAL_GW.md`
- TNN-2 build: `docs/lab/research-lead/overnight-20260928/tnn2_build/` (frozen `f4de7ff46`)
- Shim: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/` (SHIM-BUILD-PASS `23c2c0206`)
- Output: `docs/lab/research-lead/overnight-20260928/gw_eval/` (this directory; owned path only)

Paper untouched. No em dashes in this file.
