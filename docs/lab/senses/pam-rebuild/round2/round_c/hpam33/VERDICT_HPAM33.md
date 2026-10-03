# VERDICT — H-PAM-33 full battery (B-33)

**Date:** 2026-09-24
**Basis:** `RUNLOG_HPAM33.md` (7 modes × 3 runs, all byte-identical) against the
frozen bars of `PREREG_HPAM33_FROZEN.md` (commit `356e7ca8`). Bars applied
mechanically per the pre-registered verdict rule; no reinterpretation.

## Numbers vs bars

| Bar | Measurement | Verdict |
|---|---|---|
| (a) minted unendorsed admitted = 0 | 0/20 | HOLD |
| (b) tampered endorsed admitted = 0 | 0/0/0 (reparent/truncate/insert) | HOLD |
| (c) honest-loss ≤ 15% | 20/20 admitted (loss 0%) | HOLD |
| (d) WG: endorsed falses with author-writable ancestry = 0 | **20/20** (plain) and **20/20** (manifest variant) | **FIRES** |
| (e) insider root capture | 5/5 forged chains admitted | VOID-recorded (distal) |
| Class-L | 5/10 trials both-green | CONFIRMED |

## Verdict (pre-registered rule)

**(a)∧(b)∧(c) hold, (d) fires → H-PAM-33 is TESTED-killed as a
content-independence gate; it CONDITIONAL-survives as a channel-integrity
check with escape-(i) enforced externally.** This is exactly grok-4.7's
predicted outcome, now tested rather than asserted.

What the battery proves, beyond the prediction:

1. **Inside its model, H-PAM-33 works.** Bars (a)(b)(c) all hold: the channel
   gate shifts the attacker's required capability from "write acceptable
   bytes" to "enter or compromise the endorsed channel" — minted chains are
   refused, tampering breaks the chain, honest traffic flows with zero loss.
2. **The mechanism is label-blind.** The `wg_manifest` arm was the honest
   attempt to enforce escape-(i) inside the mechanism (source manifest bound
   into the endorsement tag). It fails for the reason grok named: the manifest
   labels are the harness's assertions, and the endorsement tag binds bytes,
   not causal truth. The author writes through an input the registry labels
   HARNESS; the check passes; the falses are admitted. Identical bytes and
   tags are admitted whether the ancestry is clean or author-written — the
   mechanism cannot distinguish the two worlds.
3. **Escape-(i) is an organizational/physical property, not a checkable one.**
   "Channels the author genuinely cannot write" must be enforced by whoever
   owns the channel (hardware, org boundaries, input registries with verified
   — not asserted — writability). The toy demonstrates that no tag construction
   over the percept bytes can substitute for that enforcement.
4. **Class-L is confirmed as conjunction evidence** (5/10 trials): a trainer
   corroborating the same spec-authored world adds no independence. Every
   future composition battery pairing H-PAM-33 with H-PAM-30 must include the
   Class-L fixture class (per the frozen prereg).

## Status for the backlog

H-PAM-33: **TESTED-killed as content-independence gate; CONDITIONAL-survives
as channel-integrity check** (escape-(i) externally enforced). The surviving
conditional claim is precisely: "IF no author-writable input is in the causal
ancestry of endorsed bytes, THEN admission is safe" — and the mechanism itself
cannot verify the antecedent.
