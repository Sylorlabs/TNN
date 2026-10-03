# XDOMAIN-L2-TS REPORT: Cross-Domain L2 TRUNCATE and SPECIALIZE Adaptation

Date: 2026-10-02. Branch: tnn-native-lab. All commits local; nothing pushed.

## Question

XDOMAIN-L2-COMPLETE showed H1/H2 driving L2 adaptive reuse via one
adaptation shape (REBIND: relation rebinding) on arithmetic to planning.
The follow-up: do H1 and H2 also drive DIFFERENT adaptation shapes,
TRUNCATE (X produces a longer structure than the downstream contract
accepts) and SPECIALIZE (X is too general for what the downstream
computation needs), on a NEW sealed world, with the LEARNER selecting the
correct operator per goal?

## Design (frozen in PREREG.md, commit 0a489b19c, before implementation)

New sealed world, relation 61 throughout (no relation shift; the
adaptation under test is not rebinding):

  World-T (truncate): sealed subject 103, facts
    (103,61,3) (103,61,1) (103,61,4) (103,61,1) (103,61,5).
    X=SWEEP (behav 0) collects 5 readings, sig NODE->SEQ5.
    Y1=PLAN3 (behav 1) sums exactly 3, sig SEQ3->NUM.
    D=RISK3 (behav 2) products exactly 3, sig SEQ3->NUM (semantic distractor).
    Z-T = (103,93) -> 8 needs TRUNCATE(X,3) = [3,1,4], PLAN3 = 8.
    X is too long: exact L1 reuse is blocked by the SEQ5 vs SEQ3 contract.
  World-S (specialize): sealed subject 104, facts
    (104,61,2) (104,61,7) (104,61,3) (104,61,8) (104,61,4).
    X=SWEEP, sig NODE->SEQ5.
    Y2=TOTAL (behav 3) sums all readings, sig SEQANY->NUM.
    Z-S = (104,94) -> 15 needs SPECIALIZE(X,7) = [7,8], TOTAL = 15.
    X is too general: L1 (SWEEP,TOTAL) gives 24, contract validates but
    the goal does not.

Generic operators (researcher-built machinery; selection learner-driven):
TRUNCATE (copy MAP, keep first k, sig_out=SEQk, truncate_of provenance)
and SPECIALIZE (copy MAP, keep values >= T, sig_out=SEQANY,
specialize_of provenance). Candidate lengths: k in 1..(len-1) from the
observed sweep length. Candidate thresholds: distinct observed values of
the query subject, first-seen order. Phase 2 tries SPECIALIZE then
TRUNCATE (fixed order) over all candidates, exhaustively, recording every
success; exactly one success per world is required.

## Implementation

- ts_h1.zag: H1 typed contracts + TRUNCATE/SPECIALIZE. Follows the
  xdomain_l2 H1 lineage (contract filtering, two-phase solver). New:
  sequence kinds (SEQk=10+k, SEQANY=20, optimistic compatibility),
  SWEEP/PLAN3/RISK3/TOTAL behaviors, the two operators, exhaustive Phase 2
  with per-world success accounting. 10 arms (5 per world). Compiles
  warning-free with the pinned znc.
- ts_h2.zag: H2 value composition + TRUNCATE/SPECIALIZE. Follows the
  xdomain_l2 H2 lineage (ordered mode pairs, capability evidence via
  has_behav). New: stage 1 writes a shared sequence buffer that stage 2
  reads; operators apply to the stage 1 output. 10 arms. Compiles
  warning-free.
- Both: pure Zag, 0 new modes, 0 bridges, 0 handlers, 0 new semantic
  cases, single preallocated output buffer with one raw syscall write at
  the end (no _zag_print, per the 2026-10-02 znc miscompile workaround).

## Implementation bugs found and fixed during trace audit (prereg untouched)

Two bugs were caught by auditing the first run traces against the prereg
predictions, BEFORE any verdict was claimed. Both were fixed in the
implementation only; PREREG.md was never edited.

1. Fact entry stride: entries were laid out at 12-byte stride for four
   4-byte fields, so each entry's object field overlapped the next
   entry's used flag. With 21 facts the 21st fact landed outside the
   40-entry scan range and was silently dropped (subject 103 swept 4
   readings, not 5; the sealed world did not match the prereg). Fixed:
   16-byte stride, regions relocated.
2. MAP slot exhaustion: 10 slots but Phase 2 can create up to 12 MAPs
   (taught + 5 specialized + 4 truncated + 1 composite). The 11th created
   MAP overlapped the candidate/seqbuf region and was corrupted into a
   phantom second success (a TRUNCATE map read back as SPECIALIZE).
   Fixed: 16 MAP slots.

Both fixes make the implementation faithful to the frozen prereg. The
traces below are from the fixed build.

## Results

Kill bars K-TS-1 through K-TS-7 are frozen in the prereg. All seven PASS,
for both mechanisms.

- K-TS-1 SEALED-REQUIRES-ADAPT: PASS. Established jointly by K-TS-2
  through K-TS-4: Z-T is solvable only via TRUNCATE (X too long),
  Z-S only via SPECIALIZE (X too general).
