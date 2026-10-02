# Judge rulings: wave-20260926-0821pdt

The judge renders a reasoned ruling per item with numbers cited. An
overturn requires cited evidence, never rhetoric; none is issued here.
The skeptic's verbatim provenance probe appears once per item in
SKEPTIC_REPORT.md (4 occurrences, grep-verified). Zero em-dashes in
any debate file (grep-verified before writing this ruling). Zero
Python was used by this debate group; all independent verification was
read-only git (rev-parse, ls-tree, diff --stat), sha256sum, and grep.
Micah's six pending governance rulings and his sealed blind A/B
verdicts are his to make; this debate records them as untouched and
decides none of them.

Independent verification by the debate group this session: HEAD is
4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 on branch tnn-native-lab;
the working-copy znc sha256 begins 498abcb5, matching the pin; read-only
git ls-tree confirms the pinned toolchain path is absent in both
5802fec8 and 4b76bb59f, and pull/1/head's tree root holds research
documents with no src/ directory; the chain-path diffs across
d0076134d..4328a8350 were re-verified (8564128c4 touches only
AUTHORITY_MANIFEST.md and README.md; 4328a8350 touches zero chain
paths).

## Item 1. Fork battery 0821pdt: MODIFIED (verdict CONFIRM [RE-CERT] stands; verdict line wording revised; both incidents ruled)

The advocate's numbers hold and the skeptic's attacks land as wording
corrections and new precedent, not overturns. The evidence: 36 named
entries enumerated fresh this wave; 34 PASS; 2 FAIL, both extraction
failures on pull/1/head (5802fec8) and pull/2/head (4b76bb59f), whose
trees carry no pinned znc path and no src/ directory (independently
confirmed this session); 27 unique commits; 1 unique live commit
(4328a8350d) tested under 2 live named entries; 34 fixtures; all
duplicates named with SHAs in six duplicate groups. Uniformity on
34/34, grepped not sampled: znc pin 498abcb5... byte-identical, probe
sha 3b29aa06..., B2 bin sha 75b85d3c... matching frozen, NEG1/NEG2
discriminating as required, harness rebuilt byte-identical to
a2e6284c... from source f38d9154... with VERDICT=PASS exit 0 on all
34. Local HEAD 4328a8350d static during the run; closing read-only
ls-remote 6c3c7b69c identical to run start; no untested origin tip for
next-wave pickup.

Ruling on the /tmp incident: the incident does not undermine the 34/34
PASS claim, but it must travel in the verdict line as a load-bearing
caveat. Cited evidence: the two affected entries (wt-wave3-trades,
wt-wave3-senses) were identified by the worker and were not judged on
compromised artifacts; both were re-run from scratch via read-only git
show after /tmp was freed and both completed cleanly with full
B1/B2/B3 PASS, NEG1/NEG2 failing as required, and matched znc pin and
probe shas; the final verdicts rest on the post-rerun artifacts. A
silently corrupted znc extraction would fail the byte-identical pin
check or the behavioral battery, and the uniform 34/34 evidence shows
neither. The skeptic's residual point stands as a protocol gap rather
than a verdict killer: discovery was post-hoc ("later found zeroed"),
and some sha readings were taken during the flaky window. The verdict
survives because the compromised artifacts were discarded before
judgment and the post-incident artifacts re-verified; the gap is
closed going forward by new precedent P14, not by re-running this
wave.

Ruling on the python3 one-liner: under P13's letter and the COMP-2
distinction, this is a disclosed contact, not a breach. Cited
evidence: the worker's disclosure states the exact command
(python3 -c "print('skip')"), its placement (after the results file
was written, inside a shell verification one-liner), and its effects
(printed one word to stdout; touched no wave data, no files, no
analysis, no tooling). It read and wrote no file and contacted no
wave artifact, which is factually identical to the COMP-2 case P13
distinguishes from breach. The fork battery evidence is therefore not
voided and not superseded. However, the skeptic is right that the
attestation as written contradicts itself: "Zero Python ran in this
worker's work" cannot stand in the same breath as a disclosed python3
invocation. The attestation wording is corrected going forward by new
precedent P15. Had the invocation touched any wave artifact, it would
have been a P13 breach against the affected evidence.

