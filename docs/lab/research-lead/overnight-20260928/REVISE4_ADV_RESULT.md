# H-REVISE4 Red Team: Adversary Result

**Date:** 2026-09-29
**Adversary:** H-REVISE4 Red Team (subagent)
**Branch:** tnn-native-lab
**Target:** H-REVISE4 SURVIVES (52/52), REVISE4_RESULT.md, revise4.zag
**Prereg:** PREREG_REVISE4_ADV.md (4021d99eb, frozen before any attack
implementation or execution)
**Attack implementation:** revise4_adv.zag (mechanism lines 1-421
byte-identical to revise4.zag; only main() replaced)
**Raw output:** REVISE4_ADV_RAW.txt (md5 46e012c87d74f8b35472ed5bb9acbf56,
byte-identical across 3 runs, verified with cmp)
**Toolchain:** znc 2026.07.0-dev (edition 2026)

## Verdict

**H-REVISE4 DOWNGRADED.** Attack X-RV4-1 succeeds: the R1 tie
protection is evaded by a unique wrong top, and the mechanism appends
a confident wrong revision. Attacks X-RV4-2 and X-RV4-3 behave exactly
as preregistered and are classified BOUNDARY. Attack X-RV4-4 (source
audit) PASSES with two substantive findings. The frozen K-RV4-1
through K-RV4-4 bars are NOT re-litigated and still hold; this
downgrade narrows the R1 repair claim, it does not retroactively alter
any frozen bar.

## Structural finding (guides X-RV4-1)

In `diagnose_scored`, the two score components are provably the same
signal whenever the extraction sequence comes from
`pextract(fail, fail_out)`, which holds at every harness call site.
`pextract` sets `seq[k]` to the unique input position `j` with
`inp[j] == out[k]` (returning -1 unless each output byte appears
exactly once in the input). For candidate `(p, v)` with `v = fail[p]`:

- `p` appears in `seq` iff some `k` has `seq[k] == p`, i.e.
  `out[k] == inp[p]`, i.e. `v` appears in `fail_out`.

So output-relevance (+1) and program-consistency (+1) are perfectly
correlated. Every discriminating candidate scores 0 or 2, never 1.
The "scored heuristic" is a single binary signal counted twice.
Empirical confirmation: across all fixtures in REVISE4_ADV_RAW.txt,
every emitted `DIAGNOSE candidate` line shows `score=2` or `score=0`;
zero lines show `score=1`. Consequence: the R1 repair withholds only
on exact ties. A unique incidental scoring 2 while the causal scores
0 sails through with full confidence.

## X-RV4-1: unique wrong top (SUCCESS, kill criterion met)

Fixture. Hidden truth: IF input[2]=='y' (121) THEN broadcast-first
ELSE broadcast-last (P0). Passing set "abc", "def", "ghi", "jkl".
Counterexample ("zqy"->"zzz"): truth gives broadcast-first ("zzz"
since input[2]=='y'); P0 predicts "yyy".

Mechanism trace (from REVISE4_ADV_RAW.txt):
`pextract("zqy","zzz")` yields seq=[0,0,0], sl=3 ('z' is unique in the
input at position 0). Diagnosis emits:

- candidate pos=0 val=122 score=2 (incidental 'z': in output, pos 0
  in seq)
- candidate pos=1 val=113 score=0
- candidate pos=2 val=121 score=0 (the causal 'y': not in output,
  pos 2 not in seq)

Unique top (0,122). best_count=1, so NO AMBIGUOUS is emitted. The
caller appends revision IF input[0]=='z' THEN P1 ELSE P0; vcount
becomes 1. The causal feature (2,121) is never selected.

Held-out against the hidden truth, both FAIL as preregistered:

- ("aqy"->"aaa"): truth gives broadcast-first "aaa" (input[2]=='y').
  Mechanism: slot1 (0,122) misses ('a' != 122), falls to P0,
  predicts "yyy". FAIL.
