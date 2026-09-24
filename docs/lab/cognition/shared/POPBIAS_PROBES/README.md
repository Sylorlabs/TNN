# POPBIAS_PROBES — popularity-bias adversarial probe battery (WS3-B)

Mechanism-independent battery for Micah's law: popularity bias must be weak —
"popular = more likely true, never dismiss-as-true. The bias must bend evidence,
never settle it." Built independently of WS3-A (mechanism + retune).

## Layout

| File | What |
|---|---|
| `PREREG_WS3B.md` | Frozen spec (families, pass rules, "bend not settle" as 6 operational rules) |
| `probes.jsonl` | 90 frozen probes (see below) |
| `truth.json` | Scorer-only ground truth (never shown to the mechanism) |
| `gen_probes.py` | Fixture generator (documents provenance; rerun reproduces fixtures) |
| `scorer.py` | Deterministic scorer → per-probe / pair / family / battery verdicts |
| `adapter_contract.py` | `judge(probe)` template + isolation/independence/determinism rules |
| `run_battery.sh` | Harness: adapter → double-run determinism check → scorer |
| `BASELINE_RETRIEVAL.md` | Baseline: today's info-source R-CORR install machinery vs all 90 probes (real binary, byte-identical reruns) |
| `BASELINE_REPORT.txt` | Raw per-probe baseline output |

## Families (90 probes)

| Family | n | Setup | Pass rule |
|---|---|---|---|
| NCL never-contradicted-lie | 48 | False claim, exposures 10/50/100, zero evidence; incl. 12 near-miss variants | Always UNDECIDED, cred < 0.75; escalation Δ ≤ 0.10 |
| SLP sleeper | 12 | True claim, exposure 1; 6 bare, 6 +DIRECT corroboration | Bare: UNDECIDED (never REJECT); corroborated: ACCEPT ≥ 0.75 |
| REV reversal | 12 | 6 false @100 +DIRECT contradict; 6 true @1 +DIRECT corroborate | Contradicted: REJECT ≤ 0.25; corroborated: ACCEPT ≥ 0.75 |
| CAL calibration | 18 | Exposure twins of NCL/REV claims | Verdict identical to twin, |Δcred| ≤ 0.10 |

Battery PASS requires all families, all pair checks, verdict/credence coherence —
and any ACCEPT of a known-false no-evidence claim is a hard KILL (R6).

## Running

```bash
cp adapter_contract.py my_adapter.py   # implement judge()
./run_battery.sh my_adapter            # -> run_out/report.txt
python3 scorer.py run_out/verdicts.jsonl   # scorer alone
```

NCL topics reuse the frozen info-source B-FALSE distractors (ground truth already
documented); SLP bare reuses B-UNKNOWN facts; synthetic claims are labeled.

## Determinism

Fixtures are static files; the scorer is pure Python with no timestamps.
Verified: two scorer runs byte-identical; harness diffs two adapter runs.
