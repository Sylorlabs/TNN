# Skeptic report: wave-20260926-1721pdt (four motions, argue AGAINST)

Role: skeptic. The skeptic's job is to find gaming, confounds, weak
bars, and coverage gaps. A transcript lacking the provenance probe is
incomplete and its certifications void.

## The provenance probe

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer from this wave's evidence files:

- Fork battery harness: pure-Zag fork_battery.zag inherited from the
  2321pdt wave archive (sha
  f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738),
  rebuilt binary byte-identical to prior waves (sha
  a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).
  The znc pin (498abcb5...), probe pin (3b29aa06...), and B2 bin pin
  (75b85d3c...) are all inherited across waves. Nothing in the
  instrument chain is new.
- Of the 39 named entries, 35 test fixture SHAs unchanged since
  1421pdt or earlier. The 3 unique live commits are: the task-pinned
  merge 45d449a56 (inherits the 1421pdt archive state a222f8f178 as one
  parent and his origin commits, treated as CLOSED, as the other),
  a222f8f178 (the newly enumerated pre-merge 1421pdt archive state),
  and 39bf8d5d4 (his origin tip commit, CLOSED, tested only for
  toolchain stability). The genuinely new named entry this wave is one:
  arch-wave-0926-1421 at a222f8f178, which is last wave's archive
  state, so even the "new" entry is inherited content renamed.
- Interactive instruments: baseline probe, decline-gate probe, pinned
  znc, and tnn_chat frozen sources are all inherited. Their shas are
  re-certified, not new. No probe chat was executed this wave.
- Lane survey: the prereg inventory is unchanged since wave-20260925;
  the newest material in the window is the committed 1421pdt evidence
  batch. The DP-1 sealed pair was repaired under P18 in 1421pdt and is
  carried forward [RE-CERT], not re-judged here.
- His six governance rulings: open, untouched, decided by no one here.

Verdict of the probe: everything under judgment this wave is inherited
and re-certified. Nothing is [NEW]. The wave is a stand-down wave by
design, so the question is whether the re-certifications are honest and
whether the inherited bars are strong enough to lean on.

## M1 attacks: Fork battery CONFIRM

1. The verdict line certifies more than the evidence holds. The scope
stamp says the battery certifies "toolchain and extraction stability
only, not the contents of the merged commits." A CONFIRM verdict
read by anyone downstream will be heard as "the forks are fine," when
the battery explicitly refuses to look at contents. The strongest
honest verdict line is CONFIRM of toolchain stability, not of the
forks.

2. Coverage shrank on exactly the wave that matters. 39 entries / 4
live / 3 unique live commits versus 1421pdt's 40 / 6 / 5. The advocate
names an explanation, but notice its shape: the 1421pdt queued pickups
became ancestors of the merged tip, which is why the tip's own entry
now stands in for them. The merged tip carries his two newest frontier
commits (39bf8d5d4 upscale, c094d7770 concept probe), tested only for
toolchain stability. The battery's live set is shrinking while the
merged content grows. That asymmetry is worth naming as a trend, not
just a one-wave accounting entry.

3. Five straight waves of the same two extraction FAILs (pull/1 at
5802fec8, pull/2 at 4b76bb59) is a standing hole in exactly the newest
unexplored refs on origin. Calling it an "instrument limit" is honest,
but it is a limit that has not been fixed for five waves. The refs it
covers are pull heads: the most likely place new content would first
appear. The battery is systematically blind at the one place it would
matter most.

4. Named-entry counts are inflated by design. 39 named entries cover 31
unique commits; 8 are named duplicates (rh tip duplicates rt; three
entries share 9914322267; two share 3947dca1a; two share f875b34179;
four share bd30978748). P8 names them, which is honest, but the
headline "39 entries, 37 PASS" reads as breadth the unique-commit
count (31) does not support.

5. 35 of 39 entries are fixtures: SHA-stable repeats whose verdicts
rest on determinism per P12, not on re-execution risk. Only 4 entries
are live, and of the 3 unique live commits, two are the merged tip and
its pre-merge parent. The battery is overwhelmingly a determinism
self-check.

6. The spot re-run validates the fixed parser, but it retroactively
raises a question about 1421pdt: the 1421pdt verdicts were cited for a
full wave while parsed with the buggy cut -d= -f2 extraction. This
wave confirms the corrected verdicts match, but the skeptic notes the
1421pdt certifications rested on mis-parsed output for their whole
lifetime. The fix is real; the historical exposure was also real.

## M2 attacks: Interactive TNN CONFIRM

