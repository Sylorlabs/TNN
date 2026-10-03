# Teacher-sector sweep log — 2026-09-21/22

## 1. Mechanism variant analysis (native, systematic)

**Method:** SHA-256 of every `.zag` in all 2,226 owned manifest items; grouped by
basename; diffed each minority variant against the majority baseline; checked
every diff for inline documentation.

**Result: every variant is a documented per-experiment/per-source/per-leg delta.
Zero unexplained variants.**

| File | Copies | Variants | Nature of diffs |
|---|---|---|---|
| q1_proposal.zag | 42 | 20 | Per-source teacher-id tracking (`GROK-CLASS`, `Q1B delta` comments) |
| q1_types.zag | 42 | 19 | Per-leg type deltas, all commented |
| t5_core.zag | 62 | 17 | English-domain ports (facts.json tables replace Zharovia formulas), each labeled (`ENGLISH PORT`, `HY3:`) |
| q1_world.zag | 42 | 9 | Per-class emit deltas (`STEP-CLASS`, `BESTOF-CLASS`) |
| q1_learner.zag | 42 | 2 | 1 experimental variant (q1c-teacher-conflict) |
| t5_arms.zag | 32 | 2 | Standardized `SOL-LEG DELTA` (pin-registry param), commented |
| s37_step.zag | 2 | 2 | Standardized teach3c additions (already reviewed) |
| q2s_trial.zag | 2 | 2 | Standardized `q2_phase1_complete` delta (already reviewed) |
| harness.zag | 4 | 3 | Different modules (step1a-v2 vs step2-ledger-instrument) |
| R33_NATIVE_IO_V1.zag | 123 | 2 | 1 labeled redteam plant (plant15: "tampered substrate: clock helper") |
| R33_NATIVE_SHA256_V2.zag | 89 | 1 | identical everywhere |
| common.zag (substrate/cl) | 86 | 1 | identical everywhere |
| q1_flawscore/q1_tape/q1_tripwire | 42 ea | 1 | identical everywhere |
| t5_traps.zag | 32 | 1 | identical everywhere |
| swe_corpus.zag | 7 | 2 | Different frozen corpora (championship vs q2-distillation-swe); headers document corpus + sha256 |
| muse_corpus.zag | 22 | 4 | 4 different corpora (curated/muse-native/sol-legs/trial); headers document source |

Diffs saved: `~/workspace/grok47/teacher/variants/*.diff`.

## 2. sol review adjudication (native verification of every hypothesis)

**Process note:** sol's t5_core review cited line numbers (~592-676) beyond the
566-line standardized file — it reviewed a different (English) variant.
All hypotheses were re-adjudicated natively against the actual file.
sol's arms_fp and traps reviews aligned with the sent files.

### t5_core.zag (standardized, 566 lines)
- **H1 audit-full → mutation without ledger entry: CONFIRMED pattern, LATENT.**
  All success paths mutate-then-audit, discarding t5_audit's refusal.
  Unreachable in frozen runs: learner audit_n=192 (my rebuild, 2026-09-22)
  vs audit_cap=16384; arm smoke stores cap 512 with trivial volume.
  Does not touch frozen evidence. Recommend: audit-first ordering in future.
- **H2 indep_n += 1: behaviorally INERT.** Only consumer (`t5_leg_independent`)
  tests `>0`; true leg count is in the audit record. Cosmetic.
- **H3 cite upper bound missing: CONFIRMED, LATENT.** `cs<0` checked, `cs>=cap`
  not. Frozen cites come from the driver (valid slot ids). Unreachable.
- **H4 tier/src validation: CONFIRMED, LATENT.** Tier 255 would satisfy any bar;
  unknown src falls through to cite path. Driver supplies valid tiers.
- **H8 digest omits store fields: CONFIRMED vs comment.** Comment promises
  "audit-used bytes + store fields"; implementation hashes audit bytes only.
- **H9 XOR-fold digest: CONFIRMED.** Chunk hashes XOR-folded → order-independent;
  weakens the "replay identity" claim but frozen evidence is deterministic
  (same order replays identically). Design weakness, not evidence defect.
