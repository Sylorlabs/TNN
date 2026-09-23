#!/usr/bin/env python3
"""Parallel R2A adversarial generation by task."""
import os, sys, hashlib, json
sys.path.insert(0, os.path.expanduser("~/workspace/r28work"))
import gen_r2a as G

def gen_task(ti, start_idx=0):
    out = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures/r2a")
    adir = os.path.join(out, "adversarial")
    os.makedirs(adir, exist_ok=True)
    n_photos = 170
    manifest = []
    scenes = {}
    idx = 0
    for fam, cnt in G.FAMS[ti]:
        fn = G.A_GEN[fam]
        for local in range(cnt):
            # Always compute scene metadata (deterministic, fast if file exists)
            # But skip expensive file generation if already done
            fname = "r2a_%s_%04d%s" % (G.TASKS[ti], idx, G.EXTS[ti])
            fpath = os.path.join(adir, fname)
            if idx < start_idx and os.path.exists(fpath):
                # File exists, need scene metadata. Regenerate metadata only
                # (the A_GEN returns scene; we can call it but skip writing)
                # Actually, just call it - it will overwrite identically
                if fam in G.NEEDS_PHOTOS:
                    p, t, f, scene = fn(idx, adir, n_photos)
                else:
                    p, t, f, scene = fn(idx, adir)
                scenes[os.path.basename(p)] = {"family": fam, "truth": t, "scene": scene}
                # Don't add to manifest (already there from previous run)
                idx += 1
                continue
            if fam in G.NEEDS_PHOTOS:
                p, t, f, scene = fn(idx, adir, n_photos)
            else:
                p, t, f, scene = fn(idx, adir)
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            manifest.append((h, os.path.relpath(p, out)))
            h2 = hashlib.sha256(open(p + ".truth", "rb").read()).hexdigest()
            manifest.append((h2, os.path.relpath(p + ".truth", out)))
            scenes[os.path.basename(p)] = {"family": fam, "truth": t, "scene": scene}
            idx += 1
            if idx % 50 == 0:
                print("  %s idx %d" % (G.TASKS[ti], idx), flush=True)
    # Merge manifest if resuming
    man_path = os.path.join(out, "MANIFEST_adv_%s.part" % G.TASKS[ti])
    if start_idx > 0 and os.path.exists(man_path):
        with open(man_path) as f:
            existing = [line.strip() for line in f]
    else:
        existing = []
    with open(man_path, "w") as f:
        for line in existing:
            f.write(line + "\n")
        for h, rel in manifest:
            f.write("%s  %s\n" % (h, rel))
    scenes_path = os.path.join(out, "SCENES_%s.part.json" % G.TASKS[ti])
    with open(scenes_path, "w") as f:
        json.dump(scenes, f)
    print("adversarial %s done: %d" % (G.TASKS[ti], idx), flush=True)

if __name__ == "__main__":
    ti = int(sys.argv[1])
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    gen_task(ti, start)
