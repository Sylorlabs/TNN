# NAMECHECK: C1 Pure-Zag Race Driver

Date: 2026-09-30 UTC
Worker: Pure-Zag C1 Race Driver Builder
Verdict label target: C1-ZAGDRIVER-COMPLETE

## Step 0 name-check (written before any work)

The four standing-rules sections from LOOP_STATE.md are identified:

1. Pure Zag for all research logic. No Python, no C, no other languages.
   Shell/git only for orchestration: invoke znc, run binaries, git ops,
   move/copy files. No shell scripts as substitute research programs.

2. Owned path: docs/lab/research-lead/overnight-20260928/c1_zagdriver/.
   Commit only this path with explicit pathspecs. Inspect status before
   every commit. Never remove a live .git/index.lock; wait and retry.

3. Frozen source/binary never modified. The C1 world files (c1_clean/worlds)
   are read-only inputs. The contestant and baseline binaries are invoked,
   never rebuilt or altered.

4. Contaminated paper docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
   untouched. Zero diff required on every commit.

## Prereg ordering

Fresh prereg must strictly precede implementation. The prereg commit
contains only NAMECHECK.md and PREREG.md. The driver source comes after.
