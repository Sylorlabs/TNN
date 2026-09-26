# ATTACK LOG — red-team round 2, blind black-box

Binary: `/home/hatch/workspace/strength-port-fix/redteam/fix_rt_bin`, mode G only.
Method: every sequence executed TWICE as `fix_rt_bin G <tokens>`; outputs byte-compared.
Determinism: **123/123 sequences byte-identical across both runs** (86 in `results/`, 37 in `results2/`).
Hygiene: all 123 runs end `RT_END refusals_clean=0 replay=0 ckfail=0`; every `CL_CHECK` line has expected==actual.
Blinding: no .zag files, workdirs, or committed docs were read at any point.

## Decoded rc table (grounded in observed behavior)

| rc | meaning | key evidence |
|---|---|---|
| 0 | success | — |
| 103 | no judgment in selected slot | A11 CITE7 on empty slot; A19/A20 JUST/DEL empty; O1b CITE after KILL; O7d CITE after RB-undid-ADD |
| 104 | store full — no free slot | X7: 15th ADD |
| 108 | RB: nothing to undo (empty stack, last op non-mutating, or last op refused) | O2d/O2e RB alone; O2c 2nd RB; O7b RB after CITE; O7e RB after JUST; O2h RB after refused KILL |
| 109 | destruction refused: attached cites < price | A01 (0 cites, price 4); A02 (1 of 4); A15 (1 of 2); O4a/O4b/O4d weaken variants |
| 110 | destruction attempted without JUST | A03 KILL; PD1 DEL; PD2 KILLT; PD3 OW |
| 111 | duplicate cite — episode already attached to this judgment | O1e CITE0 twice; O1c re-cite after RB-restore; F4 re-cite spent twice |
| 113 | non-trainer refusal (KILLN); also RB-after-TD (trainer op) refused | A06/A07 KILLN; PC3/F6a RB after TD — TD stands, later ops normal |
| 121 | destruction refused: fresh-attached cites < price (some attached are spent) | O1g (4 spent attached); X2 cross-slot; Z2 (1 spent + 1 fresh, price 2); F5/Z3/Z4 RB-restore re-destroy |
| 122 | over-cite: fresh-attached already ≥ price | O2a/O9a/O9b (5th/6th fresh); F3 (spent episode as excess); O10c (any cite at price 0) |
| 2001 | malformed argument (episode ≥ 2^55, strength > 100) | A13 CITE 2^55; A18 ADD101; O5g/O5h; Y4/Y5/Y6 |

## Verified mechanism model (all black-box inferred)

- **Slots:** `ADD<s>` admits to the FIRST FREE SLOT, ignoring the `SLOT<n>` selector (the brief itself says "admit … to first free slot" — spec behavior, not a bug). Slots 0–1 are unavailable at start (or search starts at 2); **14 usable slots (2–15)**; 15th ADD → 104. `SLOT<n>` routes every non-ADD op.
- **Price:** `price = ceil(strongest/25)` where strongest = max strength the judgment lineage ever held (monotonic). `OW` resets lineage but costs the full erase price first. `RB` cannot lower strongest (P-C2: ADD10 STR90 RB, 1-cite KILL → 109).
- **Destruction gate (KILL/DEL/KILLT/OW):** needs judgment (103), needs JUST (110), needs attached ≥ price (109), needs **fresh**-attached ≥ price (121). On success every attached episode enters the store-wide permanent spent set.
- **Cite-time checks:** 103 (no judgment), 111 (already attached), 122 (fresh-attached ≥ price), 2001 (malformed). **No spent-check at cite time** — spent episodes attach with rc 0 (O3d, O1g, X1, F4); they never count toward price or the 122 cap (F4: 2nd re-cite → 111 proves attachment; P-A: fresh still attachable after 4 spent attached).
- **RB:** single-level undo of the last MUTATING op (ADD/KILL/DEL/OW; WEAK/STR return 0 but strongest is preserved). Restores judgment WITH its attachment list (spent flags intact — re-destroy → 121). CITE/JUST are not mutating. A refused op leaves nothing to undo. RB after TD → 113 (refused, trainer op stands).

## Phase A — behavior mapping (results/*.run1)

