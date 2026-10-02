# REPORT.md - lane HPI, wave-20261002-1121pdt, queue item 3 (H5R3)

Task: implement the frozen H5R3 prereg (commits bfb01b47e / b675b1d5a):
test whether the H5R2 provenance gate sustains the DEP based revision chain
through FULL revert cycles (the H5R2 revision-chain-through-revert gap).

## Candidate

H5R3: zero-change evaluation of the frozen H5R2 substrate
(tnn3_h5r2.zag at 9db334bd4a, source SHA-256
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a)
through the frozen CY battery (6 cycle probes + 2 revert-after-revert
probes across 2 fresh sealed worlds) plus a post-freeze adversarial family.
No new cognition code: the hypothesis under test is a property of the
frozen substrate. Cost: one lane worker, pure Zag, safebin only.

## Numbers

- KB-S1 (substrate gate): PASS. Source hash match; diff vs H5R base shows
  exactly the t2_prov_ok gate (1 definition + 4 call sites); activate
  tag-20 hunk and promote_graph deletion hunk intact; 0/0 cognition-line
  delta; 3/3 byte-identical rebuilds reproducing the committed frozen
  binary (SHA-256 19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287).
- KB-W0: 32/32. KB-CY: 6/6. KB-RR: 2/2. KB-BCY: 18/18. KB-BRR: 6/6.
- KB-G3: PASS (byte-identical substrate; no modes/bridges/handlers/ISA
  additions; no forbidden ops; no time/clock/random in new code).
- KB-D3: 3/3 byte-identical per sealed world
  (y1 d7db929f..., y2 74df43ce...). KB-P3: PASS (safebin, python3 absent).
- Negative controls NC-1R3..NC-7R3: none fired. NC-0R3/NC-8R3: no void.
- Post-freeze adversarial family (99xxx keys): ADV-A snapshot/novel-value
  SURVIVES (novel 99399 derived via fresh MAP id 151); ADV-B back-to-back
  contradictions SURVIVES; ADV-C chain-link contradiction SURVIVES
  (NEWCHAIN ok=1; dead-chain verifying candidate declined). 3/3
  byte-identical (2483a501...).
- Prereg defect found and recorded: the prereg prints a 61-char malformed
  binary reference string; the operative KB-S1 gate is unaffected and the
  rebuild reproduces the true frozen binary byte-for-byte. Not a bar move.

## Keep / discard

KEEP: H5R3 ADVANCES. The H5R2 provenance gate sustains the revision chain
through full revert cycles on the tested worlds: the revert MAP is
superseded when its live licensing fact is contradicted, re-derivation
lands on the next live fact, and the revert-after-revert discriminator
(dead lowest-node-id candidate verifying first) anchors to the live
re-reverted fact. Nothing is promoted to canonical architecture: H5R3 is
an evaluation verdict on the frozen substrate, not a new mechanism; no
source change exists to promote. No L3 claim made.

## Commit ids (lane branch lane-hpi-20261002-1121pdt, local only)

- bfb01b47e / b675b1d5a: frozen prereg (prior wave; verified to strictly
  precede all implementation commits; no H5R3 implementation existed
  anywhere before this wave).
- 5d7e6691d: NAMECHECK Step 0 guard + KB-S1 verification.
- (this commit): CY_FRAG.zag + SMOKE_FRAG.zag + world files + run logs +
  SEALED_EVAL.md + REDTEAM_SELF.md + REPORT.md.

## Red-team findings

- The three prereg section 9 self-attacks are answered with evidence
  (selective not indiscriminate supersession; no starvation; structural
  not luck discrimination). Details in REDTEAM_SELF.md.
- Parent-requested attacks: (1) snapshot-vs-live: answered by ADV-A
  (novel value derived, not recalled) and ADV-C (chain live in both DEP
  links); (2) post-freeze adversarial revert: answered by ADV-A/ADV-B/
  ADV-C, all SURVIVE.
- Residual: single-worker adversary (no independent adversary lane
  assigned); re-teach separator family still open; no generality claim.

## Queued next

1. H5R3 is done this wave; no follow-on implementation needed (zero-change
   evaluation). If the coordinator wants independent reproduction from the
   committed source (frontier pipeline step 4), the world files and driver
   hashes above make it mechanical.
2. The re-teach separator family remains the named open gap in H5R2's
   scope; a fresh prereg plus fresh sealed worlds is the honest vehicle.
3. The malformed binary hash string in the frozen prereg should be noted
   in the wave ledger so future lanes do not trip on it; the valid
   reference is 19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287.
