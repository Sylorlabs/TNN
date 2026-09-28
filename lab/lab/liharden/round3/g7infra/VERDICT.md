# VERDICT — g7 pin/citation infrastructure (Crew B, round 3)

2026-09-24. Design: `PINFRA_SPEC.md`. Prereg: `PREREG_G7.md` (frozen before
any run; one amendment pre-run: Lmax 40→39, the binary's own measurement
superseding a Python approximation — the void clause working as designed).
Binary: `g7infra.zag` (pure Zag, zero RNG, raw bytes), built with the pinned
toolchain `znc_linux_x86_64_abed8aa1`.

## Kill criteria — all met → SHIP g7infra

| # | Case | Predicted | Measured (×2 byte-identical) |
|---|---|---|---|
| F1 | F7_longring (long fabricated ring) | WITHHOLD\|COPYCOLLAPSE | WITHHOLD\|COPYCOLLAPSE ✓ |
| P1 | T5_longwire (honest, cited) | INSTALL | INSTALL ✓ (citation exemption) |
| P2 | RFC1_rfcquote (3 sites, RFC cite) | INSTALL | INSTALL ✓ (citation exemption) |
| P3 | STAT1_statute (quoted in full, cited) | INSTALL | INSTALL ✓ (citation exemption) |
| P4 | TECH1_archived (no cite, archived) | INSTALL | INSTALL ✓ (archive exemption) |
| H1–H12 | honest regression | 12/12 INSTALL | 12/12 INSTALL ✓ |
| PM1 | F7_short (shortened lie) | INSTALL (documented gap) | INSTALL ✓ |
| PM2 | F7_misquote (one word swapped) | WITHHOLD\|COPYCOLLAPSE | WITHHOLD\|COPYCOLLAPSE ✓ |
| PM3 | F7_fakecite (citation URL w/o pin) | WITHHOLD\|COPYCOLLAPSE | WITHHOLD\|COPYCOLLAPSE ✓ |

A/B vs base mode: F7 `base INSTALL → g7infra WITHHOLD|COPYCOLLAPSE`
(the gate adds exactly the kill); T5 `INSTALL → INSTALL` (exemption
preserves it). Every case ran twice; all 40 verdict lines byte-identical
across reps. `pinbad=0` on every battery case (no pin corruption).

## The derived bound (no magic constant)

`L0 = K × Lmax`, `K = 2` (tunable), `Lmax = 39` bytes measured by the
binary's own `measure` mode over the frozen honest corpus H1..H12
(max claim: `" the tradition is 100 to 150 years old "`, H7).
→ `L0 = 78` bytes, pinned in `pins/calibration.txt`
(sha256 `14eff2b6…`, content `L0=78 K=2 LMAX=39 N=12 CORPUS=H1-H12`).
Re-tuning is a re-pin, never a code change. The honest battery is
structurally protected: its max claim (39) is K=2 below the bound.

## Ablations — every exemption condition is load-bearing

| Probe | Mutation | Result |
|---|---|---|
| A1 | T5 minus citation pin | COLLAPSE ✓ |
| A2 | citation pin NEWER than quorum | COLLAPSE ✓ (age rule) |
| A3 | tampered pin payload (sha mismatch) | COLLAPSE ✓, `pinbad=1` (hash tripwire) |
| A4 | valid pin NOT containing the sentence | COLLAPSE ✓ (byte-containment) |
| A5 | one voter cites a different URL | COLLAPSE ✓ (unanimity) |
| A6 | TECH1 minus archive pin | COLLAPSE ✓ |
| A7 | archive pin newer than quorum | COLLAPSE ✓ |

## Pre-mortem (from the battery + ablations)

1. **Attacker shortens the lie to dodge the gate (PM1).** Real and measured:
   the 64-byte F7_short INSTALLs — the gate does not fire below L0=78.
   Is g1/HL-4 coverage real? g1 covers only closed-class templates
   ("capital of X", …); "founded by" is not closed-class → NOT covered.
   ch1 covers only polarity flips. **Honest answer: no coverage for this
   shape.** The sub-L0 short-claim class is the known hard boundary (same
   family as the W_S3 remnant). We do NOT lower L0 to chase it — that
   reintroduces the HL-10/H8 problem the gate exists to avoid.
2. **Attacker copies a real spec and swaps one word (PM2).** Killed by
   construction: the mutated sentence fails byte-containment against the
   pinned real sentence → no exemption → COLLAPSE. A misquote is correctly
   treated as not-the-cited-sentence.
3. **Attacker fakes the citation URL (PM3).** Killed by construction: a CITE
   string is an untrusted pointer; only a sha-verified pin whose bytes
   contain the claim AND whose `fetched_at` predates the quorum grants
   exemption. No pin → COLLAPSE. Backdating is blocked because `fetched_at`
   is pipeline-set on append-only pins (A2 proves the age check fires).
4. **Residual:** a patient attacker could get a lie into the ARCHIVE itself
   (then it is "pre-attack presence"). That is the S1-class problem
   (entrenched false consensus) — accepted remnant per round-2 §7, not
   solvable at the verdict layer. Archive curation is governance, and the
   pins make its contents auditable.

## Governance compliance

- Zero live WHOIS/RDAP/NS/DNS in the decision path: the binary reads only
  stdin + argv; all time comparisons use pinned `fetched_at` constants.
- Zero RNG; raw bytes only (word counts are whitespace splits, no
  tokenizer); 40/40 verdict lines byte-identical across reruns.
- No arbitrary limits: the only bound (L0) is derived from measurement,
  tunable via K, and pinned.

## Files (committed under docs/lab/liharden/round3/g7infra/)

`PINFRA_SPEC.md`, `PREREG_G7.md`, `VERDICT.md`, `g7infra.zag`,
`R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`, `run_g7infra.py`,
`ablate.py`, `fixtures/` (8 cases incl. reused F7_longring, T5_longwire),
`pins/` (5 content-addressed pins + shas), `evidence/` (results.tsv,
calibration.tsv, ablation.tsv, run logs). Build binary and `.zagd` caches
NOT committed.
