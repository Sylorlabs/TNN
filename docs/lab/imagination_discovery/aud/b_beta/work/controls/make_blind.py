#!/usr/bin/env python3
"""Build the blind bake-off package for the B-beta kids benchmark.
Three 30 s candidates, deterministic shuffle (seed 20260922):
  - B-beta piece (bbeta_kids_tag.wav)
  - same-brief synth control (control_synth_kids.wav)
  - real-playground calibration (kids_park source, first 30 s unmodified)
Output: blind/A.wav, blind/B.wav, blind/C.wav + KEY sealed for the parent.
The brief text given to judges is printed and saved as blind/BRIEF.txt."""
import shutil, subprocess, numpy as np, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BB = os.path.join(HERE, '..', '..')
OUT = os.path.join(BB, 'blind')
os.makedirs(OUT, exist_ok=True)

cands = {
    'bbeta': os.path.join(BB, 'bbeta_kids_tag.wav'),
    'control': os.path.join(HERE, 'control_synth_kids.wav'),
    'real': os.path.join(OUT, 'real_calib_30s.wav'),
}
# real calibration: first 30 s of the kids_park source, unmodified
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i',
                os.path.join(BB, 'work', 'wav', 'kids_park.wav'),
                '-t', '30', cands['real']], check=True)

rng = np.random.default_rng(20260922)
names = ['bbeta', 'control', 'real']
order = rng.permutation(names)
key = {}
for letter, name in zip('ABC', order):
    shutil.copy(cands[name], os.path.join(OUT, f'blind_{letter}.wav'))
    key[letter] = name

brief = """BLIND LISTENING — brief: "kids playing and laughter" (30 seconds).

Three 30-second mono recordings, labeled A, B, C. One is assembled entirely
from real captured playground recordings. One is synthesized (oscillators
+ filtered noise) attempting the same brief. One is an unmodified real
playground field recording (calibration).

For each of A/B/C, answer:
1. Does it sound like a synthesizer to you? (yes/no + one line why)
2. Does it sound like real children playing? (yes/no + one line why)
3. Rank the three by "most like real kids playing".

Kill bars: a "sounds like a synth" verdict on the B-beta piece from the
lead listener kills its claim. Majority "more real than the synth control"
is required to pass the bake-off.
"""
open(os.path.join(OUT, 'BRIEF.txt'), 'w').write(brief)
open(os.path.join(OUT, 'KEY.sealed.txt'), 'w').write(
    "SEALED — open only after all verdicts are recorded.\n" +
    "\n".join(f"{k} = {v}" for k, v in sorted(key.items())) + "\n")
print("blind package:", {k: v for k, v in sorted(key.items())})
print("NOTE: KEY.sealed.txt must stay sealed until judging completes.")
