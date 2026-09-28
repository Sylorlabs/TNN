# R6 Motif Microscope

The Motif Microscope inspects learned raw-byte spans after training. Human word
boundaries and known labels are used only by the evaluator after the fact.

## Main observation

The lower Adaptive Motif layer is not a hidden fixed tokenizer. Across two seeds
and budgets of 32, 128, and 512 exposures, only roughly 14–30% of its top 160
motifs aligned directly with a known surface value. Many motifs crossed spaces,
covered several units, or represented recurring construction fragments.

At 512 exposures:

| Seed | Layer | Known-surface aligned | Boundary/phrase motifs | Unresolved fragments |
|---|---|---:|---:|---:|
| 1 | Adaptive Motifs | 0.1938 | 116 | 13 |
| 2 | Adaptive Motifs | 0.2188 | 117 | 8 |
| 1 | Contrastive memory | 1.0000 | 0 | 0 |
| 2 | Contrastive memory | 0.9683 | 2 | 0 |

The higher grounded contrastive layer isolates much cleaner alternatives. In
seed 1 its learned cores were exactly:

```text
Ava, Ben, Cora, Drew, Eli, Fern
moves, supports, follows, opens, guides, warns
amber cube, blue ring, green star, ivory disk, red cone, silver bar
calmly, quickly, carefully, briefly, quietly, twice
```

This suggests a useful hierarchy:

```text
messy overlapping compression motifs
    -> grounded discriminative alternatives
    -> construction schemas
    -> one-shot support-gap binding
```

It does not prove that the same hierarchy will discover natural words or syntax
from unrestricted speech/video. Natural data is the next mandatory test.
