# SKEPTIC REPORT: wave-20260926-1421pdt debate

Skeptic (red team). Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab. Read-only investigation; nothing committed by this
report's author; the coordinator commits. Zero Python used anywhere in
this work: shell coreutils only (git, sha256sum, grep, sed, awk, ls,
find, cmp). No em-dashes used in this report.

Evidence read directly, not from coordinator summaries:
docs/lab/rsi/runs/wave-20260926-1421pdt/forks/FORK_RESULTS_1421.md,
docs/lab/rsi/runs/wave-20260926-1421pdt/fit/FIT_1421.md,
docs/lab/rsi/runs/wave-20260926-1421pdt/interactive/INTERACTIVE_1421.md,
docs/lab/rsi/runs/wave-20260926-1421pdt/survey/LANE_SURVEY_1421.md,
docs/lab/rsi/runs/wave-20260926-1421pdt/dp1/blind/
(JUDGE_BRIEF_DP1.md, SEALED_MAPPING_DP1.md, LISTENING_DP1.md,
pair_RGLaA4.wav, pair_41tIYv.wav),
docs/lab/rsi/runs/wave-20260926-1121pdt/dp1/DP1_DOSSIER_1121.md,
docs/lab/rsi/runs/wave-20260926-1121pdt/debate/JUDGE_RULINGS.md,
plus live per-entry evidence in /tmp/fb1421/E and direct git/sha256sum
spot checks by this skeptic.

His six governance rulings are untouched. His sealed-pair verdicts are
unchanged. Nothing from his frontier work is re-litigated here.

## Motion 1: Spot re-run CONFIRM of the 1121pdt battery verdicts

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

Answer: the three spot re-run entries are 1121pdt artifacts, not new:
spot-a at the 1121pdt task-pinned HEAD
02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2 (live), spot-b at
bd30978748fa83bbea6e423a7074cf32b7304291 (fixture), spot-c at
5802fec8401f28b4036b0dd5ebb23905610cab57 (pull/1/head extraction
FAIL). New versus inherited: the re-run harness invocations are new;
every verdict being confirmed is inherited from 1121pdt. The fixed sed
parser is the new element under test.

Attacks:

- (A1) Three of 38 entries is a thin sample; "confirm" overclaims what
  three runs can cover. This attack FAILS on the judge's own terms. The
  1121pdt judge wrote the spot re-run requirement into the verdict line
  himself: "before the next wave's battery cites these results, a spot
  re-run (one live entry, one fixture, one extraction FAIL) with the
  fixed parser must confirm them." The worker ran exactly that design
  (one live, one fixture, one extraction FAIL) at the correct 1121pdt
  heads with the fixed parser from the start. The thin sample was his
  specified design, not the worker's improvisation.
- (A2) Does "confirm" cover the uniformity claims across 36, or just
  the 3? The spot re-run alone covers only the 3. But the 1421 full
  battery re-tested all 40 entries at current heads with the fixed sed
  parser, so the uniformity claim now rests on fresh full-battery
  evidence, not on the 3-entry sample. The spot re-run requirement is
  arguably redundant this wave. Attack FAILS as a blocker; it lands
  only as a scoping note: read "confirmed" as "the three sampled
  1121pdt verdicts are confirmed," not as "all 38 were spot re-run."
- (A3) The spot re-run ran at 1121pdt heads, so it confirms nothing
  about the current wave's verdicts. True and harmless: confirming the
  1121pdt verdicts was the requirement; the current wave's verdicts are
  covered by the full 1421 battery. Attack FAILS.

What I verified: the three spot entries' RESULT.txt files in
/tmp/fb1421/E (spot-a-1121-live verdict=PASS at ref 02ee5ae59d,
spot-b-1121-fixture verdict=PASS at ref bd3097874,
spot-c-1121-pull1 verdict=EXTRACTION_FAIL at ref 5802fec8), all with
b2_bin_a_sha256 =
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
on the two PASS entries.

Recommendation: CONFIRM stands. Motion 1 attacks do not land.

## Motion 2: Fork battery CONFIRM [RE-CERT], 40 entries, 38 PASS, 2 FAIL

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

Answer: 34 of 40 entries are fixtures (unchanged SHAs re-tested for
coverage); 6 live entries cover 5 unique live commits
(b6f96edaf8d3e7d422aa0f81db9abc91810671c6,
746ff60ba16d18c36db2ccd4394cbb9db9d6266d,
f67e989339a67b882f72378b39fad342a1aa6d9e,
006dfe027944f395a47ae8fe6d1e3329a9d7634e,
7c19065e7b1ce13f6479ba50b4f35e110156c734). The genuinely new
information this wave is 5 unique live commits, not 40 entries. The
merged-in upstream commits are treated as CLOSED and certified for
toolchain/extraction stability only, per the scope stamp.

