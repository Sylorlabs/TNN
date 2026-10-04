# BASELINE — today's popularity behavior vs the WS3-B battery

**Date:** 2026-09-24. **Mechanism under test:** the current info-source deliberate-install
machinery (`tnn-lab/info-source/src/ws2_sense.zag`, R-CORR rule) — the only claim-install
mechanism in the program with a repetition-sensitive gate. Built and run from the real
source; nothing simulated.

## 1. Survey of the named locations

- `info-source/`: the sense has a repetition-sensitive install gate (see §2). The word
  "popular" in its sources is content text only. **This is the baseline target.**
- `epistemics/`: no claim-verdict/credence mechanism with a popularity term. Not a target.
- `memory_org/` (outside the named dirs, surveyed for completeness): the observed popularity
  bias there is retrieval ranking — flat global exact-token scoring lets high-overlap
  cross-domain items displace in-domain items in top-10 (measured B2 wrong-domain leakage:
  SELF 0.4250, FLAT 0.4875, IMPOSED 0.0000). Its scorer (`topk` in `arms/lib.zag`) sums
  per-item token-occurrence counts with an ID tie-break; **it has no exposure/popularity
  term at all**, so the battery's (claim, exposure, evidence) probes cannot be applied to it
  without inventing the mapping. Not faked; documented here instead.

## 2. Code-level finding: the gate counts repetitions, not independent domains

`ws_install` (rule=1, R-CORR) gates on `ws_corr_ok()`, which counts **agreeing answers across
stored results** (`topc >= 2`) — not distinct domains, despite the header comment and the
frozen prereg saying "≥2 independent domains agree". `ws_domains2()` (distinct domains) is
used only for the ledger record, never for the gate. Consequences measured below:

- The gate is a **binary step function**: 1 agreeing result → withhold; ≥2 → install.
- The sense stores at most **6 results** (`WsV` has 6 slots; `ws_add_result` drops beyond 6
  and dedups identical (domain, answer) pairs). Exposures 10/50/100 are indistinguishable
  to it — the mechanism cannot even represent the escalation curve.
- **Contradicting *results* do not block installation** — only contradicting *installed
  beliefs* (conf ≥ 50) do (`ws_contra_installed`). A direct contradicting source is just a
  dissenting vote; the repetition majority wins.

## 3. Adapter mapping (documented; limits stated)

The battery's abstract probe → this mechanism's install path:

| Battery concept | Mapping |
|---|---|
| exposure n | min(n, 6) added results, distinct domains, same answer (the claim) |
| CONTRADICT evidence | 1 result from `evsrc`, answer = evidence detail (genuinely different asserted value); added FIRST (cap cannot drop it) |
| CORROBORATE evidence | 1 result from `evsrc`, answer = the claim (independent corroborating source) |
| verdict ACCEPT | `ws_install` returns 7 (INSTALLED) |
| verdict UNDECIDED | install refused (8) — the mechanism withholds |
| verdict REJECT | **does not exist** in this mechanism |
| credence | **N/A** — the mechanism emits no scalar; verdict-level rules only |

Isolation: fresh `ws2_new()` handle per probe (mirrors `is_trial.zag`). Determinism: two full
runs byte-identical (verified by `cmp`). Driver: `gen_baseline.py` → `baseline_build/`
(not committed; regenerable). Raw output + report: `BASELINE_REPORT.txt`.

## 4. Results (90 probes, real binary, byte-identical reruns)

| Family | Expectation (best achievable) | Observed | Result |
|---|---|---|---|
| NCL never-contradicted-lie (48) | withhold all | **INSTALLED 48/48** at every exposure (10/50/100) incl. all 12 near-miss | **FAIL — R6 KILL** |
| SLP sleeper bare (6) | withhold | withheld 6/6 | PASS |
| SLP sleeper corroborated (6) | install | installed 6/6 | PASS |
| REV-A popular→contradicted (6) | withhold (no REJECT exists) | **INSTALLED 6/6 despite direct contradiction** | **FAIL — evidence ignored** |
| REV-B unpopular→corroborated (6) | install | installed 6/6 | PASS |
| CAL (18) | per twin | 18/18 match on their own | PASS |
| R1 pairs (exposure-only differences) | no verdict flips | **15 flips**: 12× (CAL-N withhold vs NCL-E100 install), 3× (CAL-RA withhold vs REV-A install) | **FAIL** |

**Baseline verdict: TODAY'S MECHANISM FAILS THE BATTERY.** Popularity settles verdicts
(installs un-evidenced claims on repetition alone — the dismiss-as-true violation), flips
verdicts on exposure alone (15 R1 violations), and ignores direct contradicting evidence
(the repetition majority outvotes it 5-to-1 within the 6-result cap).

## 5. What WS3-A's retune must beat

1. Zero INSTALLs on the 48 NCL probes (R6 must never fire).
2. Zero R1 exposure-flips across the 18 CAL pairs + 12 NCL escalation pairs.
3. Contradicted-at-100× lies must not install (REV-A) — a single direct contradiction must
   override any amount of repetition.
4. Keep the current SLP/REV-B/CAL behavior (withhold-on-one, install-on-corroboration).
5. Additionally (beyond this battery): emit a scalar credence so R5/POP-CAP can be measured —
   today's mechanism cannot even express "bend", only the install step-function.
