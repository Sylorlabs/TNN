#!/usr/bin/env python3
"""Waveform analyzer-first: HNR, spectra, envelope, F0 track, hum audit, regularity."""
import sys, math
import numpy as np

def read_wav(p):
    import struct
    d = open(p,'rb').read()
    assert d[0:4]==b'RIFF' and d[8:12]==b'WAVE'
    pos=12; sr=None; ch=None; bits=None; data=None
    while pos < len(d):
        cid=d[pos:pos+4]; sz=struct.unpack('<I',d[pos+4:pos+8])[0]
        if cid==b'fmt ':
            fmt,chn,sr_,br,ba,bits_=struct.unpack('<HHIIHH',d[pos+8:pos+24])
            sr, ch, bits = sr_, chn, bits_
        elif cid==b'data':
            data=d[pos+8:pos+8+sz]
        pos+=8+sz+(sz&1)
    n=len(data)//(bits//8)//ch
    x=np.frombuffer(data,dtype=np.int16).astype(np.float64)
    if ch>1: x=x.reshape(-1,ch)[:,0]
    return x, sr

def f0_track(x, sr, fmin=60, fmax=1200):
    n=len(x); hop=sr//50; out=[]
    w=np.hanning(sr//20)
    for s in range(0, n-sr//20, hop):
        seg=x[s:s+sr//20]*w
        seg-=seg.mean()
        r0=np.dot(seg,seg)+1e-12
        best=0; blag=0
        for lag in range(int(sr/fmax), int(sr/fmin)+1):
            v=np.dot(seg[:len(seg)-lag], seg[lag:])/r0
            if v>best: best,blag=v,lag
        out.append((s/sr, sr/blag if blag>0 and best>0.3 else 0.0, best))
    return out

def hnr_blocks(x, sr, nb=20, f0med=0.0):
    n=len(x); out=[]
    lag=int(sr/f0med) if f0med>50 else int(sr/300)
    for b in range(nb):
        s0=b*n//nb; s1=(b+1)*n//nb
        seg=x[s0:s1].astype(float); seg-=seg.mean()
        if len(seg)<=lag or lag<=0: out.append(-60.0); continue
        r0=np.dot(seg,seg)+1e-12
        harm=np.dot(seg[:len(seg)-lag],seg[lag:])/r0
        harm=min(max(harm,1e-6),0.999999)
        out.append(10*math.log10(harm/(1-harm)))
    return out

def spectral_centroid_blocks(x, sr, nb=20):
    n=len(x); out=[]
    for b in range(nb):
        s0=b*n//nb; s1=(b+1)*n//nb
        seg=x[s0:s1]*np.hanning(s1-s0)
        X=np.abs(np.fft.rfft(seg)); fr=np.fft.rfftfreq(len(seg),1/sr)
        out.append(float(np.sum(fr*X)/(np.sum(X)+1e-12)))
    return out

def hum_audit(x, sr):
    n=len(x); w=x*np.hanning(n)
    X=np.abs(np.fft.rfft(w)); fr=np.fft.rfftfreq(n,1/sr)
    tot=X.sum()
    res={}
    for f in (50,60,100,120,150,180):
        m=(fr>f-2)&(fr<f+2)
        res[f]=float(X[m].sum()/(tot+1e-12))
    return res

def zc_blocks(x, sr, nb=20):
    n=len(x); out=[]
    for b in range(nb):
        s0=b*n//nb; s1=(b+1)*n//nb
        seg=x[s0:s1]
        zc=np.sum((seg[:-1]<0)!=(seg[1:]<0))
        out.append(zc/(len(seg)/sr))
    return out

def report(p, label):
    x, sr = read_wav(p)
    dur=len(x)/sr
    nb2=100; env=np.array([np.abs(x[b*len(x)//nb2:(b+1)*len(x)//nb2]).mean() for b in range(nb2)])
    f0=f0_track(x,sr)
    voiced=[f for _,f,c in f0 if f>0]
    print(f"== {label} ({p}) ==")
    print(f"  sr={sr} dur={dur:.2f}s peak={np.abs(x).max():.0f} rms={np.sqrt((x**2).mean()):.1f}")
    print(f"  env: max={env.max():.0f} mean={env.mean():.1f} max/mean={env.max()/(env.mean()+1e-9):.1f} (stationarity: low ratio=steady)")
    if voiced:
        print(f"  F0: voiced {len(voiced)}/{len(f0)} median={np.median(voiced):.1f}Hz range=({min(voiced):.0f},{max(voiced):.0f})")
    else:
        print("  F0: unvoiced")
    f0m=np.median(voiced) if voiced else 0.0
    print(f"  HNR blocks: "+" ".join(f"{v:+.1f}" for v in hnr_blocks(x,sr,f0med=f0m)))
    print(f"  centroid blocks: "+" ".join(f"{v:.0f}" for v in spectral_centroid_blocks(x,sr)))
    print(f"  hum audit: "+" ".join(f"{k}Hz:{v*100:.2f}%" for k,v in hum_audit(x,sr).items()))
    zc=zc_blocks(x,sr)
    print(f"  zero-cross/s: "+" ".join(f"{v:.0f}" for v in zc[:10]))
    # unnatural regularity: autocorr of envelope at 0.1-2s lags
    e=env-env.mean(); r0=np.dot(e,e)+1e-12
    lags=np.arange(max(2,int(0.1*len(e))), min(len(e)-2,int(2.0*len(e))))
    if len(lags)>3:
        rr=[np.dot(e[:len(e)-l],e[l:])/r0 for l in lags]
        i=int(np.argmax(rr)); print(f"  env periodicity: max autocorr {rr[i]:.3f} at lag {lags[i]/len(e)*dur:.2f}s (high=loop-like)")
    else:
        print("  env periodicity: n/a (too short)")
    return x, sr

if __name__=='__main__':
    for p in sys.argv[1:]:
        report(p, p.split('/')[-1])
