# RUNLOG — TRACKB arm-3 A/B/C head-to-head (resume worker, 2026-09-24)

## 0. Resume context

Predecessor (TRACKB/FELT/RC2 follow-up worker) errored 2026-09-24 17:24 UTC
on daemon-restart drain; final message never arrived. This worker verified
partial state and resumed:

- `probes/results.jsonl`: **90/90 rows present** (3 variants × 10 probes ×
  3 reps) — the matrix was NOT mid-flight; it completed. Verified row
  completeness per cell (each (variant, probe) has exactly 3 reps) and that
  the two stray run files (`varC_epin_9310.json`, `varB_revise_9210.json`)
  are NOT in results.jsonl (leftover retries, excluded from analysis).
- `probes/matrix_run.log`: determinism check 0/30 divergent — done, not redone.
- `probes/runs/`: all per-run JSONs present (timestamps 15:41–16:44 UTC).
- Binaries in `build/`: timestamps 15:16–15:17 UTC — provenance UNVERIFIED
  at resume → rebuilt all three from fetched sources (see §1). Not redone:
  probe execution, determinism check, fixture generation.

## 1. Provenance verification (done by this worker)

Toolchain pin checked first:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` ✓.

Sources: `src/FETCH_MANIFEST.json` (GitHub API fetch with blob SHAs from
committed pins; varA @ `7d056be50`). Rebuilds into `rebuild_chk/` (mirrored
layout for varB/varC's `../../harness/substrate/` @import):

| variant | rebuilt sha256 | predecessor binary sha256 | match |
|---|---|---|---|
| varA | `67c85ebbcd6cc6f96dbc312918326dd37d8d6605cd4ac1515404eb7b07c08be4` | same | YES |
| varB | `76914955ccc6fa271e2016a83c6e3763748d1d3304a5816a70f327fa68e9d76a` | same | YES |
| varC | `07c609f6155f7cf62a2ad501ed4ea2e881d33a5e7f0d9da78ba71e92ec8244e7` | same | YES |

All three probe binaries are byte-identical to pinned-toolchain builds of the
pinned committed sources. The matrix evidence stands on verified binaries.

## 2. Sharpening analysis (done by this worker)

Wrote `probes/sharpen.py` (kept) extracting from `runs/*.json`:

1. Full 90-cell aggregation: adopted_true / n_prop / efficiency /
   verdict/kind distributions / appeals / redundant / max_sightings /
   step timing per (variant, probe).
2. History-sensitivity: pairwise seqhash comparison across the 10 probes per
   variant. varA: 9/10 distinct (1 benign collision: clean==appeal_trap —
   behaviorally identical student inputs for an appeal-every-R1 teacher).
   varB: 8/10. varC: 6/10 (collisions explained by varC's 64-proposal
   self-stop + near-total R1 verdicts; see VERDICT.md).
3. Decisive per-variant failure/behavior characterization from run JSONs:
   - varB `mixed` run (`runs/varB_mixed_9260.json`): spans (6,11)×60 and
     (0,5)×59 of 190 proposals; all kind-1; cursor stalled 60 steps.
   - varB `clean` run (`runs/varB_clean_9200.json`): 8 kind-1 of 420
     proposals; phase trace INTRODUCE once then RELATE ×59.
   - varC `clean` run (`runs/varC_clean_9300.json`): span (34817,34822)
     re-proposed 19× (seq 3, 46–63) under consecutive R1; conf 60–98
     (cold band throughout); self-stop at 64 proposals.
   - varA `appeal_trap` (`runs/varA_appeal_trap_9150.json`): trap span
     (12,18) conf 168→148→128 across 3 sightings then final reject.
   - varA `r2test` (`runs/varA_r2test_9190.json`): RETRACT kind 5 at seq 3.
   - varA `revise` (`runs/varA_revise_9130.json`): 100 kind-1 → 100 kind-4
     SAME_AS, all ADOPTed.
   - `epin`: varA 12/73 steps, varB 5/60, varC 3/65 adopted.

## 3. Decision

Canonical arm-3 = **varA** (deliberative adaptive teacher). Evidence forced
it: only varA completes teaching sessions under every student behavior with
bounded, spec-exact per-decision adaptation. No PARTIAL — per Micah's
directive, tests decided. Full evidence table in `VERDICT.md`.

## 4. Deliverables

- `T2/TRACKB/headtohead/VERDICT.md` (this leg's verdict)
- `T2/TRACKB/headtohead/RUNLOG.md` (this file)

## 5. Notes / caveats

- The scripted student is not a live learner: verdicts measure the
  teacher's proposal policy against a fixed decision policy, per the
  predecessor's design (varA SPEC §12 states this explicitly). Live-learner
  closure is future work and out of scope for the canonical-choice decision.
- varB/varC failure modes are empirical findings about their designs under
  this student; they are not claims about all possible students.
- No commits made; nothing pushed. `rebuild_chk/` and `probes/sharpen.py`
  kept as working evidence.
