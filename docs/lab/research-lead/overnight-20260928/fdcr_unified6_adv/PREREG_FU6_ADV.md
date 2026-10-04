# PREREG: H-FDCR-UNIFIED6 Independent Red Team (FU6-ADV)

**Date:** 2026-09-29
**Target:** H-FDCR-UNIFIED6 SURVIVES (42/42). Prereg `814724be5`, result
  commit `0480f10a6` (per FU6 result doc).
**Adversary stance:** Assume the FU6 claim is false. Attack the R1 dedup
  and R2 uncertainty-NOTE repairs.

## Frozen mechanism under test (from code reading, before any attack run)

- `noadd_drop_record` (lines 1472-1500): increments NOADD_DROP_COUNT on
  every call; dedups the 64-entry name list by subject CONTENT
  (`streq`); appends to a free slot if new; increments
  NOADD_DROP_OVERFLOW only when the list is full AND the subject is new
  and distinct. Drop-list entries are never cleared (only init).
- `handle_proc_learn_unified` NOTE logic (lines ~1690-1722): counts
  `nlost` (vote<0 AND `noadd_vote_lost`==1) and `nnovote` (vote<0 AND
  `noadd_vote_lost`==0). If `nlost>0`: definite NOTE with lifetime
  total. Else if `nnovote>0 && overflow>0`: uncertainty NOTE. Else:
  silence.
