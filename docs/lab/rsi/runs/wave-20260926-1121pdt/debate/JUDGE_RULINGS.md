# JUDGE RULINGS: wave-20260926-1121pdt debate

Independent judge. Working copy ~/workspace/tnn-rsi, branch tnn-native-lab.
Inputs ruled on: ADVOCATE_BRIEF.md (commit b71cf5c75), SKEPTIC_REPORT.md
(commit 496b7e82), and the underlying evidence commits (DP-1 dossier
c2c6188f8, fork battery 1f4bc21a1, FIT 3eddd54a4, plus the
wave-20260925-1721pdt DP-1 prereg 18ad30fe3 and implementation 02d1dcb31).
This file contains no em-dashes, per loop rule.

Standing method: a debate overturns a coordinator verdict only on cited
evidence, never on rhetoric. Attacks that land are written into the
verdict line as qualifications, corrections, or conditions. No ruling
here narrows a frozen kill bar, and no ruling is weakened to force a
pass. The skeptic's provenance probe ("What is the provenance of the
artifacts under judgment, and what exactly is new versus inherited?") is
on the record for all six motions; the probe is answered per motion.

Global boundary, stated once and binding on all six motions: Micah's
six pending governance rulings (the S7 strike, MD-SSD-1
keep-with-UNVERIFIABLE versus re-freeze, the S11 image pull, the S11-AUD
pull, the C12 queue decision, and whether Python-mirror-developed logic
may ever be adopted) and his sealed-pair verdicts are untouched by this
debate. Nothing in these rulings decides any of them.

## M1. DP-1 doppler flyby (wave-20260925-1721pdt orphan)

RULING: MODIFY.

Coordinator draft: CERTIFY READY-FOR-JUDGE [NEW], queue for his ears.

Judge: the metrics certification stands; the ear-queueing does not. The
substance of the certification (bars, provenance, order) survives; the
disposition changes.

### Reasoning with numbers and citations

Provenance: the skeptic's provenance probe is answered from the
committed provenance header in
docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/EVIDENCE_DP1_1721.md,
quoted verbatim:

RENDER_SHA:
994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771
(independently re-hashed by the dossier worker across r1/r2/r3, exact
match; re-hashed by the skeptic for r1, exact match).
FIRST_RENDERED_WAVE: wave-20260925-1721pdt (the WAV first appears as an
added file in commit 02d1dcb31; no earlier render exists in git
history).
COMPONENT_LINEAGE: D-AUD-3-substrate (synth.zag
f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055,
vendored byte-identical as sub/synth_base.zag, re-hashed by the dossier
worker, exact match); R9, C1, C2v3, S11-IMG, S11-AUD, S13, S14,
whirlpool-planform QUEUED-UNJUDGED; S12, S12b, B1, DF-1, C-D19, ST-1
DEAD; G1 STOOD-DOWN; D-VID-1 STOOD-DOWN. No JUDGED items listed.
Nothing recycled and presented as new.
NEW_KNOWLEDGE_CLAIM: "A frozen constant-velocity flyby rendered through
a time-varying propagation delay adds motion-based realism to the
D-AUD-3 bed via doppler pitch fall, inverse-distance loudness swell,
and lateral pan at linear resampling cost." One sentence, present.
Tag: [NEW]. What is new is the time-varying propagation delay from a
frozen trajectory; inherited is the D-AUD-3 bed, vendored byte-identical
and honestly labeled substrate. The skeptic's history check confirms no
loop candidate has used source motion. Note: the dossier's "zero hits
outside wave-20260925-1721pdt" overstates the grep scope; the prereg's
scoped claim (docs/lab/rsi/runs plus docs/lab/imagination_discovery,
excluding .zag-cache: doppler 0, flyby 0, variable-delay 0,
fractional-delay 0) is the accurate novelty claim and it holds. The
verdict line rests on the scoped claim.

