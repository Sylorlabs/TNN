# SKEPTIC REPORT: wave-20260926-1121pdt debate

Role: skeptic. I argue AGAINST each draft verdict in the advocate's slate
(docs/lab/rsi/runs/wave-20260926-1121pdt/debate/ADVOCATE_BRIEF.md,
commit b71cf5c75). The judge decides. A debate overturns a coordinator
verdict only on cited evidence, so every attack below cites file paths,
commit ids, and numbers. This report contains no em-dashes, per loop rule.

Method: I read the committed evidence only, then re-ran the cheap checks
myself (git history, sha256sum, grep, git diff). Findings marked LAND
would change a verdict line or verdict; findings marked
DISCLOSED-AND-ANSWERED are probed, checked, and stand as written,
provided the named caveat keeps traveling.

## Item 1: DP-1 doppler flyby, draft CERTIFY READY-FOR-JUDGE [NEW]

### The skeptic's provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer, from the committed provenance header in
docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/EVIDENCE_DP1_1721.md:

- RENDER_SHA: 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771.
  I re-hashed dp1_variant_r1.wav myself: exact match. The r2 and r3
  variants match too (dossier section 3, confirmed).
- FIRST_RENDERED_WAVE: wave-20260925-1721pdt. The WAV first appears as an
  added file in commit 02d1dcb31 (dossier; the commit message claims
  READY-FOR-JUDGE, which was a worker claim, never a debate verdict).
- COMPONENT_LINEAGE: D-AUD-3-substrate (synth.zag
  f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055,
  vendored byte-identical as sub/synth_base.zag); prior IDs with
  statuses: R9, C1, C2v3, S11-IMG, S11-AUD, S13, S14, whirlpool-planform
  QUEUED-UNJUDGED; S12, S12b, B1, DF-1, C-D19, ST-1 DEAD; G1 STOOD-DOWN;
  D-VID-1 STOOD-DOWN. No JUDGED items.
- NEW_KNOWLEDGE_CLAIM: "A frozen constant-velocity flyby rendered
  through a time-varying propagation delay adds motion-based realism to
  the D-AUD-3 bed via doppler pitch fall, inverse-distance loudness
  swell, and lateral pan at linear resampling cost." One sentence,
  present. Tag: [NEW].

What is new versus inherited: inherited is the D-AUD-3 bed, vendored
byte-identical and honestly labeled substrate. New is the time-varying
propagation delay from a frozen trajectory (doppler pitch fall,
inverse-distance loudness swell, constant-power pan). Not a
re-certification: I checked git history for "doppler" and "flyby"
across all commits. The hits outside DP-1's own commits are text-corpus
mentions of the Doppler effect as a physics fact (docs/lab/cognition_ws
probe corpora, docs/lab/htd-1 abstention fixtures, a Gutenberg corpus
line, web-guide corpus snapshots), not loop candidate mechanisms. No
loop candidate has used source motion. The dossier's "zero hits outside
wave-20260925-1721pdt" overstates the grep scope; the prereg's scoped
claim (runs plus imagination_discovery, excluding .zag-cache) is the
accurate one and it holds.

Prereg commit order, verified by me: prereg
18ad30fe3a9c58df9515033fa8dfcd61f195bb8d (2026-09-26 00:58:46 UTC,
single file PREREG_DP1_1721.md, committed alone) strictly precedes
implementation 02d1dcb31d5f27aa69d7d22d0733a857b2b7d713
(2026-09-26 01:26:51 UTC, 18 files, all inside the dp1 run dir);
git merge-base --is-ancestor confirms the order; both are ancestors of
tnn-native-lab HEAD. All 8 bars were frozen in the prereg before
implementation. PASS on the self-check.

### Attack A1: the "red team" is a self-review, not an independent red team. LANDS (labeling correction).

