# RT-INT RED-TEAM REVIEW: CONSEQ + CONTLEARN, wave-20261001-2321pdt

Reviewer: RT-INT (subagent, depth 2/2). Toolchain: safebin PATH, pure shell
(sha256sum, cmp, git, grep). Zero Python invocations by this reviewer.
Read-only toward both lane directories; no lane artifacts modified.
This review's own files live only under
docs/lab/rsi/runs/wave-20261001-2321pdt/RT-INT/.

## Method

For each lane I (1) read the full record (judge brief, verdict, prereg,
run log, namecheck, build record); (2) independently hashed every claimed
evidence file and compared against the claimed hashes; (3) re-ran the
committed binaries myself and cmp-compared against committed transcripts;
(4) checked git commit ordering for the prereg rule; (5) audited the driver
source for structural-write calls and control-flow constructs; (6) read the
frozen preregs the lanes executed to confirm the kill bars are the frozen
ones, unweakened.

## CONSEQ lane verdict: EVIDENCE-HOLDS

### What was claimed

VALIDATION-PASS on the frozen Node2-v2 K-H3 prereg: 3/3 byte-identical
reruns reproduce the committed result hash 74c48d5a..., all 5 frozen kill
bars pass; causal ablations re-executed (Link 1 consequence-record disabled,
Link 3 production-read disabled) reproduce committed hashes d67cecf5... and
0d25a574..., showing the consequence record is necessary for the
utility-judgment shift and the production read is necessary for the
judgment to change behavior.

### Independent verification (all held)

- kh3_rerun run1/2/3: SHA-256 74c48d5a85087eab5d9c86aebf6075ce69f89be5736422e6bf63e897f527aae9
  on all three (3/3 identical). Equals the original committed
  node2v2_run/run1.txt hash exactly. The rerun reproduces the original
  result bit for bit.
- l1_run1/2/3: d67cecf5d28f7ea09396da3fd7f0ef2244f1d9e067b98ced5deb4ca90f2cf5bf
  on all three. Equals the original node2v2_ablation/abl_l1_run1.txt hash.
  The original abl_l2 runs share this hash, consistent with the lane's
  L1=L2 pair claim.
- l3_run1/2/3: 0d25a5741a3c99b7257033b7ae4881f6481b08ba86022e48f2c216aa885cb92d
  on all three. Equals the original node2v2_ablation/abl_l3_run1.txt hash.
- Re-ran the committed n2v2_test_bin myself: output byte-identical to
  committed run1.txt (cmp clean).
- Transcript content matches every claimed bar: Phase 1 default 30 no
  shift; Phase 2 mids 30, 30, 45 (shift fires only on the 3rd consistent
  revelation, not earlier); Phase 3 guide carries 45. L1 ablation: 30, 30,
  30, no shift, FAIL on the kill bar as designed. L3 ablation: write fires
  (default 45) but Phase 3 guide carries 30, FAIL on the read bar as designed.
- Source hashes: n2v2_test.zag 99774fbc... and abl_l1.zag 8698eb3e... match
  the claimed committed sources.
- Kill bars checked against the frozen prereg
  (node2v2_run/FROZEN_PREREG.md, Section 5, commit 4b05c8011): the four
  content bars plus 3/3 determinism are verbatim the frozen bars. No
  weakening, no additions.
- Commit order: prereg 4b05c8011 (2026-10-01 18:24:03 UTC) strictly precedes
  build 0988839a2 (2026-10-01 18:25:24 UTC), an 81s gap. The prereg
  commit-order rule is honored for the executed test.
- Lane commits this wave (e068ac9a, 473631b6) touch only the CONSEQ lane
  directory, local only, nothing pushed.

### Strongest attacks mounted, and whether they held

1. Mechanism-vs-artifact: the "consequence record" is node-private history
   slots (fields 8/12/16) and the "consequence-derived utility" is a
   researcher-written 3-consecutive-agreeing-revelations rule; the "world
   revelations" are events in a builder-authored test script, not an
   independent world. Attack outcome: TRUE as a description, but it does not
   kill the claim. The frozen prereg Section 6 already forbids claiming
   inquiry discrimination, learner-authored procedures, SUF, L3, H1, or
   generality, and the lane's "Scope honestly held" section carries every
   one of those bounds plus "validates the consequence re-entry template,
   not the shared tag-61 substrate itself". The ablation evidence is
   genuinely causal for the implemented mechanism: disabling the record
   blocks the shift despite identical world events, and disabling the read
   blocks behavioral change despite a fired write. The claim as stated is
   exactly what the evidence shows.
