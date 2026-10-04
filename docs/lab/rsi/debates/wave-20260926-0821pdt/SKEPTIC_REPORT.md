# Skeptic report: wave-20260926-0821pdt

The skeptic attacks the coordinator's draft verdicts. An attack lands
only with cited evidence, never rhetoric. The verbatim provenance
probe appears once per item below (4 occurrences). No em-dashes are
used in this file. Zero Python was used by this debate group; all
verification was read-only git, sha256sum, grep, and shell coreutils.

## Item 1. Fork battery: attack

Provenance probe: "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer the coordinator must give: of the 36 named entries, the only
new artifact-producing work this wave is the testing of one unique
live commit (4328a8350d) under two names, plus the from-scratch
re-runs of wt-wave3-trades and wt-wave3-senses. Everything else is
inherited: 34 fixtures are re-tests of unchanged-SHA commits for
coverage, and the uniform battery numbers (znc pin, probe sha, B2 bin
sha, harness build) are inherited values re-verified, not newly
produced. So the 34/34 PASS verdict is a verdict about this wave's
testing of overwhelmingly inherited commits. The headline must never
travel without that.

Attack 1. The /tmp incident and post-hoc discovery. The worker admits
the wt-wave3-senses artifacts were "later found zeroed in scratch":
discovery was post-hoc, not real-time. There was no integrity monitor
during the run; the run had no tripwire that fired when extraction
corrupted. The worker's own words: the trades extraction produced a
0-byte znc_raw with "silent odd exit codes" (silent: the failure mode
does not announce itself), and a concurrent git repack made "isolated
git object reads flaky" during the same window. If extraction can fail
silently and object reads can go flaky without the driver noticing,
the skeptic asks: what is the evidence that the other 32 passing
entries were not extracted during the same flaky window with subtle
corruption? The worker's answer is the uniform 34/34 evidence: pin
shas matched and the full behavioral battery passed. That is a real
answer, but it is a post-hoc consistency check, not a controlled
experiment. The re-runs themselves used read-only git show against the
same object store that was mid-repack; the evidence that the re-read
objects were intact is the sha match to the pinned values, which is
circular only if the pinned values were themselves recorded during the
flaky window. The results file says the 36 znc_raw shas were recorded
before /tmp was freed, which means some shas were recorded during the
flaky window. The final verdicts rest on the post-rerun artifacts, and
their shas matched the pinned values recorded outside the incident for
those entries, but the record does not state explicitly which sha
readings are pre-incident and which are post-rerun. The verdict line
must carry the incident as a load-bearing caveat, and the 34/34 claim
is only as strong as the weakest sha reading in it.

Attack 2. The accidental python3 one-liner and the attestation
wording. The results file states "Zero Python ran in this worker's
work" and, in the same breath, discloses one python3 -c invocation.
Those two sentences cannot both be true as written: Python did run.
The worker means "zero Python touched wave artifacts," but that is not
what the attestation says. An attestation that contradicts itself in
adjacent paragraphs undermines the credibility of every attestation in
the file, including the pure-Zag claim the battery rests on. On P13's
letter plus the COMP-2 distinction, a no-op python3 -c that read and
wrote no file and contacted no artifact is a disclosed contact, not a
breach, and the skeptic does not claim the battery evidence is void.
The skeptic's harder point: the one-liner was embedded in a shell
verification one-liner, i.e., it was part of a verification step, and
it ran after the results file was written. A verification chain that
contains a Python invocation, however no-op, is a verification chain
that is not purely the tools it claims. Accidents are exactly what red
lines exist to catch: "it was an accident" is not a defense against a
red line, it is the reason the line is absolute. If every wave may
disclose one no-op python3 -c with no consequence beyond disclosure,
the rule degrades into a disclosure ritual. The debate must decide
whether P13's breach rule triggers, and if it does not, the precedent
must tighten the attestation wording so "zero Python" can never again
sit next to a disclosed python3 run.