REDTEAM_DP1_1721.md is titled, verbatim, "self-review, adversarial". It
is the same 1721pdt sensory worker's appendix, not an independent
second pass. The dossier section 4 ("Red-team report: EXISTS, AGREES")
and the advocate brief's heading ("Independent red team EXISTS and
AGREES", conceding "adversarial self-review" only in the body)
overstate its independence. The 1721pdt wave died before any debate, so
no independent red-team pass on DP-1 exists anywhere. The standing
commitment is red-team review of every candidate; a self-review does
not satisfy it. The honest label: worker adversarial self-review,
agrees with its own verdict. This debate group is the independent red
team for DP-1. The verdict line must not claim an independent red team
agreed. This changes the verdict line, not the metric results. LANDS.

### Attack A2: the Python disclosure fails the P15 exact-command form, permanently. LANDS (verdict-line requirement).

P15 (0821pdt judge): "any Python invocation in wave work must be
disclosed with exact command, placement relative to artifact writes,
and a no-contact showing." EVIDENCE_DP1_1721.md disclosure 2 gives the
placement ("my own draft fragment", "no wave artifact written") and a
no-contact showing, but NOT the exact command (only "python3 -c").
I grepped the dp1 run dir myself: the only "python" mentions are
PREREG_DP1_1721.md line 72 (the KB6 token-grep bar text) and
EVIDENCE_DP1_1721.md line 79 (the disclosure); there are no .py files
and no scripts. So the no-contact showing is corroborated as far as the
committed record allows, but the exact command is permanently
unrecoverable (the 1721pdt worker's session is gone). The judge must
rule the classification on an incomplete P15 form. Classification as
disclosed contact rather than breach is correct under P13's letter:
this touched no tooling and no artifact, unlike the 0221pdt
python3-heredoc driver patch, which was a red-line breach against that
wave's evidence. But the verdict line must say "one disclosed python3
-c contact, exact command not recorded (pre-P15 disclosure form),
classified disclosed contact per P13", not borrow the full P15
attestation wording. LANDS as a required verdict-line qualification.

### Attack A3: the KB3 measurement filter was designed post-prereg. LANDS (required note; does not overturn the PASS).

The prereg froze KB3's windows ([3.0, 6.0] s and [15.0, 18.0] s), the
+/-3% tolerance, and the analytic reference 1.20694. It did NOT freeze
the verifier's measurement filter. dp1_verify.zag lines 247 and 254 add
"2 cascaded one-poles, k=0.0071, fc about 50 Hz" before zero crossings,
"because the 6-partial engine overcounts raw crossings" (evidence
disclosure 3). That filter was designed after the freeze, with
knowledge of the engine's spectrum. That is analytic flexibility after
the bar was frozen, even if physically principled and honestly
disclosed. Why it does not overturn: the measurement is genuinely off
the artifact (zero crossings counted on the rendered probe WAV; a
broken delay line would measure wrong), and the margin is enormous:
measured 52.500/43.500 = 1.206897 versus expected 1.20694, a 0.0036%
deviation against a 3% tolerance (roughly 850x inside). No filter
tuning could rescue a wrong mechanism, and the reported "1.207 vs
1.207" exact match is a 3-decimal rounding artifact, not a theory
miracle. The verdict line should note the verifier detail was fixed in
implementation (disclosed) and that the margin makes gaming
implausible. LANDS as a required note.

### Attack A4: no sealed blind pair exists and no loop ear has heard it; "queue for his ears" as worded is premature. LANDS (verdict modification).

LISTENING_DP1.md is listening instructions with labeled files
(baseline, variant), not a sealed blind A/B pair protocol. No sealed
pair exists for DP-1; the dossier section 6 admits this. The loop's
own audio practice puts candidates before his ears as sealed pairs
(S11-AUD sits in the judge queue as a coded pair; the whirlpool
precedent sealed pair_V7EUYZ.ppm / pair_Y5AAW5.ppm with a sealed
mapping). The sensory headspace rule says human ears outrank metrics,
and the worker could not ear-check. Certifying "READY-FOR-JUDGE, queue
for his ears" now spends his scarcest attention on an unsealed,
un-ear-checked candidate on the played-out 09-22 substrate (see A6)
while the S11-AUD thematic overlap (see A5) is unresolved. The loop
has not done everything it can before spending his attention: sealing
a blind pair is outstanding work the loop itself can do. The draft
verdict should be modified: certify the metrics, but hold the queueing
until a sealed blind pair is built, or carry the unsealed status as a
load-bearing caveat in the verdict line. LANDS.

### Attack A5: the S11-AUD thematic overlap. DISCLOSED-AND-ANSWERED, provided it travels verbatim in the verdict line and judge brief.

The mechanism distinction is real and evidenced, not just asserted:
S11-AUD is time-invariant filtering (fixed taps, fixed RT60); DP-1 is
a time-varying delay from source motion that produces pitch shift,
which no static filter can produce; no shared code, parameter, or
measurement (REDTEAM_DP1_1721.md sections 2 and 4). My history check
confirms no loop candidate used source motion. But the distinction is
argued only by the worker's self-review (see A1), and perceptually
both are "physical acoustics on a bed": only his ears can settle
whether the motion realism is a genuinely new percept or a theme
repeat. The red team itself calls it "a real judgment call for the
owner". The verdict line and the judge brief must carry the overlap
verbatim (with the provenance header quoted) so he judges the theme
knowingly, alongside the queued S11-AUD. Disclosed-and-answered only
if it travels; any verdict line that omits it is dishonest.

### Attack A6: DP-1 is another micro-lever on the played-out 09-22 substrate; the frontier tension must be named. LANDS (framing requirement).

The 2026-09-24 red-team audits found that every sensory candidate this
week iterates micro-levers on the 09-22 r8a/r8c/r9 substrate while his
actual frontier is the PAMs v2 deep dive and the b_alpha v9 rebuild.
DP-1 is exactly that class: the D-AUD-3 substrate plus one
physical-acoustics lever. Recovering the orphan is the right repair
(burying it would be worse), but queueing it for his ears is a claim
on his attention, and the alignment record says to stand down where he
has already won. The verdict line should name this tension explicitly
and let the judge weigh whether DP-1 goes to his ears now or waits
with the queued audio items until the S11-AUD verdict resolves the
theme. LANDS as a required framing element.

### Attack A7: KB6's token list is a substring lottery; passing it by renaming a comment proves nothing. DISCLOSED-AND-ANSWERED (minor).

The frozen KB6 token list includes the substring "time", which matches
ordinary words ("time-varying", "runtime", "sometimes"). The worker
passed it by renaming a comment ("time-varying" to "varying-delay",
evidence disclosure 4; recompiled, re-rendered, all SHAs unchanged).
That is cosmetic compliance with a badly specified bar. The real
purity evidence is the pinned compiler and the deterministic
rendering, both solid. Disclosed honestly; the verdict line should not
oversell KB6. Minor.

### Attack A8: ruling-6 (Python-mirror logic) taint probe. CLEARED.

I looked: the dp1 dir has no Python-mirror artifacts, no "(proven:
...)" comments, no .py files; renderer and verifier are pure Zag; the
only Python contact is the disclosed dash-count (A2). No evidence of
Python-mirror-developed logic in DP-1. Cleared.

