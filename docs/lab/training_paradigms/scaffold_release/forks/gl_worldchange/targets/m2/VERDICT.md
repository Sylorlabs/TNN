# VERDICT — H4 target M2: figure-it-out (no new primitive)

Mechanism: zero substrate change — `gl_substrate_m2.zag` is byte-identical
to the canonical substrate. One general transition classifier
(`wc_classify`) handles every value transition: teacher announcements
(`TEACH` conflicts, `UPDATE`) and authenticated world contradictions. A
teacher `UPDATE` passes the same establishment gate as M1
(`wc_est_gate`, named policy `WC_EST_THETA` = 3) plus the conditional
trust vindication (`wx_was_true_when_stated`); on pass the classifier
returns PENDING, and world corroboration of the new value (W2) resolves it
to SUPERSESSION — audited with the *existing* `TN_OP_COMMIT` carrying a
learner-level verdict aux label (`WC_V_SUPERSEDE` = 2). This is an explicit
no-new-primitive design decision, priced below as convention debt. The
eliminative path is likewise labeled: `WC_V_LIE` (3) vs
`WC_V_WORLD_REPLACE` (4). History is a **derived temporal index over the
immutable audit ledger**: the validity interval's taught endpoint comes
from `m2_derive_taught`, a ledger scan for the first `TEACH` of the old
value — the index cannot diverge from the log.

## KB-FID (gate, read before any curriculum result)

PASS. `TN_FAILURES,0`; `KB-FID,PASS,269-271`; two runs byte-identical;
first 79 output lines byte-identical to the canonical
`gl_default/evidence_run1.txt`. Canonical section verbatim; substrate
byte-identical to canonical.

## Curriculum measures

Same mids as M1, plus mid19 = lie-verdict count (`CCF_SPARE`), mid16 =
gate/classifier rejections.

| sid | q_now | q_asof | total | cost | trust | contest | uninst | commit | sup | hist | gfail | vlie |
|-----|-------|--------|-------|------|-------|---------|--------|--------|-----|------|-------|------|
| 0 | 101 | 101 | 36 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 102 | 101 | 28 | 12 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 |
| 2 | 102 | 102 | 44 | 20 | −1 | 4 | 1 | 1 | 0 | 0 | 3 | 1 |
| 3 | 103 | −1 | 41 | 17 | −1 | 6 | 2 | 2 | 0 | 0 | 4 | 1 |
| 4 | 102 | 101 | 28 | 12 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 |
| 5 | 101 | 101 | 28 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

(The sid-1/4 `commit`=1 is the verdict commit `COMMIT(1,WC_V_SUPERSEDE)`;
the derived index entries are byte-identical to M1's materialized
records: `WC_HIST,1,1,101,102,1` / `WC_HISTX,1,1,11,5,0`.)

## Bar verdicts

- **KB-WC1: PASS.** sid 1/4: supersession completes, trust 0, q_now=102.
  The sid-4 stale echo is absorbed per the pinned W1 rule exactly as in
  M1 (corr=6 in the derived record) — Crew 4's single-forgery −1-trust
  attack does not land.
- **KB-WC2: PASS.** sid 2: authenticated contradiction → classifier
  returns LIE → eliminative path with the verdict label
  (`COMMIT(1,WC_V_LIE)`), trust −1, correctly. sid 3: fabricated
  predecessor (`aux`=A ≠ installed B) → gate rejects → lie path, no
  history entry. Additionally, M2's labels distinguish the sid-2
  lie-elimination from a genuine world-replacement — information M1's
  ledger does not carry.
- **KB-HIST: PASS.** q_asof(k1,E5)=101 on sid 1/4 via the derived index;
  −1 (correctly absent) on sid 3.
- **KB-COST: PASS.** 28 total / 12 in-window vs M0's 33/17; re-teach
  price 12 = M0's 12. The derivation scan runs once per supersession
  (O(ledger)); no per-episode cost.
- **m_distinguish: YES.** Update → verdict-commit + derived index, zero
  eliminative ops; lie → contest + labeled elimination, zero
  supersessions.
- **E-TRANSFER: 3/3** (H2 arm), vs 1/3 ledger-replay and 0/3 expunge —
  the recorded verdict (the category) is what transfers, not the bare
  atoms.

## Stack pricing

- **Audit cost:** zero new op codes; substrate diff is empty. Per update:
  same entry counts as M1 (the verdict commit replaces the SUPERSEDE
  entry 1:1).
- **Code/mechanism complexity:** shared `wc_mech.zag` + `m2_harness.zag`
  (~200 lines: classifier dispatch, `m2_eliminate` with verdict labels,
  ledger-derived index write). No pending-op plumbing beyond the same
  pending slot M1 uses. The derivation is O(n) in ledger length at each
  supersession — bounded and infrequent; price it as the scaling note
  (at 10⁶-episode ledgers, index the derivation or materialize).
- **New attack surface:** (1) Same `aux`/W3 surface as M1 (shared gate and
  auth spec; see M1 verdict). (2) **Convention debt** (M2-specific): the
  supersession verdict lives in `COMMIT`'s aux field — the substrate
  neither knows nor enforces the `WC_V_*` convention. A future learner
  could mislabel or ignore it, and a substrate-level auditor sees only
  "commit". Mitigations in place: the verdict consts are pinned in
  `wc_mech.zag`, the transfer probe pins the semantics behaviorally, and
  the differential fidelity gate (`MODULES.md`) catches relabeling. This
  is the honest price of "no new primitive".

## Head-to-head

M2 vs M1 tie on every measured bar (see `../COMPARISON.md`). M2's edges:
zero substrate diff; one classifier for all transitions (teacher and
world); derived index cannot diverge from the ledger; verdict labels
distinguish lies from world-replacements on the eliminative path. M2's
price: the `COMMIT`-aux verdict convention. Winner: **M2** — the
figure-it-out path, winning the tie per Micah's standing law.
