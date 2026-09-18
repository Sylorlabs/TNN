# R33 N13 independent static numerical oracles

Date: 2026-09-06. Revision: independently authored literal table V1.

Disposition: ORACLE AUTHORSHIP ONLY. NOT EXECUTED. NOT PREREGISTRATION APPROVAL.
Final source, native evaluator, configuration, design and execution bounds still
require the separately requested final review. F1/F2 resolutions are reported
as in progress by the author, not verified or approved by this document.

The native-only execution contract and the full initial review were read before
authorship. The initial review is retained unchanged. No current `ts_*`
implementation, fixture-builder output or evaluator output was used to generate
these expected values. Byte grouping and coordinate arithmetic were worked out
statically; no numerical program, Python, runtime import, reducer, compiler,
test, primary run, training or registry action was executed. Filesystem reads
and artifact hashing are operational inspection only. This is the sole new
file written for this request.

## 1. Normative interpretation and independence

Hex pairs in a payload column are literal bytes in increasing storage address
order. Concatenate a fixture's element rows in increasing element-index order
to obtain its COMPLETE raw payload; there is no implicit padding, separator,
terminator or byte swap. Width, count and payload length are independently
specified below. The eight-byte storage count is separate from the payload.

`low` and `high` are unsigned 32-bit WORDS, carried in a sufficiently wide
integer field. Every decimal value is nonnegative and at most 4294967295.
The first up-to-four little-endian bytes form `low`; bytes four through seven
form `high`. Absent bytes contribute zero. In particular, signed storage names
do NOT authorize sign extension, and widths below eight always have `high=0`.
Both hex and decimal columns are literal expectations, not calls to a decoder.

Float annotations name conventional binary32/binary64 BIT PATTERNS only.
There is no floating conversion, arithmetic, NaN equality, NaN canonicalization,
signaling behavior or recovered historical runtime-value claim. Compare the
integer words exactly, including the negative-zero sign and every NaN payload
byte. The two NaN signs and the patterns with the quiet bit clear are distinct
raw observations. No host float should be used to construct or compare them.

Coordinate tuples, shapes, strides and offsets in this document use decimal
integers. A coordinate's storage ELEMENT index is
`offset + sum(coordinate[axis] * stride[axis])`. The payload-relative byte offset
is that index times the storage width. These two units are never interchangeable.
The formula explains the tables; the future evaluator must compare against the
listed literals, not obtain expected indices/words by calling `ts_*`, by
flattening the tested view, or by reusing the implementation's indexing helper.

Accepted empty-offset and size/stride caps below are N13's intentionally narrow
candidate policy from the initial review. They are not assertions about every
view accepted by PyTorch. The saved v2.9.0 sources are semantic references,
not identification of the continuing parent's original PyTorch version.

## 2. Storage fixtures: exact metadata and raw words

For these standalone storage blobs, use the stated ID as the ASCII storage key
in both the storage PID and the single-key list. Use module `torch`, device
`cpu`, view metadata `None`, little-endian sysinfo, and the canonical magic and
version described in section 3. The category is storage. Integer/Boolean tensor
wrappers, when used, have both gradient flags false.

| ID | Storage name | Kind code | Width | Count | Payload bytes | Eight-byte count suffix |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| S-U8 | ByteStorage | 117 | 1 | 6 | 6 | `06 00 00 00 00 00 00 00` |
| S-I8 | CharStorage | 105 | 1 | 4 | 4 | `04 00 00 00 00 00 00 00` |
| S-I16 | ShortStorage | 105 | 2 | 5 | 10 | `05 00 00 00 00 00 00 00` |
| S-I32 | IntStorage | 105 | 4 | 6 | 24 | `06 00 00 00 00 00 00 00` |
| S-I64 | LongStorage | 105 | 8 | 5 | 40 | `05 00 00 00 00 00 00 00` |
| S-F32 | FloatStorage | 102 | 4 | 8 | 32 | `08 00 00 00 00 00 00 00` |
| S-F64 | DoubleStorage | 102 | 8 | 8 | 64 | `08 00 00 00 00 00 00 00` |
| S-B1 | BoolStorage | 98 | 1 | 4 | 4 | `04 00 00 00 00 00 00 00` |
| S-BR | BoolStorage | 98 | 1 | 4 | 4 | `04 00 00 00 00 00 00 00` |

S-BR is an intentionally synthetic RAW-TRANSPORT case with noncanonical Boolean
bytes. Its expected behavior is byte preservation, not conversion to true/false
and not a claim that a normal Torch Boolean constructor emits these bytes.
All 50 rows below expect successful raw-word access with sufficient resources.

