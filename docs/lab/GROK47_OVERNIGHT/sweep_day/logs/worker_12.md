# worker_12 log — chunk_12 (50 rows: 18 md + 32 zag)

Reviewed 2026-09-22 (PT). Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
No commits, no manifest edits, no external actions. All build artifacts went to /tmp/sweep12.

## Coverage
- All 50 listed files verified present; MD5-hashed every row.
- 38 rows reviewed individually; 12 rows are exact byte duplicates → verdict `dup:<canonical>` (canonical = first path in chunk order).
- Spot builds+run on the pinned znc: `sep_trial.zag`, `curiosity_unit.zag`, `dc_pilot.zag` (s1 + s4 legs), `hyp_core/trial.zag` (std curriculum). All `znc check` clean; all builds + runs exit 0.

## Per-file notes (concise)

### wave2 ruleslab (4 rows)
- `sweep_p3_adaptive_eps_12345/trial.zag` — fixed A/B/return driver, seed 12345. Driver itself has no RNG; explore RNG is in the sibling `learner_core.zag` (not assigned in this chunk, inspected for context): seeded LCG `trl_rng` (`rng*997+7919 mod 1000003`), coin-flip explore in `trl_choose`, identical file in the eps_999 dir (md5 b19e41ad…).
- `sweep_p3_adaptive_eps_999/episode.zag` — canonical episode harness (dup target for baseline + hyp_core). No RNG in harness. Verified `trl_accept` requires `(reward!=1 && reward!=-1)`, matching world.zag's `o.value=±1` convention — coherent.
- `sweep_p3_adaptive_eps_999/learner_core.zag` — seeded LCG drives explore flips in `trl_choose`. RNG in this historical sweep variant's decision path; deterministic given seed but eps-explore-by-coin (remediation-era pattern). Stale files `trial`/`trial_p3` binaries sit in both sweep_p3 dirs (build artifacts, noted not cleaned).
- `sweep_p3_adaptive_eps_999/trial.zag` — fixed driver, seed 999; pairs with above.

### wave2 whitebox (2 rows)
- `READER_BLOCKED_SPECS.md` — precise blocked specs; consistent with STATE_SCHEMA; no stale claims vs known outcomes.
- `WHITEBOX_TESTS.md` — 43/43 claim consistent; contamination note correctly quarantines the R34-campaign reference while the whitebox tests stay untainted per workstream 2/8. Stale-claim check: none.

### wave3 INDEX (1 row)
- `INDEX.md` — 14 positive / 2 mixed / 3 negative / 1 blocked matches known outcomes; next-step (integrate the five mechanisms, developmental curriculum at 10x) consistent with program law.

### core/user separation (10 rows)
- `PREREG.md` — complete falsifiable prereg (H1–H6), law-compliant (no RNG, designed adversary, byte-identical determinism clause).
- `SEPARATION_DESIGN.md` — internally consistent; open items N1–N5 honestly scoped as specified-not-trialed.
- `TRIAL_RESULTS.md` — 127/127 CONFIRMED; my rebuild reproduces it (MA_FAILURES,0, MA_DONE, reruns byte-identical); scale honestly bounded (60-op trial, 8 user slots).
- `trial/sep_core.zag` — integer-only, no RNG; `[]u8` arenas with explicit accessors (ZNC-007-safe); invariants I1–I4 implemented as specified. Local-struct-value field reads (`sep_i32_get(s.owner,0)`) build clean on the pinned znc (no ZNC-004 trigger here).
- `trial/sep_trial.zag` — rebuilt+ran: exit 0, 127 CL_CHECK lines, MA_FAILURES,0, MA_DONE; two runs byte-identical.
- `trial/substrate/*` (5 files) — IO: `as *u8` cast is on the `_zag_malloc` return, not slice-as-`*u8` (ZNC-002 n/a); SHA256 V2: bounded native, no flags; cl/common: wire helpers, no flags; cl/observation: envelope codec + sha256 check; cl/world: world-side LCG tick documented ("RNG belongs only to the world"), never read by learner decision paths — compliant. All five are canonical copies for dups in the dc + hde trees.

