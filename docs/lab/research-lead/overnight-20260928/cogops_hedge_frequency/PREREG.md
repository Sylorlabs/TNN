# PREREG: COGOPS-HEDGE-FREQUENCY (natural hedge firing frequency)

Date: 2026-10-03. Worker: COGOPS-HEDGE-FREQUENCY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_hedge_frequency/`
Status: FROZEN on commit (this file + NAMECHECK.md +
c19_stages_predicted.txt committed alone before any
implementation file exists). No amendments after
implementation begins. Commit hash recorded in REPORT.md.

Non-ledger task (claim minting paused). Implements the
COGOPS-ALTERNATION-WORLD follow-up: "a natural-tie frequency
study would say how often the hedge's firing condition arises
unengineered" (REPORT.md recommended follow-up #2).

## 1. Research question

COGOPS-HEDGEREMOVAL priced the hedge as pure cost in the
c16/c17 battery (fires once, S8, buys nothing).
COGOPS-ALTERNATION-WORLD priced it as beneficial on an
engineered exact PW/NEED tie (6 vs 8 events, 0 vs 2 rescue
observations). The honest boundary of both: nobody knows the
BASE RATE. The hedge's firing condition is a conjunction:

  (a) initial selection (tried==0),
  (b) argmin best != 0,
  (c) in-context evidence for both PW and NEED (c1>0, c3>0),
  (d) exact integer tie: n1*(bu+2)==bn*(u1+2) AND
      n3*(bu+2)==bn*(u3+2), where (bu,bn) is the argmin
      best's (u,N) and n1/n3 are PW's/NEED's N scores.

Condition (d) is exact rational equality of learned scores.
The engineered tie satisfied it via ra==2*rb ledger
arithmetic. This worker measures, on diverse worlds NOT
engineered for ties: how often does the hedge fire per
eligible selection (conditions a-c hold), and when it fires,
does it save or waste events vs the no-hedge control?

## 2. Design

### 2.1 Binaries (two, one mechanism delta + instrumentation)

- c19 (no hedge): c18's strat_sel verbatim (hedge deleted),
  NO instrumentation. The control.
- c19h (with hedge): c18h's strat_sel (hedge present) PLUS
  exactly two added det_ev log lines (instrumentation only,
  behavior-neutral; K5 verifies):
  - kind 11 DET-HGATE, emitted at every initial selection
    (tried==0, best!=0): `DET-HGATE best=<x> c1=<y> c3=<z>`.
    Eligible selections are those with c1>0 AND c3>0.
  - kind 10 DET-HEDGE, emitted iff the hedge fires
    (r1==1 && r3==1, immediately before best=4):
    `DET-HEDGE before=<p> dt1=<x> dt3=<y> ev=<z>`
    with dt1 = n1*(bu+2)-bn*(u1+2), dt3 =
    n3*(bu+2)-bn*(u3+2), ev = c1*1000+c3.
    A genuine firing has dt1==0, dt3==0, ev>=1001 (K2).

Both binaries share: c18_base.zag (copied verbatim),
c18_world.zag (used verbatim), c19_world_add.zag (new
constructors + world augmentation, world file only),
the frozen c12 learn prefix (lines 1..1331), and one driver
c19_main.zag. The ONLY source delta between the binaries is
the strat additive section (hedge block + 2 log lines vs no
hedge, no log lines).

### 2.2 Worlds (world F base + 615/616 augmentation)

All detection goals run in world F (setup_worldF at S6B,
unchanged). Before the first period-3 stage, the driver
silently calls setup_worldF_plus(A) = setup_worldF(A) plus
the 7 rel-615/616 facts from setup_worldE (77+7=84 facts,
capacity 128). The call prints nothing; the stage block is
unaffected.

Seven world kinds via one constructor mk_goalX(G,tag,kind):

- kind 1 (P3): 830 structure (3 needs, pure lag-2
  oscillation). Context (3,613). PW-winnable.
- kind 2 (N3): need0 P=(601,621); need1 P=(613,770)
  kind-1 SELF-link (771<->772); need2 P=(604,611) kind-1
  SELF-link (612->..->618 drifter). Context (3,613).
  Whole state never repeats within the episode; needs 0,1
  match at lag 2 -> NEED-winnable. PW fails, WHOLE fails.
- kind 3 (P4): kind 1 plus need3 P=(604,611) with NO
  self-link (constant [612] each pass). Context (4,613).
  PW-winnable.
- kind 4 (N4): 831 structure (kind 1 + 604 drifter as
  need3). Context (4,613). NEED-winnable.
- kind 5 (P3E): 821 structure (615 3-cycle self-link +
  616 verify fan-out). Context (3,615). PW fails;
  WHOLE wins at lag 3.
- kind 6 (D3E): need0 carrier; need1 615 3-cycle
  self-link; need2 604 drifter self-link. Context
  (3,615). Whole state never repeats (drifter); no
  per-need lag-2 match -> all four strategies fail ->
  generic fallback (how=0).
- kind 7 (DR3): 816 structure (604 drifter + 605 verify
  fan-out). Context (3,604). All strategies fail ->
  generic fallback (how=0).

Nothing about these worlds targets the tie arithmetic; the
mix is chosen for strategy-evidence diversity (PW-winnable,
NEED-winnable, WHOLE-winnable, unwinnable) across 4
contexts.

### 2.3 Battery (26 detection stages, fresh tags)

Setup stages S1A/S1B/S2/S4/S6L/S6B copied verbatim from
c18_main.zag (K7: blocks byte-identical to c17_run1.txt's).

Detection stages (stage id, goal tag, kind, predicted how):

```
F01 840 k2 how=1    F02 841 k1 how=1    F03 842 k2 how=1
F04 843 k1 how=1    F05 844 k2 how=1    F06 845 k1 how=1
F07 846 k2 how=1    F08 847 k1 how=1    (context (3,613))
F09 850 k4 how=1    F10 851 k3 how=1    F11 852 k4 how=1
F12 853 k3 how=1    F13 854 k4 how=1    F14 855 k3 how=1
F15 856 k4 how=1    F16 857 k3 how=1    (context (4,613))
F17 860 k6 how=0    F18 861 k5 how=1    F19 862 k6 how=0
F20 863 k5 how=1    F21 864 k5 how=1    F22 865 k6 how=0
                                         (context (3,615))
