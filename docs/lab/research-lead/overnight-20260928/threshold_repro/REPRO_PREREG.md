# Threshold Mechanism Independent Reproduction: Preregistration

Date: 2026-09-30. Worker: Threshold Mechanism Independent Reproducer.
Status: FROZEN. Committed before any reproduction build or run.

## 0. Standing-rules name-check

1. Pure Zag only. No Python at any stage: extraction, building with znc,
   running, verification, byte checks. Shell tools only: sha256sum,
   md5sum, cmp, grep, wc, git, diff. Byte checks via the shell-only
   snippet docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
   Zero Python invoked from task start. LOOP_STATE.md name-checked
   (standing owner rules; fork testing is wave-level and does not govern
   this reproduction; pure-Zag red line scope; shell-only byte checks).
2. No em dashes in loop documentation. This document uses hyphens only
   and is shell-checked before commit.
3. This prereg commit strictly precedes any reproduction build or run
   commit (commit-order self-check).
4. Base sources are the committed files at d0d296650 ONLY. The
   uncommitted /tmp debug build (min slice 1, disclosed during the tax
   investigation) is NOT canonical evidence and is NOT used at any stage.
5. The contaminated research paper
   (docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md)
   is not touched.
6. Commits local, owned pathspec only
   (docs/lab/research-lead/overnight-20260928/threshold_repro/).
7. Other workers' files are not touched. If a git lock is encountered,
   wait; never remove a live lock.

## 1. Source of truth (read from committed evidence before any citation)

- Result commit: d0d296650 (THRESHOLD-PASS).
- Builder prereg: 7ae3a88fa (CONDITIONAL-THRESHOLD-PREREG-FROZEN).
- v2 base: b0d1749f2 (CONDITIONAL-TAX-FAIL).
- Frozen committed numbers, from RESULT_CONDITIONAL_THRESHOLD.md at
  d0d296650:
  - K3 determinism: R3 md5 12f93b593d65bb986e5e23ad9df33d3d (3/3);
    R1 md5 cc0300294803ee8ee8d684ced90d6aad (3/3);
    FREC md5 bde90e4686883846724d56b4ebd9c81f (3/3);
    all nine .err files zero bytes; zero Python.
  - P1'' (CONDHIT round <= 2): round=0. R3 phase-2 round 0, en=8,
    minsl1=min(4,8/8)=1.
  - P2'' (A2-PASS == 1): A2 REUSE_IV 5 true=64/64 HAS_D=1;
    A2 SCRATCH_IV 24 true=52/64.
  - P3'' (DROUND < 4): DROUND=1 (frozen baseline 4).
  - P4''(a) (A1-PASS == 1): PASS.
  - P4''(b) (R1 PASS_SEEDS >= 0/5): 1/5 (frozen 0/5; seed 84044 hits
    64/64). The R1 battery prints VERDICT=R1-FAIL (F-R1 fired) as its
    internal verdict; the frozen bar is on PASS_SEEDS only.
  - P4''(c) (FREC bests >= frozen): I1 best 48/64 (>=46/64);
    I2 best 63/64 (>=63/64); I3 best 40/64 (>=40/64, seed S33).
  - F-CASE (nine audits): none fire.
- Frozen bars (from 7ae3a88fa): K1 prereg precedes implementation; K2 all
  nine runs complete; K3 pure Zag, 3/3 byte-identical, zero stderr;
  P1'' CONDHIT round <= 2; P2'' A2-PASS == 1; P3'' DROUND < 4;
  P4'' A1-PASS == 1, R1 PASS_SEEDS >= 0/5, FREC I1 >= 46/64,
  I2 >= 63/64, I3 >= 40/64; F-CASE nine audits silent.

## 2. Rebuild plan (from committed source only)

1. Extract r3h.zag, r1h.zag, frch.zag from d0d296650 via git show into
   scratch (outside the repo); verify sha256 of each extracted file
   against the committed blob hashes.
2. Independently verify the claimed single change: diff each extracted
   file against its v2 base at b0d1749f2
   (conditional_tax_build/r3t.zag, r1t.zag, frct.zag); confirm the only
   functional change is the minsl1 = min(4, en/8) computation.
   Re-run the F-CASE string audit (audit 1): grep added/modified lines
   for Y4, Y5, y4, y5, 710202, fam8, F-PARCOND, 710101-710299.
3. Build with the pinned znc
   (/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc,
   version 2026.07.0-dev): znc <file>.zag -o <file>_bin.
4. Run each battery 3 times, stdout to .txt, stderr to .err, exactly per
   the frozen execution protocol (nine runs total).
5. Compare: md5sum per battery against the committed values in section
   1; verdict-line extraction via grep; bar-by-bar table P1''-P4'',
   K1-K3, F-CASE.

## 3. Verification criteria

THRESHOLD-REPRO-PASS iff ALL hold:

- R1: rebuild from committed source only (no /tmp debug build, no prior
  worker binaries; source commits documented in the report).
- R2: every committed number in section 1 reproduces exactly (md5 match
  per battery 3/3, all verdict lines identical, .err files empty).
- R3: pure Zag at every stage (zero Python), no em dashes.
- R4: the /tmp debug build is not used at any stage (no file from /tmp
  enters the build or run).

## 4. Discrepancy protocol

Any mismatch is reported honestly with its exact magnitude; source is
NOT adjusted to match. A mismatch on any bar yields
THRESHOLD-REPRO-FAIL with the failing bar named. Partial matches are
reported as diagnostics, never as a pass.

## 5. Honest scope

Bounded-L2 independent reproduction only. No L3 claim, no Criterion 0
claim, no pipeline promotion, no SURVIVES claim. The verdict is
THRESHOLD-REPRO-[PASS/FAIL].

THRESHOLD-REPRO-PREREG-FROZEN.
