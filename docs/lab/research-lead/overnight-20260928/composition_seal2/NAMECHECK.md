# NAMECHECK: H-SEAL2-1 Composition Second Seal

Worker: Composition Second-Seal Worker (H-SEAL2-1).
Date: 2026-10-02.
Task: independent second adversarial battery on the collapsed+integrated
composition mechanism (C234 collapse + per-MAP-shape APPL gate).
Branch: tnn-native-lab, local only, nothing pushed.

## Step 0: Toolchain guard (mandatory)

Executed at startup, before any other work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output), then
`guard-check-done`. Zero forbidden executables in PATH.

Pinned znc resolution: `znc` was not on the default PATH, so per the
worker toolchain guard it was linked into the safebin from the pinned
copy at
`/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`
(`znc 2026.07.0-dev (edition 2026)`, ELF 64-bit x86-64, statically
linked). Re-check after linking: `which python3 python` still empty,
`which znc` -> `$HOME/safebin/znc`. Guard re-verified clean.

Safebin contents: coreutils/shell tools, git, and the pinned znc only.
No python3, no python, no other interpreters.

## Frozen mechanism (read-only for this seal)

Copied verbatim from
`docs/lab/research-lead/overnight-20260928/appl_integration/`,
cmp-verified byte-identical, never edited:

- `frozen_base.zag` (1677 lines): composition_C/cc_base.zag copy.
  SHA-256 dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
- `frozen_patch_base.zag` (412 lines): C234 + DFS counters + AP
  threading, ablation arm (no gate).
  SHA-256 190fa382f63b9e28069c777778c7c2513fe9bc66095d276d4f88fe91a5dc79b2
- `frozen_patch_gate.zag` (571 lines): BASE + per-(frontier,shape)
  APPL gate (pap_*), CGATE diagnostics.
  SHA-256 581c9a993df2ad4dbf9486be1086e43f58f0ad5f1f6dc321e2f7cde309c1047e

`cmp` clean on all three copies. Worlds were designed AFTER this
freeze; the mechanism sources were not modified at any point.

## Adversarial worlds (designed post-freeze)

Nine sealed worlds in `s2_driver.zag` (shared verbatim by both
arms). S2F, S2G, S2H call `compose_try` directly (H-COMPVER-1
precedent): their Z queries are single-MAP-coverable, so
`ev_query_ap`'s `rebind_try` (S2F, S2G) or `mp_run` trial (S2H)
would bypass or mask the composition verdict. The unit under
seal is `compose_try`.

- S2A: winner-not-first at identical (frontier,shape). Two
  same-shape decoys (trained first) evaluated before the
  winner at 101. Direct compose_try.
- S2B: misleading co-use history (adversarial cb_couse_link
  D->X by fiat) with a decoy garden path at 103; S2B0 is the
  control without the edge.
- S2C0: T4-analog control, unpolluted store.
- S2C: S2C0 store polluted with a MALFORMED mark: raw type-15
  edge (m_y, aux=(0<<16)|3) on the plen-2 Y MAP whose entry
  cell is hand-pointed at X's chain start (structurally
  impossible triple, bypasses cl_mark validation).
- S2D: cross-domain (X r1 plen-3, Y r5 plen-1) with a decoy
  domain (D r9 plen-3, parallel facts over the same nodes,
  trained first).
- S2E: T4-style partial applicability; applicable
  sub-fragment (m_x,0,3) seeded DEEP (3rd) behind two
  same-shape decoy seeds.
- S2F: clean single-segment world; AP region pre-seeded with
  2 FABRICATED failure records at the exact (F(101,70),
  shape 2) via a verbatim copy of ma_features_from_paths.
  Tests whether the gate's evidence-driven withhold (skip)
  can be tricked by fabricated evidence. Direct compose_try.
- S2G: 32 satisfiable decoy marks (r7 plen-2) ahead of the
  winner (m=731, r9 plen-3, trained last via trial so its
  auto-mark is last in edge-id order) at the 101
  enumeration; 32-candidate cap truncates the scan. Direct
  compose_try.
- S2H: Z needs the same fragment (m_x,0,2) twice; per-path
  (m,start,len) reuse exclusion forbids the second use.
  Direct compose_try.

## Builds

- `s2_full_base.zag` = frozen_base + frozen_patch_base + s2_driver
- `s2_full_gate.zag` = frozen_base + frozen_patch_gate + s2_driver
- `s2_base_bin`, `s2_gate_bin`: pinned znc builds (exit 0)
- `s2_base_compile.txt`, `s2_gate_compile.txt`: build logs

## Runs (3/3 byte-identical per arm)

- `s2_run_base_1.txt`, `s2_run_base_2.txt`, `s2_run_base_3.txt`
- `s2_run_gate_1.txt`, `s2_run_gate_2.txt`, `s2_run_gate_3.txt`
- SHA-256 recorded in REPORT.md.

## Audits

- `fn compose_try` exactly 1 definition per patch; frozen sources
  unmodified (sha256 match the appl_integration originals).
- Driver uses only base/patch public functions (ev_teach,
  ev_query_ap, ev_cq, cb_newest_map, cb_couse_link, cl_mark,
  cl_chain_len, link_edge, t2_gather, ng/eg/get32/set32, emit/e64).
  No mechanism internals reimplemented except s2_feats, a verbatim
  rename-copy of ma_features_from_paths used solely to compute the
  fabrication target in S2F (driver-side, both arms).
- Zero em/en dashes in seal documentation (byte-verified).
- Pure Zag: no python3/python or other interpreters invoked at any
  point; safebin PATH active for all builds and runs.
- Research paper untouched. Nothing pushed to GitHub (local commit
  only, explicit pathspecs).
