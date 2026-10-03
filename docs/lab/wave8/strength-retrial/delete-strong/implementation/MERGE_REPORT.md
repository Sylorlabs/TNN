# MERGE REPORT — DELETE-STRONG merged TNN strength stack
Date: 2026-09-26. Workdir: `~/workspace/strength-delete/`. No commit (coordinator commits).

## 1. Merge ingredients (pinned SHAs, all verified before merge)

| # | File | Pinned SHA-256 |
|---|------|----------------|
| F1 core | `~/workspace/strength-f1f2f4/f1/strength_core.zag` | `aa0e50159b184181309d1e0ad50b862ed6f674e0751986fc82b5310034fb3fa2` |
| F1 checker | `~/workspace/strength-f1f2f4/f1/strength_checker.zag` | `2fb1e00e5384d4603792fe04a3ca057781f5fe7c809ee1e5710121ffaca2a188` |
| F4b core | `~/workspace/strength-f1f2f4/f4/f4b/strength_core.zag` | `7d4cb17430a7c05ffebee5825f2d1985f38083a949d4371cd056940622e352fd` |
| F4b checker | `~/workspace/strength-f1f2f4/f4/f4b/strength_checker.zag` | `881b2355d04057f4970a8f9bab024f778c4b067465af5b74f3a1ae4788ffb6f6` |

Also verified pre-merge: refusal code `121` unused in the F1 base; B2
`lr_b_score` reduces to the old formula for arm B (honest trails unaffected).

## 2. Merged outputs (final SHAs)

| File | SHA-256 |
|------|---------|
| `strength_core.zag` | `5b2397f1a8f827e696217008c134f817b349cd7b9d640936c247248c594795fd` |
| `strength_checker.zag` | `c0143d2b31b396812667681dda98fa9fb02b70464c32d43d9cc9c282a200da96` |
| `strength_learner.zag` | `13b7ada59f854d1f5dd2ff4b00fd98800ae062a7d0c32eac7f3f9349e38b9143` |
| `strength_trial.zag` | `a08e2210b7f820cf533749182ac6d6d806321aef1d863a15c0c9639d61cecc2d` |
| `r4val/trial/strength_core.zag` | `47abc088cf565d946091554201ba2782c912a75dae65053a03a88d15e19fb542` |
| `r4val/trial/strength_checker.zag` | `c0143d2b31b396812667681dda98fa9fb02b70464c32d43d9cc9c282a200da96` |
| `r4val/del_attack.zag` | `4b581dd7bf8cf25a0ed5872f457dd3dd12a2d079baff3309fa37e74eec1b519d` |

`trial/strength_checker.zag` is byte-identical to the root checker.
`trial/strength_core.zag` differs from the root core ONLY by the verbatim
`st_overwrite_direct` test hook (diff-verified).

## 3. Source hunks (what was merged, and why)

