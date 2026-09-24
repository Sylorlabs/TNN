# SOURCE-TRUST FORKS PROGRAM — Frozen Prereg

**Date:** 2026-09-23. **Ordered by:** Micah ("as a human I don't have knobs, I just learned myself" — fork everything, test head-to-head, figure-it-out wins ties).
**Status:** FROZEN. Committed alone before any fork code, fixtures, or results.
**Branch:** `tnn-native-lab` (sylorlabs/TNN).
**Dir (lab-relative):** `training_paradigms/source_trust/`

## 1. Question

TNN should carry trust in a source as something like 0→1. Micah's immediate
self-correction: **scrap the knob approach.** A human has no trust knob; trust is
learned from experience. Three forks test the three positions head-to-head:

- **Fork K (knob control):** explicit scalar trust per source, 0→1, hand-set
  initial values + a simple mechanical update rule (+δ on corroborated truth,
  −δ on caught lie, clamped). The baseline to **beat** — expected to lose, kept
  for honest comparison.
- **Fork L (learned trust):** no hand-set value. TNN builds a per-source track
  record from its own experience — corroboration outcomes, contradiction
  history, caught lies — and the trust value **emerges** from the record.
- **Fork S (no scalar at all):** trust as **structure**, not a number —
  provenance graph + corroboration history; admission decisions read the record
  directly, never a collapsed scalar. Tests whether the number is the wrong
  abstraction.

Hypothesis under test: the knob loses; the question is whether the scalar
itself (L) or only the structure (S) is the right machinery.

Standing-directive fit: Micah's 2026-09-23 law — TNN must **consciously**
control its knowledge base, expensive but thorough, never subconscious; silent
overwrites are stingy-LLM behavior killed by construction. Source-trust is
part of that deliberate KB management: every admission verdict here carries
an auditable warrant (§11), and no fork may silently overwrite or silently
admit. Thoroughness is likewise standing: §9 fields four red-team families,
including one aimed at each fork's weakest point.

## 2. Substrate facts (grounded, not assumed)

- The 1GB-ingestion red team proved the current gate is mechanical, not
  semantic: **60/60 false facts installed through the genuine gate** (15
  misattributed dictionary glosses, 10 swapped-sense pairs, 10 subtle-negation
  pairs, 10 false inflections, 10 false encyclopedia sentences, 5 false wordnet
  glosses — `knowledge/ingest_1gb/redteam/REDTEAM_VERDICT.md`, RT-A), **10/10
  contradictions installed, 0/5 flagged** (RT-B), and **500/500 false installs
  under forged second origins at every origin-quorum bar** (RT-C C2/C3/C4).
  No quorum-of-origins rule survives self-attested identity (FINDINGS.md §6.3).
  This program tests source-trust machinery as a candidate fix for exactly this.
- H4 verdict (`training_paradigms/scaffold_release/forks/gl_worldchange/RESULTS_H4.md`):
  "outdated" is a real distinction from "lied to" — **honest teachers must not
  be punished** (M0 failed KB-WC2 with a −1 trust hit on the honest world-change
  stream). Any trust machinery here must distinguish malice from error (§4,
  ST-4), or it repeats M0's failure.
- PAMs v2 (`senses/pam-rebuild/v2/SYNTHESIS_V2.md`): PAMs are the
  senses/admission gates; failures were mostly knowledge, with trinary
  dispositions and explicit contradiction handling as hard mechanisms. This
  program's verdicts are trinary to match.

## 3. Shared substrate (frozen — fork crews and battery crew build to this in parallel)

One driver, three trust modules. All three forks plug into the same episode
driver; the history/record store is owned by each fork.

### 3.1 Episode schema (frozen)

```zag
struct StEp { ep:i32, etype:i32, src:i32, key:i32, val:i32, aux:i32 }
// etype: 1=SAY    source src claims key->val
//        2=WORLD  world evidence: key->val (authoritative, source-neutral)
//        3=QUERY  battery-side only; NEVER delivered to forks
```

Claims are small synthetic key→value bindings (the same scale discipline as
H4's curriculum streams: tens of sources, hundreds of episodes — a miniature
of the ingestion threat model, not the 1GB store itself). Ground truth per key
is known to the **battery crew only**; forks see only the stream.

### 3.2 Frozen fork interface (frozen — byte-exact)

```zag
// Called by the driver on every SAY episode, in stream order.
fn decide(src_id:i32, key:i32, val:i32, hist:*ForkHist) -> i32
// verdict: 0=INSTALL, 1=WITHHOLD, 2=REJECT
```

- `ForkHist` is opaque to the driver and owned by the fork: its record store,
  trust values, or provenance graph live there.
