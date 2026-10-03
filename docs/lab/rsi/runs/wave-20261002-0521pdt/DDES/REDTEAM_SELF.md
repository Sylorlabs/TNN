# SELF RED TEAM: DDES steps 7+8

Wave: wave-20261002-0521pdt. Lane: DDES.
Target: the step-7 OOD BUILD-PASS and step-8 ablation BUILD-PASS
reported in SEALED_EVAL.md and ABLATION.md.

## R1: knowledge vs architecture (am I testing what I built?)

Attack: the six OOD worlds were designed by the same worker that
wrote the derivation code, so "OOD" could be theater: worlds the
machinery was already shaped to handle.

- The prereg froze all six world definitions before the
  implementation file existed, with a full prediction table
  including a negative control (O6, predicted LOUD-FAIL). The
  predictions were falsifiable and specific (exact TARGET,
  plan shape, PRED values, per-config eliminations).
- Structural difference from the repair families is real:
  two-hop chains (O1, O4, O6), t*=12 (O2), competing frontiers
  (O3), fan-in (O5), decoys (O4). The repair-family worlds were
  all single-hop from X with t* in {0,1,2,3,4}.
- Counter-evidence the worker could not have tuned away: O6 was
  predicted to fail loudly, and it did; V_nofrontier was
  predicted to change only the experiment and not the verdict,
  and it did. A theater OOD set would have been all-CORRECT.
- Residual risk (honest): the world designer and the code author
  share a head. The arrival/frontier machinery was written with
  chain support (multi-pass relaxation) already in it, so the
  OOD set tests the machinery's existing generality, not a
  capability discovered after the fact. This bounds the claim to
  "the frozen derivation generalizes to these structures," not
  "DDES invents chain handling." Nothing in the lane claims the
  latter. RISK ACCEPTED with the bound stated.

## R2: metric gaming (could the numbers be gamed?)

Attack: CELLSUM verdict labels are emitted by the worker's own
code; a bug or bias in the verdict logic could inflate CORRECT.

- The verdict logic is the frozen convention from the DDES line
  (converge iff p0 != p1 and exactly one prediction matches the
  executed real; CORRECT iff both configs converge with the true
  hypothesis surviving). It is identical across all five
  variants; any systematic bias would hit V_full and the
  ablations alike, and the ablation verdicts are RELATIVE
  (flips vs V_full), so a uniform bias cancels.
- The kill bars do not count CORRECT labels alone: (7b) requires
  exact decision-line matches against the prereg prediction
  table, which was frozen before implementation. Gaming the
  verdict label without matching TARGET/PLAN/EXEC/PRED lines
  would fail (7b).
- SILENT-WRONG is the metric that would expose gaming, and it
  appears exactly where the mechanism predicts (V_noclamp on
  t*=0 worlds), counted against C1 rather than hidden.
- The ablation verdict rule is mechanical (flips vs V_full),
  not judgmental. No room for re-labeling a flip as a pass.

## R3: presentation fabrication (are the transcripts real?)

Attack: docs could describe runs that never happened or cherry
pick cells.

- One binary, one deterministic transcript per run; 3/3 runs
  byte-identical with sha256 recorded in SEALED_EVAL.md:
  f7a7ec52bd642604c9ffc3619a72836674de4bc8a4e0d11b5895306c56dda074.
  All 30 cells (5 variants x 6 worlds x 2 configs) are in the
  same transcript files (run_78_1/2/3.txt); there is no
  separate per-cell execution to cherry pick from.
- Build stderr is exactly the 93-byte zagd warning; run stderr
  is 0 bytes every run; exit 0 everywhere. Binaries and
  transcripts are committed in the lane dir for independent
  re-execution.
- The docs quote exact transcript lines (TARGET, PLAN, PRED,
  CELLSUM) that any reviewer can grep in the committed files.

## R4: the unconsumed-marker rule applied to this lane

The DDES-ALT H1(b) rule (judge on decision lines, not print
lines) was applied mechanically: the diff table in ABLATION.md
excludes FLAG lines and variant labels. Spot check: V_noclamp
on O1/O2/O4/O5 is decision-line IDENTICAL to V_full; had the
comparison included FLAG lines, nothing would change (FLAG
appears only on t*=0 worlds, where the decision lines already
differ). The rule did not rescue or sink any verdict.

## R5: could step 8's "PARTIALLY-LOAD-BEARING" be a hedge?

Attack: C3's verdict could be read as the worker avoiding a
hard call.

- The mechanical rule left three outcomes; C3 met the middle
  one exactly: decision lines change on O3 (TARGET V*=1 t*=2
  vs V*=2 t*=0, different plan, different PRED), zero verdict
  flips. Calling it DECORATIVE would require byte-identical
  decision lines (false); calling it LOAD-BEARING would require
  a verdict flip (false). The middle verdict is forced by the
  frozen rule, not chosen. Its honest reading: frontier
  selection changes experiment choice under competing
  frontiers; on this set that never changes the verdict.

## Red-team verdict

No kill found against either step verdict. Step 7 BUILD-PASS
and step 8 BUILD-PASS stand with the bounds stated: bounded L2
guided generation on a sealed but worker-designed OOD set; the
three binding caveats still bind every citation; no L3 claim;
no new modes, bridges, handlers, or semantic cases.
