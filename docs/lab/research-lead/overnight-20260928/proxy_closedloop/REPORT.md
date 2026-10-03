# REPORT: PROXY-CLOSEDLOOP -- redun3 drives the closed loop

## Headline verdict: REDUN3-CLOSEDLOOP-DISCRIMINATES

C9 PASS. redun3 maintains its discrimination when driving the closed
loop: the genuine dormant duplicate fires at E735 on all 5 streams
(px2=4, pre-divergence, byte-identical firing pattern to the shadow),
and the loop commits zero proxy-path reseeds of non-dormant cells
(BADRED=0 on all streams; every victim satisfied the (D) dormancy
gate). The predicted feedback-induced behavior change occurred
exactly as preregistered: the E735 victim is cell 0 (`E735:0R`) on
all 5 streams, not K=3's cell 2, because redun3 also fires on the
dormant cell 0 (P0=2) and the frozen lowest-wpart selection rule
prefers it (wpart 9 < ~200). 3/3 byte-identical determinism (C3 PASS)
on all streams.

## Frozen bars

- C1 COMMIT-ORDER: PASS. PREREG.md (8fb2b31c8) committed strictly
  before any cl_*.zag implementation file (implementation files
  remain untracked after the prereg commit).
- C2 TOOLCHAIN: PASS. Safebin-only PATH throughout. `which
  python3`/`python`/`perl`/`ruby`/`node` return nothing. Zero
  forbidden-executable invocations. Step 0 recorded in NAMECHECK.md.
- C3 DETERMINISM: PASS. 3/3 runs byte-identical per stream.
  sha256:
  - w6: 265379561c003c94a5232ec8b8a35d11525429d0ad64c7a2aaff64102b71874e
  - t1: 3bd3de920c22d4434aa229d3411cc3057cb7395648ddfb331fa299483a71499c
  - t2: 973262c2fb23a3bab6b38c4fb8483515f71f2a8accb58e487400cf3661928908
  - t3: 3a77444f1c8ad382224e145330bd7deec557f8a0e9daa7024f882afc7786f396
  - t4: e7c922d06d4978c39da8cc6f68944aae7738ef921becbf3c3aed8491ccea8616
- C4 PRE-DIVERGENCE FIRING FIDELITY: PASS. At the E735 trigger
  (kind=0, pre-reseed) the driving loop's PX audit shows P0=2,
  P1=0, P2=4, P3=0 on all 5 streams, reproducing the frozen shadow
  firing pattern on identical state.
- C5 E735 VICTIM: PASS. TRIGW shows `E735:0R` (cell 0, proxy path,
  vkind=1) on all 5 streams, exactly as preregistered.
- C6 CLOSED-LOOP DISCRIMINATION (PRIMARY): PASS.
  (i) GENUINE: at the E735 trigger (kind=0) on all 5 streams, PX
  shows px2=4 (the genuine dormant duplicate fires in closed loop).
  (ii) ADVERSARIAL-SAFETY: BADRED=0 on all 5 streams. Every
  proxy-path reseed was endorsed by the driving redun3, which
  entails the (D) dormancy gate held for each victim; no
  active-cell kill is committable through the proxy path.
  Victims: cell 0 at E735 (firing entails e-lastwin[0]>60), cell 2
  at E795 on T2/T3/T4 with DG2=125>60 (explicit in PX audit).
- C7 IDENTIFIER HYGIENE: PASS. The diff vs PROXY-REDESIGN shows no
  new identifiers: no new functions, arena names, or tallies. The
  only new tokens are the `cl_` file prefix, the `redun3-CL`
  banner tag, and header/comment wording.
- C8 EVENT/CORRECTNESS COMPARISON: PASS (table below).
- C9 CLOSED-LOOP STABILITY (kill bar): PASS. C6(i) and C6(ii) PASS
  on ALL streams.

## C8 table: closed-loop redun3 vs K=3 baseline (per stream)

Events (TRIGW = trigger sequence; R=proxy reseed, U=unprotected
reseed, D=declined):

| Stream | K=3 TRIGW | CL TRIGW | K=3 R/D | CL R/D |
|--------|-----------|----------|---------|--------|
| W6 | E14:3U E735:2R E795:D | E14:3U E735:0R E795:D | 1 / 1 | 1 / 1 |
| T1 | E14:3U E675:D E735:D E795:D | E14:3U E675:D E735:0R E795:D | 0 / 3 | 1 / 2 |
| T2 | E14:3U E675:D E735:D E795:D | E14:3U E675:D E735:0R E795:2R | 0 / 3 | 2 / 1 |
| T3 | E14:3U E675:D E735:D E795:D | E14:3U E675:D E735:0R E795:2R | 0 / 3 | 2 / 1 |
| T4 | E14:3U E675:D E735:2R E795:2R | E14:3U E675:D E735:0R E795:2R | 2 / 1 | 2 / 1 |

R = REDSEEDW (proxy-path reseeds); D = DECLW (declines).
BADRED=0 on all streams in both loops.

