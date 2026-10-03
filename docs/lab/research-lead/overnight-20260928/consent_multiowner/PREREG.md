# PREREG: CONSENT-MULTIOWNER probe (owner-consent reclamation vs multi-owner churn)

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: CONSENT-MULTIOWNER worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/consent_multiowner/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

PINNING-RECLAMATION (VERDICT=PASS 7/7, 2026-10-03) found owner-consent
reclamation gets both (ret=100, drop=0) but honestly caveated: the
consent mask (owner 16) aligns with the single-owner churn adversary,
the same alignment caveat the parent lane recorded for PART.
MULTI-OWNER-CHURN (VERDICT=PASS 8/8, 2026-10-03) then killed PART under
churn that crosses the class boundary (ret 77 -> 0) while pinning held
(ret=100, drop 28/48). The parent question now: does owner-consent
reclamation survive multi-owner churn? If the churn crosses the consent
boundary, does consent still hold, and what breaks?

## Substrate (frozen, built on PINNING-RECLAMATION, not redesigned)

Identical to the PINNING-RECLAMATION substrate, byte for byte in
mechanism: same header layout (0 bumpA, 4 conflicts, 8 evictions, 12
table_full_errors, 16 pool_size=32, 20 policy, 24 bumpB, 28 drop,
32 consent_mask=16, 36 clock), same pool (base 2112, 32 slots x 16
bytes), same primary (base 64, 128 slots x 16 bytes), same conflict
path (conflicts++ on every same-key different-value write, then policy
relocation, then install), same owner-scoped read path, same A family
(35 queries), same benign B writer (cond=2 FULL, 20 conflicts, victims
with bitmasks {15,7,11,3}), same PIN first-free scan with drop fallback,
and the same PIN-CONSENT rule (policy 5): first-free scan; if the pool
is full, scan slots 0..31 for the first USED slot whose owner
intersects the consent mask (16) and evict it (ev++); benign victims
carry A-family bitmasks that never intersect 16, so they are never
consent-eligible; if no consenting slot exists, drop++ and fall back to
destroy-in-place. The only new code is the multi-owner churn routine,
carried over unchanged from MULTI-OWNER-CHURN (mode=1: keys 3998/owner 8
and 3999/owner 16 interleaved per round; mode=2: adds key 3997/owner 4
as the first write of each round), plus mode=3 (X2): keys 3997/owner 4
and 3998/owner 8 interleaved 3997-then-3998 per round, w=21 each, the
consent-missing adversary. The single-owner churn routine (key 3999,
owner 16) is carried over unchanged.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace: 1. teach A family
(multi). 2. pre-test (expect 35). 3. teach B benign FULL (20
conflicts). 4. churn: single-owner key 3999 (w in {1,21,33}) or
multi-owner mode 1/2/3 (w=21 per key). 5. post-test; retention =
100*post/pre. 6. record conflicts, evictions, drop, B accuracy, rawA.

Conditions (9): CMCON-B0/A20/A32 (policy 5, single-owner churn,
w=1/21/33), CMPIN-M2/M3 (policy 3, multi-owner modes 1/2),
CMCON-M2/M3 (policy 5, multi-owner modes 1/2), CMPIN-X2 (policy 3,
mode 3), CMCON-X2 (policy 5, mode 3).

## Predicted values (frozen; these ARE the kill-bar targets)

Anchors reproduce the two frozen parent tables exactly:

| cond     | pol | adv       | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|-----------|-----|------|-----|----|----|------|------|------|
| CMCON-B0 | 5   | single w1 | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| CMCON-A20| 5   | single w21| 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| CMCON-A32| 5   | single w33| 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| CMPIN-M2 | 3   | mode1     | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| CMPIN-M3 | 3   | mode2     | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |

New predictions (frozen derivation follows the table):

| cond     | pol | adv       | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|-----------|-----|------|-----|----|----|------|------|------|
| CMCON-M2 | 5   | mode1     | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| CMCON-M3 | 5   | mode2     | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |
| CMPIN-X2 | 3   | mode3     | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| CMCON-X2 | 5   | mode3     | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |

Derivation notes (frozen with the prereg).

Benign phase is identical in all conditions: 20 A-family victims pin
pool slots 0..19 (owners in {15,7,11,3}, none intersecting 16), slots
20..31 free. Consent scan always starts at slot 0 and takes the first
used slot with owner&16 != 0; installs carry the churn write's owner.

CMCON-M2: 40 churn relocs (rounds 1..20). Rounds 1..6 fill slots 20..31
(6 owner-8, 6 owner-16). Round 7: 3998 write evicts slot 21 (owner 16)
-> owner-16 count 5; 3999 write evicts slot 23 -> count 5. Round 8:
3998 evicts 23 -> 4; 3999 evicts 25 -> 4. Round 9: 3998 evicts 25 -> 3;
3999 evicts 27 -> 3. Round 10: 3998 evicts 27 -> 2; 3999 evicts 29 ->
2. Round 11: 3998 evicts 29 -> 1; 3999 evicts 31 -> 1. Round 12: 3998
evicts 31 -> 0; 3999 finds no consenting slot -> drop=1. Rounds 13..20
(16 relocs): no owner-16 entry is ever installed again (destroyed
values are never pool-installed), so all drop. Totals: 12 fills + 11
evictions + 17 drops = 40 relocs. ev=11, drop=17. No benign slot is
ever touched, so ret=100, rawA=35, bacc=20, cf=60.

