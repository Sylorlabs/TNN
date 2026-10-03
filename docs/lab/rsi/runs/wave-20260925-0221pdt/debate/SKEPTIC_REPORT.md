# SKEPTIC REPORT: wave-20260925-0221pdt debate

Role: SKEPTIC (red-team). Working copy ~/workspace/tnn-rsi, branch
tnn-native-lab. Method: read all four committed evidence files, then
independently re-verified the load-bearing claims with git and shell
reads only. Disclosure (recorded per judge ruling wave-20260925-0221pdt):
one read-only python3 one-liner was used to character-check this draft
file itself for dashes; no wave evidence was read or written by Python,
and the zero-dash result was re-confirmed with pure shell. Nothing was
committed. The sealed judge queue, Micah's frontier files, and the
governance ruling items were not touched.

## Provenance probe (verbatim)

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

Answers from the committed record, item by item.

1. D-VID-1 V3, verdict DEAD [NEW]. The artifacts under judgment are the
48 variant frames rendered from ocean_dvid1_v3.zag, RENDER_SHA
c654ebe4ba3a96361324fdcf362324da30ef857feed4a60202d07d4e00d3827c,
wave wave-20260925-0221pdt, frozen manifest MANIFEST_V3_SHA256.txt.
NEW: the in-plane geometry-churn displacement block, implemented fresh
this wave from the frozen prereg 0ba679b11; the independent red-team
diff against the baseline ocean.zag shows exactly three hunks (file
header comment lines 3-15, the o_sin_bh / o_sin1000 helpers lines
235-245, the churn block in o_shade_water lines 523-592), and the
v3_verify.zag (sha 7f84fbdf...) and v3_sha.zag (sha b5640570...)
tools built this wave. INHERITED, byte-identical to the 2026-09-22
D-VID-1 baseline: scene, camera, 48 frames, 1024x1024 24-bit BMP,
breakup sampling coordinates and seeds (bup 51, abup 52, sbup 54),
the bfade fade law, capth, streak ridge scale 36 seed 53, ring scale,
normal perturbation, base color, specular, fog, dither. Baseline
ocean.zag sha256
9df721dadc6c1de380ba8130958b86a2ff19e22cce4b3be576501f3ec0a8ef13,
unmodified.

2. Fork battery, 27/27 PASS [RE-CERT]. The artifacts under judgment are
FORK_RESULTS_0221.md and this wave's enumeration. NEW: this wave's
fresh branch/worktree enumeration and the per-fork results. INHERITED:
the pure-Zag harness fork_battery.zag extracted read only from archive
branch tnn-native-lab-wave-archive-20260923-2321pdt (sha
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738),
whose rebuilt binary is byte-identical to last wave's (a2e6284c...);
the shell driver adapted from the frozen 2321pdt driver.

3. tnn_chat FIT [RE-CERT]. The artifacts under judgment are
TNCHAT_FIT_0221.md and this wave's fresh re-run. NEW: the fresh re-run
on HEAD b4507fb22 after carry-over precondition (2) failed. INHERITED:
the entire frozen chain, each element sha-pinned and re-verified at
extraction: baseline tnn_chat.zag (c0776ad6...), decline
tnn_chat_decline.zag (a87011fe...), R33_NATIVE_IO_V1.zag
(e6379ddb...), R33_NATIVE_SHA256_V2.zag (9824f6db...), kb.txt
(3ef27296...), gaz.txt (b75fd113...), the three fixtures (936c35e1...,
730e2d24..., b60198b0...), and the pinned znc (498abcb5...).

4. CV-1 fallback/fail-closed MEASUREMENT [NEW]. The artifacts under
judgment are MEASUREMENT_CV1_FALLBACK_0221.md and the sealed 24-probe
set (PROBES.md sha 56fbc9b8..., KEY.md sha 77716c0f...). NEW: the
24-probe sealed set authored post-freeze from
PREREG_CV1_FALLBACK_0221.md sections G1-G6, and this wave's scoring.
INHERITED: the adopted 1721pdt cv1c.zag implementation, byte-unchanged
(sha 6d8fb9f0...), rebuilt with the pinned toolchain to a binary
byte-identical to the adopted one (710d8bc5...).

## Attack (a): the 572/572 tie is a shared verifier defect; DEAD vs UNVERIFIABLE

Attack developed: an exact pair-by-pair tie (47/47 pairs identical,
T1-GC 572 pm both) is the signature of a verifier that reads one
sequence twice, or whose flip counting is broken in a way that cannot
distinguish the inputs. If the verifier is defective, the measurement
is UNVERIFIABLE, not DEAD.

Verdict on the attack: REJECTED. The committed evidence defeats it on
four independent points.

