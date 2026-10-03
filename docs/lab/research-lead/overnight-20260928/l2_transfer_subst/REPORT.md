# REPORT: L2-TRANSFER-SUBST (SUBSTITUTE in the Arithmetic Substrate)

Worker: L2 Transfer-Subst Worker (subagent, 2026-10-02).
Prereg: `l2_transfer_subst/PREREG.md`, frozen alone at commit
733c2d7e0 before any implementation existed. Zero amendments:
every hand-derived number in the prereg matched the first build
exactly, including A_SEARCH=8/A_EXEC=3 for FULL, 58/8 for
ABLATE-N, and 54/7 for FRESH.

## Verdict

**L2-TRANSFER-SUBST-COMPLETE.** All thirteen kill bars K-0
through K-12 PASS, no falsifier fired, 3/3 byte-identical.

## What was built

The C298 SUBSTITUTE operator file (`learner.zag`, 825 lines)
copied byte-identically into the arithmetic lane (sha256
fdf33e3869969ffb38dc5334ddb184cad8283afcf23164f56040db554c2d69c1,
identical to the C298 hash pinned in the prereg), plus a new
environment side (`world.zag`: 9 price facts over subtotal
states; the $55 meal-deal price fact is the kill target) and a
new experiment side (`driver.zag`: five arms + kill-bar
evaluation with arithmetic queries and expectations), assembled
as `cat learner.zag world.zag driver.zag > arith_full.zag`
(1226 lines) and compiled with the pinned znc to `arith_bin`
(build exit 0, warnings only).

The learner holds a SUM MAP m over price facts (total 90 =
15 + 55 + 20 via the learned addition structure over subtotal
states 0 -> 15 -> 70 -> 90) and an independently learned bundle
piece n (the itemized decomposition 15 -> 40 -> 70, different
relations, disjoint facts). After the teach-then-kill of price
fact 1, the unchanged operator fires its unchanged trigger
logic: stale licensing detection at hop 1, endpoint-matching
piece search in node-id order (n matches 15 -> 70, all facts
live), execution verification of the assembled chain to
terminal 90, type-16 adapted-from promotion of m2, stale
retirement of m. The substituted sum verifies by real execution
to the hand-derived correct total 90.

## Kill-bar results (from arith_run1.txt, reproduced in runs 2, 3)

- K-0 (commit-order self-check): prereg commit 733c2d7e0
  contains PREREG.md + NAMECHECK.md only and strictly precedes
  the implementation commit in git log order. PASS.
- K-1 (n prior and independent): INTERSECT=0, M-OK ans=90
  via=0, N-OK ans=70 via=1, and shell check N-OK (line 8)
  precedes KILL (line 10). PASS.
- K-2a (ablate n): ABLATE-N t16=0, ans=90 via=3, A_SEARCH=58
  >= 5*8=40. The adapted m2 cannot exist without n; the
  learner rebuilds from scratch at 7.25x the substitution
  search cost (58 vs 8). PASS.
- K-2b (ablate m prefix): ABLATE-M ans=-2, t16=0, NM=3.
  Killing facts 0 and 1 leaves no (0,15) piece and no rebuild
  path. PASS.
- K-3 (fresh learner): FRESH t16=0, ans=90 via=0,
  A_SEARCH=54 >= 40 (6.75x). PASS.
- K-4 (white-box trace): all six frozen lines present verbatim:
  `SUB-STALE m=0 hop=1 fact=1`,
  `SUB-CAND id=1 s=15 e=70 flive=2 MATCH`,
  `SUB-BUILD rels=7,8,8,7 facts=0,3,4,2`, `SUB-VERIFY term=90`,
  `SUB-PROMOTE m2=3`, `ANS via=3 val=90`. The trace shows which
  piece was chosen (MAP1, the bundle piece) and why (endpoints
  15 -> 70, 2/2 facts live), all read from learner state. PASS.
- K-5 (no-substitute control fails): NO-SUB ans=-2 with t16=3:
  ET-TRUNC t=3 from=0, ET-EXTEND e=4 from=2, ET-EXTEND e=5
  from=3 all fired and still failed (best reach 210, 40, 15;
  none is 90). Extend/truncate provably cannot repair a
  middle-segment death in this substrate either. PASS.
