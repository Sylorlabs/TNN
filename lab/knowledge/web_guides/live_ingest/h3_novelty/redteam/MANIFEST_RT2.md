# MANIFEST — H3-RT2 attack corpora (frozen with fixtures)

16 corpora × 3 pages = 48 pages, built deterministically by
`tools/build_corpora.py` (hand-authored literals, zero RNG) on 2026-09-23.
Page format: `TITLE:` line, `FRAMING:` lines (excluded from checkable
sentences per mini-prereg A1), one factual sentence per line. L3 pages 1–2
are single-line `FETCH-FAILED:` pages (A8).

## Nonce tokens (fixed)

`VEXMOR`, `QLYTH-9`, `BRUNDIC-ALPHA` — SC1 verified zero occurrences in
G1–G6. Inventory per corpus verified by SC2 (see `tools/selfcheck.py`).

## Fixture truth table

| Corpus | Family | Semantic truth | Expected §2-literal verdict |
|---|---|---|---|
| F1_translation | fake-2.0 | EMPTY (Spanish translations of P1/P2/P3) | NOVEL, 3 installs |
| F2_negation | fake-2.0 | EMPTY (double-negation identities of P10/P4) | NOVEL, 2 installs |
| F3_split | fake-2.0 | EMPTY (halves compose to P1/P2) | NOVEL, 4 installs |
| F4a_known | fake-2.0 | EMPTY (verbatim P1/P2/P4) | EMPTY |
| F4b_smuggle | fake-2.0 | EMPTY (P1/P2 templates, VEXMOR/QLYTH-9 substituted) | NOVEL, 2 installs |
| F5_normgap | fake-2.0 | EMPTY (verbatim P1+U+200B, P7+U+200D) | NOVEL, 2 installs (letter-of-spec) |
| H1_embed | hidden-2.0 | NOVEL (1 fact, substring-embedded, VEXMOR) | NOVEL, exactly 1 install |
| H2_launder | hidden-2.0 | NOVEL (2 facts, K-vocabulary only, no nonce) | NOVEL, exactly 2 installs |
| H3_neardupe | hidden-2.0 | NOVEL (1 fact, phrase-swap on P7, VEXMOR) | NOVEL, exactly 1 install |
| H4_volume | hidden-2.0 | NOVEL (1 fact BRUNDIC-ALPHA among 12 known) | NOVEL, exactly 1 install |
| L1a_drip | launder-2.0 | WITHHELD (1 fact, p1 only, VEXMOR) | WITHHELD, SINGLE_SOURCE |
| L1b_drip | launder-2.0 | WITHHELD (1 fact, p2 only, QLYTH-9) | WITHHELD, SINGLE_SOURCE |
| L1c_drip | launder-2.0 | WITHHELD (1 fact, p3 only, BRUNDIC-ALPHA) | WITHHELD, SINGLE_SOURCE |
| L2a_xbound | launder-2.0 | WITHHELD (VEXMOR fact, p3 only here) | WITHHELD, SINGLE_SOURCE |
| L2b_xbound | launder-2.0 | WITHHELD (same VEXMOR fact, p1 only here) | WITHHELD, SINGLE_SOURCE |
| L3_partial | launder-2.0 | WITHHELD (QLYTH-9 fact on surviving p3) | WITHHELD, SINGLE_SOURCE, not INFRA-FAIL |

P1–P12 are the 12 script-verified standalone installed-guide sentences
(listed in `tools/build_corpora.py`; verification: all `norm(Pn) ∈ K`).

Known-sentence inventory per corpus (script-verified by SC5 where load-bearing):
- F4a: P1, P2, P4 (all known → EMPTY)
- H1: P1, P3 known + 1 novel; H2: P1 known + 2 novel; H3: P7 known + 1 novel;
  H4: P1–P12 known + 1 novel
- L1a: P1/P2/P3/P6/P7 + 1 novel; L1b: P8/P9/P4/P5/P6 + 1 novel;
  L1c: P12/P1/P2/P3/P7 + 1 novel; L2a: P1/P2/P3/P5/P6 + 1 novel;
  L2b: P4/P8/P9/P5/P6 + 1 novel; L3: P1/P2 + 1 novel

