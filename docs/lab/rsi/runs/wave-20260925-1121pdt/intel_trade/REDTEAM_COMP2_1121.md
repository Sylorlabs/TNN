# REDTEAM: COMP-2 entity-bridged 2-fact composition (wave-20260925-1121pdt)

Reviewer: independent red team (second opinion). Date: 2026-09-25.
Scope: docs/lab/rsi/runs/wave-20260925-1121pdt/intel_trade/ only.
Method: read the prereg, seal materials, evidence, and full source diff;
re-verified commit order, seal hashes, probe conformance (F9.1/F9.2/F9.3),
and purity with shell coreutils only; smoke-ran the committed-candidate
binary on sealed probes; no Python touched any wave artifact in this
review (one self-caught slip is disclosed in section 5).

## Verdict: MODIFY

The worker's bottom line is correct and I agree with it: **PASS on all
six frozen bars as measured, ADOPTION BARRED pending Micah's ruling 6.**
I modify the disposition in three ways:

1. The prereg's verdict mapping ("ADOPT iff COMP-B1 through COMP-B6 all
   PASS") is STRUCK as void for this lane. It cannot override the
   standing ruling-6 adoption bar, and it rests on the prereg's false
   "adopted CV-P" label. The bars and the PASS verdict stand; the ADOPT
   clause does not.
2. The worker's "isolated experiment" framing understates the coupling:
   it is not only adoption that is barred. The measured evidence itself
   (key included) is built on CV-P's Python-mirror-lineage stemmer, so
   the numbers are stemmer-contingent. If ruling 6 goes against
   Python-mirror logic, this evidence does not survive; it must be
   re-derived with an independently developed stemmer.
3. Residuals carried forward: self-attested author/implementer separation
   (M5 not met, disclosed), no committed B5 transcripts (corroborated
   independently here), narrow probe templates (generality unproven).

## 1. The governance anomaly (prereg mislabel + ADOPT mapping)

Attack: the prereg calls the base "adopted CV-P" in the provenance
header and section 2, and its verdict mapping says ADOPT on pass. CV-P is
PARTIAL, confirmed on a rotated fresh set wave-20260925-0821pdt, with
adoption explicitly barred pending Micah's ruling 6 (0821pdt judge
rulings: "Adoption remains barred pending Micah's ruling 6, which is his
alone"). Does the mislabel taint the prereg, and is the ADOPT mapping
severable?

Finding: the taint is documentation-level, and the mapping is severable.

- The prereg's technical core (mechanism in section 2, the six bars in
  section 6, the DF-1 joint-satisfiability check in section 13) does not
  depend on CV-P being adopted. It depends on CV-P being a frozen,
  byte-pinned baseline, which holds: the candidate rebuilds from the
  0521pdt cvp.zag blob (binary hash
  dcf98cdbd0648efa274d925b38818d3edbe00cd7d12f562564c2b5c308b0b4eb as
  pinned) and my diff confirms the rest of the source is byte-identical
  to that base. The mechanism-vs-bars consistency analysis is sound on
  its own terms.
- The ADOPT mapping is a policy clause, not a technical claim, and it
  conflicts with higher authority: the 0821pdt judge's adoption bar and
  the standing user-level ruling 6. Lower text cannot override higher
  standing rules, so the mapping is void for this lane whether or not the
  bars pass. Striking it leaves the bars, the evidence, and the PASS
  verdict intact.
- No behavioral taint: the worker self-flagged the anomaly, kept the
  original CV-P files byte-identical, integrated nothing into CV-P or
  CV-1, and the evidence records "ADOPTION IS NOT RECOMMENDED" with
  reasons. The repair the worker applied is the correct one.

## 2. Inheritance and stack: is COMP-2 evaluable independently of CV-P?

Attack on the "isolated experiment" framing. COMP-2 is downstream of
CV-P at three levels, and the stemmer is the load-bearing one:

- Trigger: pair deliberation fires only on deliberate_cv1's dec==2, which
  is CV-P's stemmed-coverage gate output ("no single knowledge-base
  fact" with all turn words KB-covered).
- Coverage: the pair-coverage test runs over kbws, the stemmed
  content-word sets produced by CV-P's stemmer (cv_kb_stem_precompute).
  Change the stemmer and the coverage sets, the winning pairs, and the
  answers can all change.
- Key: the sealed KEY.md was computed by the authoring enumerator, which
  documents "byte-copied" stemmer and stopword logic from the adopted
  source (pair_enum.zag lines 5-6; AUTHORING.md method section). The key
  is therefore a function of the same stemmer.

