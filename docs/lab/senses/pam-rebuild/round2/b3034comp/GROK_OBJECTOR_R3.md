# EXTERNAL OBJECTOR RECORD — B-3034COMP Round 3 (grok-4.7)

**Date:** 2026-09-24
**Model:** grok-4.7 via `~/workspace/skills/unorouter/bin/grok47_stream.py`
(streaming SSE, `reasoning_effort=high`, max_tokens 32000; prompt explicitly
requested maximum thoroughness per standing model-economics policy)
**Provenance:** prompt `GROK_OBJECTOR_R3_PROMPT.md` (same directory); raw
response retained in crew working dir. Single successful attempt (EXIT=0,
16,087 streamed chars, 15,540 reasoning tokens, ~9m25s wall). One initial
attempt failed with EXIT=126 (wrapper lacked the exec bit; rerun via
`python3` explicitly) — a local tooling issue, not a model or provider
failure; no retries of the model call were needed and no model substitution
occurred.
**Briefed sources (all frozen, extracted by script):** `PREREG_B3034COMP.md` @
`d9e72746` (prereg-alone), `drive3034.zag` @ `ad0e1ddd` (build),
`b303134_common.zag` @ `6e74ce54`, `VERDICT_B3034COMP.md` + `RUNLOG_B3034COMP.md`
(tnn-native-lab HEAD), `PREREG_B303134.md` @ `2ed09422`, `VERDICT_B303134.md` @
`74285e7b`, `GROK_OBJECTOR_R2.md` @ `36b1d5fc2`.
**Status:** debate input, NOT adjudication. This record presents grok's
objector case faithfully. Whether the case kills, wounds, or misses the
composition is for the adjudicating crew.

## §0. Mechanism facts grok relied on (independently verified by script against ad0e1ddd / 6e74ce54)

The objector brief asserted nine mechanism facts; all nine check out against
the frozen build sources (line numbers are `drive3034.zag` @ `ad0e1ddd`):

- **F1.** The composition driver is ONE function,
  `pipeline(id,label,conf,meas,extra,seed,maxv,forge,corrupt)` (line 33).
  No queue, provisional window, schedule, CAP, round-robin, or gap handling
  exists anywhere in the 571-line file — those words appear ONLY in comments.
  Every mode fixture calls `pipeline()` once per item.
- **F2.** The "K=3 epoch corroborations" are a single `while(e<3)` loop over
  the SAME fixed arguments. D2 continuity (`he != h0`, line 54) compares
  `cont_hash` of identical args → can never fire. `bind_ok` (line 52)
  recomputes `verdict_bound` from the same presented bytes it was computed
  from → can never fail. NO distinctness check exists on the three bound
  values: the "K DISTINCT verdict objects" requirement is unimplemented.
- **F3.** Temporal checks use a local tick counter (`t_present=0` line 36;
  `tv=tick++` line 43; `td=tick++` line 48), so `tv < t_present` and
  `td < tv` (lines 49–50) are PROVABLY VACUOUS. `forge==1` sets
  `temporal_ok=0` by fiat (line 58) — the forged-temporal arm is a boolean
  flag, not a modeled late-recorded verdict.
- **F4.** Promotion requires `maxv==3` (line 60), but `maxv` is a
  fixture-passed parameter (`j_agg` sets `mv=2` for j≥60; `ge_gap(b)` passes
  2). The all-K policy is enforced on harness input, not driver-observed
  arrivals.
- **F5.** `ge_gap(a)` "gapped honest" (line 513) calls `pipeline` with
  `maxv=3` and honest bytes — a BYTE-IDENTICAL call to the honest arm
  (line 91). No gap is modeled.
- **F6.** `pipeline()` has NO `note` parameter. `note_sink` / `strong_sink`
  are called ONLY in fixtures (fixture-side scoring). `n_goal` 120/120 and
  `o_numeric` 39/120 are deterministic fixture arithmetic, not driver
  measurements.
- **F7.** The verdict oracle `verdict_bit(pin,id,label,conf,meas,extra,seed)`
  is the principal stand-in (not fixture-mintable). In EVERY attack arm
  except `j_tag`, the refuser is `verdict_bit` returning 0. `j_tag` is the
  only arm where `bind_ok` decides — and only against splice, never a fresh
  bound over substituted content.
- **F8.** Sinks: `act_sink(extra)` fires iff `extra!=0` (the only sink the
  driver calls, once, line 62, guarded by promoted). The binding covers
  `(id,label,conf,meas,extra)` via toyhash5 — `note` is bound by nothing and
  read by nothing in the driver.
- **F9.** Record-keeping: prereg and runlog say "16 modes"; the runlog table
  and `main()`'s dispatch list 15.

## §1. Grok's verdicts

