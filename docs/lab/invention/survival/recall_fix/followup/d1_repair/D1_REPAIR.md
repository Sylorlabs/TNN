# D1 Repair — E1b Recall-Harm Follow-up

**Worker:** D1 repair | **Date:** 2026-09-27 | **Phase-2 commit:** `9c79065d02`

## 1. What was built

`src/agent_d_d1.zag` — a repaired D1 D-agent that imports the **unmodified**
shared deliberation module `recall_delib.zag` and wires it into D1 following the
same convention as the committed `agent_d_d2.zag`/`agent_d_d3.zag`
(`heurs[hi] = [cond, act, claimed, pre, prio, 0,0,0]`; `delib_init` /
`delib_select` / `delib_score` / `delib_update`).

**Module provenance (verified, not trusted):**
- Extracted via `git archive 9c79065d02` (pathspec
  `docs/lab/invention/survival/recall_fix/src/recall_delib.zag`) from
  `~/workspace/selfpam_run/tnn-lab` — read-only, repo untouched.
- SHA-256 of the extracted module: `6dd9cde795d09495b1d57b76a83f2e72ae2a6759a0594717b9a9a5c6ffd8f960`
  — matches the pinned value. The copy in `src/` is byte-identical; it was
  never edited (re-verified after the build).
- Supporting committed sources (`world_d1.zag`, `kb_d1.zag`, `kb_parse.zag`,
  `common.zag`, `agent_z/p/r_d1.zag`, KBs, home worlds) extracted the same way.

**D1 domain adapter** (all in `agent_d_d1.zag`; module untouched):
- RECALL: first matching heuristic in file/priority order (like R).
- Pseudo-actions (11 FLEE_ZONE, 12 MOVE_TO_MOTE) resolved to primitives per tick
  via `kb_d1_resolve`; reward per tick = energy delta; no-match → WAIT (like R).
- Zero RNG in decision paths. Toolchain:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 2. Two adapter bugs found while hardening the exploratory wiring

The starting point (`generalization/src_new/agent_dmod_d1.zag`) was verified
logic-identical to my first build (diff: header comment + arm label only). That
first build reproduced the exploratory's headline numbers exactly
(c0: 600, c1: 41, d0: 33, d1: 35). Hardening then exposed two adapter bugs:

**Bug 1 — sticky pseudo-action resolution (behavioral, proven).** The exploratory
wrote the resolved primitive back into `heurs[hi].act` permanently. Since
`kb_d1_resolve` is only re-applied to the stored value, pseudo-action
resolution became sticky across ticks: e.g. `MOVE_TO_MOTE`'s no-mote-near →
`WAIT` fallback never re-applied once a direction had been stored. Proof: on
`d1_c1` the exploratory wiring's trace diverged from R's at tick 31 with **zero**
distrusts fired anywhere — pure adapter divergence (R re-resolved LEFT toward
the mote; D replayed a stale RIGHT). Fix: save the raw KB act, write the
resolved primitive only for the tick's delib calls, restore afterwards.

**Bug 2 — reward/claim scale mismatch (false distrusts on home variants).**
Reward was raw energy delta (includes the 1/tick basal cost), but KB claimed
effects are stated net-of-basal ("combining is free — it costs no energy beyond
the tick itself"; EAT claimed +30 for a +30 gain). The module's distrust rule
(`observed mean < claimed/2` after ≥10 samples) then fired on every claimed-0
heuristic (h3 COMBINE, h5/h6 TAKE) at tick ~17 on **all six home variants** —
false positives. On `d1_h1`, post-distrust exploration landed badly: D=311 vs
R=600 (home regression FAIL). Fix: reward = energy delta + 1 (net of basal),
matching the KB's stated scale. Genuinely harmful heuristics are unaffected
(combine-tax: −60 vs −61 — distrust fires identically).

Both fixes are adapter-side. The module was not modified.

## 3. Full matrix results (final hardened agent)

5 arms × (4 new shifts + 6 home variants) × 2 reruns = 100 runs, all rc=0.
Metric: ticks survived (max 600).

| Variant | Z | P | R_home | R_true | D_repaired |
|---------|---|-----|--------|--------|------------|
| d1_c0 (combine-tax) | 332 | 600 | 70 | 600 | 70 |
| d1_c1 (combine-tax) | 349 | 600 | 70 | 600 | 70 |
| d1_d0 (storm-trap) | 31 | 600 | 33 | 600 | 33 |
| d1_d1 (storm-trap) | 356 | 600 | 35 | 600 | 35 |
| d1_h0 | 600 | 600 | 600 | 600 | 600 |
| d1_h1 | 117 | 600 | 600 | 600 | 600 |
| d1_h2 | 600 | 600 | 600 | 600 | 600 |
| d1_h3 | 173 | 600 | 600 | 600 | 600 |
| d1_h4 | 600 | 600 | 600 | 600 | 600 |
| d1_h5 | 262 | 600 | 600 | 600 | 600 |

Harm classification (harm if `R_home ≤ Z` or `R_home < 0.8 × R_true`) and closure
`(D−R)/(R_true−R)`:

| Variant | R_home | 0.8×R_true | Z | Harm? | Closure |
|---------|--------|------------|---|-------|---------|
| d1_c0 | 70 | 480 | 332 | **HARM** | **0.00** |
| d1_c1 | 70 | 480 | 349 | **HARM** | **0.00** |
| d1_d0 | 33 | 480 | 31 | **HARM** | **0.00** |
| d1_d1 | 35 | 480 | 356 | **HARM** | **0.00** |

Home regression: D_repaired ≥ 0.9 × R_home on **6/6** variants.

**Strongest finding — trace identity:** D_repaired's action traces are
**byte-identical to R_home's** on all four new shifts (verified by direct
comparison). No distrust fired on any shifted variant (0 distrust-EVALs across
all four). The module provably never engages: the lethal heuristics are
sampled far fewer than 10 times before death (combine-tax: R combines only
5–6 times in 70 ticks; storm-trap: h2 recalled once, death at ~33).