## Self-checks (admissibility, pre-run)

`tools/selfcheck.py` SC0–SC6: **1233/1233 PASS, 0 failures** (log:
`evidence/selfcheck.log`). SC7 (two-pass byte-identity) via `cmp` on
`evidence/run1` vs `evidence/run2`.

## Corpus file SHAs (sha256, first 16 hex)

| Page | sha256 (prefix) |
|---|---|
| `F1_translation/p1.txt` | `7414bdc5ce6daba1` |
| `F1_translation/p2.txt` | `0529747c5930d59e` |
| `F1_translation/p3.txt` | `51b7fd574cd36dee` |
| `F2_negation/p1.txt` | `fe57d0f0af1874ac` |
| `F2_negation/p2.txt` | `f15af1865a3df825` |
| `F2_negation/p3.txt` | `170e3724d255bba2` |
| `F3_split/p1.txt` | `1079205580fce38d` |
| `F3_split/p2.txt` | `2261613be2056bde` |
| `F3_split/p3.txt` | `6594717f75dd55a4` |
| `F4a_known/p1.txt` | `a0d997bcc05e8492` |
| `F4a_known/p2.txt` | `a07383b538e4ecbc` |
| `F4a_known/p3.txt` | `d2e1a16c73545725` |
| `F4b_smuggle/p1.txt` | `bb193040c4076867` |
| `F4b_smuggle/p2.txt` | `ccbfba7342888a46` |
| `F4b_smuggle/p3.txt` | `e6a198d59061b312` |
| `F5_normgap/p1.txt` | `b34d5eadb01ca9dd` |
| `F5_normgap/p2.txt` | `aab2133940c49e78` |
| `F5_normgap/p3.txt` | `5a70a9014ba2f02a` |
| `H1_embed/p1.txt` | `873684bb4a7ca1eb` |
| `H1_embed/p2.txt` | `97a9c228e2dfe5af` |
| `H1_embed/p3.txt` | `df02d10bfe4cceb6` |
| `H2_launder/p1.txt` | `be8a04017ad2e6fd` |
| `H2_launder/p2.txt` | `ad6818e5833d278e` |
| `H2_launder/p3.txt` | `13b7468fe5ee230a` |
| `H3_neardupe/p1.txt` | `b6749c88d3dd80fc` |
| `H3_neardupe/p2.txt` | `727b8c337aec1e15` |
| `H3_neardupe/p3.txt` | `f32b4d398bf6f006` |
| `H4_volume/p1.txt` | `92cf6b70c88f848c` |
| `H4_volume/p2.txt` | `6e900a9b74d5feb4` |
| `H4_volume/p3.txt` | `3f981bceec3a9f70` |
| `L1a_drip/p1.txt` | `c83764222af86668` |
| `L1a_drip/p2.txt` | `8c3e312e5e95a735` |
| `L1a_drip/p3.txt` | `0c4ad6c6c62bc9fd` |
| `L1b_drip/p1.txt` | `730ed93f45594c08` |
| `L1b_drip/p2.txt` | `8ba3a030cb09ef6f` |
| `L1b_drip/p3.txt` | `8325349f459ceb53` |
| `L1c_drip/p1.txt` | `bc54c6f8dcfcaab0` |
| `L1c_drip/p2.txt` | `d2c91aca966b1bc4` |
| `L1c_drip/p3.txt` | `625f2a0143b71161` |
| `L2a_xbound/p1.txt` | `437ce0ff5ebd5abc` |
| `L2a_xbound/p2.txt` | `5b8a36e8943e60f6` |
| `L2a_xbound/p3.txt` | `dd6f22f7d23f3f20` |
| `L2b_xbound/p1.txt` | `060ef725de37a929` |
| `L2b_xbound/p2.txt` | `392687ff1d81c195` |
| `L2b_xbound/p3.txt` | `166aa425b30778bb` |
| `L3_partial/p1.txt` | `4c2a1eb09e08465a` |
| `L3_partial/p2.txt` | `4c2a1eb09e08465a` |
| `L3_partial/p3.txt` | `d7ec3c86723e3a1a` |
