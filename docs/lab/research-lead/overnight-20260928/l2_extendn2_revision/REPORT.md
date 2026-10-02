# REPORT: L2-EXTENDN-2 Revision Mid-Iteration

Status: FROZEN PREREG a259f0a2d executed. Implementation faithful
to the frozen design. Verdict below against the frozen kill bars.

## Verdict

**BUILD-PASS.** K1 through K10 all pass. The EXTEND-REV operator
survives the world changing mid-iteration: after 2 extensions the
world kills the learner's committed next-step licensing fact
(fact 7, (106,2,107)); the learner's stale check detects it on
the very next iteration (detection latency 1 iteration, 0
promotions through the dead fact), re-routes through the live
alternative (106,3,107) to complete the 6-link chain as
[1,1,1,2,2,3] (R1), or terminates cleanly with EXECFAIL and
reports its partial chain honestly when no alternative exists
(R2). The no-stale control promotes the broken extension through
the dead fact, proving detection did the work.

## Per-arm results (3/3 runs byte-identical)

Run output sha256 (all three):
`10fb3633f4dac33e7c913ddde9ac88a56a5786769da3552abe69bc2e60e5847d`
pairwise cmp clean. Binary exit code 0 on all runs.

| arm | ans | ext | stop | allocs | verdict |
|-----|-----|-----|------|--------|---------|
| R1 re-route | 107 | 3 | TERM | 93 | PASS |
| R2 clean stop | 106 | 2 | EXECFAIL | 65 | PASS |
| C1 no-stale | 107 | 3 | TERM (broken) | 89 | PASS (broken as derived) |
| C2 fresh | -2 | n/a | n/a | 71 | PASS (fails as derived) |

Stop codes: 0 TERM, 1 NOFRONTIER, 2 EXECFAIL, 3 BUDGET.
allocs = node allocations (hg(W,20)) for the arm's workspace.

## Kill bars

- K1 (R1 exact): PASS. ans=107, ext=3, stop=TERM, final MAP
  relseq [1,1,1,2,2,3] verified by cc_relseq white-box, 3
  type-16 hops from final MAP 90 back to native m 24
  (90->64->42->24), ultimate ancestor == m. out[3] = fact 7,
  the killed (106,2,107), with is_superseded == 1; out[4] =
  fact 8, the live (106,3,107), with is_superseded == 0;
  died != repl. Detection latency: 1 iteration (the kill lands
  in iteration 2's post-step world hook; the stale check fires
  at the start of iteration 3 before any assembly), and 0 MAPs
  were promoted through the dead fact before detection.
- K2 (R2 exact): PASS. ans=106, ext=2, stop=EXECFAIL, final
  MAP relseq [1,1,1,2,2], 2 type-16 hops to m, ultimate
  ancestor == m, out[3] = killed fact 7 (106,2,107,
  superseded), out[4] == -1, exactly 2 adapted MAPs promoted
  (ext 1 and ext 2 only), no licensing fact of any promoted
  MAP superseded (rv_find_dead == -1).
- K3 (C1 no-stale control): PASS, behaves exactly as derived.
  Without the stale check and the step entry guard, the control
  uses the dead committed plan blindly: assembly reads
  rnew=2, vnext=107 from fact 7's intact fields and t2_exec
  verifies numerically (replay of dead values, the C295/I5
  finding), promoting [1,1,1,2,2,2] licensed by the superseded
  fact 7. ans=107, ext=3, stop=TERM, but rv_audit_live == -1
  and rv_find_dead returns fact 7 (106,2,107, superseded).
  Detection did the work in R1.
- K4 (C2 fresh learner): PASS, fails exactly as derived. With
  no native MAP, the frozen generic miss policy t2_trial
  returns -2: its gather caps at 4-link paths (101..105), none
  reaches 107, count/sum/single-link candidates all reject.
  The extra (106,3,107) fact sits beyond the 4-link horizon.