- Strings are interned append-only (`con_intern`: "Simple linear
  append; no deduplication in v1"); `mem_off` values stored in the drop
  list never dangle.
- `noadd_drop_record` has exactly one call site: `noadd_record`, in the
  NOADD-table-full branch (genuine vote refusal only).

## Attacks

### X-FU6-1 (Dedup: drop, become member, re-drop)

Setup in one world W:
1. Teach s1..s40 `| is_a | pet` (8 members + 32 NOADD, matching G-T1).
2. `T x | is_a | pet` -> x dropped, named in drop list (total=1).
3. `T x | is_a | pet` again -> x dropped again; dedup must catch it
   (total=2, x named once, overflow=0).
4. `T x | is_a | animal` -> x becomes member of a new animal concept.
5. `T x | is_a | pet` -> x matches pet, is not a pet member, NOADD
   full -> drop path; dedup must catch x again
   (total=3, x named once, overflow=0).
6. Procedure `s1>1s` (all voting): no NOTE may fire for x, because
   `con_vote_concept("x")>=0` (x is a member now).

Kill criteria (any one -> DOWNGRADED):
- (a) After step 3 or 5, the number of name slots whose content equals
  "x" is not exactly 1.
- (b) After step 3 or 5, `noadd_drop_overflow(W)` != 0.
- (c) After step 5, `noadd_vote_lost(W,"x")` != 1.
- (d) In step 6, any ULEARN NOTE line fires (spurious NOTE for a member
  input whose vote was not lost).

If none fire: X-FU6-1 FAILS (dedup sound across member-after-drop).

### X-FU6-2 (Uncertainty NOTE: trigger conditions)

Setup in one world W:
1. Teach s1..s40 `| is_a | pet`, then d1..d65 `| is_a | pet`
   (65 distinct drops: d1..d64 named, d65 beyond capacity).
2. Assert `noadd_drop_overflow(W)==1` (d65 incremented it exactly once).
3. Drop d65 two more times (`T d65 | is_a | pet` x2). Record overflow.
4. Procedure `s1>1s;ghost>tsohg` where ghost was never taught
   (features match no concept).

Kill criteria:
- (a) KILL: a DEFINITE "lost concept votes" NOTE fires for this
  procedure (false definite claim: ghost never voted, nothing was
  lost for this procedure).
- (b) KILL: NO NOTE of any kind fires (silence despite overflow>0 and
  nnovote>0; the R2 repair claims the uncertainty NOTE fires here).
- (c) DOWNGRADED: `noadd_drop_overflow` can be made >0 WITHOUT any
  genuine NOADD-table-full vote refusal (spoofed precondition). Tested
  by attempting drops without filling NOADD first; if overflow>0
  results, the uncertainty NOTE's precondition is spoofable.

If the uncertainty NOTE (and only the uncertainty NOTE) fires, and
(c) does not trigger: X-FU6-2 FAILS (conservative boundary holds as
designed; documented as an intentional conservative signal, not a
finding).

Measurement note for the report: record the overflow value after step
3. The frozen comment says overflow counts "distinct subjects dropped
beyond the 64-name capacity"; the code increments per drop EVENT of an
unnamed subject while full. If step 3 makes overflow==3 for one
distinct subject, report as a doc/code semantic mismatch (boundary
note, not a kill: the NOTE wording "O beyond name capacity" remains
true of events).

### X-FU6-3 (65th distinct subject: vote loss must not be silent)

Setup in one world W:
1. Teach s1..s40 `| is_a | pet`, then d1..d64 `| is_a | pet`
   (64 distinct drops, all named, overflow must be 0).
2. `T d65 | is_a | pet` (65th distinct drop; overflow must become 1).
3. Procedure `s1>1s;d65>56d`.

Kill criteria:
- (a) KILL: NO NOTE of any kind fires (d65's vote was genuinely lost
  and the loss is silent).
- (b) KILL: a DEFINITE "lost concept votes" NOTE fires naming a count
  that includes d65 as definite (false definite claim).
- (c) Boundary note (not a kill): procedure `s1>1s;d1>1d;d65>56d`
  (d1 named lost + d65 unnamed lost): the definite NOTE fires for d1
  but the if/else structure means d65's uncertainty is NOT separately
  signaled. Record whether the uncertainty NOTE also fires. The frozen
  code is explicit (if/else), so absence is by design; record as a
  minor information-loss boundary.

If the uncertainty NOTE (and only it) fires for the d65 procedure:
X-FU6-3 FAILS on (a)/(b) (boundary holds as designed).

### X-FU6-4 (Regression and source audit)

1. Rebuild `unified_fdcr6.zag` from `git show HEAD:...` (pristine
   blob). Run 3x. Must be byte-identical to committed
   `FDCR_UNIFIED6_RAW.txt` (cmp), md5 `4a6cb7179a588bd09cecbe4d3bbfffba`,
   42/42, exit 0.
2. Diff `unified_fdcr5.zag` vs `unified_fdcr6.zag`: the change set must
   be exactly the R1/R2/R3 repairs (dedup in `noadd_drop_record`,
   overflow counter, NOTE wording, PART G). No other mechanism
   function may differ.
3. Grep: exactly one `noadd_drop_record` call site (the genuine
   table-full branch); `NOADD_DROP_BASE` written only in init and
   `noadd_drop_record`.

Kill criteria: any regression mismatch, any undeclared mechanism
change, or any additional drop-record call site -> KILLED.

## Verdict rule

- Any KILL criterion fires -> H-FDCR-UNIFIED6 KILLED.
- Any DOWNGRADED criterion fires (and no KILL) -> H-FDCR-UNIFIED6
  DOWNGRADED (narrowed claim).
- All attacks fail -> H-FDCR-UNIFIED6 SURVIVES this red team.
- Confirmed disclosed boundaries (uncertainty NOTE conservatism,
  overflow event-vs-distinct semantics, mixed definite+uncertain
  information loss) do not change the verdict; they are recorded.

## Governance

- Pure Zag throughout: fixtures, harness, builds, runs, greps, md5,
  cmp. Zero Python at any stage.
- Harness = lines 1-2018 of committed `unified_fdcr6.zag`
  (everything before `fn main`), cmp-verified byte-identical, with an
  attack-only `main()`. No mechanism edits.
- Each attack run 3x; byte-identical via cmp required.
- Binaries built in /tmp/fu6adv only; never committed.
- Only `docs/lab/research-lead/overnight-20260928/fdcr_unified6_adv/`
  paths staged. No other worker's files touched. No broad git add.
- No em dashes in loop documentation.
