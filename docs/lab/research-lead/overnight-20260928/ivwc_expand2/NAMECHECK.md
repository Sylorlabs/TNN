# NAMECHECK.md -- IVWC-EXPAND2 Worker (Self-checking verifier + law-change limits)

## Step 0: Toolchain Guard (mandatory, executed at worker startup)

Executed before any other work (2026-10-03, this session):

```
export PATH="$HOME/safebin"
which python3   # returned NOTHING (rc=1)
which python    # returned NOTHING (rc=1)
ls ~/safebin | grep -i -E "python|perl|ruby|node"  # no output: no interpreters
```

Result: safebin active at /home/hatch/safebin (36 allowed tools).
`which python3` and `which python` return nothing. No forbidden
interpreter is reachable in PATH. All builds use the pinned compiler
at its explicit repo path
`~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned znc the IVWC baseline and IVWC-EXPAND lanes used).
All scientific computation in pure Zag via the pinned znc. Shell
used only for: znc invocation, binary runs, sha256sum, read-only
greps, file moves, git ops. Any forbidden executable invocation would
be PROCESS-FAIL; none occurred.

Guard status: ACTIVE for the whole session.

## Step 1: Task identity

IVWC-EXPAND2 (subagent, 2026-10-03, non-ledger task, claim minting
paused). Mission: expand internal verification WITHOUT any
expected-answer oracle along the two axes the parent named:
(1) "Can the learner verify its own work? (self-checking?)" --
a learner-owned pre-execution PASS/FAIL verifier trained only on
train consequences, applied to sealed plans before any sealed
outcome signal; (2) "What are the limits? (where does it break?)"
-- a deterministic law-change dial (sealed wall density 15% -> 30%
-> 45%) that must degrade and finally break the carried (frozen)
verifier, while the fresh-consequence revision protocol from
IVWC-EXPAND is re-run for contrast.

Lineage: IVWC baseline (internal_verify/, BUILD-PASS, sealed
calibration 113 vs 116) -> IVWC-EXPAND (ivwc_expand/, BUILD-PASS,
commit -> consequence -> revised-commit -> further-consequence,
sealed 235 vs 223) -> this lane. The sibling lane ivwc_expand/ is
complete and committed (d558aba2f); this worker does FRESH work in
the new sibling lane ivwc_expand2/ and does not touch ivwc_expand/.

Lane: `docs/lab/research-lead/overnight-20260928/ivwc_expand2/`.
Prereg: ivwc_expand2/PREREG.md (frozen kill bars K1..K9, committed
alone before implementation).
Implementation: ivwc_expand2/src/ivwc_expand2.zag (pure Zag, single
file). World, beliefs, composition, consequence simulator and
revision rule are copied VERBATIM from ivwc_expand/src/ivwc_expand.zag
except world_gen takes a wall-probability parameter wp (wp=15
reproduces the baseline/expand sealed worlds bit-identically, which
K7 relies on).

Branch note: this worker was spawned on the shared checkout at
~/workspace/tnn-rsi-gpi3 on branch tnn-native-lab. It stays on this
branch (no branch switch while other workers are active), commits
only its own lane directory with explicit pathspecs, local only,
never pushed. Git writes go through /usr/bin/git directly (the
safebin git symlink is known to fail object/index writes with
EPERM per AGENTS.md XP-HIERNAV-1 lesson).

## Step 2: Work plan

1. Freeze PREREG.md + this NAMECHECK.md, commit ALONE (prereg
   commit, explicit pathspec, local only, never push). Verify the
   prereg commit strictly precedes any implementation commit.
2. Implement src/ivwc_expand2.zag in pure Zag: copied world/learner
   core (wp-parameterized world_gen), new learner-section
   verifier_train / verifier_check (bucket table + learner-computed
   threshold T from train consequences only), train phases
   (setup/commit/conseq, no train revision needed), then a sealed
   shift loop sh=0..2 (wp = 15/30/45) reusing buffers: per shift,
   batched SELFCHECK commit -> in-program K1 check -> frozen-table
   verdicts -> conseq -> metrics; batched REVISION commit1 ->
   in-program K1 check -> conseq1 -> revise+conseq2 (+ empty-evidence
   ablation). In-program K3/K4/K6/K7/K8/K9 provisional computations.
3. Build with pinned znc, run 3x, sha256 determinism check.
4. Run frozen shell audits from PREREG section 5 (A1 ordering, A2
   learner-section truth-token ban, A3 oracle-token ban, A4 no-key
   comparison, A5 sha equality).
5. Write REPORT.md with verdict and numbers, commit
   implementation + binary + runs + report with explicit pathspecs.
   Local only, never pushed.

## Step 3: Zag pitfall checklist (pinned znc, applied to all new code)

- u8-backed cells with little-endian get32/set32 helpers; the z_alloc
  idiom (raw _zag_malloc as *u8, then p[0..n]) is the verified-safe
  pattern, copied verbatim. Never `as *i32` + slice construction in
  functions.
- No _zag_print for dynamic content: single preallocated output
  buffer, cursor-returning emit helpers (ob_app, ob_i32, ob_nl),
  one _zag_raw_syscall flush. ob_i32 handles signs (verdict
  arithmetic stays nonnegative; cross-multiplied comparisons avoid
  floats).
- Never trust .len on `as []f64` / `as []i64` casts (not used;
  integer only). No bitwise `&`, no hex literals; LCG in small
  modulus (25173/13849 mod 65536, no i32 overflow).
- if nesting at most 3 deep; hoist sub-conditions into flag lets.
- Never `!(A && B)` in a while condition; use De Morgan form.
- Integer arithmetic only; parenthesize mixed `-`/`/`.
- Token hygiene for K2 audits: the substrings expected/answer/key/
  target (any case) and correct/reference_plan/gold must not appear
  in the .zag source, including comments and identifiers. Watch out:
  "correction" contains "correct"; "monkey"-style words contain
  "key". Use "fix", "tgt", "plan" phrasing instead.
