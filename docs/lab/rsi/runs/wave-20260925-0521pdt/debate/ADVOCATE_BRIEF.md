# Advocate Brief, wave-20260925-0521pdt

Wave: wave-20260925-0521pdt
Debate group, depth 2/2. Role 1 of 3: ADVOCATE.
Job: argue FOR each adoption, and the strongest honest case for each
coordinator-recommended verdict. Nothing here weakens a frozen bar.

## Item 1: Fork battery CONFIRM [RE-CERT], 28/28 PASS

The case for CONFIRM:

1. Full enumeration, fresh, this wave. The worker ran `git branch -a`
   and `git worktree list` fresh and matched every enumerated fork
   against the brief: no brief-listed local branch absent, no unlisted
   local branch present. That is the exact discipline the fork battery
   exists to enforce.

2. All 28 forks PASS the full shell battery (B1, B2 rerun, B2
   recompile-identical, B3 `znc check --strict --no-zagd`, NEG1, NEG2,
   PROBE) and the rebuilt pure-Zag harness (VERDICT=PASS, exit 0) on
   every fork. The harness source extracted from
   tnn-native-lab-wave-archive-20260923-2321pdt hashes to
   f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
   (matches expectation) and the rebuilt binary is byte-identical to
   last wave's build (a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).
   Determinism of the harness build itself is therefore re-confirmed.

3. Pinned znc sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
   verified on all 28 forks, including the two live forks
   (local-tnn-native-lab at 058ee02a8a31efc66fb8e92293d399752ce33a6f and
   the new local-archive-wave-0221pdt at the same commit). The two
   explicit duplicates are named, not hidden: origin-tnn-native-lab-runstart-tip
   duplicates origin/tnn-native-lab (4050b1097941d341c2d02e5efca25fc1877906e5),
   and local-archive-wave-0221pdt duplicates the local run-start tip.