- A01 `ADD90 JUST KILL` → KILL=109 (price 4, 0 cites)
- A02 `ADD90 CITE0 JUST KILL` → KILL=109 (1 of 4)
- A03 `ADD90 CITE0 CITE1 CITE2 CITE3 KILL` → KILL=110 (no JUST)
- A04 `… JUST DEL` → DEL=0
- A05 `ADD90 JUST DEL` → DEL=109
- A06 `KILLN` → 113 (empty slot)
- A07 `ADD90 CITE0..3 JUST KILLN` → KILLN=113
- A08 `… JUST KILLT` → KILLT=0 (full price)
- A09 `ADD90 CITE0 CITE1 JUST KILLT` → KILLT=109 (authority never discounts)
- A10 `SLOT0 ADD10 SLOT1 ADD20 SLOT5 ADD30 SLOT9 ADD40` → all 0 (ADD ignores selector; lands first-free)
- A11 `CITE7` (empty) → 103
- A12 `ADD25 CITE36028797018963967 JUST KILL` → KILL=0 (2^55−1 accepted)
- A13 `ADD25 CITE36028797018963968` → 2001 (2^55 refused at entry, clean)
- A14 `ADD25 CITE0 JUST KILL` → 0 (price 1)
- A15 `ADD26 CITE0 JUST KILL` → 109 (price 2)
- A16 `ADD0 JUST KILL` → 0 (price 0, no cites)
- A17 `ADD100 CITE0..3 JUST KILL` → 0 (price 4)
- A18 `ADD101` → 2001
- A19 `JUST` (empty) → 103; A20 `DEL` (empty) → 103
- A21 `… KILLN KILL` → KILLN=113, KILL=0 (refusal left cites intact)
- A22 `ADD90 CITE0 CITE1 JUST KILL(=109) CITE2 CITE3 JUST KILL` → 2nd KILL=0 (refusal clean, top-up works)
- A23 `CITE0(=103) ADD90 CITE1..4 JUST KILL` → KILL=0 (cite on empty refused cleanly, later cites fine)

## Objective 1 — cite resurrection

- O1a (mis-designed: 2nd ADD landed same slot2; CITE0 on empty slot3 → 103) — superseded by X1
- O1b `…KILL CITE4` → 103 (slot empty)
- O1c `…KILL RB CITE0` → 111 (RB restored attachment; dup refused)
- O1d `…KILL RB SLOT3 ADD90 CITE0` → 0 (KILL undone ⇒ spend undone; honest rewind)
- O1e `ADD90 CITE0 CITE0 JUST KILL` → 2nd CITE0=111, KILL=109
- O1f `ADD90 CITE0 CITE0 CITE1 CITE2 JUST KILL` → 111, KILL=109
- O1g `…KILL ADD90 CITE0..3 JUST KILL` → re-cites 0 (accepted), final KILL=121
- O1h `…OW10 CITE0` → CITE0=0 (spent, cite-time accepted; slot2 held new strength-10 judgment)
- O1i `…DEL CITE0` → 103 (slot empty after DEL)
- X1 `ADD90 ADD90 SLOT2 CITE0..3 JUST KILL SLOT3 CITE0 CITE4..7 JUST KILL` → slot3 CITE0=0 (spent, accepted), KILL=0 (paid by 4 fresh)
- X3 `…KILLT ADD90 CITE0..3 JUST KILL` → 2nd KILL=121 (KILLT spends store-wide)
- X4 `…DEL ADD90 CITE0..3 JUST KILL` → 2nd KILL=121 (DEL spends store-wide)
- X6 `…OW10 ADD90 CITE0..3 JUST KILL` → 2nd KILL=121 (OW spends)
- F4 `…KILL ADD90 CITE0 CITE0 JUST KILL` → CITE0=0 then 111, KILL=121
- **Net: re-cites accepted at cite time (rc 0) — letter deviation from "Re-citing → refused (121)"; destruction always demands fresh cites (121). No double-spend.**

## Objective 2 — wedge recovery