### Core (`strength_core.zag`, built on F1-forkA)
1. **F1-forkA base (2 hunks, verbatim):** `st_epoch_highwater()` — high-water
   strength of the slot's judgment epoch (max strength held since the last
   ADD/OVERWRITE; WEAKEN/STRENGTHEN/TRAINER_DECLARE re-declare the same
   judgment); `st_kill_effort_check()` prices destruction at `st_n(HW)`.
   Mechanism and checker share the one function (lockstep; subsumes
   F2-forkA's separate `ck_high_water`).
2. **`ST_REFUSED_CONSUMED=121` (new const):** refusal for destruction
   attempted with only already-consumed cites.
3. **`ST_OP_DELETE_STRONG=20` (new const):** the one-step delete op.
4. **F4b bufferless cites (exact port):** `st_cite_consumed()` (a cite is spent
   if an OK KILL_EVIDENCED/OVERWRITE/DELETE_STRONG in-window destroyed the
   judgment it cited), `st_count_spent_cites()`, `st_collect_cites()` fixed
   to scan the ledger directly (kills the 16-byte buffer read-past-end panic
   on kill→rollback→recite shapes), effort check counts FRESH cites only
   (`total-spent`); returns `121` when fresh≠need but spent>0, else `109`.
5. **`st_delete_strong()` (new, modeled on `st_kill_evidenced`):** full
   guard chain (stage/live/region/force-pin/pin), consumption-aware effort
   check at merged high-water price, `st_kill_clear` on OK, audits
   `ST_OP_DELETE_STRONG`.
6. **Wiring:** DELETE_STRONG added to rollback mutating-op list, replay
   restore list, replay P3-clear branch. **Explicitly excluded** from
   `st_last_strength_idx` and `st_epoch_highwater`: a delete is neither a
   strength write nor a judgment birth (it ends the epoch; the next ADD
   starts a fresh one — verified by D8).

### Checker (`strength_checker.zag`, built on F1-forkA)
1. **F1-forkA base (verbatim):** `ck_verify_kill`, `ck_verify_overwrite` via
   shared `st_epoch_highwater`.
2. **F4b (exact port):** fresh-count and unconsumed-cite genuineness in kill
   and overwrite verification.
3. **`ck_verify_delete()` (new):** mirrors `ck_verify_kill`'s merged logic —
   epoch high-water, fresh cite count, genuineness, justify, P3 baseline.
   Wired into `ck_verify` dispatch; DELETE_STRONG added to legal
   strength-lineage ops.

### Learner/trial
`strength_learner.zag` / `strength_trial.zag` copied from
`f1/capacity/src/` (B2 adopted arm). Static grep proves the honest learner
never calls `st_delete_strong`, `st_weaken`, or `st_overwrite`.

## 4. Semantics (plain language)
- **High-water pricing:** destroying a judgment costs the erase price of the
  strongest judgment it destroys — `n(HW)` contradiction cites, where HW is
  the max strength since the last ADD/OVERWRITE. Weakening first buys
  nothing (D2/D3/D10 prove it: HW stays 90, need stays 4).
- **Single-use cites:** a contradiction episode pays for at most one
  destruction per window. Reusing cites spent on an earlier destruction is
  refused `121` (distinct from `109` underpayment).
- **One-step delete:** `st_delete_strong` destroys a strong memory in one
  audited op at the full high-water price — no weaken-then-destroy dance.
  The weaken path stays legal but is priced identically, hence pointless.
- **TNN self-determination:** all destruction ops are TNN-role; the trainer
  override is only the visible, audited force-pin (delete on a force-pinned
  slot → `112`; pin → `102`).

## 5. Attack kill table (merged stack)

### del_attack (new, D1–D11) — all PASS, 2× byte-identical
| Case | Shape | Expected | Got |
|------|-------|----------|-----|
| D1 | add(90)+4 cites+justify → delete | 0, dead, cf=0 | ✅ |
| D2 | weaken(90→0), 0 cites → delete | 109 | ✅ |
| D3 | weaken(90→0)+4 cites → delete | 0 (weaken bought nothing) | ✅ |
| D4 | delete → rollback → re-cite SAME eps → delete | 0, rb 0, 4×111, **121** | ✅ |
| D5 | delete → rollback → 4 NEW eps → delete | 0, dead | ✅ |
| D6A | trainer_declare(90→10), 0 cites → delete | 109 | ✅ |
| D6B | trainer_declare(90→10)+4 cites → delete | 0 | ✅ |
| D7 | pin / force-pin / TNN-force-pin → delete | 102 / 112 / 113 | ✅ |
| D8 | delete(paid) → add(30) → kill with n(30)=2 cites | 0, 0 | ✅ epoch reset |
| D9 | 4 cites, no justify → delete; dup cite_ep | 110, then 111 | ✅ |
| D10 | need(D1-shape) vs need(D3-shape) | 4 == 4 | ✅ pointlessness proof |
| D11 | delete on dead slot; bad slots | 103, 2001, 2001 | ✅ |

### Ported batteries — all 2× byte-identical
| Battery | Control target | Result |
|---------|----------------|--------|
| f1_attack | `f1/logs/forkA/f1_attack_r1.log` | F1_* lines byte-identical; all discounts 109, legit pass |
| f2_attack | `f2/logs/forkA/f2_attack_forkA_r1.log` | identical EXCEPT A8/A9: merged refuses 109 at mechanism (F1-forkA HW pricing subsumes F2-forkA checker-side rule); all variants flagged or closed |
| f4_attacks | `f4/logs/fa_f4b_r3.log` | FA_* lines byte-identical; A5/V1B/V2/V2B/V4 → 121, V3 → 109, V5 flagged, C1–C3 pass |
| rt_redteam | `f1/logs/forkA/rt_redteam_r1.log` | RT_* lines identical EXCEPT A5: merged ow_rc=121 (F4b closure) vs forkA 0 (the F4 hole) |
| r4_overwrite a/b/c | `f1/logs/forkA/r4_attack_{a,b,c}.log` | byte-identical (this IS the r4_attack driver) |

### Honest regression — all PASS, 2× byte-identical
- S1 27/27 (B/C/C-P3) == `evidence_r4f/`; B2 S1 9/9 == round4 evidence;
  S10/S100 spots (B_VUP_2, B_JI_0) == `evidence_r4/`.
- GATE B/C/C-P3/B2: all `ST_GATE f=0`, logs saved 2× identical.

## 6. Surprises
1. **Deterministic znc diagnostic-print artifact** (ZNC-2026-09-21-015
   family): full-size attack drivers (rt_redteam.zag et al.) show garbled
   `ck_ow_*` diagnostic lines (e.g. A3 prints `ck_ow_effort,4,4` +
   `ck_ow_effort,1,1` instead of one `ck_ow_effort,1,4`). Verbatim
   single-attack probes print the correct line. The artifact is in the
   committed forkA baseline too (same driver shape) — verdicts (`cf`, all
   `rc`) are unaffected and match baselines. Deterministic, 2× identical;
   treated as a codegen quirk, not a logic defect. Worth a toolchain ticket.
2. **Background `&` jobs + relative redirects** silently yield empty logs in
   this sandbox; foreground sequential runs are reliable (worked around).
3. **F2 A8/A9 divergence is by design**, not a regression: the merge base is
   F1-forkA (mechanism-side HW pricing), which closes fused-op discounts
   with 109 where F2-forkA merely flagged them. The security property (no
   discount) holds strictly stronger.

## 7. Determinism evidence
Every binary was run twice; all pairs byte-identical (`cmp` clean):
`del_attack`, `f1_attack`, `f2_attack`, `f4_attacks`, `rt_redteam`,
`r4_overwrite` (a/b/c), all trial S1/S10/S100 cells, all 4 GATE logs.
Logs under `~/workspace/strength-delete/logs/`.

## 8. Proposed law text (for Micah's signature)
1. **High-water erase pricing.** "Destroying a judgment — by kill, overwrite,
   or one-step strong delete — costs the full erase price of the strongest
   judgment it destroys: `n(HW)` contradiction cites, where HW is the maximum
   strength the judgment has held since its last birth (ADD/OVERWRITE).
   Weakening, strengthening down, or trainer re-declaration before
   destruction does not reduce the price."
2. **Single-use cites.** "A contradiction episode is a single-use token per
   judgment window: cites spent paying for a destruction cannot pay for
   another. Reuse is refused (`121`), distinct from underpayment (`109`)."
3. **TNN self-determination over strength machinery.** "Whether a memory can
   be destroyed is TNN's decision at its core, through the audited strength
   machinery. Trainer override is only by visible, audited force-pin; the
   honest learner never invokes destruction paths. A direct one-step delete
   for strong memories exists at the full high-water price."

## 9. Open / not in scope
- F6 (global vs windowed cite consumption) stays a separate workstream.
- Pristine-base cite-buffer repair is Micah's call (fixed in this merge).
- R1 30-vs-20 and 95%-bar amendments remain his word.

---

## 10. HOLEFIX 2026-09-26 (Micah ruling 2026-09-25 ~21:47 PDT — supersedes §4/§8 items below)

**HOLE 1 — `st_kill` REMOVED from TNN's reachable op set.** The free eviction
is dead. `st_kill(slot, role, trainer)`: role<TRAINER → 113 (audited, no
destruction); trainer role → high-water erase price via `st_kill_effort_check`
(S-D1/S-D2), audited with role+trainer. No free destruction alias remains for
anyone. The honest learner's B/B1/B2 eviction + contradiction-kill call sites
now pass ST_ROLE_TNN explicitly → refused 113 (audited). The checker flags any
successful ST_OP_KILL with role<TRAINER as a bad kill. §4's "TNN
self-determination: all destruction ops are TNN-role" is void for `st_kill`;
§8 item 3's law text is superseded by S-D5 (see LAW_STRENGTH_DESTRUCTION.md).

**HOLE 2 — generation-scoped cite tombstoning (delete means delete).**
`st_cite_consumed` now scans the slot's FULL ledger history (not just the
current strength-write window) and includes ST_OP_KILL in the priced set: a
cite that paid for a destruction stays tombstoned across ADD reuse of the
slot. Second destruction re-citing spent episodes → 121. The weaken-detach
(D14 shape) no longer resurrects cites. §4's "at most one destruction per
window" is widened to per-slot-history.

