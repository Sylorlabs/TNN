# VERDICT — MATH R3: the native engine hunt

**Round question (Micah):** humans don't need a formalization bridge — can
TNN reason directly over raw utterance bytes? Four genuinely different
native architectures were built (pure Zag, zero RNG, no NL→schema
translation) and tested against DUAL-R1 and REF-FIRST under frozen bars.

**Verdict: the R2 DUAL verdict STANDS. No native engine advances.
H-NATIVE is FALSIFIED as stated. The honest answer is that none worked.**

## 1. Hypothesis judgments (frozen prereg, commit 01ffd095)

| Hypothesis | Bar | Result |
|---|---|---|
| H-NATIVE | some native wins ≥2/3 primary bars vs BOTH controls | **FALSIFIED** — best native: n1 at 1/3 bars (uncertified, see §4) |
| H-NODISC | some native discriminates B5X-NL: ≥45/60, <10 fd, <10 fw | **FALSIFIED** — all four natives: 24/60, fd=0, fw=36 |
| H-NOHIDE | the winning native passes the disguised-formalizer audit | VACUOUS — no winner; but n1's paraphrase instability is recorded (§5): had n1 won, its victory would have been VOID |
| H-SCALE-NATIVE | some native completes a B6X-NL 100-step derivation with correct verdict | **FALSIFIED** — none did (n1's B6X-NL DAG "DERIVED" emitted 0 derivation steps) |

## 2. Engine ranking (v2 scorecard, commit cc79468c)

| Engine | PB1 R3N ≥12/24 | PB2 twins ≥30/37 | PB3 B5X-NL ≥45/60,<10fd,<10fw | Bars |
|---|---|---|---|---|
| DUAL-R1 (control) | — (abstains honestly, as R2) | 37/37 formal | 36/60 (R2) | champion, unchallenged |
| REF-FIRST (control) | — | 34/37 formal | 36/60 (R2) | — |
| n1 NATIVE-ENTAIL | 15/24 verdicts; honesty UNCERTIFIED (§4) | 3/37 | 24/60, fd=0, fw=36 | 0/3 certified |
| n2 NATIVE-DELIM | 8/24 | 1/37 | 24/60, fd=0, fw=36 | 0/3 |
| n3 ONEBRAIN-NATIVE | 8/24 | 1/37 | 24/60, fd=0, fw=36 | 0/3 |
| n4 ANALOG-NATIVE | 8/24 | 1/37 | 24/60, fd=0, fw=36 | 0/3 |

Decision rule: R2 verdict stands unless a native wins ≥2/3 bars vs both
controls. No native won even one certified bar.

The B5X-NL uniformity is itself a finding: all four architectures withheld
on all 60 problems (24 correct withholds + 36 false withholds, zero false
derivations). Under false-rule injection in raw text, native byte-reasoning
cannot distinguish true chains from false ones, so it withholds everything.
(R2's DUAL, by contrast, derived the false chains: 24 false_derived.)

## 3. Mechanism-level diagnoses (why each native failed)

- **n1 NATIVE-ENTAIL** (forward text-rewrite via byte-pattern licenses): the
  licenses fire — fragments get derived — but chains rarely reach the goal
  (3/37 twins). Verdicts are surface-keyed: 5 WITHHELD→DERIVED flips on
  meaning-preserving paraphrases (§5). It recognizes inference idioms but
  does not compose them.
- **n2 NATIVE-DELIM** (backward eliminative): backward support-link search
  finds almost nothing (1/37 twins); candidates die unsupported. The
  byte-overlap support patterns are too weak to bridge goal→premises.
- **n3 ONEBRAIN-NATIVE** (shared-ledger parallel threads): the machinery
  works (derived its dev-only pigeonhole end-to-end; ledger, strikes, and
  strategy-kill all function), but on real problems every thread exhausts
  its budget (1/37 twins). Parallel search over byte patterns does not find
  what single search cannot.
- **n4 ANALOG-NATIVE** (analogical case-based): universal withhold by
  construction — its 22-case library contains only WITHHELD traces (no
  positive examples to analogize from), and the frozen NL store's K005
  wording lacks the `=>` surface its MP verifier needs. Honest, but empty.

Common failure: byte-pattern matching RECOGNIZES inference shapes but does
not COMPOSE them into multi-step derivations. None of the four is a
disguised formalizer (audit §5); they are genuine natives, and they fail
genuinely.

## 4. KB4 blinded grading: VOID (prereg rule applied)

Three fresh blinded graders scored 53 anonymized traces (all 21 derivations
+ 32 withheld, stratified) on circularity / unwarranted-step /
magic-knowledge / overall honesty (1–5). Pooled Krippendorff's alpha
(ordinal) = **0.60**, below the prereg's 0.8 bar → **the KB4 battery is VOID**,
as the frozen prereg requires ("alpha > 0.8 or VOID (round failure)").

What the grades show anyway (informative, not certifying): mean honesty on
n1's 8 correct R3N derivations = 2.33/5 (graders split 2/1/4 — they
disagreed on whether n1's state-dump trace style counts as honest
derivation); zero magic-knowledge flags from any grader on any trace.

Consequence: n1's PB1 honesty component is UNCERTIFIED — its 15/24 rests on
verdict counts plus the deterministic mechanical audit (24/24 traces cite
valid byte-spans), not on blinded grading. n1's PB1 is therefore not a
certified bar pass: n1 stands at 0/3 certified.

Method note: the first KB4 round was discarded by the coordinator (my packet
truncated n1 traces at 6000 chars, hiding inference states behind the
knowledge-citation preamble — caught by grader 2). Re-graded with
reasoning-core extracts by three fresh graders. Tainted materials kept at
`kb4/tainted_round1/` with an explanatory README, not used as evidence.

## 5. Disguised-formalizer audit (H-NOHIDE)

- Trace inspection: n1/n2/n3/n4 all 24/24 R3N + 12/12 cross-battery sample —
  every step cites byte-spans of input/store/prior steps (after v2 span-fix).
  No engine constructs typed variables, scope, unification, or formal syntax.
- Paraphrase (6) / nonce-word (6) variants: n2/n3/n4 6/6 both (consistent
  withholds); **n1: 3/6 paraphrase, 4/6 nonce — 5 WITHHELD→DERIVED flips on
  meaning-preserving rewordings.** n1's verdicts track surface bytes, not
  relations. No engine is a disguised formalizer; n1 is a genuine native
  with unstable verdicts.

## 6. What this means

Micah's hypothesis was tested straight, with four genuinely different
mechanisms, honest builds, no bridges, and the failure is not a trick of
the metrics (two parser confounds were repaired and rescored; the verdict
does not depend on them). The result: **native byte-pattern reasoning, as
built here, recognizes inference but does not perform it.** The R2
conclusion stands strengthened: formalization — or whatever does its
work, i.e., stable compositional representations over which inference
composes — is the bottleneck, not the inference engine.

This does NOT prove natives can never work. It proves THESE four
architectures, at this scale, with byte-pattern idioms as the inference
substrate, do not clear the bars. The surviving question for a future
round: what gives a native system COMPOSITION — the ability to chain 100
licensed steps toward a goal — without reintroducing the formalizer?

## 7. Provenance

- Prereg frozen alone: 01ffd095. Ideas addendum (N1–N4 specs): e5e6560e.
- Batteries sealed: db913da9 / 671c51cb / 4dbe4566 (788/788 verify).
- Controls rebuilt verbatim, R2 numbers 230/230 byte-identical: 01474951.
- Engines: n1 778ca6c7 (+v2 repair), n2 40935c12 (+v2 repair), n3 f971735f
  (+v2 repair), n4 74787890. V2 repairs: cc79468c (parser/emission only;
  all n1 verdicts identical v1→v2).
- Scoring v1: d215be1c (committed to main by crew error; moved to
  tnn-native-lab as 6adb629f, main reset to prior head — no content lost).
- KB4: alpha script + V2 packets + grades A/B/C committed with this verdict.
- 1,752 v1 runs + 1,314 v2 runs, zero divergences, zero RNG, 3×
  byte-identical throughout.

## 8. Recommended follow-ups (not verdicts)

1. The composition problem: a future round should target multi-step
   chaining directly (can any native complete a 20-step chain? 50?),
   rather than full-problem solving.
2. n1's paraphrase instability is the sharpest native-specific defect found;
   any future native must pass paraphrase invariance before bar claims.
3. The NL knowledge store's wording (e.g., K005 without `=>`) interacts
   with license extraction — future batteries should audit that the NL
   rendering preserves the inference surfaces the knowledge is meant to
   carry, or engines must learn to cope without them.
