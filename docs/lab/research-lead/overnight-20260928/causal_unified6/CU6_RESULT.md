# H-CAUSAL-UNIFIED6 RESULT (X-CU4-2 REPAIR)

**Date:** 2026-09-29
**Researcher:** H-CAUSAL-UNIFIED6 Frontier Researcher
**Target:** H-CAUSAL-UNIFIED5 SURVIVES (builder 28/28; red team
SURVIVES 4/4); X-CU4-2 fresh-general shadow is a confirmed
pre-existing boundary (CU4_ADV_RESULT.md sec 3, CU5 prereg
residual).
**Prereg:** `PREREG_CAUSAL_UNIFIED6.md` (commit 2f48dd7e1, frozen
alone before any implementation)
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python
in research, generators, verifiers, debugging, analysis, harnesses,
or scratch. File operations via shell only. One mechanical
em-dash byte check on the prereg used a shell byte scan, not
research evidence; no Python touched any research artifact.
**Verdict: H-CAUSAL-UNIFIED6 SURVIVES.** All five frozen bars pass.

## 1. Frozen repair (exact change set)

File `unified_causal6.zag` is byte-verbatim
`unified_causal5.zag` except two insertions (diff verified; no other
function text changed):

(a) New helper `live_contra_at(W,a,s0,s1,s2)` (40 lines, before
`predict`): returns 1 if any ST_CONFL entry for action a holds 2+
distinct live (non-superseded, EP_SUP skipped) outcomes at the
exact state (s0,s1,s2), else 0. Three-or-more distinct live
outcomes also return 1.

(b) In `predict()`, immediately after the `if(i<0)` no-entry
return: if `live_contra_at(W,a,s0,s1,s2)==1`, emit
`WITHHOLD (live-contradiction)` and return 0.

Rationale (frozen): after a successful carve, the parent
tombstone's losers at the carved state are superseded, so the
tombstone holds exactly 1 distinct live outcome (the shared
winners) there; the guard does not fire and adjudicated carves
predict normally. It fires only on a genuine unresolved
contradiction (2+ distinct live outcomes at the exact query
state), so a general ACTIVE entry can no longer shadow it.

## 2. K-CU6-1: X-CU4-2 closed (PASS)

Harness `cu6_adv.zag`: mechanism lines 1..2488 byte-verbatim from
`unified_causal6.zag` (cmp-verified); adversary helpers verbatim
from `cu5_adv.zag`; new main() with the frozen K-CU6-1/K-CU6-2
fixtures. Raw: `CU6_ADV_RAW_1.txt` (runs 1..3 byte-identical,
MD5 `c0a093a60b167bdba1f867d1fa8c9674`).

Verbatim X-CU4-2 construction (CU4_ADV_RESULT.md sec 3): 20-episode
flood (nct=8), carve at (2,0,0) via `2,0,0,2>0,0,0`, re-contradiction
via `2,0,0,2>1,1,1` (carved entry -> ST_CONFL; find_entry=-1 and
query r=0 confirmed pre-shadow), then `2,0,2,2>7,7,7` (fresh [any]
ACTIVE entry).

(a) Query (2,0,0) after the fresh [any]: `WITHHOLD
    (live-contradiction)`, r=0. Under CU5 this query returned
    r=1 out=(7 7 7). The shadow is closed.
(b) Adversary helper confirms the ST_CONFL entry still holds 2+
    distinct live outcomes at (2,0,0)
    (`K1 live-contradiction at (2,0,0)=1`).
(c) Control: query (2,0,2) returns r=1 out=(7 7 7) via
    `(exact-episode)`. The guard is exact-state scoped; general
    learning is intact.

## 3. K-CU6-2: adjudicated carves still predict (PASS)

Same raw. CU5 K-CU5-1 X-CU4-1 shape (flood, carves at (2,0,0) and
(1,0,0), no re-conflict). Entry dump matches the CU5 shape
(entries 2,3 ACTIVE mask 7, parent 0; entries 0,1 ST_CONFL).

- Query (2,0,0): r=1 out=(0 0 0) via `(exact-episode)`.
- Query (1,0,0): r=1 out=(0 0 0) via `(exact-episode)`.
- Query (0,0,0): r=0 `WITHHOLD (no-entry)` (never-adjudicated
  withhold preserved).

The guard did not fire on adjudicated states, confirming the
frozen rationale: each parent tombstone holds exactly 1 distinct
live outcome at its carved states.

## 4. K-CU6-3: no regression (PASS)

- `cu6_test.zag` (battery driver, mechanism lines byte-verbatim
  from unified_causal6.zag): `=== CU4 TEST RESULT: 16/16 ===`,
  ALL PASS. Stdout byte-identical (cmp) to frozen
  `causal_unified4/CU4_RAW_TEST.txt` (MD5
  `3bde55fe381a7c8ff1cef93d8c038da3`).
