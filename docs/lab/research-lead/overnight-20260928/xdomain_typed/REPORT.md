# REPORT: xdomain_typed -- Cross-Domain Composition via Learned Typed I/O Contracts

## Verdict: XDOMAIN-TYPED-COMPLETE. All 7 frozen kill bars PASS.

## What was built
`xt.zag` (single-file standalone, 300 lines): X = chain-follow (r=81 walk),
Y = count r=82 outgoing, D1 = identity distractor, D2 = count-r=81
distractor. Behaviors installed as previously-learned structures (behavior
induction demonstrated in prior waves). Under test: signature learning and
type-directed composition.

Signature learning: `probe_kind(v)` returns 1=NODE iff v appears as a fact
subject, else 2=NUM. Each teaching query records probe_kind(input) and
probe_kind(output); `finalize_sig` sets the signature by majority once n>=2.
Composer admits pair (A,B) iff sig(A).out == sig(B).in with endpoints
matching the goal kinds. Promotion sets the composite contract by generic
contract composition in(A)->out(B) plus provenance links.

## Results (3/3 byte-identical, sha256
`666a79c213cfa14d6cd009e7edd5e1ecba4406899ec7090da23520650037b83c`)
- Learned signatures: X 1->1, Y 1->2, D1 1->1, D2 1->2. All correct, all
  from behavior observation. Zero per-MAP signature literals in source.
- TREAT: Z=(31,93)->2 solved via Z-COMP z=4 a=0 b=1 (X then Y), 3 verifies
  (Y try r=0 reject, D2 try r=1 reject, (X,Y) r=2 accept). ARM-RESULT PASS.
- Z2=(41,93)->3 solved by direct Z application, 3 verifies. Z2-RESULT PASS.
- NOTYPE: solves with 6 verifies > TREAT 3. Contract prunes the search.
- ABL-X: Z-FAIL (4 tries, all type-compatible candidates exhausted).
  ABL-Y: Z-FAIL (3 tries). FRESH: Z-FAIL (0 tries, no candidates).

## Kill bars
- K1 SOLVE: PASS. Correct composite, correct provenance.
- K2 CAUSAL: PASS. Both fragments necessary; no free solution.
- K3 CONTRACT-CAUSAL: PASS. 6 vs 3 verifies; the type filter does work.
- K4 LEARNED-NOT-ASSIGNED: PASS. Audit: sig writes only in map_new
  (init 0=unknown), finalize_sig (computed from probe observations),
  promote_comp (generic contract composition). No per-MAP literals.
- K5 DETERMINISM: PASS. 3/3 byte-identical.
- K6 NO-TEMPLATE: PASS. No CHAIN_COUNT; Z assembled at runtime.
- K7 REUSE: PASS. Z2 via Z direct, 3 <= 4 verifies.

## Why this matters
Prior wave proved A/B/C all fail cross-domain: they implement navigation
concatenation (admission = plen/relse q, assembly = chain ASM). H1 shows a
structurally different admission principle (learned typed I/O contracts)
enables composition between heterogeneous learned procedures: navigation
(node->node) feeding aggregation (node->number) via value-level handoff,
with no domain-pair template.

## Honest boundaries
- Behavior induction (how X/Y got their behaviors) is assumed as prior
  learning, not demonstrated here. The tested claim is contracts +
  composition.
- Kinds are binary (NODE/NUM) from a syntactic probe; richer type
  lattices are future work (H2/H3 lanes).
- Distractor set is small (2); the pruning claim scales with MAP count
  but that scaling test is not run here.
- Composite contract derivation in(A)->out(B) is generic machinery,
  researcher-authored; the VALUES composed are learner-observed.

## Architecture accounting
+300 cognition lines (new standalone file; frozen TNN-2 untouched).
0 modes, 0 bridges, 0 handlers, 0 new semantic cases.

## Toolchain
Safebin PATH throughout; `which python3 python` empty (NAMECHECK Step 0).
Pinned znc; compile exit 0; only benign infra notice (zagd unavailable).
Zero em/en dashes byte-verified. Committed locally, nothing pushed.
