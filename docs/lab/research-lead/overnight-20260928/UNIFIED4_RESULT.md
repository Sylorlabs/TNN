# UNIFIED4 RESULT: H-UNIFIED4 SURVIVES (16/16)

**Date:** 2026-09-29
**Prereg:** PREREG_UNIFIED4.md (commit 9dc510629, frozen before implementation)
**Implementation:** unified4_learn.zag (this directory; `unified3_learn.zag` untouched)
**Raw evidence:** UNIFIED4_RAW_OUTPUT.txt (md5 154d24b3d53ebce9c1739c998a89bc1f, 3/3 byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere.

## Verdict: H-UNIFIED4 SURVIVES (16/16)

The H-UNIFIED3 red-team downgrade (X-U3-1 authority spoofing) is
repaired. The revision channel is now structurally operator-only:
`route_line` (the stream entry point) can never return code 6, so the
adversary's exact X-U3-1 fixture is neutralized, while the legitimate
operator correction path still works.

## What was built

`unified4_learn.zag` = `unified3_learn.zag` copied verbatim, then:

**1. The `!` marker is inert on the stream path (X-U3-1 repair).**
`route_line` NEVER returns code 6. The `!`-detection stays, but the
mapping changed: `!` + remainder classifying as CAUS_LEARN (2) now
routes 2 (ordinary gated causal learn) instead of 6. Any other shape
with the marker withholds exactly as in H-UNIFIED3. The byte-33 marker
is no longer a security boundary on the stream path.

**2. `operator_route`: the sole path to revision (new function).**
Reachable only by direct call; requires the leading `!` marker
(explicitness); classifies the stripped remainder by reusing
`route_line` itself (no duplicated logic); code 2 maps to 6
(CAUS_REVISE), anything else withholds. Authority is a property of the
call path, never of a self-asserted byte.

**3. `handle_caus_learn`: defensive `!` strip.** One `if` at entry
strips a leading `!` before parsing, so the stream dispatch pattern
`route_line("!...")==2` + `handle_caus_learn(W,"!...")` parses the
stripped remainder coherently. No valid stream line begins with byte
33, so nothing else changes.

**4. `handle_caus_revise`: unchanged.** Still strips `!`, still
bypasses the gate for the trusted operator, still honest accounting.
Now reachable only via `operator_route`.

**5. `main()`: K-U3-1 block replaced; everything else verbatim.**
K-U3-1's expectation `route_line("!...")==6` is SUPERSEDED (it was the
vulnerability). Its behavioral content (poison-first corrected via the
explicit channel) is preserved in K-U4-2 through the authenticated
call path. The 12 original H-UNIFIED2 checks and K-U3-2 are byte-
identical in behavior.

## Frozen bar results

- **K-U4-1 PASS:** Truth installed via stream (stored=1, confident
  s1=0). Adversary's exact X-U3-1 line `!1,0,0>9,9;1,0,0>9,9` through
  `route_line` -> code 2 (CAUS_LEARN, NOT 6), reason "leading '!'
  ignored on stream path". Dispatched as ordinary stream learn: 0
  stored, 2 quarantined (gate consulted, quarantine delta 2). Truth
  still confident s1=0, active rule count 1. No rule CONFLICTED, no
  attacker rule installed. The gate bypass is unreachable from stream
  bytes.
- **K-U4-2 PASS:** Stream poison first (stored=1, poison ACTIVE s1=9).
  Late stream truth quarantined (stored=0, quarantine delta=2; gate
  unchanged). `operator_route("!1,0,0>1,0;1,0,0>1,0")` -> 6;
  `handle_caus_revise` -> stored=2 (poison R0 CONFLICTED, corrected
  rule R1 learned); active==1; `cpredict` confident s1=0. Stream truth
  then corroborates (stored=0, quarantined=0). Poison-first is still
  correctable, now only through the authenticated call path.
- **K-U4-3 PASS:** All 12 original H-UNIFIED2 frozen checks and K-U3-2
  (capacity refuse-with-warning) pass unchanged. `route_line` behavior
  is identical for all non-`!` inputs by construction; none of these
  blocks feed `!`-prefixed lines.
- **K-U4-4 PASS:** 3/3 runs byte-identical (cmp),
  md5 154d24b3d53ebce9c1739c998a89bc1f.
- **K-U4-5 PASS:** `operator_route("!1,0,0>1,0;1,0,0>1,0")` -> 6;
  `operator_route("!abc>cba")` -> 0; `operator_route("1,0,0>1,0")`
  -> 0 (marker required); `operator_route("!hello")` -> 0.

Total: 16/16 (12 originals + K-U4-1 + K-U4-2 + K-U4-5 + K-U3-2).

## Source audit (self)

- `route_line` contains no path to code 6: the only `code=6`
  assignment in the file is inside `operator_route`, which is not
  reachable from `route_line` (it calls `route_line` on the stripped
  body; `route_line` never calls `operator_route`). Verified by grep:
  `code=6` appears once (operator_route); `route_line`'s is_revise
  branch assigns only 2 or 0.
- `handle_caus_revise` is called only from `main()` under
  `if(or6==6)` after `operator_route`. No other call sites.
- No test-answer literals in the new code; the `!` checks
  (`line[0]==33`) are structural.

## Honest limitations (carried from prereg)

1. The operator path is trusted BY CONSTRUCTION (separate call path in
   this harness). In a deployment it MUST be a separate authenticated
   channel (distinct fd/socket/API role). The byte-33 marker is not
   authentication anywhere; on the operator path it is a syntactic
   explicitness requirement.
2. An adversary able to invoke `operator_route` directly (i.e., who IS
   the operator or has compromised the runtime) is outside the threat
   model; that is equivalent to editing the binary.
3. The unlabeled stream remains first-writer-wins; legitimate stream
   corrections are still quarantined (documented, unchanged).
4. Capacity policy remains refuse-with-warning (Repair B intact). The
   X-U3-2 composition concern now reduces to the pre-existing X-U2-2b
   boundary: stream `!` lines are stripped to ordinary stream lines,
   which could already fill the store via the normal path.

## Classification

Bounded L2 integration repair, not L3. Closes the X-U3-1 downgrade by
making the revision channel structurally operator-only; preserves the
poison-first correction capability through the authenticated path.
Recommended follow-up: independent red team re-runs the X-U3-1 fixture
against unified4 (it is now the K-U4-1 regression test) and attacks
the new threat-model claim (call-path separation).
