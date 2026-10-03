# REPORT: L2 SUBSTITUTE Operator (Chain Family)

Worker: L2 Substitute Worker (subagent, 2026-10-02).
Prereg: `l2_substitute/PREREG.md`, frozen alone at commit
1fb6db863 before any implementation existed. Two transparent
amendments, both pre-verdict: PREREG_AMENDMENT1.md (operator
firing semantics, pre-implementation, commit c83312197);
PREREG_AMENDMENT2.md (FULL A_SEARCH hand-derivation 9 -> 8,
arithmetic correction only, 5x ratio threshold unchanged).

## Verdict

**L2-SUBSTITUTE-COMPLETE.** All ten kill bars PASS, no falsifier
fired, 3/3 byte-identical.

## What was built

A standalone pure-Zag learner (`learner.zag`, 825 lines) plus
environment side (`world.zag`: frozen fact table + world-change
kill) and experiment side (`driver.zag`: five arms + kill-bar
evaluation), assembled as
`cat learner.zag world.zag driver.zag > sub_full.zag` (1220 lines)
and compiled with the pinned znc to `sub_bin` (build exit 0).

The learner holds a fact store, a MAP inventory (learned chain
routes: relation sequence + licensing facts + endpoints), an edge
store using only types 14/15/16, and the generic SUBSTITUTE
operator: on query failure it stale-detects (the m_exec licensing
check: a hop whose fact is dead records STALE_MAP/HOP/FACT),
splits the stale MAP at the dead hop, searches live pieces in
node-id order for the first endpoint-matching all-live piece,
dedups, verifies the assembled chain by real execution to the
target, promotes the adapted MAP with type-16 adapted-from edges,
retires the stale MAP, and delivers the answer through the new
MAP. A generic iterative-deepening rebuild fallback (no learned
structure guides it) is the honest from-scratch baseline. The
no-substitute control arms run generic EXTEND-ONE/TRUNCATE-ONE
instead. SUB_ON/ET_ON are driver-set causal-control flags (the
composition_l2 adapt_on precedent), never written by the learner.

## Kill-bar results (from sub_run1.txt, reproduced in runs 2, 3)

- K-1 (n prior and independent): INTERSECT=0, M-OK ans=4 via=0,
  N-OK ans=3 via=1, and shell check N-OK (line 8) precedes KILL
  (line 10). PASS.
- K-2a (ablate n): ABLATE-N t16=0, ans=4 via native m3,
  A_SEARCH=76 >= 5*8=40. The adapted m2 cannot exist without n;
  the learner rebuilds from scratch at 9.5x the substitution
  search cost (76 vs 8). PASS.
- K-2b (ablate m prefix): ABLATE-M ans=-2, t16=0, NM=3. Killing
  fact 0 as well as fact 1 leaves no (1,2) piece and no rebuild
  path (dead-ends at 12). PASS.
- K-3 (fresh learner): FRESH t16=0, ans=4 via native m3,
  A_SEARCH=72 >= 40 (9x). PASS.
- K-4 (white-box trace): all six frozen lines present verbatim
  in ARM-FULL: `SUB-STALE m=0 hop=1 fact=1`,
  `SUB-CAND id=1 s=2 e=3 flive=2 MATCH`,
  `SUB-BUILD rels=1,2,2,1 facts=0,3,4,2`, `SUB-VERIFY term=4`,
  `SUB-PROMOTE m2=3`, `ANS via=3 val=4`. The trace shows which
  piece was chosen (MAP1) and why (endpoints 2->3, 2/2 facts
  live), all read from learner state. PASS.
- K-5 (no-substitute control fails): NO-SUB ans=-2 with t16=3:
  ET-TRUNC t=3 from=0, ET-EXTEND e=4 from=2, ET-EXTEND e=5
  from=3 all fired and still failed. Extend/truncate provably
  cannot repair a middle-segment death; substitution did the
  work in FULL. PASS.
- K-6 (stale retired, not reused): FULL MAP0 live=0;
  post-query ans=4 via=3 (through m2, with m retired). PASS.
