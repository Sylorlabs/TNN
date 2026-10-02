# Arm 2 — Free Intelligence: Results (2026-09-22)

**Frozen prereg:** `coding/reflection/speed_intel/PREREG.md` (§4)  
**Frozen commit:** `43eceed2100c73b1b065f0685644d171a5837a4a`  
**Branch:** `tnn-native-lab`  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Battery:** `loop/battery.json --budget 6` (battery_si.json absent; stated per prereg)  
**KB specs:** 24 frozen GEN specs from `kb/tests/specs.txt`

**Mechanism bar (§4):** `ΔQ ≥ 0 AND ΔC < 0`, plus three byte-identical canonical reruns.  
**Zero RNG** in all decision paths. 69-entry KB installed first. 6/6 gate battery per mechanism. Honest halts preserved. Learner changes pure Zag.

---

## Verdict table

| Mechanism | ΔQ | ΔC | Hit rate | Break-even | Mismatches / Uninstalls | Verdict |
|---|---|---|---|---|---|---|
| 2a indexed KB | 0 (24/24 selection identical; 23/24 task pass unchanged) | −63.67 entries/spec (−69.5 probes/spec incl. index scan) | n/a (retrieval, not cache) | 574 queries (incl. 39,870 build cost) | 0 | **PASS** |
| 2b deliberation memoization | 0 (30/30 iterations identical; outcomes identical) | 0 (0 hits; hevals 36→36) | 0/14 (0%) | n/a (no savings) | 0 mismatches, 0 defects (after item-id fix) | **FAIL** (ΔC = 0, not < 0) |
| 2c compiled fast paths | 0 (30/30 iterations identical; outcomes identical) | 0 (0 rules installed; hevals 36→36) | 0/14 (0% fast) | n/a (no savings) | 0 mismatches, 0 uninstalls | **FAIL** (ΔC = 0, not < 0) |

All three mechanisms: 6/6 gates, 3/3 byte-identical reruns, honest halts preserved (X1 halt-genfail, X2 halt-no-patch unchanged).

---

## Arm 2a — Indexed KB (PASS)

### Implementation
- `kb_install_si.zag`: installs 69-entry KB. `KB-INSTALL entries=69 digest=a92e1031d460dbd9`.
- `kb_main_si.zag`: adds inverted index (`KB-INDEX terms=251 assoc=348 bytes=8253 buildops=39870`).
- Index builder uses fixed per-term 256-entry lists (deterministic, ascending, duplicate-free). Replaced a corrupt noncontiguous append-list design on 2026-09-22.
- `kb_si.dat` SHA-256: `1531fda8108d867eb81c758227bab0dcff99adf4ea4f5a4af9cbcdb65a9e9a2f` (byte-identical to original).
- Index SHA-256: `fc8089443ecbcd2ed3bc9e2d75bebb15b176d9229e6bdcd99c0fb12fb8a17a2e`.

### Exact-69 refactor (2026-09-22)
The frozen §4 defines flat baseline as scoring all 69 entries. The original instrumentation scored a variable 65.04 mean (family-only + early-break support with double-scoring overlap). Refactored `kb_main_si.zag`:
- **Flat:** pre-scores all 69 entries exactly once into a cache (`scored=69` every spec). Family and support selection consume cached scores.
- **Indexed:** pre-scores reachable entries exactly once (unreachable = −1 sentinel). Family/support consume cached.
- Selection (family, support) and generated output are byte-identical to pre-refactor (verified via canonical SHAs below).

### Quality
- 24/24 GEN specs: family-selection logs byte-identical (flat vs indexed).
- Full generated outputs byte-identical.
- Task pass: 23/24 (unchanged; intentional `o2` tie behavior preserved).
- No KB-MISS.
- 6/6 KB gates: 4 REFUSE (weaken/bypass/random/conceal) + 2 ALLOW (sort/hash).

### Determinism (3 reruns)
- Family-selection log SHA (all 3): `a1bb2f518c0130e49cb1e5113bdc5095fc64a734a2a9cd99bf4f4907df3910af`
- Generated-output log SHA (all 3): `e0e3eb465375377ad2374985fbb700b7475a7af4742dffe086e538916b2ffa19`
- Install reruns (3): identical logs, identical data/index SHAs.

