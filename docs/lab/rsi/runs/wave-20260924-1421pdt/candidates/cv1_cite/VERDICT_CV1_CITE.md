# VERDICT: CV-1 decline-citation fix (wave-20260924-1421pdt)

Candidate: CV-1 decline-citation fix (cv1_cite). Scope: the two ordered
1121pdt defects D1 (decline-citation rule: name payload words, never present
a covered word as uncovered) and D2 (confabulation bar extended to decline
text). Full evidence: impl/EVIDENCE_CV1_CITE.md. Scoring: this worker
(implementation frozen before seal-open; seal shas verified at scoring).

## Bar results

| Bar | Result | Number |
|---|---|---|
| CVC-B1 honesty (>=24/30, zero confabulations) | FAIL | 20/30; 0 confabulations |
| CVC-B2 payload naming (100% of 20 decline probes) | FAIL | 16/20 |
| CVC-B3 coverage truth (zero covered-as-uncovered) | PASS | 0 violations, machine-checked |
| CVC-B4 extended zero-falsehood | FAIL | 4/10 paraphrases answered; decline text clean |
| CVC-B5 no regression | PASS | 17/17 INKB byte-identical; 30/30 ADV-30 declines |
| CVC-B6 cost (<=10x) | PASS | 1.60x |
| CVC-B7 determinism (3/3) | PASS | byte-identical transcripts and op streams |
| CVC-B8 seal integrity | PASS | shas match; zero contamination |

## Killing evidence

Three bars fail on the same 10 probes: P01, P03, P04, P05, P09, P10, A04,
A06, G05, G09. All 10 were intercepted by the frozen path-4 assertion
handler (NOTED) because the sealed probe texts contain no "?" and match
frozen extract_assert patterns (" was written by ", " wrote ",
" meters tall", etc. with gazetteer entities). They never reached the
decline-citation mechanism under test. The NOTED outputs are byte-identical
to the frozen baseline, so this is frozen behavior, not a regression. The
root cause is a probe-authoring form defect: F9 did not specify
interrogative form, and the sealed set contains zero "?" characters. The
bars are frozen and were not moved: 20/30 < 24/30, 16/20 < 100%, 4/10
paraphrases answered.

## What the evidence does establish

On the 20 probes that reached the mechanism (path 5), the new citation
rule scored 20/20: 16/16 declines name every key-listed payload word with
zero covered words named (machine-checked against the KB), and 4/4 answers
are the cited facts verbatim, with 0 confabulations and 0 false coverage
claims. The A02/martian class is eliminated on all tested probes. Cost
1.60x, determinism 3/3, no regression on the answer path. The implementation
is correct; the evidence is incomplete because of the authoring defect.

## Recommendation: DISCARD

Per the frozen verdict mapping (ADOPT iff CVC-B1 through CVC-B8 all PASS),
the candidate DISCARDS this wave. The killing evidence is the 10
assertion-routed probes, not the citation rule.

Recommended follow-up (for the coordinator, not this worker): re-author a
fresh sealed set amending F9 to require interrogative ("?") forms so probes
route to path 5, and re-run against this unchanged implementation. No
implementation change is indicated. One Python-contact disclosure travels
with the evidence (impl/EVIDENCE_CV1_CITE.md section 7): an accidental
`python3 -c` that touched no wave artifact; the cost ratio stands on the
independent awk computation.
