# JUDGE RULINGS: wave-20260926-1421pdt debate

Independent judge. Working copy ~/workspace/tnn-rsi, branch tnn-native-lab,
HEAD b6f96edaf8d3e7d422aa0f81db9abc91810671c6. Inputs ruled on:
ADVOCATE_BRIEF.md, SKEPTIC_REPORT.md, and the underlying wave evidence
(forks/FORK_RESULTS_1421.md, fit/FIT_1421.md,
interactive/INTERACTIVE_1421.md, survey/LANE_SURVEY_1421.md, dp1/blind/),
plus the wave-20260926-1121pdt JUDGE_RULINGS.md as the ruling context this
wave's agenda items were directed by. The judge independently re-verified
key claims with git, sha256sum, and grep. Zero Python used by the judge in
this ruling; shell coreutils only. No em-dashes in this document, per loop
rule.

Standing method: a debate overturns a coordinator verdict only on cited
evidence, never on rhetoric. Attacks that land are written into the verdict
line as qualifications, corrections, or conditions. No ruling here narrows a
frozen kill bar, and no ruling is weakened to force a pass. The skeptic's
provenance probe ("What is the provenance of the artifacts under judgment,
and what exactly is new versus inherited?") is on the record for all six
motions; the probe is answered per motion.

Global boundary, stated once and binding on all six motions: Micah's six
pending governance rulings (the S7 strike, MD-SSD-1 keep-with-UNVERIFIABLE
versus re-freeze, the S11 image pull, the S11-AUD pull, the C12 queue
decision, and whether Python-mirror-developed logic may ever be adopted) and
his sealed-pair verdicts are untouched by this debate. Nothing in these
rulings decides any of them. Presenting anything to Micah is the parent
agent's call, not this wave's.

## M1. Spot re-run of the 1121pdt fork-battery verdicts

RULING: CONFIRM.

Provenance: the skeptic's provenance probe is answered from
FORK_RESULTS_1421.md and the live per-entry evidence. The three spot re-run
entries are 1121pdt artifacts, not new: spot-a at the 1121pdt task-pinned
HEAD 02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2 (live), spot-b at
bd30978748fa83bbea6e423a7074cf32b7304291 (fixture), spot-c at
5802fec8401f28b4036b0dd5ebb23905610cab57 (pull/1/head extraction FAIL). New
versus inherited: the re-run harness invocations are new; every verdict
confirmed is inherited from 1121pdt. The fixed sed parser is the new element
under test, in place from the first run.

Reasoning with numbers and citations:

- Spot-a: harness exit 0, VERDICT=PASS, znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  probe sha256
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
  b2_bin_a sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2,
  probe stdout R32_ZNC_PROBE_OK. 1121pdt PASS confirmed.
- Spot-b: same evidence values, VERDICT=PASS. 1121pdt PASS confirmed.
- Spot-c: extraction failed with "fatal: path
  'src/tools/toolchain/znc_linux_x86_64_abed8aa1' exists on disk, but not
  in '5802fec8401f28b4036b0dd5ebb23905610cab57'",
  VERDICT=EXTRACTION_FAIL. 1121pdt extraction FAIL confirmed, identical
  verbatim cause.
- The 1121pdt incident 2 bug (cut -d= -f2 mis-parse) cannot recur in this
  driver's construction: b2_bin_a_sha256 is parsed with sed from the first
  run, and the harness prints all B2 key/value pairs on one line.

Attacks ruled:

- A1 (thin sample, 3 of 38) FAILS as a blocker on the judge's own terms.
  The 1121pdt judge wrote this exact design into the verdict line: "before
  the next wave's battery cites these results, a spot re-run (one live
  entry, one fixture, one extraction FAIL) with the fixed parser must
  confirm them." The worker executed exactly that design at the correct
  1121pdt heads with the fixed parser from the start.
- A2 (does the spot confirm cover the 36) lands as a scoping note: the spot
  re-run confirms the three sampled 1121pdt verdicts only. The uniformity
  claims for the current wave rest on the fresh full 1421 battery (M2), not
  on the sample. The verdict line says exactly that.
- A3 (spot ran at 1121pdt heads) FAILS: confirming the 1121pdt verdicts was
  the requirement; the current wave's verdicts are covered by the full 1421
  battery.

### Verdict line (final)

