# T2-JOKE — VERDICT (replication crew, replacement)

**Verdict: REPRODUCED** — the frozen PARTIAL claim reproduces in full: every bar
figure matches, the solo-arm K1 kill-bar trip reproduces, and the glue-on-pizza
solo/helper split reproduces. No bar flips.

## Frozen prereg section (authoritative)

Source: `sylorlabs/TNN`, branch `tnn-native-lab`, commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`,
`docs/lab/crossref/PREREG_TIER2.md` (T2-JOKE section, quoted verbatim):

> ## T2-JOKE — web joke/lie/satire: PARTIAL (Type A)
>
> **Claims:** prereg `8f33adac` frozen pre-run; evidence `d7e59016` (branch head, API-verified): 30 real web items (6 satire / 6 deadpan jokes / 6 hoaxes / 6 sincere-weird truths / 6 sincere false beliefs), solo + helper arms, pure Zag, 5 runs/arm byte-identical. Bars: joke catch solo 0.17 (KILL BAR TRIPPED, arm-specific) / helper 0.67; satire 1.00/1.00 (via URL provenance, not prose — honest limitation); hoax handled 0.83/0.50; non-sincere installed solo 0.03 (1 item: tree-octopus) / helper 0.10 (glue pizza, Apple Wave, Damascus — at pass boundary). Glue-on-pizza: SOLO JOKING/withheld; HELPER SINCERE/INSTALLED. Controls: no sincere person called deceptive; no sincere truth misflagged; sincere-false called deceptive 0.00/0.00. Qualifications: intent reader is crew-built test-side English marker machinery; "installed" = ledger disposition, not live belief write.
> **Method:** full rerun from committed items + marker machinery in clean checkout; 5 runs/arm byte-identical.
> **Rule:** REPRODUCED if every bar figure matches including the solo kill-bar trip and the glue-on-pizza solo/helper split; NOT REPRODUCED if any bar flips.

## Frozen pins (API-verified before running)

| Pin | SHA | Status |
|---|---|---|
| Cross-ref prereg doc | `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch `tnn-native-lab`) | present, section extracted |
| Trial freeze (pre-run) | `8f33adac1a43249d4d5f2cebdc1cf4a24e3fed0d` | present — "WEB JOKE/LIE/SATIRE TRIAL — frozen prereg commit (pre-run)" |
| Trial evidence (post-run) | `d7e59016792c1596d1f4fb27a9c213221c18e0c5` | present — "WEB JOKE/LIE/SATIRE TRIAL — evidence + results (post-run)" |

No pin missing → no STOP. Build sources (12 `.zag` files) verified byte-identical
(sha256) to the freeze commit `8f33adac` before and after the run.

## What was run (Type A)

- Clean checkout of the trial tree `docs/lab/senses/web-search/joke-lie-trial/`
  at freeze `8f33adac`; rebuilt `j_trial.zag` from source with the pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, znc
  2026.07.0-dev). One binary, `argv[1]` selects arm (solo default / helper).
- 5 runs solo + 5 runs helper, all in scratch (`crew/runs/`). Zero RNG anywhere
  (trial is pure Zag by construction). No `.zagd`/binary copies of the original;
  nothing committed.
- Independent verification in pure Zag (`crew/build/v_verify.zag`, written by
  this crew): reads each run file from disk, recomputes every measure, checks the
  kill-bar inequalities, the glue-on-pizza split, the named installed-item set,
  M7 reason honesty (mirroring frozen `score.py` semantics exactly: skip
  "conflict"/"none"; `R_SATIRE_SOURCE` markers may cite the URL; all other
  markers must occur in the folded item text), recomputes the full hash chain
  entry-by-entry, and checks HEAD == last ledger hash. Exit 0 on all 10 runs.

## Results — every bar vs frozen claim

Intents: 1=SINCERE 2=JOKING 3=SATIRE 4=DECEPTIVE 5=UNCERTAIN; install: 1=INSTALL 2=WITHHOLD.

