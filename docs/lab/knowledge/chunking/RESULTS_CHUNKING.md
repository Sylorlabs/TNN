# RESULTS_CHUNKING — Is chunking needed, and can TNN derive it itself?

Trial executed 2026-09-22 per `PREREG_CHUNKING.md` (commit
`13de4c3348b71ce5eaefdc97f0125303d492bb1d`).

## Plain verdict

(a) **Is chunking needed at all? YES — but only in one direction.**
Whole-item conjunction (no chunking) is perfect on short items and on
long-range POSITIVE items (S1 24/24, S2 24/24), and it does not collapse at
20–30KB. Where it fails, it fails structurally: on S3 (POS about subject A,
NEG about unrelated subject B) it over-merges and endorses every item
(0/16). So the byte stream does not need chunking to *find* distant
evidence — it needs chunking to *scope* the conjunction so unrelated
evidence does not merge.

(b) **Can TNN derive chunking itself, or must it be imposed? SELF-DERIVED
WINS.** The ADAPTIVE arm (boundaries from `\n\n` structure + a 1600-byte
lookahead that extends a chunk through a found conjunction partner) scored
**80/80 (100%)** — beating both imposed grids (FIXED-64 67.5%, FIXED-512
71.2%) and whole-item (77.5%). It kept every S2 long-range reference intact
*and* fixed whole-item's S3 over-merge. The imposed grids cannot do both:
FIXED-64 destroys all long-range reference (S2 0/24); FIXED-512 destroys
most of it (S2 3/24).

Boundary, stated honestly: ADAPTIVE's win rides on the lookahead parameter
W=1600 sitting between the battery's S2 band max (1500) and S3 band min
(2000) — see caveats. Within this battery the answer is clean; in the wild,
choosing W (or learning it) is the remaining hard problem.

## Kill bars

| bar | result | numbers |
|-----|--------|---------|
| KB1 (ADAPTIVE − better-FIXED ≥ 20pp on S2+S3) | **MET** | 100.0% − 47.5% = **+52.5pp** |
| KB2 (WHOLE − FIXED64 ≥ 20pp on S2) | **MET** | 100.0% − 0.0% = **+100.0pp** — fixed windows destroy long-range reference; battery valid |
| KB3 (WHOLE ≥ 90% on LONGEST, zero crashes) | **accuracy clause NOT MET — structurally, as declared pre-freeze** | 2/4 = 50.0%. WHOLE's naive conjunction necessarily over-fires on the 2 S3-style LONGEST items (ceiling 50%). No-collapse substance holds: **zero crashes/panics** at 20–30KB, S2-style LONGEST 2/2, identical behavior to short items |
| KB4 (ADAPTIVE ≥ WHOLE on S3) | **MET** | 100.0% ≥ 0.0% — adaptive fixes the over-merge |

## Per-kind accuracy (ok/total)

| arm | S0 (12) | S1 (24) | S2 (24) | S3 (16) | S2+S3 (40) | LONGEST (4) | ALL (80) |
|-----|---------|---------|---------|---------|------------|-------------|----------|
| WHOLE | 100.0 | 100.0 | 100.0 | 0.0 | 60.0 | 50.0 | 77.5 |
| FIXED64 | 100.0 | 100.0 | 0.0 | 100.0 | 40.0 | 50.0 | 67.5 |
| FIXED512 | 100.0 | 100.0 | 12.5 | 100.0 | 47.5 | 50.0 | 71.2 |
| ADAPTIVE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DIAGUNION | 100.0 | 100.0 | 100.0 | 0.0 | 60.0 | 50.0 | 77.5 |

Notes:
- FIXED-64/512 get S3 "right" for the wrong reason: they shatter the item
  so POS and NEG never co-occur in a window (S2 0/24 is the price).
- DIAGNOSTIC FIXED-512-UNION is byte-identical in verdicts to WHOLE
  (62/80 both): windowing without per-chunk verdict scoping changes
  nothing — the failure is verdict scope, not boundary placement.

## Mechanism detail (from manifest offsets)

