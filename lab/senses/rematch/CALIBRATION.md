# CALIBRATION.md — senses rematch: threshold grids, recorded BEFORE fitting

Date: 2026-09-21. Status: pre-fit calibration record. No training data
was touched in producing this file; all values below come from the
source code and the frozen prereg amendment
(`~/workspace/senses-rematch/PREREG_AMENDMENT.md`).

Every grid parameter was enumerated against the approach sources:
`a_raw/sense.zag` (approach A) and `b_percept/percept.zag` +
`b_percept/transducer.zag` + `b_percept/sense.zag` (approach B, original
uninstrumented sources — the instrumented copies in
`~/workspace/senses-rematch/b_inst/` change no decision code; see the
validation gate log).

Fitting objective (per amendment): training accuracy on the TRAIN set,
per (approach, task, budget). Tie-break (deterministic): grid point
closest to the round-1 hand-tuned value (absolute difference;
multi-param: lexicographic on per-param distance in sweep order);
residual tie → smallest grid index. Confidence rules are NOT fitted.

"Hand-tuned value" = the value/behavior in the round-1 binaries.

## A — verified against `a_raw/sense.zag`

| Task | Score (from `debug_vec`) | Fitted rule | Hand value (source line) | Grid |
|---|---|---|---|---|
| colordisc | `dist` (RGB units, isqrt of channel-mean diffs) | SAME iff dist ≤ t | 40 (`if(dist > 40) { ji = 1; }`) | {10,20,30,**40**,50,60,80,100} |
| colorconst | `dist` (per-mille von Kries distance) | SAME_SURFACE iff dist ≤ t | 150 (`if(dist > 150) { ji = 1; }`) | {50,75,100,125,**150**,175,200,250,300} |
| shapetrans | — | NOT FITTED | nearest-prototype on ratio (1000/637/414); lum mask 382 fixed | — (documented, not fitted) |
| pitchdisc | `dppm` = |fbm−fam|·10⁶/max(fam,1); `fam`,`fbm` from `debug_vec` | SAME iff d < t; else HIGHER iff fbm > fam else LOWER | 20000 (`if(d >= 20000 ...)`) | {5000,10000,15000,**20000**,30000,50000} |
| timbredisc | `r` = 1000·ΣhE_h/ΣE_h (per-mille centroid) | PURE iff r < b1; DARK iff r < b2; RICH iff r < b3; else BRIGHT | b1=1075, b2=1400, b3=3000 (`if(r >= 1075 && r < 1400) { ji = 1; }`, `if(r >= 1400 && r < 3000) { ji = 2; }`, `if(r >= 3000) { ji = 3; }`) | b1 ∈ {1020,1040,1060,**1075**,1100,1130}; b2 ∈ {1300,1350,**1400**,1450,1500}; b3 ∈ {2600,2800,**3000**,3200,3400} |
| motiondir | `mag` = isqrt(dx²+dy²) (px); `dx`,`dy` from `debug_vec` | STILL iff mag < t; else A's octant rule on (dx,dy): ax≥2·ay → E/W by sign(dx); ay≥2·ax → S/N by sign(dy) (y down); else diagonal quadrant | 3 (`if(mag2 >= 9)` → direction iff mag ≥ 3) | {1,2,**3**,4,5} |

A pitch sweep detail: the fitted rule uses the SAME dppm score; the
direction (HIGHER/LOWER) comes from the sign of (fbm − fam) in
`debug_vec`, not from the threshold. A motiondir direction uses the
identical octant code as the binary; only the STILL gate is fitted.

A timbredisc grid note: b1 < b2 < b3 holds for every grid point
(b1 ≤ 1130 < b2 ≥ 1300 < b3 ≥ 2600), so the 4-way partition is always
well-formed.

A timbredisc sweep order: b1, then b2, then b3 (listed order), single
coordinate sweep, no iteration, starting from hand (1075, 1400, 3000).

## B — verified against `b_percept/percept.zag` + `transducer.zag`

