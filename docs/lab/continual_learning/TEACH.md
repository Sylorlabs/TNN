# TEACH.md — Frozen teaching manifest

Source texts fetched 2026-09-27 (Project Gutenberg). SHA-256:

| File | SHA-256 |
|---|---|
| `build/sources/vol1_56989.txt` | `40023207dd8e7a1c1191ece7e02f7bb35f74a4acc427fe3d9aee2289e013b4e6` |
| `build/sources/vol2_57191.txt` | `542692a64668e275648070d74dd1a3a14233cedcfd6cbd02296c2fd38f766df1` |
| `build/sources/orchestra_73991.txt` | `910156ec09c30ac646494a6de960d7c55242ce7e3b575d10bf63d62eedc0bec1` |
| `build/sources/vol4_72279.txt` | `9c7414600d59dae3093821b54dec42a13294fd16c24cd6744b639ea1e5698718` |

Source SHAs recorded from the fetched bytes on 2026-09-27. The four
`.txt` files themselves are NOT committed (regenerable downloads); the
frozen fixtures derived from them ARE committed (see MANIFEST.md).

## Frozen-prereg / source mismatches

PREREG.md is frozen (2026-09-27, commit
`8c22ffb9bbde02c4dae1fc59ac73068509742696`) and untouched. The fixture
texts follow the prereg verbatim. Where the prereg's transcription
differs from the Gutenberg source bytes, the difference is disclosed
here; the prereg text is kept as the authority for teaching/scoring:

- D1: source has `catgut[8]`; prereg omits the `[8]` marker.
- D2: source has `_breath_`, `_touch_`; prereg strips underscores.
- E2: source has `_immediate ancestor_`, `_viola da gamba_`; prereg strips underscores.
- F3: source has `_arpa_`, `_arpeggios_`; prereg strips underscores.
- P4-I1: source has `_touch_`; prereg strips underscores.
- P4-I2: normalizes case/curly quotes; abridges intervening words with an ellipsis.
- P4-B2: the ellipsis replaces `, bit every one within reach of its powerful bill, and refused food of all kinds.`

## The 18 teaching facts (prereg §3, verbatim)

| # | Episode | Concept | Section | Source | Fact |
|---|---|---|---|---|---|
| 1 | EP-P1-A1 | A | THE WOOD THRUSH | vol1_56989.txt | composed externally of dry leaves of various kinds, with a second bed of grasses and mud, and an internal layer of fine fibrous roots |
| 2 | EP-P1-A2 | A | THE WOOD THRUSH | vol1_56989.txt | The eggs are four or five, of a beautiful uniform light blue. |
| 3 | EP-P1-A3 | A | THE WOOD THRUSH | vol1_56989.txt | Their food consists of different kinds of berries and small fruits, which they procure in the woods, without ever interfering with the farmer. |
| 4 | EP-P1-B1 | B | THE HERMIT THRUSH | vol1_56989.txt | The flight of the Hermit Thrush is performed low over the ground, and in a gliding manner |
| 5 | EP-P1-B2 | B | THE HERMIT THRUSH | vol1_56989.txt | The Hermit Thrush has no song, and only utters a soft plaintive note, seldom heard at a greater distance than twenty-five or thirty yards. |
| 6 | EP-P1-B3 | B | THE HERMIT THRUSH | vol1_56989.txt | They were smaller, and had no mud or plaster of any kind |
| 7 | EP-P1-C1 | C | THE TAWNY THRUSH | vol2_57191.txt | composed of continued trills repeated with different variations, enunciated with great delicacy and mellowness |
| 8 | EP-P1-C2 | C | THE TAWNY THRUSH | vol2_57191.txt | builds its nest, which is large, composed externally of dry leaves, mosses, and the stalks of grasses, and lined with finer grasses, and delicate fibrous portions of different kinds of mosses, without any mud or clay |
| 9 | EP-P1-C3 | C | THE TAWNY THRUSH | vol2_57191.txt | feeds principally on coleopterous insects |
| 10 | EP-P2-D1 | D | THE VIOLIN | orchestra_73991.txt | The four strings—G, D, A, and E—are made of catgut and the lowest—the G—is wound with silver. |
| 11 | EP-P2-D2 | D | THE VIOLIN | orchestra_73991.txt | The bowing of a violinist is what breath is to a singer and what touch is to a pianist. |
| 12 | EP-P2-D3 | D | THE VIOLIN | orchestra_73991.txt | The violin is tuned in fifths. |
| 13 | EP-P2-E1 | E | THE VIOLONCELLO | orchestra_73991.txt | The violoncello is not a big violin; it is a little double-bass |
| 14 | EP-P2-E2 | E | THE VIOLONCELLO | orchestra_73991.txt | Its immediate ancestor was the viola da gamba. |
| 15 | EP-P2-E3 | E | THE VIOLONCELLO | orchestra_73991.txt | The violoncello belongs to that ancient and honorable family of viols |
| 16 | EP-P2-F1 | F | THE HARP | orchestra_73991.txt | The seven pedals with which it is furnished are made so that the player may, by means of each of them, raise at option each string a tone, or a semitone, only. |
| 17 | EP-P2-F2 | F | THE HARP | orchestra_73991.txt | The forty-seven strings are of catgut colored for the convenience of the player. |
| 18 | EP-P2-F3 | F | THE HARP | orchestra_73991.txt | It is even after its Italian name, arpa, that these passages have received the name of arpeggios. |

No Phase-4 text appears above. Phase-4 items are novel by construction
(§4 novelty audit) and were never added or strengthened before verdicts.
