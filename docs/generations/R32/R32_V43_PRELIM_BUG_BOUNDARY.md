# V43 preliminary execution boundary

Two reporting/adapter errors occurred without producing an aggregate scientific result:

1. The first launch treated the model dictionary returned by `v32.fit` as a tuple and stopped after fitting the first stage.
2. The repaired launch successfully fitted and persisted all four stage model populations, then stopped during report assembly because it requested `average_precision` from the expected-value subsection rather than the classifier subsection. It also exposed that evaluator-only slices with no positive examples require null-safe metrics.

`r32_v43_complete_from_models.py` reloads the already fitted authoritative models, computes null-safe metrics, and writes the final result. No failed-run aggregate is interpreted.
3. The first completion pass used the V41 label `selected_actual_advantage` for V40's persisted field `actual_mean_selected`; this was corrected before final output. The fitted models and predictions were unchanged.
