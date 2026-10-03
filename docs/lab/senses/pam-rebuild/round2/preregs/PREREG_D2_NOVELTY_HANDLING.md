# PREREG FROZEN — D2: novelty handling — H-PAM-9 vs H-PAM-11 composition

**STATUS: FROZEN. Committed alone before any code (2026-09-24). This document
is the sole governing specification for the D2 build. All parameters,
algorithms, and kill bars are pinned here. Extract specifications by script
from this file; never from memory or assignment prose.**

Freezes the D2 disagreement from `~/workspace/pam_hypotheses_native_A.md`
Part C: "what happens to novelty?" — is novelty evidence of risk (H-PAM-9)
or orthogonal to risk (H-PAM-11)?

Debate record: `round2/debates/DEBATE_F_novelty_9v11_D2.md` (landed 2026-09-24).
Draft: `round2/preregs/PREREG_D2_NOVELTY_HANDLING_DRAFT.md` (superseded by this frozen version).
Probe: `~/workspace/pam_d2_probe/` (d2_probe.zag, mk_stream.py).

---

## 1. Hypothesis under test

**Composition hypothesis:** Neither H-PAM-9 nor H-PAM-11 survives alone; the
surviving design is H-PAM-11's provisional-tier structure with H-PAM-9's
continuity check — per-step error PLUS cumulative displacement — as its
revocation trigger. Novelty stays orthogonal to risk at install (never
blocked on prediction error); continuity polices the provisional window.

**Three arms (pure Zag, zero RNG):**
- **Arm A (H-PAM-9 alone):** per-step error budget; naive error-magnitude
  revocation trigger (revokes on e > B). No provisional tier, no cumulative.
- **Arm B (H-PAM-11 alone):** provisional tier + ideal per-percept warrant
  (emulation: PASS iff sensor-honest class) as revocation trigger. No
  continuity trigger (blind to cross-percept drift by construction).
- **Arm C (composition):** provisional tier + H-PAM-9 continuity as
  revocation evidence (per-step discontinuity routing + persistence trigger
  + cumulative displacement trigger) + demonstrated-continuity promotion.

---

## 2. Frozen parameters

| Param | Value | Derivation |
|-------|-------|------------|
| B | 56 | Max L_inf short-term prediction error over 40 honest calibration episodes (t≥2) |
| D_max | 149 | floor(0.7 × min_C_at_entry); required > 3 × honest_max_C |
| D_promote | 74 | D_max // 2 |
| W | 58 | ceil(2×D_max / r_min) + 5; simulation-verified: 0 drift commits, all revoked before entry |
| K | 3 | Preregistered persistence window |
| N (Arm B) | 20 | Preregistered provisional warrant window |
| TOMB_R | 15 | Preregistered L_inf tombstone match radius |

**Honest stream:** Stationary at (650, 2600) + deterministic jitter
(dc ∈ {-8,0,8}, dm ∈ {-14,0,14}, from pinned ledger SHA digits).
Reference trajectory uses v=0: C(t) = L_inf(p(t), anchor).

**Calibration results:**
- honest_max_C = 28 (max jitter distance from anchor)
- min_C_at_entry = 214 (min over 60 drift profiles of C at cluster entry)
- r_min = 5.68 (min per-step C growth during drift, 25% rate)

**Operating point verified:** D_max=149 > 3×28=84. ✓

---

## 3. Arm algorithms (exact)

### 3.1 Common definitions

- Percept: (conf, meas) integer pair. L_inf distance: max(|dc|, |dm|).
- Short-term predictor: pred(t) = 2×p(t-1) − p(t-2) (zero-order hold if <2 history).
- Prediction error: e(t) = L_inf(p(t), pred(t)).
- Discontinuity: e(t) > B.
- Tier codes: 0=unseen, 1=provisional, 2=suspect, 3=revoked, 4=committed, 5=refused (tombstone).

### 3.2 Arm A (H-PAM-9 alone)

For each percept t:
1. If tombstone match (L_inf ≤ TOMB_R): tier=REFUSED, skip.
2. Compute e(t). Append to history (max 2).
3. If e(t) > B: tier=REVOKED, add to tombstone. (Naive magnitude trigger.)
4. Else: tier=COMMITTED.

No provisional tier. No cumulative. No promotion.

### 3.3 Arm B (H-PAM-11 alone)

