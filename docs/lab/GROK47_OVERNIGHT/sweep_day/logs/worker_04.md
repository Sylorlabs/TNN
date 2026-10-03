# worker_04.md — MANIFEST SWEEP chunk_04 log (2026-09-22)

Chunk: `wave10/int-c7s100` five-organ integration sources (src_inst leg) +
`wave10/o2-appeal` design docs + `wave10/rc3` native-reasoning-control 100x
trial + `wave11` program docs, RNG-auditor build, senses-sweep build, g1
gap-fill design.

50 rows, 45 unique files (5 exact duplicates marked `dup:`). All 50 reviewed.
Zero unevaluable rows. No Grok calls used.

## Deduplication map (5 dups, all byte-identical)

- `wave11/build/rng-auditor/work/certify.zag` → dup of `wave11/build/rng-auditor/src/certify.zag`
- `wave11/build/rng-auditor/work/gate_target.zag` → dup of `wave11/build/rng-auditor/src/gate_target.zag`
- `wave11/build/rng-auditor/work/rerun_gate.zag` → dup of `wave11/build/rng-auditor/src/rerun_gate.zag`
- `wave11/build/senses-sweep/R33_NATIVE_IO_V1.zag` → dup of `wave10/int-c7s100/work/src_inst/substrate/R33_NATIVE_IO_V1.zag`
- `wave11/build/senses-sweep/R33_NATIVE_SHA256_V2.zag` → dup of `wave10/int-c7s100/work/src_inst/substrate/R33_NATIVE_SHA256_V2.zag`

## Findings

### F1 (NEW, wave10): o_audit.zag deep else nesting — ZNC-013 pattern
`substrate/o_audit.zag`, `oa_chunk_set`: if/else chain nesting beyond 5
levels. Per workspace finding ZNC-2026-09-21-013, 5-deep else nesting
miscompiles in this znc build. Workaround is to flatten (early returns /
helpers). This function must be flattened before its output is trusted.
Everything else in the file is consistent: the 16-word audit layout is
correct (stage@52, d1@56, d2@60).

### F2 (CLOSED, wave10): main.zag `_zag_argc()` gate — no repro
`src_inst/main.zag:205` gates argv dispatch on `_zag_argc()<2`, against the
workspace lesson ZNC-2026-09-21-007 (runtime passes argc=0). Spot test
(2026-09-22, this review): compiled with the pinned toolchain
(`znc_linux_x86_64_abed8aa1`) → 611,649-byte binary; ran with arg `s2` →
emitted `CHAIN_*` telemetry lines, no USAGE message, exit 0. Argument
dispatch works in this build; the concern does not reproduce here.

### F3 (NOTE, wave10/rc3): negative-control evidence is ephemeral
`run_neg_rc3.sh` keeps negative-control evidence in `/tmp/rc3_neg/`; that
directory no longer exists (shared tmpfs, 512MB). The results document's
claim is consistent with the (sound) script, but the artifacts are gone.
Regenerate with `run_neg_rc3.sh` if durable evidence is needed.

### F4 (VERIFIED, wave11): certifier + canary + gate all behave as designed
- `certify.zag` compiled and executed against the work/ fixtures:
  `cert_clean` → CERT RESULT: PASS; `cert_rng` → FAIL (RNG hit, line 3);
  `cert_time` → FAIL (TIME hit, line 3); `cert_fenced` → PASS with
  allowlisted=1 (the `znc:allow-rng` marker honored).
- `canary.zag` (clean): `CANARY RESULT: PASS`, 8/8 rows.
- `canary_plant.zag`: `CANARY RESULT: FAIL divergences=2` (rows 6,7) — the
  planted fence-drop is caught, attribution intact.
- `rerun_gate.zag`: 4 perturbation runs compared byte-for-byte
  (stdout/status/out.bin); stderr deliberately not captured (documented
  limit). The approved no-RNG enforcement is hardened replay + thin
  per-build certifier — the thin scanner alone is not presented as
  sufficient, matching the program record.

### F5 (VERIFIED, wave11): senses pipeline selfcheck reproduced
`ss_driver.zag` compiled; `selfcheck` mode → `SS_SELFCHECK,failures,0`
(29/29 checks). Code discipline confirmed by reading: integer-only, no
RNG/time, word→byte decomposition (never slice-as-pointer), candidate-only
`deliberate_add_propose`, replay-from-ledger `verify`. Findings doc claims
K1 PASS / K4 PASS / K2-K5 NOT-TESTED — the NOT-TESTED bars are honestly
labeled; K2 (spoof-injection) remains the first trial that can kill the
design.

### F6 (VERIFIED, wave10/rc3): RC3 evidence files parsed, all claims hold
- `EVIDENCE_20260920T085850Z/`: 40/40 `CL_CHECK` actual==expected,
  `RC_FAILURES,0`, `TRIAL PASSED`, `IL_HEAD,8000` (cap 10240),
  `AUDIT_USED,13218` (cap 16384); run1==run2 byte-identical; rng_grep empty.
- `EVIDENCE_EQUIV_20260920T085700Z/`: cap-10240 vs cap-128 verdict lines
  byte-identical (same md5), each self byte-identical across reruns, 40/40
  each — the capacity-window claim holds.
- `EVIDENCE_20260920T085711Z/` (voided first run): `RC_FAILURES,3` —
  consistent with the honest port-defect record in RESULTS_RC3.md.
- `il_core_rc3.zag` differs from the canonical wave-4 core only at the
  documented capacity/comment hunk; zero RNG tokens in trial or checker.
- Prereg amendment (A) was enacted under overnight-agentic authority and is
  flagged for Micah's retroactive review — a rejection voids the leg.

## Kill bars referenced / applied

- RC3 §3 falsification bars: none fired (40/40, negative control live per
  script, replay_diff=0).
- Senses K1 (determinism) / K4 (parameter laundering): PASS on verified
  evidence. K2/K3/K5: NOT-TESTED — remain open, documented as future work.
- O2 appeal docs: no kill bars apply — these are design-only records,
  explicitly unapproved and unrun; verdicts preserve that distinction
  (no mechanism PASS is claimed).

## Spot-compile summary (pinned znc toolchain, 2026-09-22)

| Build | Result |
|---|---|
| `src_inst/main.zag` | compiled (611,649 B); s2 run emitted CHAIN_* lines |
| `ss_driver.zag` | compiled; selfcheck 0 failures |
| `canary.zag` | compiled; PASS 8/8 rows |
| `canary_plant.zag` | compiled; FAIL divergences=2 (as designed) |
| `certify.zag` | compiled; 4/4 fixture verdicts as designed |

## Follow-ups recommended

1. Flatten the `oa_chunk_set` deep else chain in `o_audit.zag` (F1) before
   trusting its chunked-audit output in this build.
2. Regenerate and retain `/tmp`-independent negative-control evidence for
   RC3 (F3).
3. Senses-sweep: run the K2 spoof-injection trial (500 ep / 40 injections)
   — the first trial that can kill the audio admission design.
4. K3/K5 for the senses slice remain untested; no verdicts claimed.

## Verdict counts

- PASS: 22 (21 mechanism/source verified — loop, main, o2_eliminate,
  o4_recall, o5_govern, probes, seam, IO substrate, SHA256 substrate,
  cl/common, RESULTS_RC3, il_core_rc3, rc3_mini, rc3_trial, canary, certify,
  gate_target, rerun_gate, senses-findings, ss_driver, ss_pipeline —
  plus canary_plant as a correctly-catching fixture)
- review (design/historical/fixture/probe, no mechanism PASS): 23
- dup: 5
- done: 50/50. Unevaluable: 0.
