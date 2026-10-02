# NAMECHECK: Node2-v2 Ablation Worker

## Step 0: Toolchain Guard
- Safebin activated: `mkdir -p $HOME/safebin`, symlinked allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"`
- `which python3 python` returned nothing. Guard check done.
- Zero forbidden executables invoked.

## Scope
ABLATION ONLY. Unfrozen variants of the Node2-v2 built mechanism. No new mechanisms designed.

## Input Provenance
- Node2-v2 build: `docs/lab/research-lead/overnight-20260928/node2v2_run/` (commit `0988839a2`).
  - `n2v2_test.zag` (1503 lines, working K-H3 PASS test, SHA-256 `74c48d5a...`).
  - `BUILD.md` (mechanism: policy node tag 40 subtype 2, `resolve_uncertainty_v2`, `ev_observe_aw`, modified `miss_inquire`).
  - `TEST_RESULTS.md` (K-H3 PASS, 3/3 byte-identical).
  - `FROZEN_PREREG.md` (frozen, commit `4b05c8011`). Read-only.
- Frozen H3-lite prereg `9084a7760`. Preserved. NOT modified.
- Base for ablations: `abl_base.zag` (verbatim copy of `n2v2_test.zag`).

## Ablation Plan
1. **Ablate Link 1 (world to record):** Disable history recording in `resolve_uncertainty_v2`. Phase 2 (3x a_w=45) should NOT shift.
2. **Ablate Link 2 (record to write):** Keep history but disable field-20 write. Phase 2 should NOT shift.
3. **Ablate Link 3 (write to read):** Keep write but `miss_inquire` ignores field 20 (literal 30). Phase 3 guide should carry 30, not 45.
4. **Ablate Link 4 (read to action):** `miss_inquire` reads field 20 but does not use value (guide hardcoded 30). Phase 3 guide should carry 30.
5. **Adversarial (inconsistent):** a_w = 45, 46, 45 in Phase 2. Write should NOT fire (needs 3 consistent).

Each: 3/3 deterministic runs, measure specific outcome.

## Constraints
- Unfrozen variants only. Frozen prereg/source read-only.
- Pure Zag via pinned znc. Zero em/en dashes.
- Paper untouched. Nothing pushed.
- Explicit pathspecs on git add and git commit.
