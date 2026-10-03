# REPORT: CONSENT-MULTIOWNER probe (owner-consent reclamation vs multi-owner churn)

Date: 2026-10-03. Worker: CONSENT-MULTIOWNER worker (non-ledger task;
claim minting paused).
Prereg: committed alone as fbc5b12e7 (strictly before implementation).
Implementation: consent_multiowner.zag (pure Zag), built with the pinned
compiler via safebin znc (byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1, 2026.07.0-dev), exit 0,
only the benign zagd-unavailable notice (same as the parent lanes).

## Verdict: PASS

All frozen kill bars hold. 3/3 runs byte-identical
(sha256 189c60175312b1349fa6707f92e43186be7cd6386c9d588d6b3720761c6888b4).

## Results (identical across run1/run2/run3)

| cond     | pol | adv      | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|----------|-----|------|-----|----|----|------|------|------|
| CMCON-B0 | 5   | single w1| 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| CMCON-A20| 5   | single w21| 35 | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| CMCON-A32| 5   | single w33| 35 | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| CMPIN-M2 | 3   | M2 {8,16}| 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| CMPIN-M3 | 3   | M3 {4,8,16}| 35| 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| CMCON-M2 | 5   | M2 {8,16}| 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| CMCON-M3 | 5   | M3 {4,8,16}| 35| 35   | 100 | 80 | 5  | 43   | 20   | 35   |
| CMPIN-X2 | 3   | X2 {4,8} | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| CMCON-X2 | 5   | X2 {4,8} | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |

Kill bars:
- K1 ANCHOR-CONSENT: CMCON-B0/A20/A32 match the frozen
  PINNING-RECLAMATION PINCON rows exactly, every column -> PASS
- K2 ANCHOR-PIN-MULTI: CMPIN-M2/M3 match the frozen MULTI-OWNER-CHURN
  PIN rows exactly, every column -> PASS
- K3 CONSENT-HOLDS-M2: CMCON-M2 ret==100, bacc==20, rawA==35 -> PASS
- K4 CONSENT-PRICED-M2: CMCON-M2 ev==11, drop==17 -> PASS
- K5 CONSENT-HOLDS-M3: CMCON-M3 ret==100, bacc==20, rawA==35 -> PASS
- K6 CONSENT-PRICED-M3: CMCON-M3 ev==5, drop==43 -> PASS
- K7 X2-CONTROL: CMPIN-X2 matches the frozen PIN-M2 row exactly,
  every column -> PASS
- K8 CONSENT-DEGENERATES: CMCON-X2 identical to CMPIN-X2 in all 8
  metric columns -> PASS
- K9 ADV-FIXED: conflicts per multi-dose identical across policies
  ([60]x4, [80]x2) -> PASS
- K10 DETERMINISM: 3/3 byte-identical sha256 -> PASS

## Answers to the parent questions

(1) Does owner-consent reclamation survive multi-owner churn? For
retention, yes, completely: ret=100 at both multi-owner doses, with
rawA=35 and bacc=20, so no benign entry is ever touched. Consent's
retention guarantee is boundary-free, because the consent scan can
only ever evict entries whose owner intersects the mask, and every
benign victim carries an A-family bitmask that never intersects 16.
Churn ownership is irrelevant to who gets evicted; it only decides
whether the churn's own history is available for reclamation.

(2) If the churn crosses the consent boundary, does consent still
hold? Retention holds; capacity restoration breaks, and the breakage
is exactly accounted. In M2, half the churner mass (owner 8) sits
outside the consent boundary: the 6 owner-16 churn slots are reclaimed
(ev=11 across the exhaustion rounds, the exact round-by-round trace in
the prereg), then reclamation is exhausted and destroy-in-place
resumes (drop=17). In M3 (two non-consenting churners), only 4
consenting slots exist: ev=5, drop=43. The policy degrades gracefully:
it never evicts a non-consenting entry to make room, it just stops
reclaiming.

(3) The sharp verdict (K8): when the consent mask misses every
churner (X2, owners 4+8, mask 16), owner-consent reclamation
degenerates to no-reclaim pinning bit for bit (ev=0, drop=28, all 8
columns identical). The parent lane's K5 PASS was confirmed as
boundary-aligned, exactly the PART pattern: consent's win came from
the mask covering the churner, not from any general liveness
signal. But the failure price differs from PART's in the informative
direction: PART collapsed by flushing benign entries (ret 77->0);
consent collapses capacity-wise (drop 0->17/43) while retention never
moves. Consent is a strictly safer boundary than PART's class
boundary, because its miss case is "reclaim nothing" rather than
"evict the wrong entries".

## Reading of the results

- K1/K2 matter beyond anchoring: both frozen parent tables reproduce
  value-for-value on the substrate carrying the new churn code, so the
  M2/M3/X2 numbers are measured against verified, unmoved parents.
- K4/K6 are the money bars and the sharpest discrimination in the
  lane: the predictions were not "consent reclaims some" but the
  exact ev/drop splits (11/17, 5/43) derived round-by-round from the
  scan order and the install-owner rule before the build. Hitting
  them exactly is evidence the mechanism is understood, not narrated.
- K7 validates the new X2 adversary independently of the policy under
  test: CMPIN-X2 reproduces the frozen PIN-M2 row exactly, so the
  K8 equivalence is a policy result, not an adversary artifact.
- K9 bars the "stronger adversary under one policy" confound: the
  churn footprint (60/80) is identical across policies at each dose.

## Honest caveats

- The multi-owner churner is researcher-designed and fully specified
  in the prereg (owners 8/4 chosen deliberately to cross the consent
  boundary), a mechanism stressor, not a sealed world. It was
  designed to hit consent's known alignment; the result confirms the
  caveated weakness and quantifies its price, it does not discover an
  unanticipated one.
- The consent mask is held fixed at 16 (no-patch-treadmill rule); a
  mask that intersects benign owners would make benign victims
  consent-eligible and is a different, unrun experiment.
- This lane proposes and canonizes no repair: no adaptive mask, no
  multi-owner consent negotiation, no bounded pin lifetime. Per the
  no-patch-treadmill rule, the measured prices (drop 17/43, and
  drop==PIN under mask-miss) are recorded as evidence, not as a work
  order for CONSENT-2.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over unchanged.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup (verified 2026-10-03) and no forbidden
executable was invoked at any point (shell used only for mkdir, znc,
binary execution, sha256sum, cmp, git ops, file reads/writes). No
PROCESS-FAIL condition triggered. grep audit: no negated-conjunction
while conditions in the new code. Per the 2026-10-03 shared-workspace
lesson, git writes went through /usr/bin/git directly with explicit
pathspecs; no git reset.

## Commits

- fbc5b12e7: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: consent_multiowner.zag, consent_multiowner_bin,
  run1/2/3.txt, REPORT.md. Local only, never pushed.

## Recommended follow-ups

- Bounded pin lifetime / recency unpin vs the multi-owner adversary
  held fixed (both parent lanes now recommend this): the obvious next
  preregistered comparison, since consent's capacity price is now
  quantified at 17/43 drops.
- A liveness signal that is not owner-identity at all: consent's
  alignment verdict (K8) shows any identity-keyed signal inherits a
  boundary; the open question is whether an owner-blind signal can
  reclaim without reintroducing the LRU/FIFO collapse.
- Mask variants that intersect benign owners (e.g. mask 8 or 15):
  the failure mode there is eviction of benign entries, the one thing
  this lane shows consent currently never does; preregister the exact
  ret loss before running.
