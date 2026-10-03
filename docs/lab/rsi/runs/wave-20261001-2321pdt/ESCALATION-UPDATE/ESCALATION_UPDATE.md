# ESCALATION UPDATE: frozen files not in HEAD (addendum to ESCALATION-LIST item 4)

Lane: ESCALATION-UPDATE (replacement worker), wave-20261001-2321pdt. Date: 2026-10-02.
Read only source: REPO-SCOPE/REPO_SCOPE_ASSESSMENT.md (replacement worker's completed lane).
Zero em/en dashes verified with check_no_dash.sh before commit.
This addendum supersedes the framing of item 4 in ESCALATION_LIST.md. Items 1, 2, 3, 5,
6, 7, I1, I2, I3 are unchanged.

## 1. The critical finding

The REPO-SCOPE replacement worker verified that the three frozen artifacts pinned by
SHA-256 in the post-freeze battery prereg
(BATTERY/PREREG_POSTFREEZE.md, section 0) exist on disk, verify byte-identical to the
pinned hashes, but are NOT in HEAD. They are untracked working-tree bytes only:

| Artifact | Pinned SHA-256 | In HEAD |
|---|---|---|
| tnn2.zag (docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag) | a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd | No |
| freeze_shim2_bin (docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin) | 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954 | No |
| pinned znc linux x86_64 (src/tools/toolchain/znc_linux_x86_64_abed8aa1) | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef | No |

A fresh clone of branch tnn-native-lab would contain NO compiler and NO frozen source.
HEAD tracks only 6,322 files, all inside the current wave dir. Nothing outside the wave
dir is tracked. The wave runs today only because untracked bytes happen to be on this
disk.

## 2. Why it matters

Three load-bearing systems rest on these untracked bytes:

- **Reproducibility of the freeze itself.** The PF-K3 kill bar (frozen binary integrity)
  asserts that frozen artifacts are unchanged at sealed-eval time, comparing live bytes
  against the pinned SHA-256 values. The bar passes only if the bytes are present. One
  `git clean -fdx`, one VM replacement, one fresh worktree checkout, and the freeze
  evidence is destroyed while the prereg still names the hashes. The claim "frozen
  tnn2.zag untouched" would become unverifiable, not false.
- **Kill bar integrity.** Six lanes froze kill bars against the tnn2.zag baseline
  (a29972ca...). If the pinned file disappears or is silently replaced, future workers
  cannot re-verify the baseline they reason about. A bar that cannot be re-run is a
  record, not a control.
- **Toolchain guard.** The worker toolchain guard's safebin links `znc` to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1, an untracked path. The pure-Zag
  constraint is enforceable today; on a fresh checkout it fails open, because there is
  no compiler at all. The guard's instruction-level reporting becomes moot if the
  environment itself is lost.

Note the scope: this is separate from the 140,541-file / 6.26 GB bulk untracked set.
Most of that is run exhaust from prior waves and generations. The critical set is
three artifacts plus their provenance and freeze evidence, on the order of 30 files
and about 30 MB.

## 3. The REPO-SCOPE recommendation (presented for approval, not adopted)

The REPO-SCOPE lane recommends AGAINST restoring all 140,541 files into HEAD. It
recommends instead:

- (a) Track a minimal pinned set: the three znc binaries, the pinned znc provenance
  JSON (src/tools/toolchain/R32_ZNC_PROVENANCE_2026-08-23.json), tnn2_build/tnn2.zag,
  core_freeze_tnn2_shim/freeze_shim2_bin, and their freeze evidence files. Roughly 30
  files, roughly 30 MB, protecting the PF-K3 kill bar and the toolchain guard.
- (b) Take a protective tar snapshot of the full untracked set with a SHA-256 manifest,
  stored alongside the existing git bundle backups (the bundle v16 pattern), recorded
  in the wave RECORD. This preserves the audit trail behind prior verdicts without
  putting 6.26 GB into git.
- (c) Record explicitly in the wave dir that `git clean -fdx` is FORBIDDEN in this
  working copy until (a) and (b) are complete, because the freeze artifacts currently
  live in untracked space.
- (d) Do NOT restore .github workflows, archive tarballs, or media into HEAD; dormant.

Caveat from the lane: it verified provenance and integrity only for the three frozen
artifacts and the znc binary. The bulk 140k set was counted and classified, not
checksum-verified. If he wants the audit trail independently re-verifiable, a full
checksum manifest pass is the next step before the snapshot in (b).

## 4. Decisions needed from Micah

**Decision 4A (updated):** Approve committing the minimal pinned set (roughly 30
files / 30 MB) into HEAD so the frozen battery and the toolchain guard survive a
fresh checkout? This changes the previous item-4 framing: the ask is no longer
"restore 142k files or leave them"; it is "protect the load-bearing 30 first, as the
lane recommends".

**Decision 4B (new):** Approve the tar snapshot of the full untracked set (6.26 GB)
stored alongside the bundle backups, with a SHA-256 manifest, before any cleanup?
This is insurance regardless of his answer to 4A, and it is the precondition the
lane names for ever allowing `git clean -fdx` in this working copy again.

Recommended framing for the parent: lead with 4A and 4B as the urgent pair, because
the frozen-battery verdicts in this wave's final report rest on bytes that are one
accidental command away from being gone. Item 4's old options (full restore vs leave
as working-tree recovery source) are superseded: full restore is rejected by the
lane for harm, and "leave as recovery source" is unsafe without the snapshot.
