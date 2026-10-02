# NAMECHECK.md: CONSEQ lane, wave-20261001-2321pdt

## Step 0 (worker toolchain guard)

- Ran: `cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"`
- Safebin output: `safebin: /home/hatch/safebin`, `linked: 36 tools`, `znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`, `verify: python3 absent from safebin PATH (OK)`, `verify: python absent from safebin PATH (OK)`, `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- Verification command: `which python3`
- Verification output: nothing printed; exit code 1 (command not found). python3 does not resolve under the safebin PATH.
- Branch: `tnn-native-lab`. Working copy `~/workspace/tnn-rsi`.
- Toolchain rule in force: pure Zag only. Forbidden-interpreter invocation = PROCESS-FAIL.

## Execution record (this lane, wave-20261001-2321pdt)

### Spec search
- Searched docs/lab/research-lead/overnight-20260928/ for K-H3, Node2-v2, shared
  consequence substrate; read canonical_ledger/CLAIM_LEDGER.md entries C171,
  C174, C175, C180, C181, C182, C183; hypothesis_frontier/HYPOTHESES.md;
  spec commit 550fa268b (SHARED-SUBSTRATE-COMPLETE).
- Found coherent spec chain. Found frozen prereg for K-H3 validation:
  node2v2_run/FROZEN_PREREG.md, commit 4b05c8011, FROZEN 2026-10-01 18:25:00 UTC.
  No fresh prereg needed; executed the frozen prereg exactly as frozen.
- Working tree clean for all read-only input dirs (git status verified).

### Independent K-H3 re-execution
- Copied committed n2v2_test.zag (SHA-256 verified 99774fbc..., byte-identical
  to ablation abl_base.zag) to kh3_rerun/. Compiled with pinned znc via
  safebin PATH. Ran 3 times.
- 3/3 byte-identical: SHA-256 74c48d5a85087eab5d9c86aebf6075ce69f89be5736422e6bf63e897f527aae9,
  exactly the committed result hash.
- Kill bars: Phase 1 no shift PASS; Phase 2 shift exactly on 3rd revelation
  (30,30,45) PASS; Phase 3 guide 45 PASS; 3/3 deterministic PASS.
- Verdict: K-H3 PASS, independently reproduced.

### Causal ablations re-executed
- Link 1 (disable consequence record, abl_l1.zag committed): 3/3 byte-identical,
  SHA-256 d67cecf5... (matches committed). Phase 2: 30,30,30, no shift. Utility
  judgment reverts to fixed 30. Consequence record NECESSARY.
- Link 3 (disable production read, abl_l3.zag committed): 3/3 byte-identical,
  SHA-256 0d25a574... (matches committed). Write fired (45) but Phase 3 guide
  carries 30. Production read NECESSARY.
- Together with committed L2/L4 results (hash-verified pairs L1=L2, L3=L4):
  all 4 chain links NECESSARY; chain is causal, not correlational.

### Toolchain
- Safebin PATH for every command. `which python3` empty throughout. Zero
  forbidden executables. Pure Zag. No commits outside CONSEQ/ lane dir. Nothing
  pushed. Frozen prereg and source untouched (read-only).