Bars: all 8 frozen bars pass, with the measured numbers cited from
EVIDENCE_DP1_1721.md and the dossier (DP1_DOSSIER_1121.md, commit
c2c6188f8): KB1 3/3 variant WAV sha256 identical, 3/3 trace sha256
identical (eb375fd6...). KB2 base_peak 21713, var_peak 21739, both under
32767, 0 clips. KB3 f_approach 52.500, f_recession 43.500, measured
ratio 52.500/43.500 = 1.2069 against analytic 1.20694, deviation
0.0036% inside the +/-3% tolerance (about 850x inside). KB4 crest_ratio
0.994 inside +/-1.5 dB (bounds 0.84140..1.18850). KB5 rms_ratio 1.007
inside +/-2 dB (bounds 0.79433..1.25893). KB6 token grep zero hits in
DP-1-authored code, pinned znc 498abcb5. KB7 variant 6.726 s /
baseline 3.603 s = 1.867x under the 2.0x bar. KB8 210/210 checkpoints,
0 mismatches at 1e-9 scale. The pure-Zag verifier independently outputs
fails=0. No bar was moved or narrowed; none is weakened here.

Prereg commit order: prereg 18ad30fe3 (2026-09-26 00:58:46 UTC, single
file PREREG_DP1_1721.md, committed alone) strictly precedes
implementation 02d1dcb31 (2026-09-26 01:26:51 UTC, 18 files, all inside
the dp1 run dir). 28 minutes apart. Both are ancestors of
tnn-native-lab HEAD; git merge-base --is-ancestor confirms the order.
Self-check PASS; no UNVERIFIABLE ORDERING.

Attacks ruled:

- A1 LANDS. REDTEAM_DP1_1721.md is titled verbatim "REDTEAM DP-1
  DOPPLER FLYBY - wave-20260925-1721pdt (self-review, adversarial)". It
  is the 1721pdt sensory worker's adversarial appendix, not an
  independent second pass. No independent red-team pass on DP-1 exists
  anywhere; the 1721pdt wave died before any debate. The dossier's
  section 4 heading ("Red-team report: EXISTS, AGREES") and the
  advocate's heading ("Independent red team EXISTS and AGREES") overstate
  its independence. The verdict line may not claim an independent red
  team agreed. This debate group is the independent red team for DP-1.
- A2 LANDS. P15 (0821pdt judge) requires the exact command, placement
  relative to artifact writes, and a no-contact showing.
  EVIDENCE_DP1_1721.md disclosure 2 records "python3 -c" once to count
  dash characters in the worker's own draft fragment, with placement
  ("my own draft fragment") and a no-contact showing, but not the exact
  command; the 1721pdt worker's session is gone, so the exact command
  is permanently unrecoverable. Corroboration as far as the committed
  record allows: grep of the dp1 run dir finds "python" mentions only
  at PREREG_DP1_1721.md line 72 (the KB6 token-grep bar text) and
  EVIDENCE_DP1_1721.md line 79 (the disclosure); no .py files exist in
  the run dir. Classification: disclosed contact per P13, not a breach
  (unlike the 0221pdt python3-heredoc driver patch, which touched
  tooling). The verdict line must say exactly that and may not borrow
  the full P15 attestation wording.
- A3 LANDS as a required note; the PASS stands. The prereg froze KB3's
  windows ([3.0, 6.0] s and [15.0, 18.0] s), the +/-3% tolerance, and
  the analytic reference 1.20694; it did not freeze the verifier's
  measurement filter. dp1_verify.zag applies 2 cascaded one-poles
  (k=0.0071, fc about 50 Hz) before zero crossings because the
  6-partial engine overcounts raw crossings. That filter was fixed in
  implementation with knowledge of the engine's spectrum; it is
  honestly disclosed (evidence disclosure 3, documented in the
  verifier source), but it is post-freeze analytic flexibility. It does
  not overturn the PASS: the measurement is genuinely off the artifact
  (zero crossings counted on the rendered probe WAV; a broken delay
  line would measure wrong), and the 0.0036% deviation against a 3%
  tolerance (about 850x inside) makes gaming implausible. The verdict
  line carries the note.