The stemmer carries the Python-mirror lineage under ruling 6: comp2.zag
line 1396 contains "(proven: 1/12 < 2/12 in the Python mirror)", and the
identical comment sits at line 1396 of the 0521pdt CV-P base, so it is
inherited verbatim, not introduced by this worker.

Consequence: the "isolated experiment" framing holds at the file level
(originals untouched, no integration) but fails at the logic level.
COMP-2 is a stack on an unadopted component, not an independent
evaluation. The genuinely new code (pair enumeration, entity bridge,
verbatim emission) is separable from the stemmer in principle: swap in
an independently developed stemmer and the mechanism stands. But the
committed evidence, key included, is not separable. If ruling 6 goes
against Python-mirror-developed logic, the correct status of this lane is
not PASS but "evidence built on barred logic; re-derive with a clean
stemmer." The worker's "ADOPTION BARRED pending ruling 6" reaches the
right outcome but understates it: the bar is not only on adoption, the
20/20 itself is stemmer-contingent.

## 3. Metric gaming and bar weakness

Source audit of comp2.zag (diffed against the 0521pdt cvp.zag base: 192
diff lines in exactly two hunks, the do_turn dec==2 branch and
deliberate_cv1's return-2 change plus the new comp2_try; everything else
byte-identical):

- comp2_try is a genuine generic enumerator. No hardcoded pair indices,
  no probe bytes, no KEY.md reference, no RNG, no clock. Lexicographic
  lowest pair wins via the best_f<0 guard; pairs sharing no entity are
  never coverage-tested. Op counting uses cv_op under the frozen F6
  discipline, applied symmetrically. No gaming found.
- Static checks: zero sealed probe bytes in comp2.zag or pair_enum.zag
  (grep for three full probe strings: 0 hits each); no "KEY.md" token in
  sources, so the binary cannot read the key by name.
- Seal integrity: PROBES.md eb00a7c8... and KEY.md 35802003... match the
  seal commit d1ad73cb1 blobs exactly. Commit order verified strict:
  prereg 5bf152b35 (19:07:20) is an ancestor of seal d1ad73cb1
  (19:33:23), which is an ancestor of implementation 621e10957
  (19:48:50); no impl/ files existed at seal time.
- Probe conformance: all 30 probes mechanically pass F9.1 (every line has
  "?"), F9.2 (none of the seven frozen assertion substrings,
  case-insensitive), and F9.3 (no template/route triggers). The key's
  expected pairs match the evidence's reported pairs for all 20 COMP
  probes.
