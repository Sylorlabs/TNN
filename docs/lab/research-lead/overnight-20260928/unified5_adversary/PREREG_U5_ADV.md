# PREREG H-UNIFIED5 RED TEAM (U5-ADV): FROZEN ATTACK PLAN

**Date:** 2026-09-29
**Status:** FROZEN. No attack code exists yet. Any attack execution must
strictly descend from this commit.
**Target:** `unified5_learn.zag` (H-UNIFIED5, SURVIVES 17/17).
**Mission:** Independently attack the H-UNIFIED5 frontier claim. Assume it
is false. A successful attack KILLS or DOWNGRADES H-UNIFIED5.
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.

## Background

H-UNIFIED5 SURVIVES (17/17): parse_ints hardened with a PARSE_GUARD
skip-and-continue on non-digit/non-comma bytes; capacity boundary
documented; no learned-behavior change. The result doc claims:

- (C1) On valid inputs (digits and commas only) the guard never
  executes: behavior byte-identical to H-UNIFIED4.
- (C2) On invalid inputs the parser always advances: no hang possible.
- (C3) Every skipped byte emits an explicit PARSE_GUARD trace naming
  the byte value: the anomaly is visible, never silent.
- (C4) Skipped bytes do not consume output slots: "1,0x,0" parses as
  [1,0,0] with one PARSE_GUARD trace.
- (C5) The pre-existing shape contract (exactly 3 ints left, 2 right)
  is unchanged; the guard does not widen what counts as valid.
- (C6) Honest limitation (documented): too many VALID numbers
  ("1,0,0,5" into a 3-slot buffer) still overflows the fixed out
  buffer exactly as in H-UNIFIED4; claimed unreachable through every
  audited dispatch path because route_line classification (field_kind
  exact counts) guarantees the shape before handle_caus_learn /
  handle_caus_revise / handle_caus_query run.

## Attack X-U5-1: guard skip-and-continue wrong-but-confident parse

**Theory:** The guard recovers by skipping bytes without consuming
slots. Skipping can SPLIT one digit run into two values ("12x34" ->
[12,34]) or SHIFT all later values ("1x,0,0" -> [1,0,0,0]). The claim
is that the PARSE_GUARD trace always flags this, so no recovery is
silent. I will try to find an input where the recovered parse is
wrong AND no trace fires, or where the parser hangs.

**Method:** Attack harness `u5_adv.zag`: mechanism lines 1..N of
`unified5_learn.zag` copied byte-verbatim (cmp-verified), only
`main()` replaced. Direct white-box parse_ints probes with a 32-byte
out buffer (8 slots, so recovery shape is fully observable without
clobbering adjacent memory):

- P1 "1,0x,0" -> expect [1,0,0], exactly 1 trace (documented).
- P2 "x1,0,0" -> expect [1,0,0], exactly 1 trace.
- P3 "1,0,0x" -> expect [1,0,0], exactly 1 trace.
- P4 "1x2,0,0" -> observe shape ([1,2,0,0] + 1 trace predicted).
- P5 "12x34" -> observe ([12,34] + 1 trace predicted).
- P6 "1x,0,0" -> observe ([1,0,0,0] + 1 trace predicted).
- P7 "1,0,0" -> expect [1,0,0], 0 traces.
- P8 ",1,0" -> observe (pre-existing comma behavior, 0 traces predicted).
- P9 "1 0,0" (space byte 32) -> expect [1,0,0] + 1 trace naming byte 32.
- P10 "1,0,0;2" (semicolon inside field) -> expect [1,0,0,2] + 1 trace.
- P11 "!!!" -> expect [] + 3 traces, terminates.
- P12 "" (empty) -> expect immediate return, 0 traces.

**Kill criteria (any one KILLS/DOWNGRADES):**
- (a) Any probe fails to terminate within the run (hang) -> KILL.
- (b) Any probe yields values inconsistent with skip-and-continue
  semantics AND emits zero PARSE_GUARD traces -> DOWNGRADE (silent
  wrong parse).
- (c) A skipped byte causes a digit run to merge/split with no trace
  -> DOWNGRADE.
- If all probes terminate, every skip is traced, and trace-free
  inputs parse exactly as the original algorithm, the attack FAILS.

## Attack X-U5-2: shape-overflow reachability through dispatch

