# G2 ARM_SPEC — Deliberate cuts under pressure (family DELIBERATE)

**Status:** KILLED — binding kill criterion branch 1 fires (see VERDICT.md)
**Prereg:** frozen §3 row, `units/ALPHABET_G-L.md:145-147`; brief `units/arms/briefs/G2.json` (read 2026-09-21)
**Mechanism (frozen):** Pressure as trigger, never as policy: pressure events open a deliberation window; cuts still chosen deliberately.
**Implementation:** `cl/arm.zag` (2,263 lines, pure Zag, zero RNG in any decision path)
**Compiler:** frozen `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Battery:** full 1x M1–M9, two runs per leg, byte-identical stdout; M8 = 5 perturbations × 2 runs, byte-identical artifacts. Run 2026-09-21.

## 1. Kill criterion (frozen — either branch kills)

> Recall-quality advantage over G1 at matched occupancy < 2 absolute points on byte-exact recall,
> OR deliberation cost per pressure event > 50× G1's sweep with no quality advantage — deliberation buys nothing.

## 2. Design

- **Slot table:** id-derived placement, `cap` slots; parallel `[]u8` arenas (`ids`, `offs`, `lens`, `corps`, `flags`, `shifts`) holding little-endian u32s; `id2slot` map sized `max_ids`.
- **Flags:** F_OCC, F_LIVE, F_PIN, F_WEAKEN.
- **Pressure model:** occupancy = nlive/cap (pure function of logged state). WARN at 80%, CRITICAL at 95% (frozen integers). A pressure event opens a **deliberation session** (cooldown 1000 ops between sessions, re-entrancy guard).
- **Deliberation session:** budget `DELIB_BUDGET = 128` proposals (PROVISIONAL — AMBIGUITY-G2-001, frozen text names budget `B` but gives no numeric value); each proposal writes 2 ledger entries (`OP_CUT_PROPOSE` 194 / evidence check); session open (`OP_SESS_OPEN` 192) + close (`OP_SESS_CLOSE` 193) → **258 ledger entries per session**, all deterministic, zero RNG.
- **Cuts chosen deliberately:** proposals are evidence-checked; refused cuts logged (`OP_CUT_REFUSE` 196); committed cuts via kill/add primitives (`OP_CUT_COMMIT` 195). Pressure never selects a victim by itself.
- **Audit ledger:** 64-byte entries: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60. Overflow is fatal (fail-loud, never silent truncation).
- **Allocation trace:** (size:i64, code:i32, size:i32) per alloc/free — raw heap addresses deliberately NOT recorded (OS-assigned under ASLR; would make M8 artifacts irreproducible).
- **Recall:** byte-exact, boundary-exact; `g_recall` resolves corpora through the `(coffs, clens)` registry over one concatenated buffer.

## 3. Modes (single binary, `argv[1]` selects)

| Mode | Corpus / task | Result (1x, double-run byte-identical) |
|------|---------------|----------------------------------------|
| M1 prose | 5,422,721 B → 84,731 units | recall 100.0, boundary 100.0; ID probe 64/64 PASS |
| M1 code | 9,515,341 B → 148,678 units | recall 100.0, boundary 100.0; ID probe 64/64 PASS |
| M2 | T1 teach → T2 zero-shot transfer | t1p_etc=1, t1c_etc=1, t2p=100.0, t2c=100.0, m9=100.0 |
| M3 | churn: 1000 valuable pinned + 3000 fresh / 3000 kill / 50 weaken / 4000 fresh | valuable survival 100.0, fresh recall 0.0, mgmt 7050, weaken 50/50, **FROZEN-UNDER-PRESSURE**; sessions=2, delib_entries=516, cost/session=258 |
| M4 | 200 defects, 50 deliberate revisions | defects 200, detected 200/200, corrected 100.0, post-recall 100.0 |
| M5 | footprint + ledger evidence | 84,731 units learned byte-exact, ledger 85,732 entries / 5,486,848 B, mismatch 0 |
| M6 | transfer (repeat of M2 structure) | t1p_etc=1, t1c_etc=1, t2p=100.0, t2c=100.0, m9=100.0 |
| M7 | dedup/reuse accounting | hit 99.6, reuse 1.00, dedup savings 0 B |
| M8 | determinism: 5 perturbations × 2 runs | M8GATE **PASS** — store_hashes, store_chain, ledger.bin, ledger_chain, alloc_trace, stdout, stderr byte-identical across all 10 runs |
| M9 | forgetting audit (folded into M2/M6 legs) | t1_prose recall 100.0 after T2 training, 0 censored |

CSV + JSON evidence per leg under `work/runs/leg_*/a/stdout.txt` (run b byte-identical).

## 4. G1 comparator (matched occupancy)

| Metric | G1 | G2 | Δ (G2−G1) |
|--------|----|----|-----------|
| M1 prose byte-exact recall | 100.0 (84,731 units) | 100.0 (84,731 units) | **0.0** |
| M1 code byte-exact recall | 100.0 (148,678 units) | 100.0 (148,678 units) | **0.0** |
| M3 valuable survival | 100.0 | 100.0 | 0.0 |
| M3 fresh recall | 94.6 | 0.0 (frozen) | −94.6 |
| Deliberation entries / pressure event | n/a (sweep arm) | 258 | — |

G1 status: already KILLED by its own junk-fusion criterion (G1 ARM_SPEC.md). G1 commit `0b8b955d836eaf` (per parent).

## 5. Ambiguities (logged, interpreted literally)

- **AMBIGUITY-G2-001:** frozen text names deliberation budget `B` with no numeric G2 value. Implemented `DELIB_BUDGET=128`, marked PROVISIONAL everywhere. A different frozen value would rescale per-session cost (2×B+2 entries) but cannot change the recall numbers or the verdict.
- **M5/A15 and M1 ID probe:** provisional as documented in the brief; the N=64 probe passes 64/64 and does not affect the kill adjudication.
- **M6 JSON keys** reuse the `m2_*` namespace (shared print block with M2; only the CSV prefix differs). Evidence is unambiguous by run directory (`leg_m6_1x`).
- **M4 `m4_detected_tenths`:** reports 2000 (= defect count × 10), not a rate in tenths; all 200 defects are detected structurally (audited defects). Documented as a metric wart; does not affect any bar.

## 6. What the arm proved and did not prove

- Proved: byte-exact recall at 100.0 on both corpora; transfer with zero-shot→100.0 after teaching; deliberate revision (50/50); determinism under 5 adversarial perturbations (M8 PASS).
- Did not prove: any recall-quality advantage over G1 (0.0 points at matched occupancy); under M3 pressure the arm freezes (fresh recall 0.0 vs G1's 94.6) — the 516 deliberation entries bought no quality.
