# TNN Research Push Summary

**Date:** 2026-10-03
**Branch:** `tnn-native-lab` → `Sylorlabs/TNN`
**Status:** COMPLETE — remote fully in sync (0 commits behind)

## What was pushed

The entire TNN RSI research history on `tnn-native-lab`, including:

### Composition Frontier (L1 → L2 → L3)

**L1 Cross-Domain Composition (DEMONSTRATED):**
- H1 (learned typed contracts) and H2 (value-level functional composition) solved 4 structurally different pairs with unmodified logic:
  1. Navigation → Aggregation
  2. Arithmetic → Planning
  3. Causal Model → Intervention
  4. Grammar Constraint → Executable Construction
- H3 (2-mode structural dispatch) retired — fundamentally finite-menu, does not generalize

**L2 Adaptive Reuse (TOP PRIORITY, demonstrated):**
- Complete operation matrix: EXTEND, TRUNCATE, SPECIALIZE, SUBSTITUTE, INTERFACE-ADAPT
- All operations work within-domain AND cross-domain
- Learner-driven decisions (chooses k, nf, order itself)
- XP-SELECT series: learner selects operation across 5 cross-domain mismatches

**L3 Novel Intermediate (AGI target, in progress):**
- L3-NIV2: Wave 2 → Wave 3 → Wave 4 BUILD-PASS (2S-CALR, depth-4)
- L3-INR: designed, implemented, DEV-validated; sealed evaluation pending
- L3-RX: conditional pass 15/16 (representational expansion under proven insufficiency)

**Composition Generality:**
- COMPOSE-COLLAPSE: H1+H2 subsume into ONE behavior-contract operation (not three engines)
- CONTRACT-UNIFICATION (C424): One 5-op module subsumes GEN+LCONT+FC
- Diamond/fan-out: C433 demonstrated diamond composition via generic multi-source fan-in
- COMPOSE-PAIR6-ADV: diamond defeats unified operation U — defines generality boundary (informative fail)

### Scaling

**Operand-Encoding Fix (BUILD-PASS, canonical):**
- Root cause: `res_op` treated `op >= 10000` as frame-slot, colliding with node ids ≥ 10000
- Fix: sign-tagged invariant (`op ≥ 0` = NODE, `op < 0` = FRAME slot `-1-op`)
- K2 (100/500/1000 MAPs): PASS — 3/3 byte-identical, 39/39 correct
- K3a (5000 build-order): PASS — 24/24 queries, all 3 orders
- K3b (scan reduction): PASS — **7007x** at 5000 MAPs
- K3c (determinism): PASS
- K4 (boundaries): PASS (25/25)
- K5 (red team): PASS (zero panics)
- K6 (semantic regression): PASS (byte-identical vectors)
- **5000-MAP scaling now canonical** on revised build

**Other scaling:**
- 5000-MAP FACT index: 13,107x reduction (exploratory, old build)
- REBIND-SCALING (C354): 100x, 0 evictions, storm eliminated

### Continuing Learner / Lifetime

- H-CONTLIFE series: 5 episodes × 2 lifetimes, persistent learner, safe revise primitive
- Learner invents own victim selection and [loo3,med] unprompted (convergent invention)
- NT series closed: 10 experiments, D1+D2 (preserve-evidence + evict-youngest) final
- Integration stress survived K1-K10

### Internal Verification

- IVWC BUILD-PASS: learner calibration via world consequences (113 vs 116)
- DELAYED-CONSEQUENCE PASS: temporal credit assignment, no expected answers
- SELFJUDGE: 24/24 self-judgment agreement (control 14/24)

### Domain-Blindness (Architectural)

- OPACITY-SWEEP (C462): **zero domain-story tokens anywhere** in codebase
- Architecture behaves identically under domain renaming (per Micah's 2026-10-03 directive)

### Architecture Compression

- CONTRACT-UNIFICATION: 5-op module subsumes 3 mechanisms
- GEN-COGOPS-UNIFY: one GEN composer can subsume COGOPS composition (feasible)
- B1/B2 contracts replace BIND table and membership routers (substitution, not addition)

## Ledger

Canonical ledger: **C1 → C463** (with collision resolution pending for C455-C462 duplicates)

## Governance

- All results: pure Zag, safebin, preregistered frozen kill bars, 3/3 deterministic
- PROCESS-FAILs documented (e.g., L3-NIV2-W1 python3 self-disclosure)
- VOID verdicts terminal, no salvage
- Sealed worlds never inspected except via authorized evaluator
- Commits local-only until this push; nothing force-pushed

## Excluded

Per instruction: reproducible cache and build artifacts excluded from documentation scope (binaries, tmp files, worktree checkouts).

## Token

The GitHub PAT used for this push should be deleted by the user as planned.
