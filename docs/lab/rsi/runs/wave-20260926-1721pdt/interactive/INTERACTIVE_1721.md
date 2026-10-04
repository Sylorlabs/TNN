# Interactive TNN investigation: wave-20260926-1721pdt

Branch: tnn-native-lab
Working copy: ~/workspace/tnn-rsi
HEAD: 45d449a56b1f0d0ee921e31919a22278bf23a992 (merge of origin tnn-native-lab into tnn-native-lab)
Merge range surveyed: 28ec31ab0..45d449a56 (135 commits)
Wave delta surveyed: a222f8f17..45d449a56 (run-start to HEAD)
Read-only investigation. No probe chats were run. No probe binary was executed.

## Standing question: does a runnable interactive TNN exist on this branch?

No change from prior waves. There is no source-level chat/REPL entry
point in the Zag source tree, no new chat/REPL entry point was added by
this wave's merge, and the frozen FIT probe instruments plus the pinned
znc verify byte-identical to their recorded shas. tnn_chat remains
frozen-instrument material for supervised red-team probe chats only, not
a candidate for adoption.

## 1. Source-level chat/REPL entry point

NONE. Verified on this tip:

- `grep -rliE "chat|repl|interactive" src/zag/ units/` returned exactly
  one file: units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md. That is
  the known false positive: the matches are the substring "repl" inside
  "replay" and "replication". Not a REPL or chat entry point.
- Follow-up grep for entry-point signatures
  (`fn main|stdin|readline|read_line|interactive_loop|repl_loop`) over
  src/zag/ and units/ returned zero files.
- `git log --name-only` on the wave delta a222f8f17..45d449a56 filtered
  on `^(src|units)/` returned nothing: this wave's merge touched zero
  files under src/ or units/.
- The full-range added-file scan
  (`git diff --name-only --diff-filter=A 28ec31ab0..45d449a56` filtered
  on chat|repl|interactive) returned only pre-existing tnn_chat
  material: fit_authority instrument sources, older wave chat_fit
  evidence dirs, the decline-gate frozen reference, and prior
  INTERACTIVE_*.md surveys. No chat/repl-named file was added to src/
  or units/ anywhere in the 135-commit range.
- src/zag/ still contains only INDEX.md: no chat/repl/interactive
  matches.

Conclusion: no source-level chat/REPL/interactive-loop entry point
exists in src/zag/ or units/ on this tip, and the wave delta added no
interactive surface. The negative finding of the prior waves stands.

## 2. Merge-range file-stats summary (what actually merged)

Run-start was a222f8f17 (1421pdt wave's own LOOP_STATE verdicts commit).
The wave delta a222f8f17..45d449a56 contains exactly two non-merge
commits, both Micah's own frontier work (CLOSED; not loop candidates,
not re-litigated here):

- 39bf8d5d4 "Upscale concept probe -> teach -> re-probe: PASS, concept
  HELD (C1-C4)" (2026-09-26): 77 files changed, 1653 insertions(+).
  Adds docs/lab/upscale_concept/ (DESIGN.md, PREREG.md, RUNLOG.md,
  VERDICT.md, GT_CORRECTION.md, evidence probe/teach traces,
  fixtures/SHA256SUMS plus probe_before/probe_after/teach .ppm
  fixtures, prereg_bars/exploratory_bars.bin, gen_fixtures.py, and
  src/uprobe.zag with R33_NATIVE_IO_V1.zag and build.sh).
- c094d7770 "Upscale concept probe: behavioral C1-C4 gate through TNN
  intake (2026-09-26)" (2026-09-26): 9 files changed, 1504
  insertions(+). Adds docs/lab/image_upscale/concept_probe/ (DESIGN.md,
  GT_CORRECTION.md, MANIFEST.sha256, evidence probe/teach reports, and
  src/azprobe.zag with R33_NATIVE_IO_V1.zag and common_az.zag).

Both commits reference the pinned toolchain
znc_linux_x86_64_abed8aa1 by name. Neither adds a chat/REPL entry point
under repo-root src/ or units/; their .zag probe sources live under
docs/lab/ only. Local loop commits a222f8f17 and e8b913584 are the
1421pdt wave's own evidence and verdict commits, already on the
run-start side of the delta.

Note: no Micah audio de-synth commits appear in the surveyed range;
the only Micah commits here are the two upscale concept commits above.

