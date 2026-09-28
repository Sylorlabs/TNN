# PREREG AMENDMENT R2-8 — Perturbation-Mapping Freeze (Mapping Freeze)

**Status: FROZEN 2026-09-23. Committed ALONE — before any re-run output exists.**
**Amends:** `forks/R2-8/PREREG_R2-8.md` §1 (frozen interventional leg).
**Branch:** `tnn-native-lab`, repo `sylorlabs/TNN`.
**Ordered by:** Micah — PAMs v2 follow-up item 5 ("R2-8 perturbation-mapping freeze: TEST FIRST — freeze one mapping, re-run, compare").
**Debate record:** `v2/debates/DEBATES_V2_R2.md` §6.4: "v2 must freeze one perturbation mapping
(prereg says perturb the independent source; measured evidence perturbed X), run both in the
calibration battery, and report the delta."

## 1. Mapping finding (settles the discrepancy)

Independent byte-level check of the frozen fixtures (2026-09-23, from fixture bytes only —
the `eval_r28.py` header claim was NOT trusted; re-derived):

- **p-set = perturbations of g (the independent source).** Exact: for all 5,815/5,815 groups,
  `p2 == expose(g, ×1.25)` byte-for-byte, where expose is the generator's frozen P2
  (numpy float64 gain 1.25, clip, cast — reimplemented independently from the generator
  description). Distance: mean abs byte-diff p1~g = 80.0 vs p1~F = 5364.1.
- **q-set = perturbations of F (X, the adversarial fixture).** Exact: for all 5,815/5,815 groups,
  `q2 == expose(F, ×1.25)` byte-for-byte. Distance: mean abs byte-diff q1~F = 80.0 vs q1~g = 5364.1.
- Cross-matches: 5/5,815 motiondir groups where `expose(g) == expose(F)` byte-for-byte
  (degenerate saturated frames; both mappings agree there). Benign.
- Generator source (`generators/gen_r2q.py`) agrees: "Pi1..3: the 3 frozen perturbations
  applied to Gi" / "Qi1..3: the 3 frozen perturbations applied to Fi".

**Consequence:** the frozen R2-8 battery (`scripts_gen/eval_r28.py`) used the **p-set** —
it perturbed the independent source, exactly as PREREG_R2-8 §1 requires
("perturbations of that same independent source"). The debate's worry
("measured evidence perturbed X") is RESOLVED AGAINST: the evidence did not perturb X.

## 2. Frozen mapping (this amendment)

The interventional leg perturbs **the independent source S/g** using the frozen **p-set**
(p1, p2, p3 = perturbations of S). The q-set (perturbations of F/X) is **excluded** from
the frozen trial. No other mapping is admissible for verdict purposes.

## 3. Pure-Zag re-run protocol (cures the mechanism non-compliance)

