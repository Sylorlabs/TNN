# NAMECHECK.md -- IVWC Worker (Internal Verification via World Consequences)

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed before any other work:

```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3   # returned NOTHING (rc=1)
which python    # returned NOTHING (rc=1)
```

Result: safebin ready at /home/hatch/safebin (36 tools, no python).
`which python3` returned NOTHING. `which python` returned NOTHING.
PATH=/home/hatch/safebin. The worker uses the pinned compiler at its
explicit repo path
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` for every build. No
other compiler is invoked.

Guard status: ACTIVE for the whole session. All scientific computation
in pure Zag via the pinned znc. Shell used only for: znc invocation,
binary runs, sha256sum, read-only greps, file moves, git ops. Any
forbidden executable invocation would be PROCESS-FAIL; none occurred.

## Step 1: Task identity

IVWC (subagent, 2026-10-02). Mission: design an experiment where the
learner commits to a composition output WITHOUT seeing the expected
answer, then receives world consequences (environmental feedback, not
a score), updates its own confidence/usefulness evaluation from those
consequences, and we test whether the self-evaluation predicts future
performance (calibration).

Lane: `docs/lab/research-lead/overnight-20260928/internal_verify/`.
Prereg: internal_verify/PREREG.md (frozen kill bars K1..K6).
Implementation: internal_verify/src/ivwc.zag (pure Zag, single file).

Branch note: the task instruction said to work on `tnn-native-lab`,
but this worker was spawned on the shared checkout at
`lane-hcontlife5-20261002` with other workers active and uncommitted
staged changes in the index. Switching branches would move the working
tree under active workers (same disruption class as the forbidden
`git reset` on a shared branch). Per AGENTS.md shared-workspace
discipline, this worker stays on the current branch, commits only its
own lane directory with explicit pathspecs, and reports the deviation
to the parent.

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit alone (prereg commit,
   explicit pathspec, local only, never push).
2. Implement src/ivwc.zag in pure Zag: 1D corridor world, noisy
   beliefs, learner_compose (NAV+GATHER composition), world_execute
   (physics simulator producing consequences), learner_update
   (per-bucket calibration table), sealed evaluation, no-feedback
   ablation arm, shuffled-feedback secondary arm.
3. Build with pinned znc, run 3x, sha256 determinism check.
4. Run frozen shell audits from PREREG section 5 (no expected-answer
   tokens; learner section free of world-truth tokens; commit-before-
   execute code ordering; in-program K1/K3 structural checks).
5. Write REPORT.md with verdict and calibration numbers, commit
   implementation + runs + report with explicit pathspecs. Local only.

## Step 3: Zag pitfall checklist (pinned znc, applied to all new code)

- u8-backed cells with little-endian get32/set32 helpers; the z_alloc
  idiom (raw _zag_malloc as *u8, then p[0..n]) is the verified-safe
  pattern. Never `as *i32` + slice construction in functions.
- No _zag_print for dynamic content: single preallocated output buffer,
  cursor-returning emit helpers (ob_app, ob_i32, ob_nl copied verbatim
  from hcontlife5-condrev), one _zag_raw_syscall flush.
- Never trust .len on `as []f64` / `as []i64` casts (not used; integer
  only). No bitwise `&`, no hex literals (not observed in the pinned
  toolchain corpus); bit tests via division/modulo, LCG in small
  modulus (25173/13849 mod 65536, no i32 overflow).
- if nesting at most 3 deep; hoist sub-conditions into flag lets.
- Never `!(A && B)` in a while condition; use De Morgan form.
- Integer arithmetic only; parenthesize mixed `-`/`/`.
