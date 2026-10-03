# NAMECHECK: Per-MAP Gate Integration Worker

## Step 0: Toolchain Guard

Executed at worker startup (2026-10-02):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result:
- `which python3 python` returned NOTHING (empty output before "guard-check-done")
- PATH=/home/hatch/safebin (python3/python do not resolve)
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: integrate the per-MAP-shape APPL gate into the collapsed
  composition mechanism (C234). UNFROZEN variant.
- Branch: tnn-native-lab (local only, nothing pushed).
- Prereg: PREREG.md committed ALONE as c4821dc44, strictly before any
  implementation file was written (commit-order self-check).
- Context inputs read (frozen, never modified):
  applicability_permap/ (prereg 1403e0b57, results d8e05afc8,
  APPLICABILITY-PERMAP-COMPLETE),
  composition_collapse/ (prereg dada745c8, results 6e3e1d47d,
  COMPOSITION-COLLAPSE-COMPLETE, ledger C234),
  composition_C/cc_base.zag (1677 lines, frozen).

## Build Records

- Base: ai_base.zag (1677 lines) = verbatim copy of
  composition_C/cc_base.zag (frozen); cmp-verified byte-identical.
- Patch BASE (ablation): ai_patch_base.zag (412 lines) = cl_patch.zag
  (C234, 382 lines) plus: DFS-work counters (STC: enum_evals,
  select_evals, skips, attempts), AP/r/ST threading through
  cl_candidates/cl_dfs/compose_try, ev_query renamed to ev_query_ap
  (6-param) plus a 5-param ev_query arity-compatibility wrapper for
  the base's internal test battery (t_c1 etc.), pap_init no-op stub
  (driver calls pap_init uniformly). No gate logic.
- Patch GATE: ai_patch_gate.zag (571 lines) = ai_patch_base.zag plus
  the per-MAP-shape APPL gate substrate (pap_init,
  ma_features_from_paths, pap_fmatch, pap_count_shape, pap_avg_sim,
  pap_decide with preregistered optimism threshold 2, pap_observe;
  records keyed by exact-F match plus fragment-len shape) and the
  gate check inside cl_candidates before cl_satisfy, with CGATE
  diagnostic lines. Diff BASE->GATE is exactly the gate.
- Driver: ai_driver.zag (327 lines) = cl_driver.zag (320 lines) plus
  AP threading (per-test 4096-byte AP region, pap_init once,
  threaded through train/couse helpers into ev_query_ap/ev_cq).
  Identical for both arms. main unchanged.
- Builds: cat ai_base.zag ai_patch_<arm>.zag ai_driver.zag >
  ai_full_<arm>.zag (base 2401 lines, gate 2566 lines); pinned
  znc_linux_x86_64_abed8aa1, exit 0, only benign A0102 warnings
  (234 per arm, same class as the collapse build).
- Binaries: ai_base_bin
  (sha256 549660e184615389ed9a73bb5d0c8b8a880d542ab2dbe34ea25cfb06353ff895),
  ai_gate_bin
  (sha256 895b1cb44ccdc0741abc13d016ee2b5abc7022cd420acb7c9f4541e9d9cf745f).
- Runs: run_base_{1,2,3}.txt, run_gate_{1,2,3}.txt.
  BASE sha256 de47314d8f96db2a28845602abe51b7b52d00e61faf190cf77ad5a5bc2bfe95a,
  3/3 byte-identical.
  GATE sha256 ebd90f76cb24dd30d7fb1550096247cb71afee285bb66b8e27fb21721837d072,
  3/3 byte-identical.
- Determinism: cmp clean across run1/run2/run3 per arm.

## Audits

- Kill-bar K11 architecture audit: `fn compose_try` exactly 1
  definition and 1 call site (ai_patch_gate.zag); COMPOSE_MODE 0
  occurrences; `_mode` identifiers 0; mode/bridge/handler words 0
  (only the inherited "Zero modes, bridges, handlers" header
  comment); whole-MAP DFS remnants 0 (no cc_relseq/cc_satisfy/
  un_dfs/un_candidates); gate is a search prune (cl_satisfy and
  t2_try_verify still arbitrate every positive result); AP region
  is learner-owned persistent state; no new semantic cases
  (features are gathered-path structure plus query relation;
  shape key is fragment len from mark aux).
- Kill-bar K9: every CGATE-STAT line on the T1/T2A/T2B/T3 sections
  shows skip=0; segment MAPs byte-match C234 on all passing tests.
- Toolchain re-check after runs: `which python3 python` still empty.

## Constraints Observed

- Unfrozen only. Frozen sources read only (cc_base.zag copied
  verbatim, cmp-verified; applicability_permap and
  composition_collapse directories never modified).
- Pure Zag for all research logic (Step 0 guard above).
- Zero em/en dashes in PREREG.md, NAMECHECK.md, REPORT.md
  (byte-verified before commit).
- Paper untouched.
- Nothing pushed to GitHub.
- Explicit pathspecs for all git add/commit operations.
