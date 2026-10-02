# PREREG: H-CAUSAL-UNIFIED Red Team (X-CU1..X-CU4)

**Date:** 2026-09-29
**Adversary:** H-CAUSAL-UNIFIED Red Team
**Target:** H-CAUSAL-UNIFIED SURVIVES (28/28), commit ba065e172
**Implementation:** unified_causal.zag (2643 lines)
**Source:** causal/causal_learn.zag (1057 lines, 129 functions)
**Stance:** Assume the claim is false. Attack to kill or downgrade.

## Attack X-CU1: Provenance Gaming (episode vs entry counting)

**Observation (pre-execution):** fu_hist_count (line 2111) counts EPISODES
with EP_SUP status via ep_st(W,i)==EP_SUP(). The hypotheses listing
(list_hypos, line 2042) displays ENTRIES with ST_SUPER status via
en_st(W,i)==ST_SUPER(). These are different stores. In run_a.txt the
listing shows H2, H6, H7, H8 as SUPERSEDED (4 entries) but CAUSHIST
reports superseded=2 (episodes).

**Kill criteria:**
- X-CU1 KILLS if: the superseded count returned by caus_hist does not
  equal the number of SUPERSEDED entries displayed in the hypotheses
  listing on any frozen test input. The provenance is then misleading:
  a user querying history sees 4 superseded hypotheses but is told 2.
- X-CU1 DOWNGRADES if: the count is technically correct under some
  definition (episodes vs entries) but the result doc misdescribes it
  (claims "H2 and H6" when H7, H8 also superseded).

**Method:** Run the frozen 17-episode stream, capture caus_hist output,
count SUPERSEDED entries in listing vs reported superseded=N. Pure Zag
test harness reading the existing run_a.txt plus a fresh run.

## Attack X-CU2: Contest Flooding (silent drop on capacity)

**Observation (pre-execution):** learn_episode (line 1893) calls
new_contest on contradiction. new_contest returns -1 when c>=8
(line 1673). The caller does NOT check for -1; it assigns c=-1 and
returns. The contradiction is silently dropped: no contest opened,
no error emitted, the conflicting evidence vanishes.

**Kill criteria:**
- X-CU2 KILLS if: feeding 9+ contradictory episodes at distinct states
  causes any contradiction to be silently dropped (no contest, no
  error, no trace). The mechanism then loses evidence without notice,
  violating the "explicit contest plus withhold" guarantee of K-CU5.
- X-CU2 DOWNGRADES if: the drop is silent but some other signal
  (e.g., entry status) reveals the loss.

**Method:** Construct a Zag test that feeds contradictory episodes at
9+ distinct states, then queries caus_hist and checks open_contests
count plus per-state prediction behavior. Expect 8 contests max and
the 9th contradiction to vanish silently.

## Attack X-CU3: Capacity Reduction (32 entries, 8 contests)

**Observation (pre-execution):** new_entry caps at 32 (was 64), new_contest
caps at 8 (was 16). The result doc admits "guards never trigger" on the
frozen test (18 episodes, 3 contests). The port is untested at capacity.

**Kill criteria:**
- X-CU3 KILLS if: exceeding 32 entries or 8 contests causes silent
  data loss, wrong predictions, or crashes (any behavior worse than
  an explicit error).
- X-CU3 DOWNGRADES if: capacity is hit but the failure is explicit
  and contained (e.g., clear error, no silent corruption).

**Method:** Feed a stream designed to create >32 entries via repeated
splits on distinct actions/states, and >8 contests via contradictions.
Observe behavior at the boundary. Check whether new_entry -1 is
handled (split_attempt caller) vs new_contest -1 (unhandled per X-CU2).

## Attack X-CU4: Source Audit (127 functions verbatim?)

**Observation (pre-execution):** Original has 129 functions. Unified is
missing i64s, load_obs, parse_int (3 functions). 129-3=126 shared
functions, not 127 as claimed. The port must be verbatim except
workspace rebasing (O_* offsets gain FUBASE+) and capacity guards
(64->32, 16->8).

**Kill criteria:**
- X-CU4 KILLS if: any shared function has logic changes beyond
  (a) FUBASE rebasing in O_* offset functions, (b) the two capacity
  guard constants, (c) comment-only changes. Any altered conditional,
  added/removed statement, or changed constant in machinery logic
  is a port infidelity.
- X-CU4 DOWNGRADES if: the function count claim (127) is wrong but all
  ported functions are faithful (documentation error only).
- X-CU4 PASSES if: all 126 shared functions match modulo the two
  allowed change classes.

**Method:** Extract each shared function body from both files, normalize
whitespace, diff. Allowlist: lines containing FUBASE, the capacity
guard lines in new_entry/new_contest. Manual review of all diffs.

## Execution order

1. X-CU4 first (static audit, no execution needed).
2. X-CU1 second (analyze existing run_a.txt + fresh run).
3. X-CU2 and X-CU3 third (require new Zag test programs).

## Verdict mapping

- Any KILL: H-CAUSAL-UNIFIED is KILLED or DOWNGRADED per the specific
  attack. Report honestly.
- All PASS: H-CAUSAL-UNIFIED SURVIVES the red team.

**Purity:** Pure Zag. No Python. Shell only for cmp/sha256sum.
**No em dashes in documentation.**
