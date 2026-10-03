# SEALED_H5R: sealed world specifications (adversary-designed post-freeze)

Lane TNN3H5R, wave-20261001-2021pdt. Adversary: independent lane agent
(TNN3H5R-ADV). All five worlds were designed after the implementation
commit 830f95ab7 (2026-10-02 04:19:13 UTC) from PREREG_H5R.md alone, with
no knowledge of the implementation beyond the frozen prereg text and the
builder's chain-of-custody evidence. The sealed directory did not exist at
builder time. Nothing is reused from the killed H5 battery's worlds, keys,
values, or ranges.

## Key/relation/value ranges

All sealed ranges live in 61xxx-65xxx and 71xxx-72xxx, disjoint from:
FW1-FW9 (3xxxx), the 1421pdt sealed battery (43xxx), the killed H5 battery
(51xxx-54xxx), the H5R builder smoke worlds (7xxx/8xxx, 9001), and small dev
keys. Per-probe (subject, relation) key ranges are disjoint within each
world. No world is a trivial variant of FW1-FW9, the 1421pdt battery, or
the killed H5 battery: the C worlds probe MAP-key re-derivation after
contradiction (the exact claim H5 failed to evidence), the R worlds re-test
the guide half with fresh relation families, and the retention world is new.

## World files (pre-run SHA-256, recorded before any run)

Each world file is a byte-copy of the committed substrate
tnn3_h5r.zag (git blob 830f95ab7, SHA-256
d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384)
with exactly one line changed
(`fn main()i32 { return run_all(); }` to
`fn main()i32 { return sealed_main(); }`, verified by diff) plus the
adversary driver appended after the marker
`// ==== H5R SEALED DRIVER (adversary-designed post-freeze, pure Zag) ====`.
The substrate portion of every world is therefore the exact source that
builds the frozen binary (independently rebuilt by the adversary to
SHA-256 59c7648287d1e8a1ae6ea851696aae38b3991e537679fc9fc2d4bd38dded0f9b,
matching the frozen record).

- w_c1.zag ac71b2ae596148ba39578cc6aa62a06a30fde3fe1d5469c69cb4c7bc0841be0d
- w_c2.zag cf00da16f72a3f29e1adfeaa418ff2a923b46d46561bb18dbfd9aec446613f01
- w_r1.zag bc42b9515605ed2724438a204a57495d1d7b19990b05e416fafd9dd34e664789
- w_r2.zag 15d946d5c07f1a095615eb1bed39270445cb479ff7f66f6d1279a00e664740be
- w_ret.zag 0e450b2b49bfa25f7c84df78404a5f169e781e14de0200755e98dfc4fec53151

## C-family (MAP half, the new claim)

Pattern per double-contradiction probe (prereg 6.7, exact):
teach chain a-RF1->b, b-RF2->c0; SNAP-IN on MAP key (a,RM);
QUERY a RM c0 (promote, expect c0 via the MAP node);
OBSERVE b RF2 c1 (fact-key contradiction, never the MAP key);
SNAP-IN; QUERY a RM c1 (expect c1 via a fresh MAP);
OBSERVE b RF2 c2; SNAP-IN; QUERY a RM c2 (expect c2 via a fresh MAP).

Pattern per revert probe: teach chain; SNAP-IN; QUERY a RM c0 (promote);
OBSERVE b RF2 c1; SNAP-IN; QUERY a RM c1 (expect c1 via fresh MAP);
OBSERVE b RF2 c0 (revert); SNAP-IN; QUERY a RM c0 (expect c0 via fresh MAP).

Frozen constraint honored: no OBSERVE on any MAP key in any world. All
contradictions arrive on fact keys (b,RF2). 12 probes x 3 MAP-key probes
= 36 SNAP-IN records (one white-box snapshot before every MAP-key probe).

### w_c1 (chain relations 6301/6302, MAP relation 6303)

- C1D1: a=63101 b=63301 c0=63401 c1=63402 c2=63403
- C1D2: a=63102 b=63302 c0=63411 c1=63412 c2=63413
- C1D3: a=63103 b=63303 c0=63421 c1=63422 c2=63423
- C1D4: a=63104 b=63304 c0=63431 c1=63432 c2=63433
- C1R1: a=63201 b=63311 c0=63501 c1=63502
- C1R2: a=63202 b=63312 c0=63511 c1=63512

