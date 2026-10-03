# NAMECHECK: verify_h1 (Verify-H1 Integration Worker)

## Step 0: toolchain guard (mandatory, recorded)

Executed at worker start, 2026-10-02:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned NOTHING (no output before
"guard-check-done"). PATH restricted to $HOME/safebin only. No forbidden
executable invoked at any point in this lane. build.sh re-verifies the
guard at build time (exits 1 if python3/python resolve); build log shows
"guard: python3/python absent, znc=/home/hatch/safebin/znc".

Toolchain lessons honored (AGENTS.md): u8-backed state cells with
little-endian get32/set32 (no `as *i32` slice construction; grep count 0
in both sources); all dynamic output formatted into ONE preallocated
buffer via cursor-returning emit helpers with a single
`_zag_raw_syscall(1,1,ptr,len)` write (no _zag_print for dynamic content);
no `as []f64` casts; no WAV reads.

## Step 1: prereg frozen alone

PREREG.md (K-VH-1..K-VH-6) committed ALONE in 3e5014de3, strictly before
any implementation source existed. Commit-order self-check: 3e5014de3 is
an ancestor of the implementation commit and contains exactly one file
(docs/lab/research-lead/overnight-20260928/verify_h1/PREREG.md).

## Step 2: implementation (pure Zag, safebin only)

- vh_mech.zag (231 lines): output helpers, state cells, world facts,
  probe_kind (real H1 kind rule), comp_run, h1_observe, h1_finalize
  (real H1 majority rule), h1_predict (contract application),
  learner_commit, world_execute, world_downstream (fixed
  accept-iff-goal-kind law), world_gate, learner_update, learner_select.
- vh_main.zag (133 lines): driver; phases TEACH, Z1, Z2, Z3, ABL;
  transcript emission; main().
- vh_full.zag: assembled (cat mech main). sha256
  ddea46a9be97e3537734937d1b285cdbf8b8e12d94107ea70f316b53342271d1.
- build.sh: guard + kill-bar source checks + compile + 3x run.

## Step 3: build

`znc vh_full.zag -o vh_bin`, exit 0 (compile.txt). vh_bin sha256:
2a4ed2cc521230f00e1acd0a3a0fe476c696d3318da03d6e02447ac1d8914922.

## Step 4: runs

run1.txt, run2.txt, run3.txt all exit 0. sha256 (all three):
4f8cfa34a3f625b2ea29cd36721cf9795f7b2d176b29ae72dd47b2ed46e9fef3.
cmp pairwise: identical. DETERMINISM-OK: 3/3 byte-identical.

## Step 5: kill-bar source checks (from build log)

- grep -ci 'expected' over both sources: 0, 0.
- gate write sites (`set32(E,0`): exactly 1 (vh_mech.zag line 195,
  inside world_downstream).
- `fn learner_select` definitions: 1. `fn learner_update`: 1.
  `fn h1_finalize`: 1.
- signature-cell writes (`ls(L,base+4` / `ls(L,base+5`): exactly 2,
  vh_mech.zag lines 145 and 151, both inside h1_finalize. Zero
  hardcoded signature writes.
- mode/bridge/handler occurrences: 0, 0.
- `as *i32` occurrences: 0, 0.

## Step 6: commits (explicit pathspecs, local only, never pushed)

- 3e5014de3: PREREG.md alone.
- Implementation commit: NAMECHECK.md, vh_mech.zag, vh_main.zag,
  vh_full.zag, build.sh, vh_bin, compile.txt, run1/2/3.txt,
  sha256sums.txt, REPORT.md (explicit pathspecs; see REPORT.md).