| ID/index | Literal element bytes | low hex | low decimal | high hex | high decimal | Pattern note |
| --- | --- | --- | ---: | --- | ---: | --- |
| S-U8/0 | `00` | `00000000` | 0 | `00000000` | 0 | Zero |
| S-U8/1 | `01` | `00000001` | 1 | `00000000` | 0 | Unit byte |
| S-U8/2 | `2e` | `0000002e` | 46 | `00000000` | 0 | STOP-valued raw byte |
| S-U8/3 | `7f` | `0000007f` | 127 | `00000000` | 0 | Lower seven bits set |
| S-U8/4 | `80` | `00000080` | 128 | `00000000` | 0 | High bit set |
| S-U8/5 | `ff` | `000000ff` | 255 | `00000000` | 0 | All byte bits set |
| S-I8/0 | `80` | `00000080` | 128 | `00000000` | 0 | No sign extension |
| S-I8/1 | `ff` | `000000ff` | 255 | `00000000` | 0 | No sign extension |
| S-I8/2 | `7f` | `0000007f` | 127 | `00000000` | 0 | High bit clear |
| S-I8/3 | `00` | `00000000` | 0 | `00000000` | 0 | Zero |
| S-I16/0 | `00 00` | `00000000` | 0 | `00000000` | 0 | Zero |
| S-I16/1 | `34 12` | `00001234` | 4660 | `00000000` | 0 | Asymmetric bytes |
| S-I16/2 | `ff 7f` | `00007fff` | 32767 | `00000000` | 0 | High bit clear |
| S-I16/3 | `00 80` | `00008000` | 32768 | `00000000` | 0 | No sign extension |
| S-I16/4 | `ff ff` | `0000ffff` | 65535 | `00000000` | 0 | No sign extension |
| S-I32/0 | `00 00 00 00` | `00000000` | 0 | `00000000` | 0 | Zero |
| S-I32/1 | `67 45 23 01` | `01234567` | 19088743 | `00000000` | 0 | Asymmetric bytes |
| S-I32/2 | `ff ff ff 7f` | `7fffffff` | 2147483647 | `00000000` | 0 | High bit clear |
| S-I32/3 | `00 00 00 80` | `80000000` | 2147483648 | `00000000` | 0 | No sign extension |
| S-I32/4 | `ef cd ab 89` | `89abcdef` | 2309737967 | `00000000` | 0 | Asymmetric high-bit word |
| S-I32/5 | `ff ff ff ff` | `ffffffff` | 4294967295 | `00000000` | 0 | All low-word bits set |
| S-I64/0 | `00 00 00 00 00 00 00 00` | `00000000` | 0 | `00000000` | 0 | Zero |
| S-I64/1 | `ef cd ab 89 98 ba dc fe` | `89abcdef` | 2309737967 | `fedcba98` | 4275878552 | All eight byte positions distinguished |
| S-I64/2 | `ff ff ff ff ff ff ff 7f` | `ffffffff` | 4294967295 | `7fffffff` | 2147483647 | Bit 63 clear; lower 63 bits set |
| S-I64/3 | `00 00 00 00 00 00 00 80` | `00000000` | 0 | `80000000` | 2147483648 | Only bit 63 set |
| S-I64/4 | `ff ff ff ff ff ff ff ff` | `ffffffff` | 4294967295 | `ffffffff` | 4294967295 | All 64 bits set |
| S-F32/0 | `00 00 00 00` | `00000000` | 0 | `00000000` | 0 | Positive-zero pattern |
| S-F32/1 | `00 00 00 80` | `80000000` | 2147483648 | `00000000` | 0 | Negative-zero pattern |
| S-F32/2 | `00 00 80 3f` | `3f800000` | 1065353216 | `00000000` | 0 | Positive-one pattern |
| S-F32/3 | `00 00 80 7f` | `7f800000` | 2139095040 | `00000000` | 0 | Positive-infinity pattern |
| S-F32/4 | `45 23 c1 7f` | `7fc12345` | 2143363909 | `00000000` | 0 | Positive quiet-NaN pattern, payload retained |
| S-F32/5 | `45 23 c1 ff` | `ffc12345` | 4290847557 | `00000000` | 0 | Negative quiet-NaN pattern, payload retained |
| S-F32/6 | `01 00 80 7f` | `7f800001` | 2139095041 | `00000000` | 0 | NaN pattern with quiet bit clear |
| S-F32/7 | `01 00 00 00` | `00000001` | 1 | `00000000` | 0 | Subnormal bit pattern |
| S-F64/0 | `00 00 00 00 00 00 00 00` | `00000000` | 0 | `00000000` | 0 | Positive-zero pattern |
| S-F64/1 | `00 00 00 00 00 00 00 80` | `00000000` | 0 | `80000000` | 2147483648 | Negative-zero pattern |
| S-F64/2 | `00 00 00 00 00 00 f0 3f` | `00000000` | 0 | `3ff00000` | 1072693248 | Positive-one pattern |
| S-F64/3 | `00 00 00 00 00 00 f0 7f` | `00000000` | 0 | `7ff00000` | 2146435072 | Positive-infinity pattern |
| S-F64/4 | `ef cd ab 89 45 23 f9 7f` | `89abcdef` | 2309737967 | `7ff92345` | 2147033925 | Positive quiet-NaN pattern, both words retained |
| S-F64/5 | `ef cd ab 89 45 23 f9 ff` | `89abcdef` | 2309737967 | `fff92345` | 4294517573 | Negative quiet-NaN pattern, both words retained |
| S-F64/6 | `01 00 00 00 00 00 f0 7f` | `00000001` | 1 | `7ff00000` | 2146435072 | NaN pattern with quiet bit clear |
| S-F64/7 | `01 00 00 00 00 00 00 00` | `00000001` | 1 | `00000000` | 0 | Subnormal bit pattern |
| S-B1/0 | `00` | `00000000` | 0 | `00000000` | 0 | Canonical byte |
| S-B1/1 | `01` | `00000001` | 1 | `00000000` | 0 | Canonical byte |
| S-B1/2 | `01` | `00000001` | 1 | `00000000` | 0 | Repeated canonical byte |
| S-B1/3 | `00` | `00000000` | 0 | `00000000` | 0 | Canonical byte |
| S-BR/0 | `02` | `00000002` | 2 | `00000000` | 0 | Raw byte, not normalized |
| S-BR/1 | `7f` | `0000007f` | 127 | `00000000` | 0 | Raw byte, not normalized |
| S-BR/2 | `80` | `00000080` | 128 | `00000000` | 0 | Raw high bit retained |
| S-BR/3 | `ff` | `000000ff` | 255 | `00000000` | 0 | Raw byte, not normalized |