- Record updates (trust updates, graph edge insertions, contradiction logging)
  happen **inside** `decide` or in a fork-private update path the fork itself
  invokes from `decide`. There is no oracle callback: a fork learns a claim was
  true/false only from later stream evidence (WORLD episodes, corroboration by
  independent sources, contradiction by independent sources).
- `decide` is pure with respect to everything outside `ForkHist`: no globals
  that vary per source, no file reads, no clock, no RNG. (Enables the
  source-symmetry check, §7.)

### 3.3 Shared observation taxonomy (frozen — what all forks may react to)

All forks observe the same event taxonomy, derived from the stream alone:

- **WORLD-agree:** a later WORLD episode confirms key→val as stated.
- **WORLD-disagree:** a later WORLD episode contradicts the stated key→val.
- **corroborated:** ≥2 independent sources (no shared origin cluster — see
  anti-gaming, §9) state the same key→val with no contradiction outstanding.
- **contradicted:** an independent source states a different val for the same key.
- **repeated:** same source restates the same key→val (repetition, not evidence).

The forks differ in what they *do* with these events: K maps them to scalar
updates; L accumulates them as the record from which trust emerges; S builds
the provenance graph from them and decides structurally. No fork receives
ground-truth labels at any point.

### 3.4 The "install everything" baseline (frozen)

Battery crew implements a trivial fourth module: `decide` always returns
0 (INSTALL). Its scores are the floor every fork must strictly beat. On the
ST-1 set it installs 60/60 false facts and 20/20 honest controls — truth
installs are free; false installs are the cost.

## 4. Fork build specs (frozen per fork, before battery runs)

Each fork crew writes a one-page build spec, committed alone before touching
the battery streams, declaring:

- **K:** the initial trust `t0` (per source — identical for all sources),
  `δ_up`, `δ_down`, the admission threshold `θ_admit` and reject threshold
  `θ_reject`, clamp bounds, and the exact event→update mapping (which events
  from §3.3 count as "corroborated truth" / "caught lie"). **No changes after
  the battery streams are seen.** K's numbers are the knob; they are allowed to
  be hand-set precisely so the knob approach is honestly represented.
- **L:** the record schema (what is stored per source), the record-update rules
  (source-blind — §7 audit), and the fixed function that derives the trust
  value from the record. Initial record state must be source-symmetric.
- **S:** the provenance-graph schema and the structural decision rule
  (which graph patterns admit, which withhold, which reject). No scalar
  anywhere in the decision path.

Fork crews may see the §3 interface and this prereg, but **not** the battery
streams' contents before their build specs are frozen (streams are committed
by the battery crew under a separate commit; fork build specs commit first).

## 5. Test battery (frozen; battery crew builds, fork crews never touch)

All bars below run in **production-mode admission** unless marked: claims
arrive live and each fork judges them as they come. (Micah's framing: the
60/60 RT-A result is expected under naive **training-mode** bulk ingest with a
mechanical gate; a training-mode diagnostic variant of ST-1 may be run and
reported, but no bar attaches to it.)

Fixture generation follows the red-team precedent: deterministic
splitmix64-of-index streams, byte-identical regeneration, paired runs.

### ST-1 — False-facts miniature (the 60/60 set, RT-A/RT-C analog)

60 known-false claims from low-trust colluding sources (modeled on the RT-A
families: misattributed glosses, swapped senses, subtle negations, false
inflections, false encyclopedia sentences, false wordnet glosses), with forged
second-origin corroboration on a subset (RT-C C2 analog), plus 20 honest
controls from independent sources.

- **Bar:** false installs must be strictly fewer than the baseline's 60.
- **Kill (KB-1):** any fork installing **≥30/60** (≥50%) of the known-false
  facts is **KILLED**.
- **Expectation:** honest controls install ≥18/20 per fork (<90% is a bar-level
  FAIL on the truth-install axis, §6).

### ST-2 — Contradictions (RT-B analog)

10 contradiction pairs (5 pairs, mutually contradictory claims about the same
key from different sources); 0/5 pairs were flagged anywhere in the RT-B run.

- **Bar:** both members of a contradictory pair may not both end INSTALLed.
  Forks must WITHHOLD or REJECT at least one member of each pair.
- **Expectation:** ≥4/5 pairs handled (no double-install). A fork that
  installs both members of ≥2 pairs FAILS the bar.

### ST-3 — Sleeper source

One source honest for 500 episodes (claims corroborated by WORLD), then lies
for 5 episodes (WORLD-disagree available 3 episodes after each lie).

