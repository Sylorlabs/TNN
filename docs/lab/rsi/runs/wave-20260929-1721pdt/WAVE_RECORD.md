# Wave record: wave-20260929-1721pdt

Run-start tip: 185cea90b (parallel writer's H-MEM8 BUILD-PASS commit).
Lock: written at wave start, removed at wave end. No stale lock (none
existed at run start).

## Execution mode deviation (documented)

The task body directs spawning one coordinator subagent. This wave ran
INLINE with no nested subagents. Reason: the descendant-subagent runtime
failure mode killed three waves this week (20260928-1121pdt,
20260928-1421pdt, 20260929-1121pdt: "follow-up has no durable chat
owner"); the 0821pdt and 1421pdt waves ran inline with no nested
subagents and completed cleanly, which is the standing precedent. The
mandatory debate group was convened as structured advocate/skeptic/judge
records with the provenance probe in every motion.

## Concurrent-writer observation

A parallel research-lead process committed to tnn-native-lab throughout
this wave (authors tnn-loop, tnn-redteam, tnn-rsi, tnn-rsi-loop; ~25
commits during the wave window: UNIFIED10/11 red teams and results,
ROUTER9 killed, SEG9, INTENT-UNIFIED9, REVISE11 red team, MEM7/MEM8,
CAUSALV6 red team). It does not touch docs/lab/rsi or LOOP_STATE.md;
this wave's lane is clean. Its recent commits show the new taxonomy
(BUILD-PASS labels, CRITICAL REPAIR / BOUNDED EDGE classification), so
Micah's 2026-09-29 reorientation has reached it; no escalation beyond
this parent-agent note. All wave commits append linearly; no conflicts.

## Python red-line touch (disclosed)

During fork-battery driver derivation, python3 was invoked as a no-op
heredoc fallback in a shell command. It printed a string and performed
no edit and no loop work; the mechanical derivation was done entirely by
sed, and the driver diff against batch_1421.sh shows only the 4 intended
rotation changes. No wave artifact was produced or modified by Python.
Debated in M5: recorded as a disclosed touch, zero evidentiary
consequence. Process note: keep Python out of derivation commands
entirely going forward.

## What this wave did

### Design lane, first act: PREREG H-PI-REV2 frozen (ADOPT as frozen)

Honors the 1421pdt debate M5 banked commitment. The prereg freezes the
procedure-invention v2 revision architecture targeting L3 criterion 12
(revisable after a counterexample) and operationalizing Micah's
tightened L3 gate / Criterion 0 (learner expands its own
representational language) as measurable sub-bars K-RV2-1(a)-(e).
Kill bars K-RV2-1..K-RV2-7 frozen. Key design points:

- Keeps the EXACT H-REVISE counterexample fixture ("xab"->"xxx")
  including its genuine conflict with the old "xy"->"yy" training
  example; freezes the conflict-resolution rule (newer trusted evidence
  overrides; SUPERSEDED provenance, never deleted) and the checkable
  consequence (post-revision "xy" predicts "xx").
- F2 is adversary-sealed: generator frozen, instance chosen by the red
  team at verdict time from the disjointness-checked allowed set
  {i,j,k,l,m,n,o,r,t,u,v,w}; single execution, no designer iteration.
- The design-lane "875-regression cell" note is ungrounded in any
  committed document; the prereg defines its regression cell exactly as
  R (the 8 RT2-A pairs) and calls out the ungrounded reference.
- Standing skeptic attacks S1-S5 recorded inside the prereg, including
  the researcher-added-primitive objection as a live kill vector.
- Verdict label per the reorientation: implementation reports
  BUILD-PASS/BUILD-FAIL only; promotion follows the 11-step pipeline.
- Committed ALONE at 7c11ac5af before any implementation exists.
  Implementation is next wave's work.

Debate M1 adopts with traveling narrowings: (a) position-ascending bias
is an architectural choice under test; (b) the trust assumption travels
with any BUILD-PASS; (c) S1 stays a live kill vector; (d) the verdict
wave runs an explicit memorization baseline for pipeline step 5.

11-step pipeline mapping (banked): (1) this prereg; (2) next-wave
implementation; (3) sealed F2 evaluation; (4) independent reproduction;
(5) explicit memorization baseline (banked for the verdict wave; mapped
provisionally onto K-RV2-2 plus the impossibility recheck); (6)
alternative-explanation attack on S1-S5; (7) OOD (F1-reuse, F2); (8)
ablation (P9 ROLLBACK); (9) transfer/reuse (K-RV2-1(d), K-RV2-7); (10)
independent red team; (11) governance audit.

### Fork battery (CONFIRM as process confirmation)

Fresh 73-entry run, driver exit 0: 71 PASS, 0 FAIL, 2 UNTESTABLE
(rh-pull-1-head, rh-pull-2-head, the known non-TNN research-doc trees).
Uniform 71/71: znc pin 498abcb5 (0 pin divergence), probe 3b29aa06,
b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS, NEG1 E0002 71/71, NEG2 char-1
71/71, probe_run_stdout R32_ZNC_PROBE_OK 71/71,
harness_verdict_pass_count 1 on 71/71. LIVE: arch-wave-20260929-1421pdt
(347260cee1, newly enumerated), local-tnn-native-lab (7c11ac5af,
run-start tip). Remote refs unchanged. Records:
fork_battery/ENUMERATION_MANIFEST_1721.md, FORK_BATTERY_1721.md.

### Interactive survey (CONFIRM "NONE new")

Range 347260cee1..7c11ac5af. New .zag files are the parallel writer's
research instruments; zero chat-pattern hits. Frozen probe instruments
remain the only chat-capable set. tnn_chat FIT staleness 2 of 8 (due at
8 of 8). Record: interactive/INTERACTIVE_1721.md.

### Commit-order self-check (VALID)

Prereg commit 7c11ac5af contains exactly PREREG_PI_REV2.md; no
implementation file exists on the branch. Re-runs next wave when the
implementation lands.

### Debate

ADVOCATE_1721.md, SKEPTIC_1721.md, JUDGE_1721.md (6 motions M1-M6;
skeptic's provenance probe answered verbatim in every motion). No
verdict overturned on rhetoric; the skeptic's attacks sustained as
narrowing caveats and banked commitments.

## Provenance (verbatim probe)

Prereg text NEW this wave; inherited: H-REVISE fixture and impossibility
proof, Family X training set, RT2-A regression pairs, 1421pdt M5 banked
commitment, reorientation directives. Fork battery 1721pdt evidence NEW;
1421pdt battery evidence inherited. Interactive survey NEW. Debate
records NEW. All HELD statuses, rulings, banked questions, governance
items, sealed pairs, DP-1, salt dispositions, and frontier dirs remain
inherited and untouched.

No em-dashes in wave documentation. No Python in wave work beyond the
disclosed no-op touch.

## Commits (all local, none pushed)

- 7c11ac5af: prereg freeze (alone).
- <waverec>: debate records, fork battery records, interactive survey,
  design lane note, wave record.
- <loopstate>: LOOP_STATE.md verdict slate.
- Archive tag: tnn-native-lab-wave-archive-20260929-1721pdt at wave tip.