Attack 3. The headline travels with padding. 36 named entries, but 27
unique commits, 34 fixtures, and the 2 "live" entries are the same
commit under two names. The live signal this wave is literally one
commit tested twice. The two FAILs are extraction failures on
non-TNN repos that have failed identically for three waves running;
they are carried as named entries that cannot pass by construction.
The 36-entry headline, unqualified, reads as broad coverage; the
honest reading is: one new commit verified, 33 inherited commits
re-verified for coverage, 2 permanently untestable forks carried for
audit continuity. Any verdict line that leads with 36/34 without the
duplicate and fixture caveats in the same breath is headline gaming.

## Item 2. tnn_chat FIT carry-over: attack

Provenance probe: "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer the coordinator must give: no new artifacts were produced this
wave. The verdict rests on sha verification of inherited frozen inputs
at the new tip, a diff of two inherited commits, and determinism
evidence inherited from the wave-20260925-1421pdt fresh re-run, itself
now cited through two intermediate records (0521pdt quoted it verbatim;
0821pdt cites the quote). The new work is the measurement at the new
tip; everything that makes the verdict a PASS is inherited.

Attack 1. Determinism-by-citation is now three waves deep. P12 permits
citing certified determinism in place of a re-run, and this wave's
precondition (3) is the cleanest yet (doc-only changes plus a zero
diff). But each wave the citation moves one step further from a live
run: 1421pdt ran it, 0521pdt quoted the record verbatim, 0821pdt cites
the quotation. The claim "a fresh re-run would reproduce identical
bytes and add no information" is asserted, not demonstrated, and it is
asserted about a toolchain (pinned znc, frozen instruments) whose
current-tip behavior has not been exercised by the FIT instruments for
three waves. The skeptic does not demand a re-run this wave; the
cryptographic case (byte-exact inputs, zero chain-path changes) is
genuinely sufficient. The skeptic demands the citation depth be
visible: the verdict line must name the wave of the last fresh re-run
so a future reader can see how many waves have passed on citation
alone. A rule that permits indefinite citation without a depth
counter is a rule that never re-runs, and "never re-runs" was not what
P12 authorized.

Attack 2. The fixtures live in a pruneable path. Three of the ten
chain inputs (KB1, KB2, KB5 fixtures) live under
docs/lab/rsi/runs/wave-20260924-0521pdt/forks/scratch/fitchat0521/, a
prior wave's scratch directory. Precondition (1) depends on files in a
location whose entire purpose is per-wave scratch. The D1 freeze
closed the hazard for the six fit_authority entries; the fixture
triplet has no equivalent durability guarantee. If a future wave
prunes old run scratch, precondition (1) fails for reasons that have
nothing to do with the chain's integrity, and the FIT verdict becomes
unreproducible. The skeptic flags this as a structural weakness the
advocate's cryptographic case quietly depends on.

Attack 3. The manifest needed correction. The 0521pdt commit corrected
the AUTHORITY_MANIFEST.md attribution (b650ea46f to bf69a6f38). The
advocate says the shas were correct either way, which is true, but the
skeptic notes the direction of the error: a frozen authority manifest
contained a wrong commit attribution, discovered and fixed by a later
wave. A manifest that needed a correctness fix is a manifest whose
other rows deserve the same suspicion the fix implies. The sha table
is verified byte-exact this wave, which answers the suspicion for the
rows that matter, but the incident shows the D1 closure was not as
clean as the closure record claimed.

## Item 3. Interactive TNN: attack

Provenance probe: "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer the coordinator must give: every artifact named in the verdict
is inherited. The baseline and decline-gate binaries are frozen builds
from September 23 and 24; the instrument sources were extracted during
wave-20260925-1421pdt; the CVP retest binaries are from
wave-20260925-0821pdt. The only new work this wave is the grep checks
and the sha verifications at this tip. No probe chat was run; the
verdict certifies availability only.

