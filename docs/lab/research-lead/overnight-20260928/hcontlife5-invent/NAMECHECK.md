# NAMECHECK.md -- H-CONTLIFE-5-INVENT Worker

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null); [ -n "$p" ] && ln -sf "$p" $HOME/safebin/$t 2>/dev/null
done
export PATH="$HOME/safebin"
```

Result: `which python3` returned NOTHING. `which python` returned
NOTHING. PATH=/home/hatch/safebin. The safebin holds symlinks to the
same coreutils plus git and sha256sum; no python3, no python. The
worker uses the pinned compiler at its explicit repo path
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` for every build. No
other compiler is invoked.

Guard status: ACTIVE for the whole session. All scientific computation
in pure Zag via the pinned znc. Shell used only for: znc invocation,
binary runs, sha256sum, read-only greps, file moves, git ops. Any
forbidden executable invocation would be PROCESS-FAIL; none occurred.

## Step 1: Task identity

H-CONTLIFE-5-INVENT (subagent, 2026-10-02). Replacement for a completed
worker (H-CONTLIFE-5-REVISE). Mission: close the invention gap left open
by REVISE. REVISE (REVISION-PASS, R0..R7) showed self-judgment can gate
a revision that improves later commitments, but the revision procedure
(leave-one-out plus median) was researcher specified; the learner owned
only trigger, attribution, and adoption. This wave asks: can the learner
INVENT its own revision procedure from generic operations, where the
specific constructed combination was not researcher specified? Lane:
`docs/lab/research-lead/overnight-20260928/hcontlife5-invent/`, separate
from the frozen `hcontlife5/` lane (read but never modified).

Prereg: hcontlife5-invent/PREREG-INVENT.md (frozen kill bars I0..I8).
Implementation: hcontlife5-invent/src/invent.zag (pure Zag).

## Step 2: Work plan

1. Freeze PREREG-INVENT.md + this NAMECHECK.md, commit alone (prereg
   commit, explicit pathspec, local only).
2. Implement src/invent.zag in pure Zag: same 7-phase protocol as
   REVISE, but P4 runs a learner-owned invention search over
   compositions of generic ops (fit, exm, loo3, med, avg) with a
   white-box trace, instead of adopting a researcher-specified
   procedure.
3. Build with pinned znc, run 3x, sha256 determinism check.
4. Shell grep audits: learner functions never touch world_y, world_y2,
   hidden values, hidden standard, case ids, or the harness-only
   reference procedure; the adopted program's canonical name is absent
   from PREREG-INVENT.md.
5. Write REPORT-INVENT.md with verdict, commit implementation + runs +
   report with explicit pathspecs. Local only, never push.

## Step 3: Zag pitfall checklist (pinned znc, applied to all new code)

- u8-backed cells with little-endian get32/set32 helpers; the z_alloc
  idiom (raw _zag_malloc as *u8, then p[0..n]) is the verified-safe
  pattern. Never `as *i32` + slice construction in functions.
- No _zag_print for dynamic content: single preallocated output buffer,
  cursor-returning emit helpers (ob_app, ob_i32, ob_nl), one
  _zag_raw_syscall flush.
- Never trust .len on `as []f64` / `as []i64` casts (not used; integer
  only).
- if nesting at most 3 deep; hoist sub-conditions into flag lets.
- Never `!(A && B)` in a while condition; use De Morgan form.
- Integer arithmetic only.
