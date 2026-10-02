# MECH-VERIFY report: independent verification of the LEARNER-MECH root-cause analysis

Wave: wave-20261001-2321pdt. Lane: MECH-VERIFY (verification only).
Analyzed: docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/LEARNER_MECH_ANALYSIS.md
(168 lines). Source verified: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
extracted via `git show f4de7ff46:<path>`. No new experiments, no Python,
no patch proposed.

Note: no em-dashes are used in this document.

## 0. Source identity (prerequisite, not one of the three claims)

- `git hash-object` on the extracted file: b226b223cb3ee0be742af673653fb8ea8605f281,
  exactly the f4de7ff46 freeze blob hash quoted in the analysis. Line count 1591,
  matches. Source identity CONFIRMED.
- Discrepancy worth recording: the SHA-256 printed in the analysis
  (a29972ca8183b2857c0c7b262d004fce6e4547c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d)
  is 79 characters long, not a valid 64-character SHA-256, and does not match the
  actual sha256 of the frozen blob, computed identically from the working-tree file
  and from `git show f4de7ff46:`:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
  The first 48 hex characters match; the tail looks like a transcription error
  in the doc. This does not affect the three claims, because the git blob hash
  pins the exact bytes analyzed, but the printed SHA-256 string should be corrected.

## Claim 1: call-site inventory. Verdict: CONFIRMED

Verified by grep over the frozen source (definitions excluded from call counts):

| Function | Def line | Call sites | All inside |
|---|---|---|---|
| mp_run | 668 | 827 | ev_query |
| t2_trial | 586 | 670 | mp_run (668-671) |
| t2_try_verify | 497 | 604, 627, 643, 658 | t2_trial (586-666) |
| promote_graph | 533 | 605, 628, 644, 659 | t2_trial |
| bootstrap_miss | 763 | 830 | ev_query (813-835) |

Every count matches the analysis exactly, including "all four in t2_trial".
Supporting closure: t2_trial's callees t2_gather (called only at 590), t2_chain
(only at 640), t2_asm_chain/t2_asm_sum/t2_asm_count (only at 603/626/642/657)
are likewise exclusive to the trial path; t2_exec is called only from
t2_try_verify (500), t2_revise_graph (732), and one self-test (1289); execute()
is called only by exec_val and t2_exec, and execute()'s own body (192-216)
contains no calls to any event, allocation, trial, promotion, or inquiry
function, so a learner-created executable graph has no call path into
construction through execute.

Two trivial line-number notes: the analysis cites ev_query as "lines 813-836",
but ev_query spans 813-835 and fn ev_observe begins at line 836; the analysis
cites the "learner-set miss policy" comment at line 828, but it is at line 826
(827 is the mp_run call, 828 is the ans check). Neither affects the claim.

## Claim 2: the mp_set/mp_get claim. Verdict: CONFIRMED

- `mp_set` occurrences: definition at 917; the single call is at 1010, inside
  fn t_c12 (1008-1012), a self-test function. No call anywhere else in the file.
- `mp_get` occurrences: definition at 916 (`return ng(W,1,20);`); the single call
  is at 1011, in the same self-test. No call anywhere else in the file.
- The mp slot `ng(W,1,20)` is read nowhere else in the source.
- `mp_run` (668-670): `let masked:i32=flags&1; let dc:i32=(flags>>1)&1;`
  `let di:i32=(flags>>2)&1; return t2_trial(W,s,r,expected,masked,dc,di);`
  All control bits come from the event's `flags` argument; the accept oracle is
  the event's `expected` argument. mp_run never reads the mp slot.

So: mp_set/mp_get are called only in a test function, and mp_run never reads
the mp slot. The "learner-set" comment is inaccurate as a control-flow
description, exactly as the analysis states.

## Claim 3: the four event entry points. Verdict: CONFIRMED

Event definitions: ev_teach (297), ev_query (813), ev_observe (836), ev_act (859).

- In the frozen source, every call site of ev_teach, ev_query, ev_observe, and
  ev_act lies at lines 920-1591, i.e. in self-test functions (t_*, run_all,
  and the ACT port r_ptest/t_r_pact* protocol tests), or in external drivers
  outside this file. Zero call sites exist in the cognitive region (lines 1-917).
  main (1357) only calls run_all. The four handlers never call each other.
- Cognitive-region construction initiation, complete enumeration:
  - ev_teach (297): alloc_node (299), link_edge ET_PRO/ET_INS (301, 307).
  - ev_query (813): activate (815, read-only retrieval), mp_run (827),
    bootstrap_miss (830), miss_inquire (833).
  - ev_observe (836): activate (838), revise_on_contradict (845) which calls
    t2_revise_graph (696) exclusively, ev_teach_in (852, 856), alloc_raw (846).
  - ev_act (859): reads guides, computes bid; its only edge write is a
    USE edge on the selected guide (897). No construction initiation.
  - miss_inquire (795) is called only from ev_query (833). ev_teach_in (310) is
    called only from promote_graph (541), t2_revise_graph (748), bootstrap_miss
    (783), and ev_observe (852, 856): all event-rooted. revise_on_contradict is
    called only from ev_observe (845). bootstrap_miss's helper k_get is called
    only at 775. rec_evict/evict_node (249-254) are reachable only via alloc_node
    (98) and tests, i.e. only through event-rooted paths.
- No learner-created structure has a call path back into construction. The
  complete call-site closure above shows every construction entry
  (mp_run, t2_trial, t2_try_verify, promote_graph, bootstrap_miss, miss_inquire,
  ev_teach, ev_teach_in, the revise chain, t2_exec/execute) is reachable only
  from the four event handlers or from self-tests; learner state is read as
  data (t2_gather, activate, ev_act bid selection) and never as control. The
  ev_query miss path (824-834) hardcodes the order trial -> bootstrap ->
  inquire with no branch keyed on learner state.

## Summary

- Claim 1 (call-site inventory): CONFIRMED. Exact matches on all five counts.
- Claim 2 (mp_set/mp_get only in tests; mp_run never reads the mp slot): CONFIRMED.
- Claim 3 (four event entry points only; no learner-state path back into
  construction): CONFIRMED.
- Non-claim discrepancies found while verifying: (a) the printed SHA-256 in the
  analysis is 79 characters and does not match the frozen blob; the git blob
  hash b226b223... is correct and exact; (b) ev_query spans 813-835, not 813-836;
  (c) the "learner-set miss policy" comment is at line 826, not 828. None of
  these affects the verdicts.
