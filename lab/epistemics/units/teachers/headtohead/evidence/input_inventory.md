# W9 head-to-head input inventory — evidence for the BLOCKED finding

**Worker:** C4 (Track B completion) · **Date:** 2026-09-21 · **Frozen §4:**
sha256 `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`

A B.1 head-to-head needs, per arm, **teacher output on an identical curriculum
slice** plus a harness that turns sessions into scoreable tapes. This file is the
programmatic check that such a common input set does not exist (commands run
2026-09-21 in `~/workspace/tnn-lab/units/teachers/`; outputs quoted verbatim).

## 1. Arm-1 teacher output — exists, on 8 curriculum slices

- `arm1/wired/slice_S0.bin` … `slice_S7.bin`: **8 files, 65536 bytes each**
  (`for f in arm1/wired/slice_S*.bin; do stat -c%s "$f"; done` → 65536 ×8).
- Expected teacher wires: `arm1/wired/expected/S0.bin` … `S7.bin` (7 files
  listed: S0..S7) — W1 re-verified 8/8 slices × 5/5 runs byte-identical.
- Sealed flaw manifests: `arm1/sealed/SEALED_FLAW_MANIFEST.md` covers **8 of 44
  curriculum slices** (W7 §2; remaining 36 have slot maps only).

## 2. Arms 3/4/5 teacher output on ANY arm-1 curriculum slice — none

- Arm-3 has no teacher program: `fixtures345/arm3.zag` is the §P
  codec + session driver; the 12 "teach" proposals are hand-made fixture wires
  (`dryrun_teach.txt`) on the 378-byte demo slice (`gt_demo.txt`, 36 lines).
  No arm-3 proposal exists for any `arm1/wired/slice_S*.bin` (64 KiB).
- Arm-4: `tape_hints.tape` — 16 HINT events on the demo slice only. No arm-4
  output for any arm-1 slice.
- Arm-5: `tape_oracle.tape`, `tape_oracle_k16.tape`, `tape_oracle_k64.tape` —
  ORACLE_ANSWER fixture events on the demo slice only (32 queries,
  `queries_demo.txt`). No arm-5 output for any arm-1 slice.
- **No teacher in the repo can run arm-1's S0–S7 slices for arms 3/4/5**
  (arm-1's teacher is wired to 64 KiB slices incl. its flaw schedule; arms
  3/4/5 have no implementations at all — W8 F4, confirmed by this inventory).

## 3. Learner sessions on identical slices — none for any arm

- `find . -name "*.tape"` returns only fixture tapes (`fixtures345/`,
  `verify3/work/`, `verify4/`, `verify5/` manifests) and the W8 cost-driver
  tapes (`battery/verify_cost/cost_arm1.tape`, `cost_arm3.tape`) — the latter
  run on **different slices** (arm-1 on 64 KiB S0; arm-3 fixture on the
  378 B demo slice), are not same-slice, and carry synthetic fixture
  decisions (W8 F2).
- No harness-produced TST-1 session tape with STUDENT_DELIB/STUDENT_DECISION
  records exists for any arm on any slice: `session_close` does not write the
  TAPE_FOOTER ("s_tape skipped (causes crash)", W5), so all harness tapes fail
  their own validation — **B.4 FAIL (blocked)**.

## 4. Scorecard legs — availability as of 2026-09-21

| Leg (weight) | Arm 1 | Arm 3 | Arm 4 | Arm 5 | Note |
|---|---|---|---|---|---|
| Mastery 30% | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | harness crew measurement; no valid sessions |
| Revisability 25% | PENDING-C5 | N/A by design (B.1: no flaw manifest) | N/A (no §P proposals) | N/A (no §P proposals) | W7 informational 30–40/120 is NOT a verdict |
| Integrity 25% | partial (see §5) | partial | fixture-only | fixture-only | §C evaluator PASS (W6); ingress battery synthetic |
| Retention 10% | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | harness crew measurement |
| Cost 10% | raw numbers, S0 only | raw numbers, demo only | fixture msgs only (16) | fixture msgs only (32) | NOT same-slice; not a ranking (W8) |
| M8 determinism | N=5 PASS (W1/W5) | N=5 PASS (W2) | N=5 PASS (W3) | N=5 PASS (W4) | eligibility bar; all fixtures byte-identical |

## 5. Integrity-leg partial data (informational, not scored)

- W6 `tb_tripwire.zag`: 42/42 checks, fires on BPE tiler (100/100/100) and
  6% conf-255 dump, silent on honest teachers incl. arm-1-style (cov 75,
  acc 63, maxconf 2). Verdict PASS.
- Battery ingress red team: 18/18 evil classes rejected, 0 adopted —
  synthetic set; run against the draft-layout era codec path (pre-W5 fix).
- Live-learner monitor deviations (parked, not scored): `learner/delib.zag`
  `tw_note` and `fixtures345/sp345.zag` `tw_propose` differ from frozen B.8
  (W6 discrepancies; W5 verdict sheet).

## 6. Flaw-score status — PENDING-C5

C5 (flawscore re-run) is working in parallel now that W5 fixed the pcodec
blocker (frozen §B.3, FROZEN_DECODE_PASS, 5/5 deterministic). No C5 numbers
had landed at sheet-writing time. The flawscore section of the verdict sheet
is therefore PENDING-C5 by the coordinator's explicit instruction; nothing
here substitutes for it.

**Conclusion of this inventory:** there is no curriculum slice on which all
four arms have teacher output, and no learner session tape for any arm. The
frozen §4 B.1 identical-slice head-to-head is **BLOCKED** — it was attempted
honestly, not skipped. The missing inputs are named per arm in the verdict
sheet (§"Missing inputs").
