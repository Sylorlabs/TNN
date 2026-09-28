# TRACE_AUDIT2 — Independent Trace + Hardcode Audit, Experiment 1b (PREREG2 §7)

**Auditor:** independent trace auditor (no prior contact with Experiment 1b; trusts nothing from the implementer).
**Date:** 2026-09-27. **Prereg:** `~/workspace/e1b_complete/PREREG2.md` (frozen).
**Scope:** `docs/lab/invention/survival/recall_fix/` on `origin/tnn-native-lab`;
phase-2 sources at commit `9c79065d02`; traces added by `9c02cb507`.
**Repo was not modified.** All extractions were read-only (`git archive`); the
working tree was left untouched.
**Audit script:** `~/workspace/e1b_complete/audit/trace_audit.py` (kept; the
bulky extraction dirs were deleted afterward for disk discipline — regenerate
with the `git archive` commands in §6).

---

## 1. Forensics verdict

### 1a. Trace manifest — VERIFIED
`runs/phase2/traces/MANIFEST.sha256` (format `hash  size  filename`, 160
lines). I independently re-hashed and re-sized every file:
**160/160 files verify — hash AND byte size both match, 0 failures.**
Layout matches the README: 96 D2 files (12 variants × 2 reruns × 4 chunks of
150 turns) + 64 D3 files (8 × 2 × 4), each turn 0–599 covered exactly once.

### 1b. Trace format vs PREREG2 §2 — CONFORMS
Every one of the 24,000 decisions has, in order: 1 RECALL (candidate id,
source heuristic, match basis, claimed effect), 3 EVAL (precondition,
effect-expectation, conflict — each with named evidence → PASS/FAIL),
1 VERDICT (chosen action + deciding reason). TSV columns
`turn \t kind \t line`; no tabs/newlines inside lines.

### 1c. `trace_emit.zag` — CONFIRMED MISSING, reproduction path broken
`git ls-tree -r origin/tnn-native-lab` contains **no** `trace_emit.zag`
anywhere, and no commit in history ever contained it — yet commit
`9c02cb507`'s message and `traces/README.md` both describe it as the added
emitter and give a "Reproduction" recipe that depends on it. The finding is
confirmed.

**What this breaks:**
- The documented reproduction path is **not executable as written** — a third
  party cannot regenerate the traces from the repo.
- The README's "Decision identity" claims 2 (emitter neutrality) and 3
  (RESULT identity of the trace-instrumented runs) **cannot be independently
  re-verified**, because the instrumented binaries cannot be rebuilt.
- It does **not** break the traces themselves (committed, manifest-intact) or
  the scores (bound independently — see §2). The emitter contract is
  described precisely enough in the README (write-only; recompute evidence
  with read-only access to the exact slots the decision logic read; old
  print blocks replaced by one emitter call each; D3 adds one pure-read
  `d3_obs(w)`) that a re-derivation is feasible — but that would verify a
  reimplementation, not the original emitter.
- **Recommendation:** commit a re-derived `trace_emit.zag` (clearly labeled
  as re-derived, with a byte-comparison of its trace output vs the committed
  TSVs), or amend the README to mark the reproduction path incomplete.

---

## 2. Binding verdict — TRACES ARE BOUND TO THE COMMITTED SOURCES AND SCORES

Method: extracted the **unmodified** phase-2 sources at `9c79065d02`
(`agent_d_d2.zag`, `agent_d_d3.zag`, `recall_delib.zag`, worlds, KBs — no
edits), built with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(SHA-256 `498abcb5…`, matches the pinned value), and re-ran **all 40**
D2/D3 phase-2 runs (12 D2 variants + 8 D3 variants × 2 reruns), pure Zag,
zero RNG. My binaries:
`agent_d_d2` = `39712abb…`, `agent_d_d3` = `5fee8de9…`.

| Check | Result |
|---|---|
| RESULT lines vs committed `runs/phase2/results.txt` (D2/D3 sections) | **40/40 byte-identical** |
| Per-tick VERDICT action sequence vs committed TSV `VERDICT act=` (40 runs × 600 turns) | **0 divergences / 24,000** |
| Per-tick RECALL hid vs committed TSV `RECALL hid=` | **0 divergences / 24,000** |

So the traces' decision skeleton — which heuristic was recalled and which
action was chosen on every tick — is exactly what the committed phase-2
sources produce, and those sources produce exactly the committed scores.
**No divergence → the traces are bound to the committed scores; nothing
K3-relevant found.**

Caveat (from §1c): this binds the RECALL/VERDICT skeleton. That the EVAL
*evidence values* were recomputed from the live decision state (rather than
e.g. re-derived post-hoc) lived in the missing emitter and cannot be
re-proven. Mitigating: the audit's independent exploration model (§3)
matched the trace's `(has N)` counts exactly on all 480 exploration turns —
fabricated evidence would have had to replicate the engine's internal
exploration table perfectly.

---

## 3. §7 trace audit — MISMATCH COUNT: 0 (24,000/24,000 decisions)

Method: replayed every decision from the **committed traces only** (no sim
access). For each turn I independently:
1. checked structure (5 lines/turn, kind order RECALL→EVAL×3→VERDICT, uniform
   tick, uniform hid, sequential turns, chunk coverage);
2. checked RECALL fields against the committed home KBs (`kb/home_d2.txt`,
   `kb/home_d3.txt`): hid→(cond, act, claimed) must match verbatim; `basis`
   re-validated against the domain matchers (`d2_obs`: signal = `f1 | f2*2`,
   match iff `s == cond-1`; D3: `t == cond-1`);