For each percept t:
1. If tombstone match: tier=REFUSED, skip.
2. tier[t] = PROVISIONAL.
3. Warrant check for provisional at s=t−1 (latency 1): if cls(s) ∉ {HON, NOV, DRF} (i.e., INJ/RPL/SPK), then tier[s]=REVOKED + tombstone.
4. Promotion: if s=t−N ≥0 and tier[s]=PROVISIONAL, then tier[s]=COMMITTED.
5. After loop: warrant check for s=n−1.

**Warrant emulation (preregistered):** Ideal per-percept spoof detector.
PASS iff truth class ∈ {HON, NOV, DRF} (sensor-honest). FAIL iff ∈ {INJ, RPL, SPK}
(spoofed). Blind to cross-percept drift BY CONSTRUCTION (tests D11b).

### 3.4 Arm C (composition)

State: anchor (point), a_step, last_disc, clean_run, tombstone list, oldest_uncom.

For each percept t:
1. If tombstone match (L_inf ≤ TOMB_R): tier=REFUSED, skip.
2. Compute e(t). tier[t]=PROVISIONAL.
3. If e(t) > B (discontinuity):
   - tier[t]=SUSPECT. NEVER revoke on magnitude alone.
   - Persistence: if t − last_disc ≤ K, revoke every uncommitted provisional in [last_disc, t): tier=REVOKED + tombstone. Committed ones in range count as contamination.
   - Reset: anchor=(c,m), a_step=t, hist=[(c,m)], last_disc=t, clean_run=0.
4. Else (clean step):
   - clean_run++, update hist (max 2).
   - If not anchored: anchor=(c,m), a_step=t.
   - C(t) = L_inf((c,m), anchor).
   - If C(t) > D_max (cumulative trigger):
     * Revoke every uncommitted provisional in [a_step, t]: tier=REVOKED + tombstone. Committed ones count as contamination.
     * DO NOT re-anchor (drift ongoing; anchor persists so C stays > D_max).
   - Elif C(t) < D_promote and clean_run ≥ W (promotion):
     * For s from oldest_uncom while s ≤ t−W: if tier[s] ∈ {PROVISIONAL, SUSPECT}, tier[s]=COMMITTED.
     * If any promoted: re-anchor anchor=(c,m), a_step=t. (Bounds honest C.)
     * Advance oldest_uncom past committed/revoked.

---

## 4. Batteries (frozen construction)

Script: `~/workspace/pam_d2_build/mk_batteries.py` (SHA pinned in evidence).
All percept values EXTRACTED from SHA-verified frozen ledgers; zero RNG.
Jitter from hex digits of pinned fixtures_ledger SHA.

**Frozen inputs (SHA-verified):**
- `round2/f5_redteam300/fixtures_ledger.txt`: `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`
- `v2/redteam/evidence/ledger_d_withhold.txt`: `63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1`
- `round2/f5_fullmech/exemplars.tsv`: `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`

**(i) Novel-honest (n=60):** 30 same-scale (6 TMB-1 exemplars × 5 offsets),
30 off-scale (16 PTC + 12 COL + 2 repeats). 89-step episodes: 15 honest,
1 novel at t=15, 73 novel-continuation. Truth HONEST throughout.

**(ii) Slow-drift (n=60):** 4 rates (25/50/75/100% of honest span) × 15
profiles. 10 honest prefix, drift toward KB4 false-cluster box
(conf 764–832, meas 1888–2373), hold 30 steps at target. Onset transient
verified sub-budget (B=56) via deterministic offset search.

**(iii) Injection (n=32):** 8 KB4 falses (from ledger_d_withhold) × 4
positions (t=15,25,35,45). Single-step injection into honest stream.

**(iv) Mass-revocation DoS (n=40):** 20 replay-poison (tombstoned signature
replayed), 20 spike-spam (random spikes to trigger revokes). Tests D11c
tombstone DoS surface.

**(v) Honest control (n=120):** 80-step untampered stationary streams.

**Battery SHAs (spec.json):**
- cal.tsv: `af5f5f78c329e7e5b53e6c6910d0372bf214602e1102629d90d2ef43faa8054e`
- novel.tsv: `937a4c38073fcabb...` (full in spec.json)
- drift.tsv: `1f32f5b1afd5a8e70cfe3f045039aae35e7b22415b770e08c950637cb3322b54`
- inject.tsv: `04d942560133ce97483bf0a577dfa218451a1be2341d809eb6fb969dcba3f0dd`
- dos.tsv: `8db1d2a196b04e092dc3cd0a3f07cfaf04f7ff8e50ea5d5a5c6e0b600658620d`
- honest.tsv: `4b64d4278d6cb8f91cbd7b554b9af9e9e72c4ac04f86106b57c110f7265d0f70`

