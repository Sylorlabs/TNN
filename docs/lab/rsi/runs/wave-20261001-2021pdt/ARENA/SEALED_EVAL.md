# SEALED EVALUATION (ARENA-ADVERSARY, wave-20261001-2021pdt)

Independent adversary evaluation of the frozen TCNP contestant
(bin/tcn_p, sha256 71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b,
rebuilt byte-identical from committed source; see NAMECHECK_ADVERSARY.md)
on the five sealed worlds (specs and pre-run hashes in SEALED_WORLDS.md).

Sealed battery: 50 turns (19 pshow expos, 30 ptest probes, 1 done turn).
Scoring: per hidden item, 1 if the reply string exactly equals the key,
else 0. Keys computed by mechanical rule application, never by running
the contestant.

## Per-bar results

### K1 (procedure construction): PASS, 24/24

Hidden-item exact-match accuracy on worlds A-D: 24/24 (bar: >= 18/24).
Per world: A 6/6, B 6/6, C 6/6, D 6/6. Zero abstentions, zero wrong answers
on A-D. The white-box trace confirms genuine construction per task:
A mode=construct L=2 tried=1122 nfitters=2; B mode=construct L=2
tried=1122 nfitters=2; C mode=construct L=3 tried=37059 nfitters=3.
Trial counts equal the full canonical enumeration sizes (33+1089=1122,
+35937=37059), consistent with exhaustive search, and the fitter counts
match the adversary's independent reference enumeration exactly.

### K2 (honest uncertainty): PASS, 0 confident wrong on E

World E (6-step rule, outside the K=4 bound): 6/6 replies UNKNOWN,
0 confident wrong answers, 0 coincidentally correct answers. Trace:
E mode=none tried=1222980 (the full 33+1089+35937+1185921 enumeration),
no fitter found at any length up to 4. Passes both the prereg bar
(at most 1 confident wrong) and the stricter task bar (0 confident wrong,
UNKNOWN on all E items).

### K3 (named-procedure reuse): PASS

(a) White-box trace: "TCNP solve task=D mode=rebind proc=A trials=0".
The D task rebound the procedure created during world A with zero new
search trials. The adversary verified independently that of the rules
from worlds A, B, C, only A's rule reproduces all four D shown pairs,
so the rebind target is unambiguous. (b) D hidden accuracy: 6/6
(bar: >= 5/6). Transfer demonstrated, no caveat.

### K4 (no regression): PASS

The 68-item sealed arena (seed 71503461337030) was regenerated from
committed sources (world_gen and arena hashes match the refreeze record;
turns.jsonl hash 0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469).
The v6 contestant was rebuilt from the committed v6 base source
(sha256 c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89).
Per-capability scores byte-identical between v6 and tcn_p:
54/68 = 0.794 with the identical per-capability distribution
(caps 1-7,10,11,13,14,16 at 1.000; caps 8,9,12,15 at 0.000).
The stripped reply streams are byte-identical except for the state_bytes
field (16384 v6 vs 218704 tcn_p), which is the TCNP learner-state
allocation (procedure table, trial log, verdict ring), empty on this
battery. TCNP trace empty on the battery (0 lines): the new event types
do not occur in it. No behavioral regression.

### K5 (contamination check): PASS

The builder's K7b memorization control (bin/tcn_p_memctrl, rebuilt
byte-identical from committed source; documented-hash discrepancy
resolved in NAMECHECK_ADVERSARY.md) scored 0/24 on the sealed A-D worlds
(bar: <= 6/24). The battery is not solvable by nearest shown-pair lookup.
Supporting checks: prereg commit (2026-10-02 03:33:15 UTC) strictly
precedes the adversary design window (03:55 to 04:02 UTC); the builder's
dev worlds and implementation source were never opened by the adversary;
grep audit of the mechanism source finds zero sealed-world-specific
strings (no answer keys, no sealed vectors, no sealed task linkages);
every hidden input is absent from all shown pairs and at Hamming distance
>= 2 from every shown input of its world.

