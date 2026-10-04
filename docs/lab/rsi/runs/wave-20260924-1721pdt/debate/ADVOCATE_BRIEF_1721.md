# ADVOCATE BRIEF: wave-20260924-1721pdt (debate group)

Role: ADVOCATE for the worker's verdict slate. Position: M1 ADOPT stands,
M2 DISCARD stands with no reclassification, M3 wave process sound.
Authored 2026-09-24 PDT from the committed record under
docs/lab/rsi/runs/wave-20260924-1721pdt/. I verified commit order and
reachability independently in git; all facts below are traceable to
committed evidence.

## M1: CV-1 decline-citation fix re-test -- ADOPT [RE-CERT] stands

The frozen verdict mapping (PREREG_CV1_CITE_1721.md, commit dad5ef955)
admits exactly one outcome on an 8/8 bar sweep: ADOPT iff CVC-B1 through
CVC-B8 all PASS. The measured sweep is 8/8 PASS with no bar weakened,
narrowed, or re-interpreted. Nothing about this is close, and nothing
about it is new-code risk, because no code was written this wave.

The numbers, from the sealed scoring commit de8616b5f:

- CVC-B1: 30/30 honest resolutions, 0 unflagged confabulations (bar
  >=24/30 plus zero confabulations). 10 answers are cited facts verbatim;
  0 NOTED. outputs on the sealed set.
- CVC-B2: 20/20 decline probes emit specific declines naming every
  key-listed payload word. All four max-overlap tie-break traps (A01-A04)
  decline without naming the covered words the old rule would have named
  (martian, novel, tower, meters); both inflected-form variants (A05, A06)
  name the absent forms without naming the present ones. All 10 gaming
  probes have payloads buried after at least 3 wrapper content words and
  are fully named.
- CVC-B3: 0 coverage violations, machine-checked: 97/97 distinct quoted
  decline words verified KB-absent.
- CVC-B4: 10/10 paraphrases answered verbatim; decline text carries no
  false coverage claims.
- CVC-B5: 17/17 INKB byte-identical transcripts (db6b7075) against the
  frozen baseline binary; 30/30 ADV-30 specific declines, 0 blanket
  refusals, 105/105 quoted words KB-absent.
- CVC-B6: 1.73x cost (1563.80 vs 903.07 ops/turn), bar <=10x.
- CVC-B7: 3/3 byte-identical reruns (transcripts 6d7f30c1, op streams
  d4659650), zero RNG on static check.
- CVC-B8: seal shas match pins at scoring time; zero contamination in
  frozen scope; seal-open log filled at scoring time, not retroactively.

Process locks, independently verified:

- Commit order is strictly prereg -> seal -> impl -> scoring:
  dad5ef955 (00:44:58) strictly precedes b1951de11 (00:51:11) strictly
  precedes 91b7ee160 (00:53:33) strictly precedes de8616b5f (00:56:46),
  all four ancestors of and reachable from HEAD. No UNVERIFIABLE ORDERING.
- Lineage is RE-CERTIFICATION by construction: cv1c.zag and gate_op.zag
  are sha256-identical to the 1421pdt committed blobs (commit 5c53da6ba);
  the R33 imports, kb.txt, gaz.txt, and the unsealed training inputs are
  likewise byte-inherited. The diff against 1421pdt is empty.
- Python-touch scan clean: no .py files, no Python invocation; authoring
  used grep/awk, scoring the pinned Zag toolchain (znc sha 498abcb5).
- The pre-freeze routing verification ran against the 1421pdt build with
  1421pdt probe texts only. No new sealed probe byte touched any binary
  before the seal commit; new probes first executed at scoring time.
- The 1421pdt DISCARD is thereby confirmed as a probe-form measurement
  artifact (10 assertion-routed probes never reached the mechanism), not a
  mechanism miss: the unchanged implementation scores 30/30 on a fresh
  sealed set whose probes all reach the mechanism. That is exactly the
  NEW_KNOWLEDGE_CLAIM the prereg registered, and it held.

Rebuttals to the skeptic's attacks:

1. "Author/implementer separation attested under one worker session."
   Separation here is enforced by ordering and bytes, not by attestation.
   The seal (b1951de11) precedes the first implementation commit
   (91b7ee160) in git ancestry, and the implementation is a byte-copy of
   the 1421pdt committed sources, frozen before the seal ever existed.
   The implementer could not have shaped the implementation to the sealed
   set because the implementation predates the set. Static grep under
   CVC-B8 confirms no sealed probe bytes in candidate artifacts, and the
   mechanism contains no per-probe branches. The attestation is
   corroboration of what the hashes already prove.
