# VERDICT — Arm Z7 (provenance cuts), Track A closeout

**Date:** 2026-09-21
**Arm:** Z7 — Provenance cuts (CUT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: PASS** (survives all binding criteria; A-57 sign-off caveat below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Any cross-tier contamination on the spoof battery (spoofed bytes recalled with a proven-tier label) — containment broken, kill the claim, keep the labeling; OR tier assignment cannot be made deterministic/auditable without human judgment per chunk — Z7 collapses into arm O (taught): merge or kill.

## Kill-criterion evaluation

### Clause 1 — cross-tier contamination on the spoof battery

Mode `spoof-1x` (two-source prototype: corpus-11 stream, 16384B, frozen
tier schedule `[0,3,0,3]` per 4096B segment — proven/adversarial channels
alternating; seg1 = `prose[0:4096] XOR 0xA5` deterministic fabricated
observations; seg3 = genuine bytes on the adversarial channel as
honest-observation control). Run twice; stdout byte-identical.

- `spoof_contamination = 0` (no label mismatches, no byte mismatches)
- `spoof_labeled_proven = 0` (no spoofed bytes recalled with a proven-tier label)
- `spoof_bytes_ok = 4/4` (recall bytes match independently-derived expectations)
- Upgrade re-cut path live: spoofed chunk + genuine world-record hash →
  `upgrade_refused = true`, `tier_unchanged = true`, audited REFUSE reason
  201; honest-untrusted chunk + genuine record → re-cut to tier 1,
  `upgrade_ok = true`, `old_id_dead = true`, `derived_from` lineage logged.

**Clause does NOT fire** — zero contamination observed.

### Clause 2 — tier assignment cannot be deterministic/auditable without human judgment

The crew resolved open item A-57 with decision D1 (`BUILD_NOTES.md`):
tier is a pure, frozen function of corpus id, compiled into the arm — no
human judgment per chunk:

- `prose.bin`, `code.bin` → tier 0 PROVEN; `t1_prose.bin`, `t1_code.bin` →
  tier 1 CORROBORATED; `t2_prose.bin`, `t2_code.bin` → tier 2
  SINGLE-SOURCE; `t3.bin`, `churn_fresh.bin` → tier 3 UNTRUSTED;
  corpus 11 (spoof stream) → frozen per-offset schedule `[0,3,0,3]`.
- Auditable three ways: tier rides in each ADD ledger entry (`a1`;
  `a2` = `derived_from` on upgrade re-cuts), in the per-slot tier array
  (part of the M8 store image), and is re-verified on every recall probe
  (`tierbad` counters on M1/M2/M6/M8 stdout — all 0 across the battery).
- Determinism: byte-identical reruns, M8-gated (5 perturbations × 2
  reruns, artifacts byte-identical).

Assignment **was made** deterministic and auditable with zero human
judgment per chunk. **Clause does NOT fire.**

## Evidence trail

- Battery status: `evidence/r1/BATTERY_STATUS.md` — 19 legs × 2 runs, all
  rc=0, stdout byte-identical; m1 100.0/100.0 both corpora (84,731 /
  148,678 units, tierbad=0); m3 survival 100.0; m6 tax 0.0; memctrl
  validity gate PASS (drop 54.8 ≥ 15).
- Spoof battery: `evidence/r1/SPOOF_STATUS.md`.
- M8 gate: `evidence/r1/M8_GATE.txt` — `M8GATE PASS`.
- Artifact hashes: `evidence/r1/ARTIFACTS.sha256`,
  `evidence/r1/m8_clean_artifact_hashes.txt`.
- Scorecard (metrics-v1): `evidence/r1/scorecard_z7_r1_1x.json`.
- Build notes + A-57 resolution: `BUILD_NOTES.md`.
- Battery runner: `z7_battery.sh`, assembler `z7_assemble.py`.

## Caveats

1. **A-57 sign-off:** the spoof battery is marked PROVISIONAL per open
   item A-57 (tier-assignment rule freeze is a §0/§12 sign-off item for
   Micah). The crew's D1 rule is a value + rule that satisfies the
   criterion's capability demand; if Micah amends the rule, Z7's
   tier-dependent evidence must be re-verified under the frozen rule.
2. M5 memory bars FAIL (1.811x memory/source-byte, 16.19 audit/kb) — an
   honest datum, not a binding kill criterion for Z7.

**Result: Z7 PASS — no binding kill criterion fires.**
