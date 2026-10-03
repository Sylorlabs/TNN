# NAMECHECK: Node2-v2 Prereg Designer

## Step 0: Toolchain Guard
- Safebin activated: `mkdir -p $HOME/safebin`, symlinked allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"`
- `which python3 python` returned nothing. Guard check done.
- Zero forbidden executables invoked. Design work only; no computation required.

## Scope
PREREG DESIGN ONLY. No implementation, no variant, no experiments.

## Input Provenance
- Frozen H3-lite prereg: commit `9084a7760` (H3LITE-PREREG-FROZEN). Read-only. Node 2 spec from Section 3. Preserved as negative finding; NOT modified.
- Node 2 unreachability analysis: `b0ad6c5d3` (node2_reachability/NODE2_REACHABILITY.md). Verdict: UNREACHABLE. Read-only.
- Frozen TNN-2 source (verbatim copy): `node2_reachability/tnn2_base.zag`. Read-only. Used to verify `ev_observe`, `ev_act`, `miss_inquire` signatures and guide creation mechanics.
- Micah directive 2026-10-01: fresh Node2-v2 prereg with reachable path; require experience -> retained consequence -> production write -> later production read -> changed action; no circular self-bootstrap.

## Design Summary
Node2-v2 sources the "resolving action" from the WORLD via an action channel in the observation (`ev_observe(W,s,r,o,a_w)`), not from the guide's own action. This breaks the circularity that made Node 2 unreachable: the update rule operates on policy-independent external information. Reachability is proven by explicit 7-step construction from the initial state.

## Constraints
- PREREG DESIGN ONLY. No implementation.
- Frozen prereg `9084a7760` preserved, not modified.
- Zero em dashes in deliverables (byte-verified).
- Paper untouched. Nothing pushed. No sealed worlds.
