# ADVOCATE BRIEF: wave-20260927-0521pdt

Role: ADVOCATE, mandatory debate group. Task: argue FOR each verdict on the proposed slate, with numbers cited from the wave evidence. Working copy: ~/workspace/tnn-rsi. Zero Python. Commit nothing.

## The skeptic's provenance probe

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: the artifacts under judgment are the three wave evidence files, all first-produced this wave inside docs/lab/rsi/runs/wave-20260927-0521pdt/: FORK_RESULTS_0521.md (fresh enumeration and battery run at this wave's run-start HEAD ecbe9b5b7), LANE_SURVEY_0521.md (fresh scan of the 02:21 to 05:21 PDT window), and INTERACTIVE_0521.md (fresh scan of merge range 463b115b6..ecbe9b5b7). Nothing in them is inherited from prior waves except the frozen pins (znc 498abcb5, probe 3b29aa06, B2 bin 75b85d3c, NEG1 E0002, NEG2 char-1 diff, R32_ZNC_PROBE_OK, the tnn_chat frozen binaries and sources) and the carried-over CONFIRMs, which are explicitly labeled [RE-CERT]. Every enumeration, every count, and every classification in this wave's evidence was produced fresh this wave.

## Verdict 1: Fork battery

CONFIRM [RE-CERT]: 49 named entries, 47 PASS, 2 extraction FAIL (expected), 0 CONFIRM. Scope: toolchain and extraction stability only on tested entries; the two pull heads remain uncovered (instrument limit, unchanged cause).

The case: this is the broadest coverage the battery has ever reported. P19 delta accounting shows named entries moved 48 to 49 with a fully audited delta: +1 newly enumerated archive branch tnn-native-lab-wave-archive-20260927-0221pdt at 463b115b6 (the first parent of the run-start merge), and a count-neutral rename of arch-20260926-2321pdt to arch-wave-20260926-2321pdt (same commit 004616f65, continuous coverage). All 9 live entries passed, including the three experimental branches (exp1 at 1010a63c3, exp2 at a2a36e657, exp-sensory at c368b8e1f) tested read-only at their run-start pinned commits, the live local HEAD ecbe9b5b7, and the live origin tip 7aad68fad via origin-tnn-native-lab-rt. Uniformity is total: 47/47 znc pin matches, 47/47 probe source matches, 47/47 B1/B2/B3, 47/47 NEG1 with E0002 from the fork's own znc, 47/47 NEG2 char-1 diff, 47/47 R32_ZNC_PROBE_OK. The single-entry dry run produced a RESULT.txt byte-identical to 0221pdt evidence, and the harness rebuild is byte-identical to prior waves. The 2 FAILs are rh-pull-1-head at 5802fec8401 and rh-pull-2-head at 4b76bb59fd, both missing the pinned toolchain path, identical cause eight waves running, non-TNN research-doc trees, still uncovered. Closing tip re-check: origin tips identical at start and close, so nothing arrived after the testing window. /tmp peaked at 5 percent; the frozen enumeration manifest ENUMERATION_MANIFEST.md is drafted, so the queued process item is now done. Local HEAD did not move during the run (ecbe9b5b7 at start and at close); the worker modified no tracked files, made no commits, and pushed nothing. Scope stamp is honest and explicit: this certifies toolchain and extraction stability only, not the contents of the merged commits.

## Verdict 2: No-new-candidates stand-down

CONFIRM [RE-CERT]: stand-down, no new mechanism. This is discipline, not stagnation; all six lanes hold prior standing with stated reasons.

The case: the lane survey counts are exact. 23 commits landed in the 02:21 to 05:21 PDT window: 9 authored by Micah (his own frontier work, CLOSED: WO-SR-1 chunker repair, native epistemics phase 1 plus NO-GO, audio round-3 MP3 kill, upscale round-3 final kill, deliberation repair rounds 2, determinism sweep with 4 hygiene work orders, the independent REDTEAM_R3 report) and 14 authored by tnn-rsi-loop, all of them the prior wave's material: 13 are the closed 0221pdt workstreams (EXP1b prereg, impl, and evidence; EXP2 follow-up prereg, freeze, and evidence; LIGHT-FIELD prereg, amendment, impl, and KILL verdict; two merges) plus 1 wave record with LOOP_STATE verdicts. The four prereg filename hits are all 0221pdt preregs, each already closed with a terminal verdict: EXP1b invention claim DEAD with certification withheld, LIGHT-FIELD KILLED clean by frozen bars (BAR1 FAIL sealed minus 1.853 dB, BAR2 FAIL checkerboard about 3x worse), EXP2 narrowed to a fidelity self-check with wire-in off the table. Zero new prereg drafts, zero re-aimed preregs, zero new design documents, zero lane-directory touches, 37 untracked entries classified as residue or fixture with zero drafts or design notes. Per-lane standing is unchanged with reasons stated: G1 stood down, D-VID-1 stood down, CV-P barred pending his ruling 6, COMP-2 ruling 6 open and P11 stemmer contingency unresolved, B1-class P9 bar reformulation not found, ST-1 DEAD on pristine evidence. No queued-item blocker was cleared (EXP1c, EXP2 grounding, and the enumeration manifest: the last of these was drafted by the fork worker this wave, which this slate's verdict 1 records as done). The judge in recent waves ruled this posture discipline, not stagnation; the numbers above are why.

