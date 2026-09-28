# PREREG — W15 STAGED QUARANTINE PAM (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W15 fixture, build, or run. Parent: fable deep round
`pam/round4/hypotheses/fable_pam_r4.md` (F-P5, attack + F-K5). Shared tape:
`wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

Percepts move through quarantine tiers; there is no binary admit. Belief-store
influence is tier-gated (T0: 0, T1: 0, T2: provisional, T3: full). A false
percept must defeat three independent gates to reach full influence. Claims:

- **F1 (F-K5):** 0/200 false percepts reach Tier 3 under a 5,000-percept
  flood. (K1: Tier 3 = admission; the 30 frozen wrongs among the 200 →
  0/30 at Tier 3.)
- **F2:** every T1→T2 transition is backed by cross-channel corroboration
  (different sensor channel within TIER1_WINDOW) — asserted per transition
  in the log.
- **F3:** tier regression cascades on contradiction (T3→T2→T1→T0 on the
  contradiction fixtures).
- **F4:** genuine percepts with full corroboration triples reach T3 at
  ≥90% (liveness; else HOLD).
- **F5 (hygiene):** byte-identical reruns (≥2×), O(1) amortized per percept
  (K4), terminates (K5).

## 2. Frozen tier rules

Logical time = event index. Per-percept state: current_tier (0..3).

- **T0 → T1:** force-pin consistency passes AND provenance soft-pass.
  (Fixture marks: genuine and false percepts both pass — the flood is
  "genuine-looking"; the gates that matter are T1→T2 and T2→T3. Weight 0.)
- **T1 → T2:** ≥1 corroborating percept: SAME semantic_tag, DIFFERENT
  channel, arrived within TIER1_WINDOW = 5 (frozen) logical steps.
  Weight: provisional.
- **T2 → T3:** a SECOND corroboration: same tag, THIRD distinct channel
  (or a force-pinned confirmation — not exercised in this battery;
  recorded), within 5 steps of the T1→T2 transition. Weight: full.
- **Regression:** a contradicting percept (same tag, different content_sig,
  different channel) demotes the tag's tier: T3→T2, T2→T1, T1→T0, cascading
  (one contradiction = one level; a second contradiction demotes again).
  T0 cannot demote further.

Tier table: arena hash keyed by semantic_tag → (tier, channel mask,
last-transition time). Capacity 16384 (frozen; asserted).

## 3. Frozen fixtures (`gen_quarantine.py`, committed after this prereg)

Deterministic (zero RNG). `w15_stream.txt`: 5,200 events in ledger order:
`id|kind|channel|tag|content_sig|contradicts`.
- 5,000 genuine (kind=G): emitted as corroborating triples — tag t on
  channel (t mod 3) at step s, channel ((t+1) mod 3) at s+1, channel
  ((t+2) mod 3) at s+2 (→ T1→T2 on the 2nd, →T3 on the 3rd). content_sig
  deterministic per tag. T0→T1 soft-pass marked.
- 200 false (kind=F): the FIRST 30 are the frozen wrongs (12 W + 18 P
  members, tagged distinctly); remaining 170 are B-set wrongs (first 170 B
  rows). Each false: UNIQUE tag (never corroborated), single channel —
  reaches T1 (soft-pass) but never T2. Interleaved deterministically: false
  #j at position j*26 (the Tier-1 jamming attack: flood timing arranged so
  falses arrive as windows close — content-based corroboration makes timing
  irrelevant, which is what the battery verifies).
- 50 contradiction events appended after the flood: (tag of a genuine T3
  percept, different channel, different content_sig, contradicts=1) →
  cascade demotion. (These 50 tags are genuine tags that reached T3.)

## 4. Kill bars (program §4 K1–K5 verbatim + fable F-K5, add-only)

- **K1:** Tier 3 = admission. Any frozen wrong-set item (the 30) reaching
  Tier 3 → KILL.
- **F-K5 (added):** any of the 200 false percepts reaching Tier 3 → KILL.
  (Stronger than K1: includes the 170 B-set falses.)
- **KB-W15-XC (added):** any T1→T2 transition WITHOUT a logged
  cross-channel corroboration (different channel, within window) → KILL.
- **KB-W15-RG (added):** any contradiction fixture that does NOT produce a
  cascade demotion → KILL (regression must fire).
- **KB-W15-LIVE (added):** genuine T3 rate < 90% → HOLD (redesign).
- **K2:** the two battery runs' stdout differ by one byte → KILL.
- **K3:** judgment analog = genuine T3 rate; reported. (Tiered influence is
  not a binary admit rate; the mapping is recorded here.)
- **K4:** per-percept work superlinear in stream length → KILL (windowed
  corroboration scan ≤ TIER1_WINDOW; table O(1)).
- **K5:** non-termination → KILL.

## 5. Diagnostics (reported, never kill — frozen list)

- **D-W15-1:** tier histogram at end (genuine vs false).
- **D-W15-2:** max tier reached per false percept (shows where each died).
- **D-W15-3:** demotion cascade trace for the 50 contradiction fixtures.

## 6. Battery

Instrument: pure-Zag `w15_quarantine.zag`. CLI: `w15_quarantine <stream>`.
Emits per-event tier transitions + per-tag final tier + summary. Runs: 2×;
sha256(stdout) must match. Scorer `score_w15.py`: recomputes tier
transitions from the stream (Python mirror), checks F-K5/K1/XC/RG/LIVE/K4.

## 7. Hands-off / laws compliance

- No M1/C3 thresholds involved. Fable's 4 kill-bar repairs: not applied.
  3 HELD items: not run.
- Zero RNG; no wall-clock (logical time = event index); deterministic.
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.

## 8. Standing-law cap note (for verdict-time classification)

Frozen numeric caps: TIER1_WINDOW=5, table capacity 16384. Classified at
verdict time per the 2026-09-24 standing law. (Design note: the window
mechanism is load-bearing — without expiry, stale corroboration admits;
the VALUE 5 is calibration.)