"CONFIRM the 1121pdt fork-battery verdicts (spot re-run, fixed sed parser
from the first run): live entry 02ee5ae59d PASS confirmed (harness exit 0,
VERDICT=PASS, znc sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef, probe
sha256 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
B2 bin sha256
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2, probe
stdout R32_ZNC_PROBE_OK); fixture entry bd3097874 PASS confirmed on the
same evidence values; pull/1/head 5802fec8 extraction FAIL confirmed
(fatal: path 'src/tools/toolchain/znc_linux_x86_64_abed8aa1' exists on
disk, but not in '5802fec8401f28b4036b0dd5ebb23905610cab57', identical
verbatim cause). Scope: the three sampled 1121pdt verdicts are confirmed;
the current wave's verdicts are covered by the full 1421 battery in M2."

## M2. Fork battery

RULING: CONFIRM with load-bearing caveats (not overturned).

Provenance: answered from FORK_RESULTS_1421.md and the live per-entry
evidence in /tmp/fb1421/E. 34 of 40 entries are fixtures (unchanged SHAs
re-tested for coverage); 6 live entries cover 5 unique live commits
(b6f96edaf8d3e7d422aa0f81db9abc91810671c6,
746ff60ba16d18c36db2ccd4394cbb9db9d6266d,
f67e989339a67b882f72378b39fad342a1aa6d9e,
006dfe027944f395a47ae8fe6d1e3329a9d7634e,
7c19065e7b1ce13f6479ba50b4f35e110156c734), including the two queued
1121pdt-close pickups tested for the first time. The genuinely new
information this wave is the 5 unique live commits, not 40 entries. The
merged-in upstream commits are treated as CLOSED and certified for
toolchain and extraction stability only, per the scope stamp.

Reasoning with numbers and citations (independent judge spot checks):

- 40 named entries, 38 PASS, 2 extraction FAIL: rh-pull-1-head
  5802fec8401f28b4036b0dd5ebb23905610cab57 and rh-pull-2-head
  4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba. Both fail at extraction step
  one with the identical cause recorded in the 1121pdt, 0821pdt, and
  0521pdt waves: both trees lack the pinned toolchain path (they carry no
  src/ directory at all, non-TNN research-doc repos). Fourth wave
  uncovered; an instrument limit, not a toolchain regression.
- All duplicates named explicitly with SHAs per P8 (f67e98933 twice,
  99143222 three ways, bd3097874 five ways, f875b3417 pair, 3947dca1a
  pair).
- Uniform pins on all 38 PASS entries, grepped across all 38 per-entry
  files: znc
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (38/38); probe source
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (38/38); B2 bin
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  (38/38, matches the frozen value); NEG1 discriminates 38/38 (compile
  exit 1, E0002); NEG2 discriminates 38/38 (stdout WRONG OUTPUT, differs at
  char 1); fork-tree probe stdout R32_ZNC_PROBE_OK 38/38; pure-Zag harness
  VERDICT=PASS exit 0 on 38/38, FAIL on 0.
- Harness rebuilt from frozen 2321pdt source (extracted sha256
  f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
  matches expected), byte-identical to prior waves at
  a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66.
- Closing tip re-check: origin tip f67e98933 static at start and close;
  every tip enumerated at 1121pdt close (006dfe02, 7c19065e, both ancestors
  of f67e98933) was tested; nothing arrived after the testing window.
- Judge spot checks: znc sha256 single-valued
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  across all 40 tested RESULT.txt files in /tmp/fb1421/E; verdict counts
  40 PASS and 3 EXTRACTION_FAIL (the 40 battery entries plus the 3 spot
  re-runs); working-copy znc sha256 498abcb5 matches the pin.

Attacks ruled:

- B1 (headline 38/40 inflates coverage) PARTIALLY LANDS on framing. The
  evidence file names every duplicate with SHAs, and the live/fixture split
  is stated (6 live, 34 fixture, 32 unique commits, 5 unique live), so
  nothing is hidden. But a reader citing 38/40 as 38 independent toolchain
  confirmations would be wrong. The verdict line carries the duplicate/
  fixture caveat every time (P8).
- B2 (two pull heads uncovered, fourth wave) LANDS as a disclosed coverage
  hole: an instrument limit, not a regression; the verdict line keeps the
  "still uncovered" caveat.
- B3 (uniformity rests on uncommitted /tmp evidence) LANDS as the P14
  inspectability caveat. The committed record (FORK_RESULTS_1421.md alone)
  holds the summary; per-entry evidence lives in /tmp/fb1421/E,
  uncommitted. This repeats the 1121pdt incident-2b archival pattern. It
  does not block CONFIRM this wave: the skeptic independently re-verified
  the uniformity claims while the evidence exists, and the judge
  independently re-verified the single-valued znc pin, the verdict counts,
  and the three spot entries. It carries forward as a standing requirement:
  per-entry evidence must be committed or archived before /tmp is reclaimed
  (P14).
