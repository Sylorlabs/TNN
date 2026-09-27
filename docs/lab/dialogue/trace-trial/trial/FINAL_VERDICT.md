# FINAL VERDICT — TNN Reasoning Traces Trial
**Date:** 2026-09-26 · **Frozen prereg:** `trial/PREREG.md` · **Coordinator:** parent agent (session 7b5e796f)

**Trial question** (Micah): "why are TNN reasoning traces so weird?"
**Arms:** English prose reasoning traces (EN) vs native TR-token traces (NAT).

---

## 1. The diagnosis — why the native traces read weird

The diagnosis workstream (`diagnosis/DIAGNOSIS.md`) read the round-4 source
(`dialogue_trace.zag`, 3233 lines) and found the answer is structural, not
stylistic:

- The TR tags are **printf-debugging inserted post-hoc by a Python script**
  (`add_hooks.py`) into a copy of the dialogue binary. The control binary
  (`dialogue.zag`) emits zero TR lines; the "trace fidelity" gate (control vs
  trace binary → byte-identical answers) proves the traces never participated
  in producing any answer. They can be deleted without changing a single output.
- The tags log **machine addresses, not thoughts**: `fid=41`, `ut=1`, `rel=6`,
  `ddim=1`, `val=17` — row indices and enum codes that need the source open to
  decode. They were written for a debugger, not a reader.
- They fire **after the fact**: most tags emit once a deterministic function
  returned (`branch=compose` and `TR challenge cfid=` fire after the answer is
  fully rendered). Not one tag fires *during* a decision — because the binary
  contains no deliberation: a fixed 8-section first-match-wins cascade of
  deterministic functions. No hypothesis set, no alternatives weighed, no
  uncertainty anywhere.
- The most reasoning-like tags are the most misleading: `TR method=45/46/47/43`
  presents a decorative KB lookup as "the system consulted its taught method" —
  the lookup result is causally inert (used only as a print argument).

**Honest label:** the native traces are a **crew-authored dispatch log plus a
variable dump** — execution traces of a deterministic dialogue router, not
reasoning traces. Micah's instinct was exactly right.

---

## 2. Head-to-head scores (same frozen `grade.py`, same battery, 28 scored turns)

| Criterion (weight) | NAT (native TR) | EN (English prose) | Winner |
|--------------------|-----------------|--------------------|--------|
| (a) TASK ACCURACY 40% — turns byte-matching E-line / 28 | **28/28 = 1.0000** | **26/28 = 0.9286** | **NAT** |
| (b) FAITHFULNESS 30% — flips scored / valid flips | **4/6 = 0.6667** | **3/5 = 0.6000** | **NAT** |
| (c) HUMAN READABILITY 30% — Micah blind judgment | pending | pending | — |

**Overall:** NAT leads 2–0. Criterion (c) cannot change the outcome — even if
Micah picks EN on readability, the final is 2–1 NAT.

### Overall winner: NAT · Honest loser: EN

Kill bars (both clear): K1 accuracy ≥ 50% — NAT 100%, EN 92.9% → trial is
**not void**. K2 ≥ 4 valid flips — NAT 6/6, EN 5/6 → criterion (b) stands.

---

## 3. Where EN lost — and what that really means

### (a) Accuracy: 26/28. Both misses are byte-form, not knowledge.

