# PREREG: PROXY-WINDOW-PRINCIPLED -- is the 60-episode dormancy window principled?

## 1. Question

PROXY-HEURISTIC-GATE closed as HEURISTIC-GATE-ALIGNED with the
caveat: "The 60-episode window itself remains unprincipled
(inherited, not tested)." PROXY-REDESIGN noted the thin margin
(65 vs 60 on the T1-T4 genuine case) and that "the absolute
threshold is not principled beyond 'one band-length'."

This lane tests whether the 60-episode dormancy window in
redun3's (D) gate (`e - lastwin[i] > 60`) can be principled:

- (a) SENSITIVITY: What happens at W=30? 90? 120? Where exactly
  does the proxy's discrimination break?
- (b) LEARNABILITY: Can the window be derived from win-history
  data (max-margin on the win-recency distribution) instead of
  inherited?
- (c) DERIVATION: Is there a principled derivation of 60, or is
  it inherently a hyperparameter (a valid point in a
  data-derived interval, but not uniquely principled)?

## 2. Base

`pr_w6.zag`, `pr_t1.zag`, `pr_t2.zag`, `pr_t3.zag`, `pr_t4.zag`
from PROXY-REDESIGN, copied to `pw_w6.zag`, `pw_t1.zag`,
`pw_t2.zag`, `pw_t3.zag`, `pw_t4.zag`. Rationale (see
NAMECHECK.md): the window's discrimination is fully specified by
the B8 dormancy table, measured in the 5-stream K=3-driven shadow
setup; the shadow setup is the only configuration where a window
sweep is provably non-interfering (K=3 drives; redun3 and all
shadows write-only; loop trajectory invariant to W). redun3 is
byte-identical (frozen) across PROXY-REDESIGN, PROXY-CLOSEDLOOP,
and PROXY-HEURISTIC-GATE. This lane continues the
HEURISTIC-GATE-ALIGNED investigation (tests its caveat) and does
NOT redesign the proxy.

Constraint: `redun3` is NOT modified (per task). Window
sensitivity is measured via write-only shadow twins.

## 3. Frozen implementation plan

Additive harness-side changes only:

1. `fn redun3w(G:[]u8,cb:i32,i:i32,e:i32,W:i32)i32`:
   byte-identical body to `redun3`, except the (D) gate reads
   `if(e-lw<=W){ return 0; }` with W as a parameter. All of
   (G), (A), (C) unchanged.

2. `fn pw_learn(G:[]u8,cb:i32,e:i32)i32` (harness-side,
   write-only): max-margin window from the win-recency
   distribution at the audit episode e:
   - Read lw_i = get32(G, 3688972+i*4), dg_i = e - lw_i, i=0..3.
   - Sort dg ascending (4-element bubble sort on locals).
   - Find the largest gap between consecutive sorted values;
     ties -> first (lowest) gap. (lo, hi) = gap endpoints.
   - Return (lo+hi)/2 (integer division). Degenerate case
     (all equal): return dg_0.

3. `fn pw_eval(G:[]u8,cb:i32,e1:i32,kind:i32,e:i32,idx:i32)void`:
   called at every PX audit point (same call sites as px_eval,
   immediately after). Records into pwlog (see 4):
   - ep=e1, kind=kind.
   - Sorted dg_0..dg_3 at e (16 bytes, auditable input to
     pw_learn).
   - W_learned = pw_learn(G,cb,e).
   - Shadow px2 = redun3w(G,cb,2,e,W) for each W in the frozen
     sweep set S = {5,10,30,45,60,64,65,90,120,125} (10 i32s).
   - Shadow px2 at W=W_learned (1 i32).
   Write-only; no feedback into cell state or loop decisions.

4. Arena: `pwn` at 3689000 (4 bytes, record count);
   `pwlog[32]` at 3689004. Record = 72 bytes: ep(+0),
   kind(+4), W_learned(+8), dg_sorted[4] (+12..+24),
   sweep px2[10] (+28..+64), px2_at_learned (+68).
   32*72 = 2304 bytes; 3689004+2304 = 3691180 < 4194304 (G
   size). Documented in the arena comment block.

5. Print: after the PX section, print `PW n=` and one `PW`
   line per record: `PW E<ep> T<kind> WL=<w_learned>
   DG=<d0>,<d1>,<d2>,<d3> S5=<..> S10=<..> S30=<..> S45=<..>
   S60=<..> S64=<..> S65=<..> S90=<..> S120=<..> S125=<..>
   SL=<px2 at learned>`.

6. Banner: append `-PW` tag.

No other logic touched. `redun3`, reseeds, tallies, triggers,
and all existing audits unchanged.

## 4. Frozen predictions (from PROXY-REDESIGN B8 dormancy gaps)

dg2 = e - lastwin[2]:

| Stream | E735 dg2 | E795 dg2 |
|--------|----------|----------|
| W6     | 65       | 5        |
| T1     | 65       | 125      |
| T2     | 65       | 125      |
| T3     | 65       | 125      |
| T4     | 65       | 3        |

(D) gate: dormant iff dg > W. (G)(A)(C) are W-independent; the
parent B8/B6 establishes their state at W=60, hence for all W.

