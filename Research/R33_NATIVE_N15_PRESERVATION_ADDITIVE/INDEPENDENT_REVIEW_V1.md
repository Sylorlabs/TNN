# R33-N15 independent pre-run review V1

Terminal disposition: **REQUEST_CHANGES**

Read-only independent review was performed against the pre-correction BUILD_05/06 candidate. The reviewer did not execute N15, compile it, or modify files.

The reviewer confirmed that development, validation, confirmation, and smoke used disjoint seed namespaces; probe evaluation occurred only after training and did not enter learner fitting, routing, preservation-anchor acceptance, or update acceptance; and Smoke01/02 were authoring evidence in a separate namespace rather than validation/confirmation evidence.

Three preregistration blockers were identified:

1. CONFIG's fallback rule says minimize total `old_lost` subject to positive aggregate `new_gain`, but the old driver additionally broke equal-loss ties using larger total `new_gain`. That extra tie-break was not declared.
2. The development selector could legally return arm1, while the old holdout entrypoint rejected selected arms below2.
3. The old candidate had no native/predeclared validation-to-confirmation scientific gate.

The reviewer required exact development selection/fallback behavior, holdout admissibility, native validation acceptance, confirmation advancement, selected-arm binding, and no-rerun discipline to be frozen before scientific exposure.

Observed pre-correction identities:

- `driver.zag`: `10884b9b18ef86134a8837829c2f976ab1c391e2a56774d2862d6de9cd1d8db5`
- `CONFIG.json`: `257a6fe68ab4b15f5c74506d28de56b796bee681945a15dcb3432dd4e6e5e91d`
- `DESIGN.md`: `0a0c388ca6edcc5f5152ddb79c4d40e4fdb4517dd8d0db6f71ccafb431f4f182`
- `AUTHORING_HISTORY.md`: `1c076adda5866647287c535ed2aab02e03361d8d8e0d0ea9e534cd1d23e82d62`
- BUILD_05/06 binary: `674fb741a64d5bc6748b3a30cc9aa64a7e615aee257df05173e95f74742d2878`
- native-only execution contract: `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e`
- experiment registry observed: `9a0f874786d2cc960f290fb1a79ff7b79aa3d337f18a988e7cb8e37bde1c9242`

No execution authorization was granted. Canonical R27 source/runtime continuity remained unresolved and N15 remained non-promotable.
