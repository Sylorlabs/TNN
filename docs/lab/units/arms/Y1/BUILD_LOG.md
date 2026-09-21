# Y1 — Negotiated cuts: BUILD_LOG

Arm Y1 (family CUT), Track A representation bake-off, round r1, scale 1x.
Built and tested 2026-09-21 by subagent ARM CREW Y1 (depth 2/2), reporting to
the Track A coordinator. Pure Zag, zero RNG in all decision paths, frozen
toolchain `znc_linux_x86_64_abed8aa1`.

## 0. Authority and corrections (both explicitly acknowledged)

1. **First coordinator correction:** the original assignment wrongly identified
   Y1 as "Adversarial corpus probe". That mechanism was voided. All wrong-path
   scripts (`tools/derive_arm.py`, `derive_arm_phase2..5.py`) and `corpus_c/`
   were deleted 2026-09-21. No wrong-path build or battery was ever completed.
2. **Second coordinator correction:** the coordinator admitted a remembered
   paraphrase of the frozen row (META family, "fast segmenter/slow verifier",
   ">25% add-latency" kill) was also wrong, and superseded it with the verbatim
   frozen row.
3. **Binding authority order:** (1) `units/arms/briefs/Y1.json`, (2) the
   coordinator's verbatim row, (3) nothing else. Brief and verbatim row agree:
   CUT family, "Two-organ cut protocol with mutual veto; deadlock →
   deliberate adjudication with a round limit", binding kill = "Over 10,000
   cuts, negotiated boundaries show ≤10% better recall-stability than arm-D
   unilateral cuts at the same granularity; OR veto rate collapses to <1%
   within the first 1,000 cuts (lazy agreement — then Y1 ≡ D with extra ledger
   cost)."

## 1. Specification

`ARM_SPEC.md` (this directory) records the literal implementation: two organs
(fast ingestion segmenter proposes 64-byte grid cut; slow recall verifier
vetoes word-token splits and counter-proposes nearest word joint), mutual veto,
deadlock → deterministic adjudication with fixed round limit N=3 (resolves
frozen ambiguity A-45), fixed justification enum
(J_NONE/J_SPLIT_TOKEN/J_EXCESS_SHIFT/J_NO_JOINT/J_ADJUDICATED), one ADD_UNIT
audit entry per committed cut carrying the negotiation evidence, persistent
sequential IDs with an explicit id2slot layer (tombstoned IDs never reused),
arm-D operationalized as the same fast segmenter with negotiation disabled at
identical 64-byte granularity (provisional, documented ambiguity Y1-A2).

## 2. Implementation

`cl/arm.zag` (~1,800 lines), single file + frozen native substrate
(`substrate/R33_NATIVE_SHA256_V2.zag`, `substrate/R33_NATIVE_IO_V1.zag`).
Compiles clean with the frozen toolchain (warnings only: ignored `nio_close`
returns, same idioms as the b64 reference).

Modes: `m1-1x-prose`, `m1-1x-code`, `m2-t1-prose`, `m2-t1-code`,
`m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`, `m3-1x`, `m4-1x-prose`,
`m4-1x-code`, `m5-baseline`, `m5-1x`, `m6-p2c-1x`, `m6-c2p-1x`, `m7-1x`,
`kill-1x` (the binding Y1 kill trial), `m8-1x` (artifact mode, §7 layout).

Notable defects found and fixed during bring-up:
- `kill-1x` initially panicked: the trial negotiates only the first 10,000
  cuts but `negotiate_all` pinned the final boundary at `buf.len` (5.4 MB),
  making the last "unit" ~4.8 MB and overflowing the 256-byte recall buffer.
  Fixed: the kill trial caps its final boundary at `n*64` (documented in
  ARM_SPEC §2; the trial covers the first 640,000 bytes of prose.bin).
- M7 C′/lookup schedule rewritten to follow `ARM_INTERFACE.md` §10 literally
  (every-100th-unit first-byte XOR 0xFF; `(l*37)%nunits` lookups split
  1666/1667/1667); new-slot counts are measured from `next_id`, not assumed.
  Still labeled PROVISIONAL-PENDING-FREEZE (A7/A8 unfrozen).

