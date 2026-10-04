# ADVOCATE BRIEF: wave-20260926-1421pdt

Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab. HEAD:
b6f96edaf8d3e7d422aa0f81db9abc91810671c6.

This brief argues FOR each confirmation/adoption on the verdict slate.
All numbers are cited from the wave evidence files, re-read this wave.

## 1. FOR: confirming the 1121pdt fork-battery verdicts (spot re-run)

The spot re-run executed first, before anyone cites the 1121pdt
verdicts, with the sed parser fix in place from the start. Three
entries re-ran:

- (a) live entry, local tnn-native-lab at 02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2:
  harness exit 0, VERDICT=PASS, znc sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  probe sha256 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
  b2_bin_a sha256 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2,
  probe stdout R32_ZNC_PROBE_OK. 1121pdt PASS confirmed.
- (b) fixture entry, wt-forktest-tnn-native-lab at
  bd30978748fa83bbea6e423a7074cf32b7304291: same evidence values,
  VERDICT=PASS. 1121pdt PASS confirmed.
- (c) extraction-FAIL entry, origin pull/1/head at
  5802fec8401f28b4036b0dd5ebb23905610cab57: extraction failed with
  "fatal: path 'src/tools/toolchain/znc_linux_x86_64_abed8aa1' exists on
  disk, but not in '5802fec8401f28b4036b0dd5ebb23905610cab57'",
  VERDICT=EXTRACTION_FAIL. 1121pdt extraction FAIL confirmed, identical
  verbatim cause.

The 1121pdt incident 2 bug (cut -d= -f2 mis-parse) is gone by
construction: this wave's driver parses b2_bin_a_sha256 with sed from
the first run, and the harness prints all B2 key/value pairs on one
line so the old cut semantics could never have been correct. All three
1121pdt verdicts stand on clean evidence. CONFIRM.

## 2. FOR: confirming the fork battery [RE-CERT]

40 named entries, 38 PASS, 2 extraction FAIL. The two FAILs
(rh-pull-1-head 5802fec8, rh-pull-2-head 4b76bb59f) fail at extraction
step one with the identical cause recorded in the 1121pdt, 0821pdt,
and 0521pdt waves: both trees lack the pinned toolchain path (they
carry no src/ directory at all, just non-TNN research documents). This
is a property of those forks' contents, not a toolchain regression,
and they remain uncovered by this battery until their trees gain the
path.

The 38 PASS entries are uniform, grepped across all 38 per-entry
evidence files, not sampled:

- znc sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef on 38/38.
- probe source sha 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919 on 38/38.
- B1/B2/B3 all PASS on 38/38; B2 bin sha 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2,
  matching the frozen value.
- NEG1 discriminates on 38/38 (compile exit 1, E0002 reported).
- NEG2 discriminates on 38/38 (stdout "WRONG OUTPUT", differs from
  expected at char 1).
- Fork-tree test: compiles with the fork's own znc, stdout
  R32_ZNC_PROBE_OK, on 38/38.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 38/38; FAIL on 0.
- Harness rebuilt from the frozen 2321pdt source (extracted sha256
  f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
  matches expected) and byte-identical to prior waves at
  a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66.

Coverage: 6 live entries naming 5 unique live commits
(b6f96edaf, 746ff60ba, f67e98933, 006dfe02, 7c19065e), including the
two queued 1121pdt-close pickups tested for the first time. 34
fixtures cover 18 local branches, 10 remote refs, and 10 worktrees.
All duplicates are named explicitly with SHAs per P8. The closing
tip re-check shows f67e98933 static at start and close, and every tip
enumerated at 1121pdt close (006dfe02, 7c19065e, both ancestors of
f67e98933) was tested. Nothing arrived after the testing window.

The battery certifies toolchain and extraction stability only, per
its scope stamp, and on that scope the evidence is complete and
uniform. CONFIRM [RE-CERT].

## 3. FOR: confirming tnn_chat FIT [RE-CERT] carry-over on b6f96edaf

The certification rests on four preconditions, all checked on working
HEAD b6f96edaf8d3e7d422aa0f81db9abc91810671c6:

1. All 10 chain inputs byte-exact to their frozen shas: both probe
   instruments, kb.txt, gaz.txt, both R33 support sources, the pinned
   znc (498abcb5), and the three probe fixtures. 10/10 PASS.
2. The authority path docs/lab/rsi/fit_authority/ is durable and
   never pruned; git status clean on all chain paths.
3. Across the full 60-commit merge range 746ff60ba..b6f96edaf: zero
   modifications, zero deletions, zero content changes, and no mode
   changes on any frozen chain input, including the merge commit and
   all 59 merged-in upstream commits. The supplementary origin-side
   check shows the pinned znc blob byte-identical (blob
   611b7f0c215385b7d3073bbebbf6078224c70b4c, sha 498abcb5) in both
   parents and the merge; only a mode-only difference (100644 vs
   100755) exists, which is not a content change.
4. Determinism is cited, not re-run, per P12: the evidence was
   certified in the wave-20260925-1421pdt fresh re-run (evidence
   commit 9692f5d1d): 2/2 binary reproducibility PASS, 9/9 rerun
   pairs byte-identical, KB1 30/30, KB2 17/17, KB5 10/10, all runs
   exit 0 with empty stderr.

Since preconditions 1, 2, and 3 hold with byte-exact shas, P12
authorizes citing rather than re-running. The open qualification is
stated explicitly in the FIT evidence file. No fresh re-run was
performed and none is claimed.

