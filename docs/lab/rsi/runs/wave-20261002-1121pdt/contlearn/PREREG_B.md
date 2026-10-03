# PREREG_B: learner-scheduled initiation (exercise b)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise b).
Date: 2026-10-02. Commit this file ALONE before any implementation.

Note: this document uses hyphens only; no em or en dashes appear.

## 1. Question

Caveat 2 binds: proposal initiation is event-triggered, not
learner-scheduled. This exercise measures whether the learner itself
can schedule WHEN to initiate a learning episode (a proposal) from its
own accumulated uncertainty state, vs harness-prompted scheduling
wearing a costume (firing at a fixed position regardless of state).

## 2. Base and instruments

Base: the frozen treat core
docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/clh2_core_treat.zag
(SHA-256 627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63).
Hash re-verified before derivation. The treat core is used (not the
control core) because it carries the proposal-first gate
(pf_propose/pf_find/pf_mp_run).

sc_core_treat.zag (learner-scheduled instrument). Two changes to the
base, nothing else:
(a) The auto-propose in ev_query is REMOVED: the lines
    `let prop:i32=pf_find(W,s,r); if(prop<0){ prop=pf_propose(W,s,r); }`
    are deleted. pf_mp_run (unchanged) then refuses engagement
    (MACHINERY_SKIPPED) when no live proposal exists; the miss path
    reaches miss_inquire which reifies UNCERT nodes. After this change
    the ONLY writer of proposals is sc_sched_scan.
(b) New core function sc_sched_scan(W, evidx). After every event it
    scans learner state: it finds a subject s with at least K=3 live
    UNCERT nodes (tag-30, field24==850, field20==s, s!=0) for the
    watched kind 850, and checks via pf_find that no live proposal for
    (s,850) exists. If both hold it prints
    `SCHED_FIRE unccount=<u> evidx=<evidx> s=<s>` and calls
    pf_propose(W,s,850). Otherwise it does nothing. K=3 frozen here.
    The scan cadence (once per event, uniform) is fixed and disclosed;
    the FIRING DECISION is a pure function of learner state. No new
    node tags, edge types, opcodes, modes, bridges, or handlers.

sc_core_costume.zag (harness-costume control). Same ev_query change as
(a). sc_sched_scan fires iff evidx==12, regardless of learner state:
it prints `SCHED_FIRE unccount=<u> evidx=12 s=98301` (u counted for
reporting only) and calls pf_propose(W,98301,850). This is the
researcher-hardcoded schedule wearing the scheduler's costume.

## 3. Drivers (fixture only)

sc_driver_a.zag (schedule A, 20 events) and sc_driver_b.zag (schedule
B, 96 events). 0 cognition functions, 0 structural writes, 0 new
tags/edge types/opcodes/modes/bridges/handlers. Each event goes through
the choke point sc_event(W,kind,s,r,o) which calls the frozen event
API, increments the hg(W,52) event counter, then calls
sc_sched_scan(W, hg(W,52)) uniformly. The drivers NEVER call
pf_propose or pf_find (B-S2 audit). PHASE markers are driver-side
prints; cognition receives only integer tuples. Masked queries use
expected=-2, flags=1 (supervisor-disconnect, disclosed; not a task
label). Kind 3 is ev_observe, the frozen counterexample protocol.

Schedule A (20 events):
 ev 1: T 98301 860 98311
 ev 2: T 98311 861 98321
 ev 3: Q 98301 850  (miss 1)
 ev 4: Q 98301 850  (miss 2)
 ev 5: Q 98301 850  (miss 3; scheduler fires, SCHED_FIRE evidx=5)
 ev 6: Q 98301 850  (episode: proposal exists, trial chains the
         860/861 facts, MAP for (98301,850), answer 98321)
 ev 7-14: T 99001+i 870+(i mod 5) 99101+i, i=0..7 (interference)
 ev 15-20: Q 99001+i 870+(i mod 5) exact, i=0..5 (interference)

Schedule B (96 events):
 ev 1: T 98301 860 98311
 ev 2: T 98311 861 98321
 ev 3-20: T 99001+i 870+(i mod 5) 99101+i, i=0..17 (18)
 ev 21: Q 98301 850  (miss 1)
 ev 22-51: T 99019+i 870+(i mod 5) 99119+i, i=0..29 (30)
 ev 52: Q 98301 850  (miss 2)
 ev 53-82: T 99049+i 870+(i mod 5) 99149+i, i=0..29 (30)
 ev 83: Q 98301 850  (miss 3; scheduler fires, SCHED_FIRE evidx=83)
 ev 84: Q 98301 850  (episode: chain MAP, answer 98321)
 ev 85-96: Q 99001+i 870+(i mod 5) exact, i=0..11 (12)

