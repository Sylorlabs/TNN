# Battery 1e: component-isolation renders (2026-09-23)

**Why:** Micah's ear verdict on v4 — "nothing improved, same damn result."
His ears outrank all metrics. v4 fixed the bed but left all 56 scored
events unchanged. These five renders isolate the components so he can
POINT at which one carries the bad percept instead of describing it.

**All five share one fixed output normalization** (v4's mix peak,
18242028 Q24 units), so they are level-comparable: the bed-only clip is
at its true mix level, the events-only clip is at its true mix level,
and the two modified mixes differ from the v4 replica ONLY inside the
6 edited windows (verified sample-exact; everything else bit-identical).

## The five candidates (all NEW — none previously shown)

1. `b_alpha_kids_1e_a_bedonly.wav` — bed ONLY, true mix level
   (−48.4 dBFS RMS). Very quiet: that IS the finding. Turn it up to hear
   bed character (crossfades, texture quality).
2. `b_alpha_kids_1e_b_eventsonly.wav` — 56 events ONLY, true mix level
   (−20.2 dBFS RMS). No bed underneath.
3. `b_alpha_kids_1e_c_mix_v4replica.wav` — full mix, byte-identical to
   the shipped v4 (`5a1b1f7b…`). The reference.
4. `b_alpha_kids_1e_d_mix_noharsh.wav` — full mix MINUS the 6 placements
   of the 5 "harsh" atoms (ai=4, 23×2, 103, 105, 108). Selection state
   identical to v4; only those windows are silent.
5. `b_alpha_kids_1e_e_mix_replaced.wav` — full mix with those 6 placements
   swapped for the lowest-crest same-class atoms
   (4→6, 23→25, 103→89, 105→102, 108→104).

## What the measurements say (for the record, not to override his ears)

- The 5 "harsh" atoms carry **11% of total event energy**. ai=4 — the one
  v4 flagged strongest (+31.7 dB transient) — ranks **#49 of 56** by placed
  RMS (−19.5 dBFS). 36 of 56 events sit within 6 dB of the loudest.
  Removing them cannot change the overall percept much by construction.
- No digital defects in any of the 5 atoms: zero clipped samples, no
  impulse/edit-click signatures. The v4 crew's "legitimate recorded
  sounds" call was correct — but it framed the wrong question.
- The systemic fact: `place_event` peak-normalizes EVERY atom to
  0.55–0.75 full scale. Median placed event: −17.1 dBFS over a −48.4 dBFS
  bed — a **~31 dB foreground/background contrast**, unchanging since v1.
  That is the constant across v1→v4, and the best explanation of
  "same damn result."
- "Random cutouts" as sparse scheduling: REJECTED by measurement. Events
  cover 75% of the 30 s; 19 gaps, median 0.12 s, max 0.90 s. The likelier
  percept is contrast, not dropout: events punch ~31 dB out of
  near-silence, so the bed-only moments between them read as the sound
  "going away."

## Recommendation for v5 (for the program, not asserted as fact)

Change the gain staging, not the atoms: stop peak-normalizing every atom
to near-full-scale; preserve natural relative levels (fixed global gain)
and/or raise the bed toward a natural ambience level so the contrast is
~10–15 dB instead of ~31 dB. The atoms are fine. The balance is not.

## Provenance

- Source: `src/render_v5.zag` + `src/common_v5.zag` (pure Zag, zero RNG).
  `kida/kidb/kidc/kidd/kide` subjects; `score_kids_iso(mode)` with
  `mode 0/1/2` = v4-identical / skip-harsh / replace-harsh.
- Verification: kidc byte-identical to shipped v4 across two independent
  builds; bed+events sums to mix; kidd/kide differ from kidc only in the
  6 edited windows (sample-exact).
- Renders: `clips/b_alpha_kids_1e_*.wav`, 30.00 s mono 44.1 kHz PCM16.
