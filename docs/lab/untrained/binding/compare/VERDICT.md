# VERDICT — BINDING confirmatory run, repaired untrained analyzer (2026-09-26)

## Verdict: **PASS**

Zero hallucinations on six fresh, novel inputs. The binding bar ("any
hallucination = FAIL") is met.

## Score

- MATCH: 39
- MISS: 3
- WEAK MISS: 2
- PARTIAL: 3
- HALLUCINATION: **0**

## What the run proved

1. **No invented structure.** On inputs the repaired analyzer never saw
   (novelty proven by Git-blob audit: all 13 input blob IDs absent from
   `tnn-native-lab` history and the repair workdir), every structural claim
   the analyzer made traced to a real, measured property of the input.
   The M1 lag-2 artifact did not recur; the one reported rhythm cycle
   (C3, 0.860 s) is a mathematically exact subharmonic of genuine
   9.3 Hz envelope beating, not the phantom 0.100 s.
2. **The repairs held on novel inputs.** Fine-grained texture reported on
   dense native speckle (C4), "mostly diagonal" on a 40-degree diagonal
   boundary (C5), silence not called a noise bed (C2), quiet-gap pitch
   correctly not interpolated (C2).
3. **The misses are honest-boundary kinds, not inventions:**
   - C1: slow-swell detector needs ≥3 detected swells; only 2 of the 3 true
     swells detected (clip-edge loss) → withheld the real 4 s cycle (MISS).
   - C3: the 250 Hz tone was MEASURED (f0 = 250.0 Hz) but the
     voicing-strength gate (0.495) vetoed it under the inharmonic rumble
     bed → two related MISSes. Named sensitivity gap for the repair line.
   - C1: subharmonic pitch wording (164.9 Hz is the real missing
     fundamental of the 330+495 dyad) and two loose bucket wordings
     (PARTIAL ×3 total with C3's rhythm subharmonic).
4. **Determinism held.** Frozen binary (SHA-256
   53caf89911b80d99e7a70b3b0e52638af3fd5e72de25c5bb729554693b194eae)
   rebuilt from frozen source byte-identically; both runs of all six
   outputs byte-identical.

## Caveats recorded (not bar-failing)

- C4 "left/right differ strongly (asymmetric)": true under the metric's
  mirror-semantics (slr = 0.447, the 40 px period genuinely doesn't mirror);
  the wording risks misreading as content difference. Wording caveat, named
  in the worksheet.
- C6 "motion concentrates left": aggregate-trajectory artifact; the
  traversal is real and left-heavy in aggregate (WEAK MISS).
- The voicing gate's strictness under inharmonic beds (C3) is the one
  genuine sensitivity finding and should be the next repair target.

## Evidence chain

- Seal: commit `206fb3f30` (human descriptions sealed 2026-09-26 20:32:37
  UTC, before any analyzer run).
- This commit: worksheets + verdict + both-run outputs + determinism log
  (on `tnn-native-lab`; binaries, caches, and derived measurement files
  excluded).
