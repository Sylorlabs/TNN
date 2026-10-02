# NAMECHECK_ADV: TNN3H5R independent adversary (sealed worlds + sealed evaluation)

Lane: TNN3H5R, wave-20261001-2021pdt. Role: independent adversary for the
sealed battery. I am a different agent from the H5R builder with no shared
working state; my task starts from the frozen prereg PREREG_H5R.md only.

## Step 0: toolchain verification (worker toolchain guard)

- 2026-10-01 21:19 PDT: ran
  `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  from /home/hatch/workspace/tnn-rsi. Output: SAFEBIN-READY,
  /home/hatch/safebin, 36 tools, znc OK, python3 and python absent.
- `export PATH="$HOME/safebin"`; `which python3` printed NOTHING
  (exit 1). PATH is safe.
- This lane will use only the pinned znc, built binaries, git read-only
  ops, and file moves/copies. Any forbidden executable invocation is
  automatic PROCESS-FAIL and will be reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
  I will NOT push, NOT git reset --hard, NOT rebase, NOT commit.
  New files only inside
  docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/: NAMECHECK_ADV.md,
  SEALED_H5R.md, SEALED_EVAL_H5R.md, and TNN3H5R/sealed/.

## Step 1: frozen prereg read (my specification)

PREREG_H5R.md read in full. Governing points for the sealed battery:
- KB-S1 substrate gate FIRST: the committed diff 830f95ab7 vs the H5
  base must contain BOTH the activate tag-20 hunk and the promote_graph
  deletion hunk. Either absent: battery does not run, H5R is VOID (NC-0R).
- KB-W0 PRIMARY: 36/36 MAP-key probe snapshots, zero live tag-1 facts on
  (s_m,r_m), each probe answered by the f28 of the single live tag-20 MAP
  with (f8,f4)==(s_m,r_m). KB-W0 applied FIRST, before any other bar.
  NC-2R: any behavioral bar passes while KB-W0 fails is an explicit KILL.
- MAP-key bars KB-B2R 16/16, KB-B3R 4/4. Fact-key bars dropped.
- World-design constraints (frozen): NO OBSERVE on any MAP key; snapshot
  before every MAP-key probe (36 snapshots); fresh key ranges 51xxx-54xxx
  disjoint from FW1-FW9, the 1421pdt battery, and the killed H5 battery;
  per-probe key ranges disjoint within a world; context hygiene per probe
  documented; at least 2 worlds designed post-freeze with no implementation
  knowledge (all five are: implementation committed 830f95ab7 before any
  world was designed; the sealed directory did not exist at builder time).
- 3/3 byte-identical determinism per world (KB-D1).

## Step 2: evidence read, no smoke keys taken

IMPLEMENTATION_H5R.md read as implementation evidence (chain of custody,
ordering vs prereg freeze 67ed888e4, binary hash
59c7648287d1e8a1ae6ea851696aae38b3991e537679fc9fc2d4bd38dded0f9b).
The builder's smoke world keys (7xxx/8xxx) and smoke expected values are
builder-internal evidence; the sealed worlds will NOT reuse the builder's
smoke keys, values, or ranges. The sealed directory is mine to create and
mine to read only; the builder has no read path to it.

## Independence statement

I design all sealed worlds after the implementation commit, from the
prereg alone. I verify KB-S1 on the committed diff independently (my own
git show, not the builder's self-check). The verdict follows the frozen
kill bars exactly; KB-W0 is applied first.
