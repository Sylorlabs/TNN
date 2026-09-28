# MECHANISM.md — the B-γ event assembler

## What it is

A **sample-placement engine with a deterministic score grammar**. Every
audible moment in every deliverable is a captured grain from a real
recording. The system invents *arrangements*: which grains, when, how
they overlap, when they morph. It never generates a waveform.

## Architecture (gamma.zag, pure Zag, zero RNG)

```
 study_src/ (12 licensed recordings, local-only)
     │  study.py (deterministic Python preprocessor: segment + classify
     │            + k-means voices; writes gamma.grpk grain pack)
     ▼
 gamma.grpk ──► pack_load() ──► [gptr, gnsamp, gcid, gvoice, gcent] arenas
     │
     ▼  score_kids / score_planet / score_ocean / score_monster
        (deterministic event grammars; see below)
     │
     ▼  place() / place_rev() / morph() into a Q24 mix arena
        (≤2 ms smoothstep glue fades, T7)
     │
     ▼  soft-clip + normalize + 30 ms/800 ms edge fades
     ▼  16-bit mono WAV, 44.1 kHz
```

**Q24 mixing:** samples accumulate as i64 Q24 in an i64 arena
(`get64/put64` accessors — the safe pattern from the AGENTS.md `[]i32`
miscompile lesson). Peak-normalized to 0.89 with tanh-ish soft limiting
(`x/(1+0.35|x|)`), never clipped hard.

**Determinism:** all "choices" come from `h01(seed, salt)`, a
splitmix64-derived 0..1 hash. Same pack + same binary → byte-identical
WAV. No wall-clock, no address hashing, no uninitialized reads (arenas
are zeroed explicitly — the AGENTS.md arena lesson).

**Selection:** `g_pick` hashes (seed,salt) into the per-(class,voice)
table and picks a grain by `h01`; no linear scan per placement (tables
are precomputed in the pack).

**Morph (T5):** `morph()` renders grain A crossfading into grain B over
min(lenA,lenB): `w(t)=A(t)·(1-t)+B(t)·t` with edge glue. One real event
becoming another — the plate-break mechanism. No pitch tools involved.

**Reversal (T4):** `place_rev` reads the grain backwards. An editorial
transform; the samples remain 100% captured.

**Brightness-order (T8):** candidates sorted by stored centroid
(`gcent` arena), placed ascending. Selection, not processing.

## Score grammars (what the four pieces compose)

| Piece | Grammar | Length |
|---|---|---|
| `kids` | Tag game: V0 leads, V1 answers, V2 third child, laughs interleave; a mid-game trip (thud + squeal), distant shouts, running feet approach/retreat, swing creaks as set dressing. | 30 s |
| `planet` | Alien world: rift booms → sub-surface hum (rumble bed) → the chorus (crack grains in brightness cascades + one morphing boom-cry) → seismic groan (creaks) → distant answering fracture. | 21 s |
| `ocean` | Alien sea: swell-crest-surge phrasing, 4 fracture cascades on the most viscous sea (cracks accelerating into surf-crashes, then recession = reversed cracks), an eddy (wash spirals + reversed wash). | 30 s |
| `monster` | The Raxith (see MONSTER.md): wind settle → 3 phrases of crack-syllables (3–7 per phrase, density rising) → plate-break (crack→rumble morph) → second creature answers sparse → interrupt overlap → dense cascade → final break. | 30 s |

## The honesty ledger

| Claim | Status |
|---|---|
| Pure-Zag render | TRUE (study.py is Python preprocessing — documented, not hidden) |
| Zero RNG | TRUE (splitmix hashes only) |
| Byte-identical 3/3 reruns | measured, TEST_RESULTS.md |
| Every grain traceable | TRUE (grains.csv → recording → time) |
| 3 distinct laugh voices | enforced by per-subclass k-means + repair; verified in TEST_RESULTS.md |
| No two grains from the same 2 s window placed adjacently | structural: g_pick never returns adjacent-sourced grains in a train — actually NOT structurally enforced; the no-copy audit (audit.py) checks the OUTPUT instead, which is the honest bar |

## What this mechanism cannot do (declared limits)

- No pitched voices: if the grains don't sing, the piece doesn't sing
  (the kids control comparison will test whether that matters).
- No continuity beyond grain length: long scenes must be composed from
  events, which can seam at boundaries (the A-NATIVE checks + ears judge).
- The pack is large (78 MB): grains are i16, loaded whole. Fine for a
  workstation; not for a tiny device.
