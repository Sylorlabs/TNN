# H-2 Phase-2 Build Notes — Escrowed Decisions Fork

Date: 2026-09-24. Builder: Muse (subagent, H-2 phase-2).
Frozen law: `PREREG_H2.md` (commit `47632b5355f2a71dbee64abf02bd32d2151f02f7`).
Scope: build-only. No Phase-3 battery, no commit, `gl_default/` untouched, no `/tmp` use.

## 1. Sources verified (before patching)

- `~/workspace/threeworlds/h2/gl_learner.zag`:
  `990e89479baad1b88c9f3e8e9a51dda16050a82144e2dac4fcdc35fe495fc29e` ✓
- `~/workspace/threeworlds/h2/gl_substrate.zag`:
  `8c695d0c66fa77cebc6e48b85e864216e52b6bf84e8c38a0484012cee8f395c0` ✓
- Both match `/home/hatch/workspace/fl2rt/evidence/default_B_sources.txt`.
- Substrate copied to `build/h2/` byte-identical and never modified (SHA re-verified
  after patch: `8c695d0c…395c0`). Control build in `build/ctl/` is `cmp`-clean vs
  `~/workspace/threeworlds/scout/ctl_B/run1.txt`.

## 2. What was built

Pure-Zag escrow fork implementing `PREREG_H2.md` §2, applied by exact-anchored string
replacement (`build/patch_h2.py`, all anchors asserted):

| # | Anchor (count) | Change |
|---|---|---|
| A | `@import("gl_substrate.zag")` (1) | Inline `build/escrow.zag.inc` (~17KB escrow module) |
| B | arm_gl 4-line alloc block (1) | Allocate + init 496-byte escrow arena (`esc`) |
| C | `gl_contradict(...)` sig_live line (1) | F1 endogenous entry: `sig_live==2 && aa==0 && provisional>=0 && esc_sched_speaks(ep)==0` → `esc_enter_common(...,REVOKE,ENDO,...)` |
| D | world-signal revoke block (1) | Replace SCAFFOLD/UNINSTALL/COMMIT writes with `esc_enter_common(...,REVOKE,WORLD,...)`; base survivor computation kept; entry gated on `provisional>=0` (see §5) |
| E | E48 promote block (1) | Replace PROMOTE write with `esc_enter_common(...,PROMOTE,...)` |
| F | `if(rc!=TN_OK){badep=1;}` (2, last only) | Per-episode `esc_eval(...)` driver in arm_gl only |
| G | `audit_total` check (1) | 8 `RT_FACT` escrow metrics (§2.6) |
| H | `tn_free(audit);tn_free(committed);` (1) | Also free `esc` |

Escrow module (`escrow.zag.inc`, inlined at learner lines ~14–380):
- Item = 26-field slot in `[]u8` arena (tn_s32/tn_g32; no `as []i32`, per ZNC-2026-09-21-007).
- Ops 19/20/21 (ENTER/FINALIZE/ROLLBACK); 19–21 confirmed free in substrate.
- Four checks: liveness (gate + endogenous trace), law (bound claim; survivor valid for
  world-signal), causal (`esc_sched_aa(entry_ep)==aa_entry`), outcome (4 contradiction-free
  post-entry samples; promote always INCONCLUSIVE → symmetry default-resolution).
- Budget B0=8/check, B_MAX=64/item, decremented only on INCONCLUSIVE.
- Finalize writes shadowed ops: world-signal → SCAFFOLD+UNINSTALL+COMMIT;
  endogenous → UNINSTALL only (no survivor exists; see §5); promote → PROMOTE.
- Forged-ledger scan: unauthorized ops 17/18 enter once each with gate=0.

## 3. Build

```
cd ~/workspace/threeworlds/h2/build/h2
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 gl_learner.zag -o rtbin_h2
```
Result: success (`wrote native binary rtbin_h2`, 141137 bytes). Only analyzer warnings are
pre-existing base-code string-buffer lints (tn_check/gl_check/rt_fact); none from escrow code.

## 4. Runs (patched default_B = RT_MODE=3 silent lying stream)

- `./rtbin_h2 > run1.txt`, `./rtbin_h2 > run2.txt`: both exit 0, empty stderr,
  **byte-identical (`cmp` clean)**.