First, the same verifier binary on the same run demonstrably processes
the two sequences as distinct inputs. T2 per-pair values differ between
A (baseline) and B (variant): pair 4 is 917 vs 916, pair 5 is 917 vs
916, pair 12 is 928 vs 927, pair 13 is 973 vs 972, and the summary
differs (variant max 1074 vs baseline max 1075, mean 976 vs 977). A
verifier that read one sequence twice could not produce these
differences. Second, T3 validates both paths independently:
T3_A_f0=1608, T3_A_f47=1543 against the frozen 1607/1543 (|1| and 0,
within the 10 gate, PASS), and T3_B_f0=1607, T3_B_f47=1543 within 5
percent of the baseline path (PASS). The variant input path is
genuinely exercised. Third, the T1-GC validation gate passes on the
frozen reference: |572 - 580| = 8, within +-25, PASS; a verifier whose
flip counting were broken would not reproduce the frozen 580 baseline
within gate. Fourth, the tie is physically explained, not merely
asserted: the independent red-team review (ffmpeg, not the verifier)
measured foam saturation in the churned sliver (base mean 253.9/255,
v3 mean 254.7/255; only 30 of 4780 sampled foam-channel pixels differ
at f10) and localized the churn footprint to a ~13 px tall sliver
(x 419..1016, y 395..408). Saturated foam has mask 1 in both sequences,
so displaced resampling flips nothing, and the exact tie is the honest
measurement of a null. The verifier itself flagged the zero rather
than hiding it: D1_f10_region_diff_pm=0 with D1_DIAGNOSTIC=FAIL.

On DEAD vs UNVERIFIABLE: UNVERIFIABLE requires compromised evidence.
G-LIVE passes, VKB1 holds (48/48 byte-identical across three renders),
both validation gates pass, and the red-team review found no procedure
defect. The prereg's frozen verdict mapping (G-LIVE passes and any VKB
fails) assigns DEAD. DEAD [NEW] is the correct call.

SUSTAINED sub-finding (design lesson, no verdict change): the frozen
T1-GC region is a 204 px radius screen circle (160 * 920 / vwz at
vwz ~= 720) while the lever's true footprint is a ~13 px tall
foreshortened sliver, so the 1.30x bar was unreachable by geometry,
not just by lever weakness. The bar was frozen and must not be
weakened; the independent redteam already logged this as its confound
1. Fix required: none for this verdict; record the lesson for future
preregs (metric regions must match the lever's actual screen
footprint, or the metric must operate in world space).

## Attack (b): the 2321pdt breach taints the prereg by association

Attack developed: the prereg was certified for carryover in the same
wave that suffered a Python breach, so guilt by association should bar
its reuse.

Verdict on the attack: REJECTED. Judge M4 in the 2321pdt debate ruled
on this exact objection with git-verifiable evidence, and I re-verified
the timestamps: prereg 0ba679b11 was committed ALONE at 2026-09-25
06:47:01 UTC (single-file commit, parent c4f006ea7); my independent git
log on the prereg path shows exactly one commit in history touches it,
so Python never read or wrote the file after freezing; the breach
disclosure was committed at 06:55:45 UTC, 8m44s after the prereg
(BREACH_DISCLOSURE.md places the breach itself at 06:55 UTC), so the
prereg predates the breach by committed timestamp. The voided 2321pdt
implementation was never committed (scratch bytes only, outside the
repo), so no implementation commit could have preceded the prereg; the
0221pdt implementation commit 81e33f192 came at 10:21:13 UTC, strictly
after. The certification's reasoning stands: the voiding operation
must have an object, and the prereg is outside that object set. Taint
by association is not a rule.

SUSTAINED minor finding: EVIDENCE_V3_0221.md and REDTEAM_V3_0221.md cite
the prereg at
docs/lab/rsi/runs/wave-20260924-2321pdt/dvid1_geomchurn_v3/PREREG_DVID1_V3_2321.md,
but the committed path is
docs/lab/rsi/runs/wave-20260924-2321pdt/dvid1_geomchurn/PREREG_DVID1_V3_2321.md
(the _v3 suffix belongs to the 0221pdt run dir, not the 2321pdt one);
and the evidence claims "(328 lines)" while the committed file is 300
lines (328 was the commit's insertion count). Fix required: correct the
path and line count in the wave record (coordinator edit; no evidence
change).

## Attack (c): 22 of 27 are fixtures; live coverage inadequate; hidden CANNOT-CONFIRM

Attack developed: only 5 of 27 forks are live, so the battery is mostly
re-running frozen fixtures, and a CANNOT-CONFIRM could be hiding in
the fixture class.

Verdict on the attack: REJECTED on the substance. The report lists
CANNOT-CONFIRM items: None, and the fixtures are not skipped: every
one of the 27 forks ran the full shell battery and the pure-Zag
harness. Fixtures serve the battery's purpose, which is pinned-compiler
tamper detection per fork, not novelty. Enumeration was fresh this
wave (git branch -a, git worktree list), and every fork whose SHA moved
since last wave is in the live set. The closing origin-tip re-check
held (4050b1097 at run start and at close; I independently confirmed
origin/tnn-native-lab = 4050b1097...). Local HEAD was unchanged during
the run.

SUSTAINED on count honesty: the "5 live" figure includes
origin-tnn-native-lab-runstart-tip, which the report itself admits
"tests the same commit as origin/tnn-native-lab this wave." The
genuinely distinct live forks are 4. Fix required: report "4 distinct
live forks (plus 1 duplicate entry)" for exactness. Coverage remains
adequate regardless, since nothing else moved.

## Attack (d): the FIT re-run's chain is not provably the frozen chain

Attack developed: the merge folded in 115 files; the worker's claim
that they are disjoint from the FIT chain is taken on trust, and the
fresh re-run sourced instruments from a different archive branch than
the designated one.

Verdict on the attack: REJECTED. The fresh re-run was the right call:
carry-over precondition (2) hard-failed because the baseline instrument
tnn_chat.zag is absent from the designated archive branch
(tnn-native-lab-wave-archive-wave-20260924-2321pdt), and the standing
rule forces a re-run on precondition failure, not a waiver. The
re-run's chain is provably the frozen chain: I independently re-hashed
the baseline instrument from the cited 0923-2321pdt archive path
(docs/lab/rsi/runs/wave-20260923-0834pdt/tnn_chat.zag) and got
c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c,
matching the frozen record. The merge-disjointness claim I verified
directly: the e33b5ddb..b4507fb22 merge touched exactly 115 files and
all 115 sit under docs/lab/ambig_1080p, docs/lab/math_logic, or
docs/lab/onebrain (zero paths outside those three), so no FIT chain
path was touched. Results: 2/2 binary reproducibility byte-identical
to the frozen records (20273a99, 1ada2fae); all three output hashes
byte-identical to the prior wave's records (a2ca4dd7, e05fb4ec,
4f1603aa); 9/9 required run-pairs byte-identical; 15/15 runs exit 0
with empty stderr.

