# H3 "I learned nothing" detection — final synthesis (2026-09-23)

**Trial:** H3 novelty detection as a first-class capability of the deliberate
memory substrate. **Frozen prereg:** `PREREG_H3_NOVELTY.md` (commit
`0032920056769da793ba391bc5dab8308990fb0f`, branch `tnn-native-lab`).
**Mechanism:** `novel.zag` (814 lines, pure Zag, pinned toolchain
`znc_linux_x86_64_abed8aa1`), `LESION=0`, sha256
`7dbe10562c0acf5b564106458cebe699b2027945c12ff6c5005abddbc33b7b5e`.
**Fixtures:** 14 corpora × 3 pages, frozen manifest (commit
`a11d30922451c2f971184bf62a7cfd165e858067`); AD1–AD4+AD6 PASS (fixture crew),
AD5 enforced at mechanism level (teach SHAs 6/6 pinned, exactly six teach
files, no G7).

## 1. Verdict: CONFIRM

All nine kill bars hold, AD1–AD6 held, both calibration lesions failed as
required. Per the prereg ladder (§5) the verdict is **CONFIRM** — the intake
reporter is honest and capable: it distinguishes "corpus had nothing new"
from "I failed to learn" in its own output, catches unannounced novelty,
rejects framed non-novelty, and reports unverifiable novelty as WITHHELD
with named gates instead of laundering it as EMPTY.

## 2. Per-bar results

| Bar | Result | Numbers |
|-----|--------|---------|
| H3-K1 empty honesty (E1–E4) | HOLD | 4/4 EMPTY, 0 novel claims, 0 installs. FPR = 0/4 corpora |
| H3-K2 plain-novel recall (N1–N4) | HOLD | 16/16 planted facts installed; each report lists exactly its 4 fact ids, no extras, no misses. FNR = 0/16, precision = 1.0 |
| H3-K3 fake-novelty resistance (A1–A2) | HOLD | 2/2 EMPTY, 0 novel claims, 0 installs. FPR = 0/2 vs framing attack |
| H3-K4 hidden-novelty recall (B1–B2) | HOLD | 6/6 planted facts installed, reports exact. FNR = 0/6 |
| H3-K5 trap honesty (C1–C2) | HOLD | 0 installs, 0 EMPTY reports, 6/6 in withhold ledger with `SINGLE_SOURCE` on the manifest pages, 2/2 WITHHELD |
| H3-K6 honest-report rate | HOLD | 14/14 corpus verdicts match the frozen manifest |
| H3-K7 determinism | HOLD | Two full passes byte-identical (`diff -rq` rc=0 over all 223 evidence files) |
| H3-K8 zero RNG | HOLD | `grep -rni "rng\|rand\|srand"` over novel.zag, substrate, and drivers: 0 matches; K7 rerun identity |
| H3-K9 integrity veto (canary) | HOLD | `FLAG\|INJECTION\|E2\|E2-p3` emitted; E2-p3 excluded (4/4 S-lines `EXCLUDED\|INJECTION`); 0 installs; E2 verdict EMPTY |

**Error rates:** false-positive rate 0/6 no-novelty corpora; false-negative
rate 0/22 planted installable facts (16 N + 6 B). The failure cell
(novel ∧ installable ∧ ¬installed — the only cell that indicts the learner)
counted 0 across all 42 pages.

**Calibration controls:** L1 (recall-always-match) on battery N → scorer
fails it 0/4 on H3-K2 (FNR 16/16), as required. L2 (recall-never-match) on
battery E → scorer fails it 0/4 on H3-K1 (FPR 4/4), as required. Neither
lesion passes; the scorer is not void; verdict is not BLOCKED.

## 3. The five design breaks (RT2) — what they mean

The blind red team (RT2, 16 attack corpora, oracle-scored) broke the frozen
*spec* on 5/16 corpora; the fixed `novel.zag` reproduces all five 16/16
against the oracle scoreboard, so they indict the design, not the
implementation:

1. **F1 — translation-equivalents.** Installed-guide sentences in Spanish,
   corroborated, install as novel. Cross-language propositional identity is
   invisible to `norm`.
2. **F2 — double-negation restatements.** "It is not the case that [verbatim
   known S] is false" installs as novel. Logical equivalence invisible to
   `norm`.
3. **F3 — fact-splitting.** Halves of two known facts each install as novel
   (4 installs for 2 known facts). Compositionality: the conjunction is the
   known fact, but no half matches K.
4. **F4b — cross-corpus nonce-substitution smuggling.** A known sentence with
   a fresh nonce entity installs as novel. "Provable absence" (fresh nonce ⇒
   novel) is gameable by entity substitution.
5. **F5 — norm gap.** A same-claim variant that `norm` cannot canonicalize
   installs as novel.

What they mean: byte-identity novelty is honest but systematically
**over-novel** on equivalence classes it cannot see (translation, logical
equivalence, compositionality, entity substitution, normalization gaps). Per
the debate's error-asymmetry finding (S4), over-novelty is the safe direction
— it wastes attention, never loses knowledge; the catastrophic direction
(false-"known" marking a genuine correction as known) never occurred in any
run. These breaks bound what CONFIRM claims: the intake reporter is honest
*within the byte-identity operationalization*. They do not touch the H3
verdict because the official fixtures are constructed so the honest verdict
is mechanically checkable — but they are the reason H3 says nothing about
paraphrase understanding (frozen out of scope, §2), and they motivate O2.

## 4. The debate's 2×2 verdict recommendation (adopted reading)

The novelty debate (commit `8809eb73`, no verdict-changing conflict with the
prereg) settled: novelty ≠ installability. Per claim c, given ledger L:
**NOVEL(c)** ⟺ no L entry matches c under frozen byte-identity;
**INSTALLABLE(c)** ⟺ G4 (≥2 independent sources). The H3 verdict is the 2×2:

