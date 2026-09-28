# PREREG5R — V4 cross-step annihilation repair (frozen 2026-09-27)

**Line:** white-box repair of the REDTEAM5 R1a/R1b defect. V4 stays
experimental — this is a repair line, not an adoption line.

## M-R1 — mechanism claim (white-boxed from the R1a trace)

In `ob_audit` the order is: duel → 2a → 2b → `audit_cleanup` (deferred).
`audit_invalidate`'s annihilation guard defines a "live bid" as
bid-row status alive only (`lr_get(wled,b,8)==0`). When 2a denies a fact,
the bids grounded on it become *effectively dead* (the deferred cleanup
will remove them) but stay row-alive until cleanup runs after 2b. 2b's
guard therefore counts phantom bids toward `live_after` and can choose a
denial whose genuinely-live consequence set is empty → all bids cleaned
→ NO_VERDICT. The same phantom window exists for 2a after a duel
reading-kill (bids gated on the dead reading are phantoms until cleanup).

## F-R1 — fix (one semantic change, no bridges)

The guard counts a bid as live iff it would survive `audit_cleanup`
right now: bid row alive AND gating reading alive AND supporting fact
alive (the exact cleanup survival predicate). Applied to every
`audit_invalidate` call. Provably a no-op whenever row state and support
state agree — i.e. it can only change decisions inside the
deferred-cleanup phantom window.

## Kill bars

- **K-R1 (defect gone):** fixed binary on redteam/rt.tsv: R1a and R1b
  produce a verdict (16, the human-right answer) instead of NO_VERDICT;
  R1c and all other rt items unchanged; 2 reruns byte-identical.
- **K-R2 (zero side effects):** fixed binary on v8.tsv (20 items, 5 modes)
  and v7.tsv (44 items, 8 modes), 3 reruns each: outputs byte-identical
  to the committed runs. Any deviation = bar failed, fix rejected.
- **K-R3 (determinism / no RNG):** all reruns byte-identical; source
  audit: no rand/time/entropy; syscalls read/write/open/close only.
- **K-R4 (no new annihilation):** fresh red-team variant set aimed at
  cross-step annihilation (predictions written before running): zero
  NO_VERDICT, zero unpredicted flips, independent red team no-kill.

Verdict rule: all four bars must hold or the repair is killed. Evidence
commits to tnn-native-lab under docs/lab/onebrain5/v4-repair/.
