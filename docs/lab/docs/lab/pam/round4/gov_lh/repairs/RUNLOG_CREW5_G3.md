# RUNLOG — PAM gov-LH crew 5, generation 3 (resume)

Subagent session 74e91fb9 (depth 2/2). Task: complete fable's four kill-bar
repairs evidence legs. Prereg frozen: PREREG_CREW5_REPAIRS.md (committed
alone on tnn-native-lab under docs/lab/pam/round4/gov_lh/repairs/ — not amended).

Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (pinned).
TMPDIR=~/workspace/tmp_commit for all commit tooling.

## Inherited state verification (2026-09-24 ~23:55 PDT)

### d2/ — VERIFIED INTACT
- 8 battery/fixture files present. SHA check vs prereg §2.2 table:
  exemplars.tsv, memory.tsv, B20, B12, B6, B10x, B100x all match.
  **B110.tsv MISMATCH vs prereg print — investigated:** the prereg's printed
  pin is 54 hex chars (f3f6daf8...69942498293994), an INVALID sha256
  (transcription dropped 10 chars "aff07fe7699" mid-string). On-disk file
  hashes to the full 64-char f3f6daf82c420a44a46f6366a3fc441b2a6a78f469
  aff07fe769942498293994, which contains the prereg string as a substring.
  Conclusion: prereg typo, not file corruption. All 24 legs ran against the
  on-disk file; the independent Python oracle re-derives EVERY trial decision
  from the same file (48,020 checked, 0 mismatches). Evidence stands; the
  typo is recorded here and in the verdict (prereg itself is frozen, not amended).
- runs/: 24 organ×battery combos × 3 runs, all trios byte-identical
  (cmp-verified). d2bar binary SHA matches runs/d2bar.sha256
  (098e1f4610087597f5993fb4144e9d65a248b2f8d6abece84dbc366988113252).
- score_d2.py, oracle_d2.py, run_all.sh present.

### o3/ — STALE BINARY FOUND AND REMEDIATED
- o3_run0/1/2.out byte-identical 3x (64ba0892...), printing
  TOTAL=11840 SIX=6 NEVER=1102 INTER=0 SIXPROGPASS=0 SIXPROGFPASS=0.
- Cross-check against the real case_o1.txt with an independent Python census:
  NEVER should be 278 (correct==1 & conf>=700 & prog!=0), and the six
  timbredisc wrongs have prog=0/progF=0 (SIXPROGPASS should be 6).
  The binary's NEVER=1102 equals the UNFILTERED correct&conf>=700 count, and
  SIXPROGPASS=0 despite all six having prog=0 → the binary never reads prog
  as 0 (field-mapping bug in the version it was built from).
- Timestamps: o3audit binary 22:54, o3audit.zag source 23:14 → source was
  fixed AFTER the build; binary never rebuilt. Inherited runs VOID as census
  evidence (byte-identical but wrong instrument).
- REMEDIATION: rebuilt o3audit.zag from the current source with the pinned
  znc → fresh binary (different size: 31417 vs 34279 bytes main, confirming
  different code). 3 fresh runs on the committed case_o1.txt:
  TOTAL=11840 SIX=6 NEVER=278 INTER=0 SIXPROGPASS=6 SIXPROGFPASS=6
  O3-UNTESTABLE-DROPS — byte-identical 3x (a89cbf0e...), matching the prereg's
  frozen expectations (NEVER=278, six all prog==PASS) and the Python oracle.
  Fresh binary + fresh runs installed as o3audit / o3_run{0,1,2}.out.
  Decision outcome is the same either way (INTER=0 < 4 → drops), but the
  census numbers are now correct.

### o1/ — VERIFIED, RUNS NOT STARTED (as inherited)
- case_real/sham/null.txt SHAs match prereg §4.2 pins exactly
  (ab5eb09e / 40d21755 / b1dce9ca). 200 lines each. Format spot-checked.

### fe3a/ — EMPTY (as inherited)

## Leg D2 — scored 2026-09-25 ~00:05 PDT
- Byte-identity: 24/24 trios byte-identical (cmp).
- Oracle: `python3 oracle_d2.py` → checked=48020 mismatches=0 (rc=0).
- Scorer output (repaired bar; min-n=10; original bar on B20 only):

  org batt      n     rel   frac  repaired   orig(B20) clauseA
  D   B20      20    18    90.0%  PASS       PASS      FREL=3/8 KILL-D-clauseA
  R   B20      20    20   100.0%  PASS       PASS      FREL=0/8
  W   B20      20     7    35.0%  KILL       KILL      FREL=0/8
  N   B20      20     0     0.0%  KILL       KILL      FREL=0/8
  D   B12      12    11    91.7%  PASS       -         FREL=3/8 KILL-D-clauseA
  R   B12      12    12   100.0%  PASS       -         FREL=0/8
  W   B12      12     3    25.0%  KILL       -         FREL=0/8
  N   B12      12     0     0.0%  KILL       -         FREL=0/8
  D   B6        6     6   100.0%  UNDECISIVE -         FREL=3/8 KILL-D-clauseA
  R   B6        6     6   100.0%  UNDECISIVE -         (all UNDECISIVE, n=6<10)
  W   B6        6     0     0.0%  UNDECISIVE -
  N   B6        6     0     0.0%  UNDECISIVE -
  D   B110    110   103    93.6%  PASS       -         FREL=3/8 KILL-D-clauseA
  R   B110    110   110   100.0%  PASS       -         FREL=0/8
  W   B110    110    11    10.0%  KILL       -         FREL=0/8
  N   B110    110     0     0.0%  KILL       -         FREL=0/8
  D   B10x   1078  1053    97.7%  PASS       -         FREL=3/8 KILL-D-clauseA
  R   B10x   1078   110    10.2%  KILL       -         FREL=0/8
  W   B10x   1078   101     9.4%  KILL       -         FREL=0/8
  N   B10x   1078     0     0.0%  KILL       -         FREL=0/8
  D   B100x 10731 10487    97.7%  PASS       -         FREL=3/8 KILL-D-clauseA
  R   B100x 10731  1095    10.2%  KILL       -         FREL=0/8
  W   B100x 10731   827     7.7%  KILL       -         FREL=0/8
  N   B100x 10731     0     0.0%  KILL       -         FREL=0/8