New precedent P14 (integrity-incident protocol): when an extraction or
environment incident compromises per-entry artifacts, the affected
entries must be discarded and re-run from source via read-only
extraction; final verdicts may rest only on post-incident artifacts
whose pin shas are re-verified after the incident; any sha readings
taken during the flaky window must be re-taken; and the incident
travels as a load-bearing caveat in the verdict line, not only in a
results-file paragraph.

New precedent P15 (Python-contact attestation): any Python invocation
anywhere in wave work, including inside verification one-liners, must
be disclosed with its exact command, its placement relative to
artifact writes, and a showing that it read and wrote no file and
contacted no artifact. When such a disclosed contact exists, the
attestation must read "zero Python touched wave artifacts," never the
unqualified "zero Python ran." Under P13's letter, a no-contact
invocation so disclosed remains a disclosed contact, not a breach; the
affected evidence stands.

Revised verdict line (mandatory elements per P1 and P8, scope stamp
included):

Fork battery 0821pdt: CONFIRM [RE-CERT]: 36 named entries, 34 PASS, 2
extraction FAILs (pull/1/head 5802fec8, pull/2/head 4b76bb59f; no
toolchain path in tree, non-TNN research-doc repos; still uncovered),
27 unique commits, 1 unique live commit (4328a8350d) under 2 live named
entries, 34 fixtures, all duplicates named with SHAs (six duplicate
groups; the 2 live entries test the same commit); znc pin 498abcb5 and
probe sha 3b29aa06 on 34/34; B2 bin 75b85d3c matches frozen; NEG1/NEG2
discriminate 34/34; harness rebuilt byte-identical a2e6284c from
source f38d9154; /tmp-full incident: wt-wave3-trades and wt-wave3-senses
re-run from scratch via read-only git show after space was freed, final
verdicts rest on intact post-rerun artifacts with matched shas (P14);
one no-op python3 -c disclosed, exact command and placement stated,
touched no wave artifact: disclosed contact per P13/COMP-2, not a
breach (P15); HEAD 4328a8350d static during run; closing ls-remote
6c3c7b69c identical to run start; the 34/36 headline travels only with
the extraction-FAIL, duplicate, fixture, and incident caveats;
certifies toolchain and extraction stability only, not the contents of
merged commits.

## Item 2. tnn_chat FIT: CONFIRMED [RE-CERT] (P12 applies cleanly; new precedent P16)

The skeptic's determinism-depth objection is the serious one, and the
answer is to make the citation depth visible rather than to order a
redundant re-run.

Cited evidence, independently re-verified by the debate group this
session: the carry-over range d0076134d..4328a8350 contains exactly two
commits; 8564128c4 touches exactly two files, both documentation only
(AUTHORITY_MANIFEST.md one-line attribution correction, sha rows
untouched; README.md residual closure); 4328a8350 shows zero diff on any
chain path. Precondition (1): 10/10 chain inputs byte-exact at
4328a8350d. Precondition (2): D1 path durable, git status clean on all
chain paths. Precondition (4): determinism cited explicitly in place of
a re-run, 2/2 binary reproducibility (decline 20273a99..., baseline
1ada2fae...), 9/9 rerun pairs byte-identical, KB1 30/30, KB2 17/17,
KB5 10/10, output hashes byte-identical to prior records. Zero Python
in the FIT work.

This wave's range needs no 0521pdt-style qualification: no freeze
landed in range, no metadata-only znc change, nothing but doc-only
fixes and an empty diff. P12's content-empty reading is satisfied on
its simplest facts. The judge does not order a fresh re-run; against
byte-identical inputs with a recorded 9/9 deterministic history, it
would reproduce identical bytes and add no information.

