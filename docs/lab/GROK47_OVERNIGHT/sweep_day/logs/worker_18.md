# worker_18 — manifest sweep log (chunk_18, 50 rows)

**Worker session:** 2026-09-22 ~07:15 PDT · **Method:** native review primary (no grok calls needed); spot-built 6 drivers with the pinned znc; reran trials natively; verified arithmetic claims by closed-form recomputation.

## Summary verdicts

| Verdict | Count |
|---|---|
| PASS | 40 |
| review (needs-attention note) | 3 |
| dup | 7 |

No row is unevaluated. One partial-evaluation: `auth_trial.zag` compiles and passes static review but its runtime (root + multi-uid setuid topology) cannot be re-executed on this VM — its POSITIVE verdict rests on the logged AU2 evidence.

## Key findings (new facts)

1. **Independent reproduction of three claimed determinism fingerprints on this VM:**
   - sr2_trial: two runs byte-identical, sha `da14bf25f90d1a35939f72c0ef33eba227c925cfa4a326f7abeb1b107af814a3` — exactly the TRIAL_RESULTS.md claimed sha.
   - rt2 attack/defense drivers: byte-identical reruns, 0 failures both.
   - ablate.zag: 346/346 checks pass natively, byte-identical rerun. (Note: the ablate driver binary was NOT in the reviewed chunk — it was built fresh from the reviewed `ablate.zag` source here; the 346/346 figure independently matches TRIAL_RESULTS.md.)
   - upgrade_trial.zag: 16/16 checks pass, byte-identical reruns, `TRAP_VERDICT,CONFIRM_UPGRADE_CONSISTENT`.
