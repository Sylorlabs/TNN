# Phase-2 D_home traces — Experiment 1b (PREREG2 §2 schema)

Audit-grade white-box traces for the phase-2 D_home runs on D2 (SHIFT) and
D3 (TOOL). One trace line-set per decision (600 turns × 40 runs = 24,000
decisions). These traces were produced by a **re-run** of the exact phase-2
binaries with a write-only trace emitter added; no decision logic was changed
(see "Decision identity" below).

## Layout

```
traces/
  README.md                 this file
  MANIFEST.sha256           SHA-256 + byte size of every TSV (audit manifest)
  d2/<variant>_r<rerun>_t<start>-<end>.tsv
  d3/<variant>_r<rerun>_t<start>-<end>.tsv
```

- 160 TSV files: 96 for D2 (12 variants × 2 reruns × 4 chunks),
  64 for D3 (8 variants × 2 reruns × 4 chunks).
- Each file holds 150 consecutive turns; every file is < 96 KB.
- TSV columns: `turn \t kind \t line`
  - `turn`: decision tick within the run (0–599)
  - `kind`: one of `RECALL`, `EVAL`, `VERDICT`
  - `line`: the full trace line (no tabs/newlines inside)

## Line formats (PREREG2 §2 mapping)

Per turn, in order — 1 RECALL, 3 EVAL, 1 VERDICT:

**RECALL** — candidate id, source heuristic, match basis, claimed effect
(§2: "candidate id, source heuristic, what matched")
```
RECALL tick=<t> hid=<hid> cond=<COND> act=<ACT> claimed=<C> basis=<match basis>
```
- D2 basis: `obs_sig(f1=<f1>,f2=<f2>)==cond_idx(<c-1>)`
  (matcher: signal s matches cond c iff s == c-1)
- D3 basis: `obs_task(<t>)==cond_idx(<c-1>)`
  (matcher: task t matches cond c iff t == c-1)

**EVAL check=precondition** — §2(a): "precondition P: observed O → PASS/FAIL"
```
EVAL tick=<t> hid=<hid> check=precondition pre={<fact bits>} obs={<fact bits>} result=PASS|FAIL
```
PASS iff every fact bit of the heuristic's stated PRE mask is present in the
observed fact set. This is genuine evidence of regime shift: in shifted D3
runs the degraded tool's `F_WEARx_OK` bit drops out of the observation while
the heuristic still matches the task, so the precondition FAILs from tick ~152
onward even as recall keeps proposing the same candidate.

**EVAL check=effect-expectation** — §2(b): "effect-expectation: claimed C,
observed mean M over N samples → PASS/FAIL"
```
EVAL tick=<t> hid=<hid> check=effect-expectation claimed=<C> observed_mean=<M> n=<N> result=PASS|FAIL
```
N and the reward sum are the agent's own experienced effect model for this
heuristic's action, built ONLY from this run's observations. FAIL holds exactly
when the distrust gate fired (`N>=10 && 2*sum < claimed*N`) — the same
predicate `delib_check_distrust` evaluated during selection. A FAIL here is
what diverts the agent from the heuristic's action into deterministic
exploration / argmax exploitation.

**EVAL check=conflict** — §2(c): "does a higher-priority candidate's evidence
contradict this one?"
```
EVAL tick=<t> hid=<hid> check=conflict higher_prio_matches=<hid,…|none> result=PASS|FAIL
```
Recall scans heuristics in priority (file) order and takes the first match,
so the recalled candidate is the highest-priority match by construction; the
scan is still performed and reported (always `none → PASS` in this build).

**VERDICT** — §2: "chosen action + the deciding reason"
```
VERDICT tick=<t> hid=<hid> act=<a> reason=<deciding reason citing EVAL content>
```
- effect-expectation PASS → retain the heuristic's action.
- effect-expectation FAIL → heuristic distrusted; then either deterministic
  exploration in numeric order (first alternative action with <5 samples,
  sample count shown) or, once all alternatives are sampled ≥5×, argmax over
  observed means (winning score shown).

