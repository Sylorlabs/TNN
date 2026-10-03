# PREREG: H-INTENT-UNIFIED8 Red Team (IU8-ADV) (FROZEN)

## Target claim under test

H-INTENT-UNIFIED8 SURVIVES (9/9): R10, an all-pairs both-verbatim
guard in `intent_winner`, closes the B1 rank-hidden verbatim
dissenter hole. For every unordered candidate pair (a,b) with
em==1 on both sides, kind-dispatched answers are compared over
qlen bytes; any disagreement emits
`INTENT VERBATIM-CONFLICT: verbatim candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
and returns kind=-2. Frozen precedence: IU3 top-two verbatim,
IU4/IU5 top-two truncated, R8 all-pairs both-truncated, R9
all-pairs verbatim-vs-truncated, then R10, then the gap==0 tie
check last. Pair-class exclusivity: R8 = em=0 both sides, R9 =
em=1 on exactly one side with the em=0 side truncated, R10 = em=1
on both sides.

Score model (read from the committed source): qscore =
em*40000 + cf*20000 + lm*10000. Proc candidates always cf=0.
`intent_exact_match` checks only the first 16 recorded inputs;
o+8 holds TRUE npairs; truncated = (TRUE npairs > 16).

## Adversary stance

Assume the R10 claim is false. Attack the dimensions the builder
did not test: rank 5+ dissenters, mixed bridge/proc verbatim
pairs (the kind-dispatch in R10's new code), the R10-vs-gap==0
precedence interaction, and truncated members of the
both-verbatim pair class (em=1 AND truncated).

## Frozen attacks

Setup-validity rule (frozen): every X-IU8 bar first checks its
learn preconditions via the `iu8_show` helper (prints kind, slot,
em, true npairs, applied answer). If any learn fails (rc<0), or
any candidate is not of the required kind, or em/answer differs
from the frozen expectation, the bar reports SETUP-FAIL: no
conclusion, NOT counted as a pass. Post-hoc fixture tuning is
forbidden. Diagnostic counting is scoped to lines after the
`--- decide ---` marker inside each attack section (learn-phase
emissions such as the INTENT WARN cap notice are out of scope).

Exact diagnostic texts:
- R10-NEW: `INTENT VERBATIM-CONFLICT: verbatim candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
- IU3-OLD: `INTENT VERBATIM-CONFLICT: top two candidates both have exact_match=1 but disagree; WITHHOLD AMBIGUOUS`
- IU4A: `INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`
- IU4B: `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS`
- R8: `INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
- R9: `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer beyond top two; WITHHOLD AMBIGUOUS`

### X-IU8-1: rank-5+ dissenter with multi-class bystanders

Fresh W. Learn order (query `xab`, qlen=3):
- V1 proc: `xab>xxx;xbc>xxx;xde>xxx`
  (constant-0; em=1, lm=1; expected score 50000, answer `xxx`)
- V2 proc: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (constant-0; em=1, lm=0; expected score 40000, answer `xxx`)
- V3 proc: `xab>xxx;xbcd>xxx;xdef>xxx;xfgh>xxx`
  (constant-0; em=1, lm=0; expected score 40000, answer `xxx`)
- V4 proc: `xab>xxx;xbcd>xxx`
  (constant-0; em=1, lm=0; expected score 40000, answer `xxx`)
- T5 proc: `xbc>xxx;xde>xxx;xfg>xxx;xhi>xxx;xjk>xxx`
  (constant-0; xab NOT recorded so em=0; npairs=5, not truncated;
  lm=1; expected score 10000, answer `xxx`)
- V6 proc: `xab>bax;abcd>dcba`
  (reverse program; em=1, lm=0; expected score 40000, answer `bax`)

Expected arrangement: top=V1 (50000), second=V2 (40000), then
V3, V4, V6 at 40000 in learn order, T5 (10000) last. The
dissenter V6 sits beyond every rank the builder tested, with an
em=0 non-truncated bystander present.

Why this attacks: R8 needs two em=0 candidates (only one
exists); R9 needs the em=0 side truncated (T5 is not); so only
R10 may fire, on the (V1..V4, V6) verbatim pairs.

PASS iff: kind=-2 AND the decide section contains R10-NEW
exactly once AND none of IU3-OLD, IU4A, IU4B, R8, R9 appears in
the decide section.
KILL iff: kind>=0 (silent resolution at rank 5+), or any panic.
DOWNGRADE iff: kind=-2 but a different guard's text fires, or
R10-NEW is absent.

### X-IU8-2: mixed bridge/proc verbatim dissenter

Fresh W. Learn order (query `xab`):
- V1 proc: `xab>xxx;xbc>xxx;xde>xxx`
  (expected score 50000, answer `xxx`, em=1)
- V2 proc: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (expected score 40000, answer `xxx`, em=1)
- B bridge: `aab>baa;abb>bba;xab>xab;xcd>xcd;xabcd>xabcd`
  No single program fits all five pairs (aab needs out[0]=inp[1],
  xab needs out[0]=inp[0]), so direct discovery fails; the
  (pos,val) split at input[0]=='a' separates {aab,abb} (reverse)
  from {xab,xcd,xabcd} (identity), so bridge induction must yield
  rc>=1000 with IF input[0]=='a' THEN reverse ELSE identity.
  xab is recorded, so em=1. Mixed input lengths give tlen=-1,
  lm=0; query xab has input[0]='x' so cf=0; expected score 40000.
  bridge_apply on xab takes the ELSE branch (identity), so the
  applied answer is `xab`, which differs from `xxx`.

Why this attacks: the builder's K-IU8-1a/1b used proc-only
pairs. R10's new code kind-dispatches per candidate
(proc_apply vs bridge_apply). A dispatch or argument-order bug
would break exactly this mixed pair while proc/proc pairs pass.

PASS iff: kind=-2 AND the decide section contains R10-NEW
exactly once AND none of IU3-OLD, IU4A, IU4B, R8, R9 appears.
Preconditions (else SETUP-FAIL): rc>=1000 for B (kind=1), em=1
for all three, applied answers `xxx`, `xxx`, `xab`.
KILL iff: kind>=0 (mixed-kind verbatim disagreement silently
resolved), or any panic.
DOWNGRADE iff: kind=-2 but a different guard's text fires, or
R10-NEW is absent.

### X-IU8-3: gap==0 top tie with a rank-3 dissenter

Fresh W. Learn order (query `xab`):
- V1 proc: `xab>xxx;xbc>xxx`
  (constant-0; em=1, lm=1; expected score 50000, answer `xxx`)
- V2 proc: `xab>xxx;xde>xxx`
  (constant-0; em=1, lm=1; expected score 50000, answer `xxx`)
- V3 proc: `xab>bax;abcd>dcba`
  (reverse; em=1, lm=0; expected score 40000, answer `bax`)

Expected arrangement: top=V1, second=V2, gap=0 (tie, V1 learned
first so strict selection keeps it top). V3 ranked third.

Why this attacks: the frozen precedence puts R10 fifth and the
gap==0 tie check last, but the builder never tested a live
gap==0 alongside a rank-3+ dissenter. If the tie check fires
instead of R10, the withhold is silent (the gap==0 branch emits
no diagnostic) and the frozen precedence is violated.

PASS iff: kind=-2 AND the decide section contains R10-NEW
exactly once AND none of IU3-OLD, IU4A, IU4B, R8, R9 appears.
KILL iff: kind>=0, or any panic.
DOWNGRADE iff: kind=-2 with NO diagnostic at all in the decide
section (gap==0 fired instead of R10: safety held, precedence
and diagnostic precision broken), or kind=-2 with a different
guard's text.

### X-IU8-4: truncated-verbatim dissenter (pair-class exclusivity)

Fresh W. Learn order (query `xab`):
- V1 proc: `xab>xxx;xbc>xxx;xde>xxx`
  (expected score 50000, answer `xxx`, em=1)
- V2 proc: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (expected score 40000, answer `xxx`, em=1)
- V3 proc, 18 pairs, `xab` FIRST (so it falls inside the 16-cap
  and em=1):
  `xab>bax;abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;abcde>edcba;vwxyz>zyxwv`
  (reverse program fits all 18; TRUE npairs=18 > 16 so
  truncated; em=1 because xab is recorded first; mixed lengths
  so lm=0; expected score 40000, answer `bax`)

Why this attacks: V3 is BOTH em=1 AND truncated. Pair-class
exclusivity says the (V1,V3) and (V2,V3) pairs belong to R10
(em=1 on both sides), not to R8 (needs em=0 both) or R9 (needs
em=1 on exactly one side). The builder never tested a truncated
member of the both-verbatim class. If R10's em==1 criterion
misfires on truncated records, or R9/R8 wrongly claim the pair,
the diagnostic or the verdict breaks.

PASS iff: kind=-2 AND the decide section contains R10-NEW
exactly once AND none of IU3-OLD, IU4A, IU4B, R8, R9 appears.
Preconditions (else SETUP-FAIL): em=1 for all three, TRUE npairs
of V3 = 18 (truncated), applied answers `xxx`, `xxx`, `bax`.
KILL iff: kind>=0, or any panic.
DOWNGRADE iff: kind=-2 but R8, R9, or an older guard's text
fires instead of R10-NEW.

### X-IU8-5: regression (production mains byte-identical)

Extract the COMMITTED `unified_learn.zag` and `intent_learn.zag`
at the H-INTENT-UNIFIED8 result commit, compile each main once
to /tmp with the pinned toolchain, run each binary 3 times
directly. PASS iff unified output md5 =
904de9f83a2873c7a8862b71804a9065 and intent output md5 =
98315faec8faea24e75533892c0b240d on all runs (the frozen IU7
hashes the builder reproduced). KILL iff any md5 differs or
runs are not byte-identical (silent behavior change).

## Frozen verdict rules

- Any KILL trigger: H-INTENT-UNIFIED8 is KILLED.
- Any DOWNGRADE trigger (no KILL): H-INTENT-UNIFIED8 is
  DOWNGRADED (survives with a named precedence/diagnostic
  defect).
- All five PASS with no SETUP-FAIL: H-INTENT-UNIFIED8 SURVIVES
  the red team.
- SETUP-FAIL on a bar: reported as no-conclusion for that bar,
  never as a pass; a second distinct fixture is forbidden
  (no post-hoc tuning).

## Frozen methodology

1. This prereg committed alone before any adversary harness
   build, compile, or run. Commit order verified by
   `git merge-base --is-ancestor`.
2. Adversary harness `iu8_adv.zag` = mechanism region of the
   COMMITTED `unified_learn.zag` (lines 1-1579, everything
   before `fn main`), extracted via `git show` at the IU8
   result commit, cmp-verified byte-identical against the
   working tree; plus t_learn, t_decide, iu4_init, iu8_show
   carried verbatim from the committed `iu8_verify.zag`;
   plus a new X-IU8-1..5 attack main. No mechanism byte
   altered.
3. Evidence method: compile once to /tmp with the pinned
   toolchain (binaries never committed); execute the binary
   directly 3 times for clean raws (exit 0, zero stderr).
   Raw evidence: IU8_ADV_RAW.txt (md5 recorded, 3/3
   byte-identical via cmp).
4. Pure Zag throughout: prereg, harness, builds, runs, greps,
   md5, cmp. No Python at any stage.
5. Toolchain: znc 2026.07.0-dev (edition 2026), pinned at
   /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc.
6. Only researcher-owned paths staged (pathspec-restricted).
   Concurrent workers' files untouched.
7. No em dashes in loop documentation (byte-verified).
