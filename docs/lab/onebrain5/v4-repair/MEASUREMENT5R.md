# MEASUREMENT5R — V4 cross-step annihilation repair results (2026-09-27)

## Mechanism (M-R1, white-boxed from the R1a trace)

`ob_audit` runs: duel → 2a → 2b → `audit_cleanup` (deferred). The
annihilation guard in `audit_invalidate` counted a bid as live from its
row status alone. When 2a denied a fact, bids grounded on it became
effectively dead but stayed row-alive until the deferred cleanup — so
2b's guard counted phantom bids toward `live_after` and could choose a
denial whose genuinely-live consequence set was empty. R1a trace:
2a denied fact 10 (forget fact, `chosen=10`), 2b's guard saw bid 15
(row-alive, fact-10-dead) as live → denied fact 11 (`chosen=11`,
`skipped_annihilate=0`) → `AUDIT_CLEAN` removed 15, 16, 22 → zero bids →
`NO_VERDICT`. The same phantom window exists for 2a after a duel
reading-kill (bids gated on the dead reading).

## Fix (F-R1)

Guard counts a bid as live iff it would survive `audit_cleanup` now:
bid row alive AND gating reading alive AND supporting fact alive — the
exact cleanup survival predicate. One semantic change, every
`audit_invalidate` call. No-op whenever row state and support state agree.

## Kill bars

- **K-R1 (defect gone):** v5 on redteam/rt.tsv — R1a/R1b now verdict 16
  (human-right) instead of NO_VERDICT; R1c unchanged at 16; all other rt
  items unchanged; 2 reruns byte-identical. Trace: 2b now
  `skipped_annihilate=1 chosen=-1 abstain_why=2`. PASS.
- **K-R2 (zero side effects):** v5 on v8.tsv (20 items × 5 modes × 3
  reruns) and v7.tsv (44 items × 8 modes × 3 reruns): 39/39 outputs
  byte-identical to the committed v4 runs. PASS.
- **K-R3 (determinism / no RNG):** all reruns byte-identical; source audit:
  no rand/time/entropy; syscalls write/open/read/close only on the run
  path. PASS.
- **K-R4 (no new annihilation):** fresh variant set W1–W5 (KB nouns, both
  2a/2b orderings). v4 control: W2–W5 → NO_VERDICT (genuine variants),
  W1 → 15 (non-annihilating control). v5: W2–W5 → 16 (repaired),
  W1 → 15 byte-identical to v4. First-draft variants V1–V4 were weak
  (no KB nouns → no facts extracted → no V4 engagement); recorded in
  PREDICTIONS5R.md addendum, not counted. **Independent red team
  (REPORT_KR4.md): NO-KILL.** 8 fresh attacks, predictions written before
  running, 8/8 correct on both binaries. 6 counted phantom-bid paths —
  duel-kill→2a phantom (D1b, T3), duel-kill→2b phantom (D2, D2b), classic
  2a→2b (Wc2, Wd) — all annihilate on v4, all produce winners on v5.
  The duel-kill→2a path (bids gated on the dead reading as phantoms for
  2a's guard) was theorized in M-R1 but never constructed before; the red
  team constructed it and the fix holds. 2 weak attacks predicted weak,
  confirmed weak.

## Plain English

The guard was counting dead bids as alive because cleanup runs late. The
fix makes the guard ask "would this bid survive cleanup right now?"
instead of "is its row still marked alive?" The two red-team items that
produced no verdict now produce the right answer, and all 39 existing run
outputs are byte-identical — the fix changes nothing except the defect.
V4 stays experimental.