- K-7 (provenance, zero new types): FULL t16=2 with exactly
  {3->0, 3->1}; t15=2 with exactly {0->1, 1->0} (co-use written
  by the learner's deliver routine on episode success);
  LINK14 34->3 exists (answer node to delivering MAP);
  other=0 (no edge type outside {14,15,16}). PASS.
- K-8 (determinism): sub_run1/2/3.txt sha256 identical:
  198ef5c6d9bdc2dae17182cb4f9a7b1c89b6f2e53208243b7bd2b4474c38f261.
  PASS.
- K-9 (audit): all 8 frozen patterns return 0 hits on
  learner.zag (`1,2,2,1`, `0,3,4,2`, `(2,2,5)`, `(2,1,3)`,
  `_MODE`, case-insensitive `bridge`, case-insensitive
  `python`, `as *i32`). PASS.
- K-10 (FULL success): ans=4 via MAP3; MAP3 relseq [1,2,2,1],
  start 1, end 4, live 1, printed from learner state. PASS.

No falsifier fired: F-NO-CAND, F-WRONG-M2, F-STALE-REUSE,
F-CTRL-PASS, F-ABLN-ADAPT, F-ABLM-PASS, F-FRESH-ADAPT,
F-EDGE-NEW, F-AUDIT, F-NONDET, F-PYTHON all silent.

## Key numbers

- Substitution cost (FULL adapt phase): A_SEARCH=8,
  A_EXEC=3. One candidate evaluated (MAP1), one verification
  exec to terminal 4.
- Fresh-rebuild cost (FRESH): A_SEARCH=72, A_EXEC=9. 8
  candidates verified across L=1..4 (terms 2,11,5,13,12,3,14,4).
- Ablated-n rebuild cost (ABLATE-N): A_SEARCH=76, A_EXEC=10.
- Ratios: 76/8 = 9.5x, 72/8 = 9x (frozen bar: >= 5x).
- Provenance: 2x type-16 (3->0, 3->1), 2x type-15 (0->1, 1->0),
  LINK14 answer->m2, 0 other edge types.
- sha256 (runs): 198ef5c6d9bdc2dae17182cb4f9a7b1c89b6f2e53208243b7bd2b4474c38f261 x3.
- Binary sha256:
  9f9a4cd1af7644f34441aa6c18f7d7a1875c05e841b72d20f956e16b902f91a1

## Architecture accounting

- Cognition lines added: 1220 (learner.zag 825, world.zag 26,
  driver.zag 369; new files, nothing else touched).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New handlers: 0. New edge types: 0 (14/15/16 reused with
  their established semantics). New opcodes: 0.
- Capability-source delta: the SUBSTITUTE capability lives in
  one generic operator plus learned MAP state; no per-problem
  researcher selection anywhere in the substitution path.

## Why this is L2 adaptive reuse

EXTEND and TRUNCATE were already demonstrated; SUBSTITUTE was
the missing operator. Here the old structure m is partly useful
(its prefix 1->2 and suffix 3->4 survive) and partly dead (the
middle 2->3 license). The learner does not rebuild: it keeps
prefix and suffix, swaps in the independently learned n for the
dead segment, verifies by execution, and promotes m2 with
provenance. The choice of n comes from learner state (node-id
order endpoint match over live pieces; the distractor d is
examined and rejected in ABLATE-N/ABLATE-M, and would be in FULL
had n not matched first). The ablations prove causal dependence
on both m's prefix (ABLATE-M fails) and n (ABLATE-N cannot
adapt, rebuilds natively at 9.5x search cost), and the fresh
learner pays 9x. The no-substitute control proves extend and
truncate, genuinely firing, cannot do this task.

## Files

All under `docs/lab/research-lead/overnight-20260928/l2_substitute/`:

- PREREG.md (frozen, committed alone at 1fb6db863)
- PREREG_AMENDMENT1.md (firing semantics, pre-implementation)
- PREREG_AMENDMENT2.md (A_SEARCH 9->8 correction, pre-verdict)
- NAMECHECK.md (toolchain guard Step 0 record, dev notes)
- REPORT.md (this file)
- learner.zag (generic SUBSTITUTE learner; 0 modes/handlers/
  semantic cases; no world data)
- world.zag (fact table + kill; environment side only)
- driver.zag (five arms + kill-bar evaluation)
- sub_full.zag (assembled 1220-line build input)
- sub_bin (compiled binary)
- sub_compile.txt (build log; exit 0)
- sub_run1.txt, sub_run2.txt, sub_run3.txt (3/3 byte-identical)

## Non-claims and bounds

- One world family (chain routing with a middle-fact kill). No
  generality claim beyond the five arms. Cross-domain
  substitution and substitution with interface adaptation
  (endpoints not exactly matching) are open future work.
- Does not claim Micah's full 12-criterion L3 bar; this is an
  L2 operator demonstration against ten frozen bars.
- The kill was builder-designed, not adversary-designed.
  Sealed-adversary generality is open future work.
- The SUBSTITUTE operator, stale-check semantics, rebuild
  fallback, control operators, edge-type conventions, and cost
  counters are disclosed researcher-supplied generic machinery.
  The claim is narrow: dead-segment substitution from
  learner-state piece search with execution verification and
  adapted-from provenance, with the no-substitute control
  provably failing.
- Pure Zag, safebin toolchain, zero forbidden executables.
  Paper untouched. Nothing pushed. Commits local on
  tnn-native-lab.
