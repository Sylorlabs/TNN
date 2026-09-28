# H3 — HELLHOLE Rescue: RUNLOG

2026-09-23. Tier-3 hardening probe H3 (prereg `PREREG_TIER3_WAVE2.md`).
All work in `~/workspace/scratch-crossref/T3/HARDEN/h3/`.

## Orientation

- Read Tier-2 T2-HELLHOLE verdict (FAIL: K1+K2 trip both arms) and the
  frozen prereg's gate counterfactual (WITHHOLD-before-corroboration on
  contested/ambiguous/evolved/skepticism → helper FULL PASS, solo fails on
  C15/C16 spam pair alone).
- First inspected `internet-trial/src/ht_trial.zag` — a Phase-1 scaffold
  with stub sense adapters (`ht_sense_gate` etc.). NOT the executed
  mechanism. Located the real Phase-2 pipeline: `phase2/src/ht_decide.zag`
  → `ht_sense2.zag` → `ws2_sense.zag` (`ws_decide`), supervised by
  `phase2/supervisor/ht_supervise.py`, scored by `ht_score.py`.
- Candidate index→ID order is NOT C1..C16 sequential: `ht_score.py`
  IDX2ID = {0:C1,1:C2,2:C3,3:C4,4:C14,5:C5,6:C6,7:C7,8:C8,9:C9,10:C10,
  11:C11,12:C12,13:C13,14:C15,15:C16,16:A1,17:A2,18:A3}. An early harness
  draft used the wrong order; caught during fidelity checking and fixed
  before any gated run.
- Known-prior candidates (ht_cand_known): idx 0 (C1), 4 (C14), 16-18
  (A1-A3), installed="AFFIRM", trigger=3. A1-A3 contra="DENY" → REVISE
  via ws_domains2 (≥2 distinct DENY domains). C1/C14 over-withhold
  reproduced: a single dissenting/IRRELEVANT observation forces the
  known-path to HOLD_INSTALLED → WITHHOLD.
- `ht2_add` stores stance-0 as answer "IRRELEVANT" (relevance 1) — NOT
  skipped. Early harness draft skipped them; fixed for fidelity (matters
  when IRRELEVANT is the plurality answer).

## Mechanism change

- Copied `phase2/src/ws2_sense.zag` → `src/ws2_sense_gated.zag`;
  original kept as `src/ws2_orig.zag`.
- Patch (applied by auditable Python script, 4 hunks):
  1. `tag:i32` field added to `WsF` (after `last_inst`).
  2. `w.*.tag=0` init in `ws2_new`.
  3. New setter `ws_set_tag(w, tag)`.
  4. In `ws_decide`, after the known-prior block, before corroboration
     counting: `if(tag==1||tag==2||tag==3||tag==6) return 2;`
     (WITHHOLD-before-corroboration). Tags: 0=SETTLED 1=CONTESTED
     2=EVOLVED 3=AMBIGUOUS 4=SPAM 5=FALSE 6=SKEPTICISM.

## Harness

- `src/h3_data.zag` (generated): 19 frozen candidates with last-visit
  (domain,stance) from `phase2/evidence/{solo,helper}/session.htsv`,
  correct IDX2ID order and tags; 12 fresh authored items F1-F12
  (contradiction pairs, spam-pair variants, stance-inversion traps).
- `src/h3_gate.zag`: replicates ht2_begin/ht2_add/ht2_end incl. known-path,
  IRRELEVANT storage, ws_domains2 contra check, trial mapping
  (2=INSTALL 3=REJECT 4=WITHHOLD 5=REVISE). argv[1]="0" ungated / "1" gated.
- Pinned toolchain `znc_linux_x86_64_abed8aa1`. Pure Zag, zero RNG.

## Runs

1. **Ungated baseline** (`./h3_gate 0`): 38/38 per-candidate dispositions
   match committed `evidence/{solo,helper}/score.json` exactly —
   solo K1 4/9 M1 5/9 K2 3/3; helper K1 2/9 M1 7/9 K2 3/3.
   (`run_ungated_r1.txt`)
2. **Gated** (`./h3_gate 1`) ×3: byte-identical, SHA
   `cbcfd5ee9b753b94710931eb0afd2d138b88b8d3f38dc3f42f1dc663a708b0e1`
   (`run_gated_r1.txt`, `r2`, `r3`).
   - Frozen: solo K1 2/9 (C15,C16 — trips), M1 7/9, K2 0/3;
     helper K1 1/9 (C15 — clear), M1 8/9, K2 0/3. K3/K4/K5 clear.
   - Fresh: F1-F4 4/4 WITHHOLD; F5-F8 4/4 INSTALL (spam, both arms);
     F9-F12 4/4 WITHHOLD (ungated they installed 4/4).

## Result

Verdict **BOUNDARY-MAPPED** (see `H3_VERDICT.md`): K2 rescued both arms,
K1 rescued for helper, K1 fail stands for solo on the spam pair alone —
exactly the Tier-2 counterfactual, now confirmed with a real mechanism
change. Spam-farm collusion (frozen C15/C16, fresh F5-F8) is outside the
gate's coverage and still installs: named boundary, follow-up is a
distinct-origin/provenance-diversity defense (not tested here).
