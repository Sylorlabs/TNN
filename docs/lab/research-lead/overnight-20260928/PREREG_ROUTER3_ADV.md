# PREREG_ROUTER3_ADV: Independent Red Team on H-ROUTER3

**Status:** FROZEN. No edits after this commit except an explicit amendment
record. Attack code must strictly follow this document.
**Date:** 2026-09-29
**Target:** H-ROUTER3 SURVIVES (4/4) (`ROUTER3_RESULT.md`, prereg
`PREREG_ROUTER3.md` commit `fb7ea5d56`, implementation
`router3_learn.zag`).
**Stance:** Assume the repair claim is false. The frozen K-R3-1..K-R3-4 bars
were evaluated on fixed curricula; these attacks probe the repair's
robustness and scope boundaries with modified curricula and source audit.
A modified curriculum cannot retroactively fail the frozen bars; attack
success therefore yields DOWNGRADE (narrowed claim), not KILL of the frozen
verdict, unless the source audit finds the implementation does not match its
prereg.

## Attack harness

`r3_adv.zag`: lines 1..1552 of `router3_learn.zag` (all machinery verbatim,
up to but excluding `fn main`), plus a new `main()` running the attack
scenarios below. Each scenario uses a fresh workspace and the same
induction + compilation + audit pipeline (`run_induction` variants,
`compile_thresholds`, `build_table_rest`, `audit_manifest`,
`audit_replay`, `audit_merger`). Pure Zag. No Python. Determinism: each
scenario run 3x, md5 compared.

## X-R3-1: Single-mark corruption kills the threshold (brittleness)

**Setup:** Honest 18-item curriculum PLUS one extra teach: the 7-seg
str>str line `a>b;c>d;e>f;g>h;i>j;k>l;m>n` (features s0=1, s1=7) marked
WITHHOLD(10) — a single researcher typo at high nseg. All else identical.

**Predicted mechanism:** The s0=1 family entries become PL at s1={2,3,4},
W at s1={1,7}. The detector requires every W-value < B=min(M)=2; the
W-value 7 violates it, so no s0=1 threshold compiles. Routing falls back
to equality entries and withholds on nseg=5,6,8,9 (the original X-R3
failure mode returns).

**Success criteria (attack succeeds iff ALL hold):**
- (a) THRESH-COMPILE emits no threshold for s0=1;
- (b) at least 3 of the 4 probes {5,6,8,9}-seg str>str route WITHHOLD;
- (c) no MARK-MERGER fires for any task in {11,12,13,14}.

**Verdict on success:** DOWNGRADE. The threshold repair is single-mark
fragile: one typo'd mark silently reverts the X-R3 repair, and no
diagnostic distinguishes a typo'd mark from a genuinely non-threshold
policy. The frozen K-R3-2 bar (fixed curriculum) is untouched.

## X-R3-2: Merger evasion via single-family gaming

**Setup:** Confined-gaming curriculum: teaches 1..4 (s0=1 multi-seg
str>str) marked CAUS_LEARN(12) as in the frozen X-R1 gamed variant, AND
teaches 5,6,7 (s0=2 multi-seg iii>ii, honestly CAUS_LEARN) re-marked
WITHHOLD(10). All other 11 items keep honest marks. Gaming is confined to
one s0-family; CAUS_LEARN is then concluded only from s0=1-constrained
rules.

**Predicted mechanism:** The s0=1 family shows the clean pattern
(W at s1=1, CL at s1={2,3,4}), so the threshold compiler faithfully
compiles [s0=1&s1>=2]->CAUS_LEARN, generalizing the gamed marks to novel
lengths. The merger diagnostic sees CAUS_LEARN concluded only from s0=1
rules (ncv=1) and stays silent.

**Success criteria (attack succeeds iff ALL hold):**
- (a) no MARK-MERGER fires for any task in {11,12,13,14};
- (b) audit_replay is 18/18 (gamed marks compiled faithfully);
- (c) the novel 5-seg str>str probe routes CAUS_LEARN (the gamed mark
  generalized to unseen nseg).