### Empty storage counterparts

Each following ID is a separate fixture with its own matching ASCII key,
correctly typed PID count zero, raw count `00 00 00 00 00 00 00 00`, and an
EXACTLY EMPTY payload. A storage-only open succeeds with `elements=0`, shape
`(0,)` and the N13 storage-only normalized stride `(0,)`. There is no successful
coordinate or raw-word expectation: access at `(0,)` must refuse.

| ID | Name | Width | Count | Payload bytes |
| --- | --- | ---: | ---: | ---: |
| E-U8 | ByteStorage | 1 | 0 | 0 |
| E-I8 | CharStorage | 1 | 0 | 0 |
| E-I16 | ShortStorage | 2 | 0 | 0 |
| E-I32 | IntStorage | 4 | 0 | 0 |
| E-I64 | LongStorage | 8 | 0 | 0 |
| E-F32 | FloatStorage | 4 | 0 | 0 |
| E-F64 | DoubleStorage | 8 | 0 | 0 |
| E-B1 | BoolStorage | 1 | 0 | 0 |

## 3. A16: fully pinned little-endian storage carrier

A16 is a separate `torch.IntStorage` with key `A16`, width 4, count 16 and a
64-byte payload. Its complete blob consists of R1, R2, R3, R4, R5, the count
suffix, and the payload below, in that exact order. No memo opcodes, optional
fields, framing opcodes or trailing bytes are present. These are inert byte
specifications, not instructions to unpickle, import or invoke anything.

R1: 15 bytes, magic LONG payload `6c fc 9c 46 f9 20 6a a8 50 19`.

```text
80 02 8a 0a 6c fc 9c 46 f9 20 6a a8 50 19 2e
```

R2: 6 bytes, serialization version 1001.

```text
80 02 4d e9 03 2e
```

R3: 100 bytes. Root fields are `protocol_version=1001`, `little_endian=True`
and `type_sizes={short:2,int:4,long:4}`. Each key is a BINUNICODE text value.

```text
80 02 7d 28
58 10 00 00 00 70 72 6f 74 6f 63 6f 6c 5f 76 65 72 73 69 6f 6e
4d e9 03
58 0d 00 00 00 6c 69 74 74 6c 65 5f 65 6e 64 69 61 6e
88
58 0a 00 00 00 74 79 70 65 5f 73 69 7a 65 73
7d 28
58 05 00 00 00 73 68 6f 72 74
4b 02
58 03 00 00 00 69 6e 74
4b 04
58 04 00 00 00 6c 6f 6e 67
4b 04
75 75 2e
```

R4: 55 bytes. A single BINPERSID referring to the six-item tuple
`(storage, torch.IntStorage, A16, cpu, 16, None)`; the class is an inert GLOBAL.

```text
80 02 28
58 07 00 00 00 73 74 6f 72 61 67 65
63 74 6f 72 63 68 0a 49 6e 74 53 74 6f 72 61 67 65 0a
58 03 00 00 00 41 31 36
58 03 00 00 00 63 70 75
4b 10 4e 74 51 2e
```

R5: 13 bytes, exactly one matching text key in a list.

```text
80 02 5d 58 03 00 00 00 41 31 36 61 2e
```

Count suffix: 8 bytes.

```text
10 00 00 00 00 00 00 00
```

Payload: concatenate the following 16 four-byte rows, in order. Their combined
length is 64 bytes. All high words are independently pinned to zero.

| Storage index | Payload-relative byte offset | Literal bytes | low hex | low decimal | high hex / decimal |
| ---: | ---: | --- | --- | ---: | --- |
| 0 | 0 | `00 00 00 80` | `80000000` | 2147483648 | `00000000` / 0 |
| 1 | 4 | `01 00 00 80` | `80000001` | 2147483649 | `00000000` / 0 |
| 2 | 8 | `02 00 00 80` | `80000002` | 2147483650 | `00000000` / 0 |
| 3 | 12 | `03 00 00 80` | `80000003` | 2147483651 | `00000000` / 0 |
| 4 | 16 | `04 00 00 80` | `80000004` | 2147483652 | `00000000` / 0 |
| 5 | 20 | `05 00 00 80` | `80000005` | 2147483653 | `00000000` / 0 |
| 6 | 24 | `06 00 00 80` | `80000006` | 2147483654 | `00000000` / 0 |
| 7 | 28 | `07 00 00 80` | `80000007` | 2147483655 | `00000000` / 0 |
| 8 | 32 | `08 00 00 80` | `80000008` | 2147483656 | `00000000` / 0 |
| 9 | 36 | `09 00 00 80` | `80000009` | 2147483657 | `00000000` / 0 |
| 10 | 40 | `0a 00 00 80` | `8000000a` | 2147483658 | `00000000` / 0 |
| 11 | 44 | `0b 00 00 80` | `8000000b` | 2147483659 | `00000000` / 0 |
| 12 | 48 | `0c 00 00 80` | `8000000c` | 2147483660 | `00000000` / 0 |
| 13 | 52 | `0d 00 00 80` | `8000000d` | 2147483661 | `00000000` / 0 |
| 14 | 56 | `0e 00 00 80` | `8000000e` | 2147483662 | `00000000` / 0 |
| 15 | 60 | `0f 00 00 80` | `8000000f` | 2147483663 | `00000000` / 0 |