F23 870 k7 how=0    F24 871 k7 how=0    F25 872 k7 how=0
F26 873 k7 how=0                         (context (3,604))
```

setup_worldF_plus(A) is called silently just before F17's
STAGE line. After every detection stage the driver calls
plan_drop(L, g_tag(G)) (harness operation; the plan region
holds 4 slots and tags are fresh, so without drops
plan_new would return -1 and stages would decline).

Predicted eligibility (DET-HGATE c1>0 AND c3>0): every
stage EXCEPT the first in each context (F01, F09, F17,
F23), because each context's first stage tries both PW
(cold-context id-lead) and NEED (cascade reaches it:
N3/N4 win; D3E/DR3 fail after trying all). Predicted
eligible = 22 of 26.

### 2.4 Frozen structural predictions

- The 26 Q lines appear in the exact id/tag/how order of
  2.3 (K9). (passes values and DET contents are the
  measurement, not frozen.)
- #DET-HGATE == #DET-STRAT == 26 (K1).
- Eligible (c1>0 && c3>0) == 22: all but F01/F09/F17/F23
  (K3 denominator).
- DET-HGATE format `DET-HGATE best=<b> c1=<c1> c3=<c3>`;
  DET-HEDGE format
  `DET-HEDGE before=<b> dt1=<d1> dt3=<d3> ev=<e>` (K1/K2).
- S1A/S1B/S2/S4/S6L/S6B blocks byte-identical to
  c17_run1.txt's (K7).

Full-stdout byte prediction is NOT frozen (unlike c18):
the 26-stage battery's table/ledger dynamics are the
object of measurement, not hand-simulable at reasonable
cost. K1/K2/K5/K6/K7 provide the integrity checks that
K8 provided in c18.

## 3. Kill bars (frozen)

- K1 (instrument integrity): #DET-HGATE lines == 26 ==
  #DET-STRAT lines in c19h runs; every DET-HEDGE line's
  `before` equals its stage block's DET-HGATE `best`.
  FAIL: any count mismatch, or before != best.
- K2 (genuine ties only): every DET-HEDGE line satisfies
  dt1==0 AND dt3==0 AND ev>=1001. FAIL: any violation.
  (A violation means the instrument reports a firing that
  was not an exact PW/NEED score tie with in-context
  evidence.)
- K3 (natural firing frequency; verdict-branching):
  eligible = DET-HGATE lines with c1>0 AND c3>0
  (predicted 22); fires = #DET-HEDGE lines;
  frequency = fires/eligible. FAIL the denominator
  prediction if eligible != 22. Interpretation branches:
  fires==0 -> the exact-tie condition is measure-zero in
  this diverse battery (DELETE-leaning); 1-2 fires
  (<10%) -> rare but nonzero (DELETE-leaning);
  >=3 fires (>=13.6%) -> material base rate
  (KEEP-leaning). The bar kills the "fires commonly"
  hypothesis if frequency < 10%, and kills the "never
  fires naturally" hypothesis if fires >= 1.
- K4 (help/hurt on natural firings; verdict-branching,
  applies iff fires >= 1; recorded N/A if fires==0):
  events per stage = #DET-CMP + #DET-NCMP lines in the
  stage block. For each fired stage: saved =
  events_c19 - events_c19h. net = sum(saved).
  Branches: net > 0 -> hedge net-beneficial on natural
  firings (KEEP-leaning); net == 0 -> neutral;
  net < 0 -> net-costly (DELETE-leaning). Per-stage
  saved/wasted and win status reported. FAIL
  (measurement integrity): any fired stage's block
  missing or unparseable in either binary.
- K5 (control purity): for every NON-fired stage, the
  c19h stage block with DET-HGATE/DET-HEDGE lines removed
  is byte-identical to the c19 stage block. FAIL:
  any other line differs. (Proves the instrumentation is
  behavior-neutral and the hedge is the only mechanism
  delta.)
- K6 (determinism): 3/3 runs byte-identical per binary
  (sha256 recorded); stderr empty for all 6 runs. FAIL
  otherwise.
- K7 (setup invariance): S1A/S1B/S2/S4/S6L/S6B blocks
  byte-identical to c17_run1.txt's corresponding blocks.
  FAIL otherwise.
- K8 (toolchain & provenance): safebin active for every
  command; `which python3`/`which python` return nothing;
  all computation pure Zag; pinned znc only; new Zag
  scanned for the `while.*!(` negated-conjunction
  pattern (must be clean) and deep nesting (none);
  c19_base.zag cmp-identical to c18_base.zag;
  c18_world.zag used verbatim (no edits); new world code
  ONLY in c19_world_add.zag; learn prefix lines 1..1331
  cmp-identical to c12_learn.zag lines 1..1331;
  c19_strat_additive.zag cmp-identical to
  c18_strat_additive.zag; c19h_strat_additive.zag diff vs
  c18h_strat_additive.zag is exactly the 2 added det_ev
  lines; zero world/goal/relation/need literals in either
  strat additive section. FAIL otherwise.
- K9 (frozen Q-sequence): the 26 Q lines match
  c19_stages_predicted.txt (id, goal tag, how) in order.
  FAIL otherwise.

## 4. What this establishes (and does not)

Establishes (if bars pass): the base rate of the hedge's
firing condition across 22 eligible selections on 7
non-engineered world kinds in 4 contexts, with each
firing verified as an exact tie (K2), and the
events-saved/wasted balance of natural firings vs the
no-hedge control (K4). This is the base-rate input to
Micah's keep/delete decision (governance item #11).

Does not establish: whether 7 world kinds and 4 contexts
represent "natural" operation in general (the battery is
diverse but still harness-built); the keep/delete decision
itself (Micah's call); L3 invention; a learner-owned hedge
policy.
