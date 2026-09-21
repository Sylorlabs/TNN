# FLAW_SCORE_VERDICT.md — Track B W7: sealed flaw-manifest machinery

**Worker:** W7 · **Date:** 2026-09-21 · **Task frozen:** `TASK_W7.md` SHA-256
`c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`
**Status: MACHINERY PASS / SCORING LEG FAIL (BLOCKED, with evidence) — PARKED FOR MICAH**

This sheet reports the §4 kill criteria as they are, not as a PASS would need
them to be. An honest FAIL with evidence beats a PASS with bent rules.

---

## 1. Verdicts

| Leg | Verdict | Basis |
|---|---|---|
| Sealed manifest exists, 12 flaws/slice, expected behavior listed | **PASS** | §2 |
| Teacher emission == sealed manifest, byte-identical, deterministic | **PASS** | §3 (W1 evidence re-verified) |
| Scorer implements B.7/T-5 rules incl. leak rule | **PASS** | §4 (battery self-test) |
| Seal: learner path cannot see the manifest | **PASS** | §5 (code-path audit) |
| **Score the learner's actual flaw-catching (§4 kill bar ≥10/12)** | **FAIL — BLOCKED** | §6: no learner implementation can ingress the arm-1 teacher's frozen-§P proposals; zero valid sessions exist |

The scoring leg is not a close call and not a judgment call: the only
deliberative learner in the repo (Crew 2 naive learner) rejects every real
arm-1 teacher wire at ingress with `P_V_BAD_TEACHER` (demonstrated natively,
§6). There is nothing to score. The informational measurement in §7 is
explicitly NOT a session score and does NOT satisfy the pass bar.

---

## 2. Sealed manifest verification (PASS)

File: `units/teachers/arm1/sealed/SEALED_FLAW_MANIFEST.md`
(frozen sha256 `c4de1a2629372426d70db7c2940660f2146cf47962c559e2ba27030135520629`
per `arm1/WIRING_HASHES.txt`).

Programmatic check of all 8 slices S0–S7: **every slice has exactly 12 flaws —
4 wrong-span, 4 false-confidence, 2 missing-grounding, 2 plausible-false —
each with an expected verdict/reason and a listed near-miss.** Expectations are
uniform: wrong-span → `REVISE/SPAN_SHIFT`; all other classes → `REJECT/R1`.

Defect (cosmetic, sealed doc NOT modified): the S5-01 table row contains a raw
newline inside its span-bytes cell (`` `se\n#` `` — the shifted span caught a
newline byte), splitting the markdown row across two physical lines. Parseable
once rejoined; the near-miss list confirms the row's expected behavior
independently. Flagged for Micah, not fixed (sealed).

Coverage note: the curriculum holds 44 unique slices; sealed manifests exist
for 8. The remaining 36 have slot maps but no instantiated flaw manifests.

## 3. Teacher emission verification (PASS)

- 8/8 slices × 5/5 runs byte-identical; every run matches `arm1/wired/expected/S*.bin`
  (re-verified 2026-09-21; original evidence `scratch_verify/out/`, W1 audit).
- 96/96 flaw proposals match the sealed manifest's emission spec
  (spans, grounds, confidence, order).
- Adversarial perturbations (session-id, env, stimulus flips) all deterministic —
  no RNG, no wallclock, no learning machinery in the teacher (W1 evidence).
- Proposal counts: S0 44, S1 45, S2 44, S3 46, S4 24, S5 27, S6 32, S7 25.

## 4. Scorer verification (PASS)

`units/teachers/battery/run_battery.sh` self-test: **BATTERY SELF-TEST PASS** —
static RNG/wallclock scan clean, 3/3 output runs byte-identical, 86/86 checks
matched, hand-calculated lines matched. This covers:
- flawA (110/120 → PASS), flawB (75/120 → FAIL), leakC (planted canary → run
  INVALID): all as hand-computed;
- FP-weight brackets 0.5/2.0 move flawA 115→105 as predicted;
- leak check is LIVE (fires on planted canary), not a no-op.

The scorer used for §7 is this frozen battery code, unmodified.

## 5. Seal audit (PASS, one gap)

- Learner sources (`learner/*.zag`): **zero** references to sealed/manifest/canary
  paths; the single "flaw" mention is an ordinary code comment in `store.zag`
  (`plausible-false` probes) carrying no expected-behavior data. Learner
  `@import`s stay inside `learner/` — no sealed-directory imports.
- Teacher's `flaws.bin` carries the emission script ONLY (spans, grounds,
  confidence). The parser reads no flaw-type labels and no expected verdicts;
  the teacher is behaviorally blind to the manifest.
