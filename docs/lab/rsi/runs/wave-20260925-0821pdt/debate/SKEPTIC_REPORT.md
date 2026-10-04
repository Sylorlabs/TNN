# SKEPTIC REPORT: wave-20260925-0821pdt verdict slate

Role: SKEPTIC. This report argues AGAINST each coordinator verdict:
gaming, confounds, weak bars, cost, taint, the origin-tip anomaly, the
empty-python3 disclosure, non-independent red-teams, and whether the
DEADs' root causes suggest re-framing rather than death. Standard: a
verdict is overturned only with cited evidence, never rhetoric. Frozen
bars are never weakened. Micah's six pending governance rulings are not
re-litigated.

## Item 1. Fork battery: CONFIRM [RE-CERT], 29/29 PASS

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: the artifacts are the shell battery fixtures, the pure-Zag
harness, and the 29 fork scratch builds. Inherited: the harness source
(read-only extracted from the 2321pdt archive, sha f38d9154... matching
expectation, rebuilt byte-identical to last wave), the shell driver
adapted from the frozen 0521pdt driver, the fixture sources, and all
fixture fork SHAs. New this wave: the fresh enumeration, the new
archive branch tnn-native-lab-wave-archive-wave-20260925-0521pdt at
0ee06268e9, the 4 live-fork entries (local tip moved 058ee02a8 to
382f70f95, origin tip moved 4050b1097 to 4d613edb1), and the explicit
run-start-tip duplicate entry.

Attacks:

1. The headline number flatters coverage. Four entries are explicit
duplicates: origin-tnn-native-lab-runstart-tip tests the same commit as
origin-tnn-native-lab (4d613edb1), and wave3-probe, wave3-senses, and
wave3-trades each test the same commit as forktest-tnn-native-lab
(bd3097874). Unique commits tested: 25, not 29. The duplicates are
named honestly in the evidence, so this is not gaming, but the verdict
slate's "29/29 PASS" reads as broader coverage than it is.

2. The origin-tip anomaly is the real coverage question. The verdict
says the battery CONFIRMs origin/tnn-native-lab while the closing tip
40935c121b is untested. If the origin tip moves every wave, there will
always be an untested tip, and the battery will perpetually certify
yesterday's tip. The practical risk this wave is limited (every wave
artifact was built from the working copy at 382f70f95, not from
origin), but the battery's stated purpose is toolchain-substrate
integrity across forks, and the newest tip is the one that will matter
next wave. The CANNOT-CONFIRM item plus a next-wave pickup request is
the minimum; the skeptic wants the pickup filed as a binding entry the
next wave's coordinator must acknowledge, not a wish.

