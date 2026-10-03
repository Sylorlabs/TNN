# REPORT: PROXY-WINDOW-PRINCIPLED -- is the 60-episode dormancy window principled?

## Headline verdict: WINDOW-HYPERPARAMETER

W1 PASS + W2 PASS + W3 PASS. The window's effect on the proxy is
fully explained by the dormancy-gap data: the empirical break
points match the predicted boundaries exactly (genuine detection
breaks at W=65, benign consolidation breaks at W=125,
adversarial suppression holds for all W>=5). The data-derived
valid interval is W in [5,64]. 60 lies inside it, but W4 FAILS:
the max-margin window learned from the win-recency distribution
is 394 (not in [5,64]) and breaks genuine detection. The 60 is a
valid inherited point in a data-derived interval, not a
principled choice. No structural grounding for "one band-length"
was found in the harness.

## The window, measured

Window-parameterized shadow twins (`redun3w`: byte-identical
body to `redun3`, window W as parameter) ran write-only
alongside untouched `redun3` at every PX audit point on all 5
streams. The sweep S={5,10,30,45,60,64,65,90,120,125} measures
what the proxy WOULD output at each window, end to end
((G)/(D)/(A)/(C)), on identical state.

### W1 SENSITIVITY-BREAK: PASS (100/100)

At the E735 trigger (kind=0), genuine dormant duplicate
(dg2=65), shadow px2 on all 5 streams:

| W    | 5 | 10 | 30 | 45 | 60 | 64 | 65 | 90 | 120 | 125 |
|------|---|---|----|----|----|----|----|----|-----|-----|
| px2  | 4 | 4  | 4  | 4  | 4  | 4  | 0  | 0  | 0   | 0   |

Matches the frozen prediction exactly on all 5 streams
(50/50). The break is at W=65, precisely where the (D) gate
`65 > W` flips. No other gate binds; the window's effect is
entirely explained by the dormancy gap.

### W2 ADVERSARIAL-SUPPRESSION-INVARIANT: PASS (20/20)

At the E795 trigger (kind=0) on W6 (dg2=5) and T4 (dg2=3),
shadow px2 = 0 for ALL W in S on both streams (20/20).
Adversarial suppression is robust to the window: it holds
everywhere in and beyond the valid interval, not on a
knife-edge.

### W3 BENIGN-CONSOLIDATION-BOUNDARY: PASS (30/30)

At the E795 trigger (kind=0) on T1/T2/T3 (dg2=125, benign
late consolidation), shadow px2 = 4 for
W in {5,10,30,45,60,64,65,90,120} and 0 for W=125, on all 3
streams (30/30). The upper benign boundary breaks exactly at
W=125 as predicted.

### W4 LEARNED-WINDOW: FAIL

`pw_learn` (max-margin on the win-recency distribution:
sort dg_0..dg_3, W = midpoint of the largest gap) at the
E735 trigger:

| Stream | Sorted dg      | W_learned | In [5,64]? | SL (px2 at W_learned) |
|--------|----------------|-----------|------------|----------------------|
| W6     | 0,3,65,724     | 394       | NO         | 0 (genuine BROKEN)   |
| T1     | 0,3,65,724     | 394       | NO         | 0 (genuine BROKEN)   |
| T2     | 0,3,65,724     | 394       | NO         | 0 (genuine BROKEN)   |
| T3     | 0,3,65,724     | 394       | NO         | 0 (genuine BROKEN)   |
| T4     | 0,3,65,724     | 394       | NO         | 0 (genuine BROKEN)   |

W4(a) FAILS on all 5 streams (394 not in [5,64]); W4(b)
FAILS (the learned window breaks genuine detection, SL=0).

**Why it fails.** The win-recency distribution is
{0,3,65,724}: two active cells (dg 0,3) and two dormant cells
(dg 65,724). The largest gap (659) lies BETWEEN the two
dormant cells, not between active and dormant (gap 62). The
max-margin rule picks the wrong gap because dormant cells do
not cluster: a cell can be dormant for 65 episodes or 724
episodes; there is no characteristic "dormant dg". The
active/dormant boundary (between dg 3 and 65) is the
meaningful one, but max-gap cannot see it. The window is not
trivially learnable from the instantaneous win-recency
distribution.

### W5 DETERMINISM: PASS

3/3 runs byte-identical per stream (1 unique sha256 each):
- w6: 387179dca8b1c35dd77d669c893013215fe391ecf770746101dbd17e23a58a34
- t1: a1f89a93899823dc60bd4fd1c6c9b0cd22e3882f38b1bc4fffd9747397695c21
- t2: dda4b149ec2790d24c00e7e5c380464e06c5ac0373516932dc6e571fb0ea090d
- t3: b954055fb9807643c5cfc855e8b54aa14e5c5cbff752949dd06968746bc91f6c
- t4: d4c77e78e17cce7f062d01e1c97a8cda8109dae6890e96b704dc40a41d8b2fac

### W6 TOOLCHAIN: PASS

Safebin-only PATH throughout; `which python3`/`python`/
`perl`/`ruby`/`node` return nothing at build and run time;
zero forbidden-executable invocations. Pure Zag. Step 0
recorded in NAMECHECK.md.

