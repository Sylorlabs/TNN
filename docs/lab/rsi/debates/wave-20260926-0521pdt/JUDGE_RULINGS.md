# Judge rulings: wave-20260926-0521pdt

The judge renders a reasoned ruling per item with numbers cited. An
overturn would require cited evidence, never rhetoric; none is issued
here. The skeptic's verbatim provenance probe appears once per item in
SKEPTIC_REPORT.md (5 occurrences, verified). Zero em-dashes in any
debate file (verified by grep before writing this ruling). Micah's six
pending governance rulings and his sealed blind A/B verdicts are his to
make; this debate records them as untouched and decides none of them.

## Item 1. Fork battery 0521pdt: MODIFIED (verdict CONFIRM [RE-CERT] stands; verdict line wording revised)

The advocate's numbers hold up and the skeptic's attacks land as scope
corrections, not overturns. The evidence: 35 named entries enumerated
fresh this wave; 33 PASS; 2 FAIL, both extraction failures on
pull/1/head (5802fec8) and pull/2/head (4b76bb59f), whose trees carry
no pinned znc path and no src/ directory; 27 unique commits; 2 unique
live commits (d0076134d, 6c3c7b69c), both tested directly at their own
tips; 3 live named entries; 32 fixtures; all duplicates named with
SHAs. Uniformity on 33/33: znc pin 498abcb5... byte-identical, probe
sha 3b29aa06..., B2 bin sha 75b85d3c... matching the frozen 2321pdt
value, NEG1/NEG2 discriminating as required, harness rebuilt
byte-identical to a2e6284c... with VERDICT=PASS exit 0 on all 33. Local
HEAD d0076134d static during the run; closing read-only ls-remote
6c3c7b69c identical to run start; no untested origin tip for
next-wave pickup. Zero Python attested this wave.

The modification is on the transit wording, per the skeptic's attack 3
and the item 4 ruling below. The 0521pdt results file anchors the
transit claims for 1c3f9571, aaabb0b89, and 58dd10ae8 partly on
"0221pdt-tested" premises, but the 0221pdt battery evidence is
superseded and carries zero lineage weight. The transit claims are
re-anchored to this wave's own evidence: this wave verified with
git merge-base --is-ancestor that 1c3f9571, aaabb0b89, 58dd10ae8,
bf69a6f38, and cc3b63d1a are ancestors of the directly tested tips
d0076134d and 6c3c7b69c. The P3 wording is retained with the premise
corrected: "transitively covered for current-tip purposes; not
directly tested at their own tips," grounded in this wave's ancestry
verification. The 0221pdt-testing history may remain in the results
file as a historical note explicitly marked superseded, never as an
evidentiary premise.

Revised verdict line (mandatory elements per P1 and P8, scope stamp
included):

Fork battery 0521pdt: CONFIRM [RE-CERT]: 35 named entries, 33 PASS, 2
extraction FAILs (pull/1/head 5802fec8, pull/2/head 4b76bb59f; no
toolchain path in tree, non-TNN research-doc repos; still uncovered),
27 unique commits, 2 unique live commits (d0076134d, 6c3c7b69c), 3 live
named entries, 32 fixtures, all duplicates named with SHAs; znc pin
498abcb5... and probe sha 3b29aa06... on 33/33; B2 bin 75b85d3c...
matches frozen 2321pdt; NEG1/NEG2 discriminate 33/33; harness rebuilt
byte-identical a2e6284c...; zero Python attested; HEAD d0076134d static
during run; closing ls-remote 6c3c7b69c identical to run start;
1c3f9571, aaabb0b89, 58dd10ae8, bf69a6f38, cc3b63d1a transitively
covered for current-tip purposes via this wave's verified ancestry of
the directly tested tips, not directly tested at their own tips (P3);
pull-1/pull-2 remain the next-wave pickup; the 33/35 headline travels
only with the extraction-FAIL and duplicate caveats; certifies
toolchain and extraction stability only, not the contents of merged
commits.

## Item 2. FIT carry-over: CONFIRMED [RE-CERT] (qualification disclosed; new precedent P12)