New precedent P16 (determinism citation depth): FIT
determinism-by-citation under P12 must name the wave of the last fresh
re-run and the citation path in the verdict line, so the number of
waves standing on citation alone is visible to any future reader. A
rule that permits indefinite citation without a depth counter is not
what P12 authorized. This wave's line therefore names
wave-20260925-1421pdt as the last fresh re-run, cited via the 0521pdt
carry-over record.

The skeptic's fixture-path point is recorded as a directive, not a
precedent: three of the ten chain inputs (KB1, KB2, KB5) live under a
prior wave's scratch directory
(docs/lab/rsi/runs/wave-20260924-0521pdt/forks/scratch/fitchat0521/),
which is a pruneable location. The coordinator should relocate those
fixtures to a durable never-prune path; until then, every FIT evidence
file must note the pruneable location as a standing caveat. The
manifest-correction point is answered by the byte-exact sha
verification this wave: the rows that carry evidentiary weight were
re-verified, not trusted.

Confirmed verdict line: tnn_chat FIT: CONFIRM [RE-CERT] on 4328a8350d
without a fresh re-run: 10/10 chain inputs byte-exact; D1 path durable;
zero modifications, deletions, or content changes to any frozen chain
input across the two commits in d0076134d..4328a8350 (only two doc-only
fixes in 8564128c4, zero chain-path diff in 4328a8350); determinism
cited from the wave-20260925-1421pdt fresh re-run via the 0521pdt
carry-over record (P16): 2/2 binary reproducibility and 9/9 rerun pairs
byte-identical, KB1 30/30, KB2 17/17, KB5 10/10. This is not a
candidate verdict and it is not merge review of the merged-in work; it
certifies the 38-fact closed-book probe chain only.

## Item 3. Interactive TNN: CONFIRMED [RE-CERT], EXISTS for supervised red-team probe chats only

The finding is negative where it is negative and positive only where
shas back it, and the verdict line must keep that order. No
source-level chat/REPL/interactive-loop entry point in src/zag/ or
units/ on this tip (zero entry-point-signature matches; the single
"repl" hit a verified false positive inside "replication"/"replay";
the d0076134d..HEAD delta adds no chat/repl-named file in src/ or
units/). What exists is inherited and sha-verified: the frozen baseline
probe binary (1ada2fae..., ELF 64-bit LSB x86-64, runnable), the frozen
decline-gate binary (20273a99..., ELF 64-bit LSB x86-64, runnable), the
CVP retest binaries, the pinned znc (498abcb5...), and the frozen
instrument sources matching the authority manifest. No probe chat was
run this wave; availability only was verified by file plus sha256sum,
and the verdict says exactly that.

The skeptic's caveat point is adopted as a standing requirement: the
confabulation caveat (tnn_chat emits unflagged confabulations on
out-of-KB questions) must survive every future rewording of this
verdict line, because availability without the caveat misreads as
reliability. The skeptic's "no probe chat run, again" point is noted
as a standing observation: the verdict certifies availability only,
which is what it claims, so no verdict change follows; but the
coordinator should record why no supervised probe run was scheduled,
or schedule one, rather than letting "availability only" become a
permanent ritual that never exercises the instruments.

Confirmed verdict line: Interactive TNN: CONFIRM [RE-CERT], EXISTS
for supervised red-team probe chats only: zero source-level
chat/REPL/interactive-loop entry points in src/zag/ or units/ on this
tip; frozen baseline probe binary (1ada2fae) and decline-gate binary
(20273a99) both ELF 64-bit x86-64 and runnable; authority sources match
manifest shas; known confabulation caveat travels (unflagged
confabulations on out-of-KB questions).

## Item 4. No new candidates this wave: CONFIRMED (stand-down is disciplined; new precedent P17)

The skeptic's stagnation charge fails on the gates but lands on the
survey. Cited evidence for the gates: CV-P and COMP-2 adoption are
barred pending Micah's governance ruling 6; B1-class re-freezes require
the P9 bar reformulation; ST-1 is DEAD on pristine evidence; D-VID-1
needs a re-aimed prereg with a different mechanism; G1 needs a
genuinely new design idea. Advancing any adoption while his rulings
are open would gamble with his explicit boundaries, and the loop may
not decide what is his to decide. On that ground the stand-down is
discipline, not stagnation, and the verdict is confirmed.

