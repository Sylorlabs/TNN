# NAMECHECK: rule_revision (Rule Revision Worker)

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

PREREG.md (K-RR-1..K-RR-6, frozen predictions P1..P8) committed ALONE in
57a04ac34, strictly before any implementation source existed.
Commit-order self-check: 57a04ac34 is an ancestor of the implementation
commit and contains exactly one file
(docs/lab/research-lead/overnight-20260928/rule_revision/PREREG.md).

Git incident (transparency note): this worker's first prereg commit
attempt raced concurrent lanes on the shared git index. The `git add`
failed on a stale index.lock held by the l2_l3_combo worker; the
immediately following `git commit` then swept that lane's staged files
under this worker's prereg message (commit 857bdb896). On the next
command the same pattern recurred in reverse: a `git commit --amend`
swept the xdomain_causal_l2 worker's staged PREREG.md. Both were repaired
before proceeding: 857bdb896's message was amended to describe the
l2_l3_combo content, then the xdomain_causal_l2/PREREG.md file was
unstaged (`git rm --cached`, file left intact and untracked in the
worktree for its worker) and the commit amended again, yielding
9e604e183 whose tree is exactly the 11 l2_l3_combo files (verified by
`git diff --name-only fb1075ef0 HEAD`). The clean prereg commit
57a04ac34 was then made with an explicit single-file pathspec and
verified to contain exactly PREREG.md. No lane lost files; all working
trees intact. Lesson: on this shared repo, verify `git show --stat HEAD`
after every commit and never assume the index holds only your files.

## Step 2: implementation (pure Zag, safebin only)

- rr_mech.zag: output helpers, state cells, world facts, probe_kind
  (real H1 kind rule), comp_run/comp_first/comp_second, obs_append
  (learner observation log), h1_observe/h1_finalize (real H1 majority
  rule), rule_induce (generic CONSTANT induction from the obs log),
  rule_pred (rule predicate application; the only prediction path, no
  lookup list exists), h1_predict_rule, learner_commit, world_execute,
  world_downstream (fixed accept-iff-goal-kind law), world_gate,
  learner_update, learner_refute (generic blame walk; appends each probe
  outcome to the obs log), learner_refine (generic first-deviation
  split), learner_select.
- rr_main.zag: driver; phases TEACH, Z2, REFUTE, REVISE, RETEST,
  REGRESS, GENERALIZE, Z4, Z5; transcript emission; main().
- rr_full.zag: assembled (cat mech main).
- build.sh: guard + kill-bar source checks + compile + 3x run.

## Step 3: build

First build attempt panicked at runtime (`panic: slice index out of
bounds`, zero stdout): the learner state slice was z_alloc(256) = 64
i32 cells but the layout uses cells up to 76 (77 cells = 308 bytes).
Fixed by sizing L to z_alloc(320); no logic change. `znc rr_full.zag -o
rr_bin`, exit 0 (compile.txt). rr_bin sha256:
1cef3b9abd26c69c2e56652fcf41044307cbc537d2584e192888cd3e884b9465.
rr_full.zag sha256:
59e0014158243861015bf5bc7868a62e219a72efba225e33b81bd4ea07b2450b.

## Step 4: runs

run1.txt, run2.txt, run3.txt all exit 0. sha256 (all three):
fa93199d9c7737cef608f97cdd057c9b7859889d7f9da4f1ead4aecc99aeb93b.
cmp pairwise: identical. DETERMINISM-OK: 3/3 byte-identical.
8/8 frozen predictions matched (see REPORT.md).

## Step 5: kill-bar source checks (from build log)

- grep -ci 'expected' over both sources: 0, 0.
- gate write sites (`set32(E,0`): exactly 1 (inside world_downstream,
  rr_mech.zag line 292).
- `fn learner_refute` definitions: 1. `fn learner_refine`: 1.
  `fn rule_induce`: 1. `fn rule_pred`: 1. `fn learner_update`: 1.
  `fn learner_select`: 1. `fn h1_finalize`: 1.
- rule-cell writes (`ls(L,rb`): exactly 6 total: 2 inside rule_induce
  (rr_mech.zag lines 243-244), 4 inside learner_refine (lines 377-380).
  Zero rule writes anywhere else.
- learner_refute / learner_refine bodies contain no 33/34/30 literals
  (build.sh sed-scoped check returns 0,0); the revision content comes
  only from the observation-log and counterexample cells, never from
  researcher constants.
- exception machinery occurrences (`grep -ci 'exception'`): 0, 0. No
  lookup list exists in the program.
- mode/bridge/handler occurrences: 0, 0 (the rule form selector is
  named rule_form).
- `as *i32` occurrences: 0, 0.
- K-RR-4 unseen-input check: `grep -c 'OBS D in=34\|OBS D in=30'`
  run1.txt returns 0: inputs 34 and 30 were never probed.

## Step 6: commits (explicit pathspecs, local only, never pushed)

- 57a04ac34: PREREG.md alone.
- Implementation commit: the branch-tip commit titled
  "rule_revision: implement learner-owned rule refinement ..." containing
  NAMECHECK.md, REPORT.md, rr_mech.zag, rr_main.zag, rr_full.zag,
  build.sh, rr_bin, compile.txt, run1/2/3.txt, sha256sums.txt
  (12 files, explicit pathspecs).
