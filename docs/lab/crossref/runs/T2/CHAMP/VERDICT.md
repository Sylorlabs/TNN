# T2-CHAMP — VERDICT: **REPRODUCED**

Wave 2 Tier 2 replacement replication crew, 2026-09-23. Type C committed-evidence
re-derivation of `docs/lab/crossref/PREREG_TIER2.md` § **T2-CHAMP — English championship
box (Type C)**, frozen at commit `7b2100d09911c5c10252c5756c7def288e70bd1f`.

Prereg rule: **REPRODUCED** if all class figures and the 0-split matrix re-derive;
PARTIAL if the 5-source class-2 acceptance question affects any figure (name it).

## Prereg claims vs independently measured (pure-Zag verifier, integer arithmetic)

| # | Prereg claim (verbatim §T2-CHAMP) | Measured | Disposition |
|---|---|---|---|
| 1 | Class 4 (direct) **0.9911**, 4-way tie (muse-native, sol, step, grok) | 12/12 reps at 0.9911 in **each** of muse-native, sol, step, grok — every rep recomputed from its own bind log + its own committed per-rep trap log | REPRODUCED |
| 2 | Class 3 (TNN teacher) **0.9921** won by swe (teacher revised all 12 planted falsehoods) | SWE raw log: revisions **12/12**, mastery **192/192**, §B.7 **96/96**, zero-gates blocked/tripwire/leak all 0, cost 0.9214 → composite **9921** (0.9921) | REPRODUCED |
| 3 | Class 2 (together) **0.9911** tied with best separate source | 5/5 teach reps at 0.9911, each with its own committed `btrap_N.txt` | REPRODUCED |
| 4 | Class 1 (together teacher) **0.9253** | Composite **9253** (mastery 0.9386 / revisability 0.8000 genuine-only / integrity 1.0000 / retention 1.0000 / cost 0.9371) | REPRODUCED |
| 5 | Curated pure-Muse **0.9911** tie, flagging **12/12** falsehoods, **0** false positives | 12/12 reps at 0.9911; 12 flags, 0 non-planted, all 12 planted IDs present (mask 4095) | REPRODUCED |
| 6 | Conflict matrix **1,140 rows, 0 splits** — all five corpora agreed on every fact value incl. the 12 planted lies | **1140** rows, **0** splits, all 12 planted IDs present; 5 reps × 228 rows | REPRODUCED |
| 7 | Together class-2 used **5 sources** (hy3 never recovered) → 6-source gate not met | 5 teach reps in evidence; no 6th source | REPRODUCED (acceptance is Micah's call; affects no figure → not PARTIAL) |
| 8 | Muse-bestof: faithfulness perfect; **12/12** falsehoods verbatim | 12/12 `"reproduce"` verbatim, id-mask 4095, all 240 items faithful | REPRODUCED |
| 9 | Muse-bestof class-4 composite **0.9911** with §B.7 **96/96** | 12/12 reps at 0.9911 (own per-rep trap logs); legB **96/96** | REPRODUCED |
| 10 | Muse-bestof class-3 §B.7 **96/96** with fresh-learner mastery **192/192** | legC **96/96**, adopted 160/240, mastery **192/192** | REPRODUCED |

**Every class figure and the zero-split matrix re-derived. Verdict: REPRODUCED.**

## How it was verified

- Independent Zag verifier `crew/verify_champ.zag` (693 lines, SHA-256
  `fedc7db5ddf668a4759e71b2eefaecd35216fa2d8d499f855f3a2736d429bf82`),
  compiled with the pinned toolchain
  `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
- Zero RNG. Three runs byte-identical:
  SHA-256 `e4b45499137d786224680d638b72bd542cb0e9b6dfbf0e9bedec58637c380e5c`
  (`cmp` clean across run1/run2/run3). Full output: `crew/run1.txt` (`ALL_CHECKS_PASS`).
- All evidence blob-SHA-verified against the frozen tree (133 files, 0 failures);
  corpus SHA-256 pins match committed SHA256SUMS (sol, grok, step, SWE, muse-native,
  curated `6fbfdb6…`, bestof `0177c7f0…`).
- Python used only as download glue; every verdict number computed in Zag.

## Frozen pins

- Prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f` (API-verified; tree `a88b8b9f3374be980628b8999b6c3ad0aabacb9a`)
- Prereg doc: `PREREG_TIER2.md` blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`
- Toolchain: `znc_linux_x86_64_abed8aa1`, SHA-256 `498abcb5…1357e58ef`
- Brief-expected pin `b9d7a6`: **unresolvable — transcription artifact.** 422 from
  `/commits/b9d7a6`, 0 commit-search hits, 0 of 1,513 frozen championship-tree object
  SHAs, 0 prereg-text occurrences, 0 hits in sylorlabs/zag. The coordinator's PIN AUDIT
  (`T2/_wave2_tally/VERDICTS.md`, 2026-09-23) already classified it (with 11 sibling
  brief pins) as a replacement-brief transcription artifact and instructed crews to
  use the prereg's own pins — which is what this replication did.

## Caveats

- No full `git clone` (HTTPS clone/fetch failed before handoff); evidence is
  API-fetched with per-blob SHA verification — content-identical to a clean checkout
  for all files used. `git fsck` on a full clone was therefore not possible.
- Class-1 paired with together rep-0 traps (single teacher run; no dedicated trap
  file in the frozen tree).
- Deliverables: `crew/VERDICT.md` (this file), `crew/RUNLOG.md`, `crew/run1.txt`,
  `crew/verify_champ.zag`.
