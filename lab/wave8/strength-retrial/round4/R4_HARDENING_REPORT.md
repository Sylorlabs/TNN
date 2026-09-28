# R4 checker hardening report — round 4 (2026-09-25)

## The blindness

The committed checker (`strength_checker.zag` as of commit dfa38c3a)
treated `ST_OP_OVERWRITE` as legal strength lineage in `ck_strength_lineage`
but never verified overwrite effort. Consequence (R4 T3, SUMMARY_R4.md):
position (a) direct write defeats the full-erase-price law 4→1 (1 citation
paid vs lawful n(90)=4) with **0 checker failures** — the law falls and the
checker sees nothing.

## The hardening

Added `ck_verify_overwrite(s, slot, ow_idx, baseline)` to
`strength_checker.zag`, called from `ck_verify`'s main ledger loop on every
OK `ST_OP_OVERWRITE` (baseline flag read from the P3-expiry tracking
*before* the post-overwrite reset clears it):

- `need = ck_n(strength_before)` — lawful price from the ledger before-word
  at the overwrite index (not from post-weakened state).
- `lss = st_last_strength_idx(s, slot, ow_idx)` — effort window.
- Distinct cites in `(lss, ow_idx)` must EQUAL `need` (`>=1` under
  P3-baseline expiry) — mirrors `st_kill_effort_check`'s law exactly
  (`cnt != need` → `ST_REFUSED_EFFORT` in the mechanism).
- A properly-clocked JUSTIFY (code in
  `[ST_J_CONFIRMED_IMPORTANT, ST_J_TRAINER_DIRECTIVE]`) must exist in
  `(lss, ow_idx)`.

This is the check R4 T4 demonstrated as purpose-built; the hardening
commits it into the checker's standing verification and extends it with
the P3-baseline carve-out the mechanism itself honors.

## Validation

Attack driver rebuilt with the hardened checker
(`r4val/r4_attack_r4`, deterministic, 2x byte-identical):

| position | attack_cites | checker_failures (old) | checker_failures (hardened) |
|---|---|---|---|
| (a) direct / discount | 1 | 0 (blind) | **2 — FLAGGED** (`ck_ow_effort`, `ck_ow_justify`) |
| (b) literal kill+add | 5 | 0 | 0 — passes (kill verified by existing kill checks) |
| (c) fused overwrite | 5 | 0 | 0 — passes (4/4 cites + justify) |

Honest-trail regression (hardened `trial_bin_r4`):
- 54/54 S1 cells (B/C/C-P3 × VUP/WBS/JI × var 0-2 × 2 runs): ST_INVALID 0.
- 27/27 run-pairs byte-identical.
- 54/54 logs byte-identical to frozen 2026-09-20 evidence.
- The honest learner emits no OVERWRITE entries; the hardening is
  vacuous on honest trails by construction and verified by measurement.

## Binary note

`trial_bin_r4` (SHA-256 in EVIDENCE_MANIFEST.md) differs from the
2026-09-20 `trial_bin_s100` — expected: the checker is compiled into the
trial binary and the hardening is a deliberate, documented change.
Baseline rebuild of the unmodified sources was verified byte-identical
*before* the change (see below), so the delta is exactly the hardening.

## Baseline provenance (pre-change)

Unmodified sources rebuilt 2026-09-25 with the pinned toolchain
(`znc_linux_x86_64_abed8aa1`): `trial_bin_baseline` byte-identical to
`trial_bin_s100` (SHA a5d38def2ee96cffc684fafc2d749164e159fe84e67e060657e18c56e841d0ab).
The hardening diff touches only `strength_checker.zag` (+2 blocks).