Fraction of S2 items where FIXED places POS and NEG in different windows:
FIXED-64 **24/24 (100%)**; FIXED-512 **21/24 (87.5%)** — the 3 it keeps
together are the closest band (300–700), which is exactly its 3/24 S2 score.

## Cost (byte comparisons inside has_sub; mean per-item ratio vs WHOLE)

| arm | total | mean ratio vs WHOLE |
|-----|-------|---------------------|
| WHOLE | 1,273,430 | 1.00x |
| FIXED64 | 1,472,762 | 1.65x |
| FIXED512 | 1,678,284 | 1.71x |
| ADAPTIVE | 5,046,118 | 4.39x |
| DIAGUNION | 3,137,979 | 2.83x |

ADAPTIVE pays ~4.4x for re-scanning chunk prefixes at each candidate
boundary plus lookahead scans. It is the most expensive arm and the only
correct one — the cost buys the verdict.

## W-sensitivity (ADAPTIVE, diagnostic)

| W | S2 (24) | S3 (16) | S2+S3 (40) |
|---|---------|---------|------------|
| 800 | 45.8% | 100.0% | 67.5% |
| 1600 (frozen) | 100.0% | 100.0% | 100.0% |
| 3200 | 100.0% | 0.0% | 60.0% |

W is load-bearing and two-sided: too short and long-range reference dies
(S2 collapses at W=800); too long and the arm degenerates to WHOLE
(W=3200 endorses everything, S3 0/16 — identical to WHOLE's 60.0%).

## Determinism

`run1.log` vs `run2.log` (ALL arms, 400 verdict lines): **byte-identical**.
W=800 and W=3200 runs likewise byte-identical across repeats. Zero RNG in
generator, binary, and analysis. No crashes/panics at any length (max item
24,220 bytes).

## Caveats (honest)

1. **The battery told ADAPTIVE the right scale.** S2 bands top out at 1500
   bytes and S3 separation starts at 2000, with W=1600 declared in the
   prereg — so the "self-derived" win is really "structure-derived
   boundaries + a correctly chosen lookahead scale." The W-sensitivity
   table proves the scale is doing real work. Whether TNN can select W
   itself (or learn it per domain) is untested and is the obvious next
   question.
2. **KB3's accuracy clause was unachievable by construction** (declared in
   the prereg before the battery existed): with 2 S3-style LONGEST items,
   WHOLE's ceiling is 50%. The informative result is no-collapse: no
   crashes, S2-style LONGEST 2/2.
3. **Generator amendment (documented, not hidden).** The frozen generator
   (`sha256 00dd81eb…b9aa28cc5`, committed in the prereg batch) FAILED
   LOUDLY on its own assertion before producing any battery: the full
   templates place the S1 pair ("fantastic","6 am") 64 bytes apart,
   violating the frozen ≤60 spec — the fail-loud design worked as intended.
   Two further fit assertions tripped during construction (S2 2KB floor,
   exact-fill remainder). The amended generator
   (`sha256 d3b9d51b…fdf66b3db`) differs only in: (a) S1 uses compact
   clauses carrying the same verbatim markers on the same subject
   (POS_S1/NEG_S1); (b) S2 trailing filler tops items up to 2KB within the
   4–8 paragraph budget; (c) exact-fill accepts the −1 remainder (perfect
   fit). Battery spec — counts, bands, labels, verdict rule — is unchanged.
4. Markers are the small closed lists from `delib_si2.zag`; real prose has
   open-ended paraphrase. The structural finding (scope the conjunction;
   derive boundaries from structure) should transfer, but the 100% is a
   battery number, not a real-world number.
5. `has_sub` comparison counts are a lower bound on ADAPTIVE's true work:
   paragraph-break scanning is not counted.

## Artifacts (this commit)

`chunk.zag` (trial binary source, pure Zag), `analyze.py`,
`manifest.tsv`, `items.txt`, `items/` (80 items), canonical logs
`run1.log`/`run2.log` (byte-identical), `run_w800_1.log`,
`run_w3200_1.log`. Prereg: `PREREG_CHUNKING.md` (commit 13de4c33).
