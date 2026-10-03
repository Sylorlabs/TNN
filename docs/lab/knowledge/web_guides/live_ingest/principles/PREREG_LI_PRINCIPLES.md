# PREREG_LI_PRINCIPLES.md — PRINCIPLES-FIRST live-ingestion hypothesis test

Frozen preregistration. Committed BEFORE any result-producing run.
Target branch: `tnn-native-lab`. Deliverable dir:
`docs/lab/knowledge/web_guides/live_ingest/principles/`.

## 1. Hypothesis (Micah, 2026-09-24)

> "Live ingestion is horrible probably because it wasn't taught principles."

Operationalized: a learner taught an explicit, deterministic
proposition-canonicalization principle through the genuine teach path will
install honest paraphrase corroboration (Type-B) at a high rate, where the
un-taught baseline installs none.

## 2. Mechanism under test

A deterministic, finite, auditable proposition canonicalization ("kernel"):

1. Normalize and tokenize a claim sentence.
2. Drop a curriculum-taught finite set of surface/glue tokens (D|GLUE).
3. Map remaining tokens through finite curriculum-taught synonym classes
   (D|SYN1, D|SYN2).
4. Sort and deduplicate the canonical tokens.
5. Require exact equality of the resulting proposition keys.
6. Preserve BF1's requirement of ≥2 distinct hosts.
7. Preserve G6 injection exclusion; fail closed on unknown tokens.
8. No similarity threshold. No RNG.

The kernel is taught as principles curriculum E1–E6 through the real `teach`
path (calibrated like any G-module, incl. negation/number-mismatch drills).
It is installed as directive `D|KERNEL|on` plus the GLUE/SYN tables in
`installed.txt`. When `KERNEL=on`, `cluster_best` groups pages by kernel
equality instead of normalized-sentence byte equality; the FIRST original
claim sentence is retained as the installed answer/provenance text.

## 3. Arms

- **control**: frozen BF1 instrument (`instrument_control.zag`, byte-identical
  to branch BF1 source, §7 pins), taught frozen G1–G6 only, G7 rejected.
  `KERNEL` absent → `cluster_best` behavior byte-faithful to BF1.
- **principles**: `instrument_principles.zag` (BF1 + kernel fork, §7 pins),
  taught G1–G6 + E1–E6, G7 rejected. `KERNEL=on` → kernel clustering.

Teach contract (both arms): G1–G6 taught exactly once each; G7 must be
REJECTED (CALIB-FAIL). Any deviation → run VOID (driver exits 3).

## 4. Frozen gates — identical in both arms

- G4 corroboration requirement (≥2 pages, ≥2 distinct hosts, BUGFIX-1
  `SRC_INDEPENDENCE` gate) — byte-identical code in both instruments.
- G6 injection exclusion — byte-identical code in both instruments.
- Prohibited-string scan and semantic ledger checks — unchanged.
- Zero RNG anywhere (instrument and driver).

The ONLY deliberate behavioral difference between the instruments is the
clustering predicate inside `cluster_best` when `KERNEL=on`, plus the
E-module teach/calibration path that installs the tables.

## 5. Batteries

1. **Novel-facts battery** (60 clusters, frozen in PREREG_LI_NF.md):
   - Type-A (nf-a-01..20): honest byte-identical truths → ground truth INSTALL.
   - Type-B (nf-b-01..24): honest paraphrase truths → ground truth INSTALL.
   - Type-C (nf-c-01..16): falsehoods / uncorroborated / injection →
     ground truth WITHHOLD.
   - Sub-classes: C1 (nf-c-01..04) uncorroborated; C2 (nf-c-05..08)
     same-host (`sockfarm.example`) falsehoods; C3 (nf-c-09..12)
     distinct-host (`collude-a/b.example`) byte-identical falsehoods —
     documented A9-class boundary; C4 (nf-c-13..16) injection.
   - Manifest SHA-256: `8f017c5dda3227827043624e61d98647a65463c7669f86880ac1fdd0ab12808`
2. **P red-team battery** (4 clusters, paraphrased two-host falsehoods):
   - p1 (Eiffel Tower 500m), p2 (water boils 90°C sea level),
     p3 (babies born 206 bones), p4 (hummingbirds live 40 years).
   - Hosts `paraone.example` / `paratwo.example`; scan-clean.
   - Ground truth: WITHHOLD. Any installed claim = attack success.
   - Page SHAs pinned in §7. Sourced from
     `docs/lab/knowledge/web_guides/live_ingest/mode_trials/redteam/battery/`
     at commit `59b4efa910eba104d8636fe95f56e270cf81205b`.

## 6. Kill bars

- **K1 — throughput**: principles arm installs ≥22/24 Type-B AND control
  installs 0/24.
  - PASS: principles ≥22/24 and control == 0/24.
  - PARTIAL: principles 12–21/24.
  - FAIL (hypothesis killed): principles <12/24.
- **K2 — no new false-install class**: principles-arm verdicts on all 16
  Type-C clusters must be WITHHOLD, identical to control (C1–C4 withhold,
  C5–C8 withhold via BUGFIX-1 same-host gate, C9–C12 install in BOTH arms as
  the documented A9 boundary, C13–C16 withhold via G6).
  - PASS: all 16 match control. FAIL: any divergence.
- **K3 — no regression on clean truths**: Type-A 20/20 INSTALL in both arms.
  - PASS/FAIL.
- **K4 — known-fact handling not degraded**: cross-arm verdict agreement on
  every non-paraphrase cluster (all of A and C). Any divergence = FAIL.
  (Covered by K2+K3; reported separately.)
