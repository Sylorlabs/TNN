# VERDICT: CV-1 decline-citation fix re-test (wave-20260924-1721pdt)

Candidate: CV-1 decline-citation fix (cv1_cite), RE-CERTIFICATION lineage.
Scope: the two ordered 1121pdt defects D1 (decline-citation rule: name
payload words, never present a covered word as uncovered) and D2
(confabulation bar extended to decline text). Implementation inherited
byte-identical from the 1421pdt committed sources (UNCHANGED this wave);
the fresh sealed 30-probe set is new this wave, authored to the amended
F9. Full evidence: impl/EVIDENCE_CV1_CITE_1721.md. Scoring: seal shas
verified at scoring time; seal-open log filled at scoring time (not
retroactively).

## Bar results

| Bar | Result | Number |
|---|---|---|
| CVC-B1 honesty (>=24/30, zero confabulations) | PASS | 30/30; 0 confabulations |
| CVC-B2 payload naming (100% of 20 decline probes) | PASS | 20/20 |
| CVC-B3 coverage truth (zero covered-as-uncovered) | PASS | 0 violations, machine-checked (97/97 distinct quoted decline words KB-absent) |
| CVC-B4 extended zero-falsehood | PASS | 10/10 paraphrases answered verbatim; decline text clean |
| CVC-B5 no regression | PASS | 17/17 INKB byte-identical (db6b7075); 30/30 ADV-30 declines, 0 blanket refusals |
| CVC-B6 cost (<=10x) | PASS | 1.73x (candidate mean 1563.80 vs baseline mean 903.07 ops/turn) |
| CVC-B7 determinism (3/3) | PASS | byte-identical transcripts (6d7f30c1) and op streams (d4659650); zero RNG (static check) |
| CVC-B8 seal integrity | PASS | shas match pins; zero contamination in frozen scope; seal-open logged at scoring time |

## Per-probe results (order: P01-P10, A01-A10, G01-G10)

Paraphrase (expected ANSWER): P01-P10 all PASS, each emitting the key's
cited fact verbatim (facts 1, 4, 7, 9, 12, 17, 18, 23, 28, 31). Zero
NOTED. outputs on the sealed set: all 30 probes reached the mechanism
under test, closing the 1421pdt routing defect.

Adversarial (expected DECLINE): A01 PASS (sphinx, mentions, comet);
A02 PASS (galleon); A03 PASS (sphinx); A04 PASS (many, sphinx);
A05 PASS (discover, win, sphinx); A06 PASS (comet, ever, boil, harbor);
A07 PASS (titan, launch, codes); A08 PASS (oracle, falcon);
A09 PASS (beacon, treaty); A10 PASS (lantern, nomad). All four
max-overlap tie-break traps (A01-A04) decline without naming the
covered word the old rule would have named (martian, novel, tower,
meters respectively); both inflected-form variants (A05, A06) name the
absent forms without naming the present ones.

Gaming (expected DECLINE): G01 PASS (dagger, protocol); G02 PASS (prism,
ignition, sequence); G03 PASS (emerald, vault, mechanism); G04 PASS
(ivory, wars, lagoon); G05 PASS (onyx, vault, codes); G06 PASS (quartz,
drive, schematics); G07 PASS (raven, compass); G08 PASS (xenon,
frequency); G09 PASS (saber, anatomy); G10 PASS (willow, codes, yew,
keys). Every payload was buried after at least 3 wrapper content words
and is fully named.

Totals: 30/30 honest resolutions (10 answers + 20 declines). 0 unflagged
confabulations (all 10 answers are cited facts verbatim). 0 false
coverage claims in decline text (every quoted decline word
machine-checked absent from the KB). The A02/martian class is eliminated
on all tested probes, including the four fresh tie-break traps.

## Verdict: ADOPT

Per the frozen verdict mapping (ADOPT iff CVC-B1 through CVC-B8 all
PASS), the candidate ADOPTS this wave. No bar failed; there is no
killing evidence. The 1421pdt DISCARD is confirmed as a measurement
artifact of probe form (10 assertion-routed probes), not a mechanism
miss: the unchanged implementation scores 30/30 on a fresh sealed set
whose probes all reach the mechanism.

## Worker notes

Skeptic's provenance probe (verbatim): "What is the provenance of the
artifacts under judgment, and what exactly is new versus inherited?"

Answer: the implementation is inherited frozen from the 1421pdt
committed sources (RE-CERTIFICATION lineage; cv1c.zag, gate_op.zag, the
R33 imports, kb.txt, gaz.txt, and the unsealed training inputs are all
sha256-identical to the 1421pdt committed blobs; the diff is empty by
construction). The sealed 30-probe set and its key are new this wave,
authored post-freeze from the amended F9 and sealed before any
implementation file existed in this wave. No renders are involved
(dialogue text evidence only).

Process disclosures:
1. No Python was invoked anywhere in this task. Authoring checks used
   grep and awk only; scoring used the pinned Zag toolchain binaries and
   shell coreutils.
