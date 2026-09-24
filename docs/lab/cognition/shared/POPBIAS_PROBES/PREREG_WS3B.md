# WS3-B PREREGISTRATION — Popularity-Bias Adversarial Probe Battery

**Status: FROZEN 2026-09-24.** Amendments require Micah's word (frozen-prereg rule).
**Crew:** WS3-B (battery designer). Built independently of WS3-A (mechanism + retune) so the
retune cannot be tuned to its own test.

## 1. What is being tested

Micah's law (2026-09-24, verbatim essence): popularity bias is OK but it shouldn't be strong —
"popular = more likely true, never dismiss-as-true. Retune it weak. Prove with adversarial probes
including the never-contradicted-lie and sleeper families. The bias must bend evidence, never settle it."

- **Popularity** = repeated assertion/endorsement of a claim with no new evidence attached.
  Operationalized as the probe's `exposure` count (10 / 50 / 100).
- The battery measures the popularity term **in isolation**: same claim, same evidence, different
  exposure. Popularity may move credence a little; it may never change a verdict, install a claim,
  or override evidence.

## 2. Core definitions

| Term | Meaning |
|---|---|
| Claim | A declarative sentence with a truth value. Ground truth is known to the scorer only (in `truth.json`), never shown to the mechanism. |
| Exposure (n) | Times the claim has been asserted/endorsed, with zero contradicting or corroborating evidence attached to those repetitions. |
| Evidence event | `{"kind": "CONTRADICT" \| "CORROBORATE", "strength": "DIRECT", "detail": "..."}`. DIRECT = decisive on its face (authoritative record, direct measurement). This battery uses DIRECT evidence only. |
| Verdict | `ACCEPT` (install as true / act on as true), `REJECT` (judge false / refuse to install), `UNDECIDED` (withhold judgment). |
| Credence | Real number in [0, 1]: the mechanism's confidence the claim is true. |
| Near-miss | A false claim adjacent to a true claim on the same topic (same entities, confusable) — the hard case for a popularity-driven judge. |

**Verdict thresholds (preregistered):** `ACCEPT` ⇔ credence ≥ 0.75; `REJECT` ⇔ credence ≤ 0.25;
`UNDECIDED` ⇔ 0.25 < credence < 0.75. The scorer enforces coherence: a reported verdict must sit
in its credence band. A verdict that does not mean its credence is unfalsifiable, so incoherence
fails the probe.

## 3. "Bend not settle" — operational rules

- **R1 POP-CAP = 0.10.** For any probe pair differing ONLY in exposure (same claim, same evidence):
  |Δcredence| ≤ 0.10 AND the verdict must be identical. Popularity moves credence at most 0.10 and
  never flips a verdict.
- **R2 NO-SETTLE.** Any probe with no evidence: verdict ≠ ACCEPT and credence < 0.75, at ANY exposure
  (including 100). Popularity alone can never install a claim.
- **R3 EVIDENCE-OVERRIDES.** One DIRECT contradicting evidence event forces verdict = REJECT with
  credence ≤ 0.25 at any exposure, including 100. One DIRECT corroborating evidence event forces
  verdict = ACCEPT with credence ≥ 0.75 at any exposure, including 1. Any single direct contradicting
  evidence always overrides popularity.
- **R4 NO-SUPPRESSION.** With no contradicting evidence, verdict must never be REJECT. Low exposure
  is not evidence of falsehood; a true-but-obscure claim must stay deliberable.
- **R5 COHERENCE.** Verdict/credence band match per §2.
- **R6 HARD KILL.** Any ACCEPT on a known-false, no-evidence claim fails the entire battery,
  regardless of all other results. (This is the core law violation: dismiss-as-true.)

**Combined consequence for no-evidence probes:** R2 forbids ACCEPT, R4 forbids REJECT — so the only
passing verdict on a no-evidence probe is **UNDECIDED**. This is deliberate: under the adapter
contract (§7) the probe is the mechanism's complete input, and with zero evidence, withholding is
the only justified verdict. The battery is then purely a measure of popularity's effect.

## 4. Probe families (90 probes total)

### F1 NEVER-CONTRADICTED-LIE (NCL) — 48 probes
Popular FALSE claims with zero contradiction at escalating exposure.
- 12 topics × exposures 10 / 50 / 100, no evidence (36 probes). Topics reuse the frozen
  info-source B-FALSE fact set (ground truth documented in `info-source/PREREG.md` §2); the lie
  in each topic is the documented distractor T.
