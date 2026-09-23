# INDEPENDENT BATTERY V2 — CALIBRATION (v1 data, v2 scoring)

determinism_5x: PASS (validity tier)

## truth (cleaned, wire-decidable only)
strata: REJ-P 2/2 | AFF-T 4/4 | ENT-P 0/1
learner: 6/7 = 0.8571 (SE 0.1323)
mirror (perfect copier): 0.7143
margin: 1 item(s), +0.1429 (+1.08 SE)
KB-TRUTH(v2): HOLD (FRAGILE — margin 1 item(s), v2 minimum n=16, this axis n=7)

## truth / ABS-C (C-undecidable, ABSTAIN-expected) — NEW in v2
abstain rate: 0/3; learner outputs: {138: 'REJECT', 139: 'REJECT', 142: 'REJECT'}
finding: GUESS-ON-UNDECIDABLE vice — reject-on-conflict policy, picks sides instead of abstaining

## floor (smooth lies — unscored, honest boundary)
rejected: 0/2; learner affirmed both (pure mirroring, irreducible from the wire)
no kill bar (a bar here would demand psychic knowledge)

## contra / false (strata + grounded KB-GAP)
contra: 12/12 = 1.0000 (surface 8/8, d3-mediated 4/4)
  coupled 1.0000 [new-mechanisms 156/156] — comparability: SAME-CAPABILITY ok
  gap +0.0000, grounded threshold 0.1667 (= max(2*SE, 2/n)) -> KB-GAP(v2): HOLD (slack 0.1667)
false: 12/12 = 1.0000 (D3-violation 6/6, D4-violation 6/6)
  coupled 1.0000 [principle-detection 13/13] — comparability: SAME-CAPABILITY ok
  gap +0.0000, grounded threshold 0.1667 (= max(2*SE, 2/n)) -> KB-GAP(v2): HOLD (slack 0.1667)

## para (ABSOLUTE — INAUGURAL; R1 removed the 0.9649 comparison)
SYN (synonym-swap present): 1/12 = 0.0833
SYNT (pure syntactic, identical lexicon): 0 probes — UNMEASURED in v1 (all 12 v1 probes contain a verb synonym swap; the v1 'syntactic survives' claim is WITHDRAWN — the single hit, probe 125, contains conveyed/ferries)
no KB-GAP: no same-capability coupled headline exists (coupled-comparability rule)

## abstain: 12/12 = 1.0000 (unchanged under v2)
## prov: 12/12 = 1.0000 (unchanged under v2)

## validity tier
KB-DET: HOLD — 5/5 byte-identical
KB-NOLEAK: HOLD — v1 source/binary audit (harness never opens expected.json)
KB-PARSE: HOLD — 72/72 probes parsed, 0 silent drops
