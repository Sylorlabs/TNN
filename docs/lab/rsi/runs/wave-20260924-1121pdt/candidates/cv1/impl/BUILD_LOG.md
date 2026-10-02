# BUILD LOG: CLAIM-VERIFY-1 (wave-20260924-1121pdt)

Date: 2026-09-24. Branch: tnn-native-lab. HEAD 68c3bb8683ab091762069efbe834293efeff2a10.
All work under docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/cv1/impl/.
No commit, no push. Pure Zag plus shell coreutils. No Python anywhere.

## Frozen inputs (verified 2026-09-24)

- KB docs/lab/dialogue/kb.txt, 38 facts, sha256
  3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1
  (matches prereg and docs/lab/dialogue/SHA256SUMS).
- Toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- Frozen decline source extracted from archive branch
  tnn-native-lab-wave-archive-20260923-2321pdt:docs/lab/rsi/runs/wave-20260923-1121pdt/tnn_chat_decline.zag
  (sha256 begins a87011fe10dbc5ba, 2300 lines). Rebuilt frozen binary: 296338 bytes.
- Frozen F4 fixtures from the archive branch (identical to the 0521 scratch mirror):
  - fixtures/kb1_out30.txt sha256 936c35e11706e98f08ea0dbe0b33f2c6d93c1a301c7a3e003f850e5f610b8188
  - fixtures/kb2_inkb.txt sha256 730e2d246926bbd91909da1799b7327c9cba586085dbfa79e2407bcc39883184
- Sealed directory candidates/cv1/probes_sealed/ was never opened, read, or listed.

## Artifacts built

Build command (pinned toolchain, -o, binary run directly):

  ~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 <src>.zag \
    --no-zagd --no-analyze --no-foreground-cache -o <bin>

1. tnn_chat_decline_frozen_ref.zag: byte copy of the frozen decline source,
   archived locally in impl/ (imports R33_NATIVE_SHA256_V2.zag and
   R33_NATIVE_IO_V1.zag copied alongside). Built to tnn_chat_decline_frozen_ref.
   Baseline reproduction: 3/3 runs byte-identical on both fixtures;
   KB1 sha256 a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308,
   KB2 sha256 e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264.
2. cv1_section.zag: the CLAIM-VERIFY-1 deliberation section (canonicalizer F7,
   content-word coverage, single-fact lowest-index selection, frozen-template
   specific decline, F8 atomic-claim substring check, pure-Zag op counter).
3. cv1.zag: frozen reference head (lines 1-1999) + cv1_section.zag +
   frozen main (line 2176 on), with surgical edits only: do_turn gains the
   candidate buffers and op counter, path 5 calls deliberate_cv1 instead of
   deliberate, the pass branch emits the selected fact id via the unchanged
   emit_fact path, main precomputes canonical KB tables once and prints
   per-turn op counts to stderr. Built to cv1 (335007 bytes main).
   One comment fix after first build (F7 count 48 to 54, comment only);
   rebuilt binary verified behavior-identical to the first build.
4. gate_op.zag: measurement instrument for CV-B4. Copy of the frozen source
   with a pure-Zag decision-op counter threaded through deliberate() and its
   helpers (kb_word_known, ent_word_ids, kb_rel_covers, cite_words, raw_cite);
   counting discipline: one op per token/id comparison loop iteration, byte
   moves and formatting not counted. Verified stdout byte-identical to the
   frozen baseline on both fixtures (gate_kb1.txt == base_kb1_r1.txt,
   gate_kb2.txt == base_kb2_r1.txt). Built to gate_op.
5. collapse_check.zag: confound-4 machine check (F7 canonicalization of all
   38 facts, pairwise content-word set comparison). Built to collapse_check.
   Result: 38 facts read, 0 duplicate content-word set pairs, COLLAPSE-CHECK-PASS.

## Test runs (all in impl/runs/, CWD=runs/ so kb.txt and gaz.txt resolve)

- base_kb1_r{1,2,3}.txt / base_kb2_r{1,2,3}.txt: frozen baseline transcripts.
- cand_kb1_r{1,2,3}.txt / cand_kb2_r{1,2,3}.txt: candidate transcripts (r1 with
  .ops per-turn op counts; r2/r3 likewise for determinism).
- gate_kb1.txt / gate_kb2.txt (+ .ops): instrumented baseline transcripts.
- selfprobe*.txt / selfprobe2*.txt / sp3.txt: confound self-probes (novel
  probes only, never sealed content).
- per_probe_kb1.md: per-probe outcome report for the 30 training probes.
