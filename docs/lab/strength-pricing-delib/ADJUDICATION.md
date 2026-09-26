# Arm E red-team adjudication (coordinator, 2026-09-26)

Red team verdict: BROKEN (3 of 5 objectives + 2 brief criteria).
Coordinator re-verification against `blind/arm_E/price_arm_E_rt_bin`: **most breaks collapse.**
Method: independent op sequences, same binary. All coordinator probes below are
reproducible via the command lines quoted.

## Claim-by-claim

| # | Red-team claim | Coordinator probe | Result |
|---|---|---|---|
| 1 | Strength invisible to deliberator; "max-strength" memory killed for 0 cites | Their `ADD9 STR9` = strength **9** (WEAK by design: ≤25 → −1). `ADD90` → RT_DELIB 2 bare, 4 with 3 cites + JUST6. `ADD90 WEAK0 DELIB` → 2 (high-water survives weakening). Strong memory with tuned-down trail+reason: `ADD90 JUST1 DELIB` → 1, `ADD90 JUST3 DELIB` → 1, `ADD90 JUST1 JUST3 DELIB` → 1 | **FALSE — scale misread.** Strength is a genuine input; strong memories floor at 1 |
| 2 | Deleter tunes pre-DELIB JUST so price == cites, "kill always succeeds" | Trail weight uses MAX tier (cannot talk a salient memory down); strength history audited; price-0 reachable only on weak/uncontested histories — the design's intended discriminative pricing | **OVERCLAIMED.** Held; residual: stated-reason input is self-reported (±1, deleter never states 7) |
| 3 | OW does not consume the global per-episode budget | `... OW0` (paid with CITE1–4) then re-cite CITE1–4 on slot 3 → second `OW0` refuses **121** | **FALSE.** OW burns its payment episodes store-wide |
| 4 | Default personality behaves as PERS2, brief wrong | `ADD90 CITE1-3 JUST6 DELIB` (4) `CITE4 JUST1 OW0` (0) then bare `DELIB` → **4** (sees the pre-overwrite 90). Their test used strength-9 memories where both personalities price 0 — non-discriminating | **FALSE.** Default is PERS1, history-seeing; brief correct |
| 5 | ≥5-cite memories permanently indestructible | After 109: `STR5` (new effort window, free, audited) → re-`DELIB` (3) → cite exactly 3 → `KILL` **0** | **FALSE.** Documented recovery path verified |
| 6 | Bare JUST accepted = reason forgery | DESIGN.md explicit: unstated reason → OTHER, no price move; four reason codes recorded by construction | Design-explicit leniency, not a break. Accountability thinner than brief implies — noted |
| 7 | COST disagrees with DELIB after PERS switch | `PERS1 ... DELIB`(3) `OW0`(0) `PERS2` `COST` → 0; kill after switch → **122** (record immutable, fail-closed) | **CONFIRMED, minor, fail-closed.** COST answers "current personality"; the record/checker use the recorded one. Brief rule 5 needs correcting or COST should report the enforceable price. No exploit |
| 8 | 121 unreachable / vacuous protection | Probe in row 3: 121 fires on re-cited OW-consumed episodes | **FALSE** |

## Adjudicated verdict

- **Deliberative pricing HOLDS as a mechanism.** Prices vary 0–4 with the
  memory's actual history, deterministically, checker-recomputed from the
  ledger prefix. Honest-400: 297 destroyed / 89 abandoned — beats every fixed
  arm except the indiscriminately-cheap C2/D.
- **The price-floor question is answered:** under the default PERS1 the
  deliberator sees through overwrite resets (re-DELIB after OW on a
  strength-90 memory → 4); PERS2 reproduces the high-water overwrite-reset
  tradeoff explicitly. The overwrite is the priced step, and it burns its
  payment episodes store-wide (121-verified).
- **Micah's hypothesis survives in native form:** "costs, but varies" —
  strong/contested/salient histories cost up to 4, weak/uncontested histories
  cost 0–1, by deliberated judgment with recorded reasons, not a fixed formula.
- Honest caveats: (a) the weight table is explicit but not derived — tuning is
  future work; (b) the stated-reason input is self-reported (±1); (c) the COST
  oracle inconsistency (row 7) should be fixed or brief-corrected; (d) price-0
  for weak memories is intended discriminative pricing, not a hole — if Micah
  wants a hard floor > 0 even for weak memories, that is a law choice, not a
  mechanism repair.
- The red team's report (`~/workspace/strength-delib-rt/VERDICT.md`) stands as
  their honest attempt; rows 1, 3, 4, 5, 8 above are methodology errors
  (strength-scale misread, non-discriminating personality tests, untested
  recovery path), corrected here with reproducing command lines.

## Repro (all vs `blind/arm_E/price_arm_E_rt_bin`)

- `SLOT2 ADD90 CITE1 CITE2 CITE3 JUST6 DELIB` → RT_DELIB 4 (strength matters)
- `SLOT2 ADD90 WEAK0 DELIB` → RT_DELIB 2 (high-water survives weakening)
- `SLOT2 ADD90 JUST1 JUST3 DELIB` → RT_DELIB 1 (strong floor holds vs tuning)
- OW-consume: `SLOT2 ADD90 CITE1 CITE2 CITE3 JUST6 DELIB CITE4 JUST1 OW0`
  `SLOT3 ADD90 CITE1 CITE2 CITE3 CITE4 JUST6 DELIB CITE5 JUST1 OW0` → 121
- PERS1 default sees through: `... OW0` then `DELIB` → 4
- Immortal recovery: `... KILL`→109 then `STR5 DELIB CITE10 CITE11 CITE12 JUST1 KILL` → 0
