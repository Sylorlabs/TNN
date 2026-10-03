# JUDGE_BRIEF: CONTLEARN-OWNED machinery-disabled discrimination

RENDER_SHA: d2fc968f4
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: CONTLEARN INTEGRATION-DEMONSTRATED (2021pdt 30/30;
2321pdt LEARNOWN-DEMONSTRATED 13/13 store, 20/20 masked reuse) with the
red-team QUALIFY that the integration work is done by researcher
machinery, not by the learner
NEW_KNOWLEDGE_CLAIM: With the event-triggered trial/promotion/P-INV
machinery verified absent from the query path, the continuing learner
stores taught facts and serves them by standing retrieval but integrates
0/6 fresh 2-hop chains (all probes miss; zero MAPs; only UNCERTAINTY/guide
accumulation), while the unmodified frozen core integrates 6/6 on the
identical battery, so the integration work sits on the researcher side of
the control-plane line.

## Verdict

MACHINERY-DEPENDENT. CO-4 passes and CO-1 fails. The red-team QUALIFY
stands, strengthened by a clean discrimination.

## Numbers vs frozen kill bars

- CO-1 (TREAT integrates to the DEMONSTRATED bar): FAIL. STORE_OK_T 0/6,
  REUSE_OK_T 6/12, DELAYED_OK_T 6/12 (bars: 6/6, 12/12, 12/12). All 18
  family-D masked probes took the true miss path (returned -2).
- CO-2 (learner-mechanism evidence): PASS. Census complete and 3/3
  consistent. TREAT: MAPC=0 at every phase; UNC/GUIDEC 6/12/18; the only
  DEP edges are guide-to-UNCERTAINTY edges from `miss_inquire`. CONTROL:
  MAPC=6; DEPC=24 (12 construction-provenance from `t2_asm_chain`, 12
  promotion citations from `promote_graph`); UNC=0, GUIDEC=0. SANITY_E_T
  6/6 proves the variant is functional (standing retrieval intact).
- CO-3 (determinism): PASS. 3/3 byte-identical per binary. TREAT
  `60a8b778a2b9ddaf629101912f20f45e7b7373ac0b09090b80a7dbb4705819ca`,
  CONTROL
  `54b3cd30d3a7ac06114ba128d488b2e9406056ed466d8f8ed3bf55eef003bcc1`;
  FNV-1a TREAT -677949997, CONTROL -1785692917; exit 0; zero stderr;
  no PID/timestamps/paths.
- CO-4 (control reproduces the DEMONSTRATED bar): PASS. STORE_OK_C 6/6,
  REUSE_OK_C 12/12, DELAYED_OK_C 12/12 on the unmodified frozen core.
- CO-5 (machinery truly absent): PASS. Source diff shows exactly the two
  removed `ev_query` call blocks (variant-diff SHA-256
  `3f385dc56367337f352da35ffd1b29bde0b7a124c68a42a57d717ad043cfaa75`);
  zero event-interface call sites to the five machinery functions by
  grep; zero MAP nodes on any of the 18 TREAT family-D probes.
- K0/K1/K2 (governance): prereg frozen alone at 3e837ff5c, Amendment A1
  re-frozen alone at d2fc968f4 (audit count 104->98; tuples/bars/decision
  unchanged); strict-descendant implementation verified by merge-base;
  6 learner processes (3+3), one per 98-event run; exactly 2 logged znc
  builds, 0 during runs; AUDIT_PASS 6/6; frozen SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  verified three times (blob `b226b223cb3ee0be742af673653fb8ea8605f281`
  equals the f4de7ff46 freeze blob); driver audit clean (0 cognition
  functions, 0 structural writes, 0 new tags/edges/opcodes/modes);
  pure Zag (`which python3` empty).
- K3 (no regression): PASS. Committed 2321pdt `lo_driver` re-run
  read-only 3/3, stdout SHA-256
  `1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9`
  (matches recorded value).

## What this does not claim

No learner agency in the causal sense (H2-v2/H3 stand); no procedure
execution at query time (Attack 6 carried forward: CONTROL reuse is
exact-hit retrieval of machinery-taught facts); no L3; no generality;
the script is disclosed-in-prereg with fresh ids/relations, not a sealed
adversarial world; the variant core is a measurement instrument, not a
proposed architecture.

## Evidence paths (lane directory)

- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/PREREG_OWNED.md`
  (frozen prereg; Amendment A1 re-freeze commit d2fc968f4)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/DRIVER.md`
  (build record; `ow_control`
  `58f2f9f2d3855c782106d41266bc30acea29870ea0cf1f1b08282ef78954d400`,
  `ow_treat`
  `6b65e6a62e56f43feb14e1afa45309c9512759ad7ba471a24d68b6b0502c2f71`)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/RUN_LOG.md`
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/VERDICT_OWNED.md`
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/transcript_ow_treat_TREAT_r{1,2,3}.txt`,
  `transcript_ow_control_CONTROL_r{1,2,3}.txt`, `harness.log`,
  `znc_invocations.log`

## Architecture accounting

Cognition source delta 0/0/0 on the frozen path. New modes/bridges/
handlers/semantic cases 0. The variant is a disabled-machinery
measurement instrument (CO-5 verified), not a learner design. One-system
rule satisfied: single persistent arena, frozen formats, no independent
subsystem state.

## Recommended follow-up

None required by this lane. The sharpened standing question for the
coordinator: the frozen core contains no learner-invoked trial/construct
machinery, so learner-owned integration currently has no mechanism to
run on. A future LEARNER-OWNED push must first propose a mechanism by
which learner-created state initiates structure construction (the
constitution's learner-authority metric); per the no-patch-treadmill
rule, this verdict is followed by root-cause analysis, not by new
handlers, modes, or opcodes.
