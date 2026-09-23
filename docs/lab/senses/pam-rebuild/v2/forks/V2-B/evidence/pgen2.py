#!/usr/bin/env python3
"""V2-B: generate P1..P3 perturbation spans from G spans (frozen families).
Vectorized with numpy for speed. Deterministic, no RNG."""
import os, struct, json, hashlib, sys
import numpy as np

LAB = "/home/hatch/workspace/tnn-lab"
R24F = LAB + "/senses/pam-rebuild/round2/forks/R2-4/fixtures"
OUT = "/home/hatch/workspace/v2work/pspans"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
IMG = {0, 1, 2}
AUD = {3, 4}
MOT = {5}

def r24_flen(buf, tc):
    if tc in IMG:
        w, h = struct.unpack_from("<II", buf, 8)
        return 8 + w * h * 3
    if tc in AUD:
        sr, n = struct.unpack_from("<II", buf, 8)
        return 8 + n * 2
    if tc in MOT:
        nf, w, h = struct.unpack_from("<III", buf, 8)
        return 12 + nf * w * h * 3
    return -1

def perturb(buf_g, tc):
    """Return (p1, p2, p3) spans (header+payload) from G span bytes."""
    if tc in IMG:
        w, h = struct.unpack_from("<II", buf_g, 0)
        hdr = buf_g[:8]
        pay = np.frombuffer(buf_g[8:8+w*h*3], dtype=np.uint8).reshape(-1, 3).copy()
        p1 = np.empty_like(pay); p1[:,0]=pay[:,1]; p1[:,1]=pay[:,2]; p1[:,2]=pay[:,0]
        # P2: central third of payload BYTES
        p2b = pay.reshape(-1).copy(); a=len(p2b)//3; p2b[a:2*a]=0
        p2 = p2b.reshape(-1,3)
        # P3: XOR every payload BYTE with ((i*0x9E3779B9)>>16)&0xFF, i=byte index
        p3b = pay.reshape(-1).copy()
        idx = np.arange(len(p3b), dtype=np.int64)
        mask = ((idx*0x9E3779B9)>>16)&0xFF
        p3 = (p3b.astype(np.int64)^mask).astype(np.uint8).reshape(-1,3)
        return hdr+p1.tobytes(), hdr+p2.tobytes(), hdr+p3.tobytes()
    if tc in AUD:
        sr, n = struct.unpack_from("<II", buf_g, 0)
        hdr = buf_g[:8]
        pay = np.frombuffer(buf_g[8:8+n*2], dtype=np.int16).astype(np.float64)
        # 1.2x resample (pitch shift)
        src_idx = np.arange(n)*1.2
        i0 = np.floor(src_idx).astype(np.int64); i0=np.clip(i0,0,n-1)
        i1 = np.clip(i0+1,0,n-1); frac = src_idx-i0
        p1 = (pay[i0]*(1-frac)+pay[i1]*frac).clip(-32768,32767).astype(np.int16)
        # P2: central third of payload BYTES
        p2s = pay.astype(np.int16).copy()
        p2b = p2s.view(np.uint8); a=len(p2b)//3; p2b[a:2*a]=0
        p2 = p2b.view(np.int16)
        pb = pay.astype(np.int16).view(np.uint8).copy()
        idx = np.arange(len(pb), dtype=np.int64)
        mask = ((idx*0x9E3779B9)>>16)&0xFF
        p3 = (pb.astype(np.int64)^mask).astype(np.uint8)
        return hdr+p1.tobytes(), hdr+p2.tobytes(), hdr+p3.tobytes()
    if tc in MOT:
        nf, w, h = struct.unpack_from("<III", buf_g, 0)
        hdr = buf_g[:12]
        fs = w*h*3
        pay = np.frombuffer(buf_g[12:12+nf*fs], dtype=np.uint8).reshape(nf,fs).copy()
        p1 = pay[::-1].copy()
        # P2: central third of payload BYTES (flattened)
        p2f = pay.reshape(-1).copy(); a=len(p2f)//3; p2f[a:2*a]=0
        p2 = p2f.reshape(nf,fs)
        pf = pay.reshape(-1).copy()
        idx = np.arange(len(pf), dtype=np.int64)
        mask = ((idx*0x9E3779B9)>>16)&0xFF
        p3 = (pf.astype(np.int64)^mask).astype(np.uint8).reshape(nf,fs)
        return hdr+p1.tobytes(), hdr+p2.tobytes(), hdr+p3.tobytes()
    raise ValueError(tc)

def wrap_as_f(span, tc):
    return struct.pack("<II", 0x41343252, tc) + span

def main():
    os.makedirs(OUT, exist_ok=True)
    shard, nsh = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv)>2 else (0,1)
    files = sorted(f for f in os.listdir(R24F) if f.endswith(".r24"))
    files = [f for i,f in enumerate(files) if i % nsh == shard]
    ledger = {"families": {
        "P1": "channel-rotate RGB / 1.2x linear-resample PCM16 / frame-reverse motion",
        "P2": "central-third payload bytes zeroed",
        "P3": "XOR payload with ((i*0x9E3779B9)>>16)&0xFF"},
        "items": []}
    for fi, fn in enumerate(files):
        task = fn.split("_")[1]
        tc = TASKS.index(task)
        buf = open(os.path.join(R24F, fn), "rb").read()
        if struct.unpack_from("<I", buf, 0)[0] != 0x41343252: continue
        if struct.unpack_from("<i", buf, 4)[0] != tc: continue
        flen = r24_flen(buf, tc)
        if flen <= 0: continue
        g = buf[8+flen:]
        try:
            p1, p2, p3 = perturb(g, tc)
        except Exception as e:
            print(f"skip {fn}: {e}", flush=True); continue
        for pi, ps in (("P1",p1),("P2",p2),("P3",p3)):
            wrapped = wrap_as_f(ps, tc)
            on = os.path.join(OUT, f"{fn}.{pi}.r24")
            if not os.path.exists(on):
                open(on, "wb").write(wrapped)
            ledger["items"].append({"src": fn, "pert": pi,
                "sha": hashlib.sha256(wrapped).hexdigest()})
        if fi % 500 == 0: print(f"shard {shard}: {fi}/{len(files)}", flush=True)
    lp = os.path.join(OUT, f"ledger_{shard}.json")
    json.dump(ledger, open(lp, "w"))
    print(f"shard {shard} done: {len(ledger['items'])} spans", flush=True)

if __name__ == "__main__":
    main()
