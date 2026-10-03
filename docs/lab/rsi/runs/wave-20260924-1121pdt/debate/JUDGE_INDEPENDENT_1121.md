# Independent judge rulings: wave-20260924-1121pdt debate

Judge: independent subagent (this document), repairing the coordinator's
self-rendered rulings in debate/JUDGE_RULINGS_1121.md. I reviewed the full
written record: ADVOCATE_BRIEF.md (advocate), redteam/REDTEAM_1121.md
(skeptic), the frozen preregs, candidates/cv1/ and candidates/g1/
evidence, and the process evidence under forks/, tnnchat/, hygiene/.
Every ruling below rests on cited evidence. Nothing is overturned on
rhetoric.

Hard lines held in these rulings: PURE ZAG ONLY and every other owner
red line are not narrowed; no frozen kill bar is moved after
implementation; Micah's five pending governance decisions (S7 strike,
MD-SSD-1, S11 pull, S11-AUD pull, C12 queue) are untouched and are not
mine to decide; nothing in these rulings adds to or removes from his
judge queue.

## M1: CLAIM-VERIFY-1

Ruling: CONFIRM ADOPT [NEW], with the coordinator's corrections
confirmed and one correction added.

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the artifacts are Zag sources and text transcripts; there are
no renders (RENDER_SHA n/a). Inherited and frozen: the decline-gate
source (a87011fe, wave 20260923-1121pdt), paths 1-4 byte-untouched,
the 38-fact KB (3ef27296), the frozen fixtures, the specific-decline
template. New this wave: the coverage-deliberated path-5 mechanism
(cv1_section.zag: F7 canonicalization, 54 stopwords, single-fact
coverage, lowest-index tie-break, fail-closed substring check), the
sealed 30-probe set and key authored by an independent agent after the
freeze, and the sealed transcripts. Nothing recycled; nothing
re-surfaced from the judge queue. The frozen commit order is now
satisfied in the committed record: 68c3bb868 (prereg freeze) strictly
precedes 5aec600dc (seal), which strictly precedes 1783234e0 (first
implementation commit), verified directly from the commit log. The
red team's "commit order pending" caveat is therefore resolved:
CV-B6's order component is SATISFIED, not pending.

Bar by bar, on cited numbers:

- CV-B1: 24/30 honest resolutions (paraphrase 10/10 with the key's
  expected facts verbatim, adversarial 13/14, gaming 1/6), with zero
  unflagged confabulations under the frozen definition (emitted
  answers only). 24 >= 24: PASS, exactly at the bar. The 6 misses are
  specificity misses counted by the key, which the red team
  re-graded and found applied consistently (A01, A10, A13, G02 PASS
  on extras; all 6 misses omit at least one listed word). The bar
  math blocks the degenerates (decline-everything caps at 20/30).
  Applying the bar as written is not weakening it.
