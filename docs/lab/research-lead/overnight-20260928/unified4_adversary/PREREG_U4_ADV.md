# PREREG H-UNIFIED4 RED TEAM (X-U4-1..X-U4-4) — FROZEN

**Date:** 2026-09-29
**Status:** FROZEN. No attack code exists yet. The result commit must
strictly descend from this prereg commit.
**Target:** `unified4_learn.zag` (H-UNIFIED4, prereg 9dc510629,
implementation 7048fc3e5). Claim under test: the X-U3-1 authority-
spoofing downgrade is closed by call-path separation — `route_line`
(the stream entry point) NEVER returns code 6, and
`handle_caus_revise` is reachable ONLY via `operator_route` (direct
call). Authority is a property of the call path, never of a
self-asserted byte.
**Stance:** Assume the claim is false. Every attack below is a genuine
attempt to break it.
**Purity:** Pure Zag. No Python anywhere, including harnesses and
analysis. No em dashes in loop documentation.

## Threat model (inherited from PREREG_UNIFIED4, frozen)

The ADVERSARY is a writer on the unlabeled input stream: exactly the
byte sequences dispatched via `route_line`. The OPERATOR path
(`operator_route`, direct call) is trusted by construction and is NOT
an attack surface for X-U4-1/X-U4-2. A bypass must be reachable from
stream bytes alone.

## Attack X-U4-1: stream bytes reaching the revise handler

**Method:** Install a verified truth rule via the stream
(`handle_caus_learn(W,"1,0,0>1,0;1,0,0>1,0")`, stored=1, cpredict
confident s1=0). Then feed an adversarial battery of `!`-prefixed and
`!`-adjacent byte sequences through `route_line` (the stream entry
point), dispatching exactly as `main()` does (`if(code==2)` then
`handle_caus_learn` with the same line). After the battery, re-check
the truth rule. The harness is `u4_adv.zag`: mechanism functions
copied verbatim from `unified4_learn.zag` (lines 1-1182), only
`main()` replaced.

