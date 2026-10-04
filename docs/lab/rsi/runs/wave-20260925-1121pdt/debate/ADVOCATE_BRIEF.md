# ADVOCATE BRIEF: wave-20260925-1121pdt debate

Role: ADVOCATE (argues FOR the coordinator's draft verdict slate).
Wave: wave-20260925-1121pdt. Lane dir:
docs/lab/rsi/runs/wave-20260925-1121pdt/. Working copy:
~/workspace/tnn-rsi, branch tnn-native-lab.
Date: 2026-09-25.

## Evidence index (all read, all committed)

- Fork battery: docs/lab/rsi/runs/wave-20260925-1121pdt/forks/FORK_RESULTS_1121.md, commit 0e4207fdb
- B1 prereg: docs/lab/rsi/runs/wave-20260925-1121pdt/sensory/PREREG_B1_1121.md, commit b2b2a3349 (alone, 2026-09-25 18:47:05 UTC)
- B1 implementation plus evidence: commit c91c88ff4
- B1 red team: docs/lab/rsi/runs/wave-20260925-1121pdt/sensory/REDTEAM_B1_1121.md, commit 7b453bb0b (AGREE with DISCARD)
- COMP-2 prereg: docs/lab/rsi/runs/wave-20260925-1121pdt/intel_trade/PREREG_COMP2_1121.md, commit 5bf152b35 (alone, 2026-09-25 19:07:20)
- COMP-2 seal: commit d1ad73cb1 (alone, 2026-09-25 19:33:23)
- COMP-2 implementation plus evidence: docs/lab/rsi/runs/wave-20260925-1121pdt/intel_trade/EVIDENCE_COMP2_1121.md, commit 621e10957 (2026-09-25 19:48:50)
- COMP-2 red team: docs/lab/rsi/runs/wave-20260925-1121pdt/intel_trade/REDTEAM_COMP2_1121.md, commit 36eb88f8f (MODIFY)

Standard applied throughout: verdicts argue from the committed numbers,
not from paraphrase. Weak spots are named in each section, then the
reason the verdict still stands.

## Position 1: Fork battery CONFIRM [RE-CERT], 30/30 PASS

The battery did exactly what a re-certification battery is for. Fresh
enumeration this wave found 30 entries: 4 live, 26 fixture. Live =
local-tnn-native-lab (moved 382f70f95 to 0ca683756af8),
origin-tnn-native-lab (moved 4d613edb1 to 84ed45077),
origin-tnn-native-lab-runstart-tip (explicit duplicate of the same
commit 84ed45077), and local-archive-wave-0821pdt (new branch this
wave at 393007563d). Fixture = the 10 unchanged archive branches, the
wave-debate-session-1-backup branch, the 5 remote heads fetched read
only into FETCH_HEAD, the 7 forktest worktrees, and the 3 wave3
worktrees. Every enumerated fork ran the full shell battery (B1, B2
rerun, B2 recompile identical via cmp -s, B3 znc check --strict
--no-zagd, NEG1, NEG2, PROBE) and the rebuilt pure Zag harness. All 30
shell batteries PASS. All 30 harness verdicts PASS, exit 0. The pinned
znc sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
matched on every fork. The rebuilt harness binary sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66 is byte
identical to last wave's, so the harness build is deterministic and
the comparison is apples to apples. NEG1 and NEG2 discriminated as
required on all 30 (NEG1 fails compile and check; NEG2 compiles,
checks, runs, and its stdout differs from expected). Zero Python
contact anywhere in the run.

Known weak spot, stated plainly: the origin/tnn-native-lab tip moved
twice around this run. The battery tested the run-start tip
84ed45077a554f9897ec55c2ca1430273c79eb69. An intermediate tip
695997f5e3df5979a10a0aa8137a1428483828e8 appeared before the battery
started, and the closing read only ls-remote reported yet another tip
236e5a17815f925bc405e659246d19498e934cfc. Neither is covered by this
wave's battery, and the file marks both as CANNOT-CONFIRM items with
the remedy stated: pick up the latest tip in the next wave's run-start
entry.

Why CONFIRM still stands: the anomaly is disclosed in the committed
file, not buried, and it is a coverage-scheduling gap, not a test
failure. The verdict CONFIRM [RE-CERT] is a claim about the 30
enumerated entries, and on that claim the evidence is complete: fresh
enumeration, explicit live vs fixture split with duplicates named, per
fork commit SHAs tabulated, and the identical pass vector grepped
across all 30 full logs with no exceptions. Nothing was re-run on a
moved local tip because the local HEAD did not move during the run
(0ca683756af8354d202828be8922ddb02e834108 at start and at close).
The correct disposition is exactly the draft's: CONFIRM [RE-CERT] on
the tested set, with the two untested origin tips carried as the next
wave's first entry. Downgrading the battery over a disclosed,
remedied scheduling gap would punish honest reporting and leave the
30 verified entries without the standing they earned.

## Position 2: B1 BOUNCE DISCARD [NEW]

B1 is the cleanest discard of the wave, because it was killed by its
own frozen bars with wide margins and the red team then supplied the
deeper kill reason. The frozen bars were never moved. KB4a measured
mean per-channel |delta| 2.03 against a floor of 3.5 (58 percent of
floor, n=141,684 shadowed land pixels, verifier output
kb4_mean_x100=203). KB4b measured 17 percent of those pixels reaching
mean |delta| >= 3.5 against a frozen 25 percent
(kb4_hit_frac_x100=17). KB6 measured max 4-neighbor delta-field
gradient 14 against a cap of 8 (1.75x the cap, kb6_maxgrad=14). The
red team re-ran the committed verifier binary against the committed
BMPs and reproduced every number exactly, including the k=192
data-amount trial (mean 0.86, hit 2 percent, max 15, grad 7) and the
rerun hashes (var_r1 == var_r2 == ef32cd97..., k192 == fbb69aa2...).
The red team's own inspection of the committed comparison crops
confirmed the two halves are indistinguishable, consistent with a
~2/255 mean move. The frozen verdict mapping makes PARTIAL
unavailable and no bar may be moved this wave, so DISCARD is the only
mapped outcome, and the worker applied it.

The stronger case for DISCARD is the structural reason the red team
derived from the two measured points (k=192: mean 0.86, grad 7;
k=384: mean 2.03, grad 14). Linear interpolation gives mean(k) approx
0.86 + (k-192)*0.00609 and grad(k) approx 7 + (k-192)*0.03646. KB4a
needs k >= ~625, where grad ~= 22.8 > 8. KB6 needs k <= ~219, where
mean ~= 1.02 < 3.5. The gap is roughly 3x on both axes, so no setting
of the frozen mechanism's single knob can jointly satisfy KB4a and
KB6 even under generous interpolation error. The effect is too weak to
see and the hard gate edges too sharp to legalize, and the tuning knob
couples the two. This is not a DF-1 bar-set failure: the red team
showed the bar set itself is jointly satisfiable (a flat +4 tint
would pass every bar), so the failure is the mechanism's, not the
bars'. The prereg's analytic satisfiability check was a calibration
error: it hand-computed 3.1 to 14.4 from dab constants and never
accounted for pass 3's aerial wash (up to 210/1024 toward
(198,168,148)) and flat cool fill, which spend the shadow-color budget
inside the light pass and leave a post-pass recolor almost no
headroom. The banked lesson is recorded and endorsed by the red team:
calibrate effect-size bars against the actual base render's pixel
statistics with a probe program, never hand arithmetic on dab
constants.

