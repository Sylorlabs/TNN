# REPORT: COGOPS-ALTERNATION-WORLD (is the hedge ever beneficial?)

Date: 2026-10-03. Worker: COGOPS-ALTERNATION-WORLD.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_alternation_world/`
Prereg: frozen commit 5abe4f174 (PREREG.md + NAMECHECK.md +
c18_predicted.txt + c18h_predicted.txt, committed alone before
any implementation file existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (11/11 kill bars)

**The hedge IS beneficial on the alternation world.** Given a
genuine PW/NEED score tie with in-context evidence for both,
the hedge (ALT-first) strictly beats the hedge-less argmin
(PW-first by lower-id tie-break): 6 events vs 8, 0 rescue
observations vs 2, a single ALT win vs the PW->WHOLE->NEED
rescue cascade. The design decision is therefore nuanced,
not a clean delete: the hedge is pure cost in the c16/c17
battery but has measurable value on a tie world where NEED
is the eventual winner. Whether to keep it is Micah's call;
the mechanism is now priced in both directions.

## Headline results

1. **PW and NEED each half-right (K1, K2 confirmed).**
   S_PW (goal 830, PW-world, whole-state lag-2 oscillation):
   cold context (3,613), PW leads by id, wins at pass 2 in
   2 CMP (DET-HYP lag=2 p=2 q=0 mask=7); NEED untried. PW
   is the efficient strategy here. S_NEED (goal 831,
   NEED-world, partial oscillation): cold context (4,613),
   PW leads by id and fails outright (2 CMP, whole state
   never repeats because need3 drifts); WHOLE fails
   (2 CMP); NEED rescues and wins at pass 4 (4 NCMP
   eq=1,1,1,0, DET-HYP lag=2 p=4 q=2 mask=7). Rescue ledger
   (6,2); table (4,613): PW=(1,0,2), WHOLE=(1,0,2),
   NEED=(1,1,4). NEED is the right strategy here; PW is
   wrong. Each strategy is the right one on one world.

2. **The tie is exact and the hedge fires (K3, K4
   confirmed).** At S_TEST (goal 832, fresh tag, same
   context (4,613)): (rt,rc)=(6,2), ra=8, rb=4;
   N_PW=N_WHOLE=N_NEED=56 (d=3), N_ALT=40 (d=2). Argmin
   leaves best=1 (PW, lower-id tie-break). With the hedge
   (c18h): tried==0, c1=2>0, c3=4>0,
   n1*(bu+2)=168==bn*(u1+2), n3*(bu+2)=168==bn*(u3+2) ->
   r1=r3=1 -> best=4. DET-STRAT chosen=4. The tie
   N1==N3==56 is exact but ledger-dependent
   (10*rb+2*ra==12*rb+ra iff ra==2*rb, satisfied at
   (6,2)); it is deterministic in this battery.

3. **The hedge's value, measured (task question 3).**
   With-hedge S_TEST: ALT's pw part fails at pass 2
   (2 CMP), ALT's need part wins at pass 3 (4 NCMP
   eq=1,1,1,0, DET-HYP lag=2 p=3 q=1 mask=7, verify at
   (4,2)). No DET-SWITCH (single strategy; rescue never
   opens). 6 events. Q how=1 passes=5. cx_rec ALT win
   cost 6 -> ALT=(1,1,6). Ledger stays (6,2).
   Without-hedge S_TEST: chosen=1; PW fails (2 CMP);
   SWITCH 1->2; WHOLE fails (2 CMP); SWITCH 2->3; NEED
   wins at pass 4 (4 NCMP, DET-HYP lag=2 p=4 q=2 mask=7).
   8 events. Q how=1 passes=6. Ledger (12,4); table
   PW=(2,0,4), WHOLE=(2,0,4), NEED=(2,2,8).
   The hedge saves 2 events and 2 rescue observations and
   avoids two failed turns. "ALT strictly best" is
   relative to the mechanism's no-hedge tie-break
   (PW-first); NEED-first would be 4 events, but the
   argmin never selects it (lower-id tie-break picks PW).

4. **No other behavioral difference (K1, K2, K11
   confirmed).** S_PW and S_NEED blocks are byte-identical
   across the two binaries (the hedge is inert on cold
   contexts: c1=0). All six setup-stage blocks (S1A/S1B/
   S2/S4/S6L/S6B) are byte-identical to c17_run1.txt's.
   The c18 vs c18h mechanism delta is exactly the hedge
   block (code-only diff: the 23-line `if(tried==0){...}`
   region; K10).

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S_PW: chosen=1; PW wins 2 CMP; HYP 830 lag2 p2 q0 mask7; passes=4; block identical c18/c18h | byte-exact, identical | PASS |
| K2 | S_NEED: chosen=1; PW fail; SWITCH 1->2; WHOLE fail; SWITCH 2->3; NEED wins p4 (4 NCMP, HYP lag2 p4 q2 mask7); 8 events; passes=6; block identical | byte-exact, identical | PASS |
| K3 | S_TEST tie: N1=N2=N3=56 d3, N4=40 d2; c1=2>0 c3=4>0; argmin best=1 | divergence chosen=4 vs 1 confirms | PASS |
| K4 | S_TEST with-hedge: chosen=4 (NOT 1); 2 CMP + 4 NCMP p=3 eq=1,1,1,0; HYP 832 lag2 p3 q1 mask7; NO SWITCH; 6 events; passes=5; alt=1,1,6 | byte-exact vs frozen | PASS |
| K5 | S_TEST no-hedge: chosen=1 (NOT 4); PW fail; SWITCH 1->2; WHOLE fail; SWITCH 2->3; NEED wins p4; 8 events; passes=6; pw=2,0,4 who=2,0,4 need=2,2,8 | byte-exact vs frozen | PASS |
| K6 | hedge S_TEST 6 < no-hedge 8 events; RESCUE (6,2) < (12,4) | 6<8; total=6 count=2 vs total=12 count=4 | PASS |
| K7 | 3/3 byte-identical per binary; stderr empty | sha256 c18 6972abbb... x3, c18h 50fb1fcb... x3; .err 0 bytes x6 | PASS |
| K8 | cmp vs frozen predictions silent x6 | cmp SILENT x6 (c18 x3, c18h x3) | PASS |
| K9 | safebin, no python, pure Zag, pinned znc, neg-conj clean | verified | PASS |
| K10 | base/world/learn provenance; additive diff = hedge block only; single driver | all verified; code diff = 23-line hedge block | PASS |
| K11 | setup blocks byte-identical to c17_run1.txt's | 6/6 blocks identical | PASS |

## What this establishes (and does not)

Establishes: on a world where PW and NEED are each
half-right and tie exactly (56/3) with in-context evidence,
the evidence-gated hedge fires and its ALT-first policy
strictly beats the hedge-less PW-first policy (6 vs 8
events, 0 vs 2 rescue observations, single ALT win vs
PW->WHOLE->NEED cascade). The hedge is not pure cost in
general; it has measurable value on tie worlds where NEED
is the eventual winner and WHOLE is useless.

Does not establish: that the hedge should be kept (design
decision for the parent); how often genuine ties arise
without engineering; that alternation-hedging generalizes
beyond this world kind; L3 representational invention; a
learner-owned hedge policy.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin;
`which python3` / `which python` return nothing before and
after; verified this session). Pinned znc
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
for both builds. All computation pure Zag; shell only for
znc/binary/git/assembly/byte verification. Zero
forbidden-executable invocations. New Zag (3 goal
constructors + driver stages) scanned for the `while.*!(`
negated-conjunction pattern: clean. Git writes via
/usr/bin/git absolute path, explicit pathspecs, current
branch (`tnn-native-lab`) only, nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_alternation_world/`:
PREREG.md (frozen, commit 5abe4f174), NAMECHECK.md (Step 0),
c18_predicted.txt / c18h_predicted.txt (frozen; K8
cmp-silent x6), c18_base.zag (cmp-identical to c17_base),
c18_world.zag (c17 + 3 constructors), c18_strat_additive.zag
(= c17, no hedge), c18h_strat_additive.zag (= c16, hedge),
c18_learn.zag / c18h_learn.zag (c12 prefix + additive),
c18_main.zag (single driver), c18_full.zag / c18h_full.zag
(assembled; exactly one `fn main` each), c18_bin / c18h_bin,
c18_compile.txt / c18h_compile.txt, c18_run1/2/3.txt
(sha256 6972abbb48dfc81ed0cf32f76016b1538b3641ab002a32ae2ee47ccdb84a0a27 x3)
+ .err (empty), c18h_run1/2/3.txt (sha256
50fb1fcba4cdae600d4ec5151585158fa3571d4c6d10e99b87fd4ebd364d61fa x3)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Policy decision: the hedge now has a priced benefit (tie
   worlds where NEED eventually wins: 6 vs 8 events, fewer
   rescue ledger entries) AND a priced cost (c16/c17
   battery: pure cost, S8's 6-event ALT re-promotion buying
   nothing). Keep for tie-worlds / delete / replace with a
   learner-owned alternation policy is a design call.
2. The tie here is engineered and ledger-dependent; a
   natural-tie frequency study would say how often the
   hedge's firing condition arises unengineered.
3. A stronger alternation world (phase-dependent NEED
   winnability, where the no-hedge path misses the win
   entirely) would test whether the hedge can be
   strictly-necessary, not just cheaper; not attempted
   here.
