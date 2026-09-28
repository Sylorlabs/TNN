# F2-WITHHOLD — build notes

Date: 2026-09-23.

## Toolchain

Pinned lab znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

Build (from `dialogue/round2_repair/f2_withhold/`):

```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 dialogue.zag -o dialogue_bin_f2
```

Build warnings only (4 analyzer warnings, pre-existing A0102 style, same as
canonical build). No errors.

## Binaries

| binary | sha256 | notes |
|--------|--------|-------|
| `dialogue_bin_base` | `912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5` | unmodified fork source; byte-identical to canonical `dialogue/dialogue_bin` — toolchain reproduction verified |
| `dialogue_bin_f2` | `1bea39bae723b4c1bd273592824fe32eac45c61cd91c392882573b50253dcde5` | fork + withhold gate (binaries excluded from repo per standing rule; rebuild with the command above) |

The binary reads `kb.txt`, `gaz.txt`, `battery.txt` relative to CWD (unchanged).

## Source changes (fork `dialogue.zag` vs canonical, +272 diff lines)

All changes are in one place: a new section `F2-WITHHOLD repair` inserted
before `do_turn`, plus a hook in `do_turn` step 5 and one new buffer
(`fout`, 512B) threaded through `do_turn`. Nothing else in the 1917-line
file was touched — correction (step 1), topic resume (step 2), composition
(step 3), and assertion handling (step 4) are byte-identical logic.

New functions (all pure, zero RNG):

- `vocab_find` — vocab id lookup without interning (mirrors `v_intern`'s
  entry layout, never inserts).
- `vid_eq`, `is_relkey`, `is_whkey`, `key_in_fact` — small predicates.
  `is_relkey` is the KB's own stemmed relation vocabulary
  (wrote/written/bear/build/publish/discover/win/capital/tall/long/open/
  dedicate/complete/landmark) — it scales with the KB, it is not a probe list.
- `is_specific` — "?" present or wh-word/demand-verb start.
- `focus_keys` — tokenizes a query region into content vocab ids with the
  exact proc_token pipeline (stopwords, digits, stemmer, irregular norms),
  never interning; optional cut at the first relation word.
- `find_last_of` — last standalone " of " in the resolved query.
- `withhold_check` — the gate. Returns 1 = decline, 0 = emit.

Gate (any firing check → decline), evaluated on the best fact AFTER
`retrieve()`:

- **G1 entity-aboutness:** query entities (gazetteer scan ∪ pronoun-bound)
  non-empty and disjoint from the fact's entity list → decline.
- **G2 relation-demand:** a query relation word missing from the fact's
  keys → decline.
- **G3 demand-focus:** structural focus — noun phrase after last " of ",
  object of "who wrote|discovered|is|was", subject of
  "when was|when did|was … <relation>", subject of "how tall|long is" —
  shares no content key with the fact → decline.
- **G4 orphan-aboutness:** no demand-focus identified, no query entity, a
  specific question, and some non-wh content key uncovered by the fact →
  decline. Skipped when G3's focus was identified AND covered: then a stray
  unmatched token is a typo/variant of the asked-about entity (this is what
  keeps round-1 WEIRD typo probes like "Herman Melvile" working).
- **G5 score floor:** no query entity, specific question, Jaccard < 1/4
  (inter×4 < union) → decline. Backstop for degenerate queries.

Decline path: emits exactly `I don't know.`; updates salience/topic/pv
state exactly as an emitted fact but with fid = -1 (no fact entities
pushed), so follow-up anaphora and corrections keep working.

## Iteration log

1. First build: 8/8 scaffold probes declined, but WE-07
   ("When was Herman Melvile born?") regressed — the typo'd surname was an
   orphan under G4. Fixed by the focus-covered exemption above (general
   principle, not a per-case branch): after the fix, full battery byte-
   identical to baseline, scaffold still 8/8.
2. No scaffold-only artifacts were ever introduced (no per-probe branches,
   no probe literals — verified by grep); nothing needed removal at release.

## Files in this directory

- `PREREG_F2.md` — frozen prereg (committed b1b6092d793c150cb02e3285b1e67d093b90ff57 before implementation)
- `dialogue.zag` — repaired fork
- `kb.txt`, `gaz.txt` — byte-identical copies of canonical
- `battery.txt` — round-1 battery copy (regression runs)
- `scaffold_probes.txt` — 8 development probes (S1–S8)
- `heldout_probes.txt` — 7 frozen held-out probes (H1–H7)
- `nogaming_probes.txt` — 20 answerable + 5 good-turn probes
- `conv_battery.txt` — round-2 conversation copy (B1 replay)
- `run_*.log` — run logs (base, scaffold, full, r2, nogaming, heldout, det1, det2)
- `dialogue_bin_base`, `dialogue_bin_f2` — built binaries
- `HELDOUT.md`, `VERDICT.md` — this report's companions
