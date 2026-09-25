# AUDIO ROUND 2 — CLIP MAP (2026-09-24)

Neutral mapping for Micah's ear verdicts. Attribution happens ONLY
via this map AFTER his numbered verdicts are recorded. Do NOT guess.

## Surviving forks (3)
- CLIP_A → glottal_formant (fork 1: LF-model + 6 formants, /ba da ga/)
- CLIP_B → skeleton_refine (fork 3: skeleton + full refinement, C5–A5)
- CLIP_C → prosody_ab (fork 4: B with vibrato + timing, 523–784 Hz)

## Killed forks (3, no clip staged)
- fork 2 (grain_unit): KILLED — kill bar 2 failed (F2 shift 43Hz < 200Hz;
  hypothesis backwards: larger PSOLA grains improve frequency resolution).
- fork 5 (transient_first): KILLED — prosody 6.5% failed shared gate;
  KS decay destabilizes F0 tracker (mechanism/gate mismatch).
- fork 6 (psola_voice): KILLED — laugh source not validated (prosody
  0.0%, marks at 990Hz); no genuine laughing recording found.

## Files
- CLIP_A: `glottal_formant/glottal_formant_NEW.m4a`
  SHA-256: 60337ba844eeef7a1b251382ca30480e6645eb2364b98d023cbe79a446c11de4
- CLIP_B: `skeleton_refine/skeleton_refine_NEW.m4a`
  SHA-256: b0bdeca810ab6d8cc861cb74575a531a2409e890a4a653a6240bea82a6c8994a
- CLIP_C: `prosody_ab/prosody_ab_NEW.m4a`
  SHA-256: 488bf0c0893a9f5b23dafa6e69d99f8fc1063f2dc8d25b2ac97021f76b734db8

CLIP_D, CLIP_E, CLIP_F: UNUSED (forks killed, no clips).