Attacks:

- (B1) The headline 38/40 inflates coverage; duplicates are disclosed
  (P8: f67e98933 tested twice, 99143222 three ways, bd3097874 five
  ways, plus f875b3417 and 3947dca1a pairs) but the headline still
  travels. Attack PARTIALLY LANDS on framing. The duplicates are named
  explicitly with SHAs, so nothing is hidden, and the live/fixture
  split is stated (6 live, 34 fixture, 32 unique commits). But a reader
  citing "38/40 PASS" as 38 independent toolchain confirmations would
  be wrong; it is 32 unique commits, 5 of them new this wave. The
  evidence file is honest; the headline needs the caveat attached every
  time it is cited.
- (B2) The two pull heads (pull/1/head 5802fec8, pull/2/head 4b76bb59)
  remain uncovered, fourth wave running. Attack LANDS as a coverage
  hole, but it is disclosed and explained: both trees lack the pinned
  toolchain path (non-TNN research-doc repos), so the battery cannot
  test them until their trees gain the path. This is a limit of the
  instrument, not a regression. I verified pull/1/head's extraction
  failure independently via the spot-c RESULT.txt (EXTRACTION_FAIL at
  ref 5802fec8).
- (B3) The uniformity claims (single distinct znc/probe/bin shas across
  38) rest on per-entry evidence files that live in /tmp/fb1421, which
  is not committed. Attack LANDS as a P14 inspectability gap: the
  committed record (FORK_RESULTS_1421.md alone) holds only the summary,
  repeating the 1121pdt incident-2b pattern the judge flagged. However,
  I independently re-verified the uniformity claim this wave while the
  evidence still exists: across all 43 RESULT.txt files in /tmp/fb1421/E
  (40 entries plus 3 spot re-runs), verdict counts are 40 PASS and 3
  EXTRACTION_FAIL; the znc sha is single-valued
  (498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
  the probe sha is single-valued
  (3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919),
  the B2 bin sha is single-valued
  (75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2),
  and neg1_e0002_hit=1 on every tested entry. The numbers check out;
  the archival gap does not.
- (B4) Spot-check of the pinned toolchain: I ran sha256sum on the
  working-copy znc myself:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  matching the pin. Attack (divergent toolchain) FAILS.

Recommendation: CONFIRM stands, with two standing caveats to carry:
cite "38/40" only with the duplicate/fixture caveat, and the
per-entry evidence should be committed or archived before /tmp is
reclaimed (P14).

## Motion 3: tnn_chat FIT CONFIRM [RE-CERT] carry-over per P12

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

Answer: all ten chain inputs are inherited frozen artifacts (baseline
and decline instruments, kb.txt, gaz.txt, two R33 support sources,
pinned znc, three fixtures), certified byte-exact at HEAD b6f96edaf.
New this wave: only the carry-over certification itself (sha checks,
diff checks, no re-run). Determinism evidence is inherited from the
wave-20260925-1421pdt fresh re-run (2/2 binary reproducibility, 9/9
rerun pairs byte-identical, KB1 30/30, KB2 17/17, KB5 10/10), cited per
P12 rather than re-run.

Attacks:

- (C1) Carry-over means no fresh re-run; the determinism evidence is
  one wave old. Attack FAILS as a blocker. The qualification is stated
  openly in the verdict line itself ("without a new re-run") and in
  precondition 4 ("no fresh re-run was performed for this carry-over;
  the determinism evidence ... is cited instead, per P12"). P12 is the
  standing precedent for exactly this. The precondition that justifies
  carry-over (byte-exact chain inputs, zero chain-path diff across the
  60-commit range) is evidenced, not asserted.
- (C2) The znc mode-only change (origin 100644, merge 100755).
  Disclosed in precondition 3 with the blob byte-identical in all three
  (blob 611b7f0c215385b7d3073bbebbf6078224c70b4c, sha256 matching the
  frozen pin 498abcb5...). A mode bit is not a content change. Attack
  FAILS. I re-verified the working-copy znc sha myself (498abcb5...,
  matches).
- (C3) The R33 support sources live under
  docs/lab/bytegen/authority_law/dialogue/, an import target path
  rather than the fit_authority path itself; is the chain-input
  enumeration complete? The FIT worker enumerates them as chain inputs
  5 and 6 with frozen shas (e6379ddb..., 9824f6db...), and precondition
  3's diff explicitly covers the bytegen dialogue path. The merge range
  diff over docs/lab/rsi/ is empty, and the authority files were
  verified present and byte-exact. Attack FAILS as gaming; the
  enumeration is complete on the evidence. Residual note: I verified 3
  of the 10 shas independently (tnn_chat.zag c0776ad6..., kb.txt
  3ef27296..., znc 498abcb5..., all match); the other 7 rest on the
  worker's table.
- (C4) Is the carry-over qualification "recorded openly enough"
  (P12/P16)? Yes: the verdict line, the basis section, and the python-
  contact statement all state it. Attack FAILS.

Recommendation: CONFIRM stands. Motion 3 attacks do not land.

## Motion 4: Interactive TNN CONFIRM [RE-CERT], no change

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

Answer: nothing new is under judgment. The survey re-verifies inherited
artifacts: frozen FIT instrument sources and binaries (shas
re-checked), the pinned znc, and the absence of any source-level
chat/REPL entry point in src/zag/ or units/. The one new commit in the
merge range touching this question (3a31cc183, docs/lab/ORIENTATION.md)
is an orientation doc outside src/ and units/, noted and closed.

Attacks:

- (D1) The survey is a grep, not execution; a grep for
  chat|repl|interactive plus entry-point signatures could miss a REPL
  with unconventional naming. Attack LANDS WEAKLY in principle but
  FAILS as a blocker this wave: the merge range
  746ff60ba..b6f96edaf contains zero commits touching src/ or units/
  at all, so no new interactive surface could have arrived through the
  merge, and the pre-merge tip was already surveyed. The grep's
  weakness is bounded by the empty delta.
- (D2) The frozen binaries were file/sha-checked, not executed, yet
  they are RUNNABLE chat instruments (tnn_chat baseline and
  decline-gate binaries). The headline "no interactive TNN exists" is
  true only for source-level entry points; runnable probe chats do
  exist and were not executed this wave. Attack LANDS as a framing
  caveat. The doc itself discloses this (the EXISTS list names both
  binaries with shas), so there is no deception, but the verdict line
  should keep the "source-level" qualifier every time it is cited.
  Not executing them is consistent with the standing rule (probe chats
  are supervised red-team work, scheduled only on change), and the
  survey revealed no change.

Recommendation: CONFIRM stands, with the standing "source-level"
qualifier preserved. Motion 4 attacks land only as framing caveats.

## Motion 5: No new candidates, CONFIRM stand-down

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

Answer: the survey window (2026-09-26 08:21 to 14:21 PDT) produced no
new prereg, no new design file, no new candidate. The only
candidate-adjacent build is the judge-required DP-1 sealed blind pair
(queue-readiness work for an already-certified candidate, not a new
mechanism). Everything else in the window is prior-wave evidence,
debate records, and the 60-commit merge of upstream work, which is
his frontier work treated as CLOSED per standing rule.

Attacks:

- (E1) Is the lane survey exhaustive enough to justify standing down
  every lane? I checked independently and honestly. Within
  docs/lab/rsi/: my `git diff --name-status
  746ff60ba..b6f96edaf -- docs/lab/rsi/` is empty, and no
  prereg/design-named commits appear in the window. The survey's
  find/grep/log checks corroborate. There IS new mechanism-like
  material in the merge range, but it sits under
  docs/lab/audio_longhorizon/ (phase3 PREREG.md, reemit63.zag, resid3.zag,
  planner PLANNER_DESIGN.md), docs/lab/destruction-pricing-governance/
  (PREREG_GOV_ABC_FROZEN.md, strength_core sources), and
  docs/lab/audio/exact_replication_phase2/ (rb_longmem6.zag and
  others). The survey names this class of material in its frontier
  note and treats it as CLOSED per the standing rule (his own work:
  RECTANGLE FIX honest upscale, H.264 CAVLC, MP3 oracle, Fusion Fork,
  pig-front, AUDIO SEMANTIC-GROWTH phase 3). The survey did not miss
  it; it classified it correctly. Attack FAILS. No genuinely new,
  ungated loop-lane mechanism exists this wave.
- (E2) Boundary risk: the 1121pdt judge ruled that advancing adoptions
  while his six governance rulings are open gambles with his
  boundaries. Does anything this wave tempt that boundary? No. Nothing
  was adopted, nothing was queued to him, DP-1 stays HELD, and the
  six rulings remain open and untouched. Attack FAILS; the wave is
  clean on boundaries.

Recommendation: CONFIRM stand-down. Motion 5 attacks do not land.

## Motion 6: DP-1 sealed blind A/B pair (queue-prep deliverable)

Provenance probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?"

Answer: the pair WAVs are copies of renders first rendered in
wave-20260925-1721pdt: baseline dp1_baseline.wav
(a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c)
and variant dp1_variant_r1.wav
(994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771),
certified by the 1121pdt judge as MODIFIED CERTIFICATION, metrics
READY-FOR-JUDGE [NEW], built on the D-AUD-3 substrate (synth.zag
f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055,
vendored byte-identical as sub/synth_base.zag). New versus inherited:
the NEW_KNOWLEDGE_CLAIM is the time-varying propagation delay doppler
flyby mechanism (tagged [NEW]); the D-AUD-3 bed is inherited. The
dossier's provenance verdict is COMPLETE AND CLEAN with no recycled
render. New this wave: only the blind packaging (coded filenames,
sealed mapping). I verified the pair WAVs byte-identical to the
certified hashes with sha256sum myself: pair_RGLaA4.wav =
a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c,
pair_41tIYv.wav =
994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771.
Both files are the same byte size (3704444), no labels in the coded
filenames.

Attacks, hardest scrutiny here:

- (F1) THE BLIND SEAL LEAKS. This attack LANDS, and it is the most
  serious finding in this report. JUDGE_BRIEF_DP1.md asserts "Judge
  brief carries no assignment." That is false when the brief is read
  whole. The brief's provenance header (quoted verbatim, as required)
  contains RENDER_SHA:
  994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771,
  which is the variant's sha. The brief's own "The pair" table maps
  pair_41tIYv.wav to 994f9402... and pair_RGLaA4.wav to a32ff18....
  Any reader of the brief can therefore recover the mapping:
  pair_41tIYv.wav is the variant. The blind is broken by the brief
  itself, not by any external file. SEALED_MAPPING_DP1.md staying
  sealed does not help, because the information it seals is already
  derivable from the brief. The pair is built correctly, but the
  protocol is not blind as packaged.
- (F2) Provenance header verbatim check. I diffed the brief's quoted
  header against DP1_DOSSIER_1121.md section 1 (normalized line joins):
  content-identical, field for field, including COMPONENT_LINEAGE with
  all statuses and Tag: [NEW]. The only difference is formatting (the
  dossier's line breaks joined with "; " in the brief). Attack on
  verbatim fidelity FAILS; the quote is faithful.
- (F3) S11-AUD overlap verbatim check. The brief's quote matches the
  1121pdt judge's line 191 ruling verbatim: "S11-AUD is time-invariant
  filtering (fixed taps, fixed RT60); DP-1 is time-varying delay from
  source motion producing pitch shift that no static filter can
  produce; no shared code, parameter, or measurement; a real judgment
  call for his ears." Attack FAILS; the overlap travels correctly.
- (F4) LISTENING_DP1.md labels its files (baseline dp1_baseline.wav,
  variant dp1_variant_r1.wav) but contains no coded filenames and no
  shas, so it does not by itself leak the coded mapping. However, the
  1121pdt judge already ruled LISTENING_DP1.md is "instructions with
  labeled files not a sealed protocol." It should not travel with the
  pair. Attack lands as a packaging rule, already anticipated by the
  judge.
- (F5) Queue disposition. The wave agenda's HELD condition was "until
  the pair exists." The pair now exists as files, but per F1 the
  protocol is not yet a valid blind, and per the 1121pdt judge's M1
  ruling, queueing for his ears was HELD outright with presentation a
  future-wave queue decision ("nothing from DP-1 reaches Micah this
  wave"). The survey correctly recommends HELD this wave. The agenda
  condition is necessary but not sufficient: the seal must actually
  hold before presentation.

What the pair certification covers: the WAVs are byte-identical to the
certified renders (verified by me), the coded filenames carry no
labels, the mapping file is correctly withheld from the judge packet,
and the codes are consistent with /dev/urandom alphanumerics (stated,
not independently auditable). The build is certified; the brief is
not seal-safe.

Recommendation: DP-1 stays HELD this wave, as the survey recommends.
Before any future presentation, repair the seal leak: either strip the
per-file sha table from the judge-facing brief (keep shas in a
separate integrity record that does not travel with the brief), or
re-code the pair with fresh randomization after the brief is fixed, and
re-verify no other field in the brief (provenance header included)
identifies either file. Do not present the current brief plus pair
together to his ears.

## Overall

Motions 1 through 5: skeptic attacks do not land as blockers; the
CONFIRM verdicts stand, with the carried caveats noted (headline
framing on the battery, P14 archival of per-entry evidence,
"source-level" qualifier on the interactive negative).

Motion 6: the DP-1 pair build is certified (byte-identical WAVs,
verified by me), but the blind protocol as packaged leaks the mapping
through the judge brief itself. This attack LANDS. DP-1 remains HELD;
the seal must be repaired before any presentation to his ears.

His six governance rulings remain open and untouched by everything in
this report. No loop artifact this wave re-litigates his frontier work.

Zero-Python attestation: no Python ran in this skeptic's work. All
checks were POSIX shell, git (read-only), sha256sum, grep, sed, awk,
find, ls, cmp, and file reads.