- K5 (no-broken-promotion audit, R1): PASS. rv_audit_live
  walks the full type-16 provenance chain (4 MAPs: the 6-link
  final, the 5-link, the 4-link, and native m): every
  licensing fact of every MAP is live (is_superseded == 0 on
  all fids from cc_satisfy), and t2_exec of each MAP's root
  from s=101 equals that MAP's terminal (final: 107). A replay
  of dead values would have failed the liveness leg per the
  C295/I5 finding; the C1 control demonstrates the audit
  bites (returns -1 there).
- K6 (3/3 byte-identical): PASS. sha256 above, pairwise cmp
  clean, exit 0 on all three runs.
- K7 (0 new machinery): PASS. New code issues link_edge only
  with type 16 (operator provenance: rv_step and the labeled
  control rv_step_blind) and type 3 (the disclosed world-kill
  self-loop in rv_world_step, reusing the frozen supersede
  semantic that is_superseded checks). 0 new edge types, 0 new
  opcodes, 0 modes, 0 bridges, 0 handlers, 0 new semantic
  cases, 0 new node tags (no ns(W,*,0,*) writes in new code).
  Frozen copies sha256:
  cc_base dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  un_patch 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2,
  adapt_patch 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0,
  all identical to the C301 origins; origins unmodified
  (git diff empty on l2_extend_iterative).
- K8 (white-box trace): PASS. Every extension logs parent id,
  new id, plen, licensing fact (s,r,o), terminal; every plan
  commit logs fact id and (s,r,o); the world kill logs fact id
  and (s,r,o); the revision logs died fact id + (s,r,o) and
  the replacement id + (s,r,o) or the clean stop. Full R1 and
  R2 traces reproduced below.
- K9 (commit order): PASS. Prereg commit a259f0a2d contains
  only PREREG.md and NAMECHECK.md (Step 0 guard);
  `git show --stat` verified 2 files, 265 insertions, no
  implementation. All implementation files were written after.
- K10 (hand derivation): PASS. Section 3 of the frozen PREREG
  derives every arm's exact chain, terminal values, and stop
  reason with the arithmetic shown; the driver asserts every
  constant inline (ans, ext, stop, relseq, hops, ultimate
  ancestor, died/repl fact contents and liveness, audit
  counts).

## White-box trace: R1 (run 1, identical in runs 2-3)

```
RV-NATIVE id=24 plen=3 term=104
RV-QUERY s=101 goal=107 start=24 startplen=3
RV-PLAN lic=5 (104,2,105)
RV-STEP n=1 parent=24 id=42 plen=4 lic=104,2,105 term=105
RV-PLAN lic=6 (105,2,106)
RV-STEP n=2 parent=42 id=64 plen=5 lic=105,2,106 term=106
RV-PLAN lic=7 (106,2,107)
WORLD-KILL fact=7 (106,2,107) after-ext=2
RV-REVISION died=7 (106,2,107) frontier=106
RV-REROUTE new=8 (106,3,107)
RV-STEP n=3 parent=64 id=90 plen=6 lic=106,3,107 term=107
RV-PLAN lic=-1
RV-STOP reason=0 ext=3 ans=107 final=90 died=7 repl=8
AUDIT-R1 live-maps=4
ARM R1 ans=107 ext=3 stop=0 allocs=93 PASS
```

Reading: the learner plans each next step from live
observations (lic=5, then 6, then 7). The world kills the
committed plan (fact 7) after ext 2 without telling the
learner. At the next iteration the stale check fires:
RV-REVISION names the died fact and the frontier; the re-scan
finds the live alternative fact 8; RV-REROUTE records the
replacement; the extension completes the chain through live
facts only, and the learner stops at its predicted terminal.
The final MAP's type-16 chain (90->64->42->24) carries the
provenance through the revision.

## White-box trace: R2 (run 1, identical in runs 2-3)

