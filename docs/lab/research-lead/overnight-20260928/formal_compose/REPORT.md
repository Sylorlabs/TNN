# REPORT: FORMAL-COMPOSE (P6 ACYCLIC constraints for DAG composition)

Worker: FORMAL-COMPOSE. Date: 2026-10-03. Non-ledger task (claim
minting paused). Branch: tnn-native-lab. Commits local only, never
pushed. Lane:
docs/lab/research-lead/overnight-20260928/formal_compose/

Verdict: **BUILD-PASS** (K1-K5 all pass on 3/3 byte-identical runs,
stderr empty, zero analyzer warnings).

## 1. Question

FORMAL-KNOWLEDGE P6: on the composition edge store, make
cycle-closing compose attempts impossible rather than avoided, so
the composer can attempt fan-out and diamond assemblies freely.
The gap found in the substrates: COMPOSE-SUSPEND-1 and
COMPOSE-BACKCHAIN-1 compose only through fresh-node interning
(monotonic tids), so their thunk stores are DAGs by construction,
but they have NO link-existing-existing operation. That operation
is what L2 adaptive reuse needs (attach an existing structure as a
dependency of an existing composite without rebuilding), and today
nothing constrains it: linking P -> C where C transitively depends
on P would commit a directed cycle.

## 2. What was built

A composition edge store with the missing `compose_link(P, C)`
operation, in four arms sharing one substrate and one frozen
battery:

