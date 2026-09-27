# Continual-Learning Machinery Recon (2026-09-27, read-only)

All paths under `~/workspace/tnn-lab`. Verified on disk; AGENTS.md toolchain lessons read first.

## 1. Deliberate memory substrate

- `wave9/trust-tiers/substrate/st_memory_core.zag` (850 lines) — newest copy. Older/duplicate copies: `wave9/integration/impl/substrate/st_memory_core.zag` (differs from trust-tiers copy), plus wave5/wave7/wave8/wave10/wave12 trial copies.
- Core API (`*StStore`): `st_init(cap,audit_cap,org)`, `st_add(s,value,region,strength,&out_slot)` (value = **i32 claim code**, not text), `st_strengthen/weaken`, `st_evidence(s,slot,code,cite_ep)` (cite evidence episodes), `st_justify`, `st_kill_evidenced`, `st_kill` (delete path — per standing rule, TNN must not use; trainer-instrument only), `st_overwrite`, `st_force_pin/unpin`, `st_pin/unpin`, `st_promote/demote`, `st_set_stage`, `st_abandon`, `st_rollback_last`, `st_snap/restore` (5 out-pointers for deliberation fork checkpoints), `st_audit_append`, 16-word audit layout: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60.
- `wave9/trust-tiers/substrate/cl/common.zag` (53 lines) — `cl_check(name,actual,expected)`, `cl_check64`, disjointness/LE IO helpers.
- Native helpers `R33_NATIVE_IO_V1.zag` / `R33_NATIVE_SHA256_V2.zag` sit beside every substrate dir (import path must be file-relative, per AGENTS.md).

## 2. Teaching / intake path

- `mg_chunking/intake.zag` — promoted (PROMOTION_VERDICT.md, 2026-09-26) text-QA intake: `run_q(qid, q, text, expected, ...)` → `d_choose(kind,text)` (deliberative chunk selector) → `d_locate` → `mg_zoom` → `d_answer`. Input = plain English (question, context-text, expected) currently baked as 24 literal `run_q(...)` calls in `main()`; output = answer + trace log.
- `knowledge/kb_control/crewB/src/kbctl.zag` — chunk-store CLI: `put|revise|delete <dir> <id> <key> <textfile>`; integer-id keyed text chunks, not a learning loop.
- `wave9/trust-tiers/substrate/trust_tiers.zag` — newest st-substrate driver: `tt_admit(...)` calls `st_add` but takes `value:i32` claim codes from scripted campaign episodes (`main()` selects campaign sims via `_zag_arg(1)`), not English.
- **Gap:** no existing code converts English facts into st-substrate slots. That wiring is crew-authored work for the experiment.

## 3. Probing / recall path

- `onebrain/impl/onebrain.zag` (1,358 lines, pure Zag, zero RNG) — shared-ledger deliberation QA. CLI: `onebrain <mode> <problem.tsv>`; TSV rows `id\tquery\texpected`; modes single/onebrain/min; emits per-item verdict + ARGMAX winner trace. Examples: `onebrain/impl/smoke.tsv`, `edge.tsv`.
- `epistemics/principles_learned/delib_base.zag` — single-claim epistemic deliberation: `deliberate_si(utterance, budget)` → ENDORSE/WITHHOLD; CLI `delib_base <workdir> <budget> <items-file>`, items as `id|utterance` lines. `delib_plearn.zag`, `delib_hinject.zag` are variants (principle-learned, hypothetical-injection).

## 4. Consolidation / promotion harness (reusable)

- `wave3/r27-consolidation/impl/psm.zag` — **deliberate consolidation policy**, the closest existing analog: `psm_init(mode,nf,ns,nh)`, `psm_observe(id,op,param,ctx,ver)` (log a skill use), `psm_consolidate(fi)` (TNN-decided fast→slow promotion), `psm_condemn`, `psm_probe`, `psm_slow_get`, `psm_hist`. Fast/slow are item tables of (id,op,param,confidence) rows; consolidation is discrete and audit-logged. Input: integer-coded (id,op,param) tuples from `trial.zag` battery; output: promotion/condemn decisions + history digest. `TRIAL_RESULTS.md` committed.
- `wave9/trust-tiers/substrate/trust_tiers.zag` — trust-tier admission gate over st slots (`tt_admit`, `tt_hold_trigger/resolve`, `tt_gate`, strength tax), campaign-driven.

## 5. GEN→ELIM→ARGMAX deliberation substrate

- `onebrain/impl/onebrain.zag`: `gen_readings` / `gen_facts` / `gen_actions` (GEN) → `elim_phase` (ELIM) → `argmax_phase` (ARGMAX) over one shared ledger (`ob_deliberate`), with fork sub-deliberations (`fork_assess`, `ob_subpasses`) and poisoning/self-audit probes (`ob_poison`, `ob_audit`). Build: `onebrain/impl/build.sh` → znc → `./onebrain` binary. Verdict: VERDICT.md (fan-out fixed 0/11 missed items; shared-ledger audits can annihilate all candidates — p02).
- Note: the "deliberation fork-divergence repair" (round-4 38/38, commit `945b061b4`) and its `dialogue.zag` are **not in the working tree** — only on the `tnn-native-lab` branch commits. Fetch/sync the branch before reusing that line.

## 6. Native mechanism vs crew scaffolding (judgment)

- **Genuinely native (TNN's own mechanisms, deterministic, audited):** `st_memory_core.zag` (the full st_* op set incl. audited promote/demote/snap/restore), `cl/common.zag` check helpers, `psm.zag` deliberate consolidation policy, `onebrain.zag` ledger deliberation, `delib_base.zag` epistemic deliberation, `mg_chunking/intake.zag` arm-D chunking QA.
- **Crew scaffolding:** all battery drivers, campaign simulators (`trust_tiers.zag` main, `trial.zag`, `run_trial.sh`), TSV problem sets, scoring scripts (`score.py`, `run.py`), kb chunk-store CLI, build scripts.
- Hardest gap for a continual-learning experiment: substrate keys are **i32 claim codes**, not text — English intake → claim-code registry → st slots must be authored.

## Recommendation

Build on `wave9/trust-tiers/substrate/st_memory_core.zag` (newest audited substrate) + `wave3/r27-consolidation/impl/psm.zag` (the only deliberate promotion/consolidation policy on disk) as the memory core, drive decisions through `onebrain.zag`'s shared-ledger GEN→ELIM→ARGMAX for adjudication, and use `epistemics/principles_learned/delib_base.zag`'s utterance intake pattern (`id|sentence`) plus `mg_chunking/intake.zag`'s QA answering for the English-facing ends. Author one thin native bridge: an English fact → claim-id registry that calls `st_add`/`st_evidence`/`st_promote` — that bridge is the experiment's core deliverable and must itself be preregistered with kill bars before any "learning" claim is made.