| Task | Score source | Fitted rule | Hand value (source) | Grid |
|---|---|---|---|---|
| colordisc | k = `pc_color_dist(p1,p2)` from emitted `percept`,`percept2` handles, tables reimplemented in Python | SAME iff k ≤ t | 1 (`pc_color_same`: `pc_color_dist(a,b) <= 1`) | {0,**1**,2,3,4} |
| colorconst | same as colordisc | SAME_SURFACE iff k ≤ t | 1 (same) | {0,**1**,2,3,4} |
| pitchdisc | k = \|bin1 − bin2\| = \|p1 − p2\| from `percept`,`percept2` (handle = 4000+bin) | SAME iff k ≤ t; else HIGHER iff p2 > p1 else LOWER | 0 (`pc_pitch_cmp(p1,p2) == 0` → SAME; sign gives HIGHER/LOWER) | {**0**,1,2,3} |
| shapetrans | 3-tuple (`percept`=corners, `shape_curv`, `shape_sym`); matches vs the 3 fixed prototypes | crew-defined vote family (see below) | current binary (`pc_shape_decide`: argmax, ties → earliest of CIRCLE,TRIANGLE,SQUARE) | min axis-matches ∈ {2,3} × 6 priority orders |
| timbredisc | instrumented `(crest, bright, form)` per-mille features from the transducer | RICH iff crest ≤ t_c; elif BRIGHT iff bright ≥ t_b; elif DARK iff form ≥ t_f; else PURE | t_c=1150, t_b=60, t_f=1780 (`if (crest <= 1150)`, `if (bright >= 60)`, `if (ff >= 1780)`) | t_c ∈ {1000,1075,**1150**,1225,1300}; t_b ∈ {40,50,**60**,70,80}; t_f ∈ {1600,1700,**1780**,1860,1950} |
| motiondir | instrumented `(mcount, dx, dy)` from the transducer | STILL iff mcount < t; else the binary's direction handle (6000..6008 → vocab name) | see CORRECTION (1) | {100,150,**200**,250,300} |

B timbredisc sweep order: crest, then bright, then form (listed
order), single coordinate sweep, no iteration, starting from hand
(1150, 60, 1780). Decision order (crest → brightness → form) is FIXED,
per the amendment; only the three thresholds move.

B shapetrans vote family (crew definition, per the amendment's "crew
defines the exact set from `pc_shape_decide`"):
- Let (m_C, m_T, m_S) = tuple-axis matches (0..3) for CIRCLE, TRIANGLE,
  SQUARE from the emitted 3-tuple.
- Qualifiers = classes with m_i ≥ min_matches.
- If qualifiers non-empty: winner = highest m_i among qualifiers;
  ties broken by the priority order.
- If qualifiers empty: winner = the priority order's FIRST class.
- Priority orders: the 6 permutations of (CIRCLE, TRIANGLE, SQUARE),
  coded CIRCLE=0, TRIANGLE=1, SQUARE=2. Grid index 0 = (0,1,2) = the
  hand order (reproduces `pc_shape_decide` tie behavior); indices 1..5
  = (0,2,1), (1,0,2), (1,2,0), (2,0,1), (2,1,0) (lexicographic).
- Sweep: coordinate 1 = min_matches ∈ {2,3} first, with order fixed at
  index 0; coordinate 2 = priority order, with min_matches fixed at the
  sweep-1 winner. Single pass, no iteration.
- Tie-break anchors (hand-tuned): min_matches anchor = 0 (the current
  binary gates on nothing); order anchor = index 0. Per-param
  distances: |m − 0| for coordinate 1; 0 for index 0, 1 for any other
  order for coordinate 2. Residual tie → smallest grid index.

## CORRECTIONS recorded (deviations from the amendment's assumptions)

1. **B motiondir hand-tuned threshold (200) is NOT implemented in the
   binary.** PERCEPT_DESIGN.md design bet 5 says "Motion STILL
   threshold (200 changed pixels/frame)", but `td_motion` implements
   no 200 threshold: STILL is emitted when no per-frame centroid pair
   with ≥8 changed pixels exists (`fa < 0 || fb <= fa`) OR when the
   centroid displacement is below w/16 (`dist < thresh`). The fitting
   family is exactly as the amendment specifies — "still iff
   mcount < t, t ∈ {100,150,(200),250,300}" on the instrumented
   changed-pixel total — and the tie-break anchor is the
   amendment-specified 200. The current binary's actual still
   behavior is the centroid rule, not "mcount < 200"; the two can
   differ, and the fit is allowed to move the gate wherever training
   accuracy is maximal.

2. **B shapetrans parameterization is the crew's** (above). The
   amendment fixed only "min axis-matches ∈ {2,3} × tie-break priority
   orders" and left the exact family to the crew. The family above is
   fully specified, deterministic, and always yields a judgment in the
   fixed 3-class vocab.

3. **B pitchdisc direction at fitted k:** the binary's judgment is
   HIGHER iff `pc_pitch_cmp(p1,p2) < 0` (p2 higher bin), LOWER iff
   `> 0`. The fitted rule keeps this sign convention for all k.

No other corrections. All other grid hand values match the sources
byte-for-byte as cited above. Nothing in this file was derived from
any training fixture.
