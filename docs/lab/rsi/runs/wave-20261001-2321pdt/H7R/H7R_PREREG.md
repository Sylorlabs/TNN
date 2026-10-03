# H7R PREREG: contradiction-driven re-derivation on the prototype substrate

Lane: H7R, wave wave-20261001-2321pdt. Status: FROZEN (this commit). No implementation
exists at freeze time; world tables are committed strictly after this freeze.

Lineage: TNN3H7 SUBSTRATE-ABSENT (wave-20261001-2021pdt: no learner construction
process, no contradiction-to-construction trigger, prereg never frozen);
TNN3-SUBSTRATE DESIGN-COMPLETE (wave-20261001-2321pdt: generic contradiction
trigger lt_fire plus construction service lb_run, kill bars KB-H7R frozen in
SUBSTRATE_PREREG.md section 8).

## 1. Hypothesis

H7 (from HYPOTHESES.md): revision as re-derivation from live facts. The contradiction
marks the old derivation superseded and the learner's construction process runs again
against the current fact store. The substrate lane supplied the two missing pieces as
generic machinery: (4B) lt_fire reifies every fact contradiction as a REDERIVE ticket
(904, field24 = -43) linking the superseded and the new fact; (4A) lb_run
materializes pending BUILD tickets into executable 4-op ISA graphs. The substrate
lane's honest boundary: ticket authoring by the learner and REDERIVE interpretation
are this re-attempt's hypothesis, not the package.

H7R hypothesis: a generic learner-side consumer that interprets REDERIVE tickets
suffices for genuine re-derivation through the trigger plus the construction service,
with no researcher-authored ticket content and no substrate modification. If the
trigger fires but the re-derived structure cannot be authored and executed through
the generic service, the verdict is SUBSTRATE-INSUFFICIENT with the exact gap named,
not a workaround with researcher-authored re-derivation.

## 2. The consumer (frozen specification of REDERIVE interpretation)