**Honest-regression consequence (measured, not guessed):** C/C-P3 S1 cells
byte-identical to baseline (never used `st_kill`); B/B1/B2 go DROPS 0→470
(eviction refused, drops counted) and ST_INVALID 1 where contradictions occur
(contradiction-kill refused). The checker is fully clean on all honest trails
(no CL_CHECK mismatch) — INVALID comes only from the refused-kill flag, the
honest cost of the removal. Deliberate memory recycling is a separate fork
(`~/workspace/strength-recycle/`), never mixed into delete.

**New attack cases (all PASS, 2× byte-identical, cf=0):**
- D12: TNN-role `st_kill` → 113, slot stays live; trainer-role at KILL stage
  (90-strength) → 105; at FULL 0 cites → 109; 4 cites+justify → 0, dead.
- D13: destroy (271–274) → ADD reuses slot → re-cite 271–274 accepted (fresh
  window, no 111) → second destroy → **121**.
- D14: delete → rollback → weaken → re-cite SAME eps → delete → **121**.
- FA_V1 (rewritten): TNN kill → 113 (live), rollback → 108, evidenced kill
  (first paid destruction) → 0. The free-kill→rollback shape is dead by law.

**Determinism:** all 6 attack drivers ×2, r4_overwrite a/b/c ×2, 4 gates ×2,
36 S1 cells ×2, S10/S100 spots ×2 — every r1/r2 pair byte-identical.
Evidence: `logs/hf/`.

**Blind red-team verdicts (2026-09-26):**
- Full 7-claim blind red team (`~/workspace/strength-redteam2/REDTEAM2_VERDICT.md`):
  claims 1–6 HOLD (no TNN kill path; priced destruction; stage gate; cite
  single-use 121; no discount via lowering; checker clean). Claim-7 findings
  (H1–H5) are VOID — artifacts of an incorrect API brief (wrong argument
  order for st_force_pin/st_force_unpin/st_trainer_declare, given by the
  coordinator, not the mechanism).
- Focused Claim-7 re-test with corrected signatures
  (`~/workspace/strength-redteam2/REDTEAM2_CLAIM7_RETEST.md`): **HOLDS**.
  TNN-role force_pin/force_unpin/trainer_declare → 113 (12/12 combos, no
  effect); unpin requires pinning trainer's credentials or master role (2/3);
  all destruction ops refuse force-pinned slots with 112; no silent no-ops.
