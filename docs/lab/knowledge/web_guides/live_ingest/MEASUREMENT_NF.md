# Measurement report — LI novel-facts fixture test ("couldn't find one new thing")

**Frozen prereg:** `PREREG_LI_NF.md` (committed 05e7552791aaad71083eb33f74b379957ab41053
BEFORE any fixture was generated or any run executed). All predictions below
are from that prereg's §5.

## Frozen stack (untouched)

| artifact | identity |
|---|---|
| instrument source | `knowledge/web_guides/webg.zag`, md5 `c1ea3e71a93205dd6facf61667c3f442` |
| instrument binary | `knowledge/web_guides/webg`, byte-identical to pinned-toolchain rebuild (proven: `cmp` clean) |
| toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| guides | `guides/g1_query.txt` … `g7_bad.txt` (frozen) |
| driver | branch `run_li.py` at HEAD, SHA-256 `b810d461c83c681127fe4a052ebddfe38db4b7f6a8960b74a63db395e677bdda` (verified against branch blob `29cad598…`) |

## Runs

Two full passes over `fixtures_novel/` (60 clusters × 2 pages, manifest
`manifest_fixtures.txt`, authored snapshots with `manifest_fetch_status.txt`
+ `snapshot_fidelity.txt`, all VERIFIED):

- pass1 DONE: `clusters=60|installed=28|withheld=32|`
  `sha_log=81f408822c7268cced42f4200df1e627016066f4e2fb9d249d6c7b24420876eb|`
  `sha_knowledge=a5988c819f7eae8e283cfb78a935b174c02f8268480108ec50942376716271cf|`
  `sha_refusal=7c733cabe3bf4c7442dd89a20f0042136fc8d6f3827bbe2373d39360564b7909`
- pass2 DONE: identical line.
- `cmp` clean on `knowledge_ledger.txt`, `refusal_ledger.txt`, `run_li.log`;
  `diff -rq` clean on the full run trees. **Determinism holds (P6).**

## Headline: did it find one new thing?

Novel INSTALL-worthy facts installed: **20 / 44** (Type A 20/20, Type B 0/24).

The "one new thing" sub-metric — realistic paraphrase coverage (Type B):
**0 / 24 installed.** Every one of the 24 genuinely-novel, true,
two-independent-source facts asserted in normal paraphrased prose was
withheld with gate NO_CORROBORATION. Micah's test answers: the frozen
instrument could not find one new thing in realistic coverage; the fixtures
are needed.

## Prereg predictions vs outcomes

| pred | claim | outcome |
|---|---|---|
| P1 | Type A installs 20/20 (byte-identical positive controls) | **HOLD** — 20/20 installed, each with 2 provenance pages |
| P2 | Type B installs 0/24, all NO_CORROBORATION | **HOLD** — 0/24, 24 × NO_CORROBORATION |
| P3 | C1–C4 (single-source true) withheld, NO_CORROBORATION | **HOLD** — 4/4 |
| P4 | C5–C8 install the false claim (same-host sockpuppet hole, BUGFIX-1 A2); C9–C12 install the false claim (A9 residual) — preregistered expected-installs | **HOLD** — 8/8 installed the false claims (disclosed frozen-instrument integrity failures, not fixture defects) |
| P5 | C13–C16 withheld with FLAG\|INJECTION on both pages | **HOLD** — 8/8 pages flagged, all 4 withheld NO_CORROBORATION |
| P6 | two passes byte-identical | **HOLD** — cmp + diff -rq clean |

Ground-truth agreement: 28 OK (20 A installs + 8 C withholds) + 8
EXPECTED-HOLE (C5–C12) = 36/60; the 24 Type-B "mismatches" are the measured
throughput gap itself (ground truth INSTALL-worthy, outcome WITHHOLD) —
that gap is the finding, not a defect.

Per-fact gate traces: `gate_traces.md` (60 rows: cluster, type, ground
truth, outcome, gate, assessment, installed claim). Raw per-cluster
`verdict.out` files are in `run_nf_pass1/work/<cid>/`.

## Novelty proof (absence_proof)

- `knowledge_ledger_full.txt` (LI-1 scale-up): empty, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` —
  absence trivial.
- 24 distinctive probes (beacon mint tokens NF20260923-*, "fixture beacon",
  "beacon ledger", "PREREG_LI_NF", "8640", "Guaylupo", "Contender Series",
  "Bayern Munich Women", "Vanuatu Women", "HB Koege", "Starlink V3",
  all 8 false-claim key phrases, "third gravity assist", "suborbital
  trajectories", "unanimous decision", "novel-facts fixture",
  "ground-truth verdicts", "distractor sentences") grepped case-insensitively
  over all 19 `corpus_snap/` files and all 194 `corpus_snap_full/` files:
  **zero hits**. Beacon tokens were minted at fixture-build time
  (2026-09-23), after every corpus snapshot; real-world facts were verified
  by web search 2026-09-23 and are absent from the corpus.

## Interpretation

The instrument installs novel facts exactly when — and only when — the same
sentence appears word-for-word on ≥2 pages (G4). Type A (20/20) proves the
install path works; Type B (0/24) proves realistic independent coverage
never clears the bar. The throughput bug is confirmed as a property of the
frozen G4 rule, not of the corpus: even with guaranteed-novel,
guaranteed-true, two-source facts, paraphrase defeats corroboration. The
C5–C12 installs re-confirm the known integrity holes (same-host sockpuppet
= BUGFIX-1; distinct-host collusion = A9 residual) on the frozen instrument.

Wave-2 forks (training-mode / unified-mode / paraphrase-tolerant variants)
must beat this baseline: ≥ the 20 Type-A installs, plus Type-B installs,
with zero installs on C1–C16.