All ids and the relations 860, 861, 870-874 are fresh to this battery
(grep-verified before writing). Relation 850 reuses the CLH2 number;
harmless (zeroed arena per run, separate processes). Interference
events never touch relation 850 and never miss on 850.

## 4. Builds and runs

Combined sources: sc_core_treat.zag + sc_driver_a.zag,
sc_core_treat.zag + sc_driver_b.zag, sc_core_costume.zag +
sc_driver_a.zag, sc_core_costume.zag + sc_driver_b.zag. Four binaries
(sc_treat_a, sc_treat_b, sc_costume_a, sc_costume_b) built once via a
logged znc wrapper (pre-run only). 3 reps each = 12 runs. Empty argv
and empty env per run (`bash -c 'exec -c'`; exactly 1 process per
run). Stdout + 0-byte stderr captured per run.

## 5. Frozen bars

B-S0 (state-driven firing + episode): in sc_treat_a and sc_treat_b,
 the SCHED_FIRE line shows unccount=3; exactly 1 PROPOSAL line with
 r=850 appears; the episode query is answered 98321; a white-box
 oracle confirms a tag-20 MAP with field8=98301, field4=850,
 field28=98321, with type-1 DEP edges to both chain-fact nodes
 (98301,860,98311) and (98311,861,98321) and a type-1 edge to the
 proposal node (EPISODE_OK 1/1).
B-S1 (schedule-independence, the crux): |evidx_A - evidx_B| = 78
 (5 vs 83), >= 50. A fixed-position firing hypothesis predicts
 evidx_A == evidx_B; the observed separation kills it.
B-S2 (no harness scheduling): the frozen driver sources contain 0
 occurrences of pf_propose and 0 of pf_find (grep audit); the only
 proposal writer in the linked binaries is sc_sched_scan (call-site
 audit: exactly 1 pf_propose call site per core).
B-S3 (costume control): sc_costume_a and sc_costume_b both print
 SCHED_FIRE with evidx=12; fire-time unccount is 3 in schedule A
 and 0 in schedule B. The costume fires identically with and
 without the triggering state, proving state-blindness.
B-S4 (determinism/hygiene): 3/3 byte-identical SHA-256 per binary;
 FNV stable per binary; rc 0 on all 12; 0-byte stderr on all 12;
 20 events (AUDIT_PASS) in schedule A runs, 96 in schedule B runs;
 capacity guard (nodes < 900, edges < 3500); 1 process per run;
 empty argv/env; 4 pre-run builds in the wrapper log, 0 during runs.
K0 (prereg commit-order): this prereg's first commit strictly
 precedes every implementation file's first commit (self-check
 before verdict).
K1 (toolchain): safebin PATH; which python3 resolves to nothing.
K2 (fixture): drivers hold 0 cognition functions (audit).
K3 (no regression): the unmodified treat core + k3 driver gives
 TOTAL p/t; sc_core_treat and sc_core_costume + k3 driver must pass
 every test the unmodified treat core passes (no new failures).
 Additional failures attributable solely to the intentional
 auto-propose removal are documented and do not fail K3; any
 failure NOT so attributable is K3-FAIL and VOIDs the lane.

Kill: B-S0 or B-S1 fails -> the scheduling claim is KILLED
(scheduling is not learner-state-driven).

## 6. Claim bound

If PASS: the learner schedules proposal initiation from accumulated
uncertainty state (timing is state-driven and schedule-independent).
The proposal CONTENT stays a fixed researcher template (caveat 1);
the scan cadence is fixed and disclosed; the scheduler does not
choose WHAT to learn about beyond the UNCERT subject. Caveats 1, 3,
4, 5, 6 bind as before. This is L2 evidence (state-driven control
of initiation timing), not L3, not agency.

## 7. Red team (adversarial, before verdict)

Attack: is the "scheduling" real, or is the driver smuggling the
timing (e.g., calling the scan selectively, or the fire position
being determined by the schedule layout rather than the state)?
The red team audits: (i) the driver calls sc_sched_scan uniformly
after EVERY event (no conditional); (ii) B-S1 separation across two
schedules with different miss positions; (iii) the costume control;
(iv) the call-site audit (scheduler is the sole proposal writer);
(v) white-box confirmation that fire-time state (unccount=3) holds
in both schedules. A further attack the red team must attempt: run
the treat core on a schedule where 3 UNCERTs NEVER accumulate and
confirm NO fire occurs (negation control). This is executed as an
ad-hoc red-team probe (not a verdict input): if the scheduler fires
without the state, the claim dies.

## 8. Decision rule

Adopt SCHEDULING-STATE-DRIVEN iff B-S0, B-S1, B-S2, B-S3, B-S4 and
K0-K3 all pass and the red team fails to break the claim. Any kill
bar failure -> VERDICT KILLED, no salvage. Bars frozen here are
never moved after.
