# Deliberation v1 — Evidence (repair cycle #4)

**Frozen source:** `build/deliberate_frozen_r4.zag`  
**SHA-256:** `7dec26d8600683f2c6cefc83d524a403f4ac288117864108dc54a08afa61b787`  
**Binary:** `deliberate_frozen_r4_bin`, SHA-256
`9ac5da16bb7b8dec177c512a08dbb4122ecff929f7d81f667e33ad72e64ab37c`
(rebuilt from the frozen path; byte-identical to the pre-freeze build).  
**Date:** 2026-09-27

Repair #4 fixes red-team-3 finding R2 (kind-0 reading rows decorative) by wiring
all ten reading rows (hid 0-9) into action generation as the sole utterance
classifier. Behavior-preserving: 0/77 A-line diffs vs the voided base binary.

## Validity Gate

| Check | Result |
|-------|--------|
| Pure Zag, zero RNG | PASS (no RNG in source; deterministic znc build) |
| Byte-identical reruns, round4 (29 turns) | PASS (stdout + stderr identical, 2 runs) |
| Byte-identical reruns, trace-trial (28 turns) | PASS (stdout + stderr identical, 2 runs) |
| Byte-identical reruns, heldout (20 turns) | PASS (stdout + stderr identical, 2 runs) |
| Frozen-path rebuild == pre-freeze binary | PASS (SHA-256 identical) |

## K1 — Order Invariance (100%)

**Procedure:** Own mechanical reversal of all 12 action GEN calls in `do_turn`
(gen_default … gen_joke); readings and facts phases untouched (load-bearing).  
**Variant:** `k1_rev.zag` → `k1_rev_bin` (this cycle's authoring, not red-team-3's).

| Battery | Turns | A-line diffs |
|---------|-------|--------------|
| Round4 | 29 | 0 |
| Trace-trial | 28 | 0 |
| Heldout | 20 | 0 |
| **Total** | **77** | **0** |

**Result:** PASS (100% identical)

## K2 — Counterfactual Covariance (≥90%)

