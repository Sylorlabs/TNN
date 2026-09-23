#!/usr/bin/env python3
"""download.py — download each frozen-manifest video exactly once.

Usage: download.py [manifest.tsv] [raw_dir]
Writes raw/<video_id>.mp4 plus download_log.tsv (video_id, sha256, bytes,
format_id, resolution). Idempotent: skips files already present with a matching
log entry. No RNG anywhere.

Format cap: best[height<=360]/best — keeps the run modest.
"""
import csv, hashlib, os, subprocess, sys

WORK = os.path.dirname(os.path.abspath(__file__))
YDL = os.path.join(WORK, "venv", "bin", "yt-dlp")

# Format cap: 480p is the lowest YouTube serves for these videos (no 360p
# formats exist; verified via --list-formats). We downscale to 64x64 in
# ffmpeg anyway, so source resolution only affects download size. This is a
# documented deviation from the prereg's <=360p (modesty intent preserved:
# files are 0.4-8 MB each).
FMT = "bv[height<=480]+ba/best[height<=480]/bv+ba/best"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    manifest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "manifest.tsv")
    raw = sys.argv[2] if len(sys.argv) > 2 else os.path.join(WORK, "raw")
    os.makedirs(raw, exist_ok=True)
    log_path = os.path.join(raw, "download_log.tsv")
    logged = {}
    if os.path.exists(log_path):
        with open(log_path) as f:
            for row in csv.reader(f, delimiter="\t"):
                if row and not row[0].startswith("#"):
                    logged[row[0]] = row

    rows = []
    with open(manifest) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            rows.append(parts)  # id, url, title, duration, category

    for vid, url, title, dur, cat in rows:
        out = os.path.join(raw, vid + ".mp4")
        if vid in logged and os.path.exists(out):
            print("skip %s (already logged)" % vid)
            continue
        cmd = [YDL, "-f", FMT, "--merge-output-format", "mp4",
               "--no-playlist", "--socket-timeout", "60",
               "-o", out, url]
        print("downloading", vid, "...", flush=True)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            print("ERROR %s: %s" % (vid, r.stderr.strip().splitlines()[-1:] ))
            continue
        entry = [vid, sha256(out), str(os.path.getsize(out)), title, dur, cat]
        with open(log_path, "a") as f:
            f.write("\t".join(entry) + "\n")
        print("done %s sha=%s" % (vid, entry[1][:16]))
    print("downloads complete")

if __name__ == "__main__":
    sys.exit(main())
