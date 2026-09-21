# Arm N — Build Log

## 2026-09-21: Correction and rebuild

### Coordinator correction (binding)
- Original dispatch ("No-ID memory", family ID) declared VOID by coordinator
  correction received 2026-09-21.
- Correct frozen row verified from `~/workspace/tnn-lab/units/arms/briefs/N.json`
  and `units/PREREG_FREEZE.md:532`: **N — Judgment-annotated chunks, family ANN**.
- Mechanism: chunks carry deliberate signed annotations; MA4 generalized from
  memories to units; signed i64 fixed-point; saturating overflow; ablation
  records judgments but ignores them during recall.
- Binding kills: (i) full fails to beat judgment-free control by ≥5pp on
  adversarial misleading-memory bar; (ii) ablation within 2pts of full;
  (iii) >10% chunks flip judgment sign >2x in any 100-episode window.

### Implementation (`cl/arm.zag`, pure Zag, zero RNG)
- Frozen compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Build: `znc cl/arm.zag -o .work/build/arm_bin` → 216,945-byte native binary.
- Unit = 64-byte chunk + persistent i32 ID + signed i64 judgment.
- Non-positional slots: `next_slot` allocator; identical content dedups to
  existing ID; changed content gets new ID/slot. (M7 exposed that positional
  slots prevented honest C′ ingestion; refactored 2026-09-21.)
- Slot stores source span (offs/lens); `n_revise`/`unit_verified` use stored
  span, not position-derived.
- Ledger: 16-word entries (op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48,
  stage@52, d1@56, d2@60). Append-only JUDGE_SET/JUDGE_REVISE with evidence
  citations; evidence-free drift refused.
- Saturating i64: `jsat_add`/`jsat_sub` clamp to I64_MAX/MIN; `jhalf_toward_zero`
  for revision decay.
- Actual-ID bookkeeping: `ingest_all_ids`/`probe_ids` record and use real IDs
  (dedup breaks id==position; initial 1.1%/3.8% M1 was a harness bug assuming
  id==index, fixed).

### Bugs found and fixed (2026-09-21)
1. **M6 LEDGER-BOUND**: ledger undersized for episode loop. Fixed by sizing to
   `4*nt+ny+4096` (stays under 2^25).
2. **M6 slice panic**: over-allocated 8×(nt+ny) ledger exceeded 2^25 bytes.
   Fixed with correct sizing (t1 corpora are small).
3. **n-adv slice panic**: `build_adversarial` ingested full 84k corpus into
   200-unit ids buffer. Fixed with `ingest_first_k_ids` (first 200 units).
4. **M4-code 23% content revision**: `code_rename` no-op patches (no pattern
   found) left F_PATCH set, causing `unit_verified` to fail. Fixed in
   `n_revise`: when content matches source, clear defect flags (no-op defect).

### 1x battery results (all PASS)
- M1 prose: 100.0/100.0, 84731 units, swap 64/64
- M1 code: 100.0/100.0, 148678 units, swap 64/64
- M2 (t1p/t1c/t2p/t3): 1 episode to criterion, 100.0 final
- M3: 100.0/100.0, 8050 survived, 50 valuable, CLEAR (no freeze)
- M4 prose: 100.0/100.0 (boundary/content revision)
- M4 code: 100.0/100.0
- M5: 84731 units, 5.4MB source, 14.2MB slot table, 5.5MB ledger
- M6 p2c: 100.0/100.0/100.0, tax 0.0
- M6 c2p: 100.0/100.0/100.0, tax 0.0
- M7: hit 100.0% (≥90), reuse 2.02 (≥1.5), dedup 49.6% (≥40)
- M8: 5 perturbations × 5 artifacts + stdout all byte-identical → DETERMINISM PASS
- n-adv: full=71.5, control=66.5, ablation=66.5, churn=0.0
  - Kill (i): 71.5−66.5=5.0pp ≥ 5pp → NOT FIRED (thin margin, noted)
  - Kill (ii): |71.5−66.5|=5.0 > 2 → NOT FIRED
  - Kill (iii): 0.0% < 10% → NOT FIRED

### 10x scale: ATTEMPTED — FAILED (toolchain limit)
- r10 corpus exists (52M prose, 91M code, 10x tiled).
- `read_file` refuses files >33,554,432 bytes (2^25 znc slice limit):
  `m1-prose` on r10 → `M1,FATAL,empty-corpus`.
- 10x would additionally exceed 2^25 for ledger (847k×64B=54MB) and slot
  `lit` table (847k×64B=54MB).
- This is a znc toolchain constraint, not an arm mechanism failure.
- Documented per "incomplete scale attempt = ATTEMPTED — FAILED".

### Provisional items (pending Micah's freeze)
- A15 ID-swap schedule (M1): provisional.
- A7/A8 M7 edit/lookup schedules (first-byte XOR, `(l*37)%nunits`): provisional.
- Preserved literally; not silently frozen.

### Commit
- Source: `cl/arm.zag`. Docs: `ARM_SPEC.md`, `BUILD_LOG.md`, `VERDICT.md`.
- Evidence: `.work/battery/*.log`, `.work/m8v2/` artifacts.
- Binaries, `.zagd`, `.zag-cache` excluded.
