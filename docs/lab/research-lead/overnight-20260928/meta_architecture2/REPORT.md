# REPORT: MA2 -- Dormant-cell protection for the multi-cell architecture

## Frozen verdict: DORMANT-CELL PROTECTION DEMONSTRATED

Per the frozen verdict mapping, B5a (primary, kill bar) PASSED (R_X = 7,
within 1..99) and B8 (co-primary, kill bar) PASSED (PROTDEST = 0: no
reseed in any condition destroyed a protected cell), with B1, B2, B3,
B5e, B5f, B6, B7 all PASS and B5b (replication guard) PASS. The
preregistered headline verdict is therefore DORMANT-CELL PROTECTION
DEMONSTRATED: the victim veto plus the decline rule kept every
demonstrated-useful cell alive across three shifts while legitimate
reallocation still fired on schedule. Nothing was weakened or
reinterpreted; no amendment was needed.

## What was built (pure Zag, safebin-only)

- `ma2.zag`: MA1's architecture plus the frozen protection mechanism.
  Each cell adds (wpart, wpsm): winner-episodes and summed winner
  error, from revealed values only. Protected iff wpart >= 5 and
  wpsm/wpart <= 10 (PACT=5, PERR=10). Victim = highest score (ties:
  highest index) among non-active, non-winner, unprotected cells. If
  no unprotected candidate exists, the reseed is declined (logged,
  consec reset). Selection, EMA scoring, absorption, and the
  consec>=3 trigger are unchanged from MA1.
- Four conditions in one frozen binary. X/Y/Z replicate MA1 exactly
  (seeds 20261020..23). W is new: D(12) + R(660) + B2(60) + R3(60) =
  852 episodes, R3 reusing the Block-R tile (the 80 block returns),
  SEED_W = 20261024. X and W share block values over episodes 0..731.
- Commit order honored: prereg (1aebf8f, PREREG.md + NAMECHECK.md
  Step 0 only) strictly before any implementation file. This commit
  adds implementation + runs + report.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/
  ruby/node all unresolvable; zero forbidden invocations. One znc
  analyzer warning (A0101 on `etc_ep`, the known false-positive class
  from MA1; max index is fbase+e*1200+1199, in bounds).
- Determinism: 3/3 runs byte-identical, sha256
  `dfdd1e47a8fa7e5e9a1ec7211d0feb2910a90985ac4bef85cfcff80be4e54ea7`.

## Results (frozen binary output, 3/3 identical)

```
RX=7 RY=2 RZ=624 RXF=3 RXB2=4 RWB2=4 RW=8 COSTXY=1022 COSTXZ=-3936
B5A=1 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 B5G=1 B8=1
DISTINCTD=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
TRIGX n=2 E14:3U F=1 E675:1U F=13
TRIGY n=0
TRIGW n=3 E14:3U F=1 E675:1U F=13 E735:D F=15
DECLX n=0 DECLY n=0 DECLW n=1
PROTDEST=0
SNAPXD S0=180 N0=9 C0=10 WP0=9 WQ0=48 S1=40 N1=1 C1=15 WP1=1 WQ1=10
       S2=54 N2=1 C2=22 WP2=1 WQ2=4 S3=47 N3=1 C3=19 WP3=1 WQ3=3
SNAPXR S0=180 N0=9 C0=59 WP0=9 WQ0=48 S1=40 N1=1 C1=39 WP1=1 WQ1=10
       S2=17157 N2=223 C2=3 WP2=223 WQ2=284 S3=35780 N3=439 C3=1 WP3=438 WQ3=660
SNAPXB S0=1056 N0=50 C0=1 WP0=50 WQ0=125 S1=342 N1=20 C1=1 WP1=19 WQ1=14
       S2=17157 N2=223 C2=55 WP2=223 WQ2=284 S3=35780 N3=439 C3=60 WP3=438 WQ3=660
SNAPWR3 S0=1056 N0=50 C0=58 WP0=50 WQ0=125 S1=342 N1=20 C1=62 WP1=19 WQ1=14
       S2=20236 N2=263 C2=3 WP2=263 WQ2=323 S3=42301 N3=519 C3=1 WP3=518 WQ3=779
```

(U = victim unprotected, P = victim protected, D = declined,
F = protection bitmask at the trigger.)

Bar scorecard:
- B1 COMMIT-ORDER: PASS (prereg 1aebf8f strictly predates
  implementation).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded, zero incidents).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (Block-D values distinct; all same-episode
  cross-condition flip vectors differ, including W vs X/Y/Z;
  per-block ones-fractions inside the MA1 v1.1 bands, W's R3 block
  in [50400, 64800]).
