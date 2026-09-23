# Arm-1 (peer-handwired) Wiring Spec — FROZEN (parent-wired)

**Status: FROZEN — wired by the parent (Muse) on 2026-09-21.**
This document supersedes `WIRING_SPEC_DRAFT.md`. Every number below is computed
deterministically from the two corpora by `wire_parent.py` (stdlib-only, no RNG,
no wallclock) via `gen_draft_reference.py`; nothing is hand-typed.

**Binding prereg:** `PREREG_FREEZE.md` §4 B.2 (wiring-spec requirements), B.7 (sealed flaw
manifest), B.8 (§C tripwire), §0 T-3/T-4/T-5/T-6/T-11/T-13/T-16 — FROZEN 2026-09-21 (§14).
**Design ref:** `TEACHERS.md` 2026-09-21 hand-wired-teacher amendment + installed-vs-learned ruling.

## 0. Provenance and corpora

Corpus files (hashes verified at wiring time — MUST match):
- `shakespeare.txt` — Project Gutenberg ebook 100, *The Complete Works of William Shakespeare*, 5,422,721 bytes, SHA-256 `a023115c2d4e2ee12221bdd780fdf2ac5a864fe225948656f51f8be462c7fffb`
- `sqlite3.c` — SQLite 3.53.4 amalgamation (https://www.sqlite.org/2026/sqlite-amalgamation-3530400.zip), 9,515,341 bytes, SHA-256 `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189`

## D. Parent wiring decisions (2026-09-21)

Recorded as W-2026-09-21-01..06. Per prereg §13 these are flagged for Micah's re-approval;
the wiring below implements them and the teacher is verified against them (A2).

- **W-01 — §P span offsets are SLICE-RELATIVE** (0 = the slice's first byte). The draft
  marked corpus-absolute as DRAFT ('parent confirms vs slice-relative'). The built harness
  indexes `stim[]` directly with proposal spans, each session's stimulus is exactly the
  slice bytes verbatim, and `STIMULUS_TAPE.md` mandates slice-relative. Corpus-absolute
  would have required rebuilding the harness, the tape format, and the curriculum docs.
- **W-02 — CHECKSUM = FNV-1a-64** over all preceding proposal bytes. The draft marked
  SHA-256-low64 as DRAFT ('coordinate with learner crew'). Both built codecs
  (`battery/tb_proposal.zag`, `harness/harness.zag`) implement FNV-1a-64 and the learner
  is verified against it.
- **W-03 — T-11 slice layout CONFIRMED** as drafted (8 slices x 65536 bytes,
  PROSE_BASE=2048, CODE_BASE=1048576).
- **W-04 — T-12 proposals/session cap CONFIRMED** (<=64; actual 24-46, see §8).
- **W-05 — T-5 flaw scoring CONFIRMED** (hit 1.0 / near-miss 0.5 / false-positive -1.0 /
  pass bar >= 10/12 per slice, averaged over slices).
- **W-06 — session_id is a harness-assigned u64 teacher INPUT** (the draft's `HARNESS`
  placeholder made precise). The teacher takes it as a CLI argument; the frozen §8 byte
  schedule is computed with the test vector session_id = 1001..1008 (S0->1001 … S7->1008).
  The production harness driver supplies the real id; proposals are validated against the
  session's id (`p_decode` IR_BAD_SESSION on mismatch).

## 1. Curriculum slice layout (T-11 — parent-confirmed per W-03)

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
- One teaching session per slice (8 sessions). Session stimulus = the slice bytes verbatim;
  `STIMULUS_REF.stimulus_byte_range` = the file byte range above; `stimulus_id` = LE64(SHA-256(slice bytes)[0..8]).
- ≤64 TEACHER_MSG per session (T-12, parent-confirmed per W-04).
  Actual per-session counts: 12 flaws + 12–34 honest = 24–46 (see §8).
- **§P span offsets are slice-relative byte offsets** (parent decision W-01): 0 = the slice's
  first byte. This matches the harness (`stim_count` indexes `stim[]` directly) and
  `STIMULUS_TAPE.md` §1.

## 2. Chunk vocabulary (B.2.1)

Every entry: stable `chunk_id`, literal byte pattern, match rule, SIGNED JUDGMENT
(sign + magnitude on the declared [-1000, +1000] scale: + = the teacher endorses this span
as a unit of knowledge; − = the teacher holds it is NOT a unit), and canonical occurrence
spans as slice-relative byte offsets (`{slice}:{start}-{end}`). Judgments are hand-set with the
rationale in §2.1; no judgment was learned, fitted, or tuned against outcomes.

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

| chunk_id | pattern | rule | J | class | canonical occurrences (slice-relative) | note |
|---|---|---|---|---|---|---|
| T1-P001 | `the` | WORD | +400 | func | S0:30-33; S1:212-215 |  |
| T1-P002 | `and` | WORD | +400 | func | S0:107-110; S1:55-58 |  |
| T1-P003 | `of` | WORD | +400 | func | S0:300-302; S1:288-290 |  |
| T1-P004 | `to` | WORD | +350 | func | S0:701-703; S1:196-198 |  |
| T1-P005 | `my` | WORD | +300 | func | S0:612-614; S1:96-98 |  |
| T1-P006 | `in` | WORD | +350 | func | S0:8-10; S1:41-43 |  |
| T1-P007 | `that` | WORD | +350 | func | S0:880-884; S1:224-228 |  |
| T1-P008 | `thy` | WORD | +300 | func | S0:175-178; S1:2945-2948 |  |
| T1-P009 | `thou` | WORD | +300 | func | S0:555-559; S1:1030-1034 |  |
| T1-P010 | `with` | WORD | +300 | func | S0:1416-1420; S1:2183-2187 |  |
| T1-P011 | `for` | WORD | +300 | func | S0:2993-2996; S1:2163-2166 |  |
| T1-P012 | `thee` | WORD | +300 | func | S0:111-115; S1:3113-3117 |  |
| T1-P013 | `but` | WORD | +300 | func | S0:1563-1566; S1:2105-2108 |  |
| T1-P014 | `is` | WORD | +300 | func | S0:868-870; S1:1276-1278 |  |
| T1-P015 | `you` | WORD | +300 | func | S0:7353-7356; S1:398-401 |  |
| T1-P016 | `not` | WORD | +300 | func | S0:942-945; S1:8-11 |  |
| T1-P017 | `be` | WORD | +300 | func | S0:62-64; S1:483-485 |  |
| T1-P018 | `it` | WORD | +300 | func | S0:780-782; S1:168-170 |  |
| T1-P019 | `me` | WORD | +250 | func | S0:5897-5899; S1:5-7 |  |
| T1-P020 | `have` | WORD | +300 | func | S0:8045-8049; S1:712-716 |  |
| T1-P021 | `he` | WORD | +300 | func | S0:1099-1101; S1:2869-2871 |  |
| T1-P022 | `his` | WORD | +300 | func | S0:657-660; S1:870-873 |  |
| T1-P023 | `him` | WORD | +300 | func | S0:2307-2310; S1:2827-2830 |  |
| T1-P024 | `as` | WORD | +250 | func | S0:5779-5781; S1:495-497 |  |
| T1-P025 | `love` | WORD | +600 | content | S0:1139-1143; S1:1133-1137 |  |
| T1-P026 | `lord` | WORD | +450 | content | S1:36494-36498; S2:368-372 |  |
| T1-P027 | `king` | WORD | +600 | content | S0:39910-39914; S1:35285-35289 |  |
| T1-P028 | `night` | WORD | +600 | content | S0:6770-6775; S1:6692-6697 |  |
| T1-P029 | `death` | WORD | +600 | content | S0:3172-3177; S1:2788-2793 |  |
| T1-P030 | `heart` | WORD | +600 | content | S0:12006-12011; S1:3724-3729 |  |
| T1-P031 | `man` | WORD | +500 | content | S0:12180-12183; S1:8770-8773 |  |
| T1-P032 | `day` | WORD | +500 | content | S0:3778-3781; S1:1290-1293 |  |
| T1-P033 | `time` | WORD | +500 | content | S0:875-879; S1:1775-1779 |  |
| T1-P034 | `good` | WORD | +500 | content | S0:8080-8084; S1:4197-4201 |  |
| T1-P035 | `fair` | WORD | +500 | content | S0:583-587; S1:457-461 |  |
| T1-P036 | `ing` | SUFFIX | +250 | morph | S0:18-21; S1:126-129 | word-final -ing |
| T1-P037 | `est` | SUFFIX | +200 | morph | S0:859-862; S1:1811-1814 | word-final -est (fairest) |
| T1-P038 | `’s` | SUFFIX | +250 | morph | S0:84-88; S1:1077-1081 | possessive ’s (U+2019) |
| T1-P039 | `cannot` | WORD | +450 | ambig | S0:23832-23838; S1:38306-38312 | A1: REVISE/SPLIT -> can+not acceptable |
| T1-P040 | `’tis` | WORD | +400 | ambig | S0:14644-14650; S1:4320-4326 | A2: REVISE/NARROW -> tis acceptable |
| T1-C001 | `int` | WORD | +450 | kw | S4:90-93; S5:4726-4729 |  |
| T1-C002 | `void` | WORD | +400 | kw | S4:352-356; S5:9421-9425 |  |
| T1-C003 | `const` | WORD | +400 | kw | S4:77-82; S5:6100-6105 |  |
| T1-C004 | `char` | WORD | +400 | kw | S4:10-14; S5:7498-7502 |  |
| T1-C005 | `if` | WORD | +350 | kw | S4:562-564; S5:1882-1884 |  |
| T1-C006 | `else` | WORD | +350 | kw | S4:1018-1022; S5:2067-2071 |  |
| T1-C007 | `return` | WORD | +400 | kw | S4:18535-18541; S5:17895-17901 |  |
| T1-C008 | `static` | WORD | +400 | kw | S4:25747-25753; S5:15524-15530 |  |
| T1-C009 | `struct` | WORD | +400 | kw | S4:4009-4015; S5:2278-2284 |  |
| T1-C010 | `assert` | WORD | +350 | kw | S4:21730-21736; S5:16304-16310 |  |
| T1-C011 | `while` | WORD | +300 | kw | S5:39835-39840; S6:7221-7226 |  |
| T1-C012 | `for` | WORD | +300 | kw | S4:16487-16490; S5:366-369 |  |
| T1-C013 | `sqlite3_value` | WORD | +550 | ident | S4:2630-2643; S5:10655-10668 |  |
| T1-C014 | `sqlite3_context` | WORD | +550 | ident | S4:3085-3100; S5:17844-17859 |  |
| T1-C015 | `sqlite3_file` | WORD | +500 | ident | S4:19359-19371; S6:35805-35817 |  |
| T1-C016 | `sqlite3_vfs` | WORD | +500 | ident | S4:1002-1013; S6:34508-34519 |  |
| T1-C017 | `sqlite3_mutex` | WORD | +550 | ident | S5:38725-38738; S6:45712-45725 |  |
| T1-C018 | `sqlite3_free` | WORD | +500 | ident | S6:31504-31516; S7:27718-27730 |  |
| T1-C019 | `sqlite3_int64` | WORD | +500 | ident | S4:14039-14052; S5:34718-34731 |  |
| T1-C020 | `sqlite3_str_appendf` | WORD | +450 | ident | S6:22294-22313 |  |
| T1-C021 | `sqlite3_result_text` | WORD | +450 | ident | S6:17440-17459 |  |
| T1-C022 | `sqlite3_mutex_leave` | WORD | +500 | ident | S5:39199-39218; S6:30485-30504 |  |
| T1-C023 | `sqlite3_` | PREFIX | +350 | morph | S4:1002-1010; S5:570-578 | namespace prefix |
| T1-C024 | `SQLITE_` | PREFIX | +300 | morph | S4:30-37; S5:1516-1523 | macro prefix |
| T1-C025 | `sqlite3_mutex_enter` | WORD | +500 | ambig | S5:39024-39043; S6:30351-30370 | A3: REVISE/SPLIT -> sqlite3_+mutex_enter acceptable |
| T1-C026 | `SQLITE_OK` | WORD | +450 | ambig | S4:10027-10036; S5:34377-34386 | A4: REVISE/SPLIT -> SQLITE_+OK acceptable |
| T1-N001 | `s` | LITERAL | -400 | neg | S0:4-5; S1:52-53 | bare letter is not a unit |
| T1-N002 | `th` | LITERAL | -300 | neg | S0:30-32; S1:59-61 | fragment is not a unit |
| T1-N003 | `ng` | LITERAL | -300 | neg | S0:19-21; S1:127-129 | fragment is not a unit |
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
(slice-relative, `{slice}:{start}-{end}`); `evidence_refs` = the next five in-slice occurrences,
slice-major order S0→S7. Entries with fewer than five further occurrences list what exists;
the appeal policy (§6) declines to appeal when no unused evidence ref remains.

| chunk_id | J | content_span | evidence_refs (≤5) |
|---|---|---|---|
| T1-P001 | +400 | S0:30-33 | S0:75-78; S0:97-100; S0:376-379; S0:841-844; S0:871-874 |
| T1-P002 | +400 | S0:107-110 | S0:477-480; S0:622-625; S0:832-835; S0:1193-1196; S0:1395-1398 |
| T1-P003 | +400 | S0:300-302 | S0:389-391; S0:594-596; S0:1071-1073; S0:1237-1239; S0:1275-1277 |
| T1-P004 | +350 | S0:701-703 | S0:1144-1146; S0:1375-1377; S0:1604-1606; S0:1700-1702; S0:1904-1906 |
| T1-P005 | +300 | S0:612-614 | S0:631-633; S0:5721-5723; S0:7897-7899; S0:8006-8008; S0:8331-8333 |
| T1-P006 | +350 | S0:8-10 | S0:207-209; S0:819-821; S0:1201-1203; S0:2483-2485; S0:3226-3228 |
| T1-P007 | +350 | S0:880-884 | S0:2080-2084; S0:2199-2203; S0:2957-2961; S0:4090-4094; S0:4328-4332 |
| T1-P008 | +300 | S0:175-178 | S0:210-213; S0:349-352; S0:392-395; S0:532-535; S0:745-748 |
| T1-P009 | +300 | S0:555-559 | S0:721-725; S0:765-769; S0:850-854; S0:937-941; S0:1254-1258 |
| T1-P010 | +300 | S0:1416-1420 | S0:1807-1811; S0:1991-1995; S0:2085-2089; S0:2330-2334; S0:2520-2524 |
| T1-P011 | +300 | S0:2993-2996 | S0:3059-3062; S0:3261-3264; S0:4666-4669; S0:5081-5084; S0:5370-5373 |
| T1-P012 | +300 | S0:111-115 | S0:1204-1208; S0:1421-1425; S0:1695-1699; S0:1899-1903; S0:1996-2000 |
| T1-P013 | +300 | S0:1563-1566 | S0:2646-2649; S0:4266-4269; S0:5066-5069; S0:7373-7376; S0:7877-7880 |
| T1-P014 | +300 | S0:868-870 | S0:1016-1018; S0:1096-1098; S0:2913-2915; S0:5476-5478; S0:5795-5797 |
| T1-P015 | +300 | S0:7353-7356 | S0:7382-7385; S0:7412-7415; S0:7460-7463; S0:7553-7556; S0:7599-7602 |
| T1-P016 | +300 | S0:942-945 | S0:1371-1374; S0:1778-1781; S0:2427-2430; S0:2731-2734; S0:2916-2919 |
| T1-P017 | +300 | S0:62-64 | S0:281-283; S0:704-706; S0:1115-1117; S0:1378-1380; S0:1907-1909 |
| T1-P018 | +300 | S0:780-782 | S0:2549-2551; S0:2576-2578; S0:2885-2887; S0:3052-3054; S0:4663-4665 |
| T1-P019 | +250 | S0:5897-5899 | S0:12379-12381; S0:12600-12602; S0:12948-12950; S0:12998-13000; S0:13262-13264 |
| T1-P020 | +300 | S0:8045-8049 | S0:14923-14927; S0:14944-14948; S0:19127-19131; S0:20400-20404; S0:21448-21452 |
| T1-P021 | +300 | S0:1099-1101 | S0:3758-3760; S0:7299-7301; S0:9186-9188; S0:15701-15703; S0:20254-20256 |
| T1-P022 | +300 | S0:657-660 | S0:1130-1133; S0:3418-3421; S0:3466-3469; S0:3510-3513; S0:3604-3607 |
| T1-P023 | +300 | S0:2307-2310 | S0:7289-7292; S0:17442-17445; S0:17472-17475; S0:17975-17978; S0:17985-17988 |
| T1-P024 | +250 | S0:5779-5781 | S0:5982-5984; S0:7177-7179; S0:7185-7187; S0:8806-8808; S0:9999-10001 |
| T1-P025 | +600 | S0:1139-1143 | S0:5205-5209; S0:5354-5358; S0:5770-5774; S0:5889-5893; S0:7377-7381 |
| T1-P026 | +450 | S1:36494-36498 | S1:36546-36550; S1:36712-36716; S1:38230-38234; S1:38277-38281; S1:43573-43577 |
| T1-P027 | +600 | S0:39910-39914 | S0:55528-55532; S1:35285-35289; S1:36027-36031; S1:36094-36098; S1:36313-36317 |
| T1-P028 | +600 | S0:6770-6775 | S0:9130-9135; S0:16905-16910; S0:16924-16929; S0:16993-16998; S0:17194-17199 |
| T1-P029 | +600 | S0:3172-3177 | S0:3297-3302; S0:7844-7849; S0:11009-11014; S0:13374-13379; S0:18664-18669 |
| T1-P030 | +600 | S0:12006-12011 | S0:13478-13483; S0:13664-13669; S0:13760-13765; S0:14033-14038; S0:14608-14613 |
| T1-P031 | +500 | S0:12180-12183 | S0:18027-18030; S0:18049-18052; S0:21293-21296; S1:8770-8773; S1:24611-24614 |
| T1-P032 | +500 | S0:3778-3781 | S0:6750-6753; S0:7821-7824; S0:9106-9109; S0:10593-10596; S0:16976-16979 |
| T1-P033 | +500 | S0:875-879 | S0:1335-1339; S0:2254-2258; S0:6726-6730; S0:7106-7110; S0:9905-9909 |
| T1-P034 | +500 | S0:8080-8084 | S0:14898-14902; S0:16081-16085; S0:22901-22905; S0:29484-29488; S0:42031-42035 |
| T1-P035 | +500 | S0:583-587 | S0:1026-1030; S0:3283-3287; S0:7714-7718; S0:9704-9708; S0:10827-10831 |
| T1-P036 | +250 | S0:18-21 | S0:328-331; S0:466-469; S0:653-656; S0:1559-1562; S0:1584-1587 |
| T1-P037 | +200 | S0:859-862 | S0:951-954; S0:1545-1548; S0:3312-3315; S0:3924-3927; S0:6069-6072 |
| T1-P038 | +250 | S0:84-88 | S0:220-224; S0:241-245; S0:542-546; S0:1182-1186; S0:1517-1521 |
| T1-P039 | +450 | S0:23832-23838 | S0:25093-25099; S0:31728-31734; S0:40829-40835; S0:44566-44572; S0:48913-48919 |
| T1-P040 | +400 | S0:14644-14650 | S0:54003-54009; S0:54014-54020; S0:61942-61948; S1:4320-4326; S1:7206-7212 |
| T1-C001 | +450 | S4:90-93 | S4:171-174; S4:230-233; S4:267-270; S4:292-295; S4:387-390 |
| T1-C002 | +400 | S4:352-356 | S4:425-429; S4:473-477; S4:522-526; S4:615-619; S4:955-959 |
| T1-C003 | +400 | S4:77-82 | S4:136-141; S4:195-200; S4:248-253; S4:317-322; S4:392-397 |
| T1-C004 | +400 | S4:10-14 | S4:45-49; S4:111-115; S4:254-258; S4:323-327; S4:398-402 |
| T1-C005 | +350 | S4:562-564 | S4:798-800; S4:4961-4963; S4:16557-16559; S4:16900-16902; S4:18260-18262 |
| T1-C006 | +350 | S4:1018-1022 | S4:2485-2489; S4:9989-9993; S4:11040-11044; S4:11200-11204; S4:11764-11768 |
| T1-C007 | +400 | S4:18535-18541 | S4:19038-19044; S4:47723-47729; S5:17895-17901; S5:21157-21163; S5:22260-22266 |
| T1-C008 | +400 | S4:25747-25753 | S4:25777-25783; S4:26838-26844; S4:29735-29741; S5:15524-15530; S5:34849-34855 |
| T1-C009 | +400 | S4:4009-4015 | S4:5813-5819; S4:59656-59662; S5:2278-2284; S5:2398-2404; S5:2488-2494 |
| T1-C010 | +350 | S4:21730-21736 | S4:52045-52051; S5:16304-16310; S5:36347-36353; S5:36400-36406; S5:36446-36452 |
| T1-C011 | +300 | S5:39835-39840 | S5:41395-41400; S5:41670-41675; S5:53521-53526; S5:53840-53845; S5:54366-54371 |
| T1-C012 | +300 | S4:16487-16490 | S4:18194-18197; S4:18942-18945; S4:19119-19122; S4:21198-21201; S4:21715-21718 |
| T1-C013 | +550 | S4:2630-2643 | S4:2698-2711; S4:2768-2781; S4:2828-2841; S4:2947-2960; S4:3001-3014 |
| T1-C014 | +550 | S4:3085-3100 | S4:8413-8428; S4:8464-8479; S4:8515-8530; S4:8545-8560; S4:8575-8590 |
| T1-C015 | +500 | S4:19359-19371 | S4:19570-19582; S4:19639-19651; S4:19699-19711; S6:35805-35817; S6:36005-36017 |
| T1-C016 | +500 | S4:1002-1013 | S4:19330-19341; S4:19424-19435; S6:34508-34519; S6:41139-41150; S6:41734-41745 |
| T1-C017 | +550 | S5:38725-38738 | S5:64265-64278; S6:45712-45725; S6:46797-46810; S6:47471-47484; S6:65088-65101 |
| T1-C018 | +500 | S6:31504-31516 | S6:35610-35622; S6:44593-44605; S6:44894-44906; S6:45308-45320; S7:27718-27730 |
| T1-C019 | +500 | S4:14039-14052 | S5:34718-34731; S5:36288-36301; S5:38650-38663; S5:38677-38690; S5:39402-39415 |
| T1-C020 | +450 | S6:22294-22313 | S6:22511-22530; S6:22601-22620; S6:22992-23011; S6:23062-23081; S6:23178-23197 |
| T1-C021 | +450 | S6:17440-17459 | S6:17514-17533; S6:18439-18458; S6:19154-19173; S6:19229-19248; S6:30615-30634 |
| T1-C022 | +500 | S5:39199-39218 | S5:47936-47955; S5:64693-64712; S6:30485-30504; S6:46069-46088; S6:47286-47305 |
| T1-C023 | +350 | S4:1002-1010 | S4:2630-2638; S4:2698-2706; S4:2768-2776; S4:2828-2836; S4:2947-2955 |
| T1-C024 | +300 | S4:30-37 | S4:96-103; S4:156-163; S4:215-222; S4:277-284; S4:337-344 |
| T1-C025 | +500 | S5:39024-39043 | S5:41120-41139; S5:64342-64361; S6:30351-30370; S6:45917-45936; S6:47065-47084 |
| T1-C026 | +450 | S4:10027-10036 | S4:11426-11435; S4:11707-11716; S5:34377-34386; S5:34411-34420; S5:39301-39310 |
| T1-N001 | -400 | — (held pattern, never proposed) | — |
| T1-N002 | -300 | — (held pattern, never proposed) | — |
| T1-N003 | -300 | — (held pattern, never proposed) | — |
| T1-N004 | -250 | — (held pattern, never proposed) | — |

## 4. Confidence policy (B.2.1 — non-255 BY CONSTRUCTION)

Deterministic formula, pure function of declared judgment and attached grounding count:

`confidence(J, g) = clamp(64 + |J|/8 + 12*g, 0, 250)`, `g` = number of grounding spans (0–3 honest).

- The clamp ceiling is **250, not 255, BY CONSTRUCTION**: no honest proposal can ever emit 255.
  Only false-confidence FLAW proposals emit 255 (see sealed manifest).
- In this frozen schedule honest confidences range 119–175; 104 of 191 honest proposals are <150
  (expressed uncertainty, not a confidence monoculture).
- Confidence is evidence weight, never a command (§P iron rule 2).

### 4.1 §C tripwire arithmetic — the honest teacher cannot fire it (T-16)

Tripwire (frozen): over any rolling 200-proposal window, FIRE iff
`coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND maxconf_rate ≥ 0.90`;
secondary: any single 255-proposal covering >5% of session stimulus fires immediately.

Frozen schedule's exact computed values (from the deterministic schedule, §8):
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

Pure function `PROPOSE(spec, slice_bytes, session_id, history) -> [Proposal]`.
`session_history` = the tape's STUDENT_DECISION records for this session (harness-provided, read-only).
`session_id` = the harness-assigned u64 for this session (parent decision W-06).
Pseudocode precise enough to implement verbatim in Zag:

```
PROPOSE(spec, S, session_id, history):
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
      occ = MATCH(S, e.pattern, e.rule)       # §2 match rules; slice-relative offsets;
                                          # first 4 occurrences suffice (only occ[0..3] used)
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
  return { magic=0x54505250, version=1, teacher_id=1, session_id=<input>,
           seq=seq, kind=1, span_start=span.start, span_end=span.end,
           aux_count=0, ground_count=len(grounds),
           grounding=[g for g in grounds], confidence=conf,
           checksum=CHECKSUM(all preceding fields) }
span_start/span_end/grounding are SLICE-RELATIVE byte offsets (parent decision W-01).
CHECKSUM = FNV-1a-64 over the canonical little-endian serialization of all
           preceding fields (parent decision W-02; matches battery/tb_proposal.zag
           and harness/harness.zag).
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
SHA-256 digests (flaw placement, `FLAW_PLACEMENT.md`) or deterministic scans (proposal order).
Verified by N=5 byte-identical re-runs + adversarial perturbations (M8 procedure, §6 of prereg).
**N3 — No wallclock.** Teacher logic is a pure function of (spec bytes, stimulus bytes,
session_id, session history). Time appears only as monotonic seq counters and the
harness-assigned session_id. TEACHER_MSG carries the deterministic logical tick (seq),
never a timestamp.

## 8. Per-session proposal schedule (deterministic reference)

Flaws: seq 0–11 in manifest order (full bytes in `sealed/SEALED_FLAW_MANIFEST.md`).
Honest: cursor order (span_start, chunk_id). **All offsets below are slice-relative**
(parent decision W-01). Byte-exact proposal encodings for the frozen test vector
(session_id = 1001..1008) are in `wired/expected/S{i}.bin`; the machine-readable schedule
is `wired/schedule.tsv`.

### Session S0 (prose [2048,67584), session_id=1001) — 12 flaws + 32 honest = 44 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 36097-36100 | 3 | 37236-37239;38256-38259 | 125 | WORD_SPAN |
| 1 | FLAW-01 | 48352-48354 | 2 | 48400-48402;48435-48437 | 125 | WORD_SPAN |
| 2 | FLAW-02 | 27936-27940 | 4 | 28983-28987;29873-29877 | 125 | WORD_SPAN |
| 3 | FLAW-03 | 16354-16358 | 4 | 18303-18307;18706-18710 | 163 | WORD_SPAN |
| 4 | FLAW-04 | 30-33 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 107-110 | 3 | 612-614;631-633 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 300-302 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 701-703 | 2 | 880-884;2080-2084 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 612-614 | 2 | — | 101 | WORD_SPAN |
| 9 | FLAW-09 | 8-10 | 2 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 880-883 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 881-884 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P036 | 18-21 | 3 | 328-331;466-469;653-656 | 131 | WORD_SPAN |
| 13 | T1-P017 | 62-64 | 2 | 281-283;704-706;1115-1117 | 137 | WORD_SPAN |
| 14 | T1-P038 | 84-88 | 4 | 220-224;241-245;542-546 | 131 | WORD_SPAN |
| 15 | T1-P012 | 111-115 | 4 | 1204-1208;1421-1425;1695-1699 | 137 | WORD_SPAN |
| 16 | T1-P008 | 175-178 | 3 | 210-213;349-352;392-395 | 137 | WORD_SPAN |
| 17 | T1-P009 | 555-559 | 4 | 721-725;765-769;850-854 | 137 | WORD_SPAN |
| 18 | T1-P035 | 583-587 | 4 | 1026-1030;3283-3287;7714-7718 | 162 | WORD_SPAN |
| 19 | T1-P022 | 657-660 | 3 | 1130-1133;3418-3421;3466-3469 | 137 | WORD_SPAN |
| 20 | T1-P018 | 780-782 | 2 | 2549-2551;2576-2578;2885-2887 | 137 | WORD_SPAN |
| 21 | T1-P037 | 859-862 | 3 | 951-954;1545-1548;3312-3315 | 125 | WORD_SPAN |
| 22 | T1-P014 | 868-870 | 2 | 1016-1018;1096-1098;2913-2915 | 137 | WORD_SPAN |
| 23 | T1-P033 | 875-879 | 4 | 1335-1339;2254-2258;6726-6730 | 162 | WORD_SPAN |
| 24 | T1-P016 | 942-945 | 3 | 1371-1374;1778-1781;2427-2430 | 137 | WORD_SPAN |
| 25 | T1-P021 | 1099-1101 | 2 | 3758-3760;7299-7301;9186-9188 | 137 | WORD_SPAN |
| 26 | T1-P025 | 1139-1143 | 4 | 5205-5209;5354-5358;5770-5774 | 175 | WORD_SPAN |
| 27 | T1-P010 | 1416-1420 | 4 | 1807-1811;1991-1995;2085-2089 | 137 | WORD_SPAN |
| 28 | T1-P013 | 1563-1566 | 3 | 2646-2649;4266-4269;5066-5069 | 137 | WORD_SPAN |
| 29 | T1-P023 | 2307-2310 | 3 | 7289-7292;17442-17445;17472-17475 | 137 | WORD_SPAN |
| 30 | T1-P011 | 2993-2996 | 3 | 3059-3062;3261-3264;4666-4669 | 137 | WORD_SPAN |
| 31 | T1-P029 | 3172-3177 | 5 | 3297-3302;7844-7849;11009-11014 | 175 | WORD_SPAN |
| 32 | T1-P032 | 3778-3781 | 3 | 6750-6753;7821-7824;9106-9109 | 162 | WORD_SPAN |
| 33 | T1-P024 | 5779-5781 | 2 | 5982-5984;7177-7179;7185-7187 | 131 | WORD_SPAN |
| 34 | T1-P019 | 5897-5899 | 2 | 12379-12381;12600-12602;12948-12950 | 131 | WORD_SPAN |
| 35 | T1-P028 | 6770-6775 | 5 | 9130-9135;16905-16910;16924-16929 | 175 | WORD_SPAN |
| 36 | T1-P015 | 7353-7356 | 3 | 7382-7385;7412-7415;7460-7463 | 137 | WORD_SPAN |
| 37 | T1-P020 | 8045-8049 | 4 | 14923-14927;14944-14948;19127-19131 | 137 | WORD_SPAN |
| 38 | T1-P034 | 8080-8084 | 4 | 14898-14902;16081-16085;22901-22905 | 162 | WORD_SPAN |
| 39 | T1-P030 | 12006-12011 | 5 | 13478-13483;13664-13669;13760-13765 | 175 | WORD_SPAN |
| 40 | T1-P031 | 12180-12183 | 3 | 18027-18030;18049-18052;21293-21296 | 162 | WORD_SPAN |
| 41 | T1-P040 | 14644-14650 | 6 | 54003-54009;54014-54020;61942-61948 | 150 | WORD_SPAN |
| 42 | T1-P039 | 23832-23838 | 6 | 25093-25099;31728-31734;40829-40835 | 156 | WORD_SPAN |
| 43 | T1-P027 | 39910-39914 | 4 | 55528-55532 | 151 | WORD_SPAN |

### Session S1 (prose [67584,133120), session_id=1002) — 12 flaws + 33 honest = 45 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 36079-36084 | 5 | 2788-2793;27787-27792 | 163 | WORD_SPAN |
| 1 | FLAW-01 | 30746-30750 | 4 | 31004-31008;31025-31029 | 163 | WORD_SPAN |
| 2 | FLAW-02 | 20534-20538 | 4 | 20751-20755;22006-22010 | 150 | WORD_SPAN |
| 3 | FLAW-03 | 41723-41726 | 3 | 41872-41875;42331-42334 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 212-215 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 55-58 | 3 | 96-98;130-132 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 288-290 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 196-198 | 2 | 224-228;3063-3067 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 96-98 | 2 | — | 101 | WORD_SPAN |
| 9 | FLAW-09 | 41-43 | 2 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 224-227 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 225-228 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P019 | 5-7 | 2 | 150-152;454-456;2797-2799 | 131 | WORD_SPAN |
| 13 | T1-P016 | 8-11 | 3 | 171-174;1126-1129;2212-2215 | 137 | WORD_SPAN |
| 14 | T1-P036 | 126-129 | 3 | 146-149;192-195;1400-1403 | 131 | WORD_SPAN |
| 15 | T1-P018 | 168-170 | 2 | 420-422;3656-3658;4122-4124 | 137 | WORD_SPAN |
| 16 | T1-P015 | 398-401 | 3 | 408-411;469-472;498-501 | 137 | WORD_SPAN |
| 17 | T1-P035 | 457-461 | 4 | 3395-3399;15128-15132;15562-15566 | 162 | WORD_SPAN |
| 18 | T1-P017 | 483-485 | 2 | 986-988;1138-1140;1227-1229 | 137 | WORD_SPAN |
| 19 | T1-P024 | 495-497 | 2 | 1173-1175;2061-2063;2516-2518 | 131 | WORD_SPAN |
| 20 | T1-P020 | 712-716 | 4 | 1644-1648;2026-2030;3887-3891 | 137 | WORD_SPAN |
| 21 | T1-P022 | 870-873 | 3 | 3557-3560;6310-6313;6473-6476 | 137 | WORD_SPAN |
| 22 | T1-P009 | 1030-1034 | 4 | 2921-2925;3341-3345;4251-4255 | 137 | WORD_SPAN |
| 23 | T1-P038 | 1077-1081 | 4 | 1942-1946;3045-3049;3138-3142 | 131 | WORD_SPAN |
| 24 | T1-P025 | 1133-1137 | 4 | 1282-1286;2493-2497;2766-2770 | 175 | WORD_SPAN |
| 25 | T1-P014 | 1276-1278 | 2 | 1461-1463;1546-1548;3862-3864 | 137 | WORD_SPAN |
| 26 | T1-P032 | 1290-1293 | 3 | 3284-3287;6684-6687;8964-8967 | 162 | WORD_SPAN |
| 27 | T1-P033 | 1775-1779 | 4 | 2132-2136;2757-2761;3623-3627 | 162 | WORD_SPAN |
| 28 | T1-P037 | 1811-1814 | 3 | 1948-1951;4655-4658;4874-4877 | 125 | WORD_SPAN |
| 29 | T1-P013 | 2105-2108 | 3 | 2179-2182;2318-2321;3243-3246 | 137 | WORD_SPAN |
| 30 | T1-P011 | 2163-2166 | 3 | 3549-3552;4013-4016;4170-4173 | 137 | WORD_SPAN |
| 31 | T1-P010 | 2183-2187 | 4 | 2723-2727;3960-3964;4975-4979 | 137 | WORD_SPAN |
| 32 | T1-P029 | 2788-2793 | 5 | 27787-27792;27819-27824;28192-28197 | 175 | WORD_SPAN |
| 33 | T1-P023 | 2827-2830 | 3 | 3905-3908;10021-10024;19207-19210 | 137 | WORD_SPAN |
| 34 | T1-P021 | 2869-2871 | 2 | 19627-19629;19789-19791;19837-19839 | 137 | WORD_SPAN |
| 35 | T1-P008 | 2945-2948 | 3 | 3208-3211;3391-3394;3836-3839 | 137 | WORD_SPAN |
| 36 | T1-P012 | 3113-3117 | 4 | 4646-4650;12294-12298;12497-12501 | 137 | WORD_SPAN |
| 37 | T1-P030 | 3724-3729 | 5 | 4601-4606;6414-6419;10278-10283 | 175 | WORD_SPAN |
| 38 | T1-P034 | 4197-4201 | 4 | 5746-5750;11717-11721;17852-17856 | 162 | WORD_SPAN |
| 39 | T1-P040 | 4320-4326 | 6 | 7206-7212;7224-7230;7413-7419 | 150 | WORD_SPAN |
| 40 | T1-P028 | 6692-6697 | 5 | 11076-11081;27085-27090;28489-28494 | 175 | WORD_SPAN |
| 41 | T1-P031 | 8770-8773 | 3 | 24611-24614;26201-26204;36139-36142 | 162 | WORD_SPAN |
| 42 | T1-P027 | 35285-35289 | 4 | 36027-36031;36094-36098;36313-36317 | 175 | WORD_SPAN |
| 43 | T1-P026 | 36494-36498 | 4 | 36546-36550;36712-36716;38230-38234 | 156 | WORD_SPAN |
| 44 | T1-P039 | 38306-38312 | 6 | 41733-41739;44352-44358;45075-45081 | 156 | WORD_SPAN |

### Session S2 (prose [133120,198656), session_id=1003) — 12 flaws + 32 honest = 44 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 34908-34912 | 4 | 35048-35052;35088-35092 | 131 | WORD_SPAN |
| 1 | FLAW-01 | 52482-52485 | 3 | 52654-52657;52688-52691 | 125 | WORD_SPAN |
| 2 | FLAW-02 | 18571-18576 | 5 | 25599-25604;34321-34326 | 163 | WORD_SPAN |
| 3 | FLAW-03 | 17812-17815 | 3 | 18123-18126;18359-18362 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 610-613 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 932-935 | 3 | 360-362;395-397 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 552-554 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 134-136 | 2 | 820-824;1721-1725 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 360-362 | 2 | — | 101 | WORD_SPAN |
| 9 | FLAW-09 | 901-903 | 2 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 820-823 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 821-824 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P014 | 104-106 | 2 | 530-532;802-804;1944-1946 | 137 | WORD_SPAN |
| 13 | T1-P022 | 107-110 | 3 | 544-547;631-634;652-655 | 137 | WORD_SPAN |
| 14 | T1-P023 | 137-140 | 3 | 456-459;513-516;526-529 | 137 | WORD_SPAN |
| 15 | T1-P015 | 152-155 | 3 | 273-276;993-996;1500-1503 | 137 | WORD_SPAN |
| 16 | T1-P013 | 170-173 | 3 | 5123-5126;5536-5539;5948-5951 | 137 | WORD_SPAN |
| 17 | T1-P038 | 226-230 | 4 | 878-882;3256-3260;3516-3520 | 131 | WORD_SPAN |
| 18 | T1-P035 | 307-311 | 4 | 11065-11069;12237-12241;14688-14692 | 162 | WORD_SPAN |
| 19 | T1-P034 | 363-367 | 4 | 6898-6902;13023-13027;13670-13674 | 162 | WORD_SPAN |
| 20 | T1-P026 | 368-372 | 4 | 13675-13679;13819-13823;15424-15428 | 156 | WORD_SPAN |
| 21 | T1-P021 | 414-416 | 2 | 575-577;5731-5733;5766-5768 | 137 | WORD_SPAN |
| 22 | T1-P036 | 522-525 | 3 | 684-687;780-783;1137-1140 | 131 | WORD_SPAN |
| 23 | T1-P029 | 555-560 | 5 | 1706-1711;4170-4175;4306-4311 | 175 | WORD_SPAN |
| 24 | T1-P019 | 583-585 | 2 | 697-699;1445-1447;1569-1571 | 131 | WORD_SPAN |
| 25 | T1-P024 | 607-609 | 2 | 709-711;5233-5235;6275-6277 | 131 | WORD_SPAN |
| 26 | T1-P037 | 618-621 | 3 | 1553-1556;1896-1899;1934-1937 | 125 | WORD_SPAN |
| 27 | T1-P020 | 763-767 | 4 | 1111-1115;2050-2054;2080-2084 | 137 | WORD_SPAN |
| 28 | T1-P018 | 928-930 | 2 | 2241-2243;2262-2264;2623-2625 | 137 | WORD_SPAN |
| 29 | T1-P016 | 1014-1017 | 3 | 1210-1213;2330-2333;2383-2386 | 137 | WORD_SPAN |
| 30 | T1-P017 | 1018-1020 | 2 | 1619-1621;2411-2413;3679-3681 | 137 | WORD_SPAN |
| 31 | T1-P011 | 1448-1451 | 3 | 2452-2455;3879-3882;4774-4777 | 137 | WORD_SPAN |
| 32 | T1-P039 | 1593-1599 | 6 | 5774-5780;15270-15276;17719-17725 | 156 | WORD_SPAN |
| 33 | T1-P012 | 1605-1609 | 4 | 2339-2343;2350-2354;3708-3712 | 137 | WORD_SPAN |
| 34 | T1-P009 | 1766-1770 | 4 | 1814-1818;2951-2955;2997-3001 | 137 | WORD_SPAN |
| 35 | T1-P010 | 2533-2537 | 4 | 2574-2578;4506-4510;5635-5639 | 137 | WORD_SPAN |
| 36 | T1-P040 | 2567-2573 | 6 | 8817-8823;8911-8917;9161-9167 | 150 | WORD_SPAN |
| 37 | T1-P008 | 3422-3425 | 3 | 4122-4125;4375-4378;4511-4514 | 137 | WORD_SPAN |
| 38 | T1-P033 | 4206-4210 | 4 | 4930-4934;7990-7994;10687-10691 | 162 | WORD_SPAN |
| 39 | T1-P031 | 5714-5717 | 3 | 9241-9244;13397-13400;17506-17509 | 162 | WORD_SPAN |
| 40 | T1-P032 | 6455-6458 | 3 | 30300-30303;30307-30310;36650-36653 | 162 | WORD_SPAN |
| 41 | T1-P027 | 10110-10114 | 4 | 10218-10222;11418-11422;16503-16507 | 175 | WORD_SPAN |
| 42 | T1-P025 | 11103-11107 | 4 | 11843-11847;11862-11866;12371-12375 | 175 | WORD_SPAN |
| 43 | T1-P028 | 36638-36643 | 5 | 38522-38527;49312-49317;51790-51795 | 175 | WORD_SPAN |

### Session S3 (prose [198656,264192), session_id=1004) — 12 flaws + 34 honest = 46 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 64704-64707 | 3 | 209-212;258-261 | 125 | WORD_SPAN |
| 1 | FLAW-01 | 47415-47418 | 3 | 47846-47849;48339-48342 | 138 | WORD_SPAN |
| 2 | FLAW-02 | 51263-51266 | 3 | 51283-51286;51447-51450 | 119 | WORD_SPAN |
| 3 | FLAW-03 | 60348-60350 | 2 | 61544-61546;61558-61560 | 119 | WORD_SPAN |
| 4 | FLAW-04 | 9-12 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 206-208 | 2 | 451-453;1710-1712 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 35-37 | 2 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 1319-1321 | 2 | 14582-14585;15091-15094 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 451-453 | 2 | — | 107 | WORD_SPAN |
| 9 | FLAW-09 | 99-103 | 4 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 99-102 | 3 | — | 119 | WORD_SPAN |
| 11 | FLAW-11 | 100-103 | 3 | — | 119 | WORD_SPAN |
| 12 | T1-P023 | 26-29 | 3 | 576-579;1117-1120;1520-1523 | 137 | WORD_SPAN |
| 13 | T1-P015 | 45-48 | 3 | 52-55;302-305;472-475 | 137 | WORD_SPAN |
| 14 | T1-P024 | 49-51 | 2 | 459-461;1063-1065;1349-1351 | 131 | WORD_SPAN |
| 15 | T1-P017 | 62-64 | 2 | 180-182;410-412;448-450 | 137 | WORD_SPAN |
| 16 | T1-P021 | 77-79 | 2 | 123-125;165-167;306-308 | 137 | WORD_SPAN |
| 17 | T1-P033 | 201-205 | 4 | 12421-12425;12567-12571;17840-17844 | 162 | WORD_SPAN |
| 18 | T1-P022 | 209-212 | 3 | 258-261;421-424;1659-1662 | 137 | WORD_SPAN |
| 19 | T1-P036 | 266-269 | 3 | 339-342;605-608;1540-1543 | 131 | WORD_SPAN |
| 20 | T1-P019 | 346-348 | 2 | 612-614;821-823;2563-2565 | 131 | WORD_SPAN |
| 21 | T1-P014 | 387-389 | 2 | 1145-1147;1550-1552;1604-1606 | 137 | WORD_SPAN |
| 22 | T1-P002 | 397-400 | 3 | 1228-1231;1277-1280;1333-1336 | 150 | WORD_SPAN |
| 23 | T1-P018 | 401-403 | 2 | 516-518;2209-2211;3373-3375 | 137 | WORD_SPAN |
| 24 | T1-P020 | 490-494 | 4 | 1874-1878;3059-3063;3118-3122 | 137 | WORD_SPAN |
| 25 | T1-P010 | 537-541 | 4 | 3123-3127;3288-3292;3394-3398 | 137 | WORD_SPAN |
| 26 | T1-P011 | 700-703 | 3 | 1826-1829;2068-2071;2175-2178 | 137 | WORD_SPAN |
| 27 | T1-P013 | 1214-1217 | 3 | 3047-3050;4289-4292;5032-5035 | 137 | WORD_SPAN |
| 28 | T1-P038 | 1508-1512 | 4 | 1954-1958;2107-2111;2279-2283 | 131 | WORD_SPAN |
| 29 | T1-P026 | 1593-1597 | 4 | 11597-11601;15467-15471;15780-15784 | 156 | WORD_SPAN |
| 30 | T1-P031 | 1816-1819 | 3 | 7220-7223;7256-7259;7774-7777 | 162 | WORD_SPAN |
| 31 | T1-P016 | 2854-2857 | 3 | 2907-2910;3381-3384;3821-3824 | 137 | WORD_SPAN |
| 32 | T1-P037 | 2951-2954 | 3 | 5191-5194;5208-5211;6972-6975 | 125 | WORD_SPAN |
| 33 | T1-P032 | 4343-4346 | 3 | 17612-17615;23643-23646;25386-25389 | 162 | WORD_SPAN |
| 34 | T1-P034 | 4471-4475 | 4 | 11592-11596;13397-13401;13418-13422 | 162 | WORD_SPAN |
| 35 | T1-P040 | 4607-4613 | 6 | 11172-11178;15679-15685;16991-16997 | 150 | WORD_SPAN |
| 36 | T1-P012 | 5666-5670 | 4 | 5843-5847;14095-14099;14514-14518 | 137 | WORD_SPAN |
| 37 | T1-P025 | 7313-7317 | 4 | 11830-11834;13373-13377;24701-24705 | 175 | WORD_SPAN |
| 38 | T1-P029 | 9514-9519 | 5 | 12292-12297;13176-13181;15761-15766 | 175 | WORD_SPAN |
| 39 | T1-P039 | 10189-10195 | 6 | 14199-14205;17657-17663;46777-46783 | 156 | WORD_SPAN |
| 40 | T1-P030 | 10477-10482 | 5 | 24219-24224;41693-41698;55997-56002 | 175 | WORD_SPAN |
| 41 | T1-P027 | 11606-11610 | 4 | 13071-13075;15832-15836;18436-18440 | 175 | WORD_SPAN |
| 42 | T1-P028 | 12102-12107 | 5 | 17620-17625;18621-18626;21851-21856 | 175 | WORD_SPAN |
| 43 | T1-P009 | 13743-13747 | 4 | 14101-14105;14593-14597;19788-19792 | 137 | WORD_SPAN |
| 44 | T1-P008 | 14582-14585 | 3 | 15091-15094;15202-15205;34791-34794 | 137 | WORD_SPAN |
| 45 | T1-P035 | 23802-23806 | 4 | 24415-24419;25284-25288;28469-28473 | 162 | WORD_SPAN |

### Session S4 (code [1048576,1114112), session_id=1005) — 12 flaws + 12 honest = 24 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 59257-59261 | 4 | 1018-1022;2485-2489 | 131 | WORD_SPAN |
| 1 | FLAW-01 | 21566-21568 | 2 | 21794-21796;23147-23149 | 131 | WORD_SPAN |
| 2 | FLAW-02 | 9447-9462 | 15 | 14076-14091;3085-3100 | 156 | WORD_SPAN |
| 3 | FLAW-03 | 29736-29742 | 6 | 25747-25753;25777-25783 | 138 | WORD_SPAN |
| 4 | FLAW-04 | 90-93 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 352-356 | 4 | 562-564;798-800 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 77-82 | 5 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 10-14 | 4 | 18535-18541;19038-19044 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 18535-18541 | 6 | — | 114 | WORD_SPAN |
| 9 | FLAW-09 | 4009-4015 | 6 | — | 114 | WORD_SPAN |
| 10 | FLAW-10 | 352-355 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 353-356 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C024 | 30-37 | 7 | 96-103;156-163;215-222 | 137 | WORD_SPAN |
| 13 | T1-C005 | 562-564 | 2 | 798-800;4961-4963;16557-16559 | 143 | WORD_SPAN |
| 14 | T1-C016 | 1002-1013 | 11 | 19330-19341;19424-19435 | 150 | WORD_SPAN |
| 15 | T1-C006 | 1018-1022 | 4 | 2485-2489;9989-9993;11040-11044 | 143 | WORD_SPAN |
| 16 | T1-C013 | 2630-2643 | 13 | 2698-2711;2768-2781;2828-2841 | 168 | WORD_SPAN |
| 17 | T1-C014 | 3085-3100 | 15 | 8413-8428;8464-8479;8515-8530 | 168 | WORD_SPAN |
| 18 | T1-C026 | 10027-10036 | 9 | 11426-11435;11707-11716 | 144 | WORD_SPAN |
| 19 | T1-C019 | 14039-14052 | 13 | — | 126 | WORD_SPAN |
| 20 | T1-C012 | 16487-16490 | 3 | 18194-18197;18942-18945;19119-19122 | 137 | WORD_SPAN |
| 21 | T1-C015 | 19359-19371 | 12 | 19570-19582;19639-19651;19699-19711 | 162 | WORD_SPAN |
| 22 | T1-C010 | 21730-21736 | 6 | 52045-52051 | 119 | WORD_SPAN |
| 23 | T1-C008 | 25747-25753 | 6 | 25777-25783;26838-26844;29735-29741 | 150 | WORD_SPAN |

### Session S5 (code [1114112,1179648), session_id=1006) — 12 flaws + 15 honest = 27 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 2013-2020 | 7 | 3513-3520;6305-6312 | 125 | WORD_SPAN |
| 1 | FLAW-01 | 64745-64749 | 4 | 64947-64951;65039-65043 | 131 | WORD_SPAN |
| 2 | FLAW-02 | 43691-43694 | 3 | 45291-45294;46193-46196 | 144 | WORD_SPAN |
| 3 | FLAW-03 | 18531-18546 | 15 | 18627-18642;58899-58914 | 156 | WORD_SPAN |
| 4 | FLAW-04 | 9421-9425 | 4 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 6100-6105 | 5 | 2067-2071;28145-28149 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 7498-7502 | 4 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 1882-1884 | 2 | 15524-15530;34849-34855 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 17895-17901 | 6 | — | 114 | WORD_SPAN |
| 9 | FLAW-09 | 15524-15530 | 6 | — | 114 | WORD_SPAN |
| 10 | FLAW-10 | 9421-9424 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 9422-9425 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C012 | 366-369 | 3 | 1022-1025;1220-1223;2818-2821 | 137 | WORD_SPAN |
| 13 | T1-C023 | 570-578 | 8 | 5450-5458;10655-10663;12651-12659 | 143 | WORD_SPAN |
| 14 | T1-C024 | 1516-1523 | 7 | 1541-1548;1671-1678;1697-1704 | 137 | WORD_SPAN |
| 15 | T1-C006 | 2067-2071 | 4 | 28145-28149;29731-29735;30087-30091 | 143 | WORD_SPAN |
| 16 | T1-C009 | 2278-2284 | 6 | 2398-2404;2488-2494;2580-2586 | 150 | WORD_SPAN |
| 17 | T1-C001 | 4726-4729 | 3 | 7627-7630;9704-9707;9763-9766 | 156 | WORD_SPAN |
| 18 | T1-C013 | 10655-10668 | 13 | 18442-18455;18660-18673;26254-26267 | 168 | WORD_SPAN |
| 19 | T1-C010 | 16304-16310 | 6 | 36347-36353;36400-36406;36446-36452 | 143 | WORD_SPAN |
| 20 | T1-C014 | 17844-17859 | 15 | 18529-18544;18627-18642;58899-58914 | 168 | WORD_SPAN |
| 21 | T1-C026 | 34377-34386 | 9 | 34411-34420;39301-39310;40950-40959 | 156 | WORD_SPAN |
| 22 | T1-C019 | 34718-34731 | 13 | 36288-36301;38650-38663;38677-38690 | 162 | WORD_SPAN |
| 23 | T1-C017 | 38725-38738 | 13 | 64265-64278 | 144 | WORD_SPAN |
| 24 | T1-C025 | 39024-39043 | 19 | 41120-41139;64342-64361 | 150 | WORD_SPAN |
| 25 | T1-C022 | 39199-39218 | 19 | 47936-47955;64693-64712 | 150 | WORD_SPAN |
| 26 | T1-C011 | 39835-39840 | 5 | 41395-41400;41670-41675;53521-53526 | 137 | WORD_SPAN |

### Session S6 (code [1179648,1245184), session_id=1007) — 12 flaws + 20 honest = 32 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 46799-46812 | 13 | 47471-47484;65088-65101 | 156 | WORD_SPAN |
| 1 | FLAW-01 | 36291-36294 | 3 | 36344-36347;36462-36465 | 144 | WORD_SPAN |
| 2 | FLAW-02 | 35609-35621 | 12 | 44593-44605;44894-44906 | 150 | WORD_SPAN |
| 3 | FLAW-03 | 46422-46427 | 5 | 48760-48765;59405-59410 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 2258-2262 | 4 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 1507-1512 | 5 | 729-733;2344-2348 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 1571-1575 | 4 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 128-130 | 2 | 1500-1506;2251-2257 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 729-733 | 4 | — | 107 | WORD_SPAN |
| 9 | FLAW-09 | 912-918 | 6 | — | 114 | WORD_SPAN |
| 10 | FLAW-10 | 2258-2261 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 2259-2262 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C012 | 327-330 | 3 | 1667-1670;1728-1731;4345-4348 | 137 | WORD_SPAN |
| 13 | T1-C023 | 850-858 | 8 | 2578-2586;3370-3378;3950-3958 | 143 | WORD_SPAN |
| 14 | T1-C024 | 919-926 | 7 | 1240-1247;1263-1270;5456-5463 | 137 | WORD_SPAN |
| 15 | T1-C026 | 1240-1249 | 9 | 5736-5745;7409-7418;36697-36706 | 156 | WORD_SPAN |
| 16 | T1-C008 | 1500-1506 | 6 | 2251-2257;3342-3348;14157-14163 | 150 | WORD_SPAN |
| 17 | T1-C009 | 1513-1519 | 6 | 30082-30088;30100-30106;49082-49088 | 150 | WORD_SPAN |
| 18 | T1-C019 | 2578-2591 | 13 | 6295-6308;7877-7890;11694-11707 | 162 | WORD_SPAN |
| 19 | T1-C001 | 3349-3352 | 3 | 3484-3487;3615-3618;3686-3689 | 156 | WORD_SPAN |
| 20 | T1-C014 | 3370-3385 | 15 | 14178-14193;15430-15445;15829-15844 | 168 | WORD_SPAN |
| 21 | T1-C011 | 7221-7226 | 5 | 12242-12247;27925-27930;28505-28510 | 137 | WORD_SPAN |
| 22 | T1-C010 | 10005-10011 | 6 | 10460-10466;12416-12422;12801-12807 | 143 | WORD_SPAN |
| 23 | T1-C013 | 14218-14231 | 13 | 15470-15483;15869-15882;16317-16330 | 168 | WORD_SPAN |
| 24 | T1-C021 | 17440-17459 | 19 | 17514-17533;18439-18458;19154-19173 | 156 | WORD_SPAN |
| 25 | T1-C020 | 22294-22313 | 19 | 22511-22530;22601-22620;22992-23011 | 156 | WORD_SPAN |
| 26 | T1-C025 | 30351-30370 | 19 | 45917-45936;47065-47084;47657-47676 | 162 | WORD_SPAN |
| 27 | T1-C022 | 30485-30504 | 19 | 46069-46088;47286-47305;47706-47725 | 162 | WORD_SPAN |
| 28 | T1-C018 | 31504-31516 | 12 | 35610-35622;44593-44605;44894-44906 | 162 | WORD_SPAN |
| 29 | T1-C016 | 34508-34519 | 11 | 41139-41150;41734-41745;41965-41976 | 162 | WORD_SPAN |
| 30 | T1-C015 | 35805-35817 | 12 | 36005-36017;36142-36154;36308-36320 | 162 | WORD_SPAN |
| 31 | T1-C017 | 45712-45725 | 13 | 46797-46810;47471-47484;65088-65101 | 168 | WORD_SPAN |

### Session S7 (code [1245184,1310720), session_id=1008) — 12 flaws + 13 honest = 25 proposals

| seq | chunk_id/base | span | len | grounds | conf | kind |
|---|---|---|---|---|---|---|
| 0 | FLAW-00 | 28902-28908 | 6 | 29376-29382;31828-31834 | 138 | WORD_SPAN |
| 1 | FLAW-01 | 65362-65368 | 6 | 662-668;1196-1202 | 138 | WORD_SPAN |
| 2 | FLAW-02 | 3086-3091 | 5 | 3256-3261;25707-25712 | 125 | WORD_SPAN |
| 3 | FLAW-03 | 21547-21550 | 3 | 21987-21990;23234-23237 | 125 | WORD_SPAN |
| 4 | FLAW-04 | 146-149 | 3 | — | 255 | WORD_SPAN |
| 5 | FLAW-05 | 669-673 | 4 | 742-744;786-788 | 255 | WORD_SPAN |
| 6 | FLAW-06 | 1246-1251 | 5 | — | 255 | WORD_SPAN |
| 7 | FLAW-07 | 2989-2993 | 4 | 1784-1790;1947-1953 | 255 | WORD_SPAN |
| 8 | FLAW-08 | 742-744 | 2 | — | 107 | WORD_SPAN |
| 9 | FLAW-09 | 944-948 | 4 | — | 107 | WORD_SPAN |
| 10 | FLAW-10 | 669-672 | 3 | — | 126 | WORD_SPAN |
| 11 | FLAW-11 | 670-673 | 3 | — | 126 | WORD_SPAN |
| 12 | T1-C012 | 381-384 | 3 | 596-599;1062-1065;7687-7690 | 137 | WORD_SPAN |
| 13 | T1-C008 | 662-668 | 6 | 1196-1202;1867-1873;2080-2086 | 150 | WORD_SPAN |
| 14 | T1-C010 | 977-983 | 6 | 1387-1393;1515-1521;1751-1757 | 143 | WORD_SPAN |
| 15 | T1-C009 | 1203-1209 | 6 | 1274-1280;1345-1351;1905-1911 | 150 | WORD_SPAN |
| 16 | T1-C011 | 1720-1725 | 5 | 3087-3092;3256-3261;25707-25712 | 137 | WORD_SPAN |
| 17 | T1-C007 | 1784-1790 | 6 | 1947-1953;1999-2005;2452-2458 | 150 | WORD_SPAN |
| 18 | T1-C024 | 2420-2427 | 7 | 2459-2466;3043-3050;6899-6906 | 137 | WORD_SPAN |
| 19 | T1-C026 | 2459-2468 | 9 | 28763-28772;47467-47476;54348-54357 | 156 | WORD_SPAN |
| 20 | T1-C025 | 3600-3619 | 19 | 5257-5276;9522-9541;18878-18897 | 162 | WORD_SPAN |
| 21 | T1-C022 | 4894-4913 | 19 | 5858-5877;9692-9711;18947-18966 | 162 | WORD_SPAN |
| 22 | T1-C017 | 15815-15828 | 13 | 35796-35809;52065-52078;52364-52377 | 168 | WORD_SPAN |
| 23 | T1-C019 | 27167-27180 | 13 | 43233-43246 | 138 | WORD_SPAN |
| 24 | T1-C018 | 27718-27730 | 12 | 53626-53638;54065-54077;64459-64471 | 162 | WORD_SPAN |

## 9. Auditor checklist (B.2.6 — procedures any auditor runs from tape + committed spec)

**A1 — Spec-hash match.** `sha256sum WIRING_SPEC.md sealed/SEALED_FLAW_MANIFEST.md`
equals the parent-pinned hashes in `WIRING_HASHES.txt` (pinned at wiring time, 2026-09-21).
**A2 — Bit-for-bit re-run.** Run the parent's Zag teacher (`teacher.zag`) on (slice bytes,
session_id per §D W-06, empty history); the emitted TEACHER_MSG proposal bytes must equal
`wired/expected/S{i}.bin` exactly (spans, grounds, confidences, seq order, session_id,
FNV-1a-64 checksums).
**A3 — No RNG / wallclock / learning.** (a) `grep -riE 'rand|random|urandom|gettime|clock_gettime|rdtsc'`
over the teacher program text returns nothing; (b) N1–N3 hold by inspection of the state struct;
(c) N=5 reruns + M8 adversarial perturbations reproduce the §8 schedule byte-for-byte.
**A4 — §C evaluable and unfired.** From the tape alone, compute coverage / accept_rate /
maxconf_rate over every rolling 200-proposal window (§4.1); assert no window fires and no
single 255-proposal exceeds 5% of session stimulus. (Secondary: `grep -rn sealed` over all
learner-side code paths returns 0 — the manifest is unreachable from the learner.)
**A5 — Vocabulary integrity.** Every proposed span's bytes equal the entry's literal pattern;
every grounding span's bytes equal the same pattern (except false-confidence flaws, whose
contradictory grounds are the planted defect); no proposal carries a string payload, token id,
or embedding (§P iron rule 1 — checkable by field inspection).
**A6 — Appeal bound.** From the tape: no proposal seq has >2 APPEAL events; no session-dead span
is re-proposed; every APPEAL carries ≥1 new_evidence_ref not present in the original proposal.

