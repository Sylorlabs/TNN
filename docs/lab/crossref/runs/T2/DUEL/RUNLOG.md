# T2-DUEL run log (2026-09-22 PDT)

Crew: T2-DUEL replication session (independent, depth-2 subagent).
Task: Type A full rerun of the sol-vs-grok duel battery.

## Pins frozen (before any run)

- prereg/scope: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- claim (expected `e18a2ca13589`): `e18a2ca135899be69c3e35497fb737124e50b78f` ✓ present
- build freeze B (expected `6c520a990a01`): `6c520a990a017499515b90003473166945cef0ba` ✓ present
- sealed battery C (expected `6978db0af55f`): `6978db0af55fcaf04e03fa2b55fc18ebfdd57ef5` ✓ present
- All pins resolved via GitHub API against sylorlabs/TNN. Nothing missing —
  no UNREPLICABLE-AS-IS trigger.

## Sequence

1. Attempted `git clone` of tnn-native-lab into `clean/`; the runtime killed
   the long-running fetch twice (SIGTERM at ~19 min; then session abort).
   Switched to pinned-SHA file fetches via `gh-api` — same bytes, same pins.
2. Fetched `docs/lab/crossref/SCOPE.md` (blob `dd4d3c67…`) and
   `PREREG_TIER2.md` (blob `b1178370…`) at the prereg commit; read the
   T2-DUEL section as the authoritative checklist.
3. Fetched from the claim commit: `VERDICT.md`, `src/sg_sol.zag`,
   `src/sg_grok.zag`, `evidence/build/BUILD_FREEZE.md`,
   `evidence/scored/scores.json`, `evidence/scored/{sol,grok}_run1.txt`,
   `gen/scored/{teach_sg.txt,probe_sg.txt,frames.tsv,expected_sg.json}`.
4. Verified source SHA256s against BUILD_FREEZE.md — exact match;
   `cmp`-verified claim-commit sources == build-freeze-commit sources.
5. Fetched the frozen front end at commit B: `sg_parse.zag`,
   `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`
   (sg_parse.zag lives at the duel dir root, not under `frozen/`).
6. Built both contenders with the pinned znc
   (`znc_linux_x86_64_abed8aa1`, md5 `0645ba22e9e61041be17e46eac81e8a0`):
   sg_sol = 186630 bytes, sg_grok = 186770 bytes — exactly the sizes in
   BUILD_FREEZE.md. (Analyzer warnings only; TMPDIR set to
   ~/workspace/tmp_commit; no /tmp use; no binaries/.zagd committed.)
7. Ran the sealed scored battery 5× per contender. All 5 byte-identical per
   contender; stdout/proof SHA256s exactly the committed VERDICT.md §2
   digests. stderr empty on all 10 runs.
8. `cmp`: my run1 outputs byte-identical to committed
   `evidence/scored/{sol,grok}_run1.txt`.
9. Wrote an independent scorer in pure Zag (`run/build/score_duel.zag`,
   zero RNG): JSON + run-file parsing, PREREG-SG §4 correctness rules, §5
   decision rules with exact rational arithmetic, post-hoc hybrid per the
   frozen definition. Two scorer bugs were found and fixed during
   development (an arena-layout overlap in the id-intern table, and a
   bump-pointer/string-region overlap) — both caught by the scorer's own
   join-count diagnostics, neither touching the committed evidence.
10. Scorer output: all per-slice cells, all six metrics per contender, and
    the hybrid table exactly match `scores.json` and VERDICT.md; wrong-value
    decomposition 32+24+24+20+4=104 matches §5; decision rules applied
    mechanically → SCENARIO-FIT. NOT-REPRODUCED triggers did not fire
    (grok WRONG 0.2407 stays above the 0.05 gate; sol WRONG stays 0).

## Environment notes

- Scratch tree: `~/workspace/scratch-crossref/T2/DUEL/` (crew/ + run/).
  No other workstream's files touched; no live processes touched.
- `clean/` clone was abandoned (runtime kills); API-pinned fetches used
  instead — documented deviation, pins unchanged.
- The `clean/` directory still holds a partial `.git` from the killed
  clone; harmless scratch.

## Artifacts

- `VERDICT.md` (this dir) — the replication verdict.
- `RUNLOG.md` (this dir) — this log.
- `run/build/sg_sol`, `run/build/sg_grok` — rebuilt binaries (scratch only).
- `run/build/score_duel.zag` + `run/build/score_duel` — independent Zag scorer.
- `run/{sol,grok}_run{1..5}.txt`, `run/proof_{sol,grok}_run{1..5}.txt` — run outputs.
- `run/score_report.txt` — full scorer report.
- `corpus/` — pinned sealed battery + committed reference outputs.
- `src/` — frozen contender + front-end sources (byte-identical to pins).
