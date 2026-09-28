# NO-STUPID-LIMITS Crew C — L7 text lower bound A/B results (2026-09-24)

Prereg: `~/workspace/scratch_10gb_work/LIMITS_AUDIT.md` §L7.
Scratch dir: `~/workspace/scratch_10gb_work/nolimit_c/`.

## Design

A/B the G1 text lower bound (1 vs 20 vs 100). Measurement: downstream
retrieval precision (P@1) on 300 held-out corpus-derived probes, plus
installed counts by length band. Variants are single-const diffs of the
frozen gate (`gate_l7_1.zag`: bound 20→1; `gate_l7_100.zag`: bound 20→100
AND pads the two frozen must-reject CAL probes R2/R4 to ≥100 chars so they
still reach their expected G2/G3 verdicts — probe purpose preserved).
`bad_l7.bin` (1000 recs, all texts ≥100 chars) keeps the frozen negcontrol
expectation (500/250/250/0) valid at all three bounds.

Corpus `l7_corpus.dat` (200k records, deterministic): 39,997 texts
truncated to 10B, 22,856 to 60B, rest full-length. **Lesson heads protected**
(16 head records drawn from bound-100-passing source records) after V1
showed truncation hitting head positions causes CAL-drop amplification
(see secondary finding). Verified: zero bound-dependent head failures.

Probes `l7_questions.tsv` (300): keyword questions derived from each
record's own text, mirroring panswer's extraction (alnum, len 3–32,
lowercased, non-stop); 150 long (≥100B, installed at all bounds), 75
medium (20–99B, installed at bounds 1/20), 75 short (1–19B, installed at
bound 1). Gold = source record key. Scored with the REAL gate panswer
(`threshold=1`, PA_MAX_PROBES=300, 857 keywords).

## Results

Installs (mirror-predicted exactly; lessons_rejected=0 all; negcontrol
1000/1000 all):
| bound | installed | g1 | g2 | g3 |
|---|---|---|---|---|
| 1 | 193,184 | 0 | 0 | 6,816 |
| 20 | 159,963 | 39,997 | 0 | 40 |
| 100 | 84,511 | 115,478 | 0 | 11 |

Retrieval P@1 (real panswer):
| bound | long (150) | medium (75) | short (75) | overall |
|---|---|---|---|---|
| 1 | 150/150 = 1.000 | 74/75 = 0.987 | 8/75 = 0.107 | 232/300 = 0.773 |
| 20 | 150/150 = 1.000 | 74/75 = 0.987 | 0/75 = 0.000 | 224/300 = 0.747 |
| 100 | 150/150 = 1.000 | 0/75 = 0.000 | 0/75 = 0.000 | 150/300 = 0.500 |

## Reading

1. **The bound is a coverage knob, not a quality knob.** On installed
   content, precision is IDENTICAL across bounds: long 1.000/1.000/1.000,
   medium 0.987/0.987. The bound changes WHAT is installed, never HOW
   WELL the installed content retrieves.
2. **No pollution.** bound=1 admits 33,221 extra short texts into the
   store; medium/long precision is byte-identical to bound=20 (74/75,
   150/150). The short texts steal zero probes from longer content.
3. **The rejected content is weakly retrievable.** bound=1's short texts
   retrieve at 0.107 P@1 even with keywords drawn from the text itself
   (most favorable probe). Nearly — but not quite — useless.
4. **bound=100 is strictly harmful.** Destroys medium-band recall
   (0.987 → 0.000) with zero quality gain anywhere (long stays 1.000).
5. **bound=1 ≥ bound=20 on every metric.** Tiny overall edge (0.773 vs
   0.747) from short-band coverage; identical everywhere else.

## Secondary finding: length-based CAL-drop amplification (from V1 corpus)

With unprotected heads (V1 corpus), bound=20 dropped 3/4 lessons
(131,107 g1; only 52,405 installed) and bound=100 dropped 4/4 (0
installed), because a short text at a lesson-head position fails CAL and
drops the whole 65,536-record lesson. Under bound=1, short texts pass G1,
so length can NEVER cause a CAL drop. This is a structural robustness
argument against the bound independent of the quality measurement: with a
noisy source, the bound converts per-record shortness into
lesson-scale data loss.

## Verdict: KILL the lower bound (tune to 1 / remove the check)

The measurement favors 1 over 20 (weakly on quality, strongly on
robustness); 100 is dominated. The bound provides no precision protection
(the ostensible reason for it), costs recall, and creates a CAL-drop
hazard. Per the prereg decision rule ("keep, tune, or kill by
measurement"): the G1 text lower bound is not load-bearing — remove the
`len<20` check (bound=1 is the measured equivalent; for any real source
they are identical).