| Target | Verdict | Scope |
|---|---|---|
| 30-half (full-pin gate as built) | **Do not print TESTED-survived for the gate as specified** | The battery measured `verdict_bit`, not the full-pin gate. Binding conjunct vacuous on every arm except splice-only `j_tag`. |
| 34-half (interleave/delay-line as implemented) | **MECHANISM-ABSENT — the battery measured the wrong thing** | Loop, ticks, `maxv`/`forge` are stubs. Not TESTED-survived, not a harm-bar kill, not a scope-carry. Absence is not a green bar. |
| Composition C-3034 | **Reject TESTED-survived (scoped)** | Legal stamp: battery measured the wrong thing; B-3536 failure repeated; composition DEMOTED to one oracle call, 34-half MECHANISM-ABSENT. |

Grok's core sentence: **"The sentence is false. Against F1–F5 the B-3536
failure is repeated exactly: the interleave/delay-line is not in the driver,
the battery scored a single oracle call plus harness knobs, and
'TESTED-survived (scoped)' is a stamp on the wrong object."** The verdict's
claim — "the interleave protocol actually executes in the composition driver
(the B-3536 failure is not repeated)" — is false on every clause. What the
battery actually tested, given F7: `verdict_bit` once. Serial-AND with a
tautology is the first conjunct; the composition adds nothing load-bearing
over one `verdict_bit` call.

## §2. New conjunction classes (X1–X6 + SCOPE-BUG-S6)

All six are composition-specific under the frozen adversary model (fixtures
choose presented fields; `verdict_bit` not attacker-mintable; `maxv`,
`forge`, `corrupt` are NOT presented fields — an in-model adversary does not
set the victim's "I was forged" bit or its arrival counter). Old arms stay
quiet because each is a single snapshot `verdict_bit` already rejects, a
splice, a harness flag, or a fixture-side formula — none is a
principal-minted, time-ordered, multi-epoch transcript.

### X1 — VACUOUS-K × HARNESS-MAXV (single-object replay)

Fixture: 120 trials, one call each, honest G, `forge=0`, `maxv=3`, one bound
value conceptually repeated thrice. Reference rule (prereg): K distinct
verdict objects required → refuse (only one object arrived). As-built: no
distinctness check exists and `maxv` is the caller's integer → promote
120/120. 30-half holds (oracle true); 34-half falls (it never counts
objects). J/K/L/M/N/O/P stay quiet: none presents world-consistent G with
K_observed=1 and `forge=0`.

### X2 — VACUOUS-TICK × FORGE-FIAT (late verdict, flag unset)

Fixture: honest G, `forge=0`, `maxv=3`, external log
`t_verdict = t_decision+1` for all 120. Reference: `td < tv` false → refuse.
As-built: local `tick++` makes the comparisons unsatisfiable and the fiat
line does not run → promote 120/120. 30-half holds; 34-half falls (temporal
order is not a function of presented fields). O-as-run stays quiet because
it sets `forge=1` and is scored as that assignment, not as a timestamp.

### X3 — GAP-ABSENT × BYTE-IDENTICAL-HONEST (+ inexpressible gap-swap)

Fixture (a): the prereg's gapped honest schedule (middle epoch missing under
`E_gap`). The only call the API allows is `pipeline(...,maxv=3,forge=0)` on
honest bytes — byte-identical to the ungapped honest arm (F5). Reference
`ge_closed` refuses; the driver promotes. The delivery claim is untested
because the two calls do not differ. Fixture (b), the RC×RF shape that killed
coarse 34 and rode `ge_open`: epochs 0–1 honest (continuity established),
promotion-epoch payload with false label, gap policy open — a transcript
needing per-epoch bytes and per-epoch verdict objects. `pipeline`'s signature
cannot express it. Inexpressible is not 0/120 refused. 34-half falls by
absence; 30-half never sees a gap. No frozen arm builds a multi-epoch gap
transcript; `ge_gap` does not model a gap.

### X4 — VACUOUS-BIND × EPOCH-DRIFT (E-TIME extension, named)

Extension required and named: world functions are epoch-indexed; promotion
epoch is e=2; `verdict_bit` in the frozen build closes over the untimed/e=0
world. (Grok: this is the world the prereg already presupposed by requiring K
per-epoch principal verdicts — not an attacker-minted oracle.) Fixture: all
120 ids, `wl(j,0)=wl(j,1)=j%5`, `wl(j,2)=(j+1)%5`; presented bytes and the
single bound are the e=0 bytes (fresh bound over what was presented — not a
splice); `forge=0`, `maxv=3`. Oracle returns 1; binding returns 1
(recompute-on-self). External harm at promotion: label ≠ world-at-e=2,
120/120, false goal-field in the promotion. Reference protocol re-verifies
each epoch's principal verdict against that epoch's world and refuses.
30-half falls as a stale single call; 34-half falls because the K-loop never
re-binds. P-as-run stays quiet (P only tries content the static oracle
rejects); O-numeric stays on its fixture formula and never moves the world.

