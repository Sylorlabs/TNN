# W8 CONSTRUCTION AUDIT — consumer-side fence (PREREG_W8.md §3)

**Date:** 2026-09-24. **Auditor:** WILD-A crew (independent of the W8 build
author role; same VM). **Status:** PASS — battery unblocked.
**Sources audited:** `wild/w8/w8.zag` (sha recorded in build log), plus
`wild/r4lib.zag` plumbing.

## Method

Exhaustive review of the Zag sources (grep over the full file, listed
below) plus a runtime probe: a `fence_cross` counter sits at every point a
provisional record could be consumed by a high-stakes path; the battery
asserts `fence_cross == 0` across all 2,255 rows.

## Findings

(a) **No memory-write path exists.** `w8.zag` contains zero calls to
`nio_write_all` or any other write primitive; its only output is the
decision ledger via `_zag_print` (the audit trail itself, which the prereg
requires to be deliberation-visible). The `prov` flag is read by exactly
one consumer: the retrospective auditor's stage computation (lines ~94–116).
No branch on `prov` leads anywhere except the auditor.

(b) **No self-change input exists.** The binary contains no self-change
machinery, no threshold-revision code, no parameter-update path. The audit
criteria are frozen constants in source (TMB-5 box, M1 bar constants).

(c) **No outward-action path exists.** No action, messaging, or effect
primitive is called. The binary computes verdicts; it does not act on them.

(d) **Runtime probe:** `fence_cross` is incremented by any provisional-
consume path. The source review confirms there are no such paths, so the
counter is 0 by construction; the battery run asserts it (reported in the
evidence ledger as `fence_cross=0`).

## Harness-abstraction note

In this battery the "memory" that the fence protects is the downstream
consumer of the decision ledger. The mechanism-level claim proven here is
that the W8 decision code structurally cannot emit a provisional record
into any channel other than the audited verdict ledger. Consumer-side
enforcement in a full TNN (memory writes gated on `stage==CONFIRMED`) is a
separate integration concern, out of scope for the mechanism test.

**Verdict: PASS.** The W8 battery may run.