### w_c2 (chain relations 6401/6402, MAP relation 6403)

Materially different relation family and subject distribution from C1.

- C2D1: a=64101 b=64301 c0=64401 c1=64402 c2=64403
- C2D2: a=64102 b=64302 c0=64411 c1=64412 c2=64413
- C2D3: a=64103 b=64303 c0=64421 c1=64422 c2=64423
- C2D4: a=64104 b=64304 c0=64431 c1=64432 c2=64433
- C2R1: a=64201 b=64311 c0=64501 c1=64502
- C2R2: a=64202 b=64312 c0=64511 c1=64512

Non-vacuity notes: each probe's MAP key (a,RM) has no fact with relation
RM anywhere, so the first MAP-key probe cannot hit an exact fact and must
go through the trial loop; the licensing chain uses two-hop facts only the
trial can compose. Post-contradiction probes must miss (superseded MAP, no
shadow fact) and re-derive, because the only live structure answering the
MAP key is the MAP node itself. The driver checks fresh promotion by
strictly increasing live-MAP node ids per probe (FRESH-FAIL otherwise).

## R-family (guide half re-test)

### w_r1 (relation 6101)

Four true misses on distinct keys (61101..61104, relation 6101), each
verified to return -2 (true miss, guide created). One never-resolved
control miss (61109, 6101). Pre-resolution white-box: 0 guide-CON,
5 live guides. Context hygiene per the H5 Attack 4 precedent: flush the
4-slot context window with distractors (61991..61994) before the
resolution sequence; each resolution does OBSERVE on (s,6101) with value
71101+k, re-presents the subject via ctx_push, then ev_act (expect 0).
Post: exactly 4 guide-CON self-edges (KB-W1R), exactly 1 live guide with
no CON edge, the never-resolved control (KB-S1R).

### w_r2 (relation 6201)

Materially different relation family and subject distribution from R1.
Four true misses (62101..62104, relation 6201). Wrong-key OBSERVE probe:
ev_observe(62109, 6209, 777) while all 4 guides are unresolved; driver
checks 0 new guide-CON edges and all 4 guides still live (KB-S2R). Then
context flush (62991..62994) and four resolutions (values 72101+k) with
re-presentation and ev_act (expect 0 each). Post: exactly 4 guide-CON
(KB-W1R), 0 live guides.

Non-vacuity notes: the misses are true misses only if the trial loop and
bootstrap cannot answer; with zero facts taught on relation 6101/6201
before the misses, both fail and miss_inquire creates the guides. The
context flush is load-bearing: without it, live guide subjects linger in
the 4-slot context and ev_act returns 30 (the Attack 4 finding), which
would contaminate KB-B1R. The control (R1) and wrong-key (R2) probes are
the selectivity checks.

## Retention world (w_ret)

Twelve collateral fact keys (65101..65112, relation 6501), values
65101+i*3+7, taught once. Interference: four teaches on other keys
(65201..65204, relations 6502/6503), a fact-level contradict-and-revert
cycle on (65201,6502) (observe 999, observe 111), and two true misses on
a fresh relation (65301/65302, 6509; unresolved guides, no MAP
involvement). Then the 12 collateral re-queries (expect exact hits,
KB-R1R 12/12) and the supplementary check of zero MAP-CON edges under
interference. No OBSERVE on any MAP key.

Non-vacuity: the interference includes a genuine contradiction cycle and
uncertainty events, so the zero-MAP-CON check is not over an empty
history; the collateral re-queries follow the interference, so KB-R1R
tests retention under interference rather than immediate recall.

## Snapshot and dump protocol

- Before every MAP-key probe the driver emits one SNAP-IN line with the
  exact count of live tag-1 facts on (s_m,r_m) (KB-W0 conjunct 1) and
  after the probe one Q line with the returned value, the live MAP count,
  id, and f28 (KB-W0 conjunct 2: single live MAP, f28 == returned value).
  36 SNAP-IN records total across w_c1 and w_c2.
- Each world ends with a canonical full state dump (headers, all live
  nodes, all live edges) for KB-D1 3/3 byte-identical comparison.
- Determinism: 3 runs per world binary; SHA-256 of full stdout compared.
