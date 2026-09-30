# COMMITORDER_BACKFILL_0821.md

Wave: wave-20260930-0821pdt. Backfill commit-order self-check for
today's 0805pdt prereg batch (no debate or run dir existed for those
waves; this wave verifies content-ordering from the commit record).

Rule: the prereg file's first commit must strictly precede the
implementation files' first commits (git log --diff-filter=A;
timestamp gaps under batch commits do not count; content ordering
does).

## (a) L3C v3

- Prereg: docs/lab/research-lead/overnight-20260928/l3c_v3/
  PREREG_L3C_V3.md first appears in 3124d2e9a (2026-09-30 15:14:36
  UTC, "Prereg: L3C v3 alternative-cover dispatch (L3C-V3-PREREG;
  FROZEN)").
- Implementation: docs/lab/research-lead/overnight-20260928/l3c_v3/
  l3c_v3.zag first appears in 3bfa0947c (2026-09-30 15:19:23 UTC,
  "Results: L3C v3 alternative-cover dispatch (L3C-V3-PASS; F2 blind
  spot closed, no OR case)").
- A git log -S probe over the l3c_v3 directory shows no earlier
  fragment: only 3124d2e9a (prereg) and 3bfa0947c (implementation)
  touch the mechanism content.
- Verdict: ORDER-VERIFIED. Prereg strictly precedes implementation.

## (b) CAUSAL-EDITADV

- Prereg: docs/lab/research-lead/overnight-20260928/causal_editadv/
  PREREG.md first appears in d71be66dc (2026-09-30 15:14:19 UTC,
  "Prereg: CAUSAL-EDITADV C0-C attack on diagnose-and-relax generality
  (FROZEN; committed alone)").
- Implementation: attackA.zag, attackB.zag, attackC.zag all first
  appear in 16c7665bd (2026-09-30 15:17:08 UTC, "CAUSAL-EDITADV attack
  implementation: 3 drivers vs frozen 4c233f82a mechanism (prereg
  d71be66dc)").
- Verdict: ORDER-VERIFIED. Prereg strictly precedes implementation.

## (c) OpScope compression

- Prereg: docs/lab/research-lead/overnight-20260928/learner_compress/
  PREREG_COMPRESS.md first appears in 08a0c0ac4 (2026-09-30 15:13:08
  UTC, "Prereg: OpScope compression via learner-owned structures
  (FROZEN; learner_compress)").
- Implementation: docs/lab/research-lead/overnight-20260928/
  learner_compress/compress_learn.zag first appears in 5722ff3a8
  (2026-09-30 15:20:22 UTC, "OpScope compression: COMPRESSION-PASS
  (compress_learn.zag; slice eliminated; 3/3 byte-identical)").
- Verdict: ORDER-VERIFIED. Prereg strictly precedes implementation.

## Summary

3/3 backfilled pairs ORDER-VERIFIED. No UNVERIFIABLE ORDERING in
this batch. These verdicts are adopted into this wave's debate slate
(M2) with the caveat that the 0805pdt waves had no debate and no run
dir; the commit-order evidence itself is now on record.

No em-dashes in this documentation.