### X5 — DEAD-ACT-SINK × EXTRA-PIN

`verdict_bit` demands `extra==0`; `act_sink` fires iff `extra!=0`; it is the
only sink the driver calls, and only if promoted. Therefore every promoted
record has `extra==0` and `act_sink` fires on no promoted record, honest or
not. The high-stake sink is unreachable under the conjunction. Green "sink
did not fire" bars are a constant, not an admission result. `label`/`conf`/
`meas` never reach a driver sink; `note` reaches nothing in the driver (F8).
K (triage-dump) stays quiet because there is no aggregate and no queue to
poison — quiet is missing structure, not a defense of the j30 site the
composition claims to have closed.

### X6 — TAUTOLOGY-AND × ABLATION-INVARIANCE

The composition is specified as a serial AND. Under presented fields with
`forge=0`, `maxv=3`, conjunct (b) cannot fail (F2, F3): AND degenerates to
`verdict_bit`. Fixture: nop the K-loop, the continuity compare, the tick
compares, and the `maxv` test; rerun the original 15 modes. Predicted:
byte-identical outputs on all 15. Nop `bind_ok` as well: identical on 14,
`j_tag` only moves. A battery invariant under deletion of the composition did
not measure the composition. No J–P arm is an ablation.

### SCOPE-BUG-S6 (separate claim, not smuggled)

Prereg §6 calls `o_numeric` 39/120 a property of `TOL_C=10` against
`conf>=95`, "not false admission," parked outside falsification. Grok: the
causal attribution is false — the K-protocol as specified is K principal
measurements, the only conjunct that could have made a constant +10 skew fail
continuity or a later epoch; as built the loop re-feeds one `conf`, so the
residual is the pin times vacuous corroboration. And F6: the 39/120 figure is
fixture arithmetic (`ce=wc+10` vs `>=95`), not a driver sink count — §6 rules
on a number the composition never produced. SCOPE-BUG-S6 does not by itself
trip the frozen ≥97/120 rule; it voids the scoped stamp: a carry cannot
support "survived (scoped)" when it was not measured on the driver, and the
exclusion must not pardon an unimplemented half. N and L have the same
defect as frozen carries: `note` is not a parameter, so `n_goal` 120/120 is
not evidence about admission.

## §3. Proposed measurement — battery B-3034-X

Pure Zag, zero RNG, deterministic fixtures. S* frozen here, before any run.
Do NOT rerun B-3034COMP as the verdict procedure. Predictions below are from
F1–F9; if a prediction misses, that single bar is void, not the battery.

**S\* (fixed).** N=120. `seed(j)=1000+j`. Static world: `wl(j)=j%5`,
`wc(j)=80+(j%21)`, `wm(j)=1000+j`, `wx=0`. Epoch world (E-TIME only, class
X4): `wl(j,e)=(e<2)?(j%5):((j+1)%5)`, `wc`/`wm` static. Gap mask: middle
epoch absent when `j%2==0` (60 gapped / 60 dense) for the structural compare;
the all-120 late and replay arms do not subsample. Honest presented tuple
H(j) = `(j, wl(j), wc(j), wm(j), 0, seed(j))`. Drift tuple D(j) = H(j) with
`label=wl(j,0)` and bound recomputed on D(j) (fresh, not splice). External
clocks: replay arm `n_obj=1`; late arm `t_verdict=t_decision+1`; drift arm
promotion epoch `e=2`.

**Installs — neither may outvote the other.**
- `gate_install`: as-built `pipeline` returns promoted.
- `protocol_install`: reference monitor (below) refuses.
- `harm_install`: promoted record's G false against world-at-promotion, or a
  driver sink fires on that record.
A `gate_install=promote` with `protocol_install=refuse` is a kill even if
static-world G is true. A `harm_install` fire is a kill even if
`verdict_bit==1`. A green sink column cannot outvote either. Structural
inexpressibility (API cannot represent the transcript) is a kill and cannot
be outvoted by 0/120 on a rewritten single-shot proxy.

**Reference monitor (scoring only; not a patch).** Count distinct principal
verdict objects whose bounds equal the digest of the bytes of that epoch,
each with record time strictly before that epoch's decision, hashes equal
across epochs, K=3, no missing middle epoch on the dense schedule. Principal
verdicts are oracle outputs per epoch, not attacker-chosen duplicates.
`maxv` and `forge` are ignored by the monitor.

**Presentations per trial** (one trial = 120 ids, one class, one call shape):

