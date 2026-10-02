# REPORT: L2-EXTENDN-1 Iterative Extension Operator

Status: FROZEN PREREG 800a9558a executed. Implementation faithful
to the frozen design. Verdict below against the frozen kill bars.

## Verdict

**BUILD-PASS.** K1 through K10 all pass. The learner-triggered
iterative extension operator (EXTEND-ITER) accumulates multi-link
chains that frozen EXTEND-ONE cannot: from native MAP m with
relse q [1,1,1] it reaches [1,1,1,2,2,2] in 3 learner-decided
extensions for the need-6 query and [1,1,1,2,2] in 2 extensions
for the need-5 query, each extension licensed by a real frontier
fact and linked to its parent by a type-16 adapted-from edge.

## Per-arm results (3/3 runs byte-identical)

Run output sha256 (all three):
`355a059fd987f78f96b5f0ccaaeae83dbe640e96adfd1d2a908fa63a7eedd59a`
pairwise cmp clean. Binary exit code 0 on all runs.

| arm | ans | ext | stop | allocs | verdict |
|-----|-----|-----|------|--------|---------|
| E1 need-6 | 107 | 3 | TERM | 89 | PASS |
| E2 need-5 | 106 | 2 | TERM | 63 | PASS |
| E3 missing fact | 105 | 1 | NOFRONTIER | 40 | PASS |
| C1 EXTEND-ONE | -3 | nmk=1 | n/a | 41 | PASS (fails as derived) |
| C2 fresh | -2 | n/a | n/a | 71 | PASS (fails as derived) |
| A1 no-TERM-rule | 108 | 4 | NOFRONTIER | 119 | PASS (overshoots as derived) |

Stop codes: 0 TERM, 1 NOFRONTIER, 2 EXECFAIL, 3 BUDGET.
allocs = node allocations (hg(W,20)) for the arm's workspace.

## Kill bars

- K1 (E1 exact): PASS. ans=107, ext=3, stop=TERM, final MAP
  relseq [1,1,1,2,2,2] verified by cc_relseq white-box, 3
  type-16 hops from final MAP 90 back to native m 24
  (90->64->42->24), ultimate ancestor == m.
- K2 (E2 exact): PASS. ans=106, ext=2, stop=TERM, final relseq
  [1,1,1,2,2], 2 type-16 hops to m. K1+K2: extension counts 3 vs
  2 with no count parameter anywhere in the operator; the count
  is decided by the loop against the per-arm goal.
- K3 (E3 missing middle fact): PASS. ans=105, ext=1,
  stop=NOFRONTIER, final relseq [1,1,1,2]. Exercises the second
  learner-owned stopping rule: frontier 105 has no live
  licensing fact, so the learner stops honestly at its best
  verified terminal instead of guessing.
- K4 (C1 EXTEND-ONE control): PASS, fails exactly as derived.
  The frozen adapt_extend promotes exactly one adapted MAP
  [1,1,1,2] (ADAPT-MK id=42 src=24 len=4); adapted MAPs are not
  re-extended; longest chain terminates at 105 != 107, answer
  -3. This reproduces the C295/K1 failure and proves the
  iteration in E1 did the work.
- K5 (C2 fresh learner): PASS, fails exactly as derived. With
  no native MAP, the frozen generic miss policy t2_trial returns
  -2: its gather caps at 4-link paths (101..105), none reaches
  107, count/sum/single-link candidates all reject. The fresh
  learner spends 71 node allocations trying and still fails;
  the 6-link gap is unbridgeable from scratch by the generic
  policy, while EXTEND-ITER bridges it at 89 allocations total
  reusing m.
- K6 (A1 no-TERM-rule ablation): PASS, overshoots exactly as
  derived. Without the TERM check the loop extends a 4th time
  via the decoy fact (107,2,108) to [1,1,1,2,2,2,2], terminal
  108, then stops NOFRONTIER at the dead frontier 108.
  ans=108 is wrong against goal 107. The stopping rule is
  load-bearing: it prevents runaway extension past the
  predicted terminal.
- K7 (3/3 byte-identical): PASS. sha256 above, pairwise cmp
  clean, exit 0 on all three runs.
