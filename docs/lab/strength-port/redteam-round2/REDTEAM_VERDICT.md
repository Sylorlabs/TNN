# REDTEAM VERDICT — round 2, blind black-box

Binary: `/home/hatch/workspace/strength-port-fix/redteam/fix_rt_bin` (mode G).
Scope: 123 attack sequences, each run twice. **Determinism: 123/123 byte-identical across runs — zero nondeterminism.**
Hygiene: every run ends `RT_END refusals_clean=0 replay=0 ckfail=0`; all `CL_CHECK` expected==actual.
Blinding held: no sources, workdirs, or committed docs touched. Nothing committed.

## Per-objective verdicts

| # | Objective | Verdict |
|---|---|---|
| 1 | Cite resurrection | **HELD** (security property) + FINDING (letter deviation, no exploit) |
| 2 | Wedge recovery | **HELD** — no wedge found by any shape |
| 3 | Cross-slot double-spend | **HELD** |
| 4 | Weaken discount | **HELD** |
| 5 | u32 aliasing (regression) | **HELD — round-1 fix VERIFIED** |
| 6 | TD-down pricing | **HELD** |
| 7 | Rollback depth | **HELD** |
| 8 | Honest regression | **HELD** |
| 9 | Over-cite (regression) | **HELD — round-1 fix VERIFIED** |
| 10 | price(0) observation | **CONFIRMED as predicted** |

## Findings

### F-1 (objective 1, letter deviation — no security impact)
**Re-citing a spent episode is accepted at cite time (rc 0) instead of refused.**
Law 2 says "Re-citing → refused (121)". Observed: `ADD90 CITE0..3 JUST KILL` (spends 0–3), then new judgment + `CITE0` → rc 0 — on the same slot (O1g, O3d, F4), on another slot (X1). The 121 refusal lands only at destruction time, when fresh-attached < price. The **security property holds completely**: a spent episode can never count toward a destruction price — every destruction demands price-many *fresh* cites (X2, O1g, X3 KILLT, X4 DEL, X6 OW, F5/Z3/Z4 RB-restore, Z2 mixed 1-spent+1-fresh → 121). Spent set is store-wide, permanent, cross-slot, across slot reuse. Duplicate attach of the same episode is still refused (111). Severity: cosmetic/spec-letter only; recommend either refusing spent cites at cite time (121) or amending the brief to "re-use as payment → refused (121)".

### F-2 (objective 7, cosmetic)
**`RB` after a trainer `TD` op returns rc 113** — the code otherwise documented for KILLN refusal. Behavior is safe (refusal; the TD stands — F6a vs F6b control identical; subsequent ops normal; RT_END clean), and semantically it reads as "trainer authority required to undo a trainer op". Recommend a distinct code or a brief note; not a vulnerability.

### Non-findings (verified safe)
- **Over-cite** (round-1 fix): 5th/6th fresh cite → clean 122; slot stays fully usable; destruction with price-many succeeds (O9a/O9b/F3). The 122 cap counts *fresh*-attached only — spent re-cites never wedge the slot (P-A).
- **u32 aliasing** (round-1 fix): `CITE0` vs `CITE4294967296` are distinct identities through cite, destroy, *and* the spent set (F2: spend 0, cite 2^32 → fresh, KILL=0). 2^31/2^32/2^33 boundaries, 2^55−1 accepted, ≥2^55 → clean 2001.
- **Weaken/TD/STR discount**: price is always `ceil(strongest/25)` over the judgment's max-ever strength; weakening/overwriting/TD-down never reduce it (O4a/b/d, O6a/d/f, Y2/Y3/Z1). `OW` resets lineage only after charging the full erase price (O4f, O10a, Y2).
- **RB**: single-level (2nd RB → 108); undoes ADD/KILL/DEL/OW; restores the attachment list with spent flags intact (re-destroy → 121, never a resurrection); CITE/JUST are non-mutating; a refused op leaves nothing to undo; RB never lowers strongest (P-C2); refusals leave the store untouched.
- **KILLN** always 113 and destroys nothing (cites survive for a later KILL — A21). **KILLT** destroys at full price, never discounted (A08/A09), and spends store-wide (X3). **DEL** spends store-wide (X4); deleted slot's citations stay spent.
- **Store capacity**: 14 usable slots (first-free from 2); 15th ADD → clean 104; destruction still succeeds when full and frees the slot (Y1). Not a wedge vector.
- **price(0)**: `OW0` consumes the 4 full-price cites, then `KILL` on the 0-strength judgment succeeds with zero cites (O10a) — exactly per the law's prediction.

## Reproducing sequences (all `fix_rt_bin G …`, deterministic)
- Letter-deviation re-cite: `G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL` → re-cites rc 0, final `KILL` → 121
- Cross-slot double-spend attempt: `G ADD90 ADD90 SLOT2 CITE0 CITE1 CITE2 CITE3 JUST KILL SLOT3 CITE0 CITE1 CITE2 CITE3 JUST KILL` → second `KILL` → 121
- RB-113: `G ADD90 TD10 RB` → `RB` → 113 (TD stands)
- Over-cite: `G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL` → `CITE4` → 122, `KILL` → 0
- u32: `G ADD90 CITE0 CITE4294967296 CITE1 CITE2 JUST KILL` → 0
- price(0): `G ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 JUST KILL` → `OW0` → 0, `KILL` → 0

## Bottom line
Both round-1 findings are **truly fixed** (verified with fresh shapes, including 64-bit spent-set identity and spent-episode over-cite). No new broken objectives. The mechanism held against resurrection, wedge, double-spend, discount, aliasing, TD-pricing, and rollback attacks across 123 deterministic sequences. Two cosmetic notes (F-1 letter deviation, F-2 code reuse) carry no exploit.
