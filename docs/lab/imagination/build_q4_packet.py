#!/usr/bin/env python3
"""Build imagination/Q4-PACKET.md: the 12 Q2 designs blinded as letters A-L
in a FIXED-seed presentation order.

Method: random.Random(20260922).shuffle over the 12 design ids; assign
letters A..L in shuffled order. The shuffle sets presentation order only
(it is not part of any decision path); the seed is a documented constant.
Descriptions are written in each design's OWN mode vocabulary (no
translation between modes). Mode is not labeled, though it may be
inferable from description style.
"""
import random

random.seed(20260922)
ids = [(m, b) for m in (0, 1) for b in range(1, 7)]  # m=0 machine, m=1 human
random.shuffle(ids)
letters = 'ABCDEFGHIJKL'
order = list(zip(letters, ids))

BRIEF = {
    1: ("Logo for a bakery called 'Crumb & Craft'. The brief asks for a grain "
        "motif, a warm color palette, no more than four elements, and a design "
        "that stays legible when small."),
    2: ("Poster for a jazz night. The brief asks for a night feel, reserved "
        "text space for the date and venue, and a cool palette with exactly "
        "one warm accent."),
    3: ("A four-note chime for a shop door. The brief asks for a welcoming "
        "sound: a rising contour that ends stable."),
    4: ("A three-note error buzz for a kiosk. The brief asks for an "
        "attention-getting sound built on tense intervals."),
    5: ("Five blocks arranged on a shelf. The brief asks for the largest "
        "block at the bottom, no overhang, and all blocks front-visible."),
    6: ("Four stones placed in a garden square. The brief asks for asymmetric "
        "balance, one dominant stone, and an airy feel with at least three of "
        "the nine zones left empty."),
}

# Faithful descriptions in each design's OWN mode vocabulary, transcribed
# from the E-lines in logs/q2m.txt and logs/q2h.txt.
DESC = {
    (0, 1): ("A triangle 80 by 80 at x 500, y 167, in RGB 200 60 30; a circle "
             "100 by 100 at x 500, y 500, in RGB 200 60 30; and a text panel "
             "200 by 60 at x 500, y 833, in RGB 240 200 90."),
    (1, 1): ("A sharp-angled, slightly curved, asymmetric warm-red triangle in "
             "the top left; a round, smooth, symmetric warm-red circle in "
             "the top right; and a very angular, slightly curved, "
             "near-symmetric warm-red text panel in the bottom center."),
    (0, 2): ("A circle 120 by 120 at x 500, y 500, in RGB 120 170 230; a "
             "rectangle 200 by 120 at x 500, y 500, in RGB 220 220 225; a text "
             "panel 160 by 50 at x 500, y 833, in RGB 240 200 90; and a second "
             "text panel 160 by 50 at x 500, y 833, in RGB 20 20 20."),
    (1, 2): ("A round, smooth, symmetric neutral-gray-blue circle in the top "
             "middle; a very angular, slightly curved, near-symmetric "
             "neutral-gray-blue rectangle at the center; a very angular, "
             "slightly curved, near-symmetric white text panel in the bottom "
             "center; and a very angular, slightly curved, near-symmetric "
             "warm-amber text panel also in the bottom center."),
    (0, 3): ("Four notes, each 250 ms at amplitude 800: 262 Hz, 262 Hz, "
             "349 Hz, 523 Hz."),
    (1, 3): ("Four soft bell notes in order: a low one, a low one, a low one, "
             "and one a small step higher."),
    (0, 4): ("Three notes, each 150 ms at amplitude 800: 262 Hz, 523 Hz, "
             "349 Hz."),
    (1, 4): ("Three soft bell notes in order: a mid one, one a step higher, "
             "and a mid one again."),
    (0, 5): ("Five blocks, all at y 850 on the shelf: at x 200 a stack of "
             "three (40 wide with its base at height 200, 80 wide with its "
             "base at height 120, 120 wide on the shelf); a 160-wide block on "
             "the shelf at x 500; and a 200-wide block on the shelf at x 800."),
    (1, 5): ("Five blocks: in the bottom-left zone a stack of three — the "
             "smallest (size rank 1) stacked on the mid-small (rank 2) stacked "
             "on the mid (rank 3) sitting on the ground; a large block "
             "(rank 4) on the ground in the bottom-middle zone; and the "
             "largest block (rank 5) on the ground in the bottom-right zone."),
    (0, 6): ("Four stones, all at ground level: size 50 at x 167, y 167; "
             "size 100 at x 167, y 500; size 150 at x 500, y 500; size 200 at "
             "x 833, y 500."),
    (1, 6): ("Four stones: the smallest (size rank 1) in the top-left zone, "
             "rank 2 in the top-middle zone, rank 3 in the top-right zone, "
             "and the largest (rank 4) in the middle-left zone; no stacking "
             "relations."),
}

L = []
L.append("# Q4 — BLIND DESIGN RATING PACKET")
L.append("")
L.append("**Protocol:** frozen in PREREG.md. The 12 Q2 designs below are blinded "
         "as letters A–L in a deterministic presentation order (Fisher–Yates "
         "shuffle with fixed seed `20260922`; the shuffle sets presentation "
         "order only and is not part of any decision path). Which mode "
         "produced each design is NOT labeled — though the mode may be "
         "inferable from the description style, since each design is described "
         "faithfully in its own mode's vocabulary (raw values vs qualitative "
         "percepts) with no translation between modes.")
L.append("")
L.append("**Rater instruction — Micah: rate each design 1–10 on how good it "
         "is as a design for its brief.**")
L.append("")
for letter, (m, b) in order:
    L.append(f"## Design {letter}")
    L.append("")
    L.append(f"**Brief:** {BRIEF[b]}")
    L.append("")
    L.append(f"**Design:** {DESC[(m, b)]}")
    L.append("")
    L.append(f"**Rating (1–10):** ___")
    L.append("")
L.append("---")
L.append("")
L.append("## Rating sheet")
L.append("")
L.append("| Design | Rating (1–10) |")
L.append("|--------|---------------|")
for letter, _ in order:
    L.append(f"| {letter} |  |")
L.append("")
L.append(f"_Presentation order seed: 20260922 → order: "
         f"{' '.join(f'{l}=(mode{m},brief{b})' for l, (m, b) in order)}_ "
         "(mapping kept in this packet footer for unblinding after rating; "
         "the rater should not read past this line until ratings are done.)")
L.append("")

with open('/home/hatch/workspace/tnn-lab/imagination/Q4-PACKET.md', 'w') as f:
    f.write('\n'.join(L))
print("order:", ' '.join(f'{l}=(m{m},b{b})' for l, (m, b) in order))
print("wrote imagination/Q4-PACKET.md")
