# AUDIO V11 — ROUND 2 DIRECTION (audio coordinator takeover, 2026-09-24)

**Handoff:** Coordinator 7b003e12's Phase-2 judge delivered
`JUDGE_VERDICT_V11_DRAFT.md` (R 9/9 ITERATE, P 7/9 ITERATE, W 2/9 ITERATE,
G KILLED). Iteration crews R/P/W are live in `aud_v11/iter_{r,p,w}/`.
This brief takes over direction. It does not re-run diagnosis.

## Standing law for this round

`~/workspace/audio_predelivery_gate.md` applies in full: waveform analysis
first, measured delta vs previous version, SHA-256 identity checks, no agent
ear claims, NEW/PREVIOUSLY SHOWN/REFERENCE labels, M4A delivery.

**No clip goes to Micah's ears until it holds the frozen 9/9 AND closes the
D3/D6 gaps below.** The V10 mistake (metrics pass, ears reject) is not
repeated.

## Frozen round-2 kill bars (from the judge's §5, now binding)

### Fork R (objective leader)
- frac_static ≥ 0.25 with steady vowels (was 0.00)
- median F1/F2 trajectory variance within 4× of anchor (was 18–66×)
- D6 blind accuracy ≤ 0.65 (was 0.89)
- KEEP: 9/9 frozen bars, D5 exact-match profile

### Fork P
- F3B > 2650 (nearer-V10 half), MOD4 < 0.571
- D2 transient rate ≥ 0.8/s (add consonant onsets)
- D3 static vowels (same steadiness bars as R)

### Fork W
- Redesign, not tune: multi-vowel tract (D1 ≥ 3 via distinct vowels, not
  jitter), F2/F3 within tolerance, real F0 dynamics

### Fork G
- KILLED. Retained as negative control only.

## The load-bearing target

D3 is the universal failure: every fork's formant trajectories are 18–66×
more variable than the anchor's and never hold still (frac_static 0.00 vs
0.40). **Real children hold vowels; all forks glide, wobble, or jitter
constantly.** Vowel-hold capability is the round-2 thesis. A fork that
cannot hold a vowel cannot be child-like, regardless of its 9-bar score.

## Adjudication

- Independent re-adjudication from raw `voice_sig` output (fork crews'
  tables are not trusted at face value — R under-claimed, W over-claimed).
- The unseen discriminators D1–D6 stay blind: fork crews do not see them.
- Byte-identical reruns required for every measurement.

## Ears

The first fork to hold 9/9 AND close the D3/D6 gaps goes to the ear panel —
in M4A, labeled NEW, with the delivery brief stating measured deltas.