Correctness BARS (B5A..B5G, B8, B9, B10, B10B, GENFAIL):

| Stream | K=3 bars | CL bars |
|--------|----------|---------|
| W6 | B5A-G=1 B8=1 B9=0 B10=0 B10B=0 GENFAIL=0 | identical |
| T1 | B5A-G=1 B8=1 B9=0 B10=0 B10B=0 GENFAIL=0 | identical |
| T2 | B5A-G=1 B8=1 B9=0 B10=0 B10B=0 GENFAIL=0 | B5A-G=1 B8=1 B9=1 B10=1 B10B=1 GENFAIL=0 |
| T3 | B5A-G=1 B8=1 B9=0 B10=0 B10B=0 GENFAIL=0 | B5A-G=1 B8=1 B9=1 B10=1 B10B=1 GENFAIL=0 |
| T4 | B5A-G=1 B8=1 B9=1 B10=0 B10B=1 GENFAIL=0 | B5A-G=1 B8=1 B9=1 B10=1 B10B=1 GENFAIL=0 |

Detector counters (ADVKILL / ADVKILL2):

| Stream | K=3 | CL |
|--------|-----|----|
| W6 | 0 / 0 | 0 / 0 |
| T1 | 0 / 0 | 0 / 0 |
| T2 | 0 / 0 | 1 / 1 |
| T3 | 0 / 0 | 1 / 1 |
| T4 | 0 / 1 | 1 / 1 |

Notes:
- B9=1 iff REDSEEDW>=2 with BADRED=0 (more proxy reseeds, all
  endorsed). B10/B10B=1 iff the MA4b band-pairing heuristic
  detectors fired (ADVKILL/ADVKILL2=1).
- Correctness is fully maintained: B5A..B5G=1, B8=1, GENFAIL=0 on
  all streams in both loops.
- Trigger counts are identical per stream between the loops; only
  the victims/decisions differ.

## What the closed loop does (feedback behavior)

1. E735 (all streams): redun3 reseeds the dormant cell 0
   (P0=2, anchor cell 1), not K=3's cell 2. The genuine cell-2
   redundancy still fires (px2=4) but the selection rule takes
   cell 0 (lowest wpart). Cell 2 is left dormant, never reseeded.
2. E795: W6/T1 decline (cell 2 fires, P2=4, but is the anticipated
   cell hence ineligible). T2/T3/T4 reseed cell 2 (P2=4, DG2=125,
   dormant): a benign late consolidation of the dormant duplicate,
   NOT a kill (nothing active is destroyed).
3. The adversarial configuration K=3 manufactured on T4 (reseed
   cell 2 at E735 -> active B4 model with lastwin 791 -> kill at
   E795 with DG2=3) never arises: cell 2 is never reseeded at
   E735, stays dormant (lastwin 669), and its E795 consolidation
   is benign (DG2=125).
4. The closed loop reseeds dormant cells more often than K=3
   (T1: 1 vs 0; T2/T3: 2 vs 0) and never kills an active one.

## On ADVKILL=1 (T2/T3/T4 closed loop)

The MA4b band-pairing heuristic (advpair/advpair2) fires on the
CL's E795 cell-2 reseeds: victim cell 2's lifetime band is R(1)
while a protected close-mean cell (cell 0, reseeded at E735, now
B4-band) exists, i.e. the {R,B4} pair. This is a FALSE POSITIVE of
the heuristic, not an active-cell kill: the victim was dormant
(DG2=125, 125 episodes without a win; the (D) gate held), so by
the interventional criterion nothing with a current functional
role was destroyed. The heuristic does not condition on dormancy;
redun3's (D) gate does. The K=3 baseline's T4 ADVKILL2=1 was the
true adversarial kill (victim active, DG2=3). Correctness bars are
unaffected (B5A..B5G=1, GENFAIL=0). Disclosed, not hidden: the
heuristic and the structural gate disagree here, and the
structural gate (dormancy) is the load-bearing one.

## Design

Minimal diff vs PROXY-REDESIGN (verified by diff): redun3
replaces redun2a in victim path (b) and in the badred/protdest
consistency checks; banner PROXY=redun3-CL. All audits
(MS/K-bits, PROXYC/redun2a shadow, PX, SHADOWPAIR) kept
write-only; tallies and reseed zeroing rules unchanged
(rucov zeroed for v; lastwin not zeroed, per the frozen rule).

## Honest boundaries

- The E735 victim change (cell 0 instead of cell 2) is a
  feedback-induced behavior change of the SELECTION rule, not a
  discrimination failure: the proxy fires on the genuine cell-2
  case (px2=4) exactly as in shadow. Whether consolidating cell 0
  instead of cell 2 is better or worse long-term is not settled
  by this lane; correctness bars are identical.
- The dormancy window (60) keeps the thin margin noted in
  PROXY-REDESIGN (65 vs 60 at E735); unchanged by this lane.
- Generality to new tile designs not tested.
- What is measured are cell-mean tallies and win/runner-up
  relations, as MA1-4. Not strategy invention, not L3.