Literal carrier offsets, relative to the start of THIS blob, not the enclosing
outer pickle/map:

| Item | Start | Length | Exclusive end |
| --- | ---: | ---: | ---: |
| R1 | 0 | 15 | 15 |
| R2 | 15 | 6 | 21 |
| R3 | 21 | 100 | 121 |
| R4 | 121 | 55 | 176 |
| PID key text `41 31 36` within R4 | 159 | 3 | 162 |
| R5 | 176 | 13 | 189 |
| Matching key text within R5 | 184 | 3 | 187 |
| Raw count | 189 | 8 | 197 |
| Raw payload | 197 | 64 | 261 |
| Whole blob | 0 | 261 | 261 |

Expected decoded kind/width/count are `105 / 4 / 16`; key length is 3.
The row's three hash inputs are the exact blob `[0,261)`, payload `[197,261)`
and PID-key bytes `[159,162)`. Their logical input lengths are `261,64,3`,
total `328` bytes. This total excludes SHA padding/scratch and the row output.
No digest value has been computed or invented here. For an outer blob beginning
at map offset B, the corresponding map offsets are B+197 and B+159; B is not
obtained from or confused with an element index.

## 4. Fixed view coordinate-to-storage-index expectations

All views in this table use A16 and admit a successful open unless explicitly
stated otherwise. Tensor wrappers use exactly six `_rebuild_tensor_v2` args,
false gradient and an empty no-argument OrderedDict hooks descriptor. The
storage object uses exactly one `_load_from_bytes` argument containing the blob.
Only serialized descriptor shapes are specified; no constructor is executed.

Every number to the right of an arrow is a STORAGE ELEMENT INDEX, not the
expected raw value. Expected words for that index are the literal A16 row in
section 3. This fixed-table lookup must not be replaced by reading the target
storage/view to discover the expected answer.

| ID / layout | Shape | Strides in elements | Offset | Elements | Literal coordinate -> storage-index expectations |
| --- | --- | --- | ---: | ---: | --- |
| V-SCALAR | `()` | `()` | 5 | 1 | `() -> 5` |
| V-R1 | `(3,)` | `(2,)` | 2 | 3 | `(0,) -> 2; (1,) -> 4; (2,) -> 6` |
| V-C contiguous | `(2,3)` | `(3,1)` | 1 | 6 | `(0,0) -> 1; (0,1) -> 2; (0,2) -> 3; (1,0) -> 4; (1,1) -> 5; (1,2) -> 6` |
| V-T transposed | `(3,2)` | `(1,3)` | 1 | 6 | `(0,0) -> 1; (0,1) -> 4; (1,0) -> 2; (1,1) -> 5; (2,0) -> 3; (2,1) -> 6` |
| V-G gapped | `(2,3)` | `(7,2)` | 1 | 6 | `(0,0) -> 1; (0,1) -> 3; (0,2) -> 5; (1,0) -> 8; (1,1) -> 10; (1,2) -> 12` |
| V-O overlapping | `(2,3)` | `(1,1)` | 2 | 6 | `(0,0) -> 2; (0,1) -> 3; (0,2) -> 4; (1,0) -> 3; (1,1) -> 4; (1,2) -> 5` |
| V-Z zero first stride | `(2,3)` | `(0,1)` | 4 | 6 | `(0,0) -> 4; (0,1) -> 5; (0,2) -> 6; (1,0) -> 4; (1,1) -> 5; (1,2) -> 6` |
| V-BCAST both strides zero | `(2,3)` | `(0,0)` | 15 | 6 | `(0,0) -> 15; (0,1) -> 15; (0,2) -> 15; (1,0) -> 15; (1,1) -> 15; (1,2) -> 15` |
| V-END exact last valid element | `(2,2)` | `(8,1)` | 6 | 4 | `(0,0) -> 6; (0,1) -> 7; (1,0) -> 14; (1,1) -> 15` |
| V-R3 | `(2,1,2)` | `(5,0,2)` | 1 | 4 | `(0,0,0) -> 1; (0,0,1) -> 3; (1,0,0) -> 6; (1,0,1) -> 8` |
| V-R4 | `(1,1,1,2)` | `(0,0,0,1)` | 14 | 2 | `(0,0,0,0) -> 14; (0,0,0,1) -> 15` |
| V-R5 | `(1,1,1,1,2)` | `(0,0,0,0,1)` | 14 | 2 | `(0,0,0,0,0) -> 14; (0,0,0,0,1) -> 15` |
| V-R6 | `(1,1,1,1,1,2)` | `(0,0,0,0,0,1)` | 14 | 2 | `(0,0,0,0,0,0) -> 14; (0,0,0,0,0,1) -> 15` |
| V-R7 | `(1,1,1,1,1,1,2)` | `(0,0,0,0,0,0,1)` | 14 | 2 | `(0,0,0,0,0,0,0) -> 14; (0,0,0,0,0,0,1) -> 15` |
| V-R8 | `(1,1,1,1,1,1,1,2)` | `(0,0,0,0,0,0,0,1)` | 14 | 2 | `(0,0,0,0,0,0,0,0) -> 14; (0,0,0,0,0,0,0,1) -> 15` |
| V-PRODUCT-MAX | `(4096,4096)` | `(0,0)` | 0 | 16777216 | `(0,0) -> 0; (4095,4095) -> 0` |
| V-STRIDE-MAX | `(1,)` | `(16777216,)` | 15 | 1 | `(0,) -> 15` |

