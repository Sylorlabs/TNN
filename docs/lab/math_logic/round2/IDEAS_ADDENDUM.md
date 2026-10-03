# IDEAS ADDENDUM — engine (d)/(e) selection (frozen before build)

## The six candidates
From the three ideas arms (all specs at ~/workspace/math_r2/ideas/):

| # | Arm | Name | Core idea |
|---|-----|------|-----------|
| 1 | Native | TMS-R | Non-monotonic ledger; deterministic culprit retraction + nogoods |
| 2 | Native | RESOLVER | Ordered resolution refutation; minimal-assumption attestation; DERIVED-ON-INJECT labels |
| 3 | Fable | PCFS | Proof-carrying forward search; dependency-localized taint |
| 4 | Fable | NFEE | Negation-first elimination; contrapositive firing; false-rule attribution |
| 5 | Grok | QUOT | Admissible-support quotient; conflict taint by support bitsets; specificity defeat |
| 6 | Grok | RESIDUAL | Goal-cube elimination; ledger branches on collapse |

## Selection
- **(d) GROK-D = QUOT** (spec: engines/quot/SPEC_QUOT.md). Sharpest test of
  H1's strong reading and H5: it predicts matching HYB's contradiction
  accuracy with NO tolerant-referee component at all (tolerance via support
  quotient + specificity). If QUOT matches HYB on B5X, H1-as-referee-value
  and H5 both take a direct hit. RESIDUAL was the runner-up; its designed
  D-vs-E divergence is valuable but QUOT's predictions are more falsifiable
  against the frozen hypotheses.
- **(e) FABLE-E = NFEE** (spec: engines/nfee/SPEC_NFEE.md). Structurally
  unique across the whole field (negation-first; no other engine leads with
  contrapositives) and the ONLY design offering rule-level attribution of
  false rules — a new measurable. PCFS was not chosen: its dependency-
  localized taint overlaps QUOT's mechanism too closely to spend a build
  slot on both.

## Considered, not built (bench for a follow-up round)
- TMS-R (native): non-monotonic retraction is genuinely uncovered — no built
  engine deletes. Strongest bench candidate if Micah wants a sixth engine.
- RESOLVER (native): different proof calculus (resolution) + labeled
  inject-dependence; uncovered, but its B5 "zero silent incorrect" claim
  overlaps NFEE's attribution story.
- RESIDUAL (grok): goal-directed elimination; overlaps NFEE's
  elimination-first flavor and QUOT's taint story in coverage.
- PCFS (fable): overlaps QUOT (forward + localized taint).

Nothing about the unchosen four is judged wrong — they are documented,
frozen in ~/workspace/math_r2/ideas/, and buildable in a follow-up.

## Diversity check (final field of 7)
ONE-R1 (match-bind + derive-NOT-H) / DUAL-R1 (prover + H5 referee +
interface) / HYB (ONE core + tolerant referee, one mechanism) /
REF-FIRST (referee-driven derivation) / LEARN-FORM (learned formalizer +
ONE core) / QUOT (support quotient + specificity, no referee) / NFEE
(negation-first elimination + attribution). No two share a core operation.
