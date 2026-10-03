# REPORT: MA3 -- Redundancy-aware victim choice

## Frozen verdict: REDUNDANCY-AWARE VICTIM CHOICE DEMONSTRATED

Per the frozen verdict mapping, B5a (primary, kill bar) PASSED
(R_X = 7, within 1..99) and B9 (co-primary, kill bar) PASSED
(REDSEEDW = 2 and BADRED = 0: the redundancy path fired exactly on
the two designed triggers and every redundancy-path victim
satisfied the redundancy predicate in-binary), with B1, B2, B3,
B5e, B5f, B6, B7, B8 all PASS and B5b (replication guard) PASS.
The preregistered headline verdict is therefore REDUNDANCY-AWARE
VICTIM CHOICE DEMONSTRATED: when the 5-block W5 stream forced the
K=4 limit, the architecture reseeded a redundant duplicate twice
and never destroyed unique demonstrated knowledge. Nothing was
weakened or reinterpreted; no amendment was needed.

## What was built (pure Zag, safebin-only)

- `ma3.zag`: MA2's architecture plus the frozen redundancy
  sub-rule. New `redun()` predicate: cell i is redundant iff it is
  protected and some other protected cell j has |mean_i - mean_j|
  <= RDDM (RDDM=10), from revealed values only; the anchor must be
  protected (a fresh cell's mean is one revealed value, not shown
  success). Victim rule: (a) unprotected candidate exists ->
  highest score, ties highest index (MA2's rule, unchanged);
  (b) else a redundant candidate exists -> lowest wpart, ties
  highest score, ties highest index (keep the stronger
  demonstration, reseed the weaker duplicate); (c) else decline
  (MA2's rule, unchanged). Selection, EMA scoring, absorption,
  consec>=3 trigger, and the protection predicate are unchanged.
- Trigger log encoding: U = unprotected path, R = redundancy path,
  D = declined, X = tripwire (protected-unique victim, never
  observed). New tallies: REDSEEDW (redundancy reseeds),
  BADRED (in-binary tripwire: redundancy victim failing the
  predicate), PROTDEST now counts only protected-UNIQUE victims.
- X/Y/Z replicate MA2 exactly (same seeds/blocks); W5 is new:
  D(12) + R(660, {76..84}) + B2(60, {16..24}) + B4(60, NEW
  {46..54}) + B5(60, NEW {91..99}) = 852 episodes, five distinct
  blocks, SEED_W5=20261025. W5's D/R/B2 tiles are drawn from the
  SEED_B stream in MA2's exact order, so values over 0..731 match
  MA2's W and X.
- Commit order honored: prereg (7be552ca4, PREREG.md + NAMECHECK.md
  Step 0 only) strictly predates all implementation files. This
  commit adds implementation + runs + report.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/
  ruby/node all unresolvable; zero forbidden invocations. One znc
  analyzer warning (A0101 on `etc_ep`, the known false-positive
  class from MA1/MA2; max index is fbase+e*1200+1199, in bounds).
- Determinism: 3/3 runs byte-identical, sha256
  `5217cb95af51b7c656df1581e8720109fc811717c5297cc58005515e90d4dec8`.

## Results (frozen binary output, 3/3 identical)

```
RX=7 RY=2 RZ=624 RXF=3 RXB2=4 RWB2=4 RWB4=5 RWB5=6 COSTXY=1022 COSTXZ=-3936
B5A=1 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 B5G=1 B8=1 B9=1
DISTINCTD=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
TRIGX n=2 E14:3U F=1 E675:1U F=13
TRIGY n=0
TRIGW n=4 E14:3U F=1 E675:1U F=13 E735:1R F=15 E795:2R F=15
DECLX n=0 DECLY n=0 DECLW n=0
REDSEEDX n=0 REDSEEDY n=0 REDSEEDW n=2 BADRED=0
PROTDEST=0
SNAPWD S0=180 N0=9 C0=10 WP0=9 WQ0=48 S1=40 N1=1 C1=15 WP1=1 WQ1=10
       S2=54 N2=1 C2=22 WP2=1 WQ2=4 S3=47 N3=1 C3=19 WP3=1 WQ3=3
SNAPWR S0=180 N0=9 C0=59 WP0=9 WQ0=48 S1=40 N1=1 C1=39 WP1=1 WQ1=10
       S2=17157 N2=223 C2=3 WP2=223 WQ2=284 S3=35780 N3=439 C3=1 WP3=438 WQ3=660
SNAPWB S0=1056 N0=50 C0=1 WP0=50 WQ0=125 S1=342 N1=20 C1=1 WP1=19 WQ1=14
       S2=17157 N2=223 C2=55 WP2=223 WQ2=284 S3=35780 N3=439 C3=60 WP3=438 WQ3=660
SNAPWB4 S0=1104 N0=51 C0=26 WP0=51 WQ0=152 S1=2894 N1=58 C1=1 WP1=57 WQ1=150
       S2=17262 N2=225 C2=26 WP2=225 WQ2=331 S3=35780 N3=439 C3=31 WP3=438 WQ3=660
SNAPWB5 S0=1104 N0=51 C0=72 WP0=51 WQ0=152 S1=2894 N1=58 C1=44 WP1=57 WQ1=150
       S2=5508 N2=58 C2=2 WP2=57 WQ2=156 S3=36060 N3=442 C3=12 WP3=441 WQ3=697
```

Bar scorecard: B1 COMMIT-ORDER PASS (prereg 7be552ca4 strictly
predates implementation); B2 TOOLCHAIN PASS; B3 DETERMINISM PASS;
B4 NOVELTY PASS (Block-D distinct; all same-episode flip vectors
differ incl. W5 vs X/Y/Z; per-block ones-fractions in bands incl.
W5 B4 [28800,43200] and B5 [61200,72000]); B5a PRIMARY PASS
(1 <= 7 <= 99); B5b PASS (624 >= 500); B5c PASS (1022 < 4690);
B5d PASS (1 <= 4 <= 30); B5e PASS; B5f PASS (PARID=1 incl. W5 vs
X over 0..731, XDISJ=1); B5g PASS (b5gok=3); B6 PASS (learner fns
read only revealed values and derived tallies; the e==/cond==
hooks are write-only snapshots with no feedback into cell
state; harness gen() is the experimenter); B7 PASS (29-word grep
empty); B8 PASS (PROTDEST=0: no protected-unique cell destroyed
in any condition); B9 CO-PRIMARY PASS (REDSEEDW=2, BADRED=0).

## Reading of the result

Four triggers, four correct victim decisions, zero declines.

T1 (X/W5, log E14) and T2 (X/W5, log E675): the unprotected path
fired exactly as in MA2 (victims cell 3, cell 1; masks F=1,
F=13). X/Y/Z outputs are byte-identical to MA2's (verified by
cmp on the X/Y/Z sections), confirming the redundancy sub-rule
changes nothing when a useless cell exists.

T3 (W5, log E735 = 0-indexed 734, Block-B4 onset): the active
distractor cell (mean 21) erred 25..33 three straight on
{46..54}-values; trigger at B4k=3. All four candidates were
protected (mask F=15), so the redundancy path fired. Post-hoc
audit from the white-box state: victim cell 1 (mean 17, WP=19,
mean win-error 0.7) was redundant via cell 0 (mean 21, WP=50;
|17-21| = 4 <= 10); cell 3 (mean 81) was redundant via cell 2
(|81-76| = 5 <= 10). The frozen lowest-wpart rule picked cell 1
(19 < 437). Cell 1 reseeded as the 50-model (SNAPWB4: mean 49,
WP=57, protected again). Note: the trigger episode's winner was
cell 0 (the active cell, err 25 on a 48-value), so candidates
were {1,2,3}, all redundant; the prereg's alternate winner=cell-2
branch yields the same victim under the frozen rule. RWB4 = 5.

T4 (W5, log E795 = 0-indexed 794, Block-B5 onset): the active
50-cell erred 41..49 three straight on {91..99}-values; trigger
at B5k=3. Winner = cell 3 (err ~14). Candidates: cell 0 (mean
21) and cell 2 (mean 76). Cell 2 was redundant via cell 3
(|76-81| = 5 <= 10, both protected); cell 0 was UNIQUE (nearest
protected mean 49, distance 28 > 10). The rule picked cell 2,
the redundant 80-duplicate, over the unique distractor cell.
This is the discriminating case the prereg designed: a naive
any-protected rule had a live unique candidate in reach, and the
architecture did not take it. Cell 2 reseeded as the 95-model
(SNAPWB5: mean 94, WP=57). RWB5 = 6. PROTDEST = 0, BADRED = 0.

The key question is answered: with K=4 saturated by demonstrated
models, the architecture distinguished redundant from unique
knowledge twice, sacrificing one duplication layer per new block
while the unique inventory (distractor-21, then 50-model)
survived untouched. The decline path remains for the
all-unique-protected case but was correctly not needed here
(DECLW=0).

## Label-convention note (disclosed, not a reinterpretation)

The prereg's T1/T2 labels (E14, E675) followed MA2's log-style
convention (1-indexed display); its T3/T4 labels (E734, E794)
were 0-indexed episode numbers. The log prints 1-indexed labels,
so T3/T4 appear as E735/E795. Both denote exactly the
mechanism-derived trigger points (3rd onset episode of B4/B5:
consec 1,2,3 at 0-indexed 732/733/734 and 792/793/794). Victim
identities, paths, masks, tallies, and all bars are unaffected.

## Honest boundaries

- What is learned are cell means, same level as MA1/MA2
  (L1/L2-ish). Not strategy invention, not L3. RDDM=10 joins the
  researcher-supplied constants; redundancy status and victim
  choice are learner-driven from revealed values.
- Mean distance is a proxy for shared regime knowledge:
  distinct regimes within RDDM would be conflated. W5 keeps
  separations >= 15 against redundant pairs at <= 5. The
  (~21, ~17) distractor/B2 pair counts as redundant by the
  measure: by value they are one regime, and no block labels
  reach the cells.
- The decline path (all candidates protected and unique) is
  preserved but was not exercised in W5 (DECLW=0); a follow-up
  should force decline-vs-redundancy path selection.
- One W5 scenario, one frozen seed quintuple; MA1/MA2's four
  seeds were reused for direct comparability.
- RWB4=5/RWB5=6 are within the preregistered <= 15 bounds; the
  fresh reseeded cell takes active duty immediately (score 0),
  so recovery needs no second trigger.

## Artifacts in this lane

- `ma3.zag`: frozen implementation (B6/B7 audited).
- `ma3_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `5217cb95af51b7c656df1581e8720109fc811717c5297cc58005515e90d4dec8`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