V-PRODUCT-MAX is a metadata boundary with TWO fixed probes, not authorization
to enumerate or allocate 16777216 logical elements. Zero strides make its
storage occupancy one element. V-STRIDE-MAX distinguishes a legal unused
large stride on a singleton axis from a large addressed span.

Two separate eight-byte scalar probes bind scalar indexing to both raw words:

| ID | Storage | Shape / strides / offset | Coordinate | Storage index | Payload byte offset | low decimal | high decimal |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| V-L64 | S-I64 | `() / () / 1` | `()` | 1 | 8 | 2309737967 | 4275878552 |
| V-D64 | S-F64 | `() / () / 4` | `()` | 4 | 32 | 2309737967 | 2147033925 |

In particular, V-SCALAR returns index 5 and words `(2147483653,0)`, not index 0
or byte offset 20. V-G at `(1,2)` returns index 12 and `(2147483660,0)`.
V-O has six logical elements but four distinct storage indices; V-BCAST has
six logical elements but one distinct index. Neither changes A16's 64-byte
whole-storage extent or the row's three hash ranges.

### Empty tensor views: metadata success, no readable element

All cases below expect `elements=0`, preserve the SERIALIZED tensor strides,
and refuse every coordinate access. Do not assign a placeholder successful
index or raw zero word to an empty view. A rank-zero scalar is not empty.

| ID | Storage | Shape | Strides | Offset | Fixed refused probe |
| --- | --- | --- | --- | ---: | --- |
| V-E1 | A16 | `(0,)` | `(1,)` | 0 | `(0,)` |
| V-EFIRST | A16 | `(0,2,3)` | `(6,3,1)` | 16 | `(0,0,0)` |
| V-EMIDDLE | A16 | `(2,0,3)` | `(7,5,2)` | 16 | `(0,0,0)` |
| V-ELAST | A16 | `(2,3,0)` | `(3,1,1)` | 16 | `(0,0,0)` |
| V-EWIDE | A16 | `(16777216,16777216,0)` | `(0,0,0)` | 16 | `(0,0,0)` |
| V-EZERO | E-I32 | `(0,)` | `(1,)` | 0 | `(0,)` |

V-EWIDE requires recognizing the zero axis before a nonempty-product cap is
applied; its huge prefix product is NOT a reason to construct a large buffer.
Offset 16 on empty A16 is the last admitted offset under this N13 policy;
offset 17 must be refused at open. The eight E-* storage-only counterparts
instead have normalized stride zero, as stated in section 2.

## 5. Parameter and tensor flag oracles

Use S-F32 or S-F64 with tensor shape `(2,)`, stride `(1,)`, offset 0, and an
empty no-argument OrderedDict at BOTH tensor and parameter hooks positions.
Parameter wrapping adds exactly `(tensor, parameter_requires_grad, hooks)`.
For each storage, all four cases below admit the same indices `(0,)->0` and
`(1,)->1` and the corresponding fixed positive/negative-zero words above.

| ID | Serialized tensor flag | Serialized parameter flag | Expected tensor_grad | Expected effective grad |
| --- | --- | --- | ---: | ---: |
| P-00 | False | False | 0 | 0 |
| P-01 | False | True | 0 | 1 |
| P-10 | True | False | 1 | 0 |
| P-11 | True | True | 1 | 1 |

The two flags need not be equal. These are metadata/bit expectations, not
autograd, training, evaluation-mode or runtime-object reconstruction claims.
For an unwrapped floating tensor, effective grad equals its tensor flag.
For each of Byte/Char/Short/Int/Long/Bool storage, the false/false counterpart
is admitted; either true flag is a dtype/gradient semantic refusal. Integer
values 0/1 in place of actual Boolean nodes are grammar/type refusals, not
accepted alternate Boolean encodings.

## 6. Branch-focused negative expectations

The labels in this section are ORACLE OUTCOMES, not invented numeric API
constants. Before execution, the final evaluator/config must freeze a mapping
from each label to its actual public status and, where statuses are shared,
an observable failing stage/reason. SCAN-CAPACITY, ALLOCATION, BINDING and
COORDINATE outcomes must remain distinguishable. A generic nonzero/negative
status or a missing result is never a passing negative control. This document
does not claim that the pending F1/F2 API already satisfies these expectations.

Each row varies ONLY its stated condition from an otherwise admitted fixture.
All unrelated resource budgets have sufficient headroom. Shape/coordinate
controls start with a valid carrier/map; coordinate controls first require a
successful open and binding. Resource controls use otherwise valid inputs and
coordinates. Allocation and budget failure must never count as proof of a
parse, metadata, layout, binding or coordinate rejection.

### Header framing, frozen scanner and storage semantics

Unless otherwise stated, the baseline is A16. Recompute syntactic byte-string
lengths when replacing a text field; do not accidentally turn a semantic
mutation into a framing failure. Offsets in a mutated blob are not inherited
from the baseline after a length change.