## 3. Test results (1x battery, double-run, byte-identical)

Full battery: `tools/run_battery_y1.sh` (local; mirrors the frozen harness
`run_battery.sh` plus the `kill-1x` leg; the frozen harness scripts were not
modified). Memorizer reference binary built from
`harness/memorizer/cl/memorizer.zag`. Scorecard assembled by
`tools/scorecard_assemble_y1.py` (local; the frozen assembler hardcodes
`arm=b64` and M7=N/A).

**Binding kill trial (`kill-1x`, 10,000 cuts, prose.bin):**
`stab_neg=100.0%`, `stab_uni=100.0%`, `veto_neg=58.7%` →
**KILLED** via disjunct 1 ("negotiated boundaries show ≤10% better
recall-stability than arm-D unilateral cuts at the same granularity";
observed improvement = 0.0%). Disjunct 2 did NOT fire (veto rate 58.7%,
far above the <1% lazy-agreement tripwire — the negotiation is genuine, it
just buys nothing). The mechanism works as designed; it is simply not worth
its cost. Y1 ≡ D with extra compute.

M1–M9 summary (see `work/battery_r1_1x/scorecard_y1_r1_1x.json`):
- M1: prose 100.0%/100.0% (84,731 units), code 100.0%/100.0% (148,678 units);
  swap probe 64/64 PASS on both (PROVISIONAL-PENDING-FREEZE); veto rates
  58.7% / 57.1%.
- M2/M9: ETC=1 on all five tiers (t1/t2 prose+code, t3 synthetic);
  M9 shape fast-then-flat everywhere.
- M3: survival 100.0%, fresh recall 100.0%, 8,050 mgmt entries, 50/50
  weakens handled, freeze CLEAR, 1,000 valuable.
- M4: rev_boundary 100.0%, rev_content 100.0%, kill_rate 0.0%, 1 episode.
- M5: memory 2.448 B/B (bar ≤1.5×: FAIL — RSS delta 8.07 MB + slot table,
  literal A4/A5/A16 accounting); audit 16.189 entries/KB (bar ≤10/KB: FAIL —
  one 64-byte ADD_UNIT entry per cut, same structural outcome as the b64
  reference's 16.189/KB).
- M6: transfer 100/100/100/0.0 tax both directions; memorizer validity gate
  (≥15pt drop in ≥1 direction): PASS/FAIL per control run.
- M7 (ID arm): hit 100.0% (bar ≥90: PASS), reuse 3.0 (bar ≥1.5: PASS),
  dedup 99.4% (bar ≥0.4: PASS). PROVISIONAL-PENDING-FREEZE.
- M8: M8GATE PASS (5 perturbations × 2 reruns, byte-identical artifacts).
- Determinism: every leg's two reruns byte-identical (double-run rule).

**10x status: NOT ATTEMPTED.** The 10x leg is gated on all 1x bars and the
Y1-specific kill bars passing. The binding kill fired at 1x, so the arm is
dead; per the hard laws, 10x was not started.

## 4. Verdict

**KILLED** — binding criterion disjunct 1 fired (see `VERDICT.md` and the
kill-trial evidence in `work/battery_r1_1x/kill-1x/`).

## 5. Deliverables

- `ARM_SPEC.md` — mechanism, kill operationalization, ambiguities, both
  corrections acknowledged.
- `cl/arm.zag` + `substrate/` — the complete Y1 implementation.
- `tools/run_battery_y1.sh`, `tools/scorecard_assemble_y1.py` — local battery
  and scorecard tooling (frozen harness untouched).
- `work/battery_r1_1x/` — raw per-leg logs (run1/run2 stdout, stderr,
  STATUS.txt, fragment.jsonl), M8 artifacts, `scorecard_y1_r1_1x.json`.
- `VERDICT.md` — the verdict with quoted criterion and evidence.
- `BUILD_LOG.md` — this file.
