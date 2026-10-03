# NAMECHECK: contract_revision (Contract Revision Worker)

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
guard at build time (exits 1 if python3/python resolve).

Toolchain lessons honored (AGENTS.md): u8-backed state cells with
little-endian get32/set32 (no `as *i32` slice construction); all dynamic
output formatted into ONE preallocated buffer via cursor-returning emit
helpers with a single `_zag_raw_syscall(1,1,ptr,len)` write (no _zag_print
for dynamic content); no `as []f64` casts; no WAV reads.

## Step 1: prereg frozen alone

PREREG.md (K-CR-1..K-CR-6) committed ALONE in 26966e353, strictly
before any implementation source existed. Commit-order self-check:
26966e353 is an ancestor of the implementation commit and contains
exactly one file
(docs/lab/research-lead/overnight-20260928/contract_revision/PREREG.md).

## Step 2: implementation (pure Zag, safebin only)

- cr_mech.zag: output helpers, state cells, world facts, probe_kind (real
  H1 kind rule), comp_run, h1_observe, h1_finalize (real H1 majority
  rule), exception-list contract storage, contract_pred (value-keyed,
  exception-aware), h1_predict_exc, learner_commit, world_execute,
  world_downstream (fixed accept-iff-goal-kind law), world_gate,
  learner_update, learner_refute (generic blame walk over the committed
  chain, learner-initiated probes), learner_revise (generic exception
  append from the counterexample cells), learner_select.
- cr_main.zag: driver; phases TEACH, Z2, REFUTE, REVISE, RETEST,
  REGRESS, Z4, Z5; transcript emission; main().
- cr_full.zag: assembled (cat mech main).
- build.sh: guard + kill-bar source checks + compile + 3x run.

## Step 3: build

`znc cr_full.zag -o cr_bin`, exit 0 (compile.txt). cr_bin sha256:
bdfde9649cef0af41f503fd17338704536e45f3407450fbc99fbbcb4b37fc919.

## Step 4: runs

run1.txt, run2.txt, run3.txt all exit 0. sha256 (all three):
3fb5c30379994cab20e7c83d833ac4e0903599596c9bae22c2f6832ffc4886b5.
cmp pairwise: identical. DETERMINISM-OK: 3/3 byte-identical.

## Step 5: kill-bar source checks (from build log)

- grep -ci 'expected' over both sources: 0, 0.
- gate write sites (`set32(E,0`): exactly 1 (inside world_downstream).
- `fn learner_refute` definitions: 1. `fn learner_revise`: 1.
  `fn h1_finalize`: 1.
- signature-cell writes (`ls(L,base+4` / `ls(L,base+5`): exactly 2,
  both inside h1_finalize. Zero hardcoded signature writes.
- exception-cell writes (`ls(L,xb`): exactly 3, all inside
  learner_revise. Zero exception writes anywhere else.
- learner_refute / learner_revise bodies contain no 33 or 34 literals
  (build.sh sed-scoped check): the revision content comes only from the
  counterexample cells, never from researcher constants.
- mode/bridge/handler occurrences: 0, 0.
- `as *i32` occurrences: 0, 0.

## Step 6: commits (explicit pathspecs, local only, never pushed)

- 26966e353: PREREG.md alone.
- Implementation commit: the branch-tip commit titled
  "contract_revision: implement learner-owned contract revision ..."
  containing NAMECHECK.md, cr_mech.zag, cr_main.zag, cr_full.zag,
  build.sh, cr_bin, compile.txt, run1/2/3.txt, sha256sums.txt,
  REPORT.md (12 files, explicit pathspecs).