- `fc_base.zag`: arenas, MAP table (WALK/COUNT/ADD2), facts, node
  table with creation-time topological ranks, demand evaluation
  over the arm read path (SUSPEND's on-stack guard kept), the
  independent cycle audit (measurement only, identical for all
  arms), the PAIR6 diamond world builder with permutation flags.
- `fc_rep.zag` (ARM-REP): representational ACYCLIC. Per-item
  rank-heads; head r holds edge records whose child has rank r.
  `compose_link` prepends C to head rank(C), unconditionally. No
  branch on cyclicity exists anywhere in the file: no
  reachability, no visited sets, no graph search. Read path =
  heads 0..rank(P)-1 only, so a cycle-closing write lands outside
  the interpreted prefix and denotes no dependency. Proof: every
  readable edge goes from strictly higher to strictly lower rank,
  so the read graph is acyclic for ANY operation sequence,
  including raw writes.
- `fc_gate.zag` (ARM-GATE): admissional ACYCLIC. Flat edge list +
  inline reachability gate on compose_link (refuse -1 if C==P or
  C reaches P). `raw_link` bypasses the gate.
- `fc_gateb.zag` (ARM-GATEB): identical store to GATE; the whole
  battery driven through raw_link (gate bypassed throughout).
- `fc_list.zag` (ARM-LIST): unconstrained control, unconditional
  append.
- `fc_main.zag`: frozen battery (build, V1, V2, V3, V5, V4, B1,
  A1..A8, audit). `fc_blind.zag`: V0..V4 rename variants.

Binaries (pinned znc 2026.07.0-dev, safebin): fc_rep_bin
(6090731d...), fc_gate_bin (c79de142...), fc_gateb_bin
(b1547860...), fc_list_bin (95466c5b...), fc_blind_rep_bin
(2c58b84d...), fc_blind_gate_bin (70570bde...).

## 3. Kill bar results

Hand derivation matched every binary's stdout bytes exactly
before trusting them.

- **K1 PASS** (REP impossibility): ARM-REP post-battery audit
  cycles=0, refusals=0. The 7 cycle-closing attempts (A1..A7) plus
  the 2 raw-write bypass attempts (A8) all executed and committed
  nothing: `FC-ADV cycles=0 refusals=0`. Discriminator:
  ARM-LIST on the same battery commits cycles=5 (nodes c,x,y,w,g),
  so the battery was genuinely adversarial; K1 is not VOID.
- **K2 PASS** (GATE admissional + honest boundary): ARM-GATE
  cycles=0 AND refusals=7 (A1..A7 refused; A8 not run on this arm
  per the frozen prereg). ARM-GATEB (full battery via raw_link)
  cycles=5: bypassing the gate commits cycles, showing the gate,
  not the world, does the work, and that admissional is not
  representational under bypass. The REP arm survives the same
  bypass probe (cycles=0): there is no gate to bypass.
- **K3 PASS** (no false positives): ARM-REP valid probes
  v1=5 v2=5 v3=3 v4dem=5 v5=5 (diamond, fan-in join, chain, L2
  attach, fresh rebuild); V4 edge present in the read graph
  (v4present=1); valid-link refusals=0. No committed cycle, no
  uncommitted valid probe.
- **K4 PASS** (domain blindness): V0..V4 summaries identical
  across relation permutation, subject-id permutation, kind
  polarity swap, and all three jointly (ANS=5, CYCLES=0,
  REFUSALS=0 on REP; REFUSALS=7 on GATE). No-wire audit: grep
  over fc_rep.zag and fc_gate.zag for domain vocabulary
  (walk/count/add/diamond/fanout/fanin/chain/node/num) returns
  empty.
- **K5 PASS** (determinism): all six binaries 3/3 byte-identical
  stdout (rep b12f6ebf..., gate 7d72ae0c..., gateb 5d05ff86...,
  list ce9d36eb..., blind_rep babf6487..., blind_gate 016d2362...),
  stderr empty on all 18 runs, zero analyzer warnings at compile.

## 4. Implementation defect found and fixed before official runs

First build ran A8 (raw bypass writes) on all four arms; GATE
then showed cycles=5, contradicting the frozen K2 ("A8 not run on
this arm"). The prereg was correct and the implementation was
wrong: A8 is the bypass probe and belongs to REP (must stay
inexpressible), GATEB, and LIST, not to GATE-inline. Fixed by an
arm-defined `do_a8()` flag (REP 1, GATE 0, GATEB 1, LIST 1);
rebuilt; all official 3/3 runs are post-fix. No prereg change was
needed or made. Disclosed here per the defect-reporting norm.

## 5. Boundary finding (B1, documented in prereg, confirmed)

B1 (acyclic cross-rank attach link(x,x2), rank(x2) >= rank(x)):
REP leaves it inert (b1present=0, 0 cycles); GATE commits it
(b1present=1). This is the rank rule's sufficient-but-not-
necessary character, exactly as preregistered: the REP store
trades that expressiveness for bypass-proofness, and the
composer-level fallback (fresh-node composition, total)
covers the case, demonstrated by f2=app2(m3,g,y2) with
demand=7 on all arms. Notably the comparison cuts both ways:
GATE's reachability is precise where REP is coarse, but GATE
collapses under bypass while REP does not. A promotion-based
re-ranking design is the sketched follow-up, not built here.

## 6. What this does NOT claim

- Not learner-induced: the rank-slot store is
  researcher-structured, learner-populated (the same split as
  FK's prototype). Constraint induction from judgments and the
  representation-migration step remain FORMAL-KNOWLEDGE
  follow-ups.
- Not absolute impossibility: FK 4.1's channel-relative boundary
  holds; the audit is measurement, not mechanism. The
  protected-core gate variant remains Micah's boundary decision.
- One predicate (ACYCLIC), one substrate family, small battery.
  Generality across other composition substrates is not shown.
- The B1 boundary (section 5) is a real expressiveness limit of
  the fixed-rank design, disclosed not hidden.

## 7. Follow-ups (not claimed, not started)

- Promotion-based re-ranking on link (sketch in PREREG 7):
  zero-false-positive representational ACYCLIC, or a proof that
  the B1 class forces an admissional decision somewhere.
- Port the rank-slot store to a live composition lane as the
  edge store for L2 attach operations (extend/specialize/graft).
- P4/P5/P7 of FORMAL-KNOWLEDGE (stale-constraint recovery,
  rename battery on the prototype, BOUND) remain open.

## Files

formal_compose/: NAMECHECK.md, PREREG.md (frozen, committed
fa768f682 before any implementation), REPORT.md (this file),
fc_base.zag, fc_rep.zag, fc_gate.zag, fc_gateb.zag, fc_list.zag,
fc_main.zag, fc_blind.zag, fc_build.sh, fc_full_*.zag,
fc_blind_*.zag (concatenated sources), fc_compile_*.txt,
fc_blind_compile_*.txt, fc_*_bin (6 binaries),
fc_run_*_{1,2,3}.txt (3/3 byte-identical per arm, stderr empty),
fc_blind_*_{1,2,3}.txt.