- K-TS-2 L1-NECESSARILY-FAILS: PASS both. H1 L1-ONLY-T: no pair
  type-checks (SEQ5 vs SEQ3), L1-FAIL. H1 L1-ONLY-S: (SWEEP,TOTAL)
  gives 24, rejected. H2 L1-ONLY-T: stage pairs fail (5 vs 3).
  H2 L1-ONLY-S: (SWEEP,TOTAL) gives v2=24, rejected.
- K-TS-3 CORRECT-OPERATOR-SELECTED: PASS both.
  H1 World-T: SPECIALIZE over {3,1,4,5} all rejected (12/60 on T=3,
  length rejects on T=1,4,5); TRUNCATE over {1,2,3,4}: only k=3
  validates ([3,1,4] -> 8; RISK3 gives 12, rejected). Exactly 1 success,
  op=TRUNCATE, k=3.
  H1 World-S: TRUNCATE over {1,2,3,4} all rejected (2/9/12/20);
  SPECIALIZE over {2,7,3,8,4}: only T=7 validates ([7,8] -> 15).
  Exactly 1 success, op=SPECIALIZE, T=7.
  H2: identical outcomes via stage pairs (T: m1=1,m2=2,op=1,param=3;
  S: m1=1,m2=4,op=2,param=7), each the single success.
- K-TS-4 ADAPTED-COMPOSITION-WITH-PROVENANCE: PASS both.
  H1 TREAT-T trace: Z-COMP z=10 a=9 b=1 with
  Z-PROV adapt_of=0 op=1 param=3 (comp_b=Y1).
  H1 TREAT-S trace: Z-COMP z=4 a=3 b=1 with
  Z-PROV adapt_of=0 op=2 param=7 (comp_b=Y2).
  H2 TREAT-T: VC-COMPOSE ok m1=1 m2=2 op=1 param=3.
  H2 TREAT-S: VC-COMPOSE ok m1=1 m2=4 op=2 param=7.
- K-TS-5 CAUSAL: PASS both. ABL-X, ABL-Y, FRESH fail in both worlds
  with l2_on=1. H1 ABL-Y-T even tries the distractor D under the
  winning truncation (12, rejected), showing it is tried and discarded,
  not skipped.
- K-TS-6 DETERMINISM: PASS both. 3/3 runs byte-identical.
  H1 sha256: 536d7703f1b9d0e3eca88ad8eafb3b9047c2b2950a023bb089eda22bdb1bd3b5
  H2 sha256: 3883a937e1a7167c185bb1916fbd147614e9f307c5470915be501047b93d5e4f
- K-TS-7 PARAMS-DISCOVERED: PASS both. grep audit: the goal values
  (8, 15) and discovered parameters (3, 7) as domain values appear only
  in add_fact world-setup lines, arm-harness query literals, and arm
  verdict oracles; the operator (truncate_map/specialize_map),
  candidate-scan (scan_values), and composer (try_pair/solve_z,
  vc_stage/vc_try_pair/vc_compose_l2) logic is literal-free. The
  candidate pools and the winning parameters come from the generic
  sealed-world scans.

## Per-mechanism adaptive scores

- H1 (typed contracts + TRUNCATE/SPECIALIZE): 7/7. Solves Z-T only via
  TRUNCATE k=3 (contract-blocked L1, distractor rejected on value) and
  Z-S only via SPECIALIZE T=7 (contract-valid L1 rejected on value).
- H2 (value composition + TRUNCATE/SPECIALIZE): 7/7. Same outcomes via
  stage pairs with the shared sequence buffer; the winning
  (op,param,m1,m2) is the single success in each world.

## Honest analysis

1. What is actually demonstrated: given two generic adaptation operators,
   both H1 and H2 select the correct one per sealed goal and discover the
   correct parameter from the sealed world, on a world structurally
   different from the rebind world (sequence length/contract mismatch and
   over-generality instead of relation shift). This is L2 adaptive reuse
   with new adaptation shapes, not L1 exact reuse and not L3 invention:
   the operators themselves are researcher-built.
2. "Selection" is exhaustive try-and-validate against the sealed goal,
   the same honest boundary as the rebind work. The learner does not
   reason about which operator fits; it tries both and the goal
   discriminates. The fixed try order (SPECIALIZE before TRUNCATE) is
   scaffolding; the evidence is the try-and-reject trace, not the order.
3. The domain gap here is modest by design (sensing/aggregation to
   planning); the novelty under test is the operators and their
   per-goal selection, stated in the prereg.
4. Expected answers are used for verification (same as the H1/H2
   lineage); learner-owned verification remains future work.
5. The two implementation bugs are reported plainly because the second
   one (phantom success from region overlap) is exactly the class of
   false positive that trace auditing exists to catch. The verdict rests
   on the fixed build's traces, which match every prereg prediction
   value for value.

## Verdict

XDOMAIN-L2-TS-COMPLETE. K-TS-1 through K-TS-7 all PASS for H1 and H2.

## Build record

- Pinned znc (sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
  safebin PATH, zero Python invocations (see NAMECHECK.md Step 0).
- ts_h1.zag -> ts_bin_h1, ts_h2.zag -> ts_bin_h2: both compile
  warning-free; 3/3 runs byte-identical (sha256 above).
- Commit order: 0a489b19c PREREG freeze (PREREG.md only), then
  implementation sources, then binaries, run outputs, compile logs,
  NAMECHECK.md, REPORT.md. All local on tnn-native-lab; nothing pushed.
- No em dashes or en dashes in any file (grep verified).