| ID | Exact mutation / construction | Required outcome and failing branch |
| --- | --- | --- |
| N-H01 | Change R1's `80 02` to `80 03`, leaving the rest unchanged. | HEADER-PROTOCOL at the protocol-2 prefix admission gate; no metadata success. |
| N-H02 | Present exactly `80 02 8a 0a 6c 2e`, with NO following bytes, to the bounded header-record surface. | HEADER-OPERAND-TRUNCATION: LONG declares ten operand bytes but only two remain. The apparent STOP is inside the claimed operand, not a record terminator. |
| N-H03 | Present only `80 02 58 ff ff ff 7f 2e` to the bounded header-record surface. | HEADER-LENGTH: declared length 2147483647 exceeds the bounded remainder, before forming an operand slice. |
| N-H04 | Replace R2 with `80 02 4b 00 4b 01 2e`. | SCAN-STACK: lexical framing succeeds but STOP has two stack results. Not a version mismatch. |
| N-H05 | Replace R2 with `80 02 28 4b 01 2e`. | SCAN-MARK/STACK: lexical framing succeeds but a MARK remains open. |
| N-H06 | Replace R2 with `80 02 68 00 2e`. | SCAN-MEMO: GET of unbound slot zero, not allocation/capacity refusal. |
| N-H07 | Add `71 00` just before R1 STOP and use R2 `80 02 68 00 2e`. | SCAN-MEMO in R2: R1's memo MUST NOT survive the record boundary. R1 itself remains valid. |
| N-H08 | Replace R2 with `80 02 4d e9 03 71 80 2e`. | SCAN-CAPACITY/memo-slot: BINPUT 128 is outside 128 slots. Positive paired record `80 02 4d e9 03 71 7f 2e` admits version 1001. These exact indices pin the initial 128-slot candidate limit. |
| N-H09 | Replace R2 with `80 02 52 2e`. | HEADER-OPCODE: REDUCE byte 0x52 is outside the header lexer admission set. It must not reach callable execution or be credited as a metadata mismatch. |
| N-H10 | Change only R1 magic byte at blob offset 4 from `6c` to `6d`. | STORAGE-MAGIC after successful lexical/stack validation. |
| N-H11 | Replace R2 with `80 02 4d e8 03 2e` (integer 1000). | STORAGE-VERSION after successful scan, not HEADER-PROTOCOL. |
| N-H12 | Change sysinfo's `little_endian` value from Boolean True to Boolean False. | STORAGE-ENDIAN. A paired integer 1 instead of Boolean True must also refuse, for the Boolean-type requirement. |
| N-H13 | Change only sysinfo `type_sizes.long` from 4 to 8. | STORAGE-SYSINFO. Host C-long width does not override this serialized format field. |
| N-H14 | Change R4 class module from `torch` to `torch.` with a complete GLOBAL line and otherwise valid operand. | STORAGE-CLASS, NOT early STOP/framing rejection at the dot inside the GLOBAL operand. |
| N-H15 | Replace `IntStorage` with `HalfStorage`, preserving well-formed grammar. | STORAGE-UNSUPPORTED-TYPE before interpreting the raw bytes; not a claim that HalfStorage is generally corrupt. |
| N-H16 | Change PID location text from `cpu` to `cuda:0`, with correct text length. | STORAGE-DEVICE; no relocation or device operation. |
| N-H17 | Keep PID key `A16`; change only the R5 key text to `B16`. | STORAGE-KEY-MISMATCH, before count/payload acceptance. |
| N-H18 | Use an empty key, a 65-byte ASCII key, or key bytes `c2 80` (UTF-8 U+0080); apply each variant to both key occurrences. | STORAGE-KEY admission failure for length/ASCII policy respectively. These are THREE separate cases, not combined mutations. |
| N-H19 | Replace PID view metadata None with an empty tuple. | STORAGE-VIEW-METADATA: unsupported non-None metadata, even when empty. |
| N-H20 | Replace the single-key list with an empty list or a two-item list containing `A16` twice. | STORAGE-KEY-LIST cardinality refusal in each separate case. Duplicate text does not satisfy the exactly-one-item rule. |
| N-H21 | Replace PID count 16 by integer -1, with all other fields unchanged. | STORAGE-COUNT at signed metadata admission, before raw-length comparison. |
| N-H22 | In S-F64 replace PID count 8 by integer 2097153 while retaining its small payload. | STORAGE-COUNT-CAP: this exceeds 16777216/8, before payload comparison or a large allocation. |
| N-H23 | Keep A16 PID count 16; replace count suffix by `11 00 00 00 00 00 00 00`. | STORAGE-LENGTH/COUNT: raw count 17 disagrees with PID count 16. |
| N-H24 | Keep A16 PID count 16; replace count suffix by `00 00 00 00 00 00 00 80`. | STORAGE-LENGTH/COUNT: bit 63 set must not become a valid nonnegative storage count. |
| N-H25 | Delete A16's final payload byte, producing a 260-byte blob. | STORAGE-LENGTH: 63 payload bytes, not 64. |
| N-H26 | Append one `00` to A16, producing a 262-byte blob. | STORAGE-LENGTH: 65 payload bytes, not 64; trailing bytes are not ignored. |

H02/H03 specifically target the bounded header-record surface. Passing these
short inputs to a whole-blob API may trigger its minimum-length gate instead;
appending later records can let a malformed operand length consume their bytes.
Neither alternative proves the pinned operand branch. The final reviewed
harness must preserve the stated call boundary or mark that branch NOT COVERED.

Two positive framing companions are also required: a valid ByteStorage with
key `.` (literal key byte `2e` in BOTH text operands) and payload
`2e 80 02 52`, count 4; and the S-U8 payload already listed. The four companion
raw-word pairs are exactly `(46,0), (128,0), (2,0), (82,0)`. Dots inside text
and opcode-looking RAW bytes are data; they cannot end or execute a record.

### Tensor grammar, shape admission, addressing and ownership