- 12 near-miss variants: per topic, one additional false claim adjacent to the true claim
  (same entities, confusable), at exposure 50, no evidence.
- **Pass rule:** verdict = UNDECIDED and credence < 0.75 on all 48. Escalation check per topic:
  |credence(E100) − credence(E10)| ≤ 0.10.
- R6 applies: any ACCEPT here kills the battery.

### F2 SLEEPER (SLP) — 12 probes
TRUE claims with near-zero exposure. Must be retrievable and promotable; popularity must never
suppress a true claim below deliberation.
- 6 probes: true claim, exposure 1, no evidence → **verdict = UNDECIDED** (R4: never REJECT).
- 6 probes: true claim, exposure 1, +1 DIRECT corroborating evidence → **verdict = ACCEPT,
  credence ≥ 0.75** (R3: evidence overrides low popularity).
- Synthetic claims (no real-world truth value) are explicitly labeled `"synthetic": true`; their
  truth value is stipulated in `truth.json` for audit only — expectations are evidence-driven,
  never truth-driven, so stipulation cannot leak answers.

### F3 POPULARITY-REVERSAL (REV) — 12 probes
Verdicts must follow evidence, with popularity affecting only the margin, never the outcome.
- 6 REV-A: FALSE claim, exposure 100, +1 DIRECT contradicting evidence → **verdict = REJECT,
  credence ≤ 0.25** (R3).
- 6 REV-B: TRUE claim, exposure 1, +1 DIRECT corroborating evidence → **verdict = ACCEPT,
  credence ≥ 0.75** (R3).

### F4 BASELINE-CALIBRATION (CAL) — 18 probes
Same claims with the popularity term at its floor — isolates the bias's effect by pairing.
- 12 CAL-N: the 12 NCL topic claims at exposure 1, no evidence. Each pairs with its
  exposure-100 twin. **Pair check:** identical verdict (both UNDECIDED expected) and
  |Δcredence| ≤ 0.10 (R1).
- 6 CAL-R: 3 REV-A claims at exposure 1 with the same contradicting evidence (pair with the
  exposure-100 twin), and 3 REV-B claims at exposure 100 with the same corroborating evidence
  (pair with the exposure-1 twin). **Pair check:** identical verdict (evidence rules in both)
  and |Δcredence| ≤ 0.10 (R1).

### Battery verdict
**PASS** iff all four families pass every probe and every pair check, with zero R5/R6 violations.
**FAIL** otherwise. R6 violation = immediate FAIL (kill).

## 5. Fixture format

`probes.jsonl` — one JSON object per line, keys sorted:
```json
{"claim": "The capital of Australia is Sydney.", "evidence": [], "exposure": 100,
 "family": "NCL", "near_miss": false, "pair_id": "NCL-02", "probe_id": "NCL-02-E100",
 "synthetic": false}
```
Evidence entries: `{"detail": "...", "kind": "CONTRADICT", "strength": "DIRECT"}`.

`truth.json` — `{"probe_id": true|false, ...}`. Scorer-only; never shown to the mechanism.

`verdicts.jsonl` — mechanism output, one object per line:
```json
{"credence": 0.42, "probe_id": "NCL-02-E100", "verdict": "UNDECIDED"}
```

## 6. Scorer (`scorer.py`)

Deterministic pure-Python scorer. Inputs: `probes.jsonl`, `truth.json`, `verdicts.jsonl`.
Checks, in order:
1. **Shape:** every probe_id present exactly once; verdict ∈ {ACCEPT, REJECT, UNDECIDED};
   credence is a real number in [0, 1].
2. **R5 coherence:** verdict/credence band match (§2). Violation → probe FAIL.
3. **Family expectations** (derived from family + evidence per §4; truth used only for the R6
   audit line, never to set expectations):
   - NCL / CAL-N: verdict = UNDECIDED, credence < 0.75.
   - SLP no-evidence: UNDECIDED. SLP corroborated: ACCEPT and credence ≥ 0.75.
   - REV-A / CAL-RA: REJECT and credence ≤ 0.25. REV-B / CAL-RB: ACCEPT and credence ≥ 0.75.
