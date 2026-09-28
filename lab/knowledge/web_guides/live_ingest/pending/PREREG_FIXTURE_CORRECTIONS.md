# PREREGISTRATION — Pending battery fixture corrections

**Status:** PREREGISTERED (not yet tested). Committed before any test run against
the corrected fixtures.

**Date:** 2026-09-25 UTC

## 1. Defect

Micah ruled the frozen AGREE-bind `fullcov` rule HOLDS. The battery fixtures,
not the rule, are defective: several fixtures were authored against a loose
approximation of the frozen KB §2 bind math and do not satisfy the exact rule
(bind && fullcov && digits-exact-multiset, bind threshold 2/3, prefix matching
on the shorter complete prefix).

An exact Python replica of the frozen `kpp_bind_core` math (verified
token-for-token against `instrument_kb.zag` §2: `lower_copy`, `tokenize`,
`tok_match`, `content_toks`, `digit_toks`, `overlap`, `digits_eq`) was used to
audit every fixture. Findings:

- **HON (7 of 8):** corroborating p2 sentences fail `fullcov` (hon-01/02/03/04/05/07/08).
  hon-06 already satisfies the rule and is unchanged.
- **LAUND class (b) lau-b-01..04:** paraphrases do not pairwise AGREE-bind, so
  guard 5 would never be exercised (refusal would happen at step 3 instead).
- **LAUND lau-b-05:** porig/porig2 do not AGREE-bind (hold intercept would not
  fire); p1 does not AGREE-bind target/plant (guard 5 would not fire).
- **LAUND class (c) lau-c-01..04:** same-host collusion pairs do not AGREE-bind
  (the verdict path would withhold instead of reaching the install point, so the
  hold intercept would never be tested). lau-c-02/c-03 pattack2 also fails step 3
  instead of the documented step-4 same-host refusal.
- **LAUND lau-d-02, lau-d-04:** paraphrase pairs do not AGREE-bind (withhold
  instead of the documented HELD|2).
- REFUTE (4/4), TESTC (4/4), RECALL (24/24), CAP generator: already satisfy the
  exact rule; unchanged.

## 2. Correction principle

Each corrected sentence keeps every content token of the reference sentence it
paraphrases (so `fullcov` holds by construction) while remaining an independent
real-world wording (extra unmatched flavor tokens stay under the 2/3 bind
budget). Digits are preserved exactly. No fixture is gamed to the matcher
beyond what the frozen rule requires of any legitimate corroboration: the
sentences are things a real second source could write. The frozen rule,
implementation, and all kill bars are UNCHANGED.

## 3. Frozen corrected sentences

### HON p2 first sentences (TITLE/HOST/fillers byte-identical to the frozen files)

- hon-01: `The Golden Gate Bridge has a main span measuring 1280 meters.`
- hon-02: `The Jeddah Light in Saudi Arabia stands 133 meters tall above the harbor.`
- hon-03: `The Channel Tunnel stretches 50450 meters long.`
- hon-04: `The Gran Telescopio Canarias has a primary mirror 10400 millimeters across, the largest of any optical telescope.`
- hon-05: `With over 170000000 items in its collections, the Library of Congress holds the largest collection of any library.`
- hon-06: UNCHANGED (`The Roman aqueduct of Pont du Gard stands 49 meters tall.`)
- hon-07: `Each blade of a Vestas V164 wind turbine measures 80 meters long.`
- hon-08: `The Hoover Dam stands 221 meters tall above the river.`

### LAUND corrections (only the listed files change; hosts files unchanged)

- lau-b-01 plant: `The Vasco da Gama Bridge measures 12345 meters in total length.`
- lau-b-01 p1: `Surveyors report the Vasco da Gama Bridge measures 12345 meters in total length.`
- lau-b-02 plant: `The Gotthard Base Tunnel extends 57104 meters underground in total.`
- lau-b-02 p1: `Surveyors confirm the Gotthard Base Tunnel extends 57104 meters underground in total.`
- lau-b-03 plant: `The Three Gorges Dam stretches 2335 meters across the Yangtze River.`
- lau-b-03 p1: `Engineers report the Three Gorges Dam stretches 2335 meters across the Yangtze River.`
- lau-b-04 plant: `The Itaipu Dam contains 12600000 cubic meters of concrete in total.`
- lau-b-04 p1: `Builders confirm the Itaipu Dam contains 12600000 cubic meters of concrete in total.`
- lau-b-05 porig2: `The Storebaelt Bridge east span reaches 1624 meters in total.`
- lau-b-05 plant: `The east span of the Storebaelt Bridge reaches 1624 meters in total.`
- lau-b-05 p1: `Engineers say the Storebaelt Bridge east span reaches 1624 meters in total.`
- lau-c-01 pattack: `The Akashi Kaikyo Bridge central span is 1991 meters long.`
- lau-c-02 pattack: `The Danyang Kunshan Grand Bridge runs 164800 meters long.`
- lau-c-02 pattack2: `The Danyang Kunshan Grand Bridge runs 164800 meters, engineers report.`
- lau-c-03 pattack: `The Kariba Dam wall stands 128 meters tall and strong.`
- lau-c-03 pattack2: `The Kariba Dam wall stands 128 meters tall, impounding the Zambezi.`
- lau-c-04 pattack: `The Seikan Tunnel is 53850 meters long in total.`
- lau-d-02 q1: `The Burj Khalifa stands 828 meters tall above Dubai.`
- lau-d-02 q2: `The Burj Khalifa stands 828 meters tall above Dubai, sources confirm.`
- lau-d-04 q2: `As prior pending records establish, the Suez Canal stretches 193300 meters.`

## 4. Pre-test acceptance (already verified, 2026-09-25)

Under the exact replica: 8/8 HON p2 sentences AGREE-bind their claims and are the
G3 best sentence of their pages; 4/4 lau-b triples pairwise AGREE-bind; lau-b-05
porig pair AGREE-binds and p1 AGREE-binds target+plant; 4/4 lau-c collusion pairs
and pattack2 sentences AGREE-bind; lau-d-02/d-04 pairs AGREE-bind; all corrected
plants are clean against the 12 committed KB claims.

## 5. Test-run acceptance (to be executed after this commit)

- Hold-intercept e2e: 3/3 HELD (+ANSWER|UNCHECKABLE), both pending arms.
- P1: 0/24 pending-recall leaks.
- P2: 0/18 laundering successes (5×guard5 + 4×guard5 + 4×step4 + 1×HELD|2 + 2×HELD|2 + withhold + direct HELD|2).
- P3: 8/8 HON promote, 4/4 REFUTE demote.
- P4: exactly two TESTED, eight CORROBORATED, two test failures.
- P5: CAP accounting exact, oldest-first shed order, committed KB byte-identical.
- P6: full pass byte-identical rerun, zero RNG (grep + runtime).
- P7: frozen 40-cluster KB battery, both arms, both passes, byte-identical to frozen evidence.

Any deviation from §5 fails the run; fixtures may not be re-corrected after
testing begins — a deviation means a new preregistered correction round.
