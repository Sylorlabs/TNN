#!/usr/bin/env python3
"""Convert v5g .npz model to Zag binary format for rb_longmem.zag.

Format (all little-endian):
  0:  magic 8 bytes: b'RBLMEMv5'
  8:  P u64, K u64, N u64, sr u64
  40: a[P] f64
  40+8P: proto[K] f64
  ...: bg[K*K*K] u64
  ...: ob0 u64, ob1 u64
  ...: floorv f64, attackv f64
  ...: frlen u64, eplen u64, EP[eplen] f64
  ...: pT u64, T0 f64, NBINS u64
  ...: plm[NBINS] f64, PMF[17] f64, boost f64
"""
import struct, sys, numpy as np

def load_npz(path):
    m = dict(np.load(path, allow_pickle=True))
    for k in ('q','uni','bg'):
        if k in m: m[k] = m[k].astype(np.int64)
    for k in ('P','K','pT','NBINS','ob0','ob1','frlen','n','sr'):
        m[k] = int(m[k])
    return m

def convert(npz_path, bin_path):
    m = load_npz(npz_path)
    P,K,N,sr = m['P'],m['K'],m['n'],m['sr']
    out = bytearray()
    out += b'RBLMEMv5'
    out += struct.pack('<4Q', P, K, N, sr)
    out += struct.pack(f'<{P}d', *m['a'])
    out += struct.pack(f'<{K}d', *m['proto'])
    bg = m['bg'].astype(np.uint64)
    out += struct.pack(f'<{K*K*K}Q', *bg.flatten())
    out += struct.pack('<2Q', m['ob0'], m['ob1'])
    out += struct.pack('<2d', m['floorv'], m['attackv'])
    EP = m['EP']; eplen = len(EP)
    out += struct.pack('<2Q', m['frlen'], eplen)
    out += struct.pack(f'<{eplen}d', *EP)
    pT = m['pT']; T0 = float(m['T0']); NBINS = m['NBINS']
    out += struct.pack('<Q', pT)
    out += struct.pack('<d', T0)
    out += struct.pack('<Q', NBINS)
    plm = m['plm'] if len(m['plm'])>0 else np.zeros(0)
    out += struct.pack(f'<{NBINS}d', *plm)
    PMF = m['PMF'] if len(m['PMF'])>0 else np.zeros(17)
    out += struct.pack('<17d', *PMF)
    out += struct.pack('<d', float(m.get('boost',1.0)))
    # score q (for reemit): N u64 indices
    q = m['q'].astype(np.int64)
    out += struct.pack(f'<{len(q)}q', *q)
    open(bin_path,'wb').write(out)
    print(f'{npz_path} -> {bin_path} ({len(out)} bytes)')

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