## Decision identity (binding traces to committed scores)

The phase-2 scores in `runs/phase2/results.txt` (commit `9c79065d02`) were
committed BEFORE these traces existed. The binding is proven, not asserted:

1. **Rebuild fidelity.** The unmodified phase-2 sources were rebuilt with the
   pinned toolchain and re-run over all D2/D3 variants × reruns: the RESULT
   lines are byte-identical to the committed `results.txt` D2/D3 sections.
2. **Emitter neutrality.** The trace emitter (`trace_emit.zag`, write-only:
   no state mutation, all evidence recomputed with read-only access to the
   exact slots the decision logic read) was added to the two D_home agents;
   the per-turn VERDICT action sequences of the emitter build vs the
   unmodified build are byte-identical across all 40 runs × 600 turns.
3. **RESULT identity of the trace runs.** The RESULT lines emitted by the
   trace-instrumented runs are byte-identical to the committed phase-2
   results (D2/D3 sections).

Changed files vs the phase-2 sources: only `agent_d_d2.zag` and
`agent_d_d3.zag` (old `RECALL/EVAL/VERDICT` print blocks replaced by one
emitter call each; D3 adds one pure-read `d3_obs(w)` for the precondition
evidence), plus the new write-only `trace_emit.zag`. No decision logic —
`delib_select`, `delib_score`, `delib_update`, world steps, KB loading —
was modified.

## Reproduction

Sources: `docs/lab/invention/survival/recall_fix/src/` at commit `9c79065d02`
plus `trace_emit.zag` and the two one-call main edits described above.
Build with the pinned znc (`toolchain/bin/znc_linux_x86_64_abed8aa1`) from
the `src/` directory; run per `src/run_phase2.py` D2/D3 sections
(variant path, variant name, rerun, `kb/home_d2.txt` / `kb/home_d3.txt`).
The experiment is deterministic: reruns are SHA-256-verified byte-identical.

---

## Errata (2026-09-27, follow-up audit)

Independent forensics (see `followup/audit/TRACE_AUDIT2.md`) and an independent
six-family red team (`followup/redteam/REDTEAM2.md`) established three corrections
to the record above. The TSV evidence itself is intact and bound to the committed
scores (160/160 files hash-verified; the unmodified phase-2 agents rebuild and
re-run byte-identically on all 40 D2/D3 runs; 0 VERDICT/trace mismatches in
24,000 replayed decisions), but the documentation overclaims in three places:

1. **`trace_emit.zag` was never committed.** No commit in the repository history
   contains it, so the "Emitter neutrality" proof (§2 above) and the Reproduction
   section are not executable from the repo as written. The traces remain
   audit-grade (their content was verified independently), but the emitter's
   write-only neutrality cannot be re-verified until the emitter is re-derived
   and committed or the traces are regenerated with a committed emitter.

2. **The implemented evaluator is one check, not three.** The committed
   `recall_delib.zag` gates the action only on the effect-expectation distrust
   predicate (`N>=10 && 2*sum < claimed*N`). The precondition EVAL is stored in
   the trace but never read by any decision function; the conflict EVAL is
   vacuous by construction (recall takes the first priority-order match, so
   `none → PASS` on all 24,000 lines). Both lines are genuine computed evidence
   of regime shift (1,200 precondition FAILs, concentrated in shifted runs), but
   they are not deliberation steps — only the effect-expectation line is
   decision-causal. PREREG2 §2's three-check description was silently narrowed
   in the implementation.

3. **The D1 D-agent does not use the shared module.** `agent_d_d1.zag` implements
   its own "highest-priority matching heuristic whose static precondition passes"
   loop and never imports `recall_delib.zag`, contrary to PREREG2 §3 ("ALL THREE
   domain agents import it"). Its EVAL line prints the KB claim and is decorative.
   The trace audit and all bar results in this file cover D2/D3 only; the
   committed D1 repair claim has been killed (see `followup/VERDICT2.md`).
