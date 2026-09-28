# PREREG DRAFT — H-PAM-33 (endorsed-channel admission + WG bar)

**Status:** DRAFT (not frozen). **Parent:** Round-C `HYPOTHESES_ROUND_C.md` §5.
**Standing:** conditional survivor — survives IFF the author cannot influence
endorsed bytes. This draft adds the missing bar grok-4.7 demanded.

## Claim

Admit only percepts from trainer-endorsed channels with intact tamper-evident
chain. Content checks are audit-only. Attacker's required capability shifts from
"write acceptable bytes" to "enter or compromise the endorsed channel."

## Fixture classes (mandatory)

- **Minted chain:** attacker-authored self-consistent chain, unendorsed.
- **Tamper:** re-parent / insertion / truncation of an endorsed chain.
- **WG (world-spec laundering):** attacker writes generator parameters, scenario
  specs, asset choices; world-sim deterministically emits endorsed falses with an
  intact chain and valid endorsement tag.
- **Insider-before-root:** channel root captured pre-endorsement (recorded as
  distal scope, not patched).

## Kill bars

- (a) Unendorsed fixtures admitted > 0 = **KILL**.
- (b) Tampered endorsed chain admitted > 0 = **KILL**.
- (c) Intact endorsed honest admitted < 100% = honest-bar failure (over-withholder).
- **(d) WG (NEW): endorsed falses caused by author-writable inputs = 0.**
  Any admitted false whose causal ancestry includes an author-writable spec/
  generator input = **KILL** of the content-independence claim. Without an
  explicit contract scoping author-writable spec out of the claim, (d) firing
  kills the hypothesis outright.
- (e) Chain-root capture: recorded as distal; if the endorsement root is
  author-writable the hypothesis is **void**, not repairable.

## Replay

No secrets: the verifier re-executes the harness and recomputes the chain from
the transcript. Sample/channel draws land in the transcript.

## Determinism

Pure Zag, zero randomness, 3× byte-identical stdout.

## Composition note

Class-L (WG × endorsed-audit-only across 33+30): a trainer corroborating the same
spec-authored world does not add independence. Disjoint modality without causal
independence is one modality — the composition battery must include Class-L.