1. The manifest gap is a records defect, but it is a records defect in
the authority chain. The pins live in fit_authority/README.md: prose
documentation, editable without any integrity anchor. "Stable across
waves" is inherited trust in prior verifiers, not a fresh chain of
authority. If README.md were silently edited, the wave's sha256 checks
would verify against attacker-chosen values and still print YES. The
confirmation basis is honest disclosure, not cryptographic authority.

2. The negative grep has blind spots. The scan covers chat, repl, and
interactive names plus five entry-point signatures (fn main, stdin,
readline, interactive_loop, repl_loop). An interactive surface named
"console," "session," "loop," "assistant," "talk," or "dialogue"
escapes the name filter. The added-file scan only filtered on
chat|repl|interactive. The advocate's best answer is that the wave
delta added zero files under src/ or units/ at all, which does close
the hole for this wave, but the survey method itself remains
name-dependent and would not survive a wave that adds files.

3. No probe chat has been executed recently, and none was run this
wave. The standing rule ("run only on change") is reasonable, but it
means the claim "no interactive TNN exists" rests entirely on static
analysis: grep patterns and diff stats. A behavioral entry point (e.g.
an interactive mode reachable through existing CLI flags) would not be
found by any step in this survey. The rule self-protects: it only
triggers on the kind of change the survey is designed to find.

4. The wave delta includes his two upscale commits adding .zag probe
sources (src/uprobe.zag, src/azprobe.zag) under docs/lab/. They are
declared CLOSED and not re-litigated, which is correct per his
authority, but the survey's headline finding (no interactive surface)
therefore rests on a convention that the newest .zag probe sources in
the merge were not inspected as interactive candidates. The convention
is his, so it stands, but the finding's scope should name it.

## M3 attacks: Stand-down CONFIRM

1. The bar is absence of evidence, and absence is doing the heavy
lifting. The five signals are: one committed batch (the 1421pdt
evidence, process material), zero name-status hits, an unchanged
inventory, no on-disk drafts, and 27 untracked entries judged by path
to be residue. The weakest link is the 27 untracked entries:
"build artifacts and frame/binary residue from older waves" is a
classification by directory name (dvid1v2/frames_v2/,
intel_trade/impl/, freelunch/bin/), not a content inspection. A prereg
draft or candidate file could sit inside any of them under an odd name
and the name-status grep over the window would not catch it (grep was
on committed name-status, not on disk contents).

2. Stacking precedents risks laundering. The motion leans on P17
(vacuous labeling, lane-survey precedent) from last wave, P18 (sealed
blind) from last wave, P11 and P9 from older waves. Each precedent is
sound in its own minting, but a stand-down built entirely on inherited
rulings inherits all their unexamined assumptions. The skeptic notes
the chain, not to break it, but so the judge does not CONFIRM by
precedent reflex.

3. DP-1 is in a quiet limbo. The pair is repaired under P18 and tagged
queue-HELD, and presentation to his ears is a "future-wave queue
decision." That future wave has not been named. A HELD item with no
scheduled decision is effectively parked. The motion does not relitigate
this, correctly, but the queue decision should not drift indefinitely.

4. The motion's cleanest load-bearing pillar is actually his authority,
not the survey: CV-P and COMP-2 are barred by his open governance
rulings, not by lane evidence. The stand-down is CONFIRM-worthy only
if the verdict line says so plainly and does not imply the lanes are
scientifically dead. They are procedurally held, pending his rulings.

## M4 attacks: Prereg commit-order self-check

1. A vacuous check on a wave with no candidates is a null result
wearing a verdict's clothes. P17 says to label it vacuous rather than
pass, which is honest, but the skeptic asks the standing question:
does a designed stand-down wave need a VACUOUS motion at all? The
answer per the mandate is yes (the debate is mandatory, the motion
list is fixed), but the record should show the motion added zero
information this wave.

2. No gaming is alleged. There is nothing to order-check, and nothing
was checked. That is the whole report for M4.

## Skeptic's bottom line

Nothing under judgment is [NEW]; everything is [RE-CERT] of inherited
artifacts or [VACUOUS]. The evidence is real and the numbers are
uniform, but the instruments certify narrow scopes (toolchain, not
contents; static names, not behavior; committed names, not disk
contents), the battery's live coverage is shrinking while merged
content grows, five waves have passed with the pull-head hole unfilled,
and the confirmation basis for frozen instruments is disclosed prose,
not an integrity-anchored manifest. None of this sinks a CONFIRM on a
stand-down wave, but it all belongs written into the verdict lines.
