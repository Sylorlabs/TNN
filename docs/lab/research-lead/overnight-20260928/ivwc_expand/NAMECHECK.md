# NAMECHECK.md -- IVWC-EXPAND Worker (Multi-step Internal Verification via World Consequences)

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed before any other work:

```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
# output: linked: 36 tools; znc: OK (.../znc_linux_x86_64_abed8aa1)
#         verify: python3 absent from safebin PATH (OK)
#         verify: python absent from safebin PATH (OK)
#         SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
export PATH="$HOME/safebin"
which python3   # returned NOTHING (rc=1)
which python    # returned NOTHING (rc=1)
which znc       # /home/hatch/safebin/znc
```

Result: safebin ready at /home/hatch/safebin (36 tools, no python).
`which python3` returned NOTHING. `which python` returned NOTHING.
`ls ~/safebin | grep -i -E "python|perl|ruby|node"` returned nothing:
no interpreters in the safebin. PATH=/home/hatch/safebin. The worker
uses the pinned compiler at its explicit repo path
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` (in the
tnn-rsi-gpi3 worktree, tnn-native-lab branch) for every build. No
other compiler is invoked.

Guard status: ACTIVE for the whole session. All scientific computation
in pure Zag via the pinned znc. Shell used only for: znc invocation,
binary runs, sha256sum, read-only greps, file moves, git ops. Any
forbidden executable invocation would be PROCESS-FAIL; none occurred.

## Step 1: Task identity

IVWC-EXPAND (subagent, 2026-10-02). Mission: expand IVWC (baseline
BUILD-PASS at C361: learner commitment -> world consequence ->
learner-owned evaluation, K1-K6, sealed calibration 113 vs 116) to
the harder multi-step variant: commitment -> consequence -> REVISED
commitment -> further consequence. The learner revises its NAV+GATHER
composition from pure physics evidence (per-action position+outcome
log: MOVE_OK/BUMP_LEFT/BUMP_RIGHT/GATHER_HIT/GATHER_MISS) with no
harness-supplied expected answer at any step; the further
consequences of the revised plan validate the revision on sealed
cases. Addresses Micah's priority #4 (reduce dependence on
harness-supplied expected answers), extended from calibration to
revision.

Lane: `docs/lab/research-lead/overnight-20260928/ivwc_expand/`.
Prereg: ivwc_expand/PREREG.md (frozen kill bars K1..K6, committed
alone before implementation).
Implementation: ivwc_expand/src/ivwc_expand.zag (pure Zag, single
file).

Branch note: this worker was spawned on the shared checkout at
~/workspace/tnn-rsi-gpi3 on branch tnn-native-lab. It stays on this
branch (no branch switch while other workers are active), commits
only its own lane directory with explicit pathspecs, local only,
never pushed.

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit alone (prereg
   commit, explicit pathspec, local only, never push). Verify the
   prereg commit strictly precedes any implementation commit.
2. Implement src/ivwc_expand.zag in pure Zag: same 1D corridor
   world/beliefs as the IVWC baseline (frozen parameters and seeds
   copied verbatim), world_execute extended with a per-action
   evidence log (physics outcomes only), learner_revise (belief
   correction from evidence + recomposition), batched phases
   COMMIT1/CONSEQ1/REVISE/CONSEQ2 on train, sealed COMMIT1/CONSEQ1/
   REVISE+CONSEQ2 with empty-evidence ablation arm and
   shuffled-evidence secondary arm, in-program K1a/K1b/K3 checks.
3. Build with pinned znc, run 3x, sha256 determinism check.
4. Run frozen shell audits from PREREG section 5 (A1a/A1b ordering,
   A2 learner-section truth-token ban, A3 answer-token ban, A4 no-key
   comparison, A5 sha equality).
5. Write REPORT.md with verdict and numbers, commit
   implementation + binary + runs + report with explicit pathspecs.
   Local only, never push.

## Step 3: Zag pitfall checklist (pinned znc, applied to all new code)

- u8-backed cells with little-endian get32/set32 helpers; the z_alloc
  idiom (raw _zag_malloc as *u8, then p[0..n]) is the verified-safe
  pattern. Never `as *i32` + slice construction in functions.
- No _zag_print for dynamic content: single preallocated output
  buffer, cursor-returning emit helpers (ob_app, ob_i32, ob_nl),
  one _zag_raw_syscall flush. Signed emit needed for pred_gain
  (can be negative): reuse the ob_i32 sign handling from the
  baseline.
- Never trust .len on `as []f64` / `as []i64` casts (not used;
  integer only). No bitwise `&`, no hex literals; bit tests via
  division/modulo, LCG in small modulus (25173/13849 mod 65536, no
  i32 overflow).
- if nesting at most 3 deep; hoist sub-conditions into flag lets.
- Never `!(A && B)` in a while condition; use De Morgan form.
- Integer arithmetic only; parenthesize mixed `-`/`/`.
- Token hygiene for K2 audits: the words expected/answer/key/target
  (any case) and correct/reference_plan/gold must not appear in the
  .zag source, including comments. Use `tgt` (not the banned word)
  for plan legs.
