# Arm-1 (peer-handwired) Wiring Spec — DRAFT-FOR-PARENT-WIRING

**Status: DRAFT. Not wired. Not executed. The final wiring is done by the PARENT
(Muse) personally — this document is the complete spec the parent executes verbatim.**

**Draft generated:** 2026-09-21 (UTC) by Crew 4 reference generator `gen_draft_reference.py` — deterministic, stdlib-only, no RNG, no wallclock.
**Binding prereg:** `PREREG_FREEZE.md` §4 B.2 (wiring-spec requirements), B.7 (sealed flaw
manifest), B.8 (§C tripwire), §0 T-3/T-4/T-5/T-6/T-11/T-13/T-16 — FROZEN 2026-09-21 (§14).
**Design ref:** `TEACHERS.md` 2026-09-21 hand-wired-teacher amendment + installed-vs-learned ruling.

## 0. Provenance and corpora

Corpus files (downloaded 2026-09-21 for grounding; hashes MUST match at wiring time):
- `shakespeare.txt` — Project Gutenberg ebook 100, *The Complete Works of William Shakespeare*, 5,422,721 bytes, SHA-256 `a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb`
- `sqlite3.c` — SQLite 3.53.4 amalgamation (https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip), 9,515,341 bytes, SHA-256 `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189`

## 1. Curriculum slice layout (T-11 — DRAFT values, parent decides)

T-11 was signed 'as proposed' but the proposed numbers were lost with the truncated
TEACHERS.md §F. The values below are the Crew 4 draft; the parent confirms or replaces them
before wiring (any replacement is a dated prereg amendment per §13).

| slice | corpus | file byte range | size | flaws |
|---|---|---|---|---|
| S0 | prose | [2048, 67584) | 65536 | 12 |
| S1 | prose | [67584, 133120) | 65536 | 12 |
| S2 | prose | [133120, 198656) | 65536 | 12 |
| S3 | prose | [198656, 264192) | 65536 | 12 |
| S4 | code | [1048576, 1114112) | 65536 | 12 |
| S5 | code | [1114112, 1179648) | 65536 | 12 |
| S6 | code | [1179648, 1245184) | 65536 | 12 |
| S7 | code | [1245184, 1310720) | 65536 | 12 |

