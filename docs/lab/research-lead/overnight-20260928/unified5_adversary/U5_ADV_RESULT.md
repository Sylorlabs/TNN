# U5-ADV RESULT: H-UNIFIED5 RED TEAM -- ALL FOUR ATTACKS FAIL

**Date:** 2026-09-29
**Prereg:** `unified5_adversary/PREREG_U5_ADV.md` (committed as
`916c64de1`, frozen before any attack code; this result strictly
descends from it)
**Harness:** `unified5_adversary/u5_adv.zag` (mechanism lines 1-1211
of `unified5_learn.zag` copied byte-verbatim, cmp-verified; only
`main()` replaced by the attack battery)
**Raw evidence:** `unified5_adversary/U5_ADV_RAW.txt`
(md5 `392ec8146e8a03f61418cdb55a6b23dd`, 3/3 byte-identical runs,
exit 0)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere, including harness and
analysis.

## Verdict: H-UNIFIED5 SURVIVES this red team

All four preregistered attacks fail. No kill or downgrade criterion
is met. The H-UNIFIED5 claims under test hold:

- The PARSE_GUARD skip-and-continue cannot produce a silent
  wrong-but-confident parse: every skipped byte is traced, and on
  trace-free inputs the parser is the original algorithm.
- The shape-overflow boundary is genuinely unreachable through every
  audited dispatch path: route_line classification withholds every
  bad shape before any handler parses.
- All 17/17 behaviors reproduce from committed sources; the frozen 16
  blocks are byte-identical to H-UNIFIED4.
- The diff contains only the three preregistered additions; the guard
  matches the frozen design exactly.

## Attack X-U5-1: guard wrong-but-confident parse -- FAILS

Twelve direct white-box parse_ints probes (32-byte out buffer so the
full recovery shape is observable). Results from U5_ADV_RAW.txt:

| Probe | Input | Values | PARSE_GUARD traces |
| P1 | "1,0x,0" | [1,0,0] | 1 (byte 120) |
| P2 | "x1,0,0" | [1,0,0] | 1 (byte 120) |
| P3 | "1,0,0x" | [1,0,0] | 1 (byte 120) |
| P4 | "1x2,0,0" | [1,2,0,0] | 1 (byte 120) |
| P5 | "12x34" | [12,34] | 1 (byte 120) |
| P6 | "1x,0,0" | [1,0,0,0] | 1 (byte 120) |
| P7 | "1,0,0" | [1,0,0] | 0 |
| P8 | ",1,0" | [0,1,0] | 0 (pre-existing comma behavior, see below) |
| P9 | "1 0,0" | [1,0,0] | 1 (byte 32) |
| P10 | "1,0,0;2" | [1,0,0,2] | 1 (byte 59) |
| P11 | "!!!" | [] (no values) | 3 (byte 33 x3) |
| P12 | "" | immediate return | 0 |

Kill-criterion assessment:

- (a) Hang: every probe terminated; all three full runs exit 0
  within the 30s timeout. No hang. NOT MET.
- (b) Wrong parse with zero traces: every input containing a
  non-digit non-comma byte fired exactly one trace per skipped byte
  (P11: 3 skips -> 3 traces). P8 (",1,0" -> [0,1,0], 0 traces) is
  the ORIGINAL algorithm's leading-comma behavior (empty first
  field -> v=0, comma consumed), identical in H-UNIFIED4 by
  construction (the guard branch never executes on comma input).
  Pre-existing, not introduced by H-UNIFIED5, unreachable via
  classification (field_kind returns -1 for leading commas). NOT MET.
- (c) Silent merge/split: junk between digits DOES split values
  ("12x34" -> [12,34]; "1x2,0,0" -> [1,2,0,0]; "1x,0,0" ->
  [1,0,0,0]) -- but every such split is accompanied by its
  PARSE_GUARD trace naming the exact byte. The recovery is
  best-effort and flagged, never silent. NOT MET.

Attack X-U5-1 FAILS. Honest boundary recorded: skip-and-continue
recovery is flagged by a text trace only; downstream consumers use
the recovered values with no programmatic anomaly flag beyond the
trace line. On classified dispatch paths this is unreachable
(field_kind rejects junk), so the residual risk is confined to
direct white-box callers.

Harness note (transparent): the first P3 probe passed hi=5 for the
6-byte string "1,0,0x", so the trailing 'x' was never examined and
the probe trivially passed with 0 traces. Caught on read-back,
corrected to hi=6, harness rebuilt, all three committed runs use
the corrected probe (P3 now shows the expected 1 trace).

## Attack X-U5-2: shape-overflow reachability -- FAILS

Eight dispatch battery cases through the REAL route_line +
main-style dispatch. Buffers at risk: lv 12B (3 slots), rv 8B
(2 slots) in handle_caus_learn / handle_caus_revise; v 12B
(3 slots) in handle_caus_query.

