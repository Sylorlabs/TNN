# R2-8 Evidence — Round-2 Rebuild (2026-09-23)

## What this is

Final evaluation of the R2-8 "Independent Interventional Program" per frozen
PREREG_R2-8.md. Verdict: **DEAD** (see `../VERDICT_R2-8.md`).

**Trial structure**: 5,815 F-trials (X=F adversarial, S=g independent, Ps=p1–p3
perturbations of S). Per prereg §1: "perturbations of that same independent
source." The p-set (perturbations of g) is used, not the q-set (perturbations
of F).

**Fixture note**: R2A adversarial suite contains 5,815 groups (explicit family
counts sum to 5,815; prose says 5,000). All groups complete.

**Recall**: X=r2n_N (R2A normal, truth from .truth), S=r2q_recall_N_g, Ps=p1–p3.
1,728 trials (shapetrans: 1,008; timbredisc: 720).

## Pipeline

1. **Percept generation** (`../scripts_gen/gen_percepts.py`, `repair_cache.py`,
   `gen_missing.py`, `merge_cache.py`): Runs the pure-Zag `sense_r28` binary on
   all fixtures. Reuses valid entries from prior cache; generates missing/
   invalid. 39,237 fixtures total. 11 shapetrans F-fixtures fail with
   `error=task_failed` (genuine binary failures; trials withheld).
2. **Battery** (`../scripts_gen/eval_r28.py`): 5,815 trials, two-leg gate per
   BUILD_NOTES, hash-chained ledger. Outputs: `battery/battery_results.jsonl`,
   `battery/ledger.txt`, `battery/summary.json`.
3. **Primary bars** (`../scripts_gen/bars_primary.py`): B1/B2/B3 from 370 harness.
   Output: `battery/primary_bars.json`.
4. **Recall** (`../scripts_gen/bars_recall.py`): Kill bar 3 from 1,728 trials.
   Output: `battery/recall.json`.
5. **Ledger verify** (`../scripts_gen/verify_ledger.py`): Independent re-chaining.
   Output: `battery/ledger_verify.log`.

## B6 determinism

- `eval_r28.py` run 3 times from the frozen cache; results SHA256 identical
  across all 3 runs (see `battery/run_hashes.txt`).
- Ledger verified by independent re-chaining (see `battery/ledger_verify.log`).

## Files in battery/

- `battery_results.jsonl`: 5,815 trial records (canonical, sorted keys).
- `ledger.txt`: Hash-chained ledger (genesis + 5,815 entries).
- `summary.json`: B4, B5, leg-ii ablation, KB2, hashes.
- `primary_bars.json`: B1, B2, B3.
- `recall.json`: Kill bar 3 (recall).
- `run_hashes.txt`: SHA-256 of outputs + 3-run byte-identity proof.
- `ledger_verify.log`: Independent ledger verification.

## Results summary

- B1: 74.05% (PASS)
- B4: 54.84% changed, reduces FI (PASS)
- B5: 1.0146% false-install (FAIL, bar <0.5%)
- B6: 3 identical runs, ledger verified (PASS)
- KB2: 97.18% self-flag (PASS)
- Recall: 12.47% (FAIL, bar ≥70%)
- Leg-(ii): 13.91pp reduction (PASS, bar ≥0.2pp)
- FS-E: CLOSED (B5 fails)
- Mechanism: NON-COMPLIANT (gate/ledger in Python, not pure Zag)

## Mechanism vs glue

- Mechanism (pure Zag): `../src/sense_r28.zag` (percept programs only).
- Non-compliant (Python, should be Zag per prereg §2): two-leg gate (decision)
  and hash-chained ledger (verification) in `../scripts_gen/eval_r28.py`.
- Evaluation glue (Python, allowed): percept caching, bar computation.
