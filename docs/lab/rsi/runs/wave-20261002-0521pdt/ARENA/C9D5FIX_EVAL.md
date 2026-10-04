# C9D5FIX_EVAL.md: C9 World Generator D5 Fix Validation

Wave: wave-20261002-0521pdt | Lane: ARENA | Date: 2026-10-02
Prereg: PREREG_C9D5FIX.md (committed alone as bc049ef67)
Implementation: world_gen_c9d5fix.zag, c9fix_check.zag (pure Zag)
Battery: fixrun2/ (frozen seed 71503461337030, unchanged)

## Verdict: GEN-PASS (G1 through G8 all PASS)

## Corrected diagnosis (owed to the 0221pdt C9GEN_FIX.md)

The 0221pdt G4 PARTIAL verdict stands (the turns-visible candidate
order was degenerate: true chain listed first in 3/3), but its
attributed cause is falsified by artifact evidence. The report
claimed "the frozen seed yields rng_bit=1,1,1". The validated
fixrun1/battery.json shows the actual seeded draws are 1,1,0
(item27 lists the alternative first). The turns.jsonl replay path
never consulted the coin flip at all: it rebuilt every C9 question
as `discrim|<true>|<alternative>` unconditionally (defect D5).
No seed was unlucky; the replay code ignored F4. This prereg's fix
addresses the actual defect, and the frozen seed is unchanged.

## Build

- world_gen_c9d5fix.zag -> bin/world_gen_c9d5fix: BUILD-PASS
  (znc exit 0; analyzer warnings are pre-existing notes also present
  for the base source).
  Binary sha256:
  7b50a9c138742b0c8ade1661bad7413a3790289f009a7adeae23fa80124ca381
- c9fix_check.zag (0221pdt committed source, sha256
  8cd797144827bac65fdee76d46b2c34ca53c6f2ce499ceb4d32d44a87df8a183)
  -> bin/c9fix_check: BUILD-PASS.
  Binary sha256:
  a2688369b9503f04ff0906c3161bf1b56c92262dc9d3bbf45513d4936f685240
- Base source sha256 verified before editing:
  edc7215213fff34f72a81350160d0f283d96e3305c1b177f308de14f38abb502
- Diff against base confined to E1-E3 (dflip declaration, flip
  recording, flip-ordered replay construction). Seed literal
  untouched.

## Validation results (per PREREG_C9D5FIX.md)

### G1 (determinism): PASS
3/3 generation runs produce byte-identical outputs:
- battery.json:
  16d29e6b507adf75acbe2565858b3a1d6f85f3a57d0a4414f171f467b1158e3e
  (3/3; identical to fixrun1, the battery path is unchanged)
- answer_key.json:
  837ada765fbd849655a4038cf6634e4837a4133be2b4a631989ac64d53196d10
  (3/3)
- turns.jsonl:
  4b774023dae4bea6d61c088afae5cd8de17304166fc7d5d08efef4a5f7718fc6
  (3/3; differs from fixrun1 only by the D5 fix, as intended)
- exposure.jsonl, exposure_tnn.jsonl, idmap.json: 3/3 identical
  (hashes recorded in lane notes).
Each run: 291 turns, 68 items.

### G2 (defect D1 still fixed): PASS
- 12 {"t":"c"} observation turns present.
- 1 observation with variable disagreement (obs_disagree=1):
  noise present via per-edge flip p=0.05 (at expectation:
  P(disagree) = 1-0.95^2 = 0.0975 per obs, expected ~1.17 of 12).
- CHECK 1 exactness absent from the fixed source (only E1-E3
  changed; the CHECK 1 removal from C9FIX is untouched).

### G3 (defect D2 still fixed): PASS
- Exactly 80 {"t":"do"} and 80 {"t":"do_out"} expo turns
  (40 do(X), 40 do(Z)), verified by c9fix_check.
- Pairing and intervention fixing verified by the check tool
  (same tool and protocol as the 0221pdt validation).

### G4 (defect D3 fixed and D5 fixed): PASS
- The 3 C9 keys are full chain strings ("X->Z->Y" x3).
- turns.jsonl C9 questions are now string-identical to
  battery.json C9 questions (D5 consistency):
  - item25: discrim|X->Z->Y|X->Y->Z (true first, flip=1)
  - item26: discrim|X->Z->Y|Y->X->Z (true first, flip=1)
  - item27: discrim|Y->Z->X|X->Z->Y (alternative first, flip=0)
- true_listed_first = 2/3 (criterion: <= 2). The frozen seed's
  actual draws (1,1,0) satisfy the order criterion with no seed
  change.
- The old format exploit (first candidate, first variable)
  scores 0/3.

### G5 (honest recoverability): PASS
c9fix_check (two-stage interventional protocol, HI=0.75, integer
arithmetic, reads only the turn stream):
- doX y==v: 36/40, doZ y==v: 40/40 (Stage 1: Y is leaf)
- doX z==v: 37/40, doZ x==v: 23/40 (Stage 2: X->Z->Y)
- inferred_chain=X->Z->Y, recovered=3/3 against answer_key.json.

### G6 (genericity): PASS
- grep for full chain-string literals in world_gen_c9d5fix.zag:
  zero hits.
- The diff against the base touches only E1-E3.
- dflip holds order bits only, never answers.

### G7 (pure Zag): PASS
`which python3` and `which python` return nothing under the
safebin PATH at lane start (NAMECHECK.md Step 0) and at lane end.
All computation in pure Zag; shell used only for file moves,
hashing, and process sequencing.

### G8 (scope honesty): PASS
`git status` on
docs/lab/research-lead/overnight-20260928/competitive_arena/ is
clean. The D5-fixed generator is a candidate instrument, not a
replacement for the frozen arena battery. No L3, substrate, or
canonical-score claim is made. Adoption is a future governance
decision.

## Artifacts

- world_gen_c9d5fix.zag: D5-fixed generator source (pure Zag)
- bin/world_gen_c9d5fix, bin/c9fix_check: built binaries
- c9fix_check.zag: check tool source (0221pdt committed source)
- fixrun2/: validated world output (291 turns, 68 items)

## Queued next

- C9 causal contestant sealed eval (frozen PREREG_CAUSAL from
  0221pdt) on fixrun1, with supplementary exploratory runs on
  fixrun2 (the D5-fixed world exercises the order-randomized
  item27 end to end).
- Bare-prompt abstention test (frozen PREREG_ABSTENTION).
- C8/C12 surface-transfer prereg on fixrun2.
