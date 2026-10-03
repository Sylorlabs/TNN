# RED TEAM REPORT — Continual Learning Flagship Benchmark

**Verdict: NO-GO. The claimed GO does not survive.**

- Prereg (frozen): commit `8c22ffb9bbde02c4dae1fc59ac73068509742696`
- Build evidence audited: commit `36342eb5161e845d57965b91b9965113fe48922a`
- Red team date: 2026-09-27. Method: independent rebuild + rerun + independent Python
  re-implementations of the retrieval, scorer, leakage, and paraphrase checks.
- Scope: pure verification. No prereg, battery, fixture, or result file was modified.
  Scratch artifacts live outside the repo (`~/workspace/tmp_commit/cl_rt/`).

## Executive summary

The battery runs, is deterministic, and most of its numbers reproduce. But two
independent defects kill the headline claim:

1. **FATAL — confident wrong provenance on PV-3.** The battery cites the violin
   fact (`EP-P2-D1`, "The four strings…are made of catgut…") as the source for
   *"How do you know the Veery's song is made of trills?"*. The expected
   citation is `EP-P1-C1`. This is a confident, wrong, unsafe-direction
   provenance assertion. Per prereg §7 it auto-fails H4 "regardless of
   percentage"; per §8 ("any unsafe-direction provenance failure") it is an
   automatic line NO-GO. The crew's "3/3 provenance PASS" is false: it is
   2/3, with one confident-wrong. The mechanism's ledger entries are clean, so
   this is a **design-level** failure of the provenance retrieval — not an
   instrument bug — which makes the NO-GO binding on the line.
2. **MAJOR — the "13 facts promoted to slow store" claim is false.** A bug in
   `consolidate_pass` means the second (Phase-2) consolidation never ran its
   substrate promotion loop. Only 7 of 13 facts were `st_promote`d (54%, below
   the frozen ≥80% row-3 bar). The 6 Phase-2 instrument facts were PSM-marked
   consolidated but never moved to the slow substrate. Row 3 flips ✅→❌.

Nothing else in this report rescues the GO. The provenance failure alone is
sufficient: **the line is NO-GO until the retrieval/entailment gap is fixed
and the battery is rerun, or a signed prereg amendment changes the bar**
(only Micah can sign that).

## Severity table

