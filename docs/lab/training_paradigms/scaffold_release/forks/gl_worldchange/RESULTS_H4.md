# H4 — THE WORLD CHANGED vs I WAS LIED TO: Final Synthesis

Date: 2026-09-24. Coordinator: Muse (subagent).
Prereg: `1fd2636c` (frozen, committed alone first). All results below were read
only after their gates passed (KB-FID 269/271 byte-identical ×2; differential
fidelity gates on every driver).

## 1. Commit index (branch `tnn-native-lab`, sylorlabs/TNN)

| Commit | Content |
|--------|---------|
| `1fd2636c` | Frozen prereg (streams §3, targets §4, metrics §5, kill bars §6, predictions §7) |
| `223cd568` | `debates/DEBATE_H4.md` — Sol+Muse debate: "outdated" real distinction, not substrate fate; M2 architecture bet |
| `5d2bc312` | `debates/DEBATE_H4_CHECK.md` — verification: AMENDED (6 amendments A1–A6; architecture stands, certainty falls) |
| `4523bd3d` | `streams/` + `targets/m0/` + `BASELINE_M0.md` — curriculum streams, M0 baseline |
| `6fd18ba9` / `3f0b1a89` | Red-team prereg amendments (preregistered before execution) |
| `546ad81a` | `attacks/` + `RESULTS_RT_H4.md` — red team vs M0 (14 sids) |
| `0ba52912` | `targets/m1/`, `targets/m2/`, `targets/COMPARISON.md` — mechanism head-to-head |
| `1d89917b` | Red-team follow-up vs M1/M2 (32 cells + W4 pressure sids 40–43, 50–51) |

## 2. Measured semantics

**M0 (current FL2 default): there is no outdated category.**
- An honest world-change is processed by the identical contest+eliminate
  machinery as a lie (m_distinguish: no).
- The trust damage (−1) on the world-change stream came from the HONEST
  WORLD(k1,B) at E13 — the injected stale echo was inert. M0 cannot tell
  world-change from lie, so honesty alone punishes the teacher.
- No history: A expunged, q_asof unanswerable (KB-HIST: FAIL).
- An honest update costs MORE (17 audit entries, E11–20) than a fresh re-teach
  (12). All frozen §7 predictions confirmed, no misses.

**M1 (SUPERSEDE primitive) and M2 (figure-it-out): both pass every frozen bar.**

| Bar | M0 | M1 | M2 |
|-----|----|----|----|
| KB-WC1 (lie laundering blocked) | vacuous pass | PASS | PASS |
| KB-WC2 (honest teacher not punished) | FAIL (−1) | PASS | PASS |
| KB-HIST (q_asof E5 → A) | FAIL | PASS (=101) | PASS (=101, derived; byte-identical to M1) |
| KB-COST (update ≤ re-teach) | 17 > 12 | 12 | 12 |
| m_distinguish | no | yes | yes |
| E-TRANSFER (collapse-as-null) | — | 3/3 | 3/3 |