2. Independent-adversary gap (carried-forward qualification): the frozen
   prereg required the sealed world to be designed by an independent
   adversary after freeze. The original evaluation used builder-sealed
   worlds, and this re-execution replays those worlds. This lane therefore
   confirms reproduction fidelity of the frozen test, not independent
   adversarial validation; it inherits the gap without closing it. The lane
   discloses this ("Builder-sealed worlds (hash-transparent)... Independent-
   adversary replication still preferred"). It does not invalidate
   VALIDATION-PASS, which is a claim about the frozen test as executed, but
   the coordinator should not cite this wave as closing the
   adversary-independence clause.
3. Metric gaming: no evidence of it. Bars are the frozen ones, numbers match
   transcripts I re-hashed and re-ran myself, hashes match committed records
   bit for bit.

No dissent. The verdict stands with the two qualifications above, both
already disclosed in the lane's own honest-bounds section.

## CONTLEARN lane verdict: EVIDENCE-HOLDS

### What was claimed

BUILD-PASS: LEARNOWN-DEMONSTRATED. K0 through K6 all pass: prereg frozen
alone at 408ffdcdc before implementation; one process per run; one logged
znc build; frozen core SHA-256 a29972ca... verified; driver audit clean;
pure Zag; 2021pdt battery re-run with no regression (stdout hash
53ff2c99..., REUSE_COUNT 30/30); probe results STORE_OK 13/13, REUSE_OK
20/20, REUSE2_ORIG 0/20 with REUSE2_NEW 20/20, NOSTORE 20/20 true misses
with 20 UNCERT nodes; UNCERT_TREAT 0; 3/3 byte-identical transcripts per
mode. The claim is bounded by prereg Section 7 to the weak H10 reading of
"learner-owned" (resident in the learner's arena, manipulated only through
the frozen event interface), with no learner agency, no procedure execution
at query time (Attack 6 carried forward), no L3, no generality, disclosed
script.

### Independent verification (all held)

- Commit order: prereg 408ffdcdc (2026-10-02 06:30:45 UTC, design only)
  strictly precedes implementation dfcd3caf (2026-10-02 06:34:07 UTC);
  `git merge-base --is-ancestor 408ffdcdc HEAD` true. K0 PASS.
- Frozen core from git object f4de7ff46: SHA-256
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
  Matches the prereg commitment. K2a PASS.
- lo_core_nomain.zag differs from the frozen core by exactly one deleted
  line (the `fn main` entry point, line 1357; diff-verified) and is
  byte-identical (26b455e7...) to the 2021pdt lane's cl_core_nomain.zag.
- Build artifact hashes match DRIVER.md: lo_driver.zag 49874d39...,
  lo_core_nomain.zag 26b455e7..., lo_combined.zag 38c76664..., lo_driver
  binary 35f78f8c....
- Driver source audit: 0 `switch`/`match` occurrences, 0
  alloc_node/link_edge/ns( calls in lo_driver.zag; znc_invocations.log has
  exactly 1 entry; harness.log shows exactly 6 spawns (3 TREAT, 3 NOSTORE),
  all rc=0, pid_leak_check=0; all 6 stderr files are 0 bytes. K1a, K1b, K2b
  PASS on independent re-check.
- Transcript hashes: TREAT 1ff527fa... and NOSTORE 839e6614..., identical
  across the 3 committed reps each. I re-ran the committed lo_driver myself
  in both modes: outputs byte-identical to the committed transcripts
  (cmp clean), exit 0, zero stderr. K6 PASS.
- Transcript content: 92 TREAT events and 20 NOSTORE events (counted), every
  query masked (`-2 MK`, no answer keys); STORE_OK 13/13; REUSE 20/20 with
  content-expected serving nodes; ABLATE contradicts return rv=0; REUSE2
  returns 0/20 original values and 20/20 successor values (9901+i on
  families A/B, 9801+i on family C); NOSTORE 20/20 misses with exactly 20
  UNCERT nodes and K4D_UNCERT 20; AUDIT_PASS on all runs; FNV-1a checksums
  match RUN_LOG (1570275895 / -2062244938); census lines match RUN_LOG
  (CENSUS STORE N1=39 N20=13 N30=0 N101=26 N102=26 N902=65 Eall=154, etc.).
  K1c, K4a-d, K5 PASS.
- K3 independently re-verified by me: committed 2021pdt cl_driver binary
  (c8c089b8..., matching the hash recorded in RUN_LOG) re-run 3x in TREAT
  mode gives stdout SHA-256 53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44
  on all 3 reps, REUSE_COUNT 30 with R1C 6, R2C 3, R3C 3, R4C 12, R5C 6.
  K3 PASS.

### Strongest attacks mounted, and whether they held

1. "Masked query" is still researcher-supplied scaffolding (the task's
   question 5). The facts: flags=1/expected=-2 are researcher-set on every
   query; the trial order (k-hop chains first, then sums, counts, 1-hop) and
   the accept rule (first candidate with v!=-2 && v!=-999999) are frozen
   researcher machinery; the event script teaches exactly the chain
   structure the queries then exercise (curriculum supervision); no
   learner-created state influences any store, accept, or retrieve decision
   (H2-v2/H3 stand, stated in prereg Section 1); query-time "reuse" is
   exact-hit retrieval of machinery-taught facts via `activate`, not
   execution of promoted MAPs (Attack 6, carried forward verbatim). Attack
   outcome: TRUE as a description, and it correctly bounds what this wave
   shows. Removing the answer keys is genuine incremental progress: it kills
   the specific confound the 2021pdt red team flagged (the learner's causal
   contribution was zero WITH keys supplied; the machinery's store/retrieve/
   reuse path is now shown not to route through the supervisor at all). It
   does not escape scaffolding in general. The lane never claims it does:
   the prereg froze the weak H10 reading as the operative definition of
   "learner-owned" for this probe, Section 7 bounds the claim to the frozen
   core's event-triggered machinery, and the verdict's "Step toward
   learner-owned, stated plainly" repeats that the strong reading (the
   learner decides or authors) is not demonstrated and not claimed. The
   strongest attack lands inside the claim's stated bounds; it does not
   kill the frozen claim.
2. Label risk: "LEARNOWN-DEMONSTRATED" will mislead any reader who imports
   the strong reading of learner-owned. This is a documentation hazard, not
   an evidence failure: the prereg defines the weak reading explicitly in
   Section 1 and the verdict repeats the bounds three times. I recommend
   the coordinator keep the weak/strong distinction attached to the label
   whenever it is cited outside this lane.
3. Metric gaming: no evidence of it. Every number was re-derived from
   committed transcripts or reproduced by my own binary re-runs; bars are
   the frozen ones (checked against PREREG_LEARNOWN.md Sections 4-5); the
   commit-order rule was verified, not merely asserted.

No dissent. The verdict stands, with the carried-forward qualification that
progress is confined to the weak H10 reading and that the scaffolding
(flag-setting, trial order, accept rule, curriculum script, and the
exact-hit nature of reuse) remains researcher-authored by frozen design.

## Reviewer notes for the coordinator

- Both lanes' honest-bounds statements are sufficient and unusually
  careful; neither over-claims relative to its frozen prereg. The main
  remaining gaps (adversary-designed sealed worlds for CONSEQ's K-H3 line;
  sealed adversarial worlds for the three new mechanisms generally) are
  the standing post-freeze battery, which both lanes explicitly defer to.
- No frozen-prereg edits, no toolchain violations, no commits outside the
  lane directories, nothing pushed. This review touched only RT-INT/
  plus read-only inspection elsewhere.
- Pure-Zag compliance of the reviewer: no forbidden interpreter invoked
  (safebin PATH; `which python3` empty at setup and recorded in
  RT-INT/NAMECHECK.md Step 0).

## Commit ids

- RT-INT review commit: (recorded at commit time)
- CONSEQ lane commits this wave: 473631b6 (re-execution + ablations),
  e068ac9a (K-H3 disambiguation)
- CONTLEARN lane commits this wave: 408ffdcdc (prereg, phase 1),
  dfcd3caf (implementation + verdict, phase 2)

## Evidence paths

- This review: docs/lab/rsi/runs/wave-20261001-2321pdt/RT-INT/RT-INT_REVIEW.md,
  docs/lab/rsi/runs/wave-20261001-2321pdt/RT-INT/NAMECHECK.md
- CONSEQ: docs/lab/rsi/runs/wave-20261001-2321pdt/CONSEQ/{JUDGE_BRIEF.md,
  NAMECHECK.md, kh3_rerun/, ablation_rerun/}
- CONTLEARN: docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN/{PREREG_LEARNOWN.md,
  VERDICT_LEARNOWN.md, JUDGE_BRIEF.md, RUN_LOG.md, DRIVER.md, NAMECHECK.md,
  transcript_TREAT_r*.txt, transcript_NOSTORE_r*.txt, harness.log,
  znc_invocations.log, lo_driver, lo_combined.zag}
- Frozen preregs executed: docs/lab/research-lead/overnight-20260928/node2v2_run/FROZEN_PREREG.md
  (commit 4b05c8011); CONTLEARN prereg in-lane (commit 408ffdcdc)
- Frozen core: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
  (commit f4de7ff46)
