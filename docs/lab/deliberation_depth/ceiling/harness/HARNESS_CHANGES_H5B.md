# H5B harness changes (vs frozen `harness_v2`)

H5's harness (`deliberation_depth/harness_v2/`) is FROZEN and untouched.
H5B carries its own harness revision: a full copy of `harness_v2/` under
`ceiling/harness/` with the changes below. The authoritative exact record
is `HARNESS_DIFF_H5B.txt` (unified diff of the three changed files).

## Why the harness changed

The residual-flip bound must be evaluated inside the deliberation loop
(it needs per-round scores, alive-sets, and the unconsumed evidence tail),
so it cannot be a config-only change. The parent task explicitly allows
harness changes if documented exactly — this file is that documentation.

## Changed files (3 of 9 sources; the rest byte-identical)

### 1. `dlb_delib.zag`
- **New function `dlb_bound_fires(st:*DSt, it:*Item) -> i32`** (the bound):
  1 iff the remaining unconsumed evidence provably cannot flip the current
  leader. For leader L (argmax over alive, ties → lowest index) and each
  alive runner-up R: `maxR = S_R + Σ remaining supports(R)`,
  `minL = S_L − Σ remaining attacks(L)`. R cannot overtake L iff
  `maxR < minL`, or (`maxR == minL` and `R > L`, since ties break to the
  lower index). Attacks on R and supports for L are omitted (they only
  strengthen L's case). Soundness: dead hypotheses never return,
  mid-stream ELIMINATE/TEST only remove contenders, and the leader never
  trails itself, so the lead can only change by score overtake. Vacuously
  true when no runner-up is alive (the leader is then final).
  Consequence: a bound-stop verdict always equals the run-to-exhaustion
  verdict (the bound guarantees "same as exhaustion", NOT "correct").
- **`dlb_run`: new `mode==3` branch** — after the ROUND bookkeeping, stop
  iff `r >= adaptive_max_rounds` (recorded `cap=1`, same as adaptive) or
  `dlb_bound_fires()` returns 1. Natural termination (top-of-loop and
  `progress==0`) is unchanged. The §6 rule is NOT active in bound mode —
  the bound replaces it, so the two rules are measured head-to-head.
- **New `stopwhy` variable** (first cause wins): 1=fixed, 2=six, 3=bound,
  4=natural, 5=cap. Set at every existing stop point without changing any
  stop *condition* (the `stop==0`/`cap==1` mechanics are byte-for-byte the
  H5 semantics; `stopwhy` is purely observational).
- **`dlb_d_verdict` takes a new `why:[]u8` parameter**; the VERDICT ledger
  detail gains ` stop=fixed|six|bound|natural|cap`. The results.jsonl
  schema is unchanged (stop reasons are read from the ledger).

### 2. `dlb_cfg.zag`
- `mode=bound` parses to mode value 3 (`dlb_cfg_mode_name(3) = "bound"`).
  The value 3 was previously unused (0=shallow, 1=deep, 2=adaptive).

### 3. `CONFIG_FORMAT.md`
- Documents `mode=bound` and its semantics; notes which config keys are
  active in bound mode (`adaptive_max_rounds` as the hard cap,
  `elim_margin`, `refute_threshold`, `evidence_cap`) and which remain
  required-but-ignored (format stability).

## Unchanged

`delib_harness.zag`, `dlb_json.zag`, `dlb_ledger.zag`, `dlb_util.zag`,
`R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`, `build.sh` — all
byte-identical to `harness_v2/` (verified by `diff -q`).

## Bound design decision (preregistered)

The implemented bound sums the ACTUAL remaining weights (the tightest
provable "cannot flip" statement). The per-evidence weight ceiling
(max |weight| = 500 per link, fixed per evidence type in both encoding
specs) is what makes those sums exact rather than estimated. A looser
`remaining_count × 500` ceiling variant fires on a PROVEN subset of the
exact version's firings (margin > 2·R·500 ⟹ maxR < minL), so the exact
measurement upper-bounds any ceiling-variant: if the exact bound shows no
strict improvement over §6 somewhere, no looser ceiling variant would
either. The key discriminating case (plateau-then-flip: §6 stops at round
5, bound refuses) is identical under both formulations.

## Verification status

- Built twice with the pinned znc toolchain; byte-identical binaries required.
- Smoke tests (shallow/deep/adaptive) must reproduce `harness_v2` behavior;
  bound mode smoke-tested on prototype items (see prereg §9).
- A/B byte-identical results+ledgers required for all 108 sweep cells.
