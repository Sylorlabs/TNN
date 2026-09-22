# ADAPTIVE DELIBERATION — CODING ARM: OPERATIONAL SPEC (FROZEN)

**Date frozen:** 2026-09-22 · **Arm:** adaptive-deliberation coding ·
**Parent prereg:** `coding/reflection/speed_intel/PREREG_ADAPTIVE.md`
(commit `242725975e62c018bf9cba5751136a692d2a204e`, branch `tnn-native-lab`).
**Authority:** Micah 2026-09-22 — no hardcoded think-count; TNN chooses per
decision how many reconsideration rounds to spend. Adaptive only.
**Work dir:** `coding/reflection/speed_intel/work_adaptive_code/` (this file's directory).
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

No trial run (policy cell) starts before this file is committed. Battery
construction pilots (fresh items, control learner only — §7) are
calibration, not trial runs, per the SI precedent
(`work_a1/battery_si_notes.md` "piloted at budget 16").

## 1. Round, cost, and the bar (frozen)

- **Coding round** = one driver iteration (gen → compile → diagnose → repair).
- The learner's existing stop judgments (pass = compile OK ∧ tests byte-match;
  honest halts `halt-genfail`, `halt-no-patch`, `halt-cycle`, `halt-thrash`,
  `halt-runtime`, `halt-noregen`, `halt-unknown`) are **untouched** in every policy.
- Adaptive policies modulate **only**: (i) the per-item iteration budget the
  learner **requests** and the driver **grants** (subject to a hard cap), and
  (ii) the in-round repair/extend/halt predicates below. Nothing else.
- **Fixed-2× baseline (frozen):** `work_a1/driver_si.py --budget 4` on
  `work_a1/battery_si.json` → 18/18 fixable, honest-halt 2/2, 46 total
  iterations, 27 znc invocations. Mean cost: **2.30 iters/item**, 1.35 znc/item
  (RESULTS_SI.md coding slice).
- **Kill bars (frozen, PREREG_ADAPTIVE §8):** WIN = quality ≥ 18/18 AND
  honest-halt 2/2 AND mean iters/item < 2.30 on the frozen battery. FAIL =
  (i) mean cost ≥ 2.30 at equal quality, (ii) any quality/honest-halt
  degradation, or (iii) non-determinism across the 3 reruns. "No adaptive
  policy beats fixed-2×" is an allowed verdict.

## 2. Binaries (frozen)

- **Byte-identical control:** `work_a1/learner`
  (sha256 `399bf907d06c111b1d62164f2fd826ffac524e6b9a3c3c5dca7ffea6e9669375`),
  built from frozen `work_a1/learner.zag`. Untouched. Control cells run it
  via the frozen `work_a1/driver_si.py --budget 4`.
  A verified copy lives at `work_adaptive_code/learner_ctl` (same sha256);
  control *runs* use the original path so there is no doubt.
- **Adaptive binary:** `work_adaptive_code/learner_adapt`, built from
  `work_adaptive_code/learner_adapt.zag` =
  `work_a1/learner.zag` **plus** new §14 (adaptive) only. Every pre-existing
  function is byte-identical to the frozen source; the diff is purely
  additive (new mode, new helpers, three gated call-sites in `do_diagnose`).
  All reasoning in pure Zag; zero RNG; deterministic.
