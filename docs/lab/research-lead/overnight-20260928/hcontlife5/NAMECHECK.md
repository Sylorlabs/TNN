# NAMECHECK.md -- H-CONTLIFE-5 Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
```

Result: `which python3` returned NOTHING. `which python` returned NOTHING.
PATH=/home/hatch/safebin. The safebin holds symlinks to: awk basename bash
cat chmod cmp comm cp cut date diff dirname echo file find git
git-receive-pack git-upload-pack grep head join ln ls mkdir mktemp mv nl od
paste printf rm sed sh sha256sum sleep sort stat strings tail tee timeout
touch tr uname uniq wc which xargs znc. No python3, no python.

Note: `znc` was not found on the default PATH before safebin setup
(`which znc` inside the loop found nothing), so the safebin has no znc
symlink. The worker uses the pinned compiler at its explicit repo path
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` for every build, which is
the pinned build named in the task. No other compiler is invoked.

Guard status: ACTIVE for the whole session. All scientific computation in
pure Zag via the pinned znc. Shell used only for: znc invocation, binary
runs, sha256sum, read-only greps, file moves, git ops. Any forbidden
executable invocation would be PROCESS-FAIL; none occurred.

## Step 1: Task identity

H-CONTLIFE-5 (subagent, 2026-10-02), replacement for a completed worker.
Mission: close the delayed-consequence loop with LEARNER-OWNED
EVALUATION. The learner commits to a prediction plus a self-derived
tolerance BEFORE consequences arrive; the world later reveals outcomes;
the learner judges its own commitment from its sealed state plus the
observed consequence, with no harness expected answer in its path.
Calibration: agreement with hidden harness judgments on a frozen 24-case
set, bar >= 0.80; no-consequence control must degrade below 0.80.

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit alone (prereg commit).
2. Implement src/selfjudge.zag in pure Zag (one binary, three roles:
   learner / world / harness, function-boundary separation).
3. Build with pinned znc, run 3x, sha256 determinism check.
4. Shell grep audits for K2/K6 (learner functions never touch world_y,
   hidden standard, or hidden judgments).
5. Write REPORT.md with verdict, commit implementation + report with
   explicit pathspecs. Local only, never push.

## Step 3: Zag pitfall checklist (pinned znc, applied to all new code)

- u8-backed cells with little-endian get32/set32 helpers; the z_alloc
  idiom (raw _zag_malloc as *u8, then p[0..n]) is the verified-safe
  pattern. Never `as *i32` + slice construction in functions.
- No _zag_print for dynamic content: single preallocated output buffer,
  cursor-returning emit helpers, one _zag_raw_syscall flush.
- Never trust .len on `as []f64` / `as []i64` casts (not used here).
- if nesting at most 3 deep; hoist sub-conditions into flag lets.
- Never `!(A && B)` in a while condition; use De Morgan form.
- Integer arithmetic only; no division needed (unit x spacing).
