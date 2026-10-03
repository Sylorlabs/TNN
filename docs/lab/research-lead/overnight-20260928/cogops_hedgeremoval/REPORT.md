# REPORT: COGOPS-HEDGEREMOVAL (hedge-removal variant)

Date: 2026-10-03. Worker: COGOPS-HEDGEREMOVAL.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_hedgeremoval/`
Prereg: frozen commit 252a627bf (PREREG.md + NAMECHECK.md +
c17_predicted.txt, committed alone before any implementation file
existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (16/16 kill bars)

The hedge-removal mechanism is fully validated: every behavioral
prediction in the frozen prereg is confirmed by the implementation,
including the byte-exact K12 `cmp` (silent x3). The experiment
answers COGOPS-PESSIMISTIC's open question directly.

## Headline results

1. **S8's ALT tax IS priced (P1 confirmed).** With the hedge
   deleted, S8's argmin stands: PW/WHOLE/NEED tie at 56/3=18.67,
   ALT demoted at 40/2=20.0 -> DET-STRAT chosen=1 (NOT 4).
   PW fails at pass 2 (2 CMP, probe-verified); DET-SWITCH 1->2;
   WHOLE fails at pass 3 (2 CMP, probe-verified); DET-SWITCH
   2->3; NEED wins at pass 4 (4 NCMP eq=1,1,1,0, HYP lag=2 p=4
   q=2 mask=7, probe-verified; DET-PRIOR set=2). 8 logged
   comparison events (not 6). Two rescue observations recorded:
   (rt,rc) goes (6,2) -> (12,4). **ALT never leads.** The
   preregistered hedge-invariance argument (P0) is resolved the
   only way it could be: no turn-cost prior prices the tax; only
   removing the hedge does.

2. **The hedge's value, measured (task question 3).** In the
   c16 battery the hedge fires EXACTLY ONCE (S8: chosen=4 is its
   unique signature, the argmin loop leaves best=1 there; every
   other initial selection is hedge-inert by code inspection:
   cold stages gate on c1>0/c3>0, S12/S13/S14 are strict
   argmins, rescue-time selections never satisfy tried==0).
   Its sole behavioral effect was the 6-event ALT re-promotion
   at S8, which buys nothing: the NEED win it routes around is
   reached anyway through the ordinary rescue cascade. Removing
   the hedge changes NO other stage's behavior. In this
   battery, the hedge is pure cost; no world here rewards
   alternation-hedging on a genuine PW/NEED tie, so whether it
   is ever beneficial remains untested (not settled by this
   experiment).

3. **No downstream breakage (P2 confirmed).** S9/S10/S9B/S11
   blocks are byte-identical to c16's (cold/APPLY stages are
   selection-invariant to the ledger). S12: NEED remains the
   strict argmin under the shifted ledger (41,10):
   247/7=35.29 < 187/4=46.75 (988 < 1309) -> chosen=3, NEED
   wins pass 2, 4 events, block byte-identical. S13: PW strict
   argmin (254/5=50.8 < 139/2=69.5; 508 < 695) -> chosen=1,
   PW fails, SWITCH 1->2, WHOLE wins lag 3, obs -> (43,11),
   block byte-identical. S14: PW strict argmin (272/5=54.4 <
   149/2=74.5; 544 < 745) -> chosen=1, PW wins pass 2,
   (43,11), block byte-identical. CTX0-4 byte-identical
   (S11's zeroing and S12's lesion erase S8's table writes).

4. **The price of pricing.** S8 costs 8 events vs the hedge's
   6 (+2), and +2 rescue observations. Battery total S3..S13:
   62 vs c16's 60 (P4 confirmed). Final rescue ledger:
   RESCUE total=43 count=11 vs c16's (37,9) (P3 confirmed).
   Trace: S7 (6,2), S8 (12,4), S9 (14,5), S10 (31,8),
   S11 (41,10), S12 (41,10) [no obs], S13 (43,11),
   S14 (43,11) [no obs].

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: chosen=1, block byte-identical to c16 | byte-exact | PASS |
| K2 | S5: chosen=1; PW wins 1 CMP; byte-identical | byte-exact | PASS |
| K3 | S7: chosen=1; cascade; rescue (6,2); byte-identical | byte-exact | PASS |
| K4 | S8 TAX-PRICING: chosen=1 (NOT 4); PW fail 2 CMP; SWITCH 1->2; WHOLE fail 2 CMP; SWITCH 2->3; NEED wins pass 4 (4 NCMP, HYP lag=2 p=4 q=2 mask=7); DET-PRIOR set=2; 8 events; (12,4); Q how=1 passes=6 | byte-exact vs frozen S8 block (chosen=1, 8 events) | PASS |
| K5 | S9: byte-identical; obs -> (14,5) | byte-exact | PASS |
| K6 | S10: byte-identical; 19 events; AGREE=1; (31,8) | byte-exact | PASS |
| K7 | S9B: two DET-APPLY match=3/3; how=2; byte-identical | byte-exact | PASS |
| K8 | S11: byte-identical; prior=3; NEED wins; (41,10) | byte-exact | PASS |
| K9 | S12 NO-BREAKAGE 1: chosen=3 (988 < 1309); NEED wins pass 2; 4 events; byte-identical | byte-exact | PASS |
| K10 | S13 NO-BREAKAGE 2: chosen=1 (508 < 695); PW fail; SWITCH 1->2; WHOLE wins lag 3; (43,11); byte-identical | byte-exact | PASS |
| K11 | S14 NO-BREAKAGE 3: chosen=1 (544 < 745); PW wins pass 2; (43,11); byte-identical | byte-exact | PASS |
| K12 | 3/3 byte-identical; stderr empty; cmp vs frozen prediction silent x3 | 3/3 identical (sha256 c062d1280b29b920554ec1af9e45505c857e04f738316f14bd58e9bc890f8464 x3); .err 0 bytes; cmp SILENT x3 | PASS |
| K13 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction, proven argmin nesting shape | verified (which python3/python empty before/after; neg-conj scan clean) | PASS |
| K14 | base/world cmp-identical; prefix 1..1331 cmp-identical; additive diff = hedge-block deletion + comments (region-verified); main = comments only | all verified | PASS |
| K15 | battery total S3..S13 = 62 | 62 | PASS |
| K16 | `RESCUE total=43 count=11` | byte-exact | PASS |

## Evidence detail

Run-vs-COGOPS-PESSIMISTIC-run diff (the complete mechanism delta):

| stage | c16 lead | c17 lead | c16 events | c17 events |
|-------|----------|----------|------------|------------|
| S3 | 1 (PW) | 1 (PW) | 2 | 2 |
| S5 | 1 (PW) | 1 (PW) | 1 | 1 |
| S7 | 1 (PW) | 1 (PW) | 8 | 8 |
| S8 | 4 (ALT, via hedge) | 1 (PW, argmin) | 6 | 8 |
| S9 | 1 (PW) | 1 (PW) | 4 | 4 |
| S10 | 1 (PW) | 1 (PW) | 19 | 19 |
| S9B | reuse | reuse | 0 (+2 APPLY) | 0 (+2 APPLY) |
| S11 | 1 (PW) | 1 (PW) | 12 | 12 |
| S12 | 3 (NEED) | 3 (NEED) | 4 | 4 |
| S13 | 1 (PW) | 1 (PW) | 4 | 4 |
| S14 | 1 (PW) | 1 (PW) | 2 (+1 skip) | 2 (+1 skip) |

Totals S3..S13: 60 (c16) vs 62 (c17). The ONLY selection that
changes is S8's (4 -> 1); every other stage block is
byte-identical to c16's. The c17-vs-frozen-prediction diff is
empty (K12).

Score computations (frozen prereg, confirmed by selection):
- S8: N_PW=N_WHO=N_NEED=56,d=3 (18.67); N_ALT=40,d=2
  (20.0). Argmin: PW by id (best=1). Hedge deleted.
  Rescue argmins: {2,3,4} -> WHO (56/3 tie, id); {3,4} ->
  NEED (56/3 < 40/2).
- S12 (ledger (41,10)): NEED 247/7 strict (988 < 1309).
- S13 (ledger (41,10)): PW 254/5 strict (508 < 695).
- S14 (ledger (43,11)): PW 272/5 strict (544 < 745).

## What this establishes (and does not)

Establishes: removing the evidence-gated hedge prices S8's ALT
tax (chosen=1, 8 events, ALT never leads); the hedge's only
behavioral effect in this 14-stage battery was S8's 6-event
ALT re-promotion (it fires nowhere else); hedge removal
breaks no other stage (S9/S10/S9B/S11 byte-identical;
S12/S13/S14 selections robust to the ledger shift, margins
verified); pricing costs +2 events and +2 rescue observations
at S8 (battery 62 vs 60; ledger (43,11) vs (37,9)).

Does not establish: that alternation-hedging is never useful
(no world here rewards it; untested, not settled); that 62
generalizes; L3 representational invention; that the hedge
should be permanently deleted (a design decision for the
parent: the mechanism is now priced, the policy choice is
not this worker's); a learner-invented hedge policy.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; `which python3` / `which python` return nothing
before, during, and after; verified this session). Pinned znc
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure Zag;
shell only for znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations, no near-misses. New Zag
scanned for the `while.*!(` negated-conjunction pattern: clean
(the change is deletion of the hedge block; the proven
`strat_sel` argmin nesting shape is untouched). Git writes via
/usr/bin/git absolute path, explicit pathspecs, current branch
(`tnn-native-lab`) only, nothing pushed.

Apparatus characterization (not implementation): a trajectory
probe (/tmp/probe_hr_bin, ephemeral) built from the frozen
c16 sources with main replaced by S1A..S7 prefix + pass-0..5
snapshot printing for goal 823 measured eq(2,0)=0, eq(2,1)=0,
eq(3,1)=0, eq(3,0)=0, per-need eq(4,2)=[1,1,1,0],
eq(4,3)=[1,0,0,0], eq(5,3)=[1,1,1], and trajectory phases at
passes 2,3 identical to S7's ([1,611][1,771][1,771][1,614] /
[1,611][1,772][1,772][1,615]), grounding the S8 cascade
prediction (PW fail / WHOLE fail / NEED wins at pass 4). The
probe implements no selection, prior, hedge, or rescue logic;
the worlds are frozen and not under test.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_hedgeremoval/`:
PREREG.md (frozen, commit 252a627bf), NAMECHECK.md (Step 0),
c17_predicted.txt (frozen; K12 cmp-silent x3),
c17_base.zag (cmp-identical to c16_base.zag),
c17_world.zag (cmp-identical to c16_world.zag),
c17_strat_additive.zag (c16's with the hedge block deleted +
comments), c17_learn.zag (assembled; lines 1..1331 cmp-identical
to the c12 prefix), c17_main.zag (c16_main with comment updates
only; non-comment diff empty), c17_build.sh, c17_full.zag
(assembled; exactly one `fn main`), c17_bin, c17_compile.txt,
c17_run1/2/3.txt (sha256
c062d1280b29b920554ec1af9e45505c857e04f738316f14bd58e9bc890f8464 x3)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Policy decision: the hedge is now priced (pure cost in this
   battery). Whether to delete it permanently from the
   architecture, keep it as a dormant option, or replace it
   with a learner-owned alternation policy is a design call.
2. A world that genuinely rewards alternation-hedging (PW and
   NEED each half-right, ALT strictly best) would test whether
   the hedge is ever beneficial; no such world exists in this
   battery.
3. Learner-estimated turn-cost prior (tracked max-observed):
   orthogonal to the hedge; the S8 verdict is now hedge-driven
   rather than P-driven.
