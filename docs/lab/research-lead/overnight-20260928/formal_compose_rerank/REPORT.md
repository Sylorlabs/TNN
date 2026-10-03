# REPORT.md -- FORMAL-COMPOSE-RERANK: promotion-based re-ranking

Date: 2026-10-03. Worker: FORMAL-COMPOSE-RERANK. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_rerank/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE (BUILD-PASS K1-K5; boundary B1:
acyclic cross-rank attach inert on REP); FORMAL-COMPOSE-PORT
(BUILD-PASS K1-K5); FORMAL-COMPOSE-E2E (BUILD-PASS EK1-EK7;
suggested follow-up: "promotion-based re-ranking with these
stacks as test bed").

## Verdict: BUILD-PASS (RR1-RR6 all green)

Promotion-based re-ranking resolves the FORMAL-COMPOSE B1
sufficient-but-not-necessary boundary: acyclic cross-rank attaches
that went inert under fixed creation-order ranks now commit via
representational promotion, while cycles remain structurally
impossible (no refusal branch anywhere in the store).

## 1. Mechanism (`es_rerank.zag`)

Rank-slot store with mutable ranks. `es_link` writes the edge
record unconditionally, then if `rank(to) >= rank(from)` runs
`es_promote`:

- Phase 1: compute target ranks `t` by relaxation (at most 23
  passes) over readable written edges only: `t[Y] := t[W]+1`
  whenever `t[Y] <= t[W]`, seeded with `t[parent] := rank(child)+1`.
  The readable graph always has strictly decreasing ranks, so it
  is a DAG and Phase 1 always converges; a pass cap sets the
  diverge flag (never triggered: diverge=0 in all runs).
- Phase 2: install `t` and relocate each promoted item's records
  from old head to new head, preserving every previously readable
  edge.

`es_raw` performs the same write+promote (there is no gate to
bypass). Grep-verified: no refusal/cycle-check branch exists;
cycles are impossible by the rank structure, not by admission.

## 2. Battery and predictions

`b1_batt.zag` (shared, frozen): two type-1 DAGs, three B1
cross-rank attaches (B1a 4->9, B1b 7->12, B1c 9->15), three
adversarial attaches (ADV1 7->9 closing DAG 9->7; ADV2 12->12
self-loop; ADV3 raw duplicates), then checks. PREREG_AMENDMENT1.md
documents the battery design flaw found in debug (B1c/ADV1 not
cross-rank/adversarial on REP as frozen) and the fix, plus the
LIST audit 3->4 update and the `es_relocate` rank-guard bug fix.

## 3. Results (3/3 byte-identical per binary, stderr empty)

| arm | B1 line | B1D line |
|---|---|---|
| rr_ex (L2-EXTEND-XDOMAIN) | `b1a=1 b1b=1 b1c=1 a1=0 a2=0 a3=0 audit=0 vall=1 t1=12 t2=3` | `maxrank=21 promotes=7 diverge=0` + `RR-EX prom0=0` |
| rr_xs (L2-SPECIALIZE-XDOMAIN) | same B1 values | same B1D + `RR-XS prom0=0` |
| b1_rep (REP discriminator) | `b1a=0 b1b=0 b1c=0 a1=0 a2=0 a3=0 audit=0 vall=1 t1=12 t2=0` | `maxrank=11 promotes=0 diverge=0` |
| b1_list (LIST discriminator) | `b1a=1 b1b=1 b1c=1 a1=1 a2=1 a3=1 audit=4 vall=1 t1=12 t2=7` | `maxrank=11 promotes=0 diverge=0` |

E2E stack lines (before the B1 trailer) are byte-identical to
`formal_compose_e2e/ex_run_rep_1.txt` and `xs_run_rep_1.txt`:
the re-ranked store changes nothing about the learners'
end-to-end behavior except the B1 summary.

## 4. Kill bars RR1-RR6

- RR1 (B1 expressiveness): RERANK b1a=b1b=b1c=1 on both stacks;
  REP b1a=b1b=b1c=0 (genuinely B1-class); LIST b1a=b1b=b1c=1.
  PASS.
- RR2 (cycle impossibility, representational): RERANK a1=a2=a3=0
  audit=0 (adversarial attaches written, all inert; no refusal
  branch); LIST audit=4 > 0 discriminates. PASS.
- RR3 (read preservation): vall=1 on all arms (all 12 type-1 DAG
  edges stay readable through 7 promotions). PASS.
- RR4 (E2E non-regression): stack outputs byte-identical to the
  frozen E2E references. PASS.
- RR5 (determinism): 3/3 byte-identical per binary, stderr empty.
  PASS.
- RR6 (promotion accounting): promotes=7, maxrank=21, diverge=0;
  prom0=0 on both stacks (no promotion during the E2E phase
  itself). PASS.

## 5. Notes

- Implementation bug found and fixed during debug: `es_relocate`
  read head slots of unregistered items (never initialized to -1),
  hanging B1b's second promotion. Fix: rank guard matching Phase 1.
  Documented in PREREG_AMENDMENT1.md section A4.
- No-wire grep audit clean; no `!(A && B)` in while conditions;
  pure Zag; safebin pinned znc throughout.
- Commits local only, explicit pathspecs, no push.

## 6. Files

Lane `docs/lab/research-lead/overnight-20260928/formal_compose_rerank/`:
PREREG.md, PREREG_AMENDMENT1.md (both frozen), NAMECHECK.md,
`es_rerank.zag` (mechanism), `b1_batt.zag` (shared battery),
`rr_es_rep.zag` + `es_list_rr.zag` (discriminator stores),
`b1_main.zag`, `rr_prelude.zag`, `rr_driver_ex.zag`,
`rr_driver_xs.zag`, `rr_build.sh`, byte-identical E2E stack copies.
Build artifacts (`*_bin`, `rr_full_*.zag`, `b1_full_*.zag`,
`rr_compile_*.txt`) are not committed.