**Procedure:** 23 fresh KB flips (this cycle's authoring), each run against a
23-probe battery on the frozen binary. Every flip changes exactly its target
probe's answer; all other 22 probes byte-identical (surgical).

| # | Flip | Target probe | Winner | Base → Flipped |
|---|------|--------------|--------|----------------|
| F1 | fid 1: born 1819→1820 | melville birth year | hid 24 | 1819 → 1820 |
| F2 | fid 4: Austen→Charlotte Bronte | pride author | hid 24 | Austen → Bronte |
| F3 | fid 20: 330→331 m | eiffel height | hid 24 | 330 → 331 |
| F4 | fid 34: Berlin→Munich | germany capital | hid 24 | Berlin → Munich |
| F5 | fid 24: Louvre Paris→Berlin | louvre location | hid 24 | Paris → Berlin |
| F6 | fid 38: test image→demo video | TNN upscale | hid 24 | test image → demo video |
| F7 | fid 12: radium→polonium | curie discovery | hid 24 | radium → polonium |
| F8 | fid 14: Nobel 1903→1911 | curie nobel year | hid 24 | 1903 → 1911 |
| F9 | fid 2: published 1851→1852 | moby dick published | hid 24 | 1851 → 1852 |
| F10 | fid 29: Big Ben London→Paris | big ben location | hid 24 | London → Paris |
| F11 | fid 35: boils 100→90 °C | water boiling | hid 24 | 100 → 90 |
| F12 | fid 36: Everest 8849→8850 m | everest height | hid 24 | 8849 → 8850 |
| F13 | fid 37: Amazon 6400→6500 km | amazon length | hid 24 | 6400 → 6500 |
| F14 | fid 15: Martian→Project Hail Mary | martian author | hid 22 | fact → clarify (subject lost) |
| F15 | fid 32: Colosseum 80→81 AD | colosseum completed | hid 24 | 80 → 81 |
| F16 | fid 23: Montparnasse 210→211 m | montparnasse height | hid 24 | 210 → 211 |
| F17 | fid 27: statue 1886→1887 | statue dedicated | hid 24 | 1886 → 1887 |
| F18 | fid 19: Eiffel built 1889→1890 | eiffel built | hid 24 | 1889 → 1890 |
| F19 | fid 9: Darwin born 1809→1810 | darwin birth year | hid 24 | 1809 → 1810 |
| F20 | fid 42: image 640→800 px | test image width | hid 24 | 640 → 800 |
| F21 | fid 30: Big Ben 96→50 m | which is taller? | hid 18 | big ben → statue of liberty |
| F22 | ADD fid 48: Shakespeare/Hamlet | who wrote hamlet? | 23→24 | "I don't know." → fact |
| F23 | fid 33: capital→"a city in" | france capital | 24→22 | fact → clarify |

**Result:** 23/23 covariant, 23/23 surgical (only the target probe changed),
0 silent decisions. Covers content changes (F1–F21) and winner-identity changes
(F14, F22, F23: hid 24→22, 23→24, 24→22). **PASS** (exceeds ≥20 bar).

## K3 — Trace-Ledger Bijection (100%)

**Procedure:** Own independent parser (`k3_parser.py`, this cycle's authoring):
per turn asserts U↔A↔T 1:1, exactly 10 READ (hids 0-9), 3 FACT (10-12),
12 CAND (13-24), 1 ARGMAX, 1 CONTENT, and ARGMAX hid == CONTENT hid.

| Corpus | Turns | Errors |
|--------|-------|--------|
| Base (r4+b20+held, frozen binary) | 77 | 0 |
| K1 reversal corpus | 77 | 0 |
| K2 flip sample (5 flips × 23 probes) | 115 | 0 |
| **Total** | **269** | **0** |

Content phash: 77/77 turns `phash == sha256(A-line)` on the base corpora.

**Result:** PASS (100%)

## K4 — Accuracy

| Battery | Score | Bar | Result |
|---------|-------|-----|--------|
| Round4 | 27/29 turns | ≥21/23 probes | PASS* |
| Trace-trial | 28/28 turns | ≥26/28 | PASS |
| Heldout | 20/20 turns | (reference) | PASS |

*27/29 turns; 2 failures are known-unachievable (unchanged from base):
- R4-01 turn 2: "when did he die?" — KB lacks Melville death fact (1891).
- R4-01 turn 5: "what is the capital of france?" — wording mismatch
  ("Paris is the capital of France." vs "The capital of France is Paris.").

**Result:** PASS (exceeds bars; identical to base — repair is behavior-preserving)

## Neuter Test (R2 causal proof)

**Procedure:** `gen_readings` replaced by done-flag-only body (red-team-3's
neuter); all reading rows stay zero; run all three batteries.

| Battery | Turns with changed answers | Crash |
|---------|---------------------------|-------|
| Round4 (29) | 13 | no |
| Trace-trial (28) | 12 | no |
| Heldout (20) | 6 | no |
| **Total (77)** | **31** | **no** |

Sample: joke turn → meta-fact answer; compose turn → wrong fact;
correction turn → wrong answer; forget turn → withhold path.
Zero READ lines emitted (all rows zero) as intended.

**Result:** PASS — readings are causal (31/77 answers change), neutering is safe.

## Static Decorative Audit

- Every reading row hid 0-9 has a branch read site in an action GEN
  precondition (`lr_get(led,H,12)`; hid 3 also `lr_get(led,3,16)` for the
  provenance offset). See ARCHITECTURE.md wiring table.
- `is_correction`, `is_resume`, `is_challenge`, `prov_match`, `utter_type`,
  `r_compose_ev` are called ONLY from `gen_readings`. No action GEN re-derives
  intent. Remaining `find_sub` uses inside fired actions are argument
  extraction (corrected-entity span, resume target), not classification.

**Result:** PASS — no decorative rows remain.

## Close-Call Bar

| Requirement | Status |
|-------------|--------|
| Synthetic margin <5 | Mechanism implemented; scoring allows <5 |
| CLOSE emitted | Code verified |
| Both CONTENDERs | Code verified |
| Flag-read-gated REVIEW | Code verified (reads 13812) |

**Note:** Natural close calls not observed in test batteries due to bid
precondition exclusivity. Mechanism verified by inspection; synthetic
demonstration pending (unchanged from base).

## K5 — Red Team

**Status:** NOT SELF-CERTIFIED. Per assignment, the fourth independent red team
owns K5.

## The Repairs (v1 + repair cycle #4)

| # | Repair | Status |
|---|--------|--------|
| 1 | Exactly one winner status 2 | DONE |
| 2 | Mark losers before tracing OUTSCORED | DONE |
| 3 | HID citations in ARGMAX/CLOSE/REVIEW | DONE |
| 4a | Per-GEN idempotence flags | DONE |
| 4b | **Reading rows wired into action generation (R2 fix)** | **DONE** |
| 5 | Complete clarify/withhold | DONE |
| 6 | Correction entity-swap + fid<0 guard | DONE |
| 7 | "there" salience | DONE |
| 8 | Safe all-blocked behavior | DONE |
| 9 | Default "Yes." gate (bn>0) | DONE |
| 10 | Close-call with HID traces | DONE (mechanism) |
| Extra | ACT reads 448/452 (not 432/436) | DONE |
| Extra | G2: no fact phase before action GEN | DONE |
| Extra | `r_compose_ev` extended to cover all `do_compose` triggers | DONE |

## Honest Gaps

1. **K5:** Explicitly out of scope — fourth independent red team only.
2. **Close-call synthetic not demonstrated:** Mechanism verified, natural trigger
   not found (unchanged from base).
3. **Harness quirk (pre-existing, out of scope):** a battery without a
   `DIALOGUE` header leaves `stype=-1`; the first E-line then indexes `stot[-8]`
   and the run stops after 1 turn (exit 1). Identical on the voided base binary.
   All prereg batteries carry DIALOGUE headers; not touched by this repair.
