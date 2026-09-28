# worker_09 sweep log — chunk_09 (LH-4 / LH-5 / LH-6 / LH-7 toolchain + results)

Date: 2026-09-22. 50 rows swept. 30 effective reviews (20 exact duplicates).

## Deduplication map (sha256-verified)

| Duplicate pair (row → canonical) |
|---|
| LH-5 hello/{diago2,diags,hello,rawprobe,sysprobe}.zag → LH-4 copies |
| LH-5 r34v3/{CLOSURE_20260917,PREREGISTRATION,README,WORKLOG_20260916}.md → LH-4 copies |
| LH-5 r34v3/{r34_continuing_harness_v3,r34_learner_core,wb_whitebox_tests}.zag → LH-4 copies |
| LH-7 R33_CONTINUING_LIFE_V1/{checkpoint,common,observation,storage,world}.zag → LH-5 copies |
| LH-7 {R33_NATIVE_IO_V1,R33_NATIVE_SHA256_V2}.zag → LH-5 copies |
| LH-7 ZAG_PLAYBOOK.md → LH-5 copy |

Every variant tree carries a full copy of the toolchain subtree — expected
(white-box apparatus), not a data problem. Reviews done on the canonical
copy; dups carry `dup:<canonical path>`.

## Per-file notes

### hello probes (LH-4, LH-5)
- `diago2.zag`, `diags.zag`, `diagd.zag`, `diagf.zag`, `diago.zag`, `diag.zag`,
  `sysprobe.zag`, `rawprobe.zag`, `hello.zag`, `add.zag`: syscall/toolchain
  bring-up probes (open flags matrices, getpid, getuid, cstr slicing,
  `add(40,2)->42`). Deterministic, no RNG, no miscompile patterns.
  `add.zag` is the same snippet cited in ZAG_PLAYBOOK §4 as the wasm test.
  PASS each.

### r34v3 docs (LH-4/LH-5, identical)
- `CLOSURE_20260917.md` (2026-09-17): numbers (baseline 8/16, trained
  16/16, return 15/16, 48 updates, update-disabled 0 updates/12/24,
  reward-scrambled 0/16, refusals 2005/2001) consistent with the source
  harness asserts and evidence dirs. Written pre-remediation: does not
  mention the quarantine, but makes no claim the quarantine contradicts.
- `PREREGISTRATION.md`: structural isolation gate (learner imports
  observation contract only; no world/checkpoint/cw_ imports, no cw_ calls)
  matches source — verified by grep (zero `cw_`/`CWOutcome` hits in
  r34_learner_core.zag outside comments). It lists "deterministic RNG"
  as a learner-core feature: that is the quarantined `r34v3_rng` LCG.
- `README.md`: module-boundary claims match source. No stale claims.
- `WORKLOG_20260916.md`: engineering evidence; same LCG documented as a
  feature. Superseded by the 2026-09-20 REMEDIATE ruling.

### r34v3 sources
- `r34_learner_core.zag` (LH-4/LH-5 identical): contains the known
  contamination — `r34v3_rng(s) = (rng*997+7919) % 1000003` at line 15,
  engaged by `r34v3_choose` as `if(explore_enabled==1 &&
  r34v3_mod(r34v3_rng(s),5)==0){obj=1-obj;ex=1;}` — 1-in-5 pseudo-random
  explore flips in the learner's decision path, violating the
  no-randomness law. This is exactly the documented contamination
  (R34 v3 quarantined permanently; LH-4/LH-7 suspended; clean reruns done
  elsewhere). Verdict flags it, matching the contamination notices.
  Tie-break in `r34v3_best` is `s.*.decisions%2` — deterministic,
  state-driven, fine. No `as []i32/[]u32/[]u16` casts, no local-struct
  slice-lets (20 scalar i32 fields only; whole-struct `s.*=t` of the
  80-byte flat struct is fine), no `slice as *u8`, no chained
  `s.field.subfield` through pointer-in-struct. `znc check` OK.
- `r34_continuing_harness_v3.zag` (LH-4/LH-5 identical): full campaign
  harness; all training phases pass `explore=1`, i.e. they engage the
  quarantined explore path. cl_check names/values match CLOSURE numbers
  exactly. `znc check` OK; no miscompile patterns.
- `r34_lh4_harness.zag` (LH-4 only): multi-return evaluator (12 visits ×
  24 train, per-return ≥15/16 gate with updates disabled). Passes
  `explore_enabled` into `r34v3_choose` — tainted leg, same quarantine.
  Evaluator-side logic deterministic and seeded.