| Case | Line | route_line code | Handler called? |
| S1 | "1,0,0,5>9,9;1,0,0>9,9" (4-int left) | 5 AMBIGUOUS | no |
| S2 | "1,0,0>9,9,8;1,0,0>9,9" (3-int right) | 5 AMBIGUOUS | no |
| S3 | "1,0,0,5" (single 4-int tuple) | 5 AMBIGUOUS | no (not 4) |
| S4 | "1,0>9,9;1,0,0>9,9" (2-int left) | 5 AMBIGUOUS | no |
| S5 | "!1,0,0,5>9,9;1,0,0>9,9" (marked bad) | 0 WITHHOLD | no |
| S6 | "1,0,0>9,9;1,0,0>9,9" (valid control) | 2 CAUS_LEARN | yes, rc=1 (1 stored) |
| S8 | "10,20,30,40>50,60;1,0,0>9,9" (multi-digit 4-int) | 5 AMBIGUOUS | no |

Kill-criterion assessment: no bad shape routed to code 2, 4, or 6
in any case; every bad shape was withheld or marked ambiguous at
classification. The valid control routes and learns cleanly. No
crash, no hang, no silent wrong values through dispatch. KILL/DOWNGRADE
NOT MET. Attack X-U5-2 FAILS.

S7 (informational, preregistered as non-kill): direct parse_ints
call with a 4-number field "1,0,0,5" into a 16-byte view over a
canaried 32-byte buffer. Result: values [1,0,0,5], canary at
offset 12 clobbered to 5, canaries at 16/20/24/28 intact. This
proves the 4th set32 lands exactly at offset 12 -- past a real
12-byte lv buffer -- i.e. the shape overflow is REAL when
classification is bypassed. Additionally, an earlier harness run
with a 12-byte-exact view panicked fail-stop ("panic: slice index
out of bounds"), showing this runtime bounds-checks the write
rather than silently corrupting. The hazard is therefore fail-stop,
not silent corruption, AND unreachable through dispatch. It remains
exactly what H-UNIFIED5 documents: a pre-existing,
classification-unreachable boundary, unchanged.

## Attack X-U5-3: regression -- FAILS

Rebuilt `unified5_learn.zag` and `unified4_learn.zag` from committed
sources with the repo znc:

- Rebuilt u5 output md5 `edb2cd39a07333b61416cc2fee4db31e` ==
  committed UNIFIED5_RAW_OUTPUT.txt md5. 3/3 runs byte-identical.
- Rebuilt u4 output md5 `154d24b3d53ebce9c1739c998a89bc1f` ==
  committed UNIFIED4_RAW_OUTPUT.txt md5 (reproducibility of the
  baseline confirmed too).
- Rebuilt u5 output lines 2-125 vs rebuilt u4 output lines 2-125:
  cmp clean -- the 16 frozen blocks are byte-identical (K-U5-2
  independently reproduced).
- PARSE_GUARD occurrences in rebuilt u5 output: exactly 2, at lines
  127-128, both inside the K-U5-1 block (the trace itself and the
  PASS line naming it). K-U5-4 independently reproduced: the guard
  never fires on frozen inputs.

No KILL/DOWNGRADE criterion met. Attack X-U5-3 FAILS.

## Attack X-U5-4: source audit -- FAILS (no finding)

- `diff unified4_learn.zag unified5_learn.zag` (95 diff lines)
  contains ONLY: the header comment (v4 -> v5), the parse_ints
  guard, the capacity-policy comment block, the main() header
  emit, the K-U5-1 block, and the verdict lines. The else-branch
  of the guarded parse_ints is the original code verbatim
  (re-indented). No other mechanism logic is touched.
- The guard matches PREREG_UNIFIED5.md's frozen design exactly:
  condition `is_digit(b[i])==0 && b[i]!=44`, trace text and
  format, `i=i+1` advance, else-branch identical to the original.
- No test-answer literals: the only numeric constants in new code
  are byte 44 (the structural comma constant already used by the
  original) and byte 48 (digit base, pre-existing).
- `unified4_learn.zag` is untouched: git status clean for it, last
  commit touching it is `7048fc3e5` (the H-UNIFIED4 implementation).
- No Python in any new adversary file (grep clean; the word
  appears only in the "Pure Zag. No Python." purity statements).

Informational deviation (not a kill): the frozen K-U5-1 prereg
described the probe as `handle_caus_query(W7,"1,0,x")`; the
implementation probes `parse_ints("1,0x,0",0,5,pt)` directly,
skipping the handle_caus_query wrapper. The kill-bar essence is
preserved: the adversarial call returns (no hang), exactly one
PARSE_GUARD trace names byte 120, the parse recovers as [1,0,0],
and the valid control is guard-silent. Flagged here for lineage
honesty.

No DOWNGRADE criterion met. Attack X-U5-4 FAILS.

## Residual risks (honest, not kill-worthy)

1. Skip-and-continue recovery is flagged by text trace only; there
   is no programmatic anomaly flag on the recovered values. A
   direct white-box caller that ignores stdout could act on
   split/shifted values ("12x34" -> [12,34]). Confined to
   non-classified callers; all audited dispatch paths classify
   first.
2. The shape overflow is fail-stop (panic) rather than silent, but
   it is still a crash-class hazard if classification is ever
   bypassed. Defense remains single-layer (route_line field_kind).
3. K-U5-1's probe vehicle deviated from the prereg text (direct
   parse_ints instead of handle_caus_query); essence preserved,
   recorded above.

## Commit lineage

- Attack prereg: `916c64de1` (PREREG H-UNIFIED5 red team FROZEN,
  alone, before any attack code).
- This result: harness + raw evidence + result doc (this commit).
- Ordering verified via `git merge-base --is-ancestor 916c64de1
  <this-result>` before reporting upward.
