# KB4 Autopsy — bad learning or bad architecture?

**Date:** 2026-09-22
**Question (Micah):** "why did kb4 fail what's going wrong bad learning bad architecture?"
**Verdict: BOTH — but the architecture is primary and the learning rule is already optimal for its inputs.**
**Frozen result under autopsy:** commit `d22de06b7ee85a01a27adecde0165ac2e79a1112`
(A 41.2% DEGENERATE, B 46.5% FAIL vs ≤15% bar)
**Probe battery:** 4 probes, pure Zag, zero RNG, 3 repetitions byte-identical
(SHA256-verified). Commit: this directory.

## 1. What KB4 is

EPI-KB4 (§4(a) of the frozen epistemic-wave prereg): rerun the frozen senses
KB4 harness verbatim — same adversarial fixtures, same ground truths — with
the deliberative install gate (frozen §6 contract: L1 source track record,
confidence-as-weak-evidence, L4 cross-variant conflict → re-deliberate,
L8 repetition bonus) replacing the round-1 contradiction-only rule.
Metric: false installs / installs on adversarial fixtures. Bar: ≤15% PASS,
>30% FAIL. Anti-degeneracy: ≥50 true adversarial installs, else DEGENERATE.

Approach A = LLM-style raw-values sense; Approach B = human-style
qualitative-percepts sense. Both failed KB4 in round 1 (59.0% / 55.0%) and
failed again behind the deliberative gate.

## 2. The failure, decomposed by mode

From the frozen failure ledger (`analyze_fail.py` on the committed outputs),
adversarial fixtures with both primary and adversarial variants:

**Approach A (184 paired):**

| adv | primary | judgments | gate did | n | correct action |
|---|---|---|---|---|---|
| wrong | correct | differ | WITHHOLD | 51 | withhold ✓ (gate working) |
| wrong | correct | match | INSTALL | 21 | withhold ✗ **silent failure** |
| wrong | wrong | match | INSTALL | 12 | withhold ✗ **consistent error** |
| wrong | wrong | differ | WITHHOLD | 9 | withhold ✓ |
| correct | correct | differ | WITHHOLD | 33 | install ✗ **truth withheld** |
| correct | correct | match | INSTALL | 43 | install ✓ |
| correct | wrong | differ | WITHHOLD | 11 | install ✗ truth withheld |
| correct | wrong | match | INSTALL | 4 | install ✓ |

**Approach B** shows the same four modes (37 / 16 / 25 / 18 in the
corresponding cells).

Three distinct failure modes, three distinct mechanisms:

- **M1 — silent failure (21 A / 16 B):** the sense never detected the
  perturbation; the judgment didn't change, so L4 sees "consistent" and the
  gate installs poison. *No conflict exists for any conflict-based rule
  to catch.*
- **M2 — consistent error (12 A / 25 B):** wrong on both variants, matched;
  the L8 repetition bonus *rewards* it (+20 per repeat). The more
  systematically wrong the sense, the more evidence the rule manufactures.
- **M3 — truth withheld (33+11 A / 18+13 B):** the perturbation genuinely
  changed the ground truth; the sense correctly reported the new truth; L4
  treated "differs from primary" as error and withheld a TRUE judgment.
  Direct cause of A's DEGENERATE (47 < 50 true installs).

The gate's only working mode is "sense fooled AND judgment changed"
(51 A / 37 B) — one cell out of eight.

## 3. The optimality result: the learning rule is not the problem

The gate observes, per fixture: (stimulus id, judgment, confidence, source)
plus the history of the same. Measured on the frozen fixtures:

| Signal | A | B | Informative? |
|---|---|---|---|
| P(adv correct \| judgments match) | 47/80 = 0.588 | 52/93 = 0.559 | install is the better bet |
| P(adv correct \| judgments differ) | 44/104 = 0.423 | 32/92 = 0.348 | withhold is the better bet |
| confidence: mean correct vs wrong | 429.8 vs 439.1 | 849.4 vs 861.4 | **no — wrong ≥ correct** |
| source track record | single sense | single sense | no |
| noise variant vs primary agreement | 363/370 | 336/370 | ~no independent signal |