Newness is verified, not assumed: spot-check greps over all prior run
dirs for bounce, ambient light, color bleed / colour bleed, indirect
illumination, global illumination, and albedo return zero hits outside
this wave's b1 directory. The only diff between the two variants is
the k constant (384 vs 192) plus its trace string, exactly 4 diff
lines; the mechanism matches the frozen spec (mix formula
384*sh/1024/1024, below/above albedo samples at y +/- 192, luma gate
24, PASS 3B block present, decision counts 270 variant vs 269
baseline). Commit order is clean (b2b2a3349 strictly precedes
c91c88ff4, verified by timestamps and ancestry), zero Python anywhere
in the lane, and the sealed judge queue is untouched. Tag: [NEW],
correctly, and never a re-certification.

Known weak spot, stated plainly: KB6 as frozen is single-worst-pixel
hypersensitive (a global max over ~1M pixels), and the measured 14
comes from hard on/off switches (luma gate >= 24, sky/land mask) with
nothing visible at the failure points. Future preregs may want a
percentile-based or boundary-aware edge bar.

Why DISCARD still stands: frozen is frozen, and the mapping forbids
moving bars this wave. But the verdict does not rest on the
hypersensitive bar alone. The primary failure is effect size (2.03 vs
3.5, sub-visible by independent inspection), and the coupling analysis
shows the mechanism cannot be tuned into a pass even if KB6 were
relaxed, because raising k toward KB4a pushes the gradient further
past any plausible smoothness cap. DISCARD is the honest verdict on
both the letter of the bars and the structure of the mechanism.