**Battery (each fed through `route_line`, dispatched per main):**
1. `!` (lone marker)
2. `!!` (double marker, empty remainder)
3. `!1,0,0>9,9;1,0,0>9,9` (adversary's exact X-U3-1 fixture)
4. `!!1,0,0>9,9;1,0,0>9,9` (double marker + valid episodes)
5. `!1,0,0>9,9` (single segment: needs 2+ segs)
6. `!abc>cba` (non-numeric fields)
7. `!1,0,0>9,9;1,0,0>9,9;` (trailing separator: empty segment)
8. `!;1,0,0>9,9` (leading empty segment)
9. `!1,0,0>>9,9;1,0,0>9,9` (double `>`)
10. `! 1,0,0>9,9;1,0,0>9,9` (space after marker)
11. `!` + 100 contradicting episode segments (long line; gate must
    quarantine, not bypass)
12. `!1,0,0>9,9;1,0,0>9,9` a second time after truth installed
    (repeat of the exact spoof)

**Recorded per item:** route code returned; stored/quarantined counts
when dispatched.

**KILL iff ANY of:** (a) any battery item makes `route_line` return
code 6; (b) `handle_caus_revise` executes on any stream-fed input;
(c) after the battery, the truth rule is altered: cpredict(1,0,0) not
confident s1=0, or active rule count != 1, or any rule marked
CONFLICTED. Otherwise the attack FAILS (reported honestly).

## Attack X-U4-2: alternative path to `handle_caus_revise`

**Method:** Static structural audit of `unified4_learn.zag` plus a
runtime cross-check.

(a) Enumerate every call site of `handle_caus_revise` (grep). KILL iff
any call site exists other than the single guarded dispatch
`if(or6==6){...handle_caus_revise...}` fed by `operator_route`.
(b) Enumerate every site that can produce code 6: grep `return 6` and
all `code=` assignments inside `route_line`. KILL iff any `return 6`
exists outside `operator_route`, or any `route_line` branch can yield
6.
(c) Call-graph check: list every caller of `operator_route` (grep).
KILL iff `operator_route` is called from `route_line`, from any
function reachable from `route_line`, or from any stream-dispatch code
in `main()` (as opposed to the delimited operator sections).
(d) Verify `operator_route`'s internal reuse of `route_line` cannot be
abused: it classifies the operator's own stripped body; confirm the
`!`-marker requirement (`line[0]==33`) and the `inner==2` gate are both
necessary for the `return 6`. (Informational; the operator path is
trusted, so a finding here is a robustness note, not a bypass.)

**KILL iff (a), (b), or (c) finds a stream-reachable path to code 6 /
`handle_caus_revise`.** Otherwise the attack FAILS.

## Attack X-U4-3: regression in the 12 original checks + K-U3-2

**Method:** Compile `unified3_learn.zag` and `unified4_learn.zag` with
the same toolchain (znc 2026.07.0-dev). Run both. Extract from each raw
output the sections for the 12 original H-UNIFIED2 checks
(K-U1, K-U2a, K-U2b, K-U2c, K-U3, K-U4a, K-U4b, K-U5, K-A, K-U2-1,
K-U2-3a, K-U2-3b) and K-U3-2 (capacity refuse-with-warning). Diff them.
The K-U3-1 block was explicitly SUPERSEDED and replaced by
K-U4-1/K-U4-2/K-U4-5; that region is excluded from the diff by design.

**DOWNGRADE (not kill) iff** any compared section differs. A
regression would narrow the "no regression" claim, not reopen X-U3-1.
Otherwise the attack FAILS (no regression found).

## Attack X-U4-4: source audit of the new/changed code

**Method:** Manual audit of the diff `unified3_learn.zag` vs
`unified4_learn.zag`, confined to changed regions: the `is_revise`
branch in `route_line`, the new `operator_route`, the defensive `!`
strip in `handle_caus_learn`, `handle_caus_revise` (unchanged, verify
byte-identical), and the replaced `main()` blocks.

(a) KILL iff any test-answer literal or fixture-specific special-case
appears in the new/changed mechanism code (the `line[0]==33` checks are
structural, not literals; verify no episode-content literals).
(b) KILL iff the `handle_caus_learn` defensive strip can diverge from
`route_line`'s classification: demonstrate a concrete input where
`route_line` returns 2 but the stripped parse in `handle_caus_learn`
sees different fields. (Both strip exactly one leading `!`; the fuzz
battery in X-U4-1 cross-checks this at runtime.)
(c) KILL iff the `return 6` in `operator_route` is reachable without
both the marker check and the `inner==2` classification gate.
(d) Informational: note that the builder's self-audit grepped `code=6`
while the actual literal is `return 6;` (methodology nit; the single-
site conclusion is verified independently here).

**KILL iff (a), (b), or (c) holds.** Otherwise the attack FAILS.

## Verdict rule

- Any KILL in X-U4-1, X-U4-2, or X-U4-4: H-UNIFIED4 is KILLED (the
  X-U3-1 closure claim is broken).
- DOWNGRADE in X-U4-3 only: H-UNIFIED4 is DOWNGRADED (repair stands,
  "no regression" claim narrowed).
- All attacks fail: H-UNIFIED4 SURVIVES this red team.

## Deliverables

- This prereg (frozen).
- `u4_adv.zag` (mechanism verbatim, attack `main()`), `U4_ADV_RAW.txt`
  (raw evidence, md5, 3/3 byte-identical runs), `U4_ADV_RESULT.md`
  (this report).
- Regression diff evidence for X-U4-3.

## Commit plan

1. This prereg, frozen alone.
2. Attack harness + raw evidence + result doc.
3. No amendment unless a harness bug is found; amendments will be
   transparent and will not change kill criteria.