- A4 LANDS. LISTENING_DP1.md is listening instructions with labeled
  baseline and variant files, not a sealed blind A/B pair protocol. No
  sealed pair exists for DP-1; the dossier section 6 admits this; no
  loop ear has heard the candidate; the worker could not ear-check
  (levels set analytically). Under the sensory headspace rule, human
  ears outrank metrics. The coordinator's "queue for his ears" as
  worded is premature: sealing a blind pair is outstanding loop work
  the loop itself can do before spending his scarcest attention. The
  verdict is modified: metric certification granted, queueing held
  pending a sealed blind A/B pair.
- A5 disclosed-and-answered; travels verbatim. The mechanism
  distinction is real and evidenced: S11-AUD is time-invariant
  filtering (fixed taps, fixed RT60); DP-1 is time-varying delay from
  source motion producing pitch shift, which no static filter can
  produce; no shared code, parameter, or measurement
  (REDTEAM_DP1_1721.md sections 2 and 4). Perceptually both are
  "physical acoustics on a bed": only his ears can settle whether the
  motion realism is a genuinely new percept or a theme repeat. The red
  team calls this "a real judgment call for the owner." The verdict
  line and the future judge brief carry the overlap verbatim (with the
  provenance header quoted) so he judges the theme knowingly, alongside
  the queued S11-AUD.
- A6 LANDS as a framing requirement. The 2026-09-24 red-team audits
  found every sensory candidate this week iterates micro-levers on the
  09-22 r8a/r8c/r9 substrate while his actual frontier is the PAMs v2
  deep dive and the b_alpha v9 rebuild. DP-1 is that class: the D-AUD-3
  substrate plus one physical-acoustics lever. Recovering the orphan
  is the right repair, but queueing it for his ears is a claim on his
  attention; the tension is named in the verdict line so the judge and
  the reader weigh it explicitly.
- A7 disclosed-and-answered (minor). The frozen KB6 token list includes
  the substring "time", which matches ordinary words; the worker passed
  it by renaming one comment ("time-varying" to "varying-delay",
  evidence disclosure 4; recompiled, re-rendered, all SHAs unchanged).
  Cosmetic compliance with a badly specified bar; disclosed honestly.
  The verdict line does not oversell KB6: the pinned compiler and the
  deterministic rendering are the substantive purity evidence.
- A8 cleared. Inspection shows no Python-mirror-developed logic in the
  dp1 dir: no Python-mirror artifacts, no "(proven: ...)" comments, no
  .py files; renderer and verifier are pure Zag; the only Python
  contact is the disclosed dash-count in A2. No ruling-6 taint in DP-1.

### Verdict line (final)

