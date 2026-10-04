# ADVOCATE_BRIEF.md - wave-20260924-2321pdt debate group
## Role: advocate (argues FOR each adoption/confirmation on the slate)

This brief argues for four confirmations, in slate order, on numbers and
committed evidence (commit sha + file cited for every material claim).
Genuine weaknesses are conceded inline; nothing here overclaims.

---

## 1. G1 v3 SUNSHAFTS: CONFIRM DISCARD [NEW] as final

**The motion.** The 1721pdt wave left the worker-reported DISCARD
provisional (no red-team, no debate). This wave, Worker 2
independently recomputed everything from committed records only
(report committed as 5c886fb1f,
docs/lab/rsi/runs/wave-20260924-2321pdt/g1v3_redteam/REDTEAM_G1V3.md)
and found the DISCARD correct with zero CANNOT-CONFIRM items. The
provisional verdict (commit 3b10a4577,
docs/lab/rsi/runs/wave-20260924-1721pdt/g1/VERDICT_G1_V3.md) should now
be confirmed as final.

**The killing numbers, recomputed independently:**

- KB1 determinism: PASS. All three variant BMPs recompute to
  96f3a899ee45155b5272536a25f71614a43ef6bca213a2ab6a4b7fc212ec3cd4,
  byte-identical across var_v3_1/2/3.bmp, matching the committed runner
  record evidence_v3_sha.txt in the implementation commit 39707e077.
- KB2 shaft ratio: CONFIRMED FAIL. Committed verifier output
  evidence_verify_v3.txt records INFO_KB2_RATIO_X10000,10000 = 1.0000
  against the frozen bar >= 1.12 (prereg lines 166-167, confirmed in
  the committed prereg at acf7cedce). Not marginal: the ratio is
  exactly unity, meaning zero mean lift on the kept wedge set.
- KB3 var(dL): CONFIRMED FAIL. INFO_KB3_VAR_X100,0 = 0.00 against the
  frozen bar >= 60.0 (prereg line 168). Not marginal either: variance
  exactly zero, meaning literally no lifted pixel touched any kept
  wedge point.
- KB4: PASS (0.00 <= 1.0). KB5: PASS (0.00 <= 6.0). KB6: PASS
  (acutance base 472 / variant 472, ratio 1.0000 <= 1.10). KB7: PASS
  (0 <= 25). KB8 cost: PASS (baseline 934ms, v3_avg 1964ms, ratio
  2.10x <= 3.0x frozen bar, from evidence_walltime.txt).
- Validator V1-V6: PASS, with kept counts 39/48/64/24 identical in
  both the validator record and the verifier record (the prereg's
  runner cross-check requirement).
- Tripwire: 28476/323997 = 87.89 per mille, inside the bar [50, 150]
  defined in run_g1v3.sh lines 118-130. No bar was weakened: the
  runner file is byte-stable within the implementation commit, and 87
  was never outside the interval.

**The killing geometry, verified by independent byte-level diff:**
the red-teamer diffed committed base.bmp vs var_v3_1.bmp at byte
level (1024x1024 24-bit BMP, bottom-up, row stride 3072) and mapped
differing pixels to image coordinates. Lifted-pixel bbox: x 125..1023,
y 308..458; zero lifted pixels with y < 300. The verifier source
(g1_verify_v3.zag, commit 39707e077, lines 107-108, 193-197)
generates wedge points as x = 110 + t*(r-1)*36, y = 300 - t*36 for
t in 1..8, r in 0..5, so every wedge point has y <= 264. The lifted
band (y >= 308) is disjoint from the wedge set (y <= 264) by
construction. Zero overlap is a geometric certainty given the
committed deterministic generator; 0 of 39 kept wedge points carry
lift. KB2 = 1.0000 and KB3 = 0.00 are exactly consistent with
dL = 0 at all 39 kept wedge points. The 2622 changed-channel bytes
vs the worker probe's 2609 nonzero-luma pixels is a non-material
delta (a few channel changes cancel to zero luma).

**Discipline checks:**

