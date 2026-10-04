# REPRO report: H-PI-REV2 step 4 independent reproduction (wave-20260930-2321pdt)

Lane: H-PI-REV2 step 4 (11-step frontier pipeline). Claim under test:
F3a3 BUILD-PASS on corrected bars K-F3-1..4, recorded in wave
wave-20260930-1121pdt (evidence commit d1b6ec51f). This worker is an
independent reproducer. It did not modify the implementation, the
prereg, or the bars.

## Inputs located and verified

1. Frozen prereg: commit 53256838f ("Prereg: H-PI-REV2-F3a3 second
   corrected re-freeze (FROZEN; committed alone)"), committed
   2026-09-30 18:28:30 UTC. Verified ancestor of the evidence commit
   d1b6ec51f (2026-09-30 18:29:55 UTC): git merge-base --is-ancestor
   returns true. Prereg committed alone and strictly before evidence.
2. Implementation: commit 847a8f10f
   ("H-PI-REV2 implementation under frozen prereg 7c11ac5af:
   procedure-invention v2 revision machinery (pure Zag)").
   Source extracted via git cat-file from that commit:
   docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag,
   840 lines, sha256
   dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12.
   This matches the recorded committed blob sha and the working tree
   (RESULT_F3A3.md records the same sha256). Verified ancestor of the
   evidence commit. No modification by this worker: the file was
   written only into /tmp and built there; the repo working tree file
   was never touched.
3. Committed evidence: d1b6ec51f contains
   docs/lab/rsi/runs/wave-20260930-1121pdt/f3a3/EVIDENCE_F3A3_run{1,2,3}.txt.
   Evidence run1 sha256 is
   b5389d713357d37bd5ca9c05b781e80d57a3a764f3cac60ebe1cd17de9527c8e
   (the b5389d71 handle in the task statement).

## Reproduction procedure

- Built the extracted source in /tmp with the safebin znc (pinned
  binary src/tools/toolchain/znc_linux_x86_64_abed8aa1):
  `znc proc_revise2.zag -o f3a3_repro_bin`. Build exit 0.
  The only analyzer output was the pre-existing benign A0102 lint on
  an ignored loadseq return at line 607, identical to the lint
  reported in RESULT_F3A3.md for the original build (pre-existing by
  construction: source is byte-identical to the committed blob).
- Ran the binary three times with argv[1]="v" (adversary byte per the
  F3a2 declared rule, last letter of the corrected allowed set
  {k,m,r,v}):
  run1 exit 0, stderr empty; run2 exit 0, stderr empty; run3 exit 0,
  stderr empty.

## Results

- Repro run1 sha256: b5389d713357d37bd5ca9c05b781e80d57a3a764f3cac60ebe1cd17de9527c8e
- Repro run2 sha256: b5389d713357d37bd5ca9c05b781e80d57a3a764f3cac60ebe1cd17de9527c8e
- Repro run3 sha256: b5389d713357d37bd5ca9c05b781e80d57a3a764f3cac60ebe1cd17de9527c8e
- 3/3 byte-identical across repro runs (determinism re-demonstrated).
- cmp: each repro run is byte-identical to the corresponding committed
  evidence file EVIDENCE_F3A3_run{1,2,3}.txt (2282 bytes each).
- All three: exit 0, empty stderr, "=== RESULT fails=0 ===", "BUILD-PASS".
- Bar markers re-checked on the reproduction output with fixed-string
  grep: COUNTEREXAMPLE_DETECTED(vab) present; DIAGNOSIS pos=0
  byte=118 present; PRIMITIVE-CONSTRUCTED pos=0 byte=118 present;
  CHECK P8-F2-alt-C0: PASS present; VERSION v3 ACTIVE present with
  zero "VERSION v4"; "vab"->"vvv" ("PREDICT vab -> vvv [ok]")
  present; priors unchanged ("xab"->"xxx", "abc"->"ccc" [ok]) with
  zero "wab"; reuse "vqw"->"vvv" with "CHECK
  P8-F2-reuse-no-revision: PASS" present; R-probe 8/8 retention
  lines byte-identical to committed evidence by construction of cmp.
  K-F3-1: PASS. K-F3-2 (determinism): PASS (3/3 byte-identical this
  run, plus byte-identical to the inherited evidence). K-F3-3 and
  K-F3-4 remain the inherited verdicts from F3a2, untouched by this
  lane.

## Verdict

REPRO-PASS. Independent reproduction from committed source is
byte-identical to the committed evidence on all three runs. No
divergence found anywhere: exit codes, byte counts, sha256 values,
stderr emptiness, fails=0, adversary byte v, and all K-F3-1..4 bar
markers reproduce exactly.

## Provenance

- SOURCE_EXTRACT: git cat-file from 847a8f10f, /tmp only.
- BUILD: pinned znc in safebin, /tmp only; binary not committed.
- REPRO RUNS: /tmp/f3a3_repro/REPRO_F3A3_run{1,2,3}.txt, copied into
  this lane directory as evidence.
- COMPARISON TARGETS: committed evidence blobs from d1b6ec51f (read
  from the working tree and cross-checked against the commit; the
  working tree evidence sha matches the committed blob).
- This lane committed nothing except this report package (report,
  NAMECHECK, three repro run files). Pure Zag; zero Python.

No em-dashes in this documentation.