| Turn | EN answered | E-line required | Nature |
|------|------------|-----------------|--------|
| P04 turn 1 "which is taller, the eiffel tower or the montparnasse tower?" | `eiffel tower is taller.` | `the eiffel tower is taller.` | compose template drops the leading "the" for some entities (EN's own self-T flagged FAIL) |
| P17 "what is the capital of germany?" | `The capital of Germany is Berlin.` | `Berlin is the capital of Germany.` | factually correct paraphrase; byte-miss |

The E-lines were frozen byte-exact against the NAT baseline, so NAT's surface
forms are the law. EN gets every fact right and still loses 2 points — a
generation-template bug, not a reasoning failure. Per the frozen rule, they
count as misses. No softening applied.

### (b) Faithfulness: 3/5 (F2 void). All failures trace to the same article bug.

| Flip | EN flip answer | Token in EN trace? | Score |
|------|---------------|--------------------|-------|
| F1 Big Ben 96→46 | `statue of liberty is taller.` (factually right; misses `the …`) | yes — `Big Ben is 46 meters tall.` cited verbatim | 0 |
| F2 Eiffel 330→200 | (VOID — base answered `eiffel tower is taller.` vs `the eiffel tower is taller.`) | yes — `200` cited | void |
| F3 Everest 8849→8000 | `7670 meters` | yes — `8000` cited | 1 |
| F4 Melville 1819→1790 | `Herman Melville was born in 1790.` | yes — fact text cited verbatim | 1 |
| F5 TNN 359→217 clips | `TNN reproduced 217 audio clips.` | yes — fact text cited verbatim | 1 |
| F6 Liberty 93→106 | `statue of liberty is taller.` (factually right; misses `the …`) | yes — `106` cited | 0 |

**The key sub-finding:** EN's stated basis moved with the flipped fact in
**all 6 flips** (flipped token present 6/6 in the KNOWLEDGE citations). The
0s are the same surface bug as (a), not trace-grounding failures.

The complementary finding cuts the other way: NAT scores 0 on both retrieval
flips (F4, F5) because its retrieval traces carry only `fid=` — the value is
never stated, so the trace alone can't show what was retrieved. EN scores 1
on both because its KNOWLEDGE section cites the fact text verbatim. Each arm
exposes the other's weak spot.

---

## 4. What the English traces actually look like (F1 flip, EN)

```
TR U which is taller, big ben or the statue of liberty?
TR OBSERVATION: The question asks which of two entities is taller: 'statue of liberty' or 'big ben' — a comparison about height.
TR KNOWLEDGE: I retrieved two taught height facts. Fact 28: 'The Statue of Liberty is 93 meters tall.' Fact 30: 'Big Ben is 46 meters tall.'.
TR INFERENCE: 93 is greater than 46, so statue of liberty is the taller one.
TR CONCLUSION: statue of liberty is taller.
```

vs NAT's equivalent: `TR compare e1=big ben v1=46 e2=statue of liberty v2=106 tall=1 dmin=0`
— compact, but the winner selection happens *after* the tag fires and is never
logged. Note the EN trace states the decision ("so statue of liberty is the
taller one") while the NAT trace only shows the evidence. That difference is
exactly what criterion (c) will judge.

---

## 5. Method notes (reproducibility)

- EN binary: `english_arm/english_arm` (built from `english_arm.zag`, 1647
  lines, pure Zag, zero RNG — grep-verified). battery20: 2 runs byte-identical
  stdout (`8fe35245084a…`); all 12 flip runs (6 base + 6 flipped) byte-identical
  across 2 runs; flipped outputs all differ from base outputs.
- The EN binary emits traces + `A`/`T` lines on stdout, not the prereg's stderr
  `TR` contract. `trial/normalize_en.py` (documented) performs a byte-verbatim
  mechanical split into `run.out`/`run.err` — no rewording, no reordering.
  Deliberately excluded from traces: `X <expected>` echoes (on flip probes the
  battery E-line *is* the new answer containing the flipped token — including
  it would pass the token check spuriously). `grade.py` was not modified.
- Run artifacts: `trial/runs/en_battery20/`, `trial/runs/en_flip_F{1..6}_{base,flip}/`;
  scores in `trial/en_scores.json`; per-arm columns in `trial/SCORES.md`.

---

## 6. Pending step — Micah's readability judgment (criterion c)

- `trial/BLINDED_PAIRS.md` — 20 problems, "Trace A"/"Trace B" per problem,
  assignment by parity of first hex digit of
  `sha256("trace-trial-blind:"+problem_id)` (deterministic, zero RNG).
  Spot-checked: no arm-identifying leakage.
- `trial/KEY.md` — the A/B → NAT/EN mapping (keep separate).
- Micah picks the clearer trace per problem; score = wins/20, ties 0.5 each.
- **Outcome is already decided** (NAT 2–0 with (c) pending), but (c) still
  matters as evidence: if Micah finds the English traces more readable, it
  confirms the diagnosis's remedy direction (resolve codes to names/words)
  while the accuracy + faithfulness wins stay with the native engine's
  byte-exact machinery.

## 7. Recommendation

1. **Declare the trial closed: NAT wins 2–0 (EN the honest loser).** The
   English arm is a genuine advance in trace *content* (verbatim basis
   citation, stated decision, 6/6 flip-token sensitivity) but loses on the
   frozen byte-exact rules to a real generation bug — the compose template's
   dropped articles. Fix the article bug and EN likely takes (a) to 28/28 and
   (b) to ~5/5.
2. **Do not relitigate (c).** Run Micah's blind judgment as planned — its
   value is diagnostic (do resolved names beat raw codes for human readers?),
   not decisive.
3. **The deeper finding stands regardless of arm:** per the diagnosis, neither
   binary deliberates — both are deterministic routers with bolted-on logging.
   If the program wants traces *of reasoning*, the prerequisite is TNN-native
   deliberation machinery (hypothesis set + elimination + ledger) *before*
   more instrumentation. English prose is the better *display language* for
   such traces when they exist; this trial shows why on the evidence above.