- ("zqw"->"www"): truth gives broadcast-last "www"
  (input[2]=='w'). Mechanism: slot1 (0,122) fires ('z' == 122),
  P1=broadcast-first predicts "zzz". FAIL.

Kill criterion (preregistered): diagnosis returns a unique top that
is not the causal (2,121); a revision is appended; at least one
held-out fails. All three hold: 7/7 X1 checks behaved as predicted.

Interpretation: X-RV3-1 (the H-REVISE3 downgrade) showed the heuristic
guessing wrong on a tie; R1 repaired ties by withholding. X-RV4-1
shows the same misattribution succeeding without any tie. The
heuristic does not identify the causal feature; it identifies "the
discriminating byte that appears in the expected output", which is the
causal byte only when the true output happens to contain it. The R1
repair narrows the failure mode but does not remove it. This is a
DOWNGRADE of the R1 claim, not a kill: the exact-tie fixture still
withholds correctly per K-RV4-1.

## X-RV4-2: AMBIGUOUS liveness (BOUNDARY, as preregistered)

On the Phase J / X-RV3-1 fixture (hidden truth (2,121),
counterexample ("xqy"->"xqy")): `diagnose_scored` emits three
candidates each scoring 2 and returns -2 (AMBIGUOUS); a second
identical call also returns -2; vcount stays 0. 3/3 checks as
predicted.

The withhold is permanent for this fixture class: the API accepts
only a single (fail, fail_out) pair, so no second counterexample can
be supplied to break the tie, and the legitimate revision (2,121)
can never be installed through the diagnosis path. This is the
documented honest behavior ("reports indistinguishability but does
not resolve it"), so it is classified BOUNDARY, not a kill. The
liveness cost is real: on a true tie the learner is permanently
stranded for that condition, with no escalation or second-chance
path in the mechanism's vocabulary.

## X-RV4-3: capacity wall (BOUNDARY, as preregistered)

Five sequential genuine revisions chained in one store, each
diagnosed from a real counterexample with a unique top, each
verified on held-out. P0 = broadcast-last; passing D as above.

- R1: ("xab"->"xxx") -> unique (0,120); appended, vcount=1;
  held-out ("xqw"->"xxx") PASS.
- R2: ("ayz"->"yyy") -> unique (1,121); genuine counterexample
  under slot1; appended, vcount=2; held-out ("byz"->"yyy") PASS.
- R3: ("zbq"->"zzz") -> unique (0,122); genuine counterexample
  under slots 1-2; appended, vcount=3; held-out ("zbw"->"zzz")
  PASS.
- R4: ("mnp"->"mmm") -> unique (0,109); genuine counterexample
  under slots 1-3; appended, vcount=4; held-out ("mqr"->"mmm")
  PASS.
- R5: ("qrs"->"qqq") -> diagnosis WOULD be unique (0,113): a
  legitimate 5th revision from a genuine counterexample (falls
  through all four slots to P0, which predicts "sss"). `vs3_revise`
  emits the VS3FULL warning, returns -1, vcount stays 4. The query
  ("qrs") permanently predicts "sss" instead of "qqq": no recourse.
  Earlier revisions intact ("xab"->"xxx" still PASS).

17/17 X3 checks behaved as predicted. The refusal is explicit, not
silent, exactly as the R2 repair claims: this attack does not break
R2. It is classified BOUNDARY with teeth: the disclosed 4-slot cap
bounds the chained-revision claim, and a continuing learner needing
a 5th genuine revision gets an explicit refusal plus a permanently
wrong answer on that condition. Five chained single-condition
revisions is a trivial real-world need, so the "chained revision"
claim should be read as "chained up to 4".

## X-RV4-4: source audit (PASS with findings)

(a) Tie logic: `best_count` resets to 1 on strict score improvement
and increments on equality; -2 is returned iff `best_count > 1` at
the end; -1 is returned iff no candidate discriminates
(`best_count == 0`). Traced by hand against the [2,2,2], [2,0,0],
and [1,2] patterns; all correct. No counting bug.

(b) VS3FULL: `vs3_revise` has exactly two return paths: -1 on
`vc >= 4` (after emitting the warning) and 1 on append. The old
silent `return 0` no longer exists in the revision path (remaining
`return 0` occurrences are in `streq`, `peval` node evaluation, and
`pfits_at`, all unrelated). No silent-drop path remains.

(c) No hardcoding: the literal scan of `diagnose_scored` and
`vs3_revise` finds no test-answer byte literals (120, 121, 122,
113, 118, 119) and no fixture-specific constants. All compared
values come from the data. The attack harness's mechanism section
(lines 1-421) is byte-identical to the committed revise4.zag
(verified with cmp).

(d) Score degeneracy: confirmed both by proof (above) and
empirically (zero `score=1` lines across all fixtures). Finding:
the prereg and result doc describe two independent signals
(output-relevance, program-consistency); they are one signal. The
honest limit "near-ties (differing by 1) still resolve by lowest
position" describes an impossible event. The accurate statement is:
scores are always 0 or 2, so any unique candidate scoring 2 wins
regardless of position, and any tie at 2 withholds.

Audit verdict: PASS. No spoofing, no hardcoding, no logic bug. Two
findings narrow the mechanism's description (degenerate scoring;
impossible near-tie limit).

