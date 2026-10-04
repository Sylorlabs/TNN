# PREREG_ROUTER8.md: H-ROUTER8 FROZEN PREREGISTRATION

**Date:** 2026-09-29
**Researcher:** H-ROUTER8 Frontier Researcher (independent subagent)
**Target:** H-ROUTER7 SURVIVES (builder) / DOWNGRADED (red team, `37ce0d271`).
**Status:** FROZEN. No amendments after this commit. Any change requires a
new prereg, not an edit.

## 1. What is being repaired

The H-ROUTER7 red team (`router7_adversary/R7_ADV_RESULT.md`, prereg
`8f795a1aa`, result `37ce0d271`) DOWNGRADED H-ROUTER7 on X-R7-1
exploratory variant V2, which demonstrated two defects through the
public `teach` interface:

**D1. Capacity defeat of the total-table headline.** A 40-mark
merge-resistant curriculum induces 25 ACTIVE FX_SET equality entries.
The 25th hits the `rt_add` 24-rule cap (`TABLE OVERFLOW`), the entry is
dropped, the R1 explicit `[any]->WITHHOLD` fallback append is refused by
the same guard, and `route3(RT,nrt,0,10,0)` returns -1. The R1 claim
("every feature triple routes to a declared task code; route3 never
silently returns -1") is false as stated.

**D2. Misleading trace at capacity.** Two emits fire for rules that were
never added: the entry loop's `TABLE-RULE` emit is unconditional after
`rt_add`, printing stale `RT[nrt-1]` content for the dropped 25th entry;
and the R1 explicit-fallback emit is unconditional inside
`if(hasany==0)`, printing a phantom `[any]->WITHHOLD` line when the
fallback was refused. The "loud emit" transparency R1 relies on is
itself unreliable at capacity.

**Narrowed C1 (evidence-supported):** the compiled table is total iff
fewer than 24 rules are compiled before the fallback append.

## 2. Base source and governance disclosure

Base: `docs/lab/research-lead/overnight-20260928/router7_learn.zag`,
verified byte-identical (`cmp`) to the blob at
`981459ee3:docs/lab/research-lead/overnight-20260928/router7_learn.zag`
(the same blob the red team verified its mechanism region against).
`router7_learn.zag` itself is NOT modified; H-ROUTER8 is implemented as
a new file `router8_learn.zag` = byte-verified copy of `router7_learn.zag`
plus exactly the frozen change set in section 3.

**Governance:** H-ROUTER7's own governance status is unresolved
(pre-prereg pilot execution; H-ROUTER6 ancestry; result files left
untracked after the `981459ee3` reset). H-ROUTER8 does not adjudicate
or cure those issues. What is clean is the H-ROUTER8 chain itself:
this prereg is frozen before any implementation edit, build, or run;
the repair is pure Zag; the result will be committed with
prereg-ancestry verification. The R7 lineage caveat is carried forward
for coordinator adjudication, stated here so it is not laundered.

## 3. Frozen repair set (R8)

**R8-1 (D2, entry loop):** gate the entry-loop `TABLE-RULE` emit on
actual insertion. Replace
```
    nrt=rt_add(RT,nrt, k0,v0, k1,v1, k2,v2, en_fp(W,e,0));
    emit("TABLE-RULE "); emit_rule(RT,nrt-1); emit(" (from H"); e64(e); emit(")\n");
```
with
```
    let r8before:i32=nrt;
    nrt=rt_add(RT,nrt, k0,v0, k1,v1, k2,v2, en_fp(W,e,0));
    if(nrt>r8before){
      emit("TABLE-RULE "); emit_rule(RT,nrt-1); emit(" (from H"); e64(e); emit(")\n");
    }
```
On the normal path (insertion succeeds) the emit is byte-identical to
before; on refusal nothing is printed for the dropped entry. The
`TABLE OVERFLOW` emit inside `rt_add` is unchanged and already loud.

**R8-2 (D1/D2, fallback):** gate the R1 explicit-fallback emit on actual
insertion; on refusal emit a loud non-totality warning instead of the
phantom line. Replace
```
  if(hasany==0){
    nrt=rt_add(RT,nrt, CK_ANY(),0, CK_ANY(),0, CK_ANY(),0, TC_W());
    emit("TABLE-RULE [any]->WITHHOLD (explicit fallback: no induced [any] rule; total-table invariant)\n");
  }
```
with
```
  if(hasany==0){
    let r8fb:i32=nrt;
    nrt=rt_add(RT,nrt, CK_ANY(),0, CK_ANY(),0, CK_ANY(),0, TC_W());
    if(nrt>r8fb){
      emit("TABLE-RULE [any]->WITHHOLD (explicit fallback: no induced [any] rule; total-table invariant)\n");
    } else {
      emit("TABLE-NON-TOTAL: explicit [any]->WITHHOLD fallback refused (TABLE OVERFLOW at 24 rules); route3 may return -1 for uncovered triples; table is NOT total\n");
    }
  }
```

**R8-3 (comments):** narrow the R1 comment block to the evidence-backed
claim (total iff the fallback append succeeds; 24-rule capacity bound;
warning declares non-totality at capacity). Update the main banner to
`router8_learn: H-ROUTER8 honest-capacity + single-segment family
audit`. Narrow the fallback-loss section comment's "total-table
invariant" phrasing to the bounded form. No other mechanism function
is touched: induction, threshold compilation, `rt_add`, `route3`,
audits, and all prior fixtures are byte-identical.

**R8-4 (test section):** new `CAPACITY-HONESTY (X-R7-1 V2 replay)`
section in `main()`, placed before the VERDICT, replaying the red
team's V2 fixture verbatim (same 40 teaches: s0=1 block W@1 PL@{2,4,6,8}
CL@{3,5,7,9}; s0=2 block W@1 CL@{2,4,6,8} PL@{3,5,7,9}; s0=3 block W@1
PL@{2..9}; s0=0 block W@1 PL@{2,4,6,8} CL@{3,5,7,9}; 4 query marks;
fresh world with `nep_set/nent_set/nct_set/new_entry` setup identical
to the adversary harness). Requires a `rep_seg` helper, copied verbatim
from committed `router7_adversary/r7_adv_v2.zag` and attributed in a
comment. The section emits `CAP-TABLE-SIZE`, `CAP-ANY-RULE present=`,
and `CAP-PROBE (0,10,0)`, plus a summary line for the VERDICT block.