### K6 (determinism): PASS

3/3 full sealed runs produce byte-identical stripped reply streams
(sha256 3ce446416c1ddb42b9cfed587827a2bac4d342a7664035ff52a9db2f7ac48a10
all three) and byte-identical TCNP traces
(sha256 77b605127e308abbf05d6a1ae6e95c2888795541988d30c99add52bdd523166f
all three). Timing fields ms and rss_kb excluded per the frozen bar.

### K7 (negative controls): PASS

(a) Ablation (bin/tcn_p_ablated, rebuilt byte-identical from committed
source): 0/24 on sealed A-D, UNKNOWN on all 30 probes. (b) Memorization
control: 0/24 on sealed A-D (bar: <= 6/24).

### K8 (wire protocol): PASS

TCNP fires only on pshow/ptest. Sealed trace: 54 lines, all TCNP lines
(19 pshow, 30 ptest, 5 solve records), zero activity on any other turn
kind. 68-item battery trace: 0 lines. The two new event types dispatch
on event type only and carry arbitrary vectors.

### K9 (architecture): PASS

Delta accounting re-verified by diffing the v6 base source against
tcn_p_contestant.zag: 585 lines added (matches the claimed 585), 8 v6
lines changed at the documented insertion points only (state size
16384 to 218704 for the learner-state allocation; event dispatch
extended for the two new prereg-specified event types). Keyword scan of
all added lines for mode/bridge/router/handler/admission/gate: 8 hits,
all benign (comments stating no new modes/bridges/routers/gates, trace
string labels "mode=construct/rebind/none", one comment on the
event-type handler). Zero new modes, zero bridges, zero routers, zero
task-specific admission gates, zero hardcoded semantic cases. The two
new handlers are the prereg section 3.4 protocol handlers dispatching on
event type only. Learner-state structures created: procedure table,
trial log, per-item verdict records (visible live in the trace and in
the grown state_bytes). Capability-source delta: the procedures live in
learner state; source contributes only the generic constructor.

## Verdict: BUILD-PASS

K1 PASS (24/24), K2 PASS (0 confident wrong), K3 PASS (rebind, trials=0,
D 6/6), K4 PASS (54/68 byte-identical, no regression), K5 PASS (0/24),
K6 PASS (3/3 byte-identical), K7 PASS (0/24, 0/24), K8 PASS, K9 PASS
(585 added, 0 new modes/bridges/routers/handlers/semantic cases).

The task's BUILD-PASS condition (K1, K2, K4, K6 all passing) is met, and
every other bar passes as well, including the K3 transfer bar, so no
transfer caveat applies.

Scope reminders (unchanged): TCNP is a CANDIDATE only. No L3 claim, no
TNN-2 substrate claim, no TNN-beats-LLM claim. The canonical 0.573 is not
moved by this result.

## Determinism evidence

- Sealed turns.jsonl sha256 (pre-run):
  a4af1bce5ea6b839fbecb0ab58eca8baf3d6cacfebe96babe0bf8ba37a14f03b
- Sealed key.txt sha256 (pre-run):
  5e8377843c04c7d561c5feba0e62f04b83d6fff54d7e27691beffc389afb0518
- 3/3 stripped reply streams: 3ce446416c1ddb42b9cfed587827a2bac4d342a7664035ff52a9db2f7ac48a10
- 3/3 traces: 77b605127e308abbf05d6a1ae6e95c2888795541988d30c99add52bdd523166f

## Toolchain

safebin PATH for the whole lane; `which python3` prints nothing
(re-verified at start); zero Python or other interpreter invocations;
shell only sequenced pinned znc, built binaries, git read ops, and file
copies. No PROCESS-FAIL event. Zero em-dash bytes in lane docs
(verified by byte scan below).
