# URGENT FLAG for the parent final report: Decisions 4A/4B (frozen files not in HEAD)

Lane: URGENT-FLAG (replacement worker), wave-20261001-2321pdt. Written 2026-10-02.
Source (read only): ESCALATION-UPDATE/ESCALATION_UPDATE.md.

## The flag, in one paragraph

**Decisions 4A and 4B are urgent and should be presented to Micah before this wave
closes.** The wave's 47 verdicts rest on frozen bytes, specifically tnn2.zag,
freeze_shim2_bin, and the pinned znc binary, that exist only as untracked files on
this disk. They are not in HEAD. A single `git clean -fdx`, a VM replacement, or a
fresh checkout of branch tnn-native-lab destroys them, and with them the
reproducibility of every frozen-battery verdict in this wave's final report. The
decisions needed are 4A (commit the minimal pinned set into HEAD, roughly 30 files
and 30 MB) and 4B (take a protective tar snapshot of the full untracked set with a
SHA-256 manifest, stored alongside the bundle backups). Both require Micah's
approval. Nothing has been done yet; nothing can safely be done yet.

## The facts (verified by this worker, 2026-10-02)

- Working copy is ~/workspace/tnn-rsi, branch tnn-native-lab (verified).
- The three frozen artifacts pinned by SHA-256 in the post-freeze battery prereg
  (BATTERY/PREREG_POSTFREEZE.md, section 0) are present on disk and byte-identical
  to their pinned hashes, but `git ls-files` confirms tnn2.zag and freeze_shim2_bin
  are NOT tracked in HEAD, and the escalation lane verified the pinned znc binary
  is not tracked either:

  | Artifact | Pinned SHA-256 | In HEAD |
  |---|---|---|
  | tnn2.zag (docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag) | a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd | No |
  | freeze_shim2_bin (docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin) | 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954 | No |
  | pinned znc linux x86_64 (src/tools/toolchain/znc_linux_x86_64_abed8aa1) | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef | No |

- A fresh clone of tnn-native-lab would contain no compiler and no frozen source.
  HEAD tracks only the files inside the current wave dir; everything outside it,
  including the toolchain and the freeze artifacts, is untracked working-tree bytes.
- This wave ran only because those bytes happen to be on this disk.

## What is at risk

1. **Freeze reproducibility.** The PF-K3 kill bar (frozen binary integrity) compares
   live bytes against the pinned SHA-256 hashes at sealed-eval time. If the bytes
   disappear, the claim "frozen tnn2.zag untouched" becomes unverifiable, not false.
   Six lanes froze kill bars against the tnn2.zag baseline (a29972ca...); a bar that
   cannot be re-run is a record, not a control.
2. **Kill bar integrity.** Future workers cannot re-verify the baseline their
   verdicts reason about if the pinned file is gone or silently replaced.
3. **The toolchain guard.** The worker toolchain guard's safebin links znc to an
   untracked path. The pure-Zag constraint is enforceable today; on a fresh checkout
   it fails open, because there is no compiler at all.

Note the scope boundary: this is separate from the 140,541-file / 6.26 GB bulk
untracked set, which is mostly run exhaust from prior waves. The critical set is
three artifacts plus provenance and freeze evidence, on the order of 30 files and
about 30 MB.

## The decisions needed (from the REPO-SCOPE lane's recommendation, presented for approval)

**Decision 4A (URGENT):** Approve committing the minimal pinned set into HEAD so the
frozen battery and the toolchain guard survive a fresh checkout. The ask is no longer
"restore 142k files or leave them"; it is "protect the load-bearing 30 first": the
three znc binaries, the pinned znc provenance JSON
(src/tools/toolchain/R32_ZNC_PROVENANCE_2026-08-23.json), tnn2_build/tnn2.zag,
core_freeze_tnn2_shim/freeze_shim2_bin, and their freeze evidence files. Roughly 30
files, roughly 30 MB.

**Decision 4B (URGENT):** Approve the tar snapshot of the full untracked set
(6.26 GB), stored alongside the existing git bundle backups with a SHA-256 manifest,
recorded in the wave RECORD. This is insurance regardless of the answer to 4A, and it
is the precondition the lane names for ever allowing `git clean -fdx` in this working
copy again.

## The rule until 4A/4B are decided

**`git clean -fdx` is FORBIDDEN in this working copy until 4A and 4B are complete.**
The freeze artifacts currently live in untracked space. No worker should run any
destructive cleanup, re-checkout, or VM hygiene step in this working copy without the
parent confirming these two decisions first.

## Timing

The parent must get Micah's decision on 4A and 4B BEFORE the wave closes. Once the
wave closes and the working copy is recycled, there may be no second chance: the
bytes that underpin the 47 verdicts would be gone, and the final report's freeze
claims would rest on hashes that no longer resolve to anything. Present this at the
top of the final report, not in an appendix.