The consumer is generic machinery: it branches only on structural metadata (node
tags, field offsets, edge types, ticket markers -41/-43, status codes, the
substrate's own supersession signal). It contains no domain constants and no
per-world branches. All ticket content (keys, values, topology) is read from learner
state: fact node fields and stale ticket steps.

(a) Derive mode h7_derive(W, f): for a taught fact f, authors one BUILD ticket
(904, R_BUILD) with the fixed generic schema [BEQ(slot0, lit(field20)) true-target
SET(slot1, lit(field28))], i.e. steps (102, 1000, s, -2) then (101, 1001, o, 0).
This schema is a fixed generic prior mirroring the substrate's own fact query
semantics (activate matches field20/field24, ev_query yields field28). It is
identical for the stale and the re-derived graph, so it cannot explain any measured
difference between them. After lb_run builds the ticket, the consumer links the
ticket to its source fact with an ET_REF edge (added post-build, so the ticket's
first ET_REF target remains its first step).

(b) Rederive mode h7_rederive_one(W, t): for a pending REDERIVE ticket t, collects
its ET_REF targets and identifies the old fact (superseded: ET_CON self-edge via
is_superseded) versus the new fact, order-independently. Marks the ticket consumed
(field28 = 1). If no BUILD ticket is linked to the old fact, consumes the ticket and
authors nothing (distractor path). Otherwise authors one new BUILD ticket by walking
the stale ticket's step chain and emitting one step per stale step with literal
re-resolution: a literal spec equal to the superseded fact's field28 (the value, the
only field a contradiction can change through the event interface, since (s, r) are
matched by activate) is replaced by the new fact's field28; frame-slot codes
(>= 1000) and back-refs (< 0) pass through unchanged. Marks the stale BUILD ticket
superseded (field28 = 2). The new ticket is pending; the substrate's lb_run
materializes it (invoked by the harness; the service, not the content, is the
substrate's).

(c) Learner-side authoring criterion (falsifiable, audited by grep): the sealed
driver never calls lb_ticket_new or lb_step_add. Every ticket in the experiment is
authored by the consumer from learner state. If grep finds either call in the driver
source, the authorship bar fails by construction and the verdict is BUILD-FAIL
(researcher-authored tickets, the 2021pdt failure mode).

## 3. Sealed worlds (values committed post-freeze)

Three fresh sealed worlds, each run in a fresh workspace. Per world: one relation
code R, four contradiction cases (k_i, R, v_i) with genuine contradictions
(k_i, R, v_i_prime) where v_i_prime != v_i, and two distractor facts (d_j, R, u_j)
with contradictions (d_j, R, u_j_prime) that have no derivation. World value
constraints (frozen): all keys and values in 1..999 (values >= 1000 are frame-slot
codes in the ticket spec encoding); within each case, key, old value and new value
are pairwise distinct (disambiguates the generic re-resolution rule); keys unique
within a world. The exact values are chosen when the driver is written, after this
freeze, and committed in the implementation commit. Tuning the worlds to the
consumer is structurally impossible: the consumer contains no domain constants, so
no world value can interact with a consumer branch.

Protocol per world, all through the event interface plus the consumer and the
substrate service:
1. Learning: ev_teach each case and distractor fact. For each case fact only, run
   h7_derive, then lb_run, then link ticket to fact. Assert each ticket built
   (field28 = 1) and each stale root executes correctly on the frozen ISA (frame
   slot0 = k_i yields slot1 = v_i). Assert zero REDERIVE tickets exist.
2. Contradiction: per case, ev_observe(k_i, R, v_i_prime) (must take the
   contradiction branch), then h7_rederive_one on the pending REDERIVE ticket, then
   lb_run. Assert exactly one REDERIVE ticket was added by the event and that it
   links the superseded and the new fact (one ET_REF target superseded, one not).
   Per distractor, ev_observe(d_j, R, u_j_prime), then h7_rederive_one: must consume
   the ticket and author zero BUILD tickets.
3. Confirms: ev_observe(k_i, R, v_i_prime) again for all cases (confirm branch).
   Assert the REDERIVE ticket count is unchanged and no BUILD ticket is authored.
4. Held-out probe: the probe frames were never presented during learning or
   contradiction (construction saw only facts, never query frames). For each case:
   execute the re-derived root (expect return 1, slot1 = v_i_prime); execute the
   stale root (expect return 1, slot1 = v_i, the superseded value); compare
   t2_sig(stale root) against t2_sig(re-derived root).

## 4. Frozen kill bars

KB-H7R from SUBSTRATE_PREREG.md section 8, unweakened, plus the task-specified
additions. Twelve contradiction cases total (3 worlds x 4).

- B1 substrate: every ev_observe contradiction on the scripted sequences yields
  exactly one REDERIVE ticket linking the superseded and the new fact. Measured two
  ways: the adopted build's dv_v2() re-run passes, and the per-event count/link
  asserts in the protocol pass. Confirms and pure teaches yield none.
- B2 sealed: the re-derivation consumer rebuilds via lb_run against the live fact
  store; post-contradiction held-out probe queries executed on the frozen ISA
  return the corrected answer on at least 80 percent of cases (frozen margin:
  accuracy(re-derived) >= 80 percent AND accuracy(re-derived) minus
  accuracy(stale-vs-corrected) >= 60 percentage points).
- B3 non-treadmill: the rebuilt graph's t2_sig signature differs from the stale
  graph's signature on at least 80 percent of contradiction cases. Per H7's own
  falsifiable prediction, re-learning the same wrong thing is the killed outcome:
  KILL if B3 below 80 percent, with no repair lineage.
- B4 ablation: without the rebuilt graph, answers stay stale. Executing the stale
  (superseded) root on the probe returns the superseded value on 100 percent of
  cases.
- B5 confirms: confirm events trigger zero REDERIVE tickets and zero consumer
  authoring (count asserts in protocol step 3).
- B6 distractors: contradictions on facts with no derivation are consumed with
  zero BUILD tickets authored.
- P1 determinism: the sealed binary is run 3 times; stdout is byte-identical
  across all 3 runs (sha256 equality).
- P2 K-C0A audit: zero new semantic cases. Audit by committed-source grep:
  (i) every conditional in the appended consumer/driver code is classified as
  structural (tags, field offsets, edge types, ticket markers, status codes, loop
  bounds) or measurement (probe scoring comparisons against expected values);
  (ii) no world-table constant appears in any conditional test outside measurement
  scoring; (iii) no new node types, edge types, or relation codes beyond the
  package's 904/902/101-104 and -41/-43; (iv) the driver contains zero
  lb_ticket_new/lb_step_add calls (same grep as section 2c).

## 5. Verdict rules

- BUILD-PASS iff B1 and B2 and B3 and B4 and B5 and B6 and P1 and P2 all pass.
- BUILD-FAIL with killing evidence if any bar fails; B3 below 80 percent kills the
  H7 re-derivation hypothesis per its own prediction (no repair).
- SUBSTRATE-INSUFFICIENT iff the trigger fires (B1 passes) but authoring or
  executing the re-derived structure through the generic service proves impossible;
  the report names the exact missing primitive or blocking interaction. No
  researcher-authored workaround is permitted as a substitute.
- No L3 authorship claim is made or needed for BUILD-PASS; the verdict concerns
  the re-derivation mechanism against the frozen bars.

## 6. Commit order (frozen with this prereg)

This prereg is committed alone. The implementation commit (world tables, consumer,
driver, extracted substrate, build script) follows strictly after. The sealed run
executes only after both commits. Amendments, if any bar proves unexecutable as
written, are transparent and re-frozen; no bar moves silently.
