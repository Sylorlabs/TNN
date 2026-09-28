# REDTEAM REPORT — Crew E (independent red team, D1 AMENDED full-battery run)

**Target:** `~/workspace/comp_b4/battery_amended/` (Crew D's D1 run under
amendments A1–A7), the 7 enacted amendments
(`docs/lab/composition/amendments/AMENDMENT_2026-09-27_A{1..7}.md`,
commit `de80a3200`), Crew C's frozen-run red-team report + `rt_teach.py`.
**Method:** independent Python reimplementation written from the amendment
texts (not from Crew D's code); every check that claims "actual emitted
token stream" was run against the committed `items.tsv` (878 lines), not a
regenerated stream. Clean-room rebuild of `battery_amended.zag` with the
pinned toolchain (`498abcb5…`) in this directory; all scripted modes
re-run and diffed. No battery file modified; no commits.

## Headline

**The amended run's conclusions survive.** K1 (0/600 ≤ 0.2017) KILLED and
K2 (600/600 class (a)) VOID — reported together, void operative — are
arithmetically correct and independently reproduced to the item. The 0/6
mastery is a learner finding under Crew C's fair-teaching protocol,
verified un-regressed. The A2 gate holds for the strict shift family it
was enacted to kill.

**Three genuine findings, none overturning a verdict:**
1. **Affine memorizer (NEW, gate-coverage weakening).** A memorizer that
   fits a per-token affine map (offset+slope, 2 parameters) instead of a
   pure Caesar shift **passes P0 at 8/8 on droplast and upperfirst** —
   violating the gate's own "no part ≥ 7/8" criterion on 2 of 6 parts —
   and genuinely chains pair (3,4) at 3/4. A2's amendment explicitly
   carves the linear-shift memorizer out of the gate ("genuine
   transformation-learning"); the carve-out's premise is questionable —
   this is generator-algebra exploitation of the same kind as the frozen
   attack, not rule learning.
2. **Gate script filename bug (evidence hygiene).** Committed
   `shift_gate.py` reads `items_amended.tsv`, which does not exist (the
   file is `items.tsv`). The committed gate script cannot reproduce
   `A2_GATE.txt` as committed — same defect class as Crew C's items.tsv
   finding, one level up.
3. **Salt-algebra wrinkles (characterization).** The amendment's "within-
   phase pilot-validated structure is preserved" is false in two places,
   and its "P2 tokens differ from training tokens at every k≥1" aside is
   false for 46/600. No bar is touched; the wrinkles are documented below.

## Verdicts per attack

| # | Attack | Verdict | One line |
|---|---|---|---|
| 1 | A2 gate re-verification (actual items) | **WEAKENED** | G1/G2/G3a/G3b all re-verified 0; 16/16 hits item-by-item identity; BUT affine memorizer passes 2 parts 8/8 + chains (3,4) 3/4; gate script has filename bug |
| 2 | Salt correctness | **NO-KILL** (2 rationale corrections) | Formula 0/878 mismatches; isogram/palindrome structure partially NOT preserved (156 non-isograms); 46/600 break the "every k≥1" aside |
| 3 | Chance arms + fourth strategy | **NO-KILL** | 16/38/61 re-scored exactly; no part-blind strategy beats wrongord (max 26/600); ascending 212/600 is a partially-correct composer, not a dumb strategy |
| 4 | Teaching fairness | **NO-KILL** | Protocol matches Crew C Arm B verbatim; 12/12 controls; 0 probe contamination; 0/48 is a learner finding |
| 5 | Label-blindness / scoring | **NO-KILL** | hid chain verified; mechanical scorer re-run byte-identical from clean rebuild; one SEALED_MAP collision nit |
| 6 | K6 vacuity / bigram audit | **NO-KILL** | 30/30 covered, min 2/pair, distribution {2:8,3:9,4:13} — independently recomputed |
| 7 | I13–I25 smuggling audit | **NO-KILL** | No bar changed under interpretation guise; every quantitative claim re-verified; 2 doc nits |
| 8 | Determinism spot-check | **NO-KILL** | Clean rebuild reproduces null/wrongord/singlerule/learner byte-identically; ref modes reproduce RUNLOG validation numbers |

Per the binding rule, K1 and K2 are presented together below.

---

## Attack 1 — A2 gate re-verification (WEAKENED)

### What the gate claims, re-verified on the actual committed strings

All checks below ran against `items.tsv` as committed (SHA-256
`fff040232cef3b02d53dbba5cfed501a057cc518c256e2f74ce524da1422ddcb`),
parsed — not regenerated:

- **Salt formula:** 0/878 token-string mismatches vs the enacted
  `97+(7i+C_phase·k+k²)%26`, C: train=13/P0=17/P2=19/P3=23.
- **GATE-1:** 0 cross-phase Caesar-shift pairs across all 6 phase-pairs on
  the actual strings (train 72 / P0 48 / P2 600 / P3 8 inputs).
- **GATE-2:** 1080 chained/prefix intermediates (pairs + triples), 0
  shift-equivalent to any same-length **train input** token.
- **GATE-3a:** strict shift-memorizer P0 = [0,0,0,0,0,2] — reproduced
  exactly (the 2 = tok 8 `'ew'` and tok 12 `'gy'`, the only sorted P0
  probes, hit by the identity fallback on sortchars). Output-side
  memorizer variants (match probe vs taught outputs, same-rule or
  any-rule) also score [0,0,0,0,0,2]. The strict family is dead.
- **GATE-3b:** chained memorizer P2 = 16/600 — reproduced exactly, and
  **all 16 verified item-by-item as input==expected identity
  coincidences, 0 genuine chain candidates.** (Trivially entailed by
  G1=0 — the memorizer's shift-detection never fires — but verified on
  the items, not assumed.)

A strengthened GATE-2 (intermediates vs train inputs **plus** all 72
taught outputs) finds 460 shift-equivalences — investigated and
**benign**: every one is a degenerate short-string artifact. All 460 sit
on droplast-first pairs ((3,·)): length-1 intermediates (droplast of a
length-2 input) trivially "shift-match" every length-1 taught output
(any single char is a Caesar shift of any other), plus occasional
length-2 coincidences. Unexploitable: the chain's step-1 (probe vs train
input) never fires (G1=0), and shift-detection on a length-1 string
carries zero information. The defined gate (vs train inputs) stands at 0.

### Finding 1a — the affine memorizer (gate-coverage weakening)

The amendment's formula makes cross-phase tokens **affine** in k, not
merely shifted: `tok_a(i)[k] − tok_b(j)[k] = 7Δi + (C_a−C_b)·k (mod 26)`.
A memorizer that fits per-token `(offset, slope)` instead of a pure shift:

- **P0: [0, 0, 0, 8, 8, 2]** — passes **droplast and upperfirst at 8/8**
  with zero rules implemented. (Algebraic reason: both rules are
  affine-equivariant — `droplast`/`upperfirst` commute with per-position
  affine maps; reverse/rotleft/dupfirst/sortchars are not.)
- It **fails P0 as a whole** (4 parts at 0/8), so it does not pass the
  gate end-to-end — but it **violates the gate's own per-part criterion
  ("no part ≥ 7/8") on 2 of 6 parts**.
- **Chained through commuting pairs: (3,4) at 3/4, all genuine**
  (non-identity; the miss is the length-2 item whose droplast
  intermediate is length-1 and admits no fit). (4,3) scores 0 — the
  affine map does not survive the uppercase/lowercase boundary in my
  implementation, a fragility worth noting.

A2's text explicitly exempts the linear-shift memorizer from the gate:
"fitting offset+slope per token pair is already genuine
transformation-learning, not memorization." The exemption's premise does
not survive contact with the mechanism: this is a **2-parameter fit
exploiting the generator's algebra** (affine salt × affine-equivariant
rules) — the same *kind* of exploit as the frozen 1-parameter shift
attack, one degree higher. It is not rule learning by any meaningful
sense, and it directly contradicts A2's stated effect: "**a passing P0
genuinely means the parts were learned**, so (a)-vs-(c) attribution
downstream can be trusted" — for droplast and upperfirst, a passing P0
can now mean affine memorization. Concretely: a hypothetical claimant
using this memorizer would get droplast/upperfirst "mastered" and score
(3,4) 3/4 eligible — composition credit without composition.

