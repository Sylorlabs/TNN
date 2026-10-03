# JUDGE_BRIEF: CONTLEARN-OWNED2 machinery-disabled integration discrimination

RENDER_SHA: ffd31dbb3
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: CONTLEARN INTEGRATION-DEMONSTRATED (2021pdt battery
REUSE_COUNT 30/30; 2321pdt LEARNOWN-DEMONSTRATED under the weak H10
reading: unsupervised store 13/13, masked reuse 20/20, ablation-verified
dependence on stored structures) and its red-team QUALIFY (the integration
work is done by researcher machinery, not the learner: frozen trial search
order, first-clean-candidate accept rule, and promotion rule; no
learner-created state influences any store, accept, or retrieve decision;
Attack 6 carried forward: reuse is exact-hit retrieval of
machinery-taught facts via activate, not execution of promoted MAPs)
NEW_KNOWLEDGE_CLAIM: With the trial/promotion/P-INV machinery verified
unreachable from the event interface, the continuing learner integrates
0/6 fresh 2-hop chains on the identical 98-event battery (all 18 D probes
take the true miss path; zero MAPs; UNCERTAINTY/guide accumulation is the
only learner-side response) while the unmodified frozen core integrates
6/6, so the red-team QUALIFY stands: integration is machinery-dependent.

## Verdict

MACHINERY-DEPENDENT. CO-4, CO-5, K0, K1, K2, K3, CO-3 pass; CO-1 fails.

## Numbers vs frozen kill bars

- CO-1 (TREAT integrates to the DEMONSTRATED bar): FAIL. STORE_OK_T 0/6
  (need 6); REUSE_OK_T 6/12 (need 12); DELAYED_OK_T 6/12 (need 12).
- CO-2 (learner's own mechanisms identified): PASS. Per-phase census 3/3
  consistent; failure signature: MAPC=0 at STORE/REUSE/DELAYED, D_MISS
  6/6 in all three probe phases, UNC 6/12/18 and GUIDEC 6/12/18
  accumulation, DEPC==GUIDEC (guide-to-UNCERTAINTY edges only),
  E_OK 6/6 in all three probe phases via activate standing retrieval.
- CO-3 (determinism): PASS. 3/3 byte-identical per binary: TREAT
  27676a22ea1043376453022063b21e85376084f6a19aa1ddb9959f0c7e387c57,
  CONTROL
  8454f6dbef98744acb8793e3cba279da72364ec76b7527c56e36213a8ad10aac;
  FNV-1a equal across reps (-677949997 / -1785692917); rc=0; 0 stderr
  bytes; AUDIT_PASS 98/98; no PID/timestamps/paths.
- CO-4 (control reproduces the DEMONSTRATED result): PASS. STORE_OK_C
  6/6, REUSE_OK_C 12/12, DELAYED_OK_C 12/12, MAPC=6, UNC=0, GUIDEC=0.
- CO-5 (machinery truly absent): PASS. (a) diff shows exactly the six
  deleted lines (diff hash
  3f385dc56367337f352da35ffd1b29bde0b7a124c68a42a57d717ad043cfaa75);
  (b) caller analysis: zero event-interface call sites of
  mp_run/t2_trial/t2_try_verify/promote_graph/bootstrap_miss; (c) zero
  new MAP nodes on any TREAT D probe.
- K0/K1/K2 (governance): PASS. Prereg ffd31dbb3 plus transparent erratum
  78d8c9e54 (98-event script correction; pilot runs voided and disclosed)
  both strict ancestors of the implementation; 6 official processes, one
  per 98-event run, pid_leak_check=0; fresh znc log exactly 2 entries
  pre-run, 0 during; frozen core SHA-256
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  verified before implementation, before builds, and after runs
  (working-tree blob b226b223c equals the f4de7ff46 blob); driver audit
  clean (0 cognition functions, 0 structural writes, 0 new
  tags/edges/opcodes/modes/bridges, 0 switch/match); cognition source
  delta 0/0/0; pure Zag (NAMECHECK.md Step 0).
- K3 (no regression): PASS. Committed 2321pdt lo_driver 3x TREAT: stdout
  1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9
  on all 3 reps.

## What this does not claim

No learner agency in the causal sense (H2-v2/H3 stand); no procedure
execution at query time; no L3; no generality; the variant core is a
disabled-machinery measurement instrument, not a proposed architecture;
the script is disclosed, not a sealed adversarial world.

## Evidence paths (lane directory)

- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2/PREREG_OWNED2.md`
  (frozen prereg, commit ffd31dbb3)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2/PREREG_OWNED2_ERRATUM1.md`
  (transparent re-freeze, commit 78d8c9e54)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2/DRIVER_OWNED2.md`
  (build record; binaries ow_driver_treat
  d969faa29232ad3601d87ffeded3a01536c95414f803e3b91524dbef633f4039,
  ow_driver_control
  769379cc556fc0a4d4d15ac806b7646c1dc7d264a60a8223ec873e05fa0883c5)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2/RUN_LOG_OWNED2.md`
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2/VERDICT_OWNED2.md`
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2/transcript_TREAT_r{1,2,3}.txt`,
  `transcript_CONTROL_r{1,2,3}.txt`, `harness_ow.log`,
  `znc_invocations_ow.log`

## Architecture accounting

Cognition source delta 0/0/0. New modes/bridges/handlers/semantic cases 0.
The single persistent workspace is the frozen arena in both binaries; all
structures in frozen formats. One-system rule satisfied by construction.