"MODIFIED CERTIFICATION, DP-1 DOPPLER FLYBY [NEW]: metrics
READY-FOR-JUDGE on all 8 frozen bars (KB1 3/3 sha-identical WAV and
trace; KB2 peaks 21713/21739, 0 clips; KB3 52.500/43.500 = 1.2069 vs
analytic 1.20694, 0.0036% deviation inside +/-3%; KB4 0.994 inside
+/-1.5 dB; KB5 1.007 inside +/-2 dB; KB6 token grep zero hits, pinned
znc 498abcb5; KB7 1.867x under 2.0x; KB8 210/210 checkpoints, 0
mismatches at 1e-9). Prereg 18ad30fe3 strictly precedes implementation
02d1dcb31 (28 minutes apart), both ancestors of tnn-native-lab HEAD:
commit-order self-check PASS. Red-team agreement exists only as the
worker's adversarial self-review (REDTEAM_DP1_1721.md, titled verbatim
'(self-review, adversarial)'); no independent red-team pass exists;
this debate group is the independent red team for DP-1. One disclosed
python3 -c contact, exact command not recorded (pre-P15 disclosure
form), classified disclosed contact per P13, not a breach. KB3 verifier
measurement filter (2 cascaded one-poles, k=0.0071, fc about 50 Hz) was
fixed in implementation (disclosed); the 0.0036% versus 3% margin makes
gaming implausible. KB6 comment rename disclosed; KB6 is not oversold.
S11-AUD thematic overlap travels verbatim: S11-AUD is time-invariant
filtering (fixed taps, fixed RT60); DP-1 is time-varying delay from
source motion producing pitch shift that no static filter can produce;
no shared code, parameter, or measurement; a real judgment call for his
ears. Frontier tension named: DP-1 is a physical-acoustics lever on the
played-out 09-22 D-AUD-3 substrate while his frontier is the PAMs v2
deep dive and the b_alpha v9 rebuild. Ruling-6 Python-mirror taint
cleared by inspection. QUEUE DISPOSITION: queueing for his ears is
HELD. No sealed blind pair exists, LISTENING_DP1.md is instructions
with labeled files not a sealed protocol, and no loop ear has heard
DP-1, so DP-1 is not placed before his ears this wave. The loop builds
a sealed blind A/B pair (coded files, sealed mapping) before DP-1
reaches him; when presented, the pair travels with the provenance
header quoted verbatim, the S11-AUD overlap quoted verbatim, and
LISTENING_DP1.md."

### Judge-queue disposition

Nothing from DP-1 reaches Micah this wave. When DP-1 reaches him, in a
future wave: a sealed blind A/B pair (coded variant files, sealed
mapping), carrying the provenance header quoted verbatim, the S11-AUD
mechanism distinction quoted verbatim, and LISTENING_DP1.md. DP-1
remains READY-FOR-JUDGE on metrics, [NEW], its lineage attached to this
debate's ruling. The skeptic's provenance probe is on the record for
this motion.

## M2. Fork battery

RULING: MODIFY (CONFIRM with a load-bearing caveat; not overturned).

### Reasoning with numbers and citations

The skeptic's provenance probe is on the record and answered from the
pin record in FORK_RESULTS_1121.md (commit 1f4bc21a1): 38 named
entries, 36 PASS, 2 extraction FAIL (origin pull/1/head
5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba; both trees lack the pinned
toolchain path, identical cause to the 0821pdt and 0521pdt waves;
non-TNN research-doc repos, genuinely untestable by this battery, third
wave, same cause). 31 unique commits; 5 unique live commits; 5 live vs
33 fixture; all duplicates named explicitly with SHAs (P1/P8). Uniform
pins on all 36 PASS entries: znc
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(36/36, single distinct value); probe source
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
(36/36); B2 recompile bin
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
(36/36). Harness fork_battery.zag extracted read-only from
tnn-native-lab-wave-archive-20260923-2321pdt (sha
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
matches expected), rebuilt with the pinned znc verified before use to
binary sha
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
byte-identical to prior waves. On all 36 PASS entries: B1 stdout
byte-identical (FORKBATTERY-OK 42), B2 rerun identical and recompile
byte-identical, B3 check exit 0, NEG1 fails as required (E0002
unterminated string literal), NEG2 fails as required (stdout differs at
char 1, line 1), fork-tree probe exit 0, harness VERDICT=PASS exit 0.
Zero-Python attestation stands (shell, git, sha256sum, stat, grep, sed,
cut, cmp, pinned znc, rebuilt pure-Zag harness only).