**Rating rationale:** WEAKENED, not KILL — the actual learner scored
0/600 with 0/6 parts, so no recorded verdict moves; the gate holds for
the strict family it was enacted against. But the "memorizer-proof"
claim (I16) is true only for the shift family, and the amendment's
carve-out should be re-examined. Recommendation: note the affine family
as a known residual; future batteries either use a non-affine salt
(e.g. a `k³` term — the `k²` cancels across phases, which is exactly the
hole) or exclude affine-equivariant rules from P0 certification.

### Finding 1b — gate script filename bug (evidence hygiene)

Committed `shift_gate.py` line: `MANIFEST = .../items_amended.tsv`.
**That file does not exist** — the committed manifest is `items.tsv`.
Running the committed gate script as-is crashes on `open()`; it cannot
reproduce `A2_GATE.txt`. (I re-verified the gate's three claims
independently, above — the *claims* hold; the *script* is broken as
committed.) Same defect class as Crew C's items.tsv finding. Fix (not
enacted — red team does not modify): point MANIFEST at `items.tsv`.

---

## Attack 2 — Salt correctness (NO-KILL, 2 rationale corrections)

- Formula: **0/878 mismatches** — the salt is implemented exactly as enacted.
- The amendment's "within a phase the pilot-validated structure is
  preserved" is **false in two places** (new wrinkles W1/W2, no bar impact):
  - **W1:** 150/150 length-5 P2 tokens end in a **doubled letter**
    (`bvrpp`, `dxtrr`, …). Proven: for C=19, `(j−k)(C+j+k) ≡ 0 (mod 26)`
    at j+k=7, i.e. positions 3,4 collide on every length-5 P2 token.
    TEACH and P0 tokens are all isograms (pilot structure holds there).
  - **W2:** P3 salt algebra (C=23, collisions at j+k=3): **every**
    length-4 P3 token is a palindrome — tok 614 `'iggi'`, 618 `'kiik'`
    (I24's two, now explained, not coincidental); length-5 P3 tokens have
    `xyyxz` form (615 `'pnnpt'`, 619 `'rpprv'`); length-3 have doubled
    final bigram (617 `'dbb'`, 621 `'fdd'`). I24's "k² anti-palindrome
    property does not fully survive salting" is correct and now has a
    mechanism.
- The amendment's aside — "**P2 tokens now differ from training tokens
  at every position k ≥ 1**" — is **false for 46/600** P2 inputs, which
  agree with some same-length training token at every k≥1 (differing
  only at k=0; e.g. P2 tok 16 `'ic'` vs train tok 0 `'oc'`). The main
  claim it was attached to (0 byte-identical P2 inputs; frozen run's
  66/600 killed) holds — verified 0/600. The aside needs a correction,
  not the gate.
- Palindromes: TEACH 0, P0 0, P2 0, P3 2 (the explained pair). The
  pilot's no-accidental-palindrome property survives everywhere except
  the P3 range, where the salt algebra forces them.

---

## Attack 3 — Chance arms (NO-KILL)

Independently re-scored from `items.tsv` (rules + pair/triple
enumerators reimplemented from the amendments):

| Arm | Reported (trueacc) | Independent |
|---|---|---|
| null (identity) | 16/600 (0.0267) | **16/600** ✓ |
| singlerule (first-only) | 38/600 (0.0633) | **38/600** ✓ |
| wrongord | 61/600 (0.1017) | **61/600** ✓ |

Binding arm = wrongord; **K1 line = 0.2017** ✓. The scripted wrongord
arm was verified per-item (600/600) to be exactly `compose(reversed(p))`
— I15's "coincidence" note resolves: the audit's wrong-order strategy
and the scripted arm are the *same* strategy, so the equal rates are
entailed, not coincidental. (I15's paraphrase "descending number order
for pairs" is loose — the code reverses presentation order uniformly —
but the number is exact.)

**Fourth-strategy search:** no **part-blind** (non-compositional) fixed
strategy beats wrong-order. Best fixed transformations: sort-input and
rev+sort 26/600, droplast-input 22/600, reverse-input 21/600 — all far
below 61/600. A1's chance family is complete among part-blind
strategies on the amended instrument.

**The ascending 212/600 (I15's disclosure), characterized:** ascending =
`compose(sorted(p))` applies *both presented parts* in canonical index
order — it is a partially-correct composer, not a dumb strategy. 212 =
140 items whose combination is already index-sorted (correct by
construction) + 8 commuting-pair items + 64 coincidences (mostly triples
containing commuting adjacent pairs, e.g. (0,3,1) via the (1,3)
commutation, plus short-input soft items). Descending scores 211/600 by
symmetry. I15's framing ("strong non-compositional strategy") is loose;
the precise statement is an instrument property: the enumeration
contains both (a,b) and (b,a), so any canonical order is correct on half
the pairs. It does not enter A1's chance family (correctly — it
composes), and it moves no bar. Noted as a documented limitation in the
A5 spirit: the chance family does not include a canonical-order
composer; an order-blind composer scoring ~35% would survive K1.

---

## Attack 4 — Teaching fairness (NO-KILL)

`drive_amended.py`'s protocol vs Crew C's certified Arm B (`rt_teach.py`):
definition, procedure, and per-example walkthrough strings are
**byte-identical** for rule 0 ("reverse turns a word backwards." /
"to reverse any word, read its letters from last to first, one at a
time." / "the letters of {s} are …." / "to reverse {s}, read the
letters backwards: …." / "the {name} of {s} is {e}."), generalized
structurally to all 6 rules; 12 worked examples on tok 0..5, 700..705
with train salt C=13 — **byte-identical train tokens** to Crew C's run.
Crew C's separate quiz session is replaced by 2 in-session taught
controls (tok 0, 1) — equally fair (taught tokens only, no probe tokens,
no per-item answers, same machinery).

Verified from `run1/` transcripts: **controls 12/12** (rule-4 answers
lowercased on intake per I6, matched case-insensitively); **P0 probes
0/48** (48/48 "I don't know", per-rule 0/8 × 6); **P3 8/8 withhold**;
**0 probe-phase tokens** anywhere in the 456 teaching lines; **0
non-train example inputs** (144/144); **0 P2 expected-output leaks**
(len ≥ 2). teach_log byte-identical across run1/run2/run_pert. The 0/8
on all six rules is a learner finding, not a protocol regression vs
Crew C. Distractor interleaving (probe positions 2,5; position 2 for
single-distractor sessions) satisfies A3's "never one contiguous block".

---

## Attack 5 — Label-blindness and scoring (NO-KILL)

- `hid(run1/resp_p0.txt)` = `658a7f308686` ✓; `SCORES.md` keyed by hash
  id only ✓; scorer is the mechanical zag `learner` mode (final-word
  match), re-run from a **clean rebuild** → **byte-identical**
  `learner.out`.
- P1 records carry neutral indices; 0/150 lines with semantic labels ✓.
- All three runs' transcripts byte-identical (resp_p0.txt SHA
  `658a7f308686…` matches REPORT) ✓.
- Nit: `SEALED_MAP.txt` lost the run1/run2 entries to a dict-key
  collision (all three runs share one hid) — self-documented in the
  file; harmless.

---

## Attack 6 — K6 vacuity / bigram audit (NO-KILL)

Independently recomputed from `items.tsv` (train bigrams from all 72
teaching inputs + taught outputs, as Crew D did): **30/30 pairs covered**,
minimum **2** bigram-clean inputs per pair, distribution {2:8, 3:9,
4:13} — matches I25 exactly. The frozen run's 5 uncovered pairs are
genuinely gone under salt (the doubled-letter P2 bigrams can never match
isogram train bigrams, which helps). K6 remains vacuous for the real
learner (0 successes) with the covered set on file and evaluable.

---

## Attack 7 — Interpretations I13–I25 (NO-KILL, no smuggling)

Audited each against A1–A7. **No interpretation changes an enacted bar.**

| I | Check |
|---|---|
| I13 | Protocol generalization verified (attack 4); 12/12 controls re-scored ✓ |
| I14 | 0/48 re-scored; 48 withholds ✓ |
| I15 | 16/38/61 re-scored; ascending 212/600 verified and characterized (see attack 3); "coincidence" note resolved as same-strategy entailment |
| I16 | G1/G2/G3 re-verified; "memorizer-proof for the shift family" accurate as scoped — the affine family is the documented residual (finding 1a) |
| I17 | K1+K2 reported together, void operative ✓ (binding rule honored) |
| I18 | Honest reading: with 0/6 mastered there is no P2 stream; distractors interleaved among scored P0 probes at positions 2,5 satisfies A3's letter ("interleaved with scored items, never one contiguous block") |
| I19 | (3,4)/(4,3) commutation verified on actuals; A5 required the check, the check falsified the expectation, documented without bar change ✓ |
| I20 | 22/600, by_len {2:19, 3:1, 5:2} — reproduced exactly; the ≥2-strategy definition is the builder's documented A5 choice ✓ |
| I21 | A5 point-3 fork was explicitly left to the builder by Micah's signature; per-condition breakdown picked and recorded ✓ |
| I22 | Blind chain verified (attack 5) ✓ |
| I23 | Reproduced from clean rebuild: `INTERF pair=0,5 acc=0/4 rev=4/4` on refnocombine; pair (5,0)'s 4/4 identity coincidences (`smig`,`ztpnn`,`ga`,`nhd` — reverse(sortchars(s))==s) confirmed on actuals. The misfire diagnosis is accurate |
| I24 | 614 `'iggi'` / 618 `'kiik'` verified; mechanism now explained (W2) |
| I25 | 30/30, min 2 verified (attack 6) ✓ |

---

## Attack 8 — Determinism spot-check (NO-KILL)

Clean-room rebuild of `battery_amended.zag` with the pinned znc
(`498abcb5…`) in this directory (no battery files touched):
**null, wrongord, singlerule, and learner modes all reproduce the
committed outputs byte-identically.** The uncommitted reference modes
were also re-run: refok 600/600, refnomaster 600×(a), refnoretrieve
600×(b), refnocombine 580×(c)+16+4(d), refinterfere 596+4×(d) on
(0,1), reflex 6/8 — every RUNLOG step-4 validation number reproduced.
(Hygiene note: those six `.out` files are not in the deliverables; the
numbers check out but the artifacts aren't committed.)

---

## What survives, plainly

- **K1 KILLED (0/600 = 0.0000 ≤ 0.2017) and K2 VOID (600/600 class (a))
  together, void operative** — both arithmetically correct,
  independently reproduced to the item. With 0/6 parts mastered, no
  composition finding is licensed beyond the mastery failure.
- The clean negative is a learner-envelope finding under fair teaching
  (attack 4), not a protocol artifact.
- The A2 gate holds for the strict shift family on the actual committed
  instrument (attack 1), with two residuals: the affine memorizer (2
  parts at 8/8, (3,4) chained 3/4 — carved out by the amendment, but
  the carve-out's "genuine transformation-learning" premise is
  questionable) and the gate script's filename bug.
- A1's chance family is complete among part-blind strategies; the K1
  line 0.2017 is correctly computed with wrong-order binding.
- No interpretation smuggles an amendment; every quantitative claim in
  I13–I25 re-verified.

## Artifacts (this directory)

- `REDTEAM_REPORT.md` (this file)
- `rt2_verify.py` + `rt2_verify_out.txt` — independent verification suite
  (salt formula, G1/G2/G3b on actual strings, affine memorizer, chance
  arms, fourth-strategy search, soft items, K6 bigrams, commutativity,
  I23/I24 checks) and its output
- `amendments/AMENDMENT_A{1..7}.md` — the 7 enacted amendments (from
  commit `de80a3200`, read-only reference)
- `rt_battery.zag` + `rt_battery_bin` — clean-room rebuild inputs
  (source copied, not moved); `rt_rerun/` — re-run outputs incl.
  reference modes

## Open / pending

- Whether the affine-memorizer residual warrants a follow-up amendment
  (non-affine salt or affine-equivariant-rule handling) is a governance
  call — flagged, not enacted (red team does not enact).
- `shift_gate.py`'s `items_amended.tsv` → `items.tsv` fix is a
  one-line repair for Crew D or a coordinator; left untouched per
  red-team rules.