But the skeptic is right that "Lane survey found no new prereg drafts
or design ideas" cites no survey record. A verdict about an absence
must show the search, or it is indistinguishable from not looking.

New precedent P17 (empty-lane verdicts): a "no new candidates" or
"no new preregs" verdict must cite the lane survey record: the lanes
checked and what was looked at (prereg drafts, design notes, candidate
queues), even if the record is one line per lane. Vacuous self-checks
must be labeled vacuous in the record, never folded into a passing
narrative. This wave's verdict is confirmed without the survey record
because the gates independently bar every lane, but the next
"no new candidates" verdict without a cited survey does not pass
debate.

The skeptic's treadmill point is answered by the scope stamps
themselves: the fork battery certifies toolchain and extraction
stability only, the FIT certifies the 38-fact probe chain only, and
neither claims anything about frontier code. The wave certified its
infrastructure honestly and declined to invent candidates to fill a
quota. That is the loop behaving as designed while Micah's rulings
are pending.

Confirmed verdict line: No new candidates wave-20260926-0821pdt:
CONFIRM the coordinator's stand-down: every candidate lane stood down
or gated for a stated reason (G1 pending a new design idea, D-VID-1
pending a re-aimed prereg, CV-P and COMP-2 barred pending Micah's
governance ruling 6, B1-class pending the P9 bar reformulation, ST-1
DEAD on pristine evidence); no new prereg drafts or design ideas found
in the lane survey; no preregs, so the prereg commit-order self-check
is vacuous (labeled vacuous, not a pass): no UNVERIFIABLE ORDERING.

## Queued next (untouched by this debate)

Micah's six pending governance rulings (S7 strike, MD-SSD-1
keep-with-UNVERIFIABLE vs re-freeze, S11 pull, S11-AUD pull, C12 queue,
Python-mirror logic) and his blind verdicts on the sealed pairs remain
his to make; this debate decided none of them. Standing items: fork
battery driver with live/fixture split, duplicate naming,
unique-commit counts, and closing tip re-check (P1, P8); pull-1/pull-2
remain untestable until their trees gain the pinned toolchain path;
CV-P and COMP-2 adoption remain doubly gated pending ruling 6; the P12
content-empty boundary, the P13 breach-disclosure precedent, and the
new P14, P15, P16, P17 precedents apply to future waves. Directives
recorded: relocate the KB1/KB2/KB5 fixtures to a durable never-prune
path (item 2); record why no supervised probe chat was scheduled or
schedule one (item 3).

New precedents recorded by this wave's judge: (P14) integrity-incident
protocol: compromised per-entry artifacts must be discarded and re-run
from source via read-only extraction; final verdicts may rest only on
post-incident artifacts with re-verified pin shas; sha readings taken
during a flaky window must be re-taken; the incident travels as a
load-bearing caveat in the verdict line. (P15) Python-contact
attestation: any Python invocation in wave work must be disclosed with
exact command, placement relative to artifact writes, and a no-contact
showing; with a disclosed contact the attestation reads "zero Python
touched wave artifacts," never the unqualified "zero Python ran";
under P13 a no-contact invocation so disclosed remains a disclosed
contact, not a breach. (P16) FIT determinism-by-citation must name the
wave of the last fresh re-run and the citation path in the verdict
line. (P17) "No new candidates" verdicts must cite the lane survey
record (lanes checked, what was looked at); vacuous self-checks must
be labeled vacuous, never folded into a passing narrative.

Ruling summary: item 1 MODIFIED (CONFIRM [RE-CERT], verdict line
reworded; /tmp incident ruled non-undermining with P14 caveat; python3
one-liner ruled disclosed contact per P13, not a breach, with P15
attestation correction); item 2 CONFIRMED [RE-CERT] (P16 citation
depth); item 3 CONFIRMED [RE-CERT]; item 4 CONFIRMED (stand-down;
P17 survey requirement). No verdict was overturned.
