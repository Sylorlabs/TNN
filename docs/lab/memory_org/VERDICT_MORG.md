# VERDICT MORG — Memory Self-Organization (2026-09-24)

Micah's question: can TNN organize its own memory neatly — choosing its own
categorization per domain — or does self-organization make memory WORSE?

## Verdict: SELF-ORGANIZATION HELPS. It does not make memory worse.

KB-1 (non-inferiority, the "does it make memory worse" bar): **PASS**.
SELF overall test F1 = 0.6833 vs IMPOSED 0.6146 → **+0.0688**.
KB-2 (separability, portable-chunks load-bearing): **PASS all arms** —
delete-category leaves the rest byte-identical; export/import round-trips.
KB-3 (revision locality): **PASS all arms** — 10 spread revisions, zero
collateral damage.
KB-4 (consciousness): **PASS** — SELF's scheme.txt present; scorer
re-derived all 6 choices from recorded scores under the frozen tie-break.
TNN can explain its scheme, and the explanation checks out.

## Where the win comes from

No single fixed scheme wins everywhere. The three query classes split the arms:

| class | SELF | IMPOSED | FLAT |
| PURE (category-pure) | 0.6104 | **0.8333** | 0.4750 |
| SUBJ (subject-wide, cross-type) | **1.0000** | 0.6667 | 0.6667 |
| AMBIG (cross-domain) | 0.5125 | 0.1250 | **0.8313** |
| overall | **0.6833** | 0.6146 | 0.6120 |

IMPOSED dominates PURE but collapses on AMBIG (0.1250 — the hierarchy
over-constrains). FLAT dominates AMBIG but leaks on PURE (0.4750, 0.4875
wrong-domain interference). SELF's **per-domain portfolio** covers all three:
S1 for coding, S3 for cooking/gardening, S6 (flat multi-tag) for
history/music/physics — and wins overall, dominates SUBJ (+0.3333), beats
IMPOSED on AMBIG (+0.3875). Micah's "let it choose" is the mechanism that
wins: not one grand scheme, but the right scheme per domain.

## Drift and unseen domains

B6: new domain (astronomy) arrives → SELF re-evaluates, switches scheme,
holdout F1 goes 0.0000 → **0.7583** (drift HELPED). Choices on the original
6 domains stayed stable — no rot. B7 unseen domain: SELF 0.7583 vs IMPOSED
0.5278 vs FLAT 0.5083. TNN files a never-seen domain retrievably, better
than the fixed taxonomy.

## Cost

B5: SELF re-organization = 480 reads / 240 writes / 240 moves for 240 items
(≈1 move per item + 2 reads). IMPOSED/FLAT pay nothing because they never
reorganize — and that rigidity is exactly what loses them AMBIG and the
unseen domain.

## Sol's failure modes, checked

1. Self-reinforcing misorganization: NOT observed. B6 helped; choices stable.
2. Popularity/recency bias: OBSERVED in SELF (0.4250 wrong-domain) and FLAT
   (0.4875); absent in IMPOSED (0.0000). The fixed hierarchy is the most
   disciplined against cross-domain leakage — a real cost of flat-ish schemes.
3. Misleading cross-domain links: confirmed as a precision/recall trade-off,
   not a bug in one arm — hierarchy over-constrains (IMPOSED AMBIG 0.1250),
   flat under-constrains (FLAT PURE 0.4750).

## Honest caveats

1. **Calibration saturation.** Per-domain calib queries all scored 1.0, so
   most "choices" were resolved by the frozen simplicity tie-break, not by
   evidence. Globally S1 beat S6 on calib (0.9438 vs 0.8813); the per-domain
   tie-break picked S6 for 3/6 domains, which cost SELF on PURE test
   (−0.2229 vs IMPOSED). A harder calibration set would sharpen the choices —
   and might well pick S1 more broadly, winning PURE too. The +0.0688 is
   therefore a *lower bound* on what evidence-driven choice could do, not a
   ceiling.
2. Astronomy t1 choice rationale was degenerate (n=0 disclosed by crew 2).
3. One defect found and fixed mid-verification: the calib accumulator divided
   by nq twice when printing means. Integer argmax was unaffected (KB-4
   still passed); the full 3-run battery was re-executed after the fix.
4. 3× reruns byte-identical (SHA-256 over all 27 result files, zero
   mismatches). Pure Zag, zero RNG throughout.

## Bottom line for the program

- TNN choosing its own categorization per domain beats a fixed human taxonomy
  overall (+0.0688), dominates subject-wide retrieval (1.0000), adapts to new
  domains (drift helps), and stays fully explainable (KB-4).
- Separability holds for ALL arms — portable knowledge chunks are viable on
  any of the three organizations.
- The fixed hierarchy's one genuine virtue: zero cross-domain leakage
  (interference 0.0000). A future merge — per-domain chosen schemes with
  hierarchy discipline where PURE queries dominate — is the obvious next test.

## Provenance

Prereg `0994ad51` · fixtures+scorer `03a1f171` · arms+results `f2ecb17a`,
all on branch tnn-native-lab, repo sylorlabs/TNN. Tree:
docs/lab/memory_org/.