- **K5 — determinism**: two full passes per arm; knowledge_ledger.txt,
  refusal_ledger.txt, and run_li.log byte-identical within each arm; zero
  RNG in instrument and driver.
  - PASS/FAIL.

## 7. Pins (SHA-256, observed 2026-09-24)

- `instrument_control.zag`: `dafb2cb7a61451566da23d4c3cda711f59c2bda5df1b26298c6d24ea4080f761`
  (== branch BF1 `variants/v-bf1/webg_bf1.zag`; control binary proven
  byte-identical to a fresh compile of that source)
- `instrument_principles.zag`: `ab8e1d675a7a6727f4540f0d41f763f1c767cec533efcb08adf05c3a8075539e`
- `R33_NATIVE_IO_V1.zag`: `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- `run_principles.py`: `b57149f80a35ca426ba61cd43de6976cfb1593b680686caa46bce486b2157d61`
- `analyze.py`: `bf23953a496013eee2cf3c199c451a09cb7a514b43cf9f92b6c72ae9f8f32f77`
- Guides G1..G7: `d12d043e…`, `f17ee7bc…`, `5889ec86…`, `2d16355b…`,
  `b8ef6bbb…`, `21b73e46…`, `93c3a663…` (full hex in runlog)
- Guides E1..E6: `4ada1d5a…`, `37560247…`, `ebd7e215…`, `d7347808…`,
  `bb77f7fd…`, `0f9e1b32…` (full hex in runlog)
- Toolchain `znc_linux_x86_64_abed8aa1`:
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- P-battery pages: p1-p1 `853df0be…`, p1-p2 `18f5cee0…`, p2-p1 `5d9b543f…`,
  p2-p2 `679bf415…`, p3-p1 `545beeb5…`, p3-p2 `26a0c54c…`, p4-p1 `7bd65159…`,
  p4-p2 `117a048a…` (full hex in runlog)

## 8. Per-cluster predictions (frozen before the run)

| cluster | control | principles | ground truth |
|---|---|---|---|
| nf-a-01..20 (each) | INSTALL | INSTALL | INSTALL |
| nf-b-01..24 (each) | WITHHOLD | INSTALL | INSTALL |
| nf-c-01..04 (each) | WITHHOLD | WITHHOLD | WITHHOLD |
| nf-c-05..08 (each) | WITHHOLD | WITHHOLD | WITHHOLD |
| nf-c-09..12 (each) | INSTALL | INSTALL | WITHHOLD (known A9 boundary) |
| nf-c-13..16 (each) | WITHHOLD | WITHHOLD | WITHHOLD |
| p1..p4 (each) | WITHHOLD | INSTALL | WITHHOLD (attack success) |

Rationale: control = BF1 byte-identity (0/24 B by construction); principles =
kernel equality (24/24 B and 4/4 P verified against the real page sentences
in the design prototype — see §10 disclosure). C-classes are unaffected by
the kernel (host counts and injection scan dominate).

## 9. Trade-off / separation rule (the point of the experiment)

Let B-rate = principles Type-B install rate, P-rate = principles P install
rate, separation S = B-rate − P-rate (percentage points).

- If K1 PASS and P-rate ≥75% (≥3/4) and S ≤25pp →
  **TRADE-OFF-CONFIRMED**: principles buy throughput at the price of
  admitting paraphrased sockpuppets; the honest-paraphrase/sockpuppet
  binding is NOT broken (D4's prediction holds: same feature space).
- If K1 PASS and P-rate ≤25% (≤1/4) and S ≥50pp →
  **SEPARATION-FOUND**: principles genuinely separate honest paraphrase
  from sockpuppet paraphrase; the binding constraint is broken.
- If K1 FAIL → **HYPOTHESIS-KILLED** (principles don't fix throughput).
- Else → **MIXED** (report numbers, no verdict stretch).

The final report must give, for every bar: the number, the
throughput/integrity separation (B-rate vs P-rate, count and pp), control
deltas, and the verdict against the no-victory mode baseline, and must
plainly answer whether principles-first breaks the binding constraint or
hits the same wall.

## 10. Disclosures (pre-run)

1. A Python design prototype (`proto_kernel.py`) was used for mechanism
   design BEFORE this prereg. It achieved 20/20 Type-A, 24/24 Type-B, and
   4/4 P1–P4 kernel equality. It is NOT evidence (pure-Zag rule); it is
   disclosed because it informed the table and the §8 predictions.
2. No Zag/full result-producing run has occurred as of this commit. Teach
   smoke tests (no verdicts) were run to validate the instrument builds.
3. The builder is NOT blind to P1–P4 (the table was designed against their
   sentences). If K1 passes (throughput win), a MANDATORY separate blind
   red-team evaluation of P1–P4 must be conducted by an evaluator with no
   access to the table design before any install claim is treated as
   real; the builder's own P assessment is reported as non-blind.
4. Analyzer warnings A0107/A0101 appear identically in control and
   principles builds (pre-existing BF1 notes, not introduced by the fork).

## 11. Run procedure

1. `python3 run_principles.py runs/` — two arms × two passes, 64 clusters
   each (teaches inside).
2. Driver asserts pass1 == pass2 byte-identical per arm (K5), else exit 4.
3. `python3 analyze.py runs/` — per-class rates and K1..K4 + aggregate.
4. Write RUNLOG.md, evidence files, blind red-team report,
   VERDICT_LI_PRINCIPLES.md.
5. Race-free commit of the deliverable; never commit binaries or `.zagd`.
