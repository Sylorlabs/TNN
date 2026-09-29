# Debate: wave-20260929-0821pdt -- JUDGE RULINGS

Judge: coordinator (acting judge). Standard: a debate overturns a
verdict only on cited evidence, never rhetoric. No frozen bar was
weakened in any motion. The skeptic's provenance probe ("What is the
provenance of the artifacts under judgment, and what exactly is new
versus inherited?") is answered verbatim in every motion below.

## M1: H-EXP adoption -- ADOPT (narrowed classification)

Provenance probe (verbatim): What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited? The prereg
(PREREG_H_EXP.md), the six hypothesis fixture files, the
implementation (exp_learn.zag), the seven execution outputs, the run
script, and the red-team report are all new this wave under
docs/lab/rsi/runs/wave-20260929-0821pdt/. Inherited and untouched: the
pinned znc toolchain, Micah's frontier dirs (surveyed read-only),
all prior wave records, and every HELD/banked item.

Ruling on the skeptic's five points, with evidence:

1. "The experiment was never run." SUSTAINED as a scope limit. The
   frozen claim was selection plus inspectable trace, and that claim
   passed 5/5 bars. No world contact occurred and no hypothesis was
   refuted. The judge therefore narrows the classification: ADOPTED
   as "bounded discriminating-sequence selection; world contact not
   demonstrated." H-EXP2 (execute a selection against a hidden law
   and refute a hypothesis) is queued, not claimed.
2. "Same-author pairs." SUSTAINED as a limit. P3 and the renamed-copy
   run prove data-drivenness within one author's fixtures, not
   across authors. A second-author adversarial pair is queued for
   H-EXP2. This limits the strength of K-E5, it does not fail it:
   K-E5's frozen bar (select [0,4] on P3 with both names in the
   trace) was met exactly.
3. "Amendment demerit." RECORDED as a hygiene demerit. The amendment
   (c06a23cfb) was transparent, pre-execution, and semantic-free
   (rule contents byte-identical; only the format-required HYP name
   lines added). It does not void the prereg, but the judge notes
   the freeze would have been cleaner had the format been
   machine-checked before freezing.
4. "Toward Level D inflation." SUSTAINED. Level D requires the
   learner to ACT to obtain missing information; this module only
   PROPOSES. The verdict classification is narrowed accordingly
   (see ruling 1). No L3 claim is made or implied; the module fails
   the criterion-12 family by design (supplied hypotheses, no
   revision machinery).
5. "Only three pairs." SUSTAINED as a scope limit; more pairs in
   H-EXP2.

No rhetoric overturns the measured result: 5/5 frozen bars passed,
red-team SURVIVES (bounded), zero regressions (no existing file
modified), no bar weakened. The verdict is ADOPT with the narrowed
classification and the two queued follow-ups.

## M2: Fork battery -- CONFIRM [NEW] (process confirmation)

Provenance probe (verbatim): What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited? The
battery execution is new this wave (fresh 67-entry run, new
batch_0821.sh with the 0521pdt archive and the run-start tip as LIVE
entries, evidence under ~/workspace/fb0821pdt/E/); driver, harness
instrument, fixture SHAs, and negative-control fixtures are
inherited frozen.

Ruling: CONFIRM as a process confirmation (toolchain and extraction
stability only). 67 named entries, 65 PASS, 0 FAIL, 2 UNTESTABLE
(rh-pull-1-head, rh-pull-2-head: non-TNN trees, twenty-two waves
running). Uniform pins (znc 498abcb5, probe 3b29aa06, 0 divergence).
The two setup anomalies (HARNESS path, entry-name collision) were
both caught by checks before any verdict and fully repaired; the
final tally rests on 67 per-entry RESULT.txt files each recording
its correct ref SHA. Scope stamp from FORK_BATTERY_0821.md stands.

## M3: tnn_chat FIT fresh re-run -- PASS [NEW]

Provenance probe (verbatim): What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited? The
re-run execution is new this wave (15 runs, fresh binaries, evidence
in fit/ and ~/workspace/tnn-fitchat-0821pdt/); all instruments,
fixtures, kb.txt, gaz.txt, R33 sources, and expected hashes are
inherited frozen.

Ruling: FRESH FIT PASS on d24eda8bd. KB1 30/30 specific declines
(26+4), 0 blanket refusals; KB2 17/17; KB5 10/10; binaries
byte-identical to frozen pins (1ada2fae, 20273a99); 9/9 rerun pairs
identical; 2/2 decline/baseline parity identical. Staleness resets
to 0 of 8. No new interactive entry points in the merge range.

## M4: Design lane -- H-EXP new; rest NULL/HELD

Provenance probe (verbatim): What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited? H-EXP is
new (see M1). All HELD statuses, stand-downs, rulings, and banked
questions are inherited and untouched.

Ruling: the design lane's new-mechanism output this wave is H-EXP
(adopted under M1 with narrowed classification). Sensory: NULL,
stand-downs hold. Intelligence trades: HELD. B1-class: NULL.
EXP2-K4/COMP2-P11/ruling 6: unchanged, HELD/banked.

## M5: Interactive survey -- NONE new

Provenance probe (verbatim): What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited? The survey
is new this wave over the fresh range d2fdf1225..d24eda8bd; all
surveyed files are inherited (morning research-lead commits,
read-only).

Ruling: no new runnable interactive TNN. The 17 new .zag files are
batch instruments with file-path args; src/ and units/ untouched.
The frozen probe instruments remain the only chat-capable
instruments, certified by M3.

## M6: Commit-order self-check -- VALID

Provenance probe (verbatim): What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited? The check
is new this wave over this wave's own commits; the commits are the
wave's new work.

Ruling: VALID. Prereg aed88c8f2 strictly precedes implementation
e2b6d5b04 and the build fix 3ae98a9c9; the transparent amendment
c06a23cfb precedes all implementation executions (first successful
run occurred after it); evidence 816fee7a7 and battery/FIT 7860c2694
follow. No candidate is UNVERIFIABLE ORDERING. Permanent caveat
travels: commit order evidences commit order only, never run order
and never content identity.

## M7: UNTOUCHED -- [VOID] items recorded

The six governance rulings, the H-C kill recommendation, EXP2-K4
redesign-or-retire, Q1, Q2, all sealed blind pairs, DP-1, the salt
dispositions, and Micah's frontier dirs remain untouched (frontier
dirs surveyed read-only only). NQ4 (F-LEAK repair) and NQ5
(single-pass copy patch/retire) require modifying his frontier
implementation files and are therefore banked to his queue, not
taken by this wave. No verdict is rendered on any of them.

No em-dashes used in this document.