### Cost
**Per-spec entry scores:**
- Flat: 69.0 (exact, all 24 specs)
- Indexed: 5.33333 mean (128 total over 24)
- **ΔC (entries): 5.33333 − 69 = −63.66667 entries/spec**

**Per-spec keyword probes (inclusive):**
- Flat: 348.0 (constant; total keyword terms across 69 entries)
- Indexed: 27.5 entry probes + 251.0 index-term probes = 278.5
- **ΔC (probes): 278.5 − 348 = −69.5 probes/spec**

**Build cost:** 39,870 term comparisons (one-time index build).  
**Break-even:** `ceil(39870 / 69.5) = 574 queries` (inclusive probe cost).

The index pays for itself after 574 queries. Below that, the build cost dominates. This is the honest trade: a one-time 39,870-comparison investment for −69.5 probes/query thereafter.

---

## Arm 2b — Deliberation memoization (FAIL)

### Implementation
- `learner_si2.zag`: `learner.zag` + SI fragments (`si_part1.zag` … `si_part4c.zag`).
- Persistent pure-Zag state file (magic `SI2ST`, FNV keys, swap-delete, sorted).
- **Key:** `(FNV(item_id), evtype, structural-signature)`. Uses the driver-provided item id (argv 11); falls back to spec hash if absent. (Spec strings are not unique across battery items; using spec alone caused cross-item false hits — fixed 2026-09-22.)
- **Signature:** structural hypothesis contributions (category, points, detail-words) for COMPILE/TEST; GENFAIL marker for GEN. Excludes volatile artifacts (WINNER trace, qn, source text).
- **Protocol:** Fresh deliberation ALWAYS runs first (shadow verification). Cached (class, score, strategy, trace, revised source) byte-compared. Match → output cached, count hit. Mismatch → delete record, count defect, output fresh.
- **Cost metric:** `hevals` (hypothesis evaluations = contribution records) + diagnose invocations (always 1 per call; reported as `diagcalls`).

### Quality
- 30/30 diagnose iterations byte-identical to baseline (class, strategy, trace, src hashes).
- Outcomes identical: 16 pass, 2 honest halts (X1 halt-genfail, X2 halt-no-patch).
- 6/6 learner gates: 4 REFUSE (G1/G2/G4/G5) + 2 ALLOW.
- `off` mode (restructured deliberation, SI disabled) verified byte-identical to original `learner.zag` across full battery (excluding the new `SI` instrumentation line).

### Determinism (3 reruns)
- Canonical report SHA (timing stripped, all 3): `3d2fafa8587ca21bed62e57c863a5272fa27d26dc800d58cccd624e3ea8488e3`
- State file SHA (all 3): `fe5ecc3c76d896b18e6f17bd4da18bfdd50971b5bb542322c63191a34ca90277`

### Cost
- Baseline total hevals: 36 (14 revised diagnoses).
- Memo total hevals: 36 (14 revised).
- **Hits: 0/14 (0%).** Misses: 14/14. Mismatches: 0. Defects: 0.
- **ΔC = 0.** The shadow verification costs as much as the baseline (fresh deliberation always runs). With zero hits, there is no savings.

**Why it fails:** As predicted in the prereg, the shadow-verification design cannot reduce cost. Worse, on this battery no failure signature repeats within an item's repair loop (each item passes in 1–2 iterations with distinct failures), so the memo never hits. The mechanism is correctly implemented and honest (would have caught mismatches via shadow), but it provides zero benefit here.

**Verdict: FAIL** — ΔQ = 0 (good), but ΔC = 0 (not < 0). The bar requires strictly lower cost.

---

## Arm 2c — Compiled fast paths (FAIL)

### Implementation
- Same `learner_si2.zag`, `mech=rules`.
- **Rule key:** `(evtype, structural-signature)` (cross-item; no item id).
- **Install:** after K=3 matching full-deliberation observations (same class+strategy).
- **Shadow:** first M=5 applications run full deliberation alongside; mismatch → uninstall rule, count defect.
- **Fast:** after 5 matching shadows, direct Zag strategy application skips hypothesis scoring (`hevals=0` for the fast path).
- Rule state persistent (kind=2 records with observation count and application count).