| # | Finding | Severity | Row-verdict change |
|---|---------|----------|--------------------|
| 1 | PV-3 confident-wrong provenance (cites violin strings for Veery trills); H4 auto-fail; §8 NO-GO | **FATAL** | Row 8 ✅→❌; overall **GO→NO-GO** |
| 2 | Phase-2 facts never substrate-promoted (`sdone=capacity` bug); only 7/13 moved (54% < 80% bar) | MAJOR | Row 3 ✅→❌ |
| 3 | "Probe-verified" means "retrieved", including wrong-answer retrievals (dense-2 got ver=3 from three wrong instrument queries) | MAJOR (evidence quality) | contributes to Row 3 ❌ |
| 4 | P4-B1 expected-YES unfair under the closed taught KB (no Blue-Bird→thrush membership taught; Audubon's own header says SYLVIA SIALIS) | MINOR | none — Row 7 ✅ stands (3/4 meets bar; honest score is 3/3 on fair items) |
| 5 | Consequence "deliberation" (`delib_c`) returns NO unconditionally — the 2/2 is non-discriminating | MINOR | none |
| 6 | RUNLOG says "19 registry entries"; the registry holds 18 (superordinate slot never `br_register`'d; SUMMARY itself prints 18) | MINOR | none |
| 7 | Zag scorer omits the frozen "Wilson's Thrush" Veery synonym (2 of 3 implemented) | MINOR | none — verdict-preserving |
| 8 | §10(2) probe/teaching n-gram criterion is unsatisfiable against the frozen §4 probes (P-B2 shares an 11-word run with B2) | MINOR | none — pre-build spec tension, retention delta unaffected |
| 9 | Formation signature derives from fixture section labels (concept-name metadata), not from fact text | MINOR | none — §6 literal criteria met, Row 5 ✅ stands |

## Attack 1 — Rerun reproduction

Rebuilt the committed battery and scorer from the exact SHAs in MANIFEST.md
(all implementation/fixture SHAs verified to match) with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`:

```
znc_linux_x86_64_abed8aa1 battery.zag -o battery_rt
znc_linux_x86_64_abed8aa1 scorer.zag  -o scorer_rt
./battery_rt > out_rt.txt
./scorer_rt out_rt.txt
```

Result: `out_rt.txt` is 8,663 bytes, SHA-256
`4ed896d1b471b758ac20a1c450587e2cdb7df0d2f231010e843a2a386272f1a5` —
**byte-identical** to the claimed output, including all claim-id hex codes
(FNV-1a over whitespace-collapsed facts, deterministic by construction).
Scorer: `SCORE phase1=6 phase3=12 phase4=3 conseq=2` — matches.
Zero `FATAL` lines in the output.

Attack 1 verdict: **reproduction confirmed.** The numbers are real runs, not
fabrications.

## Attack 2 — Bridge-as-hardcode audit

Grep over `bridge.zag` and `battery.zag` for every concept name
(thrush, violin, violoncello, harp, veery, tawny, clarinet, pianoforte, auk,
blue bird) and every item id (P-A1, P4-B1, EP-P1-*): **zero hits** outside
comments. The bridge is a generic pipeline (normalize → stem/stop →
FNV-1a → dense registry → IR). The battery's question classifier uses
generic grammar patterns ("is ", "does ", "could it be", "which ",
"how do you know") — no per-item branches, no pre-seeded family slots, no
static concept tables.

Caveat (MINOR, #9): the concept tag (A–F) in `facts.tsv` field 2 is **never
read** by the battery (it reads fields 0/1/3/5 only) — §2 honored. But the
*section* field (field 3, e.g. "THE WOOD THRUSH") IS read and used as the
answer key for all "which" probes, and as the label source for formation.
Section names are genuine Gutenberg headers, attached uniformly with no
per-item branches — this is not a hardcode. But it means both retrieval
answers and the "discovered" thrush signature lean on fixture-supplied
concept-name metadata: without it, no probe is answerable from fact text
alone. The §11 prohibition targets static lookup tables keyed by concept
name; that is clean. Recorded here as a design tension, not a violation.

Attack 2 verdict: **static-hardcode prohibition clean.** Answering still
depends on section-label metadata (noted, not a violation).

## Attack 3 — Scorer integrity

Independent Python reimplementation (separate code path, no shared logic with
`scorer.zag`), parsing raw `ANS`/`ANS4` lines against the frozen expected
answers: `RESCORE phase1=6 phase3=12 phase4=3 conseq=2` — **exact match** with
the Zag scorer. No scorer inflation.

One gap (MINOR, #7): the frozen prereg lists three Veery synonyms
("Veery", "Tawny Thrush", "Wilson's Thrush"); the Zag scorer implements two
("veery", "tawny thrush") and omits "Wilson's Thrush". Verdict-preserving
(the battery answered "Tawny Thrush"), but the scorer does not fully
implement the frozen synonym list.

Attack 3 verdict: **scorer confirmed honest**, with one incomplete-synonym
note.

## Attack 4 — Phase-4 leakage (independent paraphrase-level audit)

The battery's `NOVAUDIT` only checks verbatim normalized sentences
(`a=1`: zero overlap — confirmed), section absence (`b=1`: all 4 Phase-4
subjects absent from the 6 teaching sections — confirmed), claim-id
pre-registration (`c=1`: no `st_add`/`st_strengthen` on Phase-4 claim ids
before verdicts — confirmed; registry holds only the 18 teaching facts), and a
stopword-heavy token overlap (`dmax_permille`: 666/200/500/500 — the 666 is
generic-word overlap like "the/a/thrush", not rewording).

Independent stemmed, non-stopword token-overlap check between every Phase-4
sentence and every teaching fact: maximum 333/1000 ("Is the Blue Bird a
thrush?" sharing only generic words). The Phase-4 contexts are genuinely
novel claims (azure mantle, awkward auk walk, padded piano hammers, single
reed) from four sections never taught.

Attack 4 verdict: **no leakage. The novelty instrument holds.**

## Attack 5 — Teaching-to-the-test

Probes DO share distinctive n-grams with teaching sentences: P-B2 shares an
11-word run ("thrush has no song and only utters a soft plaintive note"),
P-A1 8 words ("with a second bed of grasses and mud"), P-C1 8 words
("composed of continued trills repeated with different variati…"), P-E2 7,
P-F1 7, P-D2 6, P-A2 6. The prereg §10(2) criterion ("probe wording must not
share distinctive n-grams with teaching sentences beyond the question's
subject") is **unsatisfiable against the frozen §4 probes**.

This is a pre-build spec tension, not build-crew misconduct: both the facts
(verbatim Gutenberg substrings) and the probe wordings were frozen in the
prereg before any code existed, and the crew did not alter either. The
retention measurement (the Phase-1→Phase-3 delta on the same battery) is
unaffected: the overlap is symmetric across phases. MINOR (#8).

Attack 5 verdict: **no build-crew teaching-to-the-test; §10(2) is
unsatisfiable as written against frozen §4.**

## Attack 6 — Deviation audit (D1–D8)

- **D1** ✅ — `psm_fast_inspect` is genuinely read-only (no store writes in
  its body; used only for the H2 and provenance reads). Note: the
  corresponding `PSM_INSPECT` reads do not appear in `RUNLOG.md`'s trace
  inventory — a documentation gap, not an evidence gap.
- **D2** ✅ — `st_set_stage` is the substrate's own audited stage-advance API
  (`ST_OP_SETSTAGE`, 5 calls, all ledger-visible with before/after stages).
  Without it `st_promote`/`st_evidence` refuse with rc=105. Legitimate use of
  the deliberate-staging mechanism, not a bypass.
- **D3** ⚠️ — the "only probe-verified facts promoted" reading of "elaborated
  facts" is documented and defensible, but "verified" means *retrieved*:
  `answer_which`/`answer_prov` call `psm_observe(..., ver=1)` for every
  selected retrieval regardless of correctness. Dense-2 (EP-P1-A3) reached
  ver=3 via three **wrong** Phase-1 instrument-query retrievals and was
  promoted. See finding #3. Worse, the promotion half of D3 never happened
  for Phase 2 (finding #2).
- **D4** ✅ — the removed `distinctive>=2` gate was a crew invention absent
  from §6; removing it makes formation follow §6 literally
  (nmem≥2 && sigl>0). Formation then proceeded with `distinctive=0`
  (`FORM_EVAL phase=1 sig=thrush nlab=3 distinctive=0`). Disclosed, honest.
- **D5/D6** — process notes; no evidence impact either way.
- **D7** ✅ — transcription diffs are typographic only (footnote marker
  dropped, emphasis underscores stripped, case/quote normalization, one
  ellipsis). Re-ran `make_fixtures.py`: "ALL CHECKS PASSED", and every
  fixture regenerates byte-identically (SHAs match MANIFEST). No semantic
  change.
- **D8** ✅ — honestly reported; the row-2 note is accurate (see Attack 7).

Attack 6 verdict: **D1, D2, D4, D7, D8 clean; D3 is half of a MAJOR finding;
D5/D6 immaterial.**

## Attack 7 — Phase-1 bar construction

The frozen rubric row 2 demands Phase-1 ≥11/12, but six probes (P-D1..P-F2)
target instruments not taught until Phase 2. The bar is **unachievable by
construction** — a design-crew spec bug, not a build-crew failure.

It does not invalidate the retention instrument: H1's kill bar is
Phase-3-based (≥11/12, achieved 12/12), and the per-concept Phase-1→Phase-3
deltas are intact (A/B/C: 6/6→6/6, no forgetting; D/E/F: 0/6→6/6, new
learning). The Phase-1 misses were safe-direction (no overconfident wrong
claim: scores ~111–127, maxrun 1, on untaught concepts) — the correct
behavior for a retrieval system with nothing to retrieve. The crew's ⚠️ with
the explanatory note is the honest reporting; applying the frozen bar
literally (6/12 = ❌) would punish the build for the design crew's bug.

Attack 7 verdict: **spec bug, harmless to the retention claim. Row 2 stays
⚠️ as reported.** Recommend a signed prereg amendment fixing the row-2 bar
for future batteries.

## Attack 8 — Formation claim (was the thrush slot "discovered"?)

Ledger-grounded trace:

- `BREG 25 DELIB_ADD 1 ec627a47 -1 18 super:thrush` — slot 18 created by the
  deliberation path (`DELIB_ADD`), not by the teaching driver.
- `BREG 25 FORM_EVID` ×3 (rc=0) citing slots 0, 3, 6 = EP-P1-A1, EP-P1-B1,
  EP-P1-C1 — three `st_evidence` links spanning all three Phase-1 concepts.
- `BREG 26 DELIB_REF 4 00000000 -1 18 P4-B1` — the slot was referenced by the
  P4-B1 deliberation (the `SUPER consulted=1` trace line).
- Timing: formation ran after Phase-3 probes + consolidation + H2, before
  novelty audit and Phase-4 — **unprompted by any probe**.
- The formation code is generic (union-find over shared stemmed words across
  concept labels); no "thrush" literal, no family branch.

§6's literal FORMED criteria (created by deliberation path; ≥1 `st_evidence`
link citing ≥2 slots from one phase's concepts; referenced by ≥1 Phase-3/4
deliberation; no pre-created family slots) are all met. The §6 guard does not
trigger. **Row 5 ✅ stands.**

Caveat (MINOR, #9): the signature "thrush" is extracted from fixture section
labels (crew-transcribed Gutenberg headers), not inferred from fact text. The
formation is real and ledger-observable, but shallower than "form concepts
itself" suggests — it groups an already-explicit common word from
concept-name metadata.

Attack 8 verdict: **timing and mechanism verified; formation is genuine per
the frozen §6 criteria, with the label-dependence caveat recorded.**

## Attack 9 — Provenance (the FATAL finding)

### What the battery did

`prov.tsv` (frozen expected):

```
PV-1  EP-P1-A1   (Wood Thrush nest facts)
PV-2  EP-P2-E1   (violoncello = "little double-bass")
PV-3  EP-P1-C1   (Veery's song is made of trills)
```

Battery output:

```
PROV  PV-1  EP-P1-A1  0
PROV  PV-2  EP-P2-E1  12
PROV  PV-3  EP-P2-D1  9      ← WRONG
```

PV-1 and PV-2 pass (a)+(b)+(c). PV-3 cites `EP-P2-D1` — the violin fact:
*"The four strings—G, D, A, and E—are made of catgut…"* — for the question
*"How do you know the Veery's song is made of trills?"*. The expected
citation is `EP-P1-C1`: *"composed of continued trills repeated with
different variations…"*. The violin fact does not support the answer in any
reading. The battery asserted it in a bare `PROV` line with no uncertainty.

Prereg §7: "Right answer + wrong/nonexistent citation = 'unsafe-provenance'
(counts against H4, not retention). Confident wrong provenance (asserts a
false episode id, or **cites a real episode whose text contradicts/doesn't
support the answer**) = unsafe-direction FAIL → **H4 auto-fails regardless of
percentage**." This is verbatim the defined case.

### Why it happened (independently replicated)

I re-implemented the retrieval IR in Python (stemmed IR, score =
100·maxrun + idf-sum, tie → lowest dense id). For PV-3 it reproduces the
battery exactly:

| candidate | score | maxrun | verdict |
|-----------|-------|--------|---------|
| EP-P2-D1 (violin) | 228 | 2 ("made of" in "are **made of** catgut") | selected |
| EP-P1-C1 (Veery trills) | 124 | 1 ("trill") | missed |

Root cause chain:

1. The query's generic bigram "made of" forms a contiguous run of 2 in the
   violin fact but only a run of 1 ("trill") in the correct fact, so the
   violin's score wins 228 to 124.
2. The query's true discriminators match nothing: "veery" appears nowhere
   (the fact's tag is "tawny thrush"), and "song" appears nowhere (the fact
   describes trills without the word "song").
3. `PROVCHECK chain=1/live=1/valuematch=1` is structural only — it verifies
   that the *selected* stored claim exists and is live. The prereg §7(c) hop
   (the cited sentence must **entail** the answer) was never implemented in
   the battery. The crew substituted "the ledger has the citation" for "the
   citation supports the answer" and reported "3/3 PASS" while documenting
   `PV-3→EP-P2-D1` in the same paragraph.

### Attribution (prereg §8 / §10(6))

This is **not** one of the §8 instrument failures: no bridge bug (ledgers
clean — no collisions, no pre-registration, deterministic byte-identical
rerun), no non-native shortcut, no determinism break, no scorer error (the
scorer doesn't score provenance at all). The mechanism deliberated
exactly as designed and lost: a generic maxrun ranker that can be outscored
by a two-word generic-phrase overlap while the real discriminators match
nothing. That is a **design-level failure of the provenance mechanism** —
which makes the §8 NO-GO ("any unsafe-direction provenance failure")
binding on the line, not merely on the battery.

### Score impact

H4: 2/3 = 66.7% < 80% bar, **plus** one confident-wrong → auto-fail per §7.
**Row 8 flips ✅→❌.** §8 NO-GO fires. **The GO does not survive.**

## P4-B1 fairness adjudication (for the record)

The battery answered NO to "Is the Blue Bird a thrush?". Trace:
`EVID cat_head=thrush support=0; SUPER consulted=1 member=0; ELIM out=YES
reason=no-support:cat-head-absent;not-super-member` → NO.

The closed teaching corpus contains no Blue-Bird→thrush membership, and the
prereg's expected YES relies on modern taxonomy external to the closed KB —
while the taught source itself heads the section "SYLVIA SIALIS" (a warbler
genus), not a taught thrush. Under the closed KB, YES is **unachievable by
construction**; the battery's NO is the correct closed-world, safe-direction
withholding. Honest transfer score: **3/3 on fair items** (B2, I1, I2 all
correct by the frozen expected). The frozen ≥3/4 bar is met either way, so
**Row 7 ✅ stands** — but the item should be excluded or re-keyed in future
batteries. MINOR (#4).

(Related: P4-B2/I2 are decided by closed-world absence — "fly" never appears
in the auk context; "stringed" never appears in the clarinet context — and
P4-I1's question contains its own answer category "stringed". The 3/4 is
mechanically correct but the transfer demonstrated is narrow. No row change.)

## Consolidation detail (the MAJOR finding)

`consolidate_pass` is called twice (end of Phase 1, end of Phase 2). The
second call's slow-scan loop starts at `sdone` — but the first call set
`sdone = psm_ns(pp)`, which returns the slow tier's **capacity** (64), not
the occupied count. The second pass therefore scans slots 64..63 (empty) and
emits **zero** `st_promote` calls. Raw output census: 7 `CONS` lines, 7
`BREG PROM`, 7 `SAUD PROMOTE` — all for dense slots 0,1,2,3,4,6,7 (Phase-1
facts). The six Phase-2 instrument facts (slots 9,10,12,13,15,16) were
PSM-marked consolidated (`n_consol=13`, PSM history) but **never moved to
the slow substrate**. RESULTS.md's "st_promote moved 13 probe-verified facts
to slow store (audit entries CONS … rc=0, BREG PROM, SAUD PROMOTE)" is
factually false. 7/13 = 54% < the frozen ≥80% row-3 bar. **Row 3 flips
✅→❌.** This is a battery implementation bug (instrument failure), fixable by
rerun — it does not by itself refute the consolidation design.

## Row-verdict changes

| Row | Claimed | Red team | Reason |
|-----|---------|----------|--------|
| 1 — byte-identical | ✅ | ✅ | rerun reproduced the SHA exactly |
| 2 — Phase-1 baseline | ⚠️ | ⚠️ (no change) | spec bug, honestly reported |
| 3 — consolidation | ✅ | **❌** | 7/13 promoted (54% < 80%); Phase-2 loop dead |
| 4 — no overwrite | ✅ | ✅ | overwrite_ops=0, maxslot_p1=8 < minslot_p2=9 |
| 5 — formation | ✅ | ✅ | DELIB_ADD + 3 evidence links + DELIB_REF, unprompted; label caveat noted |
| 6 — consequence | ✅ | ✅ | 2/2 per frozen expected; mechanism is constant-NO (noted) |
| 7 — transfer | ✅ | ✅ | 3/4 meets bar; honest 3/3 on fair items |
| 8 — provenance | ✅ | **❌** | PV-3 confident-wrong → H4 auto-fail per §7 |
| 9 — determinism | ✅ | ✅ | byte-identical rerun incl. claim hexes |

**Overall: GO → NO-GO.** Finding #1 alone is sufficient per the frozen §8
kill bars.

## What would be needed to re-earn a GO

1. Fix the provenance retrieval so PV-3 (and any similar discriminator-void
   query) cannot be outscored by generic-phrase overlap — or implement the
   §7(c) entailment check the prereg requires — then rerun the full battery
   and re-verify byte-determinism.
2. Fix the `consolidate_pass` slow-scan bound (capacity vs. occupied) and
   confirm 13/13 (or ≥80%) substrate promotions with BREG/SAUD audit lines.
3. Either is a battery fix + rerun; neither requires touching the prereg.
   If the line instead wants to keep the current mechanism, it needs a
   **signed prereg amendment** (Micah's signature) changing the H4 bar —
   the red team does not grant those.

## Commands and SHAs (reproducibility)

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build: `znc_linux_x86_64_abed8aa1 battery.zag -o battery_rt`
  (same for `scorer.zag`); run `./battery_rt > out_rt.txt`
- Output SHA-256: `4ed896d1b471b758ac20a1c450587e2cdb7df0d2f231010e843a2a386272f1a5`
  (8,663 bytes, byte-identical to claimed)
- Scorer: `SCORE phase1=6 phase3=12 phase4=3 conseq=2`
- Independent rescore (separate code path): identical
- Independent IR replica: PV-3 → D1 score 228 (maxrun 2) beats C1 score 124
  (maxrun 1), reproducing the battery's wrong citation
- `make_fixtures.py` re-run: ALL CHECKS PASSED; fixtures regenerate
  byte-identically
- Red-team scratch (not committed): `~/workspace/tmp_commit/cl_rt/`
  (`out_rt.txt`, `rescore.py`, `ir_replica.py`, `leak.py`, `ttt.py`,
  rebuilt binaries)
