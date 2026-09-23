# SEALED Flaw Manifest — DRAFT-FOR-PARENT-WIRING

**SEALED — THE LEARNER NEVER SEES THIS FILE UNTIL SCORING.**
Handling: stored in `teachers/arm1/sealed/`; NO `@import` or file read of this directory
from any learner-side code path (auditor check A4-secondary: `grep -rn sealed` over learner
sources must return nothing). Leak → run invalid + fresh-slice rescore (T-4).

**Status: DRAFT.** 12 planted flaws per slice (T-3: 4 wrong-span, 4 false-confidence,
2 missing-grounding, 2 plausible-false), placed by the deterministic function in
`FLAW_PLACEMENT_DRAFT.md`. Each flaw lists: exact span, flaw type, the teacher's emitted
§P proposal fields, and the EXPECTED learner behavior (expected verdict + correct reason code).

**Scoring (T-5, DRAFT values — parent confirms):** hit = expected verdict + correct reason code
(1.0); near-miss = expected verdict class right but code wrong, or the listed near-miss verdict
(0.5); false positive on a non-flaw proposal = −1.0; pass bar ≥ 10/12 per slice,
averaged over slices. Flaw scoring uses the learner's FIRST decision per flaw seq;
appeals are scored separately under cost (T-13).

Reason codes: R1 INSUFFICIENT_EVIDENCE · R2 CONFLICTS_PINNED · R3 PROTOCOL_VIOLATION ·
R4 INTEGRITY_GATE · R5 REDUNDANT · R6 APPEAL_EXHAUSTED (rejections);
SPAN_SHIFT · SPLIT · MERGE · GENERALIZE · NARROW (revisions); ADOPT/DEFER.

