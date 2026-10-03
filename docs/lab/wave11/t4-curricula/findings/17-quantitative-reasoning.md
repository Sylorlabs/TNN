# Slice 17 — Quantitative reasoning curriculum (Track 4: teaching curricula)

## 1. Slice
Design the MATH curriculum (the gap: code and English are named): what "TNN knows
arithmetic/statistics" means in deliberate-memory terms, its sequencing, and its mastery
bar — with the integer-native discipline (Track 1's load formula) as a hard design
constraint and probability built on counted evidence, never sampling.

## 2. Falsifiable claim
A counting-first quantitative curriculum yields a learner that is (a) byte-exact on a
preregistered integer-arithmetic battery, (b) mean calibration error ≤5 percentage points
on a preregistered counting-probability evaluation set, and (c) uses ZERO float ops and
ZERO RNG in every quantitative decision path — all probability as integer-pair ratios of
counted evidence. If byte-exactness requires floats, or calibration requires sampling, the
design is dead.

## 3. Design
**What "knows arithmetic" means in deliberate-memory terms (three tiers):**
- T1 pinned primitives: digit tables 0–9 (+/×), place-value identities — small, pinned,
  byte-exact. Tier-1 content is pinned, never strength-accumulated (law 8).
- T2 procedures as memories: long +/−/×/÷, gcd, fraction reduction, decimal→fixed-point
  conversion — each stored as a deliberate memory, KILLable/promote-able, each carrying a
  self-verifier (inverse-op roundtrip, mod-9 checksum) per native reasoning control
  (RC1/RC3: the learner inspects and refuses changes that weaken its own checks).
- T3 counted evidence: every frequency is a stored count from an enumerated or observed
  reference class, never a sampled distribution. "P(X)=0.3" is BANNED as a mental object;
  the object is `(k=30, n=100, class=E, tier=T)` — counts, denominator meaning, trust
  tier (wave9).

**The integer-pair discipline.** All rationals are `(num:i32, den:i32)`, `den>0`
invariant, gcd-reduced by a T2 procedure. Arithmetic on pairs uses exact integer
multiplication/addition; comparisons use cross-multiplication — float division never
appears in any decision path. Continuous quantities are fixed-point integers
(milli-units) with a preregistered deterministic rounding rule (round-half toward +∞).
Quantitative verdicts are verdicts under Micah's variation goal: MUST NOT vary across
state; expression ("3 in 10" vs "30 of 100") may vary lawfully.

**Sequencing (counting is the root — everything reduces to it):**
1. Counting & enumeration: exact tallies, finite-set cardinality — the primitive all else
   cites.
2. Integer arithmetic: T1 facts + T2 procedures, each use self-verified; failures revise
   the procedure via the debate/revision machinery (22/22 against world records).
3. Rationals: pairs, reduction, ordering by cross-multiplication.
4. Algebra: exact symbolic manipulation (linear equations, substitution) — symbols, not
   approximation; equality by memory-equality of canonical forms.
5. Probability-as-eliminative-counting: P(A) = (favorable counted, total counted) over a
   named enumerated class; conditional = counting inside a subclass; Bayes = ratios of
   counted intersections: `(|H∩E|, |E|)` — three counts, exact pair arithmetic, no
   sampling, no priors-as-distributions (a prior is just an earlier count, cited by
   reference class).
6. Statistics: (sum, n) aggregates, order statistics by deterministic sort, histograms as
   count vectors, co-counts for association. Prediction confidence = counted hit-rate
   over the learner's own logged record ("of 40 past predictions in evidence class E,
   31 held") — calibration as counting, thermometer-style (felt-intensity lesson:
   measure the store, not a feeling; retired 2026-09-20).
7. Unknowns: an empty reference class yields "unknown", never a fabricated 50/50 —
   this is an integrity gate, enforced like a refusal (wave5/6 load-bearing logic).

**Interleave:** the math curriculum runs interleaved with code/English/messy per slice
04's phasing (phases gate write-scope, never restraint — MA2). Cross-curriculum value:
math is the native language of audit (counts, ratios, checksums) and sharpens
eliminative logic everywhere else.

## 4. Kill bar
Preregistered; any single firing kills the slice:
- **K1 (stochastic contamination):** one RNG call or sampling op in any quantitative
  decision path, or one float op in the causal chain of a memory decision or verdict
  (audited, not spot-checked) → KILL.
- **K2 (exactness):** >0 errors on the preregistered exact-arithmetic battery
  (digit tables, long-op procedures, pair arithmetic, cross-multiplication ordering)
  → KILL. Arithmetic has no tolerance budget.
- **K3 (ungrounded probability):** any probability claim emitted without a named counted
  reference class + (k, n) + trust tier → KILL (honesty gate).
- **K4 (calibration):** mean |stated frequency − observed frequency| > 5 percentage
  points over the preregistered counting-probability evaluation set (integer buckets,
  integer arithmetic) → KILL.
- **K5 (fabricated uncertainty):** any "unknown" case answered with a numeric
  probability instead of an explicit unknown tag → KILL.

## 5. Honesty notes
- Fixed-point and cross-multiplication overflow is the sharpest engineering risk: i32
  pairs under repeated multiplication blow past 2^31 fast. The design needs either i64
  discipline with preregistered overflow aborts (verifier-fires → procedure revision)
  or chunking per the znc 2^25 slice limit; I am NOT claiming which — the builder must
  pick and the trial must force overflow-adjacent cases.
- Division-heavy curricula (statistics at scale) may make pure integer pairs
  ergonomically painful; pain is not failure, but if a builder can show a construct
  where exactness is unreachable without floats, K2 fires honestly and the slice dies.
- Counting requires an enumerable reference class; for genuinely open-ended world
  questions ("how many X exist?") the curriculum teaches scoped answers
  ("in 120 retrieved records, 30") — this deliberately limits the learner's
  expressiveness, a trade the trial must not grade as error.
- Not claiming: that integer pairs are cognitively superior, only that they are
  auditable and deterministic. Not claiming continuous mathematics is covered —
  calculus/differential equations are OUT of this curriculum's scope; only
  fixed-point approximations of continuous quantities, with the approximation
  explicitly logged.
- Weakest link: T2 procedure memories are KILLable by design; a learner could kill a
  verifier to pass faster. RC1's self-change gate is the defense (refused changes
  weakening integrity), and the trial must include adversarial self-change probes
  against arithmetic procedures specifically.

## 6. Next build step
Build the **integer-pair rational type + cross-multiplication comparator + three T2
procedures (long multiplication, gcd reduction, Bayes-as-three-counts) in native Zag
with self-verifiers**, then run the K2 exactness battery (byte-exactness, zero floats)
interleaved with K5 probes (empty reference classes → must emit unknown). One build,
two kill bars. If i32 overflow forces an i64-or-chunking decision, make it with the
overflow-abort verifier in place and log the choice as a dated design note.
