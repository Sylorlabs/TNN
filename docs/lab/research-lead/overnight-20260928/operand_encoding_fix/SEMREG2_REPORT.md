# SEMREG2_REPORT.md -- K6 semantic regression RE-RUN after instrument repair (W-SEMREG2)

Lane: `docs/lab/research-lead/overnight-20260928/operand_encoding_fix/`
Branch: tnn-native-lab. Local only, never pushed.
Amended prereg: PREREG_K6_AMEND.md (commit c409e1ad80d70d1892585e8d20febd1b4cb9e29b, verified below).
Original prereg: 447f087af. Implementation: fd79576d4.
W-SEMREG's original K6 run (SEMREG_REPORT.md, commit 2d98e3ecd): both builds panicked
byte-identically in tnn2_init (fossil z_alloc(110656) test workspaces vs ~4.7MB layout);
battery never executed, K6 verdict FAIL as frozen.

## Governance gate

Before any repair work: `git log --all` was polled (60s x up to 30 tries) for a commit
containing "fresh prereg amending K6 measurement". First 15 tries: absent. Try 16 (~16 min
in): FOUND.

Commit: `c409e1ad80d70d1892585e8d20febd1b4cb9e29b`
Message: "OPERAND-ENCODING-FIX: fresh prereg amending K6 measurement (repair fossil 110656
test allocations; bars unchanged). Local only, never pushed."
`git show --stat` on that commit: exactly 1 file changed, 56 insertions:
`docs/lab/research-lead/overnight-20260928/operand_encoding_fix/PREREG_K6_AMEND.md`.
No repair work was performed before this commit was observed.

## Step 0: Toolchain guard (2026-10-02)

Executed after gate confirmation, before any repair:

```
export PATH="$HOME/safebin"
PATH=/home/hatch/safebin
which python3  -> (empty; rc=1)
which python   -> (empty; rc=1)
```

Result: PASS. All commands ran with PATH=/home/hatch/safebin only (pinned znc +
coreutils/git; safebin confirmed to contain znc, no python3/python). All computation
pure Zag; shell used only for znc invocation, binary execution, git ops, file movement
(sed/cp/cat/diff/grep/wc). No forbidden-executable invocation occurred. No PROCESS-FAIL
condition triggered.

## Repair (per amended prereg, steps 1-2)

1. Copies only:
   `cp scaling_5000_fixed/s6_base.zag /tmp/k6fix_old_base.zag`
   `cp operand_encoding_fix/oe_base.zag /tmp/k6fix_new_base.zag`
   Committed bases never modified (verified: both still contain 49x `z_alloc(110656)`).

2. Mechanical replacement on both copies identically:
   `sed -i 's/z_alloc(110656)/z_alloc(4722752)/g'`
   Old copy: 49 occurrences before -> 0 remaining, 49x `z_alloc(4722752)` after.
   New copy: 49 occurrences before -> 0 remaining, 49x `z_alloc(4722752)` after.
   (Variants `W2`/`a`/`b` allocations included; all are t_* test workspaces fed to tnn2_init.)
   No 4722752 existed in either copy before the edit.

3. Diff verification: `diff /tmp/k6fix_old_base.zag /tmp/k6fix_new_base.zag` (37 changed
   lines) shows ONLY:
   - the 7-line header revision comment (BASE REVISION: operand-encoding fix ...), and
   - the 8 frozen operand-encoding hunks: `res_op` decoder, `t2_set` dest check,
     `t2_inc`, `t2_dec`, the stale-comment rewrite, and the 4 encoder sites
     (`10000+slot/dst/src` -> `-1-slot/-1-dst/-1-src`).
   The uniform allocation change cancels (applied identically to both). No other delta.
   Check passed; repair proceeded.

## Build (step 3)

`/tmp/runall_main2.zag` (minimal main, calls `run_all()`, emits RUNALL-RC + rc):
```
fn main()i32 {
  let r:i32=run_all();
  emit("RUNALL-RC ");
  e64(r);
  emit("\n");
  return r;
}
```
(`emit`/`e64` confirmed present in base; no `fn main` in base or patch; no signature
conflicts.)