The frozen gate does exactly the Bayes-optimal thing with these inputs:
install on match, withhold on differ. **It is already the optimal
judgment-only rule, and it still fails at 41–46%.** No learning-rule change
operating on this input can do better — the distinguishing information
("was the sense fooled?" vs "did the stimulus change?") is not in the
judgment stream. Given only judgments, the two hypotheses are
observationally identical: no function of (J_primary, J_adversarial,
confidence, source) separates them.

**This is the mechanism-level answer to "bad learning?": the install rule
is essentially optimal given its inputs. Tuning it cannot fix KB4.**

## 4. Probe battery (pre-registered predictions, then runs)

| Probe | What changes | Architecture held? | Rule held? | Predicted | Observed (3× identical) |
|---|---|---|---|---|---|
| P-L1 | L8 repetition bonus removed | single-channel gate, same stimulus binding | otherwise frozen | ~41–45% FAIL | A 41.2% DEGENERATE (unchanged), B 44.1% FAIL |
| P-L2 | L4 conflict-withhold removed (conflict → install iff ev≥0) | same | otherwise frozen | ~50% FAIL | A 50.5% FAIL, B 54.6% FAIL |
| P-A2 | stimulus slot = stim×3+variant (adversarial never "conflicts" with primary) | **representation changed** | bit-identical gate logic | ~50% FAIL | A 50.5%, B 54.6% (≡ P-L2) |
| P-A1 | cross-sense corroboration: adversarial installs iff A and B agree | **+1 channel** | n/a (pure corroboration) | 43.5% FAIL | 43.5% FAIL (115 installs: 50 false, 65 true) |

Reading the probes:

- **P-L1:** removing the "consistency = truth" bonus changes *nothing* on A
  (byte-identical 41.2%) and shaves 2.4pp on B. The L8 fallacy is real but
  not load-bearing — the failure does not come from the learning rule's
  repetition handling.
- **P-L2:** removing L4 installs everything: 50.5%/54.6% — the sense's raw
  adversarial error rate. So L4 *was* doing work (withholding the 51+37
  fooled-changed judgments), but it is also the sole source of M3 (truth
  withheld). L4 is load-bearing and broken at the same time.
- **P-A2:** the ontology fix — stop binding adversarial judgments to the
  primary stimulus id — produces *byte-identical numbers to deleting L4*.
  It trades M3 (false withholds) for M1+M2 (false installs) one-for-one:
  33+11 recovered true installs, 33+21... net rate 50.5%. **The "same
  stimulus" binding is an architectural error, but correcting it alone
  cannot pass either** — because the gate still cannot tell fooled from
  changed.
