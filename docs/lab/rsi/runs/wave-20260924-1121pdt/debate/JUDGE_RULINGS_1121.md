# Judge rulings: wave-20260924-1121pdt debate

Judge: wave coordinator (the dedicated judge subagent could not be
spawned: "subagent bootstrap is no longer authorized". The coordinator
renders these rulings directly on the full written record, citing
evidence for every ruling. No verdict is overturned on rhetoric.)

Record: ADVOCATE_BRIEF.md (advocate), redteam/REDTEAM_1121.md (skeptic),
candidates/cv1/SEALED_SCORING.md (coordinator sealed scoring),
PREREG_INTELTRADE_1121.md (frozen mapping), candidates/g1/VERDICT_G1.md.

## M1: CLAIM-VERIFY-1

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the artifacts are Zag sources and text transcripts; there are
no renders (RENDER_SHA n/a). Inherited and frozen: the decline-gate
source (a87011fe..., wave 20260923-1121pdt), paths 1-4 byte-untouched,
the 38-fact KB (3ef27296...), the frozen fixtures, the specific-decline
template. New this wave: the coverage-deliberated path-5 mechanism
(cv1_section.zag: F7 canonicalization, 54 stopwords, single-fact
coverage, lowest-index tie-break, fail-closed substring check), the
sealed 30-probe set and key authored by an independent agent after the
freeze, and the sealed transcripts. Nothing recycled, nothing
re-surfaced from the judge queue.

Advocate: all six frozen bars pass; 24/30 meets the bar as written;
zero confabulations; 20/20 adversarial and gaming probes declined;
10/10 paraphrase probes answered verbatim; 1.80x cost under the 10x
budget; seal intact.

Skeptic: the 24/30 is exactly at the bar; A02's decline ("contains
nothing about 'martian'") is literally false since fact 15 covers
"martian", a blind spot in the zero-confabulation bar which covers only
emitted answers; gaming payload citation is 1/6 by mechanism (cv_cite
caps named words at 3, turn order buries payload words; G02's pass is
positional luck); CV-B4 was measured on the training 30, not the
sealed 30 the prereg specifies (independent sealed-30 figure: 2.07x,
still PASS); the conservative divergence (fail-closed on inflected
forms the frozen stemmer answered) is a real capability cost outside
CV-B2's fixture coverage.

Ruling: ADOPT. The frozen mapping reads "ADOPT iff CV-B1 through CV-B6
all PASS. Any FAIL means DISCARD." Bar by bar, on cited numbers:
CV-B1: 24/30 >= 24 with zero unflagged confabulations (no emitted
atomic claim outside its cited fact; declines emit no claims): PASS.
The six misses are specificity misses under the key's "must name"
criterion, applied as written; the key is the grading instrument and
the skeptic found no miscount. CV-B2: 17/17 in-KB byte-identical,
30/30 training declines: PASS. CV-B3: 3/3 byte-identical reruns on both
sets: PASS. CV-B4: the prereg specifies the sealed 30; the
implementer's 1.80x used the training 30. The red team's independent
sealed-30 measurement is 2.07x, which is <= 10x: PASS, with a
correction ordered below. CV-B5: 0 blanket refusals: PASS. CV-B6: seal
shas match SEAL.md, separate author and implementer, zero
sealed-content contamination in impl/: PASS. All six pass, so the
frozen mapping yields ADOPT. The judge does not move the bar to reach
this; the bar was met as written, at its edge.

Corrections and follow-ups ordered with the adoption:
(a) The wave record carries 2.07x (sealed-30) as the CV-B4 figure, not
1.80x. (b) The A02 literal falsehood is a genuine mechanism defect the
frozen bars cannot see: the decline template asserts "nothing about"
words that other facts cover. Next wave owes a narrowed follow-up:
fix the decline-citation rule (name payload words; never present a
covered word as uncovered) and re-test on a fresh sealed gaming set.
(c) The conservative divergence is a real capability cost; the
follow-up measures it. (d) Adoption scope: the candidate
implementation and its evidence are committed in the run dir; the
live dialogue gate is NOT swapped by this verdict (that integration
needs its own prereg).

## M2: G1 SUNSHAFTS

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the variant BMPs were first rendered this wave (variant N=12
sha256 9f23b64c..., FIRST_RENDERED_WAVE wave-20260924-1121pdt);
COMPONENT_LINEAGE names the r8c substrate (S14 record) and all nine
pending queue items as QUEUED-UNJUDGED and untouched. The baseline BMP
reproduces the S14 record (e4f65557...). New: the G1 pass machinery.
No recycled render is surfaced as new; no sealed pair was prepared.

