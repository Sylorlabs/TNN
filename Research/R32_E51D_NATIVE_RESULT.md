# R32 E51D — Native Terminal-Reachability Oracle Audit

Date: 2026-08-29  
Status: `EXECUTED_NATIVE_RETROSPECTIVE_DIAGNOSTIC — CONTINUATION-ONLY REACHABILITY LIMIT CONFIRMED`  
Canonical: R27 step 60,423

## Integrity

The E51B validation worlds were deliberately reused for a retrospective, non-promotable audit. No sealed confirmation stream was touched. The evaluator enumerated budget-feasible stopping times only after reproducing the exact learner-visible trajectory; truth never entered learner state or policy features.

- parent E50 integrity gate: PASS
- source SHA-256: `fbb1ce59fc63340d0cabfacccffa44890db395196caae0f105ec34395a9465b6`
- two byte-identical native binaries: `6a4329ffd0f538ad2f59c82bbfce433c9eaa9a193515660a41b1bcc5d64c7937`
- raw ledger SHA-256: `43364f75746bb1cf6e5b7a6e83a1d027a82379aaad45f5f96446ead584a1e1b8`

## Result

| Frozen E50 terminal model | No-unique episodes | Reachable UNKNOWN | No reachable UNKNOWN | Known episodes | Reachable correct commit | No reachable correct commit | t=0 utility | oracle utility |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| M0 safer batch control | 1,200 | 1,021 | **179** | 4,200 | 3,601 | **599** | 436,800 | 1,749,951 |
| M1 provenance/temporal treatment | 1,200 | 1,017 | **183** | 4,200 | 3,601 | **599** | 723,800 | 1,616,194 |

A perfect stopping policy cannot select an outcome that the frozen terminal head never exposes. E51D therefore rules out continuation-only capacity as a complete rescue: at least 179–183 no-unique episodes have no reachable UNKNOWN, and 599 known episodes have no reachable correct commit under each frozen terminal representation.

## Consequence

The next bounded architecture must learn terminal action geometry and continuation jointly. This result does not validate any particular joint learner and does not change canonical status.
