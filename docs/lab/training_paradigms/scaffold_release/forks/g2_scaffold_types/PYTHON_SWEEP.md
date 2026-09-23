# G2 Python sweep — audit of Python in fork codebases and decision paths

Date: 2026-09-23. Conducted by the G2 subagent per the task requirement.

## Sweep commands

```
find ~/workspace/tnn-lab/training_paradigms/scaffold_release/forks/g2_scaffold_types -name "*.py"
# result: (no output — zero .py files in any fork)

# per-fork token scans over the Zag sources (comments stripped):
#   no rng/rand/seed tokens (runner check 1)
#   select-region signal-token bans: s1: reward; s2: hints; s3: shaped; s4: demo; s5: reward (runner check 2)
#   no reward accumulation in scaffold arms (runner check 3)
```

All three static checks are enforced by each fork's `run_fork.sh` before compilation and all passed on every run.

## Where Python was actually used

Python was used ONLY as build-time glue, never in any AI decision path:

1. **Source generation** — Python heredocs assembled the Zag sources (select regions, arm bodies, runner scripts) from staged text fragments in `/tmp`. The generated `.zag` files are what compiled; the Python never ran inside the trial.
2. **File transforms** — Python `str.replace`/`re` edits applied the arm swaps, renames, and helper insertions to the `.zag` sources (S4/S5 construction).
3. **Audit-cost measurement** — Python copied each trial `.zag` to `/tmp`, inserted audit-count print statements, compiled the copies with the pinned znc, ran them, and reported per-arm audit entry counts (baseline 267; S1 392; S2 448; S3 397; S4 272; S5 397). The frozen fork sources were NOT modified; the measurement binaries lived in `/tmp` only.
4. **This sweep** — the sweep itself.

## Runtime decision paths

The trial binaries (`s1_trial_linux` … `s5_trial_linux`) are compiled from pure Zag sources (`tn.zag` + `sN_trial.zag`) by the pinned native compiler `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Every learner decision (action selection, elimination, commit, disconnect, refusal) executes in compiled Zag. No Python process runs during any trial episode; no Python output feeds any decision.

## Verdict

**PASS** — zero Python in any fork directory, zero Python in any AI decision path. All five forks satisfy the no-Python-in-decisions requirement. (Build-time Python glue is documented above per the task's "conduct and document" requirement.)