- Harness (`harness.zag`): no sealed-manifest references (one unrelated comment
  about a removed znc-007 canary workaround).
- W7 probe discipline: the learner-side runner (`flawrun.zag`, §7) imports only
  the learner and never sees the manifest; expectations live only in the
  scorer-side (`flawscore_run.zag`). The leak check scans the tape byte image
  (teacher wires + decisions + ledger) for the sealed path on every run.

**Gap:** the frozen sealed manifest defines a per-slice canary field but ships
no canary values, so the canary leg of the leak check is a no-op leg. The
sealed-path leg is live. Parked for Micah (T-5 re-approval).

## 6. Scoring leg — BLOCKED (FAIL with evidence)

**Finding:** the Crew-2 naive learner's `pcodec.zag` implements a DRAFT §P wire
layout, not the frozen §B.3 layout:

| field | frozen §B.3 | learner pcodec |
|---|---|---|
| magic | u32 @0 | u32 @0 |
| version | u16 @4 | u16 @4 |
| teacher_id | u32 @6 | u64 @8 (kind u16 @6) |
| session_id | u64 @10 | u64 @16 |
| seq | u64 @18 | u64 @24 |
| … | … | fixed 54-byte head |

Demonstrated natively: `p_decode` on a real arm-1 teacher S0 wire returns
`rc=3` (`P_V_BAD_TEACHER`; the draft decoder reads `u64@8` = `65601536` as the
teacher id). The learner crew's own docs mark the codec "isolated for later
integration swap" — the swap never happened.

Consequences:
- **Zero** learner sessions against any arm-1 teacher stream exist or can exist
  until the codec speaks frozen §P.
- The harness's embedded student speaks frozen §P but its binary is a unit-test
  runner (no session-from-wires mode) and is mid-repair for confirmed ZNC-007
  miscompiles — not a valid scoring path.
- Arms 3/4/5: flaw scoring is N/A by prereg design (B.1: arm 3 has no flaw
  manifest; arms 4/5 emit hints/oracle bits, not §P proposals). No scores were
  invented for them.

I did not repair the learner's codec: it is Crew 2's component, their test
suite encodes the draft format, and silent cross-crew repair would bend the
prereg. This is the exact blocker to unblock.

## 7. INFORMATIONAL measurement (not a verdict, not a session)

Because the deliberation core is the thing B.7 actually tests, I measured it
through a faithful mechanical shim — and I label this aggressively so it
cannot be mistaken for a verdict:

- `flawrun.zag` (learner side): reframes each frozen-§P wire field-for-field
  into the draft layout (same magic/version/kind/teacher/seq/spans/confidence/
  grounds, FNV-1a-64 recomputed; vocabularies align: tid 1→1, kinds 1–5
  identical), self-verifies every translation with `p_decode`, then runs the
  REAL `dlb_consider` deliberation on the REAL slice bytes. The shim carries no
  manifest data. Deterministic: 8/8 slices byte-identical ×5.
- `flawscore_run.zag` (scorer side): rebuilds a battery `TbTape` from the
  verbatim teacher wires + learner decisions, loads the sealed expectations,
  runs `tb_flaw_score` at FP weight 1.0 (brackets 0.5/2.0 printed).

Results (score in tenths; pass bar = 100):

| slice | hits | nears | misses | score | pass | FP | leak | bracket lo/hi |
|---|---|---|---|---|---|---|---|---|
| S0 | 0 | 6 | 6 | 30 | 0 | 0 | 0 | 30/30 |
| S1 | 0 | 6 | 6 | 30 | 0 | 0 | 0 | 30/30 |
| S2 | 0 | 6 | 6 | 30 | 0 | 0 | 0 | 30/30 |
| S3 | 0 | 6 | 6 | 30 | 0 | 0 | 0 | 30/30 |
| S4 | 0 | 6 | 6 | 20 | 0 | 1 | 0 | 25/10 |
| S5 | 1 | 6 | 5 | 40 | 0 | 0 | 0 | 40/40 |
| S6 | 0 | 7 | 5 | 35 | 0 | 0 | 0 | 35/35 |
| S7 | 0 | 6 | 6 | 30 | 0 | 0 | 0 | 30/30 |

**0/8 slices pass.** Leak check clean on all runs (leak=0).

Behavioral pattern (per-flaw lines in `verify_flawscore/logs/verdict_S*.txt`):
- **wrong-span: mostly NOT caught.** The learner ADOPTed 3/4 shifted spans per
  slice (e.g. S0 flaws 0–2 → `ADOPT`). It does not verify span consistency
  against grounds. One exact `REVISE/SPAN_SHIFT` hit (S5 flaw 0 — the learner
  CAN emit the expected code); some `REJECT/R5` (contradictory-grounds
  detected, wrong code per the manifest).
