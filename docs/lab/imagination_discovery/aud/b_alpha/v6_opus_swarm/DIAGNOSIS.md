# V6 investigation — why all five v5 isolation renders fail Micah's ears

**Status:** swarm BLOCKED (see SWARM_STATUS.md) — diagnosis below is independent,
mechanically derived from the committed sources (`src/render_v5.zag`,
`src/common_v5.zag`, `catalog.bin`) and VERIFIED by measurement against the
committed WAVs. Every number comes from `measure_v6.py` (run it to reproduce).

**Micah's verbatim verdicts (the oracle, ground truth):**
- (a) bed-only: "ass sounds like someone trying to dj stuff together but its horrible"
- (b) events-only: "randomly stops and theres issues and dj sloppy mix in a way"
- (c) mix: "same issues as B"; (d): "same issue as B and C"; (e): "same issues" — "all are fails"

## The unifying mechanism

Nothing in the render is continuous. Everything is discrete excerpts with fade
envelopes laid over near-silence:

- the **bed** is ~42 crossfaded chunks per 30 s — a DJ rapidly crossfading
  between 13 short loops;
- the **events** are 56 punched-in/out blobs with 24% literal silence between
  them — a sampler triggering one-shots into digital zero;
- the **mastering** adds 2.7–3.6% THD grit on every loud transient, always on.

A real playground ambience is continuous evolving sound. This is a collage of
clips. Micah's "DJ" description is literally accurate: the renderer IS a DJ —
crossfading loops (bed) and triggering one-shots (events).

## Mechanism 1 — the bed: perpetual crossfades (his "sloppy DJ mix")

`bed()` in `render_v5.zag` lays texture chunks end to end with a 0.5 s
smoothstep crossfade at EVERY boundary, advancing `t += wlen - xf`, picking the
next texture by hash-walk (usually a DIFFERENT recording), each chunk
RMS-normalized to 500.

Measured from `catalog.bin`:
- 13 textures, lengths **0.67–2.00 s** (mean 1.21 s) → mean chunk advance
  **0.71 s** → **~42 chunks / ~41 crossfade boundaries per 30 s**.
- 7 of the 13 textures are ≤1.0 s. For those, `xf = wlen/2`, so the ENTIRE
  chunk is fade-in-meets-fade-out — it swells up and immediately back down,
  never reaching a steady level.
- The crossfade is equal-GAIN smoothstep (`sstep(x)+sstep(1-x)=1`), not
  equal-power → for uncorrelated textures each boundary carries a **~3 dB dip**.

Measured from `b_alpha_kids_1e_a_bedonly.wav`:
- Continuous (zero gaps — the v4 "guaranteed crossfade" fix did eliminate the
  v3 dropouts), but the 50 ms envelope lurches **−42.8…−55.5 dBFS constantly**
  on sub-second timescales, with no clean periodicity (the hash-walk makes the
  pumping irregular — "sloppy").
- Spectral centroid is stable (~2115 Hz ± 86 Hz): the "DJ" percept is the
  relentless swelling/pumping rhythm, not timbre jumps.

The v4 bed fix optimized the wrong thing: it replaced butt-joint dropouts with
**perpetual transitions**. At a 0.7 s chunk period, "always crossfade" IS DJ
mixing. The correct fix is an order of magnitude fewer, longer chunks — or no
chunking at all (one long evolving texture).

## Mechanism 2 — the events: blobs in literal silence (his "randomly stops")

`place_event()` peak-normalizes every atom to 0.55–0.75 full scale with an 8 ms
attack and 60 ms release smoothstep on EVERY placement — each event is a
discrete punched-in/out blob. In clip (b) there is no bed: gaps are digital
zero.

Measured from `b_alpha_kids_1e_b_eventsonly.wav`:
- **23.7% of the 30 s is below −60 dBFS** — literal silence.
- 20 gaps ≥50 ms: max **0.90 s** mid-clip (3.60–4.50 s), median 0.10 s.
- **3.40 s of trailing digital silence** (26.55–30.00 s): the score schedules
  nothing after the 26.42 s footstep — the v2 "natural ending" removed the
  27.0 s/28.6 s events and left the tail to "air resolving to the bed floor",
  but in events-only there is no bed, so the clip just stops dead for its last
  3.4 s. Plus 0.6 s of leading silence (first event at 0.60 s).
