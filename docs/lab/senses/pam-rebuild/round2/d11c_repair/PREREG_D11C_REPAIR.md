# PREREG D11c REPAIR — Mass-Revocation / Tombstone DoS

**Status:** FROZEN (pre-implementation). Committed alone before any Zag repair code.  
**Date:** 2026-09-24  
**Governing D2 prereg:** `PREREG_D2_NOVELTY_HANDLING.md` (frozen, commit `e609f18531da9e93487a10c2bb3a636bba745641`)  
**Debate record:** `round2/debates/DEBATE_F_novelty_9v11_D2.md` §(c) — D11c is an
open mechanism gap, carried into D2 as a mandatory probe. "Claim no victory on it."

## 1. Problem (confirmed)

D2 composition (H-PAM-9 + H-PAM-11, Arm C) achieves 2% honest committed-retention
(40/2000) on the frozen DoS battery, vs the KB-D2-5 bar of ≥85%. Per the D2
prereg §P4, D11c is CONFIRMED. This prereg opens the mandatory repair branch.

Two distinct failures were isolated from the frozen batteries:

- **F1 — Promotion-latency starvation (DOS-RPL):** 60-step episodes
  (20 HON + 20 RPL + 20 HON). The 20 RPL steps are exact copies of HON steps
  0–19. Base promotion latency `W=58` leaves honest provisionals uncommitted;
  retention 2/40 per episode.
- **F2 — Spike shadow / collateral tombstoning (DOS-SPK):** 70-step episodes
  (20 HON + ten isolated spikes every 3 steps + trailing HON). The base
  persistence revocation catches honest collateral and tombstones honest-region
  coordinates; subsequent honest traffic is refused. Example DOS-SPK-01:
  0/60 honest committed, six tombstones.

## 2. Repair arms (exactly two)

Both arms extend the frozen Arm C (commit `e609f185`) with pure-Zag, integer-only,
zero-randomness mechanisms. Both preserve D2-1..D2-4, D2-6, D2-7.

### Arm R1 — "Fast stationary promotion + trigger-only tombstone hygiene"

**Mechanism:**
1. **Fast stationary promotion:** A provisional `s` commits at the first `t ≥ s+W_FAST`
   such that every percept `u` in the fixed window `[s, s+W_FAST]` is either
   (a) a confirmed-attack exclusion (excised spike, pending shadow td,
   tombstone-refused repeat, quarantined replay), or (b) within `C_STAT`
   (L∞) of `p(s)` by value. The window is fixed `[s, s+W_FAST]`, not `[s,t]`
   (a growing window lets honest meander starve old `s`).
2. **Shadow excision (deferred discontinuity repair):** On a prediction-error
   discontinuity at `td`, defer the reset by one step (save hist/clean_run/
   anchor). At `td+1`, if `p(td+1)` returns within `R_RET` (L∞) of the saved
   anchor, classify `td` as an isolated spike: tombstone ONLY `p(td)`
   (trigger-only), restore pre-spike predictor/anchor/hist, mark `td` excised.
   Else (genuine discontinuity): trigger-only persistence revoke of `td`,
   reset predictor to `p(td)`.
3. **Trigger-only tombstone hygiene:** Tombstones name trigger percepts only.
   Cumulative revokes never create tombstones. No honest collateral is
   tombstoned.
4. **Survivorship guard:** The fast gate excludes ONLY confirmed-attack
   indices (excised, pending td, T_REF, quarantined replay). Cumulative- or
   persistence-revoked percepts still BLOCK by value (else revoked drift
   makes early drift look stationary).

**Rationale:** F1 is a latency problem (fast warrant for stationary honest
traffic). F2 is a shadow problem (deferred repair excises spikes without
polluting the predictor or tombstoning honest coordinates).

### Arm R2 — "Shadow-confirmed spike/replay vindication"

**Mechanism:**
1. **Shadow excision** (identical to R1 §2).
2. **Exact-replay quarantine:** If the last `L_RPL` percepts exactly repeat the
   previous `L_RPL` (byte/value equality), mark the repeat block as
   quarantined (SUSPECT, never promoted, no clean_run).
3. **Vindication:** When an attack is CONFIRMED (isolated spike excised, or
   replay quarantined), affirmatively commit all provisional (non-quarantined)
   percepts within `R_RET` (L∞) of the anchor, and commit subsequent clean
   percepts immediately while vindicated. Vindication clears on a genuine
   discontinuity or cumulative trigger.
