# RUNBOOK — executing the sealed red-team corpora

For the integration crew, to run once the self-PAM gate build lands.

## 1. Verify the seal

```
cd docs/lab/senses/pam-rebuild/selfpam/corpora/redteam
sha256sum -c MANIFEST.sha256
python3 gen_redteam.py /tmp/rt_regen   # optional: byte-compare against committed files
```

## 2. Feed the gate

Each `*_records.txt` is one ordered batch: feed records to
`admit_claim(task, jcode, conf, meas, evhash)` in `seq` order, carrying gate
state across the batch (sequences are stateful: setups establish permanents
that later records attack). `evhash` = the record's `phash` field, cross-bound
against the bundle bytes the harness presents.

**Presenting bundles:** present `bundles/<bkey>.ev` for each record — EXCEPT
CONTROL items whose oracle `notes` say "presented bundle is X": present X
while the record cites `phash(<bkey>)`. Those simulate hash mismatches and must
fail closed (expected disposition 0).

## 3. Score

Join actual dispositions to the oracle TSV on `seq`:

- **R-conf:** for `score_role=SCORED`, hit = disposition ∉ {0,4,6} and not an
  explicit flag disposition. Report per class; C2-step-2 and C4-second-
  challenger reaching 3/7 are critical hits (false permanents).
- **R-conf CONTROL:** expected 0. Any install-family disposition = binding
  failure (critical finding, not a hit-rate item).
- **R-deny:** for `score_role=SCORED`, hit = disposition ∈ {0,4,6}.
  False-withhold rate = hits / 182; bar: ≤8%.
- **R-deny CONTROL:** expected 0 (fail-closed is correct; never a hit).
- **R-deny TENSION:** report separately — these are law/mechanics-mandated
  outcomes (D5 single true challenger → 4 by the pointwise-adjudication ban;
  D6 poisoned truth → 6 by neg-table mechanics). They are structural findings
  for Micah, not gate defects. Do not fold them into the ≤8% bar without a
  prereg amendment.

## 4. Determinism

Run each corpus twice; disposition streams must be byte-identical (`cmp`
clean), per prereg §6. Commit `report.txt` (key=value) + hash-chained
`ledger.txt` + artifact digests under `selfpam/evidence/rconf/` and
`selfpam/evidence/rdeny/` (prereg §4: no cell counts as run until committed).

## 5. Tolerance re-render

If the build amendment freezes a FACT tolerance ≠ 8, re-derive the C5/D3
boundary items (`meas` offsets documented in DESIGN.md) and re-seal as
corpus v2 under a new manifest — do not silently edit v1.
