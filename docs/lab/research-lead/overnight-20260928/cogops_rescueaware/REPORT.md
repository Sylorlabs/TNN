# REPORT: COGOPS-RESCUEAWARE (rescue-aware expected-cost strategy selection)

Date: 2026-10-03. Worker: COGOPS-RESCUEAWARE.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_rescueaware/`
Prereg: frozen commit 890367dd4 (PREREG.md + NAMECHECK.md +
c15_predicted.txt, committed alone before any implementation file
existed).
Implementation commit follows this report.

## Verdict: BUILD-FAIL on K12 (prediction-file transcription slip); all mechanism bars K1-K11, K13-K16 PASS

The rescue-aware expected-cost mechanism is fully validated:
every behavioral prediction in the frozen prereg (Sections 2.3
and 6) is confirmed byte-exact by the implementation. K12's
`cmp` check fails for exactly one reason: the frozen
c15_predicted.txt is missing the `STAGE S13 WHOLE-LEAD` line, a
pre-freeze transcription slip in my file assembly (`tail -n
+219` instead of `+218`; the original S12 block was 17 lines,
not 18). The full-file diff between run output and frozen
prediction is precisely one line (215d214). This is the
worker's own assembly error, not a mechanism error: the S12
block itself matches byte-exact, and every kill bar that tests
the selection hypothesis passes.

The honest verdict is therefore BUILD-FAIL on K12, with the
failure precisely characterized and the one-line fix
identified (insert `STAGE S13 WHOLE-LEAD` before the S13
SPEC-RET line). The mechanism findings below are all
confirmed; they are reported as validated, not as passed
bars, pending the parent's decision on a transparent
amendment + re-freeze.

## Headline results

1. **Rescue-aware expected cost does NOT price S8's ALT tax
   (P2 confirmed).** After S7 the learner's rescue ledger is
   (rt,rc)=(6,2), E[rescue]=2.0. At S8 ALT-untried scores
   N=16,w=2 (8.0), strictly cheapest (48 < 64 vs 32/3 for
   PW/WHOLE/NEED) -> chosen=4; ALT's PW-form fails (2 CMP);
   ALT's NEED-form wins at pass 3 (4 NCMP, HYP lag=2 p=3 q=1);
   6 logged comparison events; no rescue observation (the lead
   won). Two mechanism-level reasons: (a) the untried
   strategy's optimistic turn-cost prior (1.0) still dominates
   even after adding P(fail)=1/2 * E[rescue]=2.0 (2.0 < 2.67
   for PW); (b) the promoted strategy wins outright via its
   NEED-form, so the rescue term never gets to bite. Pricing
   the tax would require a pessimistic turn-cost prior or a
   much larger E[rescue], not merely folding in the rescue
   term.

2. **The S12 divergence is real and mechanism-level (P4/K9
   confirmed).** Lesioned slot (4,613), R=37/10: NEED
   (N=147,w=7, 21.0) is the STRICT rescue-aware argmin over PW
   (N=97,w=4, 24.25; 588 < 679) -> DET-STRAT chosen=3 (EC chose
   1). The hedge does not fire (861 != 752). NEED leads at
   pass 2, logs 4 NCMP (eq=1,1,1,0, probe-verified apparatus
   values), HYP lag=2 p=2 q=0 mask=7, and WINS at pass 2
   (verify (3,1)=1,1,1). 4 events vs EC's 6. Q how=1 passes=4.
   OSC-CYCLE ph0=[1,611][1,771][1,771][1,612]
   ph1=[1,611][1,772][1,772][1,613] (live trajectory at q=0).
   Mechanism: the rescue term amplifies the P(fail) difference
   (NEED 1/7 < PW 1/4), rewarding reliability beyond what
   turn-level cost sees.

3. **Battery total 60 vs 62 (P7/K15 confirmed).** S3..S13
   logged comparisons (eq=-1 skips excluded): 60 under
   rescue-aware, 62 under EC/percontext. The reduction is
   entirely S12 (4 vs 6); S8's 6-event tax persists unchanged.
   Honest reading: MIXED. Rescue-aware reduces total events by
   2 via the S12 lesion (reliability rewarded) but does NOT
   price S8's ALT tax.

4. **The rescue ledger is exact (P7/K16 confirmed).**
   `RESCUE total=38 count=9`: S7 (6,2) [PW fail -> WHOLE 2;
   WHOLE fail -> NEED 4], S8 (6,2) [ALT won, no observation],
   S9 (8,3) [PW fail -> WHOLE 2], S10 (25,6) [PW fail ->
   WHOLE 2; WHOLE fail -> NEED 6; NEED fail -> ALT 9; ALT fail
   -> no successor, no empty observation], S11 (35,8) [PW
   fail -> WHOLE 2; WHOLE fail -> NEED 8], S12 (35,8) [NEED
   won as lead], S13 (38,9) [WHOLE fail -> ALT 3], S14 (38,9)
   [WHOLE won as lead].

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: cold (3,606) -> chosen=1 | byte-exact | PASS |
| K2 | S5: cold (3,613) -> chosen=1; PW wins 1 CMP; HYP p=2 q=0 | byte-exact | PASS |
| K3 | S7: cold (4,613) -> chosen=1; PW fail; SWITCH 1->2; WHOLE fail; SWITCH 2->3; NEED wins; rescue (6,2) | byte-exact | PASS |
| K4 | S8: ALT N=16 strict argmin (48<64) -> chosen=4; ALT PW-form fails; NEED-form wins pass 3; 6 events; NO rescue obs; (6,2) | byte-exact | PASS |
| K5 | S9: cold (3,615) -> chosen=1; PW fail; SWITCH 1->2; WHOLE wins lag 3; obs3 -> (8,3) | byte-exact | PASS |
| K6 | S10: cold (3,604) -> chosen=1; cascade all fail; 19 events; AGREE=1; obs4/5/6 -> (25,6); no empty obs | byte-exact | PASS |
| K7 | S9B: two DET-APPLY match=3/3; how=2; OSC-REUSE | byte-exact | PASS |
| K8 | S11: zeroed -> chosen=1; prior=3; PW->WHOLE->NEED; NEED wins; obs7/8 -> (35,8) | byte-exact | PASS |
| K9 | S12: NEED strict argmin (588<679) -> chosen=3 NOT 1/4; no hedge; 4 NCMP eq=1,1,1,0; HYP lag=2 p=2 q=0; NEED wins pass 2; 4 events; OSC-CYCLE ph0=[1,611][1,771][1,771][1,612] | byte-exact | PASS |
| K10 | S13: WHOLE N=57 strict argmin (285<308) -> chosen=2; WHOLE fails 1 CMP; SWITCH 2->4; ALT PW-form wins lag 3; obs9 -> (38,9) | byte-exact | PASS |
| K11 | S14: WHOLE N=62 strict argmin (310<336) -> chosen=2; wins 1 CMP | byte-exact | PASS |
| K12 | 3/3 byte-identical; stderr empty; cmp vs frozen prediction silent x3 | 3/3 identical (sha256 d9feba83 x3); .err 0 bytes; **cmp FAILS: 1-line diff (missing `STAGE S13 WHOLE-LEAD` in frozen prediction)** | **FAIL** |
| K13 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction, proven nesting shape | verified | PASS |
| K14 | prefix/base/world cmp-identical; additive diff = strat_sel + rescue cells/helpers/slog/det_handle hooks + comments (region-verified); main = comments + RESCUE line only | all verified | PASS |
| K15 | battery total S3..S13 = 60 (vs 62) | 60 | PASS |
| K16 | `RESCUE total=38 count=9` | byte-exact | PASS |

## The K12 transcription slip (worker's own error, fully characterized)

When assembling c15_predicted.txt from c14_predicted.txt, I
replaced the original S12 block (lines 201-217, 17 lines) using
`head -n 200` + new block + `tail -n +219`. The `+219` skipped
line 218, which was `STAGE S13 WHOLE-LEAD` (I miscounted the
original block as 18 lines). The frozen file is therefore
missing exactly one line. The complete diff:

```
215d214
< STAGE S13 WHOLE-LEAD
```

No prediction in PREREG.md Sections 2.3/6 is affected; the S12
block, CTX2 line, and RESCUE line in the frozen file are all
correct. The fix is a one-line insertion. I did not amend the
frozen file after seeing the run; that decision is the
parent's. Recommended: transparent amendment of
c15_predicted.txt (insert the missing line; no prediction
changes), re-freeze, re-verify cmp silence (the binary is
deterministic; rerunning is sufficient).

## Evidence detail

Stage-by-stage vs COGOPS-EXPECTEDCOST (lead chosen / logged
comparison events, eq=-1 skips excluded):

| stage | ec lead | ra lead | ec events | ra events |
|-------|---------|---------|-----------|-----------|
| S3 | 1 (PW) | 1 (PW) | 2 | 2 |
| S5 | 1 (PW) | 1 (PW) | 1 | 1 |
| S7 | 1 (PW) | 1 (PW) | 8 | 8 |
| S8 | 4 (ALT) | 4 (ALT) | 6 | 6 |
| S9 | 1 (PW) | 1 (PW) | 4 | 4 |
| S10 | 1 (PW) | 1 (PW) | 19 | 19 |
| S9B | reuse | reuse | 0 (+2 APPLY) | 0 (+2 APPLY) |
| S11 | 1 (PW) | 1 (PW) | 12 | 12 |
| S12 | 1 (PW) | 3 (NEED) | 6 | 4 |
| S13 | 2 (WHOLE) | 2 (WHOLE) | 4 | 4 |
| S14 | 2 (WHOLE) | 2 (WHOLE) | 1 | 1 |

Totals S3..S13: 62 (EC) vs 60 (rescue-aware).

The two rules agree on 13/14 stages. S8 agrees (ALT leads
under both; the rescue term is too small to demote the
untried, and ALT wins outright). S12 is the sole divergence:
the rescue term flips PW->NEED by amplifying the P(fail)
gap (1/7 vs 1/4).

Final context tables (CTX0/1/3/4 byte-identical to EC's):
`CTX2 sig=4,613 pw=2,2,4 who=1,0,4 need=6,6,13 alt=1,0,4`
(EC: pw=3,2,6; the PW lead-fail at EC's S12 never happens
here).

Score computations (frozen prereg, confirmed by selection):
- S8: N_ALT=16,w=2 (8.0) < N_PW=N_WHO=N_NEED=32,w=3 (10.67).
- S12: N_NEED=147,w=7 (21.0) < N_PW=97,w=4 (24.25) <
  N_WHO=N_ALT=134,w=3 (44.67).
- S13: N_WHO=N_ALT=57,w=2 (28.5) < N_PW=154,w=5 (30.8) <
  N_NEED=211,w=4 (52.75).
- S14: N_WHO=62,w=2 (31.0) < N_PW=168,w=5 (33.6) <
  N_ALT=146,w=3 (48.67) < N_NEED=230,w=4 (57.5).

## What this establishes (and does not)

Establishes: a concrete, learner-estimated rescue-aware cost
model (P(fail)=(u-w+1)/(u+2); E[rescue]=(rt+2)/(rc+2) global;
score=N_s/(u_s+2) by exact integer arithmetic); the finding
that folding P(fail)*E[rescue] into selection does NOT price
S8's ALT tax (the optimistic turn-cost prior dominates and
the promoted strategy wins outright); the S12 mechanism-level
divergence (rescue term rewards low P(fail)); the 60-vs-62
aggregate with the reduction localized to S12; an exact
rescue ledger (38,9).

Does not establish: that a pessimistic turn-cost prior would
preserve the promotion (untested); that per-context E[rescue]
behaves differently (checked analytically: S12 still picks
NEED; not implemented); that 60 < 62 generalizes beyond the
lesion battery; L3 representational invention; a
learner-invented cost model (the expectation form is
researcher-supplied).

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; `which python3` / `which python` return nothing
before, during, and after; verified this session). Pinned znc
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure Zag;
shell only for znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations, no near-misses. New Zag
scanned for the `while.*!(` negated-conjunction pattern: clean
(the only `!` hits are `!=` comparisons). The new `strat_sel`
keeps the proven COGOPS-EXPECTEDCOST nesting shape
(while -> if(ist==0) -> if(best!=0) -> comparison on hoisted
locals; hedge block tried==0 -> best!=0 -> c1>0 -> c3>0 ->
exact ==); rescue hooks use flat flag checks via
`rescue_finalize`. Git writes via /usr/bin/git absolute path,
explicit pathspecs, current branch (`tnn-native-lab`) only,
nothing pushed.

Apparatus characterization (not implementation): a trajectory
probe (/tmp/probe823, ephemeral) built from the frozen c14
sources with the S12 stage replaced by snapshot printing
measured goal 823's pass-0 snapshots ([611],[771],[771],[612])
to ground the preregistered S12 NCMP eq values (1,1,1,0). The
probe implements no selection or rescue logic; the world is
frozen and not under test.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_rescueaware/`:
PREREG.md (frozen, commit 890367dd4), NAMECHECK.md (Step 0),
c15_predicted.txt (frozen; contains the 1-line transcription
slip documented above), c15_base.zag (cmp-identical to
c14_base.zag), c15_world.zag (cmp-identical to c14_world.zag),
c15_strat_additive.zag (c14's with `strat_sel` replaced by the
rescue-aware rule + rescue ledger machinery), c15_learn.zag
(assembled; lines 1..1331 cmp-identical to the c12 prefix),
c15_main.zag (c14_main with comment updates + the RESCUE
summary line; non-comment diff verified additive-only),
c15_build.sh, c15_full.zag (assembled; exactly one `fn main`),
c15_bin, c15_compile.txt, c15_run1/2/3.txt (sha256 d9feba83 x3)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Transparent amendment of c15_predicted.txt (insert the
   missing `STAGE S13 WHOLE-LEAD` line; no prediction changes),
   re-freeze, re-verify cmp silence. The binary is
   deterministic; the mechanism is fully validated.
2. Pessimistic turn-cost prior: untried = expensive. The one
   variant not tested that could actually price S8's tax.
3. Per-context E[rescue]: implement and compare against the
   global variant (analytical check says S12 still picks
   NEED).
4. Learner-estimated P(fail) calibration: the battery is not
   designed to measure calibration; a dedicated battery with
   known ground-truth failure rates would test whether the
   Laplace estimates track reality.