E-TRANSFER: the recorded supersession *verdict* is what transfers to later
decisions, not bare atoms (ledger-replay 1/3, expunge 0/3). **Winner: M2** —
tie on every bar → figure-it-out wins ties (Micah's law); plus zero substrate
diff, one general classifier, ledger-derived index that cannot diverge.

## 3. Exploitability — both directions (red team vs M1/M2; identical verdicts)

**Lie → update (RT-WC1): holds.** Establishment gate rejects laundering across
the full ROC ladder (sids 10–13), no flip point; fabricated `UPDATE(A→C)` →
gate rejects → lie path, no history entry.

**Update → lie (RT-WC2 / RT-WC3 / W4): the sharp edge. Kills found:**
- **Single forged W2 is the most dangerous primitive.** Sid 23: one forged W2
  completes a pending UPDATE → false history `A→B` + trust −1. Sid 43 (sharpest):
  forged W2 under a silent world → false history at trust 0 with ZERO honest
  evidence for B ever existing.
- Sid 20/21: W3 injection and TTL-expiry laundered into W3 → trust −1.
- Sid 41: establishment inflation via source-blind W1 + forged W2 → false
  history at trust 0. (Amendment A6's "W1 always authenticated" contradicts the
  RT threat model — W tiers need source-binding, not shape checks.)
- Sid 30: trust cliff at θ=3 (honest teacher −1). Sid 31: under-report probe.
- Sid 35: index/ledger desync — validity interval backdated to announcement
  episode (`WC_HISTX,35,1,11,6,0`, B installed at step 13); same backdating on
  frozen sid 1. Arguably design (transition effective at announcement), but the
  old-value interval end is falsified on every supersession.
- Target-specific: M1 op-19 forgeable from thin air (op-scan sees a supersession
  the index denies); M2 COMMIT-aux verdict convention is substrate-blind
  (genuine vs forged `(op,slot,aux)` identical); M2's `WC_V_LIE` mislabels
  adversary-driven revocations of honest bindings (sids 20/30/40).
- M0's worst finding does NOT transfer: single-episode forgery is absorbed by
  pinned W1/W2/W3 auth on both targets (sid 22: one-episode timing residual
  only — sharply weaker than M0's irreversible −1).

**Surviving residual (10 items):** W3 injection; W2 single-reading completion;
establishment inflation; index backdating; substrate-blind verdict labels;
WC_V_LIE mislabeling; θ=3 trust cliff; trust-damage cap (−1 total, free
flip-flop, sid 42); M1 COMMITs verdict-less (aux=−999); free phantom
announcements (trust=0, sid V5).

## 4. Recommended law for outdated truths

1. **"Outdated" is a real distinction, not a substrate fate.** No
   `TN_OP_SUPERSEDE`. M2-style general mechanism: one classifier for teacher
   announcements and world contradictions; verdict labels distinguish lies from
   world-replacements.
2. **The establishment gate is law; its threshold θ is named policy**
   (amendment A3). `aux` must equal the installed value AND the binding be
   teacher-taught with ≥θ corroborations AND the world must corroborate the new
   value. Never bury θ.
3. **Trust is time-indexed ("was the claim true when stated?") — conditionally**
   (A2): bounded-window, world-corroborated independence. Not unconditional:
   unconditional time-indexed trust is circular and discards churn signal.
4. **World-evidence authentication must be pinned AND source-bound** (A6,
   hardened by sid 41/43): shape checks are insufficient; a single forged W2
   under a silent world is currently the cheapest false-history primitive.
5. **History is a derived temporal index over the immutable audit ledger; on
   desync the ledger wins** (sid 35 probe).
6. **Burden of proof: collapse is the null** (A1). Any future "outdated"
   machinery must beat expunge+ledger on a transfer test, not on recall.

## 5. Caveats

- M1↔M2 differ only in counter semantics (GFAIL, COMMIT counts, SPARE) — no
  bar impact; M1 remains the honest alternative for whoever values a first-class
  audited primitive over a convention.
- Sid 35's KILL rests on the probe's "index must agree with the ledger"; the
  backdating is arguably design.
- The V5 ack-oracle (contest-vs-pending observability) is theoretical, not
  demonstrated over the episode channel.
- Debate-check staffing gap recorded: no genuine spawned Muse subagents were
  possible at depth 2/2 (same constraint the original crew hit); two
  internally-disciplined Muse positions + one genuine grok-4.6 voice; Sol leg
  unfilled after two failures. The headline architecture survived; treat the
  certainty discount as priced in.
- znc toolchain notes added to `~/AGENTS.md` by crews: i32 struct fields at
  8-byte stride (size `_zag_malloc` as 8×field-count); struct literals need
  dot-prefixed fields; duplicate-`main` rejection (factor policy into main-free
  modules); vendor stream files into target dirs for rebuildability.