```
RV-NATIVE id=23 plen=3 term=104
RV-QUERY s=101 goal=107 start=23 startplen=3
RV-PLAN lic=5 (104,2,105)
RV-STEP n=1 parent=23 id=41 plen=4 lic=104,2,105 term=105
RV-PLAN lic=6 (105,2,106)
RV-STEP n=2 parent=41 id=63 plen=5 lic=105,2,106 term=106
RV-PLAN lic=7 (106,2,107)
WORLD-KILL fact=7 (106,2,107) after-ext=2
RV-REVISION died=7 (106,2,107) frontier=106
RV-STOP reason=2 ext=2 ans=106 final=63 died=7 repl=-1
AUDIT-R2 live-maps=3
ARM R2 ans=106 ext=2 stop=2 allocs=65 PASS
```

Reading: identical through the kill and the revision event;
the re-scan finds no live fact at frontier 106, so the
learner stops EXECFAIL with its best verified terminal 106.
Nothing is promoted through the dead fact (exactly 2 adapted
MAPs exist; the audit confirms all licensing facts live).
This exercises the EXECFAIL stop C301 left untested.

## Ablation numbers

- Remove the stale check (C1): the learner promotes a broken
  6-link MAP through the superseded fact (89 allocations,
  ans=107 with dead provenance). Detection is load-bearing:
  with it, 0 dead-fact promotions (R1, 93 allocations,
  ans=107, all facts live).
- Remove the alternative fact (R2 vs R1): the same detection
  machinery terminates cleanly (EXECFAIL, ans=106, 65
  allocations) instead of hallucinating a completion. A
  runaway or hallucinated completion would have been a FAIL;
  none occurred.
- Retire m (C2): generic policy fails (-2) after 71 node
  allocations; the 6-link gap is unbridgeable from scratch by
  the frozen miss policy, while EXTEND-REV bridges it at 93
  allocations reusing m and revising mid-iteration.

## Architecture accounting

- Cognition lines added (rv_patch.zag operator section: plan
  commitment, stale check + revision, guarded step, loop,
  trace helpers; non-comment non-blank): 167. Full
  rv_patch.zag: 496 lines (remainder is labeled world,
  control, prior-knowledge, and audit scaffold). Driver
  (rv_driver.zag) is harness, not cognition.
- 0 new edge/MAP types (type-16 provenance reuse; type-3
  self-loop reuses the frozen supersede semantic for the
  disclosed world kill), 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 new semantic cases.
- Researcher scaffold (disclosed): world facts, native MAP
  teaching, arm goals, the world-kill hook (fires on the
  learner's committed plan after ext 2, learner not told),
  the C1/C2 control variants, audit helpers, driver
  assertions. Learner-owned: starting MAP selection, plan
  commitment, stale detection, the re-route decision,
  continuation vs stop at every step, extension count, all
  wiring endpoints.

## Build and artifact hashes

- rv_full.zag:
  23fc9ce8ac629cf8a3f7b41b1975fb1f23f28bd3dce822ded555f70e79ea7687
  (byte-identical to cat of cc_base + un_patch + adapt_patch +
  rv_patch + rv_driver in build order)
- rv_bin:
  c4738ff5eb65ab3c9b89be2155a86e58efe07e0f176ef6d03a59cbdfc3c571e4
  (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  compile exit 0; only pre-existing A0102-class warnings, the
  same ignored-return-value class the frozen sources emit)
- rv_run1/2/3.txt:
  10fb3633f4dac33e7c913ddde9ac88a56a5786769da3552abe69bc2e60e5847d

## Notes and follow-ups (not verdict changes)

- The fourth znc defect (`!(A && B)` in while conditions) was
  grepped in the new sources: absent (grep rc=1).
- The world-kill rule (kill the learner's committed plan after
  ext 2) is learner-agnostic and needs no fact ids from the
  driver; it generalizes to any frontier layout.
- Natural next lane: revision where the re-route itself
  requires adapting the interface (different relation arity
  or a two-fact bridge), and revision under memory pressure
  where the dead fact's dependents must be re-derived.