| ID | Exact mutation / probe | Required outcome and failing branch |
| --- | --- | --- |
| N-T01 | `_load_from_bytes` with zero args; separately, with two args instead of one. | GRAMMAR-STORAGE-ARITY; no blob decode. |
| N-T02 | A tensor-v2 tuple with five args; separately, seven args including a final None. | GRAMMAR-TENSOR-ARITY. Optional metadata is outside the six-argument N13 candidate even when None. |
| N-T03 | A parameter tuple with two args; separately, four args. | GRAMMAR-PARAMETER-ARITY. |
| N-T04 | At either hooks position separately, replace the empty no-arg OrderedDict with None, an ordinary empty dict, or an OrderedDict descriptor taking one empty-list argument. | GRAMMAR-HOOKS for each variant; semantic emptiness does not replace the exact admitted descriptor grammar. |
| N-T05 | Add one nonempty hook entry or a BUILD/state attachment to an otherwise valid tensor/parameter/hooks descriptor, one target at a time. | GRAMMAR-STATE/HOOKS; no hook or stored state method executes. |
| N-T06 | Use an integer node with value 1 instead of a Boolean gradient flag. | GRAMMAR-BOOLEAN, not floating-dtype approval based on truthiness. |
| N-T07 | For each of the six nonfloating storage names, set tensor flag true; separately wrap a false-gradient tensor with parameter flag true. | STORAGE-GRADIENT-DTYPE; not successful metadata or a coordinate error. |
| N-L01 | A16 shape `(1,1,1,1,1,1,1,1,1)`, nine zero strides, offset 0. | LAYOUT-RANK: rank 9, regardless of one-element occupancy. |
| N-L02 | A16 shape `(2,3)`, strides `(3,)`, offset 1. | LAYOUT-RANK-MISMATCH before coordinate processing. |
| N-L03 | A16 shape `(-1,)`, stride `(0,)`, offset 0. | LAYOUT-DIMENSION: negative dimension. |
| N-L04 | A16 shape `(16777217,0)`, strides `(0,0)`, offset 0. | LAYOUT-DIMENSION-CAP even though there is a zero axis. |
| N-L05 | A16 shape `(1,)`, stride `(-1,)`, offset 0. | LAYOUT-STRIDE: negative stride, even though no step is needed. |
| N-L06 | V-STRIDE-MAX with stride changed to `(16777217,)`. | LAYOUT-STRIDE-CAP; paired legal stride 16777216 remains admitted. |
| N-L07 | A16 shape `(1,)`, stride `(0,)`, offset -1; separately offset 16777217. | LAYOUT-OFFSET-FIELD for negative/over-cap offset respectively, before occupancy proof. |
| N-L08 | V-SCALAR with offset changed to 16. | LAYOUT-STORAGE-BOUND: scalar needs one element, but index 16 is one past storage. |
| N-L09 | V-END with offset changed from 6 to 7. | LAYOUT-STORAGE-BOUND: greatest addressed index would be 16. Reject at open, not only when that coordinate is later requested. |
| N-L10 | A16 shape `(2,2)`, strides `(7,7)`, offset 2. | LAYOUT-STORAGE-BOUND: each individual contribution fits from offset 2, but their sum reaches index 16. |
| N-L11 | V-PRODUCT-MAX with shape changed to `(4096,4097)`, zero strides and offset 0. | LAYOUT-ELEMENT-CAP: literal logical count 16781312 exceeds 16777216 despite one-element storage occupancy. |
| N-L12 | V-EMIDDLE with offset changed from 16 to 17. | LAYOUT-EMPTY-OFFSET under N13's `offset <= count` policy. No coordinate read is attempted. |
| N-L13 | E-I32 with scalar shape `()`, strides `()`, offset 0. | LAYOUT-STORAGE-BOUND: rank zero is one element and cannot read empty storage. |
| N-C01 | Successfully open V-SCALAR; probe `(0,)` rather than `()`. | COORDINATE-RANK; binding must have succeeded first. |
| N-C02 | Successfully open V-C; probe `(-1,0)`, `(2,0)`, `(0,3)` separately. | COORDINATE-AXIS-BOUND for each. `(0,3)` must refuse even though its naive linear address 4 lies in storage. |
| N-C03 | Successfully open V-C; probe `(0,)` or `(0,0,0)` separately. | COORDINATE-RANK for too few/too many coordinates. |
| N-C04 | Successfully open each empty V-E* case; submit its fixed probe from section 4. | COORDINATE-EMPTY; no successful index or raw words, and no payload read. |
| N-B01 | Open a view normally, close the actual owning handle, then access through that cleared handle while its map remains live. | BINDING/CLOSED-VIEW, distinct from a coordinate refusal. No stale shallow copy is used. |
| N-B02 | Keep two separately owned, live, validated OUTER maps containing identical A16 blobs and storage descriptors; use a view opened against the first with the second. | BINDING/WRONG-MAP. Byte equality alone is not the required live association. The five-record A16 blob is not itself the outer map's single pickle stream. |

These ownership cases remain inside the trusted single-owner API contract;
they do not request arbitrary pointer forging, allocator reuse, use-after-free
of map memory, concurrent writers or a broader security campaign.

### Resource provenance and aggregate budgets

These are future branch controls, not requests to induce OOM or run stress
work now. A deterministic allocation-failure control needs a separately reviewed
native harness mechanism; absence of such a mechanism is NOT COVERED, not a
pass. Do not relabel an arbitrary crash/timeout as a deliberate refusal.

