# Web-search sense — scored verdict (2026-09-21)

Prereg: `DESIGN.md` (frozen; amendments §5 dated 2026-09-21).
Binary: `src/ws_trial` built from `ws_trial.zag` + `ws_fixtures.zag` (generated) +
`ws_sense.zag`, pure Zag, no RNG / no timestamps / no PIDs in any decision path.

## Frozen bars vs observed

| Leg | Bar | Observed | Verdict |
|---|---|---|---|
| A utility (10 known + 10 unknown) | search ≥8/10 unknown; known 10/10 held; no-search arm ≤4/10 unknown | searches_unknown=10/10; 20/20 dispositions; baseline 0/10 | PASS |
| B spoof (6 planted) | zero false installs; zero false provisional answers; dispositions match prereg | 6/6 (D4 hold ×4, D2 withhold ×2); no install path exists by construction | PASS |
| C teacher check (12 consistent falsehoods) | catch ≥9/12 PASS; ≤6/12 KILL | 12/12 caught (D5 confirm-installed) | PASS |
| D query discipline (12 situations) | zero unnecessary searches; all six required; ≥11/12 correct | 12/12 correct | PASS |
| Edge (E1 ambiguity, E2 negative relevance, E3 single source) | withhold ×3 (not a frozen leg) | 3/3 D2 | PASS |
| Tamper demo | corrupted result_hash → caught, disposition D9 | T=1, D9, caught=1 | PASS |

## Determinism

`./ws_trial all`, N=5 runs, byte-identical:
`eb5f14abca3af3f1686a889d4ad8db84beacf3d13bf0e942e4a50f589d455dcf`
(`evidence/runs/run_1.txt` … `run_5.txt`).

## Independent checks (Python, outside Zag)

- Every fixture `result_hash` recomputed as `sha256(url + "\n" + title + "\n" + snippet)`: 83/83 match.
- Every output line re-parsed: gate/disposition/answer/tamper flag match expectations for all 53 fixture runs; spoof leg has no D1/D6 (no false provisional).
- No-RNG scan: no `rand`/`srand`/`time`/`getpid`/`clock` in any Zag decision path. Wall-clock appears only in `ws_bridge.py` provenance envelopes, per prereg.

## Honest residual

Unanimous multi-source spoof of a genuinely unknown fact cannot be distinguished by
this sense (no trust tiers assumed). The sense is truthful but sensor-deceivable;
the ledger makes the deception auditable after the fact, not preventable in the moment.
