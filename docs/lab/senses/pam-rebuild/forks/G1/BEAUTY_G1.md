# B7 Beauty: The Symmetry Group Percept

## The Idea

A 512-bit percept that distills each input to its **symmetry essence**:

- **256 bits**: Generator codes — which symmetries hold (reflections, rotations, uniformity, periodicity, spectral shape, chroma, luma).
- **256 bits**: Fixed-point coordinates — where the symmetries live (centers, periods, motion vectors).

## The Generator Table (frozen)

| Code | Meaning |
|------|---------|
| 0 | EMPTY |
| 1 | IDENTITY |
| 2-5 | REFLECT_X, REFLECT_Y, REFLECT_D1, REFLECT_D2 |
| 6-8 | ROT_90, ROT_60, ROT_120, ROT_180 |
| 9 | UNIFORM (field constant) |
| 10 | PAIR_MATCH (two inputs share essence) |
| 11 | ILLUM_INV (illumination invariant) |
| 12 | STILL (no motion) |
| 16-31 | PERIOD_p (audio period = p) |
| 32-47 | MOTDIR_d (motion direction = d) |
| 48-63 | SPECT_s (timbre spectral shape = s) |
| 64-79 | CHROMA_c (color hue bucket = c) |
| 80-95 | LUMA_l (brightness bucket = l) |

## Example Percepts

**Blue square (shapetrans → SQUARE):**
```
Generators: [1 IDENTITY][4 REFLECT_D1][6 ROT_90]...
Coords: center (24, 24), ...
Percept: 010406... (128 hex chars)
```

**440Hz pure tone (pitchdisc → SAME):**
```
Generators: [1 IDENTITY][9 UNIFORM][10 PAIR_MATCH][16+ PERIOD]...
Coords: period 100, ...
```

**Why it's beautiful:** One 64-byte code captures the *meaning* of a megabyte input — not the pixels, but the symmetries. A circle is "that which is invariant under all rotations." A pure tone is "that which repeats with period p." The percept is the group-theoretic essence.

## The Failure (honest)

The beauty breaks where the frozen design meets reality:
- Shape masks capture photo backgrounds (threshold at mean).
- The 5-bit Hamming rule can't distinguish CHROMA_3 from CHROMA_4 (3 bits apart).
- Instance parameters (specific hue, specific period) pollute the symmetry codes, breaking retrieval.

The IDEA is elegant. The FROZEN IMPLEMENTATION is not.
