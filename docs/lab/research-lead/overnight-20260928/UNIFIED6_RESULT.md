# H-UNIFIED6 RESULT

Status: SURVIVES (20/20 in-binary checks; K-U6-3/4/5 external bars pass)
Date: 2026-09-29
Prereg: PREREG_UNIFIED6.md, md5 718ffc15f7f029d66779abebcdc97de2
Implementation: unified6_learn.zag
Raw output: UNIFIED6_RAW_OUTPUT.txt, md5 4d6eee84e8f058cadc544f61a44fddb0
Toolchain: znc 2026.07.0-dev (edition 2026)

## Mission

Push the unified learner beyond H-UNIFIED5 by (1) giving parse recovery a
programmatic anomaly result instead of only a text trace, and
(2) adding defense-in-depth against shape overflow at the handler layer,
while preserving all H-UNIFIED5 frozen behavior.

## Design (frozen in prereg, unchanged by implementation)

R1: parse_ints now returns i32. Return >= 0 = count of skipped non-digit
bytes (0 = clean parse). Return -1 = SHAPE_OVERFLOW: the field holds more
values than out can take (capacity = out.len/4); the parser stops at
capacity, emits one PARSE_SHAPE trace, and NEVER writes past out.len.
Skipped bytes consume no output slots (H-UNIFIED5 behavior kept). The
H-UNIFIED5 PARSE_GUARD text is emitted verbatim. On valid fitting input
the writes are identical to H-UNIFIED5.

R2: handler-level shape gates as a second defense layer (route_line
classification is the first). handle_caus_learn and handle_caus_revise
require each segment to be exactly 3-int > 2-int (field_kind checks on
both sides of the separator; missing separator fails the gt<0 check).
handle_caus_query requires exactly one 3-int tuple. Malformed input emits
USHAPE, is withheld/skipped, and is never parsed, never committed, and
never panics. A parse_ints return of -1 is also refused at the handler,
even though the exact field_kind gate makes it unreachable.

## Raw kill-bar outcomes

K-U6-1 (programmatic anomaly flag): parse_ints("1,0x,0") returns 1 with
recovered values [1,0,0]; parse_ints("1,0,0") returns 0 with [1,0,0];
parse_ints("!!!") returns 3 with all-zero output. PASS (asserted in code,
not scraped from stdout). The PARSE_GUARD text traces still fire
(1x byte 120, 3x byte 33), unchanged from H-UNIFIED5.

K-U6-2 (defense-in-depth): (a) 12-byte view over a 32-byte arena
canaried with -1431655766 parses "1,0,0,5" and returns -1 with values
[1,0,0] and all five canary words intact: no panic, no overflow write.
(b) Direct calls bypassing route_line: handle_caus_learn on two bad
segments stores 0 (two USHAPE traces); handle_caus_revise on a bad
segment stores 0 (one USHAPE trace); handle_caus_query on "1,0" returns
0 (QCAUS USHAPE WITHHOLD); handle_caus_learn on a missing-separator line
stores 0 (two USHAPE traces). PASS.

K-U6-3 (frozen regression): output lines 2 through 125 are byte-identical
to UNIFIED5_RAW_OUTPUT.txt lines 2-125 (cmp clean). Header line 1 differs
only by design (v5 -> v6 wording). The K-U5-1 block region is
byte-identical to H-UNIFIED5, including its PARSE_GUARD trace line.
All 16 frozen ntest checks pass. PASS.

K-U6-4 (determinism): three consecutive runs produce byte-identical
output (cmp run1 == run2 == run3, exit 0 each). PASS.

K-U6-5 (no spurious firing): zero PARSE_GUARD, zero PARSE_SHAPE, and zero
USHAPE occurrences on frozen output lines 2-125. The new layers never
fire on any frozen input. PASS.

## Governance disclosures

1. Prereg sweep: PREREG_UNIFIED6.md was written before implementation.
Its dedicated commit failed because a concurrent worker had already
committed the file inside H-CAUSALV3 prereg commit 7f535c115 (2026-09-29
23:25:38 +0000). The committed blob was verified byte-identical to the
working file (md5 718ffc15f7f029d66779abebcdc97de2 both sides) and
7f535c115 is a strict ancestor of HEAD. This sweep is disclosed, not
hidden; no duplicate prereg history was created.

2. Pure Zag: no Python anywhere in implementation, build, or verification.
All checks ran through the repo znc toolchain and shell cmp/grep/sed.

3. New checks are all explicit: no invented inputs are presented as
frozen; the new USHAPE/QCAUS/PARSE_SHAPE lines appear only in the new
K-U6-1/K-U6-2 blocks.

## Causal interpretation

The two H-UNIFIED5 residuals are closed. Parse recovery is now observable
programmatically: a caller that ignores stdout still learns that bytes
were skipped or that the field overflowed the buffer, because the anomaly
rides in the return value. Shape overflow is now defended at two layers:
classification-time field_kind checks (unchanged H-UNIFIED5 behavior on
the stream path) plus handler-time field_kind verification that refuses
malformed segments even when invoked directly. The parser itself is
capacity-safe by construction (cap = out.len/4, stop before write).

## Limitations and residual risks

1. The -1 return path at the handlers is unreachable by construction
(exact field_kind gate) and is tested only at the parser level (K-U6-2a).
A latent bug in field_kind could in principle let a shape through that
the parser then refuses; that combination is refused safely (-1 branch),
but no test exercises both layers firing together.

2. USHAPE skips are still text traces, not a programmatic code: the
anomaly-observability upgrade (R1) was applied to parse_ints, not to
handler skips. Handlers return stored counts (0 on refusal), which is
programmatic, but the reason (shape vs coherence vs full) is text-only.

3. Malformed segments are skipped, not repaired: a stream that
chronically sends bad shapes loses those episodes silently except for
the trace. This is the documented fail-safe choice (no fabricated data
enters the store), not a gap in the gate.

4. Classification remains unchanged: no new behavior on the route_line
path, by design.

## Classification

H-UNIFIED6 remains a bounded L2 learner: no new representation, no
procedure invention, no causal discovery is claimed. It hardens the
unified substrate that future invention mechanisms will build on.

## Commit lineage

H-UNIFIED6 implementation + raw output + this result doc committed
locally as commit <hash> on branch tnn-native-lab. Parent chain
verified to include prereg commit 7f535c115 as a strict ancestor.
Independent red team not yet spawned; scheduled by the coordinator.