- B4 (divergent toolchain) FAILS: judge re-hashed the working-copy znc
  (498abcb5, matches the pin).

### Verdict line (final)

"CONFIRM fork battery [RE-CERT] wave-20260926-1421pdt: 40 named entries, 38
PASS, 2 extraction FAIL (origin pull/1/head 5802fec8, origin pull/2/head
4b76bb59f; both trees lack the pinned toolchain path, identical cause to
the 1121pdt, 0821pdt, and 0521pdt waves, still uncovered by this battery,
fourth wave); 32 unique commits, 5 unique live commits (b6f96edaf,
746ff60ba, f67e98933, 006dfe02, 7c19065e), 6 live vs 34 fixture, all
duplicates named explicitly with SHAs per P8; uniform pins on all 38 PASS
entries (znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
probe source 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919;
B2 recompile bin
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2); NEG1
discriminates 38/38, NEG2 discriminates 38/38; harness rebuilt from frozen
source f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738 to
byte-identical a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66;
zero Python. Scope stamp: toolchain and extraction stability only, not the
contents of the merged commits. Closing origin tip f67e98933 static at start
and close. CAVEATS: cite '38/40' only with the duplicate/fixture split; the
two pull heads remain uncovered (instrument limit, not regression); P14:
per-entry evidence lives uncommitted in /tmp/fb1421/E and must be committed
or archived before /tmp is reclaimed."

## M3. tnn_chat FIT

RULING: CONFIRM.

Provenance: answered from FIT_1421.md and judge spot checks. All ten chain
inputs are inherited frozen artifacts, certified byte-exact at HEAD
b6f96edaf. New this wave: only the carry-over certification itself (sha
checks, diff checks, no re-run). Determinism evidence is inherited from the
wave-20260925-1421pdt fresh re-run (evidence commit 9692f5d1d), cited per
P12 rather than re-run.

Reasoning with numbers and citations:

- Precondition 1: 10/10 chain inputs byte-exact at b6f96edaf (baseline
  instrument c0776ad6, decline instrument a87011fe, kb.txt 3ef27296, gaz.txt
  b75fd113, R33 sources e6379ddb and 9824f6db, pinned znc 498abcb5,
  fixtures 936c35e1, 730e2d24, b60198b0). Judge spot-checked tnn_chat.zag
  (c0776ad6), kb.txt (3ef27296), gaz.txt (b75fd113), and the pinned znc
  (498abcb5): all match.
- Precondition 2: docs/lab/rsi/fit_authority/ durable, never pruned; git
  status clean on all chain paths.
- Precondition 3: across the full 60-commit merge range
  746ff60ba..b6f96edaf, zero modifications, zero deletions, zero content
  changes, and no mode changes on any frozen chain input, including the
  merge commit and all 59 merged-in upstream commits. Supplementary
  origin-side check: pinned znc blob byte-identical in both parents and the
  merge (blob 611b7f0c215385b7d3073bbebbf6078224c70b4c, sha256 498abcb5);
  the mode-only difference (origin 100644, merge 100755) is not a content
  change.
- Precondition 4: determinism cited, not re-run, per P12:
  wave-20260925-1421pdt fresh re-run, evidence commit 9692f5d1d (2/2 binary
  reproducibility, 9/9 rerun pairs byte-identical, KB1 30/30, KB2 17/17,
  KB5 10/10, all runs exit 0 with empty stderr). The open qualification is
  stated openly in the evidence file.

Attacks ruled:

- C1 (determinism one wave old) FAILS as a blocker: P12 is the standing
  precedent for exactly this, and the precondition that justifies carry-over
  (byte-exact chain inputs, zero chain-path diff) is evidenced, not
  asserted. The qualification travels in the verdict line.
- C2 (znc mode-only change) FAILS: blob byte-identical in all three; a mode
  bit is not a content change. Judge re-verified the working-copy znc sha.
- C3 (R33 sources under the bytegen path, enumeration completeness) FAILS:
  the worker enumerates them as chain inputs 5 and 6 with frozen shas, and
  the merge-range diff explicitly covers the bytegen dialogue path.
- C4 (qualification recorded openly enough) FAILS: the verdict line, the
  basis section, and the python-contact statement all state it.

### Verdict line (final)

