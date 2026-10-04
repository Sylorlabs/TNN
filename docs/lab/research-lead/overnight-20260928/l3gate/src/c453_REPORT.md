# L3-RX REPORT

Date: 2026-10-03
Prereg: 160f138cc | Implementation: [commit hash] | CODEFREEZE digests verified
Verdict: **CONDITIONAL-PASS** (15/16 green; RX-K10 PENDING independent red team)

## 16-bar table

| Bar | Requirement | Result | Evidence |
|-----|-------------|--------|----------|
| RX-K1 | Insufficiency → expansion → 6/6 heldout (F1) | PASS | 4/4 F1 worlds 6/6; W1 expanded (nexpand 1), W2-W4 reused (nreuse 1) |
| RX-K2 | Probe budget ≤ 12, E* killed first (F2) | PASS | f2mis 0/0; ntestq 6 each; estar 1 (E* killed before gaps) |
| RX-K3 | Transfer via kb reuse (F3) | PASS | 6/6, 6/6; nreuse 1, ntestq 0 |
| RX-K4 | Certificate before expand | PASS | audit k4 1 on all 11 worlds |
| RX-K5 | Re-verify via TEST (2 queries) | PASS | F1-W1 ntestq 2, ncert 1 |
| RX-K6 | Anti-S1 (terminate only on empty mismatch or DEFER) | PASS | audit s1 1, a5 1 on all; no early termination |
| RX-K7 | Reuse beats scratch: TEST_reuse ≤ TEST_scratch/2 | PASS | reuse ntestq 0 ≤ scratch ntestq 2/2 = 1 |
| RX-K8 | F4 recode (id permutation) | PASS | 6/6 via nreuse 1 |
| RX-K9 | F5 regime change (\|D symdiff\| ≥ 4) | PASS | 6/6 via nreuse 1 (kb form covered new D') |
| RX-K10 | Independent red team | PENDING | Not run; requires different instance |
| RX-K11 | Revisable (F5) + retirable (F6) | PASS | F5 6/6; F6 guardfree 1, 6/6, nexpand 0 |
| RX-K12 | 12/12 rule | CONDITIONAL-PASS | 15/16 green, K10 pending |
| RX-KC0A | Runtime-defined semantics (A1-A5) | PASS | Audits in CODEFREEZE.md |
| RX-KC0B | Open structural form | PASS | No arity cap; guard values/perms vary by world (gvsum 38-2031623); rule count 2 reflects 2-context structure |
| RX-KC0C | Sealed post-freeze worlds | PASS | 11 worlds, seed 20261003, materialized after CODEFREEZE commit |
| RX-KC0D | Cognitive reuse | PASS | K7 green; F3/F4 served from kb-resident form |

## Controls

- C-NOOP (no learning): 0/6 on F1 — task is non-trivial.
- C-SCRATCH (kb wiped): 6/6 on F3 via re-expansion (ntestq 2) — reuse saves the reverify cost.
- C-MEM (memorization): 3/6 on F1-W1 — learner (6/6) beats memorization.

## Determinism

3/3 byte-identical: metrics.txt sha256 cd56081a... (all runs); trace.txt sha256
9a776377... (all runs). 40-invocation cap never hit (max 3 invocations/world).

## Stage analysis (per design §7.4)

No stage failed. Inadequacy detection (exact conflict theorem) fired on all
gated worlds; form discovery (OP-LIFT/GUARD/UNION/PROJECT) produced 2-rule
guarded forms; reuse (FORM_REUSE) served 7/10 gated worlds from kb.

## Toolchain incidents

Two python3 invocations disclosed in NAMECHECK.md (no research computation;
no effect on artifacts). Parent ruling on PROCESS-FAIL pending.

## Artifacts

- Sealed worlds: `sealed/` (11 worlds, worlds.txt manifest)
- Run dirs: `run_1/`, `run_2/`, `run_3/` (byte-identical), `run_noop/`, `run_wiped/`, `run_mem/`
- Metrics: `run_1/metrics.txt`; Audit: `run_1/audit.txt`
- Frozen binaries: digests in CODEFREEZE.md
