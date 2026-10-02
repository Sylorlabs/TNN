# B-T5 evidence crew — RUNLOG

## 2026-09-24 ~08:31 PDT — session start, inheritance survey
- Task: TRACKR0 B-T5 evidence crew (Wave-2 follow-up); Micah undecided — "test more of it first, bring evidence."
- Read `~/workspace/scratch-crossref/T2/_wave2_tally/VERDICTS.md` (T2-TRACKR0 section),
  `T2/TRACKR0/crew/VERDICT.md` + `RUNLOG.md`, `T2/TRACKR0/clean/` (prereg frozen copy + ev/{b_t1,closeout,repair}/).
- Established: B-T1 FAIL stands; B-T5 claim 8 had no evidence in the crew's inherited set; prereg Method/Rule don't cover B-T5.
- Created work dir `~/workspace/scratch-crossref/T2/TRACKR0/bt5/`.
- Noted the workspace-AGENTS.md diffs that arrived mid-run (fable_stream wrapper; i32 offset rule + cast audit): unrelated to this task, no impact.

## Provenance trace (~08:35–08:55)
- `grep "B-T5"` over the prereg: exactly 1 hit — the T2-TRACKR0 section's "B-T5 split-to-merge FAIL."
  Inherited ev/ has zero B-T5 files.
- GitHub code search for `B-T5` / `split-to-merge` / `split_to_merge` in sylorlabs/TNN: 0 hits (incomplete index).
- Filesystem grep over `~/workspace/tnn-lab` found the trail in the R5 doc-stage copy:
  `docs/lab/units/r0/evidence/dynamics/BT5_FROZEN_SPEC_EXTRACT.md`,
  `VERDICT_B5_DYNAMICS.md`, `VERDICT_BT5_ROUNDTRIP.md`, `b5_*.log/csv`, `rt_*.log`,
  plus `MORNING_BRIEF_2026-09-21.md` and `NIGHT_RUN_2026-09-21.md`.
- Full chain reconstructed:
  1. PREREG_FREEZE.md §2 (Micah-signed 2026-09-21): literal bar — "a recruited chunk split then re-merged on the record."
  2. B-DYNSG crew: claimed PASS (split on "splitchk", merge on different material "AAAA"+"BBBB"); self-flagged FINDING B5-F1 (same-material re-merge unachievable); referred to Micah.
  3. Coordinator (morning brief ~06:05 2026-09-21): flagged — "FAIL or BLOCKED pending your reading."
  4. Marathon Crew 5 (2026-09-21 ~09:40): `bt5_roundtrip.zag` literal round-trip → **FAIL**, supersedes B-DYNSG PASS.
- Pin: `git log` on `VERDICT_BT5_ROUNDTRIP.md` → `d74b481df26aaa1d6c77f5ca825a499a69b3a42f`
  (2026-09-21T16:39 UTC, "MARATHON CREW 5: B-T5 literal same-material split->remerge round-trip proof (FAIL)");
  files: VERDICT_BT5_ROUNDTRIP.md, BT5_FROZEN_SPEC_EXTRACT.md, rt_leg0.log, rt_leg1.log, impl/dynamics/bt5_roundtrip.zag.
- Verified branch-head blobs byte-identical to the `d74b481df` blobs for all four evidence files
  (blob SHAs match; the 308bf365/3b011ef1 incident restored them exactly).

## Evidence fetch (~08:55–09:05)
- Via `~/workspace/skills/github/bin/gh-api` at pin `d74b481df` (no clones): bt5_roundtrip.zag,
  r0_core.zag, r0_probe.zag, m8_armor.zag, harness_common.zag, R33_NATIVE_SHA256_V2.zag,
  R33_NATIVE_IO_V1.zag, VERDICT_BT5_ROUNDTRIP.md, BT5_FROZEN_SPEC_EXTRACT.md, rt_leg0.log, rt_leg1.log.
