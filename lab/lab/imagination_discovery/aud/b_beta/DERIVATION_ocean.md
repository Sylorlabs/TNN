# DERIVATION — "an alien ocean's surf at dawn, under a sky that hums" (B-β Test 3)

Piece: `bbeta_ocean.wav` — 30 s, 44.1 kHz mono 16-bit.
Mechanism: `mech_ocean.zag` (fresh, written for this brief).
Seed: 20260922. Render SHA-256 (3/3 byte-identical): `904833c220d38eb95270dde2e3d087a3de27dae57e878c3fa9b0138c5f978654`

## 1. The imagined scene (the commitments)

Not Earth. An ocean under a different sky, at dawn:

- **The sea** is real water — surf swells and crashes from `ocean_tropical`
  and `sea_waves`. Water is water; the alienness is not in the material.
- **The sky hums**: three registers of real vocal gesture — throat-singing
  drones (low), whale phrases (mid), loon calls (high, sparse). The sky is
  made of throats, and it is the sky that conducts the sea: wave crashes
  cluster *under* whale phrases, not in Earth beach sets.
- **The water grammar is inverted**: every third crash plays REVERSED —
  water that gathers before it breaks. No Earth beach does this.
- **Dawn arc**: 0–8 s deep swells + low hum (night barely ending) →
  8–22 s the sky speaks and the sea answers → 22–30 s an alien dawn
  chorus (loon calls, sparse) as the swells recede.

## 2. Anti-Earth-pastiche audit (the kill bar, addressed structurally)

| Earth-pastiche risk | Structural defense |
|---|---|
| Regular wave sets | Crashes are timed by whale-phrase onsets (sky-conducts-sea), never by a fixed period; anti-rhythm veto on spacings |
| Beach sound | Reversed crashes (1 in 3) break the attack-decay signature of Earth surf |
| Whale = Earth whale | Whale phrases appear with no water-context grammar — they conduct crashes and overlap throat drones, a causal role no Earth scene gives them |
| Loon = Earth bird | Loon calls only in the dawn phase, sparse, over reversed surf — the company is alien |

Stated honestly: the materials are Earth recordings. If a listener hears
"beach with whales," the piece fails its kill bar and this document will
say so. The bet is that *causal grammar* — who conducts whom, what runs
backward — is what makes a scene alien, not the raw material.

## 3. Per-piece mechanisms (fresh for this brief)

1. **Sky-conducts-sea** — each placed whale phrase schedules 1–2 crash
   events inside its own time span (deterministic hash offsets). The sea
   answers the sky; this coupling exists nowhere on Earth.
2. **Reversal tide** — every 3rd crash placed with rev=1. Allowed op,
   alien grammar.
3. **Dawn arc** — three phases with shifting density/brightness (see §1);
   the mechanism phases event-type eligibility by clock, not by meter.
4. **Deterministic choice** — `h32(20260922, counter)` throughout;
   byte-identical across renders.

## 4. Anti-rename audit

No oscillators, resonators, filters, noise, chirps, envelopes, pitch/time
modification, or granular synthesis. Only constant gain, 3 ms seam fades,
mix-bus addition, writer DC/normalize. Reversal is an allowed arrangement
op, not synthesis.