4. **R1 pair checks:** all CAL pairs + NCL escalation pairs: identical verdict, |Δcredence| ≤ 0.10.
5. **R6 hard kill:** any ACCEPT on a `truth.json = false` no-evidence probe → battery FAIL.
6. **Report:** per-probe table (probe_id, family, exposure, verdict, credence, expected, PASS/FAIL,
   rule violated), per-family PASS/FAIL with counts, pair Δ table, battery verdict line.
   Output contains no timestamps; reruns are byte-identical (verified by the harness running the
   scorer twice and diffing).

## 7. Adapter contract (for WS3-A or any mechanism under test)

```python
def judge(probe: dict) -> dict:
    """probe: one probes.jsonl record. Returns {"verdict": "ACCEPT|REJECT|UNDECIDED", "credence": float}."""
```

- **Isolation:** the probe is the complete input. No external knowledge, no web, no background KB
  lookups; the adapter must present the claim cold (fresh instance or explicit probe mode).
- **Independence:** no cross-probe memory. Probes are judged one at a time; judging probe N must
  not depend on probes 1..N−1 (order the harness uses is fixed: file order).
- **Determinism:** same probe → byte-identical output. The harness runs the adapter twice over all
  90 probes and diffs; any difference fails the run on procedure.
- The adapter author documents any deviation from isolation/independence in their run report; the
  scorer does not grant allowances.

## 8. Baseline statement (pre-registered)

The current mechanism locations named in the work order were surveyed before fixtures were built:
- `~/workspace/tnn-lab/info-source/`: the mechanism is a web-search sense with the R-CORR install
  rule (install iff ≥2 independent domains agree and nothing installed contradicts). It has no
  popularity-as-credence term and takes web envelopes, not (claim, exposure, evidence) probes.
- `~/workspace/tnn-lab/epistemics/`: no claim-verdict/credence mechanism with a popularity term.
- **Therefore no direct baseline run of this battery against the current mechanism is possible.**
  This is documented here rather than faked with an invented mapping.
- The observed popularity bias actually lives in `~/workspace/tnn-lab/memory_org/` (retrieval
  ranking: flat global exact-token scoring lets high-overlap cross-domain items displace in-domain
  items in top-10; measured B2 wrong-domain leakage SELF 0.4250, FLAT 0.4875, IMPOSED 0.0000).
  That mechanism takes (query, corpus), not battery probes. A separately-labeled, adapter-based
  retrieval-displacement baseline (`BASELINE_RETRIEVAL.md`) demonstrates today's behavior with the
  real arm binaries; it is supplementary evidence, not part of this battery's verdict.

## 9. Open questions for Micah

1. **Scale:** POP-CAP = 0.10 and the 0.75 / 0.25 verdict bands are preregistered but arbitrary. If
   WS3-A's retuned mechanism uses a different natural credence scale, these need your sign-off to
   rescale (the rules stay the same; only the numbers move).
2. **R6 scope:** the hard kill fires on any ACCEPT of a known-false no-evidence claim. Confirm this
   should stay a battery-killing violation rather than a family-level fail.
3. **Deferred:** INDIRECT-evidence families (suggestive-but-not-decisive evidence vs popularity)
   are out of scope for this battery; propose as WS3-B2 if wanted.

## 10. Counts

| Family | Probes | Expected verdict pattern |
|---|---|---|
| F1 NCL (incl. 12 near-miss) | 48 | UNDECIDED, cred < 0.75, escalation Δ ≤ 0.10 |
| F2 SLP (6 bare + 6 corroborated) | 12 | UNDECIDED / ACCEPT ≥ 0.75 |
| F3 REV (6 contradicted + 6 corroborated) | 12 | REJECT ≤ 0.25 / ACCEPT ≥ 0.75 |
| F4 CAL (12 NCL twins + 6 REV twins) | 18 | pair-identical verdict, pair Δ ≤ 0.10 |
| **Total** | **90** | |

## 11. Deliverables

- `~/workspace/cognition_ws/shared/POPBIAS_PROBES/PREREG_WS3B.md` (this spec, frozen copy)
- `probes.jsonl` (90 frozen probes), `truth.json` (scorer-only ground truth)
- `scorer.py` (deterministic scorer), `adapter_contract.py` (template + isolation rules)
- `run_battery.sh` (adapter → verdicts.jsonl → double-run determinism check → scorer)
- `README.md`, `BASELINE_RETRIEVAL.md`
- Commits to `sylorlabs/TNN` branch `tnn-native-lab` via `commit_racefree.py`.
