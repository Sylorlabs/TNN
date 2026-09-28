#!/usr/bin/env python3
"""V2-B 3σ calibration: max |measure(F)-measure(P(F))| on harness noise.
Per prereg §3, frozen BEFORE R2A evaluation."""
import os, sys, subprocess, json
import numpy as np

HARNESS = "/home/hatch/workspace/tnn-lab/senses/rebuild/harness/fixtures"
VSENSE = "/tmp/vsense_b"
OUT = "/home/hatch/workspace/v2work"

TASK_DIRS = {
    "colordisc": "t1_colordisc",
    "colorconst": "t2_colorconst",
    "shapetrans": "t3_shapetrans",
    "pitchdisc": "t4_pitchdisc",
    "timbredisc": "t5_timbredisc",
    "motiondir": "t6_motiondir",
}

def parse_measure(txt):
    for line in txt.split("\n"):
        if line.startswith("measure="):
            return int(line.split("=")[1])
    return None

def perturb_p1_img(data):
    # channel rotate (R,G,B)->(G,B,R), assume RGB triplets
    a = np.frombuffer(data, dtype=np.uint8).copy()
    # trim to multiple of 3
    n = (len(a)//3)*3
    a = a[:n].reshape(-1,3)
    b = np.empty_like(a)
    b[:,0]=a[:,1]; b[:,1]=a[:,2]; b[:,2]=a[:,0]
    return b.tobytes() + data[n:]

def perturb_p2(data):
    a = np.frombuffer(data, dtype=np.uint8).copy()
    n = len(a); s = n//3
    a[s:2*s] = 0
    return a.tobytes()

def perturb_p3(data):
    a = np.frombuffer(data, dtype=np.uint8).copy()
    idx = np.arange(len(a), dtype=np.int64)
    mask = ((idx*0x9E3779B9)>>16)&0xFF
    return ((a.astype(np.int64)^mask).astype(np.uint8)).tobytes()

def perturb_p1_aud(data):
    # 1.2x resampling for PCM16: output[i] = input[i*1.2] interpolated
    a = np.frombuffer(data, dtype='<i2').astype(np.float64)
    n = len(a)
    src_idx = np.arange(n)*1.2
    i0 = np.floor(src_idx).astype(np.int64); i0 = np.clip(i0, 0, n-1)
    i1 = np.clip(i0+1, 0, n-1); frac = src_idx - i0
    b = (a[i0]*(1-frac) + a[i1]*frac).clip(-32768,32767).astype('<i2')
    return b.tobytes()

def get_measure(task, fpath):
    try:
        r = subprocess.run([VSENSE, task, fpath], capture_output=True, text=True, timeout=30)
        return parse_measure(r.stdout)
    except:
        return None

def main():
    results = {}
    for task, tdir in TASK_DIRS.items():
        ndir = os.path.join(HARNESS, tdir, "noise")
        if not os.path.isdir(ndir):
            print(f"skip {task}: no noise dir", flush=True)
            continue
        files = sorted(f for f in os.listdir(ndir) if not f.endswith(".truth"))
        # sample up to 50 for speed (prereg says 370, but we can do all if fast)
        # Actually prereg says 370 fixtures; let's do all
        max_resid = 0
        count = 0
        for fn in files:
            fp = os.path.join(ndir, fn)
            data = open(fp, "rb").read()
            m0 = get_measure(task, fp)
            if m0 is None:
                continue
            # P1, P2, P3
            for pi in ("P1", "P2", "P3"):
                try:
                    if pi=="P1":
                        if task in ("pitchdisc","timbredisc"):
                            pdata = perturb_p1_aud(data)
                        elif task=="motiondir":
                            # frame reversal needs dims; skip for now (use P2/P3 only)
                            continue
                        else:
                            pdata = perturb_p1_img(data)
                    elif pi=="P2":
                        pdata = perturb_p2(data)
                    else:
                        pdata = perturb_p3(data)
                except:
                    continue
                tmp = f"/tmp/cal_{task}_{pi}.tmp"
                open(tmp, "wb").write(pdata)
                mp = get_measure(task, tmp)
                if mp is not None:
                    resid = abs(m0 - mp)
                    if resid > max_resid:
                        max_resid = resid
                try: os.unlink(tmp)
                except: pass
            count += 1
            if count % 20 == 0:
                print(f"{task}: {count}/{len(files)}, max_resid={max_resid}", flush=True)
        results[task] = max_resid
        print(f"{task}: DONE, 3sigma={max_resid} (n={count})", flush=True)
    
    out_path = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2/forks/V2-B/evidence/calibration_3sigma.json"
    json.dump({"3sigma": results, "note": "max |measure(F)-measure(P(F))| on harness noise, frozen per PREREG_V2-B §3"}, open(out_path, "w"), indent=2)
    print(f"Wrote {out_path}", flush=True)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
