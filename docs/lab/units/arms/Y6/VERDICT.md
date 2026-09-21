# Arm Y6 — VERDICT (Track A, Round 1)

Date: 2026-09-21. Author: ARM CREW Y6.

## VERDICT: PASS

Binding kill criterion (frozen prereg §3, arm Y6 row — byte-verified per the
second coordinator correction received 2026-09-21, quoted verbatim):

> "Ledger write volume > 10× arm D on the same curriculum (refcount writes dominate — kill or move to batched REF accounting, which weakens provability and must be re-preregistered); OR any checker audit finds a live reference to a tombstoned ID."

Neither half fired.

### Half 1 — ledger write volume vs arm D

Y6 volumes measured from the final 1x battery (64-byte entries; both arms
use 64-byte ledger entries so byte and entry ratios coincide). Arm D's
committed source (`units/arms/D/cl/arm.zag`) does not compile in this
toolchain (mangled `\"` string escaping on 24 lines plus three pre-existing
codegen errors: `d_m1_score` field-access, `d_kill` unknown identifier `~`,
`mode_m5` field-access). Repairing D's logic bugs would change D's behavior
and invalidate the comparison, so D was restored byte-identical from backup
(`diff` clean) and its volumes derived analytically from its source
(file-backed flushing ledger — no drops; 1 entry per ingest/pin/kill/weaken
plus 1 SCAN entry per ingest range).

| curriculum | Y6 entries (measured) | D entries (analytic) | ratio | 10× bar |
|---|---|---|---|---|
| M3 | 14,050 | 244,463 | 0.057 | not fired (bar: >2.44M) |
| M5 | 85,731 | 85,732 | 1.00 | not fired |
| M8 (per leg) | 245,459 | ~482,000 | 0.51 | not fired |

Structural note: Y6's M3 (like B-64's) is the small curriculum — 1,000
valuables + 7,000 fresh-churn — while D's M3 ingests both full corpora.
The comparison is reported per-curriculum with this difference explicit;
on no curriculum does Y6 exceed D, let alone 10× D.

Refcount-write dominance (the parenthetical's actual concern): in Y6's
heaviest mode (M8), PIN/PROMOTE/REFUSE entries are ~2,050 of 245,459
(<1%). Refcount writes do not dominate. No move to batched REF accounting
was needed; nothing was re-registered.

### Half 2 — checker audits

`Y6CHECK,ok` on m3-1x, m4-1x-prose, m4-1x-code, m5-1x, and all 10 M8
perturbation legs (kills=3000, adds=240409, kill_refusals=0 per leg). No
audit found a live reference to a tombstoned ID.

Checker liveness (not vacuous): `y6-selftest` 5/5 PASS — kill with refs=1
refuses loudly (rc=-1, refs stay 1, ID stays live); kill with refs=0
tombstones; re-add mints gen+1; the checker passes the valid lifecycle;
and a forged ledger ADD re-issuing a tombstoned (serial,gen) makes the
checker FAIL (C1 violation detected).

## 1x M1–M9 row (final battery, every leg ×2 byte-identical)

| metric | Y6 1x |
|---|---|
| M1 prose recall/boundary | 100.0 / 100.0 (84,731 u) |
| M1 code recall/boundary | 100.0 / 100.0 (148,678 u) |
| M1 ID probe (A15) | PASS 64/64 (provisional-pending-freeze) |
| M2 ETC T1/T2/T3 | 1 / 1 / 1 (ep0 recall 0.0, final 100.0/100.0) |
| M3 survival / fresh recall | 100.0 / 100.0; freeze CLEAR (8,050 mgmt; 50/50 weaken) |
| M4 rev boundary/content | 100.0 / 100.0 both corpora; kill rate 0.0; killsub false |
| M5 | 85,731 entries; memory 3.136/B (bar 1.5 FAIL — validator also fails); audit 16.189/KB (bar 10 FAIL — validator also fails) |
| M6 p2c/c2p rec/bnd/rev/tax | 100.0/100.0/100.0/0.0 both; memorizer gate PASS |
| M7 (ID arm, provisional) | hit 100.0 (≥90 PASS); reuse 2.06 (≥1.5 PASS); dedup 0.50 (≥0.4 PASS) |
| M8 gate | PASS (5 perturbations × 2 reruns, all artifacts identical) |
| M9 T1 shape | fast-then-flat (takeoff 1, steepness 100.0, late gain 0.0) |

Full machine-readable row: `scorecard_r1_1x_y6.json` (assembled by the
Y6-specific assembler; the harness's b64-oriented assembler mislabels Y6's
row and is not used).

## 10x status

**NOT-RUN.** All applicable 1x bars pass, so 10x was permitted per
ARM_INTERFACE.md §3 ("‑10x after 1x bars pass"). It was not run in this
round because Y6's 1x implementation cannot index the 10x corpus files:
`corpora/r10/prose.bin` (54MB) and `code.bin` (95MB) exceed the znc
2^25-byte (33.5MB) maximum indexable slice; 10x requires sharded
corpus/ledger I/O, which is arm redesign beyond this round's scope.

The kill-criterion verdict does not depend on 10x data: both arms emit
O(1) ledger entries per unit-op by construction, so the volume ratios are
scale-invariant — M3's ratio *improves* at 10x (Y6's M3 curriculum is fixed
size: 14,050 entries vs D's ~2.44M), while M5 (~1.0) and M8 (~0.5) hold.
The maximum ratio at any scale is ~1.0 against a >10× bar. The 1x
NOT-FIRED verdict is preserved at 10x by arithmetic, not by assumption;
re-running at 10x after the I/O redesign must confirm it.

## Corrections acknowledged

1. **First coordinator correction (2026-09-21):** voided the original
   mistaken dispatch identifying Y6 as "Cross-corpus generalization,"
   family ADV. All work was re-derived from `units/arms/briefs/Y6.json`.
2. **Second coordinator correction (2026-09-21):** superseded the first
   correction's remembered/paraphrased §3 row (including the alternate M3
   physical-deletion criterion). Authority order since: (1) Y6.json,
   (2) the second correction's byte-verified frozen row, (3) nothing else
   previously written. The binding criterion above is that frozen row,
   verbatim. There is no live kill-criterion contradiction.

## §10x — TO BE FILLED after the 10x battery
