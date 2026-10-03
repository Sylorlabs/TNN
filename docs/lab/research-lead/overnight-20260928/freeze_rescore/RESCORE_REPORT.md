# Core Freeze Challenge: Pure-Zag Rescore Report

Date: 2026-09-30. Worker: Pure-Zag Freeze Scorer.
Verdict label: FREEZE-RESCORE-COMPLETE.

## Purpose

The tooling audit (commit 70c520637) flagged `score_probes.sh`
(core_freeze/run_phase/) as NEEDS-RERUN: all nine Core Freeze Challenge
world scores, and therefore the 1/9 WORLD-PASS verdict, were computed by
shell/awk. Under Micah's tooling ruling, scoring logic belongs in Zag.
This worker reimplemented the scorer in pure Zag, ran it against the
frozen artifacts read-only, and re-derived every score.

## Artifacts in this directory

- NAMECHECK.md (Step 0)
- rescore.zag (the pure-Zag scorer; builds with the pinned
  znc_linux_x86_64_abed8aa1)
- rescore_bin (compiled binary)
- build.err (compiler output)
- scores/ (full per-probe outputs for every derivation)
- RESCORE_REPORT.md (this file)

## What the Zag scorer implements

Two modes, matching the two scoring logics used in the run phase:

1. `score <world.txt> <out.txt> <seg-spec> [filter_s filter_r]`
   Replicates score_probes.sh exactly: collects QUERY (s r expected)
   triples from the world file and ANSWER (s r got) triples from the
   binary stdout, walks them in lockstep (output order matches event
   order), emits OK/MISS per probe, and prints SCORE n_correct n_total.
   Extensions over the shell script, all explicit:
   - seg-spec ("12,10"): scores named probe segments separately and
     prints SEGSCORE lines. The run worker derived W1 retention, W4
     pre/post/revert, W5 targeted/collateral, and W8 novel/recall as
     sub-scores; the Zag scorer makes those derivations mechanical.
   - optional (filter_s, filter_r): scores only probes matching an
     expected key. Used for the W6 vault sub-score (the 3 vault probes)
     and the W6b task-probe sub-score.
   - strictness: if QUERY and ANSWER counts differ, or a segment spec
     does not sum to the probe count, the scorer exits 2 with an error
     instead of silently mis-pairing. No frozen artifact triggered this.
   - ORDER-MISMATCH lines are emitted if a pair's (s,r) disagree,
     exactly as in the shell script. None occurred.

2. `grade7 <world.txt> <out.txt> <goal>`
   Implements the W7 frozen grader from DESIGN_WORLDS_PREFREEZE.md
   (section W7, "Grader simulation (frozen with this world)"). The
   transition model is read from the world's own OBSERVE lines
   (relation 621 = act0, 622 = act1); the instance structure is read
   from the marker OBSERVEs (9997/623 announces a start, 9998/623 is
   the perturbation) and ACT lines; CHOICE values come from the binary
   output in order. Each instance scores 1 if <goal> is visited during
   its ACTs. No transition semantics are hardcoded: the table comes
   from the world file.

## Derivations run (frozen artifacts, read-only)

World files from core_freeze/worlds_prefreeze/ and
core_freeze/worlds_adversary/; outputs from core_freeze/run_phase/
battery/. The frozen binary and world files were not modified.

| # | Invocation | Re-derived | Reported (RUN_RESULTS.md) |
| 1 | score W1_world.txt W1.out "12,10" | 10/12, ret 10/10 | 10/12, ret 10/10 |
| 2 | score W2_world.txt W2.out "8" | 0/8 | 0/8 |
| 3 | score W3_world.txt W3.out "10" | 0/10 | 0/10 |
| 4 | score W4_world.txt W4.out "6,6,6" | 1/6 pre, 2/6 post, 3/6 revert | 1/6, 2/6, 3/6 |
| 5 | score W5_world.txt W5.out "2,6" | 1/2 targeted, 4/6 collateral | 1/2, 4/6 |
| 6 | score w6_phaseA.txt W6phaseA.out "1" | 1/1 (diagnostic) | diagnostic -2 correct |
| 7 | score w6_phaseB.txt W6phaseB.out "5" | 1/5 treatment | 1/5 |
| 8 | score w6_phaseB.txt W6phaseB.out "3" 22001 22101 | 0/3 vault | 0/3 vault |
| 9 | score w6_controlA.txt W6ctrlA.out "1" | 1/1 (diagnostic) | diagnostic -2 correct |
| 10 | score w6_controlB.txt W6ctrlB.out "5" | 0/5 control | 0/5 |
| 11 | score w6b_phaseA.txt W6bPhaseA.out "1" | 1/1 (diagnostic) | not reported numerically |
| 12 | score w6b_phaseB.txt W6bPhaseB.out "3" | 0/3 | not reported numerically |
| 13 | score w6b_phaseB.txt W6bPhaseB.out "2" 22001 22101 | 0/2 task | 0/2 predicted |
| 14 | grade7 W7_world.txt W7.out 9704 | 0/4 (starts 9701,9702,9703,9702; goal never visited) | 0/4 |
| 15 | score W8_world.txt W8.out "5,4" | 0/5 novel, 0/4 recall | 0/5, 0/4 |
| 16 | score w9_treeA.txt W9treeA.out "28" | 0/28 | 0/28 |
| 17 | score w9_treeB.txt W9treeB.out "31" | 0/31 | 0/31 |

Every re-derived number matches the reported number. Zero discrepancies.
Zero ORDER-MISMATCH lines across all 17 derivations.

## W7 grader check

The Zag grader reproduced the design document's hand-worked
calculation: under the all-zero CHOICE sequence (24/24 CHOICE 0 in
W7.out), instance A (start 9701) visits 9701,9700,9700, perturb 9702,
9701,9700,9700,9700; instances B/D (start 9702) and C (start 9703)
similarly never visit 9704. 0/4 confirmed mechanically.

## Verdict

W1: main 10/12 meets the 80 percent bar (needs 10/12); retention 10/10
meets the 70 percent bar (needs 7/10). WORLD-PASS.

W2-W9: all below their bars (W6 fails on B4 attribution per the
adversary reading banked for the research director; numerically the
treatment is 1/5 against the 80 percent B1 bar). WORLD-FAIL.

Learner profile re-derived in pure Zag: 1/9 WORLD-PASS (W1 only).
The FREEZE-RUN-COMPLETE verdict stands, now on a pure-Zag scoring
foundation.

## Purity and process

- The scorer is pure Zag (rescore.zag); no Python, no shell/awk scoring
  logic anywhere in the derivation. Shell was used only to invoke znc,
  run the binary, and move files.
- Frozen artifacts were read-only: no world file, battery output, or
  state snapshot was modified (verified by re-running derivations;
  outputs are deterministic byte-identical across runs).
- No em dashes in this directory (shell-only byte check).
- Contaminated paper
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
  untouched (zero diff verified at commit).
- Pinned compiler znc_linux_x86_64_abed8aa1. The AGENTS.md slice
  lesson was honored: all integer arrays are u8-backed with get32/set32
  helpers; no function-local `as *i32` slice construction.
- Determinism: repeated runs produce byte-identical stdout (sha256
  verified on W4 and W7 derivations).

## Scope note

This remediation covers the freeze-challenge scoring (tooling audit
item A). The C1 race driver (item B, affecting C76) is a separate
rerun and is not addressed here.
