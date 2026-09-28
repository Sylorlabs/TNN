# Z6 — VERDICT (Track A, pure Zag)

## Kill adjudication

Frozen kill (§3, verbatim):

> "Scar boundaries match ground-truth units (sqlite3.c function boundaries,
> Shakespeare act/scene structure) no better than random cuts at the same
> count (±10%) — the claim is dead; OR the bootstrap arm's cuts are never
> displaced by scars after 10,000 revisions (decorative)."

Adjudicated on the frozen trial: replay of the full 10,000-revision
schedule per corpus. (The blind-only replay below is a crew diagnostic
subset, not the frozen schedule.)

### Clause A — scar rate vs same-count random control (±10% band)

| Corpus | Scar rate (≤64 B of GT) | Random control (5 reps) | Band check | Verdict |
|---|---|---|---|---|
| Shakespeare prose | 62.5% (872/1,396) | 2.0% | 62.5 > 2.0×1.10 | NOT FIRED |
| sqlite3.c | 90.9% (2,957/3,253) | 7.5% | 90.9 > 7.5×1.10 | NOT FIRED |

### Clause B — decorative (zero displacement after 10,000 revisions)

| Corpus | Displaced cuts | Verdict |
|---|---|---|
| Shakespeare prose | 1,395 of 1,414 proposals (98.6%) | NOT FIRED |
| sqlite3.c | 3,252 of 3,307 proposals (98.3%) | NOT FIRED |

**Overall: KILL DOES NOT FIRE. The Z6 claim survives.**

### Diagnostic: blind-only schedule (crew control, not the frozen trial)

| Corpus | Scar rate | Random control | Band |
|---|---|---|---|
| Shakespeare prose, blind 5k | 3.1% | 1.9% | 3.1 > 2.09 — band not fired |
| sqlite3.c, blind 5k | 6.3% | 6.5% | 6.3 ≤ 7.15 — band fires mechanically |

The code-blind cell fires the ±10% band, and it is reported here rather
than hidden. It does not adjudicate the kill, for two reasons. First, the
frozen kill attaches to the frozen 10,000-revision schedule; the blind-only
replay is a crew-added subset. Second, the blind schedule contains no
signal by construction (uniform-random revision spans), so "at random" is
the *correct* outcome — beating random there would mean hallucinating
structure from noise or leaking ground truth. The 6.3-vs-6.5 gap on
n=315 is statistical noise either way. What the diagnostic bounds is the
claim's scope: Z6 consolidates revision-correlated boundaries; it does not
discover ground-truth structure from uncorrelated revisions.

### Reading the result honestly

1. The all-schedule scar rates (62.5%, 90.9%) beat random by 12–31×. This
   is expected to favor scars: the frozen schedule plants half its
   revisions exactly on ground-truth units (trainer-side), simulating the
   theory's premise that real revisions happen at meaningful boundaries.
   The trial is not vacuous — the arm never sees which revisions are
   planted, and must still accumulate density, propose endpoints, and
   displace cuts correctly (a broken mechanism fails here via clause B).
2. The blind diagnostic shows the mechanism does not hallucinate: from
   pure-noise revisions it produces ~random boundaries.
3. `GT_WIN=64` is the crew's preregistered interpretation (one grid cell);
   the frozen row states no tolerance. Exact-match counts are computable
   from the evidence but are not the adjudication basis (ARM_SPEC §8).

## Supporting legs (1x, all byte-identical ×2)

| Leg | Result |
|---|---|
| M1 prose | recall 100.0%, boundary 100.0%, 84,731 units |
| M1 code | recall 100.0%, boundary 100.0%, 148,678 units |
| M2 T1/T2/T3 | etc=1 both corpora, ep0_recall=0.0 (no leak), M9 clean class |
| M3 | 100.0% valuable survival, 87.4% fresh recall, 500 evictions, 50/50 weakens, freeze 0 |
| M4 prose/code | repaired 100.0%, content 100%, boundary 100%, lineage ok, 200 repair ledger entries each |
| M5 | deliberate-storage ratio 2.437 **[PROVISIONAL-PENDING-FREEZE]** |
| M6 code→prose | test scar 62.5% vs 2.2% random, 1,395 displaced (policy transfers) |
| M6 prose→code | test scar 90.9% vs 7.1% random, 3,252 displaced (policy transfers) |
| M7 | ID layer live; 200 genuine resolve, 100 forged rejected |
| M8 | 5 perturbations × 2 runs: sha256(image, audit, state, alloc-trace) byte-identical across all 12 runs |
| A15 | 64/64 ID-remap probes **[PROVISIONAL-PENDING-FREEZE]** |

## Bottom line

Z6's scars are not decorative (clause B dead: ~98–99% of proposals
displace bootstrap cuts) and beat the same-count random control 12–31× on
the frozen trial on both corpora (clause A dead). The claim survives. The
honest scope bound: scars consolidate boundaries where revisions actually
happen; from uncorrelated revisions they recover nothing — which is the
mechanism behaving correctly, not a second kill.
