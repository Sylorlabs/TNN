# Bundle v16 Inventory and Verification Checklist

Date: 2026-10-01 (PDT). Preparer: Bundle v16 Preparer.
Status: INVENTORY ONLY. Bundle NOT created. Creation must wait for freeze reconciliation and GW evaluation completion (see checklist item 1).

## 1. Repo state at inventory time

- Branch: `tnn-native-lab`
- Current HEAD: `0925660726e18e01cecbe0807f877fe3384a6676`
  ("Protected-core decision brief: structural graph mutation (PREPARED FOR MICAH - NOT DECIDED)")
- v15 bundle HEAD: `10a9b2d0dc44e6fd67b3c4a6c65b6e0ea557aa41`
- Commits since v15: 55
- v15 bundle file: `~/workspace/tnn-native-lab-20260930-v15.bundle` (2.0 GB, SHA-256 `226a50bf01281e7fd67b38236eefb374eca109eed292fad4c0413cf72bf281fb`)
- v15 does NOT contain TNN-2 work. v16 must capture all 55 commits.

## 2. Frozen artifact re-verification (on disk at inventory time)

| Artifact | Path | Expected SHA-256 prefix | On-disk prefix | Match |
|---|---|---|---|---|
| TNN-2 source | `.../tnn2_build/tnn2.zag` | `a29972ca8183b285` | `a29972ca8183b285` | YES |
| TNN-2 binary | `.../tnn2_build/tnn2_bin` | `6044f91f8fe35e30` | `6044f91f8fe35e30` | YES |
| Shim dir | `.../core_freeze_tnn2_shim/` | n/a (BIN_SHA.txt/SRC_SHA.txt on disk) | present | n/a |
| Ledger | `.../canonical_ledger/CLAIM_LEDGER.md` | 159 claims (per cycle ledger updates C143-C159) | present | n/a |
| Paper | `.../TNN_RESEARCH_PAPER_20260929.md` | untouched | untouched (no uncommitted changes) | YES |

## 3. TNN-2 cycle directories: committed in HEAD (42 dirs, verified via git cat-file)

Build / freeze / seal:
- `tnn2_build/` (1.5M: source, binary, build report)
- `tnn2_prereg/` (12K)
- `tnn2_repro/` (12K)
- `core_freeze_tnn2/` (12K)
- `core_freeze_tnn2_shim/` (1.6M)
- `freeze_worlds_v2/` (224K: sealed FW1-FW9, 16 files)
- `seal_integrity/` (8.0K: SEAL_INTEGRITY.md, 16/16 hashes match)
- `canonical_ledger/` (300K)

Red teams (all ATTACK-SUCCESS):
- `tnn2_redteam_construction/` (commit `340e94e3e`)
- `tnn2_redteam_inquiry/` (commit `4e329c772`)
- `tnn2_redteam_revision/` (commit `687ba0219`)

Analyses:
- `tnn2_synthesis/` (`42b4dfa91`: enumerated-schema/filled-slot, H1/H2/H3)
- `tnn2_altexp/` (`ccee9e5e6`: answer-fed not answer-derived)
- `tnn2_inquiry_generalization/` (`dedfad368`)
- `tnn2_revision_generalization/` (`edbb0e9b5`)
- `tnn2_interaction/` (`9009ff259`: no unsupervised loop, C0-D structural)
- `tnn2_h3probe/` (`94cecdba4`)
- `tnn2_h3lite/` (`22197da2c`: 3 policy nodes, K-H3 draft)
- `tnn2_dof/` (`d2af26581`: 0 learner / 5 mixed / ~240 researcher)
- `tnn2_movable/` (`f70ab617c`: top 3 quick wins)
- `tnn2_mulcompare/` (`e2e34a4ac`)
- `tnn2_compression/` (`b2a6ae82c`)
- `tnn2_governance/` (`622363372`: audit PASS)
- `tnn2_frontier/` (`65effc909`: 17 questions)
- `tnn2_c0d/` (`8bfb80fdd`: no 9/9 can establish C0-D)
- `tnn2_targetsel/` (`01c2aacfe`: 4th H3-lite site, K-TSEL-1/2)
- `tnn2_reusepath/` (`5f15b9309`: MAP-first query, K-REUSE-1/2)

Freeze / audit / reporting:
- `freeze_audit/` (`8959a7c14`: draft 5/9 WRONG, correct 4/9)
- `freeze_interpretation/` (`a1295cb22`: 5 rules, 4 scenarios)
- `morning_report/` (`0882dffb8`: 10-section draft)
- `reclustering/` (`ed2357141`: 4/9 falsifies diagnosis)
- `ledger_tnn2_cycle_prep/`, `ledger_tnn2_redteam_prep/`, `ledger_cycle15_prep/`

