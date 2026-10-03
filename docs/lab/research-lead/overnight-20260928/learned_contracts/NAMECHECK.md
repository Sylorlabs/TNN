# NAMECHECK.md -- LCONT-1 Learned Contracts Worker

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed before any other work:

```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
```

Setup output: `linked: 36 tools`, `znc: OK
(/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
`verify: python3 absent from safebin PATH (OK)`,
`verify: python absent from safebin PATH (OK)`,
`SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
Result: `which python3` returned NOTHING. `which python` returned
NOTHING. PATH=/home/hatch/safebin. The pinned compiler is invoked as
`znc` through the safebin symlink for every build. No other compiler
is invoked.

Guard status: ACTIVE for the whole session. All scientific computation
in pure Zag via the pinned znc. Shell used only for: znc invocation,
binary runs, sha256sum, read-only greps, file moves, git ops. Any
forbidden executable invocation would be PROCESS-FAIL; none occurred.

## Step 1: Task identity

LCONT-1 LEARNED-CONTRACTS (subagent, 2026-10-03). Implements Micah's
LEARNED CONTRACTS directive: types themselves must be learned from
experience; no researcher ontology of INT/BOOL/PLAN/CAUSAL/LANGUAGE/
AUDIO; push experiments where initially insufficient contracts are
refined by failure and consequence. Lane:
`docs/lab/research-lead/overnight-20260928/learned_contracts/`, new
lane, no frozen lanes read.

Mission: the learner starts with one coarse contract kind ("value",
kind 0) for six structures; composition fails on a novel goal family
because the coarse contract filters nothing and evidence points at a
behaviorally incapable structure; the failure triggers a generic
learner-side partition refinement over the learner's own probe table
plus the episode replay; the refined behaviorally distinct kinds make
the identical selection rule succeed. A permutation control (world B:
behaviors permuted across ids) verifies the kinds track observed
behavior, not researcher labels. Prereg: learned_contracts/PREREG.md
(frozen kill bars K0..K6). Implementation: learned_contracts/src/
lcont.zag (pure Zag).

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit alone (prereg commit,
   explicit pathspec, local only). Verify the prereg commit strictly
   precedes any implementation commit.
2. Implement src/lcont.zag in pure Zag: WORLD world_apply (two worlds,
   permutation pi), LEARNER probe/select/refine, HARNESS staged
   protocol A/B/C/D per world, in-program K0..K4 checks, white-box
   trace of signatures and kind assignments.
3. Build with pinned znc via safebin, run 3x, sha256 determinism
   check (K5).
4. Shell grep audits (K6): PREREG.md contains no id-to-refined-kind
   mapping; learner code uses ids only.
5. Write REPORT.md with verdict, commit implementation + runs +
   report with explicit pathspecs. Local only, never push.

## Step 3: Zag pitfall checklist (pinned znc, applied to all new code)

- u8-backed cells with little-endian get32/set32 helpers; the z_alloc
  idiom (raw _zag_malloc as *u8, then p[0..n]) is the verified-safe
  pattern. Never `as *i32` + slice construction in functions.
- No _zag_print for dynamic content: single preallocated output buffer,
  cursor-returning emit helpers (ob_app, ob_i32, ob_nl), one
  _zag_raw_syscall flush.
- Integer arithmetic only. No f64 casts, so the .len-on-cast issue
  does not arise.
- if nesting at most 3 deep; hoist sub-conditions into flag lets.
- Never `!(A && B)` in a while condition; use De Morgan form.
- No ternary operator (not observed in the pinned toolchain's accepted
  corpus); use explicit if/else.
- Use `%` for parity, not bitwise `&` (unseen in corpus).
