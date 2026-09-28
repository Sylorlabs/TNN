# Contender B: Failure Modes (where B loses)

## 1. RESPOND is sensorless (plan-derived, not audio-measured)
B reads the cue pitch from the PLAN, not from audio. It does not "hear" the cue.
- If the plan lies about the cue pitch, B will latch to the wrong pitch.
- The hybrid v2 measures audio (ZCR) and is robust to plan/audio mismatch.
- B's octave latch is honest but brittle: it trusts the plan completely.

## 2. Near-miss nominals are not corrected
If nominal is 460Hz (not an octave of 440Hz), B renders 460Hz as-is. It does not
attempt to find the "true" pitch. This is correct per the octave-latch design,
but it means B cannot fix non-octave errors.

## 3. Truncation step slightly larger than PAR
At a hard plan truncation (15s), B's single-sample step is ~17% larger than PAR's
(12,109 vs 10,303 in 16-bit units). Both have the artifact; B's is marginally worse.
This is an edge case (truncated plans), not normal rendering.

## 4. Prefix simulation cost (mitigated)
B re-renders chain prefixes at region boundaries (up to 3s for region 9). The
hot-loop optimization brought COST to parity with PAR, but the prefix is still
redundant work. A closed-form phase seed would eliminate it (future work).

## 5. Legato threshold is fixed (80ms)
Events separated by <80ms are legato; ≥80ms are not. This is a hard threshold.
A plan with 79ms gaps gets portamento; 81ms gets fresh attacks. There's no
musical intelligence here — it's a fixed rule.

## 6. No amplitude carry (by design)
B deliberately does NOT smooth amplitude across legato (G-PER failed when tried).
This means legato notes still have per-note attacks. If Micah's ears want smoother
legato, B cannot provide it without breaking G-PER. This is a fundamental tradeoff.

## 7. Region boundaries are fixed (3s)
The 3s region size is arbitrary. A chain crossing a boundary gets a prefix
simulation, but the boundary itself is not musically meaningful. If a phrase
crosses 3s/6s/9s/etc., B handles it correctly, but the regioning is still artificial.