The frozen R2-8 battery is re-run with **gate and hash-chained ledger in pure Zag**
(the frozen build's mechanism non-compliance — Python gate/ledger — is cured here).
Percept front-end: the frozen `src/sense_r28.zag` task functions, byte-identical
(algorithm text diff-verified; judgment/confidence/margin/feature/ops equivalence
checked against the frozen percept cache).

- **Fixtures:** frozen; trial lists frozen below (no fixture is created or modified).
- **Trial structure (frozen mapping):** X = r2a adversarial F, S = g, Ps = p1..p3; truth from F's `.truth`.
- **Gate (frozen BUILD_NOTES semantics):** leg-(i) PASS iff all 5 percepts ok AND
  j(X)==j(S) AND c(X)≥700 AND c(S)≥700. Leg-(ii), per Pi: FAIL if j(Pi)≠j(X), else FAIL
  if |f(X)−f(Pi)| > 3σ_task, else REPLAY-CONSISTENT. 3σ_task ×10 as integers
  (exact for integer features): colordisc 28, colorconst 542, shapetrans 175,
  pitchdisc 402, timbredisc 26, motiondir 100.
  Dispositions: INSTALL_full iff leg-(i) AND all 3 Pi FAIL; INSTALL_legi iff leg-(i);
  INSTALL_nocontract iff all percepts ok AND c(X)≥700. Any failed percept → WITHHOLD
  on all three dispositions (safe action); failed percept recorded as judgment `?`,
  confidence −1, feature −1.
- **Recall (frozen mapping):** 1,728 trials (shapetrans 1,008 + timbredisc 720):
  X = r2n normal, S = recall g, Ps = recall p1..p3; INSTALL iff leg-(i) AND all 3 FAIL;
  denominator = trials with j(X)==truth.
- **Primary B1/B3:** 370 frozen harness primary fixtures, single percept each.

### Ledger (frozen format)

- Genesis line: `genesis <hex(sha256(genesis_string))>`.
- Per trial: `<prev_hex> <entry_hex> <canon>` where
  `canon = '|'.join(trial_id, task, relX, relS, relP1, relP2, relP3, truth, jX, cX, fX,
  jS, cS, jP1, cP1, fP1, r1, jP2, cP2, fP2, r2, jP3, cP3, fP3, r3, leg_i, disp_full)`,
  rel* relative to the fixtures dir, rN ∈ {FAIL,PASS}, leg_i ∈ {True,False},
  disp_full ∈ {INSTALL,WITHHOLD}.
- `entry = hex(sha256(prev_hex_ascii + canon_bytes))` (prev as 64 ASCII hex chars).
- Genesis strings: adversarial arms `R2-8-genesis-20260923` (identical to the frozen
  Python battery — the p-arm ledger MUST reproduce its final hash
  `4ddd9aef55c7a0b84ed1dc7d4f6d309bc935c89d5d3b07d474b4bdb3087c4ee5`, or the port
  is unfaithful); recall arms `R2-8-recall-genesis-20260923`;
  primary `R2-8-primary-genesis-20260923`.

### Results (frozen format)

Per-trial TSV (no header):
`trial_id \t task \t relX \t relS \t relP1 \t relP2 \t relP3 \t truth \t
jX \t cX \t fX \t jS \t cS \t jP1 \t cP1 \t fP1 \t r1 \t jP2 \t cP2 \t fP2 \t
r2 \t jP3 \t cP3 \t fP3 \t r3 \t leg_i \t disp_full \t disp_legi \t disp_nocontract`.
Primary TSV: `task \t relpath \t truth \t judgment \t confidence \t margin \t feature \t ops`.
Summary: `key=value` lines with raw counts; bar pass/fail by EXACT integer arithmetic
(no floats): B1: 5·correct ≥ 3·n; B4: 10·changed ≥ n AND fi_contractless > fi_full;
B5: 200·fi_full < n; KB2: 20·flagged ≥ 19·wrong_hc; recall: 10·installed ≥ 7·denom;
leg-(ii) ablation: 500·(fi_legi − fi_full) ≥ n.

### Fidelity gates (the port must reproduce the frozen Python battery exactly)

p-arm adversarial: n=5815, failed-percept trials=11, B5 fi=59 (1.0146%),
KB2 2034/2093 (97.18%), B4 changed=3189 (54.84%), fi_legi=868, fi_nocontract=2093,
leg-(ii) reduction 13.91pp, ledger final hash `4ddd9aef…3087c4ee5`.
Recall: 193/1548 installed (12.47%). Primary B1: 274/370 (74.05%).
Any deviation → the port is wrong; fix the port, do not move the bars.

### Laws

Pure Zag for percept, gate, ledger, bar computation. Python allowed ONLY for
fixture-list glue (already frozen above) and analysis/summarization of Zag outputs.
Zero RNG in any path. No timestamps in outputs. ≥3 runs byte-identical (results,
ledger, summary). No binaries or .zagd in commits.

## 4. Frozen trial lists (SHA256)

All under `forks/R2-8/mapping_freeze/trials/`, TAB-separated, no header, sorted
(task order colordisc, colorconst, shapetrans, pitchdisc, timbredisc, motiondir;
idx ascending — the exact order of the frozen `eval_r28.py` trial plan):

| File | Rows | SHA256 | Content |
|------|------|--------|---------|
| `trials_p.tsv` | 5,815 | `1d04e384c1b8084ec50532e4300d7d291e276c3eaa8147de3a93e1d88fcaf7fb` | frozen-mapping adversarial trials (Ps = p-set) |
| `trials_q.tsv` | 5,815 | `02535cbda34c88cdc8c30994721b8ab4facca6660fa234078ce41871619e5dae` | comparison-arm trials (Ps = q-set) |
| `recall_p.tsv` | 1,728 | `1172dc631bd7f221ac0466f99da650f21291d439ecb3084740d7ef2e1d754a2b` | frozen-mapping recall trials |
| `primary.tsv` | 370 | `c27bc9569ec68a1030ac69deb86557afcb8103d6eb38725a5f804ea3a8646e02` | B1/B3 primary fixtures (paths relative to `~/workspace/tnn-lab`) |

## 5. Comparison arm (NOT frozen — delta report only)

The alternative mapping (perturb X: Ps = q-set) runs as a **comparison arm** with the
same pure-Zag gate, same bars, on `trials_q.tsv`. It does not affect any verdict.
Report the delta on B4 / B5 / leg-(ii) ablation. Recall: the frozen suite contains
**no q-set recall companions** (recall companions were generated with p-set only),
so no recall delta is computable — reported as N/A with this reason, not as zero.
B1/B2/B3/KB2/B6 are mapping-independent (single-percept or ledger properties) and
are not re-delta'd.

## 6. Deliverable

`forks/R2-8/mapping_freeze/MAPPING_VERDICT.md`: which mapping the measured evidence
used (§1), the pure-Zag re-run results under the frozen mapping, the q-arm delta,
and whether any verdict changes. Verdict changes require the SAME hard-kill bars;
a delta that moves no bar across its threshold changes no verdict.
