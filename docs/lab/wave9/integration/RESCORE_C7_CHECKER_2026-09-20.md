# INDEPENDENT CHECKER VERIFICATION — INT-1 C7 RE-SCORE (2026-09-20)

**Scope:** verification of the exploratory re-score
`RESCORE_C7_DRAFT_METRIC_2026-09-20.md` under the DRAFT (unapproved) amendment
§3. Exploratory only. **§5 FAIL under the preregistered metric stands; no
verdict is rendered here.** I did not perform the re-score; all checks below
were re-derived independently.

## Method (deterministic, zero RNG)

1. Local `impl/` sources hash-compared against committed
   `evidence_s10_c5redesign/sources.sha256` — **match**.
2. Rebuilt pristine binary with the committed toolchain:
   SHA-256 `e673bae2c889b117db7656a4b77c11c4974bf6cd4823f05c50b806894c25acf0`
   — **byte-identical to the committed trial binary**.
3. Applied my own print-only instrumentation (own tag format
   `ICKR/ICKA/ICKH/ICKCAP`, independent of the analyst's `CHAIN_*`/`CAPCOMP`)
   at the exact ledger-append call sites (default-gate refusal in
   `seam4_compose`, `seam4_abstain`, `seam2_open`) plus a per-stage component
   line read directly from the metric fields. Ran s2–s5 (paired a/b:
   byte-identical 4/4) and `controls`. Instrumented run reproduced committed
   `C7_TELEMETRY …cap4,914,cap5,897` **exactly** → behavior-neutral.
4. Linked chains with my own Python script: forced =
   refusal(LG_O4/LG_OP_COMPOSE, rc=311, b1=need_id, b2=0, a1=claim_cid) →
   abstain(slot=need_id, rc=0, b1=cid) → hyp-open(slot=cid, rc=0), same
   episode, 1:1 uniqueness enforced.
5. Reconstructed the gate-less positive-control variant per the documented
   procedure (default gate excised, everything else identical + my ICK
   instrumentation) and ran `controls` + s2–s5.
6. Cross-checked the repaired baseline against committed
   `evidence_s10_repair/` and the `5aa2fb13` blob via the GitHub API.

**Ledger-access caveat:** the binary emits no ledger dump, so chain
identification is indirect — via print-only instrumentation at the ledger-append
sites on a byte-identical tree/binary. The emitted tuples correspond 1:1 to
ledger entries by construction; neutrality is proven by the exact
`C7_TELEMETRY` reproduction. I could not re-check the analyst's ephemeral
`/tmp` CHAIN logs (not committed); everything above is my own re-derivation.

## Item-by-item verdicts

1. **Forced-hypothesis counts — PASS.** My linker: DC-2=**17**, DC-3=**17**,
   DC-4=**17**, DC-5=**0**. 51/51 complete chains; **zero orphan refusals,
   zero orphan abstains, zero duplicate links**; every abstain rc=0 and every
   open orc=0. DC-2 additionally has exactly **12 elected abstains** (n=0
   `force_abstain` path), each with a completed hypothesis open — none
   refusal-linked. Matches the analyst's accounting exactly.
2. **Arithmetic + decomposition — PASS.** My ICKCAP components:
   DC-2 (256,0,639,29)→924; DC-3 (256,2,639,17)→914; DC-4
   (256,2,639,17)→914; DC-5 (256,2,639,0)→897. Recomputed `cap_old` matches
   committed `C7_TELEMETRY` exactly. Draft re-score: cap4 914−17=**897**,
   cap5 897−0=**897** → **897→897, ALIVE** under the draft bar. Confirms the
   analyst's numbers and the draft's expected re-score.
3. **Positive control — PASS.** My gate-less reconstruction reproduces
   `C7_POSCTRL,cap4d,897,cap5d,641` exactly; independently measured
   decomposition dep4=(256,2,639,0), dep5=(0,2,639,0) — collapse entirely in
   `composites_ok` 256→0. Zero refusal-fed hypotheses: structurally (gate
   excised; only remaining PARTITION site is the arm filter with b2≠0, which
   `loop.zag` never routes to L1; teacher refusals are `SEAM_REFUSED_TEACHER`,
   a different rc, never routed) and observationally (**zero ICKR lines on the
   default path across s2–s5**). Forced=0 in both arms → reads identically
   under the draft metric → **C7 still fires DEAD**. Void condition does not
   trigger. (Note: gate-less sources were never committed; I reconstructed
   them per the documented procedure. The 897→641 figures are additionally
   corroborated by the repair run's committed `C7_POSCTRL`.)
4. **Baseline — PASS.** Committed repair evidence:
   `C7_TELEMETRY …cap4,897,cap5,897`; L1COVER 0/0 in DC-3/4/5 (12/12 elected
   in DC-2); `C7_POSCTRL,cap4d,897,cap5d,641`. Structural: `loop.zag` @
   `5aa2fb13` contains **no `SEAM_REFUSED_PARTITION`** (GitHub blob
   `b56ea613a42e`) — refusals could not feed L1. Draft metric: forced=0 →
   **897→897, reading unchanged**.
5. **Displacement mechanism — PASS (sanity).** Statically, proactive
   (`loop.zag:189`, even episodes), refusal-fed (`loop.zag:156`), and elected
   (`loop.zag:170`) opens all draw from the same `next_cid < o2_cap` budget,
   and all three increment `met.hypotheses`. Empirically `mhyp` is flat at
   639 across DC-2/3/4/5 while proactive opens measure 610/622/622/639
   against abstain-fed 29/17/17/0 — **exact 1:1 displacement**. The old-metric
   +17 inflation came solely through `tr.l1_opened`. The mechanism note is
   sound.

## Discrepancies / notes

- **Minor (flagged, not a failure):** the draft's prose formula ("proactive O2
  hypotheses + elected L1 abstain-hypotheses") read literally over *measured*
  counts gives DC-4 = 256+2+622+0 = 880, not 897. The subtraction
  operationalization (`cap_old − forced`) matches the draft's own declared
  expected re-score (914−17=897) and coincides with the literal formula only
  under exact 1:1 displacement — which holds empirically (budget binds, mhyp
  flat at 639). Under the literal reading the bar's `cap5==cap4` would be
  undefined for cap5>cap4, so the subtraction reading is the only coherent
  one. Worth one line of clarification in the draft if approved.
- The analyst's "composites/commits" phrasing for the control collapse:
  measured collapse is `composites_ok` 256→0 only (`commits_constr` 2→2) —
  the analyst already noted this; no discrepancy.
- DC-2 re-scores to 907 (924−17) under the draft; C7 compares only DC-4/DC-5,
  so no effect on the C7 outcome. Reported for completeness.

**Bottom line:** all five items independently re-derived and confirmed. No
discrepancy in any number the analyst reported. The re-score's 897→897 ALIVE
reading under the draft metric is arithmetically and mechanistically sound;
the §5 FAIL under the preregistered metric is untouched.

*Independent checker, 2026-09-20. Deterministic methods, zero RNG. No verdict
rendered — authority sits with Micah and the prereg.*