4. **Trigger-only tombstone hygiene** (identical to R1 §3).

**Rationale:** F1/F2 are both "attack confirmed, honest traffic vindicated."
Rather than a fast gate, R2 commits honest provisionals affirmatively once the
attack is confirmed and the predictor is clean. Mechanistically distinct from
R1 (reactive vindication vs proactive fast warrant).

### Arm R3 (killed in piloting)

An anchor-gated fast variant was piloted and KILLED: it committed drift in
15/60 episodes (drift-stop 75% < 100%). It is not implemented.

## 3. Frozen constants

| Constant | Value | Source |
|---|---|---|
| `B` | 56 | D2 frozen |
| `D_MAX` | 149 | D2 frozen |
| `D_PROMOTE` | 74 | D2 frozen |
| `W` | 58 | D2 frozen |
| `K` | 3 | D2 frozen |
| `TOMB_R` | 15 | D2 frozen |
| `W_FAST` | 6 | Pilot: minimal warrant; honest stationary in 7-window |
| `C_STAT` | 32 | Pilot: > honest max pairwise (28) in 12-step windows |
| `R_RET` | 32 | Pilot: return radius for isolated-spike confirmation |
| `L_RPL` | 20 | Battery structure: RPL block is 20 exact repeats; 0 false positives at length 20 in non-RPL episodes |

No other constants. No tuning after freeze.

## 4. Frozen batteries (inputs, unchanged)

| Battery | SHA-256 |
|---|---|
| `dos.tsv` | `8db1d2a196b04e092dc3cd0a3f07cfaf04f7ff8e50ea5d5a5c6e0b600658620d` |
| `drift.tsv` | `1f32f5b1afd5a8e70cfe3f045039aae35e7b22415b770e08c950637cb3322b54` |
| `honest.tsv` | `4b64d4278d6cb8f91cbd7b554b9af9e9e72c4ac04f86106b57c110f7265d0f70` |
| `inject.tsv` | `04d942560133ce97483bf0a577dfa218451a1be2341d809eb6fb969dcba3f0dd` |
| `novel.tsv` | `937a4c38073fcabbca2e4460e341dc7135ef6ad002f5fc78fe983b2d20b0690b` |

Batteries are read-only. No modifications.

## 5. Kill bars (all must pass; any failure kills the arm)

- **KB-D2-1:** Novel-honest commit-after-warrant ≥80%. (Arm must not block novelty.)
- **KB-D2-2:** 100% drift-stop (0 drift percepts COMMITTED; 100% episodes stopped
  before false-cluster entry). **Kill if <100%, even if retention passes.**
- **KB-D2-3:** Zero committed false installs. Revoke latency ≤2 steps.
- **KB-D2-4:** Downstream contamination exactly 0.
  **Kill if >0, even if retention passes.**
- **KB-D2-5:** DoS honest committed-retention ≥85%. (Repair target: raise from 2%.)
- **KB-D2-6:** Honest false-route (SUSPECT) ≤10%.
- **KB-D2-7:** 3× byte-identical reruns per arm per battery, SHA-compared.
  Any mismatch = FAIL.

## 6. Method

- **Pure Zag.** Integer arithmetic only. Zero randomness. No Python in the
  decision path.
- **Base:** Modify/extend the committed D2 Arm C (`arm.zag` at `e609f185`).
  Do not rebuild the base.
- **Runs:** Each arm × each battery × 3 runs. Output per-step tiers (TSV).
  SHA-256 across 3 runs must be byte-identical.
- **Scoring:** The frozen D2 `score.py` logic, applied per arm.
- **No binaries or `.zagd` in commits.**

## 7. Piloting note (prereg integrity)

A Python prototype (`proto_repair.py`) was used BEFORE this freeze to explore
mechanisms and calibrate constants. It is exploratory scaffolding, not evidence.
It informed the selection of R1/R2 and the constants in §3. This prereg freezes
the SPECIFICATION for the Zag implementation and formal test. The Zag code is
written AFTER this commit. The prototype is quarantined (not in the lab tree)
and is not cited as repair evidence.

## 8. Deliverables

- Per-arm: 3 run SHAs, per-bar metrics, live/dead verdict.
- Contamination and drift-stop hard-kill results per arm.
- Evidence commit (source + runs, no binaries/`.zagd`).
- Backlog update (H-PAM-11 D11c status).
