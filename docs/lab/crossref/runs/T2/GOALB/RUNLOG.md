# T2-GOALB RUNLOG — replication crew (replacement, fresh start)

Crew: T2-GOALB (replacement). No predecessor state used — all work below is this
session's. Predecessor crews were killed by runtime restarts before producing a
verdict; treated as a FRESH start per dispatch.

Workdir: ~/workspace/scratch-crossref/T2/GOALB/
  clean/  — pinned evidence files (read-only semantics; see integrity note below)
  crew/   — this RUNLOG.md, VERDICT.md, build/, runs/, frozen_inputs/

## Dispatch note (2026-09-22 ~23:16 PDT)

Task: replicate T2-GOALB (Goal B random-words-to-story, Type A for mechanical bars
B1/B3/B4/B5 + Type C re-derivation of the two-judge B2 figures). Rule: REPRODUCED
if mechanical bars match and B2's two-judge FAIL re-derives with DEL 4/8 / POS 0/8;
NOT REPRODUCED if any mechanical bar flips. Do not re-run judges.

## Step log

1. Created workdir; verified toolchain binary exists:
   ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (znc usage OK).
2. Pulled PREREG_TIER2.md from prereg commit
   7b2100d09911c5c10252c5756c7def288e70bd1f via gh-api; extracted the T2-GOALB
   section verbatim → crew/frozen_inputs/T2_GOALB_section.verbatim.txt (1177 bytes,
   matches dispatch text character-for-character).
3. Verified evidence commit 5c1bf2a8babe2197160d5c092298bdb946d8bc67 via API
   (message: "Goal-B B2 second blind judge (grok-4.7): two-judge bar evaluated,
   NOT met — amended verdict"; author micahcooley, 2026-09-22T14:14:49Z).
4. Saved full recursive tree of the evidence commit (/tmp/tree_full.json, 40,485 blobs).
   Located GOAL-B material at docs/lab/GOALB_STORY (35 hits incl. src/evidence/runs).
   Corpus paths at this commit: docs/lab/dialogue/kb.txt, docs/lab/dialogue/battery.txt;
   prose-learning/v3/inputs3* does NOT exist at this commit (caveat C1).
5. Read committed VERDICT.md, PREREG.md, PREREG_AMENDMENT_A1.md (saved to
   crew/frozen_inputs/; blob SHAs a180d0b63bbc, e96d138a8f80, 27567a164b30).
   Key bar definitions captured: B1 verbatim word match, ≥7/8 per variant; B2 two
   judges blind 1–5, mean ≥3.5 on ≥6/8 per variant; B3 no ≥6-word story sentence
   verbatim in corpora; B4 kb.txt hash identical + no ≥16B substring + no write path;
   B5 3 fresh-process byte-identical reruns; positive control ≥4.0 both judges;
   negative control deleted-word story must fail B1.
6. Pulled all GOALB_STORY files + the two dialogue corpus files via gh-api, each
   SHA-1-verified against the commit tree before writing (32 blobs).
7. Noticed leftover clean/.git from an unknown prior occupant (HEAD at 461722ad…,
   unrelated audio-investigation commit, dirty working tree with deleted .github
   scripts). Left it untouched; did NOT use its objects. All inputs came from the
   authenticated GitHub API with per-file SHA-1 verification (see integrity sweep).
8. Attempted git-archive extraction of the pinned subtree into clean/pinned (would
   have used the leftover .git objects as a cross-check) — killed it after ~6 min
   on a pressured VM; not needed given per-blob API verification.
9. Build: copied story_all.zag (blob 69ee6052522c) + R33_NATIVE_SHA256_V2.zag
   (5dd858fa1097…) into crew/build. First build failed: the substrate itself
   @imports R33_NATIVE_IO_V1.zag (cwd-relative import rule). Fetched the canonical
   sibling from docs/lab trees at this commit (a6b440d2…, verified). Rebuild OK:
   `story_bin` 145,338 bytes, native target.
10. Recorded kb_before.sha256 = 3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1.
11. Ran story_bin 3× as fresh processes (cwd = crew/runs with inputs/words.txt,
    inputs/classes.txt). All runs exit=0, 8353 bytes, empty stderr.
    sha256(rep1)=sha256(rep2)=sha256(rep3)=9dd1c20c25684a305887148dcd80768b8d208309aa1eb31fa070439e47870dd7.
    cmp against committed clean/runs/rep1.log: BYTE-IDENTICAL (same sha256).
12. Mechanical verification (original verify_goalb.py logic, paths repointed):
    trials=16; B1 16/16 (POS 8/8, DEL 8/8); B3 16/16 (corpus = 28,587 bytes,
    kb.txt+battery.txt; v3 glob hit 0 files at this commit); B4-substring 16/16 clean.
13. B4 file-hash: kb_after.sha256 = 3ef27296… identical to before. Source audit of
    story_all.zag: sole file open is syscall 2 with flags=0 (O_RDONLY); only read(0)
    and close(3) on it; no write-to-file path — all output via _zag_print/_zag_println
    (stdout). B4 PASS.
14. Negative control (A1): deleted "lighthouse" from S1-DEL story; B1 checker flagged
    exactly that word → checker live. PASS.
15. Type C B2 re-derivation with independent parser on committed evidence:
    17/17 items parsed both judges; key maps T01–T16 → S1–S8 × POS/DEL, T17 → CTRL.
    Results: sol DEL 6/8 ≥3.5, POS 0/8; grok DEL 0/8, POS 0/8; two-judge mean ≥3.5:
    DEL 4/8 (S2 3.5, S4 4.0, S6 3.5, S8 4.0), POS 0/8 (all 1.5) → bar ≥6/8 FAILED
    both variants. Every DEL story > its set-pair POS on both judges. Control 5/5
    both. Max |diff| = 2. Head-to-head: sol 4.00/2.00, grok 2.50/1.00,
    combined 3.25/1.50, gap 1.75. All figures match the committed claims exactly.
16. Ran committed src/score_b2_combined.py (paths repointed to clean/) — output
    numbers identical to committed evidence/b2_combined.md. INCIDENT: the script
    also rewrites its output file, clobbering clean/evidence/b2_combined.md. Detected
    and fixed: re-fetched the blob (7cc578f7935effcf5550378f9bd48937d40b761f) from
    the API, SHA-1-verified, wrote back. Full integrity sweep of all 32 files in
    clean/ vs manifest: 32/32 SHA-1 clean.
17. Prompt byte-identity: md5(clean/evidence/b2_prompt.txt) = 7e79199cadb2e08367376750445c7357,
    matching the claimed frozen-prompt hash.

## Artifacts

- crew/VERDICT.md (verdict + claim-by-claim table + pins + caveats)
- crew/build/story_all.zag, R33_NATIVE_SHA256_V2.zag, R33_NATIVE_IO_V1.zag, inputs/*
- crew/build/story_bin (native build, 145,338 bytes)
- crew/runs/rep1..3.log (+ .err), inputs/
- crew/kb_before.sha256, crew/kb_after.sha256
- crew/combined_rerun.py (repointed committed scorer)
- crew/frozen_inputs/{PREREG.md, PREREG_AMENDMENT_A1.md, VERDICT.md, tree_manifest.json,
  T2_GOALB_section.verbatim.txt, PREREG_TIER2.frozen.md}

No judges were re-run. No commits were made. TMPDIR honored (~/workspace/tmp_commit).
