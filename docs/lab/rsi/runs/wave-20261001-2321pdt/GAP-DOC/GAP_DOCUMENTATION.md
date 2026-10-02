# Verified mechanism gap: learner cannot initiate structure construction in frozen TNN-2

Wave: wave-20261001-2321pdt. Lane: GAP-DOC (documentation only).
Sources, read-only, not modified:
- docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/LEARNER_MECH_ANALYSIS.md (168 lines)
- docs/lab/rsi/runs/wave-20261001-2321pdt/MECH-VERIFY/MECH_VERIFY_REPORT.md

This document is the verified problem statement for Micah's TNN-3 governance
decision. It proposes no patch, handler, mode, bridge, or opcode. No new
experiments were run. Note: no em-dashes or en-dashes are used in this document.

Frozen source under analysis: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
commit f4de7ff46, 1591 lines. Git blob hash b226b223cb3ee0be742af673653fb8ea8605f281
(verified identical via `git hash-object` on the working-tree file and via
`git show f4de7ff46:<path>`; MECH-VERIFY CONFIRMED source identity as a prerequisite).

## 1. The verified fact

In frozen TNN-2, no learner-created state can initiate structure construction.
Every structure-construction call path in the cognitive region is rooted in a
researcher-invoked event handler or in a self-test. Learner state is read as
DATA (by `t2_gather`, `activate`, and `ev_act` bid selection) but never as
CONTROL. Nothing in learner state can gate, enable, defer, retry, redirect,
or re-invoke the construction machinery.

All three LEARNER-MECH claims were independently verified by MECH-VERIFY with
exact call-site evidence, verdict CONFIRMED on each:

- Claim 1 (call-site inventory of the construction path): CONFIRMED. Every
  count matched exactly.
- Claim 2 (`mp_set`/`mp_get` only in tests; `mp_run` never reads the mp slot):
  CONFIRMED.
- Claim 3 (four event entry points only; no learner-state path back into
  construction): CONFIRMED.

The empirical discrimination this explains: with the event-triggered
trial/promotion/P-INV machinery removed from the query path, the continuing
learner integrated 0/6 fresh 2-hop chains (all 18 family-D probes took the
true miss path; zero MAP nodes; only UNCERTAINTY/guide accumulation), while
the unmodified frozen core integrated 6/6 with 6 MAPs and 24 machinery-written
DEP edges. Taught 1-hop facts were served 6/6 by standing retrieval in both
conditions.

## 2. The exact control-plane line

Event entry points (all invoked by the external driver / researcher, never by
learner-created state):

| Event | Line | Role |
|---|---|---|
| ev_teach | 297 | allocates a fact node, links ET_PRO/ET_INS edges |
| ev_query | 813-835 | the only event on the integration path |
| ev_observe | 836 | contradiction/revision entry point |
| ev_act | 859 | selects over learner-constructed guides by bid |

`main` (1357) only calls `run_all` (self-tests). The four handlers never call
each other. Every call site of the four events lies at lines 920-1591
(self-tests: t_*, run_all, ACT protocol tests) or in external drivers outside
the file. Zero call sites exist in the cognitive region (lines 1-917).

The `ev_query` miss path (lines 824-834) hardcodes the order trial ->
bootstrap -> inquire, with no branch keyed on learner state. Call-site
inventory of the construction chain (definitions excluded from counts):

| Function | Def line | Call sites | All inside |
|---|---|---|---|
| mp_run | 668 | 827 | ev_query |
| t2_trial | 586 | 670 | mp_run |
| t2_try_verify | 497 | 604, 627, 643, 658 | t2_trial |
| promote_graph | 533 | 605, 628, 644, 659 | t2_trial |
| bootstrap_miss | 763 | 830 | ev_query |
| miss_inquire | 795 | 833 | ev_query |

Supporting closure: `t2_gather` (590), `t2_chain` (640),
`t2_asm_chain`/`t2_asm_sum`/`t2_asm_count` (603/626/642/657) are exclusive to
the trial path. `t2_exec` is called only from `t2_try_verify` (500),
`t2_revise_graph` (732), and one self-test (1289). `execute()` is called only
by `exec_val` and `t2_exec`, and the body of `execute()` (lines 192-216)
contains no calls to any event, allocation, trial, promotion, or inquiry
function, so a learner-created executable graph has no call path into
construction through `execute`.

Cognitive-region construction initiation, complete enumeration:

- ev_teach (297): `alloc_node` (299), `link_edge` ET_PRO/ET_INS (301, 307).
- ev_query (813): `activate` (815, read-only retrieval), `mp_run` (827),
  `bootstrap_miss` (830), `miss_inquire` (833).
- ev_observe (836): `activate` (838), `revise_on_contradict` (845) which
  calls `t2_revise_graph` (696) exclusively, `ev_teach_in` (852, 856),
  `alloc_raw` (846).
