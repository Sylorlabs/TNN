# HEAD_TO_HEAD.md — recycle fork vs delete-only mainline

## Baselines

- **Fork** (`~/workspace/strength-recycle/`, this work): TNN evicts via `st_recycle`
  (audited repurposing, slot stays live); revision via evidence + priced
  `st_delete_strong`; `st_kill` trainer-only. All 36 S1 cells ST_INVALID 0,
  2× byte-identical.
- **Mainline** (`~/workspace/strength-delete/`, `trial_bin` built 2026-09-26
  04:53): delete-only with hole fixes in progress. B2/VUP valid; B2/WBS and
  B2/JI cells report **ST_INVALID 1** (learner-side `c.invalid`, checker clean)
  — the mainline is mid-fix and NOT a valid behavioral baseline. The
  comparison below is therefore fork-measured vs mainline-design-intent,
  stated openly.

## Safety properties (the required three)

| Property | Fork evidence | Status |
|---|---|---|
| No free destruction | `recycle_attack` R2/R5: retiring an 80-strength judgment into a 1-strength placeholder, then deleting the placeholder, costs n(80)=4 cites, not n(1)=1. The lien makes recycle→delete never cheaper than direct delete. | HOLDS |
| No cite double-spend | R1: 4 cites recorded pre-recycle cannot pay for post-recycle delete (refused 109 with 0 fresh cites; OK after 4 fresh cites). Recycle opens a new effort window; old cites detach. Checker `ck_del_cite_*` clean. | HOLDS |
| No silent resurrection | Gate: delete→recycle refused 122. R6: dead/core/pinned/force-pinned/zero-strength all refused with audited codes. `st_refusals_clean` + `ck_no_bad_recycle` clean on all 36 cells. | HOLDS |

## Where recycle wins vs delete-only

1. **No kill path needed for routine eviction.** The mainline's hole-1 saga
   (free kill → priced kill → remove kill) exists because eviction needed a
   destruction-shaped op. Recycle gives TNN a first-class, non-destructive
   eviction: the saturation path never touches destruction machinery.
2. **Audited lineage.** Kill+add shows "X died, Y born" as two unrelated
   entries. Recycle shows "X became Y because Z" in ONE entry with
   before/after snapshots and a purpose code — strictly more informative to
   an auditor.
3. **Revision still works, honestly.** Fork WBS: 50–52/50–52 revised (100%),
   0 false revisions, median latency 75 (waits for 4 contradiction cites to
   afford the n(80)=4 price). The priced revision path preserves the
   trial's revision metric without any free kill.
4. **Zero drops at S1.** P1_CT 500/500 admitted; the store churns without
   losing candidates to unaffordable eviction.

## Where recycle loses vs delete-only

1. **The free-retirement surface.** Recycle costs no cites. TNN can retire ANY
   unpinned judgment (e.g. an 80-strength one it finds inconvenient) into a
   placeholder for one audited op. The ledger shows it and the lien blocks
   cheap follow-on destruction — but the retirement itself is free. Whether
   "audited but free retirement" is acceptable is a LAW question, not a
   mechanism question; the mechanism cannot distinguish "genuine repurposing"
   from "inconvenient judgment retired." This is the fork's open wound and
   the red team's primary target.
2. **Lien complexity.** The anti-laundering rule adds a carried-debt concept
   (max old HW, previous lien; cleared only by priced destruction) with a
   documented conservative edge (rollback-of-recycle keeps the lien →
   possible overpricing). More machinery = more audit surface.
3. **Revision latency.** Median WBS latency 75 vs the free-kill era's ~25–50:
   TNN must accumulate 4 contradiction cites before it can afford to destroy
   an 80-strength contradicted judgment. Honest cost of the signed pricing
   law, but a real behavioral delta.
4. **Capacity never frees.** Delete empties slots; recycle keeps them live.
   A store under pure recycle never shrinks — pressure is expressed as
   placeholder churn, not capacity recovery. (Whether that matters depends
   on whether slots are the scarce resource.)

## Honest-operation summary (fork B2, S1, all valid)

- VUP: held 29–30/150, P1_PTR 8/8, P1_EC 8/10, P1_CT 500/500, P2_ER 29–30/150,
  0 drops, 0 abandons.
- WBS: revised 50–52/50–52, median latency 75, false revisions 0/20–21.
- JI: rejected 6/6, junk ≤1, entrenched 0/6.

## Bottom line for the verdict

The mechanism holds all three safety properties under the implementer's
attack battery. The residual risk is not mechanical but semantic: free,
audited retirement of arbitrary judgments. The blind red team's findings
decide whether that semantic risk is exploitable in a way the lien does
not catch.