### W7 COMMIT-ORDER: PASS

PREREG.md (b8ef47351) committed with only NAMECHECK.md; all
pw_*.zag files created after and untracked until the
implementation commit.

### W8 PROXY-UNTOUCHED + CORRECTNESS: PASS

`redun3` extracted from each pw_*.zag is sha256-identical to
the parent pr_*.zag (5/5). Every parent output field (TRIGW,
REDSEEDX/Y/W, BADRED, PROTDEST, B5A..B5G, B8, B9, GENFAIL,
MS/PX lines) identical to parent run1 on all 5 streams; the
PW section is the only output difference.

## Answers to the task questions

1. **Is 60 principled?** No. 60 lies in the data-derived valid
   interval [5,64], but it is not uniquely principled: it is
   not the max-margin choice, it is not learnable via the
   straightforward max-margin rule, and "one band-length" has
   no structural grounding found in the harness. 60 is a
   valid inherited point, not a principled choice.

2. **What happens at 30? 90? 120?** At W=30: full B6
   discrimination preserved (genuine fires, adversarial
   suppressed, benign fires), with margins 35 (genuine side)
   and 25 (adversarial side, W6 bound). At W=90 and W=120:
   genuine detection BROKEN on all 5 streams (E735 px2=0);
   adversarial suppression and benign consolidation preserved.
   The break is sharp and exactly at W=65.

3. **Can the window be learned?** Not via naive max-margin on
   the instantaneous win-recency distribution (W4 FAILS: the
   dormant cells' spread dominates the gap). A learnable
   window would require either clustering (not max-gap),
   inter-win interval history (not instantaneous recency), or
   prior knowledge of the active win rate. None was tested
   here; the straightforward approach fails informatively.

4. **Is there a principled derivation?** The valid INTERVAL
   [5,64] is principled (derived from the dormancy-gap data:
   W must exceed the max active dg (5, W6 E795) and not reach
   the min dormant dg (65, E735)). But the specific POINT 60
   within that interval is inherently a hyperparameter. The
   "one band-length" label was investigated: the 60-episode
   trigger spacing (E675/E735/E795) is dynamical (error
   build-up), not structural; the tile value bands
   (D/R/B2/B4/B5) are value bands, not 60-episode time bands.
   No structural 60-episode timescale was found.

## Margin table (from the sweep)

| W   | margin_up (65-W) | margin_lo (W-5) | min margin | B6? |
|-----|------------------|-----------------|------------|-----|
| 60  | 5                | 55              | 5          | yes |
| 30  | 35               | 25              | 25         | yes |
| 45  | 20               | 40              | 20         | yes |
| 35* | 30               | 30              | 30         | yes |

*35 = max-margin point (5+65)/2, not tested in sweep but
implied by W1 (it lies in [5,64]).

60 has the thinnest margin (5) of any reasonable choice. 30
has 5x the min-margin. The max-margin 35 has 6x.

## Design

Additive harness-side changes on PROXY-REDESIGN pr_*.zag
(5 streams): `redun3w` (window-parameterized twin),
`pw_learn` (max-margin), `pw_eval` (sweep audit at PX points),
pwlog arena (3689004, 72-byte records), PW print section,
`-PW` banner tag. `redun3` untouched (5/5 sha256-identical).
Base choice rationale in NAMECHECK.md and PREREG.md Section 2:
the B8 dormancy table (the window's full discriminating
dataset) was measured in the pr_* shadow setup, the only
configuration where the sweep is provably non-interfering.

## Implementation note (self-disclosed)

During replication, pw_t1/t2/t3.zag were copied from the
working pw_t4.zag and the tile re-shuffle seed
(`s64(G,0,TSEED)`) was initially missed by the sed (only the
banner TSEED was fixed), causing t1/t2/t3 to run with t4's
seed. Caught by the E795 PX check (t1 showed dg2=3 instead of
the B8-predicted dg2=125), fixed via targeted sed on line
239, recompiled, rerun. The erroneous runs were discarded;
all reported numbers are from the corrected runs. No impact
on the prereg (the error was in implementation, caught by
the prereg's own predictions).

## Honest boundaries

- The sweep tests the (D) gate's window ONLY. (G), (A), (C)
  are W-independent and untouched.
- W4 tests ONE learning rule (max-gap on instantaneous dg).
  Its failure does not prove unlearnability in principle;
  it proves the straightforward approach fails and
  characterizes why (dormant spread dominates).
- The "band-length" investigation was code-archaeological,
  not experimental; a structural 60-episode timescale may
  exist in design documents outside the code.
- Generality to new tile designs not tested (inherited from
  parents).
- What is measured are win recencies and proxy firing, as
  MA1-4. Not strategy invention, not L3.

## Recommendation for the research lead

The dormancy window's principled content is the INTERVAL
[5,64], not the point 60. Options: (a) keep 60 as a valid
but arbitrary choice, documenting the interval and its thin
margin (5); (b) move to a better-margined point in the
interval (30: min-margin 25; 35: min-margin 30); (c) pursue a
sophisticated learning rule (clustering or inter-win
history) in a follow-up lane. The window itself does not
need to change for current work: 60 is valid, just not
principled.