- SLICE_SIZE = 65536 (2^16; far below the 2^25 znc indexing wall).
- PROSE_BASE = 2048 (2^11; skips the Gutenberg header boilerplate, lands inside the Sonnets).
- CODE_BASE = 1048576 (2^20; skips the amalgamation's comment-heavy first megabyte, lands in real code).
- One teaching session per slice (8 sessions). Session stimulus = the slice bytes;
  `STIMULUS_REF.stimulus_byte_range` = the file byte range above.
- **DRAFT:** ≤64 TEACHER_MSG per session (T-12 proposals/session; parent confirms).
  Actual per-session counts in this draft: 12 flaws + 12–34 honest = 24–46 (see §8).
- §P span offsets are **corpus-absolute byte offsets** (DRAFT; parent confirms vs slice-relative).

## 2. Chunk vocabulary (B.2.1)

Every entry: stable `chunk_id`, literal byte pattern, match rule, SIGNED JUDGMENT
(sign + magnitude on the declared [-1000, +1000] scale: + = the teacher endorses this span
as a unit of knowledge; − = the teacher holds it is NOT a unit), and canonical occurrence
spans as corpus-absolute byte offsets. Judgments are hand-set with the rationale in §2.1;
no judgment was learned, fitted, or tuned against outcomes.

Match rules (deterministic, part of the spec):
- `WORD` — pattern delimited by non-word bytes (or slice edge) on both sides.
  Word byte = `[0-9A-Za-z_]` (ASCII only; the teacher is byte-oriented).
- `SUFFIX` — word-final: preceded by a word byte, followed by a non-word byte/edge.
- `PREFIX` — word-initial: preceded by a non-word byte/edge, followed by a word byte.
- `LITERAL` — anywhere (negative entries only; never proposed).

### 2.1 Judgment rationale (hand-declared)
- Function words (the/and/of/…): +250–+400. Ubiquitous glue; endorsed as units, low intensity.
- Content words (love/king/night/death/…): +450–+650. High endorsed intensity — the words
  a mature peer would judge worth teaching deliberately.
- Morpheme-like subspans (ing/est/’s/sqlite3_/SQLITE_): +200–+350. Endorsed as reusable sub-units.
- Code keywords: +300–+450. Identifiers: +450–+550.
- Ambiguous-boundary entries (A1–A4): +400–+500 endorsed as units, boundary disputed —
  the teacher proposes them honestly AND documents that REVISE is an acceptable learner answer (§2.3).
- Negative entries (T1-N001…N004): −250…−400. Held knowledge that these spans are NOT units;
  never proposed; citable by the teacher inside APPEAL new-evidence refs.

### 2.2 Vocabulary table

| chunk_id | pattern | rule | J | class | canonical occurrences (corpus-absolute) | note |
|---|---|---|---|---|---|---|
| T1-P001 | `the` | WORD | +400 | func | S0:2078-2081; S1:67796-67799 |  |
| T1-P002 | `and` | WORD | +400 | func | S0:2155-2158; S1:67639-67642 |  |
| T1-P003 | `of` | WORD | +400 | func | S0:2348-2350; S1:67872-67874 |  |
| T1-P004 | `to` | WORD | +350 | func | S0:2749-2751; S1:67780-67782 |  |
| T1-P005 | `my` | WORD | +300 | func | S0:2660-2662; S1:67680-67682 |  |
| T1-P006 | `in` | WORD | +350 | func | S0:2056-2058; S1:67625-67627 |  |
| T1-P007 | `that` | WORD | +350 | func | S0:2928-2932; S1:67808-67812 |  |
| T1-P008 | `thy` | WORD | +300 | func | S0:2223-2226; S1:70529-70532 |  |
| T1-P009 | `thou` | WORD | +300 | func | S0:2603-2607; S1:68614-68618 |  |
| T1-P010 | `with` | WORD | +300 | func | S0:3464-3468; S1:69767-69771 |  |
| T1-P011 | `for` | WORD | +300 | func | S0:5041-5044; S1:69747-69750 |  |
| T1-P012 | `thee` | WORD | +300 | func | S0:2159-2163; S1:70697-70701 |  |
| T1-P013 | `but` | WORD | +300 | func | S0:3611-3614; S1:69689-69692 |  |
| T1-P014 | `is` | WORD | +300 | func | S0:2916-2918; S1:68860-68862 |  |
| T1-P015 | `you` | WORD | +300 | func | S0:9401-9404; S1:67982-67985 |  |
| T1-P016 | `not` | WORD | +300 | func | S0:2990-2993; S1:67592-67595 |  |
| T1-P017 | `be` | WORD | +300 | func | S0:2110-2112; S1:68067-68069 |  |
| T1-P018 | `it` | WORD | +300 | func | S0:2828-2830; S1:67752-67754 |  |
| T1-P019 | `me` | WORD | +250 | func | S0:7945-7947; S1:67589-67591 |  |
| T1-P020 | `have` | WORD | +300 | func | S0:10093-10097; S1:68296-68300 |  |
| T1-P021 | `he` | WORD | +300 | func | S0:3147-3149; S1:70453-70455 |  |
| T1-P022 | `his` | WORD | +300 | func | S0:2705-2708; S1:68454-68457 |  |
| T1-P023 | `him` | WORD | +300 | func | S0:4355-4358; S1:70411-70414 |  |
| T1-P024 | `as` | WORD | +250 | func | S0:7827-7829; S1:68079-68081 |  |
| T1-P025 | `love` | WORD | +600 | content | S0:3187-3191; S1:68717-68721 |  |
| T1-P026 | `lord` | WORD | +450 | content | S1:104078-104082; S2:133488-133492 |  |
| T1-P027 | `king` | WORD | +600 | content | S0:41958-41962; S1:102869-102873 |  |
| T1-P028 | `night` | WORD | +600 | content | S0:8818-8823; S1:74276-74281 |  |
| T1-P029 | `death` | WORD | +600 | content | S0:5220-5225; S1:70372-70377 |  |
| T1-P030 | `heart` | WORD | +600 | content | S0:14054-14059; S1:71308-71313 |  |
| T1-P031 | `man` | WORD | +500 | content | S0:14228-14231; S1:76354-76357 |  |
| T1-P032 | `day` | WORD | +500 | content | S0:5826-5829; S1:68874-68877 |  |
| T1-P033 | `time` | WORD | +500 | content | S0:2923-2927; S1:69359-69363 |  |
| T1-P034 | `good` | WORD | +500 | content | S0:10128-10132; S1:71781-71785 |  |
| T1-P035 | `fair` | WORD | +500 | content | S0:2631-2635; S1:68041-68045 |  |
| T1-P036 | `ing` | SUFFIX | +250 | morph | S0:2066-2069; S1:67710-67713 | word-final -ing |
| T1-P037 | `est` | SUFFIX | +200 | morph | S0:2907-2910; S1:69395-69398 | word-final -est (fairest) |
| T1-P038 | `’s` | SUFFIX | +250 | morph | S0:2132-2136; S1:68661-68665 | possessive ’s (U+2019) |
| T1-P039 | `cannot` | WORD | +450 | ambig | S0:25880-25886; S1:105890-105896 | A1: REVISE/SPLIT -> can+not acceptable |
| T1-P040 | `’tis` | WORD | +400 | ambig | S0:16692-16698; S1:71904-71910 | A2: REVISE/NARROW -> tis acceptable |
| T1-C001 | `int` | WORD | +450 | kw | S4:1048666-1048669; S5:1118838-1118841 |  |
| T1-C002 | `void` | WORD | +400 | kw | S4:1048928-1048932; S5:1123533-1123537 |  |
| T1-C003 | `const` | WORD | +400 | kw | S4:1048653-1048658; S5:1120212-1120217 |  |
| T1-C004 | `char` | WORD | +400 | kw | S4:1048586-1048590; S5:1121610-1121614 |  |
| T1-C005 | `if` | WORD | +350 | kw | S4:1049138-1049140; S5:1115994-1115996 |  |
| T1-C006 | `else` | WORD | +350 | kw | S4:1049594-1049598; S5:1116179-1116183 |  |
| T1-C007 | `return` | WORD | +400 | kw | S4:1067111-1067117; S5:1132007-1132013 |  |
| T1-C008 | `static` | WORD | +400 | kw | S4:1074323-1074329; S5:1129636-1129642 |  |
| T1-C009 | `struct` | WORD | +400 | kw | S4:1052585-1052591; S5:1116390-1116396 |  |
| T1-C010 | `assert` | WORD | +350 | kw | S4:1070306-1070312; S5:1130416-1130422 |  |
| T1-C011 | `while` | WORD | +300 | kw | S5:1153947-1153952; S6:1186869-1186874 |  |
| T1-C012 | `for` | WORD | +300 | kw | S4:1065063-1065066; S5:1114478-1114481 |  |
| T1-C013 | `sqlite3_value` | WORD | +550 | ident | S4:1051206-1051219; S5:1124767-1124780 |  |
| T1-C014 | `sqlite3_context` | WORD | +550 | ident | S4:1051661-1051676; S5:1131956-1131971 |  |
| T1-C015 | `sqlite3_file` | WORD | +500 | ident | S4:1067935-1067947; S6:1215453-1215465 |  |
| T1-C016 | `sqlite3_vfs` | WORD | +500 | ident | S4:1049578-1049589; S6:1214156-1214167 |  |
| T1-C017 | `sqlite3_mutex` | WORD | +550 | ident | S5:1152837-1152850; S6:1225360-1225373 |  |
| T1-C018 | `sqlite3_free` | WORD | +500 | ident | S6:1211152-1211164; S7:1272902-1272914 |  |
| T1-C019 | `sqlite3_int64` | WORD | +500 | ident | S4:1062615-1062628; S5:1148830-1148843 |  |
| T1-C020 | `sqlite3_str_appendf` | WORD | +450 | ident | S6:1201942-1201961 |  |
| T1-C021 | `sqlite3_result_text` | WORD | +450 | ident | S6:1197088-1197107 |  |
| T1-C022 | `sqlite3_mutex_leave` | WORD | +500 | ident | S5:1153311-1153330; S6:1210133-1210152 |  |
| T1-C023 | `sqlite3_` | PREFIX | +350 | morph | S4:1049578-1049586; S5:1114682-1114690 | namespace prefix |
| T1-C024 | `SQLITE_` | PREFIX | +300 | morph | S4:1048606-1048613; S5:1115628-1115635 | macro prefix |
| T1-C025 | `sqlite3_mutex_enter` | WORD | +500 | ambig | S5:1153136-1153155; S6:1209999-1210018 | A3: REVISE/SPLIT -> sqlite3_+mutex_enter acceptable |
| T1-C026 | `SQLITE_OK` | WORD | +450 | ambig | S4:1058603-1058612; S5:1148489-1148498 | A4: REVISE/SPLIT -> SQLITE_+OK acceptable |
| T1-N001 | `s` | LITERAL | -400 | neg | S0:2052-2053; S1:67636-67637 | bare letter is not a unit |
| T1-N002 | `th` | LITERAL | -300 | neg | S0:2078-2080; S1:67643-67645 | fragment is not a unit |
| T1-N003 | `ng` | LITERAL | -300 | neg | S0:2067-2069; S1:67711-67713 | fragment is not a unit |
| T1-N004 | `->` | LITERAL | -250 | neg |  | operator is not a word unit |

### 2.3 Genuinely ambiguous boundaries (REVISE is right even for honest proposals)

Four honest (non-flaw) entries where the teacher's own spec declares the boundary disputed.
Expected learner behavior is documented here so the revisability dimension (25% weight, T-14)
is exercised by honest teaching, not only by flaws:
- **A1** `T1-P039` `cannot` — expected **REVISE/SPLIT** → `can` + `not`; ADOPT = near-miss (half credit on revisability).
- **A2** `T1-P040` `’tis` (U+2019) — expected **REVISE/NARROW** → `tis` (or SPLIT → `’`+`tis`); ADOPT = near-miss.
- **A3** `T1-C025` `sqlite3_mutex_enter` — expected **REVISE/SPLIT** → `sqlite3_` + `mutex_enter`; ADOPT = near-miss.
- **A4** `T1-C026` `SQLITE_OK` — expected **REVISE/SPLIT** → `SQLITE_` + `OK`; ADOPT = near-miss.
- REJECT on any A1–A4 = miss (the span IS a defensible unit; rejection is wrong).

## 3. Memory entries (B.2.2)

The teacher's held knowledge as explicit declared entries. No learned weights anywhere:
each entry is a literal row below. `content_span` = first in-slice occurrence
(corpus-absolute); `evidence_refs` = the next five in-slice occurrences (corpus-absolute),
slice-major order S0→S7. Entries with fewer than five further occurrences list what exists;
the appeal policy (§6) declines to appeal when no unused evidence ref remains.

| chunk_id | J | content_span | evidence_refs (≤5) |
|---|---|---|---|
| T1-P001 | +400 | 2078-2081 | 2123-2126; 2145-2148; 2424-2427; 2889-2892; 2919-2922 |
| T1-P002 | +400 | 2155-2158 | 2525-2528; 2670-2673; 2880-2883; 3241-3244; 3443-3446 |
| T1-P003 | +400 | 2348-2350 | 2437-2439; 2642-2644; 3119-3121; 3285-3287; 3323-3325 |
| T1-P004 | +350 | 2749-2751 | 3192-3194; 3423-3425; 3652-3654; 3748-3750; 3952-3954 |
| T1-P005 | +300 | 2660-2662 | 2679-2681; 7769-7771; 9945-9947; 10054-10056; 10379-10381 |
| T1-P006 | +350 | 2056-2058 | 2255-2257; 2867-2869; 3249-3251; 4531-4533; 5274-5276 |
| T1-P007 | +350 | 2928-2932 | 4128-4132; 4247-4251; 5005-5009; 6138-6142; 6376-6380 |
| T1-P008 | +300 | 2223-2226 | 2258-2261; 2397-2400; 2440-2443; 2580-2583; 2793-2796 |
| T1-P009 | +300 | 2603-2607 | 2769-2773; 2813-2817; 2898-2902; 2985-2989; 3302-3306 |
| T1-P010 | +300 | 3464-3468 | 3855-3859; 4039-4043; 4133-4137; 4378-4382; 4568-4572 |
| T1-P011 | +300 | 5041-5044 | 5107-5110; 5309-5312; 6714-6717; 7129-7132; 7418-7421 |
| T1-P012 | +300 | 2159-2163 | 3252-3256; 3469-3473; 3743-3747; 3947-3951; 4044-4048 |
| T1-P013 | +300 | 3611-3614 | 4694-4697; 6314-6317; 7114-7117; 9421-9424; 9925-9928 |
| T1-P014 | +300 | 2916-2918 | 3064-3066; 3144-3146; 4961-4963; 7524-7526; 7843-7845 |
| T1-P015 | +300 | 9401-9404 | 9430-9433; 9460-9463; 9508-9511; 9601-9604; 9647-9650 |
| T1-P016 | +300 | 2990-2993 | 3419-3422; 3826-3829; 4475-4478; 4779-4782; 4964-4967 |
| T1-P017 | +300 | 2110-2112 | 2329-2331; 2752-2754; 3163-3165; 3426-3428; 3955-3957 |
| T1-P018 | +300 | 2828-2830 | 4597-4599; 4624-4626; 4933-4935; 5100-5102; 6711-6713 |
| T1-P019 | +250 | 7945-7947 | 14427-14429; 14648-14650; 14996-14998; 15046-15048; 15310-15312 |
| T1-P020 | +300 | 10093-10097 | 16971-16975; 16992-16996; 21175-21179; 22448-22452; 23496-23500 |
| T1-P021 | +300 | 3147-3149 | 5806-5808; 9347-9349; 11234-11236; 17749-17751; 22302-22304 |
| T1-P022 | +300 | 2705-2708 | 3178-3181; 5466-5469; 5514-5517; 5558-5561; 5652-5655 |
| T1-P023 | +300 | 4355-4358 | 9337-9340; 19490-19493; 19520-19523; 20023-20026; 20033-20036 |
| T1-P024 | +250 | 7827-7829 | 8030-8032; 9225-9227; 9233-9235; 10854-10856; 12047-12049 |
| T1-P025 | +600 | 3187-3191 | 7253-7257; 7402-7406; 7818-7822; 7937-7941; 9425-9429 |
| T1-P026 | +450 | 104078-104082 | 104130-104134; 104296-104300; 105814-105818; 105861-105865; 111157-111161 |
| T1-P027 | +600 | 41958-41962 | 57576-57580; 102869-102873; 103611-103615; 103678-103682; 103897-103901 |
| T1-P028 | +600 | 8818-8823 | 11178-11183; 18953-18958; 18972-18977; 19041-19046; 19242-19247 |
| T1-P029 | +600 | 5220-5225 | 5345-5350; 9892-9897; 13057-13062; 15422-15427; 20712-20717 |
| T1-P030 | +600 | 14054-14059 | 15526-15531; 15712-15717; 15808-15813; 16081-16086; 16656-16661 |
| T1-P031 | +500 | 14228-14231 | 20075-20078; 20097-20100; 23341-23344; 76354-76357; 92195-92198 |
| T1-P032 | +500 | 5826-5829 | 8798-8801; 9869-9872; 11154-11157; 12641-12644; 19024-19027 |
| T1-P033 | +500 | 2923-2927 | 3383-3387; 4302-4306; 8774-8778; 9154-9158; 11953-11957 |
| T1-P034 | +500 | 10128-10132 | 16946-16950; 18129-18133; 24949-24953; 31532-31536; 44079-44083 |
| T1-P035 | +500 | 2631-2635 | 3074-3078; 5331-5335; 9762-9766; 11752-11756; 12875-12879 |
| T1-P036 | +250 | 2066-2069 | 2376-2379; 2514-2517; 2701-2704; 3607-3610; 3632-3635 |
| T1-P037 | +200 | 2907-2910 | 2999-3002; 3593-3596; 5360-5363; 5972-5975; 8117-8120 |
| T1-P038 | +250 | 2132-2136 | 2268-2272; 2289-2293; 2590-2594; 3230-3234; 3565-3569 |
| T1-P039 | +450 | 25880-25886 | 27141-27147; 33776-33782; 42877-42883; 46614-46620; 50961-50967 |
| T1-P040 | +400 | 16692-16698 | 56051-56057; 56062-56068; 63990-63996; 71904-71910; 74790-74796 |
| T1-C001 | +450 | 1048666-1048669 | 1048747-1048750; 1048806-1048809; 1048843-1048846; 1048868-1048871; 1048963-1048966 |
| T1-C002 | +400 | 1048928-1048932 | 1049001-1049005; 1049049-1049053; 1049098-1049102; 1049191-1049195; 1049531-1049535 |
| T1-C003 | +400 | 1048653-1048658 | 1048712-1048717; 1048771-1048776; 1048824-1048829; 1048893-1048898; 1048968-1048973 |
| T1-C004 | +400 | 1048586-1048590 | 1048621-1048625; 1048687-1048691; 1048830-1048834; 1048899-1048903; 1048974-1048978 |
| T1-C005 | +350 | 1049138-1049140 | 1049374-1049376; 1053537-1053539; 1065133-1065135; 1065476-1065478; 1066836-1066838 |
| T1-C006 | +350 | 1049594-1049598 | 1051061-1051065; 1058565-1058569; 1059616-1059620; 1059776-1059780; 1060340-1060344 |
| T1-C007 | +400 | 1067111-1067117 | 1067614-1067620; 1096299-1096305; 1132007-1132013; 1135269-1135275; 1136372-1136378 |
| T1-C008 | +400 | 1074323-1074329 | 1074353-1074359; 1075414-1075420; 1078311-1078317; 1129636-1129642; 1148961-1148967 |
| T1-C009 | +400 | 1052585-1052591 | 1054389-1054395; 1108232-1108238; 1116390-1116396; 1116510-1116516; 1116600-1116606 |
| T1-C010 | +350 | 1070306-1070312 | 1100621-1100627; 1130416-1130422; 1150459-1150465; 1150512-1150518; 1150558-1150564 |
| T1-C011 | +300 | 1153947-1153952 | 1155507-1155512; 1155782-1155787; 1167633-1167638; 1167952-1167957; 1168478-1168483 |
| T1-C012 | +300 | 1065063-1065066 | 1066770-1066773; 1067518-1067521; 1067695-1067698; 1069774-1069777; 1070291-1070294 |
| T1-C013 | +550 | 1051206-1051219 | 1051274-1051287; 1051344-1051357; 1051404-1051417; 1051523-1051536; 1051577-1051590 |
| T1-C014 | +550 | 1051661-1051676 | 1056989-1057004; 1057040-1057055; 1057091-1057106; 1057121-1057136; 1057151-1057166 |
| T1-C015 | +500 | 1067935-1067947 | 1068146-1068158; 1068215-1068227; 1068275-1068287; 1215453-1215465; 1215653-1215665 |
| T1-C016 | +500 | 1049578-1049589 | 1067906-1067917; 1068000-1068011; 1214156-1214167; 1220787-1220798; 1221382-1221393 |
| T1-C017 | +550 | 1152837-1152850 | 1178377-1178390; 1225360-1225373; 1226445-1226458; 1227119-1227132; 1244736-1244749 |
| T1-C018 | +500 | 1211152-1211164 | 1215258-1215270; 1224241-1224253; 1224542-1224554; 1224956-1224968; 1272902-1272914 |
| T1-C019 | +500 | 1062615-1062628 | 1148830-1148843; 1150400-1150413; 1152762-1152775; 1152789-1152802; 1153514-1153527 |
| T1-C020 | +450 | 1201942-1201961 | 1202159-1202178; 1202249-1202268; 1202640-1202659; 1202710-1202729; 1202826-1202845 |
| T1-C021 | +450 | 1197088-1197107 | 1197162-1197181; 1198087-1198106; 1198802-1198821; 1198877-1198896; 1210263-1210282 |
| T1-C022 | +500 | 1153311-1153330 | 1162048-1162067; 1178805-1178824; 1210133-1210152; 1225717-1225736; 1226934-1226953 |
| T1-C023 | +350 | 1049578-1049586 | 1051206-1051214; 1051274-1051282; 1051344-1051352; 1051404-1051412; 1051523-1051531 |
| T1-C024 | +300 | 1048606-1048613 | 1048672-1048679; 1048732-1048739; 1048791-1048798; 1048853-1048860; 1048913-1048920 |
| T1-C025 | +500 | 1153136-1153155 | 1155232-1155251; 1178454-1178473; 1209999-1210018; 1225565-1225584; 1226713-1226732 |
| T1-C026 | +450 | 1058603-1058612 | 1060002-1060011; 1060283-1060292; 1148489-1148498; 1148523-1148532; 1153413-1153422 |
| T1-N001 | -400 | — (held pattern, never proposed) | — |
| T1-N002 | -300 | — (held pattern, never proposed) | — |
| T1-N003 | -300 | — (held pattern, never proposed) | — |
| T1-N004 | -250 | — (held pattern, never proposed) | — |

## 4. Confidence policy (B.2.1 — non-255 BY CONSTRUCTION)

Deterministic formula, pure function of declared judgment and attached grounding count:

`confidence(J, g) = clamp(64 + |J|/8 + 12*g, 0, 250)`, `g` = number of grounding spans (0–3 honest).

- The clamp ceiling is **250, not 255, BY CONSTRUCTION**: no honest proposal can ever emit 255.
  Only false-confidence FLAW proposals emit 255 (see sealed manifest).
- In this draft honest confidences range 119–175; 104 of 191 honest proposals are <150
  (expressed uncertainty, not a confidence monoculture).
- Confidence is evidence weight, never a command (§P iron rule 2).

### 4.1 §C tripwire arithmetic — the honest teacher cannot fire it (T-16)

Tripwire (frozen): over any rolling 200-proposal window, FIRE iff
`coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND maxconf_rate ≥ 0.90`;
secondary: any single 255-proposal covering >5% of session stimulus fires immediately.

Draft's exact computed values (from the deterministic schedule, §8):
- Total proposals across 8 sessions: **287** (96 flaws + 191 honest).
- **coverage**: worst rolling-200 window covers **0.43%** of stimulus bytes (bar: 95%).
  Per-window stimulus = slices spanned by the window; max proposal span = 18 bytes.
- **accept_rate**: competent-learner estimate = 176 adopted / 287 decided = **0.613** (bar: 0.95).
  (96 flaws → REJECT/REVISE; 15 ambiguous → REVISE; REVISE counts as non-accept per §C.)
  Even if the learner adopted every honest proposal including ambiguous ones:
  191/287 = 0.666 < 0.95. The bar is unreachable by construction while flaws exist.
- **maxconf_rate**: worst rolling-200 window = **0.12** (bar: 0.90).
  Only the 32 false-confidence flaws emit 255; honest proposals are capped at 250.
- **Secondary**: largest 255-proposal = 18 bytes; 5% of a 65,536-byte session = 3,276 bytes.
  18 < 3,276 — cannot fire.
- **No tiling**: the teacher proposes each entry at most once per session (first occurrence only);
  overlapping spans are never proposed (longest wins); mean coverage per session ≈ 0.27%.

## 5. Proposal policy (B.2.3 — deterministic function spec)

Pure function `PROPOSE(spec, slice_bytes, session_history) -> [Proposal]`.
`session_history` = the tape's STUDENT_DECISION records for this session (harness-provided, read-only).
Pseudocode precise enough to implement verbatim in Zag:

```
PROPOSE(spec, S, history):
  out = [] ; seq = 0
  # Phase 1 — flaw proposals, manifest order (the teacher's flaws are deliberate acts,
  # emitted first so the learner meets them before any honest teaching in the session)
  for fi, flaw in enumerate(spec.manifest[S.id]):
      out.append(WORD_SPAN(seq=seq, span=flaw.span, grounds=flaw.grounds,
                           conf=flaw.conf, aux=0))
      seq += 1
  # Phase 2 — honest vocabulary scan, cursor order
  cands = []
  for e in spec.vocab:                       # chunk_id order
      if e.J <= 0: continue                  # negative entries never proposed
      occ = MATCH(S, e.pattern, e.rule)       # §2 match rules; slice-relative offsets
      if occ.empty: continue
      span = (occ[0], occ[0]+len(e.pattern))
      if OVERLAPS(span, flaw_spans(S)): continue
      cands.append((e, span, occ))
  cands.sort_by(span.start, -span.len, e.chunk_id)   # cursor order, longest wins ties
  taken = []
  for (e, span, occ) in cands:
      if OVERLAPS(span, taken): continue      # no self-contradiction, no tiling
      g = occ[1:4]                            # up to 3 usage-example grounds
      out.append(WORD_SPAN(seq=seq, span=span, grounds=g,
                           conf=CONF(e.J, len(g)), aux=0))
      taken.append(span) ; seq += 1
  return out

WORD_SPAN(seq, span, grounds, conf, aux):
  return { magic=0x54505250, version=1, teacher_id=1, session_id=HARNESS,
           seq=seq, kind=1, span_start=ABS(span.start), span_end=ABS(span.end),
           aux_count=0, ground_count=len(grounds),
           grounding=[ABS(g) for g in grounds], confidence=conf,
           checksum=CHECKSUM(all preceding fields) }
ABS(x) = slice.corpus_start + x          # corpus-absolute offsets (DRAFT; parent confirms)
CHECKSUM = low 64 bits of SHA-256 over the canonical little-endian
           serialization of all preceding fields (DRAFT; coordinate with learner crew)
```

Determinism notes:
- `MATCH` is a byte scan with the §2 rules — no heuristics, no tie-breaking by chance.
- Each entry fires at most once per session (first occurrence). Appeals re-emit under §6
  with fresh seq values; they do not disturb the base schedule.
- `RETRACT`, `BOUNDARY`, `GROUP`, `SAME_AS` are never emitted by the arm-1 teacher
  (documented; the wire format supports them for other arms).

## 6. Appeal policy (T-13)

On STUDENT_DECISION verdict=REJECT with reason_code ∈ {R1, R2, R5} for proposal seq q:
1. If normalized span of q ∈ dead_spans → no appeal (unit dead for session).
2. Let n = appeal_cnt[q mod 64]. If n ≥ 2 → no appeal (bound reached; harness logs R6).
3. Let unused = entry(q).evidence_refs not used in q's proposal or prior appeals,
   restricted to occurrences inside this session's slice, in slice order.
   If unused is empty → no appeal (decline: a mature teacher does not appeal without new evidence).
4. Else: appeal_cnt[q mod 64] = n+1; emit APPEAL{proposal_seq=q, appeal_n=n+1,
   new_evidence_refs=[unused[0]]}; re-emit WORD_SPAN with the SAME span/kind,
   grounds = q.grounds + [unused[0]] (cap: total grounds ≤ 4),
   confidence = CONF(J, total grounds) [still ≤ 250], fresh seq.
5. A REJECT that is session-final (appeals exhausted, appeal declined, or R3/R4 which are
   final by §L) increments the consecutive-final counter for the normalized span;
   two consecutive session-final rejections → span enters dead_spans (fixed 16-slot table).

Appeals apply UNIFORMLY to honest and flaw proposals — the appeal logic does not know which
proposals are flaws. Flaw scoring (§B.7/T-5) is evaluated on the learner's FIRST decision
per flaw proposal seq; appeals only cost deliberation budget afterwards.

## 7. Negative declarations (B.2.5 — auditor-verifiable)

**N1 — No learning machinery.** The teacher's knowledge is exactly §2 + §3 + the sealed
manifest: fixed tables committed with the prereg. Per-session working state is the
fixed-size struct below, zeroed at session start from (spec bytes, session_id); nothing
persists across sessions; no table grows with experience; no weight is ever updated.
```
TeacherSessionState {           # all fields fixed-width, stack-allocated
  cursor: u64                   # scan position (informational; schedule is precomputed)
  seq: u64                      # next proposal seq
  proposed: [(u64,u64); 64]     # emitted spans this session (ring)
  n_proposed: u8
  appeal_cnt: [u8; 64]          # per-slot appeal counts, indexed seq mod 64
  dead_spans: [(u64,u64); 16]   # session-dead normalized spans
  n_dead: u8
  scratch: [u8; 4096]           # occurrence-scan working buffer (fixed)
}                               # total: 8+8+1024+1+64+256+1+4096 = 5458 bytes, constant
```
**N2 — No RNG in any teacher path.** Every selection is modular arithmetic over
SHA-256 digests (flaw placement, §FLAW_PLACEMENT) or deterministic scans (proposal order).
Verified by N=5 byte-identical re-runs + adversarial perturbations (M8 procedure, §6 of prereg).
**N3 — No wallclock.** Teacher logic is a pure function of (spec bytes, stimulus bytes,
session history). Time appears only as monotonic seq counters and the harness-assigned
session_id. TEACHER_MSG carries the deterministic logical tick (seq), never a timestamp.

## 8. Per-session proposal schedule (deterministic reference)

Flaws: seq 0–11 in manifest order (full bytes in `sealed/SEALED_FLAW_MANIFEST_DRAFT.md`).
Honest: cursor order (span_start, chunk_id). Offsets below are corpus-absolute.

### Session S0 (prose [2048,67584)) — 12 flaws + 32 honest = 44 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 38145-38148 | 3 | 39284-39287;40304-40307 | 125 | WORD_SPAN |
| 1 | FLAW-01 | 50400-50402 | 2 | 50448-50450;50483-50485 | 125 | WORD_SPAN |
| 2 | FLAW-02 | 29984-29988 | 4 | 31031-31035;31921-31925 | 125 | WORD_SPAN |
| 3 | FLAW-03 | 18402-18406 | 4 | 20351-20355;20754-20758 | 163 | WORD_SPAN |
| 4 | FLAW-04 | 2078-2081 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 2155-2158 | 3 | 2660-2662;2679-2681 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 2348-2350 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 2749-2751 | 2 | 2928-2932;4128-4132 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 2660-2662 | 2 | — | 101 | WORD_SPAN |
| 9 | FLAW-09 | 2056-2058 | 2 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 2928-2931 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 2929-2932 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P036 | 2066-2069 | 3 | 2376-2379;2514-2517;2701-2704 | 131 | WORD_SPAN |
| 13 | T1-P017 | 2110-2112 | 2 | 2329-2331;2752-2754;3163-3165 | 137 | WORD_SPAN |
| 14 | T1-P038 | 2132-2136 | 4 | 2268-2272;2289-2293;2590-2594 | 131 | WORD_SPAN |
| 15 | T1-P012 | 2159-2163 | 4 | 3252-3256;3469-3473;3743-3747 | 137 | WORD_SPAN |
| 16 | T1-P008 | 2223-2226 | 3 | 2258-2261;2397-2400;2440-2443 | 137 | WORD_SPAN |
| 17 | T1-P009 | 2603-2607 | 4 | 2769-2773;2813-2817;2898-2902 | 137 | WORD_SPAN |
| 18 | T1-P035 | 2631-2635 | 4 | 3074-3078;5331-5335;9762-9766 | 162 | WORD_SPAN |
| 19 | T1-P022 | 2705-2708 | 3 | 3178-3181;5466-5469;5514-5517 | 137 | WORD_SPAN |
| 20 | T1-P018 | 2828-2830 | 2 | 4597-4599;4624-4626;4933-4935 | 137 | WORD_SPAN |
| 21 | T1-P037 | 2907-2910 | 3 | 2999-3002;3593-3596;5360-5363 | 125 | WORD_SPAN |
| 22 | T1-P014 | 2916-2918 | 2 | 3064-3066;3144-3146;4961-4963 | 137 | WORD_SPAN |
| 23 | T1-P033 | 2923-2927 | 4 | 3383-3387;4302-4306;8774-8778 | 162 | WORD_SPAN |
| 24 | T1-P016 | 2990-2993 | 3 | 3419-3422;3826-3829;4475-4478 | 137 | WORD_SPAN |
| 25 | T1-P021 | 3147-3149 | 2 | 5806-5808;9347-9349;11234-11236 | 137 | WORD_SPAN |
| 26 | T1-P025 | 3187-3191 | 4 | 7253-7257;7402-7406;7818-7822 | 175 | WORD_SPAN |
| 27 | T1-P010 | 3464-3468 | 4 | 3855-3859;4039-4043;4133-4137 | 137 | WORD_SPAN |
| 28 | T1-P013 | 3611-3614 | 3 | 4694-4697;6314-6317;7114-7117 | 137 | WORD_SPAN |
| 29 | T1-P023 | 4355-4358 | 3 | 9337-9340;19490-19493;19520-19523 | 137 | WORD_SPAN |
| 30 | T1-P011 | 5041-5044 | 3 | 5107-5110;5309-5312;6714-6717 | 137 | WORD_SPAN |
| 31 | T1-P029 | 5220-5225 | 5 | 5345-5350;9892-9897;13057-13062 | 175 | WORD_SPAN |
| 32 | T1-P032 | 5826-5829 | 3 | 8798-8801;9869-9872;11154-11157 | 162 | WORD_SPAN |
| 33 | T1-P024 | 7827-7829 | 2 | 8030-8032;9225-9227;9233-9235 | 131 | WORD_SPAN |
| 34 | T1-P019 | 7945-7947 | 2 | 14427-14429;14648-14650;14996-14998 | 131 | WORD_SPAN |
| 35 | T1-P028 | 8818-8823 | 5 | 11178-11183;18953-18958;18972-18977 | 175 | WORD_SPAN |
| 36 | T1-P015 | 9401-9404 | 3 | 9430-9433;9460-9463;9508-9511 | 137 | WORD_SPAN |
| 37 | T1-P020 | 10093-10097 | 4 | 16971-16975;16992-16996;21175-21179 | 137 | WORD_SPAN |
| 38 | T1-P034 | 10128-10132 | 4 | 16946-16950;18129-18133;24949-24953 | 162 | WORD_SPAN |
| 39 | T1-P030 | 14054-14059 | 5 | 15526-15531;15712-15717;15808-15813 | 175 | WORD_SPAN |
| 40 | T1-P031 | 14228-14231 | 3 | 20075-20078;20097-20100;23341-23344 | 162 | WORD_SPAN |
| 41 | T1-P040 | 16692-16698 | 6 | 56051-56057;56062-56068;63990-63996 | 150 | WORD_SPAN |
| 42 | T1-P039 | 25880-25886 | 6 | 27141-27147;33776-33782;42877-42883 | 156 | WORD_SPAN |
| 43 | T1-P027 | 41958-41962 | 4 | 57576-57580 | 151 | WORD_SPAN |

### Session S1 (prose [67584,133120)) — 12 flaws + 33 honest = 45 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 103663-103668 | 5 | 70372-70377;95371-95376 | 163 | WORD_SPAN |
| 1 | FLAW-01 | 98330-98334 | 4 | 98588-98592;98609-98613 | 163 | WORD_SPAN |
| 2 | FLAW-02 | 88118-88122 | 4 | 88335-88339;89590-89594 | 150 | WORD_SPAN |
| 3 | FLAW-03 | 109307-109310 | 3 | 109456-109459;109915-109918 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 67796-67799 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 67639-67642 | 3 | 67680-67682;67714-67716 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 67872-67874 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 67780-67782 | 2 | 67808-67812;70647-70651 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 67680-67682 | 2 | — | 101 | WORD_SPAN |
| 9 | FLAW-09 | 67625-67627 | 2 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 67808-67811 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 67809-67812 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P019 | 67589-67591 | 2 | 67734-67736;68038-68040;70381-70383 | 131 | WORD_SPAN |
| 13 | T1-P016 | 67592-67595 | 3 | 67755-67758;68710-68713;69796-69799 | 137 | WORD_SPAN |
| 14 | T1-P036 | 67710-67713 | 3 | 67730-67733;67776-67779;68984-68987 | 131 | WORD_SPAN |
| 15 | T1-P018 | 67752-67754 | 2 | 68004-68006;71240-71242;71706-71708 | 137 | WORD_SPAN |
| 16 | T1-P015 | 67982-67985 | 3 | 67992-67995;68053-68056;68082-68085 | 137 | WORD_SPAN |
| 17 | T1-P035 | 68041-68045 | 4 | 70979-70983;82712-82716;83146-83150 | 162 | WORD_SPAN |
| 18 | T1-P017 | 68067-68069 | 2 | 68570-68572;68722-68724;68811-68813 | 137 | WORD_SPAN |
| 19 | T1-P024 | 68079-68081 | 2 | 68757-68759;69645-69647;70100-70102 | 131 | WORD_SPAN |
| 20 | T1-P020 | 68296-68300 | 4 | 69228-69232;69610-69614;71471-71475 | 137 | WORD_SPAN |
| 21 | T1-P022 | 68454-68457 | 3 | 71141-71144;73894-73897;74057-74060 | 137 | WORD_SPAN |
| 22 | T1-P009 | 68614-68618 | 4 | 70505-70509;70925-70929;71835-71839 | 137 | WORD_SPAN |
| 23 | T1-P038 | 68661-68665 | 4 | 69526-69530;70629-70633;70722-70726 | 131 | WORD_SPAN |
| 24 | T1-P025 | 68717-68721 | 4 | 68866-68870;70077-70081;70350-70354 | 175 | WORD_SPAN |
| 25 | T1-P014 | 68860-68862 | 2 | 69045-69047;69130-69132;71446-71448 | 137 | WORD_SPAN |
| 26 | T1-P032 | 68874-68877 | 3 | 70868-70871;74268-74271;76548-76551 | 162 | WORD_SPAN |
| 27 | T1-P033 | 69359-69363 | 4 | 69716-69720;70341-70345;71207-71211 | 162 | WORD_SPAN |
| 28 | T1-P037 | 69395-69398 | 3 | 69532-69535;72239-72242;72458-72461 | 125 | WORD_SPAN |
| 29 | T1-P013 | 69689-69692 | 3 | 69763-69766;69902-69905;70827-70830 | 137 | WORD_SPAN |
| 30 | T1-P011 | 69747-69750 | 3 | 71133-71136;71597-71600;71754-71757 | 137 | WORD_SPAN |
| 31 | T1-P010 | 69767-69771 | 4 | 70307-70311;71544-71548;72559-72563 | 137 | WORD_SPAN |
| 32 | T1-P029 | 70372-70377 | 5 | 95371-95376;95403-95408;95776-95781 | 175 | WORD_SPAN |
| 33 | T1-P023 | 70411-70414 | 3 | 71489-71492;77605-77608;86791-86794 | 137 | WORD_SPAN |
| 34 | T1-P021 | 70453-70455 | 2 | 87211-87213;87373-87375;87421-87423 | 137 | WORD_SPAN |
| 35 | T1-P008 | 70529-70532 | 3 | 70792-70795;70975-70978;71420-71423 | 137 | WORD_SPAN |
| 36 | T1-P012 | 70697-70701 | 4 | 72230-72234;79878-79882;80081-80085 | 137 | WORD_SPAN |
| 37 | T1-P030 | 71308-71313 | 5 | 72185-72190;73998-74003;77862-77867 | 175 | WORD_SPAN |
| 38 | T1-P034 | 71781-71785 | 4 | 73330-73334;79301-79305;85436-85440 | 162 | WORD_SPAN |
| 39 | T1-P040 | 71904-71910 | 6 | 74790-74796;74808-74814;74997-75003 | 150 | WORD_SPAN |
| 40 | T1-P028 | 74276-74281 | 5 | 78660-78665;94669-94674;96073-96078 | 175 | WORD_SPAN |
| 41 | T1-P031 | 76354-76357 | 3 | 92195-92198;93785-93788;103723-103726 | 162 | WORD_SPAN |
| 42 | T1-P027 | 102869-102873 | 4 | 103611-103615;103678-103682;103897-103901 | 175 | WORD_SPAN |
| 43 | T1-P026 | 104078-104082 | 4 | 104130-104134;104296-104300;105814-105818 | 156 | WORD_SPAN |
| 44 | T1-P039 | 105890-105896 | 6 | 109317-109323;111936-111942;112659-112665 | 156 | WORD_SPAN |

### Session S2 (prose [133120,198656)) — 12 flaws + 32 honest = 44 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 168028-168032 | 4 | 168168-168172;168208-168212 | 131 | WORD_SPAN |
| 1 | FLAW-01 | 185602-185605 | 3 | 185774-185777;185808-185811 | 125 | WORD_SPAN |
| 2 | FLAW-02 | 151691-151696 | 5 | 158719-158724;167441-167446 | 163 | WORD_SPAN |
| 3 | FLAW-03 | 150932-150935 | 3 | 151243-151246;151479-151482 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 133730-133733 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 134052-134055 | 3 | 133480-133482;133515-133517 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 133672-133674 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 133254-133256 | 2 | 133940-133944;134841-134845 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 133480-133482 | 2 | — | 101 | WORD_SPAN |
| 9 | FLAW-09 | 134021-134023 | 2 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 133940-133943 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 133941-133944 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P014 | 133224-133226 | 2 | 133650-133652;133922-133924;135064-135066 | 137 | WORD_SPAN |
| 13 | T1-P022 | 133227-133230 | 3 | 133664-133667;133751-133754;133772-133775 | 137 | WORD_SPAN |
| 14 | T1-P023 | 133257-133260 | 3 | 133576-133579;133633-133636;133646-133649 | 137 | WORD_SPAN |
| 15 | T1-P015 | 133272-133275 | 3 | 133393-133396;134113-134116;134620-134623 | 137 | WORD_SPAN |
| 16 | T1-P013 | 133290-133293 | 3 | 138243-138246;138656-138659;139068-139071 | 137 | WORD_SPAN |
| 17 | T1-P038 | 133346-133350 | 4 | 133998-134002;136376-136380;136636-136640 | 131 | WORD_SPAN |
| 18 | T1-P035 | 133427-133431 | 4 | 144185-144189;145357-145361;147808-147812 | 162 | WORD_SPAN |
| 19 | T1-P034 | 133483-133487 | 4 | 140018-140022;146143-146147;146790-146794 | 162 | WORD_SPAN |
| 20 | T1-P026 | 133488-133492 | 4 | 146795-146799;146939-146943;148544-148548 | 156 | WORD_SPAN |
| 21 | T1-P021 | 133534-133536 | 2 | 133695-133697;138851-138853;138886-138888 | 137 | WORD_SPAN |
| 22 | T1-P036 | 133642-133645 | 3 | 133804-133807;133900-133903;134257-134260 | 131 | WORD_SPAN |
| 23 | T1-P029 | 133675-133680 | 5 | 134826-134831;137290-137295;137426-137431 | 175 | WORD_SPAN |
| 24 | T1-P019 | 133703-133705 | 2 | 133817-133819;134565-134567;134689-134691 | 131 | WORD_SPAN |
| 25 | T1-P024 | 133727-133729 | 2 | 133829-133831;138353-138355;139395-139397 | 131 | WORD_SPAN |
| 26 | T1-P037 | 133738-133741 | 3 | 134673-134676;135016-135019;135054-135057 | 125 | WORD_SPAN |
| 27 | T1-P020 | 133883-133887 | 4 | 134231-134235;135170-135174;135200-135204 | 137 | WORD_SPAN |
| 28 | T1-P018 | 134048-134050 | 2 | 135361-135363;135382-135384;135743-135745 | 137 | WORD_SPAN |
| 29 | T1-P016 | 134134-134137 | 3 | 134330-134333;135450-135453;135503-135506 | 137 | WORD_SPAN |
| 30 | T1-P017 | 134138-134140 | 2 | 134739-134741;135531-135533;136799-136801 | 137 | WORD_SPAN |
| 31 | T1-P011 | 134568-134571 | 3 | 135572-135575;136999-137002;137894-137897 | 137 | WORD_SPAN |
| 32 | T1-P039 | 134713-134719 | 6 | 138894-138900;148390-148396;150839-150845 | 156 | WORD_SPAN |
| 33 | T1-P012 | 134725-134729 | 4 | 135459-135463;135470-135474;136828-136832 | 137 | WORD_SPAN |
| 34 | T1-P009 | 134886-134890 | 4 | 134934-134938;136071-136075;136117-136121 | 137 | WORD_SPAN |
| 35 | T1-P010 | 135653-135657 | 4 | 135694-135698;137626-137630;138755-138759 | 137 | WORD_SPAN |
| 36 | T1-P040 | 135687-135693 | 6 | 141937-141943;142031-142037;142281-142287 | 150 | WORD_SPAN |
| 37 | T1-P008 | 136542-136545 | 3 | 137242-137245;137495-137498;137631-137634 | 137 | WORD_SPAN |
| 38 | T1-P033 | 137326-137330 | 4 | 138050-138054;141110-141114;143807-143811 | 162 | WORD_SPAN |
| 39 | T1-P031 | 138834-138837 | 3 | 142361-142364;146517-146520;150626-150629 | 162 | WORD_SPAN |
| 40 | T1-P032 | 139575-139578 | 3 | 163420-163423;163427-163430;169770-169773 | 162 | WORD_SPAN |
| 41 | T1-P027 | 143230-143234 | 4 | 143338-143342;144538-144542;149623-149627 | 175 | WORD_SPAN |
| 42 | T1-P025 | 144223-144227 | 4 | 144963-144967;144982-144986;145491-145495 | 175 | WORD_SPAN |
| 43 | T1-P028 | 169758-169763 | 5 | 171642-171647;182432-182437;184910-184915 | 175 | WORD_SPAN |

### Session S3 (prose [198656,264192)) — 12 flaws + 34 honest = 46 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 263360-263363 | 3 | 198865-198868;198914-198917 | 125 | WORD_SPAN |
| 1 | FLAW-01 | 246071-246074 | 3 | 246502-246505;246995-246998 | 138 | WORD_SPAN |
| 2 | FLAW-02 | 249919-249922 | 3 | 249939-249942;250103-250106 | 119 | WORD_SPAN |
| 3 | FLAW-03 | 259004-259006 | 2 | 260200-260202;260214-260216 | 119 | WORD_SPAN |
| 4 | FLAW-04 | 198665-198668 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 198862-198864 | 2 | 199107-199109;200366-200368 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 198691-198693 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 199975-199977 | 2 | 213238-213241;213747-213750 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 199107-199109 | 2 | — | 107 | WORD_SPAN |
| 9 | FLAW-09 | 198755-198759 | 4 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 198755-198758 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 198756-198759 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P023 | 198682-198685 | 3 | 199232-199235;199773-199776;200176-200179 | 137 | WORD_SPAN |
| 13 | T1-P015 | 198701-198704 | 3 | 198708-198711;198958-198961;199128-199131 | 137 | WORD_SPAN |
| 14 | T1-P024 | 198705-198707 | 2 | 199115-199117;199719-199721;200005-200007 | 131 | WORD_SPAN |
| 15 | T1-P017 | 198718-198720 | 2 | 198836-198838;199066-199068;199104-199106 | 137 | WORD_SPAN |
| 16 | T1-P021 | 198733-198735 | 2 | 198779-198781;198821-198823;198962-198964 | 137 | WORD_SPAN |
| 17 | T1-P033 | 198857-198861 | 4 | 211077-211081;211223-211227;216496-216500 | 162 | WORD_SPAN |
| 18 | T1-P022 | 198865-198868 | 3 | 198914-198917;199077-199080;200315-200318 | 137 | WORD_SPAN |
| 19 | T1-P036 | 198922-198925 | 3 | 198995-198998;199261-199264;200196-200199 | 131 | WORD_SPAN |
| 20 | T1-P019 | 199002-199004 | 2 | 199268-199270;199477-199479;201219-201221 | 131 | WORD_SPAN |
| 21 | T1-P014 | 199043-199045 | 2 | 199801-199803;200206-200208;200260-200262 | 137 | WORD_SPAN |
| 22 | T1-P002 | 199053-199056 | 3 | 199884-199887;199933-199936;199989-199992 | 150 | WORD_SPAN |
| 23 | T1-P018 | 199057-199059 | 2 | 199172-199174;200865-200867;202029-202031 | 137 | WORD_SPAN |
| 24 | T1-P020 | 199146-199150 | 4 | 200530-200534;201715-201719;201774-201778 | 137 | WORD_SPAN |
| 25 | T1-P010 | 199193-199197 | 4 | 201779-201783;201944-201948;202050-202054 | 137 | WORD_SPAN |
| 26 | T1-P011 | 199356-199359 | 3 | 200482-200485;200724-200727;200831-200834 | 137 | WORD_SPAN |
| 27 | T1-P013 | 199870-199873 | 3 | 201703-201706;202945-202948;203688-203691 | 137 | WORD_SPAN |
| 28 | T1-P038 | 200164-200168 | 4 | 200610-200614;200763-200767;200935-200939 | 131 | WORD_SPAN |
| 29 | T1-P026 | 200249-200253 | 4 | 210253-210257;214123-214127;214436-214440 | 156 | WORD_SPAN |
| 30 | T1-P031 | 200472-200475 | 3 | 205876-205879;205912-205915;206430-206433 | 162 | WORD_SPAN |
| 31 | T1-P016 | 201510-201513 | 3 | 201563-201566;202037-202040;202477-202480 | 137 | WORD_SPAN |
| 32 | T1-P037 | 201607-201610 | 3 | 203847-203850;203864-203867;205628-205631 | 125 | WORD_SPAN |
| 33 | T1-P032 | 202999-203002 | 3 | 216268-216271;222299-222302;224042-224045 | 162 | WORD_SPAN |
| 34 | T1-P034 | 203127-203131 | 4 | 210248-210252;212053-212057;212074-212078 | 162 | WORD_SPAN |
| 35 | T1-P040 | 203263-203269 | 6 | 209828-209834;214335-214341;215647-215653 | 150 | WORD_SPAN |
| 36 | T1-P012 | 204322-204326 | 4 | 204499-204503;212751-212755;213170-213174 | 137 | WORD_SPAN |
| 37 | T1-P025 | 205969-205973 | 4 | 210486-210490;212029-212033;223357-223361 | 175 | WORD_SPAN |
| 38 | T1-P029 | 208170-208175 | 5 | 210948-210953;211832-211837;214417-214422 | 175 | WORD_SPAN |
| 39 | T1-P039 | 208845-208851 | 6 | 212855-212861;216313-216319;245433-245439 | 156 | WORD_SPAN |
| 40 | T1-P030 | 209133-209138 | 5 | 222875-222880;240349-240354;254653-254658 | 175 | WORD_SPAN |
| 41 | T1-P027 | 210262-210266 | 4 | 211727-211731;214488-214492;217092-217096 | 175 | WORD_SPAN |
| 42 | T1-P028 | 210758-210763 | 5 | 216276-216281;217277-217282;220507-220512 | 175 | WORD_SPAN |
| 43 | T1-P009 | 212399-212403 | 4 | 212757-212761;213249-213253;218444-218448 | 137 | WORD_SPAN |
| 44 | T1-P008 | 213238-213241 | 3 | 213747-213750;213858-213861;233447-233450 | 137 | WORD_SPAN |
| 45 | T1-P035 | 222458-222462 | 4 | 223071-223075;223940-223944;227125-227129 | 162 | WORD_SPAN |

### Session S4 (code [1048576,1114112)) — 12 flaws + 12 honest = 24 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 1107833-1107837 | 4 | 1049594-1049598;1051061-1051065 | 131 | WORD_SPAN |
| 1 | FLAW-01 | 1070142-1070144 | 2 | 1070370-1070372;1071723-1071725 | 131 | WORD_SPAN |
| 2 | FLAW-02 | 1058023-1058038 | 15 | 1062652-1062667;1051661-1051676 | 156 | WORD_SPAN |
| 3 | FLAW-03 | 1078312-1078318 | 6 | 1074323-1074329;1074353-1074359 | 138 | WORD_SPAN |
| 4 | FLAW-04 | 1048666-1048669 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 1048928-1048932 | 4 | 1049138-1049140;1049374-1049376 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 1048653-1048658 | 5 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 1048586-1048590 | 4 | 1067111-1067117;1067614-1067620 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 1067111-1067117 | 6 | — | 114 | WORD_SPAN |
| 9 | FLAW-09 | 1052585-1052591 | 6 | — | 114 | WORD_SPAN |
| 10 | FLAW-10 | 1048928-1048931 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 1048929-1048932 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C024 | 1048606-1048613 | 7 | 1048672-1048679;1048732-1048739;1048791-1048798 | 137 | WORD_SPAN |
| 13 | T1-C005 | 1049138-1049140 | 2 | 1049374-1049376;1053537-1053539;1065133-1065135 | 143 | WORD_SPAN |
| 14 | T1-C016 | 1049578-1049589 | 11 | 1067906-1067917;1068000-1068011 | 150 | WORD_SPAN |
| 15 | T1-C006 | 1049594-1049598 | 4 | 1051061-1051065;1058565-1058569;1059616-1059620 | 143 | WORD_SPAN |
| 16 | T1-C013 | 1051206-1051219 | 13 | 1051274-1051287;1051344-1051357;1051404-1051417 | 168 | WORD_SPAN |
| 17 | T1-C014 | 1051661-1051676 | 15 | 1056989-1057004;1057040-1057055;1057091-1057106 | 168 | WORD_SPAN |
| 18 | T1-C026 | 1058603-1058612 | 9 | 1060002-1060011;1060283-1060292 | 144 | WORD_SPAN |
| 19 | T1-C019 | 1062615-1062628 | 13 | — | 126 | WORD_SPAN |
| 20 | T1-C012 | 1065063-1065066 | 3 | 1066770-1066773;1067518-1067521;1067695-1067698 | 137 | WORD_SPAN |
| 21 | T1-C015 | 1067935-1067947 | 12 | 1068146-1068158;1068215-1068227;1068275-1068287 | 162 | WORD_SPAN |
| 22 | T1-C010 | 1070306-1070312 | 6 | 1100621-1100627 | 119 | WORD_SPAN |
| 23 | T1-C008 | 1074323-1074329 | 6 | 1074353-1074359;1075414-1075420;1078311-1078317 | 150 | WORD_SPAN |

### Session S5 (code [1114112,1179648)) — 12 flaws + 15 honest = 27 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 1116125-1116132 | 7 | 1117625-1117632;1120417-1120424 | 125 | WORD_SPAN |
| 1 | FLAW-01 | 1178857-1178861 | 4 | 1179059-1179063;1179151-1179155 | 131 | WORD_SPAN |
| 2 | FLAW-02 | 1157803-1157806 | 3 | 1159403-1159406;1160305-1160308 | 144 | WORD_SPAN |
| 3 | FLAW-03 | 1132643-1132658 | 15 | 1132739-1132754;1173011-1173026 | 156 | WORD_SPAN |
| 4 | FLAW-04 | 1123533-1123537 | 4 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 1120212-1120217 | 5 | 1116179-1116183;1142257-1142261 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 1121610-1121614 | 4 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 1115994-1115996 | 2 | 1129636-1129642;1148961-1148967 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 1132007-1132013 | 6 | — | 114 | WORD_SPAN |
| 9 | FLAW-09 | 1129636-1129642 | 6 | — | 114 | WORD_SPAN |
| 10 | FLAW-10 | 1123533-1123536 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 1123534-1123537 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C012 | 1114478-1114481 | 3 | 1115134-1115137;1115332-1115335;1116930-1116933 | 137 | WORD_SPAN |
| 13 | T1-C023 | 1114682-1114690 | 8 | 1119562-1119570;1124767-1124775;1126763-1126771 | 143 | WORD_SPAN |
| 14 | T1-C024 | 1115628-1115635 | 7 | 1115653-1115660;1115783-1115790;1115809-1115816 | 137 | WORD_SPAN |
| 15 | T1-C006 | 1116179-1116183 | 4 | 1142257-1142261;1143843-1143847;1144199-1144203 | 143 | WORD_SPAN |
| 16 | T1-C009 | 1116390-1116396 | 6 | 1116510-1116516;1116600-1116606;1116692-1116698 | 150 | WORD_SPAN |
| 17 | T1-C001 | 1118838-1118841 | 3 | 1121739-1121742;1123816-1123819;1123875-1123878 | 156 | WORD_SPAN |
| 18 | T1-C013 | 1124767-1124780 | 13 | 1132554-1132567;1132772-1132785;1140366-1140379 | 168 | WORD_SPAN |
| 19 | T1-C010 | 1130416-1130422 | 6 | 1150459-1150465;1150512-1150518;1150558-1150564 | 143 | WORD_SPAN |
| 20 | T1-C014 | 1131956-1131971 | 15 | 1132641-1132656;1132739-1132754;1173011-1173026 | 168 | WORD_SPAN |
| 21 | T1-C026 | 1148489-1148498 | 9 | 1148523-1148532;1153413-1153422;1155062-1155071 | 156 | WORD_SPAN |
| 22 | T1-C019 | 1148830-1148843 | 13 | 1150400-1150413;1152762-1152775;1152789-1152802 | 162 | WORD_SPAN |
| 23 | T1-C017 | 1152837-1152850 | 13 | 1178377-1178390 | 144 | WORD_SPAN |
| 24 | T1-C025 | 1153136-1153155 | 19 | 1155232-1155251;1178454-1178473 | 150 | WORD_SPAN |
| 25 | T1-C022 | 1153311-1153330 | 19 | 1162048-1162067;1178805-1178824 | 150 | WORD_SPAN |
| 26 | T1-C011 | 1153947-1153952 | 5 | 1155507-1155512;1155782-1155787;1167633-1167638 | 137 | WORD_SPAN |

### Session S6 (code [1179648,1245184)) — 12 flaws + 20 honest = 32 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 1226447-1226460 | 13 | 1227119-1227132;1244736-1244749 | 156 | WORD_SPAN |
| 1 | FLAW-01 | 1215939-1215942 | 3 | 1215992-1215995;1216110-1216113 | 144 | WORD_SPAN |
| 2 | FLAW-02 | 1215257-1215269 | 12 | 1224241-1224253;1224542-1224554 | 150 | WORD_SPAN |
| 3 | FLAW-03 | 1226070-1226075 | 5 | 1228408-1228413;1239053-1239058 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 1181906-1181910 | 4 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 1181155-1181160 | 5 | 1180377-1180381;1181992-1181996 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 1181219-1181223 | 4 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 1179776-1179778 | 2 | 1181148-1181154;1181899-1181905 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 1180377-1180381 | 4 | — | 107 | WORD_SPAN |
| 9 | FLAW-09 | 1180560-1180566 | 6 | — | 114 | WORD_SPAN |
| 10 | FLAW-10 | 1181906-1181909 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 1181907-1181910 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C012 | 1179975-1179978 | 3 | 1181315-1181318;1181376-1181379;1183993-1183996 | 137 | WORD_SPAN |
| 13 | T1-C023 | 1180498-1180506 | 8 | 1182226-1182234;1183018-1183026;1183598-1183606 | 143 | WORD_SPAN |
| 14 | T1-C024 | 1180567-1180574 | 7 | 1180888-1180895;1180911-1180918;1185104-1185111 | 137 | WORD_SPAN |
| 15 | T1-C026 | 1180888-1180897 | 9 | 1185384-1185393;1187057-1187066;1216345-1216354 | 156 | WORD_SPAN |
| 16 | T1-C008 | 1181148-1181154 | 6 | 1181899-1181905;1182990-1182996;1193805-1193811 | 150 | WORD_SPAN |
| 17 | T1-C009 | 1181161-1181167 | 6 | 1209730-1209736;1209748-1209754;1228730-1228736 | 150 | WORD_SPAN |
| 18 | T1-C019 | 1182226-1182239 | 13 | 1185943-1185956;1187525-1187538;1191342-1191355 | 162 | WORD_SPAN |
| 19 | T1-C001 | 1182997-1183000 | 3 | 1183132-1183135;1183263-1183266;1183334-1183337 | 156 | WORD_SPAN |
| 20 | T1-C014 | 1183018-1183033 | 15 | 1193826-1193841;1195078-1195093;1195477-1195492 | 168 | WORD_SPAN |
| 21 | T1-C011 | 1186869-1186874 | 5 | 1191890-1191895;1207573-1207578;1208153-1208158 | 137 | WORD_SPAN |
| 22 | T1-C010 | 1189653-1189659 | 6 | 1190108-1190114;1192064-1192070;1192449-1192455 | 143 | WORD_SPAN |
| 23 | T1-C013 | 1193866-1193879 | 13 | 1195118-1195131;1195517-1195530;1195965-1195978 | 168 | WORD_SPAN |
| 24 | T1-C021 | 1197088-1197107 | 19 | 1197162-1197181;1198087-1198106;1198802-1198821 | 156 | WORD_SPAN |
| 25 | T1-C020 | 1201942-1201961 | 19 | 1202159-1202178;1202249-1202268;1202640-1202659 | 156 | WORD_SPAN |
| 26 | T1-C025 | 1209999-1210018 | 19 | 1225565-1225584;1226713-1226732;1227305-1227324 | 162 | WORD_SPAN |
| 27 | T1-C022 | 1210133-1210152 | 19 | 1225717-1225736;1226934-1226953;1227354-1227373 | 162 | WORD_SPAN |
| 28 | T1-C018 | 1211152-1211164 | 12 | 1215258-1215270;1224241-1224253;1224542-1224554 | 162 | WORD_SPAN |
| 29 | T1-C016 | 1214156-1214167 | 11 | 1220787-1220798;1221382-1221393;1221613-1221624 | 162 | WORD_SPAN |
| 30 | T1-C015 | 1215453-1215465 | 12 | 1215653-1215665;1215790-1215802;1215956-1215968 | 162 | WORD_SPAN |
| 31 | T1-C017 | 1225360-1225373 | 13 | 1226445-1226458;1227119-1227132;1244736-1244749 | 168 | WORD_SPAN |

### Session S7 (code [1245184,1310720)) — 12 flaws + 13 honest = 25 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 1274086-1274092 | 6 | 1274560-1274566;1277012-1277018 | 138 | WORD_SPAN |
| 1 | FLAW-01 | 1310546-1310552 | 6 | 1245846-1245852;1246380-1246386 | 138 | WORD_SPAN |
| 2 | FLAW-02 | 1248270-1248275 | 5 | 1248440-1248445;1270891-1270896 | 125 | WORD_SPAN |
| 3 | FLAW-03 | 1266731-1266734 | 3 | 1267171-1267174;1268418-1268421 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 1245330-1245333 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 1245853-1245857 | 4 | 1245926-1245928;1245970-1245972 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 1246430-1246435 | 5 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 1248173-1248177 | 4 | 1246968-1246974;1247131-1247137 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 1245926-1245928 | 2 | — | 107 | WORD_SPAN |
| 9 | FLAW-09 | 1246128-1246132 | 4 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 1245853-1245856 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 1245854-1245857 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C012 | 1245565-1245568 | 3 | 1245780-1245783;1246246-1246249;1252871-1252874 | 137 | WORD_SPAN |
| 13 | T1-C008 | 1245846-1245852 | 6 | 1246380-1246386;1247051-1247057;1247264-1247270 | 150 | WORD_SPAN |
| 14 | T1-C010 | 1246161-1246167 | 6 | 1246571-1246577;1246699-1246705;1246935-1246941 | 143 | WORD_SPAN |
| 15 | T1-C009 | 1246387-1246393 | 6 | 1246458-1246464;1246529-1246535;1247089-1247095 | 150 | WORD_SPAN |
| 16 | T1-C011 | 1246904-1246909 | 5 | 1248271-1248276;1248440-1248445;1270891-1270896 | 137 | WORD_SPAN |
| 17 | T1-C007 | 1246968-1246974 | 6 | 1247131-1247137;1247183-1247189;1247636-1247642 | 150 | WORD_SPAN |
| 18 | T1-C024 | 1247604-1247611 | 7 | 1247643-1247650;1248227-1248234;1252083-1252090 | 137 | WORD_SPAN |
| 19 | T1-C026 | 1247643-1247652 | 9 | 1273947-1273956;1292651-1292660;1299532-1299541 | 156 | WORD_SPAN |
| 20 | T1-C025 | 1248784-1248803 | 19 | 1250441-1250460;1254706-1254725;1264062-1264081 | 162 | WORD_SPAN |
| 21 | T1-C022 | 1250078-1250097 | 19 | 1251042-1251061;1254876-1254895;1264131-1264150 | 162 | WORD_SPAN |
| 22 | T1-C017 | 1260999-1261012 | 13 | 1280980-1280993;1297249-1297262;1297548-1297561 | 168 | WORD_SPAN |
| 23 | T1-C019 | 1272351-1272364 | 13 | 1288417-1288430 | 138 | WORD_SPAN |
| 24 | T1-C018 | 1272902-1272914 | 12 | 1298810-1298822;1299249-1299261;1309643-1309655 | 162 | WORD_SPAN |

## 9. Auditor checklist (B.2.6 — procedures any auditor runs from tape + committed spec)

**A1 — Spec-hash match.** `sha256sum WIRING_SPEC_DRAFT.md sealed/SEALED_FLAW_MANIFEST_DRAFT.md`
equals the prereg-pinned hashes (parent pins at wiring time; this draft is unpinned).
**A2 — Bit-for-bit re-run.** Run the parent's Zag teacher on (spec, slice bytes, empty history);
the emitted TEACHER_MSG proposal bytes must equal §8's schedule exactly
(spans, grounds, confidences, seq order; session_id/checksum per §5 rules).
**A3 — No RNG / wallclock / learning.** (a) `grep -riE 'rand|random|urandom|gettime|clock_gettime|rdtsc'`
over the teacher program text returns nothing; (b) N1–N3 hold by inspection of the state struct;
(c) N=5 reruns + M8 adversarial perturbations reproduce the §8 schedule byte-for-byte.
**A4 — §C evaluable and unfired.** From the tape alone, compute coverage / accept_rate /
maxconf_rate over every rolling 200-proposal window (§4.1); assert no window fires and no
single 255-proposal exceeds 5% of session stimulus. (Secondary: `grep -c sealed` over all
learner-side code paths returns 0 — the manifest is unreachable from the learner.)
**A5 — Vocabulary integrity.** Every proposed span's bytes equal the entry's literal pattern;
every grounding span's bytes equal the same pattern (except false-confidence flaws, whose
contradictory grounds are the planted defect); no proposal carries a string payload, token id,
or embedding (§P iron rule 1 — checkable by field inspection).
**A6 — Appeal bound.** From the tape: no proposal seq has >2 APPEAL events; no session-dead span
is re-proposed; every APPEAL carries ≥1 new_evidence_ref not present in the original proposal.

## 10. Open items for the parent (decisions, not guesses)

See the crew's report-back for the full list. Draft values marked DRAFT above may be replaced
only by a dated prereg amendment (prereg §13) after Micah's re-approval.