- First fetch attempt for R33_NATIVE_SHA256_V2.zag used a wrong path guess (`docs/lab/src/experiments/…`,
  404/empty JSON); corrected to `docs/lab/units/r0/impl/harness/R33_NATIVE_SHA256_V2.zag` after listing the tree.
- Verified: committed `rt_leg0.log` md5 `fc67fccf9fb59cc7b9f6137d54590054` and `rt_leg1.log`
  md5 `6c1099926b124fbd642349b4d3581b3b` match the verdict doc's determinism-manifest table.
- Toolchain `znc_linux_x86_64_abed8aa1` sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
  matches the recorded pin. Source canary clean (no RNG/clock/entropy in decision paths).

## Rebuild + re-execution (~09:05–09:20)
- Mirrored `bt5/build/impl/{dynamics,core,harness}/` layout (@import resolves relative to importing file).
- Built `bt5_roundtrip.zag` with pinned znc `--no-zagd --no-analyze --no-foreground-cache` → binary (320051 bytes main).
- Ran leg 0/1 × pert 0–4: **10/10 rc=4**.
- `cmp` canonical runs vs committed logs: **byte-identical both legs**.
- pert 1–4 vs pert 0: diffs are exactly the 2 documented self-labeling lines
  (`RT_BATTERY,leg=,pert=`, `M8_PERTURB,`) — determinism confirmed as documented.
- M8 store images + ledger hashes match the verdict doc on both legs.
- Key values (both legs): split child id 1, parent state 2 (tomb), merge rc −1/−1, ledger 1 SPLIT / 0 MERGE,
  RT-3 merge-alone id 2 8/8 bytes OK, halves concat 8/8, RT_VERDICT FAIL.

## Fork probes (~09:20–09:45)
- Copied tree to `bt5/fork/`; added `fork/impl/core/r0_core_fork_rx.zag` (imports frozen r0_core.zag):
  `r0_merge_ids_rx` (tombstoned inputs allowed), `r0_maybe_merge_forkA` (live-gate relaxed, exact gain arithmetic),
  `r0_maybe_merge_forkB` (as A + tombstoned regret forgiven). MERGE ledger op emitted in both (marked fork in d2).
- Wrote compact harness `fork/impl/dynamics/bt5_fork.zag` mirroring RT-1 (recruit → snapshot → split conditions →
  split → pair×6 → frozen merge, fork A, fork B → byte-compare).
- Built with pinned znc → binary (139527 bytes main). Ran leg 0/1, 2 runs each: deterministic.
- Results both legs: frozen −1/−1 (FAIL reproduced); fork A −1/−1 (live-gate is NOT the only blocker);
  fork B merged id 2, 8/8 bytes byte-identical to pre-split snapshot → `FORKB_COMPOSES`.
- Source analysis of `r0_core.zag`: split tombstones parent (l.684); merge requires both-live (ll.743,771);
  utility sinks only via `r0_regret_update` with 1:1 regret coupling (ll.645–656) → split needs parent regret
  ≥ ~5283 while merge needs parent regret ≤ jgain−learned_gain ≤ 1000/500: arithmetically mutually exclusive
  on the same pair, harness-independent. Prefix-shadow measured in RT-2.

## Deliverables (~09:45)
- Wrote `bt5/VERDICT.md` (**B-T5 FAIL stands, evidence supplied**; amendment case for Micah: amend prereg wording vs approve two-part core change) and this RUNLOG.
- No commits made; no repo branches touched. Build artifacts (`.zag-cache/`, `.zagd.semantic-ready`, binaries)
  remain in `bt5/build/` and `bt5/fork/` scratch trees only.

## Notes / transient issues
- One exec call flaked with "failed to store metadata for session ... timed out after 15s registering session
  metadata" (same transient noted in the predecessor's RUNLOG); retry succeeded.
- Did not use /tmp (all scratch in `~/workspace/scratch-crossref/T2/TRACKR0/bt5/`).
- The R5 doc-stage copy was used only as a pointer to repo locations; all tested bytes were fetched at the
  pinned commit via the GitHub API and verified by git blob SHA.
