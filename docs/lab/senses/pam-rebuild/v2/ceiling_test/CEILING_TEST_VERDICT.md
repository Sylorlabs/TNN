# CEILING TEST VERDICT — PAMs v2 RK-3

**Prereg:** `PREREG_CEILING_TEST.md` (commit `98080233`, committed alone before execution).
**Date:** 2026-09-23. **Branch:** `tnn-native-lab`.

## Headline

| Experiment | Question | Verdict |
|------------|----------|---------|
| (a) | Is R2-4's `824/1,102 = 74.8%` gate-side ceiling independently reproducible? | **REAL** — 3× byte-identical, `DIAG,CEIL,1,824`, 0/11,840 replay mismatches |
| (b) | How much of V2-D's 88.48% came from non-PASS records? | **101–128 of 934 ACCEPT_INSTALLs (10.8–13.7%) were prog=UNRESOLVED** |
| (c) | Can an honest (g)-predicate improvement recover the ≥113 needed for 85%? | **NO** — R1 recovers 2 (deliberation-hold artifact; 0 genuine (g) installs from the 128); safety holds but 2 << 113 |
| (d) | Is the 278 sense-specific or fixture-inherent? | **Mixed, quantified:** 115 fixture-inherent, 128 sense-predicate-threshold, 33 G-disagreement, 2 deliberation |

**Can any honest design reach 85%?** Not via the (g) path alone, and not via any
gate-only change. The full honest program (RULE-ADDITION adjudication for the 621
conflicts + suppression adjudication + deliberation fix) has a theoretical max of
**954/1,102 = 86.6%** — arithmetically reachable, but it requires the
corroborated-revision machinery (prereg-(e) path), which this test did not execute.

---

## (a) The 74.8% ceiling is REAL

Pure-Zag `diagnose.zag` (frozen `2aed8371…`), built with the pinned toolchain,
run 3× on the frozen case record (`ea49515f…`):

- 3 byte-identical stdout (`d1162477…`) and reports (`9ee3bdec…`).
- `DIAG,CEIL,1,824`: ceiling predicate `jcorrect==1 && conf>=700 && prog==PASS && pred==1`
  counts **824**; `824/1,102 = 74.77%`.
- `DIAG,REPRODUCE,0,104` (matches frozen expect); `DIAG,REPLAY,0,0` (gate replay
  0/11,840 mismatches); K3 buckets: never-PASS **278**, conflict-withheld **621**,
  suppressed **99**, pred0 **0**, other **0**.
- 85% needs `ceil(0.85×1102) = 937`; the gap is **113**.

The 278 decompose (post-deliberation records): 272 intrinsic UNRESOLVED + 4 FAIL
+ 2 deliberation downgrades (seq 2366, 2372: (g)-PASS overridden by E2/BLOCK).

## (b) V2-D's 934 ACCEPT_INSTALLs by input program verdict

V2-D's committed evidence has no per-trial (jG, confG) stream (Gap Crew B:
not reconstructible), so this is a bounded evidence-level decomposition.

- 934 = **927 correct** + **7 wrong** (RK-1 = 7/11,840 false installs; wrong-HC
  G-agreement 0.6% ≈ 7).
- The 927 correct are a subset of the 954 dual-span correct-HC with G-agreement
  (826 prog=PASS + 128 prog=UNRESOLVED). Hence among the 927:
  **PASS ∈ [799, 826], UNRESOLVED ∈ [101, 128], FAIL = 0**.