- K-6 (stale retired, not reused): FULL MAP0 live=0;
  post-query ans=90 via=3 (through m2, with m retired). PASS.
- K-7 (provenance, zero new types): FULL t16=2 with exactly
  {3->0, 3->1}; t15=2 with exactly {0->1, 1->0} (co-use written
  by the learner's deliver routine on episode success);
  LINK14 34->3 exists (answer node to delivering MAP);
  other=0 (no edge type outside {14,15,16}). PASS.
- K-8 (determinism): arith_run1/2/3.txt sha256 identical:
  ee43599d79ede190fae959392e4931c7d4554adce53e58f9464e2e98feddb027.
  PASS.
- K-9 (audit): all 8 frozen patterns return 0 hits on
  learner.zag (`7,8,8,7`, `0,3,4,2`, `(15,8,40)`, `(15,7,70)`,
  `_MODE`, case-insensitive `bridge`, case-insensitive
  `python`, `as *i32`). PASS.
- K-10 (FULL success): ans=90 via MAP3; MAP3 relseq
  [7,8,8,7], start 0, end 90, live 1, printed from learner
  state. PASS.
- K-11 (no-retuning): sha256(learner.zag) =
  fdf33e3869969ffb38dc5334ddb184cad8283afcf23164f56040db554c2d69c1,
  byte-identical to the C298 file (cmp clean); every constant
  in the prereg section-4 list is therefore unchanged between
  instantiations; world.zag/driver.zag differ from C298's only
  in the fact table, relation ids, MAP inventory, kill, query,
  and hand-derived expectations. Zero operator constants
  changed, zero edits required. F-RETUNE silent. PASS.
- K-12 (chain regression): re-running the frozen C298 binary
  `l2_substitute/sub_bin` reproduces its frozen run digest
  198ef5c6d9bdc2dae17182cb4f9a7b1c89b6f2e53208243b7bd2b4474c38f261
  exactly, confirming the shared operator file still passes
  C298's core assertions in the chain substrate. PASS.

No falsifier fired: F-NO-CAND, F-WRONG-M2, F-STALE-REUSE,
F-CTRL-PASS, F-ABLN-ADAPT, F-ABLM-PASS, F-FRESH-ADAPT,
F-EDGE-NEW, F-RETUNE, F-AUDIT, F-NONDET, F-PYTHON all silent.

## Key numbers

- Substitution cost (FULL adapt phase): A_SEARCH=8,
  A_EXEC=3. One candidate evaluated (MAP1, the bundle piece),
  one verification exec to terminal 90. Identical to C298's
  FULL cost: the operator's scan structure does not depend on
  the substrate.
- Ablated-n rebuild cost (ABLATE-N): A_SEARCH=58, A_EXEC=8.
  Ratio 58/8 = 7.25x (frozen bar >= 5x).
- Fresh-rebuild cost (FRESH): A_SEARCH=54, A_EXEC=7. Ratio
  54/8 = 6.75x (frozen bar >= 5x).
- Provenance: 2x type-16 (3->0, 3->1), 2x type-15 (0->1, 1->0),
  LINK14 answer->m2, 0 other edge types.
- sha256 (runs):
  ee43599d79ede190fae959392e4931c7d4554adce53e58f9464e2e98feddb027 x3.
- sha256 (learner.zag, shared):
  fdf33e3869969ffb38dc5334ddb184cad8283afcf23164f56040db554c2d69c1.
- sha256 (arith_bin):
  e22349b0105e3b9db8fd344782fe6ce7882c9be8700e3aea0b41733ed0af8a2e.
- sha256 (chain regression re-run):
  198ef5c6d9bdc2dae17182cb4f9a7b1c89b6f2e53208243b7bd2b4474c38f261
  (matches the frozen C298 digest).

## Shared vs substrate-specific, as executed

SHARED (byte-identical, zero changes): the entire operator,
including stale-licensing detection, node-id-ordered
endpoint-matching piece search, first-match selection, dedup,
execution verification, type-16 promotion, stale retirement,
iterative-deepening rebuild (L=1..4), TRUNCATE-ONE/EXTEND-ONE
controls, edge-type semantics, cost-counting rules, and the 5x
evaluation threshold. Constants shared verbatim: fact cap 32,
MAP cap 16, edge cap 64, answer-node cap 8, STALE sentinel 255,
retire reasons 1/2/3, Lmax 4, types 14/15/16, MAP tag 20,
answer-node id base 32, SUB_ON/ET_ON flag convention, output
machinery. No per-domain threshold, relation name, or tuning
constant was changed; no edit was required at all.

SUBSTRATE-SPECIFIC (world.zag + driver.zag only): the 9 price
facts over subtotal states (relations 7/8/9 glossed as ADD,
ITEMIZED-ADD, unrelated), the SUM MAP / bundle piece /
distractor inventory, the kill (fact 1, the $55 meal-deal price
fact), the query (0,90), and the hand-derived expectations
(total 90 = 15 + 55 + 20; bundle path 15 + 25 + 30 + 20 = 90).
The operator never names a relation, a MAP, a price, or a
total.

## Architecture accounting

- Cognition lines added: 401 new (world.zag 31, driver.zag 370;
  new files, nothing else touched). learner.zag (825 lines) is
  a byte-identical reuse of the C298 operator, not new
  cognition: the reuse IS the generality evidence.
- New hardcoded semantic cases: 0. New modes: 0. New bridges:
  0. New handlers: 0. New edge types: 0 (14/15/16 reused with
  their established semantics). New opcodes: 0.
- Capability-source delta: the SUBSTITUTE capability in the
  arithmetic substrate comes from the unchanged shared operator
  plus learned MAP state; no per-substrate researcher tuning
  anywhere in the substitution path.

## Why this is mechanism generality, not a chain-family trick

The operator file that passed C298's ten bars in the chain
substrate was copied without a single byte changed and passed
all thirteen bars here, in a substrate whose facts are price
steps over subtotal states, whose relations are arithmetic
operations, and whose kill removes a price from a sum. The
trigger logic (stale licensing check), the search discipline
(node-id order, endpoint match, all-facts-live, first match),
the verification discipline (real execution to the terminal,
never promote an unverified graph), the provenance discipline
(type-16 adapted-from, type-15 co-use, stale retirement), and
the cost discipline (identical A_SEARCH=8/A_EXEC=3 for the
substitution itself) all transferred without retuning. The
ablation contrasts transferred too: without the bundle piece
the learner rebuilds from scratch at 7.25x search cost; the
fresh learner pays 6.75x; extend/truncate genuinely fire and
still fail. The chain regression (K-12) confirms the shared
file did not regress in its original substrate.

## Files

All under `docs/lab/research-lead/overnight-20260928/l2_transfer_subst/`:

- PREREG.md (frozen, committed alone at 733c2d7e0; zero
  amendments)
- NAMECHECK.md (toolchain guard Step 0 record)
- REPORT.md (this file)
- learner.zag (byte-identical to l2_substitute/learner.zag)
- world.zag (arithmetic fact table + kill; environment side)
- driver.zag (five arms + kill-bar evaluation)
- arith_full.zag (assembled 1226-line build input)
- arith_bin (compiled binary)
- arith_compile.txt (build log; exit 0)
- arith_run1.txt, arith_run2.txt, arith_run3.txt (3/3
  byte-identical)

## Non-claims and bounds

- One arithmetic world family (summation with a middle
  price-fact kill) plus the chain regression. No generality
  claim beyond the five arms and K-12. Substitution with
  interface adaptation (endpoints not exactly matching) remains
  open future work.
- Does not claim Micah's full 12-criterion L3 bar; this is a
  mechanism-generality demonstration against thirteen frozen
  bars, framed as researcher-implemented, learner-triggered
  operator reuse across substrates.
- The kill was builder-designed, not adversary-designed.
  Sealed-adversary generality is open future work.
- The arithmetic semantics (price = obj minus sub, node id =
  subtotal) live in the world's state encoding, which is the
  substrate-specific part by design; the operator is
  state-encoding agnostic. "Real execution to the correct
  total" is the learner's chain_exec over the promoted MAP to
  terminal 90, the hand-derived correct total.
- Pure Zag, safebin toolchain, zero forbidden executables
  (`which python3` / `which python` return nothing; K-9 audit
  clean). Paper untouched. Nothing pushed. Commits local on
  tnn-native-lab.