- `unified_causal6.zag` main(): `=== CAUSAL-UNIFIED RESULT:
  28/28 ===`. Stdout byte-identical (cmp) to frozen
  `causal_unified4/CU4_RAW_MAIN.txt` (MD5
  `87f8edc29825802327029f46f045dbe3`).

No byte differed, so no supersession analysis was needed: the
repair is behaviorally silent on every previously tested path.

## 5. K-CU6-4: determinism (PASS)

- cu6_adv: 3/3 byte-identical, MD5
  `c0a093a60b167bdba1f867d1fa8c9674`.
- cu6_test: 3/3 byte-identical, MD5
  `3bde55fe381a7c8ff1cef93d8c038da3`.
- cu6_main: 3/3 byte-identical, MD5
  `87f8edc29825802327029f46f045dbe3`.

## 6. K-CU6-5: change-set purity (PASS)

`diff causal_unified5/unified_causal5.zag
causal_unified6/unified_causal6.zag` shows exactly the frozen
change set: the 40-line `live_contra_at` helper and the 10-line
predict guard (comments included). No other function text
changed. No fixture literals in mechanism functions: the helper
references only en_st/en_a/en_neps/en_ep/ep_st/ep_s/ep_ns,
ST_CONFL, EP_SUP, all pre-existing mechanism accessors.

## 7. Causal interpretation

The failure class is closed at the query level: a withhold is a
claim that a live contradiction exists at a state, and that claim
must survive the arrival of unrelated general knowledge. The old
code let `find_entry` (which skips ST_CONFL) hand prediction to
any ACTIVE entry, so a fresh [any] entry with zero evidence at
the contradicted state silently retired the withhold. The guard
makes the withhold durable by checking the contradiction itself
(2+ distinct live outcomes at the exact state) rather than the
entry that happens to be most specific. Because adjudication
supersedes losers, carved states never trip the guard, so the
repair separates "adjudicated, safe to predict" from
"contradicted, must withhold" exactly at the mechanism's own
definition of a live contradiction.

## 8. Boundaries and non-claims

- The `find_conflicted` oldest-first tie-break (CU5 red team sec
  9) was considered and deliberately not changed: every observed
  adjudication through it was safe, and changing it without a
  demonstrated safety defect would be churn, not a repair.
- Shared-winner double voting across adjudications (CU5 red team
  sec 9 boundary) remains documented and out of scope.
- Contest-capacity exhaustion still forces the untracked ST_CONFL
  path (observed in the K-CU6-1 flood: contest cap hit at seq
  18/20); the guard applies equally to untracked tombstones.
- Entry capacity 32 explicit refusal unchanged.
- This is bounded L2 mechanism repair, not L3. No representational
  invention is claimed.

## 9. Governance disclosures

- Preregistration strictly preceded implementation and execution
  (commit 2f48dd7e1, prereg committed alone). No frozen bar was
  weakened or retroactively changed. Verdict rule applied verbatim
  from the prereg.
- Pure Zag throughout: no Python in research, generators,
  verifiers, debugging, analysis, harnesses, or scratch. Harness
  assembly via shell head/sed/cat; mechanism regions cmp-verified
  byte-identical.
- One `znc` invocation emitted warnings but no binary (piped
  through head); the rerun without the pipe compiled cleanly
  (exit 0) and all evidence comes from the successful builds,
  3/3 byte-identical. Disclosed for completeness.
- Only explicitly owned paths staged:
  `docs/lab/research-lead/overnight-20260928/causal_unified6/`.
- No binaries or generated artifacts committed (raw outputs are
  text; binaries and .zag-cache removed before commit).
- Commits are local; no push attempted or authorized.
- This document contains no em dashes.

## 10. Commit lineage

- 2f48dd7e1 `PREREG H-CAUSAL-UNIFIED6 FROZEN (alone, before
  implementation). Query-path live-contradiction guard; X-CU4-2
  frozen kill criteria. Pure Zag.`
- (this commit) `unified_causal6.zag` (repaired mechanism),
  `cu6_adv.zag` (adversary driver), `cu6_test.zag` (battery
  driver), `CU6_ADV_RAW_1/2/3.txt`, `CU6_TEST_RAW_1/2/3.txt`,
  `CU6_MAIN_RAW_1/2/3.txt`, and this report.

## 11. Verdict

**H-CAUSAL-UNIFIED6: SURVIVES.** K-CU6-1 through K-CU6-5 all pass.
The X-CU4-2 fresh-general shadow is closed: the re-conflicted
withhold at (2,0,0) survives the arrival of a fresh [any] entry
(r=0, live contradiction intact) while the general entry still
predicts at non-contradicted states and adjudicated carves still
predict at theirs. All 16 builder bars and the 28/28 main
regression reproduce byte-identically. Recommended next step:
independent red team against H-CAUSAL-UNIFIED6 (probe the guard
under 3+ outcome contradictions, tombstone chains, and capacity
pressure; attack the deferred tie-break and double-voting
boundaries). Classification: bounded L2; nothing here is L3.