TNN-3 forward work (all DRAFT-NOT-FROZEN):
- `tnn3_prereq/` (`f795807cc`)
- `tnn3_killbars/` (`76231baa8`)
- `tnn3_killbar_review/` (`eb354e3a2`)
- `tnn3_roadmap/` (`67a420cca`)
- `protected_core_decision/` (`092566072`: brief PREPARED FOR MICAH, NOT DECIDED)

Post-freeze adversary:
- `postfreeze_adversary/` (`e409f5eea`: GW1-GW8 sealed, predictions frozen)

Committed TNN-2-cycle total on disk: ~17M.

## 4. NOT yet committed: must land before bundle creation (6 dirs, in-progress workers)

These directories are untracked at inventory time. They belong to running workers and must be committed by their owners. DO NOT commit them from this task.

- `core_freeze_tnn2_eval/` (5.4M: freeze evaluator work; draft known inconsistent, awaiting reconciliation)
- `gw_eval/` (20K: GW1-GW8 evaluator work)
- `tnn2_boundary/` (capability-boundary mapper)
- `tnn2_h2probes/` (H2 masked-probe designer)
- `tnn2_transfer/` (developmental transfer/reuse probes)
- `tnn3_prereg_struct/` (TNN-3 prereg structure drafter)

Plus `bundle_v16_prep/` itself (this task; committed below with explicit pathspecs).

## 5. Other untracked content (NOT for the bundle as uncommitted files)

- ~490 total untracked entries repo-wide. The majority are unrelated experiment scratch (e.g. `beam_g0/`, `beam_g2/` binaries and run logs, `intent_learn/`, `router2_learn/`, `run2.err/txt`, `run3.err/txt`, `unified_learn/`).
- Git bundles capture committed history only. Untracked files will NOT be in v16. Owners should commit or discard their scratch before bundle creation if it matters.

## 6. Size estimate

- Committed TNN-2-cycle dirs: ~17M on disk (uncompressed working tree).
- Full `.git`: 2.8G. Full working tree (excl `.git`): 6.5G.
- v15 bundle (full history to `10a9b2d0dc`): 2.0 GB compressed.
- v16 estimate: v15 size plus 55 commits of mostly small markdown/reports plus binaries (`tnn2_bin` 1.5M, shim binaries 1.6M, eval outputs 5.4M). Expected roughly 2.0-2.1 GB compressed. The TNN-2 cycle adds negligible weight relative to history.

## 7. Verification checklist (run immediately before creating v16)

1. [ ] Freeze evaluator has committed a RECONCILED report (correct 4/9 score, K-FZ2-4 resolved, W battery complete, hashes re-verified). The current draft is known wrong (claims 5/9).
2. [ ] GW1-GW8 evaluator has committed its report (GW-EVAL-COMPLETE/FAIL/BLOCKED).
3. [ ] All six in-progress dirs in section 4 are committed by their owners (or explicitly deferred with a note).
4. [ ] `git status --porcelain` shows zero uncommitted changes inside TNN-2-cycle paths.
5. [ ] Re-verify frozen hashes: `sha256sum` on `tnn2.zag` and `tnn2_bin` matches section 2.
6. [ ] Re-verify seal: spot-check `freeze_worlds_v2/worlds/` hashes against `seal_integrity/SEAL_INTEGRITY.md`.
7. [ ] Confirm paper untouched: `git status --porcelain -- .../TNN_RESEARCH_PAPER_20260929.md` empty.
8. [ ] Confirm branch is `tnn-native-lab`; record HEAD.
9. [ ] Create bundle: `git bundle create ~/workspace/tnn-native-lab-<YYYYMMDD>-v16.bundle --all` (from repo root, safebin PATH; git only).
10. [ ] Verify bundle: `git bundle verify <bundle>` reports OK and lists refs.
11. [ ] Record bundle SHA-256: `sha256sum <bundle>`; record byte size.
12. [ ] Clone-check (optional but recommended): `git clone <bundle> /tmp/v16-check` and confirm HEAD matches and `tnn2_build/tnn2.zag` hash matches.
13. [ ] Log the bundle (HEAD, SHA-256, size, commit count, date) in the parent report and memory. Do NOT push.

## 8. Explicit non-goals

- This task did not create the bundle.
- This task did not modify, move, or commit any worker's in-progress output.
- This task did not inspect sealed FW or GW world contents.
- This task did not change any verdict, score, or claim.

## Verdict

BUNDLE-V16-PREP-COMPLETE.