### curiosity substrate (6 rows)
- `PREREG.md` — BLOCKED amendment honest. Doc-hygiene note: TRIAL_RESULTS renumbers the criteria F1–F5 vs prereg F1–F4 (substance preserved, mapping inferable: F2 split into F2+F3). No silent edit of originals.
- `SUBSTRATE_ANALYSIS.md` — source-accurate; verified the 1e300→1e18 compiler-literal port diff is present in current source (`1e18` in `curiosity_v1_native.zag`).
- `TRIAL_RESULTS.md` — BLOCKED verdict honest: apparatus failure, not substrate vacuity; full trial + round-robin crashed (ZNC-2026-09-19-001, deterministic codegen corruption); unit math passed; modes 2/3 partial traces cannot satisfy prereg. Matches INDEX.
- `curiosity_trial.zag` — deterministic, zero RNG; source side clean.
- `curiosity_unit.zag` — rebuilt+ran: WB_FAILURES,0, TOOLCHAIN_DEFECT=0, all three repo assertions hold (consistent with docs: simple contexts are unaffected).
- `curiosity_v1_native.zag` — RNG-free substrate; port diff documented at the line.

### developmental curriculum (11 rows)
- `CURRICULUM.md` — design doc internally consistent; DC-0 exit gate (MA1 58/58) matches known outcomes; DC-1 pilot status matches PILOT_RESULTS; contamination note present and correctly scoped.
- `PILOT_RESULTS.md` — P1–P7 claims reproduced by my rebuild (see below); contamination note quarantines tainted LH-5 quantities while keeping pattern references descriptive.
- `PREREG.md` — complete falsifiable prereg with program-law amendments; P3 bound-scoping documented as an amendment in results, not a silent edit.
- `pilot/dc_ctx_core.zag` — no RNG; `[]u8` arenas with explicit zeroing (belt-and-braces vs the playbook); no miscompile patterns; `_zag_arg(1)` read ungated (ZNC-007-safe).
- `pilot/dc_pilot.zag` — rebuilt+ran s1 and s4: both DC_FAILURES,0, DC_COLLAPSED_BLOCKS,0, curriculum switches 7/13 = prereg flips, DC_DONE; two s1 runs byte-identical. Note: `dc_build_reg_s4` has ~13-deep nested `else` chains (ZNC-2026-09-21-013 pattern) — verified harmless in practice: the regime table executed correctly and schedules matched the prereg flips on this binary. Still logged for future toolchain work.
- `pilot/substrate/*` (5 files) — exact dups of the separation-arm canonicals (see dup list).

