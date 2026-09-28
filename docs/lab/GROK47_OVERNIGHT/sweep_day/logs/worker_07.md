# worker_07 sweep log — chunk_07 (50 rows)

**Worker:** cb4ba97b chunk_07 · **Date:** 2026-09-22 · **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Grok calls used:** 0 (native review sufficed for this chunk; nothing needed external opinion).

## Summary

- 50/50 rows evaluated. 33 unique files reviewed; 17 LH-2 toolchain files byte-identical to LH-1 twins (sha256-verified, all 16 hex prefixes matched) → `dup:` verdicts.
- **Findings: 6.** No new kill-bar fires (this chunk contains design docs with preregistered bars but no executions under them; the LCG presence is the already-remediated, quarantined violation — see F1).
- No rows unevaluable; all files present at listed paths and sizes.

## Findings

- **F1 (expected, quarantine-consistent):** `r34_learner_core.zag` line 15 retains the forbidden seeded LCG — `r34v3_rng` (`rng*997+7919 mod 1000003`) drives the 1-in-5 explore flip in `r34v3_choose` (line 38). This snapshot is the tainted pre-remediation artifact; both campaign harnesses train with `explore=1` (r34_continuing_harness_v3: `r34v3_phase(...,1,1,0,1,...)`; r34_lh_harness `lh_train_regime` passes explore=1). Consistent with the contamination notices in PREREG.md / both RESULT.md files and R34 v3's permanent quarantine. NOT a new finding — inspection confirms the taint is physically present in this exact copy.
- **F2:** `r34_lh_harness.zag` `lh_drift_next` is a *second* seeded LCG (`st*97+13 mod 100003`, commented "Small-state LCG") used as the LH-3 drift scheduler (regime `mode`). Environment-side (evaluator), not the AI's decision path; drift seed = 0 for LH-1/LH-2 so it is inert in this chunk's variants. Flagged for the record.
- **F3:** `PREREGISTRATION.md` (r34v3, 2026-09-16) claims the learner core contains "deterministic RNG" — that is the LCG later found and remediated (2026-09-20). Pre-remediation historical doc; the claim is not law-compliant as written. `CLOSURE_20260917.md` and `WORKLOG_20260916.md` are likewise frozen pre-remediation; R34 v3's permanent quarantine governs all three.
- **F4:** `ZAG_PLAYBOOK.md` §6 campaign claims (failures=0, byte sizes) predate the 2026-09-20 LCG remediation and carry no contamination annotation in this copy. Fresh recompile of `r34_continuing_harness_v3.zag` produced 172719 bytes main — exactly the playbook's recorded size — so the build claim reproduces; the *results* claims are the tainted ones. Annotation coverage for playbook §6 should be checked against the 36 annotated docs.
- **F5:** `05-integration-roadmap.md` cites an "integrity battery 137/137" I have no record of in my known outcomes. Not contradicted — flagged for coordinator verification.
- **F6 (znc behavior note):** AGENTS.md ZNC-2026-09-21-007 says the runtime passes `argc=0` regardless of real args. My spot probe on the pinned toolchain (`argc_probe.zag`, 2 user args) returned `argc=3, arg1=alpha` — correct. So the `main()` arg-gating in the r34 harnesses (`_zag_argc()==1/2/3`) is NOT broken in this probe. 007 may be version- or context-specific; treat the probe result as one data point, not a refutation.

## Per-file notes

### md (senses design reviews)
| file | note |
|---|---|
| 02-vision-requalification.md | Law-translation bar (L1–L9), preregistered K-A..E / K-a..d. Consistent: felt-intensity retired 2026-09-20, 76 torch params unrecoverable, "thermometer before thermostat", variation-split rule. Design-review only; no results claimed. |
| 03-hearing-requalification.md | Hearing bar (D1–D4) + 4-class audio spoof threat model (ultrasonic, masked speech, replay, sustained). Keeps sustained-spoofing as the accepted hole; cross-modal appendix settles shared-framework/separate-trials, consistent with law 5. |
| 04-spoof-defense-trial.md | Falsifiable C1 (bounded defense / Pareto frontier F) + C2 (principled not tuned); defense stack D1–D5 all native Zag; D3 channel-health accounting explicitly the unbuilt piece; accepts above-F region as the accepted limit. Honest about deployment channel-independence being an upper bound. |
| 05-integration-roadmap.md | P0–P3 phased plan; terminal program kill bars K1–K4 (no dated amendment on fire). §2 claim requires sense-enabled ≥90% vs text control ≤60% on NOISE/INCOMPLETENESS at 10x, else K3 kills the program. F5 applies. |

### md (longhorizon)
| file | note |
|---|---|
| wave2/longhorizon/PREREG.md | LH-1..LH-7 prereg + 2026-09-19 Agent-F amendment (P3 adaptive-eps adopted, P2 rejected, P1 queued — consistent with remediation). 2026-09-20 contamination notice present and correctly scoped: tainted verdicts "may not be cited as canonical" until clean reruns. |
| LH-1/RESULT.md | Verdict SUPPORTED (10x, 480 updates, 16/16 all blocks, fp=818888) with quarantine notice — citation properly blocked. Records the harness eval-after-train artifact fix honestly. |
| LH-2/RESULT.md | Verdict: saturation YES (correct cells pin +30000 during block 16, ≈300 net accepts), rigidity NO (ordering s00>s01 preserved, margin grows). Same quarantine annotation. |

