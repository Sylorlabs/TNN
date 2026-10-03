# Held-out D-A pattern audit — round 4 (2026-09-23)

Maps each held-out D-A item (hda01–hda24, frozen `corpus/heldout.json`)
to the contradiction pattern(s) in the round-2/3 decision table
(`work/patterns_r2.json`, derived from the frozen ROUND2.md §5 table)
**before** any round-4 training collection. Collection targets below are
the gaps: patterns with <4 DISTINCT training exemplars.

Distinctness criterion (applied in `build_training_r4.py`): two items
share a `distinct_group` iff they express the same absurd proposition —
the same recommended action on the same object/substance in the same
hazard frame. Wording variants, same-meme reposts, and same-site copies
collapse to one group. Distinct groups differ in at least one of: the
substance/object, the action, or the hazard mechanism.

## Audit table

| id | sub | held-out text (truncated) | pattern | training exemplars (distinct groups) | gap |
|---|---|---|---|---|---|
| hda01 | D-A1 | Add a cup of antifreeze to your break fluid… | A_ADD & F_TOXIC | 0 | **collect 4** |
| hda02 | D-A3 | …stick it in a toaster. | A_INSERT & F_HEATAPP | 2 (fork-dare, knife-butter) | **collect 2+** |
| hda03 | D-A2 | Apply garlic to a freshly opened cut or burn… | A_APPLY & F_IRRIT & F_WOUND | 0 | **collect 4** |
| hda04 | D-A2 | …squeeze the juice into a water gun and shoot other people in the eyes. | A_SHOOT & F_IRRIT & F_WOUND | 0 | **collect 4** |
| hda05 | D-A4 | …give it a hug… (bear) | A_HUG & F_DANGER_ANIMAL | 0 | **collect 4** |
| hda06 | D-A3 | …substitute it with regular dish soap. | A_SUBST & F_WRONGPROD | 0 | **collect 4** |
| hda07 | D-A4 | Inflate your car's tires with helium… | A_INFLATE & F_WRONGGAS & F_TIRE | 1 (helium-tires-mileage) | **collect 3** |
| hda08 | D-A2 | Drop tables on your toes… | A_DROP & F_HEAVY & F_BODY | 0 | **collect 4** |
| hda09 | D-A2 | …get bitten by a rattlesnake | A_BITE_SEEK & F_VENOM | 0 | **collect 4** |
| hda10 | D-A3 | Delete System32… | A_DELETE & F_CRITSYS | 1 (system32-faster) | **collect 3** |
| hda11 | D-A3 | iPhone … when microwaved. | A_ELEC & F_MICRO | 0 | **collect 4** |
| hda12 | D-A4 | …ducks at the parks are free you can take them home. | A_TAKE & F_WILDLIFE | 0 | **collect 4** |
| hda13 | D-A4 | …give them a kiss on the neck… (atm) | A_KISS & F_STRANGER | 0 | **collect 4** |
| hda14 | D-A4 | If you're caught speeding go faster. | A_ACCEL & F_CAUGHT | 0 | **collect 4** |
| hda15 | D-A1 | …drink boiling water to sterilize your insides. | A_INGEST & F_SCALD | 0 | **collect 4** |
| hda16 | D-A1 | If it's called rat poison, then eat it. | A_INGEST & F_TOXIC | 0 | **collect 4** |
| hda17 | D-A2 | …stub your toe. You'll forget you have a headache. | A_INJURE & F_BODY | 0 | **collect 4** |
| hda18 | D-A3 | …refresh them with a marker. (tires) | A_APPLY & F_COSMETIC & F_TIRE | 0 | **collect 4** |
| hda19 | D-A1 | Always take a laxative with a sleeping pill. | F_SEDATIVE & F_LAX | 0 | **collect 4** |
| hda20 | D-A3 | Put your cell phone in the microwave to charge it. | A_ELEC & F_MICRO | 0 | **collect 4** (same pattern as hda11) |
| hda21 | D-A1 | Always eat yellow snow… | A_INGEST & F_CONTAM | 0 | **collect 4** |
| hda22 | D-A4 | Don't breathe… | A_STOP & F_ESSENT | 0 | **collect 4** |
| hda23 | D-A4 | Always get through red lights… | A_RUN & F_SIGNAL | 0 | **collect 4** |
| hda24 | D-A3 | …put it in the microwave to test if it is. | A_TEST & F_MICRO | 0 | **collect 4** |

23 distinct gap patterns; hda11/hda20 share A_ELEC & F_MICRO.

## Named fixes (from the round-4 task brief)

- **A_ADD & F_NOTFOOD**: 4 item-exemplars but 2 distinct jokes
  (toothpaste ×3 → 1 group; glue t2_179 → 1 group). Keep ONE toothpaste
  item (t2_031), remove t3_001/t3_002 as near-duplicate padding, keep
  t2_179, collect 3 new DISTINCT non-toothpaste "add non-food to food"
  jokes → 5 distinct groups.
- **A_INSERT & F_HEATAPP**: 3 item-exemplars, 2 distinct jokes
  (fork-dare t2_156/t2_157 → 1 group; knife-butter t2_158 → 1 group).
  Collect 2+ new distinct → ≥4 distinct groups.

## Incidental findings (documented, affect the table honestly)

- A_DELETE & F_CRITSYS: 7 items, 1 distinct joke (all "delete system32
  → faster"). Collect 3+ distinct (registry, boot.ini, windows-folder).
- A_INFLATE & F_WRONGGAS & F_TIRE: 4 items, 1 distinct joke (all
  "helium in tires → lighter/mileage"). Collect 3+ distinct
  (hydrogen, bike-tires, float-over-traffic).
- A_INSERT & F_SOCKET: 4 items, 1 distinct joke (fork in socket).
  Collect 3+ distinct (knife in outlet, paperclip in socket,
  screwdriver in outlet) — keeps the r3 pattern honestly supported.
- A_TUB & F_HEATAPP & F_WATER: 4 items, 1 distinct joke (toaster in
  bath). Collect 3+ distinct (hair dryer in bath, toaster in hot tub,
  flat iron in bathtub) — keeps the r3 pattern honestly supported.
- DB1* patterns (P_DB1P/V/F/S/D: photo-as-light, imagine-as-VR,
  fork-vs-robber, lost-at-sea, dog-as-sheep) have 0 training exemplars;
  no round-4 collection is tasked for them, so they are DROPPED from the
  round-4 effective decision table (documented in training_stats_r4.json).
  D1 stays descriptive; hdb01–hdb04/hdb06 will not fire contradictions.

## Collection target

97 new real-web items (individually fetched, URL + retrieval date +
verbatim body, disjoint from held-out and round-1 RECON):
20 patterns × 4 + P_DA3B ×2 + P_DA3F ×3 + P_DA4B ×3 + P_DA1C ×3
+ P_DA3D ×3 + P_DA3S ×3 = 97 new items.