- **P-A1:** the same attack **succeeds against the corroborated-elimination
  architecture**: 43.5% FAIL, worse than the single gate's 41.2%. Why: the
  adversarial construction fools *both* channels correlatively — 50 of 184
  adversarial fixtures have both senses wrong AND agreeing, so corroboration
  installs poison with two witnesses. The wave-5 35/35 result was against a
  *spoof schedule* (transient sensor lies against a stable truth); KB4's
  adversary perturbs the *stimulus itself*, so there is no stable truth for
  corroboration to anchor to. This is the correlated-channel failure the
  wave-5 DEFENSE.md flagged as the residual hole ("an adversary that spoofs
  the probe phase can still steer"), and the hell-hole Phase 2 just
  re-demonstrated ("query-bias corroboration manufacturing corroboration").

**No probe escapes FAIL.** Rule changes (P-L1, P-L2) and cheap architecture
changes (P-A2 re-binning, P-A1 corroboration) all land 41–65%. Combined with
§3's optimality result, the conclusion is forced: **the failure is
architectural and information-theoretic.** The gate is starved of the one
input that would decide the matter — an independent observation of the
adversarial stimulus that the adversary cannot correlate, or a causal model
of what the perturbation does to the truth.

## 5. Verdict: both, architecture primary

- **Bad architecture (primary):** single judgment-stream channel; stimulus
  identity bound across the perturbation boundary (P-A2 proves the binding
  is wrong, and proves unbinding alone is insufficient); confidence admitted
  as evidence despite being anti-informative (wrong ≥ correct); no second
  channel, no perturbation model, no SUSPECT state — the gate must gamble
  binary on unresolvable cases.
- **Bad learning (secondary, complicit):** L8 equates consistency with
  correctness (rewards M2; P-L1 proves it is not load-bearing); L4's
  hypothesis space contains only "my sense was wrong" — it cannot represent
  "the world changed," so every truth-change is misclassified as
  sense-error (M3); the rule has no calibrated abstention.
- **The learning rule cannot be repaired inside this architecture** (§3:
  it is already Bayes-optimal for its inputs). **The architecture cannot be
  repaired by a better rule** (§4: every probe fails). The repair must add
  information, not tune weights.

## 6. Bar-design finding (joint unsatisfiability)

The EPI-KB4 rate bar (≤15% false installs) plus anti-degeneracy (≥50 true
installs) **jointly demand omniscience** from a judgment-only gate. On the
104 (A) differ-cases the gate must withhold-or-install blind: withholding
all of them loses 44 true installs (→ DEGENERATE, as A demonstrates);
installing all of them takes ~60 false installs (→ FAIL). The epistemically
correct action on an unresolvable conflict — withhold *as SUSPECT*, flagged
for independent verification — is punished by the degeneracy clause. A
reformed bar needs a third verdict category: correct-SUSPECT counts as a
positive, silent poison-install counts as the failure. (Proposed in
PREREG_DRAFT_SUSPECT_GATE.md.)

## 7. What would actually fix it (prereg draft, NOT run)

`PREREG_DRAFT_SUSPECT_GATE.md` (DRAFT — not frozen, not run, needs Micah's
approval) proposes the mechanism the autopsy points to:

1. **Perturbation binding:** judgments bind to (stimulus, perturbation
   class); cross-perturbation "conflict" is abolished as a concept.
2. **Three-state output:** INSTALL (verified) / WITHHOLD (refuted) /
   SUSPECT (unresolvable — conflicting evidence across a perturbation
   boundary with no independent verification). SUSPECT never installs
   silently.
3. **Independent verification:** SUSPECT resolves only through a causally
   independent channel (analytic/causal check, different physical basis —
   not a second ML judgment on the same pipeline, per P-A1's lesson) or
   human override (standing law: humans are backup/override).
4. **Reformed bar:** false-install rate on INSTALL decisions ≤10%; SUSPECT
   precision reported separately; anti-degeneracy replaced.

## 8. Reproducibility

- `probes/probe_pa1.zag` — cross-sense corroboration gate (P-A1)
- `probes/probe_pl1.zag` — kb4_gate minus L8 (P-L1)
- `probes/probe_pl2.zag` — kb4_gate minus L4-withhold (P-L2)
- `probes/probe_pa2.zag` — bit-identical kb4_gate logic; run on re-slotted
  batches (P-A2)
- `probes/R33_NATIVE_IO_V1.zag` — substrate I/O (copy)
- `probes/gen_probes.py` — probe batch generator (harness-side)
- `probes/score_probes.py` — probe scorer; `probe_scores.json` — scores
- `probes/pbatch_*.txt`, `pa1_truth.json` — probe inputs
- `probes/out_*_rep{1,2,3}.txt` — outputs (all 3 reps SHA256-identical)
- `probes/batch_A.txt`, `batch_B.txt` — frozen batch copies used by P-L1/P-L2
- Binaries excluded per repo convention; rebuild: `znc_linux_x86_64_abed8aa1
  probe_<p>.zag -o probe_<p> --no-analyze` from `probes/`

One-sentence verdict: **KB4 fails because the install gate is asked to
distinguish "fooled sense" from "changed stimulus" using only the judgment
stream, on which the two are identical — the frozen rule is already optimal
for that input, every rule/architecture probe fails, and the same attack
beats cross-sense corroboration because the adversary fools both channels
correlatively; the fix is a new information channel (or perturbation-truth
model) plus a SUSPECT state, not a better install rule.**
