# NAMECHECK.md -- Mini-Lifetime Integration Worker

## Step 0: Toolchain Guard (MANDATORY, recorded 2026-10-01)

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty). Only
`guard-check-done` printed. Safebin active. Pinned znc at
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Zero forbidden executables invoked. Recorded before any compile.

## Scope

INTEGRATION EXPERIMENT ONLY. Unfrozen variants. Compare three arms on a
persistent 5-phase mini-lifetime, no resets:

- Arm A: frozen TNN-2 baseline (verbatim base, SHA-256 a29972ca...).
- Arm B: base + structural rebinding patch (from 91585087c).
- Arm C: base + rebinding + shared consequence substrate store +
  provenance treatment + structural protection.

## Input provenance

- Base: `rebinding_adversary/adv_base.zag` (SHA-256 verified
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd).
- Rebind patch: `rebinding_adversary/adv_patch.zag` (verbatim).
- Substrate store: `substrate_build/sb_substrate.zag` (store fns only;
  Node2 policy fns sb_resolve_aw/sub_best_action/ev_observe_aw and the
  policy miss_inquire NOT used; withhold + sub_note paths used).
- Provenance: `provenance_treatment/pt_boot_trt.zag` (treatment
  bootstrap_miss) + field-16 tag writes at ev_teach (2), ev_teach_in
  (3), promote (4), revise (5), ev_observe (1).
- Protection: `structural_protection/tnn2_protection_variant.zag`
  (pro_edge_live, protect_one, protect_cells, protect_map_use + 4 call
  sites).
- Driver: new 5-phase mini-lifetime (this worker).

## Constraints

- Unfrozen variants only. Frozen source read-only, never modified.
- Pure Zag via pinned znc. Shell: znc, binaries, git, file ops only.
- Zero em/en dashes in docs (byte-verified before commit).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Nothing pushed. Local commits only, explicit pathspecs.