- CV-B2: 17/17 in-KB turns byte-identical (e05fb4ec both engines),
  30/30 training probes specific declines: PASS. The disclosed
  conservative divergence (exact F7 matching declines some
  answerable inflected forms, e.g. "did marie curie discover
  radium?") is outside the 17-turn fixture's coverage, fail-closed,
  and disclosed; it does not trip CV-B2 as specified.
- CV-B3: 3/3 byte-identical reruns, no RNG: PASS.
- CV-B4: the prereg specifies the ratio on the sealed 30. The
  implementer's 1.80x used the training 30. The red team's
  independent sealed-30 measurement is 2.07x (baseline mean 649.167
  ops/turn, candidate mean 1344.3 ops/turn), which is <= 10x: PASS.
  The record carries 2.07x. Instrument disclosure traveling with the
  evidence: no F6 artifact exists in the repo, so a comparable
  counter was built post-hoc and disclosed; the red team verified
  gate_op stdout byte-identical to the frozen baseline on the sealed
  30 and the discipline not favoring the candidate.
- CV-B5: 0 blanket refusals; every decline names specific words in
  the frozen template: PASS.
- CV-B6: PROBES.md cf2f3293 and KEY.md 371cd282 match SEAL.md;
  separate author and implementer; implementer attested the sealed
  directory was never opened; grep finds no probe bytes in impl/
  ("martian" hits are KB fact 15, expected); commit order now
  verified as satisfied above: PASS.

All six bars pass as specified, so the frozen mapping yields ADOPT.
The strongest new capability is measured: 10/10 sealed paraphrase
probes answered with the key's expected KB facts verbatim, with no
probe-specific code paths (grep-clean, red-team verified).

Corrections ordered with the adoption:
(a) The wave record carries 2.07x (sealed-30) as the CV-B4 figure,
not 1.80x. (Confirmed; this is the coordinator's correction.)
(b) The A02 defect is genuine and travels with the adoption: the
decline template asserts "contains nothing about 'martian'" while
fact 15 covers "martian", a literally false decline the frozen
CV-B1 confabulation definition cannot see (it covers emitted answers
only). Next wave owes a narrowed follow-up: fix the decline-citation
rule (name payload words; never present a covered word as uncovered)
and re-test on a fresh sealed gaming set.
(c) The conservative divergence is a real capability cost outside
CV-B2's fixture coverage; the follow-up measures it.
(d) Adoption scope: the candidate implementation and its evidence
are committed in the run dir; the live dialogue gate is NOT swapped
by this verdict (integration needs its own prereg).
(e) New in this ruling: the record carries the definitional blind
spot as a traveled defect. Future preregs must extend the
confabulation definition to decline-template claims. This does not
move any frozen bar this wave; the bars were applied as written.

## M2: G1 SUNSHAFTS

Ruling: CONFIRM DISCARD [NEW]. OVERTURN the "not a
candidate-mechanism failure" half-framing in VERDICT_G1.md; the
verdict itself stands.

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the variant BMPs were first rendered this wave (N=12
sha256 9f23b64c, also N=6 61371fe4 and N=24 87e1c437;
FIRST_RENDERED_WAVE wave-20260924-1121pdt). The baseline BMP
reproduces the S14 record (e4f65557) byte-identical. Inherited: the
r8c substrate and all nine pending queue items, named as
QUEUED-UNJUDGED and untouched. New: the G1 pass machinery. No
recycled render is surfaced as new; no sealed pair was prepared.

The frozen mapping sends any failed or unevaluable bar to DISCARD.
The verifier's own evidence shows WEDGE kept 11 of 48 (needs 36),
OFFWEDGE kept 28 of 48 (needs 36), RADCUT 10 readable of 24 (needs
16), TERRAIN PASS 64 of 64. KB2, KB3, KB5, KB7 are therefore
UNEVALUATED as frozen: DISCARD is the correct application, and
reinterpreting the bars around the defective point sets would be
moving kill bars after implementation.

The framing correction: the skeptic's full-sky analysis shows the
frozen T-gate (L=max(0,T-400)*90/624 against a field mean
transmittance of ~511) lifts 97.14 percent of sky pixels (mean dL
+33.07); INFO KB5 is 56.28 against the 6.0 bar. So even with
geometrically valid point sets, the frozen mechanism constants would
have failed KB5 decisively. The accurate record is: prereg-spec
defect in the verifier point sets AND a mechanism-calibration miss in
the frozen T-gate. VERDICT_G1.md's "not a candidate-mechanism
failure" is corrected to this dual framing. The verdict does not
change.

No sealed pair was prepared (correct: on DISCARD, preparing one
would risk presenting a washed render as a judge candidate), and
nothing reaches Micah's judge queue from G1. A next-wave re-freeze
with geometrically validated point sets and a recalibrated T-gate is
legitimate new work (fresh prereg required); the concept is not dead.

## M3: the two STAND-DOWN memos

Ruling: CONFIRM. Both STAND-DOWNs were correct; the pinned 7/38
(1842 bp) baseline stands.

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: no new artifacts. Both are NO-GO memos built on committed
evidence (the 0521pdt decisions record, the 2021pdt decisions log
recount) plus deterministic Zag recounts on HEAD. Nothing new is
claimed; the memos report distributions.

- M4 R2 T2-veto reopen: the arithmetic precondition is satisfied
  (residual falses exist in T2), but the reopen is blocked by
  closure collision. The deterministic recount reproduces the
  committed 0521pdt decisions log sha-identical (5081b621): 7/7
  residual falses in T2 colorconst, fixtures p000 p002 p006 p008
  p010 p016 p018. This is Micah's closed front (FS-F2C FINAL ALIVE
  98.58 percent; the loop retired colorconst). The one permitted
  reopen requires no collision with his closed work; the collision is
  documented, so the reopen closes. Stand-down correct.
- KB4 tail: the independent 2021pdt recount agrees verbatim (7
  falses, all in T2 colorconst, same fixtures); every other task
  holds 0 residual falses; every mechanism lane is closed (vote
  aggregation under M4/S4, veto-over-zero arithmetically dead at
  0521pdt, tainted Goertzel lineage off-target and void, denominator
  gaming not a free lunch) or owned elsewhere (T2 veto, this memo's
  sibling). Stand-down correct.

Note: the two logs record different denominators (7/37 = 1891 bp in
the 0521pdt candidate-arm recount; 7/38 = 1842 bp pinned from the
2021pdt decisions log). Both agree on the only material fact: all 7
falses sit in T2 colorconst. The denominator difference is immaterial
to the ruling.

## M4: process FIT

Ruling: CONFIRM. Fork battery 18/18 PASS; tnn_chat FIT; hygiene
dispositions correct.

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the fork battery evidence and FIT evidence are new this
wave, produced with the pinned znc (498abcb5) on HEAD; the harness
(fork_battery.zag, 507 lines, f38d9154) is inherited read-only from
the 2321pdt archive. Nothing recycled.

- Fork battery: 18/18 PASS. 11 forks from the worker enumeration
  (local tnn-native-lab at 42e24b381, three wave archives,
  wave-debate-session-1-backup, origin/tnn-native-lab, fs-gr1, main,
  r2-7, reorg/phase-0-1, wg-freeze): znc byte-identical to pinned
  498abcb5 on every fork; shell battery and pure-Zag harness agree
  on every fork. Plus the 7 forktest detached worktrees the worker
  wrongly recorded ABSENT: the coordinator ran the frozen battery
  read-only against each, 7/7 PASS (znc byte-identical everywhere).
  The pure-Zag harness was not rerun on those 7 (disclosed); the
  frozen shell battery is the instrument of record for them. The
  ABSENT row is superseded by the addendum.
- tnn_chat FIT on HEAD: 2/2 builds byte-identical (1ada2fae,
  20273a99), 30/30 specific declines, 17/17 in-KB with baseline
  parity, 10/10 KB5, 9/9 rerun pairs byte-identical, with the
  standing caveats (38-fact closed-book instrument, not a general
  interactive TNN). FIT.
- Hygiene: the orphaned sha annotated as unverifiable, the R33
  duplicate removed (byte-identical e6379ddb), the unique baselines
  void-labeled. The znc mode drift (100644 to 100755, bytes
  identical) is recorded.

No corrections ordered; the caveats above are already disclosed in
the record.

## M5: Python-accident disposition

Ruling: CONFIRM. The NO-GO memo stands; no standing-rule change.
This disposition is consistent with the 0521pdt Python-anywhere rule,
and it does not narrow any owner red line.

Skeptic's provenance probe: What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?

Answer: the artifact is the KB4 NO-GO memo, authored via the
file-write tool. The accidental python3 -c printed "skip", touched no
artifact, and the phase produced no run evidence (prereg-only).

The Python-anywhere rule voids wave evidence on Python contact. The
voiding operation must have an object: it voids the evidence the
contact touched or could have contaminated. Here the contact touched
nothing (no artifact, no run evidence; the memo was written by the
file-write tool, not by Python), so there is no wave evidence from
that phase to void. This is the same application of the rule as the
MD-SSD-1 precedent for the identical accident, and the same
distinction the record already draws: where Python contact did touch
an evidence chain (part C Goertzel scratch), the design lineage was
voided; where it touched nothing, nothing is voided. If the phase
had produced run evidence, that evidence would be void. The rule
still voids any wave evidence on contact; the ruling does not narrow
it.

The disclosure is recorded in the wave record. No new standing rules
are adopted by this debate.

## Verdict slate

| Motion | Ruling | Deciding number |
|---|---|---|
| M1 CLAIM-VERIFY-1 | CONFIRM ADOPT [NEW] (corrections (a)-(e) ordered; run-dir scope, live gate NOT swapped) | 24/30, 0 confabulations; cost 2.07x sealed-30 |
| M2 G1 SUNSHAFTS | CONFIRM DISCARD [NEW]; OVERTURN the "not a candidate-mechanism failure" half-framing (dual defect: point sets AND T-gate calibration) | KB5 would-be 56.28 vs 6.0; 97.14% sky lifted, mean dL +33.07 |
| M3 M4 R2 reopen / KB4 tail | CONFIRM STAND-DOWN (both correct) | 7/7 falses in Micah's closed T2 colorconst |
| M4 Fork battery / FIT / hygiene | CONFIRM FIT (process confirmation) | 18/18 forks PASS; FIT numbers as recorded |
| M5 Python accident | CONFIRM memo stands; no rule change; consistent with Python-anywhere rule | 0 artifacts touched, 0 run evidence in phase |

Nothing is added to Micah's judge queue this wave: G1 prepared no
sealed pair (correctly), and CV-1 is a dialogue-substrate adoption in
the run dir, not an image candidate. His five pending governance
decisions are untouched.