### hypothesis-driven exploration (14 rows)
- `DESIGN.md` — mechanism-as-designed verified in source; RNG-free core claim holds (grep-clean); baseline LCG explicitly the beaten adversary.
- `PREREG.md` — amendments A1–A3 honestly chronologized (A1/A2 pre-run, A3 post-observation); prereg kill bars F1–F5 explicit.
- `TRIAL_RESULTS.md` — NEGATIVE verdict applied mechanically per F2: flap 12>5, storm 20>5 explores (hypothesis side). My rebuild reproduces the std leg train positives 76/80 exactly. HDE total 191/240 vs baseline 189/240; F1 pass (+2 margin noted as weak-but-pass); F3/F4/F5 pass. Kill bar applied: F2 FAIL → NEGATIVE stands.
- `evidence/RECEIPT.md` — all six source sha256 hashes match the current files byte-for-byte; rerun-log hashes pair with primaries (verified the three binary-hashes are distinct from source hashes, matching the doc's claim).
- `impl/baseline/episode.zag`, `impl/hyp_core/episode.zag` — exact dups of the ruleslab canonical.
- `impl/baseline/learner_core.zag` — seeded LCG drives epsilon-greedy 1/5 explore flips; documented adversarial baseline (prereg-allowed), not the system under test; R34-v3 pattern; arm dead (HDE NEGATIVE).
- `impl/baseline/trial.zag` — fixed five-curriculum driver, seed 7331. **Toolchain finding:** the `_zag_argc()==2` gate and `_zag_arg(1)` read verified WORKING at runtime (hde_trial ran with `std` argv correctly) — no ZNC-007 trigger for this path on the pinned znc; the recorded defect (argc=0 to `main`) does not apply to `_zag_argc()` here.
- `impl/hyp_core/learner_core.zag` — genuinely RNG-free (no rng/rand/seed tokens anywhere); fixed tie-breaks, deterministic hypothesis confirmation/refutation; RECEIPT hash matches current file byte-for-byte.
- `impl/hyp_core/trial.zag` — rebuilt+ran std curriculum: exit 0, train_total pos=76/80, TRL,DONE; argv path works.
- `impl/substrate/*` (5 files) — exact dups of the separation-arm canonicals (see dup list).

### hypothesis-state substrate (2 rows)
- `PREREG.md` — falsifiable (P1–P7, F1–F4), law-compliant, explicit scale dimension with named next scale test. No result file in this chunk; no claims to verify beyond internal consistency.
- `SUBSTRATE_ANALYSIS.md` — source-accurate v1→HSS mapping (read against repo source); gaps (no commit rule, no refutation, no audit, no score machinery) honestly named.

## Duplicate map (12 rows)
| dup row | canonical |
|---|---|
| `wave3/developmental-curriculum/pilot/substrate/R33_NATIVE_IO_V1.zag` | `wave3/core-user-separation/trial/substrate/R33_NATIVE_IO_V1.zag` |
| `wave3/developmental-curriculum/pilot/substrate/R33_NATIVE_SHA256_V2.zag` | `wave3/core-user-separation/trial/substrate/R33_NATIVE_SHA256_V2.zag` |
| `wave3/developmental-curriculum/pilot/substrate/cl/common.zag` | `wave3/core-user-separation/trial/substrate/cl/common.zag` |
| `wave3/developmental-curriculum/pilot/substrate/cl/observation.zag` | `wave3/core-user-separation/trial/substrate/cl/observation.zag` |
| `wave3/developmental-curriculum/pilot/substrate/cl/world.zag` | `wave3/core-user-separation/trial/substrate/cl/world.zag` |
| `wave3/hypothesis-driven-exploration/impl/baseline/episode.zag` | `wave2/ruleslab/impl/sweep_p3_adaptive_eps_999/episode.zag` |
| `wave3/hypothesis-driven-exploration/impl/hyp_core/episode.zag` | `wave2/ruleslab/impl/sweep_p3_adaptive_eps_999/episode.zag` |
| `wave3/hypothesis-driven-exploration/impl/substrate/R33_NATIVE_IO_V1.zag` | `wave3/core-user-separation/trial/substrate/R33_NATIVE_IO_V1.zag` |
| `wave3/hypothesis-driven-exploration/impl/substrate/R33_NATIVE_SHA256_V2.zag` | `wave3/core-user-separation/trial/substrate/R33_NATIVE_SHA256_V2.zag` |
| `wave3/hypothesis-driven-exploration/impl/substrate/cl/common.zag` | `wave3/core-user-separation/trial/substrate/cl/common.zag` |
| `wave3/hypothesis-driven-exploration/impl/substrate/cl/observation.zag` | `wave3/core-user-separation/trial/substrate/cl/observation.zag` |
| `wave3/hypothesis-driven-exploration/impl/substrate/cl/world.zag` | `wave3/core-user-separation/trial/substrate/cl/world.zag` |

## Kill-bar accounting
- HDE PREREG F2 (test storms ≤ 5 on flap/storm; hypothesis must not explore): **FAILED** (12, 20). Applied mechanically → NEGATIVE stands, as documented.
- HDE F1 (+2 margin): pass; F3 (no RNG in HDE core): pass (grep-clean); F4 (byte-identical reruns): pass per receipts; F5 (all five F's gate): N/A — F2 failed.
- Curiosity PREREG criteria (F1–F4, or F1–F5 in results): **not evaluable** — apparatus blocked (ZNC-2026-09-19-001). Documented as BLOCKED, not converted to a negative; correct per "apparatus failure ≠ criterion failure."
- DC-1 prereg P1–P7: **all pass** on my rebuild (S1+S4, DC_FAILURES,0, switches=flips, reruns byte-identical) → POSITIVE stands.
- SEP1 prereg H1–H6: **all pass** on my rebuild (127 checks, byte-identical) → CONFIRMED stands.
- No other kill bars referenced by chunk rows.

## Findings (9, in order of importance)
1. **LCG explore in wave2 sweep_p3 adaptive-eps variant learner_core** (both seeds, identical file; only trial.zag assigned): seeded LCG `trl_rng` drives explore flips in `trl_choose` — RNG in a historical sweep variant's decision path. Deterministic given seed, but eps-explore-by-coin is the remediation-era pattern. Flagged, not passed-through as law-compliant.
2. **LCG explore in HDE baseline learner_core** — seeded epsilon-greedy (1/5 explore rate). Prereg explicitly documents it as the beaten adversarial baseline (not the system under test); arm is dead (HDE NEGATIVE). Allowed-by-prereg but recorded per sweep rules.
3. **world.zag world-side LCG tick** — documented in source as world-only ("RNG belongs only to the world"); no learner decision path reads it. Compliant with the law (the world can be unpredictable; the mind can't be dice). No violation.
4. **_zag_argc() works on the pinned znc** — `hde_trial std` ran correctly through the `_zag_argc()==2` gate. The recorded ZNC-007 defect (argc=0 to `main`) does not apply to `_zag_argc()` in these binaries; `_zag_arg(1)` reads fine. Resolves a stale/reproducibility concern for the HDE + DC pilots.
5. **Deep else-nesting in dc_pilot.zag** (~13 deep in `dc_build_reg_s4`; ZNC-2026-09-21-013 pattern) — verified harmless in practice: schedules executed correctly, switches matched prereg flips on the pinned binary. Logged for future toolchain work, not a result-changer.
6. **Curiosity PREREG↔TRIAL_RESULTS criterion renumbering drift** (F1–F4 vs F1–F5) — doc-hygiene issue only; substance preserved, no claim invalidated.
7. **HDE RECEIPT integrity positive** — all six source sha256 match current files byte-for-byte; no drift between evidence and source.
8. **12 exact duplicates across trees** — documented in dup map; canonical = earliest chunk-order path. No divergence.
9. **Stray binaries `trial`/`trial_p3` in both sweep_p3 dirs** — untracked build artifacts sitting in source dirs; not cleaned (not my task).

## Build evidence (pinned znc, /tmp/sweep12)
| binary | result |
|---|---|
| sep_trial | exit 0; MA_FAILURES,0; MA_DONE; 127 checks; two runs byte-identical |
| cur_unit | exit 0; WB_FAILURES,0; TOOLCHAIN_DEFECT=0 |
| dc_pilot (no arg → s1) | exit 0; DC_SCALE,s1; DC_COLLAPSED_BLOCKS,0; switches 7; DC_FAILURES,0; DC_DONE; rerun byte-identical |
| dc_pilot s4 | exit 0; DC_SCALE,s4; switches 13; DC_FAILURES,0; DC_DONE |
| hde_trial std | exit 0; train_total pos=76/80 (matches TRIAL_RESULTS); TRL,DONE |

## Unevaluable rows
None — all 50 rows evaluated (38 unique reviews + 12 exact duplicates).
