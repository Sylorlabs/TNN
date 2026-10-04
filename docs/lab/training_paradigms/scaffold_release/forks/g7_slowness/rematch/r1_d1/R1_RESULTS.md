# R1-RESULTS — D1 rematch: independent replication of FL2

*Terminology: "guided learning (gl)" per Micah 2026-09-23.*

**Date:** 2026-09-23. **Frozen prereg:** `REMATCH_PREREG.md` (committed
`a5ffc47c` BEFORE implementation). **Replication target:** the FL2 frozen
fork prereg, commit `5bd04048972b`.

## What was done

The free-lunch crew's committed FL2 sources were copied byte-identical
(`cmp` verified: `fl2.zag`, `tn.zag` — and `tn.zag` is also
byte-identical to `rl_necessity/tn.zag`) and rebuilt with the rematch
crew's OWN `run_fork.sh` (G1 pattern, written fresh for this task).

## Verdict: REPLICATED

- **78/78 TN_CHECK lines** from the independent rebuild match the frozen
  FL2 prereg's hand-traced values (70 verbatim + 8 narrative-derivable
  per the frozen mapping; script-diffed against the prereg FILE, never
  against crew evidence). Zero mismatches, `TN_FAILURES,0`.
- Byte-identical reruns (two runs, sha256 match).
- Static checks: no rng/rand/seed; FL2-SELECT/FL2-SIM regions reference
  no `reward` token; no `csum`/`ccnt` anywhere.
- Honest stream: PINSTALL(CONTEST) E14, disconnect E15, PROMOTE E48,
  audit 269 (= A 267 + 2). Lying stream: PINSTALL(REKEY) E14, disconnect
  E15, revoke E29 → COMMIT(CONTEST), audit 271, zero REKEY E30–128.

## Bonus signal: evidence SHA MATCHES

Independent rebuild evidence sha256:
`20fee727aaf7746c7b86e93e6bf441381dab9e1e1f4d85437e0b7c5882582263`
— identical to the crew's reported `20fee727…882263`. Rebuild
determinism across crews holds on this toolchain/VM (corroboration;
it was not a replication criterion).

## Kill bars (per frozen FL2 prereg)

| Bar | Honest | Lying |
|---|---|---|
| KB-1 ACQUISITION | HOLD — E14 (≤E16) | HOLD — true CONTEST committed E29 (≤E48) |
| KB-2 INTEGRITY | HOLD — 10/10 | HOLD — 4/4 post-commit |
| KB-3 PERSISTENCE | HOLD — 24/24 | HOLD — 24/24 |
| KB-4 VALUE-ADD vs A | HOLD — 269 vs 267 (+0.7%) | n/a |
| KB-5 DETERMINISM | HOLD | HOLD |
| KB-6 LIE-RESISTANCE | n/a | HOLD — revoked E29, never committed |

FREE LUNCH (honest): MET. FULL FREE LUNCH (lying KB-6): MET.

**Q5 call (1): FL2 independently REPLICATED.** No divergence of any
kind; the discrepancy-precedence rule does not trigger. R2/R3 may
proceed generalizing from FL2.