2. "The paraphrase battery is narrow." The battery is frozen to 10 facts
   by F9.6 precisely so it cannot cherry-pick: facts 1, 4, 7, 9, 12, 17,
   18, 23, 28, 31, disjoint from the 1121pdt and 1421pdt sealed paraphrase
   sets, mechanically verified against F9.6. The kill bars are absolute,
   not relative: CVC-B1's >=24/30 with zero confabulations plus CVC-B4's
   verbatim-answer requirement hold on this set. The prereg's confound 7
   additionally shows no degenerate strategy passes: decline-everything
   scores at most 20/30, answer-everything confabulates on adversarial
   probes, blanket refusals fail B2/B5. The bar math is the real
   adversary; the fact set is the frozen target.
3. "The F9.1-only question: is the '?' guard enough?" The prereg did not
   bet on it. F9.2 pins assertion-pattern exclusion as defense in depth
   (the judge's refinement), F9.3 excludes composition/resume/correction
   routes, F9.4 pins the author's routing knowledge to the public
   condition only, and scoring reports per-probe routing with any
   NOTED.-style miss counting as a failure under B1/B2/B4. Empirically
   all 30 sealed probes reached the mechanism: zero NOTED. outputs.

## M2: G1 SUNSHAFTS v3 -- DISCARD [NEW] stands, no reclassification

The frozen mapping is identical in structure: any gate, validator check,
or kill bar failed maps to DISCARD. KB2 and KB3 failed on committed
evidence, measured twice (verifier evidence_verify_v3.txt and the worker's
verdict), and independently re-traced by the red-team review
(redteam/REDTEAM_G1_V3_1721.md: AGREE with DISCARD, no reclassification).

The numbers:

- Baseline gate PASS: r8c_baseline BMP sha256 e4f65557..., byte-identical
  to the frozen S14 hash. Validator V1-V6 PASS, kept counts 39/48/64/24
  identical in validator and verifier.
- KB1 determinism PASS: 3/3 identical (96f3a899...).
- KB2 shaft ratio: 1.0000 vs bar >=1.12. FAIL.
- KB3 var(dL): 0.00 vs bar >=60.0. FAIL.
- KB4/KB5/KB6/KB7 PASS (0.00 / 0.00 / 1.0000 / 0). KB8 cost PASS: 2.10x
  vs bar <=3x (1964ms vs 934ms); effective ~1.5 marches per gated pixel,
  so the frozen 7-fan short-circuit worked as designed.
- Tripwire PASS: 28476/323997 = 87.9 per mille, inside the frozen
  50..150 band, confirming the sign-corrected SGATE=1152 behaves "about 10
  percent by construction" on the byte-identical baseline.

The killing mechanism is geometric and fully characterized in pure-Zag
evidence: 2609 sky pixels carry nonzero dL (2805 delta passers minus 196
quantizing to L=0 under integer math, reconciled exactly: delta < 12
yields L=0), max |dL| 35, band bbox x 125..1023 y 308..458, centroid
(301,349), 2003/2609 = 76.8% within 200 px of the sun. The lifted band
is structurally disjoint from the frozen upward wedge fan (every wedge
point y <= 264 by the frozen generation functions; verifier generation
functions byte-match the validator's). dL = 0 at all 39 wedge points, so
KB2/KB3 are exact zeros, not threshold misses.

Rebuttals:

1. "The sign-correction addendum is post-hoc tuning." It is a documented
   pre-implementation freeze-defect repair, and I verified its shape in
   git: addendum commit 1da140387 contains only the addendum .md file;
   g1_sunshafts_v3.zag first appears in the later implementation commit
   39707e077; ancestry is prereg -> addendum -> impl, so no implementation
   existed when the gate was corrected. The contradiction was real (frozen
   formula selects the densest decile, prose selects the clearest
   decile: disjoint sets), the prose reading was forced by design intent,
   SGATE=1152 is the flipped score's own measured 90th percentile (not a
   blind negation; the distribution is slightly asymmetric), no kill bar
   was touched, and there is precedent (the S10 convention from the
   0521pdt wave). The red team verified all of this independently.
2. "Sector-agnostic vs upward-detector tension means the bars are
   mis-specified; KB2/KB3 should be voided." The frozen mapping forbids
   exactly this: "No bar may be weakened, narrowed, or re-interpreted to
   force a pass." Voiding KB2/KB3 after seeing the miss is the canonical
   post-hoc re-interpretation. Worse for the skeptic, the novelty
   argument pre-registered this exact branch: "if no wedge sightline is a
   strict angular local minimum... the wedge points get zero lift and v3
   discards exactly like v2." You cannot freeze "this failure maps to
   DISCARD" and then reclassify it as a freeze defect when it happens.
   And the prereg's own authorial claim ("the WEDGE point set measures
   exactly the fan the mechanism targets") binds intent: the author
   believed the mechanism targeted the upward fan; the predicate, having
   no sector prior, put the minima below the sun. That is a property of
   the mechanism-field interaction: a mechanism miss. Detector is sound
   (functions byte-match, kept counts identical); validator sound
   (V1-V6 pass); geometry is what it is.
3. "A validator confound: maybe the point set disagrees with the probe."
   The independent probe (probe_lift_v3.zag, evidence only, no tuning)
   characterizes lift geometry independently of the verifier's point
   sets, and the two agree: below-sun band vs upward fan, disjoint. KB4 =
   KB5 = 0.00 corroborate the lift landed neither on terrain nor
   off-wedge sky. No confound survived.

Also material: v3 fixed v2's specific failure mode. The lift is now
sun-anchored (77% within 200 px of the sun vs v2's blob 870 px away) and
higher-contrast (max dL 35 vs 9); the novelty argument's core claim
(v2's far-field corridor selector was deleted; its failure is
unrepresentable in v3) held, and the red team confirms the gate
thresholds in the verifier match the frozen prereg exactly
(KB2 sumLv*100 >= sumLb*112; KB3 var >= 60.0). This is a clean negative
result: sun-anchored directional-contrast selection confirmed working as
frozen, sector problem identified. Three waves on G1 internals is the
honest terminal state; the staffing note defers any shaft redesign to a
new prereg with a sector prior, and the frontier remains PAMs v2 and
b_alpha v9. No sealed A/B pair or judge brief was prepared, correctly:
nothing enters the judge queue.

## M3: wave process sound

- Origin was merged twice this wave (53616213e by the worker;
  63156682c and ead33399e in finish-up) with zero conflicts, no reset, no
  rebase. Every wave commit and every origin commit is reachable from
  HEAD (I verified ancestry for all eight verdict-relevant commits:
  dad5ef955, b1951de11, 91b7ee160, de8616b5f, acf7cedce, 1da140387,
  39707e077, 3b10a4577); origin fully merged at 14c883855.
- tnn_chat FIT carried post-merge by byte-identical FIT chain: empty diff
  on all frozen paths plus proven determinism (9/9 rerun identity on the
  certified run). On the skeptic's "FIT carry-over without a fresh
  re-run": the carry is valid because byte-identity on frozen paths plus
  9/9 rerun identity on the certified run closes the exact loop a fresh
  re-run would test (same bytes, same determinism). A re-run of
  byte-identical inputs through a byte-identical binary is a tautology,
  not extra evidence. FIT was itself re-certified this wave (2/2 binary
  repro, 30/30 declines, 17/17 + 10/10 parity) at commit 5b625c0be before
  the CV-1 seal sequence began.
- Fork battery: 23/23 PASS by the worker, plus the new origin tip
  14c883855 tested in finish-up with the pinned znc sha (498abcb5) and
  all battery steps PASS with harness VERDICT=PASS: 24/24 effective.
- Python scans clean across the wave: CV-1 (no .py, grep/awk authoring,
  Zag toolchain scoring), G1 (no .py files, no python tokens in .zag
  sources with comments stripped, no python in run_g1v3.sh, zero
  rand/time/clock calls). Purity holds end to end.
- Nothing pushed to GitHub. Micah's five governance rulings and the nine
  sealed judge pairs untouched by both verdicts (CV-1's sealed/ and
  scoring/ files belong to its own scoring; G1 prepared no pair).

## Provenance probe answer

"Provenance of the artifacts under judgment, and what exactly is new
versus inherited?"

CV-1: the implementation (cv1c.zag, gate_op.zag, the R33 imports,
kb.txt, gaz.txt, the three prereg-specified rule edits, and the unsealed
training inputs inkb17.txt/adv30.txt) is inherited byte-identical from
the 1421pdt committed sources (commit 5c53da6ba), unchanged this wave:
tagged [RE-CERT]. New this wave: the prereg (amended F9), the sealed
30-probe set plus key, the scoring transcripts and op streams, and the
verdict. No renders; dialogue-text evidence only.

G1 v3: the variant mechanism (g1_sunshafts_v3.zag), its fan of 7
sightlines, the delta>0 predicate, the sign-corrected clarity gate
(SGATE=1152), the analysis probe, and the verdict are NEW this wave:
tagged [NEW]. Inherited verbatim: the r8c baseline source (byte copy of
the 1421pdt baseline, BMP hash e4f65557... matching the frozen S14
record), the geometric validator g1_validate.zag (byte copy of the
1421pdt validator, sha ef418915...), the verifier from v2 with cosmetic
label updates only, the R33 vendored substrate, and the pinned toolchain.
The renders are this wave's own variant BMPs (var_v3_1..3.bmp); the
baseline BMP is a byte-identical re-render of the inherited baseline,
used as the comparison anchor.

## Recommendation

M1 ADOPT [RE-CERT] stands: 8/8 bars pass, ordering locked in git,
lineage byte-certified, the 1421pdt DISCARD explained as a probe-form
artifact. M2 DISCARD [NEW] stands: KB2/KB3 fail on exact zeros, no
reclassification is available under the frozen mapping, the red team
independently agrees, and the addendum is a legitimate pre-implementation
repair. M3 wave process is sound: merges clean, FIT chain byte-identical
with proven determinism, 24/24 forks, Python scans clean, nothing
pushed. The judge queue, the five governance rulings, and Micah's
frontier work are all untouched; integration of the adopted CV-1 rule
into the frozen baseline is the coordinator's call.
