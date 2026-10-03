# REPORT: FORMAL-COMPOSE-E2E (the actual L2 learner stacks on the
# rank-slot store, end to end)

Worker: FORMAL-COMPOSE-E2E. Date: 2026-10-03. Non-ledger task
(claim minting paused). Branch: tnn-native-lab. Commits local
only, never pushed. Lane:
docs/lab/research-lead/overnight-20260928/formal_compose_e2e/

Verdict: **BUILD-PASS** (EK1-EK7 all PASS on 3/3 byte-identical
runs, stderr empty, no new analyzer warning classes).

## 1. Question

FORMAL-COMPOSE-PORT's suggested follow-up, verbatim: "Drive the
actual L2 learner stacks (L2-EXTEND-XDOMAIN / L2-SPECIALIZE-XDOMAIN
learners) against the rank-slot store instead of their current
unconstrained edge stores, to test this port end to end." The
port proved the store works for L2-shaped attaches on a synthetic
substrate; the open question was whether the real learners'
provenance/delivery edges survive the rank rule with zero valid
attaches broken, and whether cycle-closing attaches through the
learners' own edge interface stay inexpressible.

## 2. What was built

Minimal source surgery on the actual parent stacks, with the
edge store behind a frozen interface:

- `ex_learner.zag`: l2_extend_xdomain/learner.zag with ONLY the
  flat edge-store block removed and three `es_item_new` hooks
  added (m_teach, map_create, ex_deliver). Diff-verified: no
  other learner-logic change.
- `xs_learner_e2e.zag`: l2_specialize_xdomain/xs_learner.zag
  with ONLY xs_edge removed, its two call sites renamed to
  e_add, and `es_item_new` hooks added (m_teach, xs_promote).
  Diff-verified.
- `ex_world.zag`, `xs_world.zag`: byte-identical parent copies.
- `es_rep.zag` (ARM-REP, shared): rank-slot store ported from
  FORMAL-COMPOSE-PORT pc_rep.zag, extended with edge types
  (records are child/type/next, 12B). Items 0..23 (MAP ids;
  answer-node ids 40..47 map to 16..23). Rank = creation order,
  a valid creation-time topological rank because the learners
  only ever link newer items to older ones. e_add prepends to
  head rank(to) unconditionally; read path = heads
  0..rank(P)-1. No cyclicity branch anywhere. Structural
  vocabulary only (no-wire audit clean).
- `es_list_ex.zag` / `es_list_xs.zag` (ARM-LIST): faithful
  copies of each parent's original flat edge semantics
  (EX: dedupe; XS: no dedupe), the discriminator arms.
- `ex_driver_e2e.zag` / `xs_driver_e2e.zag`: the original arms
  and in-Zag bars/falsifiers, plus a driver-issued adversarial
  battery on the FULL arm state (cycle-closing attaches via the
  learner's own e_add, plus raw-write bypass probes via
  es_raw) and the E2E summary lines.

Binaries (pinned znc 2026.07.0-dev, safebin): ex_rep_bin,
ex_list_bin, xs_rep_bin, xs_list_bin.

## 3. Kill bar results

Hand derivation matched every binary's stdout bytes exactly
before trusting them.

- **EK1 PASS** (valid extends work on the rank-slot store):
  ex_rep_bin: k1=k2=k3=k4=k5=k8=1, FALSIFIERS 0. The real
  extension behavior is unchanged on REP: learner-chosen k=4,
  Z promoted with t16 provenance 3->1, exact F-COUNT
  (A_SEARCH=272, A_EXEC=2).
- **EK2 PASS** (REP impossibility, extend): ex_rep_bin prints
  `E2E-EX t16=1 a1=0 a2=0 a3=0 t14=4 audit=0 v16=1 v14=1`.
  All 3 cycle-closing attaches + 2 raw-write bypasses are
  inexpressible (invisible to every read path); every valid
  edge stays visible.
