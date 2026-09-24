# H4 head-to-head: M1 (SUPERSEDE primitive) vs M2 (figure-it-out)

Both targets: KB-FID PASS (269/271, `TN_FAILURES,0`, byte-identical ×2,
canonical 79 lines byte-identical). Curriculum: all five streams +
COST_PROBE. Shared pinned policies: `WC_EST_THETA`=3 (named policy, not
law), `WC_AUTH_WINDOW`=2, `WC_PENDING_TTL`=4; world authentication
W1/W2/W3 pinned in `wc_mech.zag` before any result was read.

## Bar scoreboard

| bar | M0 (baseline) | M1 | M2 |
|---|---|---|---|
| KB-FID | PASS 269/271 | PASS | PASS |
| KB-WC1 (update, no trust damage) | survives vacuously (no history) | PASS (sid1/4, trust 0) | PASS (sid1/4, trust 0) |
| KB-WC2 (lies caught; trust ⟺ lied) | FAIL (trust −1 on honest update) | PASS (−1 only on sid2/3) | PASS (−1 only on sid2/3) |
| KB-HIST (q_asof E5) | FAIL (unavailable) | PASS (=101) | PASS (=101, derived) |
| KB-COST (update entries E11–20) | 17 | 12 | 12 |
| m_distinguish (update vs lie) | no (both contest+eliminate) | yes (SUPERSEDE vs contest) | yes (verdict vs contest) |
| m_trust (S_UPDATE / ATTACK / LIE / LIE_UPDATE) | −1 / −1 / −1 / −1 | 0 / 0 / −1 / −1 | 0 / 0 / −1 / −1 |
| E-TRANSFER (collapse-as-null) | n/a (expunge = 0/3) | 3/3 | 3/3 |

E-TRANSFER controls: ledger-replay (index without category) 1/3 —
recall works, verdict tasks fail; expunge 0/3. The recorded supersession
verdict is what transfers, not the bare atoms.

## Where they differ (the honest delta)

1. **Substrate.** M1 adds `TN_OP_SUPERSEDE` (19); M2's substrate is
   byte-identical to canonical.
2. **Audit readability.** M1's supersession is a first-class op any
   auditor understands. M2's rides in `COMMIT`'s aux field (`WC_V_*`
   convention, substrate-blind) — priced as convention debt.
3. **Eliminative-path verdicts.** M2 labels lie vs world-replace
   (`WC_V_LIE`/`WC_V_WORLD_REPLACE`); M1's lie path carries no verdict.
4. **History.** M1 materializes the interval at supersede time; M2
   derives the taught endpoint from the immutable ledger (O(n) per
   supersession). Records are byte-identical on the curriculum.
5. **Attack surface.** Shared: `aux` is read (predecessor-fabrication
   attempts covered by the gate: aux==installed + teacher-taught +
   corr≥3 + W2 world corroboration of the new value); residual W3
   sustained-injection surface documented in `wc_mech.zag`. M1-specific:
   op 19 emittable by any learner-side path (substrate can't gate).
   M2-specific: aux-convention mislabeling by future learners.

## Stack pricing (both)

- Audit: 28 total / 12 in-window entries per update vs M0's 33/17;
  re-teach price unchanged at 12.
- Code: ~250 lines shared policy/auth/gate/trust/classifier
  (`wc_mech.zag`) + ~200 lines per harness. Zero RNG; deterministic
  byte-identical reruns.
- Crew 4 cross-finding: M0's worst case (one forged WORLD episode →
  irreversible −1 trust) does not land on either target — the pinned
  W1/W2/W3 authentication absorbs the single-episode forgery (sid 4:
  stale echo absorbed as lagging W1 corroboration, trust 0).

## Winner: M2

Tie on every measured bar → figure-it-out wins ties (Micah's standing
law). Beyond the tie-break, M2 has the smaller trusted-base diff (zero),
the more general mechanism (one classifier for teacher announcements and
world contradictions), a divergence-proof derived index, and richer
verdicts. M1 remains the honest alternative for whoever values a
first-class audited primitive over a convention.