Attack 1. "EXISTS" is doing a lot of work for a negative finding. The
standing question is "does a runnable interactive TNN exist on this
branch," and the honest answer remains: no source-level chat/REPL
entry point exists in src/zag/ or units/, and what runs are frozen
probe binaries from two to three days ago, plus a toolchain binary.
The verdict tag [RE-CERT] suggests something was re-certified; what
was re-certified is that old binaries still have their old shas. That
is worth recording, but the skeptic insists the verdict line keep the
negative finding first: no interactive TNN exists at the source level
on this tip. The availability claim must not be readable as progress.

Attack 2. The confabulation caveat is load-bearing, not decorative.
The record states tnn_chat emits unflagged confabulations on out-of-KB
questions (the "Paris is the capital of France" example for the
capital of Italy). Any verdict that certifies these binaries as
available for supervised red-team probe chats must carry the caveat
that the instrument under test confabulates without flagging. The
draft does carry it; the skeptic's point is that it must survive every
future rewording of the verdict line, because a future reader who sees
"EXISTS for supervised red-team probe chats" without the caveat could
mistake availability for reliability.

Attack 3. No probe chat was run, again. The verdict has been
"availability only, no probe chat run this wave" for consecutive
waves. The instruments exist for supervised red-team probing, yet no
supervised probing happens wave after wave. The skeptic asks whether
the interactive check is becoming a sha-verification ritual that never
exercises the thing it certifies. Availability without exercise rots:
a binary that is never run is only notionally runnable. The judge
should note whether "no probe chat run" remains an acceptable standing
state or whether the loop owes the instruments an actual supervised
run.

## Item 4. No new candidates: attack

Provenance probe: "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer the coordinator must give: there are no artifacts under
judgment. The verdict is about an absence. The lane-gate states are
inherited from prior waves' records and from Micah's six pending
governance rulings; the "deliberate coordinator choice" is this wave's
decision. Nothing was designed, preregistered, or tested.

Attack 1. Stagnation versus discipline is decided by evidence the
coordinator did not cite. The draft says "Lane survey found no new
prereg drafts or design ideas," but no lane survey record is cited:
no evidence file, no list of lanes checked, no statement of what was
looked at. The skeptic does not claim prereg drafts exist; the
skeptic claims the verdict asks the debate to take the survey on
faith. A "no new candidates" verdict that cannot point to the survey
behind it is indistinguishable from a coordinator who did not look.
If the loop's mandate is to hunt free lunches, the wave owes the
record a checkable account of the hunt, even if the hunt came up
empty.

Attack 2. The loop is certifying its own infrastructure while the
frontier moves elsewhere. The alignment record already states the
loop's sensory candidates iterate a played-out 09-22 substrate while
Micah's actual frontier is the PAMs v2 deep dive and the b_alpha v9
rebuild. This wave stood down every candidate lane and produced zero
preregs, zero design ideas, zero new tests of frontier code. The fork
battery's own scope stamp says it certifies toolchain and extraction
stability only, never merged frontier code; the FIT scope sentence
says it is not merge review. So this wave's entire verdict slate, by
its own scope stamps, certifies nothing about the frontier. The
advocate calls this discipline; the skeptic calls it a loop that has
settled into re-certifying its own scaffolding. The six pending
governance rulings genuinely gate adoption, but they do not gate
design: nothing stopped the wave from producing a genuinely new design
idea or a re-aimed D-VID-1 prereg except the absence of one. The judge
should say plainly whether "no new candidates" this wave reflects
gated lanes or an empty bench, because the loop's standing line is to
hunt, and a hunt with no sightings still owes the sightings log.

Attack 3. The vacuous self-check. "No preregs this wave, so the
prereg commit-order self-check is vacuous: no UNVERIFIABLE ORDERING."
A vacuous pass is not a pass; it is the absence of the thing being
checked. Recording it as a clean check normalizes the form of the
check without its substance. The skeptic asks that vacuous checks be
labeled vacuous in the record, not folded into a passing narrative.
