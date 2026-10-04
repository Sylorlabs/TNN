# PREREG_C: cross-kind rebind (exercise c)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise c).
Date: 2026-10-02. Commit this file ALONE before any implementation.

Note: this document uses hyphens only; no em or en dashes appear.

## 1. Question

Can the continuing learner rebind a learned structure across kinds
without reset: a COUNT-kind structure (learned for counting chain
links) rebound as a CHAIN-kind procedure (assembling chain graphs) on
the same underlying facts? The core is the UNMODIFIED frozen control
core (byte copy; no instrument, no new code). All structure creation
is by the frozen trial machinery.

## 2. Base

The frozen control core
docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/clh2_core_control.zag
(SHA-256 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d),
copied byte-identical as xk_core.zag. Hash re-verified before use.
No modifications whatsoever.

## 3. Drivers (fixture only)

xk_driver_full.zag (99 events) and xk_driver_nophase.zag (69 events).
0 cognition functions, 0 structural writes, 0 new tags/edge types/
opcodes/modes/bridges/handlers. Choke points xk_event (kind 1/2/3)
and xk_query (masked/unmasked). PHASE markers are driver-side prints.
CQUERY is driver shorthand for ev_query(W,s,43,3,0): unmasked count
query with disclosed expected=3 (E-ruling: expected is post-hoc
feedback, not supervision). Masked queries use expected=-2, flags=1.

xk_driver_full.zag phases (frozen):
- CAPABILITY (24 events): 6 three-link chains
  (95001+i,21,95101+i), (95101+i,21,95201+i), (95201+i,21,95301+i),
  i=0..5 (18 teaches); then 6 CQUERY(95001+i,43,3,0) promoting COUNT
  MAPs answering 3.
- INT1 (48 events): 48 interference teaches
  (95501+i,870,95601+i), i=0..47.
- INT2 (3 events): unrelated conflict+correction:
  T(95701,871,95702), O(95701,871,95703) [contradiction, rv=0],
  T(95701,871,95703) [correction by re-teach].
- INT3 (12 events): second count family, 6 two-link chains
  (95801+i,22,95811+i), (95811+i,22,95821+i), i=0..5 (12 teaches).
- RETENTION (6 events): 6 masked queries (95001+i,43,-2,1); expect
  exact hit on the COUNT MAPs, answer 3.
- REBIND (6 events): 6 masked queries (95001+i,40,-2,1); the trial
  must assemble CHAIN graphs over the never-re-taught phase-A facts,
  promoting CHAIN MAPs answering 95201+i (b_i, the 2-hop endpoint).

xk_driver_nophase.zag (control, 69 events): elides CAPABILITY and
RETENTION; runs INT1, INT2, INT3, then REBIND. The rebind queries
must answer -2 with 0 MAPs (no phase-A structures to rebind).

All ids fresh to this battery (grep-verified). Relations 21, 22,
40, 43, 870, 871 reuse frozen-test numbers; harmless (zeroed arena
per run).

## 4. Builds and runs

xk_core.zag + xk_driver_full.zag = xk_full; xk_core.zag +
xk_driver_nophase.zag = xk_nophase. Two binaries via logged wrapper
(pre-run only). 3 reps each = 6 runs. Empty argv/env
(`bash -c 'exec -c'`; 1 process/run). Stdout + 0-byte stderr.

## 5. Frozen bars

C-R0 (count capability): 6/6 tag-20 MAPs with field8=95001+i,
 field4=43, field28=3 (white-box census).
C-R1 (rebind): 6/6 tag-20 MAPs with field8=95001+i, field4=40,
 field28=95201+i, each with type-1 DEP edges to the phase-A fact
 nodes (95001+i,21,95101+i) and (95101+i,21,95201+i) (white-box).
C-R2 (kind discriminator, the crux): via the frozen t2_sig walk,
 the 6 rebind MAP graphs contain 0 tag-103 (INC) cells each, while
 the 6 phase-A count MAP graphs contain >=2 tag-103 cells each.
C-R3 (control): xk_nophase rebind answers are -2 on all 6 queries
 (all 3 reps); 0 tag-20 MAPs with field8 in 95001..96006 and
 field4=40.
C-R4 (integrity): RETENTION answers 3 on all 6 masked (95001+i,43)
 queries (all 3 reps); FACTSTABLE: all 18 phase-A fact nodes live
 (not superseded) at end of run, 18/18 (white-box); the driver
 never re-teaches them (source audit).
C-R5 (determinism/hygiene): 3/3 byte-identical SHA-256 per binary;
 FNV stable; rc 0 on all 6; 0-byte stderr; 99 events (full) / 69
 (control) with AUDIT_PASS; capacity guard; 1 process/run; empty
 argv/env; 2 pre-run builds in wrapper log, 0 during runs.
K0/K1/K2 as in prior exercises (prereg order, safebin, fixture).

Kill: C-R2 fails (rebind graphs are count-kind) -> the cross-kind
claim is KILLED. C-R3 fails (rebind without phase-A structures)
-> structure-dependence is KILLED.

## 6. Claim bound

If PASS: a COUNT-kind learned structure is rebound as CHAIN-kind
procedure within one continuing learner, without reset, with the
kind shift discriminated white-box (t2_sig) and the dependence on
phase-A structures proven by the control. The rebind is performed
by the frozen trial machinery (not a new mechanism); caveats 1, 3,
5, 6 bind. This is L2 evidence (structural reuse across kinds),
not L3 (the trial's chain assembly is frozen machinery; the
learner does not invent the chain form).

## 7. Red team (adversarial, before verdict)

Attack: is the "rebind" real, or (a) are the CHAIN MAPs just
re-discovered from scratch (not rebound from COUNT structures)?
(b) is the trial smuggling the answer via the INT3 family or
interference facts? (c) does the control really elide the
structures? The red team audits: (i) C-R2 kind discrimination
(count graphs have INC cells, rebind graphs do not); (ii) the
rebind queries are on subjects whose ONLY chain facts are phase-A
(INT3 uses disjoint subjects; INT1 facts are single links);
(iii) the control battery's transcript and white-box census;
(iv) DEP-edge provenance (rebind MAPs cite phase-A facts, not
INT3 facts). A further attack: verify the RETENTION phase does not
itself teach the rebind (it queries r=43, not r=40; no 40-facts
are ever taught).

## 8. Decision rule

Adopt REBIND-CROSS-KIND iff C-R0 through C-R5 and K0-K2 all pass
and the red team fails to break the claim. Any kill bar failure
-> VERDICT KILLED, no salvage. Bars frozen here are never moved.
