# NAMECHECK: CYCLES-FEEDBACK-REFIX

Worker: cycles-feedback-refix. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_feedback_refix/`
Task: transparent re-freeze of the C430 (CYCLES-FEEDBACK,
INFORMATIVE-FAIL) battery under a FRESH prereg correcting the QF1
TRIES arithmetic error (44 -> 28), then re-run of the UNCHANGED
frozen binary. Bookkeeping only: no source or binary changes, no
rebuild, no amendment to C430's frozen prereg.

## Step 0: toolchain guard (worker governance)

- Safebin active: `export PATH="$HOME/safebin"` at session start.
- `which python3` returns nothing; `which python` returns nothing
  (verified 2026-10-03 in-lane).
- Pinned znc: /home/hatch/safebin/znc, `znc 2026.07.0-dev`.
- No compilation is performed in this wave (the binary is frozen and
  re-run as-is). Shell only for binary runs, git ops, file copies,
  byte-verification (cmp/sha256sum/grep/sed).
- No forbidden interpreter invocation. Any such invocation would make
  this wave PROCESS-FAIL.

## Step 1: frozen artifact digests (verified before the re-run)

- qf_fbin (frozen binary, copied from the C430 lane, NOT rebuilt):
  c7c459e556f94f53b42be53d57f26d5fb6e024004a6511c6179599b1a48dddf3
- C430 run digest (qf_run1.txt, 3/3 byte-identical in C430):
  538fd190e096063abf1ae6856eacc6465219a7fbc69cd1b2fe1bce2624f51b37
- Frozen sources the binary was assembled from in C430 (unchanged
  since; nothing is rebuilt here):
  - gc_uni.zag (frozen sequence-trial mechanism):
    33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6
  - gc_base.zag (frozen base + STEP class 4):
    0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125
  - uni_nomain.zag (frozen U region, main stripped):
    e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3
- The lane copy of qf_fbin must match the binary digest before any
  execution (F7 audit in rerun.sh).

## Step 2: prereg commit order

- This NAMECHECK.md (Steps 0-2) + PREREG2.md (+ .gitignore ONLY)
  commit strictly precedes all re-run artifacts (the qf_fbin copy,
  rerun.sh, run outputs, REPORT.md).
- F1 audits this via the lane-local git log order.
