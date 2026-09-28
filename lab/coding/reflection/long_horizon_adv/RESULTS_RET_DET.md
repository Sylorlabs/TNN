# LH-ADV-2026-09-22 — Dedicated ADV-RET and ADV-DET Runs

**Trial ID:** LH-ADV-2026-09-22
**Prereg SHA (frozen, untouched):** 91afb024786fb2e208c787df0885c6addf172fbf
**Result commit:** 9e6a926b5e13
**Run date:** 2026-09-22
**Tooling:** `adv_ret_det.py` (result-side, decision-free; committed alongside)

This document completes the two bars the scored-run report left pending:
ADV-RET (retention) and ADV-DET (determinism). Both were executed against the
FROZEN committed artifacts: contracts + `adv_kb.txt` + ledger.json from
9e6a926b5e13, machinery rebuilt from the frozen .zag sources with the pinned
toolchain (`znc_linux_x86_64_abed8aa1`; fresh builds byte-identical to the
scored-run builds — the toolchain itself is deterministic), and the sealed
envelope (SHA-256 `b51a485d32c01c54accd4130fe3e3e5b7f78af6bb48eabcfe7cc4b6e1fefb09b`,
verified exact match before running; never committed).

The per-stage pipeline in `adv_ret_det.py` is the driver's pipeline copied
verbatim (propose→critique→diagnose→emit→compile→run→critic, same envelope
application, same DEP-CORRUPT upstream lookup). The only structural change is
returning the record instead of appending to a ledger. No decisions, no RNG.

## ADV-RET — retention (10/10 required)

10 stages re-run under the identical conditions of the scored run (same
envelope injections), including all 5 injected/recovered cases. Requirement:
final spec and binary output byte-identical to the frozen committed ledger.

| Stage | Injection | Cycles | Spec | Output | Accept | Verdict |
|-------|-----------|--------|------|--------|--------|---------|
| B2 | KB-CORRUPT (recovered, 3 cycles) | 3 | ✓ | ✓ | ✓ | MATCH |
| D3 | KB-CORRUPT (recovered, 3 cycles) | 3 | ✓ | ✓ | ✓ | MATCH |
| C5 | DEP-CORRUPT (recovered, 2 cycles) | 2 | ✓ | ✓ | ✓ | MATCH |
| E8 | DEP-CORRUPT (recovered, 2 cycles) | 2 | ✓ | ✓ | ✓ | MATCH |
| A7 | EMITTER-BUG (rejected→regenerated) | 2 | ✓ | ✓ | ✓ | MATCH |
| A1 | — | 2 | ✓ | ✓ | ✓ | MATCH |
| A5 | — | 2 | ✓ | ✓ | ✓ | MATCH |
| C1 | — | 2 | ✓ | ✓ | ✓ | MATCH |
| J1 | — | 2 | ✓ | ✓ | ✓ | MATCH |
| E9 | — | 2 | ✓ | ✓ | ✓ | MATCH |

**ADV-RET: 10/10 byte-identical → PASS.**

Notes:
- For the DEP-CORRUPT stages (C5 upstream C4, E8 upstream E2), the upstream
  stage was first re-run cleanly; both reproduced their frozen outputs
  byte-identically, and the live outputs fed the downstream injection path.
- A7's recovery trajectory (critic REJECT of the mutated binary, clean
  regeneration, CRITIC-ACCEPT) reproduced exactly, including its 2-cycle count.
- Source/binary have no reference hashes in the frozen ledger, so retention is
  checked on final spec + binary output; source/binary byte-identity is
  covered by ADV-DET's cross-rep comparison.

## ADV-DET — determinism (5 stages × 5 reps)

5 stages, each run 5 complete times under identical conditions (D3 with its
KB-CORRUPT injection each rep — a recovered stage is included, per the bar).
Requirement: final spec, emitted source, compiled binary, and binary output
byte-identical across all 5 reps of each stage.

| Stage | Injection | 5-rep agreement | Artifacts compared |
|-------|-----------|-----------------|--------------------|
| D3 | KB-CORRUPT (recovered) | IDENTICAL ×5 | spec, source, binary, output |
| A1 | — | IDENTICAL ×5 | spec, source, binary, output |
| A5 | — | IDENTICAL ×5 | spec, source, binary, output |
| J2 | — | IDENTICAL ×5 | spec, source, binary, output |
| E9 | — | IDENTICAL ×5 | spec, source, binary, output |

**ADV-DET: 5/5 stages byte-identical ×5 → PASS.**

Compiled-binary SHAs (first 16 hex of full SHA-256, identical across reps):
D3 `45e6689e76d6f12f`, A1 `4bce61d3e3537bf7`, A5 `572d4d27fae794ac`,
J2 `af54f37262263f8d`, E9 `16f2dc8148f70647`.

## Completed bar table

| Bar | Requirement | Result | Pass |
|-----|-------------|--------|------|
| ADV-DS | No significant positive defect slope on unseeded windows | 48/48 unseeded ACCEPT, 0 defects | ✓ |
| ADV-REC | 6/6 diagnosed; 5/5 recovered ≤12 cycles; 1/1 unrecoverable halted; zero fabrication | 6/6 diagnosed; 5/5 recovered in ≤1 extra cycle; E4 honestly halted; 0 fabrication | ✓ |
| ADV-RET | 10/10 byte-identical retention incl. recovered | 10/10 (spec + output byte-identical vs frozen ledger; all 5 injected cases reproduced incl. recovery trajectories) | ✓ |
| ADV-HH | F1 emits HALT KB-MISS | F1: HALT KB-MISS no-op-matches-DESC | ✓ |
| ADV-DET | 5 stages × 5 runs byte-identical incl. recovered | 5/5 stages identical ×5 (spec, emitted source, compiled binary, binary output); D3 recovered case included | ✓ |
| ADV-CRIT | Audit passes; 100% bug rejection; ≤5% false reject | Audit PASS; 1/1 bug rejected; 0/53 false reject | ✓ (partial: prototype critic — see caveat) |

## Standing caveats (unchanged)

- ADV-CRIT remains PARTIAL: the critic was a prototype built in-session after
  inspecting the emitter, not genuinely independently authored. LH-ADV-2
  (separate trial) closes this with a truly independent critic.
- DEP-CORRUPT diagnosis in this trial received the upstream identity in
  evidence from the driver; genuine evidence-based root-cause inference is
  LH-ADV-2's hardened variant.
