# Wave-close checklist: wave-20261001-2321pdt

Prepared by the CLOSE-PREP lane (replacement worker), 2026-10-02 ~00:47 PDT.
Status evidence is quoted from lane files read at that time; the checklist
adopts no new verdicts. Read-only toward every file named below.

Legend: DONE = landed and verified by file inspection. PENDING = not yet done.
Owner is who acts, not who already did the prep work.

## 1. Debate lands

**Status: DONE.**

- Judge ruling landed: DEBATE/JUDGE_RULING.md (commit d61447693).
- DEBATE.md written at the wave root and committed (commit cad168d3a,
  "DEBATE.md committed (8 rulings: 6 UPHOLD, 2 OVERTURN). Local only, never pushed.").
- Verbatim probe verified: the skeptic's verbatim provenance probe
  ("What is the provenance of the artifacts under judgment, and what exactly
  is new versus inherited?") is present in DEBATE/SKEPTIC_BRIEF.md and is
  recorded as verified in DEBATE.md. All three briefs (advocate, skeptic,
  judge) are present in DEBATE/.
- Rulings: UPHOLD on Q1, Q3, Q5, Q6, Q7, Q8; OVERTURN on Q2 (further narrowing
  of H-PI-REV2) and Q4 (narrow mandate for BATTERY-E3 blind re-examination).
  The 5 RT-GOV governance decisions were excluded from debate (Micah's alone).
- Owner: coordinator / debate group (complete).

## 2. SENSORY verdict lands (or wave closes without it, recorded as pending)

**Status: PENDING.**

- As of the 00:41 PDT check (SENSORY-CHECK/SENSORY_STATUS.md), the lane is
  PROGRESSING NORMALLY and needs no help: H2v1 FORWARD-SCATTER DECK FIELD is
  implemented, smoke-tested, and committed (5ca243f10, prereg frozen alone at
  58a1a0d7f). Renders h2v1a finished (07:37 UTC), h2v1b mid-render (~row
  640/960 at 00:41 PDT); h2v1c, the KB1-KB11 verifier, and the verdict remain.
- Expected verdict window was roughly 45 to 60 minutes after the 00:41 PDT
  re-check (about 01:26 to 01:41 PDT). No intervention needed.
- If the verdict lands before close, the coordinator picks it up into the
  wave record and the final report. If it does not, the wave closes without it
  and the verdict is recorded as pending pickup by the next wave.
- Owner: coordinator.

## 3. RT-F2V3 verdict lands (or recorded as pending)

**Status: PENDING.**

- As of the 00:43 PDT check (RT-F2V3-CHECK/RT_F2V3_STATUS.md), the review is
  PROGRESSING and not stuck: the reviewer is red-teaming the F2V3 lane's
  depth-9 BUILD-PASS (commits 5e4e56a5f, b5fcf9ae3, 30a1ff7e0, d0846df90 all
  verified). Only the NAMECHECK is written so far; no review verdict yet. The
  lane was 20 minutes old at the check; the check recommended re-checking in
  60 to 90 minutes.
- If the verdict lands before close, the coordinator picks it up into the wave
  record and the final report. If it does not, the wave closes without it and
  the verdict is recorded as pending pickup by the next wave.
- Owner: coordinator.

## 4. Parent's final report: sections (a) through (f) complete

**Status: PARTIAL. Parent to complete.**

- DONE: (a) The 47 verdicts, (d) Queued next (12 items), (f) Escalation items
  (7) are all present and structurally verified in
  PARENT-PREP/PARENT_REPORT_SECTIONS.md (see FINAL-CONFIRM/FINAL_CONFIRM.md).
- PENDING at parent level:
  - (b) Debate outcomes. Was marked pending in PARENT-PREP because the debate
    had not landed when that lane ran; DEBATE.md has since landed (see item 1),
    so (b) is now assemblable from DEBATE.md.
  - (c) Per-fork results. No per-fork result doc assembled; the fork battery
    aggregate is verdict 1 (59 refs, 0 FAIL) in VERDICT-LIST/VERDICT_LIST.md.
  - (e) LOOP_STATE text. Draft insertion text prepared by LOOPSTATE-DRAFT
    (LOOPSTATE-DRAFT/LOOPSTATE_DRAFT.md, ~64 KB); the parent assembles it here
    when appending the insertion text (item 5).
- The URGENT-FLAG (Decisions 4A/4B, item 8) belongs at the TOP of the final
  report, not in an appendix, per URGENT-FLAG/URGENT_FLAG.md.
- Owner: parent.

## 5. LOOP_STATE.md: parent appends the insertion text

**Status: PENDING. Parent to do.**

- Insertion text is prepared: LOOPSTATE-DRAFT/LOOPSTATE_DRAFT.md exists
  (drafted by the LOOPSTATE-DRAFT lane; LOOPSTATE-DRAFT/NAMECHECK.md records
  the toolchain guard and draft scope).
- The target is the repo-root LOOP_STATE.md. Its current tail is the
  wave-20261001-2021pdt COMPLETE section; no wave-20261001-2321pdt section has
  been appended yet. The parent appends the wave-20261001-2321pdt section
  (verdicts, debate outcomes, queued next) after the record is final.
- Owner: parent.

## 6. Archive tag: parent creates

**Status: PENDING. Parent to do.**

- Inventory is prepared: WAVE-ARCHIVE/WAVE_ARCHIVE_MANIFEST.md lists all 94
  lane directories, 46 JUDGE_BRIEF.md files, verdicts quoted from the lane
  sources, and the key commits per lane (branch tnn-native-lab, commits local
  only, never pushed).
- Tag convention from the previous archive tag:
  tnn-native-lab-wave-archive-wave-20261001-1121pdt. The parent creates
  tnn-native-lab-wave-archive-wave-20261001-2321pdt after the record is final.
- Owner: parent.

## 7. Wave lock: parent removes

**Status: PENDING. Parent to do.**

- The wave lock file ./.wave_lock exists at the repo root and contains the
  wave-start timestamp 2026-10-02T06:22:05Z (23:22 PDT, wave open). The parent
  removes it as the last step, after items 1 through 6 and item 8 are settled.
- Owner: parent.

## 8. URGENT: Decisions 4A/4B reach Micah BEFORE close

**Status: OPEN. Parent to escalate. Must not be skipped.**

- The flag is written: URGENT-FLAG/URGENT_FLAG.md. Decisions 4A (commit the
  minimal ~30-file / ~30 MB pinned set, tnn2.zag, freeze_shim2_bin, the pinned
  znc binary and provenance, into HEAD) and 4B (protective tar snapshot of
  the full untracked set with SHA-256 manifest alongside the bundle backups)
  need Micah's approval. Nothing has been done yet; nothing can safely be
  done yet.
- The parent must get Micah's decision on 4A and 4B BEFORE the wave closes.
  Once the wave closes and the working copy is recycled, the frozen bytes that
  underpin the 47 verdicts may be gone, and the final report's freeze claims
  would rest on hashes that no longer resolve to anything.
- Rule until decided: `git clean -fdx` is FORBIDDEN in this working copy.
- Owner: parent (escalate to Micah at the top of the final report).

## Close order (recommended)

1. Let SENSORY and RT-F2V3 verdicts land if they arrive before close (coordinator picks them up); otherwise record them as pending.
2. Complete the parent final report sections (b), (c), (e), with the URGENT
   Decisions 4A/4B at the top (parent).
3. Append the LOOP_STATE.md insertion text (parent).
4. Create the archive tag (parent).
5. Verify Decisions 4A/4B have reached Micah before close (parent). This is
   the blocking gate: do not close with this undecided and unflagged.
6. Remove the wave lock ./.wave_lock (parent).

Note for the next wave: OWNED-SYNTH, H5R2-SYNTH, and QUAL-SUMMARY syntheses
were still running as of 00:40 PDT (per DEBATE-READY/DEBATE_READINESS.md);
they can be folded into the record when they land.
