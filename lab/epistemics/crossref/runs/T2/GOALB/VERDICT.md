# T2-GOALB VERDICT — Goal B random-words-to-story: bounded compositional machinery

## Verdict: REPRODUCED

Per the frozen decision rule (REPRODUCED if mechanical bars match AND B2's two-judge
FAIL re-derives with DEL 4/8 / POS 0/8; NOT REPRODUCED if any mechanical bar flips):
all four mechanical bars match on a fresh Type-A rebuild, and the two-judge B2 FAIL
re-derives exactly from the committed judge records with the DEL 4/8 / POS 0/8 counts.
No mechanical bar flipped.

## Pins (all verified by this crew)

- Prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f` — PREREG_TIER2.md pulled;
  T2-GOALB section extracted verbatim, matches dispatch text.
- Evidence commit: `5c1bf2a8babe2197160d5c092298bdb946d8bc67` — resolved via GitHub
  API ("Goal-B B2 second blind judge (grok-4.7): two-judge bar evaluated, NOT met —
  amended verdict", micahcooley 2026-09-22T14:14:49Z). All 32 evidence/source/corpus
  files fetched and SHA-1-verified against the commit tree.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` — used
  for the rebuild (native target).

## Claims vs measured (all 8 from the frozen T2-GOALB section)

| # | Frozen claim (commit `5c1bf2a8babe`) | This crew's measurement | Match |
|---|---|---|---|
| 1 | Class-based composer wrote good stories; blind judge passed 7/8 vs positional 0/8 (single-judge context) | Not re-measured (single-judge claim; B2 re-derived under two-judge) | n/a (context) |
| 2 | **B1 coverage 16/16** (POS 8/8, DEL 8/8) | Type A: rebuilt `story_all.zag` with pinned znc; 3 fresh-process runs byte-identical (sha256 `9dd1c20c…`), and byte-identical to committed `runs/rep1.log`. Independent verifier: **16/16** (POS 8/8, DEL 8/8) | **YES** |
| 3 | **B3 novelty 16/16** | Same runs; per-sentence (≥6 words) substring check vs committed corpora: **16/16** | **YES** |
| 4 | **B4 leakage PASS** (kb.txt hash identical; 0/16 substrings; no belief-write path) | kb.txt sha256 identical before/after (`3ef27296…`); 0/16 ≥16-byte story substrings in kb.txt; source audit: sole file open is `open(2)` with flags=0 (O_RDONLY); only read/close syscalls; all output via stdout | **YES** |
| 5 | **B5 determinism PASS** | 3 fresh-process reruns byte-identical (`cmp` clean); also byte-identical to committed rep1.log | **YES** |
| 6 | **Two-judge B2 bar FAILS both variants: DEL 4/8 at two-judge mean ≥3.5 (bar ≥6/8); POS 0/8** | Type C re-derivation with independent parser on committed `b2_raw_gpt-5_6-sol.txt` / `b2_raw_grok-4_7.txt` / `b2_item_key.txt`: **DEL 4/8** (S2 3.5, S4 4.0, S6 3.5, S8 4.0), **POS 0/8** (all 1.5) → bar FAILED both variants. Per-judge: sol DEL 6/8 / POS 0/8; grok DEL 0/8 / POS 0/8 | **YES** |
| 7 | Both judges ranked every deliberative/planner story above its positional counterpart; positive control 5/5 both judges (apparatus valid) | Every DEL story > its set-pair POS on both judges (8/8 pairs); control T17 = 5 sol / 5 grok; max inter-rater \|diff\| = 2 (none >2 flagged). Head-to-head means: sol DEL 4.00 vs POS 2.00; grok DEL 2.50 vs POS 1.00; combined DEL 3.25 vs POS 1.50 (gap 1.75) — all exact matches | **YES** |
| 8 | Binding claim downgraded arc-structured → beat-structured; honest caveat: grok-4.7 substituted for Amendment A1's grok-4.6 | Corroborated by the re-derived figures (one judge reads 6/8 DEL as arc-bearing, the other 0/8; perfect order agreement but ±1.5 calibration gap). The substitution is documented in the committed VERDICT.md §7.1 and its evidence-commit message; taken from the committed record, not re-verified at the API level (judge panels unrepeatable by design) | **YES** |

Controls: positive control 5/5 both judges (B2 apparatus valid) ✓; negative control
(deleted-word story must fail B1) — re-run against this crew's checker: flagged
'lighthouse' correctly, checker live ✓.

## Method fidelity notes

- The rebuild used the committed post-fix composer (`src/story_all.zag`, blob
  `69ee6052522c`). The original run-honesty note (13/16 first run, defect fixed) is
  part of the committed record; this crew's build reproduces the post-fix 16/16
  output byte-identically — no defect was reintroduced or needed re-fixing.
- Build needed the substrate import chain: `story_all.zag` → `R33_NATIVE_SHA256_V2.zag`
  (`5dd858fa1097…`) → `R33_NATIVE_IO_V1.zag` (`a6b440d2…`, canonical sibling in docs/lab
  trees at the evidence commit). The composer imports but does not use the sha256
  routines; determinism comes from the fixed templates and pure-Zag logic.
- No judges were re-run (frozen method: judge panels unrepeatable).

## Caveats

- **C1 — B3 corpus shape:** at the evidence commit, `prose-learning/v3/inputs3*` does
  not exist, so the committed `verify_goalb.py` glob matches nothing; the B3 corpus
  is exactly `docs/lab/dialogue/kb.txt` + `docs/lab/dialogue/battery.txt` (28,587
  bytes). Faithful to the committed verifier; if v3 files existed at trial time under
  another path, the committed verifier would miss them too.
- **C2 — leftover .git in clean/:** the workdir contained an unrelated leftover git
  checkout (HEAD at an audio-investigation commit, dirty). Left untouched; none of its
  objects were used. All inputs came via authenticated GitHub API with per-blob
  SHA-1 verification (full clean/ tree re-swept 32/32 clean at the end).
- **C3 — self-inflicted clobber:** running the committed `score_b2_combined.py` also
  rewrote `evidence/b2_combined.md` in clean/. Detected, restored the blob from the
  API, SHA-1 re-verified, then ran the full integrity sweep. No other file was touched.
- **C4 — grok-4.7 substitution:** the judge-#2 identity (grok-4.7 via ExperientialLabs
  in place of A1's grok-4.6 via UnoRouter) is a documented fact of the committed
  evidence, accepted here per the Type-C mandate; its API-level provenance was not
  (and per prereg cannot be) re-verified.

## Bottom line

T2-GOALB claims are intact: the mechanical compositional bars (B1/B3/B4/B5) reproduce
exactly on a clean rebuild with byte-identical outputs, and the two-judge B2 FAIL
re-derives with the same DEL 4/8 / POS 0/8 counts — arc-structured remains correctly
downgraded to beat-structured. **REPRODUCED.**
