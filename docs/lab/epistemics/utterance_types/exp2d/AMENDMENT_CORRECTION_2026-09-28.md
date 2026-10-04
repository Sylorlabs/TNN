# CORRECTION Amendment — exp2d, 2026-09-28

**Status:** DATED CORRECTION. Add-only documentation; supersedes no file by
edit — `bartable.md`, `REPORT.md`, and `PREDICTIONS_LOCKED.md` remain as
committed records of what was claimed, and this file records what is true.
No code or corpus change. No re-runs required: every corrected number below
is read off already-committed evidence (commit `5871014c8a051f1bde3ef775f2c094db621731c2`,
`runs/`, `redteam/`).

## 1. abc2-a WD: "Pred match? YES" → NO

`bartable.md`, x2c novel-family table, row for `abc2-a`:

- Committed (wrong): `| abc2-a | 0/10 | 0/10 | YES |`
- Correct: `| abc2-a | 0/10 | 0/10 | NO |`

The locked prediction (`PREDICTIONS_LOCKED.md`, frozen 2026-09-27) was
**10/10** for abc2-a WD. The actual run of record is **0/10** in all 3 reps:

> `X2C_CURVE|3|WD|0|N|10` (`runs/abc2-a_rep1.txt`, rep2, rep3 — byte-identical)

The table printed the correct actual (0/10) but labeled it a prediction
match. It is not a match: 10/10 ≠ 0/10. The independent re-derivation flags
exactly one mismatch: `PRED-MISMATCH ('abc2-a', 'WD', 'X2C', 10, 0)`
(`redteam/rederive.log`).

**Mechanism of the miss (white-box, committed in REDTEAM.md KILL-1):** the
prediction's basis note assumed cc19's revocation of the `where do` marker
works in the α design. It does not — in `abc2-a` the α design learns `joke`
markers `evenly` / `says evenly` (support 1) that fire on every X2C probe
(all probes use context "says evenly"), so every probe is withheld as joke
regardless of `where do` status:

> `abc2-a wd: withheld 10/10; top markers: [('joke', 'evenly', 10), ('joke', 'says evenly', 10)]`

The prediction was derived from the "exact MDUMP reconstructor run on
committed **exp2c** MDUMP" — not from the exp2d α MDUMP that actually ran.
The α leg is the designated failing control, so this does not touch β's
results; but the exact-prediction claim and the bartable match label are
dead.

## 2. "All 9 predictions confirmed" → 8/9

`REPORT.md` line 17 — "**All predictions confirmed.** No surprises." — is
superseded. The independent red team killed the claim "all 9 pre-registered
predictions confirmed exactly" (REDTEAM.md KILL-1). The correct headline is
**8 of 9 predictions confirmed exactly**. What survives: the other 8 x2c
predictions, all 2c DP/LK predictions, and all 3 C3 collision predictions —
all match the runs exactly.

## 3. Breadth qualification — what-if generalization is construction-bound

The de2 WI 10/10 number is the **official-probe** number only. On 20 fresh
independently-authored probes (10 WI + 10 WD, zero 16-byte overlap with any
training/curriculum/probe text — `redteam/fresh_wi.txt`, `redteam/fresh_wd.txt`),
run live through base, abc2-b, de2-b:

| Leg | Fresh WI | Fresh WD |
|-----|----------|----------|
| base | 0/10 | 0/10 |
| abc2-b | 0/10 | 10/10 |
| de2-b | **4/10** | 10/10 |

(`redteam/fresh_probes_x2c.log`)

MDUMP white-box (`runs/de2-b_rep1.txt`): `what if` is revoked (status 3),
but `what if the` is **still live** (status 1). The D/E teaching installed
`what if the` only inside hypothetical-context items (vdW01–04, literal
interrogatives taught as hypothetical); the sincere vdE items are all
nominalized ("the what ifs" / "what if drills") and never counter it, so
eliminative revocation removed the former and spared the latter. The official
WI probe set exercises **only the construction taught as sincere**. The
interrogative construction — the very form taught as hypothetical — is still
withheld 0/5 on fresh probes.

**"D/E calibration revokes the what-if marker" is true of the `what if`
marker and false of the `what if the` marker. The 10/10 is construction-bound,
not family-general.** The learner discriminates constructions; the official
probe set cannot tell the difference. This qualifies the headline; it does not
kill the numbers — the locked de2-b WI 10/10 prediction on the official probes
is exact.

Caveat (from the red team, adopted): the fresh-probe runs are single-rep.
Cite 4/10 as a red-team attack result, not a locked number.

## 4. Where-do confound — no independent-generalization claim

Removing the single sincere item `cc19` ("Where do we meet the driver?")
from `cal2_abc.txt` and re-running `abc2-b`:

- WD: **10/10 → 0/10** (`redteam/cc19_removal.log`:
  `X2C_CURVE|3|WD|0|N|10`; committed reference `X2C WD 10/10`)
- T3 LK stays 10/10 (corpus otherwise intact)

The WD endorsement on every corpus leg is causally carried by **one training
item's** revocation of the `where do` marker, not by any generalization. No
independent-generalization claim may be made on WD; the wd probes confirm the
marker mechanism but do not isolate D/E (as `PREDICTIONS_LOCKED.md` itself
already flags).

## What stands unchanged

- The 8 surviving predictions (all x2c except abc2-a WD, all 2c DP/LK, all 3
  C3 collision bounds).
- C1: cleaned corpora score 0 flags at official dedupe thresholds; live
  removal of cc01/cc05 changes nothing (ab2-b T3 9/9, abc2-b T3 10/10 —
  `redteam/c1_counterfactual.log`).
- C3: v96 DP = 8/10 (T3), 9/10 (T4), 8/10 (T5) — exactly the bound.
- Design-β adoption (abc2-b passes all bars; abc2-a was and remains the
  designated failing control).
- Determinism: all 30 official runs byte-identical (3 reps each).

## Provenance

- Killed claim: REPORT.md line 17; PREDICTIONS_LOCKED.md x2c table
  (`| abc2-a | 0/10 | 10/10 | wi FAIL, wd PASS |`); bartable.md x2c table
  (`| abc2-a | 0/10 | 0/10 | YES |`).
- Evidence: commits f71ff91f66bc672d01f8b0a9544cf1067e465d90,
  736441f5d80f0307034c166f0ce9d72e56ce5d30,
  8779a026580c1ceb6efe2372506039b4d818b3db,
  5871014c8a051f1bde3ef775f2c094db621731c2 (independent red team).
- Author: correction crew, 2026-09-28. No Micah signature needed (additive
  documentation, no semantic or corpus change).
