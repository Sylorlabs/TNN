# REPORT: LIFETIME-METALEARN-3 -- Cross-family lifetime learning

## Frozen verdict: RETENTION WITHOUT META-LEARNING

Per the frozen verdict mapping, B5a (retention) and B5b (interference
control) PASS, but B5d (meta-learning) FAILS. The preregistered headline
verdict is therefore RETENTION WITHOUT META-LEARNING. This report gives
the full picture: retention, interference control, and positive transfer
all demonstrated decisively; meta-learning as defined (error reduction
from first to last 36-pair family) did not occur. Nothing in the frozen
bars was weakened or reinterpreted.

## What was built (pure Zag, safebin-only)

- `lm3.zag` (14760 bytes): 17 episodes across 5 opaque task families,
  one continuing associative learner, three conditions (T=continuing
  with partitions, R=reset per episode, S=shared-store ablation).
  Partition selection by slot-evidence only (no labels, no fingerprint);
  split-on-contradiction backstop; global answer base-rate prior;
  first-encounter slot storage.
- Commit order honored: prereg b3b3ee00a (PREREG.md + NAMECHECK.md)
  strictly before any implementation file. This commit adds the
  implementation + report only.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/ruby/
  node all unresolvable; zero forbidden invocations. One znc analyzer
  warning (A0102, ignored return value; intentional).
- Determinism: 3/3 runs byte-identical,
  sha256 `46838f88f9f245e68b9d0de6690f1d5d0dea1dcb0c3fd0a0896c17fb4e728e52`.

## Results (frozen binary output, 3/3 identical)

```
E01 T=34 R=34 S=34    (m1, criterion)
E02 T=18 R=18 S=17    (c1, criterion)
E03 T=17 R=18 S=16    (parity, fixed 160)
E04 T=39 R=36 S=39    (m2 CONFLICT, criterion)
E05 T=100 R=61 S=0    (PROBE m1)
E06 T=16 R=16 S=16    (compare, fixed 160)
E07 T=22 R=22 S=22    (c2 CONFLICT, criterion)
E08 T=100 R=10 S=0    (PROBE c1)
E09 T=40 R=48 S=48    (m3, criterion)
E10 T=16 R=46 S=33    (parity REPEAT, criterion)
E11 T=14 R=64 S=22    (compare REPEAT, criterion)
E12 T=24 R=22 S=25    (sum3 NOVEL, fixed 160)
E13 T=100 R=33 S=16   (PROBE m1)
E14 T=100 R=50 S=0    (PROBE c1)
E15 T=100 R=40 S=36   (PROBE parity)
E16 T=100 R=60 S=36   (PROBE compare)
E17 T=36 R=36 S=36    (m4, criterion)
B5A=1 B5B=1 B5C=1 B5D=0 B5E=1 B5F=1 B4=1
splits: T=1 R=0 S=0; evict=0; caphit=0; genfail=0 (all conditions)
```

Bar scorecard:
- B1 COMMIT-ORDER: PASS (prereg b3b3ee00a implementation-free).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (DIFF=15,12,11,14,13,14 all >=10; DC=4>=3; DS=1).
- B5a RETENTION (primary): PASS. T probe accuracy 100% on E05, E08,
  and mean 100% on E13-E16 (all >=85).
- B5b INTERFERENCE-CONTROL (primary): PASS. T-S = 100 on E05
  (100-0) and 100 on E08 (100-0), both >=40. The S ablation
  catastrophically forgot both conflicted families (0% accuracy);
  T retained perfectly.
- B5c POSITIVE-TRANSFER: PASS. etc_T(E10)=16<=25 and etc_T(E11)=14<=25.
  (Naive R: 46 and 64. Partition reuse collapses etc by ~3-4x.)
- B5d META-LEARNING: FAIL. err_T(E03)-err_T(E12) = 17-24 = -7 < 8.
- B5e META-MONOTONE: PASS. err_T(E06)=16 <= err_T(E03)=17.
- B5f APPARATUS: PASS (caphit=0, evict=0, genfail=0 all conditions).
- B6 NO-RESEARCHER-META-RULE: PASS (learner fns take no episode/family
  index; partitions keyed only by observed (query,answer) pairs).
- B7 OPAQUE-IDS: PASS (frozen word list grep empty).

## Reading of the result

**Retention works.** After learning conflicting mappings (m2 overwrites
m1's queries, c2 overwrites c1's), the continuing learner (T) scores
100% on retention probes, while the shared-store ablation (S) scores
0% (complete catastrophic forgetting). The partition mechanism --
selecting knowledge by observed predictive accuracy, with zero labels --
protects old knowledge from interference.

**Positive transfer works.** On repeated structure (parity, compare),
etc collapses from ~50 (naive) to ~15 (reuse). The learner recognizes
applicable past knowledge via slot-evidence and reuses it.

**Meta-learning (as defined) did not occur.** Errors on the last
36-pair family (E12 sum3, 24) exceeded errors on the first (E03 parity,
17). Diagnosis: E12 is ternary (answers 0/1/2) while the prior was
calibrated on binary/skewed families; the binary-biased prior hurts
on ternary. This is negative transfer, not a failure of learning per
se. The monotone bar (B5e) passed (E06<=E03), showing the prior does
not degrade on matched task types.

**PRNG bug fix (disclosed).** The v1 pilot used low-bit LCG output,
which has period <=16 mod 16, causing identical query streams (B4
DS=0). Fixed to high bits ((s>>16)%n) before implementation commit.
This changed calibration values from PREREG sec 5 (low-bit pilot had
E03=19, E12=6, predicting B5d PASS; high-bit gives E03=17, E12=24,
B5d FAIL). The bars themselves were not changed. The failure is honest:
the meta-learning hypothesis, as operationalized, did not survive the
bug fix.

## Honest boundaries

- Substrate is associative (L1-ish); claims are about lifetime dynamics,
  not representational invention (not L3).
- One frozen seed; generalization to other orders/seeds untested.
- The split backstop fired once (T splits=1); clean separation via
  slot-evidence handled the rest.
- Probes use no state updates (pure retention read).
- B5d's failure is specific to the ternary/binary mismatch; a
  differently operationalized meta-learning test (e.g., within binary
  families only) might pass. Follow-up work.

## Artifacts in this commit

- `lm3.zag`: frozen implementation (B6/B7 audited).
- `lm3_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `46838f88...e52`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