**Theory:** C6 admits the shape overflow but claims it is unreachable
because route_line's field_kind exact-count classification guarantees
3/2 shapes before any parse. I will try to drive a bad shape through
the REAL dispatch path (route_line -> handler, exactly as main()
does). Buffers: lv 12B (3 slots), rv 8B (2 slots) in
handle_caus_learn/handle_caus_revise; v 12B (3 slots) in
handle_caus_query.

**Method:** Same harness, dispatch battery. For each line: print
route_line code; if code==2 call handle_caus_learn as main() does;
if code==4 call handle_caus_query; operator lines via operator_route.

- S1 "1,0,0,5>9,9;1,0,0>9,9" (4-int left) -> predict code != 2.
- S2 "1,0,0>9,9,8;1,0,0>9,9" (3-int right) -> predict code != 2.
- S3 "1,0,0,5" (single 4-int tuple) -> predict code != 4 (expect 5).
- S4 "1,0>9,9;1,0,0>9,9" (2-int left) -> predict code != 2.
- S5 "!1,0,0,5>9,9;1,0,0>9,9" (marked bad shape) -> predict withhold.
- S6 "1,0,0>9,9;1,0,0>9,9" (valid control) -> predict code == 2.
- S7 direct bypass: handle_caus_learn(W,"1,0,0,5>9,9;1,0,0>9,9")
  WITHOUT route_line -> observe (predicts buffer overwrite past lv;
  INFORMATIONAL: proves the hazard is real if classification is ever
  bypassed; not a kill since main() always classifies first).
- S8 "10,20,30,40>50,60;1,0,0>9,9" multi-digit 4-int left -> predict
  code != 2.

**Kill criteria:**
- KILL iff any S1-S6/S8 line routes to code 2 or 4 (or operator 6)
  with a bad shape AND the handler writes past its fixed buffer
  (detected via canary values placed after lv/rv/v in the harness,
  checked after the call) or crashes/hangs.
- DOWNGRADE iff a bad shape reaches a handler without crashing but
  with silently wrong values and no trace.
- If every bad shape is withheld/ambiguous at classification and the
  valid control routes cleanly, the attack FAILS. S7 is informational
  only.

## Attack X-U5-3: regression (17/17 reproduction)

**Method:** Rebuild `unified5_learn.zag` and `unified4_learn.zag`
from committed sources with the repo znc. Run each 3x.

**Kill criteria:**
- KILL iff rebuilt u5 output md5 != edb2cd39a07333b61416cc2fee4db31e
  (committed UNIFIED5_RAW_OUTPUT.txt), or any of 3 runs differ.
- DOWNGRADE iff u5 output lines 2-125 differ from committed
  UNIFIED4_RAW_OUTPUT.txt lines 2-125 (frozen-block regression), or
  PARSE_GUARD appears outside the K-U5-1 block (K-U5-4 violation).
- Otherwise the attack FAILS.

## Attack X-U5-4: source audit

**Method:** Read, don't run.
- diff unified4_learn.zag vs unified5_learn.zag: must contain ONLY
  the three preregistered additions (header comment, parse_ints
  guard, capacity comment block, main() header emit, K-U5-1 block,
  verdict lines). Any other mechanism change -> DOWNGRADE.
- Guard text must match PREREG_UNIFIED5.md frozen design exactly
  (condition, trace format, advance, else-branch identical to
  original). Deviation -> DOWNGRADE.
- No test-answer literals in the guard or new code -> else finding.
- unified4_learn.zag byte-identical to its committed state.
- Record (informational): prereg K-U5-1 described the probe as
  handle_caus_query(W7,"1,0,x"); implementation probes parse_ints
  directly. Assess whether the kill-bar essence (guard fires, no
  hang, recovery, valid silent) is still tested.

**Kill criteria:** DOWNGRADE iff the diff shows undeclared mechanism
changes, the guard deviates from the frozen design, or u4 was
modified. Informational otherwise.

## Verdict rules

- Any KILL criterion met -> H-UNIFIED5 KILLED (or DOWNGRADED where
  the criterion says so).
- All four attacks fail -> H-UNIFIED5 SURVIVES this red team.
- Report honestly. Pure Zag throughout.

## Commit plan

1. This prereg (frozen, alone).
2. Attack harness + raw evidence + adversary result doc.
3. No amendment unless a harness bug is found; transparent if so.
