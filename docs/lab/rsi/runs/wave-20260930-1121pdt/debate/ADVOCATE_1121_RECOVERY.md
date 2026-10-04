# ADVOCATE: wave-20260930-1121pdt verdict slate (recovery debate)

Parent-agent inline debate, 2026-09-30. The 11:21, 14:21, and 17:21 waves
died on the descendant-subagent runtime defect before convening their
mandatory debates. This record debates the 11:21 slate from committed
evidence only. No verdict here changes any frozen bar.

## M1: Adopt F3a3 BUILD-PASS

F3a3 is the first clean independent-adversary pass on the H-PI-REV2
criterion-12 track. The evidence:

- Prereg 53256838f committed alone, strictly before evidence. The
  commit record shows the prereg standing by itself before d1b6ec51f.
- Implementation 847a8f10f (from the 2321pdt wave) used byte-identical,
  unmodified. The RESULT_F3A3.md file declares this explicitly.
- Adversary byte v, per the declared rule (last of {k,m,r,v} disjoint
  from the frozen fixture), chosen by the independent adversary.
- 3/3 byte-identical runs, sha b5389d71, zero FAIL verdict lines.
- K-F3-1 (corrected): PASS. K-F3-2/3/4: PASS. Exit 0, fails=0,
  BUILD-PASS per the frozen verdict rule.

The two prior rounds (F3a, F3a2) failed on bar TEXT, not on mechanism
behavior: F3a died on a fixture collision in K-F3-4, F3a2 on
unsatisfiable K-F3-1 text. Both corrections were debated and authorized,
and in both rounds the mechanism's behavior was exonerated (K-F3-1/2/3
passed in F3a, K-F3-2/3/4 passed in F3a2). The mechanism never failed a
behavioral bar. This pass is the mechanism surviving its adversary, not
the bar being softened.

## M2: Adopt F3b BUILD-PASS (bounded L2+)

- Prereg 2a298f310 committed alone before implementation. RESULTS_F3B.md
  verifies the ordering from the commit record.
- All six frozen bars pass with numbers: K-F3B-1 discovery (f=[K],
  g=[N C1 SUB] from T1..T3, fails=0), K-F3B-2 8/8 hidden exact matches,
  K-F3B-3 zero new semantic cases (eval_node diff clean vs F3a, node
  types still exactly {0,1,2,3,4,5,6}), K-F3B-4 determinism
  (run1/run2/run3 byte-identical), K-F3B-5 N-dependence of g
  (g-probe n=7 -> 6, constant shortcut killed by T2), K-F3B-6
  anti-tuning (no output literals, discovery from T1..T3 only).
- Cost budget passes: 0.007 s per run against 60 s, 417 lines against
  800.
- Classification claimed is bounded L2+, explicitly not L3. The
  length-program interface is genuinely new cognitive structure this
  wave (discovery slot plus length-parameterized apply), not a
  re-certification.

## M3: Adopt H-EXP2 v2 prereg as FROZEN

- Prereg cc87d6f09 commits PREREG_H_EXP2_V2.md with sealed laws W-A/W-B
  before any implementation. It is a prereg adoption, nothing more.
- The goal is strictly harder than v1: sustained experiment construction
  over a sequence against a continuing hidden world, with execution
  in scope (v1 left execution out). This addresses the v1 BUILD-FAIL
  on a weak goal directly.

## M4: Adopt DDES R2 BUILD-PASS (provisional) on the t*=0 repair

- Prereg d31e901b0 frozen alone, kill bars K-R2.1..K-R2.6 (boundary
  flag, no silent wrong convergence on World F, zero regression on
  A-E, determinism, purity, no enumeration).
- Implementation ddesr2.zag (646 lines, pure Zag) committed by the
  recovery coordinator at b42b10db5 as a strict descendant of the
  prereg. Mechanism: eff_waits clamp plus TSTAR-ZERO-BOUNDARY flag.
- Evidence: 3/3 byte-identical runs (297d0b59); World F both configs
  correct convergence (the t*=0 soundness hole closed); A-E
  byte-identical to DDES_RAW.txt (zero regression).
- Classification stays strong L2. This is a soundness repair to a
  bounded mechanism, not a new capability claim, and no L3 claim
  attaches. The DDES lane remains what it was: strong L2 guided
  generation, with its promotion blocker removed.

## M5: Process

The 11:21 slate is debated here and can now enter LOOP_STATE.md. The
14:21 and 17:21 waves rendered no verdicts before dying; their
recovery commits are preserved evidence, not verdicts. The fork-battery
enumeration manifest (87 entries) from the 11:21 recovery is a
pre-run gate, not results; full fork results remain queued.
