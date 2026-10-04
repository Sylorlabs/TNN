# PREREG H-UNIFIED4: Authenticated Revision Channel (X-U3-1 Repair)

**Date:** 2026-09-29
**Status:** FROZEN. No implementation exists yet. Any implementation commit must strictly descend from this commit.
**Base:** `unified3_learn.zag` (H-UNIFIED3, red-team report at `279ce04f3`), copied verbatim then repaired.
**Target:** `unified4_learn.zag` (new file; `unified3_learn.zag` untouched).
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.

## Background

H-UNIFIED3 SURVIVES (14/14) but was DOWNGRADED by independent red team
(unified3_adversary/ADVERSARY_REPORT_H_UNIFIED3.md, prereg 44c1dbe61,
report 279ce04f3). One downgrade, no kill. The frozen 14/14 bars still
pass; the downgrade kills the threat-model claim of Repair A.

- **X-U3-1 (authority spoofing): SUCCEEDS.** The `!` revision channel is
  unauthenticated. The adversary's line `!1,0,0>9,9;1,0,0>9,9` went
  through `route_line` -- the single standard entry point every stream
  line uses -- routed 6 (CAUS_REVISE), bypassed the coherence gate
  (quarantine delta 0), marked the verified ACTIVE truth rule
  CONFLICTED, and installed the attacker's episode as a new rule:
  `cpredict(1,0,0)` returned the attacker's s1=9 confidently. Full
  integrity takeover via a self-asserted byte. Repair A is an
  unauthenticated operator affordance, not a protected veracity path.
- **X-U3-2 (liveness): BOUNDARY CONFIRMED.** Refuse-with-warning works
  as specified; composed with X-U3-1 it was a remotely-triggerable
  permanent denial of the causal store.
- **X-U3-4 (source audit): ALL PASS.** No hardcoding; accounting honest.

Repair B (honest capacity accounting) survives the red team intact.

## Threat model (frozen)

- The ADVERSARY is a writer on the unlabeled input stream: exactly the
  byte sequences dispatched via `route_line`. The X-U2-2a / X-U3-1
  adversary never has any other input path.
- The OPERATOR is a distinct party whose input is dispatched via a
  separate call path (`operator_route`). In this harness `main()` plays
  both roles in clearly-delimited sections, modeling a deployment where
  the stream arrives on an unauthenticated socket and operator commands
  arrive on an authenticated one.
- SECURITY PROPERTY UNDER TEST: no byte sequence fed through
  `route_line` can cause `handle_caus_revise` to execute or bypass the
  coherence gate. Authority is a property of the call path, never of a
  self-asserted byte value.

## Repair design (frozen)

### 1. The `!` marker is inert on the stream path

`route_line` NEVER returns code 6. The existing `!`-detection stays,
but the mapping changes:

- `!` + remainder classifying as CAUS_LEARN (2) -> code 2, ordinary
  gated causal learn. The remainder faces the coherence gate exactly
  like any stream line. (Previously: code 6, gate bypassed.)
- `!` + any other shape -> WITHHOLD (0), exactly as in H-UNIFIED3.

The byte-33 marker is no longer a security boundary anywhere on the
stream path. The adversary's exact X-U3-1 fixture now routes 2 and is
quarantined on contradiction.

### 2. `operator_route`: the sole path to revision (new function)

```text
fn operator_route(line:[]u8)i32
```

- Reachable only by direct call. `route_line` cannot return 6, so no
  stream byte sequence can invoke the revise handler. This is enforced
  structurally (call path), not by byte inspection.
- Requires the leading `!` marker (explicitness); without it, WITHHOLD
  with an explicit reason.
- The stripped remainder is classified by reusing `route_line` itself
  (no duplicated classification logic); code 2 maps to 6 (CAUS_REVISE),
  anything else WITHHOLDS.
- `main()` dispatches `if(or==6){handle_caus_revise(W,line);}` exactly
  as it previously dispatched on `route_line`'s 6.

### 3. `handle_caus_learn`: defensive `!` strip

One `if` at entry strips a leading `!` before parsing, so the stream
dispatch pattern `route_line("!...")==2` +
`handle_caus_learn(W,"!...")` parses the stripped remainder coherently.
No valid stream line begins with byte 33, so this changes nothing else.

### 4. `handle_caus_revise`: unchanged

Still strips `!`, still bypasses the coherence gate, still uses
`clearn`'s native revision semantics with honest accounting. It is now
reachable only via `operator_route`.

### 5. `main()`: K-U3-1 block replaced; everything else verbatim

The K-U3-1 block is replaced by K-U4-1, K-U4-2, K-U4-5 blocks (below).
All other blocks (the 12 original H-UNIFIED2 checks, K-U3-2 capacity,
final verdict) stay byte-identical in behavior. `route_name(6)` stays
("CAUS_REVISE").

## Explicit supersession

K-U3-1's expectation `route_line("!1,0,0>1,0;1,0,0>1,0")==6` is
SUPERSEDED by K-U4-1/K-U4-2. That expectation IS the X-U3-1
vulnerability (stream bytes invoking the revise handler); keeping it to
pass a frozen bar would be dishonest. Its behavioral content --
poison-first corrected via the explicit channel -- is preserved in
K-U4-2 through the authenticated call path.

