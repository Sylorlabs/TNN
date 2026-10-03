# IMPLEMENTATION VERDICT: CLAIM-VERIFY-1 (wave-20260924-1121pdt)

Implementer: CLAIM-VERIFY-1 worker. Date: 2026-09-24.
Working copy ~/workspace/tnn-rsi, branch tnn-native-lab,
HEAD 68c3bb8683ab091762069efbe834293efeff2a10. No commit, no push.

## What was built

A coverage-deliberated replacement for the word-literal match inside the
frozen decline gate (path 5 only; paths 1-4 byte-untouched). Per the frozen
prereg: F7 canonicalization (lowercase ASCII, keep [a-z0-9 ], collapse
whitespace, trim, drop the 54 frozen stopwords), canonical content-word sets
precomputed once for the 38 frozen KB facts, single-fact coverage with
lowest-index tie-break, specific decline in the frozen "contains nothing
about" template naming uncovered words from the maximum-overlap fact, F8
atomic-claim splitting with fail-closed substring verification against the
selected fact's canonical form, and a pure-Zag per-turn op counter. Zero
RNG. No fact composition: the gate either declines or selects exactly one
fact, emitted verbatim through the unchanged frozen emit path.

Sources: impl/cv1.zag (candidate), impl/cv1_section.zag (deliberation
section), impl/gate_op.zag (cost instrument), impl/collapse_check.zag
(confound-4 check). Evidence: impl/BUILD_LOG.md, impl/RESULTS_CV1.md,
impl/CONFOUNDS_CV1.md, impl/runs/ (transcripts, op streams, per-probe
report), impl/fixtures/ (canonical F4 fixtures).

## Measured numbers

- Frozen KB sha256: 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1 (38 facts).
- Toolchain sha256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- CV-B2: 17/17 in-KB turns byte-identical to frozen baseline (sha256
  e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264 both
  engines); 30/30 training probes specific declines, 0 blanket refusals.
- CV-B3: 3/3 reruns byte-identical, transcripts and op counts.
- CV-B4: baseline per-turn mean 376.333 ops, candidate 677.4 ops, ratio
  1.80x (bar: at most 10x). Instrument note: no F6 artifact exists in the
  repo, so a comparable pure-Zag decision-op counter was threaded through
  the frozen deliberate() and verified stdout-identical to the frozen
  baseline; both engines counted under the same discipline.
- CV-B5: 100 percent of declines name specific uncovered content in the
  frozen template; 0 blanket refusals.
- Confound 4: 0 duplicate content-word sets across the 38 facts
  (machine-checked).
- Static: no RNG, no composition, no sealed references, no Python.
- Disclosed conservative divergence: exact F7 matching (no stemming, per
  prereg) declines some answerable inflected-form probes where the frozen
  gate's stemmer matches (existence: "did marie curie discover radium?").
  Fail-closed, never a confabulation; 9/30 training decline lines differ
  from baseline in cited words only, all still specific declines.

Sealed scoring (CV-B1 honest-resolution count, CV-B6 seal-open) is the
coordinator's later step; the sealed directory was never opened.

IMPLEMENTATION-READY-FOR-SEALED-SCORING