- OLD: `cat /tmp/k6fix_old_base.zag scaling_5000_fixed/s6_patch.zag /tmp/runall_main2.zag > /tmp/k6fix_old.zag`
  then `znc /tmp/k6fix_old.zag -o /tmp/k6fix_old_bin` -> rc 0, 145 analyzer warnings,
  binary 263254 bytes.
- NEW: `cat /tmp/k6fix_new_base.zag scaling_5000_fixed/s6_patch.zag /tmp/runall_main2.zag > /tmp/k6fix_new.zag`
  then `znc /tmp/k6fix_new.zag -o /tmp/k6fix_new_bin` -> rc 0, 145 analyzer warnings,
  binary 263174 bytes.
- Warning count identical (145/145). The concatenated-source diff old-vs-new is
  byte-identical to the base-only diff (verified: same 37 changed lines).

## Execution (step 4)

- OLD: `timeout 1800 /tmp/k6fix_old_bin > k6fix_old_runall.log` -> completed ~5.7 min,
  battery rc=1 (1 failing test), OLD-RC=1.
- NEW: `timeout 1800 /tmp/k6fix_new_bin > k6fix_new_runall.log` -> completed ~5.6 min,
  battery rc=1, NEW-RC=1.

Both batteries now execute to completion (no panic): the repair worked.

## Per-test comparison (step 5)

- `diff` of the two logs (excluding the appended OLD-RC=/NEW-RC= label lines):
  BYTE-IDENTICAL. 74 lines each.
- Per-test PASS/FAIL vectors: identical, every test, both builds. 68 PASS lines each.
- TOTAL line: `TOTAL 45/46` on both.
- FAIL lines: exactly one on each: line 6, `C6 FAIL` (both).
- `T2-REVISE PASS` on both, including the NEW build.

Full log (identical old/new):
C1 PASS, C2 PASS, C3 PASS, C4 PASS, C5 PASS, C6 FAIL, C7..C15 PASS,
A1..A6 PASS, P1..P7 + F2/P2b/P3a/P3b/ABL-I/ABL-C (all PASS),
DV PASS, XCAP PASS, R-PACT1..6 PASS, T2-CHAIN4 PASS, T2-REJECT PASS,
T2-INQUIRE PASS, T2-ACTLIVE PASS, T2-REVISE PASS, TOTAL 45/46, RUNALL-RC 1.

## t_c6 status (explicit)

C6 FAILS on both builds, byte-identically. W-SEMREG's audit prediction (FAIL on both:
field4=1000 rejected by old `d<10000` and new `d>=0` dest checks) is now CONFIRMED
EMPIRICALLY on the repaired instrument. Zero divergence old-vs-new on this test.

## K6 verdict: PASS

Per the unchanged verdict rule in PREREG_K6_AMEND.md:
(a) per-test PASS/FAIL vectors identical old-vs-new: YES (byte-identical logs,
    same single FAIL = C6).
(b) T2-REVISE passes on the new build: YES (`T2-REVISE PASS` in k6fix_new_runall.log).
No test diverges old-vs-new; no reinterpretation needed. The operand fix introduced zero
observable semantic divergence in the full run_all battery (45/46 on both, same test failing).

## Files

- `k6fix_old_runall.log` -- OLD build stdout (74 lines, TOTAL 45/46, C6 FAIL)
- `k6fix_new_runall.log` -- NEW build stdout (74 lines, byte-identical modulo rc labels)
- `SEMREG2_REPORT.md` -- this file

Committed bases, patch, driver untouched. Test mains and concatenated sources stayed in
/tmp (ephemeral). Other workers' files in this lane were not touched. Commits local,
never pushed.

## Caveats

- The repaired copies are measurement scaffolding in /tmp per the amendment; they are
  not committed as base files and the committed bases still carry the fossil 110656
  allocations (preserving them for any future frozen-base work).
- run_all on this lineage was previously unexecuted; the repaired battery is the first
  run_all execution on the s6 base lineage. W-SEMREG's "zero test lines in s6_run1.txt"
  observation is consistent with this.
