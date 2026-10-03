# NAMECHECK: GEN-NM10

Worker: gen-nm10. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/gen_nm10/`
Branch: lane-gennm10-20261003
Task: NM=10+ batteries on the canonical GEN-REDIM composer: B1 10-chain
(nm=11, layout-hold + round-cap decline) and B2 fan-out/fan-in DAG
(nm=11, composition at 10+). New drivers only; canonical sources
untouched.

## Step 0: toolchain guard (worker governance)

- Safebin active from the FIRST command of this lane's work:
  `export PATH="$HOME/safebin"` (the lane's setup_safebin.sh path did
  not exist; `~/safebin` was already provisioned with 49 tools
  including the pinned znc, and was verified before any other command).
- `which python3` returns nothing; `which python` returns nothing
  (verified in the lane shell before any other command).
- All computational research operations in pure Zag via pinned safebin
  znc. Shell only for: znc, binary runs, git ops, file assembly,
  byte-verification (cmp/sha256sum/diff/grep/sed/awk).
- No forbidden interpreter invocation. Any such invocation would make
  this wave PROCESS-FAIL per governance (self-disclosure rule).
- Git via /usr/bin/git directly (safebin git symlink EPERM defect, per
  AGENTS.md); explicit pathspecs only; never git reset on a shared
  branch; dedicated lane branch lane-gennm10-20261003 (created from a
  HEAD containing GEN-REDIM-CLEAN).

## Step 1: canonical source digests (verified before implementation)

GEN-REDIM lane
(docs/lab/research-lead/overnight-20260928/gen_redim/, canonical per
GEN-REDIM-CLEAN commit c28ac7ad3), the frozen mechanism under test.
This lane MUST NOT modify these files; build.sh re-verifies the
digests (kill bar N5):

- rbase.zag (337 lines):
  17dd1cbdeb6a36e654f0b2d8fc57a730a7e58da8c5097081d466de1cc4eb8afc
- rgen.zag (270 lines):
  3c7ebbe140b341cd90d7629117fcc4d7604cb86bc2cb4505ff0ebb31b3572476
- rgen_nomain.zag (rgen.zag with main stripped; assembly input):
  da8760b68ca8d710a3d2545a484f65bf3d14d97bbcd3005422a17c989fb9dfcc

Frozen rules reused unchanged: dynamic NM layout (GEN-REDIM PREREG
Section 2), tried2 encoding m*4096+i*64+j, 64-pool / 64-tried2 /
6-round bounds, WIDEN-once, admission, trial order, round snapshots,
quiet-round detection, provenance-closure recording, one ADD2 class.

## Step 2: battery spec (frozen in PREREG.md Sections 4-5)

- B1: setup_b1, 10-chain, nm=11, gen_solve(s=201, exp=3).
  Predicted: ANS=-2, TRIES=66, zero WIDEN=1 lines, exact 67-line
  block (66 INTER= lines + ARM line) per PREREG Section 4.
- B2: setup_b2, fan-out/fan-in DAG (chains A/B/C converge via m8),
  nm=11, gen_solve(s=301, exp=315).
  Predicted: ANS=315, TRIES=67, zero WIDEN=1 lines, exact 68-line
  block (60 INTER= + 7 INTER2= + ARM line) per PREREG Section 5.
- Assemblies: canonical rbase.zag + canonical rgen_nomain.zag +
  nm_b1main.zag (resp. nm_b2main.zag); exactly one main each.
- Kill bars N1-N7 per PREREG Section 7; verdict mapping per
  PREREG Section 8; boundaries per PREREG Section 9.