Recommendation to the coordinator (not a verdict defect): the
designated archive branch pruned the 09-23 run dirs that held the
baseline instrument, which is why precondition (2) failed. Archive
pruning is degrading the carry-over precondition's future usability.
Freeze the frozen instrument sources into a never-pruned authority
path.

## Attack (e): CV-1 measurement, small set, self-attestation, M5, adoption language

(e1) Adoption language. Verified absent. The document states "It makes
no adoption claim, no readiness certification, and no verdict of any
kind" and closes with "Measurement only. No adoption claim. Baseline
integration remains held pending Micah's Python-mirror ruling." The
only "adopted" tokens refer to the historical 1721pdt implementation.
The baseline-integration hold is respected. Attack REJECTED.

(e2) 24 probes is a small set. The set was authored post-freeze from
prereg sections G1 through G6; the scope (the two never-exercised path
classes named in the 1721pdt verdict addenda) is stated; numbers are
reported with explicit caveats ("records numbers and observations
only"). Small-N is a documented scope limitation, not a defect in the
measurement. Attack REJECTED as an honesty challenge. Standing note:
future measurements should widen the set.

(e3) M5 fired 0/24 on a pre-registered unreachable check, a coverage
hole smuggled as a pass. REJECTED as "smuggled": M5 was pre-registered
as a behavior log with expected 0, and the document states plainly
that "Its firing behavior remains unobserved by probe; only its
silence is measured here." It is not presented as verification of the
fail-closed path. SUSTAINED as a coverage gap: a fail-closed path
whose firing is pre-registered unreachable cannot be probe-verified,
and the unreachability argument is an argument, not evidence. Fix
required: do not cite M5 as verification of the fail-closed path in
any future verdict; a future wave should engineer a fault-injection
probe (for example, deliberately corrupted fact text) to observe the
firing.

(e4) Self-attested author/implementer separation. The report discloses
this honestly ("self-attested (single worker session)"), so there is
no deception. SUSTAINED as a process weakness: future sealed
measurements should use structural separation (different workers for
author and implementer), not self-attestation. Fix required:
coordinator staffing rule for sealed sets.

## Recommendations to the judge

1. D-VID-1 V3: ACCEPT the recommendation DEAD [NEW]. The evidence is
uncompromised, the T1-GC bar was frozen, and the kill is on the bar,
not on the procedure. Record the metric-region geometry lesson for
future preregs. Require the prereg-path citation correction
(dvid1_geomchurn, not dvid1_geomchurn_v3; 300 lines) in the wave
record.

2. Fork battery: ACCEPT 27/27 PASS [RE-CERT]. No CANNOT-CONFIRM. Require
the count correction to "4 distinct live forks (plus 1 duplicate
entry)" in the record.

3. tnn_chat FIT: ACCEPT FIT [RE-CERT] on b4507fb22. The fresh re-run
was mandatory and its chain is independently verified as the frozen
chain. Recommend the coordinator freeze the frozen instrument sources
into a never-pruned authority path, since archive pruning broke
precondition (2) this wave.

4. CV-1 fallback: ACCEPT as MEASUREMENT [NEW], numbers only. No
adoption claim exists in the document, and the baseline-integration
hold pending Micah's Python-mirror ruling is respected. Bar M5 from
being cited as fail-closed-path verification in any future verdict
until a fault-injection probe observes the firing; require structural
author/implementer separation for future sealed sets.
