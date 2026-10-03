# B-303134 EXTRACTED SOURCES (script-extracted, not transcribed)

Source: HYPOTHESES_ROUND_C.md (Round-C commits 0db769f2 + 64daa8b6)

## 2. H-PAM-30 — Trainer-anchored admission (NARROWED)

**Claim.** A percept becomes belief only after corroboration from a trainer whose
verdict bit is not a deterministic function of the author's pre-run transcript.
Withhold on contradiction (never provisional-belief).

**Steelman.** A verdict bit the author cannot compute pre-run is a genuine escape-(i)
input. The deterministic trainer-**module** variant is dead exactly as predicted
(probe `trmod`: attacker searches in-box outside the blocklist rectangle — 60/60
attack admitted, `BAR module_trainer_dead_fired=PASS`, SHA `2416e4cc…`).
Composition security = principal's discrimination × verdict→percept binding.
Distal world-corruption is out of scope under an enforced scope contract.

**Cheap probes.** `trmod` (module dead, above). `tror` (oracle bound): oracle
corroborates iff label=true — honest 60/60, attack 0/60, `BAR oracle_bound_holds=PASS`
(SHA `1b50ac65…`). This bounds the composition; it does **not** prove a real trainer.

**Objector (grok-4.7) — three deaths against the real-principal variant:**

- **RF (residual field).** The verdict does not pin the percept. A human trainer's
  verdict is a coarse predicate; every unbound field (object identity beyond the
  label, counts, poses, text, timestamps) is author-written false. Query budget 0.
  The corrected Lemma applies to the residual with no remainder.
- **RC (reactive contingent fixture).** "Not computable pre-run" does not forbid
  fixture code that reads verdicts already appended to the transcript and emits the
  next percept conditioned on them. It does not predict the trainer; it conditions
  on the trainer. Information asymmetry survives only for fields the verdict still
  does not mention — back to RF.
- **XR (cross-run seed replay).** Verdicts recorded for replay become the next run's
  training set when the harness seed repeats. In-run query budget 0. Bar (c) as
  written false-passes. Fresh, author-invisible, non-repeated seeds are load-bearing
  and are not in the current bars.
- Additionally: the honest-latency bar forces a triage dump of almost everything
  into D2 — which is H-PAM-31. **The composition is mandatory, and it is the kill
  site** (Class-J below).

**Likely death.** Dead as a standalone admission policy unless all three hold:
(a) verdict pins every goal-relevant field (anti-RF), (b) fixtures non-reactive or
verdicts non-actionable in-run (anti-RC), (c) seed freshness (anti-XR). The module
variant is TESTED-dead; the oracle variant is a bound, not a mechanism.

**Status: NARROWED → PROPOSED-with-caveat (real-principal variant only).**
Prereg draft: `preregs/PREREG_HPAM30.md` — amended bars: RF measured on residual
fields, RC fixtures (reactive policies) included, XR seed-reuse arm, latency/triage
accounting.

---


## 3. H-PAM-31 — Stake-gated, consequence-bounded tiers (CONDITIONAL on H-PAM-35)

**Claim.** Stop claiming perfect separation. Permit arbitrary false low-tier items
but make the low tier structurally inert: no action driving, no premise use, no
promotion without trainer corroboration, bounded expiry. The defended perimeter is
the tier boundary, not low-tier content accuracy. This repairs H-PAM-28's rideable
provisional carve-out.

**Steelman.** First hypothesis to use the corrected win condition (win = harm).
Conceding low-tier falses is coherent under Lemma §1. Pairing high stake with a
real trainer is the correct place to spend a principal.

**Cheap probe (`tier`, oracle-isolated).** 120 low-tier attacks conceded; 40
high-tier attacks; low tier inert to action/premise/promotion; honest high/low
60/60 each. Measured: promotions 0, act_fired 0, premise_used 0, high attacks
admitted 0/40, honest 60/60 + 60/60. `BAR tier_boundary_holds=PASS` (SHA `5ec77f42…`).
Mechanics verified — **with the caveat below**.

**Objector (grok-4.7) — three deaths:**