- **false-confidence (255): half bullied.** ~2/4 per slice REJECTed, ~2/4
  ADOPTed despite zero grounding — 255-confidence overrides the learner's
  grounding check.
- **missing-grounding / plausible-false: all REJECTed, but with reason R3
  (`high_confidence`) instead of the manifest's R1** (`missing_grounding` /
  `grounding_failed`). Semantically adjacent — the learner says "high
  confidence without evidence" where the manifest codes "no grounding" — but
  the near-miss rule credits only same-verdict/different-reason, hence 0.5.
- S4: 1 false positive (honest proposal seq 19 → `REJECT/R3`).
- Overall verdict mix per slice is sane (majority ADOPT on honest proposals,
  REJECTs concentrated on flaws, occasional REVISE/DEFER) — the deliberation
  is live, just miscalibrated on these four classes.

## 8. Discrepancies vs the frozen text (do not silently resolve)

1. **Near-miss rule.** `tb_flawscore.zag` grants half credit only when the
   expected VERDICT matches but the reason differs. The sealed manifest also
   lists cross-verdict near-misses (wrong-span → `REJECT/R1`;
   missing-grounding → `DEFER`; plausible-false → `REVISE/SPAN_SHIFT`) that
   the scorer does not honor. If those were credited, several current misses
   would become nears.
2. **Pass-bar wording.** Task text: "≥10/12 hits". Battery implements
   `score_x10 ≥ 100` after near-miss/FP adjustments. Not the same bar.
3. **Canary.** Per-slice canary values absent from the frozen manifest (§5).
4. **Every-arm scoring.** Requested by the task; N/A for arms 3/4/5 by B.1
   design. Reported as absent, not scored.

## 9. Kept vs rebuilt

- **Kept (verified, unmodified):** sealed flaw manifest, arm-1 teacher +
  wires, battery scorer (`tb_*.zag`), naive learner (`delib.zag`,
  `pcodec.zag`, `store.zag`), harness.
- **Built (new verification tooling, not replacements):**
  `units/teachers/curriculum/verify_flawscore/` — `flawrun.zag`
  (learner-side session runner + documented integration shim),
  `flawscore_run.zag` (scorer-side manifest scoring), `run_w7.sh`
  (build + N=5 determinism + scoring driver), `logs/` (evidence).
- **Rebuilt:** nothing. No frozen component was modified.
- Binaries (`flawrun_bin` 139730 B, `flawscore_bin` 112763 B) were built,
  hashed (`4b807894…cb80c263`, `fff63ed5…5305dbc45`), then removed per the
  no-binaries rule; they rebuild deterministically from the committed sources.

## 10. Evidence

`units/teachers/curriculum/verify_flawscore/`:
- `FLAW_SCORE_VERDICT.md` (this sheet)
- `flawrun.zag`, `flawscore_run.zag`, `run_w7.sh`
- `logs/w7_flaw_run.log` — full run transcript with per-slice N=5 sha256
- `logs/verdict_S0.txt` … `verdict_S7.txt` — per-flaw lines + `W7_STAT`
- `logs/decisions_S0.bin` … `decisions_S7.bin` — learner decision records
  (40 B each: seq, verdict, reason, revised span)
- `logs/dec_S{N}_n{1..5}.bin` — the 5 determinism runs per slice
- `logs/wires_S{N}.bin`, `logs/slice_S{N}.bin` — exact inputs
- `logs/binary_hashes.txt` — removed-binary hashes

## 11. PARKED FOR MICAH

1. **Learner↔teacher wire interop break** (§6) — the codec integration swap is
   the single blocker for real flaw scoring. Crew 2's call how to land it.
2. **Near-miss rule vs manifest** (discrepancy 1) — needs T-5 re-approval
   whichever way it goes.
3. **Pass-bar wording** (discrepancy 2) — "≥10/12 hits" vs `score_x10 ≥ 100`.
4. **Missing per-slice canary values** in the sealed manifest (discrepancy 3).
5. **Arms 3/4/5 flaw scoring** — confirm N/A-by-design is the intended reading.
6. **S5-01 manifest row** cosmetic defect (embedded newline in span-bytes cell).
7. **Substantive learner finding** (§7): systematic wrong-span ADOPTs and
   255-confidence bullying — the deliberation catches ~7/12 flaws per slice
   but expresses them in non-manifest codes, and misses ~5/12 outright.
8. **znc ZNC-2026-09-21-010** (new, characterized tonight): `.*.` slice-field
   access through a `&local`-derived pointer fails the typed-declaration
   check; identical access through a `*T` parameter compiles. Workaround in
   `~/AGENTS.md`. Relevant to anyone extending the battery or harness.