3. **recomputed** each EVAL result from its own line: precondition PASS iff
   pre-bits ⊆ obs-bits (bit sets from the domain codebooks); effect-expectation
   FAIL iff `n>=10 && 2*sum < claimed*n` (the exact `delib_check_distrust`
   predicate); conflict PASS iff `higher_prio_matches=none`;
4. **recomputed** the VERDICT per the documented rule (README): ee PASS →
   retain the heuristic's action (act id from the domain codebook); ee FAIL →
   exploration (first alternative action in numeric order with <5 samples) or
   argmax (only after all alternatives ≥5). Exploration was verified against
   an **independent per-(run, hid) model** I maintained from the trace stream
   (order, chosen action, and the `(has N)` counts); argmax turns were checked
   to occur only when the independent model showed all alternatives ≥5.
   Reason text was cross-checked: claimed/mean/samples triple, and any
   precondition/conflict restatement, must equal the EVAL lines.

| Category | Count |
|---|---|
| Decisions audited | 24,000 (160 files) |
| ee PASS → heuristic action retained | 19,856 |
| ee FAIL → exploration (independently model-verified) | 480 |
| ee FAIL → argmax (gating independently model-verified) | 3,664 |
| EVAL results disagreeing with recomputation | **0** |
| VERDICT actions disagreeing with the recomputed rule | **0** |
| Reason↔EVAL cross-consistency failures | **0** |
| RECALL↔KB / basis mismatches | **0** |
| Structural defects (order, ticks, hids, coverage) | **0** |
| Integer-mean truncation-ambiguous ee lines | **0** (checked: no line sits in the band where `sum/n` truncation could flip the predicate) |
| **Total mismatches** | **0** |

Known limitation: the argmax *winner* cannot be re-derived from trace-only
data (alternative-action rewards are not in the traces); only the gating
(all alternatives ≥5 first) was verified. The ee `observed_mean` values
themselves cannot be re-derived either (reward stream not in traces) — but
their *use* in the decision (the PASS/FAIL predicate) was verified on all
24,000 lines.

---

## 4. §7 hardcode audit — NO SCENARIO/DOMAIN CONDITIONALS FOUND

Method: full read of `src/recall_delib.zag` (the one shared module, 150
lines, identical at `9c79065d02` and branch head) plus case-insensitive
greps for `d1/d2/d3`, `signal`, `task`, `tool`, `approach/hold/retreat/wait`,
`shift`, `regime`, `domain`, `home`, `variant`, `wear`, `sig_`, `cond_idx`,
`tick`. Zero code hits; the only `regime`/`domain` hits are comments
asserting the file contains no such branches. Every `if` in the file
branches on abstract quantities only: distrust predicate
(`n>=10 && sum*2 < claimed*n`), action identity (`a==hact`), sample counts
(`n<10`, `na>=5`), numeric exploration order, argmax comparison. The module
operates on abstract `[cond_id, act, claimed, pre_mask, prio]` records; the
numeric parameters (10-sample distrust gate, 5-sample exploration) are
identical across all domains — generic mechanism parameters, not
scenario branches. **K4(i) does not fire.**

---

## 5. Explicit kill-bar verdicts

- **K3(iii) — trace audit VERDICT/trace mismatches: 0 → PASS (does not fire).**
  All 24,000 VERDICTs recompute exactly from their RECALL+EVAL lines under
  the documented rule; the traces are the decisions' audit trail.
- **K4(i) — scenario-specific conditionals in the shared module: none found →
  PASS (does not fire).**

---

## 6. Observations (not bar-triggering, recorded for the record)

1. **Precondition EVAL is informational, not decision-causal.** `DH_PRE`
   (slot 3) is defined and stored but never read by any function in
   `recall_delib.zag` (`delib_select` consults only the distrust gate).
   The precondition line is genuine evidence of regime shift (1,200 FAILs,
   concentrated in shifted runs), but it does not gate the action. PREREG2
   §2's "deterministic argmax over surviving candidates" reads as if all
   three checks gate survival; the implementation gates only on
   effect-expectation. This matches the README's documented rule, so it is
   not a trace-audit mismatch — but the "conscious every step" claim rests
   on one EVAL line the decision ignores.
2. **Conflict EVAL is vacuous by construction** (24,000× `none → PASS`):
   recall takes the first match in priority order and conds are mutually
   exclusive, so no higher-priority match can exist. Honest but decorative.
3. **Missing emitter (§1c)** is the one genuine gap: the binding evidence is
   strong (§2) but the documented reproduction path is incomplete.

## 7. Reproduction of this audit
```
cd ~/workspace/selfpam_run/tnn-lab   # read-only; do not modify
git archive 9c79065d02 docs/lab/invention/survival/recall_fix/src \
  docs/lab/invention/survival/recall_fix/kb docs/lab/invention/survival/recall_fix/worlds | tar -x -C /tmp/e1b_src
git archive origin/tnn-native-lab docs/lab/invention/survival/recall_fix | tar -x -C /tmp/e1b_fix
# point trace_audit.py's TRACE_DIR/KB_DIR at those, then: python3 trace_audit.py
# rebuild: <pinned znc> agent_d_d2.zag -o agent_d_d2   (from the src dir)
```

**Bottom line:** forensics clean (160/160 manifest, §2-conformant traces);
binding proven (40/40 byte-identical RESULTs, 24,000/24,000 per-tick
decisions identical); trace audit 0 mismatches; hardcode audit clean.
K3(iii) and K4(i) both PASS. The single open item is the uncommitted
`trace_emit.zag`, which breaks the documented reproduction path but does not
undermine the traces, the scores, or the bars.
