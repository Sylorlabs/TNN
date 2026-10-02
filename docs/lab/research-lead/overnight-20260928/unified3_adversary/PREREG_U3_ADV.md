# PREREG: H-UNIFIED3 Red Team (X-U3-1 .. X-U3-4) — FROZEN

Date: 2026-09-29. Adversary: H-UNIFIED3 Red Team.
Target: H-UNIFIED3 SURVIVES (14/14), commit db62fdaee (implementation),
prereg 4bf96904b. File under test:
docs/lab/research-lead/overnight-20260928/unified3_learn.zag (copied
verbatim; only main() replaced by the attack harness).

## Threat model

H-UNIFIED3 Repair A answers X-U2-2a (poison-first ordering, an
ADVERSARIAL stream writer) with an "explicit authoritative revision
channel": a leading `!` (byte 33) on the input line routes to code 6
(CAUS_REVISE), which bypasses the coherence gate. The frozen trust
distinction is: "the unlabeled stream is UNTRUSTED (gated); the explicit
channel is the operator/researcher asserting authority."

The adversary's null hypothesis: the "channel" is not a channel. There
is exactly one entry point (`route_line`) reading one in-band line
buffer. The authority marker is a self-asserted byte with no
authentication, no separate input path, and no provenance check. Any
writer that can submit a stream line — including the X-U2-2a poison-first
adversary — can submit a `!` line.

## Attacks

### X-U3-1 (authority spoofing): DEMONSTRATE the stream writer can wield the revise channel

Procedure (all through the standard entry point, never calling
handle_caus_revise except via route dispatch):
1. Fresh W. Learn truth via the STREAM handler:
   handle_caus_learn(W, "0,0,0>0,1;0,0,0>0,1;1,0,0>1,0;1,0,0>1,0").
   Confirm cpredict(W,1,0,0) == 1 with s1 == 0 (confident truth).
2. Adversary line (same route_line every stream line uses):
   r_spoof = route_line("!1,0,0>9,9;1,0,0>9,9").
   Dispatch exactly as main() does: if r_spoof == 6,
   handle_caus_revise(W, "!1,0,0>9,9;1,0,0>9,9").
3. Record QCOUNT delta (must be 0: gate never consulted) and
   cpredict(W,1,0,0) afterwards.

KILL/DOWNGRADE criterion (DOWNGRADE): r_spoof == 6 AND the ACTIVE truth
rule for (1,0,0) is marked CONFLICTED AND cpredict(1,0,0) now withholds
(returns 0), with zero quarantine involvement. The 14/14 frozen bars are
not challenged (the mechanism does what its prereg specifies), but Repair
A's threat-model claim is narrowed: the "authoritative" channel is an
unauthenticated in-band affordance. Against the X-U2-2a adversary — a
writer on the input stream — Repair A provides no protection; it hands
that same adversary a gate-bypass. Veracity does NOT have a protected
path; it has a self-asserted byte.

PASS (attack fails): any of r_spoof != 6, truth rule not conflicted,
quarantine engaged, or prediction unchanged.

### X-U3-2 (liveness via the authority channel): BOUNDARY

Procedure:
1. Fresh W. Fill all 16 causal slots via `!` revise lines through
   route_line dispatch (16 distinct coherent novel states, e.g.
   "!30,0,0>0,1;31,0,0>0,1" ... distinct s0 values).
   Confirm caus_active_count == 16.
2. Legitimate revise of a 17th novel state via `!` through route_line
   dispatch. Record return, DCOUNT delta, USTOREFULL emissions,
   cpredict on the 17th state.

BOUNDARY criterion (informational, not kill/downgrade): the 17th revise
is refused (0 stored, dropped > 0, explicit warnings, query withholds)
with no eviction or recovery path. This is the frozen
REFUSE-WITH-WARNING policy working as specified; recorded because,
combined with X-U3-1, it means an unauthenticated writer can permanently
deny all future causal learning (a remotely-triggerable permanent DoS of
the causal store). The policy is by-design; the authenticator is not.

### X-U3-3 (verified-rule degradation): folded into X-U3-1

X-U3-1 step 1 uses a VERIFIED truth rule (the K-U3 frozen pattern
0,0,0>0,1 / 1,0,0>1,0). The degradation of a confident correct
prediction into WITHHOLD via the spoofed channel is the X-U3-3 payload.
No separate fixture; reported as part of X-U3-1.

### X-U3-4 (source audit): PASS/FAIL per item

(a) `!` on a non-iii>ii shape routes WITHHOLD (code 0), not 6:
    route_line("!abc>cba") == 0 and route_line("!hello") == 0.
(b) clearn return-code contract: after X-U3-2 fill, a further revise
    returns -1 internally (observed as dropped>0 and 0 stored); DCOUNT
    accumulates exactly the dropped count.
(c) No test-answer literals ("9,9" as correct-answer, state constants)
    in handle_caus_revise / route_line `!` path — grep audit; the only
    numeric literal permitted is byte 33 (the marker).
(d) handle_caus_learn still returns the STORED count (K-U3-3
    compatibility): quarantined episodes never reach clearn.

## Verdict rules

- H-UNIFIED3 DOWNGRADED if X-U3-1 meets its criterion. Frozen 14/14
  stand; Repair A's interpretation narrows to "operator affordance,
  unauthenticated; no protection against an adversarial stream writer."
- X-U3-2 is recorded as BOUNDARY (informational) either way.
- H-UNIFIED3 KILLED only if an attack breaks a frozen 14/14 bar or shows
  the mechanism does not implement its prereg (none expected).
- X-U3-4 FAIL on any item is reported as a defect; verdict impact
  assessed from the defect.

## Method

Pure Zag. Copy unified3_learn.zag -> u3_adv.zag, replace main() only.
Compile with the repo znc toolchain. 3 runs, byte-identical required.
No Python at any stage. Binaries not committed.