### On "were all 8 bars genuinely frozen before implementation": yes, with the A3 exception noted.

The prereg froze all 8 bars 28 minutes before the implementation
commit, in the required order. The pre-prereg characterization
(disclosed in the prereg) tuned the design so the bars were satisfiable
by construction; the prereg's consistency check states that if
measurement disagrees the candidate is DISCARDED and bars do not move.
So the freeze is genuine; the bars certify a well-engineered design,
not a discovery. Recorded, not an attack that lands.

## Item 2: Fork battery, draft CONFIRM [RE-CERT]

### The skeptic's provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer: this is process infrastructure, not a candidate; its provenance
is the pin record, and every pin held this wave. znc sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
on 36/36 PASS entries (single distinct value). Probe source sha
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
on 36/36. Harness fork_battery.zag extracted read-only from
tnn-native-lab-wave-archive-20260923-2321pdt (sha
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
matches expected), rebuilt with the pinned znc verified before use;
built binary sha a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
byte-identical to prior waves. B2 recompile bin pin
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
on 36/36. Nothing new is claimed; the wave re-verifies uniform pins.

Independent spot checks by me: at the task-pinned run-start HEAD
02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2, read-only extraction of the
pinned znc and probe gives exactly the two pin shas above, and the
binary executes (znc 2026.07.0-dev). The mid-run origin tip
7ea4d2e61bee5e96f0c4db157a792794b7b176e4 exists locally and its tree
carries the pinned znc (sha matches), so it was genuinely testable at
its own tip.

