"""Generate truth-free gate inputs: classmap + segment files (frozen spec)."""
import json

RERUN = '/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun'
OUT = '/home/hatch/workspace/scratch_suspect1/build'

CLASS = {'colordisc': 0, 'colorconst': 1, 'shapetrans': 2,
         'pitchdisc': 3, 'timbredisc': 4, 'motiondir': 5}

m = json.load(open(RERUN + '/mappings.json'))
# stimuli: idx(str) -> "task/p000"
cmap = {}
for idx, label in m['stimuli'].items():
    task = label.split('/')[0]
    cmap[int(idx)] = CLASS[task]
assert len(cmap) == 370 and min(cmap) == 0 and max(cmap) == 369
with open(OUT + '/classmap.txt', 'w') as f:
    for s in range(370):
        f.write('%d %d\n' % (s, cmap[s]))

# frozen segmentation (prereg section 3.3): task start nprim nnoise
# task order in batch == CLASS id order
SEG_A = [(0, 0, 60, 60), (1, 150, 40, 40), (2, 250, 90, 90),
         (3, 474, 60, 60), (4, 624, 60, 60), (5, 774, 60, 60)]
SEG_B = [(0, 0, 60, 60), (1, 150, 40, 40), (2, 250, 90, 90),
         (3, 475, 60, 60), (4, 625, 60, 60), (5, 775, 60, 60)]
for name, seg in (('segments_A.txt', SEG_A), ('segments_B.txt', SEG_B)):
    with open(OUT + '/' + name, 'w') as f:
        for t, start, np, nn in seg:
            f.write('%d %d %d %d\n' % (t, start, np, nn))

# sanity: last task span end == batch line counts
for tag, seg, nb in (('A', SEG_A, 924), ('B', SEG_B, 925)):
    t, start, np, nn = seg[-1]
    nlines = sum(1 for _ in open(RERUN + '/batch_%s.txt' % tag))
    assert nlines == nb, (tag, nlines)
print('inputs written: classmap.txt (370), segments_A/B.txt')
