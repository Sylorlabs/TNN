# Preregistration: Beam Redesign Build (Niching + Tax Annealing + Diverse IV)

Status: FROZEN. This prereg's first commit strictly precedes any
beam_impl implementation or run. Design: BEAM_REDESIGN.md (27a8fd108),
sections 4 (frozen parameters), 6 (builder protocol), 7 (falsifiers).
R3 baseline: 023b4f84a (R3-FAIL; Arm 1 PASS, Arm 2 FAIL; 3/3
byte-identical md5 7ed09fda269b59cdbbf75e0df720661c).

## 1. Question

Does the A+B+D beam redesign let the Q4 reuse mechanism discover the
true compositional form E = (D AND Y4) OR ((NOT D) AND Y5) where the
frozen greedy beam failed (R3 Arm 2: reuse 53/64, never 64/64)?

## 2. Frozen design parameters (adopted verbatim from design sec 4)

- Beam width: 32 total, unchanged.
- Species signature: (tree depth, sorted operator multiset), computed
  generically from each candidate expression tree. No target, family,
  or library knowledge enters the signature. Encoding (deterministic):
  key = (((depth*8 + nAND)*8 + nOR)*8 + nNOT)*8 + nXOR, via iterative
  DFS with an explicit stack (shared subexpressions counted per visit).
- Keep rule: top 4 per species, at most 8 species. If more than 8
  species are non-empty, merge the two smallest (fewest members, tie
  broken by lower best score, then lower species key) until 8 remain;
  a merged species keeps the top 4 of the union. If fewer than 8,
  fill remaining slots from the global score ranking.
- Beam layout (frozen): slots 0..S-1 hold the S species champions
  (top 1 per species), ordered by (champion score desc, champion opc
  asc, champion node asc, species key asc). Remaining slots hold
  runners-up (2nd/3rd/4th per species, species order), then global
  rank fill. beam[0] remains the global best, preserving the BEST
  convention used by phase1/phase2.
- IV hypothesis set: top 1 per species, up to 8 hypotheses. Realized
  by the beam layout above: select_iv is UNCHANGED and reads the
  first min(8, beam_n) beam slots, which are now the species
  champions. The disagreement machinery itself is untouched.
- Tax schedule: tax(t) = round(200*t/25) = 8t for extension round t
  in 0..24. Threaded as an explicit parameter: score =
  (c*10000)/en - tax*opc. phase1 (kept compiling, not run by main):
  loop r passes t=r, final extend passes t=24. phase2: initial extend
  passes t=0, loop iteration r passes t=r+1.
- Compute guard: candidate generation and per-candidate evidence
  scoring are byte-identical in structure to the frozen beam; the
  only additions are species-key tree walks (no node_pred calls, no
  evidence simulations). Per-round candidate simulation count is
  therefore unchanged by construction.
- All tie-breaks are deterministic; no RNG enters selection.

## 3. Protocol

1. Control first: extract the frozen q4_r3.zag at 023b4f84a, compile
   with the same znc, run 3x. K2 requires all three runs
   byte-identical with md5 7ed09fda269b59cdbbf75e0df720661c and the
   R3-FAIL verdict (A1-PASS 1, A2-PASS 0). This confirms the baseline
   still fails identically before any new code is trusted.
2. Implement beam.zag as a copy of the frozen source with ONLY these
   changes: species_key fn (new), score_node takes tax, beam_extend
   takes tax and performs niching selection, phase1/phase2 pass the
   round-derived tax. No sealed(), terminal, passive, IV, keep-bar, or
   main-arm logic is touched. The frozen q4_r3.zag stays untouched.
3. Compile with znc 2026.07.0-dev. Run 3x. All runs must be
   byte-identical (md5), zero stderr.
4. Score Arms 1 and 2 under the R3 prereg bars (unchanged):
   - Arm 1: reuse final_true = 64/64 AND reuse_iv*2 <= scratch_iv.
   - Arm 2: reuse final_true = 64/64 AND reuse_iv*2 <= scratch_iv AND
     HAS_D = 1.
   Arm 3 stays DEFERRED.
5. Pure Zag at every stage: implementation, compilation, execution,
   verification. Zero Python anywhere, including byte checks (shell
   grep only). Zero em/en dash bytes in loop docs (shell-verified
   before commit).

## 4. Kill bars

- K1 (prereg frozen before implementation): PASS iff this prereg
  commit is a strict ancestor of the implementation commit and no
  beam.zag existed at prereg time (commit-order self-check).
- K2 (control reproduces R3-FAIL): PASS iff the control binary's 3
  runs are byte-identical with md5
  7ed09fda269b59cdbbf75e0df720661c and report R3-PASS 0 with
  A1-PASS 1 and A2-PASS 0.
- K3 (pure Zag, deterministic): PASS iff the new beam binary's 3
  runs are byte-identical (md5), zero stderr, and zero Python was
  used at any stage.

## 5. Falsifiers

- F-DIVERSE-FAIL: Arm 2 still fails its bar after a faithful build
  of section 2. The design is wrong, not just unbuilt.
- F-REGRESS: Arm 1 passes on the control and fails on the new beam.
  The fix breaks what worked.
- F-BLOAT: per-round candidate simulations exceed the old beam's
  count by more than 10 percent on any round. Diversity must not be
  bought with simulation budget.
- F-CASE: any fix component keys on target, family, or library
  identity (sealed-world, fam, or lib-signature branching in the
  search machinery). Generic machinery only; a dedicated semantic
  case kills the build on the spot.

## 6. Verdict

- BEAM-PASS: A1-PASS = 1 AND A2-PASS = 1 on the new beam, K1-K3 all
  PASS, no falsifier fired.
- BEAM-FAIL: any other outcome. The result names which bar or
  falsifier decided.

## 7. Honest scope

Bounded-L2 reuse robustness for one compositional form at most. No
L3 claim, no Criterion 0 claim, no Q4 revival (the conjunction is
dead: R1-FAIL, R3-FAIL, R4-FAIL). If BEAM-PASS, the defined next
target from R3 is met at the mechanism level; transfer, ablation,
and red-team steps remain future work under their own preregs.

Builder label: PREREG (frozen, awaiting implementation).
