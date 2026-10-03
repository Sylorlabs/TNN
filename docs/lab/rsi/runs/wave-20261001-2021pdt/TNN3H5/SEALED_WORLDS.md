# SEALED WORLDS: H5 adversary battery, wave-20261001-2021pdt

Designed post-freeze by the independent adversary (lane TNN3H5-ADVERSARY)
from the frozen prereg PREREG_H5.md section 4 family requirements only.
Freeze commit: 57aac4b81 (2026-10-02 03:30:27 UTC). Worlds written
2026-10-01 20:45-21:00 PDT (2026-10-02 03:45-04:00 UTC), strictly after
freeze. The builder has no read path to sealed/ (coordinator Q4 ruling).

Key/relation/value ranges 51xxx-54xxx are disjoint from: builder dev
worlds (7xxx/8xxx and small dev keys), FW1-FW9 (3xxxx), the 1421pdt sealed
battery (43xxx). No world is a trivial variant of FW1-FW9 or the 1421pdt
battery: all use trial-loop MAP promotion on fresh chain keys, interleaved
distractors, out-of-order resolution, wrong-key observes, first-link
contradiction, and teach/contradict/revert sequences absent from those
batteries.

Build method (documented for reproducibility): each w_<name>.zag is a
byte-copy of the frozen tnn3_h5.zag with only the main line replaced
(`fn main()i32 { return run_all(); }` becomes
`fn main()i32 { return sealed_main(); }`) plus the appended adversary
driver (common_driver.zag + world_<name>.zag). Verified by diff: zero
removed or changed cognition lines in all five builds (w_r1: 132 added,
w_r2: 133, w_c1: 156, w_c2: 157, w_ret: 145; 0 removed in each). The
cognition code executed is byte-identical to the frozen binary's source.

## Pre-run SHA-256 (recorded BEFORE any compile or run)

Driver sources:
- common_driver.zag: ed307b803e37f4ad36f309f554eeaf20a92bbf88334139eade7631e0f305b675
- world_r1.zag: 2fd6f5fc511029755db088891770c8f33b6dad09056171338e1bc83bf395d871
- world_r2.zag: 07dfd03a4044fe5c8ce3a1cee087a15fc27121c5284e1e82a94fa57678467e8e
- world_c1.zag: e007917a72a69d4b1094cdef3ce47b61ef44fc1b211ae6882df016a0e5b7e5f0
- world_c2.zag: d122bb4faf664328d43692d8ddf8761c3967b4c05e5ae7abbf0e5c360a45765c
- world_ret.zag: e2ee9589348a8ca26ff27d7e4ac82fd32132212d758f7a12e65ead7a089353c2

Assembled sealed builds (pre-run):
- w_r1.zag: 777843fdc2e969b1253c6d4ceed1d47139f0dfc5aa27e381df4bcea76bc6eb1d
- w_r2.zag: 5d66ff575c3374dd57d0ef817c85956cf83e795c7d8b60913729c23aa438f4f1
- w_c1.zag: 471b345adcb998c4748f4b927a74f068c006f5511edfff557fcd0a67f71cd049
- w_c2.zag: 097b4c5ff7753601d1968c368c4eeb4e880cc5798ab0ca1b8bb8e68b7342b8a9
- w_ret.zag: a006db5721d1da1ed0ffa3124922ade38d72446dd2712fb5869176e80982883b

## World R1: resolution, dense subjects (4 events)

Relation family 5101. Misses on (51101,5101), (51102,5101), (51103,5101),
(51104,5101), each verified a true miss (-2). Distractors before
resolution: an unrelated observe (51901,5191,77) that teaches a fact and
resolves nothing, and a fifth miss on (51301,5103) that is NEVER resolved
(genuine-uncertainty control: its guide must stay live). Before the
resolution loop the 4-slot context is flushed (ctx_push of 51991-51994):
this is probe hygiene, because ev_act fires any LIVE guide whose subject
is in context, and distractor subjects would otherwise contaminate the
probes. Resolutions in order with values 611-614; after each, the subject
is re-presented (ctx_push) and ev_act is invoked (must return 0). Final
white-box: exactly 4 guide-class CON edges; exactly 1 live guide (the
control).

World-design correction (recorded transparently, not a prereg amendment):
the first sealed version lacked the context flush, and the first ev_act
probe in each R world returned 30 because a still-live guide (R1: the
never-resolved control; R2: the not-yet-resolved 51201 guide) had its
subject in the context window from a distractor event. That is correct
ev_act behavior for live guides, but it contaminated the KB-B1 probes.
The flush fixes probe isolation; the family requirements are unchanged.

## World R2: resolution, scattered subjects (4 events)