- Findings: repaired bar KILLS W and N on every n>=10 battery; PASSES D
  clause (b) at all scales; R PASSES at 1x but is KILLED at 10x/100x
  (10.2%) — the preregistered density falloff of R's fixed-300-point
  ε-recognition memory (organ property, measured honestly). B12 exercises
  the repair's new decisive range (W 3/12 KILL, N 0/12 KILL) where the
  original bar was untestable. B6: all UNDECISIVE (min-10 floor works).
  Verdict-change on existing R3 evidence (B20): NONE — D/R PASS (b) under
  both bars; D stays killed at clause (a) under both (FREL=3/8).

## Leg O3 — census completed 2026-09-25 ~00:10 PDT
- After the stale-binary remediation above: 3x byte-identical runs
  (a89cbf0e2f6e12e13bfb7d5f0847dcd13f54740df108a03764496ea60874ec9d):
  TOTAL=11840 SIX=6 NEVER=278 INTER=0 SIXPROGPASS=6 SIXPROGFPASS=6
  O3-UNTESTABLE-DROPS.
- INTER=0 < 4 → per the repair's own terms O3 is UNTESTABLE and DROPS.
  The six timbredisc wrongs all already emitted PASS (prog=0, progF=0),
  confirming the repair's diagnosis that O3 "cannot touch already-PASS items".
  No extended-scale run authorized.

## Leg O1 — completed 2026-09-25 ~00:20 PDT
- Rebuilt committed src/o1.zag (digest-verified b395e10f...) with pinned znc
  → o1/o1bin (binary excluded from commits).
- §4.1: mode 0/1 on committed evidence/case_o1.txt (digest-verified ed1ad01f),
  3x each byte-identical AND byte-identical to the committed evidence files
  (mode0 a946b989..., mode1 54122164... — match digests.sha256).
- §4.2: 3 cases × 2 modes × 3 runs, all trios byte-identical.
- score_o1.py asserts the exact prereg-predicted metrics (fails loud on any
  deviation) and applies the repaired bar:

  real     K1=95.00% K2'=95.00% gap= 0.00pp RK3=10.00% RK3'=16.00% rise=+6.00pp -> SURVIVE
  sham     K1=95.00% K2'=95.00% gap= 0.00pp RK3=10.00% RK3'=10.00% rise=+0.00pp -> KILL-clause2
  null     K1=95.00% K2'=70.00% gap=25.00pp RK3=10.00% RK3'=10.00% rise=+0.00pp -> KILL-clause1
  fid-4.1  K1=96.37% K2'=86.57% gap= 9.80pp RK3= 9.44% RK3'= 9.62% rise=+0.18pp -> KILL-clause1

- real under ORIGINAL bar: closed_gap=25.00pp, rise=+6.00pp < half-gap=12.50pp
  → KILL (demonstrates the FATAL defect the repair cures).
- ALL ASSERTIONS PASS (scorer rc=0).

## Leg FE3a — completed 2026-09-25 ~00:25 PDT
- Built fe3a/fe3a.zag (pure Zag, zero RNG, []u8 arena + LE64 accessors) with
  pinned znc. Frozen Python prototype prototype_fe3a.py written first;
  prototype output matches the prereg's frozen prediction exactly.
- 3 runs byte-identical (fe45c6d1966e330954b9a97f57cd00afb19cea298628f4549b357e3892292e58),
  each byte-identical to the prototype output:
    it=0 T=100 reversals=1 first_rev=0 errs=10 T_next=99
    it=1 T=99 reversals=1 first_rev=0 errs=8 T_next=98
    it=2 T=98 reversals=1 first_rev=0 errs=6 T_next=97
    it=3 T=97 reversals=0 errs=4 STOP
    FINAL T=97 errs=4 iters=4
- PASS → FE3b buildable-in-principle (FE3b itself out of scope).

## Commit
- Evidence + verdict committed to tnn-native-lab branch under
  docs/lab/pam/round4/gov_lh/repairs/ via ~/workspace/commit_racefree.py
  (TMPDIR=~/workspace/tmp_commit). No binaries, .zagd, or .zag-cache committed.
- Commit: de7da0f9c1bd924f5bdb244479960e0c72543d68 on tnn-native-lab
  (parent bfbc758bf446), 128 files under docs/lab/pam/round4/gov_lh/repairs/
