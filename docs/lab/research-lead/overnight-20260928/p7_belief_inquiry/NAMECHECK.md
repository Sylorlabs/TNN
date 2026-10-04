# NAMECHECK: P7-BELIEF-INQUIRY

Lane: `docs/lab/research-lead/overnight-20260928/p7_belief_inquiry/`
Date: 2026-10-03.

## Hygiene rules this lane commits to

1. **Isolation.** All work in the private worktree created by
   `tools/lane.sh new p7belief`. `git rev-parse --show-toplevel` inside
   it returns the worktree path, never `/Users/Shared/micah/Documents/TNN/TNN`.
   Never `git checkout` in the main repo. Never touch another lane.
2. **Pure Zag.** Every build and run under
   `. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`, which shadows
   python, node, bun, deno, tsc, cc, gcc, rustc, julia, perl, ruby, R,
   make and cmake by name and restricts PATH. `tnn_pure_zag_report`
   printed `VERDICT: PURE-ZAG-CLEAN` before implementation. Shell and
   git are orchestration only. No awk/sed arithmetic on results.
3. **Compiler flags.** `--target macos-arm64 --no-zagd --no-analyze
   --no-foreground-cache`, always via `tools/zbuild.sh`.
4. **Output.** `_zag_print` / `_zag_println` only. Zero
   `_zag_raw_syscall` in this lane's sources, because it is inert on
   darwin/arm64 and produces an empty log with rc=0
   (`docs/ops/ZAG_LANGUAGE_AND_WORKER_BRIEF.md` section 4.0).
   Output is asserted non-empty in-driver (K-NONEMPTY) and by `wc -c`.
5. **Determinism.** `tools/zbuild.sh ... --rep 3` asserts 3/3
   byte-identical stdout. Recorded as K-DET.
6. **Dashes.** Zero em/en dash bytes in authored files and run outputs.
7. **Naming.** Opaque identifiers: `p7b_*`, `PA/PB`, `M1..M6`,
   `K-B01..K-B35`, `C500..C506`. No word that names an inquiry mode.
8. **No new vocabulary in the frozen store.** 0 new edge types, 0 new
   node types, 0 modes, 0 bridges, 0 handlers. The dependency fraction
   rides on `field12` of the pre-existing `ET_SUP` (type 2) edge; the
   REVISION reason is a novel `field12` VALUE on the pre-existing
   kind-3 self-edge already written by `bp2_retire`. Both disclosed in
   PREREG section 2.3.
9. **Frozen block untouched.**
   `xhier_countmap_fix/xf_block.zag` SHA-256
   `172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a`
   re-verified before and after the build.
10. **Frozen belief layer untouched.** The `bp2_*` section of
    `p7b_learner.zag` is byte-identical to
    `belief_provenance_9/bp9_learner.zag`
    (SHA-256 `2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e`).
11. **Explicit pathspecs.** Never `git commit -a`.
12. **Claim IDs.** C5xx block only (C500..C506). C377-C466 untouched.

## Probe hygiene

The two pre-implementation probe rounds (`pr.zag`, `pr2.zag`) lived in
an ephemeral directory outside the repo and are not part of the lane.
They were pure Zag, one binary each, built with the pinned `znc` and
the mandatory target flag. Their measurements are quoted in PREREG
section 2.2 as PB1..PB8 and were used only to hand-derive predictions.