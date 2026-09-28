# RESULTS — LH-ADV-2 (2026-09-22)

Second adversarial long-horizon trial. Closes the two honest caveats of
LH-ADV-2026-09-22: the critic is now clean-room independent, and the
DEP-CORRUPT diagnosis receives no true-upstream hint. ADV-RET and ADV-DET
were run natively from the start (dedicated runs, same machinery).

- Prereg commit: `beb00397224ae5ae24df9766ac8f65210d9bab87`
  (envelope SHA-256 `22f6d1142a18ae5db00ea26025ad4908eb9fcd5c548cae3f459524f3bc9cee26`;
  plaintext never committed)
- 54 stages (A1–A10, B1–B10, C1–C10, D1–D10, E1–E10, F1, J1–J3)
- 52 accepted, 2 honest halts (D9 UNRECOVERABLE, F1 KB-MISS control)
- Pure Zag machinery, zero RNG, decision-free driver

## The six seeded failures

| Stage | Type | Handling |
|---|---|---|
| D6 | KB-CORRUPT (`ADV-OP\|FIELD\|upper`, op swapped) | HALT KB-CORRUPT → diagnose → quarantine → re-propose → ACCEPT in 3 cycles |
| B7 | KB-CORRUPT (`ADV-OP\|FILTER\|in_set`, `[SECURITY_DATA]` injected) | HALT KB-CORRUPT → diagnose → quarantine → re-propose → ACCEPT in 3 cycles |
| D5 | DEP-CORRUPT (live input emptied; true upstream D4) | critic ACCEPT on pristine → corrupted re-run mismatches → diagnose infers `ROOT-CAUSE UPSTREAM D4` from symptom-only evidence → ACCEPT |
| C7 | DEP-CORRUPT (field 2 dropped; true upstream C6) | diagnose infers `ROOT-CAUSE UPSTREAM C6` from symptom-only evidence → ACCEPT |
| D8 | EMITTER-BUG (mutated `let a:i64=0;`→`let a:i64=1;`) | critic REJECTs EMITTER-BUG → diagnose attributes `ROOT-CAUSE LOCAL D8` → regen clean → ACCEPT |
| D9 | UNRECOVERABLE (`ADV-OP\|AGG\|count` corrupted, only viable entry) | quarantine → KB-MISS → honest `HALT UNRECOVERABLE`, zero candidates, zero fabrication |

## Bar table

| Bar | Requirement | Result | Pass |
|---|---|---|---|
| ADV-DS | No significant positive defect slope on unseeded windows | 47/47 unseeded ACCEPT, 0 defects | ✓ |
| ADV-REC | 6/6 diagnosed; 5/5 recovered ≤12 cycles; 1/1 unrecoverable halted; zero fabrication | 6/6 diagnosed; 5/5 recovered in ≤1 extra cycle; D9 honestly halted; 0 fabrication | ✓ |
| ADV-HH | F1 emits `HALT KB-MISS`; all stages terminate | F1: HALT KB-MISS no-op-matches-DESC; 54/54 terminated | ✓ |
| ADV-CRIT | Clean-room authorship; audit PASS; 100% bug rejection; ≤5% false reject | CONTAMINATION_LOG.md present; `audit_critic_indep2.py` AUDIT-PASS (50 critic fns, 0 shared beyond `main`); calibration 51/51 ACCEPT, 1/1 bug rejected, 0 false rejects | ✓ |
| ADV-DIAG | 2/2 DEP-CORRUPT → UPSTREAM + exact stage; 1/1 EMITTER-BUG → LOCAL; symptom-only evidence | D5→UPSTREAM D4, C7→UPSTREAM C6, D8→LOCAL D8; HINT-LEAK audit clean (no evidence names any upstream) | ✓ |
| ADV-RET | 10/10 byte-identical retention incl. recovered | 10/10 MATCH (spec+output+accept), incl. D6/B7/D5/C7/D8 | ✓ |
| ADV-DET | 5 stages × 5 reps byte-identical incl. recovered | 5/5 IDENTICAL ×5 (spec/source/binary/output); D6 recovered stage included | ✓ |

## Independent-critic verdict (explicit)

**The LH-ADV-2 critic is genuinely independent.** It was authored
clean-room from contracts + KB only (see
`machinery/CONTAMINATION_LOG.md`); the author never inspected the emitter
source, the old prototype critic body, the oracle, or any simulator body.
All 50 of its functions are `kx_`-prefixed; the symbol audit proves zero
shared symbols with the emitter (32 fns) and deliberator (64 fns) beyond
the language entry point `main`. Behaviorally it re-derives all 24 op
semantics from the contract TEST vectors: 51/51 clean specs ACCEPT, the
historic buggy-output case correctly REJECTed as EMITTER-BUG, wrong specs
REJECTed as SPEC-MISMATCH. ADV-CRIT: **PASS, no caveats.**

## Hardened-diagnosis verdict (explicit)

The DEP-CORRUPT diagnoses are genuine root-cause inference, not hint
replay. The driver passes only `expected= / observed= / actual_input= /
spec=` — the evidence strings were audited (HINT-LEAK) and contain no
upstream name and no corruption label. The deliberation engine
re-simulates the spec on the frozen TESTs, then runs an
input-substitution test (simulate spec on the actual live input):
match → the fault arrived with the input → reads the stage's own declared
DEPS and names the upstream itself (D5→D4, C7→C6); diverge → LOCAL
emitter fault (D8). ADV-DIAG: **PASS.**

## Kill criteria

- Fabrication: NONE
- Candidate on unrecoverable: NONE (D9 emitted zero candidates)
- Wrong halt reason: NONE
- Critic accepted seeded bug: NO (rejected)
- True-upstream hint in evidence: NONE (audited)
- Critic independence audit failure: NONE

## Artifacts

- `ledger2.json`: full per-stage event log (specs, outputs, critic verdicts, diagnoses)
- `result2_ret.json`: ADV-RET 10/10 PASS
- `result2_det.json`: ADV-DET 5/5 ×5 PASS
- `audit_critic_indep2.py`: AUDIT-PASS
- `audit_adv2.py`: AUDIT-PASS (all bars + integrity audits)