- K8 (0 new machinery): PASS. New code issues exactly one
  link_edge call: type-16 adapted-from, parent linkage only.
  0 new edge types, 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 new semantic cases, 0 new node tags (no
  ns(W,*,0,*) writes in new code). Frozen copies sha256:
  cc_base dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  un_patch 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2,
  adapt_patch 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0,
  all identical to origins; origins unmodified (git diff empty
  on composition_integration).
- K9 (white-box trace): PASS. Every extension step logs parent
  id, new id, plen, licensing fact (s,r,o), and terminal. Full
  E1 trace reproduced below.
- K10 (commit order): PASS. Prereg commit 800a9558a contains
  only PREREG.md and NAMECHECK.md (Step 0); `git show --stat`
  verified 2 files, 238 insertions, no implementation.

## White-box trace: E1 (run 1, identical in runs 2-3)

```
EXTN-NATIVE id=24 plen=3 term=104
EXTN-QUERY s=101 goal=107 start=24 startplen=3
EXTN-STEP n=1 parent=24 id=42 plen=4 lic=104,2,105 term=105
EXTN-STEP n=2 parent=42 id=64 plen=5 lic=105,2,106 term=106
EXTN-STEP n=3 parent=64 id=90 plen=6 lic=106,2,107 term=107
EXTN-STOP reason=0 ext=3 ans=107 final=90
ARM E1 ans=107 ext=3 stop=0 allocs=89 PASS
```

Reading: the learner selects native MAP 24 ([1,1,1], term 104)
by its own longest-satisfied scan. 104 != 107, so it extends:
frontier 104 is licensed by real fact (104,2,105) to MAP 42
(type-16 -> 24). Term 105 != 107: extend again from the new
frontier via (105,2,106) to MAP 64 (type-16 -> 42). Term
106 != 107: extend via (106,2,107) to MAP 90 (type-16 -> 64).
Term 107 == 107: STOP TERM. The decoy fact (107,2,108) is never
touched because the learner stops at its predicted terminal.

## Ablation numbers

- Retire m (C2): generic policy fails (-2) after 71 node
  allocations of candidate assembly; rebuild-from-scratch does
  not reach the 6-link target at any spent cost within the
  frozen miss policy.
- Remove TERM rule (A1): 4 extensions, 119 allocations, wrong
  answer 108. The rule is load-bearing against overshoot.
- EXTEND-ONE only (C1): 1 extension, 41 allocations, answer -3.
  Iteration (E1: 3 extensions, 89 allocations, answer 107) is
  what bridges the gap.

## Architecture accounting

- Cognition lines added (extn_patch.zag operator section:
  selection, step, loop, trace helpers; non-comment
  non-blank): 133. Full extn_patch.zag: 293 (remainder is
  labeled ablation/control/prior-knowledge scaffold).
  Driver (extn_driver.zag) is harness, not cognition.
- 0 new edge/MAP types (type-16 reused), 0 new opcodes,
  0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Researcher scaffold (disclosed): world facts, native MAP
  teaching, arm goals, the C1/C2/A1 control variants, driver
  assertions. Learner-owned: starting MAP selection, which
  frontier fact licenses each step, extension count,
  continuation vs stop at every step, all wiring endpoints.

## Build and artifact hashes

- extn_full.zag:
  d835d2d605c1fd1015d645c236d7b27fcbfb8e108da7c5b9d6441ff7ab709e65
  (byte-identical to cat of cc_base + un_patch + adapt_patch +
  extn_patch + extn_driver in build order)
- extn_bin:
  d6a20a0537745d4d564bc744b3eafa6ef8af837c5c0bf5d876aa281260f1b016
  (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  compile exit 0; only pre-existing A0102 warnings from frozen
  sources)

## Notes and follow-ups (not verdict changes)

- One harness assertion bug was fixed during implementation
  (driver A1 compared a 7-link relseq against a 6-slot
  expected buffer); the operator already produced exactly the
  preregistered A1 values. No frozen bar was touched.
- The fourth znc defect noted in AGENTS.md during this session
  (`!(A && B)` in while conditions) was grepped: the pattern
  appears nowhere in the new sources.
- E3 shows the NOFRONTIER rule fires honestly on a missing
  middle fact; a natural next lane is stale-fact revision
  during iteration (a licensing fact dying mid-extension),
  which would exercise EXECFAIL.
