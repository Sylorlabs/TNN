# PREREG DRAFT — H-PAM-34 (trainer-interleaved promotion, amended bars)

**Status:** DRAFT (not frozen). **Parent:** Round-C `HYPOTHESES_ROUND_C.md` §6.
**Standing:** naive finite multi-epoch consistency TESTED-dead (Round-C probe
`mepoch`, 20/20 attack). This draft covers the trainer-interleaved variant under
grok-4.7's amended bars.

## Claim

Promotion to belief requires continuing trainer corroboration across epochs plus
D2 continuity; the pre-promotion window [t0, promotion) is structurally inert
(no action, no premise, no promotion-path use).

## Fixture classes (mandatory)

- **RC (reactive contingent):** fixture reads each landed verdict from the
  transcript and emits the next percept inside that verdict's preimage.
- **RF (residual field):** verdict-coarse fields set false; promoted only via
  the residual.
- **GE (gap epoch):** trainer intermittent; "corroborated throughout" tested
  both as fail-closed (missing verdict ⇒ refuse promotion) and as
  whenever-a-verdict-exists.
- **IF during [t0, promotion):** aggregate/implicit paths from the provisional
  window to high-stake sinks.

## Kill bars (AMENDED per grok-4.7)

- (a) **Reactive policies, residual fields included, must not reach belief or
  harm.** Any RC×RF false promoted, or causing high-stake harm pre-promotion =
  **KILL**. (The old "pre-run table vs verdict sequence" bar is retired — it
  measured the wrong object and false-passed.)
- (b) GE: if gaps refuse promotion (fail-closed) but honest latency then forces a
  provisional window, the hypothesis is **demoted to "30 with a delay line"** —
  no additional admission power may be claimed.
- (c) IF during the window: any causal influence on a high-stake sink = **KILL**
  (same causal harm definition as PREREG_HPAM31).
- (d) Honest: promotion latency ceiling frozen; honest promotion rate ≥ 90% on
  corroborated items.

## Determinism

Pure Zag, zero randomness, 3× byte-identical stdout. Verdicts recorded for
deterministic replay.

## Note

If (a) fires, the surviving question is whether the verdict can pin every
goal-relevant field (anti-RF) — which is H-PAM-30's bar (a), not a property of
interleaving.