| ID | Isolated precondition / action | Exact required outcome |
| --- | --- | --- |
| N-R01 | Otherwise valid open; the first temporary header-map allocation is deliberately denied. | ALLOCATION at header-map initialization, not SCAN-CAPACITY or malformed-header success. No live result escapes. |
| N-R02 | Otherwise valid open; first shape-array allocation succeeds and the second is deliberately denied. | ALLOCATION; the first owned array is released and no live view escapes. |
| N-R03 | Valid live view and coordinate; an allocation required by binding revalidation is deliberately denied. | ALLOCATION, propagated through the access API, not BINDING or COORDINATE. |
| N-R04 | Valid row request; its output-buffer allocation is denied. | ALLOCATION with no owned successful row. |
| N-R05 | Valid row request; a SHA scratch allocation is denied after the row buffer exists. | ALLOCATION with the owned row buffer released; not row-format or coordinate refusal. |
| N-Q01 | Remaining open allowance 0, other allowances sufficient; make one otherwise valid public open request. | BUDGET-OPEN before any uncharged open work. No successful view. |
| N-Q02 | Remaining decode allowance 0, other allowances sufficient; request an otherwise valid operation that needs an uncached storage decode. | BUDGET-DECODE before that decode is performed; not a parse refusal. |
| N-Q03 | Open/bind prerequisites satisfied; remaining probe allowance 0; request V-SCALAR at `()`. | BUDGET-PROBE, not COORDINATE. The coordinate is valid and the expected index would have been 5. |
| N-Q04 | Valid view; remaining row allowance 0; request one row. | BUDGET-ROW; no successful owned output and no bypass by reopening another handle. |
| N-Q05 | First uncached A16 row; hash allowance 327 logical input bytes, other budgets sufficient. | BUDGET-HASH: full row needs 328 bytes. No successful row, and charged hashing must never exceed 327. Work already charged need not be rolled back. |
| N-Q06 | First uncached A16 row; hash allowance exactly 328 logical input bytes, other budgets sufficient. | Positive boundary: success, total hash input charged exactly 328, remaining allowance 0. This covers message bytes, not SHA padding. |
| N-Q07 | After consuming that 328-byte allowance, request a second uncached A16 row using a distinct handle under the SAME aggregate budget context. | BUDGET-HASH; opening/closing a view must not reset the aggregate allowance. No second successful row. |

For opens/decodes/probes/rows, the final public API must document its exact
charging surface, including nested binding work. At that surface, a one-unit
allowance must permit exactly one otherwise valid one-unit charge and refuse
the next; other budgets must be isolated. Do not infer that one high-level API
call necessarily consumes one unit of every nested counter. Freeze the actual
counter mapping in the final config before interpreting any control result.

Q05-Q07 deliberately fix the hash unit to logical bytes in the three A16
message ranges. Any planned digest cache or different hash-accounting unit
requires explicit final-review reconciliation; do not silently alter the
literal 261/64/3-byte oracle or treat cached work as an uncached test. Budget
refusal must leave a clear incomplete/refused result, never a success with
silently omitted probes, rows or hashes. Refused work must not modify input
bytes or the validated map. Retained output ownership must be bounded too.

## 7. Evidence identities and handoff

All paths below are relative to
`/Users/Shared/micah/Documents/TNN/TNN/`. Hashes identify the read files, not
executed code or a new source freeze. References were inspected as inert text.

| File | SHA-256 | Read scope used for authorship |
| --- | --- | --- |
| `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` | Full contract, read first. |
| `Research/R33_NATIVE_N13_TORCH_VIEWS/INDEPENDENT_INITIAL_REVIEW.md` | `1d6caae05614b1963470e706f5412a817882db24ccacdc4d2a3664489de9f83b` | Full 205-line review; retained unchanged. |
| `Research/R33_NATIVE_N13_TORCH_VIEWS/REFERENCES/torch_v2_9_0_storage.py.txt` | `ed06de01cc398ad7f428b472049f07944ae892aa1a10d88bd66bba97de4bc785` | Legacy storage-name mapping at 561-591; inert reduction definition at 1233-1244. |
| `Research/R33_NATIVE_N13_TORCH_VIEWS/REFERENCES/torch_v2_9_0_utils.py.txt` | `b52db634d2378395685499de1fbb2b3a1bef21bb87677d830792179b492edc75` | Tensor metadata/hooks at 170-244; parameter helper at 472-497; element-size rules at 891-906. |
| `Research/R33_NATIVE_N13_TORCH_VIEWS/REFERENCES/torch_v2_9_0_serialization.py.txt` | `7fe6755ba65409b510e75e0435a33f444c893a82ea817ff618a5be5943298a3c` | Constants at 54-67; legacy PID/sysinfo/record sequence at 1090-1143; loader text at 1720-1770 and 1800-1839. |
| `Research/R33_NATIVE_N13_TORCH_VIEWS/REFERENCES/torch_v2_9_0_serialization.cpp.txt` | `e960f3d18debb8642bcbdc6612831e0f67876a63647b3727e1cb86edda006d35` | Raw count/element writer and little-endian handling at 234-309. |

The reference attribution supports the storage names, legacy framing, count
units and helper argument meanings. The chosen payloads, unsigned words,
coordinates and mutations are independent synthetic oracle authorship, not
captured PyTorch execution or evidence about the parent's historical behavior.

Transfer these constants literally into the NEW bounded native N13 evaluator
only within its subsequently reviewed plan. Review the builder's output bytes
against the literal carrier/payload specifications rather than allowing the
builder and interpreter to agree on the same wrong encoding. Preserve this
table's identity in the final source/config evidence. Any discrepancy, omitted
case or proposed semantic change must remain explicit for final review; do not
rewrite expected answers to match observed implementation results.

No approval, launch, rerun, registry change or implementation change is granted
by this file. N12 remains consumed. Await the requested final source/evaluator/
config review before interpreting this authorship as anything beyond a static
oracle specification.