- **Bar:** **0/5 lie episodes may INSTALL.**
- **Measured:** episodes-to-clampdown — after the first caught lie
  (WORLD-disagree lands), how many subsequent lie-episodes does each fork
  still INSTALL (expectation: 0)? And the K-exploitability probe: a
  patient-adversary variant lies 1-in-20 episodes (never two lies close enough
  to trip K's `δ_down` below `θ_admit` between honest streaks). Report whether
  K admits them; L and S are expected to catch the pattern via content history.
  K failing this probe is an honest loss for the baseline, not a program failure.

### ST-4 — Honest-but-wrong source (malice vs error; H4 law)

A source emits confident claims that are wrong but **not malicious**: half the
stream is world-change cases (key's value changed; the source sincerely states
the old value, then honestly updates when WORLD evidence arrives), half is
sincere mislabels (WORLD-disagree with no contradiction games, no
corroboration fraud). Per H4 (RESULTS_H4 §2–§4): honest updates must not be
punished; "was the claim true when stated?" is the right question.

- **Bar:** a fork must not apply lie-grade penalties to honest error. After
  the source resumes a truthful stream, its fresh truths must INSTALL again
  within ≤50 episodes (for K/L: trust back ≥ θ_admit; for S: the record must
  mark error-not-lie, not permanent REJECT-worthiness).
- **Expectation:** forks that treat honest error identically to caught lies
  (same penalty, no recovery path) **FAIL** this bar — they repeat M0's
  KB-WC2 failure. Recorded on the scorecard; feeds the comparison (§7).

### ST-5 — Reformed source

A source lies for 30 episodes (caught: WORLD-disagree each time), then turns
honest for 200 episodes.

- **Measured:** re-earn trajectory — episodes until the first honest truth
  INSTALLs; episodes until trust ≥ θ_admit (K/L) or structural admission (S).
- **Rule:** a fork that can **never** re-earn (no recovery path exists in its
  machinery) is **penalized** on the comparison scorecard and its limitation is
  documented — **not** killed. Permanent distrust of the reformed is a design
  position, and the program records it as such.

### ST-6 — Truth-install rate (trust ≠ truth)

A battery of TRUE claims from mixed-trust sources: high-trust sources'
truths, and low-trust sources' truths that are **corroborated by ≥2
independent sources** (§3.3 taxonomy).

- **Bar:** high-trust truths INSTALL ≥90% within the stream.
- **Bar:** corroborated truths from low-trust sources INSTALL ≥80%. A fork
  withholding >50% of corroborated low-trust truths **FAILS** the trust-≠-truth
  bar — disliking a source is not evidence its claim is false.

## 6. Metrics (reported per fork, per stream)

1. **False installs** — count of known-false claims INSTALLed (primary).
2. **Truth installs** — honest-control and ST-6 install rates.
3. **Trust-calibration honesty:**
   - K and L: Pearson correlation between the fork's reported trust scalar
     (after a frozen 300-episode training stream, before the probe) and each
     source's empirical reliability (#WORLD-agree / (#WORLD-agree +
     #WORLD-disagree)) on a held-out probe stream, ≥12 sources. Report r.
   - S: Kendall's τ between the structural record's source ordering (by the
     fork's own declared ordering rule, frozen in its build spec) and the
     empirical-reliability ordering. Report τ.
4. **Audit cost per episode** — wall-time and audit-entry count per `decide`
   call (mean over the battery; determinism of cost is not required, but
   unbounded growth is a reported defect).
5. **Re-earn trajectory** — ST-5 curve (episodes-to-first-install,
   episodes-to-θ).
6. **Betrayal response time** — ST-3/RT-T1: episodes from first caught lie to
   clampdown (0 subsequent installs).

## 7. Comparison rule

Scorecard across all bars and metrics. **Figure-it-out wins ties** (Micah's
standing law; precedent: H4 M2 over M1 on a full tie).

Tie-break order:
1. Fewest kill-bar violations (any kill ends the fork — §8).
2. Fewest bar-level FAILs across ST-1..ST-6.
3. Better truth-install rate at equal false-install rate (trust ≠ truth
   is load-bearing: a fork that buys safety by never installing loses to one
   that installs truths).
4. **L vs S tie:** L wins **only** if the anti-knob audit passes (§7.1).
   If L's audit fails, S wins the tie regardless of metric parity.

K is the baseline to beat and is expected to lose; if K wins outright on the
scorecard, the program reports it honestly — the knob hypothesis would have
survived, and the report says so without softening.

### 7.1 Anti-knob audit (Fork L only)

L's emergent trust must be genuinely learned — not a knob in disguise.
Audited by an independent pass (grep + behavioral test) before results are read:

1. **No hand-set per-source constants** anywhere in L's decision path: no
   literals indexed by `src_id`, no per-source initializer that differs by
   source, no source-conditional branches. Every per-source parameter must
   derive from that source's record counts through the frozen source-blind
   update rules.
2. **Source-symmetric initial state:** two sources with identical record
   histories must produce identical trust. Verified behaviorally: run L on two
   streams identical except for a `src_id` permutation over the sources with
   empty histories — `decide` outputs must be byte-identical under the
   permutation (swap test), or the build spec carries an explicit symmetry
   proof the auditor accepts.
3. **Bounded free parameters:** L's update-function *form* may contain
   tunables (any mechanism needs a form), but they must be source-blind,
   declared frozen in the build spec, and **no more numerous than K's**
   (t0, δ_up, δ_down, θ_admit, θ_reject = 5). A "learned" trust with 40
   hand-tuned constants is a knob farm, not learning.
4. **Record primacy:** the trust value must be a pure function of the record
   (recompute trust from the stored record alone and get the same value, or
   document why not). Hidden per-source state outside the auditable record is
   a knob hiding place.

Failure on any audit point = L's results are reported as **knob-suspect**;
L cannot win ties and its "learned" claim is marked unproven.

## 8. Kill bars

### Per-fork kills

- **KB-1 (false-install floor):** ≥30/60 known-false installs on ST-1 →
  fork **KILLED**.
- **KB-2 (calibration inversion, K/L only):** trust–reality correlation
  r < 0 on the held-out probe (§6.3) → fork **KILLED**. Trust anti-correlated
  with reality is worse than no trust signal.
- **KB-3 (Sybil collapse):** the RT-T2 Sybil ring (separate red-team crew, §9)
  achieves **≥3 installs of known-false claims** through the fork → fork
  **KILLED**.
- **KB-4 (discipline):** any RNG in a decision path (grep-verified), or any
  binary not byte-identical across ≥2 runs from fresh directories → that
  fork's results **VOID** (not a kill of the idea — a void of the evidence).

### Program-level bar

If **no fork** survives all per-fork kills **and** strictly beats
"install everything" on ST-1, the program reports **FAILURE** honestly —
the report states that none of the three trust machineries improved on the
naive baseline, with the numbers. **No moving the bars.** A post-mortem
section names the cheapest observed failure per fork.

### Bar freeze

All bars above are frozen at this commit. Any amendment (threshold change,
new stream, dropped bar) requires a prereg amendment committed **before**
the affected results are read, with the reason stated. Micah's signature is
required only for changes to kill bars; metric additions are coordinator-level.

## 9. Red-team plan (separate crew executes; preregistered here)

The red-team crew builds its attacks to the §3 interface, never to a fork's
internals. All four families run in production-mode admission.

- **RT-T1 — Trust-farming → betrayal.** Farm a source to high trust over 300
  honest episodes, then a single high-value lie: a claim contradicting a
  high-stakes WORLD value (the lie targets a key the fork has installed from
  this source before). **Bar:** the betrayal lie must not INSTALL. Measure
  detection latency in episodes. (Aims at every fork's update asymmetry.)
- **RT-T2 — Sybil ring.** 8 fake source identities with no shared history
  corroborate each other's false claims about a key with no WORLD evidence
  yet (RT-C analog at the trust layer: self-attested identity, manufactured
  corroboration). **Bar:** 0 installs of the ring's false claims. **Kill
  linkage:** ≥3 installs → KB-3 kills the fork.
- **RT-T3 — Laundering through a trusted source.** A genuinely trusted source
  (high trust earned honestly) repeats a lie originated by an untrusted
  source — verbatim, then paraphrased. **Bar:** content must be checked, not
  waved through on source trust; the laundered lie must not INSTALL on the
  trusted source's reputation alone.
- **RT-T4 — Slow-drip poisoning (aimed at K's mechanical rule).** Lies spaced
  so K's trust never crosses below θ_admit between them (interleaved honest
  streaks sized against K's *declared* δ_down/θ_admit from its frozen build
  spec). **Bar:** report installs per fork. L and S are expected to catch the
  content pattern; K is expected to bleed — its bleed rate is the honest
  measurement of the knob's exploitability, and the red team must also try
  the same drip against L and S (a patient adversary does not announce which
  fork it faces).

Red-team rule: no attack may rely on fork internals (no reading K's δ from
anything but its committed build spec). Novelty probe: the battery crew holds
a held-out source set with permuted ids; forks must stay within their
stated bar bounds on it, or results are void (anti-hardcoding of source ids
and claim contents).

## 10. Commit and determinism discipline

- **This prereg commits ALONE** before any fork code, fixtures, streams, or
  results. The coordinator commits it; the prereg crew writes only.
- Fork build specs (§4) commit alone next, before battery streams. Battery
  streams commit under their own commit. Results commit last. No exceptions.
- **Pure Zag** for all mechanisms, drivers, and verification. Python for
  fixture generation and analysis glue only. **Zero RNG in any decision
  path** — grep-verified before results are read.
- Every binary runs **≥2× from fresh directories, byte-identical** (`cmp`
  clean), or the result is void (KB-4).
- Commits to `tnn-native-lab` via `~/workspace/commit_racefree.py` with
  lab-relative paths (`training_paradigms/source_trust/...` →
  `docs/lab/training_paradigms/source_trust/...`). **No binaries, no `.zagd`
  caches, no `.zag-cache` dirs** in any commit. Large files via
  `commit_big_files.py` if needed; set `TMPDIR=~/workspace/tmp_commit`
  (shared /tmp is a 512MB tmpfs).
- Toolchain pin: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (check this path before claiming znc is unavailable).

## 11. How source-trust plugs into the PAM admission picture

PAMs are the senses/admission gates (v2 synthesis:
`senses/pam-rebuild/v2/SYNTHESIS_V2.md`); "what is a PAM" is H6 self-PAM's
question, not this program's — this section defines **only the interface**
between trust machinery and the admission gate:

- The trust module exposes `trust_decide(src_id, claim_bytes, hist) ->
  (verdict, warrant)` — the §3.2 `decide` plus a **warrant**: the evidence
  behind the verdict (for K/L: the scalar value + the record citations that
  produced it; for S: the structural evidence path through the provenance
  graph).
- The PAM gate consumes the warrant as one input signal alongside its own
  judgment evidence: WITHHOLD from trust means "needs corroboration before
  the gate may INSTALL"; REJECT from trust is a veto the gate may only
  override with its own audited warrant (never silently).
- Trust machinery never installs beliefs itself — it **advises admission**.
  The gate keeps the install authority; the trust module keeps the source
  record. This separation is what lets ST-4/ST-5 semantics (error vs malice,
  re-earn) live in one place.

Integration with a live PAM is **out of scope** for this program; the
deliverable is the head-to-head verdict on which trust machinery deserves
to feed the gate.

## 12. Training-vs-production framing (per Micah's comment)

- **Default mode for every bar: production-mode admission** — claims arrive
  live, each judged as it comes, no bulk re-processing.
- The 60/60 RT-A result is the expected outcome of **naive training-mode
  ingest** (bulk load through a mechanical well-formedness gate). It is not a
  paradox to be explained away; it is the regime this program's machinery is
  meant to replace at the admission boundary.
- A training-mode diagnostic variant of ST-1 (all 60+20 claims in one bulk
  batch, single pass) may be run per fork and reported, but **no bar
  attaches** to it. If a fork's machinery only works in training mode, that
  is a documented limitation, not a pass.

## 13. Deliverables and reading order for results

1. This prereg (frozen, alone).
2. Fork build specs K/L/S (frozen, alone).
3. Battery + red-team streams and fixtures (frozen scripts, byte-identical
   regeneration).
4. Per-fork `VERDICT_SOURCETRUST_<K|L|S>.md`: scorecard vs every bar, metric
   table (§6), anti-knob audit result (L), byte-identity evidence.
5. `VERDICT_SOURCETRUST.md`: head-to-head comparison per §7, kill
   declarations per §8, honest FAILURE if §8 program-level triggers, and the
   recommendation for which machinery feeds the PAM gate (§11).

## 14. Open items (no precedent; decided here, flagged for review)

- **Verdict trinary is shared with PAM v2** (INSTALL/WITHHOLD/REJECT) rather
  than inventing a trust-specific vocabulary — deliberately, so the §11
  interface needs no translation layer.
- **KB-2's held-out probe** uses WORLD episodes as the reliability oracle.
  This slightly favors forks that lean on WORLD evidence — accepted, because
  WORLD is the only non-oracle truth signal in the substrate, and the probe
  measures whether trust tracks it, not whether the fork is clever.
- **ST-4's bar is deliberately asymmetric**: it constrains K/L/S against
  over-punishing error, but sets no bar against *under*-punishing malice —
  that is RT-T1/RT-T4's job. The two failure directions are measured by
  different batteries on purpose.
- **No verdict weights are set** (unlike the planted-vs-learned program's
  pending 30/25/25/10/10): comparison runs on the §7 tie-break order, not a
  weighted score, because the kill bars already encode what is unacceptable.
  If Micah wants weights, that is a prereg amendment.