- B1 LANDS as a load-bearing caveat. Verified by me: evidence commit
  1f4bc21a1 contains only FORK_RESULTS_1121.md; the raw per-entry
  evidence files (RESULT.txt, zag_harness.out, znc.sha256,
  tree_probe.zag) lived in /tmp scratch and are gone. "Verdicts were
  recomputed from them with fixed parsing" cannot be audited by the
  debate. Incident 2a's fix (re-run all 38 entries from scratch) is
  clean; incident 2b's fix (re-parse with a hand-fixed sed extraction
  of b2_bin_a_sha256) is unauditable from the committed record. The
  skeptic spot-checked pin claims for two entries (znc and probe shas
  at the task-pinned run-start HEAD 02ee5ae59d; mid-run tip 7ea4d2e61's
  tree carries the pin) but not the parser. The uniform pins (single
  distinct values across 36 entries), the byte-identical harness
  binary, and the from-scratch nature of the 2a re-run all support the
  numbers; but P14's spirit (final verdicts rest only on inspectable
  post-incident artifacts) is weakened. The CONFIRM therefore carries
  a standing spot-re-run requirement written into the verdict line. The
  numbers stand; this is not a pretext to re-litigate them.
- B2 disclosed-and-answered. The FETCH_HEAD-scoped fetch
  fast-forwarded origin/tnn-native-lab from 94625817c to 7ea4d2e61.
  It disturbed nothing: extraction keys on SHAs, the run-start value
  was snapshotted first and tested at it, and both in-window tips
  (e7427101, 7ea4d2e61) were tested PASS at their own tips. The two
  post-window tips (006dfe02, 7c19065e) were not tested and are flagged
  for next-wave pickup.
- B3 disclosed-and-answered. pull/1 and pull/2 remain genuinely
  untestable by this battery (same cause, third wave); the verdict line
  keeps the "still uncovered" caveat.
- B4 disclosed-and-answered (minor). The tested local entry was the
  task-pinned run-start HEAD 02ee5ae59d; local HEAD moved to 3eddd54a4
  on coordinator wave commits during the run; the battery certifies
  toolchain extraction, which is content-independent.

### Verdict line (final)

"CONFIRM fork battery [RE-CERT] wave-20260926-1121pdt: 38 named entries,
36 PASS, 2 extraction FAIL (origin pull/1/head 5802fec8 and origin
pull/2/head 4b76bb59; both trees lack the pinned toolchain path,
identical cause to the 0821pdt and 0521pdt waves, still uncovered by
this battery); 31 unique commits, 5 unique live commits, 5 live vs 33
fixture, all duplicates named explicitly with SHAs in the evidence
file; uniform pins on all 36 PASS entries (znc
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
probe source
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919;
B2 recompile bin
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2);
harness fork_battery.zag f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
rebuilt deterministically to
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
byte-identical to prior waves; zero Python. Scope stamp: toolchain and
extraction stability only, not the contents of the merged commits.
In-window origin tips e7427101 and 7ea4d2e61 both tested PASS; the two
newer tips 006dfe02 and 7c19065e arrived after the testing window and
are flagged for next-wave pickup. The tested local entry was the
task-pinned run-start HEAD 02ee5ae59d. LOAD-BEARING CAVEAT: the
incident-2b verdict recomputation rests on raw per-entry files that
lived in /tmp and are no longer inspectable (evidence commit 1f4bc21a1
holds the summary only); before the next wave's battery cites these
results, a spot re-run (one live entry, one fixture, one extraction
FAIL) with the fixed parser must confirm them."

## M3. tnn_chat FIT

RULING: CONFIRM.

### Reasoning with numbers and citations

The skeptic's provenance probe is on the record and independently
re-verified by the skeptic. 10/10 chain inputs byte-exact at 02ee5ae59:
baseline instrument c0776ad6, decline instrument a87011fe, kb.txt
3ef27296, gaz.txt b75fd113, R33 sources e6379ddb and 9824f6db, pinned
znc 498abcb5, fixtures kb1_out30 936c35e1, kb2_inkb 730e2d24,
kb5_nogame b60198b0. C1 disclosed-and-answered: the relocated fixtures
were verified against the original frozen pins, not just
self-consistent (the skeptic re-verified: relocated copies and originals
both match the frozen pins 936c35e1, 730e2d24, b60198b0). C2
disclosed-and-answered: determinism by citation per P12, P16 satisfied
(wave-20260925-1421pdt fresh re-run, evidence commit 9692f5d1d, path
docs/lab/rsi/runs/wave-20260925-1421pdt/chat_fit/FIT_1421.md named; the
21-commit merge range 4bbbca69c..02ee5ae59 adds zero chain changes,
empty diff re-verified by the skeptic). The literal-scope sentences
travel verbatim (quoted in the verdict line). Zero-Python attestation
stands (shell coreutils only; no python3 invocation of any kind).