## Kill bar assessment (preregistered mapping)

- X-RV4-1 success -> DOWNGRADE. Met: 7/7 checks.
- X-RV4-2 -> expected BOUNDARY. Met: 3/3 checks.
- X-RV4-3 -> expected BOUNDARY. Met: 17/17 checks (plus 4 setup
  checks counted in the 31 total).
- X-RV4-4 -> PASS with findings.

Total: 31/31 attack checks behaved as predicted. 3/3 runs
byte-identical.

## What this does and does not change

- H-REVISE4's frozen bars K-RV4-1 (tie fixture -> AMBIGUOUS),
  K-RV4-2 (explicit VS3FULL), K-RV4-3 (45/45 no regression), and
  K-RV4-4 (determinism) are untouched by this red team and still
  hold. This report does not retroactively alter them.
- The downgrade narrows R1: tie-aware withholding handles exact
  ties, but confident unique misattribution remains, and the
  underlying score carries half the advertised signal content.
- H-REVISE3's SURVIVES verdict on its frozen bars stands, as before.

## Classification after red team

Bounded L2+ revision with a known diagnosis failure mode: the scored
diagnosis is a single binary signal ("discriminating byte appears in
the expected output") that misattributes whenever the true condition
byte is absent from the output while an incidental byte is present.
Exact ties withhold honestly; unique wrong tops do not. Capacity is
explicitly 4. Not general L3.

## Boundaries and honest limits of this red team

- X-RV4-1 uses hand-set P0 (broadcast-last), exactly as the Phase J
  fixture does; the diagnosis under attack is the mechanism's own
  `diagnose_scored`, unmodified.
- The held-out "hidden truth" is the adversary's fixture truth, not
  a claim about any real deployment.
- X-RV4-2 and X-RV4-3 are boundary demonstrations by preregistered
  design; they confirm documented behavior rather than breaking it.
- The degeneracy proof assumes `seq` comes from
  `pextract(fail, fail_out)`; a caller passing an unrelated sequence
  could produce score 1, but no harness call site does so.

## Pure Zag compliance

Prereg, attack harness, compilation (znc 2026.07.0-dev), execution,
and all analysis in Zag only. No Python used at any stage: no
generators, no verifiers, no scratch computation. The md5 and cmp
invocations are shell file utilities, not analysis code. No em
dashes in this document.

## Commit lineage

- Prereg: 4021d99eb (frozen before any attack code).
- This report, revise4_adv.zag, REVISE4_ADV_RAW.txt: committed
  together in the adversary result commit (see git log).
- Target source: revise4.zag as committed (mechanism lines 1-421
  byte-identical in the attack harness, verified with cmp).
