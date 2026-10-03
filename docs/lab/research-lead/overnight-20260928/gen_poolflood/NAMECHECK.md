# NAMECHECK: GEN-POOLFLOOD

Worker: gen-poolflood (replacement; the prior worker was interrupted
before producing work). Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/gen_poolflood/`
Branch: lane-genpoolflood-20261003 (created from tnn-native-lab
88626d65b). Work is performed in the git worktree
~/workspace/tnn-rsi-gpf: the ~/workspace/tnn-rsi working tree carried
other workers' uncommitted changes (including permission-denied sealed
files that broke both `git stash` and `git checkout -b`), so an
isolated worktree on the required branch is used instead; the lane
path inside the repo is unchanged.
Task: pool-flood battery at nm=11 on the canonical GEN-REDIM
composer, per the GEN-NM10 (C438) follow-up: confirm the silent-drop
signature is NM-independent. New driver only; canonical sources
untouched.

## Step 0: toolchain guard (worker governance)

- Safebin active from the FIRST command of this lane's work:
  `export PATH="$HOME/safebin"` prefixes every shell command in this
  session, starting with the very first command (which verified
  `which python3` / `which python` return nothing before doing any
  other work).
- The task's `docs/lab/research-lead/overnight-20260928/safebin_setup/
  setup_safebin.sh` path does not exist (same as GEN-NM10);
  `~/safebin` was already provisioned with 49 tools including the
  pinned znc 2026.07.0-dev, verified before any other command.
- All computational research operations in pure Zag via pinned
  safebin znc. Shell only for: znc, binary runs, git ops, file
  assembly, byte-verification (cmp/sha256sum/grep/sed/awk/head/
  tail/wc).
- No forbidden interpreter invocation. Any such invocation would make
  this wave PROCESS-FAIL per governance (self-disclosure rule).
- Git via /usr/bin/git directly (safebin git symlink EPERM defect; see
  the workspace operating manual); explicit pathspecs only; commits
  local, never pushed; no git reset on shared branches.

## Step 1: canonical source digests (verified before implementation)

GEN-REDIM lane
(docs/lab/research-lead/overnight-20260928/gen_redim/, canonical per
GEN-REDIM-CLEAN, C434), the frozen mechanism under test. This lane
MUST NOT modify these files; build.sh re-verifies the digests (kill
bar F5):

- rbase.zag (337 lines):
  17dd1cbdeb6a36e654f0b2d8fc57a730a7e58da8c5097081d466de1cc4eb8afc
- rgen.zag (270 lines):
  3c7ebbe140b341cd90d7629117fcc4d7604cb86bc2cb4505ff0ebb31b3572476
- rgen_nomain.zag (rgen.zag with main stripped; assembly input):
  da8760b68ca8d710a3d2545a484f65bf3d14d97bbcd3005422a17c989fb9dfcc
- rd_sec_S5.txt (canonical nm=4 pool-flood signature, GEN-REDIM C9):
  a43078d45410faefcc46689ea2951a1857e4f23af07aace7da202239658386d1
  (2735 lines, 27349 bytes: 3 INTER=, 2731 INTER2=, 0 WIDEN=1,
  ARM=GEN PROB=S5 ANS=-2 TRIES=2734)

Frozen rules reused unchanged: dynamic NM layout (GEN-REDIM PREREG
Section 2; the pool regions MOVE with NM: VPOOL 1024->1408,
KPOOL 1280->1664, PROV 1536->1920 from nm=4 to nm=11), tried2 pair
encoding m*4096+i*64+j, 64-value pool cap with silent drop
(gen_addval: dup scan, add iff n<64, else return -1 with no line and
no panic), 64-entry tried2 cap, 6-round cap, WIDEN-once, admission
(g_khas, empty=compatible), trial order (1-input MAPs in id order,
then 2-input MAPs in id order; lex pair order), round snapshots,
quiet-round detection, provenance-closure recording, one ADD2 class.

## Step 2: battery spec (frozen in PREREG.md Sections 4-5)

- PF1: setup_pf1 (byte-exact copy of the frozen setup_s5: 4 MAPs),
  world_new_nm(4), gen_solve(s=201, exp=999999, nm=4). Predicted:
  PF1 section byte-identical to the canonical S5 section modulo the
  PROB label (S5->PF1): ANS=-2, TRIES=2734, 3 INTER= lines,
  2731 INTER2= lines, zero WIDEN=1 lines.
- PF2: setup_pf2 (S5 facts and S5's 4 MAPs m0..m3, plus 7 IDENT
  distractors m4..m10 with teach(201,201) giving in{1}), 
  world_new_nm(11), gen_solve(s=201, exp=999999, nm=11). Predicted:
  PF2 section byte-identical to the canonical S5 section with
  exactly 7 "INTER=201" lines inserted after line 3 and the ARM line
  re-labeled (PROB=PF2, TRIES=2741): ANS=-2, TRIES=2741,
  10 INTER= lines, 2731 INTER2= lines, zero WIDEN=1 lines. The full
  hand derivation is PREREG Section 5: the 7 extra structures are
  tried exactly once each (R1, on the kind-1 seed) and never touch
  the pool dynamics again, so the flood's 2731 pair-result lines are
  predicted byte-identical to nm=4.
- Assembly: canonical rbase.zag + canonical rgen_nomain.zag +
  pf_main.zag; exactly one main per assembly (grep check).
- Kill bars F1-F7 per PREREG Section 7; verdict mapping per
  PREREG Section 8; boundaries per PREREG Section 9.