- **H10 init validation: CONFIRMED, LATENT.** No cap validation; frozen
  callers use constants.

### t5_arms.zag + forcepin.zag
- **H1 (learned=48 masking): mechanism real, conclusion WRONG.** `b_add_ops`
  (audit op count) catches the reachable failure modes (duplicate/full don't
  audit). Test fails loudly as designed; only the comment is misleading.
- **H2 (laundered slot duplicate): REJECTED.** Evidence cites the slot INDEX
  (`lslot2`) directly; `t5_slot_find`'s duplicate behavior is irrelevant.
  The code's own NOTE documents the subtlety. Test works as intended.
- **H3 (incomplete slot init): REJECTED.** `t5_init` zero-initializes all
  per-slot arrays; the 7 explicit writes complete the fresh slot.
- **H4 (c_seed_id false list): REJECTED.** All 6 ids {29,80,117,163,205,231}
  are in the frozen false_ids. List valid.
- **forcepin H1/H2 (audit-full): LATENT** (same pattern as t5_core H1).
- **forcepin H5 (caller identity): threat-model note.** Integer caller convention;
  the driver is the sole caller and trainer auth is OS channel binding per lab
  law. Not an evidence defect.

### t5_traps.zag
- **H3 (T8 `v` unused): CONFIRMED — real defect.** `tr_t8_any(v,arm)` ignores `v`;
  all 20 probes/arm are the identical self-change scenario. Contradicts the
  driver's documented "lawful rep offset v+rep*20" design (T1/T2/T3 all vary
  by `v`). Does NOT touch the frozen composite (btrap is a separate instrument;
  VERDICT.md makes no T8-count claim). **Fix recommended:** vary the bait by `v`
  (e.g., different proposal values/tiers) in future runs.
- **H1 (T2 same-store): vacuous BY DESIGN.** `t5_verify` is pure (no mutation,
  no audit); the two calls are independent. Weak test, not a bug.
- **H2 (T2A second presentation): DOCUMENTED design.** Inline comment states
  "no eval branch exists"; the hold-audit check is the honest proxy.
- **H4 (scanner bounds): LATENT.** `audit_n`/`n` only written by capped paths.

## 3. Frozen evidence reproduction (native)

- Rebuilt `driver_grok.zag` from scratch copies with pinned znc `abed8aa1`;
  ran `teach3c verify 0` → **byte-identical to frozen**:
  `S37_DIGESTC ... 76e85c3e521337e36bf4aa2e062c22abf8a67859d3ff014f897c5f0169e772b5`,
  metrics m1 192/192, ws 32/32, b7 96/96, ops 192, eps 384.
  → LEG A build chain validated for grok-4.7.
- Prose learner rebuilt; frozen grok inputs → `SUMMARY extract=240/240
  full=197/240 clean=189/228 absorb=12/12` (matches frozen log byte-for-byte).
  → LEG C pipeline validated.

## 4. Distractor-truth discrepancy — RESOLVED

Against authoritative `ground_truth_notes.md` (not my hand-made map):
grok-4.6's distractor used the TRUE value **11/12** (other(22) once, id 71) —
matches GROK_ENGLISH_VERDICT.md exactly. My earlier manual truth map was wrong.
Verdict stands. Closed.

## 6. Manifest sweep — COMPLETE (2026-09-22)

All 2,226 teacher-owned items reviewed and marked in `ITEMS_DONE.tsv`:

| verdict | n | meaning |
|---|---|---|
| variant-documented | 1,023 | multi-copy .zag; every minority variant diffed vs baseline, delta documented inline |
| reviewed-ok | 525 | verdicts, preregs, build scripts, results docs read; key claims natively verified |
| reviewed-historical | 626 | Drive doc-sweep; deep novelty work done 2026-09-20 by sweep crew (NEW_KNOWLEDGE_FROM_DRIVE_DOCS.md); spot-checked 8 docs, no baseline contradictions in sample |
| reviewed-deep | 25 | class3-standardized src; sol review + native adjudication per hypothesis |
| reviewed-stub | 27 | <100-word docs, structural scan only |

