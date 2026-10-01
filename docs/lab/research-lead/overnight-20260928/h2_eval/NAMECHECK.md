# NAMECHECK.md - H2 Evaluator

## Step 0: Toolchain Guard

- Safebin activated: `export PATH="$HOME/safebin"`
- `which python3 python` returns nothing (verified)
- Zero forbidden executables invoked
- All computation in pure Zag via pinned `znc_linux_x86_64_abed8aa1`
- Shell used only for: invoking znc, running binaries, git ops, file moves

## Authorization Chain

1. **Micah's H2 ruling** (2026-10-01 07:10 PDT): "APPROVE H2 immediately. Freeze K-H2-1 through K-H2-4 using the reviewed recommendations. Authorize the evaluator to open the already-sealed H2A/H2B/H2C worlds."

2. **Freeze commit**: `c15a47d63` (H2-PREREG-FROZEN). Strictly precedes this evaluation.

3. **Sealed worlds**: commit `86389b108` (H2-TRAPWORLDS-COMPLETE).

4. **This evaluator**: Authorized by freeze commit section 10 to open H2A/H2B/H2C.

## Hash Verifications (BEFORE opening)

### Seal hashes (from SEAL_H2.md at 86389b108)
- h2a_world.txt: `be358e7ae423d55d99018288f9a6e14c72b2e86d649637652e1eb22a0ddf7499`
- h2b_world.txt: `6cac9f6b22c8e303e75bfadac0cd13459ce1e0c64a999c25c8a0b0e2ca31ca6c`
- h2c_world.txt: `2b721d49e0f04e9aef915eaec69fa9d5ec3db71c5c8d0293eafa75418eb846ba`

### Measured (before opening)
- h2a_world.txt: `be358e7ae423d55d99018288f9a6e14c72b2e86d649637652e1eb22a0ddf7499` MATCH
- h2b_world.txt: `6cac9f6b22c8e303e75bfadac0cd13459ce1e0c64a999c25c8a0b0e2ca31ca6c` MATCH
- h2c_world.txt: `2b721d49e0f04e9aef915eaec69fa9d5ec3db71c5c8d0293eafa75418eb846ba` MATCH

**Seal: VERIFIED. No compromise.**

### Frozen TNN-2 binary
- Build commit: `f4de7ff46`
- Recorded hash: `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`
- Measured: `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b` MATCH

**Frozen binary: VERIFIED.**

### Frozen source (for driver harness)
- Source hash: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
- Driver uses byte-identical copy. Learner logic UNMODIFIED.

## Scope

- Open ONLY: h2a_world.txt, h2b_world.txt, h2c_world.txt
- Do NOT open any other sealed worlds (FW, GW, other H2)
- Do NOT modify TNN-2 source, binary, or learner logic
- Driver harnesses in pure Zag only
- 3 byte-identical runs per probe

## Micah's Architecture Clarification (2026-10-01)

"Freeze means freeze researcher-authored architecture/source for controlled
scientific evaluation. It does NOT mean freeze the learner."

During H2 evaluation:
- Learner state REMAINS FREE to change (memories, revisions, policies)
- Do NOT reset learner state between probes within a world unless prereg specifies isolation
- Report per-probe results AND learner-state changes across probes

## Constraints

- No em dashes in documentation
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`)
- Nothing pushed (local commits only)
- If any hash fails: STOP and report SEAL-COMPROMISED
