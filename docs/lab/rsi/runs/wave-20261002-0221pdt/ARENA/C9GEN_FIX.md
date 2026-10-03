# C9GEN_FIX.md: C9 World Generator Fix Validation

Wave: wave-20261002-0221pdt | Lane: ARENA | Date: 2026-10-02
Prereg: PREREG_C9GENFIX.md (committed alone as 2ec987e84)
Implementation: world_gen_c9fix.zag, c9fix_check.zag (pure Zag)

## Summary

The C9FIX implementation correctly addresses defects D1-D4 per the frozen
prereg F1-F6. The generator builds, runs deterministically, and produces
valid C9 worlds. However, validation is PARTIAL: the frozen G4 order
criterion ("true chain not always listed first") is not satisfied because
the frozen seed (71503461337030) yields coin flip bits 1,1,1 (true first
in all 3 items). This is a prereg seed inconsistency, not an implementation
defect.

## Build

- world_gen_c9fix.zag -> bin/world_gen_c9fix: BUILD-PASS (znc exit 0)
- c9fix_check.zag -> bin/c9fix_check: BUILD-PASS (znc exit 0)
- Toolchain: safebin PATH, `which python3` and `which python` return nothing.
  Pure Zag only.

## Validation Results (per PREREG_C9GENFIX.md)

### G1 (determinism): PASS
3/3 runs of world_gen_c9fix with the frozen seed produce byte-identical
outputs. Verified via sha256sum:
- battery.json: 16d29e6b507adf75acbe2565858b3a1d6f85f3a57d0a4414f171f467b1158e3e (3/3 match)
- answer_key.json: 837ada765fbd849655a4038cf6634e4837a4133be2b4a631989ac64d53196d10 (3/3 match)
- turns.jsonl: 2c7880f5bb9727fb392197b9b347931be957de0a3da30da7562fad62477515eb (3/3 match)
Each run: 291 turns, 68 items.

### G2 (defect D1 fixed): PASS
- 12 {"t":"c"} observation turns present.
- At least one observation with variable disagreement (obs_disagree=1):
  noise is present via per-edge flip p=0.05.
- CHECK 1 (x==y==z enforcement) is REMOVED from the source. Only mentions
  are in comments documenting the removal.

### G3 (defect D2 fixed): PASS
- Exactly 80 {"t":"do"} and 80 {"t":"do_out"} expo turns.
- 40 do(X) and 40 do(Z), each do_out immediately follows its do turn.
- The intervened variable is fixed to the do val in every pair
  (verified by c9fix_check: pairfail=0).

### G4 (defect D3 fixed): PARTIAL
- The 3 C9 keys are full chain strings ("X->Z->Y", length 7): PASS.
- The old format exploit (first candidate, first variable) scores 0/3: PASS.
  (A single-variable reply can never match a full-chain key.)
- The true chain is not always listed first: FAIL.
  The frozen seed yields rng_bit=1,1,1 at the three coin flip positions,
  so the true chain is listed first in all 3 items:
  - item 0: q=discrim|X->Z->Y|X->Y->Z key=X->Z->Y (true first)
  - item 1: q=discrim|X->Z->Y|Y->X->Z key=X->Z->Y (true first)
  - item 2: q=discrim|X->Z->Y|Y->Z->X key=X->Z->Y (true first)
  true_listed_first=3/3.
  This means the "pick first candidate" strategy scores 3/3 on this battery.
  The implementation correctly follows prereg F4 (rng_bit per item, heads(1)
  = true first per the explicit prereg mapping). The failure is a prereg
  seed inconsistency: the frozen seed does not satisfy the frozen G4 order
  criterion. This is an honest negative finding about the prereg, not the fix.

### G5 (honest recoverability): PASS
The c9fix_check tool implements the C9BAT two-stage interventional protocol
(HI=0.75, integer arithmetic, reads only the turn stream, never the key
except for comparison):
- doX y==v: 36/40, doZ y==v: 40/40 (Stage 1: Y is leaf)
- doX z==v: 37/40, doZ x==v: 23/40 (Stage 2a: X->Z->Y)
- inferred_chain=X->Z->Y, recovered=3/3 against answer_key.json.

### G6 (genericity): PASS
- world_gen_c9fix.zag contains zero full chain-string literals
  (grep for "X->Y->Z" etc. returns nothing).
- c9fix_check.zag contains zero chain-string literals in logic
  (one match is a code comment only).

### G7 (pure Zag): PASS
`which python3` and `which python` return nothing under the safebin PATH.
No Python was invoked. All computation in pure Zag.

### G8 (scope honesty): PASS
`git status` on docs/lab/research-lead/overnight-20260928/competitive_arena/
is clean. The frozen arena is untouched.

## Verdict

C9FIX VALIDATION: PARTIAL.

The implementation correctly fixes D1 (noise, CHECK 1 removed), D2 (80/80
interventions, properly paired), D3 (full-chain keys, old exploit 0/3), and
D4 (proofs rewritten). G1, G2, G3, G5, G6, G7, G8 all pass.

G4 fails solely on the order-randomization criterion: the frozen seed
produces 1,1,1, so the true chain is always listed first. The coin flip
mechanism (rng_bit, correct heads/tails mapping per prereg F4) is honestly
implemented; the seed is simply unlucky.

Recommendation: The C9FIX code is sound and should be retained. For a fully
validating battery, a future prereg should select a different seed (with the
G4 order criterion verified against that seed before freezing). The current
battery is usable for mechanism development but has a known order exploit.

## Artifacts

- world_gen_c9fix.zag: fixed generator source (pure Zag)
- bin/world_gen_c9fix: built binary
- c9fix_check.zag: validation tool source (pure Zag)
- bin/c9fix_check: built validator binary
- fixrun1/: validated world output (291 turns, 68 items)

## Queued Next

- Part A: PREREG_CAUSAL.md (C9 candidate mechanism), then implementation
  and sealed eval. Note: the Part A contestant must NOT rely on candidate
  order (it must infer the chain from interventions, not position).
- Part C: PREREG_ABSTENTION.md, then abstention test.
