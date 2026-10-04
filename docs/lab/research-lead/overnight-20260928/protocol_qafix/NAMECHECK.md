# NAMECHECK: Protocol QA Fixer

## Step 0: Toolchain guard

- Safebin configured per the mandatory guard script:
  `mkdir -p $HOME/safebin`, symlinked `git znc sh bash ls cp mv rm
  mkdir cat grep sed awk wc cmp sha256sum` (git-receive-pack,
  git-upload-pack, git-upload-pack not needed for this task),
  `export PATH="$HOME/safebin"`.
- `which python3 python` returns nothing (empty output, verified in
  the exec shell before any other work).
- Zero forbidden executables invoked. This task required no
  computation: read-only document inspection (muse.read, grep, sed)
  plus four text edits (muse.edit) to the DRAFT protocol.

## Scope

DRAFT FIX ONLY. The lifetime protocol v2 is DRAFT-NOT-FROZEN; it was
updated in place and is still not frozen. No frozen artifact was
touched. No sealed worlds opened or created. Nothing pushed.

## Input provenance

- Protocol QA report: `protocol_qa/PROTOCOL_QA.md`, report a125a1984
  (issues QA-1, QA-2, QA-3; 3 minor, 0 blocking).
- P4 profile definition: `tnn2_transfer/TRANSFER_ANALYSIS.md` P4
  result (lines 114-141). Note: the QA report traced "P4 profile" to
  `q4_baseline/PREREG_Q4BASELINE.md`, but the P4 used by the protocol
  ("corruption-first, then fossilization, then catastrophic answer
  loss") is the transfer-analysis P4, not the q4-baseline prediction
  P4 (a different P4 about MEM-COMP). The fix cites the correct
  source.
- H1 / H1 widening definition: `tnn3_roadmap/TNN3_ROADMAP.md`
  section 2 ("How H1, H2, and H3 relate").

## Fix log

1. QA-1 (Section 0 changelog item 7): replaced the stale four-state
   list "live, retired (future), deleted, fossil (accidental)" with
   the Section 7.7 taxonomy "live, deleted, fossil (accidental),
   zombie (corrupted)". Added the explicit note that retirement does
   not exist in frozen TNN-2 and would be a fifth end-state only if a
   future build implements it.
2. QA-2 (Section 11, K-LT-2): added an in-document definition of the
   P4 profile (executable structures die first, MAPs fossilize,
   learned answers catastrophically forgotten) with an explicit
   source citation to `tnn2_transfer/TRANSFER_ANALYSIS.md` P4 result.
3. QA-3 (Section 17): added an in-document definition of H1 (the
   hypothesis that each mechanism's output space is enumerated in
   source) and "H1 widening" (opening the constructor beyond the
   enumerated space), with an explicit source citation to
   `tnn3_roadmap/TNN3_ROADMAP.md` section 2.
4. Added Section 0 changelog item 11 recording the three QA
   corrections, following the document's existing pattern of logging
   each update.

## Verification

- Title line still reads "DRAFT-NOT-FROZEN" (no freeze language
  added or removed).
- Zero em-dash (U+2014) and zero en-dash (U+2013) bytes in the
  edited file, verified with grep on the UTF-8 byte sequences.
- All three fix sites located by grep; changelog item 11 present.
- Line count 1206 -> 1225 (four edits: item 7 rewrite, K-LT-2
  insertion, Section 17 insertion, item 11 addition).

## Constraints honored

- DRAFT UPDATE ONLY. No freeze. Paper
  (`TNN_RESEARCH_PAPER_20260929.md`) untouched. Frozen artifacts
  untouched. No sealed worlds. Nothing pushed.
- Zero em dashes in this NAMECHECK (byte-check at commit time).

## Standing metrics

All zero (documentation fix only; no cognition, no mechanisms).
