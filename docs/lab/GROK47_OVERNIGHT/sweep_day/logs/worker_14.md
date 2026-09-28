# worker_14 — manifest sweep log

**Chunk:** GROK47_OVERNIGHT/sweep_day/chunks/chunk_14.tsv · **Rows:** 50 · **Date:** 2026-09-22
**Unique hashes:** 39 (11 exact-duplicate rows, 5 groups). All 50 rows evaluable — none missing.

## Deduplication (sha256)

| Hash prefix | Canonical path | Dup rows |
|---|---|---|
| 8aec83cb | wave3/native-structural-revision/substrate/cl/common.zag | self-model-substrate/trial/substrate/cl/common.zag, teaching-without-tables/trial/substrate/cl/common.zag, unified-partition-slots/substrate/cl/common.zag |
| 0ff371c4 | wave3/native-structural-revision/substrate/cl/observation.zag | unified-partition-slots/substrate/cl/observation.zag |
| 092085ad | wave3/native-structural-revision/substrate/cl/world.zag | unified-partition-slots/substrate/cl/world.zag |
| e6379ddb | wave3/self-model-substrate/trial/substrate/R33_NATIVE_IO_V1.zag | teaching-without-tables ×1, unified-partition-slots ×1, whitebox-at-scale ×1 |
| 9824f6db | wave3/self-model-substrate/trial/substrate/R33_NATIVE_SHA256_V2.zag | teaching-without-tables ×1, unified-partition-slots ×1, whitebox-at-scale ×1 |

All dups are byte-identical; canonical = first occurrence in chunk order.

## Independent verifications performed