### md (r34v3 docs) — all frozen pre-remediation; see F3
| file | note |
|---|---|
| CLOSURE_20260917.md | Frozen closure of the 2026-09-16 evidence dir; grants nothing. Historical under v3 quarantine. |
| PREREGISTRATION.md | Structural-isolation gate + behavioral gates; "deterministic RNG" wording stale per F3. |
| README.md | Accurate structural description of the v3 lane (core vs harness split, run_native.zsh). Quarantine caveats from parent docs apply. |
| WORKLOG_20260916.md | Pre-freeze witness log; explicitly "not the final v3 qualification"; honest about the revoked Codex host token blocking run_native.zsh. |

### zag (LH-1 toolchain — randomness + znc-pattern inspection)
- **checkpoint/common/observation/storage.zag, R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag:** clean. No RNG anywhere (world module is the only RNG holder and is never imported by the learner core). No `as []i32/[]u32/[]u16` casts (ZNC-007), no `slice as *u8` (only `_zag_malloc as *u8` / `null as *u8` and the sanctioned `_zag_slice_ptr`), no annotated slice-let off a local struct (ZNC-004/010), no chained `s.field.subfield` through pointer-in-struct (ZNC-012). `cl_u32` returns unsigned i64 and all sign-interpreting reads compensate (`r34v3_get_signed` shift-offset, `cl_pcm_at` explicit 16-bit sign extension) — consistent with the AGENTS f3_get32 lesson. `ns_sha256` uses `*i64` pointer-sliced buffers (`wp[0..64]`) — i64 is in the CLEAN type scope for ZNC-007. Storage/constants match the playbook §5 Darwin→Linux port map.
- **world.zag:** environment-only seeded RNG (`48271x mod 2^31-1` per step), documented inline ("RNG belongs only to the world"). World seeds documented per variant in the prereg. Law-compliant by the documented evaluator/mind split.
- **r34_learner_core.zag:** F1 (LCG present). Otherwise: tie-break `decisions%2` is state-driven (lawful); whole-struct copy `s.*=t` is into a `*R34V3State` parameter, not a local (ZNC-009/010-safe); isolation gate intact (imports only observation.zag; no `cw_`/`CWOutcome`).
- **r34_continuing_harness_v3.zag:** compiles clean (172719 B, matches playbook). Campaign/baseline train phases pass explore=1 → tainted per F1. Negative tests use explicit corruption fixtures (refuse-inner-corrupt 2005, refuse-torn 2001).
- **r34_lh_harness.zag:** compiles clean. `lh_train_regime` → explore=1 (tainted); eval → explore=0. F2 (drift LCG). Modes 1/2 correspond to suspended LH-4/LH-7 protocols; `LH_DRIFT_SEED=0` keeps drift off for LH-1/2. `nio_free` only on `nio_alloc`'d slices (AGENTS _zag_arg lesson-safe).
- **wb_whitebox_tests.zag:** compiles clean; **ran fresh build → WB_FAILURES,0, exit 0.** `r34v3_rng` use is a seeded determinism unit test, not decision-path randomness. `wb_i32_get` respects unsigned-read lesson (values bounded < 2^31 by test construction).

### hello probes (all compiler diagnostics, no TNN content)
- add.zag compiles (215B main), exits 42. hello.zag, diag*.zag, diago*.zag, diags.zag, rawprobe.zag: syscall/flag/malloc probes, no randomness. sysprobe.zag intentionally documents that `_zag_linux_syscall` does not exist (compile error is the proof, per playbook §8).

## Compile-check results (pinned toolchain, `znc --no-zagd --no-analyze --no-foreground-cache`)
| file | result |
|---|---|
| hello/add.zag | ✓ 215B main, ran, exit 42 |
| r34v3/r34_learner_core.zag | "no main function found" — library module, not compiled standalone (expected) |
| r34v3/r34_continuing_harness_v3.zag | ✓ 172719B main (matches playbook's recorded size byte-for-byte) |
| r34v3/wb_whitebox_tests.zag | ✓ built, ran WB_FAILURES,0 |
| r34v3/r34_lh_harness.zag | ✓ 150996B main |
| hello/sysprobe.zag | fails `_zag_linux_syscall` — intended (F-probe) |

## Kill bars
- None of this chunk's preregistered bars (vision/hearing requalification K-bars, spoof-trial kill bar, integration K1–K4) had trial executions in this chunk, so none fire here.
- The LCG violation is the already-adjudicated, remediated one (Micah's REMEDIATE ruling, 2026-09-20); quarantine annotations are present where they belong. Exception: playbook §6 campaign claims (F4) — recommend the coordinator confirm they are covered by the 36-doc annotation pass.

## Outputs
- [worker_07.tsv](../fragments/worker_07.tsv) — 50 rows, status=done, verdicts filled.
- This log: `logs/worker_07.md`.
- No commits, no cron jobs, no external contact, no spending. No grok-4.7 calls made.
