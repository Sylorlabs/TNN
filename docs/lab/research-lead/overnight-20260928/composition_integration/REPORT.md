# REPORT: H-COMPINTEG-1 Composition Integration

Status: FROZEN PREREG 05d1b7a28 executed. Implementation faithful to
the frozen design. Verdict below against the frozen kill bars K1-K8.

## Verdict

**COMPOSITION-INTEGRATION-INCOMPLETE.** K2, K4, K6, K7, K8 pass.
K1, K3, K5 fail. I5 diagnostic fails (non-gating, reported).

This is not a VOID: toolchain guard clean (pure Zag, safebin, no
forbidden interpreter), prereg commit 05d1b7a28 strictly precedes
implementation (commit contains only PREREG.md, verified via
`git show --stat`), no bar weakened or reinterpreted. The failures
are prereg hand-derivation errors and genuine integration breaks,
which the parent mandate explicitly asked to be reported.

## Per-arm results (3/3 runs byte-identical)

Run output sha256 (all three): `d0ec18fd37dbe43b8122251ca0a8d083fec7a8b56d0fed42319103cd6fc0d1bc`

### I1 INTEGRATE-EXTEND: FAIL (bar: ans=108)

Observed: ans=105. Explore (4 cycles, op=1) created exactly one
trial per cycle (ADAPT-MK len=4, src=27=MAP_X); each executed v=105,
never 108. The learner honestly taught FACT(101,70,105) and raised
it to score 3 (bar expected FACT(101,70,108) score 3;
id_fact_score(101,70,108) = -999999). Query: p=105 rel=3, native DFS
fails, bracket ADAPT-CREATED n=3 (extend [1,1,1,2] id=160, truncate
[1,1] id=170, specialize [70] id=176), lv_dfs terminates at 105 via
160 (longest first), verify 105==105, MAP_Z LINK14->160.

Assertion detail: p1(ans==108)=0, p2(a type-16->MAP_X kind 1)=1,
p3(MAP_Z LINK14->a)=1, p4(exactly 2 live adapted)=0 (3 live),
p5(score==3 for the 108 FACT)=0.

Root cause (prereg hand-derivation error, not an implementation
bug): the frozen adapt_extend is EXTEND-ONE (adapt_patch.zag: it
extends each fully-satisfied native MAP by exactly one frontier
fact). From 101, [1,1,1,2] ends at 105: 101-1->102-1->103-1->104,
104-2->105. The prereg's "creates trial [1,1,1,2], executes to 108"
is arithmetically impossible; 108 needs [1,1,1,2,2,2] (6 links),
i.e. three successive extensions. adapt_extend only extends native
MAPs and explore retires trials (retire=1), so the chain can never
accumulate. No implementation change inside the frozen design can
produce 108; doing so would need a new multi-link operator. The
integration machinery itself worked coherently at 105: learner
prediction, learner verification, and self-wiring (type-16, LINK14)
all fired as designed.

Secondary: p4's "exactly 2 live adapted" contradicts the frozen
bracket, which runs extend+truncate+specialize (3 created here).

### I2 INTEGRATE-TRUNCATE: PASS

ans=13. t=[1,1] with type-16->MAP_X, kind 2; MAP_Z LINK14->t;
FACT(11,72,13) score 3. Bracket: extend created nothing (frontier
14 dead end, as hand-derived), truncate [1,1], specialize 2 MAPs
(neither terminates at 13; harmless). All four assertions pass for
the reasons the prereg gives.

### I6 INTEGRATE-SPECIALIZE: FAIL (bar: ans=99)

Observed: ans=-3 (withheld, rel=0). Explore (op=3) created per
cycle: len=2 [1,2] (->99) AND len=1 [71] (->14). The [71] trial
substitutes link 0 with the learner's own FACT(11,71,14) relation;
later cycles also create [74] trials from self-taught FACTs.
Observation stream alternates 14/99; FACT(11,74,99) score stuck at
0, never reaching 3.