## Verdict 3: Interactive TNN

CONFIRM [RE-CERT]: EXISTS for supervised red-team probe chats only, unchanged.

The case: the interactive survey is a four-layer scan with clean results at every layer. Layer 1: 1390 added files in the merge range, word-boundary scan for chat/repl/interactive: zero hits. Layer 2: 206,688-line diff, zero hits; substring check on "repl" found only "replan" and "replace" in prose, "chat" and "interactive" substrings zero. Layer 3: zero changed files in src/ or units/. Layer 4: tip grep of src/zag plus units/ for word-boundary chat/repl: zero hits. The two close cases were reviewed and dismissed on the merits: deliberate_frozen_r4repair2.zag is a batch battery runner with zero stdin reads and its loop predates the range; epistemic.zag is an argv-driven CLI verdict engine with zero stdin reads. Frozen pins verified by sha256: baseline probe binary 1ada2fae..., decline-gate probe binary 20273a99..., pinned znc 498abcb5, both frozen sources matching their README pins; zero changes to fit_authority anywhere in the range. Nothing was re-run this wave per the standing rule, and the tnn_chat FIT CONFIRMATION carries over per P12/P16 from the wave-20260925-1421pdt fresh re-run 9692f5d1d (2/2 binary reproducibility, 9/9 rerun pairs byte-identical, KB1 30/30, KB2 17/17, KB5 10/10). The confabulation caveat and the SHA256SUMS record defect travel with it. The label is therefore [RE-CERT]: not a new finding, a fresh verification that the standing posture still holds.

## Verdict 4: Prereg commit-order self-check

VACUOUS this wave (no loop candidate commits), labeled vacuous per P17.

The case: the check requires loop candidate commits in the wave, and there are none. The lane survey's prereg section independently confirmed commit order on the three prior-wave pairs (7e0326d2c before 938d188cb; 06e28f088 before 32eadf722; 4a937d994 before aa76f9b8d; amendment c6b8190f3 pre-run) matching the 0221pdt LOOP_STATE claim, but those commits belong to the closed 0221pdt workstreams, not to this wave. Since wave 0521pdt produced zero loop candidate commits, the self-check has no input and is vacuous by definition, per P17. Reporting it vacuous rather than skipping it is the correct discipline: the check was considered and found to have nothing to operate on.

## Verdict 5: His six governance rulings and his sealed-pair verdicts

UNTOUCHED [VOID]. Never decide, never re-litigate.

The case: the six governance rulings (S7 strike, MD-SSD-1, S11 pull, S11-AUD pull, C12 queue, Python-mirror logic) remain OPEN, and the lane survey records that nothing was decided, relitigated, or re-presented this wave. The sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) were not touched. This is a VOID verdict: it asserts nothing about what the correct rulings are, only that this wave did not and must not touch them. The advocate's position is that any deviation from this line would violate the standing mandate that these decisions are his alone.

## Verdict 6: DP-1 repaired sealed blind pair

Queue-HELD, ready. Presentation to his ears is the parent agent's queue decision, not this wave's.

The case: DP-1's repaired sealed blind pair is ready and remains queue-HELD per the lane survey. This wave produced no new evidence about it and no reason to move it; moving it is a presentation decision, and presentation decisions belong to the parent agent's queue, not to this wave's verdicts. Holding the queue is the correct posture: it preserves his eyes as the image kill bar and his sealed judging protocol exactly as the standing mandate requires.