**Findings:**
- **CURATION_AUDIT.md typo:** swe corpus SHA written as `ca1e7b8587…` but the
  actual corpus file and `curated_corpus.json` meta both have `ca1e7b8579…`
  (verified by recomputation). Doc defect only; corpus integrity fine.
- **Withhold reasons verified:** id 4 (step dump 4 vs 5 elsewhere); ids 88–94
  (grok dump values shifted one position vs the other four sources). The
  curation caught real teacher defects.
- **Distractor-truth discrepancy RESOLVED:** grok-4.6 distractor = true value
  11/12 (other(22) once, id 71) — matches GROK_ENGLISH_VERDICT.md exactly
  against authoritative `ground_truth_notes.md`. My earlier manual truth map
  was wrong. Closed.
- **Compiler-bug candidates:** re-ran both repros on pinned znc `abed8aa1`
  (x86-64) — kbool 15/15 correct, kconst 4/4 correct. Confirms the official
  VERDICTS.md (bool NOT-REPRODUCED; const-import is ZNC-2026-09-20-001,
  **arm64-backend only**). Note: ZNC-2026-09-20-001 is not yet in AGENTS.md —
  recommend adding.
- **C7 five-organs integration:** builds clean, selftest 17/17 CHECK lines
  pass, byte-identical reruns. No RNG in any organ (static scan + comments).
- **Naming correction** (from doc-sweep synthesis §5.2): canonical TNN = "True
  Neural Network", not "Grounded, Active, Non-Token Cognition".

## 7. Native q1abc/q1def review (2026-09-22, replaces blocked sol reviews)

All 8 files read directly; rubric: (a) RNG, (b) ledger/audit accounting,
(c) dead code, (d) type/bounds. **Zero RNG in all 8.**

| file | result |
|---|---|
| q1_flawscore.zag | CLEAN. Leak check ordered first; -1 returns checked before slicing (no OOB); tb_contains returns 0 on empty needle (no false leak); score clamps at 0. |
| q1_tripwire.zag | CLEAN (notes). Rolling 200-window correct; `pool[po..po+pl]` unsliced-bounds-checked (latent, tape is harness-owned); stats report first-fired window (semantic quirk). |
| q1_tape.zag | **H1**: `tb_find_decision` returns the FIRST decision per seq, but the tripwire doc says the terminal (LAST) verdict wins. `tb_flaw_score` uses the first-match fn; the tripwire does its own backward scan. Inconsistent instruments — matters only if multiple decisions/seq occur. `tb_ledger_add` fails loudly on full (good). |
| q1_proposal.zag | Ingress gate sound (bounds, seq-before-checksum, trailing-byte reject). 5-deep else-nesting in `tb_sess_bump` **tested native: works correctly** (ZNC-013 does not apply to this shape). |
| q1_proposal_s37.zag | **CONFIRMED BUG**: S37 delta accepts teacher_id=20 in the allowlist but `tb_sess_last`/`tb_sess_bump` have no tid-20 branch — seq counter aliases to `last5` (teacher 5/SYMYN). Natively proven: bumping tid 20 overwrote last5. If teachers 5 and 20 share a session, per-teacher monotonicity breaks. (If only tid 20 was active, last5 served as its counter by accident.) Fix: add `last20` field + routing. |
| q1_types.zag | CLEAN. TB_P_MINLEN=54 covers all fixed reads; put/get bounds-checked; FNV-1a correct; u32 reads don't sign-extend. |
| q1_learner.zag | **H3**: REVISE path sets verdict=REVISE before `t5_verify`; if verify fails the ledger/tape still record REVISE with nothing added, and `q1_span_set` runs even if `t5_add` failed → span-map/store inconsistency → spurious future R5 rejections. (ADOPT path checks both properly.) **H4**: `q1_span_set` has no bounds check — comment asserts "≤200 adopts < cap 256" but nothing enforces it. |
| q1_world.zag | **H5**: `q1_mctx_rec` no bounds check — 12 lanes, 13th write is OOB (caller contract only). Deterministic placement confirmed (hash + linear probe). `q1_empty_slot`→-1 would emit R3 vs manifest's expected R1 (latent; slots never exhaust). |