- Commit order PASS: prereg acf7cedce (2026-09-25 00:57:43 UTC) <
  addendum 1da140387 (01:17:00 UTC, committed alone, dated 2026-09-24,
  quoting the coordinator's clarity-gate reading with
  s'(P) = (T(P) - BMEAN_T[b])*1024/BSTD_T[b], SGATE = 1152 verbatim) <
  implementation 39707e077 (01:24:34 UTC); both predecessors are
  merge-base ancestors of the implementation. S10 satisfied.
- Baseline-first invariant PASS: the rebuilt base.bmp recomputes to
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
  byte-identical to the S14 sealed baseline in wave-20260923-2021pdt
  commit a4a42758 (r8c_baseline_1024.bmp and s14_blind/pair_39ca6681.bmp
  both recompute to that hash).
- Purity PASS: no .py files under g1/ or preregs/; grep for python
  tokens finds only self-referential purity statements and the
  runner's own static-check lines. "Python contact: none" CONFIRMED.

**Conceded weaknesses (non-material):**

- The sun-anchoring characterization (77% of lifted pixels within
  200 px of sun S=(110,300)) was not re-derived independently. It is
  a descriptive post-run probe result (probe_lift_v3.zag output), not
  a frozen bar; no verdict depends on it.
- The tripwire bar definition lives in run_g1v3.sh, not in the frozen
  prereg. It is a runner sanity check, byte-stable within the
  implementation commit; nothing was re-interpreted to force a pass.

**Why the line stands down:** the mechanism-miss reading is
consistent with the recomputed evidence (a sector-agnostic
angular-minimum predicate that lifts the region below and right of
the sun instead of the frozen upward wedge fan). Two frozen bars
failed by the maximum possible margin (1.0000 exactly, 0.00 exactly),
so this is not a near miss to patch; it is a design miss. The lane
should stand down until a genuinely new design idea exists, not be
kept warm with micro-variants of the same predicate.

**No provenance header is owed for this item:** the prereg requires
the provenance header on JUDGE_BRIEF.md only if the verdict is
READY-FOR-JUDGE (prereg acf7cedce, lines 190-203). This verdict is
DISCARD, so nothing enters the judge queue.

---

## 2. Fork battery: CONFIRM [RE-CERT] 25/25 PASS

**The motion.** Worker 1 ran the full frozen fork battery this wave
(evidence commit b03063b37,
docs/lab/rsi/runs/wave-20260924-2321pdt/forks/FORK_RESULTS_2321.md):
25/25 forks PASS, shell driver and pure-Zag harness in full
agreement. Confirm the re-certification: the toolchain is healthy.

**The numbers:**

- Enumeration was fresh (git branch -a, git worktree list; no stale
  lists). All 8 local refs tested: tnn-native-lab (ead33399e,
  unchanged during the worker's run), six archive branches including
  the new tnn-native-lab-wave-archive-wave-20260924-1721pdt
  (d24bb4b502022efc675dda80e0e97436acc09278), and
  wave-debate-session-1-backup.
- origin/tnn-native-lab tested at BOTH tips: run-start tip
  14c8838558a29a558a041789189cf05287d98e8a (superseded mid-wave) and
  moved tip 787212443060fe454a8a6a686a90c15994e82d59. Both tested
  read-only, never checked out, never merged. Both PASS.
- Five other remote heads fetched read-only into FETCH_HEAD one at a
  time (no local ref created or updated): fs-gr1 23f6c0f9 (unchanged
  since last wave), main 6e621178 (moved since last wave's f2a0ecfdc24;
  current tip passes), r2-7 2d99d183, reorg/phase-0-1 991432226,
  wg-freeze f875b341. All PASS.
- Seven forktest/* detached worktrees tested read-only (SHAs
  unchanged: main 293602fb1, r2-7 a0e7f8ba2, reorg_phase-0-1 991432226,
  tnn-native-lab bd3097874, tnn-native-lab-remote cea8db22f,
  wave-debate-session-1-backup 3947dca1a, wg-freeze f875b3417). Three
  wave3 worktrees (probe, senses, trades at bd3097874) enumerated and
  tested this wave. All PASS.
- znc byte-identical on every fork:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (25/25). znc_probe.zag sha identical on every fork:
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.
- Frozen invocations per fork: B1 compile+run stdout byte-identical
  to "FORKBATTERY-OK 42"; B2 rerun identical, two recompiles
  sha256-equal; B3 strict check exit 0; NEG1 unterminated-string
  compile and check both exit 1 (fails as required); NEG2 compiled
  and passed check but stdout differed from reference (fails
  byte-compare as required); fork-tree probe printed exactly
  "R32_ZNC_PROBE_OK\n". NEG1/NEG2 discriminated on all 25 forks.
- The rebuilt pure-Zag harness agrees with the shell driver on every
  fork: 25/25 VERDICT=PASS with harness exit 0. The harness was
  extracted read-only from the 20260923-2321pdt archive
  (sha f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
  matching expectation) and the rebuilt binary is byte-identical to
  last wave's build (a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66),
  so harness-build determinism holds too.
- No fork reported CANNOT-CONFIRM. No absent forks vs the brief.
- Purity: no Python interpreter invoked at any point (git, sha256sum,
  cmp, printf, chmod, grep, wc, stat, znc, and the compiled pure-Zag
  harness only). Scratch under ~/workspace/tnn-forkbattery-2321pdt,
  never /tmp.

**Conceded weaknesses (handled correctly):**

- origin/tnn-native-lab moved mid-wave (14c883855 to 787212443) and
  origin/main moved since last wave (f2a0ecfdc24 to 6e621178). The
  worker tested both origin tips read-only and the current main tip;
  nothing was re-merged. Coverage is complete, not lost.
- Git mode drift persists (extracted copies come out 644, some
  worktree copies 660/770; the chmod +x-on-copy workaround recurs).
  It is metadata only: every extracted znc sha256 matches the pinned
  498abcb5 sha.

---

## 3. tnn_chat FIT: CONFIRM [RE-CERT] FIT on ead33399e

**The motion.** Worker 1 re-certified the frozen FIT instrument chain
on the new merge commit ead33399e (evidence commit c4f006ea7,
docs/lab/rsi/runs/wave-20260924-2321pdt/chat_fit/TNCHAT_FIT_2321.md).
Confirm the FIT re-certification with its traveling caveats.

**The numbers:**

- Binary reproducibility 2/2 PASS. Decline rebuild sha256
  20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7,
  byte-identical to the frozen 20273a99 record. Baseline rebuild
  sha256 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
  byte-identical to the frozen 1ada2fae record. STOP condition did not
  trigger.
- Source verification before build, all from the 20260923-2321pdt
  archive and matching frozen shas: baseline tnn_chat.zag c0776ad6...,
  decline tnn_chat_decline.zag a87011fe...,
  R33_NATIVE_IO_V1.zag e6379ddb..., R33_NATIVE_SHA256_V2.zag (HEAD copy)
  9824f6db...; HEAD's canonical docs/lab/dialogue/kb.txt 3ef27296...
  and gaz.txt b75fd113... matched their canonical shas. 38 facts loaded
  at startup on every run.
- KB1 re-decline (30 adversarial out-of-KB turns, 3 runs): 30/30
  specific declines on every run (26 turns "My knowledge base contains
  nothing about ...", 4 turns "No knowledge-base fact connects/covers
  ..."), 0 blanket refusals. Output sha256
  a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308
  on every run, byte-identical to the prior wave's recorded output.
- KB2 in-KB (17 turns, 3 runs each binary): 17/17 answered, 0 declines,
  output sha256 e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264
  byte-identical to the rebuilt baseline binary (zero regression).
- KB5 no-decline-gaming (10 turns, 3 runs each binary): 10/10 answered,
  0 declines, output sha256
  4f1603aa2a798a97679e91f54c0614d0de8465856a982a61debc54bc4670e88d
  byte-identical to the baseline binary.
- Rerun determinism: 9/9 required run-pairs byte-identical (r1/r2,
  r2/r3, r1/r3 across all three fixtures); the six baseline run-pairs
  also byte-identical. All 15 runs exited 0; all stderr logs empty.
- No Python used anywhere (shell only: extraction, building, running,
  greps). Nothing was pushed to GitHub.

**Literal scope (this is what the FIT certifies, and nothing more):**
the 38-fact closed-book probe chain on merged HEAD ead33399e. It is
process confirmation of the supervised red-team probe chat, not merge
review of the merged-in work (the merge included Micah's own frontier
work; the FIT shows no observable deviation, and per scope that is a
chain check, not a review of his work). Nothing in
docs/lab/senses/pam-rebuild/ was touched by this work.

**Conceded facts that travel as caveats, not as weaknesses:** the FIT
instrument sources are not in the HEAD working tree; they were
extracted read-only from the frozen archive branch and matched their
frozen shas before building. That is the frozen design (archive
sources + canonical HEAD KB files), and the byte-identical rebuilds
and outputs confirm the chain is stable. The traveling caveats stand
verbatim: the chat is a closed-book probe instrument over a fixed
38-fact KB, not an open-domain conversational model; the decline
binary is a supervised red-team probe instrument, not a general
interactive TNN; no live learning, no open-domain conversation.

---

## 4. D-VID-1 V3 (geometry-churn video lever): CERTIFY the frozen prereg (0ba679b11) as prereg-only; record the breach; VOID the implementation evidence

**The motion.** Three distinct deliverables, three distinct verdicts:

1. The frozen prereg commit 0ba679b11 (0ba679b1131b438552f209cda9ccc615849c3dc8)
   is CERTIFIED as a prereg for a future wave to implement (the S8
   return path). It was frozen and committed ALONE at 2026-09-25
   06:47:01 UTC (file written 06:46:50 UTC), strictly before any
   implementation file (ocean_dvid1_v3.zag created 06:48:30 UTC) and
   strictly before the breach (~06:53 UTC). Python never touched it.
2. The breach is recorded: Worker 3's self-disclosure is committed as
   ca1d4a13a (docs/lab/rsi/runs/wave-20260924-2321pdt/dvid1_geomchurn/BREACH_DISCLOSURE.md).
3. The wave's implementation/evidence phase is VOID as wave evidence
   under the prospective 0521pdt M4 R1 Python-anywhere rule. No verdict
   is rendered on V3. No sealed pair.

**Provenance header (quoted verbatim from the frozen prereg,
PREREG_DVID1_V3_2321.md, commit 0ba679b11), because the standing rule
requires verbatim provenance quotes when discussing a candidate:**

- "RENDER_SHA: (to fill at implementation; sha256 of the frozen variant generator source ocean_dvid1_v3.zag, 64 hex chars)"
- "FIRST_RENDERED_WAVE: wave-20260924-2321pdt"
- "COMPONENT_LINEAGE:
    - D-VID-1 V1 (flow-advected foam breakup): DEAD [NEW], wave-20260923-2321pdt. Killed on frozen T1 bar: variant 606 vs baseline 580 per-mille foam flips, ratio 1.045 against bar <= 0.700.
    - D-VID-1 V2 (co-rotating foam breakup): DEAD [VOID], wave-20260924-0521pdt. Analytic no-op proof: bfade = o_clamp01k((200 - wz) * 1000 / 140) = 0 for wz >= 200; vortex disc wz 560..880, so every V2-retargeted term is gated dead (bupm = 1000, streak multiplier = 1, abupm dead code); ocean.zag diff exactly three hunks. Wave evidence VOID on a mid-wave python3 heredoc touching v2_verify.zag (frozen VKB5).
    - Whirlpool SCOOP: DISCARDED.
    - Whirlpool surface-planform: READY-FOR-JUDGE, QUEUED-UNJUDGED."
- "NEW_KNOWLEDGE_CLAIM: In-plane deterministic displacement of disc foam geometry (not breakup sampling) raises screen-space foam boil by at least 30 percent over the rigid-sweep baseline while holding the V-TEMP, V-SHARP, determinism, and cost bars, giving the loop a live non-rigid churn lever for whirlpool foam."

**Why the prereg satisfies the M4 R3 reopen condition:** the 0521pdt
debate M4 R3 closure reads "DEAD is the coordinate-retargeting of
breakup sampling for disc foam churn (bfade = 0 kills every retargeted
term). OPEN under a fresh prereg only: (a) disc foam churn via a
DIFFERENT mechanism (geometry churn), or (b) a redefined goal." This
prereg takes path (a) explicitly: in-plane deterministic displacement
of disc foam geometry via a frozen sine displacement field
(Bhaskara-I o_sin1000, amplitudes 22/14/20/12 world units, gated
r <= 150 full / r >= 190 zero), with bup/sbup/abup keeping exact
baseline sampling coordinates and seeds (51, 54, 52) and the bfade
fade law untouched. It is a genuinely new mechanism, not a re-freeze
of V1/V2. The prereg also satisfies S8's new-prereg requirement, and
the VKB5 bar plus the explicit "No Python is authorized by this
prereg... Any Python contact with a new wave artifact voids its wave
evidence (M4 R1, prospective)" closes the void-on-sight governance
question: this prereg pre-authorizes no Python anywhere.

**The breach, stated plainly:** exactly one python3 heredoc (the full
command line is in BREACH_DISCLOSURE.md), executed ~06:53 UTC from
/home/hatch/workspace/tnn-frames/dvid1_geomchurn, read and wrote only
a scratch byte-copy (probe.zag) outside the repo, inserted
_zag_print debug statements, and was deleted via rm immediately after
the breach was recognized. It did not read, write, analyze, or
otherwise contact: the prereg file, ocean_dvid1_v3.zag, substrate/,
v3_bin, any frame BMP, any other run-dir file, or anything under
~/workspace/tnn-rsi. The qualification is disclosed honestly:
probe.zag was a byte copy of ocean_dvid1_v3.zag, so Python processed
bytes derived from a wave artifact, but only in a disposable scratch
copy that generated no evidence.

**Argue (a): the breach was handled exactly as the standing rules
require.** Immediate self-disclosure, exact command line recorded,
the complete read/write surface enumerated, the touched scratch copy
deleted, the post-breach copy recreated with cp (no Python), no
further Python this wave, no cure attempted (S3 honored). The worker
did not hide it, did not minimize it in the disclosure, and did not
attempt to salvage the voided phase. This is what the rules exist for:
disclosure within the hour, evidence preserved for the record.

**Argue (b): the frozen prereg, never touched by Python and frozen
before the breach, should be CERTIFIED as a prereg for a future wave
to implement.** The Python-anywhere rule voids wave evidence; it does
not reach back in time to void a prereg frozen alone at 06:47:01 UTC,
six minutes before the first implementation byte and the first
Python contact. Voiding the prereg too would punish rule-following
(the breach was self-disclosed precisely because the prereg's own
VKB5 demanded it) and would erase a genuinely new mechanism that
satisfies M4 R3. The S8 return path is exactly this: a certified
frozen prereg that a future wave implements clean. Note also that no
verdict is rendered on V3: the V3 mechanism remains unjudged, not
dead, and no sealed pair is prepared.

**Argue (c): no new standing rule is needed beyond noting this as
precedent that pre-breach frozen preregs survive.** The existing rules
already produced the correct outcomes: M4 R1 voided the tainted phase,
VKB5's self-authorizing void clause fired as written, S3 prevented any
cure attempt, and the disclosure was committed. The one open question
(pre-breach frozen preregs) is settled here: they survive, certified
prereg-only, as the S8 return path. Record it; do not legislate
further.

**Conceded weaknesses (genuine):**

- The breach is a real Python-anywhere violation under the literal
  M4 R1 reading, even though no wave artifact was touched. The
  advocate does not minimize this: the voiding of the
  implementation/evidence phase is correct and complete.
- Post-breach, the worker recreated the scratch copy with cp and
  continued debugging before recognizing the void. All post-breach
  work is voided as wave evidence regardless of its content.
- The prereg certification buys nothing yet: V3 is unimplemented and
  unjudged, and the lane returns only under the frozen prereg in a
  later wave. Certification preserves the option; it does not adopt a
  candidate.

**Verdict tags defended:** D-VID-1 V3 prereg CERTIFIED (prereg-only);
implementation evidence VOID; no verdict on V3; no sealed pair.

---

## Summary of the advocate's position

| # | Item | Motion defended |
|---|---|---|
| 1 | G1 v3 SUNSHAFTS | CONFIRM DISCARD [NEW] as final; lane stands down until a genuinely new design idea exists |
| 2 | Fork battery | CONFIRM [RE-CERT] 25/25 PASS; toolchain healthy |
| 3 | tnn_chat FIT | CONFIRM [RE-CERT] FIT on ead33399e, with traveling caveats |
| 4 | D-VID-1 V3 | CERTIFY frozen prereg 0ba679b11 (prereg-only); breach recorded at ca1d4a13a; implementation evidence VOID; no verdict on V3 |

The skeptic may attack the handling, but the numbers hold: KB2 1.0000
against 1.12 and KB3 0.00 against 60.0 are kills, not near misses; 25/25
fork PASS with both harnesses in agreement is health, not luck; the FIT
numbers are byte-identical down to the output shas; and the prereg's
6-minute head start on the breach is a committed timestamp, not a claim.