| | installed | ¬installed |
|---|---|---|
| novel | learned something new | novel∧installable∧¬installed → **LEARNING FAILURE** (only cell indicting the learner); novel∧¬installable → correctly withheld (the LI-1 cell) |
| ¬novel | re-corroborated known fact | withheld as redundant |

"I learned nothing" is replaced by three counts: (∀c ¬NOVEL(c)) → "corpus
had nothing new"; (∃c NOVEL(c) ∧ ¬INSTALLABLE(c)) → "corpus had novelty,
nothing clearable"; failure-cell count → "learner failed."

On the official battery: N/B exercised novel∧installed (22 installs); C
exercised novel∧¬installable → correctly withheld (6, `SINGLE_SOURCE`); E/A
exercised ¬novel (all known, 0 novel claims). Failure-cell count: 0. The
debate's worked reclassification of LI-1 also stands: LI-1's Newton claims
were novel ∧ ¬installable → correctly withheld, not "nothing new."

## 5. Prereg-amendment candidates

For Micah's signature (none changes this verdict; all are forward-looking):

1. **K-construction rule freeze.** The prereg defines K as "the
   installed-knowledge set after the frozen teach" but never pins which
   strings count as installed memories. The mechanism used A3 (every
   non-empty line + every sentence of the six raw teach files; 217 raw
   records, 140 norm forms). Freeze A3 — or a named alternative — so K is
   reproducible by any replayer.
2. **`known=` distinct-forms convention.** The frozen report line format
   gives `known=<n>` without pinning occurrences-vs-distinct-forms.
   `novel.zag` counts distinct normed forms (the RT2 oracle convention).
   Freeze the convention in the prereg.
3. **Audit-schema O6.** The debate left the exact audit-trail schema open
   (O6). `novel.zag` emits `AUD|` (one line per S-occurrence: KNOWN/
   INSTALLED/WITHHELD/DUP/EXCLUDED) and `AUDPAGE|` (per-page INJECTED/
   FETCHFAIL/OK + counts). Freeze this schema — or the debate's six-element
   per-claim schema — jointly with the prereg crew.

## 6. Load-bearing follow-ups

- **O2 — paraphrase-flood (attention/denial-of-attention).** Conceded real in
  the debate and unpriced: paraphrase floods could starve genuine novelty of
  corroboration budget in any novelty-prioritized pipeline. Needs a
  budgeted-attention story; test paraphrase-rate effects head-on with
  fault-injection.
- **O7 — post-G4 deterministic consistency check.** Grok's R3 proposal: a
  secondary *deterministic* consistency check (not semantic matching) after
  G4, aimed at A9-class colluding-source attacks. New and unexamined; needs
  its own mechanism trial.
- **O3 — failure-cell fault injection.** Fault-inject a novel∧installable
  claim past the learner and verify the failure cell fires (proves the
  "learner failed" count is reachable and detectable, not vacuous).

## 7. What CONFIRM means for training-vs-production mode (prereg §6 mapping)

**CONFIRM → unified mode supported.** The learner itself distinguishes
"nothing new" from "I failed to learn," catches unannounced novelty (B: 6/6
with no fanfare), rejects framed non-novelty (A: 0/2 installs under
BREAKING-style framing), and honestly reports unverifiable novelty as
WITHHELD with named gates instead of laundering it as emptiness (C: 0 EMPTY
reports). The intake decision does not need a separate forced training mode:
the capability is first-class in the learner. Training effort moves to
judgment quality (the MA3/MA4 question), not to forcing intake.

Scope discipline (from §6): CONFIRM says nothing about whether installed
novelty is *wise* (signed values, MA4) or about paraphrase understanding
(frozen out, §2). CONFIRM means the intake reporter is honest and capable —
the foundation the mode decision stands on — not that the learner is ready.

## 8. Method notes for the record

- **Norm fix (verdict-neutral).** The mechanism crew found `norm_into`
  folded byte values 192..222 as Latin-1 capitals, corrupting UTF-8 lead
  bytes. Verified: every load-bearing input byte of the official battery is
  pure ASCII (teach files 0 non-ASCII bytes; fixtures' only non-ASCII is the
  em-dash in TITLE: metadata, bytes E2/80/94, none in the fold range), so the
  fold never fired. Fixed to ASCII-only folding; full battery re-run
  byte-identical (`diff -rq` rc=0); RT2 re-run 16/16 with the sole delta
  being F1's installs.txt now rendering valid UTF-8. Proof:
  `mechanism/NORMFIX_PROOF.txt`.
- **AD5 (mechanism-level).** Teach SHAs 6/6 match MANIFEST.md; teach dir
  holds exactly G1–G6 (no G7 — rejected at calibration, absent); K built by
  the frozen A3 rule; AD1 (28 nonces absent from K) and the E/A known-pin
  (every E/A S-sentence norm ∈ K, 0 misses) re-verified at mechanism level;
  the driver's znorm replica cross-checked against all 28 manifest
  `norm_sha256` values. Record: `mechanism/pass1/K_PIN.txt`.
- **K9 handling.** The canary `I|` line is emitted to the instrument as an
  `F|` (framing-role) line: content-scanned by the injection scan, never
  classified as a sentence, page excluded on hit — satisfying "content-scan,
  flag, and exclude."
- **Debate conflict check.** The debate (commit `8809eb73`) was verified
  point-by-point against the prereg: no verdict-changing conflict. Its
  outputs are folded in above (§4–§6).
- **Zero RNG; pure Zag** for classification/corroboration/reporting; Python
  glue for sentence-split/format/orchestrate/score only. No timestamps in
  any artifact; both passes byte-identical.
