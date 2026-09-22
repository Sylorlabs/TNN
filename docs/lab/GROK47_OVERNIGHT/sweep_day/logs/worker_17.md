# worker_17 log — chunk_17 (50 rows: wave5 ledger-gating, llm-failure-research, phase-transitions-remaining, redteam-rt2)

Method: sha256 dedup first (many evidence snapshots identical), then per-kind grok-loop:
md read fully (key sections for the 25KB ones), zag grepped for RNG/miscompile patterns + spot-compiled
with ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 + several binaries run natively.
No grok-4.7 calls — native review (compile + execute + diff) was primary and conclusive for every headline claim.

## Findings (numbered for the parent)

F1. **All headline verdict claims verified by native rerun (fresh builds from the reviewed sources):**
- lg_trial.zag → LG_RESULT,PASS, LG_FAILURES,0, 433 LG_CHECK lines.
- trial01/23/34 → exit 0, FAILURES 0, two consecutive runs byte-identical; CL_CHECK counts 35+52+39 = 126, exactly matching TRIAL_RESULTS.md's "126 CL_CHECK lines".
- RT2 attack (EVIDENCE_RT2_20260920T022058Z): 73/73 RT2_CHECK, RT2_FAILURES,0; verdict lines match the documented table exactly (R0 HOLD fire=12, R1 HOLD fire=22, R2 BREAK fire=30 fcommit=1, R3 BREAK fire=24 fcommit=1 caf=1/1).
- RT2 defense (EVIDENCE_RT2D_20260920T022242Z): 35/35 RT2D_CHECK, RT2D_FAILURES,0, D3 HOLD + D3b HOLD.

F2. **sr.zag byte-identical to wave4/scaffold-release/sr.zag** (diff verified) — the runner's "real learner, unmodified" assertion holds.

F3. **il_core -1 sentinel is sound.** The AGENTS.md lesson ("f3_get32 readers return unsigned, ~4e9 for negatives") made `il_i32_get`'s `>=0` sentinel checks suspect. Tested both: a native probe with the exact il_i32_set/il_i32_get code showed znc i32 arithmetic wraps mod 2^32 — -1, 0, 5, INT_MAX, INT_MIN all round-trip exactly; the stored -1 marker reads back as -1. The f3_get32 lesson does not apply to this implementation.

F4. **Zero randomness anywhere.** RNG grep over all unique zag files found exactly one hit: `seed:i32` in world.zag's `cw_init` — a fixed config parameter stored into the world image, with NO callers anywhere in ledger-gating. Not a decision-path RNG. No lcg/xorshift/time/clock anywhere.

F5. **No known znc miscompile patterns found:** zero `as []i32/[]u32/[]u16` casts in any file (ZNC-007 N/A — the code consistently uses []u8 arenas + explicit LE accessors, the documented workaround); no `slice as *u8` (only `_zag_malloc(n) as *u8`, which is the approved allocator cast); no chained `s.field.subfield` through pointer-in-struct-field; struct literals only store value/slice fields, never `&local`; else-chains max 4 flat (ZNC-013 5-deep N/A).

F6. **Two dead driver snapshots don't compile (dev history, not claim violations):**
- rt2_dtrial @022205Z: sr_replay arity mismatch (8 args vs 9).
- rt2_dtrial @022218Z: leftover rt2_num call after the rt2_common import was dropped (renamed rt2d_num).
The docs cite only the working evidence dirs (022058Z attack, 022242Z defense); nothing inconsistent.

F7. **Evidence-snapshot evolution corroborates the documented amendments:** rt2_trial @022038Z compiles and runs to exit 1 with RT2_FAILURES,14 — exactly the documented Amendment-A1 first run (spoof tables mis-targeted B episodes, fixed by moving to A episodes). rt2_dtrial @022229Z runs with RT2D_FAILURES,3; @022238Z already passes (0). The snapshot ladder matches the "calibration runs taught" narrative.

F8. **rt2_def.zag is byte-identical across all 6 defense dirs** — the defended mechanism never changed during the calibration; only the driver did.

F9. **Dedup within chunk:** rt2_common identical ×8, rt2_def ×6, sr.zag ×2, substrate trio ×2 each, dtrial @022315Z = @022242Z byte-identical. All marked dup:<first-path>.