### Attack B1: the incident-2b re-parse is unauditable; the raw per-entry files are gone. LANDS (conditional caveat).

Incident 2a (redirect into a not-yet-created dir) was fixed by
re-running all 38 entries from scratch: the battery tests did re-run.
But incident 2b's fix was a re-parse of the raw per-entry files with a
hand-fixed parser (sed extraction of b2_bin_a_sha256 instead of
cut -d= -f2), and the evidence commit 1f4bc21a1 contains ONLY
FORK_RESULTS_1121.md: the raw per-entry files (RESULT.txt,
zag_harness.out, znc.sha256, tree_probe.zag) lived in /tmp scratch and
are gone. So "verdicts were recomputed from them with fixed parsing"
cannot be audited by the debate. The 2321pdt judge's bar says
record-checks must be labeled as such: it IS labeled ("recomputed"),
so the letter is met, but P14's spirit (final verdicts rest only on
post-incident artifacts with re-verified pin shas) is weakened when
those artifacts are no longer inspectable. The cheap remedy is a spot
re-run of a small sample (one live entry, one fixture, one pull-head
extraction FAIL) to confirm the fixed parser's verdicts. The CONFIRM
should carry this as a load-bearing caveat, or the judge should
condition confirmation on the spot re-run. (My own spot checks
re-verified the pin claims for two entries, but not the parser.)
LANDS.

### Attack B2: the FETCH_HEAD fetch fast-forwarded origin/tnn-native-lab mid-run. DISCLOSED-AND-ANSWERED.

The fetch moved the remote-tracking ref 94625817c to 7ea4d2e61. It did
not disturb any tested entry: extraction keys on SHAs, the run-start
value was snapshotted first and tested at it, and both in-window tips
(e7427101, 7ea4d2e61) were tested at their own tips (I verified
7ea4d2e61's tree carries the pin). The two post-window tips (006dfe02,
7c19065e) are untested and flagged for next-wave pickup. The "36/36"
headline honestly excludes them. Disclosed-and-answered.

### Attack B3: pull/1 and pull/2, "genuinely untestable or untested-by-choice". DISCLOSED-AND-ANSWERED.

Three waves running, same cause, reproduced this wave: those trees
lack the pinned toolchain path (non-TNN research-doc repos, no src/
dir). Genuinely untestable by this battery, not untested-by-choice;
building from source would break the pin discipline. The verdict line
must keep traveling with the "still uncovered" caveat.
Disclosed-and-answered.

### Attack B4: the tested local HEAD is stale. DISCLOSED-AND-ANSWERED (minor).

The local entry was tested at the task-pinned run-start HEAD
02ee5ae59d, but local HEAD moved to 3eddd54a4 on coordinator wave
commits during the run. Those commits are documentation and evidence
only; the battery certifies toolchain extraction, which is
content-independent. Disclosed-and-answered.

## Item 3: tnn_chat FIT, draft CONFIRM [RE-CERT]

### The skeptic's provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer: the frozen 38-fact closed-book probe chain, inherited
byte-exact from the archive. 10/10 chain inputs byte-exact at
02ee5ae59: baseline instrument c0776ad6, decline instrument a87011fe,
kb.txt 3ef27296, gaz.txt b75fd113, R33 sources e6379ddb and 9824f6db,
pinned znc 498abcb5, fixtures kb1_out30 936c35e1, kb2_inkb 730e2d24,
kb5_nogame b60198b0. What is new this wave: the carry-over
verification across the 21-commit merge range, plus the judge-ordered
fixture relocation to docs/lab/rsi/fit_authority/fixtures/.

