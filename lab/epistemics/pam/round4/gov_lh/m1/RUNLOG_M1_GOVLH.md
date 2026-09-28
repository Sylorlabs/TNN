# RUNLOG — M1 Gov-LH Crew 4 (held-out wrongs at long horizon)

**Date:** 2026-09-24. **Prereg:** `PREREG_M1_GOVLH.md` (frozen).

## Sequence

1. **Prereg frozen & committed alone.** `PREREG_M1_GOVLH.md` written to
   `~/workspace/pam_gov_lh/crew4_m1/`, copied to
   `~/workspace/tnn-lab/pam/round4/gov_lh/m1/PREREG_M1_GOVLH.md`, committed
   ALONE to branch `tnn-native-lab` via `commit_racefree.py`
   (TMPDIR=`~/workspace/tmp_commit`):
   **commit `1f6d190c0538c42c5b93ba37ecd70ef58be51e4d`**
   (parent `f13383e81328`). No fixture, build, or output existed at commit
   time.
2. **Fixture generated.** `gen_m1_govlh.py` read the frozen Round-3 fixture
   `m1_cases.txt` (sha verified `5d4160d1…c611` before parsing) and wrote
   `m1_govlh_cases.txt`: 3,125 rows
   (C=1102, W=12, P=18, B=1109, N1=1, N2=311, N3=144, N4=12 pairs,
   N5real=400, N5synth=4),
   sha `420af6e5d86cc04bf912242451682192e9721ac271698adb0f1d87a7c707229f`.
   Partition check passed in-generator: N1+N2+N5real = 712 = B rows passing
   OPT. N4 dropped one leftover point `(1000, 10410)` (odd count 25 → 24,
   12 pairs), per the frozen consecutive-pairing rule.
3. **Instrument built.** `m1_govlh.zag` + `R33_NATIVE_IO_V1.zag` (sha
   `e6379ddb…f61d8`, matches the Round-3 pin) compiled with the pinned
   toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
   → `build/m1_govlh` (73,808 bytes). znc analyzer warnings only
   (unused `* 1`); build rc=0. `[]u8` arenas with LE accessors throughout;
   no slice > 2^25 bytes (largest arena 4096×8 = 32 KiB).
4. **Three runs.** `./build/m1_govlh m1_govlh_cases.txt` × 3 →
   `evidence/run1/2/3.txt`, sha256
   `187e5bf9e1ed2f5ff097e30c98e511d9ad9527939b0fd22b0068291b688fb696`
   **×3 byte-identical.** S=1 anchors reproduced Round 3 exactly
   (tp_opt=910, tp_safe=671, W=0, P_inst=0, B_opt=712, B_base=7).
5. **Independent mirror.** `score_m1_govlh.py` recomputed all 82 reported
   keys from the fixture + frozen bars + frozen jitter: **82/82 match**,
   anchors OK, partition OK. (One scorer-side bug found and fixed before
   any comparison: `passes(c,m,s,a,*OPT)` unpacked the bar tuple into 8
   args; corrected to `passes(c,m,s,a,OPT)`. Instrument and fixture
   untouched — the fix is recorded in `evidence/DIGESTS.txt` via the
   scorer's sha.)
6. **Verdict written** (`VERDICT_M1_GOVLH.md`) from the mirrored numbers.

## Notes

- The single N1 row (the real 1145-class wrong in the frozen sweep) is
  B-row `conf/mrgF` high with strong=agree=1; it passes OPT and SAFE at
  every scale — the irreducible residual.
- Pair V5 (`(718,6600)+(704,6603)`) is the jitter-flip source for P installs:
  its weaker member sits at conf=704, one unit under CT=705.
- No binaries, `.zagd`, or `.zag-cache` are committed (build/ is local only).
