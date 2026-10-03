# RUNLOG — onebrain v4 problem-set build (Experiment 2)

Workdir: ~/workspace/onebrain/v4/. All commands run from this dir unless noted.
Modes run: `single` ONLY (calibration-permitted). `onebrain` / `ablate` /
`poison` were NEVER run during construction (H1-tuning prohibition).

## 1. Setup + source verification (2026-09-26 ~23:30 PDT)
- `mkdir -p ~/workspace/onebrain/v4`
- Read ~/workspace/onebrain/impl/SELFTEST.md (machinery spec, modes, K1-K6).
- Read ~/workspace/onebrain/impl/PREREG_FROZEN.md (frozen prereg @ 1ab40adceff78d71460b992b078508acea7e8abc; K1-K6 binding).
- Verified against onebrain.zag source (1358 lines):
  - `rd_trig` (lines 194-244): trigger words per reading match the brief exactly
    (rd0: no/actually/meant/correction; rd1: continue/resume; rd2:
    prove/challenge/doubt/really; rd3: source/cite/origin/according;
    rd4: joke/funny/laugh/hilarious/knock; rd5: remember/recall/memory/remind;
    rd6: forget/delete/erase/remove; rd8: compare/versus/vs/combine/difference/between).
  - `gen_readings` (402+): rd7 assertion ev=1 iff no '?' anywhere; rd9 plain ev=1
    iff no reading 0-8 except 7 fired. NO mismatches.
  - `act_base` (702+): 13=240, 14=237, 15=234, 16=231, 17=228, 18=225,
    19=222, 20=219, 21=216, 22=213, 23=210, 24=207. `act_gate_rd` (717+):
    13<-4, 14<-5, 15<-6, 16<-0, 17<-1, 18<-8, 19<-2, 20<-3, 21<-(7 AND 9),
    24<-9; 22 fires iff >=2 surviving ev=1 readings; 23 fires iff no gated fact.
  - `fork_assess` (866+): FORK iff nread>=2 AND top-two fired-bid margin<=12;
    skipped entirely in single mode. NO mismatches.
  - Bonus = corr_of(gating reading) capped at 3, added to base (732-800).
  - `argmax_phase`: ties break to the lower hid.
  - Query buffer lowercased via to_low at load (lines 1268, 1329) ->
    case-insensitive trigger matching. Token-level exact match (beq2).
  - `elim_phase`: kills unfired bids (PRE_FAIL) and fired bids with empty
    answers (GATE) — every bid stages a fallback answer, so no fired bid dies here.
- RESULT: all brief semantics VERIFIED, zero mismatches. No FAIL LOUD needed.

## 2. Drafted v4.tsv (28 single-turn problems, p01..p28)
- Hand-authored with trigger-level reading analysis per problem; expected bids
  spread across all 12 action bids (13..24); entities restricted to the 12-fact KB.
- Design: 14 problems where single-mode's argmax (lowest-hid fired bid) is
  judged correct, 14 where careful human judgment picks a different bid
  (revoke compounds, untaught predicates per G6, correction-vs-compose,
  either-or/idiom clarify cases).

## 3. Freeze v4.1 (BEFORE any scoring run)
- `sha256sum v4.tsv` -> e74bfa51d3a4697eb885c0b45f63a13e4b4f0b2023bc5cb8623451460f18dde6
- `date -u` -> 2026-09-27 06:26:07 UTC
- Recorded in FREEZE.txt (v4.1 entry). 29 lines (header + 28 problems).

## 4. Calibration run — single mode (frozen v4.1)
- Command: `../impl/onebrain single v4.tsv > run_single_v41.txt 2>&1`
- exit=0, 28 VERDICT lines, fork=0 on all (expected: single never forks).
- Winners: p01=13 p02=13 p03=13 p04=13 p05=13 p06=14 p07=14 p08=13 p09=16
  p10=16 p11=16 p12=16 p13=17 p14=13 p15=18 p16=19 p17=19 p18=19 p19=20
  p20=24 p21=24 p22=24 p23=24 p24=24 p25=24 p26=21 p27=21 p28=18
  (scores: 242,240,241,240,242,238,238,240,232,232,232,233,229,241,227,
   224,224,224,219,209,209,209,209,208,209,217,217,225)
- close=1 on p03,p07,p08,p10,p13,p15,p26,p27 (8 close calls).

## 5. Determinism check
- Reran `../impl/onebrain single v4.tsv` to a second file; SHA-256 of both
  outputs identical: 8d0c7ced48aed4dfe76a90246daf5e786e2b1b2277148c69519e6a028d7b54b4
  (rerun file deleted after comparison).

## 6. Scoring vs expected (v4.1 frozen — no edits after observing scores)
- Correct (14): p01,p03,p06,p09,p10,p15,p16,p17,p19,p20,p21,p22,p26,p27
- Wrong (14): p02,p04,p05,p07,p08,p11,p12,p13,p14,p18,p23,p24,p25,p28
- Single-mode accuracy: 14/28 = 50.0% — UNDER the 70% target. NO REWRITE NEEDED.
- No re-freeze entries: v4.1 stands as the frozen set.

## Notes
- `onebrain`, `ablate`, `poison`, `min` modes were never invoked. Only `single`.
- Raw output kept in run_single_v41.txt (28 verdict lines).
