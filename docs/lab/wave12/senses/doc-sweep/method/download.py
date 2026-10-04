#!/usr/bin/env python3
"""Download tier1+tier2 docs from Drive to workspace. Checkpointed.
Read-only on Drive."""
import json, os, subprocess, sys

CLI = "hatch_gws_cli"
SWEEP = os.path.expanduser("~/workspace/tnn-lab/wave12/senses/doc-sweep")
DEST = f"{SWEEP}/docs_local"
os.makedirs(DEST, exist_ok=True)
CKPT = f"{SWEEP}/download_ckpt.json"

def main():
    tiers = json.load(open(f"{SWEEP}/tiers.json"))
    items = tiers["tier1"] + tiers["tier2"]
    done = set()
    if os.path.exists(CKPT):
        done = set(json.load(open(CKPT)))
    print(f"{len(items)} files, {len(done)} already downloaded", flush=True)
    n_new = 0
    for i, d in enumerate(items):
        key = f"{d['id']}"
        if key in done:
            continue
        safe = f"{i:04d}_{d['name']}".replace("/", "_")
        out = os.path.join(DEST, safe)
        cmd = [CLI, "drive", "files", "get",
               "--params", json.dumps({"fileId": d["id"], "alt": "media"}),
               "--output", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAIL {d['path']}: {r.stderr[:200]}", flush=True)
            continue
        done.add(key)
        n_new += 1
        if n_new % 25 == 0:
            json.dump(sorted(done), open(CKPT, "w"))
            print(f"... {n_new} new ({len(done)}/{len(items)})", flush=True)
    json.dump(sorted(done), open(CKPT, "w"))
    # manifest
    man = []
    for i, d in enumerate(items):
        safe = f"{i:04d}_{d['name']}".replace("/", "_")
        man.append({"local": safe, "drive_path": d["path"],
                    "drive_id": d["id"], "size": d.get("size"),
                    "modifiedTime": d.get("modifiedTime"),
                    "tier": "tier1" if i < len(tiers["tier1"]) else "tier2"})
    json.dump(man, open(f"{SWEEP}/manifest.json", "w"), indent=1)
    print(f"DONE downloaded={len(done)}/{len(items)}")

if __name__ == "__main__":
    main()
