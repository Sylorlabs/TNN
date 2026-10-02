# REDTEAM_SELF.md - H5R3 adversarial red team (post-freeze)

Lane: HPI, wave-20261002-1121pdt. Adversary: the lane worker, post-freeze
(the prereg froze with a single worker acting as coordinator, builder, and
evaluator; these attacks were designed after the freeze, 2026-10-02 12:08
PDT, with fresh seeds and fresh 99xxx key ranges, and were never used to
tune the substrate, which is byte-identical to the frozen H5R2 record).

Adversarial family: ADV_FRAG.zag, SHA-256
191e5a772eec70ae43b3630de97e6627d65208fb8390ef87d0b75dc1dea26fc8
(recorded before any run). World: world_adv.zag, SHA-256
b7925fc85c0fd784e2399498a5e4b28e4c52a4ba33aed336f5ccf7d535dc9607.
Runs: 3/3 byte-identical, stdout SHA-256
2483a501bd20d129ae5e8a7db8fd9ddbc150836fc65ee2d09c48204dfb5194a6.
Zero FAIL marker lines.

## Attack 1: stored snapshot vs live revisable structure (ADV-A)

Question: is the "surviving revision chain" just a stored snapshot that
happens to return the right values on the prereg's scripted path, rather
than a live structure that re-derives?
Method: after a full contradict/revert/contradict cycle, contradict with a
NOVEL value 99399 that was never taught and never expected anywhere in the
run, then query. A snapshot has no path to a value it never saw; only a
live trial loop plus provenance gate can promote a MAP for it. Then
contradict with a historical non-immediate-predecessor value (c1) to check
the chain does not just ratchet forward.
Result: SURVIVES. P5 returned 99399 via a FRESH MAP (id 151, strictly
increasing from 103); P6 returned 99306 via fresh MAP id 208. Final dump:
5 superseded MAPs with CON self-edges, exactly 1 live MAP (f28=99306),
every DEP edge to a live tag-1 non-superseded fact. The novel value was
derived, not recalled.

## Attack 2: adversarial revert ordering (ADV-B)

Question: does the chain survive a revert pattern the prereg never
scripted: two contradictions back-to-back with no intervening query, so
the intermediate dead fact never licensed a MAP?
Method: teach, query (M0), OBSERVE c1, OBSERVE c2 immediately, then query
expecting c2. The intermediate F1 is dead but unlicensed; a brittle
provenance scheme could either starve (no verifying live candidate found)
or anchor to F1.
Result: SURVIVES. P2 returned 99317 via fresh MAP id 45. Final dump:
exactly 1 superseded MAP (M0), 1 live MAP f28=99317, DEP edges to the live
chain fact and the live F2. No starvation, no dead anchoring.

## Attack 3: chain-link contradiction (ADV-C)

Question: the prereg only ever contradicts the VALUE fact. If the revision
chain is live, contradicting the CHAIN fact must kill the live MAP through
its second DEP link, and re-derivation must anchor to the NEW chain fact,
even though a dead-chain candidate verifies the expected value first in
enumeration order (the exact H5R killing configuration in a new position).
Method: full cycle, then OBSERVE (a,RF1,b9) contradicting the chain fact,
teach (b9,RF2,c2), query (a,RM,c2).
Result: SURVIVES. All 4 MAPs superseded via their chain DEP link (SELC
con=4). P5 returned 99327 via fresh MAP id 152 whose DEP set includes the
NEW chain fact (a,RF1,b9), live and non-superseded (NEWCHAIN ok=1); the
verifying dead-chain candidate was declined by the gate. The chain is live
in both DEP links.

## Prereg section 9 self-attacks, answered with evidence

- Attack 1 (indiscriminate supersession): would leave stray CON edges or
  wrong DEP targets. Evidence against: SELC con=3 on all 8 sealed probes
  and con=5/1/4 exactly matching the adversarial probes' contradiction
  counts; every DUMP ok required DEP targets live tag-1 non-superseded.
  Supersession is DEP selective, not indiscriminate.
- Attack 2 (dead-candidate starvation): would return miss (-2) instead of
  re-deriving. Evidence against: all 32 sealed probes and all 11
  adversarial probes returned exact expected values via fresh MAPs; zero
  VAL-FAIL lines.
- Attack 3 (fresh-key luck): the RR probe is constructed so the dead F1
  (lowest node-id c1 fact) verifies before the live F5 in enumeration
  order; without the gate, H5R's exact killing failure recurs there. The
  live MAP's DEP targets the live F5 (tgt=66 in both worlds' RR dumps),
  so the discrimination is structural, not luck. ADV-C repeats the same
  structural discrimination on the chain link.

## Residual risks (honest)

- The battery exercises one substrate, two sealed worlds, three
  adversarial probes: it does not establish generality, and no L3 claim
  is made. The four C0 clauses are not asserted.
- The re-teach separator family remains an explicit open gap (prereg
  section 10).
- Adversarial probes share the driver's marker logic; an independent
  adversary lane would strengthen the claim. None was assigned this wave.