Relation family 5102. Misses on (51201,5102), (51207,5102), (51213,5102),
(51229,5102). Wrong-key distractor: observe on (51201,5199,5), a pending
subject but a different relation; white-box verified to resolve nothing
(0 guide CON edges, 4 live guides after). Before the resolution loop the
4-slot context is flushed (51991-51994) for the same probe-hygiene reason
as R1. Resolutions out of order:
51213, 51201, 51229, 51207 (values 621-624), each followed by
re-presentation and an ev_act probe (must return 0). Final white-box:
exactly 4 guide-class CON edges.

Material difference R1 vs R2: different relation families (5101 vs 5102),
different subject distributions (dense block vs scattered), in-order vs
out-of-order resolution, distractor observe vs wrong-key observe, plus the
never-resolved control only in R1.

## World C1: contradiction, second-link target (4 double + 2 revert)

Relation families 5201/5202/5203, dense subjects. Each double probe:
teach (a,5201,b) and (b,5202,c0); promote a MAP on (a,5203) via the trial
loop (query with expected c0); contradict the SECOND chain link twice in
sequence, c0 -> c1 -> c2, with a re-derivation query on the fact key
between; final query on the fact key must return c2 (twice-corrected);
per-probe MAP-CON delta must be >= 1. Probes: (52101,52201,100,200,300),
(52102,52202,101,201,301), (52103,52203,102,202,302),
(52104,52204,103,203,303). Each revert probe: teach (a,5201,b) and
(b,5202,v0) [the old taught fact FA]; promote MAP; contradict
(b,5202) to v1 (FA must carry CON after); revert by observing v0 again;
final query must return v0 sourced from a FRESH live node (white-box:
original FA node superseded, live node id != FA id, live node holds v0).
Probes: (52401,52501,400,500), (52402,52502,401,501). One supplementary
bridge-key query (non-bar) after the probes.

## World C2: contradiction, first-link target (4 double + 2 revert)

Relation families 5301/5302/5303, scattered subjects
(a = 53101+7i, b = 53201+11i). Same skeleton as C1, but contradictions
target the FIRST chain link: teach (a,5301,b), (b,5302,c0); promote MAP
on (a,5303); contradict (a,5301) b -> b2 -> b3 with a re-derivation query
between; final query returns b3; per-probe MAP-CON delta >= 1. Probes:
(53101,53201,900,610,620), (53108,53212,901,611,621),
(53115,53223,902,612,622), (53122,53234,903,613,623). Revert probes
teach/contradict/revert the first link: (53401,53501,910),
(53406,53510,911), with the same white-box node-identity checks as C1.
One supplementary bridge-key query (non-bar).

Material difference C1 vs C2: different relation families, different
subject distributions, contradiction on the second vs the first chain
link, different value magnitudes.

## World RET: retention, no contradictions (12 probes)

Three chains (54101,5401,54201)/(54201,5402,10) etc., MAPs promoted on
(54101,5403), (54102,5403), (54103,5403). Interference with no
contradictions: unrelated teaches, one unrelated MAP promotion on
(54903,5408), two unrelated misses, one unrelated observe. Twelve
collateral probes: the six chain facts, the three MAP keys, one unrelated
fact, one unrelated MAP key, one re-probe. All 12 must return the taught
or derived value. Supplementary white-box: zero MAP-CON edges (no spurious
supersession under interference).

## Adversarial notes on bar operationalization

- KB-W1: counted in the final dump per world (R1: 4, R2: 4; total 8
  events, bar >= 6/8). Guide class is the frozen Q3 definition.
- KB-W2: per-probe MAP-CON delta (snapshot before first contradiction,
  count after final query), 8 double probes total, bar >= 6/8.
- KB-B1: per-event ev_act after resolution + re-presentation, 8/8.
- KB-B2: final query on the contradicted FACT key after the second
  contradiction, 8/8. (The prereg pins the query without naming the key;
  the fact key matches the builder dev tests D2/D3 and the 1421pdt M3-W2
  probe placement. Limitation: on the fact key the expected value equals
  the most recent observation, so a recency parrot passes the behavioral
  bar; the white-box KB-W2 bar carries the causal weight. Recorded
  transparently.)
- KB-B3: revert probes teach/contradict/revert on a fact key. White-box:
  the ORIGINAL taught node carries a type-3 self-edge and the live node is
  a different node. Behavioral: the final query returns the re-observed
  value. "Never the stale taught value" is read as node-sourced (the
  value must not come from the superseded stale node), per the prereg 3.8
  mechanism story, which is entirely about nodes; the re-observed value
  is correct behavior when sourced from a fresh node.
- KB-R1: 12/12 behavioral probes on the retention world.