**Explicitly declined (documented, not implemented):** raising the
24-rule cap or evicting lowest-specificity rules. Rationale: the cap is
a frozen capacity bound (192-byte table, 8 bytes/rule); changing it
alters frozen semantics and every downstream bar. The repair's scope is
trace honesty plus loud non-totality declaration. Cap/eviction remains
future work.

## 4. Frozen kill bars

Raw output: `ROUTER8_RAW_OUTPUT.txt`, direct binary execution (no
`--run` stderr pollution), 3 consecutive runs byte-identical via `cmp`,
exit 0, md5 recorded.

**K-R8-1 (capacity honesty, in-code):** in the CAPACITY-HONESTY section,
`CAP-TABLE-SIZE == 24`, `CAP-ANY-RULE present == 0`, and
`CAP-PROBE (0,10,0) == -1`. Hand-derived from the red team V2 evidence
(24 real rules; 25th entry dropped; fallback refused; probe -1). The
induction is untouched by R8, so these structural facts must reproduce
exactly. FAIL if any differs.

**K-R8-2 (honest trace, external greps on the committed raw):**
within the section delimited by `########## CAPACITY-HONESTY` and
`########## CAPACITY-HONESTY DONE`:
- `grep -c "TABLE-NON-TOTAL"` == 1 (loud warning fired exactly once)
- `grep -c "TABLE-RULE \[any\]->WITHHOLD (explicit fallback"` == 0
  (no phantom fallback line; under R7 this count is 1)
- `grep -c "TABLE-RULE .* (from H"` == 24 (equals CAP-TABLE-SIZE; under
  R7 this count is 25, the stale 25th emit)
- `grep -c "TABLE OVERFLOW"` == 2 (25th entry drop + fallback refusal)
Across the whole raw:
- `grep -c "TABLE-RULE \[any\]->WITHHOLD (explicit fallback"` == 1
  (only the normal-path fallback-loss section emits the real line;
  proves R8-2 did not break the normal path)

**K-R8-3 (no regressions):** all prior bar conditions hold unchanged:
K-R7-1 (fbany==1, fbprobe==10), K-R7-2 (tfam8 bit0), K-R6-1, K-R6-2,
K-R5-1, K-R5-2a/b/c, K-R4-1..5, i.e. the existing verdict conjunction
plus the new K-R8-1 term. The verdict banner becomes
`H-ROUTER8 AUTOMATED BARS PASS`.

**K-R8-4 (determinism):** 3 consecutive full runs byte-identical
(`cmp`), exit code 0, zero FAIL lines, md5 recorded in the result.

**Kill rule:** if any of K-R8-1..K-R8-4 FAILs, H-ROUTER8 is KILLED.
H-ROUTER8 claims bounded L2+ structural learning with provenance
diagnostics and honest capacity signaling. No L3 claimed.

## 5. Files and commits

New files (owned by this researcher):
- `docs/lab/research-lead/overnight-20260928/PREREG_ROUTER8.md` (this file)
- `docs/lab/research-lead/overnight-20260928/router8_learn.zag`
- `docs/lab/research-lead/overnight-20260928/ROUTER8_RAW_OUTPUT.txt`
- `docs/lab/research-lead/overnight-20260928/ROUTER8_RESULT.md`

Commit plan: this prereg committed ALONE before any implementation edit,
build, or run. Result commit afterwards with pathspec-restricted staging
of exactly the four owned files. `git merge-base --is-ancestor` check
before the result commit. No push.

## 6. Methodology and governance

- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp. Zero Python at any stage.
- Binaries built in /tmp only, never committed.
- No em dashes in loop documentation (byte-checked).
- Toolchain pinned: `znc 2026.07.0-dev (edition 2026)`.
- The X-R7-1 V2 fixture is adversary evidence reused as a regression
  fixture, attributed, not presented as new discovery.