- **Driver:** `work_adaptive_code/driver_adapt.py`, a copy of
  `work_a1/driver_si.py` with exactly these plumbing changes:
  (1) `LEARNER` → `work_adaptive_code/learner_adapt`;
  (2) `--policy {a,b,c,d,e}` CLI arg (experiment constant, like `--budget`;
  passed to the learner's `diagnose` as argv[9]);
  (3) per-item budget-request protocol (§3) before the loop;
  (4) loop bound = granted budget; per-item log adds `requested`, `granted`;
  (5) report adds `policy`.
  The driver makes no coding decisions: the grant is `min(max(req,1),16)`
  (resource plumbing, like `--budget`); `BUDGET <n>` parsing is
  sentinel-style (first line only, default 16 on unparseable — same pattern
  as `GEN_SENTINELS`); the policy tag is never branched on for content.
  Grep-verified against the INTERFACE.md law (§8).

## 3. Budget-request / grant protocol (all policies)

Before the loop (after `gate`, before gen/seed), the driver calls:

```
learner_adapt budget <policy> <spec> <item-mode> <seed-or-empty> <patterns> <demo> <card>
```

The learner prints exactly `BUDGET <n>\n`. The driver grants
`G = min(max(n,1),16)` iterations for the item and logs `requested=n`,
`granted=G`. Hard cap for every policy: **16 iterations**.

**Request rule** (`do_budget`, pure Zag):
- Policies **a, b, c** → `n = 16`. The stop/extend rules do the work; the
  request is headroom only.
- Policies **d, e** → the learner's own difficulty judgment `budget_request`:
  - item-mode `gen` → `n = 2` (one gen round + one repair headroom; the
    learner judges T4-goal specs low-difficulty but non-zero-uncertainty —
    generation itself is the uncertain step).
  - item-mode `seed` → `n = 1 + class_count_src(seed) + goal_extra`,
    clamped to [1,16], where:
    - `class_count_src` = number of distinct defect classes with a positive
      **source-only** signal (no compiler evidence, no reference paths, no
      answer keys — only the seed text):
      - SYNTAX: `review_braces(src)==0`
      - DUPFN: some defined name has `count_def ≥ 2`
      - NAME: some called name is neither `fn_defined` nor `is_intrinsic`
        (`unknown_calls`: identifier immediately followed by `(`)
      - ARITY: `patch_arity` applies for some defined name (try on scratch,
        discard), **or** for some unknown called name U with nearest similar
        defined name D, `param_count(D) ≠ call_argc(U)` (masked-arity: the
        defect is hidden behind the misspelled name)
      - TYPE: `patch_ret_word`, `patch_arg_unquote`, or `patch_del_badassign`
        applies on scratch (first wins)
      - OUTPUT_FORMAT: source contains `_zag_print` but no `\n` (backslash-n)
        literal anywhere
    - `goal_extra` = 1 if the seed's spec begins with `T4|GOAL`, else 0.
      Rationale (the learner's own signal): a seed carrying a goal spec —
      not just "repair this" — may have wrong *logic*, which no source-only
      signal can detect; the learner budgets one round of logic-uncertainty.
      (Covers S08/F08: NAME is visible, LOGIC_VALUE is not.)

## 4. Per-round extend / halt predicates (learner-side, pure Zag)

`do_diagnose` reads the policy tag from argv[9] (`""` = control behavior).
The primary evidence-driven diagnosis (`diag_compile`/`diag_test`) and the
thrash/cycle guards run **unchanged** first. Then, only when the primary
strategy is not `halt-*`:

- **(b)/(e) verify-extend** (`verify_extend`, only when `evtype == COMPILE`):
  an *independent* re-derivation of the repair. Independent = it uses only
  the source text (no compiler evidence) and a different code path from the
  primary evidence-driven classifier. Loop (max 3 passes):
  1. Scan the current source, classes in fixed order
     SYNTAX → DUPFN → NAME → ARITY → TYPE → OUTPUT_FORMAT, and apply the
     first applicable patch (`patch_brace`; `patch_dupfn` per defined name;
     `patch_unknownfn` per unknown called name; `patch_arity` per defined
     name; `patch_ret_word`/`patch_arg_unquote`/`patch_del_badassign`;
     `patch_add_newline` only if braces balance AND the source prints AND
     no `\n` literal exists — the most speculative patch, guarded).
     Every patch function returns 0 when it has nothing to do, so
     re-scanning a fixed class is a safe no-op; each application is logged
     `VERIFY-EXTEND+1:<CLASS>` in the trace.
  2. If a full pass applies nothing → `VERIFY-AGREE+1:no-further-defect`
     ("halt when it agrees": the round's repair loop halts when the
     independent re-derive agrees the source is clean) → round ends.
  3. If ≥1 extension applied, the emitted strategy is `verify-multi`
     (driver treats it as continue — it does not start with `halt-`); the
     `class`/`score` stay the primary's. If 0 applied, strategy is the
     primary's and the trace records `VERIFY-AGREE+1:single-fix-sufficient`.
  - TEST rounds are excluded: behavioral defects (LOGIC_VALUE/RUNTIME)
    need execution evidence; source-only speculation is too risky there.
    The next round's compile+test is the verifier for those.
- **(c)/(e) diminishing-evidence halt** (`check_diminishing`):
  `PREV`/`STALLED`/`CYCLE` come from the driver's trailer (unchanged).
  Let `(pc, ps)` = previous round's (class, strategy), `(cc, cs)` = current.
  If `pc ≠ "none"` AND `cc == pc` AND `cs == ps` → the iteration yielded
  **no new diagnostic information** vs the previous round → trace
  `DIMINISH+99:no-new-diagnostic-information`, strategy overridden to
  **`halt-hopeless`**, source left unchanged. (Halt judgments for
  `halt-*` primaries are untouched; this only fires on non-halt primaries
  that repeat the previous round's diagnosis exactly.)
  Known limitation (documented, not hidden): the predicate compares
  (class, strategy), not the raw evidence bytes — two same-class diagnoses
  over genuinely different evidence would compare equal. On the frozen
  battery the predicate is expected to be inert (every round fixes a
  different class); the cell measures exactly that.

## 5. The five policies (frozen)

| policy | name (frozen intent) | request (§3) | per-round (§4) | cap |
|---|---|---|---|---|
| (a) | stop-at-unanimity | 16 | control diagnose; stop = compile-OK ∧ tests-byte-match made explicit (the existing success stop; the unanimity predicate is STOP ⟺ rc==0 ∧ all vectors byte-match) | 16 |
| (b) | stop-at-verification-agreement | 16 | primary + verify-extend; round halts when the independent re-derive agrees | 16 |
| (c) | stop-at-diminishing-evidence | 16 | control diagnose + halt-hopeless on no-new-information | 16 |
| (d) | uncertainty-routed | difficulty judgment (§3) | control diagnose | 16 |
| (e) | cost-capped adaptive (combination) | difficulty judgment (§3) | verify-extend + diminishing-halt | 16 |

No other policies. (e) is the cheap combination named in PREREG_ADAPTIVE §4
("combinations like d+e"); (b) is inside it.

**Learner's own signals (no peeking):** routing/extension criteria use only
information available to the learner at decision time — the spec, the
current source, the evidence envelope, the PREV/STALLED/CYCLE trailer.
Reference repair paths (`battery_si_notes.md`, `battery_adaptive_fresh_notes.md`)
and test expectations are never consulted by the learner. The driver never
sees them either (it reads only id/mode/spec/seed/patterns/demo/card/tests).

## 6. Cells and driver invocations

Run from `coding/reflection/speed_intel/`. `<R>` ∈ {1,2,3}.

- **Control (frozen battery):**
  `python3 work_a1/driver_si.py work_a1/battery_si.json --budget 4 --workdir work_adaptive_code/sweep_adapt/ctl_frozen_r<R>/run --out work_adaptive_code/sweep_adapt/ctl_frozen_r<R>/run.json`
- **Control (fresh battery):**
  `python3 work_a1/driver_si.py work_adaptive_code/battery_adaptive_fresh.json --budget 4 --workdir work_adaptive_code/sweep_adapt/ctl_fresh_r<R>/run --out work_adaptive_code/sweep_adapt/ctl_fresh_r<R>/run.json`
- **Policy P ∈ {a,b,c,d,e} (frozen battery):**
  `python3 work_adaptive_code/driver_adapt.py work_a1/battery_si.json --policy P --workdir work_adaptive_code/sweep_adapt/P_frozen_r<R>/run --out work_adaptive_code/sweep_adapt/P_frozen_r<R>/run.json`
- **Policy P ∈ {a,b,c,d,e} (fresh battery):** same with
  `work_adaptive_code/battery_adaptive_fresh.json` and `P_fresh_r<R>`.

12 cells × 3 reruns = 36 runs. Canonical form (timing-free) must be
byte-identical within each cell (sha256 of canonical JSON).

**Harness sanity gate (before the sweep):** policy (a) on the frozen battery
must reproduce the control cell's per-item outcomes and `iters_used`
exactly — the budget protocol and policy plumbing are behavior-neutral.
If not, stop and diagnose; do not proceed.

## 7. Fresh battery (secondary, anti-overfit)

`work_adaptive_code/battery_adaptive_fresh.json` — **12 items**, same
construction discipline as `battery_si.json` (SI notes §"build notes"):
new seeds from the same defect classes (2–3 classes each, new combinations),
new T4 gen specs composing ≥2 KB patterns, new SHAs, reference paths
recorded in `work_adaptive_code/battery_adaptive_fresh_notes.md` and never
exposed to the learner. Piloted at budget 16 with the **frozen control
learner** (`work_a1/learner` + `work_a1/driver_si.py`) to record reference
paths and confirm hardness by iteration floor (seeds need 3–4 control
iterations; gen items first-try; X5 halts). Also committed before any policy
trial run. SHA-disjointness vs `battery_si.json` (on seed+spec bytes) is
checked by script and reported; the SI-Arm-1 extended crew's lists are
epistemic-side (`work_a1x/`); no coding extended battery from another crew
exists in the repo — if one appears before analysis, overlap is checked by
SHA and reported.

Designed items (seeds frozen by this spec; reference paths recorded at pilot):

| id | classes (design) | seed sketch | expected |
|---|---|---|---|
| F01 | DUPFN, ARITY | dup `fn add`, call `add(4,5,6)` | `9\n` |
| F02 | TYPE, OUTPUT_FORMAT | `add("4",5)` (i32), no trailing newline | `9\n` |
| F03 | SYNTAX, DUPFN | dup `fn dbl`, unclosed `main` | `42\n` |
| F04 | NAME, OUTPUT_FORMAT | `mul2(6,7)` → `mul`, no trailing newline | `42\n` |
| F05 | DUPFN, ARITY, TYPE | dup `fn add`, call `add("3",4,5)` | `7\n` |
| F06 | SYNTAX, NAME, OUTPUT_FORMAT | `sbu(10,4)` → `sub`, unclosed main, no `\n` | `6\n` |
| F07 | TYPE, NAME | `return "42";` in `i64` fn + call `answr()` → `answer` | `42\n` |
| F08 | NAME, LOGIC_VALUE | `fibsm(6)` → `fibsum`, off-by-one fib sum; spec `T4\|GOAL\|compute the sum of the first 6 fibonacci numbers` | `20\n` |
| G11 | gen (p_math+p_loop) | `T4\|GOAL\|compute the sum of the prime numbers below 40` | `197\n` |
| G12 | gen (p_math+p_loop) | `T4\|GOAL\|compute the sum of the first 8 fibonacci numbers` | `54\n` |
| G13 | gen (p_sort+p_search) | `T4\|GOAL\|sort the numbers 9,2,7,4,6 with selection sort` | `2 4 6 7 9\n` |
| X5 | unfixable (NAME, no similar) | `qqzx` accumulator, no similar defined name | halt-no-patch |

If piloting shows a seed needs ≠3–4 control iterations (or a gen item is
not first-try, or X5 does not halt), the seed is reworked within the same
discipline until it pilots clean — battery construction, not a result.

## 8. Metrics and verdict (per policy × battery)

`work_adaptive_code/analyze_adapt.py` computes: Q_c (fixable pass /18 frozen,
/11 fresh), honest-halt (X items with `halt-*`, /2 frozen, /1 fresh),
mean iters/item, FULL rounds histogram (`iters_used` distribution),
max iters/item + item IDs, total znc invocations (per-iter records with
evtype ∈ {COMPILE, TEST}, same counting rule as `run_sweep_si.py`), total
wall-clock, canonical sha256 per rerun (must be 1 distinct digest per cell),
plus per-policy: requested-vs-granted table (d/e calibration), count of
`verify-multi` rounds and `VERIFY-EXTEND` applications (b/e), count of
`halt-hopeless` firings (c/e).

**Ceiling (required):** per policy, max rounds ever actually spent, on how
many items (count + fraction), and which item IDs — read off the data.

Deliverable: `work_adaptive_code/ADAPTIVE_VERDICT.md` with the policy×battery
quality/cost table (including the fixed-budget-4 baseline row), the rounds
histograms, the discovered ceiling per policy, per-policy verdict
(WIN/FAIL vs §1 kill bars), and the champion policy (or NONE).

## 9. Standing laws

Zero RNG in decision paths. Byte-identical reruns. Pure Zag for reasoning;
Python is glue (drivers, analysis, commits). No binaries or `.zagd` caches
committed. Commits via `~/workspace/commit_racefree.py` from
`~/workspace/tnn-lab` with `TMPDIR=~/workspace/tmp_commit`, lab-relative
paths not starting with `docs/lab/`.