- ev_act (859): reads guides, computes bid; its only edge write is a USE
  edge on the selected guide (897). No construction initiation.
- `ev_teach_in` (310) is called only from `promote_graph` (541),
  `t2_revise_graph` (748), `bootstrap_miss` (783), and `ev_observe`
  (852, 856): all event-rooted. `revise_on_contradict` is called only from
  `ev_observe` (845). `miss_inquire` is called only from `ev_query` (833).
  `bootstrap_miss`'s helper `k_get` is called only at 775. `rec_evict` /
  `evict_node` (249-254) are reachable only via `alloc_node` (98) and tests,
  i.e. only through event-rooted paths.

The control-parameter path: `mp_set` is defined at 917 and called once, at
1010, inside `fn t_c12` (1008-1012), a self-test. `mp_get` is defined at 916
(`return ng(W,1,20);`) and called once, at 1011, in the same self-test. The
mp slot `ng(W,1,20)` is read nowhere else in the source. `mp_run` (668-670)
derives its control bits from the event's `flags` argument
(`masked = flags & 1`, `dc = (flags >> 1) & 1`, `di = (flags >> 2) & 1`)
and its accept oracle from the event's `expected` argument; it never reads
the mp slot. The "learner-set miss policy" comment (line 826) is inaccurate
as a description of control flow: the researcher, as event caller, sets
whether trials run and how they are verified.

Summary of the line: every construction entry (`mp_run`, `t2_trial`,
`t2_try_verify`, `promote_graph`, `bootstrap_miss`, `miss_inquire`,
`ev_teach`, `ev_teach_in`, the revise chain, `t2_exec`/`execute`) is
reachable only from the four event handlers or from self-tests. The
initiation graph is event-rooted at every root.

## 3. Transcription errors found by MECH-VERIFY (recorded, none verdict-relevant)

1. The SHA-256 printed in LEARNER-MECH
   (`a29972ca8183b2857c0c7b262d004fce6e4547c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`)
   is 79 characters long, not a valid 64-character SHA-256, and does not
   match the frozen blob. The true SHA-256, computed identically from the
   working-tree file and from `git show f4de7ff46:`:
   `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
   The first 48 hex characters match; the tail is a transcription error.
   The git blob hash (b226b223...) is exact and pins the bytes analyzed, so
   no claim is affected.
2. The analysis cites `ev_query` as lines 813-836; the function spans
   813-835 and `fn ev_observe` begins at line 836.
3. The analysis cites the "learner-set miss policy" comment at line 828;
   it is at line 826 (827 is the `mp_run` call, 828 is the answer check).

## 4. What this means for TNN-3 governance

Learner authority over integration scores effectively zero on the
constitution's metric: the learner records facts (`ev_teach`), reifies
uncertainty (`miss_inquire`), and selects guides (`ev_act`), but cannot
initiate the one construction act that integrates new experience. Human
hand-holding is maximal on the integration path: the researcher fires the
query event, sets flags and expected, and the machinery does the work. The
6/6 to 0/6 drop when exactly that machinery is removed is the measurement
of the hand-holding share. Until a run exists in which the event-triggered
machinery is disabled and the learner nevertheless integrates, with
white-box evidence that a learner-created structure initiated the
construction, any integration result on TNN-2 remains MACHINERY-DEPENDENT
in the strong sense: the learner does not decide or author the integration.

Any TNN-3 design that claims learner-owned integration must address three
absent properties (white-box visibility of the initiation act already
holds, as `promote_graph` leaves construction-provenance DEP edges):

1. Initiation-from-state. A construction service (trial, promote, or a
   successor) must be reachable from learner-created state, not only from
   the event interface. A structure the learner created must be able to
   cause construction machinery to run on the learner's schedule, not on
   the arrival of a researcher event.
2. Control-from-state. The gating and parameterization of construction
   (whether to attempt, in what search order, under what accept rule)
   must be readable from learner-created state, not only from event
   arguments. A miss policy set by the event caller is researcher-set,
   whatever the comment says.
3. Trigger-from-state. The decision of when to attempt integration versus
   merely reify uncertainty must be expressible in learner state and
   honored by the control plane. The current miss path hardcodes the
   escalation order and gives state no vote in it.

The acceptance run that would close this gap, in the constitution's terms:
the event-triggered machinery disabled, the learner still integrates, with
white-box evidence of the learner-created structure that initiated
construction; the bar to pass is CO-1 (6/6 store, 12/12 reuse, 12/12
delayed) via a construction path reachable from learner state, not via the
event path.

## 5. This is not a patch proposal

This document proposes no patch, handler, mode, bridge, or opcode. Any
change to the protected-core boundary or to initiation semantics is a
TNN-3 governance decision. This document is the verified problem statement
that such a decision must address: the control plane of frozen TNN-2
structurally excludes learner state from initiating construction, and all
three supporting claims were confirmed with exact call-site evidence.