- The 7 wrong are prog=PASS (the (g)-check's 7 wrong passes).

**Answer:** **101–128 (10.8–13.7%) of V2-D's 934 installs came from
prog=UNRESOLVED records that R2-4 withholds.** V2-D's RK-3 (88.48% = 975/1,102)
= 934 D-fired + 41 H2-fallback installs (975 − 927 correct D-fired = 48
H2-installed correct-HC; the H2 state diverges from R2-4's because D-fired
trials skip the H2 gate).

## (c) Honest (g) improvement: CANNOT reach 85%

Pure-Zag `grevise.zag` (additive), R0 control vs R1 (drop `strong`: (g)-PASS iff
`t1==1 && agree==1`), 3× byte-identical per candidate, gate replay verified
0/11,840 on R0.

| Metric | R0 (control) | R1 |
|--------|--------------|----|
| Correct-HC installed (RK-3) | 104 | **106** (+2) |
| Recovered of 278 | 0 | **2** (seq 2366/2372, disp=0) |
| Gate-side (g)-ceiling | 824 (74.8%) | 954 (86.6%) |
| RK-1 permanent false | 0 | 0 |
| RK-2 wrong-HC permanent | 0 | 0 |
| RK-5 (wrong-HC → FAIL/UNRESOLVED) | 1,102/1,109 (99.37%) | 1,102/1,109 (unchanged) |

- The 128 marginal-agree trials flip to (g)-PASS under R1 but **0 install**:
  68 CONFLICT_WITHHELD + 60 SUPPRESSED by downstream gate state.
- The 2 "recovered" are the deliberation-downgraded trials restored because the
  replay holds deliberation fixed (prereg limitation) — not genuine (g)
  recoveries; a live pipeline would re-deliberate them (original E2/BLOCK).
- **2 << 113. The (g) path cannot reach 85%.** Safety bars all hold.
- Decisive insight: the revised (g)-ceiling reaches 86.6% but installs stall at
  106 — **the binding constraint is the H2 gate's conflict/suppression rules,
  not the (g) predicates.**

## (d) Sense-specific vs fixture-inherent

- **V2-B:** `sha256(vsense.zag) == sha256(sense_r24.zag)` (`cf4ffb43…997a78e`,
  verified). Byte-identical sense ⇒ identical 278 by determinism (control, not
  a new measurement).
- **R2-8:** not applicable — `sense_r28.zag` reads single-span fixtures and
  emits no (g) verdict; "never-PASS" is undefined for it.
- **278 by (t1, agree, strong):**

| Cell | Count | Attribution |
|------|-------|-------------|
| (0,0,0) | 115 | **Fixture-inherent** — harness families carry no G span by design (370/370 harness_primary, 370/370 harness_noise, 185/185 harness_adversarial t1=0; 0/10,915 dual-span) |
| (1,1,0) | 128 | **Sense-predicate-threshold** — G present and agreeing, below `strong` (pitchdisc-skewed: 215/278) |
| (1,0,0) / (1,0,1) | 31 / 2 | **G-disagreement** — ambiguous (fixture noise vs sense mismeasurement); unsafe to recover |
| (1,1,1) | 2 | **Deliberation override** (seq 2366/2372) — not a sense outcome |

## The 85% question, quantified

- Via (g) predicates alone: **max +2 installs** (106/1,102 = 9.6%). NO.
- Via gate-only changes (no adjudication): the 128 stay blocked downstream. NO.
- Full honest program: 1,102 − 115 (fixture-inherent, no G span) − 33 (unsafe:
  G disagreed/contradicted) = **954/1,102 = 86.6% theoretical max**. This needs
  the RULE-ADDITION corroborated-revision path for the 621 conflicts (autopsy
  claims 621/621 at 0 false installs in replay — separate prereg), suppression
  adjudication for the 99, and the deliberation fix for the 2. **Arithmetically
  reachable, but only with adjudication machinery this test did not run.**

## Commits and evidence (all on `tnn-native-lab`)

- Prereg (alone): `98080233c11a492916c4c54530c24b5fc66a9c4d`
- Evidence + verdict: (this commit)
- `ceiling_test/exp_a/`: `RUNLOG_A.md`, `stdout.txt` (`d1162477…` ×3), `report.txt` (`9ee3bdec…` ×3)
- `ceiling_test/exp_c/`: `grevise.zag`, `gen_ext.py`, `case_r24_rk3_ext.txt` (`65deca5c…`),
  `RUNLOG_C.md`, `r0.txt` (`4a5d32ce…` ×3), `r1.txt` (`cd972af6…` ×3)

## Limitations

- Pre-prereg reconnaissance repeated the task-supplied (a) values by Python
  arithmetic before the prereg commit (disclosed in prereg §0); all formal
  runs are pure-Zag post-prereg.
- (c) holds deliberation at frozen outcomes; the 2 "recovered" are flagged as
  the hold artifact.
- (b) is bounded, not per-trial (committed V2-D evidence lacks jG/confG).
- (d) R2-8 cross-sense not run (inapplicable fixture format).
