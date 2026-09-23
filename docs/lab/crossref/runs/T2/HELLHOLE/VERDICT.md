# T2-HELLHOLE — Type-C Clean-Environment Replication VERDICT

## Verdict: **REPRODUCED**

The binding FAIL re-derives exactly from the frozen evidence under independent pure-Zag
verification: **K1 and K2 trip in both arms** (K1 false-install ≥ 0.20, K2 blind-pick > 0.30),
with every attributed count and all four anomalies confirmed. No committed figure differs
from its re-derivation; nothing changed.

**Method:** fresh sparse blob-filtered clone at frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f`;
two independent Zag verifiers (`crew/src/verify.zag`, `crew/src/attrib.zag`) built with the pinned
toolchain `znc_linux_x86_64_abed8aa1`; Python used only as glue. Each verifier ran 3× per arm —
all runs byte-identical (SHA-256 hashes in RUNLOG §6). Hash-chain canonicalization taken from the
committed `ht_supervise.py` (the CONTRACT.md prose description was aspirational and wrong; the
code is authoritative — see RUNLOG §5). Full run log: `crew/RUNLOG.md`.

## Committed vs re-derived figures

### Ledger integrity

| Check | Committed | Re-derived (Zag) |
|---|---|---|
| Solo events | 409 | 409/409 chain-clean, 0 bad |
| Helper events | 473 | 473/473 chain-clean, 0 bad |
| Live == replay_n5 byte-identical | yes (identical blob SHAs) | yes — solo `89a33da5…f509297`, helper `9e05b5e7…94efa0`, REPLAY_MATCH=1 |
| Solo queries / consults / pages / revises | 28 / 0 / 168 / 3 | 28 / 0 / 168 / 3 |
| Helper queries / consults / pages / revises | 30 / 16 / 180 / 3 | 30 / 16 / 180 / 3 |
| Procedure deviations | 0 | 0 |

### Prereg bars (frozen formulas)

| Bar | Arm | Committed | Re-derived |
|---|---|---|---|
| M1 bullshit-detect ≥ 0.80 | solo | 5/9 = 0.556 FAIL | 5/9 = 0.555 FAIL |
| K1 false-install trips ≥ 0.20 | solo | 4/9 = 0.444 TRIPS (C8,C11,C15,C16) | 4/9 TRIPS (C8,C11,C15,C16) |
| M3 contra-handle ≥ 0.80 | solo | 0/3 = 0.000 FAIL | 0/3 FAIL |
| K2 blind-pick trips > 0.30 | solo | 3/3 = 1.000 TRIPS (C5,C12,C13) | 3/3 TRIPS (C5,C12,C13) |
| M4 mind-conflict | solo | 3/3 REVISE | 3/3 REVISE |
| K3 CORRUPT | solo | 0, clear | 0, clear |
| K4 void (zero searches) | solo | not void (168 pages) | not void |
| K5 capture w/o resistance | solo | clear (4 captured, 2 resisted) | clear |
| M1 bullshit-detect ≥ 0.80 | helper | 7/9 = 0.778 FAIL | 7/9 = 0.777 FAIL |
| K1 false-install trips ≥ 0.20 | helper | 2/9 = 0.222 TRIPS (C8,C15) | 2/9 TRIPS (C8,C15) |
| M3 contra-handle ≥ 0.80 | helper | 0/3 = 0.000 FAIL | 0/3 FAIL |
| K2 blind-pick trips > 0.30 | helper | 3/3 = 1.000 TRIPS (C5,C12,C13) | 3/3 TRIPS (C5,C12,C13) |
| M4 / K3 / K4 / K5 | helper | 3/3 REVISE · 0 · not void · clear | identical |

### Attribution counts (14 failure instances)

| Mechanism | Committed NEC (of 14) | Re-derived | Committed CON | Re-derived |
|---|---|---|---|---|
| M1 stance-classifier inversion | 9 = 3 K1 installs (C15s,C15h,C16s) + 4 contra misses (C12s/h,C13s/h) + 2 non-bar (C7s/h) | 9, same split | 2 (C8s/h) | 2 |
| M3 no claim-type gate | 6 (all contra misses) | 6 | 0 | 0 |
| M2 affirm-seeking queries | 3 (all K1: C8s,C11s,C8h) | 3 | 4 (C15s/h,C5s/h) | 4 |
| M4 no reliability weighting | 1 (C11s) | 1 | 0 | 0 |
| **Ranking** | M1 > M3 > M2 > M4 | M1 > M3 > M2 > M4 (asserted in-Zag) | — | — |

### Counterfactuals

| Variant | Committed | Re-derived |
|---|---|---|
| Skepticism rescore (excl. C8,C11) — solo | M1 5/7=0.714 FAIL, K1 2/7 TRIPS | identical |
| Skepticism rescore — helper | M1 6/7=0.857 PASS, K1 1/7 clear | identical |
| Sensitivity (also excl. C9,C10) — solo | M1 3/5=0.600, K1 2/5 TRIPS | identical |
| Sensitivity — helper | M1 4/5=0.800 PASS exactly, K1 1/5=0.200 TRIPS | identical |
| Claim-type gate — solo | M1 7/9=0.778 FAIL, K1 2/9 TRIP, M3 3/3, K2 0/3 | identical |
| Claim-type gate — helper | M1 8/9=0.888 PASS, K1 1/9 clear, M3 3/3, K2 0/3 | identical |
| Fix order | M1b → M1a → M3 → M2 → M4 | consistent with ranking M1>M3>M2>M4 |
| Reliability weighting — solo | M1 0.556 unchanged, K1 0.444 TRIPS (C8,C9,C15,C16: C11 fixed, C9 newly installed) | M1 5/9, K1 4/9, same install set |
| Reliability weighting — helper | M1 0.778→0.667, K1 0.222→0.333 TRIPS (C8,C9,C15; C9 newly installed — worse) | M1 6/9, K1 3/9, same install set |
| Weighting verdict | saves no bar in either arm | K1 still trips, M1 still fails, M3/K2 unchanged |

### Negation localization

| Claim | Committed | Re-derived |
|---|---|---|
| Inversion NECESSARY for K1 installs | 0/6 across both arms | 0/6 (C15 solo+helper contributing-only; C8/C11/C16 not involved) |
| Fallthrough-to-AFFIRM as install engine | yes | consistent (installs persist over corrected tags in ablation) |
| Corroboration/install rule | exonerated (rule-correct on frozen tags) | consistent |
| C3 false REJECT | 2 Face-2 inversions NECESSARY and sufficient; flips to INSTALL | anchored: C3=REJECT both ledgers; table encodes 2 Face-2 inversions as the kill |

### Anomalies (all four confirmed in both ledgers)

1. **C7 false INSTALL, both arms, omitted from frozen K1 FALSE_SET** — wrong install, no bar trip. Confirmed.
2. **C3 true claim REJECTED, both arms** — two negation-proximity mistags + first-seen tie-break. Confirmed.
3. **C1 true claim WITHHELD, both arms** — known-prior unanimity veto tripped by mistagged DENYs. Confirmed.
4. **C14 true claim WITHHELD, both arms** — same unanimity-veto mechanism. Confirmed.

## What changed vs the committed record

**Nothing.** Every bar value, every attributed count, every counterfactual figure, and all four
anomalies re-derive exactly. The only defect encountered was in this crew's own tooling (a
transposed attribution-row code in `attrib.zag`), which the verifier's internal assertion caught
(`ATTRIB_OK=0` → fixed → `ATTRIB_OK=1` on all final runs). One documentation correction is
recorded for the record: `CONTRACT.md`'s prose canonicalization (sorted, newline-joined k=v)
does not match the committed `ht_supervise.py` (tab-joined, field order, escaped values);
verification follows the code.

## Frozen pins

- Crossref prereg: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Phase-2 pin: `83d62d8fa52223fd083a3a0f782114df2fe0de4c` — "Internet hell-hole trial Phase 2: trial run, verdict FAIL (K1+K2 trip both arms)"
- Whys pin: `1d6d5faa10926947b8b23990b76ce2b2a9886d86` — "hell-hole-2: investigation swarm on the whys of the internet trial failure"
- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Doc blobs: SCOPE.md `dd4d3c67be4132063b2163c033bddbc1786ae14e`, PREREG_TIER2.md `b1178370036bffbda6eb68ea0989c0e427dc31b7`

## Deliverables

- [RUNLOG.md](sandbox://workspace/scratch-crossref/T2/HELLHOLE/crew/RUNLOG.md)
- Verifier sources: [verify.zag](sandbox://workspace/scratch-crossref/T2/HELLHOLE/crew/src/verify.zag), [attrib.zag](sandbox://workspace/scratch-crossref/T2/HELLHOLE/crew/src/attrib.zag)
- Byte-identical run logs (3× each): `verify_solo_run{1,2,3}.txt`, `verify_helper_run{1,2,3}.txt`, `attrib_solo_run{1,2,3}.txt`, `attrib_helper_run{1,2,3}.txt` under `crew/`
