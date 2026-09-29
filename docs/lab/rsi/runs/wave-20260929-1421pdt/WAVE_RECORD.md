# Wave record: wave-20260929-1421pdt

Run-start tip: d18f7f68d (wave-20260929-1121pdt INCOMPLETE wave record).
Lock: written at wave start, removed at wave end.

## Execution mode deviation (documented)

The task body directs spawning one coordinator subagent. This wave ran
INLINE with no nested subagents. Reason: the descendant-subagent runtime
failure mode killed three waves this week (20260928-1121pdt,
20260928-1421pdt, 20260929-1121pdt; see
~/workspace/goals/tnn-rsi-loop/hidden_files/wave-20260929-1121pdt-failure.log:
"follow-up has no durable chat owner"). The 0821pdt wave ran inline with no
nested subagents and completed cleanly, which is the standing precedent for
this failure mode. Spawning a coordinator risked a fourth consecutive
runtime death and a stale lock; the time-budget priorities (debate,
LOOP_STATE, commit plus tag, lock removal) favored the inline path. The
mandatory debate group was convened as structured advocate/skeptic/judge
records with the provenance probe in every motion.

## What this wave did

Completed the 1121pdt incomplete work: red-team review and debate over the
carried causal2 evidence, a fresh fork battery, the interactive survey, and
verdicts.

### H-CAUSAL2 (independent causal arc, S8 re-freeze and re-run)

- 1121pdt finding: the wave record's "separate commits" claim is FALSE.
  All causal2 files first appear in the single commit d18f7f68d, so the
  prereg cannot be shown to predate the code. Recorded UNVERIFIABLE
  ORDERING for 1121pdt; the claim is struck (red-team F1).
- S8 remedy this wave: prereg text re-frozen byte-identical, committed
  alone (55fece368), then the full battery re-run under it with the
  pinned znc. World regenerated the frozen observation logs
  byte-identically; learner and baselines reproduced all 18 evidence
  outputs byte-identically (cmp-verified). No Python; pure Zag toolchain.
- Red-team review: redteam/REDTEAM_CAUSAL2.md (F1-F9). Independent
  recomputation of all 8 kill bars from the re-run evidence: all PASS.
- Debate: ADVOCATE_1421.md, SKEPTIC_1421.md, JUDGE_1421.md. No verdict
  overturned on rhetoric; the skeptic's attacks sustained as narrowing
  caveats (F5 recall-vs-rule, authorship-ordering distinction, 1121pdt
  integrity correction).
- Verdict: ADOPT as SURVIVES (bounded, L2 structural learning, not L3),
  with mandatory traveling caveats.

### pi_rev2 lane

NO-EVIDENCE. The 1121pdt pi_rev2 directory is empty; the worker delivered
nothing before the runtime death. No verdict possible. Debate M5 banks the
commitment: the next wave's design lane freezes the procedure-invention v2
revision prereg (L3 criterion 12) as its first act.

### Fork battery

- 1121pdt battery (69 entries): evidence intact; independently re-tallied
  67 PASS / 0 FAIL / 2 UNTESTABLE. Debate M2 CONFIRMs it as a re-tally of
  inherited outputs with the missing-debate process gap recorded.
- 1421pdt battery (71 entries): fresh full run, driver exit 0: 69 PASS,
  0 FAIL, 2 UNTESTABLE (rh-pull-1/2, expected). znc pin 498abcb5 uniform
  69/69; probe 3b29aa06 69/69; negative controls discriminate 69/69.
  Debate M3 CONFIRMs as process confirmation.

### Interactive survey

NONE new. Zero .zag files added or modified in d18f7f68d..55fece368.
tnn_chat FIT staleness 1 of 8 (due at 8 of 8).

### Commit-order self-check (this wave)

Prereg freeze 55fece368 strictly precedes the re-run evidence commit;
red-team and debate follow. VALID under S8 with the recorded distinction
(evidence-run ordering cured; source-authorship separation rests on K2-7
by-construction). No candidate adopted on 1121pdt ordering.

### Design lane

DESIGN_LANE_1421.md: no new mechanism this wave; queue re-affirmed with
the pi_rev2 prereg freeze as the next wave's first act.

## Provenance (verbatim probe)

H-CAUSAL2 prereg text, sources, logs, and probes inherited from 1121pdt;
new this wave: the re-freeze commit, the re-run evidence (byte-identical
reproductions), the red-team review, debate records, this wave record.
Fork battery 1421pdt evidence new; 1121pdt battery evidence inherited.
Interactive survey new. pi_rev2: nothing exists.

No em-dashes in wave documentation. No Python anywhere in loop work.

## Commits (all local, none pushed)

- 55fece368: prereg re-freeze (alone).
- 12c566a75: re-run evidence plus RERUN_REPORT.md.
- <debate>: red-team review, debate records, fork battery records,
  interactive survey, design lane, wave record.
- <loopstate>: LOOP_STATE.md verdict slate.
- Archive tag: tnn-native-lab-wave-archive-20260929-1421pdt at wave tip.
  (Also created retroactively: tnn-native-lab-wave-archive-20260929-1121pdt
  at d18f7f68d, pinning the 1121pdt partial-evidence tip which had no
  archive pointer.)