## Position 3: COMP-2 PARTIAL [NEW], adoption doubly gated

The measured results are real and the bars PASS as measured. On the
fresh sealed 30-probe set (20 COMP, 10 UNANS, seal d1ad73cb1,
PROBES.md eb00a7c8b5be31ccd3ff0f021f4e0e5abce0437decb1f503a4be1b11ebf5537c,
KEY.md 35802003ee0140ae6163efbd85d2750d59030ae8f55deeee854bdd0242f25aed):

- COMP-B1 20/20: every COMP probe answered with the key's expected
  fact pair, both facts emitted byte-verbatim in index order with
  exactly one space. Bar requires at least 14/20.
- COMP-B2 10/10: every UNANS probe declined through the frozen decline
  path; no pair emitted.
- COMP-B3 17/17: inkb17.txt turns byte identical between the adopted
  cvp rebuild (binary
  dcf98cdbd0648efa274d925b38818d3edbe00cd7d12f562564c2b5c308b0b4eb) and
  the candidate on identical fresh-conversation inputs.
- COMP-B4 7.17x per-turn mean ops vs the cvp baseline, under the 10x
  budget and inside the prereg's expected 6x to 9x range. P6
  individually measures 10.1x (10373/1025); the bar is on the mean, and
  this was disclosed for transparency.
- COMP-B5 3/3: three full sealed runs byte identical (transcript SHA
  243a6a9f3c1a78ac4c9b156d21f096655e1c7efa68588fcb5b5216ed53f63bf),
  zero RNG in decision paths, zero Python contact.
- COMP-B6: seal integrity holds; static grep confirms no sealed probe
  bytes in the candidate sources, and the binary never reads KEY.md.

Commit order is strict and verified (5bf152b35 < d1ad73cb1 <
621e10957 by timestamps and merge-base ancestry; no impl files existed
at seal time). The mechanism is genuinely new: grep across prior run
dirs found no entity-bridged pair-enumeration mechanism; the only
prior art is the two frozen do_compose templates (hardcoded 2-fact
lookups), and COMP-2 handles a disjoint probe class since F9.3 excludes
the templates. The red team's source audit (192 diff lines in exactly
two hunks against the 0521pdt cvp.zag base, everything else byte
identical) found comp2_try to be a genuine generic enumerator: no
hardcoded pair indices, no probe bytes, no KEY.md reference, no RNG,
no clock, lexicographic lowest pair wins, pairs sharing no entity
never coverage-tested, op counting under the frozen F6 discipline
applied symmetrically. Degenerate strategies are mechanically closed:
answer-everything-pair fails COMP-B2, decline-everything fails
COMP-B1. Emission is verbatim concatenation of cited facts in index
order, so confabulation is impossible by construction. The 7.17x cost
for converting a documented decline class (the engine's explicit "no
single knowledge-base fact" message) into 20 correct two-fact answers
is a genuine intelligence trade against the standing hunt priority
(10x cost for a genuine new capability is good). The smoke test
reproduced by the red team (P1 answered with facts 0 and 2 verbatim,
UNANS declined with the frozen message, 10647/10127 ops inside the
reported range) corroborates the numbers independently.

The draft says PARTIAL, not PASS-with-adoption, and the advocate
holds that PARTIAL is the only defensible disposition, for three
reasons that the red team's MODIFY makes precise:

1. The prereg's verdict mapping ("ADOPT iff COMP-B1 through COMP-B6
   all PASS") is void for this lane. It conflicts with higher standing
   authority: the 0821pdt judge's adoption bar and the standing ruling
   6, which reserves the Python-mirror question to Micah alone. Lower
   text cannot override higher standing rules, so the mapping is
   struck as a policy clause, severable from the mechanism, the bars,
   and the PASS verdict, none of which depended on CV-P being adopted
   rather than frozen and byte-pinned. The worker self-flagged the
   "adopted CV-P" mislabel; the taint is documentation-level.
2. Gate (a), rotated-author re-test: author and implementer are the
   same worker in one session, attested by that worker and disclosed
   in COMP-B6. The "independent enumerator" is an independent
   implementation but shares byte-copied stemmer logic with the same
   author. The 20/20 therefore measures rule-implementation fidelity,
   not independent discovery. Per precedent P3, missing structural
   author/implementer separation caps at PARTIAL. The technical PASS on
   bars stands as measured; any future adoption needs a rotated-author
   re-test on a fresh sealed set first.
3. Gate (b), ruling 6 on Python-mirror logic: COMP-2 is downstream of
   CV-P's stemmer three ways, as the red team showed. Pair deliberation
   fires only on deliberate_cv1's dec==2, which is CV-P's
   stemmed-coverage gate output. The pair-coverage test runs over kbws,
   the stemmed content-word sets produced by CV-P's stemmer, so a
   different stemmer changes coverage sets, winning pairs, and answers.
   The sealed key itself was computed by the authoring enumerator with
   byte-copied stemmer logic. The lineage is in the source: comp2.zag
   line 1396 carries "(proven: 1/12 < 2/12 in the Python mirror)",
   inherited verbatim from the 0521pdt CV-P base. So the numbers are
   stemmer-contingent, not merely adoption-barred. If Micah's ruling 6
   rejects Python-mirror-developed logic, this lane's evidence (key
   included) must be derived again with an independently developed
   stemmer; it does not survive as a re-vote. The worker's "isolated
   experiment" framing holds at the file level (originals byte
   identical, nothing integrated, run-dir evidence only) but not at
   the logic level. Until Micah rules, PARTIAL is the holding pattern
   the evidence earns: measured PASS on bars, adoption doubly gated.

