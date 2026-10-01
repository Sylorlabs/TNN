# NAMECHECK.md: POST-FREEZE Adversary (TNN-2 generality worlds GW1-GW8)

Date: 2026-10-01. Role: Post-Freeze Adversary for TNN-2.
Task: design NEW sealed adversarial worlds (GW1-GW8) attacking TNN-2's three
claimed mechanisms, from the PUBLIC architecture claim only.

## Step 0: Toolchain guard (mandatory)

Executed at session start, before any work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (no output lines before
"guard-check-done"). Safebin is clean. PATH exported to $HOME/safebin for
all subsequent commands in this task.

This is a DESIGN task. No research computation is performed. No Python, C,
C++, JavaScript, or Rust is invoked at any point. World files are generated
by a pure-Zag program compiled with the pinned znc. Shell is used only for
file operations, git, sha256sum, and invoking znc/binaries.

## Step 1: Identity and scope

- I am the POST-FREEZE ADVERSARY. I do not modify TNN-2 source or binary.
- I read ONLY the public architecture claim: tnn2_build/TNN2_BUILD_REPORT.md
  (commit f4de7ff46) and the TNN-2 prereg. I did NOT read hidden builder
  fixtures, builder test files, or sealed FW world contents.
- I read the PUBLIC sealed-asset pattern (SEAL.md structure, world file
  line format from the shim report, responder contract from the run
  script) in order to follow the same format. I did not read FW world
  file contents.
- Owned path only:
  docs/lab/research-lead/overnight-20260928/postfreeze_adversary/
- Constraints honored: no new opcodes required by any world (frozen 4-op
  ISA is sufficient in principle for every world); no em dashes in
  documentation; paper untouched; explicit git pathspecs on commit.

## Step 2: Deliverables checklist

- [x] NAMECHECK.md (this file; Step 0 recorded)
- [x] ADVERSARY_DESIGN.md (8 worlds, mechanisms, material-difference
      arguments, frozen pass criteria, predictions)
- [x] seal_src/gen_gw.zag (pure-Zag generator; pinned znc)
- [x] seal_src/gw5_respond.zag (GW5 two-stage responder, sealed)
- [x] worlds/gw1_world.txt ... worlds/gw8_phaseC.txt (sealed assets)
- [x] SEAL_GW.md (sha256 table, id hygiene, anti-smuggling scan vs
      frozen TNN-2 source)
- [x] Committed with explicit pathspecs.

## Verdict

ADVERSARY-DESIGN-COMPLETE. Eight sealed generality worlds (GW1-GW8)
delivered. No TNN-2 modification. No new opcodes. Pure-Zag generation.