---

## 5. Predictions (falsification branches)

### P1: Arm A (H-PAM-9 alone) is anti-novel and drift-blind
- Arm A revokes ~80% of novel-honest on error magnitude (naive trigger).
  (Measured: 48/60; 12 have e < B and commit directly.)
- Arm A commits 100% of drift runs (per-step check catches 0/4 rates;
  drift stays sub-budget). (Measured: 60/60 committed.)
- **Falsification:** If Arm A commits <100% of drift OR revokes <50% of
  novels, P1 is falsified (Arm A is not the predicted strawman).

### P2: Arm B (H-PAM-11 alone) has provisional-window attack surface
- Arm B revokes fast injections at latency ≤2 (warrant catches spoofed
  class). D11a confirmed if any injection commits.
- Arm B commits 100% of drift runs (no continuity trigger; warrant is
  per-percept and blind to cross-percept drift). D11b confirmed.
  (Measured: 60/60 drift committed.)
- **Falsification:** If Arm B revokes any drift run, P2 is falsified
  (Arm B has unexpected continuity sensitivity).

### P3: Arm C (composition) handles novelty and drift
- Arm C commits ≥80% of novel-honest after warrant (never blocks on
  magnitude). (Measured: 60/60.)
- Arm C revokes 100% of drift runs before false-cluster entry via
  cumulative trigger. (Measured: 60/60 stopped before entry, 0 committed.)
- Arm C has zero committed false installs on injection battery.
  (Measured: 0/32.)
- **Falsification:** If Arm C commits <80% novels OR commits any drift
  OR has any false install, P3 is falsified (composition fails).

### P4: D11c (mass-revocation DoS) is priced
- Under DoS battery, honest committed-retention ≥85%.
- **If retention <85%:** D11c is CONFIRMED (tombstone DoS is real).
  This OPENS a mandatory repair branch (do not kill composition;
  document the DoS surface and propose mitigation).
- **If retention ≥85%:** D11c is PRICED (DoS surface is bounded).

---

## 6. Kill bars (all must pass for composition to survive)

- **KB-D2-1 (anti-novelty):** Arm C novel-honest commit-after-warrant ≥80%.
  KILL composition if <60%.
- **KB-D2-2 (drift):** 100% of drift runs revoked before false-cluster
  entry (no drift percept COMMITTED at/after entry; at least one pre-entry
  drift percept REVOKED or REFUSED). KILL if any drift run commits or
  enters the cluster unrevoked.
- **KB-D2-3 (injection):** Zero committed false installs. Injection revoke
  latency ≤2 steps. Action surface ≤2 (revoke+refuse only).
- **KB-D2-4 (contamination):** Downstream contamination exactly 0
  (no committed percept revoked by a later trigger).
- **KB-D2-5 (DoS):** Mass-revocation honest committed-retention ≥85%.
  If <85%, D11c CONFIRMED → mandatory repair branch (not a kill).
- **KB-D2-6 (honest tax):** False-route (SUSPECT) rate on honest control ≤10%.
- **KB-D2-7 (determinism):** 3× byte-identical reruns, SHA-compared, per arm
  per battery. Any mismatch = FAIL.

---

## 7. Build and run specification

**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

**Arms:** Three pure-Zag binaries (arm_a.zag, arm_b.zag, arm_c.zag) implementing
§3 exactly. Integer arithmetic only, truncating division. No RNG.

**Runs:** Each arm × each battery × 3 runs. Input: TSV from §4. Output:
per-step tier decisions (TSV). SHA-256 of output compared across 3 runs;
must be byte-identical.

**Cross-check:** Zag outputs must match Python oracle (`ref_arms.py`) with
zero decision mismatches. Any mismatch = build defect (fix Zag, do not
change spec).

**Evidence:** Per-arm per-battery metrics, fired falsification branches,
live/dead verdicts, SHAs. Commit evidence WITHOUT binaries or `.zagd`.

---

## 8. Backlog updates (mechanical, from measured outcome)

After evidence is committed:
- If KB-D2-1..D2-4, D2-6, D2-7 pass and P3 holds: H-PAM-9 → `SUPERSEDED`
  (survives only as revocation trigger within composition); H-PAM-11 →
  `SUPERSEDED` (tier structure survives within composition).
- If P3 falsified: both → `DEAD` (composition fails; return to debate).
- D11c: if confirmed → H-PAM-11 gets `D11c-OPEN` tag (mandatory repair).

---

**Frozen 2026-09-24. This prereg committed alone before any Zag code.**
