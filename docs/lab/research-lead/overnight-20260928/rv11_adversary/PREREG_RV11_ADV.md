# PREREG H-REVISE11 ADVERSARY (RV11-ADV): FROZEN

**Date (UTC):** 2026-09-30
**Target:** H-REVISE11 (result commit `1a2fd99bd`; prereg `36b2fbc71`;
claim: SURVIVES 145/145, R10 in-function contradiction guard sound,
P3b precondition violation handled by guard, Branch B correct-member
veto unreachable post-R10, exact counts 145/129/16/2xGUARD).
**Stance:** the claim is false. Kill criteria are frozen below.

**This prereg is committed alone, before any attack code, build, or run.
No amendments. Pure Zag throughout (implementation, fixtures, builds,
runs, analysis via shell grep/cmp/md5/diff only). No em dashes.**

## Inspection already performed (not attacks)

Read PREREG_REVISE11.md, REVISE11_RESULT.md, revise11.zag (1978 lines),
REVISE11_RAW.txt. Established: 129 CHECK lines all PASS; 0 failing
CHECKs; 2 GUARD lines at raw lines 276 (inside P3b banner window
273-291) and 295 (inside Q1 banner window starting 292); RESULT
145/145; raw md5 `0fcb31f29db9d05a1c80809aa78619c3` matches the frozen
value; 145 `ntest_total` increments in source; the 2 raw lines
containing "FAIL" are expected `CORROBORATE FAIL:` diagnostics inside
passing withhold phases (L4, M1); the revise10-to-revise11 diff touches
only `//` comments, the `=== H-REVISE` banner emit, and the two
`H-REVISE1x SURVIVES/KILLED` verdict emits; `vs3_firing_set` orders
most-recent-first.

## Harness construction (frozen)

`rv11_adv.zag` = lines 1-838 of the frozen `revise11.zag` blob at
`1a2fd99bd` (everything before `fn main`), verified byte-identical via
`cmp` against `git show 1a2fd99bd:...`, plus an attack-only `fn main`.
Zero mechanism lines edited. Builds in /tmp/rv11adv only; no binaries
committed. Raw output `RV11_ADV_RAW.txt`, 3/3 byte-identical runs.

## X-RV11-1: guard soundness (P3b replication + overreach attempt)

Replicate the P3b fixture exactly (P0=p0a ["zbq"->"qqq"]; slot1
(0,122) wprogP wrong; slot2 (1,98) p0aP correct most-recent; input
"zbq"; trusted label "qqq"). Assert: `diagnose_rollback_check` returns
exactly 0; both slots remain PROVISIONAL (status 1); the call emitted
the GUARD line. Then attempt the overreach construction: search for any
store where the guard fires (store predicts the passed label) yet the
claim's own definition requires action (a revision that overrode a
correct prediction on this input). By the claim's definition, override
requires store-with-revision mispredicting while store-without predicts
the label; a firing guard means the store predicts the label, so no
override exists. The attack is the attempt plus this definitional
closure; a found counterexample KILLS.
Out-of-scope robustness probe (no kill criterion): one call with a
20-byte input against the fixed 16-byte scratch buffers, documented as
an observation only.
KILL if: P3b replication deviates (rb!=0, state change, GUARD absent),
or an overreach counterexample is constructed.

## X-RV11-2: exact counts (independent recount)

Rebuild pristine from the frozen blob; 3/3 byte-identical; md5 must
equal `0fcb31f29db9d05a1c80809aa78619c3`; source must contain exactly
145 `ntest_total` increments; raw must contain exactly 129 CHECK lines
all PASS and 0 failing CHECKs; GUARD must appear exactly 2 times, one
inside the P3b banner window and one inside the Q1 banner window.
KILL on any mismatch.

## X-RV11-3: Branch B veto reachability (brute-force sweep)

The prereg discloses the Branch B correct-member veto (`allmiss==0`
path, silent return 0) as unreachable post-R10. Sweep the
configuration space: 1-3 revision slots; per slot cpos in {0,1,2},
cval in {98,113,122}, program in {p0aP correct, wprogP wrong, p0bP
identity}, status in {1,2}; P0=p0aP (second sweep P0=p0bP); input
"zbq"; trusted label "qqq". Per configuration: rebuild a fresh store;
skip when the store predicts the label (guard would fire; verified
with the guard's exact condition); compute the firing set and
`allmiss` with the mechanism's own helpers; call
`diagnose_rollback_check`; record rb and per-slot status before/after.
VETO-REACHED iff allmiss==0 AND rb==0 AND zero status change (the
guard never fires in this sweep, so silent-0 with allmiss==0 uniquely
identifies the veto path). DOWNGRADE if any VETO-REACHED (the
unreachability disclosure is false). KILL if additionally a wrong
PROVISIONAL firing member survives the call (core claim violated: a
genuine contradiction failed to fell it).

## X-RV11-4: regression diff audit (revise10 -> revise11)

Programmatic hunk audit of
`aa422610f:revise10.zag` vs `1a2fd99bd:revise11.zag`: every added or
removed line must be a `//` comment line, the `=== H-REVISE` banner
emit, or one of the two `H-REVISE1x SURVIVES/KILLED` verdict emits.
KILL if any changed line falls outside these categories.

## Verdict rules

Any KILL criterion firing KILLS H-REVISE11. A DOWNGRADE criterion
firing (X-RV11-3 reachability without survivor violation) DOWNGRADEs it.
Otherwise H-REVISE11 SURVIVES this red team. All evidence committed to
`tnn-native-lab` under `docs/lab/research-lead/overnight-20260928/rv11_adversary/`.
Only owned paths staged.