The skeptic's procedural objection is the serious one, and the answer
is to record the qualification's boundary as precedent rather than
bury it or pretend the literal reading held.

Cited evidence, verified by the debate group independently this
session: all three merges in range 9526cdb5c..d0076134d (cc3b63d1a,
aaabb0b89, d0076134d) exist; all six parent-to-merge diffs restricted
to the chain paths show only Additions plus one Modification on the
znc binary; that Modification is mode-only (100644 to 100755, blob
611b7f0c215385b7d3073bbebbf6078224c70b4c identical on both sides);
zero modifications, zero deletions, zero content changes to any frozen
chain input. Precondition (1): 10/10 chain inputs byte-exact at
d0076134d. Precondition (2): D1 path durable, hazard closed.
Precondition (4): 2/2 binary reproducibility, 9/9 rerun pairs
byte-identical, KB1 30/30, KB2 17/17, KB5 10/10, output hashes matching
prior records, cited explicitly in place of a re-run. Zero Python in
the FIT work.

The literal empty-diff reading fails only because the D1 freeze, which
the 1421pdt record itself recommended as the D1 closure, landed inside
the carry-over range. Failing the wave on that ground would punish the
loop for executing the prior record's own recommendation. The judge
confirms the CONFIRM [RE-CERT] and records the boundary openly as new
precedent P12: precondition (3) is content-empty. The rule's purpose is
that no frozen chain input was modified or deleted by intervening
merges. Additions of sha-verified byte-exact frozen content that a
prior certified record recommended, metadata-only changes with
identical blob shas, and evidence-scratch additions byte-exact to
frozen fixture shas do not fail the precondition, provided every delta
is enumerated in the evidence file and precondition (1) passes
byte-exact at the new tip. The qualification must be stated in the
verdict record, as it was. This is a disambiguation of scope, not a
weakening of a bar: the bar still fails the wave on any content change
to any frozen input, and the P12 boundary cannot widen without a new
debate.

The coordinator retains discretion to order a literal fresh re-run; the
evidence does not require it, and the judge does not order it. A
re-run against byte-identical inputs with a recorded 9/9 deterministic
history would reproduce identical bytes and add no information.

Confirmed verdict line: tnn_chat FIT: CONFIRM [RE-CERT] on d0076134d
without a fresh re-run: 10/10 chain inputs byte-exact; D1 path durable;
zero modifications, deletions, or content changes to any frozen chain
input across the three merges in 9526cdb5c..d0076134d (only
sha-verified D1 freeze additions, a mode-only znc change with identical
blob, and scratch additions); determinism cited 2/2 binary
reproducibility and 9/9 rerun pairs byte-identical. This is not a
candidate verdict and it is not merge review of the merged-in work; it
certifies the 38-fact closed-book probe chain only.

## Item 3. Interactive TNN: CONFIRMED (EXISTS for supervised red-team probe chats only)

The finding is negative where it is negative and positive only where
shas back it. No source-level chat/REPL/interactive-loop entry point in
src/zag/ or units/ on this tip (zero entry-point-signature matches; the
single "repl" hit was a verified false positive inside
"replication"/"replay"). What exists is inherited and sha-verified: the
frozen baseline probe binary (1ada2fae..., ELF x86-64, runnable), the
frozen decline-gate binary (20273a99..., ELF x86-64, runnable), the CVP
retest binaries, the pinned znc (498abcb5...), and the frozen
instrument sources matching the authority manifest. No probe chat was
run this wave; availability only was verified by file plus sha256sum,
and the verdict says exactly that. The confabulation caveat travels:
tnn_chat answers closed-book from the 38-fact kb.txt with unflagged
confabulations on out-of-KB questions. FIT FOR SUPERVISED red-team
probe chats only. This is a re-certification of the standing finding;
nothing new was claimed and nothing new is certified.

Confirmed verdict line: Interactive TNN: CONFIRM [RE-CERT], EXISTS for
supervised red-team probe chats only: frozen baseline probe binary
(1ada2fae...) and decline-gate binary (20273a99...) both ELF x86-64 and
runnable; authority sources match manifest shas; zero source-level
chat/REPL/interactive-loop entry points in src/zag/ or units/ on this
tip; known confabulation caveat travels.

