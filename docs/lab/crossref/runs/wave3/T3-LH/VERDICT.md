# VERDICT — T3-LH (wave3 tier-3 crossref): SPOT-REPRODUCED

**Workstream:** T3-LH — delayed-credit rule + clean reruns; R34 v3 quarantine holds.
**Prereg:** `docs/lab/crossref/PREREG_TIER3.md` §T3-LH, frozen 2026-09-22; committed
blob 943ab5c984cd16b4a618bbc94329780b2d425a68, sha256
`538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1` —
byte-identical to the on-disk copy used for extraction. (Initial mismatch
reading was a `gh-api --raw` wrapper artifact; re-fetched blob properly.)

## Anomaly (record-keeping, not evidence): commit c28f2e3a does not exist
The dispatch cites "clean contamination-remediated verdicts at commit
c28f2e3a". That identifier does not resolve:
- GitHub API `GET /repos/sylorlabs/TNN/commits/c28f2e3a` → HTTP 422 "No commit
  found for SHA: c28f2e3a" (any branch).
- `git fetch origin c28f2e3a` → "couldn't find remote ref"; no c28f2e3a prefix
  in the branch history listing.
- No local references to `c28f2e3a` in docs/lab, crossref, or ops.
The remediation evidence it points to IS on `tnn-native-lab` under the actual
commit chain verified below (final comparison verdict:
`fe0cda3d86485eb56a0802c5dde2ca40ab5ea2cc`).

## Verification-of-record (all on branch tnn-native-lab, via API)
Remediation commit chain (each resolves; files enumerated):
- `94498e7d0a84` freeze preregistration (wave12)
- `c3dc58d472` clean learner core + whitebox suite
- `3cb3a8b46` / `a4f91852` verification evidence
- `825594a5` analogy prereg; `b3f1df23` analogy driver + evidence + verdict
- `9ed0203a` freeze LH battery clean-rerun prereg (PREREG_RERUN.md)
- `3642f69e` rerun apparatus (harness + runner)
- `445464a3` / `22ad3a90` clean-rerun evidence + verdict (1/4)
- `18330599` evidence (2/4: LH-1 and LH-5 runs); `c7fcf8d3` (3/4: LH-2);
  `0cd56df2` (4/4: LH-3)
- `c9ac9fb1fd8f886fe26cfccb86b12d3b95fff6e4` annotate tainted evidence —
  exactly 36 files (35 modified docs + CONTAMINATION_REGISTRY.md)
- `a01a5e83` freeze COMPARISON prereg; `fe0cda3d86485eb56a0802c5dde2ca40ab5ea2cc`
  COMPARISON analysis + verdict (RNG verdict DID-NOT-HELP)
Spot-check 3 annotated docs at branch head: all carry
"## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)"
intact. Static audit of the committed clean sources: core has zero forbidden
terms, imports only `observation.zag`; harness hard terms none; harness
`seed` identifiers are the documented world/drift seeds (prereg A6). No
quarantined R34 v3 code path is reachable (r34v3/ is not imported).

## Spot rerun: LH-1R from committed sources, clean checkout
- Sources fetched from the branch as git blobs with SHA verification:
  `r34_clean_learner.zag` (blob f1dbdbdc…), `r34_lh_clean_harness.zag` (blob
  7823055f…) — their sha256
  (`4f4b436b93a32076aac4968d8b39a1a8289348135a6dc2aa52df55ad56af412c`,
  `c95144bb976b8c0f44ef384952a6f2ea1c693dbc9a7e942f0d793db77c370869`)
  exactly match the `source.sha256.txt` the original crew recorded — i.e. the
  exact sources behind the committed evidence.
- Toolchain substrate: R33_CONTINUING_LIFE_V1 libs + pinned compiler
  `znc_linux_x86_64_abed8aa1` (sha256 498abcb5…, matches evidence
  `compiler.sha256.txt`). Toolchain libs are not on the branch; used from the
  pinned local substrate as the build substrate (documented; libs are not the
  experiment).
- Build: `znc <harness> --no-zagd --no-analyze --no-foreground-cache -o lh_clean`
  from a mirrored `r34-remediation/rerun/` cwd — compiled clean, exit 0.
- `./lh_clean lh1` run TWICE:
  - stdout byte-identical between the two runs (excluding `LH_RESOURCE`
    wall-clock `cpu_us` telemetry — the same exclusion the original runner's
    determinism check used): sha256
    `da312916cfcdd9e861ff7620b6a72b42d7eeaca7ea2b6f563cd9aefda79d383e` both.
  - Output byte-identical to the committed evidence `lh1_run1.stdout.log`
    (blob faa7d297…, verified; matches the bundle's own SHA256SUMS entry
    `54054ff74a9d56f13ae346714b88279f1ce52e48ba970e94a8e00feb2fda0c0e`).
- LH-1R PASS bars (from the frozen prereg, un-bent):
  - `CL_CHECK,lh_train_updates,480,480` — 480 updates ✓
  - `LH_FAILURES,tag=LH-1R,0` — zero LH_BLOCKFAIL; per-block ea=16,eb=16 ✓
  - `LH_RETURN,tag=LH-1R,ra=15,active=0,upd_delta=0` — return-A 15/16, zero
    weight updates ✓
  - controls: disabled-update B probe `disabled_updates,0,0` +
    `disabled_B_positive,12,12` ✓; scrambled-reward A probe
    `scramble_defeats_A,0,0` ✓
  - dynamics: 19 training switches + 1 return switch (campaign switches=20),
    16 explores (all block 0), max |score| 22300 — matches the recorded
    verdict exactly ✓

## Verdict: SPOT-REPRODUCED
LH-1R PASS holds on the remediated (LCG-free) learner from committed sources,
two runs byte-identical, output byte-identical to the committed evidence, and
no quarantined R34 v3 code path is reachable in the clean build. The frozen
prereg, the 36 quarantine annotations, and the full remediation commit chain
are all on `tnn-native-lab` as the prereg requires.