### Verdict line (final)

"CONFIRM tnn_chat FIT [RE-CERT] on 02ee5ae59. 'This is not a candidate
verdict and it is not merge review of the merged-in work; it certifies
the 38-fact closed-book probe chain only.' 10/10 chain inputs
byte-exact against frozen shas. The three probe fixtures were relocated
to the durable never-prune path docs/lab/rsi/fit_authority/fixtures/
(shell cp, no edits) and verified against the original frozen pins
before and after (936c35e1, 730e2d24, b60198b0). Zero modifications or
deletions to any frozen chain input across the 21 commits in range
4bbbca69c..02ee5ae59. Determinism cited, not re-run: wave-20260925-1421pdt
fresh re-run, evidence commit 9692f5d1d, path
docs/lab/rsi/runs/wave-20260925-1421pdt/chat_fit/FIT_1421.md (2/2 binary
reproducibility, 9/9 run-pairs byte-identical, KB1 30/30, KB2 17/17,
KB5 10/10), per P12/P16. 'These instruments certify the 38-fact
closed-book probe chain only.'"

## M4. Interactive TNN

RULING: CONFIRM.

### Reasoning with numbers and citations

The skeptic's provenance probe is on the record: a sha-verified
inventory on the merged tip. Baseline probe binary
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
(ELF 64-bit, runnable); decline-gate probe binary
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7
(runnable, sibling source present); frozen instrument sources c0776ad6
and a87011fe, kb.txt 3ef27296, gaz.txt b75fd113, pinned znc 498abcb5,
all matching the authority manifest. Negative finding: no source-level
chat/REPL/interactive-loop entry point exists in src/zag/ or units/
(the single grep hit was the substring "repl" inside
"replay"/"replication" in
units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md); the 21-commit
merge range contains zero commits touching src/ or units/ and no newly
added chat|repl|interactive file. D1 disclosed-and-answered: the
standing rule (probe chat only when the survey reveals change) was
applied; the survey revealed no change; no probe chat was run,
correctly. The confabulation caveat travels verbatim. Zero-Python
attestation stands.

### Verdict line (final)

"CONFIRM interactive TNN [RE-CERT]: EXISTS for supervised red-team
probe chats only. Negative on source entry points: no
chat/REPL/interactive-loop entry point in src/zag/ or units/ on this
tip, and the 4bbbca69c..02ee5ae59 merge added none. Runnable surface
verified by sha only (no execution): baseline probe binary
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c and
decline-gate probe binary
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7,
frozen instruments and pinned znc 498abcb5 all byte-identical to the
authority manifest. No probe chat was run; the survey revealed no
change. Caveat travels: tnn_chat emits unflagged confabulations on
out-of-KB questions, so this surface is for supervised red-team probe
chats only, never a candidate for adoption."

## M5. No new candidates this wave

RULING: CONFIRM.

### Reasoning with numbers and citations

The skeptic's provenance probe is on the record: the lane survey record
per P17. No new prereg drafts since the 0821pdt wave; every lane stood
down or gated (G1, D-VID-1, CV-P and COMP-2 pending his ruling 6 on
Python-mirror logic, B1-class pending P9, ST-1 DEAD); all six of his
governance rulings remain open. E1 disclosed-and-answered: the
stand-down is discipline, not stagnation; the frontier tension (orphan
recovery but no frontier work on PAMs v2 or the b_alpha v9 rebuild)
was landed at M1's queueing decision (A6), where it belongs. The prereg
commit-order self-check is not vacuous this wave: it covers the
recovered DP-1 commits, prereg 18ad30fe3 strictly before implementation
02d1dcb31, each committed alone: PASS, no UNVERIFIABLE ORDERING.

