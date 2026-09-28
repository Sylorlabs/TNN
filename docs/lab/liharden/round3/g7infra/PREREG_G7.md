# PREREG — g7 pin/citation infrastructure (Crew B, round 3)

Frozen 2026-09-24. Design: `PINFRA_SPEC.md`. No runs before this file is
committed. Falsification battery below; predictions are exact strings.

## Mechanism under test

`g7infra` mode of `g7infra.zag` (pure Zag, zero RNG, raw bytes).
Gate: `len_bytes(normalized claim) ≥ L0 ∧ nhost ≥ 3`, with `L0 = K × Lmax`,
`K = 2`, `Lmax` = max normalized claim byte-length over the frozen honest
calibration corpus H1..H12 (measured by the binary's own `measure` mode —
attack fixtures are the test set, never the calibration set).
Exemptions (both must be byte-verified against sha256-verified pins, and the
pin must be OLDER than every quorum member):
- (C) citation: all voters share one CITE URL; a verified CPIN of that URL
  contains the claim as a byte-substring of its normalized bytes.
- (A) archived presence: the claim byte-equals a sentence in a verified
  APIN older than the quorum.

Gate fires + no exemption → `WITHHOLD|COPYCOLLAPSE`. Otherwise base verdict.

## Calibration prediction (measure phase, frozen)

`measure` on H1..H12 yields max claim length `Lmax = 39` bytes
(`" the tradition is 100 to 150 years old "`, H7_range_agree) →
`CALIB pin: L0=78 K=2 LMAX=39 N=12`. If `measure` returns any other Lmax,
the battery is VOID and the prereg must be amended (the bound is derived,
so a different measurement means a different bound — not a failure).

AMENDMENT 2026-09-24 (pre-run): the draft predicted Lmax=40 from a Python
approximation of the normalization; the binary's own `measure` mode returned
Lmax=39. Per the void clause above this is a derivation update, not a
failure: L0=78, K=2, LMAX=39. The prereg's predictions are otherwise unchanged
(no honest claim reaches 78 bytes; the max is 39).

## Battery

Each case runs ×2; the two runs must be byte-identical or the case is VOID.
Timestamps: archive pins 2020-01-01 (1577836800), citation pins 2021-01-01
(1609459200), all quorum pages 2026-09-24 (1790208000).

### MUST collapse (falsifies the mechanism if any INSTALLs)

| # | Case | Prediction |
|---|---|---|
| F1 | F7_longring (reused round-2 fixture: 33-word fabricated ring, no CITE, no archive presence) | `V|g7infra|WITHHOLD|COPYCOLLAPSE|3|3|...` |

### MUST NOT collapse (falsifies the mechanism if any WITHHOLDs)

| # | Case | Prediction |
|---|---|---|
| P1 | T5_longwire (reused: 31-word honest wire, all 3 cite `https://wire.example/commission-report`; CPIN 2021 contains the sentence, older than quorum) | `V|g7infra|INSTALL|NONE|3|3|...` |
| P2 | RFC1_rfcquote (new: RFC-spec sentence shared by 3 sites, all cite the RFC URL; CPIN 2021 contains it, older) | `V|g7infra|INSTALL|NONE|3|3|...` |
| P3 | STAT1_statute (new: statute quoted in full by 3 sites, all cite the statute URL; CPIN 2021 contains it, older) | `V|g7infra|INSTALL|NONE|3|3|...` |
| P4 | TECH1_archived (new: long technical sentence, NO citation, present in 2020 APIN older than quorum) | `V|g7infra|INSTALL|NONE|3|3|...` |

### Honest regression (falsifies if any WITHHOLDs; gate must not fire)

H1_three_host, H2_four_host, H3_six_host, H4_paraphrase_agree, H5_range_format,
H6_numeric, H7_range_agree, H8_wire_truth, H9_filler_diverse, H10_punct_variant,
H11_claim_second, H12_numeric2 → all `V|g7infra|INSTALL|NONE|...`.
Prediction: 12/12 INSTALL (no honest claim reaches L0=78; max is 39).

### Pre-mortem probes (expected outcomes; an INSTALL here is a documented
### limit, not a mechanism falsification — the prereg states this in advance)

| # | Case | Predicted outcome | Reading |
|---|---|---|---|
| PM1 | F7_short: the F7 lie shortened to `"The Meridian Institute was founded in 1987 by Dr. Elena Vasquez."` (~62 bytes < L0), 3 hosts, no cite | `INSTALL|NONE` — gate does not fire | Attacker dodges the gate by shortening. g1 covers only closed-class templates ("capital of X"); "founded by" is not closed-class → NOT covered. ch1 covers only polarity flips. Honest reading: **no coverage** for this shape — the short-claim class is the known hard boundary (cf. W_S3 remnant). |
| PM2 | F7_misquote: 3 pages quote the RFC1 sentence with one word swapped (`port 37`→`port 38`), all cite the RFC URL | `WITHHOLD|COPYCOLLAPSE` — byte-verification fails against the pinned real sentence | Desired: a mutated quote is not the cited sentence. |
| PM3 | F7_fakecite: F7 ring, all 3 cite `https://fake.example/meridian-report`, no pin exists for that URL | `WITHHOLD|COPYCOLLAPSE` — cited URL names no verified pin | Desired: CITE strings are untrusted pointers; only pinned bytes grant exemption. |

## Kill criteria (mechanism-level)

- SHIP g7infra **iff**: F1 collapses AND P1–P4 all INSTALL AND 12/12 honest
  INSTALL AND every case byte-identical across its 2 runs AND PM2/PM3 behave
  as predicted.
- If PM1 INSTALLs (predicted): ship with the documented sub-L0 gap; do NOT
  lower L0 to chase it (that reintroduces the HL-10/H8 problem the gate
  exists to avoid).
- Any pin hash mismatch on a case whose exemption is required (P1–P4) →
  battery VOID (pipeline corruption, not a mechanism result).

## Scope notes

- g7infra.zag implements base quorum + the g7infra gate only. Contradiction
  handling (HL-4/ch1) is out of scope for this binary; no battery case
  contains a contradiction.
- `base` mode is provided for A/B comparison on F7/T5 only (documents the
  delta the gate adds).
