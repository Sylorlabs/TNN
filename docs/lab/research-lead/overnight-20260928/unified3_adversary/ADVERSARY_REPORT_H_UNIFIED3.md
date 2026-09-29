# H-UNIFIED3 Red Team: Adversary Report (X-U3-1..X-U3-4)

Date: 2026-09-29. Pure Zag, no Python at any stage.
Prereg: unified3_adversary/PREREG_U3_ADV.md, frozen at 44c1dbe61 BEFORE
any attack code was written or executed.
Harness: unified3_adversary/u3_adv.zag = unified3_learn.zag copied
verbatim (lines 1..1144); only main() replaced by attack scenarios.
Toolchain: znc 2026.07.0-dev (edition 2026).
Determinism: 3/3 runs byte-identical, md5 e470fb2959fe2e4ee2dbeacb3c28a841.

## Verdict: H-UNIFIED3 DOWNGRADED (not killed)

X-U3-1 meets its preregistered downgrade criterion, and the observed
effect is strictly stronger than the criterion's minimum. X-U3-2
confirms its boundary. X-U3-4 passes all four audit items. The frozen
14/14 bars are not challenged and not altered: the mechanism implements
its prereg exactly. What fails is Repair A's threat-model claim.

## X-U3-1 (authority spoofing): SUCCEEDS -> DOWNGRADE

Raw evidence (run1.txt, deterministic):

```
--- X-U3-1: spoofed '!' revision of a verified truth rule ---
causal: new rule R0 IF s0==0 AND a==0 THEN s1:=1
causal: new rule R1 IF s0==1 AND a==0 THEN s1:=0
ULEARN: 2 stored, 2 corroborated, 0 quarantined, 0 dropped (store full)
confident truth before: 1 (expect 1)
ROUTE [!1,0,0>9,9;1,0,0>9,9] -> CAUS_REVISE (explicit revision channel: authoritative causal revision)
spoof route code: 6 (expect 6)
causal: R1 CONFLICTED
causal: new rule R2 IF s0==1 AND a==0 THEN s1:=9
UREVISE: 2 stored, 0 corroborated, 0 dropped (store full)
revise stored=2 quarantine_delta=0 (expect 0: gate never consulted)
cpredict after: rc=1 s1=9
```

What this proves, step by step:

1. Truth "1,0,0>1,0" was installed via the STREAM handler
   (handle_caus_learn) and predicted confidently (s1=0).
2. The adversary's line "!1,0,0>9,9;1,0,0>9,9" went through route_line,
   the single standard entry point every stream line uses. The ONLY
   difference from an ordinary stream line is the self-asserted leading
   byte 33. It routed 6 (CAUS_REVISE).
3. Dispatched to handle_caus_revise exactly as main() dispatches it, the
   coherence gate was never consulted (quarantine delta 0).
4. The verified ACTIVE truth rule R1 was marked CONFLICTED, and the
   attacker's episode was installed as new rule R2: cpredict(1,0,0) now
   returns the ATTACKER's value s1=9 confidently (rc=1).

The prereg criterion required only degradation-to-withhold; the observed
outcome is a full integrity takeover: the stream writer replaced verified
truth with an attacker-chosen confident prediction, gate bypassed.

