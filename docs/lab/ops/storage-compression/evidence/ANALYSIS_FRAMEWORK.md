# Storage-compression results — analysis framework

## Schemes

| Scheme | Description | Expected B/fact (written) |
|---|---|---:|
| base | Baseline: 24B slot + 4B index + 64B audit | 92 |
| S1 | FL1 (slot id removed) + FL2 (24B compact audit) | 48 |
| S2 | S1 + FL3 (sparse lc/strength) + FL4 (chunk clock) | 40 |
| S3 | S2 + H5 (identity index, 4→0B) | 36 |
| S4 | S3 + H1 (audit→per-chunk SHA-256 chain + event log) | ~12.01 |
| S5 | S4 + H3 (per-chunk tagged-width values) | ~5.6 |

## Metrics per scheme (3 reps at 240K and 1M)

- Logical bytes/fact (SCALE_MEM, written basis)
- Install µs/fact (THRU_INSTALL ns_teach_cpu_total / N — CPU time, contention-immune)
- Recall probes/sec (THRU_RECALL ns_cpu_total — CPU time)
- Eval-sweep probes/sec (THRU_EVALSWEEP — wall clock, noisy under contention)
- Digest (KB-CORRECT: must match base)
- Flaw battery (must be 96/96)
- Bytes saved per µs of slowdown: (92 - scheme_bpf) / (scheme_us - base_us)

## Kill bars

- KB-CORRECT: digest mismatch or flaw < 96/96 → DEAD.
- KB-WIN: install slowdown > 10% AND < 20% headline reduction → DEAD.
- KB-RECALL: recall slowdown > 10% → flagged (not necessarily dead if install wins big).
- S4/H1 structural: tamper demo must detect; replay must be byte-identical.

## Notes

- Deliberation episodes/sec: N/A for the throughput instrument (no deliberation path).
  The deliberation learner is a separate instrument; wiring compression there is future work.
- Cold-fact consolidation: no hot/cold skew in the battery; scoped as designed-not-measured.
- String interning (H6): predicted dead on the instrument (values are small ints);
  designated for string-ref workloads (prereg family b).