- **EK3 PASS** (LIST discriminator, extend): ex_list_bin prints
  `E2E-EX t16=5 a1=1 a2=1 a3=1 t14=5 audit=3 v16=1 v14=1`.
  The same battery commits on the unconstrained store
  (audit=3: items 1, 3, 16 on directed cycles), so EK2 is not
  VOID.
- **EK4 PASS** (valid specializes work on the rank-slot
  store): xs_rep_bin: k1-k8 all PASS, FALSIFIERS 0. The real
  specialization is unchanged on REP: nf=3, dual provenance
  3->1 and 3->2, exact frozen F-COUNT per query.
- **EK5 PASS** (REP impossibility, specialize): xs_rep_bin
  prints `E2E-XS t16=2 a1=0 a2=0 a3=0 audit=0 v1=1 v2=1`.
- **EK6 PASS** (LIST discriminator, specialize): xs_list_bin
  prints `E2E-XS t16=7 a1=1 a2=1 a3=1 audit=3 v1=1 v2=1`
  (audit=3: items 1, 2, 3 on cycles), so EK5 is not VOID.
- **EK7 PASS** (determinism): all four binaries 3/3
  byte-identical stdout (ex_rep 051aabd8..., ex_list
  c03ac26f..., xs_rep f2175cf0..., xs_list 26709498...),
  stderr empty on all 12 runs, zero new analyzer warning
  classes (all warnings are the benign A0102/B0103/E0101/
  E0102 classes inherited from the parent lanes; the new
  store and battery code is warning-clean).

Strongest single finding: ex_rep vs ex_list (and xs_rep vs
xs_list) stdout is byte-identical EXCEPT the one E2E summary
line. The L2 learners behave identically on the rank-slot
store and their original unconstrained stores through every
arm and query; the store swap changes nothing except the
adversarial outcome.

## 4. Implementation defect found and fixed before official runs

First build read smid from SRC_ID32 after Q2B, but ex_query
resets 1268 to -1 at every query start, so the battery issued
attaches from item -1 (E2E-EX v16=0, LIST a1=0). Fixed by
capturing smid immediately after Q2 (PREREG_AMENDMENT1, committed
pre-verdict); the debug build that exposed it was discarded.
EK7's "zero warnings" phrasing was corrected to the parent
lanes' standard (PREREG_AMENDMENT2, pre-verdict). No kill bar
or hand-derived prediction changed.

## 5. What this does NOT claim

- The rank-slot store remains researcher-structured,
  learner-populated (same split as FORMAL-COMPOSE and the
  port). Constraint induction from judgments is still open.
- Creation-order rank inherits the B1 sufficient-but-not-
  necessary boundary: an acyclic attach from an older item to
  a newer one would go inert on REP. Neither learner issues
  such attaches in these worlds.
- The adversarial battery is driver-issued against the real
  learner's state, not learner-issued. One predicate
  (ACYCLIC), two L2 stacks, small battery. No generality
  claim beyond these stacks.

## 6. Follow-ups (not claimed, not started)

- Promotion-based re-ranking on link (the FORMAL-COMPOSE
  sketch): decide whether the B1 class forces an admissional
  decision somewhere, now with the real L2 stacks as the test
  bed.
- Learner-issued adversarial attaches (a learner that tries
  to close cycles through the store interface) rather than
  driver-issued probes.

## Files

formal_compose_e2e/: NAMECHECK.md, PREREG.md (frozen, committed
alone at 2761574dc before implementation), PREREG_AMENDMENT1.md,
PREREG_AMENDMENT2.md (both pre-verdict), REPORT.md (this file),
ex_learner.zag, ex_world.zag, ex_driver_e2e.zag,
xs_learner_e2e.zag, xs_world.zag, xs_driver_e2e.zag, es_rep.zag,
es_list_ex.zag, es_list_xs.zag, e2e_build.sh, ex_full_*.zag,
xs_full_*.zag (concatenated sources), ex_compile_*.txt,
xs_compile_*.txt, ex_rep_bin, ex_list_bin, xs_rep_bin,
xs_list_bin, ex_run_*_{1,2,3}.txt + .err, xs_run_*_{1,2,3}.txt
+ .err (3/3 byte-identical per binary, stderr empty).
