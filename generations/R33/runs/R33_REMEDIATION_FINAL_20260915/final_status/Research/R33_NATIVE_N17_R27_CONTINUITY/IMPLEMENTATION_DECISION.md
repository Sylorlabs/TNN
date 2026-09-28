# N17 implementation decision

Status: **FRESH NATIVE STATIC CHECKS AND EXACT R26/R27 DIGEST MATCHES; FULL VERIFIER FAIL-CLOSED**.

2026-09-15 Lane B superseding decision: `LANE_B_AUDIT_20260915/AUDIT.json`
records fresh execution of frozen existing native tools using only the stable
`/Users/Shared/micah/Documents/zag/znc` and local shell. Both semantic digests
match exactly. The source-line matrices have 50 directly exercised static
passes and 30 unresolved required rows. There are zero reviewed native
runtime-equivalent passes and no full-verifier/admission/authority credit.
V91 still requires actual native generation of all 16 strings, not oracle
printing. R25 lineage remains blocked by exact inputs and a missing import.

2026-09-15 final remediation supersedes the preceding audit counts: 54 scoped engineering rows (50 static and four inert identity/class equivalents) pass; 26 remain blocked (five R27, 21 R26). The isolated compatibility import/constant gap is repaired. Complete R25 lineage remains blocked by exact input/source/release bindings and unimplemented full lineage semantics. Exact historical receipt custody is closed, with no native lineage credit. V91 generates zero strings. Fresh original qualification and refusals: `../R33_REMEDIATION_FINAL_20260915/REQUAL_RESULT.json`.

The rationale below is retained as the pre-audit design record. Its statements
that digest implementations or source-index bindings are absent are superseded
by this dated decision, not current absence claims. Full native runtime,
paired mutational fixture admission and independent review remain unresolved.

This is a positive engineering decision, not an abandoned work item. The
available native evidence is enough to design the boundary, but not enough to
write a trustworthy R26/R27 semantic digest or verifier.

## Evidence that is sufficient

- The N10 native map has a read-only, hash-bound reconstruction of the accepted
  parent bytes and inert descriptor tables.
- The recovered digest excerpts identify the historical preimage order and the
  fields that matter if their native views are proven.
- Native Zag substrate exists for bounded map loading, numeric storage/tensor
  views and SHA-256 primitives.

## Evidence that is not sufficient

- No R25 accepted-state/source/manifest inputs and individual hashes are present
  in this N17 source index.
- The exact map selectors and byte layouts for every R26 digest field are not
  populated: video basis/mean, entity state dictionaries, graph views,
  name-memory motifs/counts, abstraction models and optional segmenter state.
- The exact R27 selectors and tensor-byte semantics for active head objects,
  specialists, architecture and evidence are not populated.
- The native equivalent of Python canonical JSON, `str(...)`, sorted specialist
  formatting and float32 conversion has not been bound to known answers from
  the actual parent.
- The historical verifier includes behavior/runtime checks that cannot be
  reconstructed from the digest source alone.

## Decision rule

N17 may add a separate native digest/verifier implementation only when every
direct digest field has: (1) an exact inert-map selector, (2) a reviewed type,
(3) a byte-order/shape/ordering rule, (4) an individual input hash, (5) a
known-answer fixture and (6) a negative control. Until then, code that merely
returns the retained R26/R27 digest, counts historical checks, or recursively
guesses R25 is prohibited and would invalidate continuity.

The current correct deliverable is therefore concrete closure artifacts and
explicit blockers, not an empty or witness-substituting implementation.
