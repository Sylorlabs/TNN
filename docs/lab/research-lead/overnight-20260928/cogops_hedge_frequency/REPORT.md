# REPORT: COGOPS-HEDGE-FREQUENCY (natural hedge firing frequency)

Date: 2026-10-03. Worker: COGOPS-HEDGE-FREQUENCY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_hedge_frequency/`
Prereg: frozen commit ee97f04d6 (PREREG.md + NAMECHECK.md +
c19_stages_predicted.txt, committed alone before any
implementation file existed).
Implementation commit follows this report.

## Verdict: BUILD-PASS (9/9 kill bars; K4 N/A by preregistered condition)

**The hedge never fired.** Across 22 eligible selections on
7 non-engineered world kinds in 4 contexts, the exact-tie
firing condition arose zero times: 0/22 = 0%. The positive
control proves the instrument can fire (it reproduces the
engineered c18 S_TEST tie exactly: `DET-HEDGE before=1
dt1=0 dt3=0 ev=2004`, chosen=4). So the zero is a genuine
measurement, not a broken detector. Per the preregistered
K3 branches, this kills the "fires commonly" hypothesis and
is DELETE-leaning base-rate evidence for governance item
#11. K4 (help/hurt on natural firings) is N/A: there were
no natural firings to price.

## Headline results

1. **Frequency: 0/22 eligible selections (K3).** 26
   detection stages ran; 26 DET-HGATE == 26 DET-STRAT
   (K1 count part); eligible (c1>0 AND c3>0) = 22, exactly
   the frozen prediction (all stages except the
   context-first F01/F09/F17/F23). Zero DET-HEDGE lines.
   The 95% rule-of-three upper bound is ~13.6%, but the
   selections share learner state (not i.i.d.), so 0/22
   is reported as the point measurement with that caveat.

2. **Why it never fired: per-context strict dominance,
   not near-ties.** Initial selections by context:
   - (3,613): NEED (best=3) on all 7 eligible stages.
     NEED wins at 3 events on BOTH the N3 and P3 world
     kinds, ending (8,8,24); PW froze at (1,0,2) after
     F01 and was never selected again. The score gap
     widens monotonically.
   - (4,613): NEED (best=3) on all 7 eligible stages,
     ending (8,8,32); PW frozen at (1,0,2).
   - (3,615): PW (best=1) on all 5 eligible stages.
     PW always fails here but has the cheapest
     rescue-aware expected cost; c1 grew 2->7 while
     NEED/WHOLE/ALT accumulated failure costs.
   - (3,604): PW (best=1) on all 3 eligible stages,
     same pattern.
   ALT was never selected by any path (0/26): neither by
   the hedge (0 firings) nor by the argmin. The
   Laplace-smoothed rescue-aware scores separate as
   evidence accumulates asymmetrically: the leader gets
   picked, accrues a matching record, and extends its
   lead. Exact ties are knife-edge, and the selection
   dynamics are ANTI-tie: nothing in 22 selections
   produced a leadership transition, which is where a
   tie could occur.

3. **Instrument validity (positive control).** A separate
   build (c19pos: instrumented c19h strat + c18's
   alternation driver) reproduces the known engineered
   firing: S_TEST emits `DET-HEDGE before=1 dt1=0 dt3=0
   ev=2004` and `DET-STRAT chosen=4`, and the stripped
   output is byte-identical to c18h_run1.txt. The
   instrument therefore reports genuine ties correctly;
   the battery's zero is real. (K2 is vacuously
   satisfied on the battery itself: no HEDGE lines to
   violate dt1==0/dt3==0/ev>=1001.)

4. **Control purity (K5).** With zero firings, all 26
   stages are non-fired: c19h output minus
   DET-HGATE/DET-HEDGE lines is byte-identical to c19
   output. The instrumentation is behavior-neutral and
   the hedge is the only mechanism delta.

5. **No other behavioral anomalies.** Q sequence matches
   the frozen predictions exactly (26/26: id, goal tag,
   how; how=1 on kinds 1-5, how=0 on kinds 6-7). Setup
   blocks S1A/S1B/S2/S4/S6L/S6B byte-identical to
   c17_run1.txt's. 3/3 byte-identical per binary
   (sha256 c19 c72aa165..., c19h 91693144...), stderr
   empty x6. Max DET lines per stage 25 < 32 (ring never
   near overflow). plans_built=26 (one per fresh tag);
   plans_loaded=7 = the 7 how=0 fallback stages
   (compose_iter path increments the same counter).

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | 26 HGATE == 26 STRAT; every HEDGE before == its stage's HGATE best | 26/26; zero HEDGE lines (implication vacuous) | PASS |
| K2 | every HEDGE: dt1==0, dt3==0, ev>=1001 | zero HEDGE lines (vacuous); positive control shows dt1=0 dt3=0 ev=2004 on the engineered tie | PASS |
| K3 | eligible == 22 | eligible=22; fires=0; frequency 0/22 | PASS (fires==0 branch: DELETE-leaning) |
| K4 | per-fired-stage saved/wasted, iff fires>=1 | fires=0 -> N/A per prereg | N/A |
| K5 | non-fired c19h blocks minus instrument lines == c19 blocks | byte-identical across all 26 stages | PASS |
| K6 | 3/3 byte-identical per binary; stderr empty | sha256 c19 c72aa165... x3, c19h 91693144... x3; .err 0 bytes x6 | PASS |
| K7 | setup blocks byte-identical to c17_run1.txt's | 6/6 identical | PASS |
| K8 | safebin, no python, pinned znc, neg-conj clean, provenance diffs exact | all verified; c19h strat diff = exactly the 2 det_ev lines | PASS |
| K9 | 26 Q lines match c19_stages_predicted.txt | 26/26 match (id, tag, how) | PASS |

## What this establishes (and does not)

Establishes: on a diverse battery (7 world kinds:
PW-winnable, NEED-winnable, WHOLE-winnable, unwinnable; 4
contexts; 22 eligible selections), the hedge's exact-tie
firing condition arose 0 times. Combined with the two
prior pricings (c16/c17: 1 firing, pure cost; c18: 1
firing, engineered benefit), the lifetime record is now 2
firings total, 0 of them natural. The selection dynamics
actively suppress ties (rich-get-richer score
separation), so the hedge is not merely rarely-triggered
by chance; the mechanism's own learning dynamics move
scores away from exact equality.

Does not establish: that ties NEVER occur naturally (0/22
bounds the rate, it does not prove impossibility; a
battery with leadership transitions might produce one);
the keep/delete decision itself (Micah's call, governance
#11); that the 7 world kinds represent natural operation
in general.

## Governance input for Micah (item #11)

Base-rate evidence now exists on both sides of the ledger:
- KEEP side: the hedge has ONE priced benefit (c18
  engineered tie: saves 2 events + 2 rescue observations
  when PW/NEED tie exactly and NEED is the eventual
  winner).
- DELETE side: the firing condition occurred 0/22 times
  naturally, and the learner's score dynamics are
  anti-tie (leaders extend leads; no transitions in 22
  selections). The c16/c17 battery's single firing was
  pure cost.
The hedge is therefore a mechanism that is pure cost in
one battery, beneficial on one engineered tie, and
inert (0/22) across a diverse natural battery. Whether
that option value justifies keeping it is the design
call.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin;
`which python3` / `which python` return nothing before and
after; verified this session). Pinned znc
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
for all three builds (c19, c19h, c19pos). All computation
pure Zag; shell only for znc/binary/git/assembly/byte
verification. Zero forbidden-executable invocations. New
Zag (world-add file, driver, 2-line strat instrumentation)
scanned for the `while.*!(` negated-conjunction pattern:
clean; no deep nesting. Git writes via /usr/bin/git
absolute path, explicit pathspecs, current branch
(`tnn-native-lab`) only, nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_hedge_frequency/`:
PREREG.md (frozen, commit ee97f04d6), NAMECHECK.md (Step 0),
c19_stages_predicted.txt (frozen; K9 verified 26/26),
c19_base.zag (cmp-identical to c18_base.zag),
c19_world_add.zag (setup_worldF_plus + 7-kind mk_goalX),
c19_strat_additive.zag (cmp-identical to
c18_strat_additive.zag), c19h_strat_additive.zag
(c18h + exactly 2 det_ev instrumentation lines,
diff-verified), c19_main.zag (c18_main helpers + new
26-stage main + kind 10/11 dump branches), c19_build.sh,
c19_full.zag / c19h_full.zag (assembled; one `fn main`
each), c19_bin / c19h_bin, c19_compile.txt /
c19h_compile.txt, c19_run1/2/3.txt (sha256
c72aa165522f7e0c5877eec5cd141a9be6e9425e7e0950c65eeff445d38fb903
x3) + .err (empty), c19h_run1/2/3.txt (sha256
91693144f8669cc2b087b35766f0320a1c027a92ccf5dccfc736e6aae97ad3a6
x3) + .err (empty), c19pos_main.zag / c19pos_full.zag /
c19pos_bin / c19pos_run1.txt (positive control:
instrumented strat on the c18 alternation battery;
S_TEST DET-HEDGE before=1 dt1=0 dt3=0 ev=2004,
stripped output byte-identical to c18h_run1.txt),
REPORT.md (this file).