- B5a RECOVERY (PRIMARY): PASS (1 <= 7 <= 99).
- B5b BASELINE-REPLICATION: PASS (RZ=624 >= 500; C435 replicated).
- B5c COST: PASS (1022 < 4690).
- B5d SHIFT-BACK: PASS (1 <= 4 <= 30).
- B5e APPARATUS: PASS (max etc <= 1200, genfail 0).
- B5f STREAM-VALIDITY: PASS (PARID=1 incl. W over 0..731, XDISJ=1).
- B5g MANIPULATION: PASS (in-binary white-box: cell 0 of X and of W
  both end Block D at (sum=180, n=9)).
- B6 NO-RESEARCHER-RULE: PASS (learner fns use only revealed values
  and tallies derived from them; the episode-index-conditioned hooks
  are write-only snapshots with no feedback into cell state; the
  trigger/victim/decline logic reads only scores, errors, wpart,
  wpsm).
- B7 OPAQUE-IDS: PASS (labels E0001..; case-insensitive grep for the
  frozen 29-word list in ma2.zag returns empty; two substring hits
  found and reworded before compilation).
- B8 PROTECTION (CO-PRIMARY): PASS (PROTDEST = 0).

## Reading of the result

Three triggers, three correct victim decisions, one correct decline.

T1 (X/W E14, mask F=1: only cell 0 protected): the victim is cell 3,
the unprotected atypical spare, exactly as preregistered. The
distractor cell (WP=9, mean win-error 48/9 = 5.33 <= 10) survives its
first trigger untouched, where MA1's naive rule destroyed it.
Recovery is unchanged: R_X = 7, and X's entire Block-R output is
byte-identical to MA1's (COSTXY=1022, RXF=3), confirming the
protection veto alters nothing when the spare inventory suffices.

T2 (X/W E675, mask F=13: cells 0, 2, 3 protected): the victim is
cell 1, the last unprotected atypical spare, as preregistered. Both
80-cells survive. The dormant distractor cell then does something
MA1's architecture could never show: it WINS Block-B2 episodes as
the best explainer (N0: 9 -> 50, WP0: 9 -> 50), re-earning mass while
never being the active cell. Dormant knowledge is reused, not just
hoarded. R_XB2 = R_WB2 = 4.

T3 (W E735, mask F=15: all four cells protected): the preregistered
case A occurred. Cell 2 earned protection during Block R (WP2=223,
mean win-error 1.27), so every candidate was a demonstrated block
model and the reseed was DECLINED (DECLW=1, zero destruction) rather
than killing a useful cell to make room. Score selection moved the
active cell to the dormant 80-cell (cell 2, mean 76) at R3k=4, and W
was within-1 of 80 by R3k=8 (RW=8) with no reseed at all. The final
snapshot shows four cells holding block mass (two ~= 20, two ~= 80),
all protected, none ever reseeded while protected.

The key question is answered: the victim veto steered both
reseeds onto unprotected spares (reallocation never blocked when a
useless cell existed), and the decline rule absorbed the one trigger
where no useless cell existed (knowledge never destroyed when every
cell was useful). Y had no triggers and Z is unchanged, both
byte-identical to MA1.

## Honest boundaries

- What is learned are cell means, same level as MA1 (L1/L2-ish).
  Not strategy invention, not L3. PACT=5/PERR=10 are
  researcher-supplied; protection status, victim choice, and decline
  are learner-driven from revealed values.
- The decline path's case B (cell 2 below the bar, reseeded at T3)
  did not occur; only case A was exercised. Both were
  preregistered as bar-satisfying.
- K=4 covers at most 4 demonstrated block models. A fifth distinct
  block with all cells protected would be declined indefinitely;
  the decline does not distinguish redundant from unique knowledge
  (at T3, cells 2 and 3 both held 80-mass). Redundancy-aware victim
  choice is future work, not claimed here.
- The decline relies on score selection to switch the active cell
  within a few episodes of a declined trigger (observed: 1 episode).
- Prereg estimate vs observed: the distractor cell's mean win-error
  at T1 was 5.33 (prereg said ~= 2); the protection inequality
  (<= 10) holds with margin, and the bar is unaffected.
- One W scenario, one frozen seed quintuple; MA1's four seeds were
  reused for direct comparability (frozen before MA1's outcomes).

## Artifacts in this commit

- `ma2.zag`: frozen implementation (B6/B7 audited).
- `ma2_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `dfdd1e47a8fa7e5e9a1ec7211d0feb2910a90985ac4bef85cfcff80be4e54ea7`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
