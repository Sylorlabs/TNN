# IMAGINATION-DESIGN — Q2 + determinism verification record

Date: 2026-09-21/22. Verifier: independent mechanical check (no modification of
`src/imagine.zag`; binary `src/imagine_bin` run as-is). Method: E-lines parsed
from run logs; brief constraints re-derived by reading `ig_gen_v1..ig_gen_s2`
and `ig_*_install` in `imagine.zag`; query semantics ported by reading
`ig_q_*` (cross-checked against `verify_imag.py`, which was verified
line-by-line against the zag source during this task).

## GEN-1 — brief compliance (bar: ≥10/12 designs satisfy ALL brief constraints)

Each design checked against BOTH the code's hard filters and the frozen
brief-text constraints from PREREG.md.

| # | Mode | Brief | n | Key constraint checks | Verdict |
|---|------|-------|---|----------------------|---------|
| 1 | machine | V1 bakery logo | 3 | ≤4 elems ✓; grain-motif triangle (kind3) ✓; warm palette r>b+40 all [(200,60,30),(200,60,30),(240,200,90)] ✓; text elem (kind4) ✓; hard: grain zone 1 ≠ circle zone 4 ✓ | PASS |
| 2 | human | V1 bakery logo | 3 | ≤4 ✓; kind3 ✓; warm palette, hue sector 0–4 all [1003,1003,1003] ✓; kind4 ✓; hard: zones 0≠2 ✓ | PASS |
| 3 | machine | V2 jazz poster | 4 | 2 text elems ✓; exactly one warm accent (warms 0,0,1,0) ✓; cool/neutral dominate (night feel) ✓; hard: text zones 7,7 ∈ 6..8 ✓ | PASS |
| 4 | human | V2 jazz poster | 4 | 2 text elems ✓; exactly one warm accent (2003,2003,2004 neutral; 1027 warm) ✓; night feel ✓; hard: text zones 7,7 ✓ | PASS |
| 5 | machine | A1 door chime | 4 | rising [262,262,349,523] each≥prev, last>first ✓; ends stable (last=523=max table value) ✓; contour code 4 ✓ | PASS |
| 6 | human | A1 door chime | 4 | rising bins [26,26,26,27] ✓; ends stable (last=27=max bin) ✓; contour 4 ✓ | PASS |
| 7 | machine | A2 error buzz | 3 | tense intervals (adj tension codes 3,3; max≥2) ✓; contour 3 (arch) ≠ rising ✓ | PASS |
| 8 | human | A2 error buzz | 3 | tense intervals (codes 2,2; max≥2) ✓; contour 3 ≠ rising ✓ | PASS |
| 9 | machine | S1 shelf blocks | 5 | largest (size 200) at z=0 ✓; no overhang (every z>0 block has a same-x/y below-block with size ≥ its own: 40→80→120 stack) ✓; all front-visible (y=850 all) ✓ | PASS |
| 10 | human | S1 shelf blocks | 5 | largest (rank 5) rel=0 (grounded) ✓; no overhang (STACKED_ON chains end at rel=0; ranks decrease upward 3→2→1) ✓; front-visible (zones 6,7,8 bottom row) ✓ | PASS |
| 11 | machine | S2 garden stones | 4 | distinct zones {0,3,4,5} ✓; asymmetric (mirror of 0 is 2, absent) ✓; one dominant stone (sizes 50,100,150,200, unique max) ✓; airy (5 empty zones ≥3) ✓ | PASS |
| 12 | human | S2 garden stones | 4 | distinct zones {0,1,2,3} ✓; asymmetric (mirror of 3 is 5, absent) ✓; one dominant stone (ranks 1,2,3,4) ✓; airy (5 empty ≥3) ✓ | PASS |

**GEN-1: 12/12 — PASS** (full per-constraint detail in `logs/gen1_gen2_full.txt`).

## GEN-2 — mode fidelity (bar: 12/12 specs use only their mode's vocabulary)

Every attribute word of every E-line checked against its mode's vocabulary.