## Frozen kill bars

### K-U4-1: stream `!` spoof neutralized (X-U3-1 regression)

Fresh workspace W5. Uses the adversary's exact fixture:

1. Install truth via stream:
   `handle_caus_learn(W5,"1,0,0>1,0;1,0,0>1,0")` -> stored=1;
   `cpredict(W5,1,0,0)` confident s1=0.
2. Adversary line through the stream entry point:
   `route_line("!1,0,0>9,9;1,0,0>9,9")` -> returns 2 (NOT 6).
3. Dispatched as ordinary stream learn:
   `handle_caus_learn(W5,"!1,0,0>9,9;1,0,0>9,9")` -> stored=0,
   quarantine delta=2 (gate consulted).
4. `cpredict(W5,1,0,0)` still confident s1=0; active rule count is 1
   (no CONFLICTED truth, no attacker rule).

PASS iff route code is 2, stored=0, quarantine delta=2, truth intact
and confident, active==1. KILL iff the spoof reaches the revise
handler (code 6) or alters the truth rule.

### K-U4-2: legitimate operator revision corrects poison-first (X-U2-2a)

Fresh workspace W6 (mirrors K-U3-1 steps, operator path authenticated):

1. Stream poison: `handle_caus_learn(W6,"1,0,0>9,9;1,0,0>9,9")` ->
   stored=1; `cpredict(W6,1,0,0)` confident s1=9 (poison ACTIVE).
2. Late stream truth quarantined (gate unchanged):
   `handle_caus_learn(W6,"1,0,0>1,0;1,0,0>1,0")` -> stored=0,
   quarantine delta=2; poison still confident s1=9.
3. Operator revision: `operator_route("!1,0,0>1,0;1,0,0>1,0")` -> 6;
   `handle_caus_revise(W6,"!1,0,0>1,0;1,0,0>1,0")` -> stored=2
   (poison CONFLICTED, corrected rule learned); active==1;
   `cpredict(W6,1,0,0)` confident s1=0.
4. Stream truth now corroborates:
   `handle_caus_learn(W6,"1,0,0>1,0;1,0,0>1,0")` -> stored=0,
   quarantine delta=0.

PASS iff all four hold. KILL iff the authenticated operator path
cannot correct poison-first state.

### K-U4-3: no regression

All 12 original H-UNIFIED2 frozen checks (K-U1, K-U2a, K-U2b, K-U2c,
K-U3, K-U4a, K-U4b, K-U5, K-A, K-U2-1, K-U2-3a, K-U2-3b) plus K-U3-2
(capacity refuse-with-warning) pass unchanged. Their main() blocks are
copied verbatim; none feed `!`-prefixed lines, and `route_line`
behavior is identical for all non-`!` inputs by construction.

### K-U4-4: determinism

Three full runs of the final binary are byte-identical (cmp). md5
recorded in the result doc.

### K-U4-5: operator channel shape requirements

- `operator_route("!1,0,0>1,0;1,0,0>1,0")` -> 6.
- `operator_route("!abc>cba")` -> 0 (remainder not iii>ii).
- `operator_route("1,0,0>1,0")` -> 0 (marker required).
- `operator_route("!hello")` -> 0.

PASS iff all four hold.

## What is NOT changed

- The coherence gate, `clearn` (1/0/2/-1 contract), Repair B accounting,
  `handle_caus_revise` internals, procedure/bridge stores, AMBIGUOUS
  code 5, subset direct discovery, and the query path: behavior
  identical to H-UNIFIED3.
- The X-U3-2 composition concern now reduces to the pre-existing
  X-U2-2b boundary: stream `!` lines are stripped to ordinary stream
  lines, which could already fill the store via the normal path.
  Refuse-with-warning still governs; no new denial surface is added.

## Honest limitations (frozen)

1. The operator path is trusted BY CONSTRUCTION (separate call path in
   this harness). In a deployment it MUST be a separate authenticated
   channel (distinct fd/socket/API role). The byte-33 marker is not
   authentication anywhere; on the operator path it is a syntactic
   explicitness requirement, nothing more.
2. An adversary able to invoke `operator_route` directly -- i.e., who
   IS the operator or has compromised the runtime -- is outside the
   threat model. That is equivalent to editing the binary.
3. The unlabeled stream remains first-writer-wins; legitimate stream
   corrections are still quarantined (documented, unchanged).
4. Capacity policy remains refuse-with-warning (Repair B intact).
   Principled eviction is future work (H-MEM lane).

## Commit plan

1. This prereg (frozen).
2. Implementation: `unified4_learn.zag` + `UNIFIED4_RAW_OUTPUT.txt`
   (raw evidence, 3 runs) + `UNIFIED4_RESULT.md`.
3. No amendment unless a harness bug is found; any amendment will be
   transparent and will not change kill criteria.

## Classification sought

Bounded L2 integration repair, not L3. Closes the X-U3-1 downgrade by
making the revision channel structurally operator-only; preserves the
poison-first correction capability through the authenticated path.
