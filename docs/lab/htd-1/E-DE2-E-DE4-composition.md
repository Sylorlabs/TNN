# E-DE2+E-DE4 composition — head-to-head evidence (HTD-1)

**Date:** 2026-09-21 · **Crew:** MARATHON CREW 9 · **Branch:** `tnn-native-lab`
**Status:** COMPLETE — composition arm RUN and scored; verdict by frozen bars.

## 0. Question

The frozen prereg (§3a) requires a composition arm, E-DE2+E-DE4 stacked,
versus FULL-DELIB and each mechanism alone on the D-P1/D-P2
duplicate-enriched workloads, with the prediction of sub-additive savings and
the annotation rule: *if stack divergence exceeds either mechanism alone,
annotate both "do not compose."*

The verdict sheet (commit `8d74c47b5737`) recorded the composition as
held-and-never-run and called the premise dead — but it had **no composition
evidence**. This document replaces that inference with a direct,
preregistered measurement.

The question it answers: **does E-DE2 contribute anything on top of E-DE4,
or is its contribution zero/negative?**

## 1. Design (frozen-spec-faithful)

- **Outer layer — E-DE4 narrow:** the exact frozen narrow key
  `(input-hash, relevant-state-hash)` with provenance-carrying relevance
  partitions (`artifacts/ede4_relevance.json` v1, unchanged). On a hit the
  cached `(winner, mask, features)` is served and a `CACHE_HIT` entry
  (op 10, distinct from E-DE2's op 8/9) points at the originating episode.
  No deliberation on hits.
- **Inner layer — E-DE2 arm (a) naive exit:** on a cache miss, the early-exit
  deliberation runs (incremental expansion, incremental elimination with
  first-violation reasons, exit when `|live|==1`, `SUFFICIENCY_CERTIFICATE`
  with in-run certificate replay), then the outcome is inserted into the
  cache. Arm (a) — not the revival-guarded arm (b) — because on D-P1/D-P2 the
  two sub-arms are behaviorally identical (the (b) guard blocked zero exits on
  all 1,499 previously scored items; the guard is vacuous on these monotone
  workloads), and (a) is the minimal preregistered mechanism with maximal
  saving — a "truly dead" verdict under (a) is the strongest statement.
- **Op accounting** composes per the frozen cost-model contract ("Same rules
  composed; report the interaction term"): cache-hit paths cost OP-09/10/11
  only; misses cost full E-DE2 accounting plus cache insert (OP-06/07/08).
- **Frozen bars applied:** KB1 (divergence >2% kills), KB2 (saving <15%
  kills), KB4 (R=5 byte-identical artifacts required), E-DE4's inherited
  KB1/KB3/KB4 (zero false hits, hit/origin replay, hostile collision —
  the key machinery is byte-unchanged), and the composition annotation rule.

## 2. Method

- One new pure-Zag binary, `builds/comp/comp_bin`, importing the canonical
  E-DE4 module (`builds/ede4/ede4.zag`) verbatim for all cache/key/ledger
  machinery and a verbatim copy of the E-DE2 mechanism (`c2_item`,
  `c2_elim_depth`, `c2_cert_replay`) for the miss path. No randomness in any
  decision path; deterministic given state.
- Workloads: the frozen duplicate-enriched manifests
  `builds/ede4/dup_p1.txt`, `builds/ede4/dup_p2.txt` — 600 unique items
  repeated once each, 1,200 scored episodes per leg. The pristine snapshot
  (`builds/ref-baselines/runs/snapshot.bin`,
  sha256 `244d50997e7c15391440b7433e7ac8665ef2317b68129080acbdcc9fcd2692c1`)
  is copied fresh per run; the pristine file is never written.
- Four legs, all on the same 1,200-item workloads, R=5 each:
  1. `fd` — FULL-DELIB (`ref-baselines/fulldelib_bin`) reference.
  2. `e2a` — E-DE2 arm (a) alone (rebuilt `ede2_bin_rebuild`, see §6).
  3. `e4n` — E-DE4 narrow alone (`ede4/ede4_bin narrow`).
  4. `comp` — the composition (`comp/comp_bin`).
- Frozen cost model weights `w=[1,12,5,0.2,0.5,0.02,20,1000,0.05,30,3]`,
  extracted programmatically from `contracts/COST_MODEL_FROZEN.md`
  (extraction script notes in `builds/comp/`).
- Evidence: 40 artifacts in `builds/comp/runs/`, each R=5 with SHA-256 in
  `runs/battery.log`; `runs/analysis.json` holds the full parsed numbers,
  `runs/score_summary.txt` the human-readable summary, `score_comp.py`
  the scorer.

## 3. Results — headline (frozen cost C, lower is better)

| leg | D-P1 C | D-P1 saving | D-P2 C | D-P2 saving | aggregate C | aggregate saving |
|-----|-----------|-------------|-----------|-------------|-------------|------------------|
| fd (FULL-DELIB) | 35,002,899.68 | — | 54,973,421.28 | — | 89,976,320.96 | — |
| e2a (E-DE2 arm a) | 36,506,406.24 | **−4.30%** | 48,499,066.52 | +11.78% | 85,005,472.76 | +5.52% |
| e4n (E-DE4 narrow) | 20,240,219.68 | +42.18% | 30,371,593.28 | +44.75% | 50,611,812.96 | +43.75% |
| comp (E-DE2+E-DE4) | 20,992,228.96 | +40.03% | 27,134,415.90 | **+50.64%** | 48,126,644.86 | **+46.51%** |

Cross-checks: the `fd` and `e4n` aggregates reproduce the E-DE4 handoff's
reported numbers exactly (baseline 89,976,320.96; E-DE4 50,611,812.96;
43.75% saving). The `e2a` D-P1 saving (−4.30%) reproduces the E-DE2
handoff's −4.33% on unique items; D-P2 (+11.78%) reproduces its
+11.85%/+11.23% range.

### Composition vs E-DE4 alone (the decision-relevant comparison)

| battery | C_comp − C_e4n | E-DE2's contribution |
|---------|----------------|----------------------|
| D-P1 | **+752,009.28** (comp *worse*) | **NEGATIVE** |
| D-P2 | **−3,237,177.38** (comp *better*) | **POSITIVE** |
| aggregate | **−2,485,168.10** (comp better) | net positive |

### Interaction term (frozen contract: "report the interaction term")

`I = C_comp − (C_e4 + C_e2 − C_fd)` (additive-independence prediction):

| battery | additive prediction | actual C_comp | I |
|---------|--------------------|---------------|---|
| D-P1 | 21,743,726.24 | 20,992,228.96 | −751,497.28 |
| D-P2 | 23,897,238.52 | 27,134,415.90 | **+3,237,177.38** |

D-P2 confirms the prereg's predicted **sub-additivity** (I > 0): the stack
saves less than the sum of independent savings, because E-DE2's early exits
and E-DE4's duplicate hits attack the same redundant work. On D-P1 the
interaction sign is vacuous (E-DE2 alone is net-negative there, so the
additive baseline is pessimistic); the decision-relevant fact is the direct
+752k loss vs E-DE4 alone.

### Mechanism read

- D-P1: E-DE2 **never early-exits** (0 exits in 600 composition misses).
  Its miss path is strictly more expensive than E-DE4's (exit checks +
  certificates + replays with zero benefit; E-DE2 alone costs 1,252.92/item
  more than FULL-DELIB). The composition pays that overhead 600 times:
  600 × 1,252.92 ≈ 751,754 ≈ the observed +752,009. E-DE2 is pure overhead.
- D-P2: E-DE2 early-exits on **165 of 600** composition misses (27.5%).
  The per-miss saving vs full deliberation is 5,395.30/item; 600 × 5,395.30
  = 3,237,177.6 ≈ the observed −3,237,177.38 **exactly**. E-DE2 genuinely
  cheapens the first copies that E-DE4 then serves from cache.
- Divergence: **0/1,200** winner+mask mismatches vs FULL-DELIB on all six
  mechanism legs (KB1 holds everywhere; the "do not compose" annotation
  trigger — stack divergence exceeding either parent — does not fire).
- KB3: in-run hit-vs-originating-episode equality held on all 1,200 hits
  (600 per battery); zero certificate replay failures; zero false hits.
- KB4: all 8 configs R=5 byte-identical (SHA-256 in `runs/battery.log`).

## 4. Verdict (by frozen bars, no preferences)

- **E-DE2 alone: KILLED on KB2** (aggregate +5.52% < 15%; D-P1 −4.30%,
  D-P2 +11.78%). Confirms the E-DE2 handoff's kill on the
  duplicate-enriched workload. KB1/KB3/KB4 hold (0 divergence, all
  certificate replays pass, R=5 byte-identical).
- **E-DE4 narrow: SURVIVES** (43.75% aggregate; all bars hold). Unchanged.
- **Composition: SURVIVES its bars** (KB1 0 divergence, KB2 46.51%
  aggregate / 40.03% D-P1 / 50.64% D-P2, KB4 R=5 byte-identical) **and
  beats E-DE4 alone in aggregate by 2,485,168.10 (46.51% vs 43.75%)**.
- **E-DE2's contribution is battery-dependent, not zero:** positive on D-P2
  (−3.24M vs E-DE4 alone), negative on D-P1 (+752k vs E-DE4 alone).
  The verdict sheet's "premise dead" inference is **refuted for D-P2-like
  workloads and confirmed for D-P1-like workloads**.
- **Composition rule of thumb (evidence-determined):** compose E-DE2 under
  E-DE4 only where E-DE2's early exits actually fire (early-decisive
  features, D-P2-like); where they never fire (D-P1-like), the stack is
  strictly worse than E-DE4 alone — do not compose there.
