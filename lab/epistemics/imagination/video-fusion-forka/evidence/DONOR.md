# DONOR.md — FUSION FORK A, front-facing pig donor clip (Worker 1 deliverable)

## The clip (PRIMARY)

- **File:** `donor_frames/frame_0001.ppm` … `frame_0054.ppm` (54 frames, raw P6 PPM)
- **Resolution:** 480×854 (portrait — see note), 29.97 fps (30000/1001), ~1.8 s
- **Content window:** t=15.4 s → t=17.2 s of the source clip (frame-accurate seek)
- **What it shows:** a domestic pig, standing upright outdoors, lifting its head off a
  watermelon and looking **directly at the camera, head-up, dead-frontal**:
  - frames 0001–0006 (~t15.4–15.6): head lifting, 3/4 view
  - frames 0007–0045 (~t15.6–16.9): **dead-frontal, head up, both eyes and snout
    visible** (frame_0027 is the money frame)
  - frames 0046–0054 (~t16.9–17.2): pig approaches the lens, snout closeup, slightly right
- **Honesty caveats (read before fusing):**
  1. The pig is **dirty** — mud and watermelon juice on its snout/face. Real footage;
     not a defect to hide, but the fusion's texture mapping must expect it.
  2. The truly dead-frontal core is ~1.3 s (t15.7–16.9), not a full 3 s. The
     delivered 1.8 s window includes the head-lift lead-in and the snout-approach
     tail. There is no longer continuous frontal stretch in this clip.
  3. Source is **portrait 2160×3840**; frames were downscaled to 480×854.
     The pig's head fills most of the frame throughout the window, so a head-crop
     is trivial. If the fusion intake wants landscape, it should crop/scale itself.

## Source / license / author

- **Source file:** `File:Pigs Love Watermelon.webm` on Wikimedia Commons
- **Commons page:** https://commons.wikimedia.org/wiki/File:Pigs_Love_Watermelon.webm
- **Direct original (VP9, 2160×3840, 22.42 s, 40.5 MB):**
  https://upload.wikimedia.org/wikipedia/commons/6/67/Pigs_Love_Watermelon.webm
- **SHA-256 of downloaded original:** `8d4f4d43c7daa75cca245129e3133af83e7224577de8d9db4a028c1cc6f1ba30`
- **Original YouTube:** https://www.youtube.com/watch?v=RY_8iRuQ7GQ ("Pigs Love Watermelon")
- **Author:** Two Drs Homestead (https://www.youtube.com/@twodrshomestead), dated 2022-10-05
- **License:** **CC BY 3.0** (https://creativecommons.org/licenses/by/3.0) — free to use
  AND adapt (remix allowed, including this extraction), **with attribution**:
  credit "Two Drs Homestead", link the license, indicate changes. Any published
  use of the fused output must carry this attribution.
- **Species honesty:** *Sus scrofa domesticus* — **real domestic pig** (adult,
  reddish-brown sow), not AI-generated, not a boar/warthog stand-in. Verified by
  visual inspection and the Commons category `Videos of Sus scrofa domesticus`.
  No species fallback was needed.

## Extraction command (reproducible)

```bash
# 1. download the original
curl -sL -o watermelon_orig.webm \
  "https://upload.wikimedia.org/wikipedia/commons/6/67/Pigs_Love_Watermelon.webm"
# 2. extract the frontal window as raw PPM (accurate seek: -ss after -i)
ffmpeg -y -i watermelon_orig.webm -ss 15.4 -t 1.8 \
  -vf "scale=480:854" -r 30000/1001 \
  ~/workspace/fusion_forka/donor_frames/frame_%04d.ppm
```

- SHA-256 frame_0001.ppm: `0b4afec4eba2bea5398c51c1d74e8b1aa50fb75df8c14c1d766fc591b642256a`
- SHA-256 frame_0054.ppm: `0285776bfd2b0f6bf11f4674cb033f76b2a1de4730c8362a9402347aeefaff3a`
- Container/codec boundary (VP9→raw) stays outside TNN: the fusion intake reads
  only the raw PPMs. `ffmpeg` version on this box: run `ffmpeg -version` to log it.

## Why this clip

Step 6 proved the cross-view wall: the current donor's head is down for all 26 s
(the face is never observed). Micah ordered a front-facing pig clip. This is the
best freely-licensed **real, upright, dead-frontal, head-up** pig footage I could
find after a genuine multi-source search (search record below). The pig stands,
lifts its head, and looks straight into the lens — exactly the view the step-6
donor never gave.

## Alternate donor (NOT extracted — pull if wanted)

- **File:** `File:Pig Eating Candy.webm` (Wikimedia Commons), CC BY 3.0,
  author "Sorry Bro" (https://www.youtube.com/@sorrybro121)
- **Page:** https://commons.wikimedia.org/wiki/File:Pig_Eating_Candy.webm
- **Direct:** https://upload.wikimedia.org/wikipedia/commons/b/b8/Pig_Eating_Candy.webm
- **What:** 34.74 s, 852×480, 29.97 fps — a clean **white pig lying down indoors**,
  face pointed toward the camera for most of the clip, being hand-fed candy
  (chewing motion, mouth opens/closes). Longest continuous face-observed segment
  of any candidate, BUT the animal is reclined, not head-up/upright — anatomically
  a worse match for a head swap onto a standing bunny body. A human hand enters
  frame repeatedly. Pulled as backup only.

## Search record (what was checked and rejected)

- **Wikimedia Commons, `Category:Videos of Sus scrofa domesticus` (47 files surveyed):**
  - `2024-06-01 LJUBLJANA ZOO LJUBLJANA - pig.webm` (26 s, CC BY 3.0) — pig
    rooting with head DOWN for all 26 s (verified frame-by-frame; this matches
    the step-6 donor's description). REJECTED.
  - `Saerbeck - Wildfreigehege Nöttler Berg - Mangalica 01 ies.webm` (110 s,
    CC BY-SA 3.0, Frank Vincentz) — Mangalica rooting, head down the whole
    time. REJECTED.
  - `Hand Feeding a Baby Pig.webm` (9 s, CC BY 3.0) — piglet eating from a
    trough, head down; only a brief snout-lift toward a hand. REJECTED.
  - `Piglet Finds Safety and Friends.webm` (155 s, CC BY-SA 4.0, DxE) —
    activist montage with text overlays, distant shots, graphic content.
    REJECTED.
  - `Wuppertal - Zoo - Sus scrofa domesticus 01 (1).ogv` — 480p transcode
    corrupt (EBML parse failure); did not pursue.
  - Remaining 40 files: farm/slaughter/documentary footage with no frontal
    head-up candidate.
- **Vecteezy:** ruled out per standing order — hits are AI-generated or
  Pro-license (purchase). Not revisited.
- **Getty Images / Adobe Stock / Depositphotos:** purchase-only. Ruled out.
- **Pexels:** only AI-bundle files and a sleeping-pig clip surfaced — nothing
  frontal/head-up. Not usable.
- **Pixabay:** searched; no usable front-facing pig video found (mirror/aggregator
  dead ends only).
- **Internet Archive:** no usable frontal pig footage surfaced.
- No wild-boar/warthog fallback was needed (found a real domestic pig), so none
  was taken.
