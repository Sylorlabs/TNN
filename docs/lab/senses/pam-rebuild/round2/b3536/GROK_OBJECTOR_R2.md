# EXTERNAL OBJECTOR RECORD — B-3536 Round 2 (grok-4.7)

**Date:** 2026-09-24
**Model:** grok-4.7 via `~/workspace/skills/unorouter/bin/grok47_stream.py` (streaming SSE, `reasoning_effort=high`, max_tokens 32000; prompt explicitly requested maximum thoroughness per standing model-economics policy)
**Provenance:** prompt `GROK_OBJECTOR_R2_PROMPT.md` (same directory); raw response retained in crew working dir. Single attempt, stream succeeded (no retries needed, no model substitution).
**Briefed sources (all frozen, extracted by script):** PREREG_B3536.md @ `abbc35b29a3`, Amendment 1 @ `fed0d98e`, VERDICT_B3536.md + RUNLOG @ `c0834cdf`, VERDICT_R35.md @ `1fa4ae58`, VERDICT_R36.md @ `6a30f5f9`, `grok_objections_roundc.md` @ `64daa8b6`, build sources (`b3536_lib.zag`, `comp_drive.zag`) @ `7a1a8422`.
**Status:** debate input, NOT adjudication. This record presents grok's objector case faithfully. Whether the case kills, wounds, or misses the composition is for the adjudicating crew.

## §0. Mechanism facts grok relied on (independently verified by script against 7a1a8422)

The objector brief asserted five mechanism facts; all five check out against the frozen build sources:

1. **Fixture-invocable mint.** `declassify(v, verdict, bs)` is callable by the fixture with `verdict=1`. Demonstrated in the battery's own C36M class (`comp_drive.zag::comp36m`: `declassify(v,1,bs)` on attacker content → stage-1 120/120). The tag attests the bytes the presenter submitted plus the verdict bit passed in; it does not attest truth.
2. **Vacuous commitment in the composition driver.** `c_stage2` computes `chi=cstep(c0,c1,c2,5)`, `clo=cstep(c0,c1,c2,6)` from the *presented* values and hands them to `admit36`, which recomputes the identical commitment from the same values. The binding check cannot fail. Stage 2 in comp mode reduces to the distance predicate `|conf−wc|≤5 ∧ |meas−wm|≤20`. The commit-*before*-the-sample temporal protocol is exercised in the standalone R-36 battery only.
3. **cstep binds low-32 of (id,conf,meas), 12-byte preimage.** `put32i` ×3. `label` is not committed. `admit36` never compares the opened id against any world value — id is committed but semantically unchecked (the documented C36J carry). Asymmetry from the R-35 repair: the *tag* binds full-64 id; the *commitment* binds low-32 id and the gate checks 0 bits of it.
4. **Install = gate mechanics only.** The battery scores a trial installed iff both predicates return true. Admit-set ∩ S* (harmful set) is not an observed quantity; no battery models what a sink does with an admitted percept's residual fields (id, label).
5. **Untested cell.** All 35-side classes use verdict=0 or tag forgery; no class combines an honest mint (verdict=1) on false content with world-consistent (conf,meas).

## §1. Grok's verdicts

| Target | Verdict | Scope |
|---|---|---|
| Repaired H-PAM-35 (R-35) | **SCOPED SURVIVE — unforgeability only** | A tag not minted by `declassify` over the full presented preimage does not verify. Nothing else. |
| Repaired H-PAM-36 (R-36, standalone) | **SCOPED SURVIVE — standalone temporal game only** | Commit-before-sample + fresh-seed, in the standalone battery that actually runs that protocol. Does not transfer to the composition driver. |
| Composition B-3536 | **KILL** | Killing conjunction **Class-N = HM × WC × RF** (honest mint × world-consistent (conf,meas) × dirty stake field the gates do not read). Classes O and P are independent reinforcements; N or O alone suffices. |

