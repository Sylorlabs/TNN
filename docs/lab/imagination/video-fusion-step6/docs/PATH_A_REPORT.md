# PATH A Report: View-Matched Donor Footage (front-facing pig)

## The question
Find REAL footage of the donor pig facing the SAME WAY as the recipient
bunny (front-facing, head up, face visible to the camera). No mirroring,
no 3D-guessing, no AI-generated stand-ins.

## Search 1: the local source (exhaustive)

Source: `pig_source.webm` — "2024-06-01 LJUBLJANA ZOO LJUBLJANA - pig", 26 s,
3840x2160, CC BY 3.0 (NaIzletuSi, via Wikimedia Commons). SHA-256
`b1dbe434629a1b02ffec629089be56dfe58b13d2cbc2f7e44bc205b9fb63540a`.
The same pig as the step-5 donor; the most honest possible PATH A material.

Method: full-video scan at 1 fps (26 frames, `fps=1,scale=160:120`), every
second inspected; ambiguous regions re-extracted at full resolution
(320x240); transition windows (fence->walk t=10.5-13.5, walk->puddle
t=21.5-24.5) extracted at 8 fps (24 frames each); donor segment frames
viewed at full 320x240.

Result, second by second:
- t=0-11: pig at the fence, head DOWN grazing (the step-5 donor window
  t=3-6 is inside this; full-res donor frames confirm the face is never
  visible — snout points at the ground, we see side/top of head).
- t=12-17: pig walks toward the camera, head DOWN (we see the crown of the
  head and ears, not the face).
- t=18-23: pig walks, head DOWN (side view, grazing posture).
- t=24-25: pig at the puddle, head DOWN drinking (faces the camera but the
  face points into the water).

**No second of the 26 shows the pig's head up with the face visible to the
camera. No 3.0 s front-facing window exists. The pig's face (eyes,
snout-front, mouth) is occluded or ground-pointing in every frame.**

## Search 2: the web (freely-licensed real footage)

- Wikimedia Commons pig videos: only activist investigation footage
  (disturbing, unusable), a misnamed glacier video, and the Ljubljana
  source itself. Nothing else.
- Pexels: photos only (not footage), plus one video of a pig SLEEPING
  (not facing the camera).
- Vecteezy "pig looking at camera" hits: marked AI GENERATED — ruled out
  ("do not fake it").
- Getty Images / Adobe Stock: purchase-license only (£150-375) — not
  freely sourceable; buying stock was not authorized.
- YouTube shorts ("piglet noticed the camera"): standard YouTube license,
  not CC; unclear rights for a committed research artifact — ruled out.

**No freely-licensed, real, front-facing pig video footage found.**

## Search 3: capture

No camera on this VM; the paired Mac cannot run shell commands for the
agent. New capture is not possible in this workstream.

## Verdict on PATH A: NEGATIVE (honest)

No view-matched donor footage exists in any source this workstream can
honestly use. PATH A stops here, per the brief. A negative is a result:
the program should not keep looking for front-facing pig footage of this
pair — it does not exist in the available sources.

What would unblock PATH A: a new capture session (a real pig filmed
head-up facing the camera for 3+ continuous seconds), or a different
donor animal with available front-facing footage.