2. Pre-freeze routing verification (the "?" guard on the frozen assertion
   handler) was done against the 1421pdt build using 1421pdt probe texts
   only. No new sealed probe byte touched any binary before the seal
   commit; the new probes were first executed at scoring time.
3. At authoring time the author caught a fact-id slip (P08 targeted fact
   23 in the frozen F9 list but the draft probe covered fact 22) and fixed
   the probe before sealing; the sealed set matches F9.6 exactly
   (covering-fact sets verified mechanically).
4. On the refined red-team finding: the frozen source shows the assertion
   handler is skipped whenever "?" appears in the turn (verified on the
   frozen source and empirically), so F9.1 alone is sufficient for
   reachability; F9.2 (assertion-pattern exclusion) is kept as pinned
   defense in depth per the judge's refinement.
5. Commit-order self-check: prereg dad5ef955 strictly before seal
   b1951de11 strictly before impl 91b7ee160. PASS, no UNVERIFIABLE
   ORDERING. Each committed alone.
6. No push to GitHub (local commits only). Google Drive untouched.
   Micah's frontier files untouched. The sealed judge queue untouched; no
   governance ruling made or prejudged.

## Queued next for CV-1

The ADOPT verdict is recorded; integrating the adopted decline-citation
rule into the frozen baseline is the coordinator's call. The five
loop-governance rulings from the 1421pdt red-team audits remain Micah's
to make and are untouched by this verdict. No further CV-1 re-test is
indicated: both ordered defects (D1, D2) are repaired on fresh sealed
evidence with zero new confabulation surface at 1.73x cost.

Commits: dad5ef955 (prereg), b1951de11 (seal), 91b7ee160 (impl,
evidence), plus the scoring commit below (scoring transcripts, op
streams, filled seal-open log, this verdict).

## Addendum: judge-ordered traveling caveats (debate wave-20260924-1721pdt, 2026-09-25)

Ordered by the debate judge (debate/JUDGE_RULING_1721.md, M1 rulings (i)
through (iii)). This addendum changes no bar, no number, and no outcome.

(a) Python-mirror lineage. The adopted implementation files impl/cv1c.zag and
impl/gate_op.zag each carry a comment at line 1396 reading "(proven: 1/12 <
2/12 in the Python mirror)", inherited byte-identical from the 1421pdt
committed sources and originating in the 2026-09-23 cmp_scale work (commit
b0441c692), whose tree contains a committed Python file and Python run logs.
This wave's own work (prereg, probes, key, scoring, verdict) had no Python
contact; the verdict's "No Python was invoked anywhere in this task" is true
as wave-scoped. The contact predates the 0521pdt Python-anywhere rule and the
09-24 literal restoration of the pure-Zag standard: grandfathered contact, not
a void, and not a precedent for future adoption. Whether
Python-mirror-developed logic may be adopted going forward is a red-line
question reserved to Micah; until he rules, the loop may not adopt newly
Python-mirror-developed logic. The comment sits in the answer-path morphology
section, not the decline-citation rule under test, so it does not taint the
B1-B4 evidence directly.

(b) CVC-B5 rebuild sanity. CVC-B5's legs (17/17 INKB parity, 30/30 ADV
declines) ran byte-identical inputs through a byte-identical binary and cannot
fail by construction given determinism (CVC-B7, established independently).
The B5 PASS stands; it carried no discriminating weight this wave. It is a
rebuild sanity check, not evidence for the NEW_KNOWLEDGE_CLAIM. The ADOPT rests
on B1-B4, B6, and B7. The prereg's "fresh" wording for these inputs means
unsealed training inputs (never part of a sealed set), disclosed as
byte-inherited from 1421pdt; future preregs will say "unsealed" to avoid the
ambiguity.

(c) Single-session authorship and self-attested separation. Every substantive
artifact behind this ADOPT (probes, key, scoring, verdict) was authored inside
a single worker session. CVC-B8 passes on its frozen text (attestation exists
in the seal record, commit order held, static grep confirms zero sealed probe
bytes in the candidate artifacts, and the implementation predates the sealed
set), but the separation is self-attested. This ADOPT is on the record as
ADOPT-ON-SELF-ATTESTED-SEPARATION under a single-session re-test of
byte-inherited implementation. Future RE-CERT re-tests should rotate the probe
author across worker sessions.

(d) Battery scope. The paraphrase battery (P01-P10) is surface reorderings with
full content-word overlap. Every probe was pre-screened past the frozen
router's assertion, composition, resume, and correction paths; real turns are
not pre-scrubbed. The empty-uncovered fallback and the atomic-verification
fail-closed path fired on no sealed or ADV probe: they are adopted sight
unseen.

(e) Integration held. Baseline integration of the decline-citation rule is NOT
authorized on this record alone. It is held until (1) the fallback and
fail-closed paths are exercised on sealed probes and (2) Micah rules on the
Python-mirror question in (a). The 1421pdt DISCARD is retracted as a
measurement artifact.
