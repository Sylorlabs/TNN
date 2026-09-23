# RUNLOG.md — T2-HELLHOLE re-verification (replacement coordinator)

## 2026-09-23 — resume
Replacement coordinator. Adopted frozen REVERIFY_PREREG.md (commit 8747608b).
No reverify/ dir existed on branch — implementation starts here.

## Tier-3 de-dup amendment (flagged per prereg protocol)
Tier-3 H3 (f988e4da, BOUNDARY-MAPPED) implemented the real
WITHHOLD-before-corroboration gate after the prereg froze. Deviation: the
prereg's RESCUE-H1 leg is NOT re-implemented; instead the H3 gate numbers are
independently re-derived via pure rescoring (different method), with
agree/diverge recorded. Distinct angles H2/H3 are the only fresh builds.

## RV1 — hh_verify2.zag (fresh, ledger-grounded)
- Copied committed session.htsv ledgers (solo 409 events, helper 473) from the
  T2 crew's evidence dir into work/hellhole/ as solo.htsv/helper.htsv.
- Wrote hh_verify2.zag: parses EVT/SENSE_DECIDED lines, cand=/disposition=
  fields, last-wins per candidate; frozen bitmask sets; frozen formulas
  (M1*10>=n*8; K1*5>=n trips; K2*10>n*3 trips; M3 counts WITHHOLD=4).
- Built with pinned znc 2026.07.0-dev. 3 runs/arm byte-identical:
  solo 2d50fdb8c55b3f52db3cd844f5bd8a6a1fc5fdbb11bd25b3f723dc26574fb213,
  helper c0f9ee7bde0ba1d18a9787bac000ab2d5022251e48a2ffa7c989c24c8a9b22aa.
- Result: solo M1=5/9 K1=4/9 TRIP M3=0/3 K2=3/3 TRIP M4=3/3 K3=0 K5=0;
  helper M1=7/9 K1=2/9 TRIP M3=0/3 K2=3/3 TRIP M4=3/3 K3=0 K5=0.
  BINDING_FAIL=1 both. FAIL confirmed.

## H3 de-dup — hh_rescore2.zag (pure rescoring)
- Fetched from branch: hellhole-rescue/run_gated_r1.txt (blob 7c0764f6…),
  h3_data.zag (blob e9fbabe1…).
- Gate tags (frozen 0..18): 0,0,0,0,0,1,2,5,6,5,5,6,3,3,4,4,5,5,5.
- Wrote hh_rescore2.zag: reads committed score.json dispositions, applies
  gate (tag in {1,2,3,6} & INSTALL→WITHHOLD), recomputes bars. 3x
  byte-identical: solo 03edc51d…, helper 795b1434….
- Result: solo K1=2/9 TRIP M1=7/9 K2=0/3 M3=3/3; helper K1=1/9 clear M1=8/9
  PASS K2=0/3 M3=3/3. EXACT agreement with Tier-3 H3 mechanism numbers.

## RV2 H2 — spam-pair killer (real mechanism fork)
- Fetched ws2_sense_gated.zag (blob 186786d4…), h3_gate.zag (4a01c3aa…),
  ws2_orig.zag (24725f01…) from branch.
- Fork: h2/ws2_sense_h2.zag = gated + `if(tg==4){return 2;}` (SPAM joins gate);
  h2/h2_gate.zag = h3_gate.zag with import swapped + header note.
- Built with pinned znc. Ungated run reproduces trial (solo 4/9,5/9,3/3) —
  fork faithful. Gated 3x byte-identical: SHA
  115485a287e1d3f06289f736ffbdf6b629fc226a135c303a2da13b77e11657bc.
- Gated frozen: solo K1=0/9 M1=9/9 K2=0/3; helper K1=0/9 M1=9/9 K2=0/3.
  Fresh 12: 12/12 WITHHOLD both arms. K3=0 CORRUPT, K4 not void, K5 clear.
  → RESCUE-SUCCEEDS. Binding FAIL broken by native-logic rescue.

## RV2 H3 — negation repair: DEAD by construction
- C3 (negation bug's clean kill) is a true claim outside all bar sets;
  repairing its REJECT cannot move K1/K2/M1/M3. No build; recorded with
  reasoning in VERIFY.md. C3=REJECT confirmed present in RV1.

## To commit
- reverify/VERIFY.md, reverify/RUNLOG.md, reverify/evidence/{hh_verify2_solo.out,
  hh_verify2_helper.out, hh_rescore2_solo.out, hh_rescore2_helper.out,
  h2_gated_r1.txt, ws2_sense_h2.zag, h2_gate.zag}
