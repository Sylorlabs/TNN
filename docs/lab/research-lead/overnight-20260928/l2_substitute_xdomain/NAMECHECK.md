# NAMECHECK: L2-SUBSTITUTE-XDOMAIN (cross-domain substitute with interface adaptation)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.

## Step 0: toolchain guard (recorded before any research computation)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`:
  `linked: 36 tools`, `znc: OK (.../src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns NOTHING (rc=1).
  Verified 2026-10-02 at worker startup, before any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler only).
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.
- Pure Zag for all scientific computation. Shell only: znc invocation,
  running binaries, git ops, file movement, sha256sum/cmp checks.

## Reading disclosures

- Read `l2_substitute/REPORT.md` (predecessor lane, verdict
  L2-SUBSTITUTE-COMPLETE): SUBSTITUTE operator idiom (stale-detect,
  piece search, execution verification, type-16 adapted-from
  provenance, five arms, driver-flag causal controls), and its
  stated open future work: "Cross-domain substitution and
  substitution with interface adaptation (endpoints not exactly
  matching) are open future work." This lane is that follow-on.
- Read `l2_substitute/PREREG.md` (kill-bar structure precedent K-1..K-10).
- Skimmed `l2_substitute/learner.zag` for pinned-znc-safe Zag idioms
  only (u8-cell fact store, cursor emit helpers, no `as *i32` slices,
  no `!(A && B)` while-conditions, shallow if-nesting). No code copied;
  this lane's learner is designed from this lane's frozen PREREG.md.
  All function names use the `xa_` prefix; trace tags use `XA-`.
- Noted `xdomain_select5` (another worker's staged, uncommitted lane):
  cross-domain SELECTOR over value-level composition, a different
  operation (selection among options, not L2 substitution with
  interface adaptation). No overlap in claim; did not read its
  implementation beyond NAMECHECK.md header to confirm non-overlap.

## Steps

- [x] Step 0: toolchain guard (above).
- [x] Step 1: PREREG.md frozen, committed ALONE (this file + PREREG.md).
  Commit 6bed092c3, 2026-10-02. PREREG_AMENDMENT1.md committed at
  d6d8e01ee (pre-implementation: fold-discovery valrel skip,
  FULL A_SEARCH 671->865). PREREG_AMENDMENT2.md committed at
  4d69d7459 (pre-verdict: FULL A_SEARCH 865->941, pure arithmetic
  correction of the arity LINK loop count).
- [x] Step 2: implementation (learner.zag, world.zag, driver.zag,
  xa_full.zag, xa_bin). One-line diff class fixes only:
  map_create moved to after verification success (prereg:
  never promote an unverified graph; fixes NOADAPT NM=4->3),
  driver F-COUNT 865->941 per AMENDMENT2. Binary compiles with
  pinned znc (exit 0).
- [x] Step 3: 3/3 runs byte-identical (sha256
  eea8678d436a927788fdb451d5fadecf3ff39cc563539a2ec9a9d29e9d439b08),
  REPORT.md. Verdict: L2-SUBSTITUTE-XDOMAIN-PASS. All 8 kill
  bars PASS, zero falsifiers.