Why this is a downgrade of Repair A and not a kill of H-UNIFIED3:
the 14/14 frozen bars all test the mechanism as specified, and the
mechanism does exactly what the prereg specifies. What does not survive
is the threat-model claim the repair was built to address. X-U2-2a's
threat was an ADVERSARIAL WRITER ON THE INPUT STREAM (poison-first).
Repair A's answer was "veracity has a path; it is not the unlabeled
path" via "the operator/researcher asserting authority." The mechanism
enforces no such distinction: there is one line buffer, one route_line,
and authority is asserted by the writer itself prepending `!`. The
X-U2-2a adversary can therefore skip the stream race entirely and take
the "authoritative" path directly — Repair A does not protect against
the threat it was built for; it arms that same threat with a
gate-bypass. The honest statement is: Repair A is an unauthenticated
operator affordance (as the result doc's limitation 3 discloses), not a
protected veracity path. Against a benign operator distinct from the
stream it works as frozen-tested; against an adversarial stream writer
it provides nothing.

## X-U3-2 (liveness): BOUNDARY CONFIRMED (informational)

All 16 causal slots filled via `!` lines through route_line dispatch
(active=16). The 17th revise ("!99,0,0>0,1;98,0,0>0,1") routed 6,
returned 0 stored, dropped 2 with explicit USTOREFULL warnings, DCOUNT
delta exactly 2, and cpredict(99,0,0) withholds. No eviction path exists.

This is the frozen REFUSE-WITH-WARNING policy operating as specified:
verified knowledge is never evicted, refusals are loud, accounting is
honest (X-U3-4b/d below). Recorded as a boundary because, composed with
X-U3-1, it is triggerable by any unauthenticated stream writer: fill the
store with `!` junk and no future causal learning — stream or revise —
is ever possible again. The policy is by-design; the missing
authenticator turns it into a remotely-triggerable permanent denial of
the causal store.

## X-U3-3 (verified-rule degradation): demonstrated inside X-U3-1

The X-U3-1 target rule was the K-U3 frozen-pattern truth rule
(1,0,0>1,0), i.e. verified knowledge, and the outcome was stronger than
degradation (attacker takeover). No separate fixture needed.

## X-U3-4 (source audit): ALL PASS

(a) `!` on non-iii>ii shapes routes WITHHOLD: route_line("!abc>cba")==0,
    route_line("!hello")==0, route_line("!")==0. The marker cannot smuggle
    non-causal lines into code 6.
(b) clearn -1 contract holds: the X-U3-2 17th revise dropped exactly 2
    episodes and DCOUNT accumulated exactly 2. Return-code plumbing
    (1/0/2/-1) behaves as documented.
(c) No test-answer literals in the revise path: grep over route_line's
    bang section and handle_caus_revise finds no state/action/effect
    constants; the only numeric literal is byte 33 (the marker), checked
    structurally at two sites (route_line:785, handle_caus_revise:1038).
(d) handle_caus_learn returns the STORED count: contradicting stream
    episodes returned 0 stored with exactly 2 quarantined (honest
    accounting preserved; K-U3-3 compatibility intact).

## Revised classification

Bounded L2 integration with an explicit but unauthenticated revision
affordance and honest refuse-with-warning capacity accounting. Not L3
(unchanged). Repair B (honest capacity accounting) survives this red
team intact — the accounting was verified honest under adversarial fill.
Repair A survives as specified behavior but its threat-model claim is
narrowed: it is an operator affordance for a trusted operator, not a
protected path against the X-U2-2a adversary.

## Recommended follow-ups for the parent

1. Authenticate the revision channel or remove its authority claim:
   e.g. a provenance/role tag on the input path that the stream writer
   cannot set (out-of-band channel separation), or provenance-weighted
   revision where `!` lines still pass a (possibly weaker) coherence
   check against verified rules.
2. Capacity policy for the continuing learner: with X-U3-1 unaddressed,
   refuse-with-warning is a permanent-DoS surface. Consider verified-rule
   pinning plus principled eviction (H-MEM lane) or per-source quotas.
3. Re-run this red team after any Repair A rework; the X-U3-1 fixture
   (spoofed `!` through route_line) is the regression test.

## Artifacts (adversary-owned only)

- unified3_adversary/PREREG_U3_ADV.md (frozen 44c1dbe61, before execution)
- unified3_adversary/u3_adv.zag (mechanism verbatim; main() replaced)
- unified3_adversary/ADVERSARY_REPORT_H_UNIFIED3.md (this file)
- unified3_adversary/u3_adv_run1.txt (authoritative raw evidence,
  md5 e470fb2959fe2e4ee2dbeacb3c28a841; runs 2-3 byte-identical, hashes
  recorded in commit message)
- Binary /tmp/u3adv/u3_adv NOT committed per convention.