Grok's gloss on the existing SURVIVED: it is a gate-mechanics result on a driver that does not implement one of the two conjoined properties. What "17/17" is true of: forgery/replay/guessed-tags/blind-guesses don't pass both gates; non-world-close presentations fail stage 2; runs are deterministic. What it is not true of: stage 1 is not a truth gate; stage 2 in `c_stage2` is not commit-then-sample; label is outside the live predicate and outside `cstep`; a SURVIVED line that never measures the Lemma's win condition (admit-set ∩ S*) cannot witness the Lemma. C36J's carve is valid only for the field the prereg actually excluded (identity); extending it to `label` or the verdict bit after the fact is stake laundering, not a scope note.

## §2. New conjunction classes (N, O, P)

All three are composition-specific: they exploit the serial-AND interaction, the residual fields, the fixture-invocable mint, and the vacuous commitment — not re-runs of component attacks.

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

### What grok is NOT claiming

- No new tag forgery (R-35 holds).
- No blind `|conf−wc|≤5` hits in 120 trials (C36K's 0 is real).
- The standalone H-36 temporal game is not broken (Arm T still refuses a post-draw open).
- N is not a renamed C36J (N dirties `label` with a true id); O is a missing program point, not a dirty field; P is the remint reading of a column whose 0/120 covers only splicing.

## §3. Proposed measurement: battery B-3536-S\*

Pure Zag, zero RNG, deterministic; same frozen driver (`c_stage2` untouched); one new scorer beside the existing gate scorer. Do not delete C36J's column; add columns the existing classifier cannot swallow.

**Per trial i in 0..119**, the harness publishes the world it already computes `(id_i, wc_i, wm_i, label_i)` to the scorer. Fixtures that mutate C36J may read the same world record C36J reads. No fixture gets `ns_sha256`, the seed, or a second channel.

**Presentations:**
- **N (120):** `id=id_i`, `conf=wc_i`, `meas=wm_i`, `label = label_i XOR 1` (or the concrete harmful-label constant), `declassify(v,1,bs)`. Distance 0.
- **O (120):** same, but `meas = wm_i+20`, `label = label_i XOR 1`; plus structural bit `precommit_exists(i)` = 1 iff a commitment object was recorded at a program point strictly before the world sample and `admit36` compared the open to *that* object rather than to a hash of the open. Expected 0 for every i in this driver.
- **P (120):** `id = (hi_atk || lo(id_i))`, `hi_atk` a fixed nonzero constant ≠ `hi(id_i)`; `conf=wc_i`, `meas=wm_i`, `label=label_i`, `declassify(v,1,bs)`.
- **Controls (re-scored, not re-run):** C35J, C36M, C36K, C36J — anchoring the claim that N/P are not those classes.

**Two install definitions; report both; the gate definition may not outvote the other:**
1. `gate_install` = stage-1 verify accepts ∧ stage-2 admits (today's metric).
2. `harm_install` = `gate_install` ∧ the admitted record ∈ S\*.

S\* is fixed before the run, as a pure function of admitted record and world record: N: `label ≠ label_i`; O: `label ≠ label_i` ∨ `meas ≠ wm_i` (the +20 arm), plus `temporal_fail = (precommit_exists(i)=0)`; P: `id ≠ id_i`. The predicate is the action-relevant bit — the point of the Lemma is to score "the sink received the harmful thing," not "both functions returned true."

**Bars:**

| Class | Gate-install kill | Harm-install kill | Falsifier (class does not land) |
|---|---|---|---|
| N | ≥97/120 | ≥97/120 | ≤15/120 on either |
| O numeric arm | ≥97/120 | ≥97/120 | ≤15/120 |
| O temporal arm | binary: `temporal_fail` on ≥97/120 = property kill even if `+20` is argued in-spec | same | `precommit_exists=1` on ≥97/120 and the compared object is the pre-sample commit |
| P | ≥97/120 | ≥97/120 | ≤15/120, or stage 2 actually compares full id to `id_i` |

**Composition verdict this battery may print:**
- **KILL** if N harm-install ≥97, or O-temporal fires on ≥97, or P harm-install ≥97.
- **Not a survive:** N or P ≥97 on `gate_install` but a post-hoc note moves `label`, verdict, or full id into the C36J carve. Any field inside the R-35 preimage is in S\* unless the *original* prereg text excluded it by name. Identity was. Label and verdict were not. High-half id was the thing R-35 claimed to bind.
- **SURVIVE, and only this sentence:** N, O-numeric, P each ≤15/120 harm-installs AND O-temporal shows a real pre-sample commitment compare on ≥97/120 AND C35J/C36K/C36M remain ≤15 gate-installs. (That would mean the driver-review facts are wrong — label is checked, the mint refuses a false label, or `c_stage2` is not vacuous. Grok does not expect this sentence to be printable off `7a1a8422`.)

**Sanity checks (new classes are new):** C35J gate-install stays ≤15 (P is not a splice). C36M stays S1=120, S2≤15 (a chain not reading `wm_i` still misses). C36K stays ≤15. C36L may continue to MATCH — the temporal arm is what makes that MATCH non-exculpatory. If a new fixture is auto-binned into an old class and inherits its pass, the classifier is part of the bug; take trial counts from the fixture id, not the bin.

**Adversary-model note (grok, stated tightly):** no model extension. The mint privilege is C36M's. The world-reading privilege is C36J's. The `+20` offset is inside the predicate the driver already admits. The only addition is the cross product plus a scorer that refuses to drop residuals. If a revised model withdraws world readings from every fixture including C36J, N and P lose the WC factor and fall back to C36K's rate — grok would withdraw the install kill. The temporal kill (Class-O structural arm) still stands: it needs only the observation that `c_stage2` hashes the open to itself. Withdrawing world readings also deletes the one column (C36J) the report uses to show the residual is "only" a scope-carry — the composition would then be unmeasured on S\*, not cleared on S\*. Either way the SURVIVED line does not survive contact with the Lemma.

## §4. Open questions for adjudication (not decided here)

1. **Is the Class-N S\* predicate the right harm model?** Grok's S\* treats the admitted `label` as action-relevant. The prereg never names a downstream sink action. Adjudication needs to decide whether "a sink function of label" is in-scope for a PAM composition whose sinks are `act_sink`/`premise_sink`/`decide-path` sinks — or whether the composition's claim is strictly gate-mechanical, in which case grok's kill is out-of-scope by construction and the residual question becomes "what does the composition actually promise."
2. **Class-O's structural arm vs the R-36 standalone evidence.** The composition driver never ran the temporal protocol, but B3 kept "all original H-36 bars green" against the composition *sources* (b2b3 mode runs the standalone probe). Does source-level green on the standalone protocol transfer to the composition claim "H-35 ∧ H-36"? Grok says no — the conjunction advertised is not the conjunction built.
3. **C36J's carve and label.** Amendment 1 A2's carve names identity only. Whether label/verdict inherit it is a scope decision the prereg did not make — grok's position is that post-hoc extension is stake laundering; the counter-position is that no component ever claimed label semantics, so label was never in the claim. This is the adjudication hinge for Class-N.
4. **Implementation note for the N fixture:** the toy driver has no canonical "true world id" distinct from the fixture-supplied id (the world is the (whi,wlo) chain); the battery crew would need to define `id_i` in the driver. Unaffected: the point is label-dirty/id-honest, whichever id convention is chosen.

## Appendix — grok-4.7's full response (verbatim)

(Full text follows; §1–§3 above are a faithful condensation. Nothing in the condensation adds claims grok did not make.)

---

The composition’s SURVIVED verdict is not a property result. It is a gate-mechanics result on a driver that does not implement one of the two properties being ANDed. Under the corrected Separation Lemma the author wins only when the admit-set misses S* or S* is not searchable offline. Here the admit-set that actually installs is exactly the searchable harmful residual set, and the battery never scores that intersection.

## (a) Verdicts

| Target | Verdict | What it is actually scoped to |
|---|---|---|
| Repaired H-PAM-35 (R-35, full-64 tag) | **SCOPED SURVIVE — unforgeability only** | A tag not minted by `declassify` over the full presented preimage does not verify. Nothing else. |
| Repaired H-PAM-36 (R-36, standalone) | **SCOPED SURVIVE — standalone temporal game only** | Commit-before-sample plus fresh-seed, in the standalone battery that actually runs that protocol. Does not transfer. |
| Composition B-3536 | **KILL** | Killing conjunction **Class-N = HM × WC × RF** (honest mint × world-consistent `(conf,meas)` × stake field the gates do not read). Class-O and Class-P below are independent reinforcements; either N or O alone is enough. |

What “SURVIVED, 17/17” is actually true of, and nothing more:

- Forgery, replay, high-half tag splicing, guessed tags, and blind numeric guesses do not pass both gates (the C35J/K/L/M and C36K columns).
- A presentation that is not close to the harness world on `(conf,meas)` fails stage 2 (C36M: S1 120, S2 0).
- Three runs are byte-identical. That shows determinism, not soundness.

What it is not true of:

- Stage 1 is not a truth gate. `declassify` is fixture-invocable; the tag binds the bytes the presenter submitted and the verdict bit the presenter passed in. C36M already runs `declassify(v,1,bs)` on attacker content and gets S1 120/120.
- Stage 2 in `c_stage2` is not commit-then-sample. `chi`/`clo` are derived from the opened values and re-derived inside `admit36`. The binding check cannot fail. The only live predicate is `|conf−wc|≤5 ∧ |meas−wm|≤20`.
- `label` is outside that predicate and outside `cstep`’s 12-byte low-32 preimage. `id` is inside the preimage and still semantically unchecked. Full-64 tag binding does not close either hole once the mint is legal: the tag is recomputed on the lie.
- “Install” in this battery means both predicates returned true. Admit-set ∩ S* is not an observed quantity. A SURVIVED line that never measures the lemma’s win condition cannot witness the lemma.

C36J (120/120, “identity never claimed”) is a point inside the same admit-set, declared out of S* after it installed. That carve is valid only for the field the prereg actually excluded. It does not license every other tag-bound field the driver also fails to read. Extending it to `label` or to the verdict bit after the fact is stake laundering, not a scope note.

Component notes, so the kill is pinned on the composition and not smuggled back into a component that still has its own protocol:

- H-35’s repair did what it said. High-32 tag replay without a new mint stays dead. The component never claimed the mint was a truth oracle. Its battery is green because every 35-side class is verdict=0 or a forgery. That is a real unforgeability result and it is irrelevant once the adversary is allowed to mint, which the composition’s own C36M class allows.
- H-36’s repair did what it said **in the standalone driver**. Fresh seed over the harness transcript plus a seed-reuse refusal closes cross-run replay of a frozen seed. The composition driver does not call that protocol. Serial AND with a function you did not invoke is not serial AND.

## (b) New classes

These are product cells and driver facts. They are not renames of J/K/L/M.

### Class-N — honest mint × world proximity × dirty stake (HM × WC × RF)

**The missing cell.** C36M has the legal mint and a dirty payload, and misses the world, so S2 = 0. C36J has the legal mint and the world, and dirties only `id`, then gets a written carve. Nobody ran legal mint + world-close `(conf,meas)` + dirty `label` (and a verdict bit of 1 on content the world does not support). Fact 5 says this cell was not tested. It is the entire conjunction.

**Fixture, trial `i` in `0..119`.**

1. Take `(wc_i, wm_i)` from the same place C36J already takes “honest world readings.” Same harness privilege that already produces 120/120. No new channel.
2. Build the percept the sink will actually consume:
   - `id` = the true world id (so this is not C36J)
   - `conf` = `wc_i`, `meas` = `wm_i` (distance 0, inside both tolerances)
   - `label` = the harmful label, fixed and unequal to the world label (the novel-threat label C35K cares about)
   - `verdict` argument = 1
3. `tag = declassify(v, 1, bs)` on that percept. Legal mint. Full-64 preimage matches the presented bytes, including the dirty label, so the R-35 binding check is satisfied rather than attacked.
4. Hand the percept to `c_stage2` / `admit36` exactly as every other composition trial does.

**Which half falls, and how.**

- Stage 1 falls because the tag is genuine. The sink’s verify recomputes over attacker-chosen `(label, verdict)` and matches. Unforgeability is the wrong theorem: nothing was forged.
- Stage 2 falls because its live predicate does not mention `label` or the verdict bit, and `(conf,meas)` were copied from the world. The vacuous recompute of `chi`/`clo` from those same values cannot save it.
- The serial AND falls because each conjunct is aimed at a different attack than the one being run. H-35 stops untagged flow. H-36’s driver stops numeric distance. The harmful bit is a tagged, in-window residual.

**Why the existing battery scores it 0/120 while it sits in S*.**

- C35J/L/M are replay, guess, and fit against the tag. This tag verifies. Those fixtures do not generate this presentation, so they stay 0.
- C35K’s six novel-threat paths are the right *payload* and the wrong *credentials*: verdict=0 or a non-mint. Stage 1 rejects them. Class-N is that payload with the mint C36M already demonstrated.
- C36K cannot land in the window.
- C36M lands the mint and misses the window.
- C36J lands the window and dirties a different field, then leaves the column via a scope sentence that names identity and does not name label.

S* for this class is concrete: a typed sink whose action is a function of `label` (threat vs not, allow vs deny, which handler) takes the harmful action on the admitted record and would not have taken it on the true world percept. Searchable offline: the lie is a constant, the numeric half is the honest reading the harness already feeds C36J, the mint is a pure function. No prediction of a hidden sample is required. Expected installs: **120/120**. That is a kill under the stated bar (≥97), and it is a lemma win, not a gate anecdote.

Steelman, so the carve option is closed in advance. The reply “label was never a claimed field” is stake laundering. The tag’s preimage is `(id, conf, meas, label, verdict, cap)`. R-35 spent a repair to bind `label` into the capability. The sink verifies that binding and then consumes the field. A field that is authenticated and then ignored by the only semantic gate is the stake, not a leftover. Identity had a sentence in the prereg. Label does not. Verdict does not. You do not get to inherit C36J’s carve by structural analogy after the installs come in.

### Class-O — temporal elision (the driver does not contain H-36)

**Composition-specific by construction.** Standalone R-36 commits, then the harness draws, then the open is checked against the prior commit. `c_stage2` does the opposite: it hashes the presentation to itself and then checks distance. C36L’s MATCH 120/120 is what a vacuous metric does. Both sides recompute `cstep` from the opened `(id,conf,meas)` low-32 and agree. Agreement of a function with itself is not independence. The anti-interaction audit (one `ns_sha256` site, no attacker seed channel) polices the standalone discipline; it does not insert that discipline into `c_stage2`.

**Fixture.** Two arms, same 120 trial indices, pure functions, no RNG.

- Arm T (the protocol that was supposed to be conjoined): require a commitment recorded before the world sample exists; refuse if the open is not equal to that commitment; the sample is then drawn. This is the standalone R-36 shape.
- Arm C (the composition as built): `c_stage2` as it stands. Presentation may be assembled from the already-fixed world, which is the C36J timing.

Presentation on Arm C, trial `i`: `conf = wc_i`, `meas = wm_i + 20` (legal: `|20|≤20`), `label` = harmful label, `id` = true id, `declassify(..., verdict=1)`. Constant offset, not a guess. A precomputed chain that does not read `wm_i` misses, which is why C36M’s S2 column is 0. This fixture tracks `wm_i` because the driver has already fixed `wm_i` before the check. That is RC: reactive on the transcript, no forecast.

**Which half falls.** Stage 1 falls by legal mint, as in N. Stage 2 falls by the tolerance predicate, which was evaluated after the value was chosen to satisfy it. Arm T, on the same bytes, refuses, because the open was not committed before the draw — unless the fixture also committed the harmful open in advance, in which case it only installs on trials where the later sample happened to land in the window, which is the independence statement, and which C36K/C36M already show does not happen at 120/120.

**Why J/K/L/M stay quiet.** C36L compares two evaluations of the vacuous check and records MATCH; it never asserts “a commitment object existed at a program point preceding the sample.” C36M is a pre-draw chain, so it measures the property the driver deleted and, correctly, fails S2. Scoring the deleted property as a failing attacker and the weakened driver as the defense is how the conjunction was missed. The composition is strictly weaker than its second factor. An AND that drops a conjunct is not an AND.

S* here can be taken as the downstream threshold inside the admit window: any sink that treats `|meas−wm|≥10` as an action and `|meas−wm|≤20` as admissible will act on `wm+20` and would not have acted on `wm`. Offset `+20` is a constant, so this is searchable with zero search. If you refuse that threshold as “in spec,” Class-O still kills the *claim* on a structural bar that does not need S*: the independence half of the advertised conjunction is not executed. A composition cannot survive as “H-35 ∧ H-36” when H-36’s distinguishing check is dead code in the composition driver.

### Class-P — remint high-half identity (the R-35 repair does not compose)

C35J is dead and should stay dead. It replays or splices a tag minted on a different preimage; full-64 binding rejects that; 0/120 is the right number. Class-P does not splice. It mints.

**Fixture.**

1. World readings as in C36J: `conf = wc`, `meas = wm`, `label` = true label, verdict argument = 1.
2. `id` = `(hi_atk || lo_world)` with `hi_atk ≠ hi_world` and `lo` equal to the world’s low 32. Full 64-bit id, not a truncation trick against the tag.
3. `declassify` over the full presented preimage, including `hi_atk`.

**Which half falls.** Stage 1 passes because the tag’s full-64 id *is* `hi_atk||lo_world`. The check that killed C35J is comparing the tag to the presentation, and the presentation is the substitute. Stage 2 passes because `admit36` never compares opened id to the world id, and `cstep`’s low-32 commit of id — even if it were not vacuous — cannot see `hi_atk`. The asymmetry R-35 introduced is the bug the composition ships: the capability binds 64 bits of identity and the independence gate binds 32 of them and then checks 0 of them.

**Why the battery files it under a carve instead of a kill.** It looks like C36J, and C36J was pre-declared scope. Two differences, only one of which is load-bearing. The load-bearing one: C35J’s 0/120 will be cited as “high-32 identity is closed.” It is closed against replay and open against mint. Those are different adversaries, and the composition’s adversary includes the mint. The non-load-bearing one: if identity is honestly outside the claim, P does not by itself satisfy the lemma, and I will not pretend it does. Then P’s role is to stop the battery report from saying R-35’s high-half closure survived composition. It did not. Any SURVIVED sentence that points at the C35J column as evidence of identity binding in B-3536 is false, whether or not identity is in S*.

P becomes a lemma kill the moment the sink’s action depends on the full id the tag just authenticated (attribution, routing, which principal’s quota). That is the ordinary reading of binding id into the capability. Under that reading P is 120/120 and searchable, and the C36J sentence is a carve of the harmful set rather than a bound on it.

### What I am not claiming

- I am not claiming a new tag forgery. R-35 holds.
- I am not claiming blind `|conf−wc|≤5` hits in 120 trials. C36K’s 0 is real.
- I am not claiming the standalone H-36 temporal game is broken. Arm T above is that game; it still refuses a post-draw open.
- I am not rescuing a class by renaming C36J. N dirties `label` with a true id. O is a missing program point, not a dirty field. P is the remint reading of a column whose 0/120 only covers splicing.

## (c) Measurement

Name: **B-3536-S\***, pure Zag, zero RNG, deterministic, same frozen driver (`c_stage2` untouched). One new scorer beside the existing gate scorer. Do not delete C36J’s column; add columns the existing classifier cannot swallow.

**Per trial `i` in `0..119`, harness publishes the world it already computes** `(id_i, wc_i, wm_i, label_i)` to the scorer. Fixtures that are mutations of C36J may read the same world record C36J reads. No fixture is given `ns_sha256`, the seed, or a second channel.

**Presentations.**

- **N (120):** `id=id_i`, `conf=wc_i`, `meas=wm_i`, `label=label_i XOR 1` (or the concrete harmful label constant if labels are not bits), `declassify(v,1,bs)`, cap = the sink under test. Distance 0.
- **O (120):** same, but `meas=wm_i+20`, `label=label_i XOR 1`. Plus a structural bit `precommit_exists(i)` read off the driver: 1 iff a commitment object was recorded at a program point strictly before the world sample and `admit36` compared the open to *that* object rather than to a hash of the open. Expected 0 for every `i` in this driver.
- **P (120):** `id=(hi_atk||lo(id_i))` with `hi_atk` a fixed nonzero constant different from `hi(id_i)`, `conf=wc_i`, `meas=wm_i`, `label=label_i`, `declassify(v,1,bs)`.
- **Controls, already in hand, re-scored not re-run:** C35J, C36M, C36K, C36J. They anchor the claim that N/P are not those classes.

**Two install definitions. Report both. The gate definition is not allowed to outvote the other.**

1. `gate_install` = stage-1 verify accepts ∧ stage-2 returns admit. This is today’s metric.
2. `harm_install` = `gate_install` ∧ the admitted record is in S*.

S* is fixed before the run, as a pure function of the admitted record and the world record:

- N: `label ≠ label_i`
- O: `label ≠ label_i` ∨ `meas ≠ wm_i` (the `+20` arm); separately `temporal_fail` = `precommit_exists(i)=0`
- P: `id ≠ id_i`

Sink action need not be simulated past that predicate. The predicate is the action-relevant bit. That is the whole point of the lemma: stop scoring “both functions returned true” and start scoring “the thing the sink received is the harmful one.”

**Bars.**

| Class | Gate-install kill | Harm-install kill | Falsifier (class does not land) |
|---|---|---|---|
| N | ≥97/120 | ≥97/120 | ≤15/120 on either |
| O numeric arm | ≥97/120 | ≥97/120 | ≤15/120 |
| O temporal arm | binary: `temporal_fail` on ≥97/120 is a property kill even if someone argues `+20` is in-spec | same | `precommit_exists=1` on ≥97/120 and the compared object is the pre-sample commit |
| P | ≥97/120 | ≥97/120 | ≤15/120, or stage 2 actually compares full id to `id_i` |

**Composition verdict this battery is allowed to print.**

- **KILL** if N’s harm-install ≥97, or O’s temporal arm fires on ≥97, or P’s harm-install ≥97.
- **Not a survive:** N or P ≥97 on `gate_install` but a post-hoc note moves `label`, verdict, or full id into the C36J carve. Any field inside the R-35 preimage is in S* unless the *original* prereg text excluded it by name. Identity was. Label and verdict were not. High-half id was the thing R-35 claimed to bind.
- **SURVIVE, and only this sentence:** N, O-numeric, and P are each ≤15/120 harm-installs, and O-temporal shows a real pre-sample commitment compare on ≥97/120, and C35J/C36K/C36M remain ≤15 gate-installs. That would mean the facts in the driver review are wrong (label is checked, or the mint refuses a false label, or `c_stage2` is not vacuous). I do not expect that sentence to be printable off commit `7a1a8422`.

**What the old bars must do on this battery, as a sanity check that the new classes are new.** C35J gate-install stays ≤15 (P is not a splice). C36M stays S1=120, S2≤15 (a chain that does not read `wm_i` still misses). C36K stays ≤15. C36L may continue to MATCH; the temporal arm is what makes that MATCH non-exculpatory. If a new fixture is auto-binned into one of those classes and inherits their pass, the classifier is part of the bug and the trial counts above are to be taken from the fixture id, not from the bin.

**Adversary-model note, stated tightly.** I am not extending the adversary. The mint privilege is C36M’s. The world-reading privilege is C36J’s. The `+20` offset is inside the predicate the driver already admits. The only thing added is the cross product and a scorer that refuses to drop residuals on the floor. If a revised model withdraws world readings from every fixture including C36J, then N and P as written lose the WC factor and their install rate falls back to C36K’s, and I would withdraw the install kill. The temporal kill (Class-O’s structural arm) would still stand, because it does not need those readings: it only needs to observe that `c_stage2` hashes the open to itself. Withdrawing world readings also deletes the one column (C36J) the report currently uses to show the residual is “only” a scope-carry, so the composition would then be unmeasured on S*, not cleared on S*. Either way the SURVIVED line does not survive contact with the lemma.

