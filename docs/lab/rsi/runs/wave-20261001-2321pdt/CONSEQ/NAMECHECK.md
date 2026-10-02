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

## K-H3 disambiguation (coordinator pointer verification, 2026-10-01)

Per coordinator pointer, read the CLAIM_LEDGER.md K-H3 entries and
H3LITE_DESIGN.md K-H3 definition to check whether the K-H3 in those
files is a different K-H3 from the Node2-v2 K-H3 this lane executed.

Result: SAME K-H3, direct lineage. No second K-H3 exists.

Evidence:
- H3LITE_DESIGN.md Section 6 drafts K-H3 (Policy Revisability): for every
  structural decision not determined by immediate input, the prereg must
  list (1) the decision (examples: "trial search order", "guide default
  action", "repair topology selection"); (2) the learner-state node and
  fields; (3) the production write path; (4) the triggering experience;
  (5) a sealed demonstration. Failure conditions: (a) source-literal,
  (b) read-only policy, (c) unreachable write path, (d) researcher-encoded
  histories. DRAFT-NOT-FROZEN at that point.
- The Node2-v2 frozen prereg (commit 4b05c8011, executed by this lane)
  Section 4 performs the K-H3 Audit with the same six elements for the
  structural decision "guide default action" (one of the exact examples
  in the H3LITE_DESIGN.md draft) and the same (a)-(d) failure conditions.
- The frozen prereg's stated purpose: replace the unreachable H3-lite
  Node 2 (guide template policy) with a reachable experience-dependent
  write path, "preserving the diagnostic intent". The frozen H3-lite
  prereg (9084a7760) Node 2 was the guide-default-action node; its
  unreachability was proven in b0ad6c5d3.
- CLAIM_LEDGER.md C171 is explicitly "NODE2V2 K-H3 PASS + ABLATION",
  the same result this lane independently reproduced.
- TNN3_ROADMAP.md references the same K-H3 draft bar lineage (commits
  76231baa8, 22197da2c) as the policy-revisability kill bar.

Conclusion: one K-H3 lineage, from draft (H3LITE_DESIGN.md Section 6) to
frozen instantiation (Node2-v2 prereg 4b05c8011). The validation verdict
(VALIDATION-PASS) stands against the correct, intended K-H3.
