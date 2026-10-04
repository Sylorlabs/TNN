# COMMITORDER_1421.md

Wave: wave-20260930-1421pdt. Checkpoint: mid-wave (governance draft;
re-check at wave end after the coordinator commits preregs before
implementations).

## This wave's lanes

| Lane | ORDER.txt present | PREREG file committed | Implementation committed | Ordering status |
|---|---|---|---|---|
| integration | NO | not yet | not yet | UNVERIFIABLE ORDERING |
| mul_from_add | NO | not yet | not yet | UNVERIFIABLE ORDERING |
| ddes | NO | not yet | not yet | UNVERIFIABLE ORDERING |
| devang | NO | not yet | not yet | UNVERIFIABLE ORDERING |
| trades | NO | not yet | not yet | UNVERIFIABLE ORDERING |
| sensory | NO | not yet | not yet | UNVERIFIABLE ORDERING |

Lane directories contain only NAMECHECK.md (integration, ddes,
trades, sensory) or are empty (mul_from_add, devang). No prereg and
no implementation has been committed by any lane yet this wave, so
no ordering can be verified. Per the wave's standing rule the
coordinator commits centrally at wave end with preregs before
implementations; governance must re-run this check on the committed
range before any verdict is adopted. The prereg-first invariant is
NON-NEGOTIABLE: any lane whose prereg cannot be shown to predate its
code stays UNVERIFIABLE ORDERING, and any verdict depending on that
lane's implementation cannot be adopted that wave.

## Inherited: pre-wave landings (commit order verified this wave)

The CLA-2, CAM-1, and ACT landings were committed before this wave
started (commits e639904f2, 371d20743, f7d87938f). Their frozen
preregs were committed earlier the same day (2026-09-30):

- CLA-2: prereg 24351fd31 ("prereg only, no implementation") is an
  ancestor of implementation e639904f2. ORDER VERIFIED.
- CAM-1: prereg 68a41be8a ("design only, no implementation") is an
  ancestor of implementation 371d20743. ORDER VERIFIED.
- ACT: prereg 51a818141 ("prereg only, no implementation") is an
  ancestor of implementation f7d87938f. ORDER VERIFIED.

These three landings were measured in ARCH_ACCOUNTING_1421.md; the
accounting stands independently of wave-1421pdt ordering because the
order was verified on the committed range above.

## Action for wave end

Re-collect ORDER.txt from each lane (or derive order from the
coordinator's commit range with `git merge-base --is-ancestor`
checks), and update this document before debate. No verdict motion
may cite a lane implementation whose prereg-first order is
UNVERIFIABLE.

No em-dashes in this documentation.