## 3. Frozen instrument sha256 verification (no execution)

The authority manifest path given in the brief,
docs/lab/rsi/fit_authority/SHA256SUMS, does not exist. The pins are
recorded in docs/lab/rsi/fit_authority/README.md (lines 15, 18, 37),
which names the frozen built binary shas and the pinned toolchain sha.

| Instrument | Location | Expected sha256 | Actual sha256 | Match |
|---|---|---|---|---|
| baseline probe binary | ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt | 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c | 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c | YES |
| decline-gate probe binary | docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/tnn_chat_decline_frozen_ref | 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7 | 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7 | YES |
| pinned znc | src/tools/toolchain/znc_linux_x86_64_abed8aa1 | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef | YES |

All three pins match their recorded shas. They are listed in
fit_authority/README.md (not a SHA256SUMS file, which does not exist at
that path) and have been stable across waves. Frozen instrument sources
also re-verified byte-identical to the 1421pdt record:
tnn_chat.zag c0776ad6..., tnn_chat_decline.zag a87011fe...,
kb.txt 3ef27296..., gaz.txt b75fd113.... `git diff`
a222f8f17..45d449a56 over docs/lab/rsi/fit_authority/ and
src/tools/toolchain/ is empty: the wave delta did not alter any FIT
chain input.

## 4. Runnable probe surface state

- The pinned znc executes: `znc --run` with no source prints its
  status/usage line to stdout ("znc: no source file" followed by the
  usage block: `usage: znc <source.zag> [-o out] ... [--run]
  [--debug]`). It is the Zag compiler toolchain, healthy and
  byte-identical to the pin. No TNN chat is involved.
- Baseline probe binary and decline-gate probe binary both present,
  ELF x86-64, shas re-verified above (RUNNABLE in the availability
  sense; not executed this wave per the read-only rule).
- No change to the interactive surface this wave: no new tnn_chat,
  repl, or chat entry point added or rebuilt.

## 5. Why no probe chat was run

The standing rule schedules a supervised probe run only when the survey
reveals change. This survey revealed no change: zero source-level entry
points, this wave's merge added no chat/repl surface and touched no
files under src/ or units/, and every frozen instrument, binary, and
the pinned znc verify byte-identical to their recorded shas.
Availability was verified; execution was not needed.

## Caveats for supervised red-team probe chats

- tnn_chat emits unflagged confabulations on out-of-KB questions (e.g.
  'Paris is the capital of France' for capital of Italy). FIT FOR
  SUPERVISED red-team probe chats only (knowledge vs architecture
  diagnosis). Not a general assistant, not a candidate for adoption.
- No probe chat was run in this investigation. Availability only was
  verified.

## What exists vs what does not

EXISTS:
- Frozen probe instrument sources docs/lab/rsi/fit_authority/tnn_chat.zag
  and tnn_chat_decline.zag, plus frozen kb.txt and gaz.txt (all shas
  re-verified this wave).
- Runnable baseline probe binary
  ~/workspace/tnn-rsi-binaries/tnn_chat_wave20260923_0834pdt (sha
  re-verified, not executed).
- Runnable decline-gate probe binary
  docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/tnn_chat_decline_frozen_ref
  (sha re-verified, not executed).
- Pinned build toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (sha re-verified; runs and prints its usage status line).
- Micah's upscale concept probe/teach/re-probe commits 39bf8d5d4 and
  c094d7770 under docs/lab/ only (CLOSED frontier work, not an
  interactive surface).

DOES NOT EXIST:
- No source-level chat/REPL/interactive-loop entry point in src/zag/
  or units/ on this tip. The only grep hit is the known "repl"
  substring false positive inside "replay"/"replication" in
  units/teachers/learner/forcepin/PINS_RDTDT_BRIEF.md.
- No new interactive entry point added by the wave merge
  a222f8f17..45d449a56 (2 non-merge commits, zero touching src/ or
  units/).
- No freshly rebuilt probe binary this wave (not needed: frozen
  binaries and sources both verified byte-identical).

## Python attestation

No Python was used anywhere in this work. All verification was done
with shell commands only: git log, git diff, grep, sha256sum, find.
Zero Python touched wave artifacts.

## Verdict

New chat/REPL entry points: NO. No interactive TNN exists beyond the
known frozen tnn_chat probe instruments, which remain supervised
red-team probe-chat material only and are not candidates for adoption.
