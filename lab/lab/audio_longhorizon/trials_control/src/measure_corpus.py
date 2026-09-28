#!/usr/bin/env python3
"""measure_corpus.py — offline harness step 1 (Phase B2b).

Measures every sealed corpus clip with the FROZEN scorer definitions
(audio_principles/crew_p/scorer_p.py — deterministic, numpy only) and writes
a per-clip measurement table for target selection.

Not in the per-trial path: this is harness prep (like preparing intents).
The trial binary (ctrl) never sees these values; it hears only WAV bytes.
"""
import json, hashlib, os, sys
import numpy as np

sys.path.insert(0, '/home/hatch/workspace/audio_principles/crew_p')
import scorer_p as SP  # noqa: E402  (frozen measurement definitions)

BASE = '/home/hatch/workspace/audio_longhorizon'
OUT = os.path.join(BASE, 'trials_control', 'targets', 'clip_measure.json')


def cv_of(fe):
    v = fe['f0'][fe['voiced']]
    if len(v) < 5:
        return 0.0
    m = float(v.mean())
    return float(v.std() / m) if m > 0 else 0.0


def main():
    man = json.load(open(os.path.join(BASE, 'corpus', 'CLIP_MANIFEST.json')))
    rows = []
    for c in man:
        p = os.path.join(BASE, c['path'])
        fe = SP.features(p)
        f0 = SP.med_f0(fe)
        env = SP.ans_env(fe)
        cv = cv_of(fe)
        vf = float(fe['voiced'].mean())
        dur = fe['nfr'] * 1024 / 44100.0
        rows.append(dict(clip_id=c['clip_id'], path=c['path'], cls=c['class'],
                         f0_hz=round(f0, 3), env=env, cv=round(cv, 5),
                         voiced_frac=round(vf, 4), dur_s=round(dur, 3),
                         nfr=int(fe['nfr'])))
    # integrity: sha of the table for the runlog
    body = json.dumps(rows, indent=1, sort_keys=True)
    open(OUT, 'w').write(body)
    print('clips measured:', len(rows))
    print('wrote', OUT)
    print('sha256:', hashlib.sha256(body.encode()).hexdigest())


if __name__ == '__main__':
    main()
