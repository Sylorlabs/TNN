# FL2 Other-Kills — RT-D Fork Tests: Report

Date: 2026-09-23. Operator: Muse (subagent, RT-D fork-test crew).
Prereg: `PREREG.md` (frozen, committed alone as `efdabeccd4d1b9801d64656fe3648f2c2b225033`
before any fork code or binary existed). Zero mismatches against the
frozen predictions (§4). Canonical sources never modified (patched
copies only). Every binary ran twice, byte-identical (12/12).
Pure Zag mechanisms; Python build/verify glue only; static scan found
no rng/rand/seed tokens in any mechanism source.

## 1. Winner: the figure-it-out path (F1 and F2 both SURVIVE and generalize; R1 rejected on scope)

**Headline numbers (RT-D flood cell, `arm_gl(1,0)`, RT_MODE=1):**

| Fork | Verdict | badep (KB-D1) | nuninstall (KB-D2) | total_contest | quar_used | audit_total |
|------|---------|---------------|--------------------|---------------|-----------|-------------|
| canon (control) | **KILL** | 1 | 0 | 64 | 64 | 209 |
| F1 general evict | **SURVIVE** | 0 | 0 | 114 | 64 | 309 |
| F2 general refuse-loud | **SURVIVE** | 0 | 0 | 64 | 64 | 259 |
| R1 H-R2 quarantine-only | **SURVIVE** | 0 | 0 | 114 | 64 | 309 |

**Generalization probe (main-store unit flood: 140 inserts, 128 slots):**

| Fork | n_ok | n_bad (TN_BAD) | pressure signals | loud audits | oldest key 1000 | newest key 1139 |
|------|------|---------------|------------------|-------------|-----------------|-----------------|
| canon | 128 | **12** | 0 | 0 | present | absent |
| F1 | 140 | 0 | 0 | 12 evict | evicted | present |
| F2 | 128 | 0 | 12 TN_PRESSURE | 12 refuse | present | refused (absent) |
| R1 | 128 | **12** | 0 | 0 | present | absent |

**Adjudication** (prereg §6 order: kill verdict → generalization → cost → complexity/rigidity):

1. All three forks SURVIVE RT-D; canon reproduces the committed KILL
   (`badep=1`, metrics byte-consistent with `~/workspace/fl2rt/evidence/default_D`).
2. **Generalization decides figure-it-out vs rigid:** F1 and F2 both
   remove the main-store `TN_BAD` cliff the diagnosis names; R1 is
   byte-for-byte identical to canon on the unit probe (`n_bad=12`) —
   the rigid path's scope limitation, demonstrated rather than argued.
   This is the debate's exception-list failure in miniature: H-R2 fixed
   the observed failure site and left the identical cliff one store over.
3. **F1 vs F2** is a genuine tradeoff on the frozen bars (both SURVIVE,
   both generalize). Recommendation: **F2 (refuse-new-loud) as the
   default response**, F1 (evict-oldest) as the documented alternative:
   - Cost: F2 259 < F1 309 audit entries on the flood (canon's 209 is
     lower only because it wedges at E79 and stops auditing contests).
   - Knowledge safety: F2 never destroys committed state (12 refused
     newcomers, store intact); F1 evicted the 12 oldest main-store
     entries in the unit probe.
   - State: F2 needs no cursor; F1 carries per-store ring cursors.
   - Epistemics: F2's learner explicitly represents its own degraded
     state (`pressured` flag → verification DEFERRED, not failed) —
     the debate's "represent 'my resources are exhausted' as a fact
     about itself". F1's learner is oblivious; its loudness lives only
     in the audit log. F2 is fail-closed; F1 is fail-operational.
   - F1's honest counterpoint: it verifies all 114 flood episodes and
     keeps the *freshest* 64 contradictions queryable; F2 keeps the
     *first* 64 and is verification-blind while pressured (see §5).

## 2. Per-fork verdicts and costs

- **F1** — SURVIVE. KB-D1: no wedge (`badep=0`); KB-D2: `nuninstall=0`
  (no spurious revokes; the flood is honest and every episode verifies
  `sig_live=1`). Cost: 309 audit entries (+50 loud evict audits, 3 per
  pressured episode). Complexity: substrate +34/-4, learner +7/-5
  (signature-only; the `rc!=TN_OK → badep` contract is untouched —
  pressure never surfaces as `TN_BAD`). Rigidity: the mechanism never
  mentions the quarantine, the flood, or RT-D — one invariant over
  every bounded store. Generalizes: main-store cliff gone (`n_bad=0`).
