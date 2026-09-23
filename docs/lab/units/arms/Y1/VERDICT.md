# Y1 — Negotiated cuts: VERDICT

**Verdict: KILLED**

## Binding criterion (verbatim frozen row)

> "Over 10,000 cuts, negotiated boundaries show ≤10% better recall-stability
> than arm-D unilateral cuts at the same granularity; OR veto rate collapses
> to <1% within the first 1,000 cuts (lazy agreement — then Y1 ≡ D with extra
> ledger cost)."

## Kill evidence (`kill-1x` mode, 10,000 cuts, first 640,000 bytes of prose.bin)

| Measure | Value |
|---|---|
| Negotiated recall-stability | 100.0% |
| Unilateral (arm-D) recall-stability | 100.0% |
| Relative improvement | **0.0%** (≤10% → disjunct 1 FIRES) |
| Veto rate, first 1,000 cuts | 58.7% (≥1% → disjunct 2 does not fire) |

Raw output:
```
KILLTRIAL,cuts=10000,stab_neg=100.0,stab_uni=100.0,veto_neg=58.7,d1=1,d2=0,verdict=KILLED
```

Disjunct 1 fired: the negotiated boundaries are exactly 0% better on
recall-stability than unilateral cuts at the same 64-byte granularity.
Disjunct 2 did not fire — the veto rate is 58.7%, so the negotiation is
genuine mutual veto, not lazy agreement. The mechanism works as specified;
it is simply not worth its cost. Y1 ≡ D with extra compute.

Recall-stability (provisional operationalization, ARM_SPEC §2): fraction of
the 10,000 cuts whose committed span is intact, original ID intact, and
byte-exact recall holds after a shared 200-defect revision curriculum
(100 boundary + 100 content defects, all revised). Arm-D is operationalized
as the identical fast segmenter with negotiation disabled (same granularity;
provisional ambiguity Y1-A2, documented).

## 1x scorecard (M1–M9)

Full row: `work/battery_r1_1x/scorecard_y1_r1_1x.json`. Every leg double-run,
byte-identical stdout.

- **M1:** prose 100.0% recall / 100.0% boundary (84,731 units); code 100.0% /
  100.0% (148,678 units). Swap probe 64/64 PASS both corpora
  (PROVISIONAL-PENDING-FREEZE). Veto rates 58.7% / 57.1%.
- **M2/M9:** ETC=1 all five tiers; M9 fast-then-flat everywhere; ep0 recall
  0.0% (no leak), final 100.0%.
- **M3:** survival 100.0%, fresh recall 100.0%, 8,050 mgmt entries, 50/50
  weakens, freeze CLEAR, 1,000 valuable marked.
- **M4:** boundary revision 100.0%, content revision 100.0%, kill rate 0.0%,
  1 episode, no killsub.
- **M5:** memory 2.448 B/B (bar ≤1.5×: FAIL — RSS delta 8.07 MB + slot table;
  literal accounting); audit 16.189 entries/KB (bar ≤10/KB: FAIL — one 64-byte
  ADD_UNIT per cut, same structural outcome as the b64 reference).
- **M6:** p2c and c2p 100.0/100.0/100.0, tax 0.0; memorizer validity gate
  evaluated per control run.
- **M7:** hit 100.0% (≥90 PASS), reuse 3.0 (≥1.5 PASS), dedup 99.4%
  (≥0.4 PASS). PROVISIONAL-PENDING-FREEZE(A7/A8) emitted in the fragment.
- **M8:** M8GATE PASS — 5 perturbations × 2 reruns, byte-identical artifacts.

## 10x status

**NOT ATTEMPTED.** Gated on all 1x bars and the Y1 kill bars passing; the
binding kill fired at 1x.

## Ambiguities (carried, not resolved)

Y1-A1 (both coordinator corrections acknowledged — see ARM_SPEC §4);
Y1-A2 (arm-D = negotiation-disabled Y1, provisional); Y1-A3 (M8 includes swap
probes); Y1-A4 (kill corpus = prose first 10,000 cuts); Y1-A5 (M7 field
names); Y1-A6 (recall-stability operationalization, provisional); Y1-A7 (A15
swap-probe schedule, PROVISIONAL-PENDING-FREEZE); Y1-A8 (M7 C′ edit + lookup
schedule, PROVISIONAL-PENDING-FREEZE). Inherited harness ambiguities A1–A17
applied literally.

## Corrections acknowledged

1. The original "Adversarial corpus probe" assignment was voided; all
   wrong-path work was discarded (nothing from it was built or tested).
2. The coordinator's remembered fast/slow/latency paraphrase was superseded
   by the verbatim frozen row; authority order brief → verbatim row →
   nothing else.
