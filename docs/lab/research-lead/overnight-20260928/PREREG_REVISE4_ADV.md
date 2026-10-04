# Preregistration: H-REVISE4 Red Team (Adversary)

**Date:** 2026-09-29
**Adversary:** H-REVISE4 Red Team (subagent)
**Status:** FROZEN (committed before any attack implementation or execution)
**Branch:** tnn-native-lab
**Target:** H-REVISE4 SURVIVES (52/52), REVISE4_RESULT.md, revise4.zag

## Mission

Assume the H-REVISE4 repair claim is false. Attack the two repairs:
R1 (tie-aware diagnosis with AMBIGUOUS withhold) and R2 (explicit
VS3FULL capacity policy). Four preregistered attacks below.

## Structural observation guiding the attacks

In `diagnose_scored`, the two score components are provably the same
signal when the extraction sequence comes from `pextract(fail,
fail_out)` (as in every harness call site). `pextract` sets
`seq[k]` to the unique input position `j` with `inp[j]==out[k]`.
Hence for candidate `(p, v=fail[p])`: `p` appears in `seq` if and
only if `v` appears in `fail_out`. The two "+1" terms are perfectly
correlated: every discriminating candidate scores 0 or 2, never 1.
The "two signals" (output-relevance, program-consistency) are one
signal counted twice. Consequence: the R1 repair only withholds on
exact ties; a unique incidental scoring 2 while the causal scores 0
sails through and appends a wrong revision with full confidence.

## Attack X-RV4-1: unique wrong top (evades the tie protection)

Fixture. Hidden truth: IF input[2]=='y' (121) THEN broadcast-first
ELSE broadcast-last (P0). Passing set: "abc"->"ccc", "def"->"fff",
"ghi"->"iii", "jkl"->"lll" (P0 examples). Counterexample:
fail="zqy", fail_out="zzz" (truth: input[2]=='y', so broadcast-first;
P0 predicts "yyy").

Expected mechanism trace (computed by hand from the source):
`pextract("zqy","zzz")` gives seq=[0,0,0] ('z' unique in input at
position 0), sl=3. Candidates: (0,'z'=122): discriminating (pos0 of
passing is a,d,g,j); 'z' in "zzz" (+1); 0 in seq (+1); score 2.
(1,'q'=113): discriminating; score 0. (2,'y'=121, the causal):
discriminating; 'y' not in "zzz"; 2 not in seq; score 0. Unique top
(0,122). best_count=1, so NO AMBIGUOUS. The caller appends revision
IF input[0]=='z' THEN P1 ELSE P0. vcount becomes 1.

Held-out (against the hidden truth): ("aqy"->"aaa") [input[2]=='y',
truth gives broadcast-first "aaa"; mechanism: slot1 (0,122) misses
('a'!=122), falls to P0, predicts "yyy"] must FAIL. ("zqw"->"www")
[input[2]=='w', truth gives broadcast-last "www"; mechanism: slot1
(0,122) fires ('z'==122), P1=broadcast-first predicts "zzz"] must
FAIL.

Kill criterion: diagnosis returns a unique top (dr >= 0) that is NOT
the causal (2,121); a revision is appended (vcount=1); at least one
held-out test fails. If all three hold, H-REVISE4 is DOWNGRADED: the
R1 tie protection does not cover confident unique misattribution,
and the scored heuristic is not a causal identifier. If the diagnosis
returns -2 (AMBIGUOUS) or the causal (2,121), the attack FAILS.

## Attack X-RV4-2: AMBIGUOUS liveness (does the withhold strand a
legitimate revision?)

Fixture: the Phase J / X-RV3-1 fixture (hidden truth (2,121),
counterexample ("xqy"->"xqy")). Call `diagnose_scored` exactly as
Phase J does. Then demonstrate there is no recovery path: a second
call on the same input still returns -2; the API accepts only a
single (fail, fail_out) pair, so no second counterexample can be fed
to break the tie; the legitimate revision (2,121) can never be
installed through the diagnosis path.

