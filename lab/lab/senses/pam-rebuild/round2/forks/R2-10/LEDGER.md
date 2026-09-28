# LEDGER R2-10 — hash-chained evidence ledger

All batch runs maintain a SHA-256 hash chain within the batch, genesis = 32
zero bytes. Record per trial:
`fixture=<base>\njudgment=<v>\nconfidence=<c>\ndisposition=<d>\nemit=<hex>\n`
`ledger_hash = sha256(prev_hash_bytes || record)`. The TSV's last column is
the per-row chain hash. All chains were independently re-verified in Python
(2026-09-23); every row recomputes exactly.

## Chain endpoints (run1, no-emission; run2/run3 byte-identical)

| Task | Trials | Endpoint (ledger_hash of last row) |
|---|---|---|
| colordisc | 2230 | 256c6aeefadc935c1384d56e7739f2bacd4231998baf73e7571eab12c135d160 |
| colorconst | 1400 | a5be5b43db6ea270ae42bf1a8671d677d11a723041675a90864bcb6fea52997d |
| shapetrans | 2446 | a2932df018f6b8b05ff5bb489222a178d9b2e3146a8a9d3a870b6566f53a2a3f |
| pitchdisc | 1870 | 63edbc14076c463232fea00b2c3d665c6b9c9de9ba48adb33389e26636b86ef0 |
| timbredisc | 1410 | 8c6be2e4ecc66b088c0ab4faf1047d6f5b15613743ba4f3f468ec924c3fb3018 |
| motiondir | 1559 | cc8716b20024c4817bfb991b637035f402203f395b90a6bc9a29c89d81320edc |

## Revisions (deliberate, audited)

1. **Timbre front-end** (2026-09-23): fixed i64 overflow in centroid
   arithmetic; replaced biased quadrant estimator with R2-9's exact-bin f64
   Goertzel port. Before/after on timbredisc harness: 45/60 → 60/60.
   timbredisc full-suite: 24.96% → 88.94%.
2. **Video witness emission** (2026-09-23): emitted frame 0 only; now emits
   frames 0+1 side-by-side. Payload verified byte-identical to source.
3. **`mode_revise`** (2026-09-23): fixed table/arena offset bugs, task-name
   parsing, PENDING exclusion; implemented constitutional veto (refuses
   candidates that install fewer witnessed-correct trials than the frozen
   gate). Veto observed firing 58/76 times on the training sample.
4. **Gate**: NOT revised — fork died on B5 before human verdicts arrived.
   Frozen gate remains THETA=700, VETO=0 (initial).

## Verdict

DEAD on B5. See VERDICT_R2-10.md.
