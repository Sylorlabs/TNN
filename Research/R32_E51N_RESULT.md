# R32 E51N — Domain-Separated World RNG + E51M Replication Result

Date executed: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Status

`VALID NATIVE NEGATIVE — CALIBRATION DOSE/CAPACITY PLATEAU WITH TRADEOFFS`

E51N repaired the evaluator seed/world namespace without changing learner cognition, then repeated the E51M calibration dose × capacity question under fresh, injective world identities.

## Native authority

- GitHub Actions run: `33344381320`
- source head: `d61079a57c9fe47547307613463c87b65588a7b1`
- artifact id: `9741534632`
- artifact digest: `sha256:2b3999dba639f9875d74ceb8c69cf3782310f811047c5646f055edfc4db79757`
- assembled native source SHA256: `34b8495bb3c1f7f12b04966215b360a1e5ccac44e9d705e4daa3ad98401bf552`
- frozen E45 core SHA256: `6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`
- native binary SHA256: `65882dba024957a68d4616e271c085b0b65bcf471573c24978857fcc06453292`
- two builds byte-identical: PASS
- native exit code: 0
- native experiment runtime: 84 s

## Evaluator infrastructure repair

Fresh world identities:

- development: 55,000,000 .. 55,012,959
- validation: 56,000,000 .. 56,005,399
- sealed confirmation: 57,000,000 .. 57,010,799

Integrity:

- world partitions disjoint: PASS
- five evaluator RNG domain initial-state ranges disjoint: PASS
- requested worlds: 29,160
- assignment failures: **0**
- E50 parent integrity: PASS
- learner change relative to E51M: 0
- topology change: 0
- graph privilege: 0
- UNKNOWN positive target: none
- UNKNOWN learned parameters: zero
- base terminal fit identity: PASS
- scalar forward/reverse identity: PASS
- hinge forward/reverse identity: PASS
- overall E51M replication integrity gate: PASS

This establishes the domain-separated world identity/RNG transport as a scalable evaluator infrastructure replacement for the exhausted global transient-PRNG-state allocator. It is evaluator infrastructure, not a cognitive improvement.

## Validation grid

Format: `known correct reachability / 4200 ; no-unique UNKNOWN reachability / 1200`.

| Development dose | 0 hinges | 4 hinges | 8 hinges | 16 hinges |
|---|---:|---:|---:|---:|
| 1x / 55,080 states | 4195 ; 1157 | 4192 ; 1156 | 4194 ; 1162 | 4191 ; 1176 |
| 2x / 110,160 states | 4194 ; 1160 | 4190 ; 1157 | 4185 ; 1175 | 4189 ; 1180 |
| 4x / 220,320 states | 4194 ; 1157 | 4191 ; 1158 | 4185 ; 1173 | 4191 ; 1174 |

Uncalibrated base: `4191 / 4200 known ; 1098 / 1200 no-unique`.

No arm reached the exact validation gate. Confirmation remained sealed.

## Why the coarse printed flags are not the conclusion

The inherited E51M helper prints `dose_signal=1` and `capacity_signal=1` when **any single adjacent step** gives a local Pareto improvement. E51N's preregistered scientific interpretation requires a meaningful monotone direction, not an isolated local step.

The actual grid is not monotone:

- at 0 hinges, increasing 1x→2x loses one known case while gaining three UNKNOWN cases, and 4x then gives those UNKNOWN gains back;
- at 8 hinges, more dose sharply loses known reachability while gaining some UNKNOWN reachability;
- 16 hinges improves UNKNOWN over the linear arm but repeatedly sacrifices known reachability;
- 4x does not dominate 1x at any capacity;
- greater hinge capacity does not consistently dominate lower capacity.

Therefore the defensible classification is a **dose/capacity plateau with operating-point tradeoffs**, not a validated training-dose rescue or monotone capacity curve.

## Development-fit evidence

Even at 4x dose the boundary remains substantially heterogeneous:

- linear sign fit: positive 138,252 / 152,283; negative 33,594 / 68,037;
- 16-hinge sign fit: positive 134,013 / 152,283; negative 39,668 / 68,037.

Additional additive hinges mostly move the positive-vs-negative operating point rather than solve the boundary. This matches E51J–L's diagnosis and survives a much larger valid development dose.

## Causal conclusion

The current scalar calibration deficit is not explained by:

- exact state aliasing (E51F ruled that out);
- too little 1x training dose alone;
- a small shortage of additive hinge capacity;
- the exhausted old seed namespace.

The remaining evidence points to **local / heterogeneous calibration geometry**: distinguishable learner states require different commit-vs-UNKNOWN corrections that a single global scalar surface plus a few additive hinges cannot express without trading one region against another.

The next justified mechanism is a bounded learner-owned local/prototype calibration memory on the same 32-feature state and frozen commit ordering. It must recruit its own prototypes from development residuals, pay explicit memory/execution cost, preserve UNKNOWN=0, and be compared against the valid E51N global controls. This is not a graph rewrite.

No E51N result promotes R32 or establishes AGI.
