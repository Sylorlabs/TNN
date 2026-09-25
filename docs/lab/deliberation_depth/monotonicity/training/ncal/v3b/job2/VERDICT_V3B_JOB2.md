# VERDICT — NEC m20 JOB 2 (v3b): unseen-class knowledge, K-A vs K-B

Full evidence: `RUNLOG_V3B_JOB2.md` (same directory).

## Verdict ladder (§3.4), applied

**Rung 3 — machinery ceiling.** Neither design "closes it" in the §3.4 sense:
T3 closes (0.470 → 0.0000, bias +0.0000) for both, but "zero bar regressions"
fails — B13 breaks 0/0/0 → 22/24/24 on both designs. Kill criterion §3.3(iii)
fires independently: **both designs are DEAD forks — reported as killed, never a fix.**

## The white-box evidence (which lookup, which cap, which composition)

Item `H5B-O-20-04` (ceiling/O family, bin 15, always correct at depths 1/2/4):
m24 confs [775, 775, 775]; m25 [776, 776, 776]; m20 [950, 950, 950].

- **Which lookup (works):** the new-item branch at tp=0 seeds `confs` with the
  frozen schema value (`ka_schema(15)` = 775578, the true bin released rate).
  The knowledge bears here — T3 mean|err| = 0.0000 with zero bias proves it.
- **Which cap (fails):** at tp≥1 the adopted ceiling min-latch
  (`if(cl_mil>pc){cl_mil=pc;}`) pins conf at the first-observation value.
  The item's own perfect track record (p_raw = 1.0) can never lift it.
- **Which composition (breaks the bar):** schema-seed + min-latch → always-correct
  items in sub-0.9 bins are pinned at the bin rate forever → per-(F,d)
  G = −0.225 < −0.100 → B13 0 → 22/24/24.

This is the adopted ceiling's consequence B ("an always-correct item is pinned at
950 permanently, never reaching 1000") with the pin now at the schema value
instead of d1prior. m20's pin of 950 gave G = −0.050 — inside the −0.100 floor.
Any honest first-observation value below ~0.9 on always-correct items breaks it.
**The pin value is load-bearing for B13**: a knowledge channel that seeds the
latch with honest sub-0.9 values is structurally incompatible with the adopted
min-latch as composed.

## On Micah's hypothesis ("it's a knowledge issue")

**Falsified as stated for this composition.** The knowledge was supplied in full
(K-A oracle), acquired essentially perfectly by TNN's own deliberate machinery
(K-B: 34/35 bins installed, max |learned − oracle| = 500 millionths, bin 28
honestly ABSTAINed to the disclosed fallback), and it bears at the lookup
(T3 0.470 → 0.000). The failure is not in the knowledge, its acquisition, or the
lookup — it is in the adopted ceiling latch's composition with a
knowledge-seeded first observation. **No learning gap**: K-B ≈ K-A everywhere
(bars within 0.0002, T3 outputs byte-identical).

## No other regressions

B3 = 2/2/2 at all scales both designs (no O-rise reintroduction, kill criterion
(i) clean). All other bars hold at adopted levels. T1 byte-identical to m20
(CALIBRATING). T2 would_rise β = −0.021, p = 0.935 (CALIBRATING). Channel audit
clean: schema consulted only at the tp=0 branch, class ledger never read or
written (nopool=1 guards), no runtime schema updates, no test outcomes entering
the K-B schema.

## Disposition

- K-A (variant 24): DEAD fork — killed by §3.3(iii), B13 regression. Oracle
  diagnostic only; never adopted (per prereg).
- K-B (variant 25): DEAD fork — killed by §3.3(iii), B13 regression.
  Adoption-eligible no longer; **not recommended for adoption**.
- No fix round: killed designs are reported as killed, not fixed (§3.3).
- The surviving positive result: TNN's deliberate machinery learns the schema
  honestly (34/35 bins, correct ABSTAIN on the empty bin) and the knowledge
  bears at first observation (T3 closes). The blocker is the ceiling latch's
  composition — a machinery question, not a knowledge question. Any future
  knowledge-first design must change how first-observation knowledge composes
  with the ceiling, or change the ceiling itself; either route needs a new
  prereg and Micah's word.
