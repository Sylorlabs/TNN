#!/usr/bin/env python3
"""Determinism proof: re-run sampled episodes twice, compare hashes of
(trace, output image, memory delta). Byte-identical reruns required."""
import hashlib
import os
import shutil
import sys

import gen
from gen import write_op_spec
from run import run_op, run_learn, KBC, WORK
import score as scorer

SAMPLE = [3, 7, 11, 19, 23, 31, 42, 55, 61, 67, 73, 79, 89, 97, 103,
          111, 121, 129, 137, 149, 151, 163, 167, 173, 179, 181, 191,
          193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
          1001, 1007, 1013, 1019, 1027, 1033, 1041, 1049, 1053, 1057, 1059]


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def run_once(idx, regime, workdir, mem_src):
    """Run one episode (operate+learn), return hashes of artifacts."""
    epdir = os.path.join(workdir, f'ep{idx:05d}')
    os.makedirs(epdir, exist_ok=True)
    mem = os.path.join(epdir, 'mem.mem')
    shutil.copy(mem_src, mem)
    sp0, img0, meta = gen.build_episode(idx, regime, epdir)
    ops = meta['ops']
    hashes = []
    img_cur = img0
    for j, op in enumerate(ops):
        sp = sp0 if j == 0 else write_op_spec(
            epdir, j, op, img_cur, meta['frozen_hints'],
            lambda jj, be: meta['frozen_hint_used'],
            meta['chunk'], idx * 10, len(ops))
        trace = os.path.join(epdir, f'trace{j}.txt')
        img_next = os.path.join(epdir, f'img{j + 1}.bin')
        verdict = os.path.join(epdir, f'verdict{j}.txt')
        rc, _ = run_op('operate', sp, img_cur, mem, trace, img_next)
        assert rc == 0
        scorer.score_op(sp, img_cur, img_next, trace, verdict)
        mem2 = os.path.join(epdir, f'mem2_{j}.mem')
        rc2 = run_learn(sp, trace, verdict, mem, mem2)
        assert rc2 == 0
        shutil.copy(mem2, mem)
        hashes.append(sha_file(trace) + sha_file(img_next) + sha_file(mem))
        img_cur = img_next
    return '|'.join(hashes)


def main():
    mem_src = os.path.join(WORK, 'train-v1', 'memory.mem')
    assert os.path.exists(mem_src), 'train first'
    base = os.path.join(WORK, 'determinism')
    os.makedirs(base, exist_ok=True)
    mism = 0
    for idx in SAMPLE:
        regime = 'heldout' if idx >= 1000 else 'train'
        h1 = run_once(idx, regime, os.path.join(base, 'run1'), mem_src)
        h2 = run_once(idx, regime, os.path.join(base, 'run2'), mem_src)
        ok = 'IDENTICAL' if h1 == h2 else 'MISMATCH'
        if h1 != h2:
            mism += 1
        print(f'ep {idx}: {ok}')
    print(f'{len(SAMPLE) - mism}/{len(SAMPLE)} byte-identical')
    return 1 if mism else 0


if __name__ == '__main__':
    sys.exit(main())
