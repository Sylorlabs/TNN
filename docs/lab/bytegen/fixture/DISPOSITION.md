# BYTEGEN fixture disposition (2026-09-23)

Resolves VERDICT.md caveat 1: the frozen prereg (PREREG_BYTEGEN.md §26)
required reusing a frozen V10-era plan fixture, but no such fixture exists in
the V10 materials. `fixture/plan_v1.txt` was created new for the run.

## Search performed

- `~/workspace/aud_v10/` (full tree): no `*plan*.txt` fixture, no fixture
  dir. V10's PREREG froze **bars** (consistency gate), not a plan.
- `~/workspace/tnn-lab/imagination_discovery/` (full tree): no plan fixture,
  no fixture dir.
- The only V10-era "events" files (`aud_v10/headtohead/events_{artic,paradd,
  specstat}.txt`, `imagination_discovery/aud/b_alpha/src/events_v10_*.txt`)
  are single-column **detected onset-time lists**, not renderable plans —
  they carry no frequencies, durations, amplitudes, or timbre, so no
  renderer can turn them into audio and neither fork could have used them.
- Full-tree search of `~/workspace/tnn-lab` for `BED `/`DUR_S` and for
  "plan fixture" found only bytegen's own files.

Conclusion: **the prereg's "frozen V10-era plan fixture" never existed.**
There is nothing real to designate. Option (b) — designate + rerun — has
no valid candidate.

## Decision: BLESS `fixture/plan_v1.txt` as the frozen fixture

SHA256 of the blessed fixture:
`b9df27d6fde0904021cc17987e223a5dd126c07aa11b6a922eb5f15a677b52a7`

### Why it is adequate as the battery's standard

The battery measures: quality gate, CHOP-1/2/3, motif recurrence coherence,
RT-CASCADE, RT-LONG, RT-EDGE, determinism. The fixture exercises every one:

- **Cascade (RT-CASCADE, fault at t=3 s):** falls inside the first MOTIF-A
  occurrence (2.0–5.15 s) — rich signal on both sides of the fault, so the
  post-cut sample comparison (0 vs 5,791 differing samples) is meaningful.
- **Recurrence (coherence xcorr):** identical 8-note MOTIF-A at 2.0 and 24.0
  (identical parameters, byte-level), giving the [1.8,5.4] vs [23.8,27.4]
  windows a true ground-truth pair (PAR 1.000000, AR 0.741083).
- **Chop (CHOP-1/2/3):** 16 motif note boundaries on a 0.4 s grid with 40 ms
  attack / 150 ms release — exactly the transients the chop probes target
  (PAR's CHOP-3 spikes all landed ≤ 0.35 s of note boundaries, confirming
  the fixture exercises the phenomenon).
- **Edge (RT-EDGE, cut at 15 s):** lands in a bed-only region between arc
  events (14.8 → 16.0 s), measuring whether the renderer injects a
  discontinuity where the plan itself has none (0 for both forks).
- **Long (RT-LONG, wrong nominal pitch):** pure harmonic-tone events with
  exact known frequencies (440 Hz motif) give AR's pitch inference a known
  ground truth to hit or miss (it inferred 440 Hz from its own output).
- **Quality gate (9 bars):** constant 110 Hz bed keeps energy above silence
  (G-SIL friendly); no hard transients (CHOP-1 friendly); vibrato, glide,
  and timbre (1..10 harmonics) parameters exercise the spectral machinery.
- **Fairness:** one ASCII plan, static, zero RNG; both forks render the same
  file (prereg §26's actual requirement, which IS satisfied).

### Evidence hygiene (verified 2026-09-23 during disposition)

- Both forks rebuild clean from the pinned toolchain
  (`tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`) on the blessed fixture.
- PAR rerun: byte-identical (`cmp` clean), SHA256
  `1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4`
- AR rerun: byte-identical (`cmp` clean), SHA256
  `66dd62d6d4090daa9f966ff7e719501dccfbf896ecdba2b245dd7935ee1d3594`
- Fresh builds on the blessed fixture reproduce the verdict's stored
  artifacts `fork_par/src/par_seq1.wav` and `fork_ar/src/ar_seq1.wav`
  **byte-for-byte** — so the verdict's numbers were generated from exactly
  these fixture bytes. **Verdict numbers survive; no battery rerun needed.**

## Versioning rule going forward

1. `fixture/plan_v1.txt` is FROZEN. Any byte change requires a Micah-signed
   prereg amendment (standing rule from `fixture/README.md`).
2. It is replaced only when the battery gains a dimension the fixture cannot
   exercise (e.g. stereo/multichannel, vocal-formant content, non-musical
   constructed-vs-believed utterances). A replacement gets a NEW filename
   (`plan_v2.txt`, ...); old versions are retained, never overwritten.
3. The fixture is INVALID for a run if its SHA256 does not match the value
   recorded above (tamper check before every run), or if a fork cannot parse
   it into the documented SR/DUR_S/BED/EVENT semantics.
4. The red-team scenario plans (`tests/plan_edge_cut.txt`,
   `tests/plan_edge_full.txt`, `tests/plan_long.txt`) are scenario fixtures,
   not the standard — they are versioned alongside the standard but never
   silently substituted for it.