- The v5 crew measured "max gap 0.9 s" and rejected sparse-scheduling as the
  percept — they missed the 3.4 s tail and, more importantly, they theorized
  about "contrast illusion" instead of measuring the silence structure of the
  actual clip. His ears were right; their analysis was wrong.

Why (c), (d), (e) inherit (b)'s verdict exactly: the bed sits at **−48.4 dBFS
RMS** against a −17.1 dBFS median event — 31 dB contrast. At 80 dB SPL event
peaks the bed is at ~49 dB SPL, ~19 dB above a quiet room floor: faintly
audible in dead quiet, otherwise masked. **Between events the mix is
effectively silent too.** So clips (c)/(d)/(e) ARE "events in silence" —
"same issues as B" follows mechanically. Removing/replacing 6 harsh atoms
(d)/(e) cannot touch this; the v5 crew's prediction that (d)/(e) would sound
like (c) was correct for the wrong reason (they blamed gain staging; the
mechanism is the gap structure, which gain staging alone won't fix either).

Silent-drop check: all 41 composed-beat times show energy in [t, t+0.6] s —
the `ai<0 → return -1` path does NOT trigger in the composed score. Red
herring (checked, not assumed).

## Mechanism 3 — the mastering: always-on soft-clip grit (contributor)

`wav_write()` applies `x = x/(1+0.35|x|)` to EVERY sample of EVERY clip, even
far below clipping. Sine-test THD:
- at the measured events peak (0.68): **3.60% (−28.9 dB)**
- at typical event level (0.50): **2.73% (−31.3 dB)**
- at 0.30: 1.70%; at 0.10: 0.59%

3.6% THD on percussive peaks is clearly audible grit/harshness on every loud
transient of every clip. The crew never questioned it. It doesn't explain
"randomly stops" or "DJ mix", but it contributes to "horrible" — a constant
distortion floor under everything.

Also measured: the fixed FIXPEAK normalization delivers the bed-only clip at
peak −33.4 dBFS — **9.4 effective bits**. ~64 dB SNR, so quantization is a
minor contributor at worst; noted for the record.

Red herrings checked and cleared: whole-file DC removal (residual DC 68–88 dB
below RMS in all clips — negligible); the silent-drop path (not triggering);
harsh atoms (11% of event energy — correctly dismissed by v5).

## Recommended fix direction (v6)

1. **Bed: stop DJ-ing.** Either (a) use textures tens of seconds long so
   boundaries are rare events, not a 1.4 Hz rhythm; or (b) build the bed as ONE
   long evolving texture (slow parameter drift over a single long source —
   amplitude/timbre evolving continuously, never concatenated); or (c) layer
   2–3 long loops with slow independent amplitude LFOs instead of sequential
   crossfades. Kill the 0.5 s crossfade-everywhere rule — it was the wrong fix.
2. **Events: fill the silence.** The composition needs a continuous middle
   ground: raise the bed to an audible ambience level (~20 dB below foreground,
   not 31 dB), give atoms overlapping/reverberant tails so they decay INTO each
   other instead of into digital zero, and compose THROUGH 30 s — no 3.4 s dead
   tail, no 0.6 s dead head.
3. **Mastering: fix the soft clip.** Engage limiting only when actually
   clipping; an always-on 3.6%-THD waveshaper is a defect, not headroom.
4. **Process lesson:** when the oracle says "randomly stops", measure the
   silence structure of the actual clip — don't theorize it away. The v5 crew's
   "contrast illusion" dismissal was contradicted by the WAV itself, and the
   v4 bed "fix" replaced one audible defect (dropouts) with another (perpetual
   crossfades) because the chunk RATE was never questioned.

## Files

- `measure_v6.py` — all measurements above, reproducible (`python3 measure_v6.py`)
- `prompt_bed.txt`, `prompt_events.txt`, `prompt_master.txt` — the three swarm
  prompts (unsent output; kept for retry after top-up)
- `SWARM_STATUS.md` — why the opus-5.5 swarm itself produced no model output
- `../clips/b_alpha_kids_1e_{a,b,c,d,e}.wav` — the analyzed clips (committed v5)
- `../src/render_v5.zag`, `../src/common_v5.zag` — the analyzed sources