I re-verified the relocation myself: relocated copies and originals
both match the frozen pins (936c35e1, 730e2d24, b60198b0). I re-ran
the restricted chain-path diff across 4bbbca69c..02ee5ae59: empty.
The FIT evidence commit 3eddd54a4 contains only the evidence file plus
the three relocated fixtures. P16 citation present (wave-20260925-1421pdt
fresh re-run, evidence commit 9692f5d1d, path named). P12 applied.
The literal-scope sentences travel.

### Attack C1: were the relocated fixtures verified against the ORIGINAL scoring shas or only self-consistent? ANSWERED by my own check.

Against the originals. Both copies match the frozen pins; the
report's before/after table is accurate. Disclosed-and-answered
(independently re-verified by the skeptic).

### Attack C2: determinism by citation, now two waves removed from the last fresh re-run. DISCLOSED-AND-ANSWERED.

The last fresh re-run is wave-20260925-1421pdt (9692f5d1d); this wave
cites it via the 0821pdt carry-over, naming wave and path per P16. The
21-commit merge range adds zero chain changes (empty diff,
re-verified). The citation chain is getting long; a fresh re-run every
N waves would be healthy hygiene, but P12 permits this and every
precondition is met. Disclosed-and-answered.

## Item 4: Interactive TNN, draft CONFIRM [RE-CERT], EXISTS for supervised red-team probe chats only

### The skeptic's provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer: an availability survey, not a candidate. Provenance is the
sha-verified inventory on the merged tip: baseline probe binary
1ada2fae, decline-gate binary 20273a99 (both ELF x86-64, runnable),
instrument sources c0776ad6 and a87011fe, kb.txt, gaz.txt, pinned znc
498abcb5. Nothing new is claimed. Negative finding: no source-level
chat/REPL/interactive-loop entry point in src/zag/ or units/; the
21-commit merge delta adds none.

### Attack D1: third-wave re-certification of the same negative with the same method. DISCLOSED-AND-ANSWERED.

The standing rule (probe chat only when the survey reveals change) was
applied; the survey covered the probe chain paths with empty diffs;
no probe chat was run, correctly. The confabulation caveat travels
(tnn_chat emits unflagged confabulations on out-of-KB questions).
Marginal value is low but the discipline is consistent.
Disclosed-and-answered.

## Item 5: No new candidates this wave, draft CONFIRM the stand-down

### The skeptic's provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer: the lane survey record (P17). No new preregs; every lane stood
down or gated (G1, D-VID-1, CV-P, COMP-2 pending his ruling 6,
B1-class pending P9, ST-1 DEAD); his six governance rulings all open.
The only candidate motion is the DP-1 orphan recovery, whose
commit-order self-check passes (18ad30fe3 strictly before 02d1dcb31,
verified above). The self-check is not vacuous this wave.

### Attack E1: is "no new candidates" still discipline while the loop recovers orphans instead of hunting the frontier? DISCLOSED-AND-ANSWERED for the stand-down itself.

The stand-down is sound: advancing any adoption while his six rulings
are open would gamble with his explicit boundaries, and the 0821pdt
judge already called it discipline. The tension (orphan recovery but
no frontier work on PAMs v2 or the b_alpha v9 rebuild) bites at item
1's queueing decision, where I have already landed it (A6), not here.
Disclosed-and-answered.

## Item 6: Record wave-20260925-1721pdt as INCOMPLETE, no verdict tag

### The skeptic's provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"

Answer: the dead wave's committed evidence: fork battery 3ebca4de0
(33 PASS, 2 FAIL, self-reported), FIT carry-over b37e7e590, DP-1
prereg 18ad30fe3 and implementation/evidence 02d1dcb31. No LOOP_STATE
section, no debate, no judge ruling. DP-1 never reached Micah. Note:
the "READY-FOR-JUDGE" in commit 02d1dcb31's message was a worker
claim, never a debate verdict.

### Attack F1: the advocate cites the wrong precedent; the finish-up-debate precedent applies. LANDS (record correction).

