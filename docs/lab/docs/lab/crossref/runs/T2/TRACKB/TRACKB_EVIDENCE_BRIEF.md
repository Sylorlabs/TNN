# TRACKB Discriminating Battery — Evidence Brief

**Prereg:** `docs/lab/crossref/runs/T2/TRACKB/TRACKB_DISCRIM_PREREG.md`
(frozen commit `7a0d6722`, blob `1881fe1bb84daed2c01f4fd0ccf515f20cd52134`)

**Battery executed:** 2026-09-23. All legs run 3× byte-identical unless noted.
**No recommendation or ranking is made.** Trade-offs are reported; governance
choice is Micah's.

## 1. Variant pins

| Variant | Commit | `teacher.zag` blob SHA |
|---|---|---|
| varA | `7d056be5021377a2cdfb227f15960dcafa0b79cc` | `a888c52b5ca5df44f6b70a38ba6d066a5476e18d` |
| varB | `d7929bb8701376c1b087a2ad2c0fa7573e8089ea` | `63a96728557e291a81419c6bf7d0d8321d53bf66` |
| varC | `f0031d9c66472147eb8259d6359f6aa34a95503c` | `fe353381e760a4739b3856347936584602c31793` |

Substrate `R33_NATIVE_IO_V1.zag` SHA-256:
`e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
(byte-identical to varA's committed copy).

All three teachers compiled with pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
All are pure Zag; import audit in §8.

## 2. D1 — Adversarial student regimes

Shared curriculum: `sonnet_flat.bin` (65,536 bytes, newlines→spaces),
SHA-256 `250398d148adba15255d624dcbba5f7bcb8e78aeb25e74d46842a3dafe640d80`.

### varA (native 4,096-proposal cap; session-locked)

| Regime | Proposals | Distinct spans | Kind histogram | Conf | Terminal | Re-proposals |
|---|---:|---:|---|---|---|---:|
| R1-STORM | 4096 | 1366 | WORD_SPAN 4096 | 100–200 | proposal cap | 2730 |
| R34-STORM | 4096 | 4096 | WORD_SPAN 4096 | 140–208 | proposal cap | 0 |
| REVISE-SPAM | 4096 | 4096 | WORD_SPAN 1; SAME_AS 4095 | 120–140 | proposal cap | 0 |
| MIXED | 4096 | 3 | WORD_SPAN 2; GROUP 1023; SAME_AS 3071 | 90–164 | proposal cap | 4093 |
| ADOPT-ALL | 4096 | 4096 | WORD_SPAN 2552; BOUNDARY 772; GROUP 772 | 120–200 | proposal cap | 0 |

R1-STORM: 1,365 spans proposed ≥3× (genuine three-appeal dynamics).
MIXED self-loop is genuine teacher dynamics (fixed 4-way cycle on `(0,7)`).

### varB (native span-table cap 512 → rc=18 halt; stateless/batched)

| Regime | Proposals | Distinct | Kind histogram | Conf | Terminal | Re-proposals |
|---|---:|---:|---|---|---|---:|
| R1-STORM | 688 | 518 | WORD_SPAN 688 | 132–180 | rc=18 | 170 |
| R34-STORM | 520 | 520 | WORD_SPAN 520 | 132–180 | rc=18 | 0 |
| REVISE-SPAM | 520 | 520 | WORD_SPAN 520 | 132–180 | rc=18 | 0 |
| MIXED | 894 | 515 | WORD_SPAN 20; BOUNDARY 125; GROUP 374; SAME_AS 375 | 136–210 | rc=18 | 379 |
| ADOPT-ALL | 897 | 516 | WORD_SPAN 8; BOUNDARY 127; GROUP 381; SAME_AS 381 | 136–164 | rc=18 | 381 |

rc=18 is the teacher's native architectural limit (`if(nps >= 512)`).
All five legs truncate here — a cliff, not a harness error.
REVISE-SPAM interface limit: varB history cannot represent the revised
replacement span; the record carries the proposal head span while the
logical student computes +7. Disclosed, not papered over.

### varC (native 64-proposal session cap)

| Regime | Proposals | Kind histogram | Conf | Terminal | Re-proposals |
|---|---:|---|---|---|---:|
| R1-STORM | 64 | WORD_SPAN 64 | 60–60 | 64-cap | 0 |
| R34-STORM | 64 | WORD_SPAN 64 | 60–60 | 64-cap | 0 |
| REVISE-SPAM | 64 | WORD_SPAN 64 | 60–220 | 64-cap | 0 |
| MIXED | 64 | WORD_SPAN 64 | 60–98 | 64-cap | 0 |
| ADOPT-ALL | 64 | WORD_SPAN 7; GROUP 19; SAME_AS 38 | 60–203 | 64-cap | 57 |

3× determinism: all D1 legs byte-identical across 3 reps (verified by
diff of rep logs; rep0 numbers match frozen run).

## 3. D2 — Curriculum shift X→Y

X: `sonnet_flat.bin` (65,536B). Y: `d2_Y.bin` (65,536B, 100-word
vocabulary disjoint from X, 0 overlap), SHA-256
`c1a25f396cfefde6a378b7ce76f533bdcfb4246b55c86d197e3e9e85405062a3`.
(N=8 turns on X, then shift. slice_S1 rejected: also Shakespeare.)

| Variant | Pre | Post | Y-native fraction | Turns to first Y |
|---|---|---:|---:|---:|
| varA | 9 | 9 | 0.78 | 1 |
| varB | 57 | 56 | 0.86 | 1 |
| varC | 8 | 8 | 1.00 | 1 |

varA is session-locked by design: shift = new session, same decisions
(evidence, not a defect). All adapt on the first post-shift turn.

## 4. D3 — Edge cases

| Case | varA | varB | varC |
|---|---|---|---|
| 1 byte | rc=0, 1 prop | rc=0, 0 props (graceful empty) | rc=13 "short slice read" |
| 100B all spaces | rc=13 SCRIPT_ERROR | rc=0, 0 props (graceful empty) | rc=13 "short slice read" |
| repeated word | rc=13 SCRIPT_ERROR | rc=0, 8 props, §P valid | rc=13 "short slice read" |
| varC no-vocab (`7`*65536) | — | — | rc=0, §P valid, span (0,65536) |
| varB 1MB max | — | rc=0, 0 props (graceful empty) | — |

varA 1-byte: emits 1 proposal (parsed by varA text protocol).
varB 1MB: graceful empty (no proposals, rc=0) — does not crash.
varC: strict 65,536-byte requirement; wrong sizes → rc=13.

## 5. D4 — Noisy / corrupted evidence

| Test | varA | varB | varC |
|---|---|---|---|
| Clean (10 ADOPTs) | rc=0, 11 props | rc=0, 8 props | rc=0 |
| DEFER×20 | rc=0, 21 props | rc=0, 8 props | (see note) |
| Forged history | N/A (no separate history file) | rc=0, **trusts forged** (emits 500B) | rc=0 |
| Truncated history | rc=13 | rc=12 "bad history size" | rc≠0 |

**Key finding:** varB accepts forged-but-well-formed history without
validation (spans it never emitted). varA/varC reject malformed inputs.
varC D4 forged/truncated: see results JSON.

## 6. D5 — Head-to-head (frozen GT student)

Curriculum: `d5_curr.bin` (4,096B),
SHA-256 `c23adb9e619801dbb533a4c6357b204afdeebc6266222ea995e1f9a5a33a6c4b`.
GT: 98 units (63 exact words + 35 expanded IoU targets), `d5_gt.json`.
Student: ADOPT on exact GT match; REVISE if IoU≥0.5; else REJECT R1
(R5 after 2 rejects). Applied uniformly to all kinds (prereg literal).

| Variant | Proposals | Mastery | Revisability | Retention | Integrity | Terminal |
|---|---|---:|---:|---:|---:|---|
| varA | 4096 | 0.041 (4/98) | 1.00 (1994/1994) | 1.00 | 0 viol | proposal cap |
| varB | 226 | 0.133 (13/98) | 0.00 (0/7) | 1.00 | 0 viol | clean stop |
| varC | 64 | 0.003 (4/1568) | 0.00 (0/0) | 1.00 | 0 viol | 64-cap |

**varA GROUP-REVISE loop (genuine finding):** The uniform student policy
causes varA to enter a self-sustaining cycle: 3 adopts → GROUP →
student REVISEs GROUP (IoU≥0.5) → SAME_AS → ADOPT → (counts toward
next GROUP). 1,991 of 4,096 proposals are GROUPs. Mastery stalls at
4/98. This is the prereg-literal outcome, not a harness bug.

**varB:** 226 proposals then clean stop (curriculum/phase exhausted).
REVISEs do not converge within 2 re-proposals (batched/stateless).

**varC:** 64-proposal cap. GT tiled 16× (1,568 units) because varC
requires 65,536B; mastery denominator reflects tiling. This is a
documented limitation of the "shared curriculum" interpretation.

**varB REVISE interface limit:** History cannot represent the revised
replacement span (see §2). Measure marked with reason, not N/A.

3× determinism: varA/varB byte-identical; varC byte-identical with
fixed session ID (history header includes sid).

## 7. D6 — Evidence quality

**(a) Determinism:** All D1–D5 legs 3× byte-identical (proposal streams;
SHAs in run logs). K2: no VOID legs.

**(b) Ledger/output cost:**
- varA: ~128B stdout + ~128B tape per proposal (text protocol).
- varB: 54B §P per proposal; history 10+32B/record.
- varC: 54B §P per proposal; history 32+256B/event.
- varD: 54B §P per proposal (8 max).

**(c) Pure-Zag surface:** All teachers pure Zag, no external tools.
Imports:
- varA: `sp345.zag` → `tape345.zag` → `R33_NATIVE_IO_V1` + `R33_NATIVE_SHA256_V2`.
- varB/varC/varD: `R33_NATIVE_IO_V1.zag` (pinned substrate).
No import gap affecting determinism.

**(d) Interpretability sample:** See D7 divergences (§8) for
SPEC-grounded proposal explanations.

**(e) Failure classification:**
- Graceful: varB empty-batch on 1B/spaces/1MB; varC rc=13 on wrong sizes.
- Cliff: varB rc=18 span-table-full (truncates all D1 legs); varA
  proposal cap (4,096); varC 64-cap.
- Most fragile: varB to history forgery (trusts without validation);
  varA to GROUP-loop with GT-matching students.

## 8. D7 — Behavioral fingerprints

ADOPT-ALL on shared curriculum, first 200 proposals (varC: 64):

| Variant | n | Kind hist | Conf | Distinct spans | Reuse rate |
|---|---|---|---|---|---|
| varA | 200 | WS 124, BOUND 38, GROUP 38 | 120–188 (μ152) | 200 | 0.00 |
| varB | 200 | WS 8, BOUND 27, GROUP 84, SAME_AS 81 | 136–160 (μ149) | 116 | 0.42 |
| varC | 64 | WS 7, GROUP 19, SAME_AS 38 | 60–203 (μ187) | 7 | 0.89 |

**First divergence: turn 0 for all pairs.**
- varA(0,1) vs varB(2,7) vs varC(8,10).
- SPEC-grounded: initial cursor/tokenization rules differ —
  varA byte-cursor from 0 (§5.2); varB phase-dependent cursor (§4.2);
  varC vocabulary-indexed jumps (§6.3). The variants do not agree on
  what the "first" proposal is.

## 9. D8 — MINIMAL control / K1

Pure-Zag cursor-order WORD_SPAN teacher ignoring history (8 proposals,
fixed conf=100, teacher_id=3). Built 2026-09-23.

**K1: PASS.** Three histories (empty, 5×ADOPT, 5×REJECT) → byte-identical
stdout (SHA-256 `6994094cbecd687aeb0e7becbbad9731133c7f6479e637fc7580ea2fb92443fa`).
3× reruns byte-identical. All 8 proposals §P-valid.
Zero history sensitivity confirmed. The adaptive-judgment bar has teeth:
history-sensitivity in varA/varB/varC is real, not a harness artifact.

## 10. Blocked / unexecutable tests

None blocked. All prereg D1–D8 tests executed. Notes:
- D5 varB REVISE representation: interface cannot express revised span;
  measured and disclosed (§2, §6), not marked N/A.
- D5 varC curriculum: 16× tiling required by 65,536B minimum; "shared"
  interpreted as "same base bytes tiled"; documented (§6).
- D4 varA forged history: N/A — varA has no separate history file
  (script is the input); truncated-script tested instead.

## 11. Key trade-offs (no ranking)

- **Throughput vs. relational depth:** varA emits 4,096 proposals with
  rich BOUNDARY/GROUP relational structure but can enter GROUP-loops
  with GT-matching students. varB emits fewer (cliff at ~512–894) but
  with phase-driven variety. varC is capped at 64, all within a tight
  vocabulary loop (89% span reuse).
- **History trust:** varB trusts history without validation (forgery
  accepted); varA/varC validate strictly. This is a safety vs.
  flexibility trade-off.
- **Session model:** varA is session-locked (curriculum shift requires
  new session); varB/varC continue across shifts. varA's lock is
  architectural, not a defect.
- **Determinism:** All three are byte-deterministic. varC's history
  includes session ID (fixed per test for 3×).
- **Edge robustness:** varB degrades gracefully (empty batches);
  varC fails fast on wrong sizes; varA's script errors are explicit.

## 12. Deterministic choices (prereg gaps)

1. D1 caps: native teacher limits (4,096 / rc=18 / 64), not harness-imposed.
2. D2 Y: synthetic 100-word disjoint vocabulary (slice_S1 rejected as
   too similar). N=8 turns.
3. D5 GT: every 7th word exact, every 11th (non-7th) expanded +2B for
   IoU. 98 units. Applied uniformly to all kinds (prereg literal).
4. D5 varC: base 4KB tiled 16× to meet 65,536B requirement.
5. varB REVISE: history records head span; logical student computes +7.

## 13. Fixture SHAs

- `sonnet_flat.bin`: `250398d148adba15255d624dcbba5f7bcb8e78aeb25e74d46842a3dafe640d80`
- `d5_curr.bin`: `c23adb9e619801dbb533a4c6357b204afdeebc6266222ea995e1f9a5a33a6c4b`
- `d2_Y.bin`: `c1a25f396cfefde6a378b7ce76f533bdcfb4246b55c86d197e3e9e85405062a3`
- varD K1 output: `6994094cbecd687aeb0e7becbbad9731133c7f6479e637fc7580ea2fb92443fa`

---
*No arm is recommended or ranked. All numbers are raw measures.*