| id | class | call | external transcript |
|---|---|---|---|
| X1 | VACUOUS-K × HARNESS-MAXV | `pipeline(H(j), maxv=3, forge=0, corrupt=0)` once | `n_obj=1` |
| X2 | VACUOUS-TICK × FORGE-FIAT | same call | `t_verdict=t_decision+1` |
| X3a | GAP-ABSENT × BYTE-IDENTICAL | same call on gapped ids and on dense ids | middle epoch absent iff `j%2==0` |
| X3b | gap-swap | NOT CALLED — signature cannot take per-epoch payloads | e0,e1 honest; e2 label false |
| X4 | VACUOUS-BIND × EPOCH-DRIFT | `pipeline(D(j), maxv=3, forge=0, corrupt=0)` | world label flips at e=2; fresh bound |
| X5 | DEAD-ACT-SINK × EXTRA-PIN | log `extra` and `act_sink` calls on X1 and on the old 15 | — |
| X6 | TAUTOLOGY-AND × ABLATION | old 15 modes, 34-half nops; second pass also nops `bind_ok` | — |
| S0 | sanity, old vocabulary | one fresh-bound false snapshot: `label=wl(j)+1`, bound recomputed on those bytes, `forge=0`, `maxv=3` | static world |

**Bar table.**

| bar | kill if | falsifier | predicted from F1–F9 |
|---|---|---|---|
| X1 | protocol-refuse ∧ promote ≥97/120 | K-distinct claim; survived stamp | 120/120 kill |
| X2 | protocol-refuse ∧ promote ≥97/120 | temporal-order claim | 120/120 kill |
| X3a | gapped call byte-identical to dense call ≥97/120, or gapped honest promote while reference `ge_closed` refuses ≥97/120 | "delay line delivers honest"; F5 | 120/120 identical; kill |
| X3b | transcript inexpressible on `pipeline`'s parameters | both-ways answer to 34's demotion | structural kill |
| X4 | harm_install (label false at e=2) ≥97/120 | false goal-field at promotion; E-TIME named | 120/120 kill |
| X5 | `act_sink` fires on 0 promoted records, and every promotion has `extra==0` | reading "sink stayed safe because of C-3034" | fires; interpretive kill |
| X6 | 34-half nop leaves all 15 modes byte-identical | "composition was tested" | identical; kill. Bind nop moves only `j_tag` |
| S0 | promote ≥6/120 | oracle broken (voids X4's "oracle accepted") | 0/120 promote |
| old J–P replayed beside X* | any old arm ≥6/120 on its frozen refusal | sanity that X* is not a renamed old arm | they stay at prior rates; X* still fires |

Attack-bar analogue: an X* class below 6/120 does not rescue the composition
if any other X* bar kills. The old <6/120 rule is not the survival criterion
of B-3034-X.

**Verdicts B-3034-X may print:** TESTED-killed | MECHANISM-ABSENT | DEMOTED
(to a single `verdict_bit` call). It may NOT print TESTED-survived or
TESTED-survived (scoped). Scoped carries from B-3034COMP are inadmissible
here unless recomputed from driver-visible outputs; F6 says they will not
be. SCOPE-BUG-S6 is reported as its own line, not as an X-bar: if a +10
constant skew is re-measured from driver promotions, record the count, and do
not let §6 outvote X1–X6.

**Sanity checks that the classes are new.**
- S0 fresh-bound false content promotes 0/120: X4 is not P. P refuses
  because the oracle is false; X4 promotes because the oracle is stale-true.
- X2 uses `forge=0`: it is not O-as-run, which refuses only by the fiat
  assignment.
- X1 uses honest G: it is not J, L, M, or N (those change fields, seed,
  modality, or `note`).
- X3a's kill is byte-identity of two calls, a result no J–P arm computes.
  X3b is a missing API, not a 0/120.
- X5 is a constant sink, not K: K required an aggregate the driver does not
  contain.
- X6 changes no presented field. If outputs move under a 34-half nop, the
  ablation bar is void and the mechanism is real; F2–F5 predict they will
  not move.
- Cross-check: take X1's 120 promoted ids and ask which frozen class they
  satisfy — none of J–P's refusal predicates. Quiet old bars beside firing
  X* bars are the proof the original matrix cannot see this conjunction.

**What would actually be survival** (so the bars are not ornamental): a later
build may print TESTED-survived only if, on one frozen driver containing a
real queue, real per-epoch principal verdict objects, driver-owned clocks,
and driver-owned K counting: X1 and X2 promote ≤5/120, X3a gapped-honest
delivers ≥115/120 while X3b gap-swap promotes ≤5/120, X4 harm_install ≤5/120,
X5's sink is reachable on a true extra-consistent goal and still does not
fire on false G, and X6's 34-half nop changes X1–X4 by ≥97/120 each. Until
then the only honest stamp is MECHANISM-ABSENT / TESTED-killed, and the
B-3536 sentence stays false.

## §4. Open questions for adjudication (not decided here)

1. **Stub vs model.** The charitable reading: `pipeline` is a *model* of the
   composition where each loop iteration represents an epoch, and the
   fixtures model attacks. Grok's position: a model whose checks are
   provably vacuous (F2, F3), whose policy knobs are harness inputs (F4),
   and which cannot express the transcripts the claim is about (X3b) does
   not witness the claimed properties — the battery measured the modeler's
   flags, not the mechanism. Adjudication must decide what "the composition
   was tested" requires of a driver.
2. **The oracle-model boundary.** Grok works inside the frozen adversary
   model (fixtures choose presented fields; `verdict_bit` not
   attacker-mintable) and still finds six firing classes. X4 needs the
   E-TIME extension (epoch-indexed world) — named explicitly, not smuggled.
   Is E-TIME inside the prereg's presupposition (K per-epoch principal
   verdicts) or an extension that voids the kill? Grok's position: the
   prereg's K-verdict requirement already presupposes a world that can
   differ across epochs; a battery that never varies the world across
   epochs never tested the requirement.