Recompiled + reran four trial binaries with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`), all exit 0 and reproduced claimed verdicts:
- sm_trial.zag → `SM_FAILURES,0`
- twt_trial.zag → `TWT_FAILURES,0`
- trial_upt1.zag → `UPT1_FAILURES,0`
- comp.zag → `COMP_FAILURES,0`
wasm characterization spot-confirmed: `znc: wasm codegen error: call to unknown function` on a trivial `_zag_println` file — matches PORTABILITY.md §2a.
comp.stripped.zag verified byte-identical to comment-stripped comp.zag (595 normalized lines) — the static no-RNG check ran on the real source.
Evidence bundles opened and counts cross-checked: SM1 (26 checks, SM_FAILURES,0, rng_grep empty), TWT (2 runs × TWT_FAILURES,0), UPT1 (18 checks, UPT1_FAILURES,0), comp (92/92, double-run byte-identical), SR (5 latest bundles SR_FAILURES,0; earlier bundles show 35/17/15 failures — intermediate attempts consistent with the driver's "bug found in attempt 2" comment), WB3 (2469 CL_CHECK lines, WB_FAILURES,0).
Toolchain SHA in SM1 TRIAL_RESULTS.md (498abcb5…) matches the actual pinned binary.

## Per-file notes

### zag — substrate + trials
1. **cl/common.zag** (×4): bounded wire helpers (copy/u32/put/zero/hash/disjoint). No RNG. No znc miscompile patterns: no `as []i32/u32/u16` consecutive-cast aliasing, no annotated slice-let off a local struct, no `slice as *u8` (`_zag_slice_ptr` then `as i64` only), no chained `s.field.subfield`. PASS.
2. **cl/observation.zag** (×2): TNNOBS01 encode/check, CLStream through `*CLStream` params — the ZNC-010-approved pattern. PASS.
3. **cl/world.zag** (×2): environment-side deterministic Park-Miller LCG `(seed*48271)%2147483647`, seeded from world state; module header says "NEVER imported by the learner" and "RNG belongs only to the world". This is environmental determinism, not a decision-path RNG — compliant. PASS.
4. **trial_sr.zag**: `sr_lcg_next` (1103515245/12345) is used ONLY for arm-1 (SHIFT-LCG) harness stimulus — cue values and flip sampling — explicitly labeled "seeded harness scaffolding only" in the header; seeded deterministically (seeds 11/22/33). The learner policy path (`sr_diagnose/propose/promote/rollback/record`) lives in sr_core.zag, which I grepped: zero rand matches. No miscompile patterns. PASS with note.
5. **r34_self_model_v1.zag** (ref): two-timescale delta-rule prediction substrate; matches SELF_MODEL.md's description (inverse-error-EMA blend, delayed outcomes only, explicit non-goals in header). No RNG, no miscompile patterns. **BUT**: does NOT compile with the pinned toolchain — E0010 parse error at line 76: `let ae:f64=if(e<0.0){-e}else{e};` (inline if/else as expression). This is a 2026-09-16 toolchain dialect drift; the file is reference-only (NEVER WIRED IN, and the SM1 trial does not depend on it), so no verdict is affected. Flagged as **review** — should be annotated or kept only as a text artifact.
6. **r34_self_model_v1_tests.zag**: matches documented substrate behavior (20× two-strategy delayed outcomes, utility ordering, state/counts equality); unbuildable only because of the above import. Same review flag.
7. **sm_trial.zag**: zero RNG; all field access through `*MaStore` helper params (local struct `let sa:MaStore=ma_init()` + `&sa` passed down — ZNC-010-safe); hand-computed expectations (10 attempts / 4 refused / 400‰) reproduce. Recompiled+ran → SM_FAILURES,0. PASS.
8. **R33_NATIVE_IO_V1.zag / R33_NATIVE_SHA256_V2.zag** (×4 each): integrity substrates — syscall wrappers and RFC6234-native SHA-256 with word-separated, length-checked round constants. Deterministic; no decision paths. PASS.
9. **twt_core.zag**: header "No RNG anywhere in this file" verified by grep. Verify gate is structural (in the op impl: ≥2 agreeing own obs AND zero contradicting). 12-field TwtStore returned by value (not nested — no ZNC-009 risk); arenas hand-zeroed per playbook §12 ("nio_alloc is NOT zeroed"). PASS.
10. **twt_trial.zag**: designed curriculum, zero RNG; `&local` → `*T` params, all access inside helpers — ZNC-010-safe. Cross-checked masked-truth math: 21323 = bits 0,1,3,6,8,9,12,14, matches code and prereg; honest item-5 wrong-commit path present. Recompiled+ran → TWT_FAILURES,0. PASS.
11. **comp.zag**: zero RNG; placeholder opcodes honestly scoped ("lab-canonical v1" per header, substrate analog). Recompiled+ran → COMP_FAILURES,0. PASS.
12. **comp.stripped.zag**: comment-stripped system source; byte-identical to normalized strip of comp.zag — the static no-RNG guarantee holds on the real source. PASS.
13. **up_core.zag**: unified slot substrate, zero RNG; 18-field UpStore (12 slices) — under the ZNC-009 "~8 fields" caution but never nested and it compiles/runs clean; all access via `*UpStore` params. PASS.
14. **trial_upt1.zag**: zero RNG; `s.live[3]`, `s.audit_n` scalar direct access on a local struct value (ZNC-004 applies only to annotated slice-let aliases, which don't appear). Recompiled+ran → UPT1_FAILURES,0. PASS.

### md — investigations and preregs
1. **perceptual-origins/ORIGINS.md**: PASS. NEGATIVE verdict matches program record; proven-not-absent argument (345 commits, code search, transfer bundles, pickle node sweep) is sourced and coherent.
2. **perceptual-origins/RECOVERY_SPEC.md**: PASS. Consistent. One note: its "remaining lead" (Micah's pre-git environment) is now CLOSED per his standing ruling — the pre-git session-file hunt is cancelled, so item 1 is no longer actionable; worth a dated one-line amendment.
3. **perceptual-origins/NATIVE_PERCEPTION.md**: **review — scope staleness**. Dated 2026-09-19, it predates the 2026-09-20/21 senses directives (LLM-vs-human percept head-to-head, rematch crossover bar, "rebuild from scratch" order). Its behavioral-parity-probing-vs-frozen-oracles plan is fine under REFERENCE_ONLY but needs a dated amendment before any reuse, so it isn't silently read as the current plan.
4. **recovery/RECOVERY_DIG.md**: PASS. Exhaustion verdict matches program record (VM find, 0-byte v62 blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, transfer bundles grepped, GitHub code search).
5. **self-model-substrate/PREREG.md, SELF_MODEL.md, TRIAL_RESULTS.md**: PASS. Kill bars F1–F5 all checkable and all cleared in evidence; negative controls in /tmp (broken sim fires F1, forced-B fires F2) genuinely validate the checks. Scale dimension honest (SM2 named next).
6. **teaching-without-tables/PREREG.md**: PASS. Honest §8 amendment (item-9 refusal reason mislabeled INSUFFICIENT→CONTRADICTED; mechanism untouched). Cosmetic: sections ordered §8 before §7. Falsification bars applied mechanically; E1–E5 expectations verified against trial source.
7. **teaching-without-tables/TEACHING_DESIGN.md, TRIAL_RESULTS.md**: PASS. Item-5 own-evidence failure is first-class in both design and results ("no copying, not no error"). Evidence matches claims.
8. **trace-composition/PREREG.md, COMPOSITION.md, TRIAL_RESULTS.md**: PASS. Placeholder semantics explicitly declared as assumption ("Documented assumption: both implement lab-canonical v1 semantics"), matching SEMANTICS.md's requirement that v1 be labeled provisional, not mistaken for recovered truth. Amendment record (harness setup bug on first run; failed bundle retained) is honest.
9. **trace-op-semantics/SEMANTICS.md, RECOVERY_SPEC.md**: PASS. NEGATIVE verdict + full 19-opcode census match program record; the acceptance trial is deterministic, preregistered, and blocks any claim beyond faithful implementation.
10. **trace-op-semantics/opcode_census.py**: **review — not evaluable as code**. It's the forensic census tool behind SEMANTICS.md (sanctioned analysis-only, not a TNN decision path), but it is NOT runnable as-is: hardcoded placeholder path `<path-to>/parent-r27-accepted-state.pkl` and requires `/tmp/restricted_load.py`, which does not exist on this VM. No self-test present. Historical artifact only.
11. **unified-partition-slots/PREREG.md**: PASS. 10 falsification criteria + honest post-first-run amendment (single-level/idempotent ROLLBACK semantic; criterion 8 corrected). Zero RNG even in harness.
12. **unified-partition-slots/TRIAL_RESULTS.md**: **review — stale evidence-dir name**. Doc cites evidence dir `EVIDENCE_20260919T002121Z/` which does not exist; the actual dir is `EVIDENCE_20260920T002141Z/`. All claims within (18/18 checks, UPT1_FAILURES,0, 103 ledger entries, 6 committed switches, 2 REFUSED_UNVERIFIED, first-run `UPT1_FAILURES,1` rollback_switch story) cross-check against the actual evidence dir and the trial source. Cosmetic fix only, no evidence gap.
13. **unified-partition-slots/UNIFIED_DESIGN.md**: PASS. Consistent with prereg/results; the single-level rollback amendment is incorporated (§2). Note: UP keeps MA1's KILL-resets-region→CORE convention while WB3 deliberately diverges from it (documented in WB3's A1) — recorded as an explicit difference, not a contradiction.
14. **non-toy-evaluation/EVALUATION_PROTOCOL.md**: PASS. Methodology protocol, marked not-yet-executed; entry gate G0 (no RNG in decision paths) and the "seeded harness scaffolding tolerated, never in the system" rule are consistent with program law; no claim contradicts known outcomes.
15. **portable-runtime/PORTABILITY.md**: PASS. wasm characterization spot-confirmed on the pinned build (exact error string); AArch64 QEMU path and claimed `~/workspace/tnn-lab/toolchain/bin/qemu-aarch64-static` both exist on disk; matches the program's known 3-bug characterization. §6 next steps (file the bugs) are consistent with the open filing-location question in standing memory.
16. **whitebox-at-scale/PREREG_WB3.md, TRIAL_RESULTS_WB3.md, WHITEBOX_SPEC.md**: PASS. Kill bars mechanical (8 criteria); first-run 9-failure honest record with three root causes matches PREREG A1; the margin-formality of the scale gate (`dbytes*26 == dops*952`) is honestly recorded as a restatement, not a system fix.

## Findings (all minor; no program-law violations)

| # | File(s) | Finding | Severity |
|---|---|---|---|
| 1 | wave3/self-model-substrate/trial/ref/r34_self_model_v1.zag + _tests.zag | No longer compiles with pinned znc (E0010, inline-if expression at line 76). Reference-only; annotate or archive. | cosmetic |
| 2 | wave3/unified-partition-slots/TRIAL_RESULTS.md | Cites nonexistent evidence dir `EVIDENCE_20260919T002121Z/`; actual is `EVIDENCE_20260920T002141Z/`. | cosmetic |
| 3 | wave3/perceptual-origins/NATIVE_PERCEPTION.md | Design spec superseded by 2026-09-20/21 senses directives (head-to-head, rematch bar, rebuild-from-scratch). Needs dated amendment before reuse. | scope-staleness |
| 4 | wave3/trace-op-semantics/opcode_census.py | Hardcoded placeholder path + missing /tmp/restricted_load.py; not runnable, no self-test. Historical forensic tool. | non-evaluable-as-code |
| 5 | wave3/perceptual-origins/RECOVERY_SPEC.md | "Micah's pre-git environment" recovery lead closed by his standing ruling (hunt cancelled); worth a one-line dated amendment. | cosmetic |

## Randomness audit

- `cl/world.zag`: environment-side Park-Miller LCG, never imported by learner — allowed.
- `trial_sr.zag`: seeded harness LCG for arm-1 stimulus only, explicitly labeled; learner path RNG-free — allowed (seeded harness scaffolding, verdict distinguishes system determinism from test adversity).
- All other system/decision code: zero rand matches (grep `rand|rand\(|srand|random` over all 15 zag files). No randomness in any TNN decision path.

## znc miscompile-pattern audit (15 unique zag files)

- Consecutive same-size `as []i32/u32/u16` casts: 0 hits.
- Annotated slice-let off a local struct value (ZNC-004): 0 hits.
- `slice as *u8` garbage reads: 0 hits (`_zag_slice_ptr` then `as i64` only, in nio/cl substrate).
- Chained `s.field.subfield` through pointer-in-struct-field (ZNC-012): 0 hits. All field access routes through `*T` function parameters (ZNC-010-approved) or direct scalar access on local struct values.
- Large structs: TwtStore (12 fields), UpStore (18 fields) returned by value but never nested — no ZNC-009 pattern; both compile and run clean.

## Kill bars (mechanical, applied)

- SM1: F1–F5 all clear in evidence; negative controls (/tmp tampered runs) fire F1/F2 — checks genuinely detect failures.
- TWT: prereg E1–E5 all match evidence; COPY-arm negative control discriminates (dependence 0 vs 1.0).
- COMP: F1–F4 all clear; honest amendment recorded.
- UPT1: 10 falsification criteria all pass; criterion 8 amended after first run.
- WB3: 8 falsification criteria all pass; amendment A1 recorded.
- NSR: evidence shows attempts-2/3 failures (35/17/15) converging to SR_FAILURES,0 in 5 final bundles — honest iteration, not silent reruns.

## Not evaluated (out of scope for this chunk)

Nothing. All 50 rows were present and evaluable. `grok-4.7` was not needed; 0 model calls used.
