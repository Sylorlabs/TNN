# worker_13 — manifest sweep log (chunk_13, 50 rows)

Date: 2026-09-22. Worker: subagent (depth 2). Method: native review primary —
read all 10 md files, grepped all 40 zag files for RNG + znc miscompile
patterns, spot-`znc check`ed 6 drivers/modules, verified evidence bundles
(SHA256SUMS, byte-identical reruns). grok-4.7 not needed (no ambiguities
required a second opinion).

## A. Scope

Four wave-3 trial dirs: hypothesis-state-substrate (4), learner-driven-switching
(12), lifecycle-as-advisor (12), native-structural-revision (22). No jsonl/py
rows in this chunk.

## B. Verdict tallies

- PASS: 23
- review (finding attached): 11
- dup: 16 (byte-identical copies; see §D)
- Not evaluable: 0

## C. Findings

### C1. RNG audit — no randomness in any TNN decision path (PASS)

Scanned all 40 zag files for `rng|rand(|srand|/dev/urandom|getrandom|seed`.

- `ht2_learner.zag`: **0 hits** for `rng|episode|clock` — PREREG_HT2's static
  bar verified independently.
- `ctx_core.zag`, `sr_core.zag` (all copies), `hss.zag`,
  `r34_hypothesis_state_v1.zag`, `adv_*.zag`, `ma_common.zag` (except dead
  helper, §C3): no RNG tokens outside "no RNG" attestation comments.
- RNG found only in harness/world-side, seeded, prereg-declared scaffolding:
  - `trial_ht2.zag`: `ht_next` seeded streams for curriculum R flip sequence
    + 15% channel noise (world side). Curriculum A is zero-RNG. Declared in
    PREREG_HT2 amendment log. PASS.
  - `trial_sr.zag` (all copies): `sr_lcg_next` used only in `sr_gen_cue` /
    `sr_flip` for the SHIFT-LCG arm's cue values and measurement flips
    (arm==1 only). The mechanism path (`sr_diagnose/propose/promote/rollback`)
    takes batch hit counts, never the LCG. Declared in SR PREREG as
    "seeded harness LCG as explicitly-tolerated scaffolding". PASS.
  - `substrate/cl/world.zag` (ht2 + advisor copies): LCG in `cw_step` is the
    *world* model; comment explicitly states "RNG belongs only to the world".
    Not in any decision path. PASS (flagged as review so the scope is visible).
- `toy_core.zag` (R34 v3, quarantined lineage): LCG + random-explore branch
  present, but `r34v3_choose(t,0,&was)` — explore_enabled=0 at the only call
  site, so `r34v3_rng` is never invoked (short-circuit). The 357-switch storm
  is reproduced via table dynamics, not RNG. Kept strictly as the
  expected-negative control — consistent with the R34 v3 quarantine.
  Verdict: review (lineage noted, no active RNG).

### C2. znc miscompile-pattern scan (all 40 zag) — clean

- ZNC-007 (`as []i32/[]u32/[]u16` consecutive same-size casts): **zero
  occurrences** in the chunk.
- `slice as *u8` (ZNC-2026-09-21-002): all `as *u8` hits are
  `_zag_malloc(n) as *u8` — malloc-to-pointer casts, not slice casts. Clean.
- ZNC-004 (annotated slice-let off a LOCAL struct value): all annotated
  `let x:[]u8` are from `nio_alloc`, `p[0..n]`, `_zag_i64_to_str`, `nio_cstr`.
  Clean.
- ZNC-012 (chained `s.field.subfield` through pointer-in-struct): zero
  occurrences. Codebase consistently uses byte arenas + explicit
  `_get/_put` accessors (the AGENTS.md-recommended style).
- `zalloc` name collision: none. `nio_alloc(N) as *Struct` (ZNC-005): none —
  `nio_alloc` returns `[]u8` directly.
- Stray `};`: all hits are struct-literal initializers in `let` statements
  (required semicolons) or inside comments. Clean.
- `_zag_arg`: no uses.

### C3. Dead code — `ma_common.zag`

`ma_rng_next` (LCG helper) is defined but **never called** anywhere in the
advisor trial (only the definition greps). Harmless but a leftover; recommend
removal at next edit. Verdict: review.

### C4. Stale claim — SR DESIGN.md §2

§2 still says "expected: 2 promotes, 0 rollbacks on the designed SHIFT".
Amendment A3 added the designed dip curriculum (eps 10–11), which adds one
rollback; the amended prereg predicts "2 promotes, 1 rollback" and
TRIAL_RESULTS shows 6 diag / 2 prom / 1 rb. The design doc predates A3 and
was not updated. Verdict: review (stale expectation; amendment is
authoritative). Recommend an amendment note in DESIGN.md.

### C5. Kill bars applied mechanically

- **HSS** (TRIAL_RESULTS): falsification tripwires F1–F4 armed; argmax
  control is harness-only (`trial.zag`); commit-region code tokens verified
  free of `conf`/claims/score state (49 `hss_check` call sites match the
  49/49 claim). None fired. PASS.
