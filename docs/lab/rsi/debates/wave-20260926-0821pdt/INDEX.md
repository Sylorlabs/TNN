# Debate index: wave-20260926-0821pdt

Debate group transcript for TNN RSI loop wave wave-20260926-0821pdt
(working copy ~/workspace/tnn-rsi, branch tnn-native-lab, HEAD
4328a8350d987a65c4e86e4973dbe45c9d5f6cd5). Written in three genuine
phases: advocate first, then skeptic, then judge. All four files are
left untracked for the wave coordinator to commit. No em-dashes in any
file (grep-verified). Zero Python used by the debate group.

## Files

- ADVOCATE_BRIEF.md: steelman FOR each draft verdict, numbers cited
  from FORK_RESULTS_0821.md, FIT_0821.md, INTERACTIVE_0821.md.
- SKEPTIC_REPORT.md: adversarial attack on each draft verdict
  (gaming, confounds, weak bars, cost, incident handling). The verbatim
  provenance probe ("What is the provenance of the artifacts under
  judgment, and what exactly is new versus inherited?") appears once
  per item (4 occurrences, grep-verified).
- JUDGE_RULINGS.md: reasoned CONFIRM / MODIFY / OVERTURN per item with
  numbers cited; explicit rulings on both incidents; new precedents
  P14, P15, P16, P17; P1/P8 verdict-line wording requirements kept.
- INDEX.md: this file.

## Draft slate (coordinator)

1. Fork battery: draft CONFIRM [RE-CERT]. 36 named entries, 34 PASS, 2
   extraction FAILs (pull/1/head 5802fec8, pull/2/head 4b76bb59f).
2. tnn_chat FIT: draft CONFIRM [RE-CERT] on 4328a8350 without a fresh
   re-run (per P12).
3. Interactive TNN: draft CONFIRM [RE-CERT], EXISTS for supervised
   red-team probe chats only; availability only, no probe chat run.
4. No new candidates this wave, by deliberate coordinator choice; all
   lanes stood down or gated; prereg commit-order self-check vacuous.

## Final ruled verdicts (judge)

1. Fork battery: MODIFIED. CONFIRM [RE-CERT] stands; verdict line
   reworded to carry the /tmp incident as a load-bearing caveat (P14),
   the single-live-commit and duplicate caveats, and the corrected
   attestation. Incidents ruled: /tmp-full incident does not undermine
   the 34/34 PASS (compromised artifacts discarded before judgment,
   both entries re-run from scratch via read-only git show, final
   verdicts rest on intact post-rerun artifacts with matched shas);
   the accidental no-op python3 -c is a disclosed contact per P13 and
   the COMP-2 distinction, not a breach, with the P15 attestation
   correction going forward.
2. tnn_chat FIT: CONFIRMED [RE-CERT] on 4328a8350d without a fresh
   re-run. P12 applies on its simplest facts (doc-only changes plus a
   zero chain-path diff). New precedent P16: determinism-by-citation
   must name the last fresh re-run wave (wave-20260925-1421pdt) and the
   citation path in the verdict line. Directive: relocate the
   KB1/KB2/KB5 fixtures out of the pruneable prior-wave scratch path.
3. Interactive TNN: CONFIRMED [RE-CERT], EXISTS for supervised
   red-team probe chats only. Negative finding kept first (zero
   source-level entry points on this tip); confabulation caveat must
   survive every future rewording. Standing observation: record why no
   supervised probe chat was scheduled, or schedule one.
4. No new candidates: CONFIRMED. The stand-down is disciplined while
   Micah's six governance rulings gate adoption. New precedent P17:
   future "no new candidates" verdicts must cite the lane survey
   record; vacuous self-checks must be labeled vacuous.

No verdict was overturned.

## New precedents

- P14: integrity-incident protocol (discard and re-run from source;
  re-verify pin shas post-incident; re-take flaky-window sha readings;
  incident travels as a load-bearing verdict-line caveat).
- P15: Python-contact attestation (exact command, placement, and
  no-contact showing disclosed; attestation reads "zero Python touched
  wave artifacts" when a contact is disclosed; no-contact invocation
  remains a disclosed contact, not a breach, under P13).
- P16: FIT determinism-by-citation must name the last fresh re-run
  wave and the citation path in the verdict line.
- P17: "No new candidates" verdicts must cite the lane survey record;
  vacuous self-checks labeled vacuous.

## Untouched by this debate

Micah's six pending governance rulings and his sealed blind A/B
verdicts remain his to make; none were decided here.
