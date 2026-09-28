# Key Repair Record — grow-with-me retry battery (2026-09-28)

## What happened

The probe re-seal (AMENDMENT_2026-09-27_PROBE_RESEAL.md, committed in
`b825f54dd91a5d8570a33f07b5287345e1816c5c`) claimed: "Keys are byte-identical
to the frozen set... all other keys carried over unchanged." The independent
red team (Crew 3, `4cc98b945`, errata `2f9749700`) proved this false: **79
probe keys were changed** across 5 suites. 15 immediate-recall items became
unhittable under the re-sealed keys (no taught fact or fact pair reaches the
70% word-overlap bar), manufacturing 15 of M3's 42 misses. One re-sealed key
(F6-01) outright contradicts the taught fact and its frozen key.

The red team's standing recommendation: do NOT evaluate M2 until the frozen
keys are restored. This document records that restoration.

## What was restored

Every changed key was restored to its frozen value, byte-verified against the
frozen battery at `docs/lab/growwithme/frozen/probes/` (branch head
`origin/tnn-native-lab`, verified byte-identical to the amendment's pinned
commit `df3f77c3bee77ff189688d1cee07c8b98bcb3ca6` AND to `f71ff91f6` — the
"frozen originals untouched by the re-seal" claim checks out).

The repaired battery = **re-sealed questions + frozen keys**, exactly the
combination the re-seal amendment's scoring rule always intended ("C1/C2
gates and H1–H7 are scored against the RE-SEALED questions with the FROZEN
keys and FROZEN rubric thresholds"). The re-seal's validated properties are
preserved: 151/151 manifest hashes, zero old-question reuse, no key leakage
into agent-visible `.q` files (all re-verified by the red team; untouched
here).

### Per-suite result (independently re-derived, suite-scoped by file-stem + probe-id)

| Suite (re-sealed file) | Frozen source file(s) | Keys changed | Restored |
|---|---|---:|---|
| immediate_S1 | frozen immediate_S1 | 0/18 | n/a (intact) |
| immediate_S2 | frozen immediate_S2 | 0/18 | n/a (intact) |
| immediate_S3 | frozen immediate_S3 | 0/18 | n/a (intact) |
| immediate_S4 | frozen immediate_S4 | 0/18 | n/a (intact) |
| immediate_S5 | frozen immediate_S5 | 18/18 | 18 |
| immediate_S6 | frozen immediate_S6 | 18/18 | 18 |
| composition | frozen composition | 12/12 | 12 |
| corrections_pending_falsehoods | frozen corrections, pending, falsehoods | 18/18 | 18 |
| dependency_contradiction | frozen dependency_pre_S4, dependency_post, contradiction_resolution | 13/13 | 13 |
| S7_recall | frozen S7_recall | 0/108 | n/a (intact) |
| **Total** | | **79** | **79** |

Method: independent Python re-derivation (scripts `step1_inventory.py`,
`step2_diff_restore.py` in this directory), suite-scoped `(file-stem,
probe-id)` indexing — the same indexing that corrected the red team's own
82/85 errata. Zero probe-ID collisions across the multi-file suite maps
(corrections/pending/falsehoods and dependency_pre/dependency_post/
contradiction_resolution share no IDs). Zero re-sealed IDs lack a frozen
counterpart.

Verification on every restored file:
- Every restored `Key:` line is byte-identical to its frozen counterpart
  (0 mismatches across all 79).
- Every restored file differs from its re-sealed version ONLY on the
  restored `Key:` lines — all questions, Pair/Target/Source lines, and
  headers are byte-identical, except the two header fixes below.
- Full per-key diff: `KEY_DIFF.tsv` (79 CHANGED rows with frozen vs
  re-sealed key text; 237 SAME rows).

### No amendment was needed

All 79 keys restored cleanly — no key "genuinely cannot be restored," so no
per-key justifying amendment. The re-seal amendment's key claim is repaired,
not re-justified.

### Incidental header fixes (documentation only, not keys)

While restoring, two re-sealed header lines were found to swap the
PENDING/falsehood probe IDs relative to the frozen headers and the plant
ledger (ledger: S5 PENDING=F5-15 / falsehood=F5-14; S6 PENDING=F6-20 /
falsehood=F6-04):

- `immediate_S5.md`: "excludes PENDING F5-14 and falsehood F5-15" →
  "excludes PENDING F5-15 and falsehood F5-14"
- `immediate_S6.md`: "excludes PENDING F6-04 and falsehood F6-20" →
  "excludes PENDING F6-20 and falsehood F6-04"

Both probe files exclude both IDs either way (18 clean-fact probes), so
scoring is unaffected; the fix prevents future misreading. No other header
prose was touched.

## What was NOT changed

- Agent-visible `probes/*.q` files: byte-identical (questions only, no key
  material — re-verified by red team).
- `probes_resealed/MANIFEST.md`: byte-identical (151 question hashes hold).
- The M3 mechanism sources (`runner.zag`, `src/`): byte-identical to
  `b825f54dd`. The repair touches keys only.
- S1–S4 and S7 keys: verified 0 changes; the M3 kill stands on S1–S4 alone
  and is unaffected by this repair.

## Package restoration note

The full M3 retry package (`docs/lab/growwithme/retry/`) had been deleted
from the branch head by the unrelated exp2d tree-surgery accident
(`d09d5bfde`); only `redteam/` survived. As part of this repair the package
is restored to its original path, byte-identical to `b825f54dd`, with the
single exception of the five repaired key files above (plus this
`keyrepair_2026-09-28/` record). The restored package IS the staged M2
battery (see `../PREREG_M2_2026-09-28.md`).

## Sanity check (fresh rebuild + re-run, D/N arms) — COMPLETE 2026-09-28

Full evidence: `SANITY.md` (this directory).

- **Build:** pinned toolchain (`znc_linux_x86_64_abed8aa1`, SHA-256
  `498abcb5...35a4277dedfba4782e1373137e58ef` verified); binary SHA-256
  `4b8d7f473d7b05c5505ed02989a35116c11c449b4956dfb2d3505b753a582cac` —
  byte-identical to the red team's independently rebuilt binary.
- **Determinism:** fresh `runs/D_run1` and `runs/N_run1` byte-identical
  (recursive diff, zero differences) to the red team's original runs.
- **Rescore vs restored keys** (frozen 70%-overlap scorer) — exactly the
  red team's frozen-key rescore:

| Arm | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| D | 17/18 .944 | 13/18 .722 | 11/18 .611 | 16/18 .889 | 13/18 .722 | 11/18 .611 |
| N | 17/18 .944 | 13/18 .722 | 11/18 .611 | 16/18 .889 | 13/18 .722 | 11/18 .611 |

C1/C2 still fail every session — the M3 kill is unaffected by the repair,
as predicted. The battery is clean and staged for M2.
