# RESUME RUNLOG — Wave-2 crossref re-verification (replacement re-verifier)

**Date:** 2026-09-24 (UTC)
**Re-verifier:** replacement coordinator (Wave-2 crossref resume)
**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, `docs/lab/crossref/PREREG_TIER2.md`

## Predecessor state (observed 2026-09-24 04:39–04:40 UTC)

- Predecessor runtime dead after daemon restart (system uptime 4 min, no
  verifier/build processes). Filesystem handle at
  `/home/hatch/agents/agent-a4a09a9a-9296-4344-9671-b482f8891a72` survived;
  last transcript write 2026-09-24 04:35:30 UTC.
- Nine staged preregs existed (mtime 2026-09-23 18:01:26 UTC). Contrary to
  the initial task premise, branch inspection showed all nine
  `REVERIFY_PREREG.md` files were already individually committed before the
  replacement coordinator's executions.
- At branch head `01df1f4775eaa6c2d276c262132b4894497a0105` (observed
  2026-09-24 04:41 UTC), all nine families had `reverify/VERIFY.md` and
  `RUNLOG.md`.
- Local staged files byte-identical to branch for AUDIOCONT, PROSEV3,
  RAWVSHUMAN, SENSESH2H. GOALB/INFORICH/JOKE local copies older than branch
  follow-ups. CERT/HELLHOLE had no staged local VERIFY/RUNLOG; complete
  branch versions fetched and inspected.

## Evidence inheritance vs independent recheck

**Independently rechecked by this re-verifier:**
- PROSEV3: Full RV2 executed (CHAL-P1 deviationectomy, CHAL-P3 analysis,
  QUOTE-FIX fork). All championship runs, scoring, and digests produced
  by this session. See commit `f7f9094196934ece6a4800737ac2bfd0caf5c833`.
- CERT: `evidence/cert/results.tsv` vs `work/CERT/results.tsv` byte-identical
  (36 lines), verified by direct comparison.
- RAWVSHUMAN: In-bin attribution re-derived from local jsonl
  (color 505/506=99.80%, pitch 131/132=99.24%); matches frozen figures.

**Inherited on trust (branch VERIFY.md inspected, not re-executed):**
- AUDIOCONT, GOALB, HELLHOLE, INFORICH, JOKE, SENSESH2H: branch VERIFY.md
  and RUNLOG.md fetched and read; figures not independently recomputed by
  this session. The predecessor's API-verified commit SHAs are cited in the
  final report.

## Prereg commit history (correction to task premise)

The task initially stated the nine preregs were "never committed." Branch
inspection proved otherwise: all nine `REVERIFY_PREREG.md` files were
committed individually before the replacement coordinator's executions.
Example: CERT prereg commit `5f067515…`, HELLHOLE prereg `8747608b…`.
(Exact SHAs for all nine retrieved separately for the final report.)

## Work completed by this session (2026-09-24)

### PROSEV3 RV2 — COMPLETE, committed as `f7f9094196934ece6a4800737ac2bfd0caf5c833`
- CHAL-P1 "deviationectomy": narrowed coreference trigger; sub-core 16/24
  (fixes exactly the 5 registered items); championship 4 sources × 5 reps,
  all byte-identical within source; scores unchanged (183/204/208/227).
- CHAL-P3 "wrong-value counterfactual": analysis from logs shows grok max
  185 < 189, sol max 204 (no gain); kill bar unreachable.
- QUOTE-FIX fork (additional principled repair): curly-quote recognition in
  tagger rule 2a + quote stripping in ent_finalize. Sol 204→215/228
  (3 reps byte-identical, sha256 `ac181523efd85802…`); others unchanged.
  2/4 FAIL stands. RV-CONFIRM.
- CHAL-P2 not executed (cannot affect RV-BROKE kill bar; documented as
  limitation in VERIFY.md).
- Pure-Zag external scorer (`verify3.zag`) built and used; binaries excluded
  from commit per rule.

### RAWVSHUMAN RV2 — NOT COMPLETED (documented limitation)
- Frozen RV1 figures independently re-derived and confirmed.
- RV2 (R1 fine-split, R2 hybrid, R3 oracle) requires raw fixture data
  (.img/.pcm files) not available locally and substantial Zag implementation
  of the transducer/binning system. Not executed. Flagged as limitation.

## Commits by this session
- `f7f9094196934ece6a4800737ac2bfd0caf5c833` — PROSEV3 RV2 (VERIFY.md,
  RUNLOG.md, learn3_devectomy.zag, learn3_quotefix.zag, verify3.zag,
  RV2_DIGESTS.md). 6 blobs, no binaries, no .zagd.

## Open items for final report
- Exact commit SHAs for all nine preregs, HELLHOLE, SENSESH2H, and
  PROSEV3/RAWVSHUMAN initial outputs (to be retrieved).
- SENSESH2H 184-vs-185 fixture-count discrepancy (to be investigated or
  disclosed).
- RAWVSHUMAN RV2 incomplete (disclosed above).
