# REPORT: FORMAL-COMPOSE-PORT (rank-slot store as the edge store for
# live L2 attach ops)

Worker: FORMAL-COMPOSE-PORT. Date: 2026-10-03. Non-ledger task
(claim minting paused). Branch: tnn-native-lab. Commits local
only, never pushed. Lane:
docs/lab/research-lead/overnight-20260928/formal_compose_port/

Verdict: **BUILD-PASS** (K1-K5 all PASS on 3/3 byte-identical runs,
stderr empty, zero analyzer warnings).

## 1. Question

FORMAL-COMPOSE's suggested follow-up, verbatim: "Port the
rank-slot store into a live composition lane as the edge store
for L2 attach ops (extend/specialize/graft)." The synthetic
diamond substrate proved representational ACYCLIC for
`compose_link(P, C)`, but its valid probes were
assembly-shaped. The open question was whether the store works
for live L2-shaped attaches: extend (attach an independently
built extension leg under an existing composite), specialize
(attach a binding const under an existing item), graft (attach
an existing composite from a second structure under an existing
composite of the first). Two failure modes would have refuted
the port: (1) attach ops L2 reuse needs stop functioning (false
positives from the rank rule), or (2) adversarial cycle-closing
attach attempts become committable.

## 2. What was built

A port of the FORMAL-COMPOSE substrate with a two-structure
world, in four arms sharing one base and one frozen battery:

- `pc_base.zag`: arenas, MAP table (WALK/COUNT/ADD2), facts,
  item table with creation-time topological ranks, demand
  evaluation over the arm read path, the independent cycle
  audit (measurement only, identical for all arms), and the
  world builder: structure X (aggregation chain
  c->x->y/w->g, demand(g)=5), structure Y (second chain
  c2->x2->y2, demand(y2)=2), and the extension leg
  (independently built ec->ex->ew, demand(ew)=3, the L2-EXTEND
  artifact the battery attaches).
- `pc_rep.zag` (ARM-REP): the rank-slot store ported from
  fc_rep.zag: per-item rank-heads; head r holds edge records
  whose child has rank r; compose_link prepends C to head
  rank(C) unconditionally. No cyclicity branch anywhere.
  Read path = heads 0..rank(P)-1.
- `pc_gate.zag` (ARM-GATE): admissional ACYCLIC: flat edge
  list + inline reachability gate (refuse -1 if C==P or C
  reaches P). `raw_link` bypasses the gate.
- `pc_gateb.zag` (ARM-GATEB): identical store to GATE; the
  whole battery driven through raw_link (gate bypassed).
- `pc_list.zag` (ARM-LIST): unconstrained control,
  unconditional record.
- `pc_main.zag`: frozen battery (build, V1 extend, V2
  specialize, V3 graft, B1, A1..A7, A8, audit).
- `pc_blind.zag`: V0..V4 rename variants (blind attach +
  adversarial summary).

Binaries (pinned znc 2026.07.0-dev, safebin): pc_rep_bin,
pc_gate_bin, pc_gateb_bin, pc_list_bin, pc_blind_rep_bin,
pc_blind_gate_bin.

## 3. Kill bar results

Hand derivation matched every binary's stdout bytes exactly
before trusting them.

- **K1 PASS** (REP impossibility under the L2 attach
  battery): ARM-REP post-battery audit cycles=0, refusals=0.
  The 7 cycle-closing attach attempts (A1..A7: reverse graft
  cycles x<-g, self g<-g, y<-g, y2<-g after the valid graft,
  self ew<-ew, c<-y, self c2<-c2) plus the 2 raw-write bypass
  attempts (A8) all executed and committed nothing.
  Discriminator: ARM-LIST on the same battery commits
  cycles=8 (items c,x,y,w,g,c2,y2,ew), so the battery was
  genuinely adversarial; K1 is not VOID.
