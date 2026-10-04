# PREREG AMENDMENT A1 (POST-RESULTS, DISCLOSED)

Lane: `propertyzag/`. Filed AFTER the first results were observed, therefore
marked POST-RESULTS. It is not a silent bar change: the original twelve-code
battery is retained and its failure is reported alongside.

## A1.1 What the original battery could not see

`PZ-I01 .. PZ-I12` were all satisfied on a tnn2 arena whose sequence chain had
been severed (ARM11a): the runtime returned `execute(...) = 1` (SUCCESS) with a
value that differed from the intact program's, and the twelve-code battery
reported **zero** violations. That is the important result, not a nuisance: an
arena can be perfectly well formed by every structural criterion and still be
a corrupt structure, because the corruption is in the RELATION between the
owner and the owned program, not in any single record.

Reported finding, stated as such: **the twelve-code structural battery is
blind to semantic truncation of an owned program.** This is a limitation of
structural invariant checking in general, and it is why the lane also carries a
metamorphic and a differential arm.

## A1.2 The added invariant

**PZ-I13 STRUCTURE-OWNERSHIP / PROVENANCE CLOSURE.** For every live node whose
tag is the declared learned-structure tag:

1. its program root field must name a live node;
2. walking the program's control-flow relation from that root, following both
   the conditional opcode's branch targets and the sequence successor, must
   reach every fact the owner licenses through a provenance edge. Equivalently:
   the multiset of facts licensed by the closure must equal the multiset
   licensed by the owner.

Record shape: `code = 13, a = owner node, b = facts licensed by the closure,
c = facts licensed by the owner`.

This is the invariant the prereg's "structure ownership" bullet was reaching
for; it was under-specified and is now stated exactly.

## A1.3 Effect on the kill bars

- K3 is restated as "the battery must find at least one injected violation of
  each of I01..I09 and I11, and I13 on ARM11a". No bar was weakened: I13 is
  additive and its pass on the clean arena (ARM0, ARM7, 63 seeds) is required.
- K4 is unchanged and still requires zero violations on a clean arena. I13
  produces no false positive on ARM0 or on any of the 63 well-formed
  generator seeds, which is reported as evidence it is not vacuous.
- No prediction P1..P7 was altered. P3 and P4 are now detected by I13 and I11
  respectively rather than only demonstrated by the runtime's own behaviour.

## A1.4 Two smaller design corrections, also disclosed

1. **Frame-operand scan is rule-driven, not field-window-driven.** The first
   implementation scanned a fixed field window for operands `>= D_FBASE`. That
   produced a false positive on the frozen MAP node, whose field 2 holds a
   plain subject id (4101). The scan is now driven by the descriptor's
   conditional reference rule table, so a field a given tag uses as a plain
   value is never mistaken for a frame operand. Recorded because it is a
   battery change made after seeing a result.
2. **Descriptor field indices are i32 indices, not byte offsets.** The frozen
   core's `ng(W,n,f)` and `eg(W,e,f)` take BYTE offsets. The descriptor's
   node/edge field indices are i32 indices into the record, i.e. byte offset
   times 4. Mixing the two is a real hazard for any lane reusing this battery;
   it is documented in `pz_desc.zag`.

## A1.5 A defect in this lane's own first oracle, disclosed

The first version of `pz_or_vfy` wrote its verdict into `C[900]`, outside the
512-byte chain buffer it was handed. The differential arm immediately reported
`VFY disagree = 15/15`. The oracle, not the frozen implementations, was at
fault: `vfy_gen` and `vfy_spec` had agreed with each other on all 15 worlds and
both were right. Fixed by giving the oracle an explicit one-cell output
buffer. Reported because a differential harness that is only ever run against
one implementation would have "confirmed" the bug.