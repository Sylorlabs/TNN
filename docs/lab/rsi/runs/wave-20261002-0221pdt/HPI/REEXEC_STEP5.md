# REEXEC: H-PI-REV2 step-5 re-execution under the AMENDED prereg (wave-20261002-0221pdt, HPI lane)

Lane: docs/lab/rsi/runs/wave-20261002-0221pdt/HPI/
Executor: HPI lane worker (this file's author). Safebin toolchain guard
verified at Step 0 of NAMECHECK.md (python3 absent; pure Zag only).

## Frozen prereg binding (read-only; not modified)

Amended prereg: docs/lab/rsi/runs/wave-20261001-1721pdt/HPIREV2/PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md
Frozen alone at commit 72168c60803b95b3b586eb1cf6f1fc9bd001b174
(dated 2026-10-02 00:39:47 UTC; 4 files, all writing-only, no
implementation). The prereg text was re-read in full from the working
tree before any build or run; it is unambiguous and reachable, so no
BLOCKED condition arose.

### Commit-order self-check

- 72168c608 strictly precedes the first commit adding any step-5
  re-execution artifact (fdd37d7fd92, 2026-10-02 03:48:26 UTC), which
  added the 2021pdt re-execution transcripts.
- This lane's dir was empty at lane start; all builds and runs below
  were created after the freeze. No implementation predates it.
- Incident note (transparent): commit f461e812d (2026-10-02 07:19:22
  UTC, "H5R2-SKEPTIC2 implementation") accidentally deleted the amended
  prereg file from the tree along with 4833 other wave files. The
  LANE-AUDIT record (commit 84727be29) documents the mass deletion and
  byte-identical restoration. Verification: git hash-object of the
  restored working-tree file returns 08872e3d8cd920a08be9d7d15ed6de65842da68b,
  exactly the blob recorded in 72168c608. The text read for this
  re-execution is byte-identical to the frozen text.

### Byte-identity of frozen mechanism and baseline sources

- Frozen mechanism: proc_revise2.zag at commit 847a8f10f (commit type,
  not blob; the mechanism file inside it):
  sha256 dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12
  (committed blob, working tree, and this lane's copy all match).
- Baseline sources (byte-exact cp from the recorded lanes, sha256
  re-verified after copy):
  b0.zag  c6ccc64ab57e962607ef3cccc37c3374c9d0b486b21e4bb4542bfd6c7202f7d6
  b1.zag  532ec1df6d4acc56dcaf1841feb69815770641700688374bed61f8a00dd936ae
  b2.zag  9c476796b1bdb8336a93feb1fb3352081848982e8043d80b9e387d376b0100ca
  b1t.zag 3f31a4da83918809137f0f4fc5eb6914f34fd446f75ca45814066e669bf9d3d3
  (b0/b1/b2 match the wave-20261001-1421pdt originals byte for byte;
  b1t is the amended-K-SB4b source from the 2021pdt lane.)
- Cognition source delta: 0 (all sources are byte-identical copies of
  recorded frozen/recorded artifacts; no new cognition code written).

## Builds (pinned znc, safebin PATH)

Command: `znc <src>.zag -o <bin>` for b0, b1, b2, b1t, mech_revise2.zag.
All 5 builds exit 0. Raw build logs in /tmp (the compiler-emitted
A0102 lint em-dash stays out of the lane per K-SB6).

Binary sha256 (each matches the 2021pdt record byte for byte):
- b0_bin   4f5698c6a4a980e153ba866108cedd335aee0598c882545eaed9af254478290f  22331 bytes
- b1_bin   ba47b700f03d34701371ee7d3aafdd570f99e0f5451b10df6a52b0e08480a7d2  34776 bytes
- b1t_bin  dbd735384feeffc188fe28ee9c83275fbc0dc310a356a5ec8e9a74c4f6f109a6  34825 bytes
- b2_bin   5de7632da1fd1cb1a8d2145932fb8afc4865f6990e51674c4e014930b370c2b3  26588 bytes
- rev2_r_bin 7b4caa77d2e67e6df14f5f1fecf0f75180d50338961b80e00073ec06883a395c 106770 bytes

## Run matrix (15 runs, sealed)

- ./rev2_r_bin r (x3); ./b0_bin (x3); ./b1_bin (x3); ./b1t_bin (x3); ./b2_bin (x3).
- Adversary byte 'r' (114): last letter of frozen set {k,m,r} per
  ADVERSARY_BYTE_SET4.md; disjoint from every frozen fixture input
  string by that audit.
- All 15 runs exit 0. Wall ms (run order):
  REV 6/5/6; B0 3/3/3; B1 4/4/4; B1T 3/4/3; B2 3/4/3.

## Determinism (K-SB5)

- cmp across run1/run2/run3 stdout per binary: all clean (5/5 binaries
  3/3 byte-identical).
- All 15 stderr files are 0 bytes.
- Stdout sha256 (run1; runs 2-3 identical), each byte-identical to the
  wave-20261001-2021pdt re-execution record:
  REV d5eb722d8b0a204ce155e7d82f237fa6682d88d9d0d885b930629e1c69913801
  B0  c910b18728e5cd8c14da09ac49597700c2ea1c447c75a530976ad3b8b96ad2ab
  B1  0c5f9370256fcb37b3e92730fd44e8d98bb645c84fa8eefaba0d78ae844043c4
  B1T 3599e93a07f0e6bb3041e8a140bc446435f9910c74cebcedf59ca7f2b6a3afd5
  B2  ca3df82dd472f039db719c54adaabc867058ddb5b555c719fa146543cb528c7c

## Per-bar scorecard (frozen thresholds, amended prereg 72168c608)

- K-SB1 (problem real): PASS. B0: "B0 PREDICT rab -> bbb" (3/3
  identical). Kill needed "rrr"; the revision problem is real.
- K-SB2 (revision cheaper than re-search): PASS. revision_evals=5
  (3 diagnosis candidates ranked + 1 primitive-construction
  byte-equality test + 1 SPECIALIZE application, per the prereg
  formula; transcript lines: "DIAGNOSIS pos=0 byte=114 conflicts=0",
  "PRIMITIVE-CONSTRUCTED pos=0 byte=114", "VERSION v3 ACTIVE (parent
  v2)"); b1_enumerated=1055; 5 < 1055 strictly.
- K-SB3 (revision beats storage on reuse): PASS. REV: "PREDICT rqw ->
  rrr [ok]", "CHECK P8-F2-reuse-no-revision: PASS"; zero
  DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after the reuse check
  (lines 69+). B2: "B2 PREDICT rqw -> www" (mispredict, no stored
  entry) vs "B2 PREDICT rab -> rrr" (stored entry, correct).
- K-SB4a (revised procedure correctness): PASS. All 5 checks emit
  [ok]: abc->ccc, xy->xx (conflict-rule update), defg->gggg,
  rab->rrr, rqw->rrr; "=== RESULT fails=0 ===", BUILD-PASS.
- K-SB4b (baseline competence): PASS. B1T: first-fit-index=38 (>= 0;
  matches frozen v1 discovery index 38 [N C1 SUB]),
  programs-evaluated=39, fails-on-T=0.
- K-SB4c (verified-impossibility recheck): PASS. B1 over T+F1r:
  first-fit-index=-1, programs-enumerated=1055 (matches the K-RV2-1b
  verification: exhaustive, no false negative).
- K-SB5 (determinism): PASS. 15/15 exit 0; 3/3 byte-identical stdout
  per binary; all 15 stderr files 0 bytes.
- K-SB6 (purity and docs): PASS. Pure Zag only: executables invoked
  were safebin bash, cp, cmp, date, diff, grep, head, awk, sha256sum,
  stat, wc, znc. `which python3` and `which python` return nothing
  under the safebin PATH. check_no_dash.sh byte scan of all lane text
  files (NAMECHECK.md, *.zag, *.txt): exit 0, zero em-dash and zero
  en-dash bytes. Compiler-emitted lint em-dash confined to /tmp build
  logs.

## Machine-greppable cost accounting

revision_evals=5
b1_enumerated=1055
b1_first_fit_index=-1
b1_wall_ms=4
b1t_wall_ms=3
revision_wall_ms=6
b0_wall_ms=3
b2_wall_ms=3
binary_bytes_rev2_r_bin=106770
binary_bytes_b0_bin=22331
binary_bytes_b1_bin=34776
binary_bytes_b1t_bin=34825
binary_bytes_b2_bin=26588
source_delta_lines=0
new_semantic_cases=0
new_modes=0
new_bridges=0

(wall_ms are run1 of each binary, same convention as prior records;
source_delta_lines=0 because all sources are byte-identical copies of
recorded artifacts, no new cognition code.)

## Shared-code disclosure (sealing protocol)

Baselines share only the frozen benum algorithm (B1, B1T) and the
frozen v1 procedure (B0, B2); byte-exact extracts of the frozen
Section A discovery machinery from proc_revise2.zag (committed
847a8f10f); no Section B revision-machinery code (observe, diagnose,
build_test, specialize, branch predict, rollback) is shared with any
baseline. The F1r-reuse input "rqw" is presented only after VERSION v3
is ACTIVE.

## Honest boundaries

Bounded L2 ceiling per the amended prereg: a step-5 PASS means the
revision is genuinely cheaper than re-search and genuinely reuses
beyond storage; it is not evidence toward L3 and must not be claimed
as such. No protected-core changes. The original step-5 verdict
(BASELINE-FAIL, wave-20261001-1421pdt) stands unchanged and is not
retroactively altered by this re-execution.

## Verdict

REEXEC-PASS. H-PI-REV2 step-5 re-execution under the amended prereg
72168c608: all 8 amended bars pass (K-SB1, K-SB2, K-SB3, K-SB4a,
K-SB4b, K-SB4c, K-SB5, K-SB6); the re-execution reproduces the
wave-20261001-2021pdt step-5 PASS transcript-byte-identically. Citation
with debate Q2 OVERTURN qualifiers (binding, from the
wave-20261001-2321pdt debate ruling): the H-PI-REV2 bound holds only on
rank-diagnosable single conflicts with probe-dependent trip. This
REEXEC-PASS inherits exactly those qualifiers: it re-verifies the
step-5 baseline comparison on the frozen fixtures, not the broader
unqualified bound, which ADV-S4 falsified.

No em-dashes in this documentation.