F10. **Kill bars:** nothing triggers mechanically. Phase-transitions "per-gate cost linear in ledger window" is a deferred PT2-scale trial (not run here). RT-2's single-channel kill condition (demonstrate two-consecutive-forgery vs defended learner) is named-not-run. lg_trial's leg-A2 asserts head≤IL_CAP — passed (90≤128).

## Per-file notes

### wave5/ledger-gating (8)
- il_core.zag: zero RNG; LE byte-arena with -1 unused-provenance markers; il_check implements rules 1–6 mapping to IL_OK/101–106 exactly as the lg.zag comment claims. Sign probe (F3) clears the one risk.
- lg.zag: pure wiring; lg_attempt_commit audits HOLD on blocked path, never calls hss_commit there; hss.zag present in dir (not in chunk, build works).
- lg_trial.zag: compiles clean; runs PASS. Legs A (60 honest), B (6 cheat probes B1–B6 at check boundary), C (belief revision + stale-claim block + superseded-observation silence). All designed, zero RNG.
- substrate R33_NATIVE_IO_V1.zag / R33_NATIVE_SHA256_V2.zag / cl/common.zag: standard substrate; compiled clean as part of lg_trial build chain.
- substrate/cl/observation.zag: compiles (analyzer style warnings A0102 only); provenance-only encoding, explicitly never learner-imported shape.
- substrate/cl/world.zag: compiles (warnings only); cw_init seed is config, no callers in ledger-gating (F4).

### wave5/llm-failure-research (2)
- LLM_FAILURE_CATALOG.md: 7 failure-mode families, each with mechanism + structural lesson + documented instances; honest caveats (in-context vs trained-in gap; contamination≠cheating; post-hoc vs trapped table). Claims traceable to SOURCES.md; nothing contradicts known outcomes.
- SOURCES.md: attribution catalog with explicit evidence-gap notes; no claims of its own.

### wave5/phase-transitions-remaining (7 docs + 4 zag)
- PREREG_01/23/34.md: consistent with known outcomes — MA2 firewall lesson (system-granted firewall is no firewall), force-pin-as-law, arms B/C alive, trainer-as-counterparty for 3→4. Scenario-H freshness self-correction documented in-line in PREREG_34 (gate clause for stale petitions after dissolve).
- SPEC_AMENDMENTS.md: trial-over-spec rule; amendment 1 (2→3 clause 4: visibility not refusal), clarification 2, bindings 3–5. Coherent with TRIAL_RESULTS.
- TRIAL_RESULTS.md: claims verified (F1); "no compiler bugs encountered" plausible given clean builds; honest negatives + PT2-scale next step with kill criterion.
- trial01/23/34.zag: all compile + run PASS + byte-identical reruns (F1). Local-struct scalar reads (s.audit_n) and direct s.audit[i] indexing compiled fine; trial-local byte-arena patterns per playbook.

### wave5/redteam-rt2 (4 docs + 19 evidence files)
- PREREG.md: thorough; H1 vs H0; hand-computed traces; amendments A1 (parity) / A2 (s3-probe blind spot) documented; falsification criteria binding.
- DESIGN.md: evaluator separation (ground truth only in driver), deterministic integer-only protocol, spoof tables as pure fn(rung,step), mechanistic judge, zero-RNG static grep gate.
- DEFENSE.md: ledger-grounded diagnosis; corroborated-elimination rule matches rt2_def.zag exactly; honest residual (two consecutive forgeries still force UNCOMMIT — single-channel undecidability stated); architectural fix specified-not-built (wave-6).
- TRIAL_RESULTS.md: verdicts verified natively (F1); calibration history (14/73, s3-probe) corroborated by snapshot ladder (F7); "Learned = persists after disconnect seals the lie" matches R3 verdict line caf=1/1.
- Evidence dirs: see F6–F9. The 022038Z attack snapshot is the pre-A1 artifact (14 failures); 022058Z is the passing run. 022205Z/022218Z dtrials are non-compiling dead snapshots.

## Rows not evaluable
None — all 50 rows evaluated. (No jsonl/py in this chunk.)
