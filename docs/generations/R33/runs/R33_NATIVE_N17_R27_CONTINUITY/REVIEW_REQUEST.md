# R33-N17 independent preregistration review request

Review target: the **design and source-contract mapping only**. No execution authorization is requested.

Review `DESIGN.md`, `SOURCE_REFERENCE_INDEX.json`, `VERIFY_CONTRACT.md`, `HISTORICAL_WITNESSES.md`, `SELECTED_ORIGINAL_MANIFEST.sha256`, `PARENT_TYPE_INVENTORY_SCHEMA.json`, `VERIFIER_CHECK_MATRIX.json`, `R25_LINEAGE_REQUIREMENTS.md`, `INDEPENDENT_REVIEW_V1.md` and the files under `SOURCE_REFERENCES/` against the native-only execution contract and the already-consumed N10/N12/N13A evidence.

Required reviewer judgments:

1. Does the recovered R27/R26 digest material and ordering match the exact original sources without silently inserting historical digest literals?
2. Are Python JSON/string/float32/tensor-byte semantics bounded tightly enough to implement natively, with fail-closed treatment of unsupported types?
3. Does the verifier contract distinguish direct recomputation, proposed native equivalents, historical witnesses and deferred blockers without laundering the historical 33/33 receipt into new evidence?
4. Are the negative controls sufficient to falsify likely canonicalization, ordering, identity-linkage and policy-gate mistakes?
5. Is the success ladder narrow enough to prevent digest reproduction from being mislabeled full behavioral continuity?
6. Does any required source/runtime semantic remain unpinned before preregistration?
7. Are the new inventory schema, draft matrix and R25 requirements sufficient
   to prevent an incomplete matrix from being treated as continuity evidence?

Allowed terminal dispositions for this review:

- `REQUEST_CHANGES`
- `APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION`

The reviewer must not create an admission, execute the candidate, mutate R27, rerun N16 or run any historical Python verifier.