- **K2 PASS** (admissional gate + honest bypass boundary):
  ARM-GATE cycles=0 AND refusals=7 (A1..A7 all refused).
  ARM-GATEB (full battery via raw_link) cycles=8: bypassing
  the gate commits cycles, showing the gate, not the world,
  does the work, and that admissional is not representational
  under bypass. The REP arm survives the same bypass probe
  (cycles=0): there is no gate to bypass.
- **K3 PASS** (no false positives on L2 attach ops): ARM-REP
  valid probes: ext_link=0 ext_present=1 ext_dem=5,
  spec_link=0 spec_present=1 spec_dem=2, graft_link=0
  graft_present=1 graft_dem=5. Valid-attach refusals=0 on all
  four arms. Extend, specialize, and graft all function; the
  rank rule broke no valid attach.
- **K4 PASS** (domain blindness): V0..V4 summaries identical
  across relation permutation, subject-id permutation, kind
  polarity swap, and all three jointly (ANS=5, CYCLES=0,
  REFUSALS=0, ATT=1 on REP; REFUSALS=7 on GATE). The blind
  graft attach (ATT=1) is itself rename-invariant. No-wire
  audit: grep over pc_rep.zag and pc_gate.zag for domain
  vocabulary (walk/count/add/extend/specialize/graft/
  diamond/node/num) returns empty.
- **K5 PASS** (determinism): all six binaries 3/3
  byte-identical stdout (rep 1c6521e9..., gate a7bd6abc...,
  gateb 4648f6bf..., list 2992a915..., blind_rep 4eaf5c21...,
  blind_gate 2a742f54...), stderr empty on all 18 runs, zero
  analyzer warnings at compile (compile logs carry only the
  benign environmental `zagd unavailable` note, identical to
  the parent lane).

## 4. Boundary finding (B1, preregistered, confirmed)

B1 (cross-rank attach x<-x2, rank(x2) >= rank(x), acyclic):
REP leaves it inert (b1present=0, 0 cycles); GATE/LIST/GATEB
commit it (b1present=1). This is the rank rule's
sufficient-but-not-necessary character inherited from
FORMAL-COMPOSE, disclosed not hidden: the REP store trades
that expressiveness class for bypass-proofness, and the
composer-level fresh-node fallback covers the class.
Promotion-based re-ranking remains the sketched follow-up.

## 5. What this does NOT claim

- Not learner-induced: the rank-slot store is
  researcher-structured, learner-populated (the same split as
  FORMAL-COMPOSE and FK's prototype).
- Not absolute impossibility: FK 4.1's channel-relative
  boundary holds; the audit is measurement, not mechanism.
- One predicate (ACYCLIC), one substrate family, small
  battery. Generality across other L2 substrates is not
  shown; the full L2-EXTEND-XDOMAIN / L2-SPECIALIZE-XDOMAIN
  learner stacks were not re-run on this store.

## 6. Follow-ups (not claimed, not started)

- Promotion-based re-ranking on link (the FORMAL-COMPOSE
  sketch): zero-false-positive representational ACYCLIC, or a
  proof that the B1 class forces an admissional decision.
- Drive the actual L2 learner stacks (extend/specialize
  lanes) against the rank-slot store instead of their current
  unconstrained edge stores, to test the port end to end.

## Files

formal_compose_port/: NAMECHECK.md, PREREG.md (frozen,
committed alone before any implementation), REPORT.md (this
file), pc_base.zag, pc_rep.zag, pc_gate.zag, pc_gateb.zag,
pc_list.zag, pc_main.zag, pc_blind.zag, pc_build.sh,
pc_full_*.zag, pc_blind_*.zag (concatenated sources),
pc_compile_*.txt, pc_blind_compile_*.txt, pc_*_bin (6
binaries), pc_run_*_{1,2,3}.txt + .err (3/3 byte-identical
per arm, stderr empty), pc_blind_*_{1,2,3}.txt + .err.