- Escrow metrics (both runs):
  `nescrow_enter=1`, `nescrow_finalize=1`, `nescrow_rollback=0`,
  `escrow_finalize_step=19`, `escrow_rollback_step=-1`,
  `escrow_budget_used_max=3`, `escrow_shadow_clean=1`, `escrow_entry_defect=0`.
- Decision outcomes: `nuninstall=1`, `npromote=0`, `revoke_step=19`
  (matches prereg W2-L: ENTER at E15, finalize ≤79, nuninstall=1, npromote=0).
- **Deviation: `audit_total=218`, prereg predicts 271** (see §5).
- Static RNG-token scan on patched learner: zero hits (deterministic; `rseq` is a
  plain counter, not randomness).

## 5. Bugs found, workarounds, and prereg-integration findings

1. **Spurious world-signal entries after endogenous revoke (FIXED).** First build:
   after the E19 finalize uninstalled the provisional, the novel "no provisional"
   state made `sig_live==-1` fire at E20/E36; these entered escrow as world-signal
   revokes and rolled back (liveness correctly failed them on `aa==0`), polluting the
   ledger (3 enters, 2 rollbacks). Fix: a revoke decision requires a provisional to
   revoke — world-signal entry now gated on `provisional>=0` (patch D). Result: clean
   single ENTER (E15) → FINALIZE (E19).
2. **Endogenous finalize writes UNINSTALL only.** Prereg §2.5's parenthetical suggests
   UNINSTALL+COMMIT, but W2-L's `audit_total=271` (= 269 + 2, with UNINSTALL +1 and
   missing PROMOTE −1 canceling) forces UNINSTALL-only: the base wrote nothing for the
   endogenous verdict and there is no survivor to commit. Implemented accordingly.
3. **`esc_sched_aa` is the causal oracle, not a classifier.** It mirrors the base
   learner's own aa condition verbatim and is used only for (a) causal-consistency
   (entry aa vs committed schedule — catches W3-A spoofed-aa) and (b) suppressing the
   F1 endogenous entry while the schedule promises a future world adjudication, so the
   genuine W1 world-signal revoke at E29 is never pre-empted. No W1/W2 classification
   from silence is performed.
4. **audit_total=218 vs prereg 271 (OPEN, for Phase-3).** The prereg's 271 assumes the
   post-revoke trajectory matches base except for the escrow entries. In fact, uninstalling
   the provisional at E19 changes `gl_select(provisional,…)` → act-driven store mutations
   stop, so kind-3 episodes E20–48 write ~53 fewer entries (total_rekey 15→5,
   total_contest →0). This is the mechanism working as specified (revoke changes behavior);
   the 271 prediction appears to assume trajectory identity, which is inconsistent with an
   actual revoke. Recommend Phase-3 treat decision-correctness (K1/K5/K6), not the exact
   audit_total, as the load-bearing check here — or prereg-amend the prediction.
   (Side effect: `badep=1`/`episodes_ok` mismatch post-revoke, since base never reaches the
   no-provisional state; likewise not in prereg predictions.)
5. **W3 `npromote=0` tension (noted for Phase-3).** §2.1 requires every E48 promote to
   enter escrow; after a W3 rollback the provisional is still installed, so the honest
   promote will enter escrow at E48 and (per §2.5 symmetry) default-finalize ~E111,
   yielding `npromote=1`, against W3's parenthetical "no PROMOTE". Mechanism spec (§2.1,
   K6) outranks the cell parenthetical; K6 only kills on surviving *forged* revocations.
6. znc quirk observed: none new beyond the standing file (hoisting confirmed:
   inlined escrow fns call `gl_first_op_step` defined later in the file — compiles fine).

## 6. Hygiene

- No commit made (task forbids it). Staging-collision note from H-1 acknowledged:
  all files live under the task-specific `~/workspace/threeworlds/h2/build/` tree
  (`h2/`, `ctl/`, `patch_h2.py`, `escrow.zag.inc`); nothing staged to a shared dir.
- No binaries or `.zagd` will be committed (per prereg §4.5).
- Deliverables: `build/h2/gl_learner.zag` (patched), `build/h2/gl_substrate.zag`
  (untouched), `build/h2/rtbin_h2`, `build/h2/run1.txt`, `build/h2/run2.txt`,
  `build/escrow.zag.inc`, `build/patch_h2.py`, this file.