- Smoke test: the impl/comp2 binary answers the P1 probe with facts 0
  and 2 verbatim ("Herman Melville wrote the novel Moby Dick. Moby Dick
  was published in 1851.") and declines the UNANS probe with the frozen
  message. Per-turn ops 10647/10127, inside the evidence's reported
  range. Three repeat runs of a 3-probe script were byte-identical,
  corroborating COMP-B5.

Weaknesses, stated plainly:

- Author and implementer are the same worker in one session
  (self-attested, disclosed in COMP-B6). The "independent enumerator" is
  an independent implementation but shares byte-copied stemmer logic and
  the same author. Key and candidate are two implementations of one
  frozen rule, so 20/20 measures rule-implementation fidelity, not
  independent discovery. Honest as a capability-existence proof; weak as
  a generality claim.
- Probe diversity is narrow: the 20 COMP probes fall into about four
  surface templates (author/publication-year, birth-year/authorship,
  landmark/city/date, tower/height), and F9.5 explicitly uses "KB surface
  forms to avoid stemmer-sensitive inflections." Paraphrase robustness is
  untested; a reworded probe could fail coverage or take a different
  route.
- M5 requires structural (different-worker) author/implementer
  separation for future sealed sets; not met here. Per precedent P3,
  missing independent red-team review caps at PARTIAL. This review is
  that independent red-team review, done with mechanical re-verification
  rather than paraphrase, so the technical PASS on bars stands as
  measured. The separation residual is disclosed and carried as a
  condition on any future adoption. It has no practical effect this wave
  because the ADOPT pathway is barred by ruling 6 regardless.
- COMP-B5 evidence gap: the 3/3 claim cites a transcript SHA but no
  transcript or op log is committed. Corroborated here by construction
  (no RNG, no clock, deterministic scan order) and by my 3/3
  byte-identical spot check. Accept with the gap noted; future lanes
  should commit the logs.
- Prereg fidelity deviation (minor, conservative): prereg section 2(a)
  specifies install-time entity precompute with ops excluded from
  per-turn costs, but the implementation builds the fact-entity matrix
  inside comp2_try per declined turn and counts the ops. This inflates
  the measured 7.17x relative to the prereg's accounting; the bar still
  passes under the stricter accounting, so the deviation favors honesty,
  but the prereg text and the code disagree and the record should note
  it.
- Documentation inaccuracy (non-binding): AUTHORING.md A3 claims all
  probes avoid a long phrase list including " in 18" and " in paris",
  but several probes contain them (P1 "published in 1851" contains
  " in 18"; P6-P8 and P16 contain " in paris" case-insensitively). The
  frozen spec is F9.2/F9.3, which the probes satisfy; the A3 list is
  author-side notes, but the "all pass" claim is inaccurate on its face.

## 4. Provenance and newness

Grep across all prior run dirs for entity-bridged, pair-enumeration,
2-fact composition, and deliberation-ensemble mechanisms found nothing
outside this wave's directory. The only prior art is the frozen
do_compose templates in the adopted source: two hardcoded 2-fact
lookups ("was the author of", "which is taller"). COMP-2 is a different
algorithm (entity-indexed pair enumeration over stemmed coverage with the
bridge principle) handling a disjoint probe class (F9.3 excludes the
templates). The "composition" mentions in the 1721pdt CV-1 verdict
documents refer to router paths, not mechanisms. Verdict: genuinely new
mechanism, correctly tagged [NEW]; not a re-certification.

## 5. Commit order and purity

- Order: prereg 5bf152b35 < seal d1ad73cb1 < implementation 621e10957,
  verified by commit timestamps and merge-base ancestry; the seal commit
  contains probes, key, authoring record, fixtures, and the enumerator,
  and no implementation files. PASS.
- Purity: no Python in any wave source (grep over the intel_trade tree
  finds only the words "Python"/"python" in prose about the purity rule
  and the inherited Python-mirror comment). Binaries present
  (impl/comp2, tools/pair_enum) are untracked build artifacts from the
  pinned znc toolchain, not committed. PASS.
- Disclosure: during this review I ran one `python3 -c` command that
  printed a literal string while composing a shell check. It read and
  wrote no file, contacted no artifact, and its output was unused. It
  does not touch the evidence, but I record it because the purity rule
  says to avoid even the carve-out.

## 6. Cost: genuine trade or cost without capability?

The numbers: 7.17x per-turn mean ops versus the adopted cvp binary on
the sealed 30 (bar: at most 10x). Baseline declines all 30; the candidate
answers 20 with verbatim 2-fact pairs and declines 10. P6 individually
measures 10.1x; the bar is on the mean, disclosed transparently.

Assessment: genuine intelligence trade within the frozen budget, with
tempered generality. The capability is real: a documented decline class
(the engine's explicit "no single knowledge-base fact" message) is
converted into correct verbatim answers, the UNANS bar holds at 10/10
declines, and confabulation is impossible by construction (emission is
verbatim concatenation of cited facts in index order). Against the
standing hunt priority ("10x cost for a genuine new capability is
good"), 7.17x for 20 newly answered probes is a legitimate trade, and
the true steady-state cost is lower than measured because the per-turn
entity-table build (section 3 deviation) would be install-time under the
prereg's accounting. The temper: the 20 probes are template-narrow and
surface-form-engineered, so the result proves the capability exists, not
that it generalizes. Cost without capability would be a faster decline;
this is slower answers where there were none.

## 7. Interactive finding (side claim)

Spot-checked and confirmed: src/zag/ contains only INDEX.md (empty,
reserved); units/ contains only teachers documentation. Runnable chat
artifacts exist only in run directories (e.g.
wave-20260924-1121pdt/candidates/cv1/impl/tnn_chat_decline_frozen_ref,
plus the cvp/comp2 binaries tested here). The worker's finding stands.

## Residuals for any future adoption consideration

1. Ruling 6 must be decided; if it goes against Python-mirror logic, this
   lane's evidence (key included) must be re-derived with an
   independently developed stemmer, not merely re-voted.
2. The prereg's ADOPT verdict mapping is void for this lane.
3. M5 structural author/implementer separation for any future sealed set.
4. Commit B5 transcripts and op logs; do not cite uncommitted SHAs.
5. Paraphrase-robustness probes before any generality claim.

## Bottom line

AGREE with the worker's measured results (20/20, 10/10, 17/17, 7.17x,
3/3, seal PASS) and with "ADOPTION BARRED pending ruling 6." MODIFY the
disposition: strike the prereg ADOPT mapping as void, and record that the
evidence is stemmer-contingent, not merely adoption-barred. The lane is
an honest, well-instrumented, genuinely new capability proof whose
numbers stand or fall with Micah's ruling 6.
