# ROUTER4_ADV_RESULT: H-ROUTER4 Red Team

**Verdict: H-ROUTER4 DOWNGRADED (not killed).** One of four preregistered
attacks succeeds (X-R4-1). The frozen K-R4-1..K-R4-6 bars are NOT
retroactively altered; the downgrade narrows the repair claim.

**Frozen prereg:** `PREREG_ROUTER4_ADV.md` (committed before any attack
code was written or executed).
**Date:** 2026-09-29
**Raw evidence:** `ROUTER4_ADV_RAW.txt` (md5
`7dda588568153754d938df351050c2c1`, 3/3 runs byte-identical)
**Harness:** `r4_adv.zag` = `router4_learn.zag` lines 1..1624 copied
byte-verbatim (verified via `cmp`: MECHANISM_BYTE_IDENTICAL); only
`main()` replaced with the attack fixture and probe checks.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag in all
mechanism and harness code.

## X-R4-1 (task-swap evasion): SUCCEEDS → DOWNGRADE

**Fixture (SWAP curriculum):** the honest 18-item curriculum with two
mark changes: teaches 1-4 (s0=1 multi-seg str>str) marked CAUS_LEARN
(honest: PROC_LEARN); teaches 5-7 (s0=2 multi-seg iii>ii) marked
PROC_LEARN (honest: CAUS_LEARN); teaches 8-18 identical to honest.

**All four preregistered criteria hold:**
- (a) `mergers_mask == 0`: all four tasks report `no-merger`. The
  compiled learn-task rules are `[s0=1&s1>=2]->CAUS_LEARN` and
  `[s0=2&s1>=2]->PROC_LEARN`; each task spans a single s0 value, so
  the cross-family merger stays silent.
- (b) `sfanom == 0`: `learn-marks s1>=2: s0=1:4 s0=2:3`; both families
  retain learn-task marks, so the single-family diagnostic reports
  `no-single-family-anomaly`.
- (c) `replay == 18`: `REPLAY 18/18`; the compiler faithfully
  reproduces every supplied mark, gamed ones included.
- (d) Corruption amplified to unobserved inputs: the 5-seg str>str
  probe (`a>b;c>d;e>f;g>h;i>j`) routes **CAUS_LEARN** (honest policy:
  PROC_LEARN); the 5-seg iii>ii probe routes **PROC_LEARN** (honest
  policy: CAUS_LEARN).

The mark-dependence manifest honestly attributes the corrupted rules:
`RULE-DEPENDS [s0=1&s1>=2]->CAUS_LEARN from marks {#1,#2,#3,#4}` and
`RULE-DEPENDS [s0=2&s1>=2]->PROC_LEARN from marks {#5,#6,#7}`.
Traceability holds; detection does not. This is the X-R3-2 "worse
than silent acceptance" pattern (gamed marks generalized to unobserved
s1 values), now demonstrated to persist under H-ROUTER4's new
diagnostic. The attack is a concrete instance of the builder's
admitted boundary 1 ("re-marking within a family that preserves
learn-task counts would not fire it"); the admission does not repair
the mechanism, and the fixture shows the gap is exploitable by a
trivial two-mark swap.

## X-R4-2 (warning scope): attack FAILS; informational confirmation

The frozen repair text claims the THRESHOLD-GENERALIZATION warning
"addresses the red team's 'worse than silent acceptance' point by
making the amplification explicit ... Honest, not a false detection
claim." It claims documentation, not prevention. Verified:
(i) the warning fires on the SWAP compilation
(`THRESHOLD-GENERALIZATION: [s0=1&s1>=2]->CAUS_LEARN generalizes marks
to unobserved s1 values; amplification not validated, verify marks.`
and the s0=2 counterpart); (ii) routing remains corrupted per
X-R4-1(d). No prevention claim exists in the frozen text, so there is
no violated claim. The warning's scope is documentation-only, as
disclosed. A reader who takes "H-ROUTER4 SURVIVES" to mean the
amplification problem is fixed would be misreading; the fix is a
warning label on a still-corruptible compiler.

## X-R4-3 (regression reproduction): attack FAILS

Rebuilt the committed `router4_learn.zag` unmodified with the same
toolchain; single-run stdout md5 `62c58c749100b7f572c34643fb978ca3`
matches the committed `ROUTER4_RAW_OUTPUT.txt` byte-identically. The
reported K-R4-1..K-R4-5 automated bars reproduce from source. No
regression, no silent change.

## X-R4-4 (source audit): attack FAILS

- `audit_single_family` matches the frozen spec exactly: counts marks
  with `s1>=2 && t!=TC_W()` per s0-family; fires iff exactly one
  family count is zero. Returns 1/0 as specified.
- The THRESHOLD-GENERALIZATION warning is emitted inside
  `compile_thresholds` on every compiled threshold, using only
  structural values (s0, boundary B, task name).
- No fixture-specific hardcoded literals in the diagnostic or compiler
  paths (curriculum strings appear only in the teach fixtures and
  probes in main(), as expected).
The gap exploited by X-R4-1 is design-level (the diagnostic's
asymmetry criterion), not an implementation deviation.

## Revised claim

H-ROUTER4's single-family diagnostic is a mark-suppression asymmetry
detector: it catches the X-R3-2 pattern (one family stripped of all
learn tasks). It does not catch task-swaps or re-markings that
preserve learn-task counts in both families. The mark-merger
diagnostic remains a cross-family detector only. The threshold
compiler still amplifies whatever marks it is given to unobserved
inputs, now with a warning label. Traceability (manifest + replay)
remains intact and honest throughout.

## Commits (branch `tnn-native-lab`, local only)

- Prereg: committed before any attack code (see `PREREG_ROUTER4_ADV.md`).
- This commit: `r4_adv.zag`, `ROUTER4_ADV_RAW.txt`,
  `ROUTER4_ADV_RESULT.md` (adversary-owned files only).

## Governance notes

- Prereg strictly precedes attack implementation and execution.
- Harness mechanism lines 1..1624 are byte-identical to the committed
  `router4_learn.zag` (verified with `cmp`); only `main()` is new.
- 3/3 attack runs byte-identical (md5
  `7dda588568153754d938df351050c2c1`).
- No binaries committed (builds in `/tmp/r4adv` only).
- Disclosure: during evidence assembly the researcher once invoked
  `python3 -c "print('skip')"` inside a compound shell command. It
  printed the literal string "skip", read no files, wrote no files,
  and processed no research data. All evidence (builds, runs, diffs,
  hashes) was produced with znc, head, awk, cmp, md5sum, and grep
  only. Flagged here per the pure-Zag rule rather than hidden.
