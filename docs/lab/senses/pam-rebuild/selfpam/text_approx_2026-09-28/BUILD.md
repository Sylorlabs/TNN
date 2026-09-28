# BUILD.md — Self-PAM text-approximate builder package

**Date:** 2026-09-28. **Branch:** `tnn-native-lab`. **Corpus seal:** `879bbb4cf89a41b8723b69a478c0319e1a4af9db`.

## What was built

### 1. Prereg (committed BEFORE corpus seal)
- `PREREG_TA.md` — committed `b92e3937e4c21a8a1168c931a9ed737a4b143f58`.
- Ratified kill bars KB-TA-1..6 (shared) and mechanism bars H-TA1-K1..K3, H-TA3-K1..K3.

### 2. TA-CORPUS v1 (sealed, read-only)
- **Commit:** `879bbb4cf89a41b8723b69a478c0319e1a4af9db`
- **Path:** `docs/lab/senses/pam-rebuild/selfpam/corpora/cell-ta/`
- **Seal SHA-256:** `c36108728ebce982bc0255cd835f05a65c25952722c3af45a2c6032c0283ce03`
- 950 main items + 450 stress + 200 evidence + 64 episodes + 64 edges.
- Dual-label audit: 1454/1454 pre-selection, 1400/1400 on sealed set.
- Deterministic regeneration verified: fresh rebuild byte-identical (11/11 files).

### 3. H-TA1 equivalence answer
**The learner does NOT already derive provenanced P⇔Q beliefs.**
No equivalence-derivation log, edge store, or warrant-edge machinery exists in
the Self-PAM codebase. `ta1_derive` (below) is the first such instrumentation.
The gate (`ta1_gate`) only reads edges; it never creates them.

### 4. Zag sources (pure Zag, zero RNG)
| File | Status | Description |
|---|---|---|
| `src/text.zag` | ✅ Complete | Byte-level string utilities (R33-compact style) |
| `src/lists.zag` | ✅ Complete | Frozen closed-class (191) + negation (11) lists, byte-identical to Python |
| `src/io.zag` | ✅ Complete | Minimal file I/O via Linux syscalls |
| `src/ta1_derive.zag` | ✅ Working | Edge derivation logger; 3 edges from dev episodes, 0 refused |
| `src/ta1_gate.zag` | ⚠️ Stub | Read-only gate; verdict logic incomplete |
| `src/ta3_gate.zag` | ❌ Not built | H-TA3 detector gate not implemented |

### 5. OPEN dev set (38 items, ≤50)
- `dev/dev_evidence.jsonl` (12 claims), `dev/dev_items.jsonl` (38),
  `dev/dev_episodes.jsonl` (3), plus TSV views.
- Disjoint from sealed corpus (verified, zero collisions).
- Covers: identity, subset, paraphrase, polarity flip, quantity mismatch,
  entity substitution, zero overlap, chained equivalence, episode ablation,
  adversarial paraphrase.

## Determinism (KB-TA-5, dev set only)
`ta1_derive` on dev episodes: 3/3 byte-identical runs including
`MALLOC_PERTURB_=1` (stdout, stderr, edges.tsv). See RUNLOG.md.
Full-corpus determinism is the tester's responsibility.

## Honest weak cells
- **H-TA1:** `ta1_gate` verdict logic incomplete; chained-equivalence and
  ablation probes untested. Edge derivation works but the gate cannot yet
  consume edges.
- **H-TA3:** Not built. Detector-blind confabulations, modality/temporal/scope
  changes, and ADV-PARA handling are untested.
- **znc hazards hit:** `usize` unsupported (use `i32`); `if`/`while` conditions
  cannot have spaces around operators; `fn` return type uses `name()type`
  syntax (not `->`); top-level mutable globals forbidden; `@import` resolves
  from CWD.

## Reproduction
```bash
cd src && znc ta1_derive.zag -o /tmp/ta1_derive
/tmp/ta1_derive ../dev/dev_episodes.tsv /tmp/edges.tsv
```
