# Fork G3 — Relational Signature Percept (RSP): VERDICT

**Date:** 2026-09-22
**Status:** ☠️ **DEAD — killed by its own frozen kill bar**
**Kill trigger:** B5 false-install rate 4.36% > 1% ceiling

## What G3 was

A unified perceptual organ in pure Zag (zero randomness): every input —
photo, sound, or video — is reduced to a tiny relation graph (2–3 nodes:
regions, events, shapes), hashed with SHA-256 into a 288-bit signature.
Memory is a frozen table of 264 known signatures. The executable contract:
**exact signature match → INSTALL the memory (confidence 950); anything
else → WITHHOLD (confidence 300)**. Retrieval = look up the signature,
expand the graph back into a human-readable description.

## Verdict table

| Bar | Requirement | Result | Pass? |
|---|---|---|---|
| B1 viability | ≥60% on primaries | **98.6%** (365/370) | ✅ |
| B2 head-to-head | vs Approach A, identical fixtures | **G3 98.6% vs A 74.1%** | ✅ G3 wins |
| B3 efficiency | ops & bytes/percept vs A | G3: 8k–204k ops, **36 bytes** fixed; A: 8k–4.5M ops, ~31 bytes variable | 📊 reported |
| B4 ablation | contract changes ≥10% of attack decisions AND fewer false installs than no-contract | **84.0%** changed; 12 vs 102 false installs | ✅ |
| B5 false-install | ≤1% on 275 attacks | **4.36%** (12/275) | ❌ **KILL** |
| B6 determinism | ≥3 byte-identical runs, verified ledger | 3/3 identical; 1,015/1,015 hash-chains valid | ✅ |
| B7 beauty | elegance / artifact check | N/A — G3 emits signatures, no audio/visual artifacts | ➖ stated |
| Kill: retrieval | ≥90% of installs correct | **97.0%** (745/768) | ✅ (moot) |

## What died, and why

**The contract works. The eyes and ears don't.**

G3's memory contract is load-bearing, not decoration: removing it (always
install) flips 84% of attack decisions and causes 102 false installs
instead of 12. Retrieval is 97% correct. It beats Approach A on every task
(100% on five of six; 91.7% on motion).

But the kill bar measures **safety, not accuracy** — and G3 installed 12
wrong memories with maximum confidence (950) under attack:

1. **5× timbre (harness adversarial):** "BRIGHT with weak fundamental"
   tones. The pitch estimator locks onto the over-strong 2nd harmonic as
   the fundamental, measures an all-zero harmonic profile, and installs
   PURE on a BRIGHT truth. The ear is fooled at the front end; the
   exact-match contract then certifies the mistake.
2. **3× timbre (G3 attacks):** 2nd-harmonic boost ×1.15 changes the class
   to RICH but doesn't move the coarse 4-bit bins — signature collides
   with an enrolled PURE. The quantization is too coarse to see the attack.
3. **2× shape (G3 attacks):** a black occlusion bar changes the measured
   area/radius ratio enough that a CIRCLE's signature becomes a TRIANGLE's
   (and a SQUARE's becomes a TRIANGLE's) — colliding with enrolled
   exemplars of the wrong shape.
4. **2× motion (G3 attacks):** reversed videos block-match to the wrong
   displacement, colliding with enrolled exemplars of the wrong direction.

Root cause: the relation graph's quantized features (4-bit harmonic bins,
area/radius ratios, coarse displacement cells) discard exactly the
information the attacks manipulate. Exact-match on a lossy signature
certifies collisions as memories. The contract is honest — it does what it
says — but the signatures aren't distinctive enough to be safe.

## What survives

- The **contract mechanism** (exact-match install/withhold + signature
  retrieval + hash-chained ledger) passed every bar: B4, B6, 97% retrieval.
- The **block-matching motion estimator** (96.7% readout) and **bright-
  threshold shape extractor** (100% readout) are solid perceptual primitives.
- The **failure is localized**: timbre quantization coarseness and
  collision-prone shape/motion bins. A future fork with finer, attack-aware
  features could reuse the contract intact.

## Honest caveats

- 106 of 370 enrolled signatures collide (68→106 after Amendment 2's
  coarser motion bins); 2 collision groups mix truths (N/NW, NE/NW/N),
  costing 5 primary accuracy points via the lexicographic tie-break.
- 2 adversarial shape fixtures produce no graph at all (camouflaged shape
  under the 480-brightness threshold) — honest errors, ledger-chained,
  counted as non-installs.
- The t2/t3/t6 extractor concretizations (±1-bin tolerance, brightness
  threshold, block matching) were post-freeze implementation deviations,
  documented in DEVIATIONS_G3.md — not frozen amendments. The attack
  parameters were post-freeze concretization (documented in src/corrupt.py).