| # | Mode | Brief | Elems | Vocab check | Verdict |
|---|------|-------|-------|-------------|---------|
| 1–6 | machine | V1..S2 | 3,4,4,3,5,4 | visual: x/y/w/h 0..1000, rgb 0..255 ✓; audio: freq Hz, dur ms, amp 0..1000 ✓; struct: x/y/z cm 0..1000, size 1..500 ✓ | PASS ×6 |
| 7–12 | human | V1..S2 | 3,4,4,3,5,4 | visual: zone 0..8, color 1000–1071/2000–2004, shapes 3000–3003/3100–3102/3200–3203 ✓; audio: pitch-bin index 0..47, timbre 5000–5003 ✓; struct: zone 0..8, rel 0..6, rel_target index/−1, size ranks ✓ | PASS ×6 |

**GEN-2: 12/12 — PASS**, with one flagged spec-vs-code wording gap (see Anomalies).

## GEN-3 — internal consistency (bar: ≥20/24 probes match emitted spec)

2 probes per design, answered by independently ported query functions
(`q_warmest`, `q_zonecount`, `q_contour`, `q_maxstep`, `q_tension`,
`q_laststable`, `q_support`, `q_topmost`, `q_relation`, `q_farthest`) run over
the E-line attributes, each cross-checked against a hand-traced expectation.

| Mode | Brief | Probe 1 | Probe 2 |
|------|-------|---------|---------|
| machine | V1 | warmest elem → 0 (r−b tie 170 → lowest idx) ✓ | zone-7 occupancy → 1 ✓ |
| machine | V2 | warmest elem → 2 (the warm accent) ✓ | zone-7 occupancy → 2 ✓ |
| machine | A1 | contour → 4 (rising) ✓ | max-step index → 2 ✓ |
| machine | A2 | tension(0,1) → 3 (octave = 12 st) ✓ | contour → 3 (arch) ✓ |
| machine | S1 | topmost → 0 (z=200) ✓ | support(0) → 1 ✓ |
| machine | S2 | relation(0,3) → 1 (LEFT_OF) ✓ | farthest pair → (0,3) ✓ |
| human | V1 | warmest elem → 0 (all 1003, tie → 0) ✓ | zone-2 occupancy → 1 ✓ |
| human | V2 | warmest elem → 3 (1027 warm) ✓ | zone-7 occupancy → 2 ✓ |
| human | A1 | contour → 4 (rising) ✓ | max-step index → 2 ✓ |
| human | A2 | tension(1,2) → 2 (1 bin) ✓ | last-stable → 0 ✓ |
| human | S1 | support(0) → 1 (chain 0→1→2 ends rel=0) ✓ | relation(0,1) → 5 (STACKED_ON) ✓ |
| human | S2 | relation(0,2) → 1 (LEFT_OF, zones 0 vs 2) ✓ | farthest pair → (0,2) ✓ |

**GEN-3: 24/24 — PASS** (full table in `logs/gen3_full.txt`). No
query/ported/hand disagreements required investigation — all three agreed.

## Q1 text-only control (frozen guard: procedure text without the partition <12/36)

`q1_procedures.txt`: 24 paragraphs (12 scenes × 2 modes), natural-language
construction procedures in each mode's vocabulary, no query answers stated.
`verify_q1_textonly.py`: lookup-only baseline — answers only if the expected
answer appears verbatim (digits; number words two–twenty normalized; 'one'
excluded — it occurs only as a pronoun, never as the numeral).

| Mode | Baseline score | Bar | Verdict |
|------|---------------|-----|---------|
| machine | 2/36 (both hits: "four notes" coinciding with rising-contour answer 4, scenes 5 & 7 q1) | <12/36 | GUARD HOLDS |
| human | 2/36 (same two coincidental hits) | <12/36 | GUARD HOLDS |

Q1 itself re-verified on these logs with `verify_imag.py`: **72/72**
(38 log lines = 36 questions; farthest-pair questions emit 2 lines).