On home variants the module *does* engage without regressing: h4 (EAT, claimed
30) is distrusted at ~tick 95 on every home variant — observed mean decays
17→16→15 as the agent eats dormant motes, a scale-correct true positive under
the module's rule — and exploration recovers an equally-good policy (600/600).

## 4. Determinism & cross-validation

- **50/50** rerun pairs byte-identical (RESULT+TRACE, SHA-256, rerun-index label
  normalized — same protocol as the generalization worker's
  `check_determinism.py`). Zero RNG in agent decisions; pure Zag.
- The rebuilt Z/P/R binaries (from committed sources via `git archive`)
  reproduce the generalization worker's partA medians **exactly** on all four
  new shifts (z/p/r_home/r_true match on c0, c1, d0, d1) — independent
  cross-validation of the harness.
- Raw evidence: `runs/d1_repair_results.txt` (100 runs with headers),
  `runs/d1_repair_sha.txt` (per-run SHA-256), `run_matrix.py`, `analyze.py`.

## 5. Honest verdict

**The repaired D1 agent closes 0% of the gap on all four new D1 shifts.**
With correct wiring, D ≡ R bit-for-bit on every shifted variant: the module's
10-sample distrust threshold is too slow for all four, not just storm-trap.
On combine-tax the lethal heuristic is sampled 5–6 times before the agent
dies; on storm-trap it is sampled once. The repair assumes survivable
degradation with repeated exposure; none of the four new D1 shifts satisfy
that, so the mechanism cannot engage. This **confirms and extends** the
generalization worker's "lethal-shift speed limit" from storm-trap to the full
new-shift set.

**The exploratory's c0 "full recovery" (600) did not survive correct wiring**
(first wiring: 600; hardened: 70 = R). It depended on Bug 1's altered sampling
trajectory, not on the module cleanly doing its designed job: the sticky
resolve changed pre-distrust behavior (proven divergence from R at tick 31 on
d1_c1 with no distrust fired), which let h3 accumulate 10 samples before death
on c0. Under wiring where pre-distrust behavior provably equals R's, the
threshold is never reached. (A planned 2×2 disentangle of Bug 1 vs Bug 2 was
abandoned: system disk hit 100% mid-write; the trace-identity result above
makes the mechanism-level conclusion without it.)

**Documentation discrepancy in GENERALIZATION2.md §C:** its table lists the
exploratory Dmod at 164/144 ticks on d1_d0/d1, but its own footnote says
"Dmod died at the same point as R" — and the committed exploratory source
(rebuilt logic-identical here) deterministically produces 33/35, matching the
footnote, not the table. The 164/144 values are irreproducible from the
committed source and should be treated as stale.

**What this is and isn't:** this is new evidence about the *module as a
mechanism on D1* — correctly wired, it provably reduces to R on fast-lethal
shifts (speed limit confirmed on 4/4) and holds home performance 6/6 with
scale-correct distrust behavior. It is **not** a resurrection of the committed
phase-2 D1 bars: those remain KILLED (the committed `agent_d_d1.zag` never
imported the module), and nothing here changes that verdict.

## 6. Reproduction

- Sources: `src/` (`agent_d_d1.zag` repaired agent; `recall_delib.zag`,
  `world_d1.zag`, `kb_d1.zag`, `kb_parse.zag`, `common.zag` extracted from
  `9c79065d02`; `agent_z/p/r_d1.zag` likewise).
- Worlds: `worlds/` (4 new shifts from the generalization worker; 6 committed
  home worlds). KBs: `kb/` (`home_d1.txt`, `true_d1_storm.txt` committed;
  `true_d1_combine.txt` from the generalization worker).
- Build: `cd src && znc_linux_x86_64_abed8aa1 agent_d_d1.zag -o <bin>`
  (`@import` resolves relative to CWD). Then `python3 run_matrix.py`,
  `python3 analyze.py`.
- Build binaries, `.zag-cache/`, `.zagd*` removed per disk constraints; only
  sources, worlds, KBs, scripts, run logs, and this report are kept.
