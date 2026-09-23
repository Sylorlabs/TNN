#!/usr/bin/env python3
"""convert.py — extract frames from each downloaded video and write 8-frame
64x64 .vid windows.

Usage: convert.py [raw_dir] [windows_dir] [stride_frames]
Pipeline per video (deterministic, zero RNG):
  ffmpeg -i raw/<id>.mp4
      -vf "crop=min(iw,ih):min(iw,ih),scale=64:64" (center square crop)
      -pix_fmt rgb24 -f rawvideo frames.raw
  then slice: window k = frames[k*stride : k*stride+8], k = 0..
  writes windows/<id>_w<k:03d>.vid via vidio.write_vid
  plus convert_log.tsv (video_id, window_idx, start_frame, fps, src_sha256)

Why center-crop, not stretch: keeps pixel aspect 1:1; recorded in the log.
Stride default 30 (per task spec example); overlap = 7 frames between windows.
ffmpeg swscale is deterministic on identical input bytes (proven by rerun test).
"""
import csv, hashlib, os, subprocess, sys

WORK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WORK)
from vidio import write_vid  # noqa: E402

W = H = 64
NF = 8

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def probe_fps(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=avg_frame_rate",
                        "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    num, den = r.stdout.strip().split("/")
    return float(num) / float(den)

def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "raw")
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(WORK, "windows")
    stride = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    os.makedirs(outdir, exist_ok=True)
    log_path = os.path.join(outdir, "convert_log.tsv")

    manifest = os.path.join(WORK, "manifest.tsv")
    vids = []
    with open(manifest) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            vids.append(line.rstrip("\n").split("\t")[0])

    with open(log_path, "w") as log:
        log.write("# video_id\twindow_idx\tstart_frame\tstride\tfps\tsrc_sha256\n")
        for vid in vids:
            src = os.path.join(raw, vid + ".mp4")
            if not os.path.exists(src):
                print("SKIP %s (no download)" % vid)
                continue
            src_sha = sha256(src)
            fps = probe_fps(src)
            rawf = os.path.join(outdir, vid + "_frames.raw")
            vf = "crop=min(iw\\,ih):min(iw\\,ih),scale=64:64"
            cmd = ["ffmpeg", "-y", "-v", "error", "-i", src,
                   "-vf", vf, "-pix_fmt", "rgb24", "-f", "rawvideo", rawf]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print("ERROR ffmpeg %s: %s" % (vid, r.stderr.strip()[:200]))
                continue
            fsz = W * H * 3
            total = os.path.getsize(rawf) // fsz
            data = open(rawf, "rb").read()
            k = 0
            while k * stride + NF <= total:
                frames = [data[(k * stride + j) * fsz:(k * stride + j + 1) * fsz]
                          for j in range(NF)]
                name = "%s_w%03d.vid" % (vid, k)
                write_vid(os.path.join(outdir, name), W, H, frames)
                log.write("%s\t%d\t%d\t%d\t%.3f\t%s\n"
                          % (vid, k, k * stride, stride, fps, src_sha))
                k += 1
            os.remove(rawf)
            print("%s: %d frames @ %.2f fps -> %d windows (stride %d)"
                  % (vid, total, fps, k, stride))
    print("convert complete")

if __name__ == "__main__":
    sys.exit(main())