"CONFIRM tnn_chat FIT [RE-CERT] on b6f96edaf8d3e7d422aa0f81db9abc91810671c6.
'This is not a candidate verdict and it is not merge review of the
merged-in work; it certifies the 38-fact closed-book probe chain only.'
10/10 chain inputs byte-exact against frozen shas. Zero modifications, zero
deletions, zero content changes, and no mode changes to any frozen chain
input across the 60-commit merge range 746ff60ba..b6f96edaf (origin-side
supplementary check: pinned znc blob 611b7f0c215385b7d3073bbebbf6078224c70b4c
byte-identical in both parents and the merge; the 100644 vs 100755 mode-only
difference is not a content change). Determinism cited, not re-run, per P12:
wave-20260925-1421pdt fresh re-run, evidence commit 9692f5d1d, path
docs/lab/rsi/runs/wave-20260925-1421pdt/chat_fit/FIT_1421.md (2/2 binary
reproducibility, 9/9 run-pairs byte-identical, KB1 30/30, KB2 17/17, KB5
10/10). 'These instruments certify the 38-fact closed-book probe chain
only.'"

## M4. Interactive TNN

RULING: CONFIRM.

Provenance: answered from INTERACTIVE_1421.md. Nothing new is under
judgment. The survey re-verifies inherited artifacts: frozen FIT instrument
sources and binaries (shas re-checked), the pinned znc, and the absence of
any source-level chat/REPL entry point in src/zag/ or units/. The one new
commit in the merge range touching this question (3a31cc183,
docs/lab/ORIENTATION.md) is an orientation doc outside src/ and units/,
noted and closed.

Reasoning with numbers and citations:

- Zero chat/REPL/interactive-loop entry points in src/zag/ or units/ on
  b6f96edaf. The single grep hit for "repl" is a verified false positive
  (substring inside "replay"/"replication" in
  units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md). Follow-up grep for
  entry-point signatures (fn main, stdin, readline, read_line,
  interactive_loop, repl_loop) returned zero files.
- The 60-commit merge range 746ff60ba..b6f96edaf contains zero commits
  touching src/ or units/ at all, and added zero chat/repl-named files.
- 3a31cc183 ("Investigator orientation: map of the live TNN program",
  2026-09-26 14:01:48 -0700) adds only docs/lab/ORIENTATION.md (68 lines);
  no entry point, no interactive surface.
- Frozen instruments (c0776ad6, a87011fe, 3ef27296, b75fd113), both runnable
  probe binaries (baseline
  1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
  decline-gate
  20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7),
  and the pinned znc (498abcb5) re-verify byte-identical.
- No probe chat was run, per the standing rule: a supervised probe run is
  scheduled only when the survey reveals change, and the survey revealed no
  change.

Attacks ruled:

- D1 (grep is not execution) lands weakly in principle but FAILS as a
  blocker: the merge delta is empty for src/ and units/, so no new
  interactive surface could have arrived; the pre-merge tip was already
  surveyed. The grep's weakness is bounded by the empty delta.
- D2 (runnable probe binaries exist but were not executed) LANDS as a
  framing caveat: the "no interactive TNN" negative holds at the source
  level only; runnable probe chat surfaces exist and were verified by sha,
  not executed. The verdict line keeps the "source-level" qualifier every
  time. Not executing them is consistent with the standing rule.

### Verdict line (final)

"CONFIRM interactive TNN [RE-CERT]: negative on source-level entry points
only. No chat/REPL/interactive-loop entry point in src/zag/ or units/ on
b6f96edaf (the single grep hit is the 'repl' substring inside
'replay'/'replication' in
units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md; entry-point signature
grep returned zero files); the 60-commit merge range 746ff60ba..b6f96edaf
added zero chat/repl-named files and zero commits touching src/ or units/;
origin commit 3a31cc183 adds only docs/lab/ORIENTATION.md (68 lines), no
interactive surface. Runnable probe surface verified by sha only, no
execution: baseline probe binary
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
decline-gate probe binary
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7, frozen
instruments and pinned znc 498abcb5 all byte-identical to the authority
manifest. No probe chat was run; the survey revealed no change. Caveat
travels: tnn_chat emits unflagged confabulations on out-of-KB questions, so
this surface is for supervised red-team probe chats only, never a candidate
for adoption."

## M5. No new candidates this wave

RULING: CONFIRM.

Provenance: answered from LANE_SURVEY_1421.md per P17. The survey window
(2026-09-26 08:21 to 14:21 PDT) produced no new prereg, no new design file,
no new candidate. The only candidate-adjacent build is the judge-required
DP-1 sealed blind pair (queue-readiness work for an already-certified
candidate, not a new mechanism). Everything else in the window is
prior-wave evidence, debate records, and the 60-commit merge of upstream
work, which is his frontier work treated as CLOSED per the standing rule.