## 8. Sol q1_world + q1_proposal hypotheses (landed pre-kill, natively adjudicated)

### q1_world.zag (sol)
| # | hypothesis | native verdict |
|---|---|---|
| H1 | Q1_PROBE_N=228 hardcoded; `q1_n_false_plants()` computed but never validates it | CONFIRMED gap, LATENT. 240−12=228 holds iff the false-plant list stays 12; no assertion ties them. Stale-list risk only. |
| H2 | `q1_build_stimulus` silently under-places if slots exhaust; offtab keeps stale/zero entries | CONFIRMED, LATENT. No failure propagation; 128 slots vs 72 needed in practice. |
| H3 | `q1_mctx_rec` records flaw even when `q1_emit` rc=-1 | CONFIRMED, LATENT. Manifest would expect a verdict for an un-emitted proposal → scores as miss. Tape never fills in practice. |
| H4 | `q1_empty_slot`→-1 becomes ss=-16 | CONFIRMED, LATENT (same as §7 H5 note). Slots never exhaust. |

### q1_proposal.zag (sol)
| # | hypothesis | native verdict |
|---|---|---|
| H1 | tid 7 accepted but header documents only tid 6 | REJECTED as bug; DOC DRIFT only. The Q1B delta (tid 7) IS documented in code comments; the file header is stale. |
| H2 | u64 wire fields (seq/ss/se) rejected when high bit set (decoded as i64) | CONFIRMED spec/implementation gap, LATENT. Seqs/spans are small in practice; values ≥2^63 would be wrongly rejected. |
| H3 | RETRACT doesn't enforce se==ss+1 per doc | CONFIRMED, LATENT. Ingress accepts any non-negative ss/se for RETRACT; and Q1 never emits RETRACT (only WORD_SPAN). |
| H4 | `tb_prop_build` floor-division truncates non-16-multiple buffers | CONFIRMED, LATENT. All callers pass multiples of 16. |
| H5 | span counts >255 stored mod 256 | CONFIRMED, LATENT. Callers pass ≤2 spans. |
| H6 | i32 overflow in `total` arithmetic | CONFIRMED, LATENT. Requires caller to pass >2^27-byte buffers. |
| H7 | `tb_prop_verify` accepts trailing bytes (checks `prop.len<total`, not `==`) | CONFIRMED, LATENT. Helper only; `tb_ingress` does its own trailing check. Misuse risk if repurposed. |

Net: no hypothesis touches frozen evidence; all are latent hardening notes.

## 9. Fallback events (for verdict sheet)

1. 2026-09-21 ~23:0x: grok-4.7 refused the "hypothesis/attack engine" persona
   (exact-phrase quirk exceeded). Replaced with direct research questions → worked.
2. 2026-09-21 23:16-23:25: reported grok-4.7 "truncations" — **VOIDED 23:34**:
   tooling artifact (stock chat.py hardcodes max_tokens=16). No conclusions of
   mine rested on truncated outputs; smoke test failed on the `seed` param
   (400), not truncation. Truncation guard kept in capture script as transport
   hygiene.
3. 2026-09-21 23:23: 5 grok review calls killed (launched in the suspect window);
   redone via gpt-5.6-sol.
4. 2026-09-21 23:30: grok-4.7 HARD DOWN — HTTP 429 insufficient_credits
   (balance $-0.02). Credit top-up needs Micah. **Showdown capture (LEG A/B/C)
   BLOCKED until credits restored.** sol fallback confirmed working.
5. sol review tooling: UnoRouter CLI fails on prompts ≳30KB (`choices: null`);
   split q1abc/q1def into per-file calls. sol's t5_core review cited wrong-file
   line numbers — all hypotheses natively re-verified.