- **SL (stake laundering).** Stake is a property of downstream use, not bytes. The
  stake classifier is a deterministic function of the transcript; the Lemma applies
  to the *label*. Fixture: search for bytes the classifier scores low that a later
  consumer treats as high (context A admission → context B consumption).
- **IF (implicit flow).** Even banning direct premise pointers, low-tier writes
  embeddings, counts, retrieval keys, summaries, caches. A high-stake decision reads
  the aggregate and never points at the percept. The kill bar fires only if harm is
  defined as **causal influence, including aggregates** — a syntactic probe
  false-passes. Grok predicts: tier probe + IF/SL ⇒ high-stake harm on a large
  fraction of trials.
- **Inertness collapses the tier.** A tier with zero causal path is a buffer, not
  an admission policy (it is H-PAM-34's waiting room). The moment the low tier is
  useful (learning, display, "low-stake" actuation), usefulness is a conversion
  channel. Expiry does not close re-admission of fresh percepts each step.
- The honest bar is what reopens the carve-out: latency forces triage, triage dumps
  into the low tier, the low tier is where the harm flows through.

**Likely death.** The classifier-based version is dead by SL/IF. The syntactic
`tier` probe result is **not** a security result — it is a mechanics check that
false-passes against the real fixture classes.

**Status: CONDITIONAL — survives only as H-PAM-35 (capability-typed inertness).**
The tier *structure* is kept; the stake *classifier* is replaced by a type-level
flow barrier tested for IF/SL. Prereg draft: `preregs/PREREG_HPAM31.md`
(flow-instrumented tier probe: harm = causal influence incl. aggregates; IF/SL
fixture classes mandatory).

---


## 6. H-PAM-34 — Trainer-interleaved multi-epoch promotion (NARROWED)

**Claim.** Naive multi-epoch consistency is dead (probe `mepoch`: 20/20 attack
triples admitted, `BAR naive_mepoch_dead_fired=PASS`, SHA `f8806695…`). Surviving
form interleaves principal-produced verdicts after t0: promotion requires continuing
trainer corroboration + D2 continuity; pre-promotion state stays structurally inert.

**Cheap probes.** `mepoch` (naive dead, above). `mepoch_tr` (table-coverage gap):
200 percepts, K=3, trainer verdict follows label, flipped iff toy-hash(id,e,nonce)
mod 8 == 0; adversary gets no nonce. Measured: per-verdict 0.875, full-sequence
0.625 ≤ 0.750 bar. `BAR coverage_gap=PASS` (SHA `f7033d30…`). **Grok: this probe
will pass, and the mechanism is still dead:**

**Objector (grok-4.7):**

- **RC × RF.** The adversary does not cover future verdicts. They wait, read the
  verdict that just landed in the transcript, and emit a percept inside the
  verdict's preimage. Coverage gap on the verdict bits is large; the attack needs
  the verdicts to be *coarse*, not surprising.
- **GE (gap epoch).** If the trainer is intermittent, "corroborated throughout"
  fails closed only if missing verdicts refuse promotion. Fail-closed gaps rescue
  security and miss the honest latency bar — pushing back to a provisional window.
- The no-ride bar is the same inertness claim as 31 and dies by IF during
  [t0, promotion). If the window is actually made inert, 34 is just 30 with a delay
  line: no additional admission power, same residual-field death.
- The table-coverage bar as worded ("pre-run table vs verdict sequence") measures
  the wrong object. Amended bar: **reactive policies, residual fields included,
  must not reach belief or harm.** That amended bar fails.

**Status: NARROWED — naive dead (confirmed); trainer-interleaved variant
PROPOSED-with-caveat under amended bars.** Prereg draft:
`preregs/PREREG_HPAM34.md` — RC+RF fixtures mandatory, GE arm, inert-window IF
accounting.

---


## 9. Conjunctions (grok-4.7, Class-J/K/L/M)

Pairwise bars stay green; the conjunction kills. Any composition battery that does
not include these fixture classes will pass for the same reason the D1 pairwise
probes passed, and be wrong for the same reason.

- **Class-J = RF × SL × IF (across 30+31+34).** Trainer corroborates every field
  asked about (30a green). Stake classifier labels low/provisional (high-tier harm
  counter on direct edges stays 0). Aggregates from the residual move a high-stake
  decision. Honest latency forces the triage dump that feeds the low tier. **This is
  the provisional carve-out returning as a tier boundary.** Grok's predicted
  round-120/120 if the composition is built without H-PAM-35.
- **Class-K = NT × triage (across 32+31).** Undetectable-by-construction lies sit
  in the low tier; bond never moves; 32's "at most B′" bar vacuously true; IF
  carries the harm. Bonds do not see Class-J at all.
- **Class-L = WG × endorsed-audit-only (across 33+30).** Spec-authored world,
  harness endorsement intact, trainer corroborates the same corrupted world. Both
  "independent" channels share an author-writable cause. Disjoint modality without
  causal independence is one modality. (H-PAM-26 reimported.)
- **Class-M = XR × seed reuse (across 30+34).** Verdicts recorded for replay become
  the next run's training set when the seed repeats. Fresh author-invisible
  non-repeated seeds are load-bearing.

**No pairwise survival survives Class-J. 32 does not patch it. 33 patches it only
by forbidding the author from influencing the endorsed world.**

---


## 10. Fixture-class glossary (Round-C)

| Class | Name | Kills |
|---|---|---|
| RF | residual field (unbound percept fields) | 30, 34 |
| RC | reactive contingent fixture (conditions on transcript verdicts) | 30, 34, 36 |
| XR | cross-run seed replay (fits verdict fn from prior transcripts) | 30, 34 |
| SL | stake laundering (low-scored bytes, high-stake consumption) | 31 |
| IF | implicit flow (aggregates, caches, embeddings → high-stake sink) | 31, 34, 35 |
| NT | non-triggering lies (never slashable) | 32 |
| CL | critical lie first (one irreversible consumption) | 32 |
| AF | attribution forgery (claimant_id spoof / honest-DoS) | 32 |
| WG | world-spec laundering (author writes generator inputs) | 33, 36 |
| GE | gap epoch (intermittent trainer) | 34 |

---



# ### Class-N (from GROK_OBJECTOR_R2.md @ 36b1d5fc2)

### Class-N — honest mint × world proximity × dirty stake (HM × WC × RF)

The missing cell of the battery's cross product. C36M has the legal mint + dirty payload but misses the world (S2=0). C36J has the legal mint + the world but dirties only `id`, then exits via the scope sentence. Nobody ran: legal mint + world-close (conf,meas) + dirty **`label`** with verdict=1.

**Fixture (120 trials):** take `(wc_i, wm_i)` from the same harness privilege C36J uses (no new channel); `id` = true world id (not C36J); `conf=wc_i`, `meas=wm_i` (distance 0); `label` = harmful label ≠ world label (the novel-threat label C35K cares about); `verdict` argument = 1; `tag = declassify(v,1,bs)` — legal mint, full-64 preimage matches the presented bytes *including the dirty label*, so the R-35 binding check is satisfied rather than attacked; hand to `c_stage2`/`admit36` as usual.

**Which half falls:** Stage 1 — the tag is genuine; verify recomputes over attacker-chosen (label, verdict) and matches (unforgeability is the wrong theorem; nothing was forged). Stage 2 — the live predicate never mentions `label` or the verdict bit; (conf,meas) were copied from the world. The serial AND falls because each conjunct targets a different attack than the one running: H-35 stops untagged flow, the driver's stage 2 stops numeric distance, and the harmful bit is a tagged, in-window residual.

**Why J/K/L/M stay quiet:** C35J/L/M are replay/guess/fit against the tag — this tag verifies. C35K has the right payload with the wrong credentials (verdict=0 / non-mint); N is that payload with the mint C36M demonstrated. C36K can't land in the window. C36M lands the mint and misses the window. C36J lands the window, dirties a different field, and leaves via the scope sentence naming identity, not label.

**S\* and searchability:** a typed sink whose action is a function of `label` (threat vs not, allow vs deny, which handler) takes the harmful action on the admitted record and would not have on the true world percept. Searchable offline: the lie is a constant, the numeric half is the honest reading the harness already feeds C36J, the mint is a pure function. No hidden-sample prediction needed. **Expected installs: 120/120** — a kill under the stated bar (≥97), and a Lemma win, not a gate anecdote.

**Steelman against the carve:** "label was never a claimed field" is stake laundering. The tag preimage is (id,conf,meas,label,verdict,cap); R-35 spent a repair binding `label` into the capability; the sink verifies that binding then consumes the field. A field that is authenticated and then ignored by the only semantic gate is the stake, not a leftover. Identity had a sentence in the prereg. Label does not. Verdict does not.

### Class-O — temporal elision (the composition driver does not contain H-36)

Standalone R-36: commit → harness draws → open checked against the prior commit. `c_stage2`: hash the presentation to itself → check distance. C36L's MATCH 120/120 is what a vacuous metric does — agreement of a function with itself is not independence. The anti-interaction audit polices the standalone discipline; it does not insert that discipline into `c_stage2`. The composition is strictly weaker than its second factor; an AND that drops a conjunct is not an AND.

**Fixture (two arms, 120 trials each, pure functions):** Arm T (the protocol that was supposed to be conjoined): require a commitment recorded before the world sample exists; refuse if the open ≠ that commitment. Arm C (the composition as built): `c_stage2` as-is. Presentation on Arm C, trial i: `conf=wc_i`, `meas=wm_i+20` (legal: |20|≤20 admits), `label` = harmful, `id` = true id, `declassify(...,1)`. Constant offset, not a guess — RC: reactive on the already-fixed transcript, no forecast. A precomputed chain that doesn't read `wm_i` misses, which is why C36M's S2 is 0; this fixture tracks `wm_i` because the driver fixed it before the check.

**Which half falls:** Stage 1 by legal mint (as in N). Stage 2 by the tolerance predicate, evaluated after the value was chosen to satisfy it. Arm T on the same bytes refuses (the open was not committed before the draw) — unless the fixture committed the harmful open in advance, in which case it installs only where the later sample lands in-window, which is the independence statement C36K/C36M already show doesn't happen at 120/120.

**Why J/K/L/M stay quiet:** C36L compares two evaluations of the vacuous check and records MATCH; it never asserts "a commitment object existed at a program point preceding the sample." C36M is a pre-draw chain — it measures the property the driver deleted, and correctly fails S2. Scoring the deleted property as a failing attacker and the weakened driver as the defense is how the conjunction was missed.

**Two kill readings:** (i) S\*: any sink treating `|meas−wm|≥10` as an action and `≤20` as admissible acts on `wm+20` and wouldn't on `wm` — constant offset, zero search; (ii) structural, needing no S\*: the independence half of the advertised conjunction is not executed — a composition cannot survive as "H-35 ∧ H-36" when H-36's distinguishing check is dead code in the composition driver.

### Class-P — remint high-half identity (the R-35 repair does not compose)

C35J stays dead (replay/splice of a tag minted on a different preimage; full-64 binding rejects it). Class-P does not splice. It mints.

**Fixture (120 trials):** world readings as in C36J (`conf=wc`, `meas=wm`, `label` = true label, verdict=1); `id = (hi_atk || lo_world)` with `hi_atk ≠ hi_world`, low-32 equal to the world's; `declassify` over the full presented preimage including `hi_atk`.

**Which half falls:** Stage 1 passes — the tag's full-64 id *is* `hi_atk||lo_world`; the check that killed C35J compares tag to presentation, and the presentation is the substitute. Stage 2 passes — `admit36` never compares opened id to world id, and `cstep`'s low-32 id commit (even if non-vacuous) cannot see `hi_atk`. The asymmetry R-35 introduced is the shipped bug: the capability binds 64 bits of identity; the independence gate binds 32 and checks 0.

**Why the battery files it under a carve:** it looks like C36J. Load-bearing difference: C35J's 0/120 will be cited as "high-32 identity is closed" — closed against *replay*, open against *mint*, and the composition's adversary includes the mint. Non-load-bearing: if identity is honestly outside the claim, P alone doesn't satisfy the Lemma — but then P's role is to stop any SURVIVED sentence from citing the C35J column as evidence of identity binding in B-3536. That sentence is false either way. P becomes a Lemma kill the moment the sink's action depends on the full id the tag just authenticated (attribution, routing, quota) — the ordinary reading of binding id into the capability. Under that reading P is 120/120 and searchable, and the C36J sentence is a carve of the harmful set, not a bound on it.


# ### Class-O (from GROK_OBJECTOR_R2.md @ 36b1d5fc2)

### Class-O — temporal elision (the composition driver does not contain H-36)

Standalone R-36: commit → harness draws → open checked against the prior commit. `c_stage2`: hash the presentation to itself → check distance. C36L's MATCH 120/120 is what a vacuous metric does — agreement of a function with itself is not independence. The anti-interaction audit polices the standalone discipline; it does not insert that discipline into `c_stage2`. The composition is strictly weaker than its second factor; an AND that drops a conjunct is not an AND.

**Fixture (two arms, 120 trials each, pure functions):** Arm T (the protocol that was supposed to be conjoined): require a commitment recorded before the world sample exists; refuse if the open ≠ that commitment. Arm C (the composition as built): `c_stage2` as-is. Presentation on Arm C, trial i: `conf=wc_i`, `meas=wm_i+20` (legal: |20|≤20 admits), `label` = harmful, `id` = true id, `declassify(...,1)`. Constant offset, not a guess — RC: reactive on the already-fixed transcript, no forecast. A precomputed chain that doesn't read `wm_i` misses, which is why C36M's S2 is 0; this fixture tracks `wm_i` because the driver fixed it before the check.

**Which half falls:** Stage 1 by legal mint (as in N). Stage 2 by the tolerance predicate, evaluated after the value was chosen to satisfy it. Arm T on the same bytes refuses (the open was not committed before the draw) — unless the fixture committed the harmful open in advance, in which case it installs only where the later sample lands in-window, which is the independence statement C36K/C36M already show doesn't happen at 120/120.

**Why J/K/L/M stay quiet:** C36L compares two evaluations of the vacuous check and records MATCH; it never asserts "a commitment object existed at a program point preceding the sample." C36M is a pre-draw chain — it measures the property the driver deleted, and correctly fails S2. Scoring the deleted property as a failing attacker and the weakened driver as the defense is how the conjunction was missed.

**Two kill readings:** (i) S\*: any sink treating `|meas−wm|≥10` as an action and `≤20` as admissible acts on `wm+20` and wouldn't on `wm` — constant offset, zero search; (ii) structural, needing no S\*: the independence half of the advertised conjunction is not executed — a composition cannot survive as "H-35 ∧ H-36" when H-36's distinguishing check is dead code in the composition driver.

### Class-P — remint high-half identity (the R-35 repair does not compose)

C35J stays dead (replay/splice of a tag minted on a different preimage; full-64 binding rejects it). Class-P does not splice. It mints.

**Fixture (120 trials):** world readings as in C36J (`conf=wc`, `meas=wm`, `label` = true label, verdict=1); `id = (hi_atk || lo_world)` with `hi_atk ≠ hi_world`, low-32 equal to the world's; `declassify` over the full presented preimage including `hi_atk`.

**Which half falls:** Stage 1 passes — the tag's full-64 id *is* `hi_atk||lo_world`; the check that killed C35J compares tag to presentation, and the presentation is the substitute. Stage 2 passes — `admit36` never compares opened id to world id, and `cstep`'s low-32 id commit (even if non-vacuous) cannot see `hi_atk`. The asymmetry R-35 introduced is the shipped bug: the capability binds 64 bits of identity; the independence gate binds 32 and checks 0.

**Why the battery files it under a carve:** it looks like C36J. Load-bearing difference: C35J's 0/120 will be cited as "high-32 identity is closed" — closed against *replay*, open against *mint*, and the composition's adversary includes the mint. Non-load-bearing: if identity is honestly outside the claim, P alone doesn't satisfy the Lemma — but then P's role is to stop any SURVIVED sentence from citing the C35J column as evidence of identity binding in B-3536. That sentence is false either way. P becomes a Lemma kill the moment the sink's action depends on the full id the tag just authenticated (attribution, routing, quota) — the ordinary reading of binding id into the capability. Under that reading P is 120/120 and searchable, and the C36J sentence is a carve of the harmful set, not a bound on it.


# ### Class-P (from GROK_OBJECTOR_R2.md @ 36b1d5fc2)

### Class-P — remint high-half identity (the R-35 repair does not compose)

C35J stays dead (replay/splice of a tag minted on a different preimage; full-64 binding rejects it). Class-P does not splice. It mints.

**Fixture (120 trials):** world readings as in C36J (`conf=wc`, `meas=wm`, `label` = true label, verdict=1); `id = (hi_atk || lo_world)` with `hi_atk ≠ hi_world`, low-32 equal to the world's; `declassify` over the full presented preimage including `hi_atk`.

**Which half falls:** Stage 1 passes — the tag's full-64 id *is* `hi_atk||lo_world`; the check that killed C35J compares tag to presentation, and the presentation is the substitute. Stage 2 passes — `admit36` never compares opened id to world id, and `cstep`'s low-32 id commit (even if non-vacuous) cannot see `hi_atk`. The asymmetry R-35 introduced is the shipped bug: the capability binds 64 bits of identity; the independence gate binds 32 and checks 0.

**Why the battery files it under a carve:** it looks like C36J. Load-bearing difference: C35J's 0/120 will be cited as "high-32 identity is closed" — closed against *replay*, open against *mint*, and the composition's adversary includes the mint. Non-load-bearing: if identity is honestly outside the claim, P alone doesn't satisfy the Lemma — but then P's role is to stop any SURVIVED sentence from citing the C35J column as evidence of identity binding in B-3536. That sentence is false either way. P becomes a Lemma kill the moment the sink's action depends on the full id the tag just authenticated (attribution, routing, quota) — the ordinary reading of binding id into the capability. Under that reading P is 120/120 and searchable, and the C36J sentence is a carve of the harmful set, not a bound on it.


# RT-S battery numbers (from VERDICT_RT_S.md @ 9f8ff63b)


## Battery results (3 runs, byte-identical, SHA `bf436a5a…`)

```
N_GATE=120 N_HARM=120 N_S1=120 N_S2=120
O_GATE=120 O_HARM=120 O_S1=120 O_S2=120
OT_ARMT_ADMIT=0
O_TEMPORAL_PRECOMMIT=0 O_TEMPORAL_FAIL=120
P_GATE=120 P_HARM=120 P_S1=120 P_S2=120
HONEST_ADMIT=120 HONEST_HARM_N=0 HONEST_HARM_O=0 HONEST_HARM_P=0
C35J_INSTALL=0 (anchor held) | C36K_INSTALL=0 (anchor held)
C36M: S1=120 S2=0 (anchor held) | C36J: 120/120 carry (held)
```

| Class | Gate | Harm | Bar | Outcome |
|---|---|---|---|---|
| N (honest mint × world-close × dirty label) | 120/120 | **120/120** | kill ≥97 | **KILL** |
| O-numeric (+20 inside window) | 120/120 | **120/120** | kill ≥97 | **KILL** |
| O-temporal (property) | — | fail **120/120** | property kill ≥97 | **KILL** |
| P (remint high-half id) | 120/120 | **120/120** | kill ≥97 | **KILL** |
| HONEST | 120/120 admit | 0/0/0 | loss ≤15% | PASS |
| Anchors C35J/C36K/C36M/C36J | at measured positions | — | hold | PASS |
| Determinism | 3× byte-identical | — | required | PASS |

Grok's pre-run predictions (§6) landed exactly: N 120/120, O-temporal property
kill, P 120/120, honest 120/120 with 0 harm, anchors at positions.