Reasoning with numbers and citations:

- Five independent sweeps: git log on docs/lab/rsi/ (8 commits),
  name-status grepped for "prereg|design" (zero hits), find for
  prereg/design files (only pre-existing; newest preregs predate the
  window), find for new files in the window (only evidence batches and the
  DP-1 blind pair), git status (scratch plus the DP-1 pair).
- G1 STAND DOWN; D-VID-1 STAND DOWN; CV-P STAND DOWN (doubly gated: barred
  pending his governance ruling 6 on Python-mirror-developed logic, still
  open; no rotated-author re-test); COMP-2 STAND DOWN (ruling 6 open, no
  rotated-author re-test, P11 stemmer-contingency unresolved); B1-class
  STAND DOWN (P9 bar reformulation not found); ST-1 DEAD on pristine
  evidence.
- The skeptic independently checked: within docs/lab/rsi/, git diff
  746ff60ba..b6f96edaf is empty and no prereg/design-named commits appear
  in the window. The mechanism-like material in the merge range sits under
  docs/lab/audio_longhorizon/, docs/lab/destruction-pricing-governance/,
  and docs/lab/audio/exact_replication_phase2/; it is his own frontier work
  (RECTANGLE FIX, H.264 CAVLC, MP3 oracle, Fusion Fork B, pig-front, AUDIO
  SEMANTIC-GROWTH phase 3), classified as CLOSED, correctly not treated as
  loop candidates.
- The 1121pdt judge's boundary stands: advancing adoptions while his six
  governance rulings are open gambles with his boundaries; nothing this wave
  was adopted, nothing was queued to him, DP-1 stays HELD, and the six
  rulings remain open and untouched.
- Prereg commit-order self-check is vacuous this wave: no new preregs
  exist, so it is labeled vacuous per P17, not a pass.

Attacks ruled:

- E1 (lane survey exhaustiveness) FAILS: the survey did not miss the
  merge-range material; it classified it correctly as his closed frontier
  work.
- E2 (boundary risk) FAILS: the wave is clean on boundaries.

### Verdict line (final)

"CONFIRM the no-new-candidates stand-down for wave-20260926-1421pdt. P17
lane survey (window 2026-09-26 08:21 to 14:21 PDT, five independent
sweeps): no new prereg drafts, no new design ideas, no re-aimed preregs
since the 0821pdt wave. G1 STAND DOWN; D-VID-1 STAND DOWN; CV-P STAND DOWN
(barred pending his governance ruling 6, no rotated-author re-test);
COMP-2 STAND DOWN (ruling 6 open, no rotated-author re-test, P11
stemmer-contingency unresolved); B1-class STAND DOWN (P9 reformulation not
found); ST-1 DEAD on pristine evidence. Merge-range mechanism-like material
is his own frontier work, treated as CLOSED. The only in-window
candidate-adjacent build is the judge-required DP-1 sealed blind pair
(queue-readiness, not a new mechanism). Prereg commit-order self-check:
vacuous this wave, labeled vacuous per P17. His six governance rulings
remain open and untouched."

## M6. DP-1 sealed blind A/B pair (queue-prep deliverable)

RULING: MODIFY. The pair construction is certified sound; the blind
protocol as packaged leaks the mapping. The seal must be repaired before any
presentation; DP-1 stays HELD this wave.

Provenance: answered from dp1/blind/ and judge re-verification. The pair
WAVs are copies of renders first rendered in wave-20260925-1721pdt:
baseline dp1_baseline.wav
(a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c) and
variant dp1_variant_r1.wav
(994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771),
certified by the 1121pdt judge as MODIFIED CERTIFICATION, metrics
READY-FOR-JUDGE [NEW], built on the D-AUD-3 substrate (synth.zag
f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055,
vendored byte-identical as sub/synth_base.zag). New versus inherited: the
NEW_KNOWLEDGE_CLAIM is the time-varying propagation delay doppler flyby
mechanism (tagged [NEW]); the D-AUD-3 bed is inherited. New this wave: only
the blind packaging (coded filenames, sealed mapping).

Reasoning with numbers and citations (independently re-verified by the
judge):

- Pair WAVs byte-identical to the certified hashes: pair_RGLaA4.wav =
  a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c;
  pair_41tIYv.wav =
  994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771.
  Both files are 3704444 bytes.
- Coded filenames carry no labels. Codes drawn from /dev/urandom (stated,
  not independently auditable). Zero Python used in the build.