### Verdict line (final)

"CONFIRM the no-new-candidates stand-down for wave-20260926-1121pdt.
Lane survey per P17: no new prereg drafts since the 0821pdt wave; all
lanes stood down or gated while his six governance rulings remain open.
Prereg commit-order self-check covers the recovered DP-1 commits:
18ad30fe3 strictly precedes 02d1dcb31, each committed alone. PASS; no
UNVERIFIABLE ORDERING. The only candidate motion this wave is the DP-1
orphan recovery ruled on in M1."

## M6. Record for wave-20260925-1721pdt

RULING: MODIFY the coordinator's draft record.

### Reasoning with numbers and citations

F1 LANDS. The advocate cites the 2026-09-26 0221pdt backfill precedent
(INCOMPLETE, zero lineage weight). That wave had a red-line breach
(python3-heredoc driver patch, P13) and no candidates. The correct
precedent for "wave died before its debate with candidate evidence
committed" is wave-20260924-1721pdt: it timed out before its debate with
G1 v3 and CV-1 evidence committed, and the loop did not bury it as
INCOMPLETE. A finish-up run completed the red-team review, and a full
debate group (advocate, skeptic, independent judge) ruled on all motions
(commit 088a1914e; LOOP_STATE section "Wave 20260924-1721pdt verdicts
(2026-09-24; debate completed 2026-09-25)"). The wave-20260926-1121pdt
debate IS the finish-up debate for wave-20260925-1721pdt. F2 is
answered conditional on this correction: the burial concern is answered
because DP-1 is recovered in M1 via a read-only dossier and this
debate, and the record below names the recovery explicitly. Verified
facts: the 1721pdt debate dir was empty; LOOP_STATE.md contains zero
mentions of wave-20260925-1721pdt (no section existed); commit
02d1dcb31's "READY-FOR-JUDGE" was a worker claim, never a debate
verdict; DP-1 never reached Micah before this wave.

### Exact record wording (to be written into LOOP_STATE.md)

"## Wave 20260925-1721pdt: closed by finish-up debate (2026-09-25; debate
completed 2026-09-26 in the wave-20260926-1121pdt debate group)

The 20260925-1721pdt wave died before its debate with committed
evidence: fork battery 3ebca4de0 (33 PASS, 2 FAIL, self-reported), FIT
carry-over b37e7e590, and the DP-1 doppler flyby (prereg 18ad30fe3,
implementation 02d1dcb31). Precedent: wave-20260924-1721pdt, completed
by a finish-up debate group (debate ruling commit 088a1914e; LOOP_STATE
section 'Wave 20260924-1721pdt verdicts (2026-09-24; debate completed
2026-09-25)'). The 0221pdt INCOMPLETE precedent does not apply: that
wave had a red-line breach and no candidates. Record repair: (1)
commit 02d1dcb31's 'READY-FOR-JUDGE' was a worker claim, never a debate
verdict; (2) the 1721pdt fork battery and FIT numbers are superseded
historical evidence with zero lineage weight into any future verdict,
per the existing supersession rules, superseded by this wave's fresh
fork battery and FIT re-verifications; (3) DP-1's lineage attaches to
the wave-20260926-1121pdt debate ruling (M1), and DP-1 never reached
Micah before that ruling."

(The LOOP_STATE.md edit applying this wording is outstanding
coordinator work; it is not part of this ruling document.)

## Closing

No verdict was overturned outright. Seven skeptic attacks landed as
corrections, qualifications, or conditions, and all seven are written
into the verdict lines above (A1, A2, A3, A4, A6, B1, F1); the rest were
probed and answered on cited evidence (A5, A7, A8, B2, B3, B4, C1, C2,
D1, E1, F2). No frozen kill bar was narrowed and no verdict was
weakened to force a pass. Micah's six pending governance rulings and
his sealed-pair verdicts are untouched by this debate.
