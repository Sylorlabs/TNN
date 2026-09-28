# PILOT REPORT — Composition Battery Instrument Validation (2026-09-27)

**Scope:** validates the INSTRUMENT (generator, scorer, failure-mode
classifier), not TNN. Seven scripted reference agents with injected failure
modes. Pure Zag, zero RNG, byte-identical reruns (each mode run twice, `cmp`
clean on all 7).

**Build:** `pilot.zag` → pinned `znc_linux_x86_64_abed8aa1`, 38,405-byte
binary. One analyzer warning (`1*16` in `agent_retrieve` — cosmetic, kept).

**Generator fix during pilot:** first build's tokens produced accidental
palindromes (`"ana"`-type), making the P3 reflex probe insensitive (reflex
agent caught 4/8). Fixed with a quadratic term in `tokfill`
(`(97+(7i+13k+k*k)%26)`); prereg §4 documents the change. Rebuilt, re-ran.

## Results (second build)

| Mode | Mastery | Retrieval | Composition | Class of failures | Reflex |
|------|---------|-----------|-------------|-------------------|--------|
| ok (positive control) | 4/4 | 12/12 | **48/48** | — | 0/8 |
| nomaster | 0/4 | 0/12 | 0/48 | **A×48** | 0/8 |
| noretrieve | 4/4 | 0/12 | 0/48 | **B×48** | 0/8 |
| nocombine | 4/4 | 12/12 | 2/48 | **C×46** | 0/8 |
| interfere | 4/4 | 12/12 | 36/48 | **D×12** | 0/8 |
| reflex | 4/4 | 12/12 | 48/48 | — | **8/8** |
| null (chance) | 0/4 | 0/12 | 0/48 | A×48 | 0/8 |

Interference detail (P4): pairs (0,1), (2,1), (3,1) scored 0/4 while their
reverses scored 4/4, parts mastered in isolation → all 12 items reclassified
C→D. No other pair met the asymmetry criterion (no false D).

## Pilot kill bars

| Bar | Condition | Result |
|-----|-----------|--------|
| PK1 | REF-OK ≥ 0.90 combo accuracy | 48/48 = 1.00 — **PASS** |
| PK2 | NULL ≤ 0.10 | 0/48 = 0.00 — **PASS** |
| PK3 | ≥80% of each mode's failed items carry intended class | A 48/48, B 48/48, C 46/46, D 12/12 — **PASS** |
| PK4 | byte-identical reruns | 7/7 `cmp` clean — **PASS** |

## Honest notes

1. **Degenerate coincidences are real and handled:** nocombine (applies only
   the first rule) still scores 2/48. CORRECTION (red-team 2026-09-27): the
   original note blamed accidental palindromes/uniforms — wrong; the quadratic
   token term makes every token an isogram (0 palindromes/uniforms in the
   stream). The real mechanism, confirmed item-by-item: pairs (3,0)@input 52
   (`"ao"`) and (3,2)@input 60 (`"es"`) — length-2 inputs where DROPLAST yields
   a 1-char intermediate on which REVERSE/ROTLEFT are identity. Count (2/48)
   stands; explanation corrected. The classifier counts them correct, as the
   semantics demand — the instrument measures semantics, not intent.
2. **nomaster/null ace the reflex probe (0/8)** — trivially, since identity is
   the correct distractor answer. The P3 probe only bites agents that *act*;
   that is by design (it targets the harmful-COMBINE mechanism: uncritical
   application, not inaction).
3. **What the pilot does NOT show:** anything about TNN. The full battery
   (D1+D2 vs the real learner, cuing audit, K1–K6) is preregistered and
   **blocked on disk** (99% full at pilot time). Re-run command for auditors:
   `pilot <mode>` twice, `cmp` the outputs.

**Verdict: instrument VALIDATED — PK1–PK4 all pass. The battery discriminates
(a)/(b)/(c)/(d)/(c-r) as designed. Ready to run against the real learner when
disk headroom exists.**

## Post-red-team instrument repair (2026-09-27, same night)

The independent red team (`REDTEAM_REPORT.md`) confirmed PK1–PK4 and the
discrimination claim but demonstrated 3 latent implementation bugs, all now
repaired in `pilot.zag` (implementation repairs matching the frozen spec's
intent — no bar or design changes):

1. **B-items hardcoded `ok=0`:** composition output was never scored when
   retrieval failed. Fixed: scoring is now decoupled from classification —
   every item's output is compared, and SUMMARY reports `elig=X/Y`
   (accuracy over items where composition was actually attempted, i.e. not
   class A/B) alongside the raw 48-item count.
2. **P4 `nC=nC-4` count corruption:** reclassification assumed all 4 pair
   items were C (demonstrated `C=-4`, `C=-1` on red-team modes). Fixed:
   per-item class array; only items actually in C move to D; counts can no
   longer go negative (verified: no negative counts in any mode).
3. **D-gate missing retrieval requirement:** the gate could fire on a pair
   whose own retrieval failed. Fixed: D requires `retarr==1` for both the
   pair and its reverse.

Re-ran all 7 modes ×2 after repair: byte-identical reruns, PK1–PK4 still
pass, INTERF lines fire exactly on the 3 intended pairs, `elig` behaves
(0/0 for all-A/all-B modes, 48/48 for ok/reflex, 2/48 nocombine, 36/48
interfere). Note: ITEM TSV lines show pre-P4 classes; SUMMARY counts are
post-P4 (authoritative).

Deliberate pilot-vs-prereg deviation (documented, not hidden): the pilot
implements P0 as 6 probes at ≥5/6 over tok 6–11; the frozen prereg specifies
8 probes at ≥7/8 over tok 6–13. The full battery implements the prereg's
numbers (see AMENDMENT_PROPOSAL.md).
