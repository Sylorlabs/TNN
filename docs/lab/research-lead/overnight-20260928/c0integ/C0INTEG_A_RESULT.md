# C0INTEG Phase A: Result

## Verdict

**PHASEA-PASS**

## Preregistration

- Prereg file: `docs/lab/research-lead/overnight-20260928/c0integ/PREREG_C0INTEG_A.md`
- Prereg commit: `c4a7e325fc2022654869edf00c082f79555bdafc`
- Prereg message: "Prereg: C0INTEG Phase A implementation (frozen before any implementation)."
- The prereg commit strictly precedes all implementation commits. K1 satisfied.

## Implementation

- Source: `docs/lab/research-lead/overnight-20260928/c0integ/c0integ_a.zag` (pure Zag, no Python/C/other)
- Compiler: `znc 2026.07.0-dev (edition 2026)` via `znc build` only
- Build: clean, warnings only (no errors)

## Test results

All five preregistered tests pass:

| Test | Result | Detail |
|------|--------|--------|
| T-RV1 | PASS | Recruited op=32, arity=3, len=7, gain=5, freq=4; 1 recruit event; 4 rec refs in kept trees; no F-BREAK |
| T-MENU | PASS | rexp=512, reccnt=512, verified=512 (all recruited expansions match body semantics) |
| T-RETIRE | PASS | 1 retirement, nrec=0 after idle, no new recruitment |
| T-NOFIRE | PASS | 0 recruitments on distinct trees |
| T-Q4REG | PASS | F-CONJ 64/64, F-XOR 64/64, trace counts match q4_impl exactly (4012/4020, 4091/4099) |

## Determinism

- 3 runs, all exit 0, empty stderr.
- stdout byte-identical across all 3 runs (verified with `cmp`).
- SHA256 of run1.txt: `ec5d7c2312e7171ab768b06783611c91b5dc331ebf667c5554f7d37edaf91737`
- Zero em dash (U+2014) and zero en dash (U+2013) bytes in source and all run outputs (verified with shell `grep`).

## Audits

### A1: One generic recruited-op dispatch

- Exactly one function constructs recruited-op nodes: `node_new_rec` (line ~293).
- Opcode computed as `32+ri` (line 327). No other opcode construction.
- Range checks are generic: `op>=32` (lines 800, 1043).
- Recruited-op indexing is generic: `32+r`, `32+k` (lines 1149, 1168, 1175).
- **No numeric literals 33 through 63 appear as values anywhere in the source.** The only occurrences of "33..63" are in comments describing the design. Verified with shell grep.
- No branch names a recruited meaning. The dispatch interprets opcodes solely via `bodies[]` (learner-owned persistent state).

### A2: Tree-based recruited bodies with placeholders

- Bodies are 16-byte tree nodes in `bodies[]`, not instruction sequences.
- Placeholders (P0..P3) bind to terminals via first-appearance preorder canonicalization.
- T-RV1 recruited `OR(AND(P0,P1),AND(P0,P2))`: 7 body nodes, 3 operator nodes, arity 3.

### A3: Information barrier (observed samples only)

- VALIDATE compares INLINE vs WRAPPED on 16 observed x values only.
- Never touches sealed-world answers. The sealed families (F-CONJ, F-XOR, nested pair) are used only for Q4 discovery and final scoring, not for recruitment decisions.

### A4: Deterministic candidate ranking

- Frequency counted once per kept variable (deduplicated by canonical shape).
- Winner selection is deterministic: highest gain, tie-broken by lowest shape index.
- 3-run byte-identical output confirms determinism.

## Disclosed researcher-authored residue

1. **Base operators**: AND, OR, NOT, XOR are researcher-supplied primitives with hand-written truth tables.
2. **Recruitment thresholds**: freq>=3, 2-6 operator nodes, arity 1-4, gain>0 are researcher-chosen constants.
3. **Canonicalization scheme**: first-appearance preorder placeholder naming is researcher-designed.
4. **Q4 beam/discovery**: the beam search, scoring, and intervention selection are researcher-authored infrastructure.
5. **The fragment shape**: the specific `OR(AND(P0,P1),AND(P0,P2))` fragment was anticipated in the prereg as the T-RV1 worked example. The learner discovered it via the frozen mechanism, but the test was designed around it.
6. **Rewrite bypass**: `node_new_op_fresh` (non-deduplicating node creation) was added during implementation to prevent signature dedup from collapsing rewritten trees. This is researcher-authored machinery, not learner-discovered.

## Honest ceiling

**Bounded L2 infrastructure, not L3 and not yet a C0 strengthening.**

Phase A integrates OP-RECRUIT v2 and Q4 discovery into one continuing learner with a working recruit/retire loop. The learner does recruit a useful fragment (op 32) and reuses it in the beam menu (T-MENU: 512/512 verified expansions). However:

- The recruited "abstraction" is a fixed tree fragment, not an open-ended representation the learner designed.
- The recruitment criteria, canonicalization, and validation are all researcher-specified.
- Phase A does not demonstrate the learner inventing a representation with semantics it defined (C0-A), nor open structural growth beyond the fixed fragment form (C0-B).
- Grown-menu reuse benefit (sample efficiency, transfer) is explicitly Phase B, not claimed here.

Phase A is integration substrate. The L3 question remains open for Phase B.

## Kill bars

- K1 (prereg frozen before implementation): SATISFIED. Commit c4a7e325f precedes all implementation.
- K2 (implementation complete): SATISFIED. All preregistered components implemented and tested.
- K3 (pure Zag and deterministic): SATISFIED. Pure Zag, 3-run byte-identical, no Python/C.

## Final

**PHASEA-PASS**