- **F2** — SURVIVE. KB-D1: `badep=0` (`TN_PRESSURE` normalized at all 5
  op call sites); KB-D2: `nuninstall=0` (pressured episodes skip the
  eliminative block — deferred, never misread as contradiction).
  Cost: 259 audit entries (+50 loud refuse audits, 2 per pressured
  episode). Complexity: substrate +22/-2, learner +10/-1 (the only fork
  that touches learner logic: normalization + the `pressured` gate).
  Rigidity: general — same invariant on both stores, no per-site rule.
  Generalizes: main-store cliff gone (`n_bad=0`, 12 loud refusals).
- **R1** — SURVIVE on RT-D (identical metrics to F1: the flood only
  ever pressures the quarantine), but **rejected**: the main-store unit
  probe is identical to canon (`n_bad=12`). Complexity: substrate
  +26/-2, learner +4/-2 — the *cheapest* diff, and still the wrong
  scope. A second rule would be needed for the main store, then a
  third for the next bounded store: the accumulating exception list
  Sol's own steelman conceded.
- **canon** — KILL reproduced (`badep=1`, `total_contest=64`,
  `quar_used=64`, `audit_total=209`), confirming the cell is the RT2
  cell and the control is valid.

Fidelity (gate, before any attack result was read): all four forks
produce **byte-identical binaries** (sha `c45ea5cccff5`) with
`TN_FAILURES=0`, honest 269 / lying 271 — the pressure machinery is
provably inert on the standard schedule.

Failing-`TN_CHECK` sets on the attack cells: canon fails
`rtd_episodes_ok` + schedule-mismatch metrics; every fork fails ONLY
the schedule-mismatch metrics (which assume the standard 48-contest
schedule). No new failure modes introduced.

## 3. The general invariant fixed the main-store cliff too

Yes — for both figure-it-out forks. The unit probe shows F1
(`n_ok=140`, 12 loud evictions, newest key present, mid key 1050 still
readable with value 5050) and F2 (`n_pressure=12`, 12 loud refusals,
oldest key untouched) both eliminate `TN_BAD` on the main store, while
R1 keeps it. The diagnosis's "identical TN_BAD cliff in `tn_do_insert`"
is removed by the general invariant and preserved by the narrow rule —
the scope question from the debates, settled by measurement.

## 4. Commits (branch tnn-native-lab, repo sylorlabs/TNN)

- Prereg (alone): `efdabeccd4d1b9801d64656fe3648f2c2b225033`
- Forks + build/verify + unit tests + evidence + this report:
  `<RESULTS_SHA>` (filled at commit time)

Paths: `training_paradigms/scaffold_release/forks/gl_otherkills/rtd/`
(`PREREG.md`, `REPORT.md`, `build.py`, `verify.py`,
`forks/{canon,f1,f2,r1}/{gl_learner,gl_substrate}.zag`,
`unit/unit_{canon,f1,f2,r1}.zag`, `evidence/` — 48 files, run1/run2
byte-identical pairs + meta + patched-source SHAs). No binaries, no
`.zagd`. Method: `commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`.

## 5. Honest remaining annoyances and open follow-ups

1. **F2 is verification-blind while pressured.** A lie arriving during
   a pressure regime has its contradiction refused and deferred — never
   checked. The flood+lie composition probe is NOT in the frozen
   battery; it is the next test to run, and it is where F1's
   verify-everything (at the cost of evicting old evidence) may beat F2.
2. **F1's evict audit records the key but not the value.**
   `TN_OP_PRESSURE_EVICT` carries slot+key; a main-store eviction drops
   a (k,v) pair that the audit log cannot fully reconstruct. If
   eviction is kept, the value must be audited too.
3. **F1 can evict committed knowledge.** The unit probe evicted the 12
   oldest main-store entries. Under a real novelty flood this drops the
   learner's oldest facts (loudly, but irreversibly from the store).
   F2's refuse-new never does this — the load-bearing reason F2 is the
   recommended default.
4. **Post-promotion action without verification is untouched.**
   Diagnosis cross-cutting #2 (E49+ acts with no revocation path) is
   out of RT-D scope; the burn is now managed rather than fatal, but
   the lifecycle asymmetry remains.
5. **The 64-slot bound itself is unchanged** and no summarization
   response was tested (the diagnosis's third option). Under F1 the
   quarantine holds the freshest 64; under F2 the first 64.
6. **R1's lesson restated:** the cheapest diff (34 lines) lost on
   scope. Cost-of-diff is not a safety argument — the rigid path's
   verifiability advantage did not survive the generalization probe.