| Bar | Frozen claim | Rerun (solo) | Rerun (helper) | Match |
|---|---|---|---|---|
| Joke catch M1 | 0.17 / 0.67 | 1/6 = 0.1667 | 4/6 = 0.6667 | yes |
| K1 (<0.50 → FAIL, arm-specific) | TRIPPED in solo | tripped (1/6) | not tripped (4/6) | yes |
| Satire catch M2 | 1.00 / 1.00 | 6/6 | 6/6 | yes |
| Hoax handled M3 | 0.83 / 0.50 | 5/6 | 3/6 | yes |
| Sincere-false called deceptive M3b | 0.00 / 0.00 | 0/6 | 0/6 | yes |
| Sincere-truth misflagged M4 | 0.00 / 0.00 | 0/6 | 0/6 | yes |
| Non-sincere installed | 0.03 (1: tree-octopus) / 0.10 (3: glue pizza, Apple Wave, Damascus — at pass boundary) | 1/30 = 0.033 (c3 only) | 3/30 = 0.10 (b1, c1, c5 only) | yes |
| K3 (≥0.25 → FAIL) | not tripped | 1/30 < 0.25 | 3/30 = 0.10 ≤ 0.10, at pass boundary | yes |
| Glue-on-pizza (b1) | SOLO JOKING/withheld; HELPER SINCERE/INSTALLED | intent 2, install 2 | intent 1, install 1 | yes |
| Reason honesty M7 | 1.00 / 1.00 | 30/30 | 30/30 | yes |
| Ledger entries | 32 / 62, chain verifies | 32, chain recomputed OK | 62, chain recomputed OK | yes |
| Determinism | 5 runs/arm byte-identical | sha256 `14aa6774…` ×5 | sha256 `3cfd88c0…` ×5 | yes |
| Rerun vs frozen evidence | — | byte-identical to `d7e59016` runs | byte-identical to `d7e59016` runs | yes |

Corpus: 30 items, 6 per category (a/b/c/d/e), confirmed from the frozen
`fixtures/corpus.json`. Installed-item titles confirmed: c3 "Save The Pacific
Northwest Tree Octopus"; b1 "Woman Takes Google's AI Advice, Adds Glue To Keep
The Cheese From Slidin…"; c1 "No Matter What This Ad Says, Do Not Microwave
Your Phone" (Apple Wave hoax); c5 "Rachel's Team Pick: A Gay Girl In Damascus".

Per-item intents reproduce the frozen confusion matrices cell-for-cell
(e.g. solo: (b) = 1 JOKING + 5 UNCERTAIN; (c) = 1 SINCERE + 5 UNCERTAIN;
helper: (b) = 1 SINCERE + 4 JOKING + 1 DECEPTIVE; (c) = 2 SINCERE + 1 JOKING +
3 DECEPTIVE).

## Decision

Per the frozen rule — REPRODUCED iff every bar figure matches including the
solo kill-bar trip and the glue-on-pizza solo/helper split — the verdict is
**REPRODUCED**. The frozen PARTIAL standing (solo K1 kill trip, arm-specific;
helper improves jokes 0.17→0.67 but degrades hoaxes 0.83→0.50 and installs 3
non-sincere items) is confirmed exactly as stated, with the honest limitations
(satire via URL provenance; intent reader is crew-built test-side machinery;
"installed" = ledger disposition) intact.

## Notes / anomalies

- Predecessor crew left only a bare `git init` + remote in `clean/` (no objects);
  full re-clone was required. The full `git clone` of `sylorlabs/TNN` times out
  on this VM (repo too large); a partial clone (`--filter=blob:none`) fetching
  only the two frozen pins + sparse checkout of the trial tree was used instead.
- Mid-run, the entire `clean/` checkout (`.git` + working tree) vanished for an
  unknown reason; `crew/` (runs, build, logs) was untouched. Repo was re-fetched,
  pins re-verified, sources re-verified byte-identical, and the frozen evidence
  re-extracted. Cause unknown; flagged for the parent.
- Two transient runtime hiccups ("failed to store metadata for session",
  one service restart) did not affect files or results.
- Nothing was committed; no live workstreams touched. Binaries live only in
  `crew/build/` (scratch).