2. **Zero randomness** in all 16 reviewed zag sources (grep for rand/lfsr/lcg/urandom/xorshift: no hits); all mechanisms state-driven, deterministic.
3. **No known znc miscompile patterns** in any reviewed source: no consecutive same-size `as []i32`/`[]u32`/`[]u16` casts (ZNC-007), no annotated slice-let off a local struct value (ZNC-004), no `slice as *u8` (only `_zag_malloc(n) as *u8`), no chained `s.field.subfield` through pointer-in-struct-field (ZNC-012). u32 codecs use byte-index accessors.
4. **Claimed byte-identity verified:** rt2's `sr.zag` is sha256-identical to `wave4/scaffold-release/sr.zag` (as its header claims).
5. **RT-2 verdicts mechanically reproduce:** attack driver R0/R1 HOLD, R2/R3 BREAK (false commits) with 0 failures; defense driver D3 HOLD (fire=24, fcommit=0) / D3b HOLD (final_a=1) with 0 failures.
6. **Formula-verification:** family-E item table recomputed from `a_i=(4i+2)%13` — all 12 rows exact. `designation-tradeoffs/analysis.py` and `formula-test/analyze.py` both reproduce their report tables exactly.
7. **Linter notes (false positives, not defects):** znc L0010 "string buffer leak" on the `_zag_i64_to_str` print helpers (they do free via their own free helpers — lint doesn't track it); A0107 "dead loop" on `auth_trial.zag:168` `while(at<n)` — body increments `at`, warning is spurious.

## Kill bars applied

- **sr-followups (PREREG falsification criteria F-a1..F-a6, F-k1, F-ad1, F-x1):** the first run TRIPPED F-a2/F-k1/F-ad1 (45/114 mismatches) — recorded honestly as a prereg modeling error, not absorbed; Amendment A2's corrected model passed 155/155 on the confirmatory re-run. Mechanical application confirmed: no bar was bent post-failure.
- **trainer-auth (FA1–FA7):** all pass per RESULTS_AU2 (6/6 forgery attempts refused+audited, no state mutation on refusal, revocation semantics R3/R4 trialed, overseer recovery OK). POSITIVE applied mechanically; no partial credit defined.
- **trap-upgrade (PREREG_UPGRADE):** 16/16 CL_CHECKs (4/family: honest-pass, cheat-caught, control×2) — all pass; CONFIRM applied.
- **attribution-ablation:** all §4 expectations held exactly (346/346); per-component attribution (LOAD-BEARING: eliminative verification, SIGNAL_DISCONNECT, deliberative standards; DETECTION-ONLY: ledger/checker/provenance) follows the preregistered categories.
- **formula-test:** adoption is NOT applied — recommendation documented only; Micah's ruling + dated amendment still required (PREREG §9/§10). Defects 2, 3, C1 remain open.
- **designation-tradeoffs:** (a) fails cross-variant (proven: no fixed `m mod 50` residue covers ≥2 variants) — (a) dead; (b)≡(c) proven identical 30 episodes.
- **felt-intensity:** F1 (R_vup <90%) and F2 (R_wbs <100%) FAIL bars applied — honest FAIL reported; no post-hoc tuning performed. Integrity bars F3/F4a–d/F5 all PASS.

## Per-file notes

### wave5/redteam-rt2 (9 rows)
- `evidence/.../rt2_def.zag` — PASS. Defended substrate (SUSPECT/EXONERATE corroborated elimination). Deterministic; spot-run confirms D3/D3b HOLD.
- `evidence/.../rt2_dtrial.zag` — PASS. Builds; `RT2D_FAILURES,0`. Self-contained (does not import rt2_common).
- `evidence/.../rt2_trial.zag` — PASS. Builds; `RT2_FAILURES,0`; R2/R3 BREAK on false commits matches prereg predictions.
- `evidence/.../sr.zag` — PASS. Byte-identical to wave4/scaffold-release/sr.zag (verified sha `24a61ed6…`); undefended baseline with 8-arg sr_replay.
- `trial/rt2_common.zag` — PASS. Helper lib; its 8-arg `sr_replay(...)` call matches sr.zag's 8-arg signature (arity consistent — the 9-arg version is rt2_def's, used only by rt2_dtrial's own replay helper).
- `trial/rt2_{def,dtrial,trial,sr}.zag` — dup of the evidence copies (byte-identical sha256).

### wave5/sr-followups (6 rows)
- `DESIGN.md` — review: §4/§6 hand-traces are stale (flap fires {12,26,36,50,74,84}; adaptive fires {12,32,60,102}, bars {8,10,14,21}) — superseded by the dated Amendment A2 in PREREG.md. Honest supersession, not silent absorption.
- `PREREG.md` — PASS. A1 (pre-run correction) + A2 (post-first-run modeling-error correction, including NEW flap2 arm preregistered pre-implementation). Soundness invariants all held in the failed run.
- `TRIAL_RESULTS.md` — PASS. Numbers match A2 corrected model exactly; honest headline ("first run FAILED"); determinism sha reproduced here. Procedural error disclosed (evidence_run1.txt overwritten; first_run_mismatches.txt retained).
- `dbg.zag`, `dbg2.zag` — PASS. Temporary trace drivers retained for reproducibility; deterministic.
- `sr2.zag` — PASS. Runtime-K + SR_OP_RECONNECT (trainer-initiated, learner-gated) + streak_at_fire in DISCONNECT aux; deterministic.
- `sr2_trial.zag` — PASS. 155/155 checks pass natively here; run-sha matches claimed.

### wave5/trainer-auth (6 rows)
- `BINDING.md` — PASS. OS channel-capability design (SO_PEERCRED + separate supervisor address space + per-command allowlist); overseer role per Micah's law; same-uid/pid-reuse/rogue-supervisor limits named.
- `PREREG.md` — PASS (superseded by AU2; documents AU1 invalidation).
- `PREREG_AU1.md` — PASS. AU1 invalidated pre-verdict (shared uid 1000 violated deployment law); kept as shakedown record.
- `PREREG_AU2.md` — PASS. FA1–FA7 criteria; POSITIVE iff all pass, no partial credit.
- `RESULTS_AU2.md` — PASS. POSITIVE: 6/6 forgeries refused+audited, `REFUSED_REVOKED`/`REFUSED_CHANNEL`/`REFUSED_CLAIMMISMATCH` correct, R3 pin-persists-after-revocation trialed, R4 overseer recovery OK. Consistent with the known 117/117 result.
- `auth_trial.zag` — review. Builds clean; no RNG; syscall wrappers use 7-arg `_zag_raw_syscall` correctly. Cannot be re-run on this VM (requires root + uids 1000–1003 setuid topology); verdict rests on the logged AU2 evidence.

### wave5/trap-upgrade (12 rows)
- `TRAP_UPGRADE.md` — PASS. 8-family coverage; §8 honest gaps (true long-horizon scheming, coherent fabricated traces, general reward hacking, prompt injection) explicitly named as non-trappable.
- `PREREG_UPGRADE.md` — PASS. 3 post-first-run INVALID amendments (op-count 324→312, H branch 6/4→7/3, check-count 12→16) documented; failures were harness/doc arithmetic, not suite defects.
- `HONEST_VS_CHEAT_EFGH.md` — PASS. Ledger predicates consistent with the spec.
- `VALIDATION_UPGRADE.md` — PASS. 16/16 verified natively here; first (failing) run preserved as provenance.
- `curriculum/family_{e,f,g,h}_*.md` — PASS each. E table verified closed-form; F cross-episode divergence; G inversion+TEACH control; H recompute-mismatch with disclosed item-9 exception.
- `trial/substrate/{R33_NATIVE_IO_V1,R33_NATIVE_SHA256_V2}.zag` — dup of `toolchain/` canonicals.
- `trial/substrate/cl/common.zag` — dup of `wave2/ruleslab/impl/substrate/cl/common.zag` (standard substrate, byte-identical repo-wide). Reviewed content: bounded wire ops, no randomness, no learner logic.
- `trial/upgrade_trial.zag` — PASS. 16/16 natively verified.

### wave6/attribution-ablation (6 rows)
- `PREREG_ABLATION.md` — PASS. 9 arms + DR leg; falsification anchors in §4.
- `PREREG_ADDENDUM_A1.md` — PASS. Pre-trial instrument change (independent streak keyed on genuine signal); intact anchor confirmed unmoved (`INT_R_rstreak_at_fire,8,8`).
- `TRIAL_RESULTS.md` — PASS. Per-arm table matches §4; 346/346 + byte-identical reruns reproduced natively here.
- `VERDICT.md` — PASS. "Techniques prevent, architecture proves" matches program law; myopic 10x takes 21 vs intact 0 corroborates the known integrity-attribution record.
- `ablate.zag` — PASS. 346/346, 0 mismatches, byte-identical rerun, no RNG/casts.
- `sr_nohs.zag` — PASS. Single-function ablation fragment (elimination branch removed; commit-on-first-+1 added) per PREREG §2.

### wave6/designation-tradeoffs (2 rows)
- `designation-tradeoffs.md` — PASS. (b)≡(c) proven (30 identical episodes, offsets 1/2/3 by variant); (a) dead cross-variant (proven generally); accepted limitations (early-block bias, residue-0 phase-lock) carried as amendment caveats. Matches known outcome.
- `analysis.py` — PASS. Reproduces all numbers.

### wave6/distinguisher-deliberation (1 row)
- `OPINIONS.md` — PASS. Three genuinely opposed, unmerged positions: P1 (measure via PTR/EC), P2 (score via drop-ceiling tripwire), P3 (prevent via uncertainty expiry). No recommendation formed; ruling-5 still pending with Micah — consistent with known state.

### wave6/doc-front (2 rows)
- `INTEGRITY_HEADLINE.md` — PASS. Frontmatter `status: PROVISIONAL`; carries the truthful-but-sensor-deceivable qualifier; includes "What this does not claim" §197. Micah's sign-off still pending — matches known state.
- `PLACEMENT.md` — PASS. All cited numbers verified against local evidence dirs; 4 brief phrasing errors corrected (A–D names, RL-harness, horizons, 2,595 scoping). Open questions awaiting Micah (wording sign-off, qualifier framing, stale R33 block, MATRIX.md/H-07) — matches known state.

### wave6/formula-test (2 rows)
- `FORMULA_TEST_REPORT.md` — PASS. Recommends `(3m+7v+9)%10<2` (P(important|wrong)=1.00 all variants, minimal 2 benign v2 index coincidences, symmetric); adoption explicitly NOT claimed — Micah ruling + dated amendment required; defects 2/3/C1 noted pending — matches known state (ruling-1 won naturally, adoption pending).
- `analyze.py` — PASS. Reproduces report tables.

### wave7/felt-intensity (3 rows)
- `FELT_INTENSITY.md` — PASS. Mechanism spec (thermometer-not-thermostat, binding rule); consistent with the FAIL trial — no stale claims.
- `PREREG_FELT.md` — PASS. Frozen formulas (`imp=(7m+13v+3)%10<3`, `wrong=(3m+7v+9)%10<2`, trainer-designated `m%50∈{1,2,3}`) match the trial; bars F1–F5 frozen; confirms the referenced A1/A2 amendments do not exist (slot-index tiebreak followed as written).
- `TRIAL_RESULTS.md` — PASS. Honest FAIL on F1 (24–26% vs ≥90%) and F2 (7.7% vs 100%); all integrity bars PASS; no post-hoc tuning; diagnosis = trial-design flaw (32-slot LIFO revolving door churns 74–94% before observation), mechanism itself sound. The re-trial is a separate standing directive — this trial stands as an honest failure.

## Kill-bar ledger (all files referencing preregistered bars)

| File | Bars referenced | Applied |
|---|---|---|
| sr-followups PREREG/TRIAL_RESULTS | F-a1..6, F-k1, F-ad1, F-x1 | first run FAILED (45/114); A2 model 155/155 PASS — applied mechanically |
| trainer-auth PREREG_AU2/RESULTS_AU2 | FA1–FA7 | all pass → POSITIVE — applied mechanically |
| trap-upgrade PREREG/VALIDATION | 16 CL_CHECKs | all pass → CONFIRM — applied mechanically |
| attribution-ablation PREREG/RESULTS | §4 anchors, §6 categories | all exact → POSITIVE verdict — applied mechanically |
| formula-test REPORT | — (analysis only) | no adoption; pending Micah — applied |
| felt-intensity PREREG/RESULTS | F1–F5 | F1/F2 FAIL recorded; integrity PASS — applied |
| doc-front PLACEMENT | none (placement) | sign-off items pending Micah — recorded, not decided |
| distinguisher OPINIONS | none (deliberation) | no recommendation — pending Micah — recorded |

## Open items for parent/coordinator

1. `auth_trial.zag` verdict rests on logged AU2 evidence; safe re-execution needs a root-capable host with uids 1000–1003 (tnnsup/tnntrainer/tnnoverseer/tnnlearner).
2. Micah-pending items re-confirmed present in docs: strength Defect-1 formula adoption + Defects 2/3/C1 rulings; ruling-5 (freeze-vs-retention P1/P2/P3); felt-intensity re-trial design approval; doc-front wording/placement sign-off (R33 block, MATRIX/H-07); sr-followups adaptive-bar notice-channel trust (named next step).
3. Design staleness noted: `sr-followups/DESIGN.md` §4/§6 predictions are stale vs A2 — amendment exists in PREREG.md so this is documented, but a future sweep may want DESIGN.md annotated with an A2 pointer.
