# R5-PRIMARY VERDICT — KB4 autopsy Type A replication

**Verdict: REPRODUCED.**

Independent Type A replication of the KB4 autopsy under the 2026-09-22
"run everything" ruling. All probes rebuilt from committed sources with the
pinned toolchain, run 3× byte-identical each, and scored by an independent
pure-Zag verifier. Every observed number matches the committed number;
every structural sub-claim checked out; no hole found in the impossibility
argument.

## Frozen pins (observed 2026-09-23 UTC, before any run)

- Evidence commit: `66fbb329aa831c14f3f3100a20e177bbb12e27b1`
- `docs/lab/kb/autopsy/` @ that commit: tree `b4585b7123c0a8dd430202c60b802b7715468d29` — **exactly 37 files**
- WHY_REPORT commit: `bc6d130539e4a5539ea3361f57e02e39378f26ba`
  (`docs/lab/kb/autopsy/WHY_REPORT.md` blob `bd12da7161fa30b9d24d17d4cf7744f90eb493c6`)
- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`

## Observed vs committed numbers

**Probe outputs:** all 7 probe×batch outputs byte-identical to the committed
`out_*.txt` (sha256 match), and each 3× byte-identical across my own runs.
Zero RNG.

**Scores** (independent pure-Zag scorer `probes/scorer.zag`, Python glue only
for TSV conversion; truth from committed `truth.json` blob
`dd1f4bcb32bd5023dcab254773ffdc534eeba289` and committed `pa1_truth.json`):

| Probe | Observed (mine) | Committed `probe_scores.json` | Match |
|---|---|---|---|
| P-L1 A (L8 removed) | 33/80 = **41.25%**, DEGENERATE | 33/80 = 0.4125, DEGENERATE | ✅ |
| P-L1 B (L8 removed) | 41/93 = **44.09%**, FAIL | 41/93 = 0.44086, FAIL | ✅ |
| P-L2 A (L4 removed) | 93/184 = **50.54%**, FAIL | 93/184 = 0.50543, FAIL | ✅ |
| P-L2 B (L4 removed) | 101/185 = **54.59%**, FAIL | 101/185 = 0.54594, FAIL | ✅ |
| P-A2 A (rebind) | 93/184 = **50.54%**, FAIL | 93/184 = 0.50543, FAIL | ✅ |
| P-A2 B (rebind) | 101/185 = **54.59%**, FAIL | 101/185 = 0.54594, FAIL | ✅ |
| P-A1 (corroboration) | 50/115 = **43.48%**, FAIL | 50/115 = 0.43478, FAIL | ✅ |

**Structural sub-claims** (each independently re-derived from committed evidence):
- L8 removal on A: **0/924** decision flips vs the original frozen gate;
  rate unchanged at 41.25%. L8 did not cause the consistent-error installs.
- L8 removal on B: **exactly 6** flips (INSTALL→WITHHOLD), 5 false + 1 true
  installs removed; 46/99 = 46.46% → 41/93 = 44.09% (−2.37pp ≈ −2.4pp).
- P-A2 ≡ P-L2: INSTALL/WITHHOLD streams **line-identical** (0 mismatches,
  924/924 A, 925/925 B) — the conflict bit was the gate's entire discrimination.
- P-A1: all 50 both-fooled-and-agreeing adversarial fixtures installed;
  43.5% > 41.2% — corroboration fails worse than the single gate.
- WHY_REPORT audit: A = pure match rule **exactly** (0/184 deviations);
  confidence anti-informative on adversarial lines (recomputed means match
  the report to the decimal: A 429.8/439.1, B 849.4/861.4); M3 cells
  **44/184 A (23.9%)**, **31/185 B**. No hole found in the impossibility
  argument. (W1 bit-counts, W3 Python gate model, W5 LP proof scripts are
  uncommitted and were not re-runnable; every checkable quantitative claim
  reproduced exactly.)

## Changes made during this replication

1. Corrected my own verifier bug: Git blob ids are `SHA1("blob <len>\0" +
   content)`, not raw-content SHA1. After correction all 37 evidence files
   verified against the committed tree.
2. Built an independent pure-Zag scorer (`primary/probes/scorer.zag`) as the
   verification authority, replacing the committed Python scorer (which
   hardcodes an uncommitted local path) for this replication.
3. Removed `.zag-cache`/`.zagd.semantic-ready` from the build dir; binaries
   are local-only and will not be committed.

## Corrections to standing prose (documentation-level, no data impact)

1. Tier-1 prereg line 99 says P-A1 fooled "50 of **185** paired fixtures".
   The committed pa1 common batch has **184** adversarial (stim,variant)
   fixtures (A∩B intersection; truth.json holds 184 A-side / 185 B-side
   adversarial keys). The 50 both-fooled fixtures and 50/115 = 43.5% are
   unaffected — the 185 figure belongs to B's standalone adversarial count.
2. AUTOPSY.md's "P-L1 byte-identical on A" holds at decision/score level
   (0/924 flips, 33/80); only the audit evidence column differs where L8's
   +20 no longer prints, which is expected.

## Bottom line

The autopsy's headline stands on replicated evidence: the frozen gate is
Bayes-optimal for its judgment-only input and still fails at 41–46%;
removing the repetition bonus changes nothing load-bearing; removing the
conflict rule exposes ~50%+ raw error; rebinding variants trades errors
1:1; correlated both-senses-fooled defeats corroboration at 43.5%. The
failure is architectural (observational identity of fooled-vs-changed on
the judgment stream), with the learning/config layer complicit, not causal.