The advocate cites the 2026-09-26 0221pdt backfill (INCOMPLETE, zero
lineage weight). But that wave had a red-line breach (python3-heredoc
driver patch, P13) and NO candidates. The closest precedent for "wave
died before its debate with candidate evidence committed" is
wave-20260924-1721pdt: it timed out before its debate with G1 v3 and
CV-1 evidence committed, and the loop did NOT bury it as INCOMPLETE.
A finish-up run completed the red-team review and a full debate group
(advocate, skeptic, independent judge) ruled on all motions (commit
088a1914e; LOOP_STATE section "Wave 20260924-1721pdt verdicts
(2026-09-24; debate completed 2026-09-25)"). This wave's debate IS the
finish-up debate for the 2026-09-25 1721pdt wave. Recording the dead
wave INCOMPLETE with "zero lineage weight into any future verdict"
and "no verdict tag" mislabels the repair and risks a future reader
concluding the DP-1 worker claim was voided without review. The
record should instead: name the 20260924-1721pdt finish-up precedent,
state that the 1721pdt fork battery and FIT numbers are superseded by
this wave's fresh re-runs (consistent with the 0521pdt judge striking
the "0221pdt-tested" premise as evidentiary), state explicitly that
02d1dcb31's "READY-FOR-JUDGE" was a worker claim and not a verdict,
and point DP-1's lineage to this debate's ruling. LANDS as a
modification of the record wording, not of the recovery itself.

### Attack F2: does INCOMPLETE-with-supersession quietly bury a wave that produced a READY-FOR-JUDGE claim? ANSWERED, conditional on F1.

It would bury it only if DP-1 were not recovered; it is recovered in
item 1 via a read-only dossier and this debate. The burial concern is
answered provided the F1 record correction is made, so the recovery
is traceable. Disclosed-and-answered conditional on F1.

## Summary: attacks that LAND

1. A1: the verdict line must not claim an independent red team agreed;
   REDTEAM_DP1_1721.md is the worker's adversarial self-review; this
   debate group is the independent red team.
2. A2: the P15 exact-command gap is permanent (pre-P15 disclosure);
   the verdict line must say so and classify per P13, not borrow the
   full P15 attestation form.
3. A3: the KB3 verifier filter (k=0.0071 lowpass, dp1_verify.zag
   lines 247/254) was fixed post-prereg; note it in the verdict line.
   The 0.0036%-vs-3% margin makes gaming implausible; PASS stands.
4. A4: no sealed blind pair exists and no loop ear has heard DP-1;
   "queue for his ears" as worded is premature. Modify: conditional
   certify, or carry the unsealed status as a load-bearing caveat.
5. A6: the substrate/frontier tension (micro-lever on the 09-22 bed
   while his frontier is PAMs v2 and the b_alpha v9 rebuild) must be
   named in the verdict line; the judge weighs queueing now versus
   holding with the queued audio items.
6. B1: the fork battery's incident-2b re-parse is unauditable (raw
   per-entry files were /tmp scratch, gone; evidence commit 1f4bc21a1
   holds only the summary). CONFIRM carries a spot-re-run caveat, or
   the judge conditions on one.
7. F1: the 1721pdt record must follow the 20260924-1721pdt finish-up
   precedent (commit 088a1914e), not the 0221pdt INCOMPLETE precedent;
   name the recovery and the worker-claim status explicitly.

## Attacks probed and answered (no verdict change)

A5 (S11-AUD overlap: real mechanism distinction, must travel verbatim
in the verdict line and judge brief); A7 (KB6 token-list cosmetics,
disclosed); A8 (ruling-6 taint cleared by inspection); B2 (FETCH_HEAD
fast-forward, entries keyed on SHAs, in-window tips genuinely tested);
B3 (pull/1 and pull/2 genuinely untestable by this battery, third wave,
same cause); B4 (stale tested local HEAD, content-independent);
C1 (fixture relocation verified against originals, re-checked by me);
C2 (determinism by citation, P12/P16 satisfied); D1 (interactive
negative, standing rule applied); E1 (stand-down is discipline);
F2 (burial concern answered by the recovery, conditional on F1).

No verdict is overturned outright by rhetoric. The seven landing
attacks above are corrections, qualifications, and conditions the
judge should write into the verdict lines. The DP-1 metrics are
sound; what is not yet sound is presenting DP-1 to his ears as a
finished, independently red-teamed, sealed-ready judgment.
