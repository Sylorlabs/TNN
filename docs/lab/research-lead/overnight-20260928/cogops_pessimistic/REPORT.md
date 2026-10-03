# REPORT: COGOPS-PESSIMISTIC (pessimistic turn-cost prior)

Date: 2026-10-03. Worker: COGOPS-PESSIMISTIC.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_pessimistic/`
Prereg: frozen commit ec01245307 (PREREG.md + NAMECHECK.md +
c16_predicted.txt, committed alone before any implementation file
existed).
Implementation commit follows this report.

## Verdict: BUILD-FAIL on K12 (two worker prediction/assembly errors); all mechanism bars K1-K11, K13-K16 PASS

The pessimistic-prior mechanism is fully validated: every
behavioral prediction in the frozen prereg (Sections 2.3 and 6)
is confirmed by the implementation, except two worker-side
errors in the frozen prediction file. K12's `cmp` check fails
for exactly two reasons, both characterized below. The honest
verdict is therefore BUILD-FAIL on K12, with the failures
precisely characterized. The mechanism findings are reported
as validated, pending the parent's decision on a transparent
amendment + re-freeze.

## Headline results

1. **The pessimistic turn-cost prior does NOT price S8's ALT
   tax (P2 confirmed).** With P=4, ALT-untried scores N=40,d=2
   (20.0), DEMOTED below PW/WHOLE/NEED (N=56,d=3, 18.67) in
   the argmin -> the loop leaves best=1 (PW). But the
   evidence-gated hedge then fires (tried==0; PW/WHOLE/NEED
   tie at 56/3 with c1=2>0, c3=4>0; n1*(bu+2)==bn*(u1+2) and
   n3*(bu+2)==bn*(u3+2)) -> DET-STRAT chosen=4. ALT's PW-form
   fails (2 CMP); ALT's NEED-form wins at pass 3 (4 NCMP,
   HYP lag=2 p=3 q=1); 6 logged comparison events; no rescue
   observation; (6,2). The S8 block is byte-identical to
   COGOPS-RESCUEAWARE's. Mechanism: the preregistered
   hedge-invariance (P0) holds -- the PW-NEED score tie at S8
   is exactly P-invariant (score_PW - score_NEED = (R-2)/3 =
   0 when R=2.0), so whenever the prior demotes ALT, the
   hedge re-promotes it. Pricing the tax through the prior
   alone is impossible; it would require changing or removing
   the hedge, a different experiment.

2. **The S12 NEED win is preserved (P4 confirmed).** Lesioned
   slot (4,613), R=37/10: NEED (N=207,d=7, 29.57) is the
   STRICT pessimistic-prior argmin over PW (N=157,d=4, 39.25;
   828 < 1099) -> DET-STRAT chosen=3. The hedge does not fire
   (157*7=1099 != 207*4=828). NEED leads at pass 2, 4 NCMP
   eq=1,1,1,0, HYP lag=2 p=2 q=0, WINS at pass 2. 4 events.
   S12 block byte-identical to RESCUEAWARE's. No untried
   strategy is present; the prior shift preserves NEED's
   reliability advantage.

3. **The prior is a blunt instrument (P5/P6 confirmed).** S13:
   PW is the strict argmin (N=214,d=5, 42.8 < N_WHO=117,d=2,
   58.5) -> chosen=1 (NOT 2); hedge does not fire; PW fails
   at pass 2 (2 CMP: (2,0,eq=0),(2,1,eq=0), probe-verified);
   DET-SWITCH 1->2; WHOLE wins at pass 3 (2 CMP:
   (3,1,eq=0),(3,0,eq=1), HYP lag=3, probe-verified);
   obs finalizes (37,9); 4 events; Q how=1 passes=5. S14:
   PW is the strict argmin (N=232,d=5, 46.4 < N_WHO=127,d=2,
   63.5) -> chosen=1 (NOT 2); PW wins at pass 2 (skip +
   2 CMP, HYP lag=2, probe-verified); no rescue obs; (37,9);
   Q how=1 passes=4. The prior cannot distinguish S8's bad
   untried from S13/S14's good untried: pricing S8's tax
   (which it doesn't) would cost S13/S14's untried leads.

4. **Battery total 60, unchanged (P8 confirmed).** S3..S13
   logged comparisons (eq=-1 skips excluded): 60 under both
   RESCUEAWARE and pessimistic-prior. S13 contributes 4
   (2+2) vs RESCUEAWARE's 4 (1+3). The tax is not priced;
   the total is unchanged.

5. **Rescue ledger (37,9) (P8 confirmed).** S7 (6,2), S8
   (6,2) [ALT won, no obs], S9 (8,3), S10 (25,6), S11 (35,8),
   S12 (35,8) [NEED won, no obs], S13 (37,9) [PW fail ->
   WHOLE 2], S14 (37,9) [PW won, no obs].

6. **The pessimistic-value question (Section 2.4).** Fixed
   P=4 demotes ALT in S8's argmin (20.0 > 18.67) but the
   hedge re-promotes it. The global-mean candidate
   (P=8/3 at S8) would not even demote (ALT 44/3=14.67 <
   136/9=15.11), leaving S8 RESCUEAWARE-identical via the
   argmin path. Max-observed coincides with P=4 at S8
   (NEED's 4). The S8 verdict is P-invariant (P0), so the
   "right" value is moot for the tax question; P=4 is the
   transparent fixed choice that makes the hedge's role
   observable.

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3: cold (3,606) -> chosen=1 | byte-exact vs RA run | PASS |
| K2 | S5: cold (3,613) -> chosen=1; PW wins 1 CMP | byte-exact vs RA run | PASS |
| K3 | S7: cold (4,613) -> chosen=1; cascade; rescue (6,2) | byte-exact vs RA run | PASS |
| K4 | S8: argmin demotes ALT (40/2=20.0 > 56/3=18.67) but hedge fires -> chosen=4; ALT PW-form fails; NEED-form wins pass 3; 6 events; no obs; (6,2); S8 block byte-identical to RA | byte-exact (chosen=4 implies hedge fired: loop leaves best=1) | PASS |
| K5 | S9: cold -> chosen=1; PW fail; SWITCH 1->2; WHOLE wins lag 3; (8,3) | byte-exact vs RA run | PASS |
| K6 | S10: cold -> chosen=1; cascade; 19 events; AGREE=1; (25,6) | byte-exact vs RA run | PASS |
| K7 | S9B: two DET-APPLY match=3/3; how=2 | byte-exact vs RA run | PASS |
| K8 | S11: zeroed -> chosen=1; prior=3; cascade; NEED wins; (35,8) | byte-exact vs RA run | PASS |
| K9 | S12: NEED strict argmin (207*4=828 < 157*7=1099) -> chosen=3; hedge silent; NEED wins pass 2; 4 events | byte-exact | PASS |
| K10 | S13: PW strict argmin (214/5 < 117/2) -> chosen=1; PW fails pass 2 (2 CMP); SWITCH 1->2; WHOLE wins pass 3 (2 CMP, HYP lag=3); (37,9); 4 events | byte-exact | PASS |
| K11 | S14: PW strict argmin (232/5 < 127/2) -> chosen=1; PW wins pass 2 (skip+2 CMP, HYP lag=2); (37,9) | byte-exact | PASS |
| K12 | 3/3 byte-identical; stderr empty; cmp vs frozen prediction silent x3 | 3/3 identical (sha256 9659274a x3); .err 0 bytes; **cmp FAILS: 2 worker-side diffs (STAGE S13 line position; CTX1 line)** | **FAIL** |
| K13 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction, proven nesting shape | verified | PASS |
| K14 | prefix/base/world cmp-identical; additive diff = 3 constants + comments (region-verified); main = comments only | all verified | PASS |
| K15 | battery total S3..S13 = 60 | 60 | PASS |
| K16 | `RESCUE total=37 count=9` | byte-exact | PASS |

## The K12 failures (worker's own errors, fully characterized)

Two diffs between run output and the frozen c16_predicted.txt:

1. **STAGE S13 WHOLE-LEAD line position** (assembly slip).
   The binary emits `STAGE S13 WHOLE-LEAD` BEFORE the
   SPEC-RET/LSTATE lines (run line 215); my assembled
   prediction placed it AFTER them (predicted line 219),
   because I copied the line structure from RA's
   c15_predicted.txt, which itself had the transcription
   slip. The complete diff hunk:
   ```
   215d214
   < STAGE S13 WHOLE-LEAD
   219a219
   > STAGE S13 WHOLE-LEAD
   ```
   Fix: move the line before `SPEC-RET rev=9`.

2. **CTX1 line** (prediction error). I predicted CTX1
   byte-identical to RESCUEAWARE's (`pw=3,2,6 who=1,1,1
   need=2,0,8 alt=1,0,4`), forgetting that S14's harness
   lesion (`strat_lesion_s14`) OVERWRITES the (3,613) slot,
   erasing S5's history. Correct value: lesion PW[3,2,6]
   NEED[2,0,8] ALT[1,0,4] WHO[0,0,0], then S14's PW win
   (tc=3, skip counts) -> `CTX1 sig=3,613 pw=4,3,9
   who=0,0,0 need=2,0,8 alt=1,0,4`, exactly as the run
   shows. The mechanism is correct; my P9 hand-trace was
   wrong.

Both are worker-side errors, not mechanism errors: the
S13/S14/CTX3/RESCUE predictions are byte-exact, and the
run-vs-RA-run diff contains exactly the predicted
mechanism changes (S13/S14 leads, CTX3, RESCUE) plus the
correct CTX1. I did not amend the frozen file after seeing
the run; that decision is the parent's. Recommended:
transparent amendment of c16_predicted.txt (move the STAGE
line; correct the CTX1 line; no prediction changes),
re-freeze, re-verify cmp silence (the binary is
deterministic; rerunning is sufficient).

## Evidence detail

Run-vs-RESCUEAWARE-run diff (the complete mechanism delta):

| stage | RA lead | pess lead | RA events | pess events |
|-------|---------|-----------|-----------|-------------|
| S3 | 1 (PW) | 1 (PW) | 2 | 2 |
| S5 | 1 (PW) | 1 (PW) | 1 | 1 |
| S7 | 1 (PW) | 1 (PW) | 8 | 8 |
| S8 | 4 (ALT) | 4 (ALT, via hedge) | 6 | 6 |
| S9 | 1 (PW) | 1 (PW) | 4 | 4 |
| S10 | 1 (PW) | 1 (PW) | 19 | 19 |
| S9B | reuse | reuse | 0 (+2 APPLY) | 0 (+2 APPLY) |
| S11 | 1 (PW) | 1 (PW) | 12 | 12 |
| S12 | 3 (NEED) | 3 (NEED) | 4 | 4 |
| S13 | 2 (WHOLE) | 1 (PW) | 4 | 4 |
| S14 | 2 (WHOLE) | 1 (PW) | 1 (+0 skip) | 2 (+1 skip) |

Totals S3..S13: 60 (RA) vs 60 (pessimistic). S8 agrees
(ALT leads under both; the prior demotes ALT in the
argmin but the hedge re-promotes it). S13/S14 flip to PW
(the blunt-instrument cost).

Score computations (frozen prereg, confirmed by selection):
- S8: N_PW=N_WHO=N_NEED=56,d=3 (18.67); N_ALT=40,d=2
  (20.0). Argmin: PW (best=1). Hedge: r1=r3=1 -> chosen=4.
- S12: N_NEED=207,d=7 (29.57) < N_PW=157,d=4 (39.25) <
  N_WHO=N_ALT=194,d=3 (64.67). chosen=3.
- S13: N_PW=214,d=5 (42.8) < N_WHO=N_ALT=117,d=2 (58.5) <
  N_NEED=271,d=4 (67.75). chosen=1.
- S14: N_PW=232,d=5 (46.4) < N_WHO=127,d=2 (63.5) <
  N_ALT=210,d=3 (70.0) < N_NEED=293,d=4 (73.25). chosen=1.

## What this establishes (and does not)

Establishes: the pessimistic turn-cost prior (P=4) does NOT
price S8's ALT tax, because the evidence-gated hedge
re-promotes ALT whenever the prior demotes it (the PW-NEED
tie is P-invariant at R=2); the S12 NEED win is preserved
under the pessimistic prior; the prior is a blunt
instrument (S13/S14 flip to PW); the battery total is
unchanged at 60; the rescue ledger is (37,9); the fixed
P=4 coincides with max-observed at S8 while the global
mean would not even demote.

Does not establish: that removing/changing the hedge would
price the tax (untested; the hedge is load-bearing
elsewhere); that 60 generalizes; L3 representational
invention; a learner-invented cost model (P=4 is
researcher-supplied, like the Laplace constants).

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; `which python3` / `which python` return nothing
before, during, and after; verified this session). Pinned znc
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation pure Zag;
shell only for znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations, no near-misses. New Zag
scanned for the `while.*!(` negated-conjunction pattern: clean
(the change is three constants; the proven `strat_sel`
nesting shape is untouched). Git writes via /usr/bin/git
absolute path, explicit pathspecs, current branch
(`tnn-native-lab`) only, nothing pushed.

Apparatus characterization (not implementation): a trajectory
probe (/tmp/probe_traj_bin, ephemeral) built from the frozen
c15 sources with main replaced by pass-0..5 snapshot printing
measured goal 824 eq(2,0)=0 eq(2,1)=0 eq(3,1)=0 eq(3,2)=0
eq(3,0)=1 eq(4,1)=1 and goal 825 eq(2,0)=1 eq(2,1)=0
eq(3,1)=1, reproducing all RA-verified values exactly and
grounding the new S13/S14 turn predictions. The probe
implements no selection, prior, or rescue logic; the worlds
are frozen and not under test.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_pessimistic/`:
PREREG.md (frozen, commit ec01245307), NAMECHECK.md (Step 0),
c16_predicted.txt (frozen; contains the 2 worker-side errors
documented above), c16_base.zag (cmp-identical to c15_base.zag),
c16_world.zag (cmp-identical to c15_world.zag),
c16_strat_additive.zag (c15's with three `(c+2)`->`(c+8)`
N-term constants + comments), c16_learn.zag (assembled; lines
1..1331 cmp-identical to the c12 prefix), c16_main.zag
(c15_main with comment updates only; non-comment diff empty),
c16_build.sh, c16_full.zag (assembled; exactly one `fn main`),
c16_bin, c16_compile.txt, c16_run1/2/3.txt (sha256
9659274a96b59cf8c511a0974dda7229ee6373753ad332f11647a98676283d17 x3)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Transparent amendment of c16_predicted.txt (move the
   `STAGE S13 WHOLE-LEAD` line before `SPEC-RET rev=9`;
   correct the CTX1 line to `pw=4,3,9 who=0,0,0`; no
   prediction changes), re-freeze, re-verify cmp silence.
   The binary is deterministic; rerunning is sufficient.
2. Hedge-removal variant: the one experiment that could
   actually price S8's tax (P0 shows the prior alone cannot).
   Preregister whether S8 then picks PW and what the
   downstream costs are (S13/S14-like flips elsewhere?).
3. Learner-estimated pessimistic value (tracked max-observed
   turn cost): the S8 verdict is P-invariant, but the
   dynamics at other stages would differ from fixed P=4.