- **HT2** (PREREG_HT2 criteria 1–9): report claims all met; code supports it
  (38 `cl_check` sites match 38/38; learner static bar verified; per-episode
  doubt/switch attribution matches the prereg's expected totals:
  doubts 13, switches 11, explained 1, overturned 1). PASS.
- **Advisor** (PREREG §6): POSITIVE required wins in all 6 cells AND
  acceptance in (0.05, 0.95); NEGATIVE required zero advice wins OR
  acceptance outside the band. Observed 2 wins / 0 losses / 4 ties,
  acceptance 98/164 = 59.8% → MIXED, correctly applied. 19 CL_CHECK lines =
  3 per-cell × 6 cells + 1 determinism check. PASS.
- **SR** (PREREG falsification criteria): SHIFT ≥1 promote on all 3 seeds
  (observed 2/seed); SHIFT−FROZEN R1 endpoint diff = 10/16 ≥ 5 gate;
  NO-SHIFT 0 promotes (churn gate); white-box gates all 0 errors;
  byte-identical double runs verified via cmp on run1/run2.stdout.
  SCALE: 9 promotes = 9 inversions, r1ep 13/16, finalep 26/32 — matches the
  results table exactly. PASS.

### C6. Evidence integrity (native-structural-revision)

- `EVIDENCE_20260920T002523Z`: `sha256sum -c SHA256SUMS` → all OK;
  `cmp run1.stdout run2.stdout` → IDENTICAL; receipt shows
  `checks_total=94 checks_bad=0`, `system_rng_symbols=none`,
  `core_isolation=ok`.
- Failure trail preserved and consistent with the attempt narrative:
  002045Z → SR_FAILURES,35 (attempt 1); 002155Z → 17, 002251Z → 15
  (attempt 2); 002401Z/002407Z/002513Z/002519Z/002523Z → 0 (attempt 3).
  Honest negatives kept as evidence. PASS.

### C7. znc spot typechecks (pinned toolchain abed8aa1) — all OK

1. `wave3/hypothesis-state-substrate/trial.zag` — OK (analyzer string-buffer
   warnings only, non-fatal).
2. `ht2/ht2_learner.zag` — OK.
3. `ht2/trial_ht2.zag` — OK.
4. `trial/adv_gate_test.zag` — OK.
5. `trial/adv_trial.zag` — OK.
6. `EVIDENCE_20260920T002523Z/trial_sr.zag` — OK (in scratch dir with
   substrate symlink; evidence dirs don't vendor substrate/, so
   `@import("substrate/cl/common.zag")` fails if checked in place —
   expected per the AGENTS.md substrate lesson; the bundle's own
   compile.stdout shows the original build succeeded).

## D. Duplicates (16 rows → dup:<canonical>)

GitHub check: `docs/lab/wave3` is **not committed** (404), and code search
for `R33_NATIVE_IO_V1` returns 0 hits repo-wide — none of these files are
exact duplicates of already-committed files. The dup verdicts below mark
within-workspace byte-identical copies so the commit step dedupes:

- Substrate vendored ×3 → canonical
  `wave3/learner-driven-switching/ht2/substrate/…`:
  advisor copies (R33_NATIVE_IO_V1, R33_NATIVE_SHA256_V2, cl/common,
  cl/observation, cl/world) + native-structural-revision copies
  (R33_NATIVE_IO_V1, R33_NATIVE_SHA256_V2) — 7 rows.
- `sr_core.zag`: 002401Z/002407Z/002513Z/002519Z/002523Z evidence copies →
  canonical `wave3/native-structural-revision/sr_core.zag` (5 rows);
  002251Z copy → canonical `…/EVIDENCE_20260920T002155Z/sr_core.zag` (1 row).
- `trial_sr.zag`: 002407Z → canonical `…/EVIDENCE_20260920T002401Z/trial_sr.zag`
  (1 row); 002513Z + 002519Z → canonical
  `…/EVIDENCE_20260920T002523Z/trial_sr.zag` (2 rows).

## E. Consistency vs known outcomes

No contradictions found. Cross-checks: HT2 numbers match the known
"357-switch storm / 16/16 endpoints" outcome; SR arms predate the
strength-trial ruling-1 context (different mechanism, no conflict);
advisor references MA3's signed-values recommendation (consistent with
MA4 18/18); HSS's argmax-falsification control is the same shape as the
class-3 teacher-quality debate's implementation-artifact lesson
(controls must be real mechanisms, and here the control is real).

## F. Open questions / recommended follow-ups

1. `ma_common.zag`: remove dead `ma_rng_next` (C3).
2. SR DESIGN.md §2: add amendment note for the A3 rollback expectation (C4).
3. Evidence dirs don't vendor `substrate/` — fine for the bundle format, but
   a future re-verifier must reconstruct the import root (C7.6).
4. grok-4.7 not used (0/5 calls); native review sufficed.
