# FREEZE NOTE: world_tneg_a.zag (F3 Phase 3 T-NEG re-freeze)

Date: 2026-09-30. Worker: F3 T-NEG Executor.
Amendment: commit c35da8aa0
(`PREREG_F3P3_AMENDMENT_A.md`, status AMENDMENT-COMPLETE).
Parent prereg: 97287f87c. This note executes re-freeze protocol
steps 2 and 3 of the amendment.

## 1. What was created

`docs/lab/research-lead/overnight-20260928/f3_phase3/world_tneg_a.zag`
is a byte-identical copy of the sealed `world_tneg.zag` with the
amendment-specified `fn main()` block appended after the final
`w_verify` function, preceded by one blank line. No other byte
was added, changed, or removed.

sha256(world_tneg_a.zag) =
`47f38c99d5f96a5f09c7ffa4316ab30ecbff19265e7a7de4002baa32a3324cf4`

## 2. Unified diff (world_tneg.zag vs world_tneg_a.zag)

```
--- world_tneg.zag
+++ world_tneg_a.zag
@@ -84,3 +84,9 @@
             candbuf:[]u8, exhausted:i32, nalive:i32)i32 {
   return 0;
 }
+
+fn main()i32 {
+  let m:i32=L_run();
+  emit("TNEG DONE mask="); e64(m); emit("\n");
+  return 0;
+}
```

## 3. Diff-gate verdict

K1 (executor): PASS. The diff contains only additions: one blank
line plus the six-line main block specified verbatim in amendment
section 2. No modified lines, no deleted lines, no changes to the
sealed w_* interface or the sealed truth. The appended block matches
the amendment text character for character, including the
`TNEG DONE mask=` harness marker (log marker only, not a verdict).

Purity scan: zero em/en-dash bytes (E2 80 93 / E2 80 94) in
world_tneg_a.zag. Zero Python used at any step of creation
(cp, printf, diff, sha256sum, grep only).

## 4. Freeze record

- Frozen artifact: world_tneg_a.zag (sha256 above).
- Original sealed world_tneg.zag: unmodified, still in history.
- Freeze commit: 179ec88a40336835aa8f610cf9e1d8643899c2ec
  (recorded in this note by follow-up commit 179ec88a4^..HEAD touching
  this note only; the frozen artifact is unchanged and no build or
  test ran before the freeze commit).
- Rule: no build or test may run before the freeze commit exists.
