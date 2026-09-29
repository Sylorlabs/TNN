# ADVOCATE: wave-20260928-1721pdt debate

Role: argue FOR each motion on the verdict slate, with evidence cited.
The skeptic's provenance probe is acknowledged in every motion verbatim:
"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

## M1: Fork battery CONFIRM [NEW] as process confirmation only

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The 1421pdt fork battery ran a full fresh execution at pin
547b2132c0435b11e51099ae8a598e5547095f52 and the coordinator this wave
re-verified its files line by line: 59 evidence dirs, 59 verdict lines
summing to 57 PASS plus 2 UNTESTABLE, the two UNTESTABLEs being the
expected rh-pull-1-head (5802fec8) and rh-pull-2-head (4b76bb59) with
the standing cause (pinned toolchain path absent, git show exit 128).
The run-start pin equals the current tip exactly (git rev-parse HEAD
returns 547b2132c0435b11e51099ae8a598e5547095f52; git status shows no
tracked-file changes since the battery ran), so this battery certifies
the current tip directly, with no pin gap to bridge. The summary
records a uniform znc pin 498abcb5, a pure-Zag harness byte-identical
to the frozen instrument (binary sha256 a2e6284c), B1/B2/B3 passing,
negative controls discriminating on all 57 tested forks (neg1_ok
57/57, neg2_ok 57/57), R32_ZNC_PROBE_OK on all 57, and the 1721pdt
probe-loss FAIL staying closed (repair 37d1d3cab is an ancestor of the
pin). This is a process confirmation only: toolchain and extraction
stability, never the contents of the tested commits. The evidence was
produced by the dead 1421pdt worker, but it is machine-checkable and
this wave checked it; the verdict becomes debated this wave.

## M2: H-C kill governance audit CONFIRMED-ON-RECORD [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The audit is tight, read-only, and scoped to git archaeology. On the
committed record, the K-HC4 applied at the salt commit 57d055bbb
("minimum capability includes swap-first-last", FIRES, kills H-C) is
not the K-HC4 frozen 81 minutes earlier at a95e0d50c ("learn the D1
six", PASS with D1/D2 deviations). The defining phrase first appears
in the tree at the salt commit itself (pickaxe returns only
57d055bbb), and K-HC5, K-HC6, K-HC7 have no freeze commit anywhere in
the combiner_arch record. The caveat is stated honestly: the cited
HYPOTHESIS.md is absent from the tree, so a never-committed document
cannot be excluded, but on evidence in the tree the change is
confirmed. The finding is CONFIRMED-ON-RECORD with the recommendation
banked to Micah (strike the kill or re-run H-C under the original
frozen bar). The loop documents the change and moves on; it does not
weaken any bar, it does not alter his verdict, it decides nothing.

## M3: Design lane NULLs and HELDs [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

HUNT_1421.md is methodical: survey range 81f0cfe12..547b2132c, exactly
1 commit in range (loop-owned 547b2132c), 4 files changed, all loop
records, zero origin commits, 0 new mechanism text in
docs/lab/invention/, 0 added .zag files. The verdicts follow the
evidence: EXP2-K4 HELD (expiry question banked to Micah at 2321pdt,
re-confirmed at 0221pdt, not re-asked, no new blocker evidence);
B1-class mechanism NULL (0 mechanism hits; P9 stays a re-freeze
template; the prior DISCARD stands); COMP2-P11 HELD (ruling 6 still
OPEN; tree-wide grep finds no new ruling-6 text); intelligence trades
HELD (no genuinely new expensive capability with a real mechanism; no
knob proposed, and an expensive knob without a capability would be
manufacturing); sensory NULL (standing stand-downs hold: G1, D-VID-1,
ST-1 dead; E3 rejected by Micah in blind A/B). The nothing-manufactured
statement is present. Nothing was invented to fill the wave.

## M4: Interactive survey NONE [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

INTERACTIVE_SURVEY_1421.md surveyed the same merge range with a file
sweep: 4 added files, all 1421pdt-anchored survey records and an
ls-remote listing, none containing interactive entry-point code and
none referencing a new chat/REPL/stdin-loop instrument; 0 added .zag
files outside prior records. Verdict: NONE loop-owned. The frozen
batch probes (fit_authority/tnn_chat.zag, tnn_chat_decline.zag) remain
the only loop-owned chat instruments, batch-only, and tnn_chat FIT
staleness is kept visible. Read-only throughout; Micah's frontier
REPLs untouched.

## M5: EXP1c attempt-5 stand-down honored [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The 0221pdt judge banked two explicit questions to Micah (Q1
exploration/exploitation redesign as a new design direction; Q2 K7-bar
attainability or re-specification) and ruled no attempt-5 retune until
he rules. The commit record honors it: zero EXP1c commits, zero
experiment dirs, zero retune or re-run in the survey range. The two
questions stay banked and are not re-asked here; re-asking would be
prosecution by repetition. Stand-down honored.

## M6: Commit-order self-check VALID, VACUOUS for adoption [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

This wave's candidate set is empty: zero adoptions, zero preregs, zero
implementation commits. The check fires on an empty set and is VALID
and VACUOUS. The 1421pdt lane files are uncommitted evidence carried
forward, not adoptions; they gate nothing. Nothing this wave changes
the standing caveat: commit order evidences commit order only, never
run order and never content identity.

## M7: tnn_chat FIT staleness 3 of 8 [NEW]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The last fresh FIT re-run was at 2021pdt, where staleness reset to 0
of 8. The 0829pdt debate recorded staleness 2 of 8 (confirmed by that
wave's judge, and it stands as recorded). This wave is the next
verdict-bearing wave, so staleness advances to 3 of 8: not re-run, not
due (due at 8 of 8). The intervening commits are docs-only loop
records, so no regression path exists for the FIT to miss. The 8-wave
cadence is a standing rule the loop may not unilaterally change;
re-running early would burn znc build cycles for no verdict value.

## M8: UNTOUCHED [VOID]

Provenance probe (verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The six governance rulings (S7 strike, MD-SSD-1, S11 pull, S11-AUD
pull, C12 queue, Python-mirror logic) remain OPEN; every sealed blind
pair (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14,
whirlpool-planform) untouched; DP-1 presentation remains the parent
agent's queue decision; Micah's frontier dirs untouched beyond
read-only survey. This wave neither decided, relitigated, nor
re-presented any of them. VOID is the only honest verdict for items
the loop must not touch.