Root cause (frozen operator behavior the hand derivation missed):
ts_specialize_src treats learner FACT nodes (field 0==1) as
alternative-relation candidates (any fact with field 20==vj and
field 24 != rj). The prereg assumed one [1,2] trial per cycle;
actual behavior self-referentially substitutes the learner's own
FACT relations, polluting learner-owned verification. The [71]->14
"execution" replays the operator's own construction values through
t2_exec, so it is not an independent world interaction.

### I4 INTEGRATE-WITHHOLD: PASS

ans=-3; zero type-16 edges workspace-wide; live MAP count == 1
(MAP_X only). The adapt bracket never fired. The withhold gate
works: no prediction basis, no restructuring, no side effects.

### I3 INTEGRATE-STALE-REVISE: FAIL (bar: q1=108, q2=-2)

Observed: q1=105, q2=105. Cascades from the I1 root cause (q1 was
never 108). After the world change (teach (104,2,140), kill
(104,2,105)): adapt_revise2 never fired. q2's native lv_dfs found
seg 176, the [70] self-referential MAP built from the learner's
own FACT(101,70,105), terminating at p=105; verify 105==105;
promoted MAP_Z2 LINK14->176. a=160 ([1,1,1,2]) still live (not
retired); no a2 created; MAP_Z (q1) LINK14->160 still present
(id_count14to(160)=1); FACT(101,70,108) score=-999999.

Findings beyond the cascade: (a) the stale-revision path never
engaged because a self-justifying MAP let the stale prediction
verify against itself: the learner's FACT became an executable
"relation", so verification-against-own-prediction is circular here.
(b) t2_exec replays assembled value chains rather than re-deriving
through live facts, so the killed fact did not change trial
execution (m=160 still yields 105 in I5).

### I5 INTEGRATE-RECOVERY (diagnostic, non-gating): FAIL

10 cycles, no convergence: pred oscillates 105/140, rel stuck at
0/1; q3=-3 (withheld). Each cycle executes stale-replay m=160
(->105) and fresh m=221 ([1,1,1,2] via (104,2,140) ->140);
lv_observe supersedes each cycle so no FACT reaches score 3.
Structural: with retire=0 both trials persist, and value-replay
execution immunizes the stale trial against the fact kill.

## Kill bars

- K1 (I1 assertions): FAIL. ans=105 vs bar 108; prereg hand
  derivation contradicts frozen EXTEND-ONE semantics.
- K2 (I2 assertions): PASS.
- K3 (I6 assertions): PASS criteria not met: FAIL. ans=-3;
  self-referential specialize trials block score convergence.
- K4 (I4 assertions): PASS. -3, zero adaptation side effects.
- K5 (I3 assertions): FAIL. q1=105, q2=105; no revision fired;
  self-justifying MAP short-circuits the break probe.
- K6 (3/3 byte-identical): PASS. sha256
  d0ec18fd37dbe43b8122251ca0a8d083fec7a8b56d0fed42319103cd6fc0d1bc,
  pairwise cmp clean.
- K7 (dashes; `expected` token; 0 modes/bridges/handlers/semantic
  cases): PASS. check_no_dash.sh exit 0 on all deliverables;
  `expected` appears nowhere in integ_patch.zag (grep audit; three
  comment occurrences reworded to researcher-provided/answer, code
  semantics untouched); 0 new edge/MAP types (16/14/15 reused), 0
  new opcodes, 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- K8 (frozen source integrity): PASS. All six copies sha256-identical
  to origins; origins unmodified (git diff empty); un_patch.zag
  3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2
  matches the prereg record.

Frozen bar citations: PREREG.md sections 3 (battery) and 4 (K1-K8).

## Integration breaks found (mandate: report where it breaks)

1. I1 hand derivation vs EXTEND-ONE: the prereg's 108 is
   unreachable under the frozen one-link operator. Design-level
   inconsistency; the implementation is faithful.