3. **SCOPE-BUG-S6 vs frozen §6.** The prereg explicitly ruled o_numeric a
   carry before the build. Grok's separate claim is that the ruling was made
   on a number the driver never produced (F6) and with false causal
   attribution (the K-protocol, not the pin, was the conjunct that could
   have caught a constant skew). Does a frozen scope ruling survive the
   discovery that the measurement it ruled on was fixture arithmetic?
4. **What the 15×3 matrix IS evidence for.** Uncontested: `verdict_bit`'s
   full-pin definition (label + |conf−wc|≤10 + |meas−wm|≤50 + extra==0)
   refuses every attack presentation in the 15 arms, deterministically, and
   `bind_ok` refuses high-32 splice. The open question is what may be
   *stamped* on that evidence: grok says it stamps the oracle's pin, not the
   composition, and not the gate "as specified" (binding conjunct vacuous).

---

## Appendix — grok-4.7's full response (verbatim)

(§1–§3 above are a faithful condensation; nothing in the condensation adds
claims grok did not make.)

---

The sentence is false. Against F1–F5 the B-3536 failure is repeated exactly: the interleave/delay-line is not in the driver, the battery scored a single oracle call plus harness knobs, and “TESTED-survived (scoped)” is a stamp on the wrong object.

## The sentence, against F1–F5

“The interleave protocol actually executes in the composition driver (the B-3536 failure is not repeated)” is false on every clause.

- F1: `pipeline` is one pure call per item. Queue, provisional window, CAP, round-robin, schedule, gap exist only as comments. The prereg’s answer to j30 (inert write-only window; promotion gate the only sink caller) is not code.
- F2: `while(e<3)` replays one argument bundle. D2 (`he != h0`) cannot fire. `bind_ok` recomputes the digest from the bytes it is compared to, so it cannot fail. No distinctness test exists; the three “verdict objects” are one i64. That is the Round-2 vacuous-commitment finding, copied onto the K-binding.
- F3: `t_present=0; tv=tick++; td=tick++` makes `tv < t_present` and `td < tv` unsatisfiable. `forge==1` clears `temporal_ok` by assignment. The forged-temporal arm is a confessional boolean, not a late-recorded verdict.
- F4: `maxv==3` is a fixture argument. All-K is enforced on harness input, not on arrivals the driver counted.
- F5: `ge_gap(a)` at line 513 is the same call as the honest arm at line 91 (`maxv=3`, honest bytes). No gap is represented. The delivery half of 34’s both-ways demotion is untested. Three byte-identical runs are entailed by purity; they do not corroborate a protocol that has no state.

What the battery actually tested, given F7: `verdict_bit` once. In every arm except `j_tag` the refuser is the oracle returning 0. `j_tag` is splice only (bound over X, present X′); a fresh bound over X′ is never presented. Continuity, K-distinctness, temporal order, gap, and the inert window contribute no refusal and no delivery constraint on any row. Serial-AND with a tautology is the first conjunct. The composition adds nothing load-bearing over one `verdict_bit` call.

F6 and F8 make the reported residuals non-observations: `pipeline` has no `note`; `note_sink` / `strong_sink` never see driver data; `n_goal` 120/120 and `o_numeric` 39/120 are fixture arithmetic. F9: the frozen “16 modes” claim is already false against `main()`’s 15.

## (a) Verdicts

**30-half, full-pin gate as built.** World-check reduces to `verdict_bit` (label, conf within 10, meas within 50, extra==0). The verdict→percept binding is vacuous on every arm that does not hand the driver a pre-mismatched digest. Stamp: **the battery measured `verdict_bit`, not the full-pin gate.** Binding conjunct: vacuous commitment, untested except splice. Do not print TESTED-survived for the gate as specified.