Known weak spots, stated plainly: single-session self attestation
(M5 not met); the 3/3 determinism claim cites a transcript SHA but no
transcript or op log is committed (corroborated by the red team's
independent 3/3 spot check and by construction, but the gap is noted);
the 20 COMP probes fall into about four surface templates and F9.5
explicitly uses KB surface forms to avoid stemmer-sensitive
inflections, so paraphrase robustness is untested and generality is
unproven; AUTHORING.md A3's "all pass" phrase-list claim is inaccurate
on its face against the frozen F9.2/F9.3 spec (non-binding, but sloppy);
the prereg specified install-time entity precompute with ops excluded,
while the implementation builds the fact-entity matrix inside
comp2_try per declined turn and counts the ops, which inflates the
measured 7.17x relative to the prereg's accounting (conservative, so
it favors honesty, but the text and code disagree); and the red team
disclosed a self-caught python3 -c slip during review that read and
wrote nothing and contacted no artifact.

Why PARTIAL [NEW] still stands: every one of these weaknesses is
disclosed in the committed record and carried as a residual on future
adoption, not hidden. The P3 precedent exists precisely for the
self-attestation case, and it caps at PARTIAL, which is the verdict
being argued. The stemmer contingency does not erase the measured
capability: the genuinely new code (pair enumeration, entity bridge,
verbatim emission) is separable from the stemmer in principle, and
within the documented condition the 20/20, 10/10, 17/17, 7.17x,
3/3, and seal PASS are honest, independently re-verified numbers. The
ruling-6 contingency is real and goes to the evidence's survival, but
PARTIAL is the correct status while the ruling is pending: it claims
nothing about adoption, promises a re-derivation if the ruling goes
against, and keeps the capability proof on the books. Nothing was
integrated; run-dir evidence only.

## Advocate's closing recommendation to the judge

1. Fork battery: CONFIRM [RE-CERT], 30/30 PASS on the tested set.
   Carry 695997f5 and 236e5a17815f as the next wave's run-start entry.
2. B1 BOUNCE: DISCARD [NEW]. Primary: KB4a/KB4b/KB6 fail with margin
   on frozen bars, sub-visible effect confirmed independently.
   Structural: KB4a and KB6 are jointly unsatisfiable within the
   frozen k family, so no tuning passes. Bank the calibration lesson
   (probe base-render pixel statistics before freezing effect bars)
   and the substrate lesson (pass 3's wash and flat fill spend the
   shadow-color budget; post-pass recolor gets ~2/255 at honest
   mixes). Consider a direction bar for future recolor preregs so a
   magnitude-only cheat cannot pass KB4.
3. COMP-2: PARTIAL [NEW], adoption doubly gated. Strike the prereg's
   ADOPT mapping as void against higher standing authority. Gate (a):
   rotated-author re-test on a fresh sealed set before any adoption
   verdict (precedent P3; M5 not met this wave). Gate (b): Micah's
   ruling 6; on rejection, re-derive the evidence with an
   independently developed stemmer, key included. Record the evidence
   as stemmer-contingent. The numbers stand as measured unless and
   until the ruling changes their foundation.

Nothing in this brief touches Micah's frontier files, the six
governance rulings, or the sealed judge queue. No browser work was
required or performed. No Python was invoked in preparing this brief.
