# CORPUS2 — Round-2 diverse training corpus

12 real photographs from Wikimedia Commons, 768px wide, RGB JPEG q90,
normalized by subagent 2026-09-27. Full provenance in MANIFEST.tsv.

## Images

| File | Category | Author | License | Source |
|------|----------|--------|---------|--------|
| brick_wall.jpg | brick_wall | Tomwsulcer | CC0 | File:Surfaces_brick_wall_closeup_view_with_some_bricks_jutting_out.JPG |
| stone_wall.jpg | stone_wall | Acabashi | CC BY-SA 4.0 | File:Broadwell_stone_wall_texture_West_Oxfordshire_England.jpg |
| foliage.jpg | foliage | Undeka 11 | CC BY-SA 4.0 | File:Fresh_Green_Peperomia_Pellucida_Sirih_Cina_Leaves_Macro_Nature_Background.jpg |
| lake_water.jpg | lake_water | Pseudopanax at English Wikipedia | Public domain | File:Calm_Lake_Matheson_with_mist_at_sunrise.jpg |
| fabric.jpg | fabric | Pink Sherbet Photography | CC BY 2.0 | File:Blue_Denim_Fabric_Texture_Free_Creative_Commons_(6816223272).jpg |
| woodgrain.jpg | woodgrain | Vijayanrajapuram | CC BY-SA 4.0 | File:Growth_Rings_tree_rings_01.jpg |
| treebark.jpg | treebark | Bob Harvey | CC BY-SA 2.0 | File:Bark_of_an_Oak_tree_-_geograph.org.uk_-_7235881.jpg |
| portrait.jpg | portrait | Jamshid Nurkulov | CC BY-SA 4.0 | File:A_portrait_of_an_old_man_of_Bukhara.jpg |
| car.jpg | car | Suzanne Mischyshyn | CC BY-SA 2.0 | File:Bunratty_Folk_Park_-_The_Village_Street_-_Classic_Car_402_YUB_-_Front_-_geograph.org.uk_-_3115932.jpg |
| building.jpg | building | Юрий Д.К. | CC BY 4.0 | File:Moscow_-_2025_-_Details_of_the_facade_of_the_Historical_Museum1.jpg |
| cat.jpg | cat | Georgios Liakopoulos | CC BY-SA 3.0 | File:Cat_Portrait_(200194163).jpeg |
| market.jpg | market | Steve Browne & John Verkleir | CC BY 2.0 | File:Corner_Market,_Calcutta_-_Nov_2010.jpg |

## Seal verification

SEALCHECK.txt: 0 SHA-256 hits, 0 Commons source-title hits vs the 9 sealed
test photos. Filename overlap (8 categories) is expected by design (same
category names, different photos) and is NOT a leak.

## Teaching

BMPs converted deterministically (PIL, 24-bit). Teaching via azteach2.zag:
caps 96/96/64/48 (S=64/32/16/8), thin 64. vocab_new.bin SHA-256:
51c67ed32b422c29422acbb84a1e75e6a4341549bd7ef94533b5ca1ec364fba0.
Byte-identical across 3 runs.
