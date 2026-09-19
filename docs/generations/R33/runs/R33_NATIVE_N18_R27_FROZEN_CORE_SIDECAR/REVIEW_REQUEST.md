# R33-N18 independent design review request

Review target: design and source-contract mapping only. No implementation,
preregistration, admission or execution authorization is requested.

Review these files against `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md`,
the current N17 continuity blocker and the consumed N16 qualification:

- `DESIGN.md`;
- `VERIFY_CONTRACT.md`;
- `SOURCE_REFERENCE_INDEX.json`;
- `SIDECAR_INTERFACE_CONTRACT.md`;
- `PREFREEZE_MANIFEST_REQUIREMENTS.md`;
- `AMENDMENT_REQUEST.md`;
- `ROUTE_FREEZE_TEMPLATE.json`;
- `STATUS.json`.

Required judgments:

1. Does the design honestly separate custody, native-surrogate behavior and
   full R27 continuity?
2. Are C0 parent-only, C1 no-op-wrapper, C2 arm19 and C3
   randomized/untrained-sidecar controls sufficient to isolate learning from
   wrapper, budget and nonspecific sidecar effects?
3. Are fresh namespaces, paired conditions, stage consumption and no-rerun
   rules complete and disjoint from consumed N16 evidence?
4. Are the primary endpoints, fixed margins, C1 guard and C3 failure rule
   precise enough to freeze before exposure without external rescoring?
5. Are training/evaluator separation, parent write isolation, canonical hash
   custody, resource refusal and literal-substitution controls explicit enough?
6. Does the proposed amendment preserve a surrogate-only claim boundary and
   avoid laundering digest or historical verifier evidence into continuity?
7. What source/runtime, evaluator or authority dependency remains unpinned?
8. Is the explicit R27-to-sidecar feature/output mapping blocker sufficient to
   prevent a synthetic 16D N16 interface from being laundered into R27 behavior?
9. Does the pre-freeze checklist adequately bind every map page, substrate,
   source, fixture, seed allocation, filesystem identity and expected refusal?
10. Is the stage-relative C3 nonspecific-benefit sentinel explicit enough to
    catch a smaller nonspecific gain during development or validation?
11. Does the response encoding distinguish valid negative decisions from
    malformed, overflow, unsupported and skipped refusals, and does C3 match
    C2's full weight-plus-bias state shape?

Allowed terminal dispositions:

- `REQUEST_CHANGES`;
- `APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION`.

The reviewer must not execute or compile N18, run Python or historical
verifiers, rerun N16, create a registry entry, create an admission, mutate R27,
grant authority or authorize promotion.
