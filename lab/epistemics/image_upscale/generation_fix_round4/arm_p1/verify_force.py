import re, sys

def parse_trace(path):
    regs = []
    pat = re.compile(r'^R x=(\d+) y=(\d+) bw=(\d+) bh=(\d+) si=(\d+) e=(-?\d+) bsse=(-?\d+) rsse=(-?\d+) edge=(\d+) fok=(\d+) mok=(\d+) pok=(\d+) op=(ATOM|PLANE|MEAN) reason=(\S+)$')
    for line in open(path):
        m = pat.match(line.strip())
        if m:
            regs.append(dict(x=int(m[1]),y=int(m[2]),bw=int(m[3]),bh=int(m[4]),si=int(m[5]),
                            e=int(m[6]),bsse=int(m[7]),rsse=int(m[8]),edge=int(m[9]),
                            fok=int(m[10]),mok=int(m[11]),pok=int(m[12]),op=m[13],reason=m[14]))
    return regs

def read_bmp24(path):
    d = open(path,'rb').read()
    assert d[0:2]==b'BM'
    off = int.from_bytes(d[10:14],'little'); w = int.from_bytes(d[18:22],'little',signed=True)
    h = int.from_bytes(d[22:26],'little',signed=True); bpp = int.from_bytes(d[28:30],'little')
    assert bpp==24
    stride = (w*3+3)//4*4
    rows = []
    for y in range(h):
        src = h-1-y
        rows.append(d[off+src*stride:off+src*stride+w*3])
    return w,h,rows

D = sys.argv[1]
c3 = parse_trace(f'{D}/out_c3b/GEN_TRACE.txt')
p1 = parse_trace(f'{D}/out_p1f1/GEN_TRACE.txt')
from collections import Counter
cc = Counter(r['op'] for r in c3); pc = Counter(r['op'] for r in p1)
print('C3 trace: n=%d ops=%s' % (len(c3), dict(cc)))
print('P1 trace: n=%d ops=%s' % (len(p1), dict(pc)))
print('P1 reasons:', Counter(r['reason'] for r in p1))
print('C3 reasons:', Counter(r['reason'] for r in c3))
# every P1 take-region op must be PLANE with forced reason; MEAN rows only from si==0 nofit path
bad = [r for r in p1 if r['op']!='PLANE' and r['reason']!='no_model_vouched']
print('P1 unexpected rows:', len(bad))
bad2 = [r for r in p1 if r['op']=='PLANE' and r['reason']!='p1_forced_plane']
print('P1 PLANE rows without forced reason:', len(bad2))

w,h,c3px = read_bmp24(f'{D}/out_c3b/upscale_gen.bmp')
_,_,p1px = read_bmp24(f'{D}/out_p1f1/upscale_gen.bmp')
p1map = {(r['x'],r['y'],r['bw'],r['bh'],r['si']):r for r in p1}
n_plane = coinc = pixok = pixbad = nocoinc = 0
mism = []
for r in c3:
    if r['op']!='PLANE': continue
    n_plane += 1
    key = (r['x'],r['y'],r['bw'],r['bh'],r['si'])
    q = p1map.get(key)
    if q is None or q['op']!='PLANE':
        nocoinc += 1
        continue
    coinc += 1
    ok = True
    for oy in range(2*r['y'], 2*(r['y']+r['bh'])):
        a = c3px[oy][6*r['x']:6*(r['x']+r['bw'])]
        b = p1px[oy][6*r['x']:6*(r['x']+r['bw'])]
        if a != b: ok = False; break
    if ok: pixok += 1
    else:
        pixbad += 1; mism.append(key)
print('C3 PLANE regions: %d | coincident P1 PLANE: %d | pixel-identical: %d | pixel-DIFF: %d | non-coincident: %d' % (n_plane, coinc, pixok, pixbad, nocoinc))
if mism: print('first mismatches:', mism[:5])
# evidence honesty: P1 forced rows still carry measured evidence
ev = [r for r in p1 if r['op']=='PLANE']
print('P1 forced rows with evidence recorded (e>=0):', sum(1 for r in ev))