- Provenance header in the brief is faithful to DP1_DOSSIER_1121.md
  section 1 (field for field, including COMPONENT_LINEAGE statuses and Tag:
  [NEW]; formatting only differs). S11-AUD overlap matches the 1121pdt
  judge's line 191 ruling verbatim.
- SEALED_MAPPING_DP1.md correctly holds the per-file assignment (RGLaA4 =
  baseline, 41tIYv = variant) and stays sealed.

Attacks ruled:

- F1 (the blind seal leaks) LANDS, and it is the most serious finding of
  this debate. JUDGE_BRIEF_DP1.md asserts "Judge brief carries no
  assignment." That is false when the brief is read whole. The variant sha
  994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771
  appears twice in the brief: once as RENDER_SHA in the verbatim provenance
  header, once in "The pair" table mapped to pair_41tIYv.wav. Any reader of
  the brief can therefore recover the mapping: pair_41tIYv.wav is the
  variant. The blind is broken by the brief itself, not by any external
  file. SEALED_MAPPING_DP1.md staying sealed does not help, because the
  information it seals is already derivable from the brief.
- F2 (provenance header verbatim fidelity) FAILS as an attack: the quote is
  faithful.
- F3 (S11-AUD overlap verbatim) FAILS: the overlap travels correctly.
- F4 (LISTENING_DP1.md) lands as a packaging note: the file labels its
  files (baseline dp1_baseline.wav, variant dp1_variant_r1.wav) but
  contains no coded filenames and no shas, so it does not by itself leak
  the coded mapping. The 1121pdt judge already ruled it is "instructions
  with labeled files not a sealed protocol." It travels as listening
  instructions, not as part of the sealed protocol.
- F5 (queue disposition) answered below.

Repair (minimal, completes this wave): strip the per-file sha-to-filename
assignment from the judge-facing brief. Keep the certification assertion
that one file matches RENDER_SHA
994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771 and one
matches the baseline sha
a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c,
without saying which. The per-file assignment stays only in
SEALED_MAPPING_DP1.md. No re-coding is required: the coded filenames never
appeared in any judge-facing material alongside the assignment except in
this uncommitted brief, which is repaired before any presentation; the
blind that matters is his, and he has not seen the brief or the pair. If
the unrepaired brief were ever presented, the seal would be void; that is
why the repair is mandatory.

Queue disposition:

- The wave agenda's HELD condition was "until the pair exists." The pair
  now exists as files, but per F1 the protocol is not yet a valid blind, so
  the condition is not yet met.
- DP-1 stays HELD this wave regardless: per the 1121pdt judge's M1 queue
  disposition, nothing from DP-1 reaches Micah this wave, and presenting the
  pair is a future-wave queue decision.
- After the repair, the pair meets the 1121pdt judge's three conditions:
  the provenance header quoted verbatim, the S11-AUD overlap quoted
  verbatim, and LISTENING_DP1.md carried as listening instructions. Actual
  presentation to Micah is the parent agent's call, not this wave's.

### Verdict line (final)

"DP-1 SEALED BLIND PAIR: construction certified; blind protocol DEFECTIVE
as packaged. Pair WAVs byte-identical to certified renders (pair_RGLaA4.wav
a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c,
baseline; pair_41tIYv.wav
994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771,
variant); coded filenames carry no labels; codes from /dev/urandom; zero
Python; provenance header quoted verbatim from DP1_DOSSIER_1121.md section
1; S11-AUD overlap quoted verbatim. DEFECT: the brief's 'The pair' table
maps each coded filename to its sha256, and the provenance header carries
RENDER_SHA 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771,
so the blind mapping is recoverable from the brief alone; the brief's
'carries no assignment' claim is false when read whole. REPAIR (completes
this wave): strip the per-file sha-to-filename assignment from the
judge-facing brief; keep the certification assertion that one file matches
RENDER_SHA and one matches the baseline sha without saying which; the
per-file assignment stays only in SEALED_MAPPING_DP1.md; no re-coding
required. QUEUE DISPOSITION: DP-1 stays HELD this wave; the agenda's
HELD-until-pair condition is not met by a valid blind until the repair
lands. After repair, the pair meets the 1121pdt judge's three conditions
(provenance header verbatim, S11-AUD overlap verbatim, LISTENING_DP1.md as
listening instructions). Presentation to Micah is a future-wave queue
decision and the parent agent's call, not this wave's."

## Additional rulings

### The skeptic's P14 inspectability caveat

