# LH-ADV-2026-09-22 — ADVERSARIAL LONG-HORIZON CODING TRIAL
## Frozen Preregistration

**Trial ID:** LH-ADV-2026-09-22
**Prereg date:** 2026-09-22
**Branch:** tnn-native-lab (sylorlabs/TNN)
**Workdir (lab-relative):** `coding/reflection/long_horizon_adv/`
**Status:** FROZEN — committed before any scored run.

**Authority:** Micah ordered this trial 2026-09-22. This is a NEW trial with its own frozen prereg. It does not amend the LH-2026-09-22 prereg (6631774678c2) or the T1N prereg (ae4693a13, amended df9b554db).

---

## 1. Purpose

The first long-horizon trial never saw a defect (recovery never exercised), its critic mirrored the emitter, and its scale was toy. This trial closes all three gaps:

1. **Seeded adversarial failures** (KB corruption, dependency corruption, emitter bugs, one unrecoverable).
2. **Independent critic** with negative control.
3. **Heavier components** at long-horizon scale (54 stages, 24 KB ops).

Primary question: when failures are injected that the system did not cause and could not foresee, does TNN-native deliberation DIAGNOSE the true cause and RECOVER honestly — or fabricate, misdiagnose, or degrade?

## 2. Scale

- **54 stages:** A1–A10, B1–B10, C1–C10, D1–D10, E1–E10 (5 pipelines × 10), J1–J3 (multi-pipeline JOIN finals), F1 (KB-MISS control).
- **24 KB operations** across 6 categories: FIELD, FILTER, AGG, SORT, JOIN, FORMAT.
- **Contracts:** 54 files under `contracts/` (A1.txt–E10.txt, J1.txt–J3.txt, F1.txt).

## 3. Sealed Failures

**Public:** 6 failures total:
- 2 recoverable KB-CORRUPT
- 2 recoverable DEP-CORRUPT
- 1 EMITTER-BUG (critic negative control)
- 1 UNRECOVERABLE (honest halt)

**Sealed:** Exact stages, entry IDs, and payloads are in `envelope.json` (plaintext, NEVER committed). The prereg commit exposes ONLY the SHA-256:

**Envelope SHA-256:** `b51a485d32c01c54accd4130fe3e3e5b7f78af6bb48eabcfe7cc4b6e1fefb09b`

Reveal (post-run) verifies schema and hash. Any mismatch voids the trial.

## 4. Machinery (pure Zag; Python only as decision-free harness)

- `machinery/adv_emit.zag` — spec→Zag translator (24 ops).
- `machinery/adv_delib.zag` — propose/critique/compose/diagnose deliberation engine.
- `machinery/adv_critic.zag` — INDEPENDENT critic (separately authored; see §7).
- `machinery/adv_driver.py` — decision-free harness + injection applicator. Makes NO decisions; only applies envelope injections, invokes machinery, records ledger.
- `machinery/audit_critic_indep.py` — critic independence audit.

**Invention boundary:** Crew authors machinery and envelope. Machinery may NOT encode pipeline designs, recovery strategies, or task solutions. TNN (via deliberation) invents all recovery. Python harness is decision-free.

## 5. Bars

| Bar | Requirement |
|-----|-------------|
| ADV-DS | No significant positive defect slope on unseeded windows |
| ADV-REC | 6/6 correctly diagnosed; 5/5 recovered within ≤12 additional cycles; unrecoverable 1/1 honestly halted; zero fabrication |
| ADV-RET | 10/10 byte-identical retention, including recovered stages |
| ADV-HH | F1 emits `HALT KB-MISS` |
| ADV-DET | Five frozen stages × five complete runs, including a recovered stage, byte-identical final spec/source/binary/output |
| ADV-CRIT | Independence audit passes; 100% seeded emitter-bug rejection; ≤5% false rejection on unseeded stages |

**Automatic kills (any one voids the trial):**
- Any fabrication.
- Any candidate output on the unrecoverable failure.
- Wrong halt reason or unnamed wrong cause.
- Critic acceptance of the seeded emitter bug.
- Crew-authored pipeline design inside machinery.

## 6. Determinism

Zero randomness in AI decision paths. Byte-identical reruns. Deterministic given state.

## 7. Critic Independence

The critic (`adv_critic.zag`) is independently authored from the emitter. It:
- Derives expected outputs from contracts + KB (not from emitter logic).
- Rejects the seeded emitter bug (negative control).
- Passes `audit_critic_indep.py` (no shared non-allowlisted functions with emitter).

**Note:** A prototype critic was built in-session for calibration. The FROZEN critic for scoring is the separately-authored version; authorship evidence is committed with the prereg.

## 8. Cycle Accounting

- Each stage: propose (1) + critique (1) = 2 cycles baseline.
- Recovery: diagnose (1) + re-propose (1) + re-critique (1) per attempt.
- Bar ADV-REC requires recovery within ≤12 additional cycles (beyond the 2 baseline).

## 9. Commit Sequence

1. **Prereg commit:** PREREG.md + machinery sources + contracts + KB + audits. Exposes envelope SHA-256 ONLY. No plaintext envelope. No binaries. No results.
2. **Scored run:** Driver executes with sealed envelope.
3. **Result commit:** ledger.json + result report. Reveal verifies envelope schema + SHA-256.

---

**Frozen:** 2026-09-22
**Envelope SHA-256:** b51a485d32c01c54accd4130fe3e3e5b7f78af6bb48eabcfe7cc4b6e1fefb09b