The literal scope sentences travel verbatim: this is not a candidate
verdict and it is not merge review of the merged-in work; it certifies
the 38-fact closed-book probe chain only. Nothing about the 59 merged
upstream commits is judged here. CONFIRM [RE-CERT].

## 4. FOR: confirming Interactive TNN [RE-CERT], no change

The survey on b6f96edaf finds:

- Zero chat/REPL/interactive-loop entry points in src/zag/ or units/.
  The single grep hit for "repl" is a verified false positive: the
  substring inside "replay"/"replication" in
  units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md. A follow-up
  grep for entry-point signatures (fn main, stdin, readline,
  read_line, interactive_loop, repl_loop) returned zero files.
- The 60-commit merge range added zero chat/repl-named files in src/
  or units/; git log shows zero commits in the range touching src/
  or units/ at all.
- New origin commit 3a31cc183 ("Investigator orientation: map of the
  live TNN program") adds only docs/lab/ORIENTATION.md (68 lines). It
  sits outside src/ and units/, names no entry point, and adds no
  interactive surface.
- All frozen probe instruments, both runnable reference binaries
  (baseline 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
  decline 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7),
  and the pinned znc (498abcb5) re-verify byte-identical this wave.

No probe chat was run, per the standing rule: a supervised probe run
is scheduled only when the survey reveals change, and the survey
revealed no change. Availability was verified; execution was not
needed. The negative finding of the prior waves stands. CONFIRM
[RE-CERT].

## 5. FOR: confirming the stand-down, no new candidates

The P17 lane survey covered the window 2026-09-26 08:21 PDT to
2026-09-26 14:21 PDT with five independent sweeps: git log on
docs/lab/rsi/ (8 commits), name-status grepped for "prereg|design"
(zero hits), find for prereg/design files (only pre-existing), find
for new files in the window (only evidence batches and the DP-1
blind pair), and git status (scratch plus the DP-1 pair). Result:

- G1: STAND DOWN, no new design idea or re-aimed prereg since 0821pdt.
- D-VID-1: STAND DOWN, no re-aimed prereg with a different mechanism.
- CV-P: STAND DOWN, doubly gated: adoption barred pending Micah's
  governance ruling 6 on Python-mirror-developed logic (still open),
  and no rotated-author re-test exists.
- COMP-2: STAND DOWN, same dual gating as CV-P, plus the P11
  stemmer-contingency unresolved.
- B1-class: STAND DOWN, re-freezes need the P9 bar reformulation
  first, which was not found in the window.
- ST-1: DEAD on pristine evidence, nothing resurrected.

The only in-window candidate-adjacent item is the judge-required DP-1
sealed blind pair, which is queue-readiness work for an
already-certified candidate, not a new mechanism, not a new prereg,
not a new design. No new preregs exist this wave, so the prereg
commit-order self-check is vacuous per P17; it is labeled vacuous,
not a pass. The 1121pdt judge ruled that advancing adoptions while
Micah's six governance rulings are open gambles with his boundaries,
and nothing in this survey changes that. CONFIRM the stand-down.

## 6. FOR: the DP-1 sealed blind A/B pair is certified correct and the queue-prep deliverable is complete

The 1121pdt judge ruled the loop builds a sealed blind A/B pair
(coded files, sealed mapping) before DP-1 reaches Micah's ears. The
pair is now built and certified in
docs/lab/rsi/runs/wave-20260926-1421pdt/dp1/blind/:

- pair_RGLaA4.wav (baseline): sha256 a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c.
- pair_41tIYv.wav (variant): sha256 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771,
  matching the judge-certified DP-1 render sha.
- SEALED_MAPPING_DP1.md holds the coded assignment (RGLaA4 = baseline,
  41tIYv = variant); it stays sealed and does not travel to the judge.
- JUDGE_BRIEF_DP1.md carries no assignment, only the two pair files
  with their shas, the verbatim provenance header, and the verbatim
  S11-AUD overlap. The brief is explicitly a queue-prep deliverable,
  not an adoption and not a verdict.
- LISTENING_DP1.md is carried byte-identical alongside.
- Both WAVs were copied from the certified source renderings in
  docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/ and verified
  byte-identical via cmp after cp. Codes were drawn from /dev/urandom
  for the blind seal only. Zero Python was used in the build.

The skeptic's provenance probe: "What is the provenance of the
artifacts under judgment, and what exactly is new versus inherited?"
Answer for the DP-1 pair: the variant file pair_41tIYv.wav hashes to
RENDER_SHA 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771,
FIRST_RENDERED_WAVE wave-20260925-1721pdt, with component lineage as in
the dossier (D-AUD-3 substrate synth.zag f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055,
vendored byte-identical as sub/synth_base.zag), tagged [NEW]. The
render is inherited and hash-verified against the certified render;
what is new this wave is the sealed blind pair itself: two coded WAV
files, the sealed mapping, and the judge brief with the verbatim
provenance header and verbatim S11-AUD overlap. The pair is certified
correct, the judge's queue condition is met, and per the 1121pdt judge
DP-1 stays HELD this wave: presenting the pair to Micah is a
future-wave queue decision, not this wave's.

## Boundaries held

Micah's six governance rulings remain open and untouched by this
wave. His sealed-pair verdicts are unchanged. None of his frontier
work (RECTANGLE FIX f67e98933, H.264 CAVLC, MP3 oracle, Fusion Fork B,
pig-front, SEMANTIC-GROWTH, ORIENTATION.md) is re-litigated: it was
treated as CLOSED throughout.