## Item 4. Backfill of wave-20260926-0221pdt: CONFIRMED (INCOMPLETE; breach recorded; superseded; no verdict tag)

The coordinator's proposed handling is confirmed in full.

Facts on the record: the 0221pdt wave ran the fork battery only and
self-reports 35 entries, 33 PASS, and the same 2 extraction FAILs on
pull/1 and pull/2. Its worker disclosed one python3 heredoc used to
patch the wave's driver text. The wave had no debate and no
LOOP_STATE.md update; its results file was left untracked and is
committed by this wave.

Classification: a python3 heredoc that patches the wave's driver text
touches a wave artifact, and the pure-Zag rule's letter is absolute, so
this is recorded as a red-line breach disclosure against the 0221pdt
wave's driver evidence. This is distinguished on both sides: from the
COMP-2 precedent (a python3 -c that read/wrote no file and contacted no
artifact, recorded as a disclosed contact, not a breach), and from
void-on-sight (which applies to preregs that pre-authorize Python
tooling; this was unapproved, self-disclosed, and not repeated).

Evidentiary status: the 0221pdt battery numbers travel as the wave's
self-reported record for audit-trail completeness and carry zero
evidentiary weight. No coverage claim, no transit premise, and no
lineage claim may cite the 0221pdt battery as its source; this wave's
fresh zero-Python re-run supersedes its results. This severs the
"0221pdt-tested" premises in the 0521pdt results file (see the item 1
modification). The backfill section is marked INCOMPLETE and carries no
verdict tag, because no debate rendered a verdict for that wave.
Committing its results file now is evidence preservation, not
certification. New precedent P13: Python contact that touches a wave
artifact is a red-line breach disclosure; evidence from a breached
wave is superseded, not adopted, and its numbers travel only as
self-report with the breach as a load-bearing caveat.

## Item 5. Documentation: CONFIRMED as maintenance, not a verdict (no tag)

The fit_authority README's stale residual note is fixed and the
AUTHORITY_MANIFEST.md attribution is corrected to bf69a6f38 for the
kb.txt/gaz.txt addition; the shas were correct either way, and the four
frozen chain inputs are untouched. Recorded as documentation
maintenance. No verdict tag applies, and no future citation of these
docs as evidence beyond their shas may rest on this record.

## Queued next (untouched by this debate)

Micah's six pending governance rulings (S7 strike, MD-SSD-1
keep-with-UNVERIFIABLE vs re-freeze, S11 pull, S11-AUD pull, C12 queue,
Python-mirror logic) and his blind verdicts on the sealed pairs (R9,
C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) remain
his to make; this debate decided none of them. Standing items: fork
battery driver with live/fixture split, duplicate naming,
unique-commit counts, and closing tip re-check (P1, P8); pull-1/pull-2
remain untestable until their trees gain the pinned toolchain path;
CV-P and COMP-2 adoption remain doubly gated pending ruling 6; the
P12 content-empty boundary and P13 breach-disclosure precedent apply
to future waves.

New precedents recorded by this wave's judge: (P12) FIT carry-over
precondition (3) is content-empty: sha-verified additions of
prior-record-recommended frozen content, metadata-only changes with
identical blob shas, and evidence-scratch additions byte-exact to
frozen fixture shas do not fail it when every delta is enumerated and
precondition (1) passes byte-exact at the new tip; the qualification
must be stated in the record. (P13) Python contact that touches a wave
artifact is a red-line breach disclosure against that wave's evidence;
a breached wave's results are superseded by a fresh clean re-run and
travel only as self-report with the breach attached, carrying zero
lineage weight; distinguished from no-contact disclosed contact and
from pre-authorized tooling (void-on-sight).

Ruling summary: item 1 MODIFIED (CONFIRM [RE-CERT], verdict line
reworded); item 2 CONFIRMED [RE-CERT]; item 3 CONFIRMED [RE-CERT];
item 4 CONFIRMED (INCOMPLETE, breach recorded, superseded, no tag);
item 5 CONFIRMED (documentation maintenance, not a verdict, no tag).
No verdict was overturned.