- The prereg's sub-additivity prediction is **confirmed** on D-P2
  (I = +3.24M): savings overlap, they do not multiply.

## 5. Reproduction

```
cd builds/comp
./comp_bin <snapshot> <dup_p1.txt|dup_p2.txt> <out.bin>   # composition
./run_battery2.sh        # full 4-leg × R=5 battery (fd legs in run_battery.sh)
python3 score_comp.py    # -> runs/analysis.json, runs/score_summary.txt
```

Toolchain: `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
Pristine snapshot SHA-256:
`244d50997e7c15391440b7433e7ac8665ef2317b68129080acbdcc9fcd2692c1`
(copied per run, never modified).

## 6. Incident: latent parse miscompile in the frozen E-DE2 binary

During the battery, the frozen `builds/ede2/ede2_bin` (built 2026-09-21
07:58) rejected `dup_p2.txt` with `ITEMS_PARSE_BAD` while `fulldelib_bin`
and `ede4_bin` parsed it fine. Bisection: any item with byte-length
**> 65,535** was rejected; the threshold is exactly 2^16. Item
`D-P2 sqlite3 6716471 72658` (72,658 bytes) was the first offender.

Root cause: a build-specific codegen defect in that binary's copy of the
manifest bound check (`ln>4194304`, byte-identical source in all three
binaries — `ref-baselines/delib_core.zag` and `ede4/delib_core.zag` are
SHA-identical, `ca2e498d...`). The defect is latent: it only triggers on
items longer than 65,535 bytes, which no E-DE2 validation manifest
contained.

Remediation (evidence-backed, no source change): rebuilt `ede2.zag` from
identical source with the pinned toolchain →
`builds/ede2/ede2_bin_rebuild` (258,263 bytes, same size as the original).
The rebuild (a) parses the 72,658-byte item, (b) reproduces the handoff's
`e2a_dp2` artifact SHA **byte-identically**
(`795dee4ca49fcadd908aa1316c09e70db73e4435a7dcdece5b54a37b020745f8`)
on the original 599-item manifest, and (c) reproduces the old binary's
`e2a_p1` artifact SHA byte-identically (`fb2119679764829cf7f9dff2a568a48633adad6d2e2bc18127da8307c2bcd592`)
on the 1,200-item duplicate-enriched D-P1 workload. The `e2a` leg above ran
entirely on the rebuilt binary. The original binary is preserved untouched;
this incident is logged for the toolchain record (candidate ZNC-2026-09-21
parse-bound entry).

## 7. Files

- `builds/comp/comp.zag`, `builds/comp/comp_main.zag` — composition harness
  (pure Zag; E-DE4 module imported verbatim, E-DE2 mechanism copied verbatim).
- `builds/comp/run_battery.sh`, `builds/comp/run_battery2.sh` — battery drivers.
- `builds/comp/score_comp.py` — scorer (frozen weights).
- `builds/comp/runs/battery.log` — per-run SHAs (40 artifacts, R=5).
- `builds/comp/runs/analysis.json`, `builds/comp/runs/score_summary.txt`.
- `builds/ede2/ede2_bin_rebuild` — rebuilt E-DE2 binary (§6).
