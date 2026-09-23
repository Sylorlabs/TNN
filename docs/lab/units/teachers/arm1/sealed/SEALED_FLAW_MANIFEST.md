# SEALED Flaw Manifest — FROZEN (parent-wired)

**SEALED — THE LEARNER NEVER SEES THIS FILE UNTIL SCORING.**
Handling: stored in `teachers/arm1/sealed/`; NO `@import` or file read of this directory
from any learner-side code path (auditor check A4-secondary: `grep -rn sealed` over learner
sources must return nothing). Leak → run invalid + fresh-slice rescore (T-4).

**Status: FROZEN — wired by the parent (Muse) on 2026-09-21.** 12 planted flaws per slice
(T-3: 4 wrong-span, 4 false-confidence, 2 missing-grounding, 2 plausible-false), placed by the
deterministic function in `FLAW_PLACEMENT.md`. Each flaw lists: exact span (slice-relative,
parent decision W-01), flaw type, the teacher's emitted §P proposal fields, and the EXPECTED
learner behavior (expected verdict + correct reason code). This document supersedes
`sealed/SEALED_FLAW_MANIFEST_DRAFT.md`.

**Scoring (T-5, parent-confirmed per W-05):** hit = expected verdict + correct reason code
(1.0); near-miss = expected verdict class right but code wrong, or the listed near-miss verdict
(0.5); false positive on a non-flaw proposal = −1.0; pass bar ≥ 10/12 per slice,
averaged over slices. Flaw scoring uses the learner's FIRST decision per flaw seq;
appeals are scored separately under cost (T-13).

Reason codes: R1 INSUFFICIENT_EVIDENCE · R2 CONFLICTS_PINNED · R3 PROTOCOL_VIOLATION ·
R4 INTEGRITY_GATE · R5 REDUNDANT · R6 APPEAL_EXHAUSTED (rejections);
SPAN_SHIFT · SPLIT · MERGE · GENERALIZE · NARROW (revisions); ADOPT/DEFER.