- O2a `ADD90 CITE0..3 CITE4(=122) CITE5(=122) JUST KILL` → KILL=0 (excess refused cleanly)
- O2b spent episode mid-sequence then fresh top-up → KILL=0
- O2c `…KILL RB(=0) RB(=108) CITE4..7 JUST KILL` → KILL=0 (single-level undo)
- O2d/O2e `RB` / `RB RB RB` → 108
- O2f `…KILL RB CITE4..7 JUST KILL` → KILL=0 (restore + fresh destroy)
- O2g `…DEL RB CITE0` → 111 (restore keeps spent flags)
- O2h `ADD90 CITE0 JUST KILL(=109) RB(=108) CITE1..3 CITE4(=122) JUST KILL` → KILL=0
- O2i `…KILL RB WEAK0 CITE4 JUST KILL(=109) CITE5..7 JUST KILL` → final KILL=0
- O2j `ADD90 TD0 CITE0..3 JUST KILL` → KILL=0 (TD can't wedge pricing)
- P-A `…KILL ADD90 CITE0..3(spent, all 0) CITE4(=0!) JUST KILL` → KILL=121 — spent attaches don't consume the fresh cap; slot still accepts fresh cites (no wedge)
- Y1 full store (14 ADDs): SLOT2 CITE0 JUST KILL=0, then ADD10=0 (destruction works when full; slot freed)
- X7: 15th ADD → 104 (capacity refusal, clean)
- **Net: no wedge found by any shape; every refusal leaves the slot/store usable.**

## Objective 3 — cross-slot double-spend

- O3a disjoint cites both slots → KILL=0, KILL=0
- O3b shared pre-cite: SLOT2 KILL=0, SLOT3 KILL=121
- O3c interleaved shared pre-cite: SLOT2 KILL=0, SLOT3 KILL=121
- O3d same-slot re-cite (spent, 0) + fresh CITE20, price(10)=1 → KILL=0 (paid by fresh)
- O3e one shared cite: SLOT2 KILL=0 spends it, SLOT3 KILL=121
- X2 true cross-slot double-spend attempt → 121
- **Net: one episode never pays twice; second destruction always 121.**

## Objective 4 — weaken discount

- O4a `ADD90 WEAK0 CITE0 JUST KILL` → 109
- O4b `ADD90 WEAK75 CITE0 CITE1 JUST KILL` → 109
- O4c `ADD90 WEAK89 CITE0..3 JUST KILL` → 0 (honest full price)
- O4d `ADD50 STR90 WEAK0 CITE0 JUST KILL` → 109 (strongest 90 rules)
- O4e `ADD90 CITE0 JUST OW10` → 109 (overwrite priced)
- O4f `ADD90 CITE0..3 JUST OW10 CITE4 JUST KILL` → OW10=0, KILL=0 (price(10)=1)
- O4g `ADD10 STR90 CITE0..3 JUST KILL` → 0 (price rose to 4)
- Y2 `ADD10 CITE0 JUST OW90 CITE1..4 JUST KILL` → 0 (price 4 by strongest 90)
- Y3 `ADD10 WEAK90 CITE0 JUST KILL` → 109 (WEAK sets to 90; price 4)
- Z1 `ADD50 WEAK90 CITE0..3 JUST KILL` → 0; Z1b 1 cite → 109; Z1c `ADD50 WEAK30` + 2 cites → 0
- **Net: price always by strongest-ever; no strength manipulation discounts destruction.**

## Objective 5 — u32 aliasing (REGRESSION PROBE)

- O5a `CITE0 CITE4294967296 CITE1 CITE2 JUST KILL` → 0 (0 and 2^32 distinct)
- O5b `CITE2147483648 CITE2147483649 CITE2147483647 CITE4294967295` → 0 (2^31 boundaries fine)
- O5c `ADD25 CITE4294967296 JUST KILL` → 0
- O5d `… CITE8589934592` (2^33) → 0
- O5e (mis-designed slots) — superseded by F2
- O5f `CITE36028797018963967` (2^55−1) → 0
- O5g/O5h `CITE36028797018963968`, `CITE18446744073709551615` → 2001, then KILL=109 (clean)
- O5i `CITE0 CITE0 CITE1 CITE2 JUST KILL` → 111, KILL=109 (no double-count)
- F2 `ADD25 CITE0 JUST KILL ADD25 CITE4294967296 JUST KILL` → 2nd KILL=0 (**spent set is 64-bit**: 2^32 not aliased to spent 0)
- **Net: round-1 aliasing fix VERIFIED — full 64-bit episode identity everywhere.**

## Objective 6 — TD-down pricing

- O6a `ADD90 TD10 CITE0 JUST KILL` → 109
- O6b `ADD90 TD10 CITE0..3 JUST KILL` → 0
- O6c `ADD10 TD90 CITE0..3 JUST KILL` → 0 (TD raises price correctly)
- O6d `ADD90 TD0 CITE0 JUST KILL` → 109
- O6e `TD90` on empty → 103 (and all follow-ons 103)
- O6f `ADD90 WEAK50 TD10 CITE0 JUST KILL` → 109
- **Net: TD never lowers price below ceil(strongest/25).**

## Objective 7 — rollback depth

- O7a `…KILL RB CITE0(=111) CITE4..7 JUST KILL` → 0
- O7b `ADD90 CITE0 CITE1 RB(=108) CITE2 CITE3 CITE4(=122) JUST KILL` → 0 (CITE not mutating)
- O7c `…KILL RB(=0) RB(=108) …` → 0 (single level)
- O7d `ADD90 RB(=0) CITE0(=103)` (ADD undone)
- O7e `…JUST RB(=108) KILL` → KILL=0 (JUST not mutating)
- O7f cites then double RB → 108, 108
- O7g `…OW10 RB(=0) CITE4 JUST KILL` → 109 (OW undone; strongest back to 90)
- P-C1 `ADD90 WEAK10 RB(=0) …` → KILL=0
- P-C2 `ADD10 STR90 RB(=0) CITE0 JUST KILL` → 109 (strongest NOT lowered by RB)
- P-C3/F6a `ADD90 TD10 RB` → **113** (refused; TD stands — F6b control identical at 109)
- F5 `…DEL RB JUST DEL` → 121; Z3 `…KILL RB JUST KILL` → 121; Z4 DEL variant → 121
- P-B `…KILL RB CITE0(=111) CITE4..7 JUST KILL` → 0
- P-A2 `…KILL RB CITE4..7 CITE8(=122) JUST KILL` → 0 (122 counts fresh-only)
- **Net: RB is honest — single level, restores attachments with spent flags intact, never resurrects spend, never lowers strongest, refuses to undo trainer ops.**

## Objective 8 — honest regression

- O8a `ADD90 CITE0..3 JUST KILL` → 0
- O8b `… JUST DEL` → 0
- O8c `… JUST KILLT` → 0
- All RT_END zeros. **HELD.**

## Objective 9 — over-cite regression (REGRESSION PROBE)

- O9a `ADD90 CITE0..3 CITE4(=122) JUST KILL` → KILL=0
- O9b two excess cites → 122, 122, KILL=0
- O9c (mis-designed slots) — superseded by F3
- O9d `…CITE0(=111) JUST KILL` → 0
- F3 `…KILL ADD90 CITE10..13 CITE0(spent, =122) JUST KILL` → KILL=0 (excess refused; slot usable)
- **Net: round-1 over-cite fix VERIFIED — excess refused cleanly at cite time, destruction with price-many succeeds.**

## Objective 10 — price(0) observation

- O10a `ADD90 CITE0..3 JUST OW0(=0) JUST KILL` → KILL=0 with zero cites attached
- O10b `ADD90 JUST OW0` → 109 (overwrite priced at full erase price)
- O10c `…OW0 CITE0(=122) JUST KILL` → KILL=0 (price-0 cap refuses any cite; destruction free)
- **CONFIRMED as predicted: OW0 destroyed the 90-strength judgment at full price (4 cites consumed); the subsequent KILL prices the 0-strength judgment at 0.**

## Follow-up probes (results2/)

- E1/E3/E5/E6 — slot-model determination (ADD → first free slot; 14 usable slots)
- P-D1/D2/D3 — DEL/KILLT/OW without JUST → 110
- Z2 — 1 spent + 1 fresh attached, price 2 → 121 (fresh-count rule precise)
- X5 — 4 spent + 4 fresh attached → KILL=0 (paid by fresh)
- X7/Y1 — store capacity: 14 ADDs ok, 15th → 104; destruction + refill fine when full
- Y4/Y5/Y6 — WEAK200/TD200/STR200 → 2001 (clean)
