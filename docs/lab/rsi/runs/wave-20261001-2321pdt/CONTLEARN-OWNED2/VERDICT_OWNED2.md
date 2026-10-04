# VERDICT_OWNED2: machinery-disabled integration discrimination

Wave: wave-20261001-2321pdt. Lane: CONTLEARN-OWNED2. Date: 2026-10-02.
Frozen prereg: PREREG_OWNED2.md (commit ffd31dbb3), transparently amended
by PREREG_OWNED2_ERRATUM1.md (commit 78d8c9e54; the frozen script is 98
events, STORE is 24; no tuple, oracle, bar, or decision-rule change).
Implementation strictly descendant of both; merge-base ancestry verified.

## Per-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| CO-1 TREAT integrates to the DEMONSTRATED bar | FAIL | STORE_OK_T 0/6 (need 6); REUSE_OK_T 6/12 (need 12); DELAYED_OK_T 6/12 (need 12) |
| CO-2 learner's own mechanisms identified | PASS | Census 3/3 consistent; failure signature unambiguous (see below) |
| CO-3 determinism | PASS | 3/3 byte-identical per binary (TREAT 27676a22..., CONTROL 8454f6dbe...); FNV equal across reps; rc=0; 0 stderr bytes; AUDIT_PASS; no PID/timestamps/paths |
| CO-4 control reproduces DEMONSTRATED | PASS | STORE_OK_C 6/6; REUSE_OK_C 12/12; DELAYED_OK_C 12/12; MAPC=6; UNC=0 |
| CO-5 machinery truly absent | PASS | (a) diff = exactly the six deleted lines; (b) caller analysis: no event-interface path reaches the five machinery functions; (c) TREAT MAPC=0 at all three censuses |
| K0 commit order | PASS | Prereg ffd31dbb3 and erratum 78d8c9e54 both strict ancestors of the implementation commit (note below) |
| K1a one learner, no reset | PASS | 6 official processes (3 TREAT + 3 CONTROL), one per 98-event run; pid_leak_check=0; 6 pilot processes disclosed and voided in the erratum |
| K1b builds logged | PASS | Fresh znc_invocations_ow.log: exactly 2 entries pre-run, 0 new during runs |
| K1c audit, no task labels | PASS | AUDIT_PASS 98/98 on all 6; choke points; masked queries expected=-2, flags=1; empty argv and env |
| K2a frozen ISA boundary | PASS | a29972ca... before implementation, before builds, after runs; working-tree blob b226b223c equals the f4de7ff46 blob (note below) |
| K2b driver audit | PASS | 0 cognition functions; 0 ns(/link_edge/alloc_node; 0 new tags/edges/opcodes/modes/bridges; 0 switch/match |
| K2c source delta | PASS | Cognition lines added 0, deleted 0, net 0; variant is a lane-dir measurement instrument |
| K2d pure Zag | PASS | Zero Python/C/JS/Rust; `which python3` empty under safebin PATH (NAMECHECK.md Step 0) |
| K3 no regression | PASS | Committed 2321pdt lo_driver 3x TREAT: stdout 1ff527fa... matches the recorded value on all 3 reps |

K0 note: the prereg commit ffd31dbb3 briefly swept in two already-staged
files from the RT-SENSE lane (staged by another worker, unrelated to this
lane); the tree was verified correct afterward, and no implementation
file of this lane existed at or before that commit. The commit-order
self-check (the substantive requirement) holds.

K2a note: the frozen path is currently untracked at HEAD, a side effect of
the LANE-AUDIT repair sweep that rewrote recent history. The working-tree
bytes are verified identical to the frozen blob (sha256 a29972ca...,
git blob b226b223c). This worker never wrote to the frozen path.

## Verdict

**MACHINERY-DEPENDENT.** CO-4, CO-5, K0, K1, K2, K3, and CO-3 pass; CO-1
fails. Per the frozen decision rule: the learner does not integrate the
new experience without the researcher machinery; the red-team QUALIFY
stands; integration is machinery-dependent.

## CO-2 white-box evidence: which mechanisms did the work

TREAT (machinery verified absent), all three reps identical:

- STORE phase: the 6 family-D integrate queries all returned -2 (true
  miss). Census: MAPC=0, UNC=6, GUIDEC=6. Zero MAP structures were created
  on any D probe.
- REUSE phase: D_HIT 0/6, D_MISS 6/6; family E served 6/6 by standing
  retrieval via `activate`. Census: MAPC=0, UNC=12, GUIDEC=12.
- DELAYED phase: D_HIT 0/6, D_MISS 6/6; family E 6/6 again. Census:
  MAPC=0, UNC=18, GUIDEC=18.
- DEPC equals GUIDEC at every census (6/12/18): the only type-1 edges
  ever written are the guide-to-UNCERTAINTY links from `miss_inquire`.

The kept learner-side mechanisms behaved exactly as the frozen core
defines them and nothing more: `ev_teach` stored the taught facts (N1
grew 24 -> 60 -> 86 across the teaches); `activate` served pre-existing
facts (family E 6/6 in every probe phase, proving the variant is otherwise
functional); `miss_inquire` reified one UNCERTAINTY node and one guide per
miss (18 each, the only learner-side response to the chain experience).
No kept mechanism constructs a MAP, a DEP citation, or any chain
structure.

CONTROL (unmodified frozen core), all three reps identical:

- STORE_OK 6/6: six MAP(9501+i,702) nodes with alive DEP edges to the
  licensing chain facts, all six integrate queries answered 9101+i.
- REUSE_OK 12/12 and DELAYED_OK 12/12; UNC=0, GUIDEC=0 throughout: no miss
  path was ever taken.

The discrimination is clean: the identical 98-event battery integrates
6/6 chains with the machinery present and 0/6 with it verified absent,
while standing retrieval is intact in both.

## Root-cause analysis (per the no-patch-treadmill rule)

The frozen core provides no learner-invoked path from a miss to structure
construction. The only responses to a query miss that create integrating
structure are the researcher event-triggered machinery
(mp_run/t2_trial/t2_try_verify/promote_graph/bootstrap_miss). With that
machinery unreachable, a miss can only be served by pre-existing standing
structure or reified as UNCERTAINTY plus a guide, and neither constructs
chains. Notably, the UNCERTAINTY/guide machinery, the strongest candidate
for a learner-owned integration path, does not feed back into
integration: 18 guides accumulate across the run, but no mechanism reads
them to build anything. The integration work sits entirely on the
researcher side of the control-plane line. This strengthens the red-team
QUALIFY with a clean discrimination rather than weakening it.

What this verdict does NOT claim: no statement about learner agency in
the causal sense (H2-v2/H3 stand); no procedure execution at query time;
no L3 and no generality; the variant core is a measurement instrument,
not a proposed architecture. The script is disclosed, not a sealed
adversarial world.

## Follow-ups for the coordinator

- None required by this lane beyond the standing direction: the open
  question is what general learner-owned memory representation or policy
  would let one frozen learner initiate structure construction from its
  own state (the continuing-learner HIGH PRIORITY item), since this
  discrimination shows the current miss path has no such initiation point.
- Per the no-patch-treadmill rule, this MACHINERY-DEPENDENT result is
  followed by root-cause analysis (above), not by new handlers, modes, or
  opcodes.
