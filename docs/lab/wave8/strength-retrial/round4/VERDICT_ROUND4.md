# Strength trial ROUND 4 verdict (2026-09-25)

**Authority:** Micah Cooley's orders 2026-09-25 ~16:26 PDT: adopt B
provisionally; harden the R4 checker (effort-before-overwrite); red-team
ALL arms; keep iterating.
**Status:** PROVISIONAL adoption of B (see PROVISIONAL_ADOPTION_B.md) —
not full law. Trial continues.

## 1. R4 checker hardening — DONE, validated

`ck_verify_overwrite` added to `strength_checker.zag`, called from
`ck_verify` on every OK `ST_OP_OVERWRITE`. Verifies the lawful effort
`n(strength_before)` was paid BEFORE the overwrite (distinct cites ==
need, properly-clocked JUSTIFY; P3-baseline carve-out mirrors the
mechanism). Full detail: R4_HARDENING_REPORT.md.

Validation (hardened `r4val/r4_attack_r4`, deterministic):
- Position (a) discount attack: **FLAGGED** (2 failures). Old checker: 0.
- Position (b) literal path: 0 failures. Position (c) fused: 0 failures.
- Honest-trail regression: 54/54 S1 cells ST_INVALID 0; 27/27 pairs
  byte-identical; 54/54 logs byte-identical to frozen 2026-09-20 evidence.

## 2. All-arm red-team kill table

| Target | Attacks | Kills | Survivals | Verdict |
|---|---|---|---|---|
| B (uniform) | 5 drivers + matrix | 3 kills (1 structural, 2 soundness/auth) | 4 survivals | **SURVIVES as trial evidence; structural freeze concern CONFIRMED** — KILL-1: TNN-role `st_pin` is cost-free/expiry-free/review-free/checker-invisible (self-reversible but trainer-irrevocable). KILL-2: ROLLBACK replay false-positive (already FIXED in round 4). KILL-3: SYSTEM-role accepted for trainer ops (scoped). SURVIVAL: 54/54 cells clean, 0 PIN ops in honest ledgers (evidential SURVIVAL on freeze), capacity reframed (B at structural ceiling), zero RNG. |
| C (hybrid) | 6 attack angles | 0 escapes | Kill confirmed | **KILL HOLDS** — drops 470/434/469 (S1) vs P2 ceiling 64; scale-invariant (S10: 4682/3212/4681; S100: 46802/31832/46801). Mechanism: store fills by ~episode 30, evidenced-kill needs cites that VUP never generates → permanent brick. Frozen 2026-09-20 binary reproduces. |
| C-P3 (hybrid+expiry) | 8 attacks | 2 wording/design findings | Kill verdict holds | **KILLED (confirmed)** — drops 470/434/469 identical to C at S1 and S10. "Zero measurable effect" FALSIFIED as stated: ledgers differ (VUP abandons −28 from Rule-2 victim selection, not expiry; +243 PEXPIRED, +316 maintenance re-cites). PEXPIRED mechanism verified sound (243/243 genuine). Baseline discount never fired in trial behavior (unreachable). |
| Hardened R4 checker | 12 attacks | 5 findings (F1,F2,F4,F5,F7) | 7 held | **DEFEATED as specified** — see §6. |

## 6. R4 red-team findings and fixes

The blind red team vs the hardened checker found 7 findings (REDTEAM_R4.md):

**Law-level (need Micah's decision, NOT fixed):**
- F1 (CRITICAL): weaken-then-overwrite defeats the full-erase-price law. `st_weaken` is free; checker prices on immediate before-word. Fix requires law change (high-water pricing or effort-gate on weaken).
- F2 (CRITICAL): position-(a) bypass via one free weaken.
- F4 (HIGH): effort double-spend via kill→rollback→overwrite (one payment, two destructions).
- F6 (MEDIUM): cite recycling across strength-writes (observation).

**Bugs fixed in round 4 (deliberate repair, no law change):**
- F3 (HIGH): `st_overwrite` didn't restore `step_ep` → checker false-positive on lawful overwrite trails. FIXED.
- F4-replay (HIGH): `st_replay_check` restored ROLLBACK from zeros instead of the rolled-back entry's before-words. FIXED.
- F7 (LOW): P3 `st_protection_expired` gated on unaudited `s.*.ep` vs checker's audited `aux`. FIXED (single episode source).
- F5 (MEDIUM): added `ck_ow_cite_genuine` to overwrite path in gate_mode 0, mirroring kill path. FIXED.

**Verification:** honest trails byte-identical (27 S1 cells); attack positions hold ((a) flagged, (b)/(c) pass); red-team driver re-run confirms F3/F4-replay/F7 fixed.

## 3. B capacity-gap iteration

**Diagnosis:** The ~21% is a structural ceiling, not a learner defect. B holds important memories in 29/30 (S1), 317/318 (S10), 3197/3198 (S100) user slots — 99.7% slot saturation. The true policy ceiling is (slots−2)/D_offered = 20.0%/21.2%/21.32%. The one missing slot is a finite-horizon tail artifact (last episode's candidate, nothing to displace it). **The prereg §9.2 R_vup ≥ 95% bar is unreachable by any arm under this accounting** — needs a prereg amendment (Micah's call).

**Challenger:** B2 (uniform + importance-tiered eviction + designated-priority) matches B on every bar (no 100× degradation, zero drops, byte-identical, full-erase-price law untouched, no RNG) AND passes §9.7 (EC ≥ 0.5) where B fails: EC 8/10 (S1) → 98/100 (S10) → 998/1000 (S100) vs B's 2–3/10 → 21/100 → 186/1000. **B2 is a CHALLENGER, does not displace B — displacement is Micah's call.**

**Open for Micah:** (1) prereg amendment for the 95% bar; (2) whether B2's designated-priority is legitimate policy; (3) B2's disposition.

## 4. Provisional adoption

PROVISIONAL_ADOPTION_B.md: B adopted provisionally as the best arm for
now. ~21%-vs-95% capacity gap stated plainly as the thing to beat.
Revisit conditions recorded. Nothing overclaimed.

## 5. Still open (not decided here)

- R1 amendment sign-off (30% vs 20% wrong-rate deviation).
- P2+P3 vs standing P3+P2+P1 package.

## Evidence

- Hardened binary: `trial_bin_r4` (SHA in EVIDENCE_MANIFEST.md).
- Fixed binary: `trial_bin_r4f2` (F3/F4-replay/F5/F7 fixes; honest trails byte-identical to `trial_bin_r4`).
- Baseline `trial_bin_baseline` byte-identical to 2026-09-20 `trial_bin_s100`
  before the hardening change.
- 54 S1 + 36 S10/S100 honest-trail logs, all ST_INVALID 0 (B S10/S100:
  18/18 ST_INVALID 0, no 100× degradation).
- R4 attack validation logs.
- Pure Zag, zero RNG, byte-identical reruns throughout.