## Slice S0 (prose [2048,67584)) — slice_hash `b8150b41673e9543…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S0-00 | wrong-span | T1-P011 | 36100-36103 | 36097-36100 | `ck ` | 125 | 37236-37239;38256-38259 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-01 | wrong-span | T1-P014 | 48353-48355 | 48352-48354 | ` i` | 125 | 48400-48402;48435-48437 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-02 | wrong-span | T1-P009 | 27935-27939 | 27936-27940 | `hou ` | 125 | 28983-28987;29873-29877 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-03 | wrong-span | T1-P025 | 16357-16361 | 16354-16358 | `do l` | 163 | 18303-18307;18706-18710 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S0-04 | false-confidence | T1-P001 | 30-33 | 30-33 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S0-05 | false-confidence | T1-P002 | 107-110 | 107-110 | `and` | 255 | 612-614;631-633 | REJECT/R1 | REVISE/* |
| F-S0-06 | false-confidence | T1-P003 | 300-302 | 300-302 | `of` | 255 | — | REJECT/R1 | REVISE/* |
| F-S0-07 | false-confidence | T1-P004 | 701-703 | 701-703 | `to` | 255 | 880-884;2080-2084 | REJECT/R1 | REVISE/* |
| F-S0-08 | missing-grounding | T1-P005 | 612-614 | 612-614 | `my` | 101 | — | REJECT/R1 | DEFER/- |
| F-S0-09 | missing-grounding | T1-P006 | 8-10 | 8-10 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S0-10 | plausible-false | T1-P007 | 880-884 | 880-883 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S0-11 | plausible-false | T1-P007 | 880-884 | 881-884 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1001 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S0-00: seq=0 span=[36097,36100) ground_count=2 confidence=125
- F-S0-01: seq=1 span=[48352,48354) ground_count=2 confidence=125
- F-S0-02: seq=2 span=[27936,27940) ground_count=2 confidence=125
- F-S0-03: seq=3 span=[16354,16358) ground_count=2 confidence=163
- F-S0-04: seq=4 span=[30,33) ground_count=0 confidence=255
- F-S0-05: seq=5 span=[107,110) ground_count=2 confidence=255
- F-S0-06: seq=6 span=[300,302) ground_count=0 confidence=255
- F-S0-07: seq=7 span=[701,703) ground_count=2 confidence=255
- F-S0-08: seq=8 span=[612,614) ground_count=0 confidence=101
- F-S0-09: seq=9 span=[8,10) ground_count=0 confidence=107
- F-S0-10: seq=10 span=[880,883) ground_count=0 confidence=119
- F-S0-11: seq=11 span=[881,884) ground_count=0 confidence=119

## Slice S1 (prose [67584,133120)) — slice_hash `6870b11a18b9573e…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S1-00 | wrong-span | T1-P029 | 36081-36086 | 36079-36084 | `e dea` | 163 | 2788-2793;27787-27792 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-01 | wrong-span | T1-P025 | 30744-30748 | 30746-30750 | `ve, ` | 163 | 31004-31008;31025-31029 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-02 | wrong-span | T1-P035 | 20537-20541 | 20534-20538 | `no f` | 150 | 20751-20755;22006-22010 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-03 | wrong-span | T1-P016 | 41724-41727 | 41723-41726 | ` no` | 125 | 41872-41875;42331-42334 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S1-04 | false-confidence | T1-P001 | 212-215 | 212-215 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S1-05 | false-confidence | T1-P002 | 55-58 | 55-58 | `and` | 255 | 96-98;130-132 | REJECT/R1 | REVISE/* |
| F-S1-06 | false-confidence | T1-P003 | 288-290 | 288-290 | `of` | 255 | — | REJECT/R1 | REVISE/* |
| F-S1-07 | false-confidence | T1-P004 | 196-198 | 196-198 | `to` | 255 | 224-228;3063-3067 | REJECT/R1 | REVISE/* |
| F-S1-08 | missing-grounding | T1-P005 | 96-98 | 96-98 | `my` | 101 | — | REJECT/R1 | DEFER/- |
| F-S1-09 | missing-grounding | T1-P006 | 41-43 | 41-43 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S1-10 | plausible-false | T1-P007 | 224-228 | 224-227 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S1-11 | plausible-false | T1-P007 | 224-228 | 225-228 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1002 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S1-00: seq=0 span=[36079,36084) ground_count=2 confidence=163
- F-S1-01: seq=1 span=[30746,30750) ground_count=2 confidence=163
- F-S1-02: seq=2 span=[20534,20538) ground_count=2 confidence=150
- F-S1-03: seq=3 span=[41723,41726) ground_count=2 confidence=125
- F-S1-04: seq=4 span=[212,215) ground_count=0 confidence=255
- F-S1-05: seq=5 span=[55,58) ground_count=2 confidence=255
- F-S1-06: seq=6 span=[288,290) ground_count=0 confidence=255
- F-S1-07: seq=7 span=[196,198) ground_count=2 confidence=255
- F-S1-08: seq=8 span=[96,98) ground_count=0 confidence=101
- F-S1-09: seq=9 span=[41,43) ground_count=0 confidence=107
- F-S1-10: seq=10 span=[224,227) ground_count=0 confidence=119
- F-S1-11: seq=11 span=[225,228) ground_count=0 confidence=119

## Slice S2 (prose [133120,198656)) — slice_hash `fca4a9e16368c378…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S2-00 | wrong-span | T1-P007 | 34911-34915 | 34908-34912 | `of t` | 131 | 35048-35052;35088-35092 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-01 | wrong-span | T1-P016 | 52484-52487 | 52482-52485 | `t n` | 125 | 52654-52657;52688-52691 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-02 | wrong-span | T1-P030 | 18572-18577 | 18571-18576 | ` hear` | 163 | 25599-25604;34321-34326 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-03 | wrong-span | T1-P011 | 17815-17818 | 17812-17815 | `e, ` | 125 | 18123-18126;18359-18362 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S2-04 | false-confidence | T1-P001 | 610-613 | 610-613 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S2-05 | false-confidence | T1-P002 | 932-935 | 932-935 | `and` | 255 | 360-362;395-397 | REJECT/R1 | REVISE/* |
| F-S2-06 | false-confidence | T1-P003 | 552-554 | 552-554 | `of` | 255 | — | REJECT/R1 | REVISE/* |
| F-S2-07 | false-confidence | T1-P004 | 134-136 | 134-136 | `to` | 255 | 820-824;1721-1725 | REJECT/R1 | REVISE/* |
| F-S2-08 | missing-grounding | T1-P005 | 360-362 | 360-362 | `my` | 101 | — | REJECT/R1 | DEFER/- |
| F-S2-09 | missing-grounding | T1-P006 | 901-903 | 901-903 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S2-10 | plausible-false | T1-P007 | 820-824 | 820-823 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S2-11 | plausible-false | T1-P007 | 820-824 | 821-824 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1003 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S2-00: seq=0 span=[34908,34912) ground_count=2 confidence=131
- F-S2-01: seq=1 span=[52482,52485) ground_count=2 confidence=125
- F-S2-02: seq=2 span=[18571,18576) ground_count=2 confidence=163
- F-S2-03: seq=3 span=[17812,17815) ground_count=2 confidence=125
- F-S2-04: seq=4 span=[610,613) ground_count=0 confidence=255
- F-S2-05: seq=5 span=[932,935) ground_count=2 confidence=255
- F-S2-06: seq=6 span=[552,554) ground_count=0 confidence=255
- F-S2-07: seq=7 span=[134,136) ground_count=2 confidence=255
- F-S2-08: seq=8 span=[360,362) ground_count=0 confidence=101
- F-S2-09: seq=9 span=[901,903) ground_count=0 confidence=107
- F-S2-10: seq=10 span=[820,823) ground_count=0 confidence=119
- F-S2-11: seq=11 span=[821,824) ground_count=0 confidence=119

## Slice S3 (prose [198656,264192)) — slice_hash `51f4850286071d6b…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S3-00 | wrong-span | T1-P022 | 64707-64710 | 64704-64707 | `th ` | 125 | 209-212;258-261 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-01 | wrong-span | T1-P002 | 47417-47420 | 47415-47418 | `, a` | 138 | 47846-47849;48339-48342 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-02 | wrong-span | T1-P036 | 51262-51265 | 51263-51266 | `ng.` | 119 | 51283-51286;51447-51450 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-03 | wrong-span | T1-P024 | 60346-60348 | 60348-60350 | ` l` | 119 | 61544-61546;61558-61560 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S3-04 | false-confidence | T1-P001 | 9-12 | 9-12 | `the` | 255 | — | REJECT/R1 | REVISE/* |
| F-S3-05 | false-confidence | T1-P003 | 206-208 | 206-208 | `of` | 255 | 451-453;1710-1712 | REJECT/R1 | REVISE/* |
| F-S3-06 | false-confidence | T1-P004 | 35-37 | 35-37 | `to` | 255 | — | REJECT/R1 | REVISE/* |
| F-S3-07 | false-confidence | T1-P005 | 1319-1321 | 1319-1321 | `my` | 255 | 14582-14585;15091-15094 | REJECT/R1 | REVISE/* |
| F-S3-08 | missing-grounding | T1-P006 | 451-453 | 451-453 | `in` | 107 | — | REJECT/R1 | DEFER/- |
| F-S3-09 | missing-grounding | T1-P007 | 99-103 | 99-103 | `that` | 107 | — | REJECT/R1 | DEFER/- |
| F-S3-10 | plausible-false | T1-P007 | 99-103 | 99-102 | `tha` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S3-11 | plausible-false | T1-P007 | 99-103 | 100-103 | `hat` | 119 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1004 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S3-00: seq=0 span=[64704,64707) ground_count=2 confidence=125
- F-S3-01: seq=1 span=[47415,47418) ground_count=2 confidence=138
- F-S3-02: seq=2 span=[51263,51266) ground_count=2 confidence=119
- F-S3-03: seq=3 span=[60348,60350) ground_count=2 confidence=119
- F-S3-04: seq=4 span=[9,12) ground_count=0 confidence=255
- F-S3-05: seq=5 span=[206,208) ground_count=2 confidence=255
- F-S3-06: seq=6 span=[35,37) ground_count=0 confidence=255
- F-S3-07: seq=7 span=[1319,1321) ground_count=2 confidence=255
- F-S3-08: seq=8 span=[451,453) ground_count=0 confidence=107
- F-S3-09: seq=9 span=[99,103) ground_count=0 confidence=107
- F-S3-10: seq=10 span=[99,102) ground_count=0 confidence=119
- F-S3-11: seq=11 span=[100,103) ground_count=0 confidence=119

## Slice S4 (code [1048576,1114112)) — slice_hash `4e716f24770e2d10…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S4-00 | wrong-span | T1-C006 | 59258-59262 | 59257-59261 | ` els` | 131 | 1018-1022;2485-2489 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-01 | wrong-span | T1-C005 | 21569-21571 | 21566-21568 | `ue` | 131 | 21794-21796;23147-23149 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-02 | wrong-span | T1-C014 | 9449-9464 | 9447-9462 | `m(sqlite3_conte` | 156 | 14076-14091;3085-3100 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-03 | wrong-span | T1-C008 | 29735-29741 | 29736-29742 | `tatic ` | 138 | 25747-25753;25777-25783 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S4-04 | false-confidence | T1-C001 | 90-93 | 90-93 | `int` | 255 | — | REJECT/R1 | REVISE/* |
| F-S4-05 | false-confidence | T1-C002 | 352-356 | 352-356 | `void` | 255 | 562-564;798-800 | REJECT/R1 | REVISE/* |
| F-S4-06 | false-confidence | T1-C003 | 77-82 | 77-82 | `const` | 255 | — | REJECT/R1 | REVISE/* |
| F-S4-07 | false-confidence | T1-C004 | 10-14 | 10-14 | `char` | 255 | 18535-18541;19038-19044 | REJECT/R1 | REVISE/* |
| F-S4-08 | missing-grounding | T1-C007 | 18535-18541 | 18535-18541 | `return` | 114 | — | REJECT/R1 | DEFER/- |
| F-S4-09 | missing-grounding | T1-C009 | 4009-4015 | 4009-4015 | `struct` | 114 | — | REJECT/R1 | DEFER/- |
| F-S4-10 | plausible-false | T1-C002 | 352-356 | 352-355 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S4-11 | plausible-false | T1-C002 | 352-356 | 353-356 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1005 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S4-00: seq=0 span=[59257,59261) ground_count=2 confidence=131
- F-S4-01: seq=1 span=[21566,21568) ground_count=2 confidence=131
- F-S4-02: seq=2 span=[9447,9462) ground_count=2 confidence=156
- F-S4-03: seq=3 span=[29736,29742) ground_count=2 confidence=138
- F-S4-04: seq=4 span=[90,93) ground_count=0 confidence=255
- F-S4-05: seq=5 span=[352,356) ground_count=2 confidence=255
- F-S4-06: seq=6 span=[77,82) ground_count=0 confidence=255
- F-S4-07: seq=7 span=[10,14) ground_count=2 confidence=255
- F-S4-08: seq=8 span=[18535,18541) ground_count=0 confidence=114
- F-S4-09: seq=9 span=[4009,4015) ground_count=0 confidence=114
- F-S4-10: seq=10 span=[352,355) ground_count=0 confidence=126
- F-S4-11: seq=11 span=[353,356) ground_count=0 confidence=126

## Slice S5 (code [1114112,1179648)) — slice_hash `47c59a7aa1c9408b…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S5-00 | wrong-span | T1-C024 | 2010-2017 | 2013-2020 | `ITE_ENA` | 125 | 3513-3520;6305-6312 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-01 | wrong-span | T1-C006 | 64743-64747 | 64745-64749 | `se
#` | 131 | 64947-64951;65039-65043 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-02 | wrong-span | T1-C001 | 43690-43693 | 43691-43694 | `nt ` | 144 | 45291-45294;46193-46196 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-03 | wrong-span | T1-C014 | 18529-18544 | 18531-18546 | `lite3_context o` | 156 | 18627-18642;58899-58914 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S5-04 | false-confidence | T1-C002 | 9421-9425 | 9421-9425 | `void` | 255 | — | REJECT/R1 | REVISE/* |
| F-S5-05 | false-confidence | T1-C003 | 6100-6105 | 6100-6105 | `const` | 255 | 2067-2071;28145-28149 | REJECT/R1 | REVISE/* |
| F-S5-06 | false-confidence | T1-C004 | 7498-7502 | 7498-7502 | `char` | 255 | — | REJECT/R1 | REVISE/* |
| F-S5-07 | false-confidence | T1-C005 | 1882-1884 | 1882-1884 | `if` | 255 | 15524-15530;34849-34855 | REJECT/R1 | REVISE/* |
| F-S5-08 | missing-grounding | T1-C007 | 17895-17901 | 17895-17901 | `return` | 114 | — | REJECT/R1 | DEFER/- |
| F-S5-09 | missing-grounding | T1-C008 | 15524-15530 | 15524-15530 | `static` | 114 | — | REJECT/R1 | DEFER/- |
| F-S5-10 | plausible-false | T1-C002 | 9421-9425 | 9421-9424 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S5-11 | plausible-false | T1-C002 | 9421-9425 | 9422-9425 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1006 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S5-00: seq=0 span=[2013,2020) ground_count=2 confidence=125
- F-S5-01: seq=1 span=[64745,64749) ground_count=2 confidence=131
- F-S5-02: seq=2 span=[43691,43694) ground_count=2 confidence=144
- F-S5-03: seq=3 span=[18531,18546) ground_count=2 confidence=156
- F-S5-04: seq=4 span=[9421,9425) ground_count=0 confidence=255
- F-S5-05: seq=5 span=[6100,6105) ground_count=2 confidence=255
- F-S5-06: seq=6 span=[7498,7502) ground_count=0 confidence=255
- F-S5-07: seq=7 span=[1882,1884) ground_count=2 confidence=255
- F-S5-08: seq=8 span=[17895,17901) ground_count=0 confidence=114
- F-S5-09: seq=9 span=[15524,15530) ground_count=0 confidence=114
- F-S5-10: seq=10 span=[9421,9424) ground_count=0 confidence=126
- F-S5-11: seq=11 span=[9422,9425) ground_count=0 confidence=126

## Slice S6 (code [1179648,1245184)) — slice_hash `a09d298771e646cd…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S6-00 | wrong-span | T1-C017 | 46797-46810 | 46799-46812 | `lite3_mutex *` | 156 | 47471-47484;65088-65101 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-01 | wrong-span | T1-C001 | 36289-36292 | 36291-36294 | `t s` | 144 | 36344-36347;36462-36465 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-02 | wrong-span | T1-C018 | 35610-35622 | 35609-35621 | ` sqlite3_fre` | 150 | 44593-44605;44894-44906 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-03 | wrong-span | T1-C011 | 46423-46428 | 46422-46427 | ` whil` | 125 | 48760-48765;59405-59410 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S6-04 | false-confidence | T1-C002 | 2258-2262 | 2258-2262 | `void` | 255 | — | REJECT/R1 | REVISE/* |
| F-S6-05 | false-confidence | T1-C003 | 1507-1512 | 1507-1512 | `const` | 255 | 729-733;2344-2348 | REJECT/R1 | REVISE/* |
| F-S6-06 | false-confidence | T1-C004 | 1571-1575 | 1571-1575 | `char` | 255 | — | REJECT/R1 | REVISE/* |
| F-S6-07 | false-confidence | T1-C005 | 128-130 | 128-130 | `if` | 255 | 1500-1506;2251-2257 | REJECT/R1 | REVISE/* |
| F-S6-08 | missing-grounding | T1-C006 | 729-733 | 729-733 | `else` | 107 | — | REJECT/R1 | DEFER/- |
| F-S6-09 | missing-grounding | T1-C007 | 912-918 | 912-918 | `return` | 114 | — | REJECT/R1 | DEFER/- |
| F-S6-10 | plausible-false | T1-C002 | 2258-2262 | 2258-2261 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S6-11 | plausible-false | T1-C002 | 2258-2262 | 2259-2262 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1007 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S6-00: seq=0 span=[46799,46812) ground_count=2 confidence=156
- F-S6-01: seq=1 span=[36291,36294) ground_count=2 confidence=144
- F-S6-02: seq=2 span=[35609,35621) ground_count=2 confidence=150
- F-S6-03: seq=3 span=[46422,46427) ground_count=2 confidence=125
- F-S6-04: seq=4 span=[2258,2262) ground_count=0 confidence=255
- F-S6-05: seq=5 span=[1507,1512) ground_count=2 confidence=255
- F-S6-06: seq=6 span=[1571,1575) ground_count=0 confidence=255
- F-S6-07: seq=7 span=[128,130) ground_count=2 confidence=255
- F-S6-08: seq=8 span=[729,733) ground_count=0 confidence=107
- F-S6-09: seq=9 span=[912,918) ground_count=0 confidence=114
- F-S6-10: seq=10 span=[2258,2261) ground_count=0 confidence=126
- F-S6-11: seq=11 span=[2259,2262) ground_count=0 confidence=126

## Slice S7 (code [1245184,1310720)) — slice_hash `3ce0422a53b2a801…`

| flaw | type | base chunk | true span (rel) | flaw span (rel) | span bytes | conf | grounds (rel) | expected | near-miss |
|---|---|---|---|---|---|---|---|---|---|---|
| F-S7-00 | wrong-span | T1-C007 | 28905-28911 | 28902-28908 | `
  ret` | 138 | 29376-29382;31828-31834 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-01 | wrong-span | T1-C008 | 65364-65370 | 65362-65368 | `}
stat` | 138 | 662-668;1196-1202 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-02 | wrong-span | T1-C011 | 3087-3092 | 3086-3091 | ` whil` | 125 | 3256-3261;25707-25712 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-03 | wrong-span | T1-C012 | 21549-21552 | 21547-21550 | `r f` | 125 | 21987-21990;23234-23237 | REVISE/SPAN_SHIFT | REJECT/R1 |
| F-S7-04 | false-confidence | T1-C001 | 146-149 | 146-149 | `int` | 255 | — | REJECT/R1 | REVISE/* |
| F-S7-05 | false-confidence | T1-C002 | 669-673 | 669-673 | `void` | 255 | 742-744;786-788 | REJECT/R1 | REVISE/* |
| F-S7-06 | false-confidence | T1-C003 | 1246-1251 | 1246-1251 | `const` | 255 | — | REJECT/R1 | REVISE/* |
| F-S7-07 | false-confidence | T1-C004 | 2989-2993 | 2989-2993 | `char` | 255 | 1784-1790;1947-1953 | REJECT/R1 | REVISE/* |
| F-S7-08 | missing-grounding | T1-C005 | 742-744 | 742-744 | `if` | 107 | — | REJECT/R1 | DEFER/- |
| F-S7-09 | missing-grounding | T1-C006 | 944-948 | 944-948 | `else` | 107 | — | REJECT/R1 | DEFER/- |
| F-S7-10 | plausible-false | T1-C002 | 669-673 | 669-672 | `voi` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |
| F-S7-11 | plausible-false | T1-C002 | 669-673 | 670-673 | `oid` | 126 | — | REJECT/R1 | REVISE/SPAN_SHIFT |

Emitted §P fields per flaw (seq 0–11 in table order; all kind=1 WORD_SPAN, aux_count=0,
teacher_id=1, session_id=1008 (frozen test vector), magic=0x54505250, version=1,
checksum=FNV-1a-64):

- F-S7-00: seq=0 span=[28902,28908) ground_count=2 confidence=138
- F-S7-01: seq=1 span=[65362,65368) ground_count=2 confidence=138
- F-S7-02: seq=2 span=[3086,3091) ground_count=2 confidence=125
- F-S7-03: seq=3 span=[21547,21550) ground_count=2 confidence=125
- F-S7-04: seq=4 span=[146,149) ground_count=0 confidence=255
- F-S7-05: seq=5 span=[669,673) ground_count=2 confidence=255
- F-S7-06: seq=6 span=[1246,1251) ground_count=0 confidence=255
- F-S7-07: seq=7 span=[2989,2993) ground_count=2 confidence=255
- F-S7-08: seq=8 span=[742,744) ground_count=0 confidence=107
- F-S7-09: seq=9 span=[944,948) ground_count=0 confidence=107
- F-S7-10: seq=10 span=[669,672) ground_count=0 confidence=126
- F-S7-11: seq=11 span=[670,673) ground_count=0 confidence=126

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