2. Self-referential specialization: ts_specialize_src substitutes
   learner FACT relations ([71], [70], [74] trials), polluting
   learner-owned verification (I6) and enabling circular
   self-verification that defeats stale revision (I3 q2).
3. Value-replay execution: t2_exec replays assembled chains, so
   fact kills do not invalidate trial executions (I3/I5).
4. REBIND exclusion confirmed per prereg 2.4: rebind_try's
   signature takes a researcher answer; no learner-verified
   variant exists in the frozen sources.
5. Latent ts_patch misdispatch for unrecorded-kind stale MAPs
   handled per prereg 2.2 via integ_tag_extend (kind 1 completion);
   kind recording verified live (kinds 1/2/3 asserted in I1/I2).

## Architecture accounting

- Cognition lines added (integ_patch.zag, non-comment non-blank):
  157. Driver (integ_driver.zag) is harness, not cognition.
- 0 new edge/MAP types, 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 new semantic cases.
- Researcher scaffold (disclosed): pipeline order, withhold gate,
  kind-completion tagging, explore/exploit split, KIND/REBIND
  boundary decisions. Learner-owned: predictions, reliability,
  which adaptations are created, verification outcomes, all wiring
  endpoints. No harness code writes edges in the integrated path
  (driver helpers are read-only scans; I3's world change is the
  preregistered teach-then-kill).

## Build and artifact hashes

- integ_full.zag: 047bd54e070aaedc10d800209e0e70d0064b126ba866efc8901d8919001e13ce
  (byte-identical to cat of the 8 sources in build order)
- integ_bin: a44e696642dd6e38a9d3696b6393ced1880030519e92549d4a1a813d2c7ffc7c
  (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  compile exit 0)
- Frozen copies: cc_base dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6;
  un_patch 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2;
  adapt_patch 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0;
  revise_patch 5113000b1360bf3e978cb106f91f15a1e5956db113eb4b3c26a1ebde1fa7f6e3;
  ts_patch 07b7b3952db65b04d8bccf288d28ff0a2aaa899fefd75a1da0250baa7d22b451;
  lvcomp_patch ea833de28d21657b6cb6dcf2ad8c378b6cf604ccbe81680b6acfdcc68e24c302

## White-box trace excerpts (run 1)

I1 query bracket: `ADAPT-MK id=160 src=27 len=4`,
`TS-TRUNC-MK id=170 src=27 linkto=27 len=2`,
`TS-SPEC-MK id=176 src=27 linkto=27 len=1`,
`INTEG-ADAPT-CREATED n=3`, `INTEG-COMP-SEGS n=1 160`, `I1-ANS=105`.
I2: `INTEG-ADAPT-CREATED n=3`, `INTEG-COMP-SEGS n=1 113`, `I2-ANS=13`.
I6 cycle 1: `TS-SPEC-MK id=65 ... len=1`, `TS-SPEC-MK id=75 ... len=2`,
`INTEG-EXPLORE-EXEC m=65 v=14 pred=-999999`,
`INTEG-EXPLORE-EXEC m=75 v=99 pred=14`; final
`INTEG-WITHHOLD unreliable rel=0`, `I6-ANS=-3`.
I3 q2: `INTEG-NATIVE-SEGS n=1`, `INTEG-COMP-SEGS n=1 176`,
`I3-Q2=105` (no REVISE2-STALE line: revision never fired).
I5: `INTEG-EXPLORE-EXEC m=160 v=105` alongside
`INTEG-EXPLORE-EXEC m=221 v=140` every cycle; 10 cycles, q3=-3.

## Recommended follow-ups (not verdict changes)

- The I1 arm needs a prereg amendment (fresh preregistration, not
  salvage): either Z facts within one EXTEND-ONE reach of MAP_X, or
  an explicit multi-extension protocol in the explore phase.
- Self-referential FACT substitution in ts_specialize_src deserves
  its own red-team lane: a learner-verified operator should not
  treat the learner's predictions as world relations.
- Value-replay vs live-fact execution in t2_exec is a semantic
  gap the stale-revision design assumes away.
