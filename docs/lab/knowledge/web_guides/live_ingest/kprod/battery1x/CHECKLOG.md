# CHECKLOG.md — battery1x protocol checks (PREREG_KPROD §3.1)

Checker: `check_protocol.py` implements the frozen §2.2 `kb_tv` pair rule in
Python (lowercase → `[a-z0-9]+` tokens minl=2 → exact-drop of the taught G1
DROP stoplist → `tok_match` prefix semantics → `overlap` counts; bind =
`3*sh >= 2*an`; AGREE = bind + full coverage + exact digit-multiset equality;
CONTRADICT = bind + candidate has ≥1 digit token + digits differ).
Full pass output: `/tmp/check2.log` (this session), reproducible via
`python3 check_protocol.py` (exit 0 = all pass).

12 reference claims: `../knowledge_base.txt` (pin 6552481b... per §6).

## Check suite (all PASS on the final battery)

**A. Novel claims: no-bind vs all 12 original claims** (both orientations:
novel→claim and claim→novel), plus PARSE gate (≥4 tokens, ≤600 chars, no `|`).
24/24 pass. Worst overlaps (fraction of candidate content tokens matching):

| cluster | claim | worst vs 12 |
|---|---|---|
| pn-01 | Venus completes one orbit of the Sun in about 225 days. | 0.25 (claim#9) |
| pn-02 | Honeybees have five eyes: two large compound eyes and three small simple ones. | 0.08 (claim#12) |
| pn-03 | The Amazon River flows more than 6400 kilometers from the Andes to the Atlantic. | 0.10 (claim#2) |
| pn-04 | The adult human brain weighs roughly 1400 grams. | 0.29 (claim#5) |
| pn-05 | Sound travels through air at about 343 metres per second near room temperature. | 0.23 (claim#6) |
| pn-06 | The Library of Congress in Washington holds more than 170 million cataloged items. | 0.00 |
| pn-07 | Jupiter is circled by at least 95 officially recognized moons. | 0.11 (claim#3) |
| pn-08 | Leonardo da Vinci painted the Mona Lisa in the early 1500s. | 0.12 (claim#9) |
| pf-01 | The Sahara Desert covers about 2 million square kilometers. (false; true ≈9M) | 0.29 |
| pf-02 | Emperor penguins migrate north each winter by flying hundreds of kilometers. (false; penguins cannot fly) | 0.10 |
| pf-03 | A newborn human baby has about 400 bones in its body. (false; true ≈270–300) | 0.25 |
| pf-04 | Pure gold melts at 500 degrees Celsius. (false; true 1064°C) | 0.33 |
| pf-05 | The Nile River stretches only 2000 kilometers from source to sea. (false; true ≈6650 km) | 0.33 |
| pf-06 | Saturn has exactly 12 confirmed moons. (false; true 146+) | 0.20 |
| pf-07 | The Statue of Liberty stands 200 metres tall from base to torch. (false; true 93 m) | 0.33 |
| pf-08 | The Great Pyramid of Giza was completed around 500 BC. (false; true ≈2560 BC) | 0.14 |
| pc-01 | The Amazon rainforest spans about 5500000 square kilometers. | 0.12 |
| pc-02 | A Boeing 747 typically seats about 660 passengers. | 0.14 |
| pc-03 | The Burj Khalifa rises 828 metres above the ground. | 0.43 (claim#7) |
| pc-04 | Lake Baikal plunges to a maximum depth of 1642 metres. | 0.14 |
| pc-05 | The Colosseum in Rome could hold about 50000 spectators. | 0.14 |
| pc-06 | The International Space Station circles Earth near 420 kilometers altitude. | 0.22 |
| pc-07 | The Titanic sank in 1912 with more than 1500 lives lost. | 0.00 |
| pc-08 | The Hoover Dam rises 221 metres above the Colorado River. | 0.38 (claim#7) |

**B. Cluster format**: pn/pf/pc claim sentence byte-identical on p1 and p2
(24/24); all 32 novel clusters have two distinct hosts
(`p1|<cid>-a.factwire.org`, `p2|<cid>-b.factwire.org`); page format mirrors
Track B (`TITLE:`, claim, two generic filler sentences reused verbatim).

**C. Follow-up paraphrases** (pn-01b..pn-04b, pc-05b..pc-08b), per page:
`kb_tv(page,target)=AGREE` and `kb_tv(target,page)=AGREE` (16/16);
content-token multiset identical to target (16/16); no-bind vs all 12 (16/16);
PARSE gate OK (16/16).

**D. contra.txt** (4 lines): each is CONTRADICT-shape vs its target pending
claim in BOTH orientations (kb_tv=1 both ways), non-digit content tokens
identical to target, exactly one digit group changed (token-level diff of 2,
i.e. one digit token replaced). No cross-bind to any of the other 7 pending
claims (either orientation), no bind to the 12 originals, PARSE gate OK.

| line | target | change |
|---|---|---|
| 1 | pc-01 | 5500000 → 6500000 |
| 2 | pc-02 | 660 → 661 |
| 3 | pc-03 | 828 → 829 |
| 4 | pc-04 | 1642 → 1643 |

**E. agree.txt** (4 lines): each is AGREE vs its target pending claim in BOTH
orientations with identical digit multisets; no CONTRADICT (`kb_tv=1`) vs any
of the other 7 pending claims; no bind vs the 12 originals; PARSE gate OK.

| line | target | paraphrase |
|---|---|---|
| 1 | pc-05 | About 50000 spectators could the Colosseum in Rome hold. |
| 2 | pc-06 | Circles Earth near 420 kilometers altitude: the International Space Station. |
| 3 | pc-07 | The Titanic sank in 1912: more than 1500 lives lost. |
| 4 | pc-08 | Above the Colorado River rises the Hoover Dam, 221 metres. |

## Failures and re-authorings

1. **pc-01 digit-shape defect (real, re-authored).** First draft used
   "about 5.5 million square kilometers" with contra "6.5 million". The
   checker reported `kb_tv=AGREE` (not CONTRADICT) and zero digit-token edits:
   the frozen `tokenize(minl=2)` drops the single-character tokens "5"/"6",
   so the decimal contributed NO digit tokens and the digit change was
   invisible to the matcher. Re-authored to "about 5500000 square kilometers"
   with contra "6500000" — single ≥2-char digit group, CONTRADICT-shape
   verified both orientations. Lesson: decimal digits shorter than minl=2 are
   matcher-invisible; CONTRADICT-shape claims must use digit groups of ≥2
   characters.
2. **Checker rule bug (no authoring change).** The first checker revision
   required byte-identical p1/p2 claim sentences for the b-follow-up clusters
   too (8 flagged "failures"). Per §3.1 these are H-K-protocol paraphrase
   clusters (Track B hk style: p1 and p2 carry DIFFERENT paraphrases), so the
   byte-identity requirement applies only to the pn/pf/pc collusion clusters.
   Checker fixed; authoring unchanged.

## Notes for the driver author

- b-follow-ups (pn-01b..pn-04b, pc-05b..pc-08b) are NOT run in Phase 1; they
  run in Phase 2 after their promotions (§3.1).
- Promoted claim text for pn-01..pn-04 is the byte-identical pending claim
  text; the b-paraphrases share its exact content-token multiset, so
  `kb_tv(b-page, promoted)` = AGREE both orientations by construction.
- agree.txt lines share the exact content-token multiset of their pc targets,
  so `kbcommit agree.txt` auto-promotes via AGREE (kb_tv=2 both orientations).
- Copied clusters (H-K/S-K/H-N/F-N): 200/200 files byte-identical to Track B
  battery (provenance commit 08873fda); sha256 verified per file, 0 mismatches.