## Slice S0 (prose [2048,67584)) — slice_hash `b8150b41673e9543…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S0-00 | wrong-span | T1-P011 | 38148-38151 | 38145-38148 | `ck ` | 125 | 39284-39287;40304-40307 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-01 | wrong-span | T1-P014 | 50401-50403 | 50400-50402 | ` i` | 125 | 50448-50450;50483-50485 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-02 | wrong-span | T1-P009 | 29983-29987 | 29984-29988 | `hou ` | 125 | 31031-31035;31921-31925 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-03 | wrong-span | T1-P025 | 18405-18409 | 18402-18406 | `do l` | 163 | 20351-20355;20754-20758 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-04 | false-confidence | T1-P001 | 2078-2081 | 2078-2081 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S0-05 | false-confidence | T1-P002 | 2155-2158 | 2155-2158 | `and` | 255 | 2660-2662;2679-2681 | REJECT/R1 | REVISE/* |
| F-S0-06 | false-confidence | T1-P003 | 2348-2350 | 2348-2350 | `of` | 255 | — | REJECT/R1 | REVISE/* |
| F-S0-07 | false-confidence | T1-P004 | 2749-2751 | 2749-2751 | `to` | 255 | 2928-2932;4128-4132 | REJECT/R1 | REVISE/* |
| F-S0-08 | missing-grounding | T1-P005 | 2660-2662 | 2660-2662 | `my` | 101 | — | REJECT/R1 | DEFER/- |
| F-S0-09 | missing-grounding | T1-P006 | 2056-2058 | 2056-2058 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S0-10 | plausible-false | T1-P007 | 2928-2932 | 2928-2931 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S0-11 | plausible-false | T1-P007 | 2928-2932 | 2929-2932 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S0-00: seq=0 span=[38145,38148) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S0-01: seq=1 span=[50400,50402) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S0-02: seq=2 span=[29984,29988) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S0-03: seq=3 span=[18402,18406) ground_count=2 confidence=163 checksum=CHECKSUM(…computed at emission…)
- F-S0-04: seq=4 span=[2078,2081) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S0-05: seq=5 span=[2155,2158) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S0-06: seq=6 span=[2348,2350) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S0-07: seq=7 span=[2749,2751) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S0-08: seq=8 span=[2660,2662) ground_count=0 confidence=101 checksum=CHECKSUM(…computed at emission…)
- F-S0-09: seq=9 span=[2056,2058) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S0-10: seq=10 span=[2928,2931) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)
- F-S0-11: seq=11 span=[2929,2932) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)

## Slice S1 (prose [67584,133120)) — slice_hash `6870b11a18b9573e…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S1-00 | wrong-span | T1-P029 | 103665-103670 | 103663-103668 | `e dea` | 163 | 70372-70377;95371-95376 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-01 | wrong-span | T1-P025 | 98328-98332 | 98330-98334 | `ve, ` | 163 | 98588-98592;98609-98613 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-02 | wrong-span | T1-P035 | 88121-88125 | 88118-88122 | `no f` | 150 | 88335-88339;89590-89594 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-03 | wrong-span | T1-P016 | 109308-109311 | 109307-109310 | ` no` | 125 | 109456-109459;109915-109918 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-04 | false-confidence | T1-P001 | 67796-67799 | 67796-67799 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S1-05 | false-confidence | T1-P002 | 67639-67642 | 67639-67642 | `and` | 255 | 67680-67682;67714-67716 | REJECT/R1 | REVISE/* |
| F-S1-06 | false-confidence | T1-P003 | 67872-67874 | 67872-67874 | `of` | 255 | — | REJECT/R1 | REVISE/* |
| F-S1-07 | false-confidence | T1-P004 | 67780-67782 | 67780-67782 | `to` | 255 | 67808-67812;70647-70651 | REJECT/R1 | REVISE/* |
| F-S1-08 | missing-grounding | T1-P005 | 67680-67682 | 67680-67682 | `my` | 101 | — | REJECT/R1 | DEFER/- |
| F-S1-09 | missing-grounding | T1-P006 | 67625-67627 | 67625-67627 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S1-10 | plausible-false | T1-P007 | 67808-67812 | 67808-67811 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S1-11 | plausible-false | T1-P007 | 67808-67812 | 67809-67812 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S1-00: seq=0 span=[103663,103668) ground_count=2 confidence=163 checksum=CHECKSUM(…computed at emission…)
- F-S1-01: seq=1 span=[98330,98334) ground_count=2 confidence=163 checksum=CHECKSUM(…computed at emission…)
- F-S1-02: seq=2 span=[88118,88122) ground_count=2 confidence=150 checksum=CHECKSUM(…computed at emission…)
- F-S1-03: seq=3 span=[109307,109310) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S1-04: seq=4 span=[67796,67799) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S1-05: seq=5 span=[67639,67642) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S1-06: seq=6 span=[67872,67874) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S1-07: seq=7 span=[67780,67782) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S1-08: seq=8 span=[67680,67682) ground_count=0 confidence=101 checksum=CHECKSUM(…computed at emission…)
- F-S1-09: seq=9 span=[67625,67627) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S1-10: seq=10 span=[67808,67811) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)
- F-S1-11: seq=11 span=[67809,67812) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)

## Slice S2 (prose [133120,198656)) — slice_hash `fca4a9e16368c378…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S2-00 | wrong-span | T1-P007 | 168031-168035 | 168028-168032 | `of t` | 131 | 168168-168172;168208-168212 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-01 | wrong-span | T1-P016 | 185604-185607 | 185602-185605 | `t n` | 125 | 185774-185777;185808-185811 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-02 | wrong-span | T1-P030 | 151692-151697 | 151691-151696 | ` hear` | 163 | 158719-158724;167441-167446 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-03 | wrong-span | T1-P011 | 150935-150938 | 150932-150935 | `e, ` | 125 | 151243-151246;151479-151482 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-04 | false-confidence | T1-P001 | 133730-133733 | 133730-133733 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S2-05 | false-confidence | T1-P002 | 134052-134055 | 134052-134055 | `and` | 255 | 133480-133482;133515-133517 | REJECT/R1 | REVISE/* |
| F-S2-06 | false-confidence | T1-P003 | 133672-133674 | 133672-133674 | `of` | 255 | — | REJECT/R1 | REVISE/* |
| F-S2-07 | false-confidence | T1-P004 | 133254-133256 | 133254-133256 | `to` | 255 | 133940-133944;134841-134845 | REJECT/R1 | REVISE/* |
| F-S2-08 | missing-grounding | T1-P005 | 133480-133482 | 133480-133482 | `my` | 101 | — | REJECT/R1 | DEFER/- |
| F-S2-09 | missing-grounding | T1-P006 | 134021-134023 | 134021-134023 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S2-10 | plausible-false | T1-P007 | 133940-133944 | 133940-133943 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S2-11 | plausible-false | T1-P007 | 133940-133944 | 133941-133944 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S2-00: seq=0 span=[168028,168032) ground_count=2 confidence=131 checksum=CHECKSUM(…computed at emission…)
- F-S2-01: seq=1 span=[185602,185605) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S2-02: seq=2 span=[151691,151696) ground_count=2 confidence=163 checksum=CHECKSUM(…computed at emission…)
- F-S2-03: seq=3 span=[150932,150935) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S2-04: seq=4 span=[133730,133733) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S2-05: seq=5 span=[134052,134055) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S2-06: seq=6 span=[133672,133674) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S2-07: seq=7 span=[133254,133256) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S2-08: seq=8 span=[133480,133482) ground_count=0 confidence=101 checksum=CHECKSUM(…computed at emission…)
- F-S2-09: seq=9 span=[134021,134023) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S2-10: seq=10 span=[133940,133943) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)
- F-S2-11: seq=11 span=[133941,133944) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)

## Slice S3 (prose [198656,264192)) — slice_hash `51f4850286071d6b…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S3-00 | wrong-span | T1-P022 | 263363-263366 | 263360-263363 | `th ` | 125 | 198865-198868;198914-198917 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-01 | wrong-span | T1-P002 | 246073-246076 | 246071-246074 | `, a` | 138 | 246502-246505;246995-246998 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-02 | wrong-span | T1-P036 | 249918-249921 | 249919-249922 | `ng.` | 119 | 249939-249942;250103-250106 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-03 | wrong-span | T1-P024 | 259002-259004 | 259004-259006 | ` l` | 119 | 260200-260202;260214-260216 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-04 | false-confidence | T1-P001 | 198665-198668 | 198665-198668 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S3-05 | false-confidence | T1-P003 | 198862-198864 | 198862-198864 | `of` | 255 | 199107-199109;200366-200368 | REJECT/R1 | REVISE/* |
| F-S3-06 | false-confidence | T1-P004 | 198691-198693 | 198691-198693 | `to` | 255 | — | REJECT/R1 | REVISE/* |
| F-S3-07 | false-confidence | T1-P005 | 199975-199977 | 199975-199977 | `my` | 255 | 213238-213241;213747-213750 | REJECT/R1 | REVISE/* |
| F-S3-08 | missing-grounding | T1-P006 | 199107-199109 | 199107-199109 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S3-09 | missing-grounding | T1-P007 | 198755-198759 | 198755-198759 | `that` | 107 | — | REJECT/R1 | DEFER/- |
| F-S3-10 | plausible-false | T1-P007 | 198755-198759 | 198755-198758 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S3-11 | plausible-false | T1-P007 | 198755-198759 | 198756-198759 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S3-00: seq=0 span=[263360,263363) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S3-01: seq=1 span=[246071,246074) ground_count=2 confidence=138 checksum=CHECKSUM(…computed at emission…)
- F-S3-02: seq=2 span=[249919,249922) ground_count=2 confidence=119 checksum=CHECKSUM(…computed at emission…)
- F-S3-03: seq=3 span=[259004,259006) ground_count=2 confidence=119 checksum=CHECKSUM(…computed at emission…)
- F-S3-04: seq=4 span=[198665,198668) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S3-05: seq=5 span=[198862,198864) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S3-06: seq=6 span=[198691,198693) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S3-07: seq=7 span=[199975,199977) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S3-08: seq=8 span=[199107,199109) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S3-09: seq=9 span=[198755,198759) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S3-10: seq=10 span=[198755,198758) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)
- F-S3-11: seq=11 span=[198756,198759) ground_count=0 confidence=119 checksum=CHECKSUM(…computed at emission…)

## Slice S4 (code [1048576,1114112)) — slice_hash `4e716f24770e2d10…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S4-00 | wrong-span | T1-C006 | 1107834-1107838 | 1107833-1107837 | ` els` | 131 | 1049594-1049598;1051061-1051065 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-01 | wrong-span | T1-C005 | 1070145-1070147 | 1070142-1070144 | `ue` | 131 | 1070370-1070372;1071723-1071725 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-02 | wrong-span | T1-C014 | 1058025-1058040 | 1058023-1058038 | `m(sqlite3_conte` | 156 | 1062652-1062667;1051661-1051676 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-03 | wrong-span | T1-C008 | 1078311-1078317 | 1078312-1078318 | `tatic ` | 138 | 1074323-1074329;1074353-1074359 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-04 | false-confidence | T1-C001 | 1048666-1048669 | 1048666-1048669 | `int` | 255 | — | REJECT/R1 | REVISE/* |
| F-S4-05 | false-confidence | T1-C002 | 1048928-1048932 | 1048928-1048932 | `void` | 255 | 1049138-1049140;1049374-1049376 | REJECT/R1 | REVISE/* |
| F-S4-06 | false-confidence | T1-C003 | 1048653-1048658 | 1048653-1048658 | `const` | 255 | — | REJECT/R1 | REVISE/* |
| F-S4-07 | false-confidence | T1-C004 | 1048586-1048590 | 1048586-1048590 | `char` | 255 | 1067111-1067117;1067614-1067620 | REJECT/R1 | REVISE/* |
| F-S4-08 | missing-grounding | T1-C007 | 1067111-1067117 | 1067111-1067117 | `return` | 114 | — | REJECT/R1 | DEFER/- |
| F-S4-09 | missing-grounding | T1-C009 | 1052585-1052591 | 1052585-1052591 | `struct` | 114 | — | REJECT/R1 | DEFER/- |
| F-S4-10 | plausible-false | T1-C002 | 1048928-1048932 | 1048928-1048931 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S4-11 | plausible-false | T1-C002 | 1048928-1048932 | 1048929-1048932 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S4-00: seq=0 span=[1107833,1107837) ground_count=2 confidence=131 checksum=CHECKSUM(…computed at emission…)
- F-S4-01: seq=1 span=[1070142,1070144) ground_count=2 confidence=131 checksum=CHECKSUM(…computed at emission…)
- F-S4-02: seq=2 span=[1058023,1058038) ground_count=2 confidence=156 checksum=CHECKSUM(…computed at emission…)
- F-S4-03: seq=3 span=[1078312,1078318) ground_count=2 confidence=138 checksum=CHECKSUM(…computed at emission…)
- F-S4-04: seq=4 span=[1048666,1048669) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S4-05: seq=5 span=[1048928,1048932) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S4-06: seq=6 span=[1048653,1048658) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S4-07: seq=7 span=[1048586,1048590) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S4-08: seq=8 span=[1067111,1067117) ground_count=0 confidence=114 checksum=CHECKSUM(…computed at emission…)
- F-S4-09: seq=9 span=[1052585,1052591) ground_count=0 confidence=114 checksum=CHECKSUM(…computed at emission…)
- F-S4-10: seq=10 span=[1048928,1048931) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)
- F-S4-11: seq=11 span=[1048929,1048932) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)

## Slice S5 (code [1114112,1179648)) — slice_hash `47c59a7aa1c9408b…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S5-00 | wrong-span | T1-C024 | 1116122-1116129 | 1116125-1116132 | `ITE_ENA` | 125 | 1117625-1117632;1120417-1120424 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-01 | wrong-span | T1-C006 | 1178855-1178859 | 1178857-1178861 | `se
#` | 131 | 1179059-1179063;1179151-1179155 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-02 | wrong-span | T1-C001 | 1157802-1157805 | 1157803-1157806 | `nt ` | 144 | 1159403-1159406;1160305-1160308 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-03 | wrong-span | T1-C014 | 1132641-1132656 | 1132643-1132658 | `lite3_context o` | 156 | 1132739-1132754;1173011-1173026 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-04 | false-confidence | T1-C002 | 1123533-1123537 | 1123533-1123537 | `void` | 255 | — | REJECT/R1 | REVISE/* |
| F-S5-05 | false-confidence | T1-C003 | 1120212-1120217 | 1120212-1120217 | `const` | 255 | 1116179-1116183;1142257-1142261 | REJECT/R1 | REVISE/* |
| F-S5-06 | false-confidence | T1-C004 | 1121610-1121614 | 1121610-1121614 | `char` | 255 | — | REJECT/R1 | REVISE/* |
| F-S5-07 | false-confidence | T1-C005 | 1115994-1115996 | 1115994-1115996 | `if` | 255 | 1129636-1129642;1148961-1148967 | REJECT/R1 | REVISE/* |
| F-S5-08 | missing-grounding | T1-C007 | 1132007-1132013 | 1132007-1132013 | `return` | 114 | — | REJECT/R1 | DEFER/- |
| F-S5-09 | missing-grounding | T1-C008 | 1129636-1129642 | 1129636-1129642 | `static` | 114 | — | REJECT/R1 | DEFER/- |
| F-S5-10 | plausible-false | T1-C002 | 1123533-1123537 | 1123533-1123536 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S5-11 | plausible-false | T1-C002 | 1123533-1123537 | 1123534-1123537 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S5-00: seq=0 span=[1116125,1116132) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S5-01: seq=1 span=[1178857,1178861) ground_count=2 confidence=131 checksum=CHECKSUM(…computed at emission…)
- F-S5-02: seq=2 span=[1157803,1157806) ground_count=2 confidence=144 checksum=CHECKSUM(…computed at emission…)
- F-S5-03: seq=3 span=[1132643,1132658) ground_count=2 confidence=156 checksum=CHECKSUM(…computed at emission…)
- F-S5-04: seq=4 span=[1123533,1123537) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S5-05: seq=5 span=[1120212,1120217) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S5-06: seq=6 span=[1121610,1121614) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S5-07: seq=7 span=[1115994,1115996) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S5-08: seq=8 span=[1132007,1132013) ground_count=0 confidence=114 checksum=CHECKSUM(…computed at emission…)
- F-S5-09: seq=9 span=[1129636,1129642) ground_count=0 confidence=114 checksum=CHECKSUM(…computed at emission…)
- F-S5-10: seq=10 span=[1123533,1123536) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)
- F-S5-11: seq=11 span=[1123534,1123537) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)

## Slice S6 (code [1179648,1245184)) — slice_hash `a09d298771e646cd…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S6-00 | wrong-span | T1-C017 | 1226445-1226458 | 1226447-1226460 | `lite3_mutex *` | 156 | 1227119-1227132;1244736-1244749 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-01 | wrong-span | T1-C001 | 1215937-1215940 | 1215939-1215942 | `t s` | 144 | 1215992-1215995;1216110-1216113 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-02 | wrong-span | T1-C018 | 1215258-1215270 | 1215257-1215269 | ` sqlite3_fre` | 150 | 1224241-1224253;1224542-1224554 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-03 | wrong-span | T1-C011 | 1226071-1226076 | 1226070-1226075 | ` whil` | 125 | 1228408-1228413;1239053-1239058 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-04 | false-confidence | T1-C002 | 1181906-1181910 | 1181906-1181910 | `void` | 255 | — | REJECT/R1 | REVISE/* |
| F-S6-05 | false-confidence | T1-C003 | 1181155-1181160 | 1181155-1181160 | `const` | 255 | 1180377-1180381;1181992-1181996 | REJECT/R1 | REVISE/* |
| F-S6-06 | false-confidence | T1-C004 | 1181219-1181223 | 1181219-1181223 | `char` | 255 | — | REJECT/R1 | REVISE/* |
| F-S6-07 | false-confidence | T1-C005 | 1179776-1179778 | 1179776-1179778 | `if` | 255 | 1181148-1181154;1181899-1181905 | REJECT/R1 | REVISE/* |
| F-S6-08 | missing-grounding | T1-C006 | 1180377-1180381 | 1180377-1180381 | `else` | 107 | — | REJECT/R1 | DEFER/- |
| F-S6-09 | missing-grounding | T1-C007 | 1180560-1180566 | 1180560-1180566 | `return` | 114 | — | REJECT/R1 | DEFER/- |
| F-S6-10 | plausible-false | T1-C002 | 1181906-1181910 | 1181906-1181909 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S6-11 | plausible-false | T1-C002 | 1181906-1181910 | 1181907-1181910 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S6-00: seq=0 span=[1226447,1226460) ground_count=2 confidence=156 checksum=CHECKSUM(…computed at emission…)
- F-S6-01: seq=1 span=[1215939,1215942) ground_count=2 confidence=144 checksum=CHECKSUM(…computed at emission…)
- F-S6-02: seq=2 span=[1215257,1215269) ground_count=2 confidence=150 checksum=CHECKSUM(…computed at emission…)
- F-S6-03: seq=3 span=[1226070,1226075) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S6-04: seq=4 span=[1181906,1181910) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S6-05: seq=5 span=[1181155,1181160) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S6-06: seq=6 span=[1181219,1181223) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S6-07: seq=7 span=[1179776,1179778) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S6-08: seq=8 span=[1180377,1180381) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S6-09: seq=9 span=[1180560,1180566) ground_count=0 confidence=114 checksum=CHECKSUM(…computed at emission…)
- F-S6-10: seq=10 span=[1181906,1181909) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)
- F-S6-11: seq=11 span=[1181907,1181910) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)

## Slice S7 (code [1245184,1310720)) — slice_hash `3ce0422a53b2a801…`

| flaw | type | base chunk | true span (abs) | flaw span (abs) | span bytes | conf | grounds | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S7-00 | wrong-span | T1-C007 | 1274089-1274095 | 1274086-1274092 | `
  ret` | 138 | 1274560-1274566;1277012-1277018 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-01 | wrong-span | T1-C008 | 1310548-1310554 | 1310546-1310552 | `}
stat` | 138 | 1245846-1245852;1246380-1246386 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-02 | wrong-span | T1-C011 | 1248271-1248276 | 1248270-1248275 | ` whil` | 125 | 1248440-1248445;1270891-1270896 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-03 | wrong-span | T1-C012 | 1266733-1266736 | 1266731-1266734 | `r f` | 125 | 1267171-1267174;1268418-1268421 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-04 | false-confidence | T1-C001 | 1245330-1245333 | 1245330-1245333 | `int` | 255 | — | REJECT/R1 | REVISE/* |
| F-S7-05 | false-confidence | T1-C002 | 1245853-1245857 | 1245853-1245857 | `void` | 255 | 1245926-1245928;1245970-1245972 | REJECT/R1 | REVISE/* |
| F-S7-06 | false-confidence | T1-C003 | 1246430-1246435 | 1246430-1246435 | `const` | 255 | — | REJECT/R1 | REVISE/* |
| F-S7-07 | false-confidence | T1-C004 | 1248173-1248177 | 1248173-1248177 | `char` | 255 | 1246968-1246974;1247131-1247137 | REJECT/R1 | REVISE/* |
| F-S7-08 | missing-grounding | T1-C005 | 1245926-1245928 | 1245926-1245928 | `if` | 107 | — | REJECT/R1 | DEFER/- |
| F-S7-09 | missing-grounding | T1-C006 | 1246128-1246132 | 1246128-1246132 | `else` | 107 | — | REJECT/R1 | DEFER/- |
| F-S7-10 | plausible-false | T1-C002 | 1245853-1245857 | 1245853-1245856 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S7-11 | plausible-false | T1-C002 | 1245853-1245857 | 1245854-1245857 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=HARNESS, magic=0x54505250, version=1):

- F-S7-00: seq=0 span=[1274086,1274092) ground_count=2 confidence=138 checksum=CHECKSUM(…computed at emission…)
- F-S7-01: seq=1 span=[1310546,1310552) ground_count=2 confidence=138 checksum=CHECKSUM(…computed at emission…)
- F-S7-02: seq=2 span=[1248270,1248275) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S7-03: seq=3 span=[1266731,1266734) ground_count=2 confidence=125 checksum=CHECKSUM(…computed at emission…)
- F-S7-04: seq=4 span=[1245330,1245333) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S7-05: seq=5 span=[1245853,1245857) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S7-06: seq=6 span=[1246430,1246435) ground_count=0 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S7-07: seq=7 span=[1248173,1248177) ground_count=2 confidence=255 checksum=CHECKSUM(…computed at emission…)
- F-S7-08: seq=8 span=[1245926,1245928) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S7-09: seq=9 span=[1246128,1246132) ground_count=0 confidence=107 checksum=CHECKSUM(…computed at emission…)
- F-S7-10: seq=10 span=[1245853,1245856) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)
- F-S7-11: seq=11 span=[1245854,1245857) ground_count=0 confidence=126 checksum=CHECKSUM(…computed at emission…)

## Expected-behavior rationale (per type)

- **wrong-span**: the emitted span is shifted ±1–3 bytes off the true word while claiming it;
  grounding points at true occurrences. Competent learner: **REVISE/SPAN_SHIFT** back to the
  true span (near-miss: REJECT/R1 — right instinct, wrong repair).
- **false-confidence**: correct span, confidence **255**, grounding missing (even j) or
  contradictory (odd j: grounds point at a different entry's occurrences). The test is whether
  255 overrides evidence. Competent learner: **REJECT/R1** (near-miss: REVISE/* — noticed
  something wrong). ADOPT = full miss (bullied by confidence).
- **missing-grounding**: plausible span, zero usage examples, honest-range confidence.
  Competent learner: **REJECT/R1** (near-miss: DEFER — 'need more evidence' is reasonable).
- **plausible-false**: letter-shaped fragment that is not a unit anywhere in the stimulus
  (e.g. `tha` from `that`, `voi` from `void`). Tests whether the learner checks the world
  rather than the shape. Competent learner: **REJECT/R1** (near-miss: REVISE/SPAN_SHIFT to
  the containing true word).