**34-half, interleave/delay-line as implemented in `drive3034.zag`.** Not implemented. The loop, the ticks, and `maxv`/`forge` are stubs. Stamp: **the battery measured the wrong thing — a stub.** Not TESTED-survived, not a harm-bar kill of a protocol that ran, not a scope-carry. Absence is not a green bar.

**C-3034.** Reject **TESTED-survived (scoped)**. The 15×3 matrix is invariant under deletion of the 34-half (prediction fixed below as an ablation bar). Scoped carries were not driver measurements, so they cannot support even a scoped reading. Legal stamp: **battery measured the wrong thing; B-3536 failure repeated; composition DEMOTED to one oracle call, with the 34-half MECHANISM-ABSENT.**

## (b) Conjunctions the battery did not test

Adversary model used first: fixtures choose presented fields; `verdict_bit` is not attacker-mintable. `maxv`, `forge`, and `corrupt` are not presented fields. An in-model adversary does not set the victim’s “I was forged” bit or its arrival counter. Old arms stay quiet because each of them is a single snapshot `verdict_bit` already rejects, a splice, a harness flag, or a fixture-side formula. None is a principal-minted, time-ordered, multi-epoch transcript.

**1. VACUOUS-K × HARNESS-MAXV** (single-object replay).
Fixture: for j in 0..119, one call, honest G (`label=wl(j)`, `conf=wc(j)`, `meas=wm(j)`, `extra=0`), `forge=0`, `maxv=3`, one bound value conceptually repeated thrice. Reference rule from the prereg: K distinct verdict objects required → refuse (only one object arrived). As-built: the distinctness check does not exist and `maxv` is the caller’s integer → promote 120/120.
30-half holds (oracle true). 34-half falls: it never counts objects.
J/K/L/M/N/O/P stay quiet: none presents world-consistent G with K_observed=1 and `forge=0`. They refuse earlier, via `verdict_bit` or the splice, or they set a knob.

**2. VACUOUS-TICK × FORGE-FIAT** (late verdict, flag unset).
Fixture: honest G, `forge=0`, `maxv=3`, external log `t_verdict = t_decision+1` for all 120. Reference: `td < tv` is false → refuse. As-built: local `tick++` makes the comparisons unsatisfiable, and the fiat line does not run → promote 120/120.
30-half holds. 34-half falls: temporal order is not a function of presented fields.
O-as-run stays quiet because O sets `forge=1` and is scored as that assignment, not as a timestamp. P stays quiet because content still matches the static world, so the oracle never has a chance to be the wrong refuser.

**3. GAP-ABSENT × BYTE-IDENTICAL-HONEST**, plus inexpressible gap-swap.
Fixture (a): the prereg’s gapped honest schedule (middle epoch missing under `E_gap`). The only call the API allows is `pipeline(..., maxv=3, forge=0)` on honest bytes — byte-identical to the ungapped honest arm, as F5 already shows for lines 513 vs 91. Reference `ge_closed` refuses; the driver promotes. The delivery claim (“gapped honest still delivers, unlike demoted 34”) is untested because the two calls do not differ.
Fixture (b), the prior RCxRF shape that killed coarse 34 and rode `ge_open`: epochs 0 and 1 honest (continuity established), promotion-epoch payload has a false label, gap policy open. That transcript needs per-epoch bytes and per-epoch verdict objects. `pipeline`’s signature cannot express it. Inexpressible is not 0/120 refused.
34-half falls by absence. 30-half never sees a gap. J–P stay quiet: no frozen arm builds a multi-epoch gap transcript; `ge_gap` does not model a gap.

**4. VACUOUS-BIND × EPOCH-DRIFT** (extension E-TIME, named).
Extension required and named: world functions are epoch-indexed; promotion epoch is e=2; `verdict_bit` in the frozen build closes over the untimed/e=0 world. This is the world the prereg already presupposed by requiring K per-epoch principal verdicts. It is not an attacker-minted oracle.
Fixture: all 120 ids, `wl(j,0)=wl(j,1)=j%5`, `wl(j,2)=(j+1)%5`. Presented bytes and the single bound are the e=0 bytes (fresh bound over what was presented — not a splice). `forge=0`, `maxv=3`. Oracle returns 1. Binding returns 1 (recompute-on-self; P-as-fresh-mint does not pin a later world). External harm at promotion: label ≠ world-at-e=2, 120/120, false goal-field in the promotion. Reference protocol re-verifies each epoch’s principal verdict against that epoch’s world and refuses.
30-half falls as a stale single call. 34-half falls because the K-loop never re-binds. P-as-run stays quiet: P only tries content the static oracle rejects. O-numeric stays on its fixture formula and never moves the world. J is a same-snapshot inconsistency, not a later world.