- E735 (all 5 streams): G/A/C hold (parent px2=4 at W=60);
  fires iff 65 > W.
  => W in {5,10,30,45,60,64}: px2=4;
     W in {65,90,120,125}: px2=0.
- E795 W6 (dg2=5): (D) suppresses for all W>=5 (5<=W).
  => all 10 W: px2=0.
- E795 T4 (dg2=3): (D) suppresses for all W>=5 (3<=W).
  => all 10 W: px2=0.
- E795 T1/T2/T3 (dg2=125): G/A/C hold (parent px2=4 at W=60);
  fires iff 125 > W.
  => W in {5,10,30,45,60,64,65,90,120}: px2=4; W=125: px2=0.

Predicted empirically valid interval: W in [5,64] (integer).
W=60 is inside with upper margin 5; W=30 with margins 35/25;
max-margin point is (5+65)/2 = 35 with margins 30/30.

No prediction is made for W_learned (that is the learnability
test); the bar requires only that it land in [5,64] and
preserve B6.

## 5. Frozen kill bars

- W1 SENSITIVITY-BREAK (PRIMARY, discriminating): At the E735
  trigger (kind=0) on all 5 streams, shadow px2 matches the
  Section 4 prediction for every W in S: {5,10,30,45,60,64}
  -> 4; {65,90,120,125} -> 0. PASS iff 5 streams x 10 W =
  100/100 match. FAILS if the empirical break is not exactly
  at W=65 (e.g. another gate binds, or the dg analysis is
  wrong).

- W2 ADVERSARIAL-SUPPRESSION-INVARIANT: At the E795 trigger
  (kind=0) on W6 and T4, shadow px2 = 0 for ALL W in S.
  PASS iff 2 x 10 = 20/20 match. (Guards that the sweep does
  not disturb adversarial suppression.)

- W3 BENIGN-CONSOLIDATION-BOUNDARY: At the E795 trigger
  (kind=0) on T1, T2, T3: shadow px2 = 4 for
  W in {5,10,30,45,60,64,65,90,120}, and px2 = 0 for W=125.
  PASS iff 3 x 10 = 30/30 match.

- W4 LEARNED-WINDOW (discriminating): (a) W_learned from
  pw_learn at the E735 trigger (kind=0) satisfies
  5 <= W_learned <= 64 on all 5 streams. (b) The shadow proxy
  at W=W_learned reproduces B6 on all streams: E735 px2=4
  (all 5), E795 px2=0 (W6,T4), E795 px2=4 (T1,T2,T3)
  (read from the SL field). PASS iff (a) and (b) hold on all
  5 streams. FAILS if the win-recency distribution is not
  usefully bimodal or the learned window does not preserve
  discrimination. (Tests learnability, not a predicted value.)

- W5 DETERMINISM: 3/3 runs byte-identical per stream (1 unique
  sha256 per stream).

- W6 TOOLCHAIN: Safebin-only PATH; `which python3`/`python`/
  `perl`/`ruby`/`node` return nothing at build and run time;
  zero forbidden-executable invocations. Pure Zag.

- W7 COMMIT-ORDER: This PREREG.md (+NAMECHECK.md) committed
  strictly before any pw_*.zag implementation file exists
  (implementation files untracked until the implementation
  commit).

- W8 PROXY-UNTOUCHED + CORRECTNESS: `redun3` extracted from
  each pw_*.zag is sha256-identical to the parent pr_*.zag
  (5/5). Every parent output field (TRIGW, REDSEEDX/Y/W,
  BADRED, PROTDEST, B5A..B5G, B8, B9, GENFAIL, MS/PX lines)
  identical to parent run1 on all 5 streams; the PW section
  is the only output difference.

## 6. Frozen verdict mapping

- WINDOW-PRINCIPLED: W1-W8 PASS, and W_learned is either ~60
  or has an independent principled derivation (e.g. a
  structural "band-length" grounding found in the harness).
- WINDOW-VALID-BUT-UNPRINCIPLED: W1-W3 PASS (60 lies in the
  data-derived valid interval [5,64]) but W4 yields a learned
  window != 60 with strictly better margins, and no
  structural grounding for "one band-length" is found: 60 is
  a valid inherited point, not a principled choice.
- WINDOW-HYPERPARAMETER: W1-W3 PASS but W4 FAILS (window not
  learnable from win history): the window is inherently a
  hyperparameter; report the valid interval [5,64] as the
  principled content.
- WINDOW-BROKEN: W1 FAILS: the window's effect is not
  explained by the dormancy-gap data; halt and investigate
  (do not reinterpret the bars).

Margins to report: for each candidate W (60, 30, learned),
margin_up = 65 - W (genuine side), margin_lo = W - 5
(adversarial side, W6 bound).

## 7. Artifacts planned

- `pw_w6.zag`, `pw_t1.zag`, `pw_t2.zag`, `pw_t3.zag`,
  `pw_t4.zag` (+ compiled `pw_*_bin`, 3/3 run outputs
  `*_run{1,2,3}.txt`).
- `REPORT.md` with the W1-W8 verdicts, the empirical valid
  interval, W_learned per stream, margin table, and the
  principled/unprincipled verdict.