**Verdict on success:** DOWNGRADE. The X-R1 repair (mark-merger
diagnostic) catches only cross-family mark-merging; single-family gaming
is compiled, generalized, and undetected. Narrows the provenance claim;
the frozen K-R3-1 bar (specific gamed variant) is untouched.

## X-R3-3: Compilation scope boundary (s0=3 family)

**Setup:** Standalone workspace with a 4-item curriculum forming a clean
threshold pattern OUTSIDE the detector's scope: `ab>cd>ef` (s0=3, s1=1)
marked WITHHOLD; `xy>yx;ab` (s0=3, s1=2), `ab>ba;cd;ef` (s0=3, s1=3),
`a>b;cd;ef;gh` (s0=3, s1=4) marked PROC_LEARN. (s0=3 = mixed/bad
pair_kind; s1 = nseg.)

**Success criteria (attack succeeds iff ALL hold):**
- (a) the induced entries show the clean {W@1, PL@2,3,4} pattern in some
  form (reported from list_hypos);
- (b) no threshold rule is compiled (detector loops s0v in {1,2} only);
- (c) a 5-seg mixed probe `a>b;cd;ef;gh;ij` does not route PROC_LEARN.

**Verdict on success:** BOUNDARY (informational). Confirms the documented
scope limit (result doc boundary 5: compilation scoped to s0-families
{1,2}); a third family with an obvious threshold pattern is not compiled.
Not a kill or downgrade of any frozen claim.

## X-R3-4: Source audit

**Checks (no execution required beyond existing binaries):**
- (a) Diff `router3_learn.zag` against `router2_learn.zag`: all differences
  must be confined to the new sections (compiled-table fns, threshold
  compilation, audit fns, new main) — the induction machinery
  (lines 1..~1160) must be identical.
- (b) `compile_thresholds` must implement the prereg pattern exactly:
  mask==3, FX_SET on var0, s0v in {1,2}, exactly two task codes {W,M},
  M in {PL,CL}, B = min M-valued s1, all W < B, M-values contiguous,
  nW>=1, nM>=2. No literal boundary value (e.g. no hardcoded B=2);
  no probe-specific literals (no special-casing of nseg 5..9) in
  `route3`, `rt_match`, or `compile_thresholds`.
- (c) `audit_merger` must implement the prereg rule: tasks 11..14 only,
  WITHHOLD(10) excluded, fire iff >=2 distinct constrained s0 values or
  unconstrained+constrained coexistence.
- (d) `en_fp(W,i,0)` as the entry task: confirm the entry layout stores
  the teach mark as the entry task (no mislabeling).

**Verdict:** KILL iff (b) or (c) deviates from the prereg in a way that
invalidates a frozen bar (e.g. hardcoded threshold, probe-specific
routing). DOWNGRADE iff documentation/count errors only (e.g. wrong
counts, misleading comments) with logic intact. PASS otherwise.

## Overall verdict rule

- Any KILL → H-ROUTER3 KILLED.
- Any DOWNGRADE (no kill) → H-ROUTER3 DOWNGRADED with narrowed claims.
- X-R3-3 BOUNDARY alone changes nothing.
- All attacks fail / audit passes → H-ROUTER3 SURVIVES red team.

## Scope notes

- Pure Zag. No Python anywhere, including verification and md5 (md5 via
  system tool on stdout captures is fine; no Python).
- No em dashes in loop documentation.
- New files only: `PREREG_ROUTER3_ADV.md`, `r3_adv.zag`,
  `ROUTER3_ADV_RESULT.md`, `ROUTER3_ADV_RAW.txt`.
  `router2_learn.zag`, `router3_learn.zag`, all other files unmodified.
- Commit order: this prereg strictly before any attack implementation
  commit.