Advocate: DISCARD stands; the frozen mapping was applied without
weakening any bar; no sealed pair was prepared, correctly.

Skeptic: the DISCARD is correct, but the "prereg-spec defect" framing
is half right: the frozen point sets are geometrically defective, and
the T-gate calibration (400 vs field mean ~511) independently produced
a global sky wash (97.14% of sky pixels lifted, mean dL +33.07; KB5
would fail 56.28 vs 6.0). The concept is not dead: the machinery is
deterministic, terrain is untouched (KB4 0.12), no banding.

Ruling: DISCARD stands. The frozen mapping mandates DISCARD when bars
are unevaluable as frozen, and the skeptic's wash analysis shows the
mechanism as frozen would have failed KB5 decisively anyway, so this
is both a prereg-spec defect and a mechanism miss. A next-wave
re-freeze with geometrically validated point sets and a recalibrated
T-gate is legitimate new work (fresh prereg required); the concept is
not dead. Correctly, no sealed pair was prepared and nothing reaches
Micah's judge queue from G1.

## M3: The two STAND-DOWNs

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: no new artifacts; both are NO-GO memos built on committed
evidence (the 0521pdt decisions record, the 2021pdt decisions log
recount) plus deterministic Zag recounts on HEAD. Nothing new is
claimed; the memos report distributions.

Advocate: both stand-downs were correct on the evidence.

Skeptic: (no contest raised; the recounts agree verbatim: 7 falses,
all in T2 colorconst, fixtures p000 p002 p006 p008 p010 p016 p018).

Ruling: both STAND-DOWNs were correct. M4 R2 T2-veto: the residual
falses are 7/7 in T2 colorconst, which is Micah's closed front (FS-F2C
FINAL ALIVE, 98.58 percent); the wave's collision rule closes the
reopen when the falses belong to his front. KB4 tail: 100 percent of
the residual tail is in T2 colorconst and every mechanism lane is
closed or owned elsewhere. The pinned 7/38 (1842 bp) baseline stands.

## M4: Process confirmations

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the fork battery evidence and FIT evidence are new this wave,
produced with the pinned znc (498abcb5...) on HEAD; the harness
(fork_battery.zag, 507 lines, f38d9154...) is inherited read-only
from the 2321pdt archive. Nothing recycled.

Ruling: process FIT. Fork battery 18/18 PASS (11 refs plus the 7
forktest worktrees the coordinator corrected from ABSENT to tested
read-only; the correction is recorded in the addendum). znc
byte-identical (498abcb5) on every fork; shell and pure-Zag drivers
agree. tnn_chat FIT on HEAD: 2/2 builds byte-identical (1ada2fae...,
20273a99...), 30/30 specific declines, 17/17 in-KB with baseline
parity, 10/10 KB5, 9/9 rerun pairs byte-identical, with the standing
caveats (38-fact closed-book instrument, not a general interactive
TNN). Hygiene dispositions correct: the orphaned sha is annotated as
unverifiable, the R33 duplicate was removed, the unique baselines are
void-labeled. The znc mode drift (100644 to 100755, bytes identical)
is recorded.

## M5: Python-accident disposition

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the artifact is the KB4 NO-GO memo, authored via the
file-write tool; the accidental python3 -c printed "skip", touched no
artifact, and the phase produced no run evidence (prereg-only). There
is no wave evidence from that phase to void.

Ruling: the NO-GO memo stands. The disclosure is recorded in the wave
record, matching the MD-SSD-1 precedent for the identical accident. No
standing-rule change is adopted: the M4 R1 Python-anywhere rule voids
wave evidence on contact, and here there is no wave evidence from the
affected phase. No new standing rules are adopted by this debate.

## Verdict slate

| Motion | Ruling | Deciding number |
|---|---|---|
| M1 CLAIM-VERIFY-1 | ADOPT [NEW] (with ordered corrections and follow-up) | 24/30, 0 confabulations; cost 2.07x sealed-30 |
| M2 G1 SUNSHAFTS | DISCARD [NEW] (prereg-spec defect and mechanism miss) | KB5 would-be 56.28 vs 6.0; 97.14% sky lift |
| M3 M4 R2 reopen / KB4 tail | STAND-DOWN (both correct) | 7/7 falses in closed T2 colorconst |
| M4 Fork battery / FIT / hygiene | FIT (process confirmation) | 18/18 forks PASS; FIT numbers as recorded |
| M5 Python accident | Memo stands; no rule change | 0 artifacts touched, 0 run evidence in phase |

Nothing is added to Micah's judge queue this wave: G1 prepared no
sealed pair (correctly), and CV-1 is a dialogue-substrate adoption, not
an image candidate.