- `lh5_corruption_harness.zag` (LH-5 only): corruption RNG is a
  harness-side glibc-style LCG `(state*1103515245+12345) % 2147483647`
  seeded from argv — evaluator-side, deterministic given seed, learner
  core untouched. Delivered flips 46/480, 124/480, 241/480 = 9.6%,
  25.8%, 50.2%, matching RESULT.md's "nominal rates" claim. `znc check`
  OK. One caveat for future crews: `state*1103515245` overflows i32
  before the mod — deterministic on this build (two's-complement wrap),
  but portable only via byte-identical rerun, not math; fine here since
  `deterministic_runs_equal=true` was recorded.
- `wb_whitebox_tests.zag` (LH-4/LH-5 identical): five deterministic groups
  (trace ops, revision rule, lineage chaining, learner-core exactness,
  ledger consistency). No RNG anywhere; uses `cl_check` (correct helper
  per lab convention). `znc check` OK.

### R33_CONTINUING_LIFE_V1 (LH-5/LH-7 identical)
- `checkpoint.zag`: 12-section transport contract, corrupt/torn refusal.
- `common.zag`: bounded wire ops; `cl_u32` returns unsigned i64 and is
  NAMED unsigned — sign-interpreting code (`r34v3_get_signed`) applies
  the ±30000 offset explicitly, consistent with the AGENTS.md
  f3_get32-sign lesson.
- `observation.zag`: encoding/validation only. Pure.
- `storage.zag`: Linux port; `cl_usage` uses `_zag_malloc(144) as *i64`
  pointer indexing — the ZNC-007 scope covered `as []i64` slices (clean),
  and pointer `p[i]` on a single `*i64` cast was never implicated.
  `znc check` OK.
- `world.zag`: seeded Park-Miller LCG `(state*48271) % 2147483647`
  held in world state, tick-updated in `cw_step`, with the comment
  "Unpredictable to a stateless observer; RNG belongs only to the
  world." Evaluator/world-side seeded RNG, deterministic given seed
  (byte-identical world reruns recorded). Not in the learner's decision
  path — law-compliant as documented.

### R33 native substrate (LH-5/LH-7 identical)
- `R33_NATIVE_IO_V1.zag`: Linux syscall substrate. `nio_open_child` with
  create=1 uses flags 657602 = O_RDWR|O_CREAT|O_EXCL — per AGENTS.md
  this makes rewrites to existing files FAIL SILENTLY (fd<0, old content
  kept). The flag is documented in the source comment; checkpoint commit
  paths delete/recreate externally — known pattern, not a bug, but any
  future "rerun output doesn't change" debugging should check this first.
- `R33_NATIVE_SHA256_V2.zag`: pure SHA-256 (RFC6234 constants),
  word-separated, length-checked. No RNG.

### ZAG_PLAYBOOK.md (LH-5/LH-7 identical)
- Compiler SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
  VERIFIED byte-for-byte against
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Import-graph (§6) matches the r34v3 tree as found. §7 isolation-gate
  spec matches source (verified by grep). "Deterministic" checks
  (deterministic_learner/world) are same-seed LCG reruns — deterministic,
  but the RNG-in-decision-path violation stands; the playbook claims no
  law-compliance for them. No stale claims vs known outcomes.

### RESULT / BLOCKED docs
- LH-5 `RESULT.md`: knee at/below 10% matches the known outcome
  (19→181 regime switches). Contamination notice (2026-09-20) is accurate:
  LCG, `(rng*997+7919) mod 1000003`, 1-in-5 flips, explore_enabled=1,
  REMEDIATE, LH-5 suspended. Left-intact original + dated notice — correct
  remediation pattern.
- LH-7 `RESULT.md`: interference hypothesis REJECTED per prereg rule
  (A 15/16 = slow level, B 16/16 = slow level; rule needed ≤12/≤13).
  Probe-order artifact disclosed (A-before-B measured lock-in, not
  knowledge loss; fixed to settled-regime-first, evaluator-side,
  within prereg). Contamination notice accurate.
- LH-6 `BLOCKED.md`: gate applied correctly (no LH-1/LH-2 RESULT.md →
  not built). Contamination notice on its LH-5 citations accurate.

## Kill bars applied mechanically
- LH-5 prereg hypothesis "graceful degradation with measurable knee":
  REJECTED by the data (10% already total per-block collapses) — reported
  as a fragility finding, recorded above.
- LH-7 prereg interference rule (A ≤12 or B ≤13 ⇒ interference):
  15/16 and 16/16 ⇒ NO interference, hypothesis rejected — recorded.

## Findings summary
1. QUARANTINED LCG confirmed in `r34_learner_core.zag`
   (line 15: `(rng*997+7919)%1000003`; line 38: 1-in-5 explore flip) —
   matches all three contamination notices; nothing new, nothing
   contradicting.
2. Harness-side seeded RNGs (LH-5 corruption LCG, world Park-Miller) are
   evaluator-owned and deterministic — law-compliant as documented.
3. O_CREAT|O_EXCL on `nio_open_child` create — known silent-fail pattern
   from AGENTS.md present here; flagged for future debugging awareness.
4. `znc check` OK (capability claims proven) on: r34_learner_core,
   wb_whitebox_tests, diago2, lh5_corruption_harness,
   r34_continuing_harness_v3, storage. Analyzer warnings only (A0102
   unused-result hints).
5. Zero ZNC-004/007/012 miscompile patterns, zero `slice as *u8`
   garbage-read casts across all 18 unique zag files grepped.
6. No stale claims vs known outcomes in any md.

## Rows not evaluable
None — all 50 rows read and verdict'd (30 native reviews + 20
sha256-verified dups).