CMCON-M3: 60 churn relocs. Rounds 1..4 fill slots 20..31 (4 owner-4, 4
owner-8, 4 owner-16 at slots 22,25,28,31). Round 5: 3997 evicts 22 ->
3; 3998 evicts 25 -> 2; 3999 evicts 28 -> 2. Round 6: 3997 evicts 28 ->
1; 3998 evicts 31 -> 0; 3999 finds nothing -> drop=1. Rounds 7..20 (42
relocs): all drop. Totals: 12 fills + 5 evictions + 43 drops = 60.
ev=5, drop=43, ret=100, cf=80, bacc=20, rawA=35.

CMPIN-X2 / CMCON-X2 (mode 3, churners owners 4+8): 40 relocs. Rounds
1..6 fill slots 20..31 (6 owner-4, 6 owner-8); no owner-16 entry ever
appears in the pool. Rounds 7..20 (28 relocs): policy 3 goes straight
to drop++ (drop=28, ev=0); policy 5 scans, finds no consenting slot,
drop++ identically. Both rows identical to the frozen PIN-M2 row:
ret=100, cf=60, ev=0, drop=28, bacc=20, rawA=35. CMPIN-X2 validates the
mode-3 adversary is well-formed; CMCON-X2 tests the sharp prediction
that consent contributes nothing when the mask misses every churner.

## Frozen kill bars

- K1 ANCHOR-CONSENT: CMCON-B0/A20/A32 match the frozen
  PINNING-RECLAMATION PINCON rows exactly, every column (ret=[100,100,
  100], cf=[20,40,52], ev=[0,8,20], drop=[0,0,0], bacc=20, rawA=35).
  Else VOID: the consent substrate moved.
- K2 ANCHOR-PIN-MULTI: CMPIN-M2/CMPIN-M3 match the frozen
  MULTI-OWNER-CHURN PIN rows exactly (ret=[100,100], cf=[60,80],
  ev=[0,0], drop=[28,48], bacc=20, rawA=35). Else VOID: the
  multi-owner adversary moved.
- K3 CONSENT-HOLDS-M2: CMCON-M2 ret==100, bacc==20, rawA==35.
  Retention holds even though half the churner mass sits outside the
  consent boundary.
- K4 CONSENT-PRICED-M2: CMCON-M2 ev==11 AND drop==17. The exact
  white-box mechanism model: consent reclaims only consenting churn
  entries; once they are exhausted, destroy-in-place resumes. Capacity
  restoration is partial (drop 17 > 0).
- K5 CONSENT-HOLDS-M3: CMCON-M3 ret==100, bacc==20, rawA==35.
- K6 CONSENT-PRICED-M3: CMCON-M3 ev==5 AND drop==43.
- K7 X2-CONTROL: CMPIN-X2 matches the frozen PIN-M2 row exactly,
  every column. The mode-3 adversary is well-formed.
- K8 CONSENT-DEGENERATES: CMCON-X2 matches CMPIN-X2 exactly, every
  column (ev=0, drop=28). When the consent mask misses every churner,
  owner-consent reclamation contributes nothing: it degenerates to
  no-reclaim pinning bit for bit.
- K9 ADV-FIXED: conflicts per multi-dose identical across policies:
  60 in CMPIN-M2, CMCON-M2, CMPIN-X2, CMCON-X2; 80 in CMPIN-M3,
  CMCON-M3. Only the reclamation outcome may differ by policy.
- K10 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else VOID.

Verdict: PASS iff K1..K10 all hold. Any kill-bar miss names the bar
and yields FAIL. K1, K2, or K10 failure yields VOID. Thresholds are
frozen; they are not moved after results. rawA is reported as a
diagnostic inside K3/K5 and is otherwise not kill-barred.

Discrimination design: K1/K2 anchor both parents (a moved substrate
invalidates the probe); K3/K5 ask the headline question (does consent
hold retention when churn crosses its boundary); K4/K6 test the exact
white-box mechanism trace (ev/drop split at exhaustion), which
falsifies the worker's mechanism model if wrong; K7 validates the new
adversary independently of the policy under test; K8 is the sharp
boundary-alignment verdict (consent's K5 win in the parent lane was
alignment; here the mask-miss case reproduces pinning exactly);
K9 bars the "stronger adversary under one policy" confound.

## What this does NOT test

The consent mask is held fixed at 16 (no mask redesign per the
no-patch-treadmill rule); mask 15/8 variants that would make benign
victims consent-eligible are out of scope. Benign re-reads during
churn, bounded pin lifetime, and learner-issued unpin are out of
scope. The multi-owner churner is a researcher-designed mechanism
stressor, not a sealed world. Owner-scoped reads are retained, so the
label-free routing caveat carries over unchanged.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(consent_multiowner.zag), build, runs, and REPORT.md only after.