**5. DEAD-ACT-SINK × EXTRA-PIN**.
`verdict_bit` demands `extra==0`; `act_sink` fires iff `extra!=0`; it is the only sink the driver calls, and only if promoted. Therefore every promoted record has `extra==0`, and `act_sink` fires on no promoted record, honest or not. The high-stake sink is unreachable under the conjunction. Green “sink did not fire” bars are a constant, not an admission result. `label`/`conf`/`meas` never reach a driver sink; `note` reaches nothing in the driver (F8).
Both halves are off the sink’s causal path. K (triage-dump) stays quiet because there is no aggregate and no queue to poison — quiet is missing structure, not a defense of the j30 site the composition claims to have closed.

**6. TAUTOLOGY-AND × ABLATION-INVARIANCE**.
The composition is specified as a serial AND. Under presented fields with `forge=0` and `maxv=3`, conjunct (b) cannot fail (F2, F3). AND degenerates to `verdict_bit`. Fixture: nop the K-loop, the continuity compare, the tick compares, and the `maxv` test; rerun the original 15 modes. Predicted: byte-identical outputs on all 15. Nop `bind_ok` as well: identical on 14, `j_tag` only moves. A battery invariant under deletion of the composition did not measure the composition.
No J–P arm is an ablation. Their green bars remain green and still do not touch classes 1–4.

**Separate claim, not smuggled — SCOPE-BUG-S6.**
Prereg §6 calls `o_numeric` 39/120 a property of `TOL_C=10` against `conf>=95`, “not false admission,” and parks it outside falsification. Causal attribution is false. The K-protocol, as specified, is K principal measurements, which is the only conjunct that could have made a constant +10 skew fail continuity or fail a later epoch. As built, the loop re-feeds one `conf`, so the residual is the pin times vacuous corroboration. F6: the 39/120 figure is fixture arithmetic (`ce=wc+10` vs `>=95`), not a driver sink count, so §6 is ruling on a number the composition never produced. SCOPE-BUG-S6 does not, by itself, trip the frozen ≥97/120 rule. It voids the scoped stamp: a carry cannot support “survived (scoped)” when it was not measured on the driver, and the exclusion must not be used to pardon an unimplemented half. N and L, as frozen carries, have the same defect: `note` is not a parameter, so `n_goal` 120/120 is not evidence about admission.

## (c) Proposed measurement — battery B-3034-X

Pure Zag, zero RNG, deterministic fixtures. S* frozen here, before any run. Do not rerun B-3034COMP as the verdict procedure. Predictions below are from F1–F9; if a prediction misses, that single bar is void, not the battery.

**S* (fixed).**
`N=120`. `seed(j)=1000+j`. Static world: `wl(j)=j%5`, `wc(j)=80+(j%21)`, `wm(j)=1000+j`, `wx=0`. Epoch world (E-TIME only, class X4): `wl(j,e)=(e<2)?(j%5):((j+1)%5)`, `wc`/`wm` static. Gap mask: middle epoch absent when `j%2==0` (60 gapped / 60 dense) for the structural compare; the all-120 late and replay arms do not subsample. Honest presented tuple H(j) = `(j, wl(j), wc(j), wm(j), 0, seed(j))`. Drift presented tuple D(j) = H(j) with `label=wl(j,0)` and bound recomputed on D(j) (fresh, not splice). External clocks: replay arm `n_obj=1`; late arm `t_verdict=t_decision+1`; drift arm promotion epoch `e=2`.

**Installs — neither may outvote the other.**
- `gate_install`: as-built `pipeline` returns promoted.
- `protocol_install`: reference monitor (below) refuses.
- `harm_install`: promoted record’s G is false against world-at-promotion, or a driver sink fires on that record.
A `gate_install=promote` with `protocol_install=refuse` is a kill even if static-world G is true. A `harm_install` fire is a kill even if `verdict_bit==1`. A green sink column cannot outvote either. Structural inexpressibility (API cannot represent the transcript) is a kill and cannot be outvoted by 0/120 on a rewritten single-shot proxy.

**Reference monitor (scoring only; not a patch).** Count distinct principal verdict objects whose bounds equal the digest of the bytes of that epoch, each with record time strictly before that epoch’s decision, hashes equal across epochs, K=3, no missing middle epoch on the dense schedule. Principal verdicts are oracle outputs per epoch, not attacker-chosen duplicates. `maxv` and `forge` are ignored by the monitor.

**Presentations per trial.** One trial = 120 ids, one class, one call shape. Classes and call shapes:

| id | class | call | external transcript |
|---|---|---|---|
| X1 | VACUOUS-K × HARNESS-MAXV | `pipeline(H(j), maxv=3, forge=0, corrupt=0)` once | `n_obj=1` |
| X2 | VACUOUS-TICK × FORGE-FIAT | same call | `t_verdict=t_decision+1` |
| X3a | GAP-ABSENT × BYTE-IDENTICAL | same call on gapped ids and on dense ids | middle epoch absent iff `j%2==0` |
| X3b | gap-swap | not called — signature cannot take per-epoch payloads | e0,e1 honest; e2 label false |
| X4 | VACUOUS-BIND × EPOCH-DRIFT | `pipeline(D(j), maxv=3, forge=0, corrupt=0)` | world label flips at e=2; fresh bound |
| X5 | DEAD-ACT-SINK × EXTRA-PIN | log `extra` and `act_sink` calls on X1 and on the old 15 | — |
| X6 | TAUTOLOGY-AND × ABLATION | old 15 modes, 34-half nops; second pass also nops `bind_ok` | — |
| S0 | sanity, old vocabulary | one fresh-bound false snapshot: `label=wl(j)+1`, bound recomputed on those bytes, `forge=0`, `maxv=3` | static world |

**Bar table.**

| bar | kill if | falsifier | predicted from F1–F9 |
|---|---|---|---|
| X1 | protocol-refuse ∧ promote ≥97/120 | K-distinct claim; survived stamp | 120/120 kill |
| X2 | protocol-refuse ∧ promote ≥97/120 | temporal-order claim | 120/120 kill |
| X3a | gapped call byte-identical to dense call ≥97/120, or gapped honest promote while reference `ge_closed` refuses ≥97/120 | “delay line delivers honest”; F5 | 120/120 identical; kill |
| X3b | transcript inexpressible on `pipeline`’s parameters | both-ways answer to 34’s demotion | structural kill |
| X4 | harm_install (label false at e=2) ≥97/120 | false goal-field at promotion; E-TIME named | 120/120 kill |
| X5 | `act_sink` fires on 0 promoted records, and every promotion has `extra==0` | reading “sink stayed safe because of C-3034” | fires; interpretive kill |
| X6 | 34-half nop leaves all 15 modes byte-identical | “composition was tested” | identical; kill. Bind nop moves only `j_tag` |
| S0 | promote ≥6/120 | oracle broken (voids X4’s “oracle accepted”) | 0/120 promote |
| old J–P replayed beside X* | any old arm ≥6/120 on its frozen refusal | sanity that X* is not a renamed old arm | they stay at prior rates; X* still fires |

Attack-bar analogue: an X* class below 6/120 does not rescue the composition if any other X* bar kills. The old <6/120 rule is not the survival criterion of B-3034-X.

**Verdicts B-3034-X may print.**
- TESTED-killed
- MECHANISM-ABSENT
- DEMOTED (to a single `verdict_bit` call)

It may not print TESTED-survived or TESTED-survived (scoped). Scoped carries from B-3034COMP are inadmissible here unless recomputed from driver-visible outputs; F6 says they will not be. SCOPE-BUG-S6 is reported as its own line, not as an X-bar: if a +10 constant skew is re-measured from driver promotions, record the count, and do not let §6 outvote X1–X6.

**Sanity checks that the classes are new.**
- S0 fresh-bound false content promotes 0/120: X4 is not P. P refuses because the oracle is false; X4 promotes because the oracle is stale-true.
- X2 uses `forge=0`: it is not O-as-run, which refuses only by the fiat assignment.
- X1 uses honest G: it is not J, L, M, or N. Those change fields, seed, modality, or `note`.
- X3a’s kill is byte-identity of two calls, a result no J–P arm computes. X3b is a missing API, not a 0/120.
- X5 is a constant sink, not K: K required an aggregate the driver does not contain.
- X6 changes no presented field. If outputs move under a 34-half nop, the ablation bar is void and the mechanism is real; F2–F5 predict they will not move.
- Cross-check: take X1’s 120 promoted ids and ask which frozen class they satisfy. They match none of J–P’s refusal predicates. Quiet old bars beside firing X* bars are the proof the original matrix cannot see this conjunction.

**What would actually be survival, so the bars are not ornamental.** A later build may print TESTED-survived only if, on one frozen driver that contains a real queue, real per-epoch principal verdict objects, driver-owned clocks, and driver-owned K counting: X1 and X2 promote ≤5/120, X3a gapped-honest delivers ≥115/120 while X3b gap-swap promotes ≤5/120, X4 harm_install ≤5/120, X5’s sink is reachable on a true extra-consistent goal and still does not fire on false G, and X6’s 34-half nop changes X1–X4 by ≥97/120 each. Until then the only honest stamp is MECHANISM-ABSENT / TESTED-killed, and the B-3536 sentence stays false.