Question: does the P14 caveat carry load-bearing weight? Answer: the caveat
is valid and it stands, but it does not block CONFIRM this wave. The
committed record (FORK_RESULTS_1421.md alone) holds the summary; the
per-entry evidence lives uncommitted in /tmp/fb1421/E, repeating the
1121pdt incident-2b archival pattern the judge flagged. What saves CONFIRM:
both the skeptic and the judge independently re-verified the uniformity
claims against the live /tmp evidence this wave (skeptic: 43 RESULT.txt
files, 40 PASS and 3 EXTRACTION_FAIL, single-valued znc/probe/B2-bin shas,
neg1_e0002_hit=1 on every tested entry; judge: single-valued znc sha
498abcb5 across all 40 tested RESULT.txt entries, verdict counts 40 PASS
and 3 EXTRACTION_FAIL, the three spot entries verified). The archival gap
is a records defect, not an evidence defect. Standing requirement (P14):
per-entry evidence must be committed or archived before /tmp is reclaimed;
no wave may cite these uniformity numbers after the evidence is gone
without that archive.

### The duplicate/fixture caveat on the 38/40 headline

Stands as a standing framing rule, attached to P8. The headline "38/40
PASS" may be cited only with the split attached: 32 unique commits, 5
unique live commits, 6 live vs 34 fixture, all duplicates named explicitly
with SHAs. A reader citing 38/40 as 38 independent toolchain confirmations
would be wrong; the genuinely new coverage this wave is the 5 unique live
commits. This caveat travels in the M2 verdict line and needs no new
precedent number.

### New standing precedent

One new precedent is warranted, grounded in the F1 defect:

P18 (sealed blind protocol): a judge-facing brief for a sealed blind pair
must contain no per-file identifier that links a coded filename to a
condition or a certified sha. The provenance header and the certification
assertions travel with the brief; the per-file assignment stays only in the
sealed mapping. Any brief that links a coded file to its condition or sha
voids the seal.

No other new precedent numbers are minted this wave; do not inflate.

## Closing

No verdict was overturned outright. Two skeptic attacks landed as a
correction with a condition (F1: the DP-1 seal leak, with mandatory repair
and HELD disposition) and one as a required standing archival condition
(B3/P14); the rest landed only as framing caveats written into the verdict
lines (A2 scoping, B1 duplicate/fixture framing, B2 coverage hole, D2
source-level qualifier, F4 packaging note), or were probed and answered on
cited evidence. No frozen kill bar was narrowed and no verdict was weakened
to force a pass. Micah's six pending governance rulings and his sealed-pair
verdicts are untouched by this debate.

## FINAL VERDICT LINES (verbatim, for the coordinator's LOOP_STATE.md update)

M1: "CONFIRM the 1121pdt fork-battery verdicts (spot re-run, fixed sed
parser from the first run): live entry 02ee5ae59d PASS confirmed (harness
exit 0, VERDICT=PASS, znc sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef, probe
sha256 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
B2 bin sha256
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2, probe
stdout R32_ZNC_PROBE_OK); fixture entry bd3097874 PASS confirmed on the
same evidence values; pull/1/head 5802fec8 extraction FAIL confirmed
(fatal: path 'src/tools/toolchain/znc_linux_x86_64_abed8aa1' exists on
disk, but not in '5802fec8401f28b4036b0dd5ebb23905610cab57', identical
verbatim cause). Scope: the three sampled 1121pdt verdicts are confirmed;
the current wave's verdicts are covered by the full 1421 battery in M2."

M2: "CONFIRM fork battery [RE-CERT] wave-20260926-1421pdt: 40 named
entries, 38 PASS, 2 extraction FAIL (origin pull/1/head 5802fec8, origin
pull/2/head 4b76bb59f; both trees lack the pinned toolchain path, identical
cause to the 1121pdt, 0821pdt, and 0521pdt waves, still uncovered by this
battery, fourth wave); 32 unique commits, 5 unique live commits (b6f96edaf,
746ff60ba, f67e98933, 006dfe02, 7c19065e), 6 live vs 34 fixture, all
duplicates named explicitly with SHAs per P8; uniform pins on all 38 PASS
entries (znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
probe source
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919; B2
recompile bin
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2); NEG1
discriminates 38/38, NEG2 discriminates 38/38; harness rebuilt from frozen
source f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738 to
byte-identical
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66; zero
Python. Scope stamp: toolchain and extraction stability only, not the
contents of the merged commits. Closing origin tip f67e98933 static at
start and close. CAVEATS: cite '38/40' only with the duplicate/fixture
split; the two pull heads remain uncovered (instrument limit, not
regression); P14: per-entry evidence lives uncommitted in /tmp/fb1421/E and
must be committed or archived before /tmp is reclaimed."