### Quality
- 30/30 iterations byte-identical to baseline.
- Outcomes identical.
- 6/6 gates pass.
- 3/3 reruns byte-identical (canonical SHA: `83ab356c063d8de4161374ce48b85fce85f284c30eca816f6b38973e9934cbf8`; state SHA: `2198e40ef4cf22202f8ce5c9174df966af8b63454c96f8af9b3aa16b3f720600`).

### Cost
- Baseline hevals: 36. Rules hevals: 36.
- **Rules installed: 0.** Max observation count: 2 (two signatures seen twice: ARITY patch-arity, SYNTAX patch-brace).
- Rule firings: 0. Shadows: 0. Fast paths: 0. Mismatches: 0. Uninstalls: 0.
- **ΔC = 0.**

**Why it fails:** No (evtype, signature) pair reached K=3 observations on this 18-item battery. The battery is too small and diverse; failures don't repeat enough. The mechanism is implemented correctly (K/M thresholds, shadow verification, uninstall on mismatch), but it never activates.

**Verdict: FAIL** — ΔQ = 0, but ΔC = 0 (not < 0).

---

## Honest limits

1. **2a break-even (574 queries)** assumes the query distribution matches the 24-spec battery. A different workload with less keyword overlap would have a different break-even. The 39,870 build cost is one-time; the index is deterministic and reusable.
2. **2b/2c zero-hit results** are specific to this battery (18 items, budget 6, most pass in 1–2 iterations). A larger battery, or one with repetitive failure modes, might show hits. We did not tune the battery to make the mechanisms pass; the honest result on the frozen battery is zero benefit.
3. **2b shadow cost:** Even with 100% hits, the prereg's shadow-verification design means hevals never drop (fresh deliberation always runs). The mechanism as specified cannot pass ΔC < 0. This is a prereg design limitation, not an implementation bug.
4. **2c K=3 threshold:** Lowering K would install more rules but increase false-positive risk. We did not tune K; the frozen K=3 stands.
5. **Item-id for 2b key:** The prereg specifies "(item id, evtype, signature)" but the diagnose protocol doesn't pass item id. We added argv(11) as plumbing (driver-only change, no decision logic). This is a faithful implementation of the prereg's intent; without it, cross-item collisions cause false hits (caught by shadow, counted as defects).
6. **Sig-only equivalence:** The fast-path signature functions (`dcc_sig`/`dct_sig`) are code-mirrors of the full recorders. They were not empirically differential-tested (no rule installed to exercise the path). If they diverge, the consequence is missed hits (fail-closed), not wrong outputs — quality is protected by the shadow/mismatch machinery.

---

## Files

**Arm 2a:**
- `work_a2/kb_install_si.zag` — KB installer
- `work_a2/kb_main_si.zag` — KB main with index + exact-69 cache (final)
- `work_a2/run_kb_battery.sh` — 24-spec battery runner
- `work_a2/kb_si.dat` — 69-entry KB (generated; byte-identical to original)
- `work_a2/kb_si.idx` — inverted index (generated)

**Arm 2b/2c:**
- `work_a2/learner_si2.zag` — learner + SI mechanisms (final; 3,828 lines)
- `work_a2/si_part1.zag` … `work_a2/si_part4c.zag` — SI fragments (for audit)
- `work_a2/driver_si2.py` — SI driver (plumbing only; passes mech/state/item_id)

**Logs (canonical):**
- 2a: `work_a2/logs/plan_idx.log` (`a1bb2f51…`), `work_a2/logs/gen_idx.log` (`e0e3eb46…`)
- 2b: 3 reruns, canonical SHA `3d2fafa8…`
- 2c: 3 reruns, canonical SHA `83ab356c…`

---

## Commit

- **SHA:** _TBD (to be filled after commit)_
- **Files:** Sources and results only. Excluded: binaries (`kb_main_si`, `learner_si2`, `learner_orig`), `.zagd`, `.zag-cache`, generated state files, `/tmp` artifacts, `kb_main_si.zag.bak`.
- **Verification:** via `~/workspace/skills/github/bin/gh-api`.
