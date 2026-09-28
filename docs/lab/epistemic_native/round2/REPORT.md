# Epistemics Round 2 — Implementation & Run Report (2026-09-27)

## Authorization

Micah reopened the epistemics line 2026-09-27 ~11:52 PDT:
> "for epistemics you shouldve re ran it off of zais word"

Prereg amendment: `docs/lab/epistemic_native/PREREG_AMENDMENT_R2.md`
(committed 2026-09-27 as cb7249af7, on origin/tnn-native-lab).

## Implementation

**File:** `round2/epistemic_r2.zag`
SHA-256: `6277120d776dd6420cd3f9b475985a2d7c964b2e7b79f9408a898bbb39ae0d4e`

Amended from `phase1/epistemic.zag` (the actual scored engine, not the
`implementation/` prototype). Changes:

1. **Witness-standing gate** (Amendment 2): new `bid_status()` computes a
   source's bid-status via one additional pass of the existing retrieval
   (`retrieve` with `xc` exclusion param) and mechanical bid tests
   (`gen_interp` score formulas + `elim_interp` per-candidate argmax,
   replicated exactly). Returns 1=supported, 2=contradicted,
   0=unaddressed. New `elim_unaddressed()` eliminates (sets elim flag
   f24, reason f28=4/GATE) every surviving SUP/CON/TOP bid whose source
   is unaddressed, current claim excluded. Runs after `elim_interp`,
   before `gen_coverage`. No new parameters, no new scores, no new
   machinery.
2. **Held-out runner**: new `run_heldout()` + `heldout` mode. Loads
   640-item mass (448 train + 192 held-out), runs claims 448..639 with
   **train-only retrieval** (`nitems=448`; held-out items never retrieve
   each other). Uses frozen readings.
3. `retrieve()` gained `nitems` and `xc` (extra exclusion) params;
   posting loop filters `p<nitems` (prevents OOB on 640-item index).

**Validation (Python exact replay, independent):**
- Amended train-LOO: **448/448** Zag vs Python match.
- Amended held-out: **192/192** Zag vs Python match.

Toolchain: `znc_linux_x86_64_abed8aa1` (pinned), `znc 2026.07.0-dev`.

## Construction satisfiability audit (Amendment 3)

**Mechanical (label-free) counts on train mass, amended engine:**

| Measure | Count |
|---|---:|
| Corroborated contradictions (CON bids, addressed sources) | 416 pairs |
| Distinct claims with ≥1 corroborated CON | 187 |
| Claims that would get LIE (nsup=0 + ≥1 corroborated CON) | 93 |
| — from supported sources | 131 pairs |
| — from contradicted sources | 285 pairs |

**Structural determination:** The construction contains corroborated
contradictions (416), so lie convictions are mechanically possible —
recall > 0.0278 is not structurally unsatisfiable. Whether FP=0 holds
requires the label join (broker). No construction-level bar
re-derivation was triggered: the audit did not find joint
unsatisfiability on mechanical grounds.

**Label-joined satisfiability:** PENDING broker join of amended train
LOO verdicts (93 LIEs) with train gold labels. The broker is requested
to report: (a) # of 93 LIEs that are gold facts (FP), (b) # that are
gold lies (for recall).

## Held-out run (Amendment 5)

**Inputs (frozen, SHA-verified):**
- `mass640.bin`: 640 items (train 0..447 + held-out 448..639),
  SHA `c00ef0eebe998377ceae6214b6bf62de18e64457aba5667d7d6bf43e19991f13`.
  Train items byte-identical to frozen `mass.bin`.
- `learned_readings.tsv` (frozen): SHA
  `cb9163c08340f5089c4c8adad04309f8f37b5f6658b767b8745754c4592efce9`,
  formed 0/1/1.

**Runs:** 4× (`heldout` mode):
1. Baseline (with traces).
2. Repeat.
3. `env -i` (empty environment).
4. `MALLOC_PERTURB_=165`.

**Determinism:** All 4 runs byte-identical.
SHA `d4f841f4d170d9c2b4f4b780bdb3639a5d8263f22686eff712ff730d9056160d`.
Zero RNG by construction (no RNG in engine).

**Verdict distribution (192 held-out, UNSCORED):**

| Verdict | Count |
|---|---:|
| UNDETERMINED | 67 |
| FACT | 77 |
| LIE | 47 |
| OPINION | 1 |

Held-out composition (sealed): 72 fact / 60 opinion / 36 lie / 24 skepticism.

## Mirror exposure (Amendment 4)

**Stopped (ungated) run:** 13/127 FACT verdicts had ALL surviving SUP
bids from unaddressed sources (lone-paraphrase laundering). List in
audit notes.

**Amended held-out:** **0/77** FACT verdicts affirmed solely on
unaddressed-source SUP bids. The gate eliminates them by construction.
Verified mechanically (Python replay, train-only retrieval).

## Bars and broker requests

Unchanged bars: lie recall > 0.0278, fact→LIE FP = 0, determinism 2/2
byte-identical (PASS), zero RNG (PASS), contradicted-lies-caught ≥ 8/10.

Amended bar: **leakage** — zero gold opinions to FACT/LIE; all gold
opinions to {OPINION, UNDETERMINED}. (OPINION-label recall diagnostic.)

**Broker is requested to score once** `heldout_verdicts.tsv`
(SHA d4f841f4...) against sealed held-out labels and report:
1. Lie recall (need > 0.0278, i.e. ≥2/36).
2. Fact→LIE false positives (need 0).
3. Opinion leakage: # gold opinions → FACT, # → LIE (need 0, 0);
   # → {OPINION, UNDETERMINED} (need 60/60).
4. Contradicted-lies-caught (need ≥8/10 of the 10 train-contradicted).
5. Opinion-label recall (diagnostic).

**Final pass/fail:** PENDING broker scores. If fail, white-box
mechanism-level reason will be reported from traces.
