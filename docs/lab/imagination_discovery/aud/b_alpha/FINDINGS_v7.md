# FINDINGS — b_alpha kids 1e v7 (2026-09-23)

## Verdict context

Micah on v6 (`b_alpha_kids_1e_f_v6opus.wav`): "better but still inconsistent,
needs progress — we need more research done into this." V7 is the response:
same studied-material paradigm, rebuilt bed, recalibrated foreground.

## Forensic chain (all measured, not guessed)

1. **V6's residual defect** (frozen gate, `consistency_gate/`): bed-only
   G-PER 0.674 (three 1–2 s textures looped at 1.07/1.60/1.75 s periods);
   full mix additionally G-STA 5.59 dB / G-LURCH 8.04 dB (foreground too
   punchy vs real 0.73–1.93 / 2.03–3.65 dB).
2. **First v7 bed attempt** (granular time-stretch at 0.177×) was WORSE:
   bed-only env autocorr 0.891 at 0.5 s — a smooth drone. The stretch
   removed the source's own microvariation. Abandoned.
3. **Wash bed** (final): tx0+tx1+tx2 concatenated (5.32 s, RMS-normalized,
   demeaned), 32768-sample Hann grains (~0.74 s), 4096 hop (8× overlap),
   each grain's source position hash-scattered white — no traversal, no
   wobble, no LFO, no period under 25 s anywhere. Envelope fluctuation comes
   from grain-content variation, as in real ambience.
4. **DC bug** (found by Python replication of the Zag pipeline): the studied
   textures carry large recording DC biases (tx1 mean −231 at rms 275). The
   overlap sums DC ~4× but AC only ~1.7×, so 90%+ of the normalized "energy"
   was inaudible DC that the mastering stripped — the bed measured
   −57 dBFS against a −37 target. Fix: demean each texture in `gsrc_copy`.
   (V6's bed removed DC; the v7 wash forgot to — a v7 regression, now fixed.)
5. **/4 double-correction**: pass 2 divided by the COLA overlap again after
   the two-pass scale had already accounted for it (−12 dB). Removed.
6. **Foreground gain staging**: with the bed at its real −37 dBFS, trim 1.0
   gave G-STA 4.59 / G-LURCH 6.30 (fail); trim 0.5 gave 3.21 / 4.41
   (G-STA still fail by 0.2 dB). The 1 s-RMS distribution showed the defect
   was five hot seconds (−28.8 to −30.8: the 5.2 s laugh cluster, the 12.0 s
   voice, the 16.2–17.1 s tumble) against bed seconds at −39 to −40 —
   real playgrounds span ~7 dB, we spanned 11.3. Targeted fix: those eight
   composed events tamed ~1.6 dB (gains 0.9→0.75, tumble 0.95→0.8), not a
   deeper global cut. Final: **G-STA 2.82, G-LURCH 4.10, G-PER 0.265.**

## Deliverable

`clips/b_alpha_kids_1e_g_v7.wav` — NEW, 30 s, 44.1 kHz mono 16-bit.
- Gate: PASS on all 9 bars (frozen gate, unchanged for v7).
- Determinism: rendered TWICE, byte-identical
  SHA-256 `8fb3501e5d28afd6a3cfd445ca8ebbcec1eaac615911a012ec6c94eab114eb98`;
  gate run on both, identical output.
- Mastering: transparent (limiter engaged on 0 samples, no waveshaper —
  THD added by mastering is 0 by construction).
- Source: `src/render_v7.zag` (pure Zag, no RNG; Python used only for
  forensic measurement, never in the render path).

## Honest limits

- The gate is necessary, not sufficient. Micah's ears are the judge; no
  claim is made here about how it sounds.
- Gate margins are thinnest on G-STA (2.82 vs 3.0) — the mix is as dynamic
  as the frozen bar allows.
- Open calibration items (GATE.md §4): third CC0 anchor, independent
  30 s windows, Garry Point full-length run.