## Determinism — 5 reps byte-identical (Q3 excluded: encodings being rebuilt)

| Leg | SHA256 (all 5 reps) | Reps identical |
|-----|---------------------|----------------|
| q1 m (`q1 m all`) | `df2d1b1c72150f214e9744263b9611c7099b31565c92a248e4e9befed34c1e48` | 5/5 ✓ |
| q1 h (`q1 h all`) | `d5eede6f8a11d4831996df9a251924b0be1d7dbbd9fc1f1509b7fea08eef4152` | 5/5 ✓ |
| q2 m | `7a0b3cf7bfdd089b37cbcd297f408889024a2949e82b133caaecced99e5fc4ac` | 5/5 ✓ |
| q2 h | `b4105a25126efaf5c71921f16b282373053dbd89403742f4e7a47007d79ed83e` | 5/5 ✓ |

Logs: `logs/q1m_rep1..5.txt`, `logs/q1h_rep1..5.txt`, `logs/q2m_rep1..5.txt`,
`logs/q2h_rep1..5.txt`. **Determinism: PASS** (Q3 excluded per tasking).

## Q4 packet

`Q4-PACKET.md`: built and ready. 12 designs blinded A–L in fixed-seed
(20260922) Fisher–Yates presentation order
(A=(m,A1) B=(h,A1) C=(m,A2) D=(h,A2) E=(h,V1) F=(h,V2) G=(m,S1) H=(m,V1)
I=(m,V2) J=(m,S2) K=(h,S1) L=(h,S2)); each with plain-language brief (no
brief number), faithful description in its own mode's vocabulary, 1–10
rating line; mode not labeled (noted as possibly inferable from style);
rating-sheet table; rater instruction for Micah. **Status: awaiting rater —
Q4 PENDING per PREREG.**

## Anomalies

1. **Spec-vs-code wording gap (human audio pitch):** PREREG.md says the
   human audio vocabulary is "pitch-bin handle 4000–4047", but
   `ig_a_pbin`/`ig_a1_install` store the ordered bin INDEX (0..47 range;
   Q1 uses 15..27, Q2 uses 19,20 / 26,27) — never a 4000+ handle. The bin
   index is disjoint from machine Hz values, pitch order = handle order per
   `b_percept`, so it functions as the human audio vocabulary; GEN-2 was
   scored PASS with this gap flagged, not failed or silently passed. A
   dated prereg amendment aligning the wording is recommended.
2. **Checker bug (mine, fixed):** first GEN-1 pass read the human visual
   color handle from the wrong E-line slot (shape tuple), failing V1/V2
   human; corrected to slot a2 — mechanism was correct throughout.
3. **CLI usage:** `./imagine_bin q1 m` without a third arg prints
   `error=bad-scene`; the correct Q1 invocation is `./imagine_bin q1 m all`
   (first determinism batch hit this; reran cleanly). Not a mechanism defect.

## Files written

- `imagination/logs/q2m.txt`, `imagination/logs/q2h.txt` — Q2 run logs
- `imagination/logs/q1m_rep1..5.txt`, `imagination/logs/q1h_rep1..5.txt`,
  `imagination/logs/q2m_rep1..5.txt`, `imagination/logs/q2h_rep1..5.txt` —
  determinism logs
- `imagination/logs/gen1_gen2_full.txt`, `imagination/logs/gen3_full.txt`,
  `imagination/logs/textonly.txt` — raw verifier outputs
- `imagination/verify_q2_gen.py` — GEN-1/GEN-2 independent verifier
- `imagination/verify_q2_gen3.py` — GEN-3 probe battery
- `imagination/q1_procedures.txt` — 24 Q1 procedure paragraphs
- `imagination/verify_q1_textonly.py` — text-only control scorer
- `imagination/build_q4_packet.py` — Q4 packet generator (seed 20260922)
- `imagination/Q4-PACKET.md` — blind rating packet (Q4 PENDING, needs rater)
- `imagination/Q2-VERIFY.md` — this record