4. No gaps: remote heads were fetched read only into FETCH_HEAD one at
   a time, nothing checked out, nothing written to any origin/* ref, no
   fetch failed. Closing origin-tip re-check shows 4050b1097941d341c2d02e5efca25fc1877906e5
   at both run start and close: the tip did not move. Local HEAD was
   058ee02a8 at run start and at the closing check.

5. Zero Python contact anywhere in the run, explicitly attested. Mode
   drift on the git-extracted znc copies (100755 vs 100644 on some
   archive branches) is disclosed as metadata only; every extracted
   copy sha256-matches the pinned sha, so it changes nothing.

Weakness I concede: the results file is not yet committed. The
coordinator commits after debate, so the confirmation should be
conditioned on the commit landing, but the numbers in the working tree
are complete and auditable.

## Item 2: ST-1 STEREO FIELD [NEW], coordinator says DEAD on KB7

The case for DEAD, on cited evidence:

1. The candidate is genuinely new: a repo survey found no prior
   stereo/binaural/two-channel loop work, and the mechanism (42
   deterministic stems from D-AUD-3 world-element groups with
   world-derived constant-power stereo panning) has no prior judged
   lineage. No S11-AUD stacking, no b_alpha contact.

2. Commit order is clean: prereg d7c5253ad (2026-09-25 12:41:59 UTC,
   alone) strictly precedes addendum A1 44667e16a (12:57:39 UTC, alone,
   numeric bar unchanged at plus/minus 0.5 dB) strictly precedes
   implementation+evidence 40c632bea (13:22:11 UTC). The A1
   clarification was conceived after implementation existed but before
   any implementation commit and before seeing energy numbers; the
   worker disclosed this unprompted.

3. Seven of eight bars pass on hard numbers: KB1 3/3 byte-identical
   (4e9ea742e4b76e646a77aa7763bf754f45e4680592e8187a83ad7117282cb99f),
   KB2 ratio 1.003009 (+0.013 dB) within plus/minus 0.5 dB, KB3 0
   mismatches, KB4 peaks 22236 < 32767, KB5 pure-Zag grep clean, KB6
   corr 0.999605 with RMS -1.76 dB, KB8 1.84x within 3x.

4. KB7 FAIL is on cited numbers: crest ratio 1.203907 (+1.61 dB) vs the
   frozen plus/minus 1.5 dB bar, a miss of 0.11 dB. The frozen verdict
   mapping says any failed bar maps to DEAD.

5. Crucially, the worker refused to rescue the candidate. The
   total-energy reading (-1.40 dB, would PASS) was considered only after
   the numbers were seen, and the worker explicitly refused
   post-hoc re-interpretation as outcome-driven. That is exactly the
   frozen-bar discipline the loop demands: a bar is not re-read to
   force a pass.

6. The mechanism lesson is real and worth recording: constant-power
   stereo panning of world-element stems raises per-channel crest by
   about 1.6 dB versus a mono mix. The bar was calibrated on mono
   precedent (S11-AUD) and appears miscalibrated for stereo. A future
   wave may re-preregister with a stereo-appropriate crest definition.

On the Python touch: the disclosure is on the record (one text edit on
st1_verify.zag, reverted via backup, redone properly). The WAVs and
traces committed in 40c632bea are deterministic outputs of bin_st1, and
the KB numbers are independently re-checkable from the committed
artifacts: crest ratio is a pure function of st1_r1/r2/r3.wav, which
are committed bytes (3,704,444 bytes each) that Python never touched.
The honest verdict on the cited numbers is DEAD, and the evidence for
re-checking survives the incident.

## Item 3: CV-P stemmed-coverage citation gate [NEW], coordinator says PARTIAL

The case for PARTIAL:

1. All nine frozen bars PASS on the sealed 30: 30/30 honest resolutions
   (B1 bar 24), B2 inflection recall 10/10 (bar 8), B3 10/10, B4 10/10
   declines naming every payload word, B5 0 covered-as-uncovered
   violations, B6 17/17 byte parity vs the adopted cv1c on INKB-17, B7
   cost 1.0626x (37044 vs 34864 ops, bar at most 10x), B8 3/3 runs
   byte-identical with zero RNG, B9 seal integrity holds (PROBES.md and
   KEY.md hashes at scoring equal the seal-commit values; the candidate
   never reads KEY.md).

2. Commit order is clean and stronger than required: prereg 397a97c7a
   (12:49:54 UTC, alone) strictly precedes sealed probe set 63cef111d
   (13:09:05 UTC, alone) strictly precedes implementation 358a8013c
   (13:29:24 UTC) precedes evidence 7d845b53a (13:29:33 UTC) precedes
   seal-open log 5a7d6402f (13:30:22 UTC). The probe set was sealed
   before the implementation existed, so the 30/30 cannot be tuned to
   the probes.

3. The diff is 108 lines in frozen scope: the coverage test in
   deliberate_cv1 compares STEMMED content words; the stemmer is reused
   byte-verbatim (diff-verified function-for-function, including the
   write-family exclusion); decline text still cites raw words; the F8
   atomic-claim check still runs on raw canonical text. Static grep
   finds no sealed probe bytes in cvp.zag.

4. Baseline context confirms the gap is real: adopted cv1c declines all
   10 inflected probes on the same sealed set; CV-P converts those 10
   to verbatim answers with 17/17 byte parity and 1.06x cost. That is
   new knowledge: stemming the coverage test closes the inflected-form
   false-decline gap without moving any honesty bar.

5. On red-team: the worker is at depth 2/2 and could not arrange an
   independent reviewer, and the evidence doc says so plainly instead of
   laundering self-review as red-team. The verdict is capped at PARTIAL
   per the frozen mapping (0221pdt judge ruling), self-review ran 9
   structured attacks, and the two residuals are disclosed (single-session
   authorship; tie-break guard covers the known corridor only). The
   queued rotated-author re-test is the correct disposition, and CV-1
   integration stays HELD pending Micah's Python-mirror ruling.

6. On the empty Python invocation: `python3 - <<EOF / EOF` executed an
   empty program, opened/read/wrote no artifact. The operative condition
   under the standing rule is contact with a wave artifact. An empty
   program touching nothing cannot contact anything. No taint.

PARTIAL is the strongest honest verdict available, and it is fully
supported. No adoption is claimed, none is owed, and nothing is
integrated into any live instrument.
