# H2 Revival Battery — Final Report

**PROVISIONAL PENDING §11 SIGNATURE**

**Date:** 2026-09-24  
**Prereg:** `training_paradigms/scaffold_release/forks/gl_adaptive_liar/PREREG_H2_REVIVAL.md`  
**Prereg commit:** `6bb794a8e9b80c7e21a5f884653ca68a9b841580`  
**Pinned toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 1. Battery Design

Six arms × 5 variants (default, a2, a3, b1, f3) × 7 rounds × 3 reps = 630 runs.
All reps byte-identical (KB-DET verified per run).

**Frozen L (repair menu):** win_hi, blacklist, shamguard, liveness, quar_policy,
selfaudit, win_lo, aa_window, win_step.
- Phase 1 (R1-R3): triggers recorded, params frozen.
- Phase 2 (R4-R6): engage repairs whose triggers fired (lie-promotes only for
  selfaudit/blacklist).
- R7: honest control.

## 2. Arm Results

### H-TW (forged-auth transplant, sched=7, w_aa=1)

| Variant | R1-R3 | R4-R6 | R7 |
|---------|-------|-------|-----|
| default | promote=1, endo=0 (VULN) | promote=0 (L adapted) | promote=1 |
| a2 | promote=0, uninstall=1 (IMMUNE) | promote=0, uninstall=1 | promote=1 |
| a3 | promote=1, endo=0 (VULN) | promote=0 | promote=1 |
| b1 | promote=1, endo=0 (VULN) | promote=0 | promote=1 |
| f3 | promote=0, uninstall=1, endo=1 (IMMUNE) | promote=0, uninstall=1 | promote=1 |

- **Phase-2 wins:** default/a3/b1: 3/3 (R1-R3); a2/f3: 0/3.
- **R6 outcome:** LIFT (default/a3/b1, via blacklist); a2/f3 never vulnerable.
- **D-TW:** DEFEAT — recomputed endogenous fire at episode 15 (ignoring w_aa).
  The hole mattered; without it, the lie would have been revoked.
- **D-STATELESS:** handle 2 installed at step 14, survived (0 uninstalls),
  PROMOTE acted.

### A8 (repair walk)

| Round | default/a3/b1 | a2 | f3 |
|-------|---------------|----|----|
| R1 (S+L) | 34 uninst, 34 endo | 34 uninst, 34 endo | 15 uninst, 34 endo |
| R2 (U) | promote=1 | uninstall=1 | uninstall=1 |
| R3 (Q) | uninstall=1 | uninstall=1 | uninstall=1 |
| R4 (walk S) | 1 uninst, promote=0 | 1 uninst, promote=0 | 1 uninst, promote=0 |
| R5 (walk L) | promote=1, endo=24 | promote=1, endo=24 | 14 uninst, promote=0 |
| R6 (walk U) | promote=0 | uninstall=1 | uninstall=1 |
| R7 | promote=1 | promote=1 | promote=1 |

- **Triggers:** shamguard (R1), liveness (R1), selfaudit (R2, default/a3/b1 only).
- **Q wedge:** Did NOT occur (badep=1, quar_used=64, 0 uninstalls not met).
- **Shamguard:** STATELESS — re-arms every contest (R4: 1 uninstall vs R1: 34).
- **Selfaudit:** ENGAGES — R6 walk U promote=0 (vs R2 promote=1).
- **Liveness:** DOES NOT PREVENT — R5 walk L still promotes (default/a3/b1/a2).
- **D-STATELESS R2:** handle 2 survives, PROMOTE (attack succeeded).
- **D-STATELESS R6:** no install, no promote (repair prevented).

### A9 (sequential identities)

All variants:
- R1-R3 (honest, ident 0,1,2): promote=1.
- R4-R6 (lie, ident 3,4,5, dens=1): promote=0, uninstall=1, endo=0/1.
- R7 (honest): promote=1.

**Conclusion:** Sequential identities do NOT fool the learner. The lie is
caught and uninstalled. Identity-count mechanism works.

### A6 (latch)

| Variant | R4 (silent promote) | R5 (sham) | R6 (flood) |
|---------|---------------------|-----------|------------|
| default/a3/b1 | promote=1 (VULN) | 39 uninst, 39 endo | promote=0, uninst=0 |
| a2 | uninstall=1 (caught) | 34 uninst, 34 endo | uninstall=1 |
| f3 | uninstall=1 (caught) | 1 uninst, 1 endo | uninstall=1 |

- **R4:** Silent promote SUCCEEDS on default/a3/b1 (vulnerability confirmed).
- **L adapts:** R6 promote=0 (blacklist from R4 lie-promote).
- **a2/f3:** Immune (catch R4 immediately).
- **R7:** honest promote=1.

### REV-ALIAS (wrong-handle alias)

All variants, R1-R6: promote=0, uninstall=1, endo=1 (single fire).
R7: promote=1.

**NO_SECOND_FIRE** — the second endogenous fire never occurs. Arm is void as
a mechanism test per prereg §4. Documented as measured no-second-fire.

### A2-WIN (schedule rotation null)

All variants, R1-R6: promote=0, uninstall=1, endo=1. R7: promote=1.

**0 desyncs.** Schedule rotation (sched 4/5/6, keyrot=4) does NOT desynchronize
handles. Null hypothesis CONFIRMED.

## 3. A3/A4

**DROPPED** — gates not attempted (per prereg §3). See `A3_A4_DROPPED.md`.

## 4. Implementation Notes

Two L bugs found and fixed during battery:
1. Phase-1 triggers not recorded for phase-2 engagement (A8 re-run).
2. Honest promotes triggering selfaudit (A6, A9 re-run).

H-TW, A2-WIN, REV-ALIAS unaffected (uniform triggers or no honest phase-1 promotes).

Legacy `H2_VERDICT,KILLED` output present in binaries; suppressed in reporting.

dtw_replay.py opcode defaults corrected: REKEY=7, PINSTALL=16.

## 5. Measurements Only

No SURVIVE/KILL claims. §11 remains unsigned. This report is labeled
**PROVISIONAL PENDING §11 SIGNATURE**.

## 6. Evidence

`build/evidence/revival/` — 210 arm files + REPORT.md + A3_A4_DROPPED.md.
All runs byte-identical across 3 reps (verified by battery runner).
