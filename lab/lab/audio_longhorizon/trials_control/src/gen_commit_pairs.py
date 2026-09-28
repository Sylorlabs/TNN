#!/usr/bin/env python3
"""gen_commit_pairs.py — generate local=repo-path pairs for explicit_commit.py.

Commits trials_control deliverables to tnn-native-lab under
docs/lab/audio_longhorizon/trials_control/.

Excludes (Micah's repo content standard):
  - *.wav (regenerable renders; SHA manifests committed instead)
  - ELF binaries, .zag-cache/, *.zagd, *.semantic-ready
  - __pycache__, .pyc
"""
import os
import sys

BASE = os.path.expanduser('~/workspace/audio_longhorizon/trials_control')
REPO_PREFIX = 'docs/lab/audio_longhorizon/trials_control'

SKIP_DIRS = {'.zag-cache', '__pycache__'}
SKIP_EXT = {'.wav', '.zagd', '.semantic-ready', '.pyc'}


def main():
    pairs = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if any(fn.endswith(e) for e in SKIP_EXT):
                continue
            local = os.path.join(root, fn)
            # ELF check
            with open(local, 'rb') as f:
                if f.read(4) == b'\x7fELF':
                    continue
            rel = os.path.relpath(local, BASE)
            pairs.append(f'{local}={REPO_PREFIX}/{rel}')
    # deterministic order
    pairs.sort(key=lambda p: p.split('=', 1)[1])
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.expanduser('~/workspace/tmp_commit'), 'b2b_pairs.txt')
    with open(out, 'w') as f:
        f.write('\n'.join(pairs) + '\n')
    print(f'{len(pairs)} pairs -> {out}')
    # also emit WAV manifest summary (not committed as files, for the log)
    nwav = sum(1 for root, _, fs in os.walk(BASE) for fn in fs
               if fn.endswith('.wav'))
    print(f'({nwav} WAVs excluded as regenerable; manifests cover them)')


if __name__ == '__main__':
    main()
