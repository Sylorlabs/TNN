# P2 #8 proof correction (2026-09-27)

Commit `ca2cabd77ad44a07c03407c0621aceb99b85d4bb` ("Fix-or-kill P2 #8")
is CORRECT in its code changes and in its verdict (renders are
byte-identical), but its commit message recorded two SHA-256 values for
the `desynth_render` flat/contour proof that were **never measured**:
the proof run was aborted by infrastructure (disk-crisis cleanup removed
the proof directory mid-run), and the SHAs were written from the
intended run rather than an observed one. That is a recording error, not
a code error. The proof was re-run in full on 2026-09-27 (pinned znc
`abed8aa1`, `atom0_child.bin` from `~/workspace/desynth/atoms/`):

## Corrected measurements

| Binary | Mode | Old SHA-256 | New SHA-256 | Verdict |
|---|---|---|---|---|
| `desynth_render` | flat (f0=220000, amp=1000000) | `58d9a1544702fa8eb841780fcfc6e7aaaaba9194f3c153a118d0e2fc3718e944` | identical | BYTE-IDENTICAL |
| `desynth_render` | contour (16x220472 mHz) | `6cac56911b4d545c92685817a79c6edfd661e6f50555d24e5d4695253ef2fa7a` | identical | BYTE-IDENTICAL |
| `render_plan` standalone (`render_main` driver, amode0/f0=890172/p1=1000000) | fixed verification plan | `196deadec6be9b11561edbf13529aab9db2555bb810ad3df55ca109a85192da7` | identical | BYTE-IDENTICAL (measured in the original session; stands) |

Additionally verified: the planner's `render_plan` copy in
`plan_main_desynth.zag` is code-identical to the standalone copy
(comment lines stripped before diff); a planner compile shows zero
`render_plan` errors (only unrelated missing `hear` helpers from the
partial assembly).

## What was wrong in the original message

The original message listed `6d6c0fda...` (flat) and `c3b8d1...`
(contour) for `desynth_render`. Those values were never produced by any
run and must be disregarded. The corrected values above replace them.

## Standing lesson

Never record a measurement from an intended run. If the proof
infrastructure dies mid-run, the proof is un-run until it is re-run --
the verdict column stays empty, not filled from expectation, however
certain the dataflow analysis makes the outcome.