3. Mode drift (100644 on the 0221pdt and 0521pdt archives,
wave-debate-session-1-backup, and the origin run-start tip) is
asserted metadata-only because every extracted sha matches the pinned
sha. Accepted, but the skeptic notes the assertion rests on the sha
check having run on every fork, which the evidence claims ("on every
fork") and the pass vector grep supports.

The battery itself shows no gaming: NEG1/NEG2 discriminated as
required on all 29, zero Python contact, harness provenance intact.
The verdict is defensible; the coverage claim should be narrowed to
unique commits and the new tip picked up next wave.

## Item 2. ST-1 pristine re-verification: DEAD [NEW]

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: the artifacts are the preserved ST-1 stereo renders
st1_r1/r2/r3.wav (sha 4e9ea742...), the traces, dry_ref.wav (frozen
gate 7728fbee...), and the generator st1_stereo.zag. Inherited: all of
these were first rendered and committed wave-20260925-0521pdt; the
generator is UNTAINTED (only the 0521pdt verifier was voided). New this
wave: the pristine verifier st1_verify_pristine.zag (authored fresh
from the frozen prereg spec via shell heredoc, never copied from the
voided st1_verify.zag) and its measurements, plus the fresh
re-verification renders used for the cross-time determinism
cross-check.

Attacks:

1. The verifier needed a bug fix during the measurement run. The worker
found and fixed its own mysqrt (Newton iteration needed range
reduction for magnitudes near 1e37) mid-run, and the final numbers come
from the fixed verifier. A verifier that required debugging during a
pristine re-verification is exactly the artifact class the pristine
requirement was meant to exclude. What saves the numbers is the
independent awk cross-check: E_st matches awk to the sample, Pearson
0.999605 vs awk 0.999606, RMS -1.761 vs -1.76156 dB. The skeptic
accepts the cross-check as load-bearing but notes the measurement now
rests on awk arithmetic the frozen prereg did not name, validated by
the same worker who wrote both. It is the best available evidence, and
it is consistent to the sample, but it is not the pristine-only chain
the plan promised.

2. Margins: KB7 failed by 0.111 dB (1.611 vs 1.5) and KB2 by 0.898 dB
(1.398 vs 0.5). The skeptic asks whether 0.111 dB is real or noise.
The evidence answers algebraically: KB7 = 10*log10(2) - KB2 = 1.612 dB,
so the two killing readings are one mechanism measured twice, and the
KB2 margin is unambiguous. Both readings fail as frozen; no
re-interpretation is available or requested.

3. The empty-python3 disclosure: the worker invoked `python3` with an
empty stdin script while reaching for an editing shortcut, and attests
it read no files, wrote no files, and touched no artifact. The skeptic
notes this attestation is self-reported and uncheckable after the
fact. The 0521pdt judge precedent (no artifact contact means no taint)
is the governing rule, and the KB5 machine checks do not depend on the
claim, so there is no cited evidence of contact and therefore no void
under the standing rule. But the skeptic flags the incentive shape:
voluntary disclosure of nothing-events is good only if the rule is
predictable, and the precedent makes it predictable. Do not punish the
disclosure; do not pretend it was independently verifiable either.

4. Re-framing versus death. The root-cause note is the most important
paragraph in the evidence: in the Q24 stem domain the candidate
preserves energy as designed (+0.013 dB), 42/42 pans are bit-exact, and
the KB2/KB7 failures are produced by the frozen 0.89 peak normalization
interacting with constant-power panning (the stereo WAV is normalized
with a ~1.17x larger gain than the dry WAV). The mechanism met its own
design spec; the frozen measurement contract measured the normalized
WAVs while the design criterion lived in the stem domain. The DEAD
verdict is correct for this wave's artifact under the frozen mapping,
but the skeptic argues the DEAD label misattributes the failure: it
should attach to the frozen bar-domain choice, not to world-derived
stereo panning as an idea. The honest output is DEAD for the artifact
plus a recorded recommendation: a future re-prereg should freeze
stem-domain or energy-renormalized bars (a new prereg, new bars, no
weakening of these).

## Item 3. CV-P rotated-author re-test: PARTIAL (CONFIRMED on rotated fresh set) [NEW]

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: per the evidence's COMPONENT_LINEAGE: the tnn_chat decline
gate (ADOPTED 1121pdt), CLAIM-VERIFY-1 (ADOPTED), the CV-1
decline-citation fix (ADOPT [RE-CERT] 1721pdt), the frozen stemmer
(morphology crew 2026-09-21, byte-reused not re-authored), and the
0521pdt CV-P PARTIAL (sealed 30, single-session authorship). Inherited:
cvp.zag (the 0521pdt committed implementation, rebuilt byte-identical,
sha dcf98cdb...), the adopted cv1c/gate_op sources (byte-identical
rebuilds), the KB (3ef27296...) and gazetteer (b75fd113...). New: the
fresh sealed 30 probe set authored post-freeze by worker C1 from F9-CVP
(sealed at 35a54297c, UNJUDGED), the pure-Zag scorer written by worker
C2, and the runs, transcripts, and op streams.

Attacks:

1. "Rotated authorship" between two workers in the same session is
rotation of hats, not independence. C1 authored the probes and the
key; C2 rebuilt, ran, and scored. Both are the same depth-2/2 worker
in one session. The 0521pdt prereg capped the verdict at PARTIAL
precisely because "structural different-worker author/implementer
separation is impossible in this session," and this re-test inherits
that structural limitation. Gate (a), the structural separation gate,
was therefore approximated, not satisfied: the re-test ran against a
fresh author, which is real (the 6-gram sweep finds zero probe bytes
in the candidate, and the scorer reads KEY.md at runtime), but the
separation itself is single-session self-attestation, disclosed not
resolved. The verdict's "(CONFIRMED on rotated fresh set)" should be
read as "the bars survived a fresh author," not as an independence
claim. The cap at PARTIAL is the fence that keeps this honest; any
reading that treats the rotation as true independence would be
over-claiming.

2. The scorer is new trust-bearing code with no independent review.
Every bar reading (B1 through B5, the B7 sums) passes through C2's
scorer. Mitigations are all self-review: pure Zag on the pinned
toolchain, 30/30 per-probe verdicts eyeball-verified against the
transcript, B7 sums cross-checked with awk, the 163 stemmed-word count
consistent with the frozen KB. The machine-checked parts (commit
order, seal pins, byte-identity of rebuilds, zero probe bytes, zero
RNG) do not depend on the scorer and all hold. But the skeptic is
blunt: if the scorer mis-scores in the candidate's favor, the
bar readings move with it, and no independent eye has checked. This
is the residual the evidence discloses in self-review point 10, and
it is the reason PARTIAL is the ceiling, not the floor.

3. The S11 tie-break guard (B6, 17/17 parity) covers the exact-form
corridor only. The prereg's named risk, a lower-index fact newly
covering an exact-form turn under stemming, is guarded on 17 turns,
not on all possible inputs. The evidence discloses this residual. The
B7 ratio is 1.0619x on the fresh set versus 1.0626x on the 0521pdt set:
stable, consistent, no cost anomaly.

4. Non-independent red-team: the ten-point self-review is thorough and
finds no confound, but it is self-review by the implementer, disclosed
as such. The skeptic does not claim a hidden confound; the skeptic
claims the confound-hunting was done by the person with the most to
lose from finding one, and the verdict must be priced accordingly.
PARTIAL with adoption barred pending Micah's ruling 6 is the correct
price. Nothing in the numbers argues for more.

## Item 4. DF-1 foreground defocus: DEAD [NEW]

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: RENDER_SHA 6155ae8448...; FIRST_RENDERED_WAVE
wave-20260925-0821pdt. Inherited: r8c_alien.zag (committed, 395663d4;
baseline BMP e4f65557), the vendored R33_NATIVE_IO_V1 substrate
(e6379ddb...), the pinned znc (498abcb5...), and the queue lineage
listed only so the judge queue stays honest (R9, S11-IMG, C1, C2v3,
C12, S11-AUD, S13, S14, whirlpool-planform all QUEUED-UNJUDGED and not
stacked; D19 DISCARDED, opposite mechanism, not stacked; E3 REJECTED
by Micah). New: the DF-1 renders (first blur attempt anywhere in the
loop), the 121-line pass block, the pure-Zag verifier and probe, and
the traces. The [NEW] tag rests on the grep survey finding zero prior
art for defocus/blur/bokeh.

Attacks:

1. The prereg froze a mechanism and a bar that were jointly
unsatisfiable. KB4 requires |variant - baseline| <= 24 luma levels for
every pixel; the frozen mechanism is a genuine R=7 defocus. The
evidence's own probe shows the max-diff pixels sit on a ~100-level
hard edge (the lit arch pillar against the dark field), where any real
R=7 blur must move edge pixels toward the neighborhood mean by up to
roughly half the step: 48 observed. The prereg text said KB4 "bounds
pathological amplification," but the bar as frozen bounds all shifts,
including honest defocus. DF-1 was therefore dead on arrival the
moment both the mechanism (R=7) and the bar (<= 24 everywhere) were
frozen together. The skeptic's charge is governance quality, not
worker honesty: preregs should be consistency-checked (mechanism
against bars) before implementation, so a full implementation plus
verification cycle is not spent discovering that the frozen contract
contradicted itself. The worker implemented the frozen mechanism
exactly (121-line pure addition, passes 1-5 byte-identical, mask
counts recomputed exactly at 257803/5229) and measured the failure
honestly. The failure is real; the design that produced it was
frozen before the first render.

2. KB6 margin is thin: worst variant render 1.856 s against the 2.0 s
bar, a 7% margin. It passed, and it passed on the frozen machine this
wave, but the skeptic notes the cost bar would not survive much load
variance. KB3 passed by 4.4x on efficacy and ~350x on the HF ratio;
KB2 and KB7 passed with zero violations. The bars that passed were not
close calls except KB6, and no bar was re-interpreted.

3. No sealed pair prepared: correct per the frozen sealing plan (a
pair is built only on a clean pass of every bar), and the frozen
mapping forbids judging a DEAD candidate. The skeptic agrees this was
the honest call and notes the temptation it resisted: a
defocused-foreground pair would have been interesting to Micah's eyes,
but the bars are the bars.

4. Re-framing versus death. The mechanism behaved as a lens would; the
probe tail (49+: 0, 203 pixels at 0.019%, fully localized, KB7 zero
overshoot over 33792 feather checks) is the signature of genuine
defocus, not amplification. The skeptic argues the DEAD verdict must
not be read as "defocus is a bad idea." It is the verdict on this
frozen pair: R=7 plus a <= 24 everywhere bound. A future prereg could
freeze a smaller radius with an edge-aware bar, or keep R=7 with a bar
that distinguishes edge shift from amplification; that is a new prereg
with new bars, not a weakening of this one. The knowledge to carry
forward: the E3 grain guard as written is incompatible with any
real-radius blur on hard-edged substrates; the next defocus prereg
must resolve that tension before freezing, or it will burn another
wave.

## Item 5. D1 intelligence lane: NO-CANDIDATE

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answer: there are no artifacts under judgment; the item is a survey
memo. Inherited: the cited prior verdicts (D-SEARCH, Ensemble OVT5,
Trades Candidate A, ITER-FP, SHAPED-MEMBERS, the KB4 substrate
deliberation work, SP-B1) and the standing closures (S4, S11 at
hypothesis-class level, the D-SEARCH/ITER-FP family, M4 R2, the
collision rule). New: the metric ranking (deliberation quality as the
weakest VERIFIED metric), the eight considered-and-rejected ideas with
reasons, and the NO-CANDIDATE conclusion itself. No prereg was
written; nothing was implemented.

Attacks:

1. The surveyor grades their own homework. The eight rejections had no
adversarial pressure. Idea 1 (non-monotone confidence reshaping) was
rejected partly as "unprincipled" and as inside S11's "evident purpose"
though outside its letter. That is a taste judgment plus a self-serving
extension of a closure, not a frozen rule. The skeptic does not claim
the idea would work; the skeptic claims the rejection standard is
softer than the survey presents.

2. The "not framable with a frozen kill bar in Phase 1" rejection
(idea 5, contest second path) is doing heavy lifting. A candidate that
dies honestly still produces knowledge; DF-1 this wave is the proof.
The skeptic asks whether the lane's bar for proposing is set so high
that only pre-dead ideas get proposed, and whether NO-CANDIDATE wastes
a lane's wave. The counter, which the skeptic must concede, is that
proposing without a framable kill bar is padding by definition: the
loop's verdicts are bar-relative, and an idea with no bar cannot be
judged, only admired.

3. The weakest-VERIFIED-metric ranking is constructed honestly: the
unmeasured metrics (learning persistence, capability breadth) are
excluded from the "verified" ranking rather than smuggled in. The
quoted numbers for the five failed classes are the verified record.
The skeptic finds no number misquoted.

The NO-CANDIDATE verdict is the honest output of a survey that found
every foothold closed and every open idea either unprincipled,
evidence-predicted to fail, or unframable. Padding the lane would be
the dishonest move. The skeptic's residual: the rejections should face
adversarial review in a future wave before they harden into
pseudo-closures of their own.