M3: "CONFIRM tnn_chat FIT [RE-CERT] on b6f96edaf8d3e7d422aa0f81db9abc91810671c6.
'This is not a candidate verdict and it is not merge review of the
merged-in work; it certifies the 38-fact closed-book probe chain only.'
10/10 chain inputs byte-exact against frozen shas. Zero modifications, zero
deletions, zero content changes, and no mode changes to any frozen chain
input across the 60-commit merge range 746ff60ba..b6f96edaf (origin-side
supplementary check: pinned znc blob 611b7f0c215385b7d3073bbebbf6078224c70b4c
byte-identical in both parents and the merge; the 100644 vs 100755 mode-only
difference is not a content change). Determinism cited, not re-run, per P12:
wave-20260925-1421pdt fresh re-run, evidence commit 9692f5d1d, path
docs/lab/rsi/runs/wave-20260925-1421pdt/chat_fit/FIT_1421.md (2/2 binary
reproducibility, 9/9 run-pairs byte-identical, KB1 30/30, KB2 17/17, KB5
10/10). 'These instruments certify the 38-fact closed-book probe chain
only.'"

M4: "CONFIRM interactive TNN [RE-CERT]: negative on source-level entry
points only. No chat/REPL/interactive-loop entry point in src/zag/ or
units/ on b6f96edaf (the single grep hit is the 'repl' substring inside
'replay'/'replication' in
units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md; entry-point signature
grep returned zero files); the 60-commit merge range 746ff60ba..b6f96edaf
added zero chat/repl-named files and zero commits touching src/ or units/;
origin commit 3a31cc183 adds only docs/lab/ORIENTATION.md (68 lines), no
interactive surface. Runnable probe surface verified by sha only, no
execution: baseline probe binary
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
decline-gate probe binary
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7, frozen
instruments and pinned znc 498abcb5 all byte-identical to the authority
manifest. No probe chat was run; the survey revealed no change. Caveat
travels: tnn_chat emits unflagged confabulations on out-of-KB questions, so
this surface is for supervised red-team probe chats only, never a candidate
for adoption."

M5: "CONFIRM the no-new-candidates stand-down for wave-20260926-1421pdt.
P17 lane survey (window 2026-09-26 08:21 to 14:21 PDT, five independent
sweeps): no new prereg drafts, no new design ideas, no re-aimed preregs
since the 0821pdt wave. G1 STAND DOWN; D-VID-1 STAND DOWN; CV-P STAND DOWN
(barred pending his governance ruling 6, no rotated-author re-test);
COMP-2 STAND DOWN (ruling 6 open, no rotated-author re-test, P11
stemmer-contingency unresolved); B1-class STAND DOWN (P9 reformulation not
found); ST-1 DEAD on pristine evidence. Merge-range mechanism-like material
is his own frontier work, treated as CLOSED. The only in-window
candidate-adjacent build is the judge-required DP-1 sealed blind pair
(queue-readiness, not a new mechanism). Prereg commit-order self-check:
vacuous this wave, labeled vacuous per P17. His six governance rulings
remain open and untouched."

M6: "DP-1 SEALED BLIND PAIR: construction certified; blind protocol
DEFECTIVE as packaged. Pair WAVs byte-identical to certified renders
(pair_RGLaA4.wav a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c,
baseline; pair_41tIYv.wav
994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771,
variant); coded filenames carry no labels; codes from /dev/urandom; zero
Python; provenance header quoted verbatim from DP1_DOSSIER_1121.md section
1; S11-AUD overlap quoted verbatim. DEFECT: the brief's 'The pair' table
maps each coded filename to its sha256, and the provenance header carries
RENDER_SHA 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771,
so the blind mapping is recoverable from the brief alone; the brief's
'carries no assignment' claim is false when read whole. REPAIR (completes
this wave): strip the per-file sha-to-filename assignment from the
judge-facing brief; keep the certification assertion that one file matches
RENDER_SHA and one matches the baseline sha without saying which; the
per-file assignment stays only in SEALED_MAPPING_DP1.md; no re-coding
required. QUEUE DISPOSITION: DP-1 stays HELD this wave; the agenda's
HELD-until-pair condition is not met by a valid blind until the repair
lands. After repair, the pair meets the 1121pdt judge's three conditions
(provenance header verbatim, S11-AUD overlap verbatim, LISTENING_DP1.md as
listening instructions). Presentation to Micah is a future-wave queue
decision and the parent agent's call, not this wave's."