Kill criterion: this attack is preregistered as a BOUNDARY
demonstration, not a kill path. Withholding on a true tie is the
documented honest behavior ("does not resolve it"). It becomes a
DOWNGRADE only if a recovery path exists inside the mechanism's own
vocabulary and was missed (then the withhold would be gratuitous).
Expected outcome: BOUNDARY (liveness cost of honest withholding;
indistinguishable ties permanently strand the revision).

## Attack X-RV4-3: capacity wall at 4 for a continuing learner

Five sequential genuine revisions, each diagnosed from a real
counterexample with a unique top, each verified on held-out, chained
in one store. P0 = broadcast-last (hand-set, as in Phase J). Passing
D = "abc","def","ghi","jkl".

- R1: ("xab"->"xxx") -> unique (0,120). P1=broadcast-first.
- R2: ("ayz"->"yyy") -> unique (1,121). Counterexample under slot1
  ('a'!=120, P0 gives "zzz"). P1=broadcast-first.
- R3: ("zbq"->"zzz") -> unique (0,122). Counterexample under
  slots 1-2 ('b'!=121, 'z'!=120, P0 gives "qqq"). P1=broadcast-first.
- R4: ("mnp"->"mmm") -> unique (0,109). Counterexample under slots
  1-3 (P0 gives "ppp"). P1=broadcast-first. vcount=4.
- R5: ("qrs"->"qqq") -> diagnosis WOULD be unique (0,113), but
  `vs3_revise` must refuse: VS3FULL warning, rc=-1, vcount stays 4.

Each of R1..R4 is verified on at least one held-out input that the
accumulated store must get right. R5's query ("qrs") falls through
to P0 and gives "sss" instead of "qqq": the correction is
permanently unrepresentable.

Kill criterion: preregistered as BOUNDARY, not a kill path. The R2
repair claims explicit refusal, never silent drop; the attack
succeeds as a demonstration iff R5 is refused explicitly (warning
emitted, rc=-1, vcount=4, earlier revisions intact) AND the R5
condition is genuinely legitimate (unique diagnosis, real
counterexample). It becomes a DOWNGRADE/KILL only if R5 is silent,
corrupts earlier revisions, or crashes. Expected outcome: BOUNDARY
with teeth: the disclosed 4-slot cap bounds the chained-revision
claim, and a continuing learner needing a 5th genuine revision gets
an explicit refusal plus a permanently wrong answer on that
condition.

## Attack X-RV4-4: source audit (tie detection, VS3FULL, no
hardcoding, score degeneracy)

Static audit of revise4.zag lines 1-421 plus dynamic confirmation:
(a) tie logic: best_count resets to 1 on strict improvement and
increments on equality; -2 returned iff best_count>1 at end; (b)
VS3FULL: vc>=4 is the only full path, emits warning, returns -1,
callers handle -1; (c) no byte-value literals in the diagnosis or
revision paths (all compared values come from data); (d) confirm
the score degeneracy (every candidate scores 0 or 2) on the attack
fixtures by inspecting the emitted DIAGNOSE candidate lines.

Kill criterion: DOWNGRADE if any hardcoding of test answers,
literal byte constants steering diagnosis, or a tie-counting bug is
found. PASS otherwise, with the degeneracy recorded as a finding
that narrows the "scored heuristic" description.

## What is NOT in scope

The frozen K-RV4-1..K-RV4-4 bars are not re-litigated; a red-team
DOWNGRADE narrows the repair claims, it does not retroactively alter
frozen bars. Pure Zag only: no Python anywhere, including
generators, verifiers, analysis, and scratch work. Mechanism code
(lines 1-421 of revise4.zag) is copied byte-verbatim into the attack
harness; only main() is replaced. Three consecutive runs must be
byte-identical (cmp). No em dashes in any document.

## Verdict mapping

- X-RV4-1 success -> H-REVISE4 DOWNGRADED (R1 incomplete: unique
  wrong tops evade the tie protection).
- X-RV4-2 -> expected BOUNDARY (permanent withhold on true ties).
- X-RV4-3 -> expected BOUNDARY (4-slot wall demonstrated; refusal
  explicit as repaired).
- X-RV4-4 -> PASS with findings, unless hardcoding/bug found.
